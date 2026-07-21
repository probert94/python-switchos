"""Generate compatibility report showing field coverage across devices.

This tool generates a markdown report documenting field coverage for python-switchos
endpoints across all device/version combinations in the analysis data.

Usage:
    python3 -m tests.tools.compatibility_report
    python3 -m tests.tools.compatibility_report --output report.md
"""

import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Tuple

from tests.tools.compare_fields import (
    ALL_ENDPOINT_CLASSES,
    extract_field_ids,
    find_devices_with_endpoint,
    load_analysis_data,
)


# Endpoints not yet implemented (deferred to future phases)
DEFERRED_ENDPOINTS = {"dco.b", "ups.b", "poeoutports.b"}


def get_all_endpoints(analysis_data: List[dict]) -> Set[str]:
    """Get set of all endpoints across all devices."""
    endpoints = set()
    for entry in analysis_data:
        endpoints.update(entry.get("endpoints", []))
    return endpoints


def count_devices_by_type(analysis_data: List[dict]) -> Tuple[int, int, int, int]:
    """Count devices by firmware type.

    Returns:
        (swos_full_count, swos_lite_count, swos_full_models, swos_lite_models)
    """
    swos_full = [e for e in analysis_data if e.get("fw_type") == "swos"]
    swos_lite = [e for e in analysis_data if e.get("fw_type") == "swos-lite"]
    swos_full_models = len(set(e.get("model") for e in swos_full))
    swos_lite_models = len(set(e.get("model") for e in swos_lite))
    return len(swos_full), len(swos_lite), swos_full_models, swos_lite_models


def endpoint_coverage_table(analysis_data: List[dict]) -> str:
    """Generate endpoint coverage table.

    Shows which endpoints are available on SwOS full vs SwOS Lite devices.
    """
    lines = ["| Endpoint | SwOS Full | SwOS Lite | Total |"]
    lines.append("|----------|-----------|-----------|-------|")

    swos_full = [e for e in analysis_data if e.get("fw_type") == "swos"]
    swos_lite = [e for e in analysis_data if e.get("fw_type") == "swos-lite"]

    # Get all endpoints
    all_endpoints = get_all_endpoints(analysis_data)

    for endpoint in sorted(all_endpoints):
        full_count = len([e for e in swos_full if endpoint in e.get("endpoints", [])])
        lite_count = len([e for e in swos_lite if endpoint in e.get("endpoints", [])])
        total = full_count + lite_count

        # Mark implemented vs deferred
        if endpoint in ALL_ENDPOINT_CLASSES:
            status = ""
        elif endpoint in DEFERRED_ENDPOINTS:
            status = " (deferred)"
        else:
            status = " (?)"

        lines.append(f"| {endpoint}{status} | {full_count}/{len(swos_full)} | {lite_count}/{len(swos_lite)} | {total}/{len(analysis_data)} |")

    return "\n".join(lines)


def field_coverage_section(endpoint_path: str, analysis_data: List[dict]) -> str:
    """Generate field coverage section for a specific endpoint.

    Shows which fields are available in the dataclass and their device coverage.
    """
    if endpoint_path not in ALL_ENDPOINT_CLASSES:
        return ""

    endpoint_class = ALL_ENDPOINT_CLASSES[endpoint_path]
    dataclass_fields = extract_field_ids(endpoint_class)

    devices = find_devices_with_endpoint(analysis_data, endpoint_path)
    device_count = len(devices)

    if device_count == 0:
        return f"\n### {endpoint_path}\n\nNo devices found with this endpoint.\n"

    lines = [f"\n### {endpoint_path} ({endpoint_class.__name__})"]
    lines.append(f"\nDevices: {device_count}")
    lines.append("")
    lines.append("| Field ID | Coverage | Notes |")
    lines.append("|----------|----------|-------|")

    # Note: Analysis data has flat fields dict, not per-endpoint
    # We can only show if field exists somewhere in the firmware
    for fid in sorted(dataclass_fields):
        # Count how many devices have this field in their fields dict
        count = 0
        for device in devices:
            if fid in device.get("fields", {}):
                count += 1

        pct = (count / device_count * 100) if device_count > 0 else 0
        note = "-" if pct == 100 else "incomplete coverage"
        lines.append(f"| {fid} | {count}/{device_count} ({pct:.0f}%) | {note} |")

    return "\n".join(lines)


def device_variants_section(analysis_data: List[dict]) -> str:
    """Generate device variants section documenting SwOS vs SwOS Lite differences."""
    lines = ["## Device Variants"]
    lines.append("")
    lines.append("### SwOS Full vs SwOS Lite Key Differences")
    lines.append("")
    lines.append("| Aspect | SwOS Full | SwOS Lite |")
    lines.append("|--------|-----------|-----------|")
    lines.append("| Stats endpoint | stats.b (2.17+) or !stats.b (2.16) | !stats.b |")
    lines.append("| ACL stats | Not available | !aclstats.b |")
    lines.append("| LACP | lacp.b | Most don't have LACP |")
    lines.append("")

    # List models
    swos_full_models = sorted(set(e.get("model") for e in analysis_data if e.get("fw_type") == "swos"))
    swos_lite_models = sorted(set(e.get("model") for e in analysis_data if e.get("fw_type") == "swos-lite"))

    lines.append("### SwOS Full Models")
    lines.append("")
    lines.append(", ".join(swos_full_models))
    lines.append("")
    lines.append("### SwOS Lite Models")
    lines.append("")
    lines.append(", ".join(swos_lite_models))
    lines.append("")

    return "\n".join(lines)


def deferred_endpoints_section(analysis_data: List[dict]) -> str:
    """Generate section documenting deferred (not implemented) endpoints."""
    lines = ["## Deferred Endpoints"]
    lines.append("")
    lines.append("The following endpoints exist in firmware but are not yet implemented:")
    lines.append("")

    for endpoint in sorted(DEFERRED_ENDPOINTS):
        devices = find_devices_with_endpoint(analysis_data, endpoint)
        if devices:
            models = sorted(set(e.get("model") for e in devices))
            fw_types = sorted(set(e.get("fw_type") for e in devices))
            lines.append(f"- **{endpoint}** ({len(devices)} device configs, {', '.join(fw_types)})")
            lines.append(f"  - Models: {', '.join(models)}")
        else:
            lines.append(f"- **{endpoint}** (not found in any analyzed device)")

    lines.append("")
    return "\n".join(lines)


def generate_report(analysis_data: List[dict] = None) -> str:
    """Generate full compatibility report as markdown.

    Args:
        analysis_data: Optional pre-loaded analysis data. If None, loads from file.

    Returns:
        Markdown report as string
    """
    if analysis_data is None:
        analysis_data = load_analysis_data()

    # Calculate stats
    total_devices = len(analysis_data)
    swos_full, swos_lite, full_models, lite_models = count_devices_by_type(analysis_data)
    implemented_endpoints = len([ep for ep in ALL_ENDPOINT_CLASSES if ep != "stats.b"])  # Don't double-count alias

    # Build report
    lines = ["# Python-SwitchOS Compatibility Report"]
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("")

    # Summary section
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- **Device configurations analyzed**: {total_devices}")
    lines.append(f"  - SwOS Full: {swos_full} configs ({full_models} models)")
    lines.append(f"  - SwOS Lite: {swos_lite} configs ({lite_models} models)")
    lines.append(f"- **Implemented endpoints**: {implemented_endpoints}")
    lines.append(f"- **Deferred endpoints**: {len(DEFERRED_ENDPOINTS)}")
    lines.append("")

    # Endpoint coverage
    lines.append("## Endpoint Coverage")
    lines.append("")
    lines.append(endpoint_coverage_table(analysis_data))
    lines.append("")

    # Field coverage by endpoint
    lines.append("## Field Coverage by Endpoint")
    lines.append("")
    lines.append("Note: Analysis data contains a flat field dictionary per device firmware,")
    lines.append("not field-to-endpoint mappings. Coverage shows if field exists in firmware.")

    for endpoint_path in sorted(ALL_ENDPOINT_CLASSES.keys()):
        # Skip stats.b (it's an alias for !stats.b with same class)
        if endpoint_path == "stats.b":
            continue
        section = field_coverage_section(endpoint_path, analysis_data)
        if section:
            lines.append(section)

    lines.append("")

    # Device variants
    lines.append(device_variants_section(analysis_data))

    # Deferred endpoints
    lines.append(deferred_endpoints_section(analysis_data))

    return "\n".join(lines)


def main():
    """Run compatibility report generation."""
    parser = argparse.ArgumentParser(
        description="Generate compatibility report for python-switchos"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path (default: stdout)"
    )
    args = parser.parse_args()

    try:
        report = generate_report()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        print("Please ensure the mikrotik analysis data is available.")
        return 1

    if args.output:
        Path(args.output).write_text(report)
        print(f"Report written to {args.output}")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    exit(main())

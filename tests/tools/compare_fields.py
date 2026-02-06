"""Compare python-switchos dataclass fields against analysis data.

This tool extracts field IDs from endpoint dataclass metadata and cross-references
them against the all_analyses.json data from the mikrotik analysis project.

Usage:
    python3 -m tests.tools.compare_fields
"""

import json
from dataclasses import fields
from pathlib import Path
from typing import Dict, List, Set, Type

from python_switchos.endpoint import SwitchOSDataclass, SwitchOSEndpoint
from python_switchos.endpoints.acl import AclEndpoint, AclEntry, AclStatsEndpoint
from python_switchos.endpoints.fwd import ForwardingEndpoint
from python_switchos.endpoints.host import DynamicHostEndpoint, HostEndpoint, HostEntry
from python_switchos.endpoints.igmp import IgmpEndpoint, IgmpEntry
from python_switchos.endpoints.lacp import LacpEndpoint
from python_switchos.endpoints.link import LinkEndpoint
from python_switchos.endpoints.poe import PoEEndpoint
from python_switchos.endpoints.rstp import RstpEndpoint
from python_switchos.endpoints.sfp import SfpEndpoint
from python_switchos.endpoints.snmp import SnmpEndpoint
from python_switchos.endpoints.stats import StatsEndpoint
from python_switchos.endpoints.sys import SystemEndpoint
from python_switchos.endpoints.vlan import VlanEndpoint, VlanEntry


# Path to analysis data
ANALYSIS_PATH = Path("/ssd/source/mikrotik/analysis/all_analyses.json")

# Mapping of primary endpoint paths to their classes
# Note: Some endpoints use entry classes for list parsing
ENDPOINT_CLASSES: Dict[str, Type[SwitchOSEndpoint | SwitchOSDataclass]] = {
    "link.b": LinkEndpoint,
    "sys.b": SystemEndpoint,
    "sfp.b": SfpEndpoint,
    "snmp.b": SnmpEndpoint,
    "host.b": HostEntry,  # Uses entry class for field extraction
    "!dhost.b": HostEntry,  # Shares entry class with host.b
    "!igmp.b": IgmpEntry,  # Uses entry class
    "vlan.b": VlanEntry,  # Uses entry class
    "lacp.b": LacpEndpoint,
    "rstp.b": RstpEndpoint,
    "!stats.b": StatsEndpoint,
    "fwd.b": ForwardingEndpoint,
    "acl.b": AclEntry,  # Uses entry class
    "!aclstats.b": AclStatsEndpoint,
    "poe.b": PoEEndpoint,
}

# Alternate path mappings for endpoints with path variants
# SwOS Lite uses ! prefix, SwOS full 2.17+ uses non-prefixed paths
ENDPOINT_ALTERNATES: Dict[str, Type[SwitchOSEndpoint | SwitchOSDataclass]] = {
    "stats.b": StatsEndpoint,      # SwOS full 2.17+ uses stats.b
    "aclstats.b": AclStatsEndpoint,  # SwOS full uses aclstats.b
}

# Combined mapping of all paths (primary + alternates) to classes
ALL_ENDPOINT_CLASSES: Dict[str, Type[SwitchOSEndpoint | SwitchOSDataclass]] = {
    **ENDPOINT_CLASSES,
    **ENDPOINT_ALTERNATES,
}


def extract_field_ids(endpoint_class: Type[SwitchOSDataclass]) -> Set[str]:
    """Extract all field IDs (iXX format) from an endpoint dataclass's metadata.

    Args:
        endpoint_class: A dataclass type inheriting from SwitchOSDataclass

    Returns:
        Set of field IDs found in metadata (e.g., {"i01", "i0a", "i06"})
    """
    field_ids = set()
    for f in fields(endpoint_class):
        metadata = f.metadata
        # Get field names from metadata
        names = metadata.get("name", [])
        for name in names:
            # Filter for iXX format field IDs
            if name.startswith("i") and len(name) >= 2:
                field_ids.add(name)
        # Also check for high byte fields (uint64 type)
        high = metadata.get("high")
        if high and isinstance(high, str) and high.startswith("i"):
            field_ids.add(high)
        # Check for pair fields (bitshift_option type)
        pair = metadata.get("pair")
        if pair and isinstance(pair, str) and pair.startswith("i"):
            field_ids.add(pair)
    return field_ids


def load_analysis_data(path: Path = ANALYSIS_PATH) -> List[dict]:
    """Load the all_analyses.json file.

    Args:
        path: Path to the analysis JSON file

    Returns:
        List of device/version analysis entries
    """
    with open(path) as f:
        return json.load(f)


def get_device_fields(analysis_entry: dict) -> Set[str]:
    """Get all field IDs from a device analysis entry.

    Note: The analysis data has a flat `fields` dict, not per-endpoint.
    This returns ALL field IDs present in the device firmware.

    Args:
        analysis_entry: A single device/version entry from all_analyses.json

    Returns:
        Set of field IDs (e.g., {"i01", "i02", "i03"})
    """
    return set(analysis_entry.get("fields", {}).keys())


def find_devices_with_endpoint(analysis_data: List[dict], endpoint_path: str) -> List[dict]:
    """Find all device entries that have a specific endpoint.

    Args:
        analysis_data: Full list from all_analyses.json
        endpoint_path: Endpoint path to search for (e.g., "link.b")

    Returns:
        List of matching analysis entries
    """
    return [
        entry for entry in analysis_data
        if endpoint_path in entry.get("endpoints", [])
    ]


def compare_endpoint(endpoint_path: str, analysis_data: List[dict]) -> dict:
    """Compare dataclass fields against analysis data for an endpoint.

    Args:
        endpoint_path: Endpoint path (e.g., "link.b")
        analysis_data: Full list from all_analyses.json

    Returns:
        Dictionary with comparison results:
        {
            "endpoint": str,
            "dataclass_fields": set,
            "device_count": int,
            "field_coverage": {field_id: count of devices with this field}
        }
    """
    # Use ALL_ENDPOINT_CLASSES to handle both primary and alternate paths
    if endpoint_path not in ALL_ENDPOINT_CLASSES:
        return {
            "endpoint": endpoint_path,
            "error": f"No dataclass mapping for {endpoint_path}",
        }

    endpoint_class = ALL_ENDPOINT_CLASSES[endpoint_path]
    dataclass_fields = extract_field_ids(endpoint_class)

    # Find devices with this endpoint
    devices = find_devices_with_endpoint(analysis_data, endpoint_path)

    # Count how many devices have each field
    field_coverage: Dict[str, int] = {}
    all_device_fields: Set[str] = set()

    for device in devices:
        device_fields = get_device_fields(device)
        all_device_fields.update(device_fields)
        for fid in device_fields:
            field_coverage[fid] = field_coverage.get(fid, 0) + 1

    return {
        "endpoint": endpoint_path,
        "dataclass_fields": dataclass_fields,
        "device_count": len(devices),
        "field_coverage": field_coverage,
        "all_device_fields": all_device_fields,
    }


def main():
    """Run field comparison for all endpoints and print results."""
    print("Loading analysis data...")
    try:
        analysis_data = load_analysis_data()
    except FileNotFoundError:
        print(f"ERROR: Analysis file not found at {ANALYSIS_PATH}")
        print("Please ensure the mikrotik analysis data is available.")
        return

    print(f"Loaded {len(analysis_data)} device/version entries\n")

    # Process each endpoint
    for endpoint_path, endpoint_class in ENDPOINT_CLASSES.items():
        # Skip duplicate endpoint paths (e.g., stats.b is alias for !stats.b)
        if endpoint_path == "stats.b":
            continue

        result = compare_endpoint(endpoint_path, analysis_data)

        if "error" in result:
            print(f"=== {endpoint_path} ===")
            print(f"Error: {result['error']}\n")
            continue

        print(f"=== {endpoint_path} ===")
        print(f"Dataclass: {endpoint_class.__name__}")
        print(f"Dataclass fields: {', '.join(sorted(result['dataclass_fields']))}")
        print(f"Devices with endpoint: {result['device_count']}")

        if result["device_count"] == 0:
            print("No devices found with this endpoint.\n")
            continue

        # Show field coverage for dataclass fields
        print("\nField coverage (dataclass fields):")
        for fid in sorted(result["dataclass_fields"]):
            count = result["field_coverage"].get(fid, 0)
            pct = (count / result["device_count"] * 100) if result["device_count"] > 0 else 0
            status = "" if count == result["device_count"] else " *"
            print(f"  {fid}: {count}/{result['device_count']} devices ({pct:.0f}%){status}")

        # Fields in dataclass but not in any device
        missing_from_devices = result["dataclass_fields"] - result["all_device_fields"]
        if missing_from_devices:
            print(f"\nFields in dataclass but NOT in analysis data: {', '.join(sorted(missing_from_devices))}")

        print("\nNote: Field-to-endpoint mapping not in analysis data.")
        print("      Showing all fields present in device firmware.\n")


if __name__ == "__main__":
    main()

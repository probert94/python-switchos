import ast
import pytest
from pathlib import Path

FIXTURE_DIR = Path(__file__).parent / "fixtures"

# Map fixture parameter names to their endpoint directories
# Some endpoints have alternate paths (e.g., stats.b vs !stats.b)
_ENDPOINTS = {
    "acl": "acl_b",
    "aclstats": "!aclstats_b",
    "dhost": "!dhost_b",
    "fwd": "fwd_b",
    "host": "host_b",
    "igmp": "igmp_b",
    "lacp": "lacp_b",
    "link": "link_b",
    "poe": "poe_b",
    "rstp": "rstp_b",
    "sfp": "sfp_b",
    "stats": ["!stats_b", "stats_b"],  # SwOS Lite uses !stats.b, SwOS full 2.17+ uses stats.b
    "snmp": "snmp_b",
    "sys": "sys_b",
    "vlan": "vlan_b",
}


def discover_all_fixtures(endpoint_dir):
    """Discover fixtures across all device directories AND flat structure.

    Searches both:
    - fixtures/{endpoint_dir}/ (legacy flat structure)
    - fixtures/{device_version}/{endpoint_dir}/ (new device-based structure)

    Returns list of (response_text, expected_dict, fixture_id) tuples.
    """
    pairs = []

    # Legacy flat structure
    legacy_path = FIXTURE_DIR / endpoint_dir
    if legacy_path.exists() and legacy_path.is_dir():
        for response_file in sorted(legacy_path.glob("*_response_*.txt")):
            expected_file = response_file.with_suffix(".expected")
            response_text = response_file.read_text()
            expected_dict = None
            if expected_file.exists():
                expected_dict = ast.literal_eval(expected_file.read_text())
            pairs.append((response_text, expected_dict, response_file.stem))

    # New device-based structure
    for device_dir in sorted(FIXTURE_DIR.iterdir()):
        if not device_dir.is_dir():
            continue
        # Skip if it looks like an endpoint dir (contains _b or .b)
        if "_b" in device_dir.name or ".b" in device_dir.name:
            continue
        endpoint_path = device_dir / endpoint_dir
        if not endpoint_path.exists():
            continue
        for response_file in sorted(endpoint_path.glob("*_response_*.txt")):
            expected_file = response_file.with_suffix(".expected")
            response_text = response_file.read_text()
            expected_dict = None
            if expected_file.exists():
                expected_dict = ast.literal_eval(expected_file.read_text())
            # Include device in fixture ID for clarity
            fixture_id = f"{device_dir.name}/{response_file.stem}"
            pairs.append((response_text, expected_dict, fixture_id))

    return pairs


@pytest.fixture
def fixture_dir():
    """Return the path to the test fixtures directory."""
    return FIXTURE_DIR


def pytest_generate_tests(metafunc):
    """Auto-parametrize fixtures based on discovered response files."""
    for name, endpoint_dirs in _ENDPOINTS.items():
        response_param = f"{name}_response"
        expected_param = f"{name}_expected"
        has_response = response_param in metafunc.fixturenames
        has_expected = expected_param in metafunc.fixturenames
        if not has_response and not has_expected:
            continue
        # Handle both single directory and list of directories
        if isinstance(endpoint_dirs, str):
            endpoint_dirs = [endpoint_dirs]
        pairs = []
        for endpoint_dir in endpoint_dirs:
            pairs.extend(discover_all_fixtures(endpoint_dir))
        if not pairs:
            # Mark with skip so tests are collected but clearly indicate no fixtures
            if has_response and has_expected:
                metafunc.parametrize(
                    f"{response_param},{expected_param}",
                    [pytest.param(None, None, marks=pytest.mark.skip(
                        reason=f"No fixtures in {endpoint_dir}/"))],
                    ids=["no_fixtures"],
                    indirect=False,
                )
            elif has_response:
                metafunc.parametrize(
                    response_param,
                    [pytest.param(None, marks=pytest.mark.skip(
                        reason=f"No fixtures in {endpoint_dir}/"))],
                    ids=["no_fixtures"],
                    indirect=False,
                )
            continue
        if has_response and has_expected:
            metafunc.parametrize(
                f"{response_param},{expected_param}",
                [(r, e) for r, e, _ in pairs],
                ids=[fid for _, _, fid in pairs],
                indirect=False,
            )
        elif has_response:
            metafunc.parametrize(
                response_param,
                [r for r, _, _ in pairs],
                ids=[fid for _, _, fid in pairs],
                indirect=False,
            )

import ast
import pytest
from pathlib import Path

FIXTURE_DIR = Path(__file__).parent / "fixtures"

# Map fixture parameter names to their endpoint directories
_ENDPOINTS = {
    "link": "link_b",
    "sys": "sys_b",
    "poe": "poe_b",
}


def discover_fixtures(endpoint_dir):
    """Discover response/expected fixture pairs in an endpoint directory.

    Finds files matching *_response_*.txt and pairs each with its
    .expected file (Python dict literal). Returns list of
    (response_text, expected_dict, fixture_id) tuples.
    """
    path = FIXTURE_DIR / endpoint_dir
    if not path.exists():
        return []
    pairs = []
    for response_file in sorted(path.glob("*_response_*.txt")):
        expected_file = response_file.with_suffix(".expected")
        response_text = response_file.read_text()
        expected_dict = None
        if expected_file.exists():
            expected_dict = ast.literal_eval(expected_file.read_text())
        pairs.append((response_text, expected_dict, response_file.stem))
    return pairs


@pytest.fixture
def fixture_dir():
    """Return the path to the test fixtures directory."""
    return FIXTURE_DIR


def pytest_generate_tests(metafunc):
    """Auto-parametrize fixtures based on discovered response files."""
    for name, endpoint_dir in _ENDPOINTS.items():
        response_param = f"{name}_response"
        expected_param = f"{name}_expected"
        has_response = response_param in metafunc.fixturenames
        has_expected = expected_param in metafunc.fixturenames
        if not has_response and not has_expected:
            continue
        pairs = discover_fixtures(endpoint_dir)
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

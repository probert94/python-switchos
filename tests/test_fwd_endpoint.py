"""Tests for ForwardingEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/fwd_b/. Expected values
come from companion .expected files (Python dict literals).
"""

import pytest
from dataclasses import asdict
from python_switchos.endpoint import readDataclass
from python_switchos.endpoints.fwd import ForwardingEndpoint


# Boolean fields (18 total)
BOOL_FIELDS = [
    # Port isolation matrix (10)
    "from_port_1", "from_port_2", "from_port_3", "from_port_4", "from_port_5",
    "from_port_6", "from_port_7", "from_port_8", "from_port_9", "from_port_10",
    # Port lock (2)
    "port_lock", "lock_on_first",
    # Mirroring (3)
    "mirror_ingress", "mirror_egress", "mirror_to",
    # Flood/limit (2)
    "limit_unknown_unicast", "flood_unknown_multicast",
    # VLAN (1)
    "force_vlan_id",
]

# Integer fields (4 total)
INT_FIELDS = [
    "storm_rate", "ingress_rate", "egress_rate", "default_vlan_id",
]

# Option fields (2 total)
OPTION_FIELDS = [
    "vlan_mode", "vlan_receive",
]


class TestForwardingEndpointParsing:
    """Generic parsing tests that run against all fwd.b fixtures."""

    def test_parses_to_fwd_endpoint(self, fwd_response):
        result = readDataclass(ForwardingEndpoint, fwd_response)
        assert isinstance(result, ForwardingEndpoint)

    def test_bool_fields_are_bool_lists(self, fwd_response):
        result = readDataclass(ForwardingEndpoint, fwd_response)
        for field_name in BOOL_FIELDS:
            field_value = getattr(result, field_name)
            assert isinstance(field_value, list), f"{field_name} should be a list"
            assert len(field_value) > 0, f"{field_name} should not be empty"
            assert all(isinstance(v, bool) for v in field_value), (
                f"{field_name} values should be booleans"
            )

    def test_int_fields_are_int_lists(self, fwd_response):
        result = readDataclass(ForwardingEndpoint, fwd_response)
        for field_name in INT_FIELDS:
            field_value = getattr(result, field_name)
            assert isinstance(field_value, list), f"{field_name} should be a list"
            assert len(field_value) > 0, f"{field_name} should not be empty"
            assert all(isinstance(v, int) for v in field_value), (
                f"{field_name} values should be integers"
            )

    def test_option_fields_are_str_lists(self, fwd_response):
        result = readDataclass(ForwardingEndpoint, fwd_response)
        for field_name in OPTION_FIELDS:
            field_value = getattr(result, field_name)
            assert isinstance(field_value, list), f"{field_name} should be a list"
            assert len(field_value) > 0, f"{field_name} should not be empty"
            assert all(isinstance(v, str) for v in field_value), (
                f"{field_name} values should be strings"
            )

    def test_all_port_lists_same_length(self, fwd_response):
        """All per-port fields should have the same number of entries."""
        result = readDataclass(ForwardingEndpoint, fwd_response)
        all_fields = BOOL_FIELDS + INT_FIELDS + OPTION_FIELDS
        lengths = {len(getattr(result, f)) for f in all_fields}
        assert len(lengths) == 1, f"Inconsistent port counts: {lengths}"


class TestForwardingEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, fwd_response, fwd_expected):
        if fwd_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = asdict(readDataclass(ForwardingEndpoint, fwd_response))
        for field, expected in fwd_expected.items():
            assert result[field] == expected, (
                f"Field {field!r}: expected {expected!r}, got {result[field]!r}"
            )

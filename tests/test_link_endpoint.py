"""Tests for LinkEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/link_b/. Expected values
come from companion .expected files (Python dict literals).
"""

import pytest
from dataclasses import asdict
from typing import get_args
from python_switchos.endpoint import readDataclass
from python_switchos.endpoints.link import LinkEndpoint, LinkState, Speed


class TestLinkEndpointParsing:
    """Generic parsing tests that run against all link.b fixtures."""

    def test_parses_to_link_endpoint(self, link_response):
        result = readDataclass(LinkEndpoint, link_response)
        assert isinstance(result, LinkEndpoint)

    def test_enabled_is_bool_list(self, link_response):
        result = readDataclass(LinkEndpoint, link_response)
        assert isinstance(result.enabled, list)
        assert len(result.enabled) > 0
        assert all(isinstance(v, bool) for v in result.enabled)

    def test_name_is_str_list(self, link_response):
        result = readDataclass(LinkEndpoint, link_response)
        assert isinstance(result.name, list)
        assert all(isinstance(v, str) for v in result.name)
        assert all(len(v) > 0 for v in result.name)

    def test_auto_negotiation_is_bool_list(self, link_response):
        result = readDataclass(LinkEndpoint, link_response)
        assert isinstance(result.auto_negotiation, list)
        assert all(isinstance(v, bool) for v in result.auto_negotiation)

    def test_speed_values_are_valid(self, link_response):
        result = readDataclass(LinkEndpoint, link_response)
        assert isinstance(result.speed, list)
        valid = set(get_args(Speed)) | {None}
        assert all(v in valid for v in result.speed)

    def test_man_speed_values_are_valid(self, link_response):
        result = readDataclass(LinkEndpoint, link_response)
        assert isinstance(result.man_speed, list)
        valid = set(get_args(Speed)) | {None}
        assert all(v in valid for v in result.man_speed)

    def test_link_state_values_are_valid(self, link_response):
        result = readDataclass(LinkEndpoint, link_response)
        assert isinstance(result.link_state, list)
        valid = set(get_args(LinkState))
        assert all(v in valid for v in result.link_state)

    def test_full_duplex_is_bool_list(self, link_response):
        result = readDataclass(LinkEndpoint, link_response)
        assert isinstance(result.full_duplex, list)
        assert all(isinstance(v, bool) for v in result.full_duplex)

    def test_man_full_duplex_is_bool_list(self, link_response):
        result = readDataclass(LinkEndpoint, link_response)
        assert isinstance(result.man_full_duplex, list)
        assert all(isinstance(v, bool) for v in result.man_full_duplex)

    def test_flow_control_rx_is_bool_list(self, link_response):
        result = readDataclass(LinkEndpoint, link_response)
        assert isinstance(result.flow_control_rx, list)
        assert all(isinstance(v, bool) for v in result.flow_control_rx)

    def test_flow_control_tx_is_bool_list(self, link_response):
        result = readDataclass(LinkEndpoint, link_response)
        assert isinstance(result.flow_control_tx, list)
        assert all(isinstance(v, bool) for v in result.flow_control_tx)

    def test_all_port_lists_same_length(self, link_response):
        """All per-port fields should have the same number of entries."""
        result = readDataclass(LinkEndpoint, link_response)
        lengths = {
            len(result.enabled), len(result.name), len(result.speed),
            len(result.man_speed), len(result.link_state),
            len(result.full_duplex), len(result.man_full_duplex),
            len(result.auto_negotiation),
            len(result.flow_control_rx), len(result.flow_control_tx),
        }
        assert len(lengths) == 1, f"Inconsistent port counts: {lengths}"


class TestLinkEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, link_response, link_expected):
        if link_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = asdict(readDataclass(LinkEndpoint, link_response))
        for field, expected in link_expected.items():
            assert result[field] == expected, (
                f"Field {field!r}: expected {expected!r}, got {result[field]!r}"
            )


class TestLinkEndpointMissingFields:
    """Document fields present in engine.js link.b but missing from LinkEndpoint."""

    @pytest.mark.parametrize("field_id,field_name", [
        ("i0d", "hops"),
        ("i0e", "last_hop"),
        ("i0f", "length"),
        ("i10", "fault_at"),
        ("i11", "cable_pairs"),
        ("i13", "flow_control_status"),
        ("i14", "flow_control_status_high_bit"),
    ])
    def test_link_missing_fields(self, field_id, field_name):
        pytest.skip(
            f"MISSING: {field_name} ({field_id}) exists in engine.js link.b "
            f"but not in LinkEndpoint"
        )

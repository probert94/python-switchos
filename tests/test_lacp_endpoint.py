"""Tests for LacpEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/lacp_b/. Expected values
come from companion .expected files (Python dict literals).
"""

import pytest
from dataclasses import asdict
from typing import get_args
from python_switchos.endpoint import readDataclass
from python_switchos.endpoints.lacp import LacpEndpoint, LacpMode


class TestLacpEndpointParsing:
    """Generic parsing tests that run against all lacp.b fixtures."""

    def test_parses_to_lacp_endpoint(self, lacp_response):
        result = readDataclass(LacpEndpoint, lacp_response)
        assert isinstance(result, LacpEndpoint)

    def test_mode_is_str_list(self, lacp_response):
        result = readDataclass(LacpEndpoint, lacp_response)
        assert isinstance(result.mode, list)
        assert len(result.mode) > 0
        # mode values are strings (from Literal mapping)
        assert all(isinstance(v, str) or v is None for v in result.mode)

    def test_mode_values_are_valid(self, lacp_response):
        result = readDataclass(LacpEndpoint, lacp_response)
        valid = set(get_args(LacpMode)) | {None}
        assert all(v in valid for v in result.mode)

    def test_group_is_int_list(self, lacp_response):
        result = readDataclass(LacpEndpoint, lacp_response)
        assert isinstance(result.group, list)
        assert len(result.group) > 0
        assert all(isinstance(v, int) for v in result.group)

    def test_trunk_is_int_list(self, lacp_response):
        result = readDataclass(LacpEndpoint, lacp_response)
        assert isinstance(result.trunk, list)
        assert len(result.trunk) > 0
        assert all(isinstance(v, int) for v in result.trunk)

    def test_partner_is_str_list(self, lacp_response):
        result = readDataclass(LacpEndpoint, lacp_response)
        assert isinstance(result.partner, list)
        assert len(result.partner) > 0
        assert all(isinstance(v, str) for v in result.partner)

    def test_all_port_lists_same_length(self, lacp_response):
        """All per-port fields should have the same number of entries."""
        result = readDataclass(LacpEndpoint, lacp_response)
        lengths = {
            len(result.mode),
            len(result.group),
            len(result.trunk),
            len(result.partner),
        }
        assert len(lengths) == 1, f"Inconsistent port counts: {lengths}"


class TestLacpEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, lacp_response, lacp_expected):
        if lacp_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = asdict(readDataclass(LacpEndpoint, lacp_response))
        for field, expected in lacp_expected.items():
            assert result[field] == expected, (
                f"Field {field!r}: expected {expected!r}, got {result[field]!r}"
            )

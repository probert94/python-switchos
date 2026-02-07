"""Tests for RstpEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/rstp_b/. Expected values
come from companion .expected files (Python dict literals).
"""

import pytest
from dataclasses import asdict
from typing import get_args
from python_switchos.endpoint import readDataclass
from python_switchos.endpoints.rstp import RstpEndpoint, RstpMode, RstpRole, RstpState, RstpType


class TestRstpEndpointParsing:
    """Generic parsing tests that run against all rstp.b fixtures."""

    def test_parses_to_rstp_endpoint(self, rstp_response):
        result = readDataclass(RstpEndpoint, rstp_response)
        assert isinstance(result, RstpEndpoint)

    def test_rstp_is_bool_list(self, rstp_response):
        result = readDataclass(RstpEndpoint, rstp_response)
        assert isinstance(result.rstp, list)
        assert len(result.rstp) > 0
        assert all(isinstance(v, bool) for v in result.rstp)

    def test_mode_is_str_list(self, rstp_response):
        result = readDataclass(RstpEndpoint, rstp_response)
        assert isinstance(result.mode, list)
        assert len(result.mode) > 0
        assert all(isinstance(v, str) for v in result.mode)

    def test_mode_values_are_valid(self, rstp_response):
        result = readDataclass(RstpEndpoint, rstp_response)
        valid = set(get_args(RstpMode))
        assert all(v in valid for v in result.mode)

    def test_role_values_are_valid(self, rstp_response):
        result = readDataclass(RstpEndpoint, rstp_response)
        valid = set(get_args(RstpRole)) | {None}
        assert all(v in valid for v in result.role)

    def test_root_path_cost_is_int_list(self, rstp_response):
        result = readDataclass(RstpEndpoint, rstp_response)
        assert isinstance(result.root_path_cost, list)
        assert len(result.root_path_cost) > 0
        assert all(isinstance(v, int) for v in result.root_path_cost)

    def test_type_is_str_list(self, rstp_response):
        result = readDataclass(RstpEndpoint, rstp_response)
        assert isinstance(result.type, list)
        assert len(result.type) > 0
        assert all(isinstance(v, str) for v in result.type)

    def test_type_values_are_valid(self, rstp_response):
        result = readDataclass(RstpEndpoint, rstp_response)
        valid = set(get_args(RstpType))
        assert all(v in valid for v in result.type)

    def test_state_is_str_list(self, rstp_response):
        result = readDataclass(RstpEndpoint, rstp_response)
        assert isinstance(result.state, list)
        assert len(result.state) > 0
        assert all(isinstance(v, str) for v in result.state)

    def test_state_values_are_valid(self, rstp_response):
        result = readDataclass(RstpEndpoint, rstp_response)
        valid = set(get_args(RstpState))
        assert all(v in valid for v in result.state)

    def test_all_port_lists_same_length(self, rstp_response):
        """All per-port fields should have the same number of entries."""
        result = readDataclass(RstpEndpoint, rstp_response)
        lengths = {
            len(result.rstp),
            len(result.mode),
            len(result.role),
            len(result.root_path_cost),
            len(result.type),
            len(result.state),
        }
        assert len(lengths) == 1, f"Inconsistent port counts: {lengths}"


class TestRstpEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, rstp_response, rstp_expected):
        if rstp_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = asdict(readDataclass(RstpEndpoint, rstp_response))
        for field, expected in rstp_expected.items():
            assert result[field] == expected, (
                f"Field {field!r}: expected {expected!r}, got {result[field]!r}"
            )

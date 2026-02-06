"""Tests for AclStatsEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/!aclstats_b/. Expected values
come from companion .expected files (Python dict literals).
"""

import pytest
from dataclasses import asdict
from python_switchos.endpoint import readDataclass
from python_switchos.endpoints.acl import AclStatsEndpoint


COUNTER_FIELDS = ["counter_1", "counter_2", "counter_3", "counter_4"]


class TestAclStatsEndpointParsing:
    """Generic parsing tests that run against all !aclstats_b fixtures."""

    def test_parses_to_dataclass(self, aclstats_response):
        result = readDataclass(AclStatsEndpoint, aclstats_response)
        assert isinstance(result, AclStatsEndpoint)

    def test_counter_1_is_list_of_int(self, aclstats_response):
        result = readDataclass(AclStatsEndpoint, aclstats_response)
        assert isinstance(result.counter_1, list)
        assert all(isinstance(v, int) for v in result.counter_1)

    def test_counter_2_is_list_of_int(self, aclstats_response):
        result = readDataclass(AclStatsEndpoint, aclstats_response)
        assert isinstance(result.counter_2, list)
        assert all(isinstance(v, int) for v in result.counter_2)

    def test_counter_3_is_list_of_int(self, aclstats_response):
        result = readDataclass(AclStatsEndpoint, aclstats_response)
        assert isinstance(result.counter_3, list)
        assert all(isinstance(v, int) for v in result.counter_3)

    def test_counter_4_is_list_of_int(self, aclstats_response):
        result = readDataclass(AclStatsEndpoint, aclstats_response)
        assert isinstance(result.counter_4, list)
        assert all(isinstance(v, int) for v in result.counter_4)

    def test_all_counters_have_consistent_length(self, aclstats_response):
        """All counter arrays should have the same length (matching port count)."""
        result = readDataclass(AclStatsEndpoint, aclstats_response)
        # Get expected length from first counter
        expected_length = len(result.counter_1)
        for field_name in COUNTER_FIELDS:
            field_value = getattr(result, field_name)
            assert len(field_value) == expected_length, (
                f"{field_name} has {len(field_value)} elements, expected {expected_length}"
            )


class TestAclStatsEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, aclstats_response, aclstats_expected):
        if aclstats_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = asdict(readDataclass(AclStatsEndpoint, aclstats_response))
        for field, expected in aclstats_expected.items():
            assert result[field] == expected, (
                f"Field {field!r}: expected {expected!r}, got {result[field]!r}"
            )

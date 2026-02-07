"""Tests for VlanEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/vlan_b/. Expected values
come from companion .expected files (Python dict literals).
"""

import pytest
from dataclasses import asdict
from python_switchos.endpoint import readListDataclass
from python_switchos.endpoints.vlan import VlanEntry, VlanEndpoint


class TestVlanEndpointParsing:
    """Generic parsing tests that run against all vlan_b fixtures."""

    def test_parses_to_list(self, vlan_response):
        result = readListDataclass(VlanEntry, vlan_response)
        assert isinstance(result, list)

    def test_entries_are_vlan_entry(self, vlan_response):
        result = readListDataclass(VlanEntry, vlan_response)
        assert all(isinstance(entry, VlanEntry) for entry in result)

    def test_each_entry_has_vlan_id_int(self, vlan_response):
        result = readListDataclass(VlanEntry, vlan_response)
        for entry in result:
            assert isinstance(entry.vlan_id, int)

    def test_each_entry_has_igmp_snooping_bool(self, vlan_response):
        result = readListDataclass(VlanEntry, vlan_response)
        for entry in result:
            assert isinstance(entry.igmp_snooping, bool)

    def test_each_entry_has_members_list(self, vlan_response):
        result = readListDataclass(VlanEntry, vlan_response)
        if not result:
            return  # Empty list is valid
        # All entries should have same-length members list
        expected_length = len(result[0].members)
        for entry in result:
            assert isinstance(entry.members, list)
            assert len(entry.members) == expected_length
            assert all(isinstance(m, bool) for m in entry.members)


class TestVlanEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, vlan_response, vlan_expected):
        if vlan_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = readListDataclass(VlanEntry, vlan_response)
        result_dicts = [asdict(entry) for entry in result]
        assert len(result_dicts) == len(vlan_expected), (
            f"Entry count mismatch: expected {len(vlan_expected)}, got {len(result_dicts)}"
        )
        for i, (actual, expected) in enumerate(zip(result_dicts, vlan_expected)):
            assert actual == expected, (
                f"Entry {i}: expected {expected!r}, got {actual!r}"
            )


class TestVlanEndpointEmptyList:
    """Test that empty arrays return empty list."""

    def test_empty_array_returns_empty_list(self):
        result = readListDataclass(VlanEntry, "[]")
        assert result == []

    def test_none_equivalent_returns_empty_list(self):
        """Empty JSON object should return empty list."""
        result = readListDataclass(VlanEntry, "{}")
        assert result == []

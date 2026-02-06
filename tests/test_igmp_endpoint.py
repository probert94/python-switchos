"""Tests for IgmpEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/igmp_b/. Expected values
come from companion .expected files (Python dict literals).
"""

import pytest
from dataclasses import asdict
from python_switchos.endpoint import readListDataclass
from python_switchos.endpoints.igmp import IgmpEntry, IgmpEndpoint


class TestIgmpEndpointParsing:
    """Generic parsing tests that run against all igmp_b fixtures."""

    def test_parses_to_list(self, igmp_response):
        result = readListDataclass(IgmpEntry, igmp_response)
        assert isinstance(result, list)

    def test_entries_are_igmp_entry(self, igmp_response):
        result = readListDataclass(IgmpEntry, igmp_response)
        assert all(isinstance(entry, IgmpEntry) for entry in result)

    def test_each_entry_has_group_address_str(self, igmp_response):
        result = readListDataclass(IgmpEntry, igmp_response)
        for entry in result:
            assert isinstance(entry.group_address, str)

    def test_each_entry_has_vlan_int(self, igmp_response):
        result = readListDataclass(IgmpEntry, igmp_response)
        for entry in result:
            assert isinstance(entry.vlan, int)

    def test_each_entry_has_member_ports_list(self, igmp_response):
        result = readListDataclass(IgmpEntry, igmp_response)
        if not result:
            return  # Empty list is valid
        # All entries should have same-length member_ports list
        expected_length = len(result[0].member_ports)
        for entry in result:
            assert isinstance(entry.member_ports, list)
            assert len(entry.member_ports) == expected_length
            assert all(isinstance(p, bool) for p in entry.member_ports)

    def test_group_address_is_ip_format(self, igmp_response):
        """Group address should be in dotted decimal IP format."""
        result = readListDataclass(IgmpEntry, igmp_response)
        for entry in result:
            parts = entry.group_address.split(".")
            assert len(parts) == 4, f"IP {entry.group_address} does not have 4 parts"
            for part in parts:
                assert part.isdigit(), f"IP part {part} is not numeric"
                assert 0 <= int(part) <= 255, f"IP part {part} out of range"


class TestIgmpEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, igmp_response, igmp_expected):
        if igmp_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = readListDataclass(IgmpEntry, igmp_response)
        result_dicts = [asdict(entry) for entry in result]
        assert len(result_dicts) == len(igmp_expected), (
            f"Entry count mismatch: expected {len(igmp_expected)}, got {len(result_dicts)}"
        )
        for i, (actual, expected) in enumerate(zip(result_dicts, igmp_expected)):
            assert actual == expected, (
                f"Entry {i}: expected {expected!r}, got {actual!r}"
            )


class TestIgmpEndpointEmptyList:
    """Test that empty arrays return empty list."""

    def test_empty_array_returns_empty_list(self):
        result = readListDataclass(IgmpEntry, "[]")
        assert result == []

    def test_none_equivalent_returns_empty_list(self):
        """Empty JSON object should return empty list."""
        result = readListDataclass(IgmpEntry, "{}")
        assert result == []

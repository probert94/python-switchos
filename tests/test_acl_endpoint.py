"""Tests for AclEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/acl_b/. Expected values
come from companion .expected files (Python dict literals).
"""

import pytest
from dataclasses import asdict
from typing import get_args
from python_switchos.endpoint import readListDataclass
from python_switchos.endpoints.acl import AclEntry, AclEndpoint, VlanMatch, AccountAs


class TestAclEndpointParsing:
    """Generic parsing tests that run against all acl_b fixtures."""

    def test_parses_to_list(self, acl_response):
        result = readListDataclass(AclEntry, acl_response)
        assert isinstance(result, list)

    def test_entries_are_acl_entry(self, acl_response):
        result = readListDataclass(AclEntry, acl_response)
        assert all(isinstance(entry, AclEntry) for entry in result)

    def test_each_entry_has_from_ports_list(self, acl_response):
        result = readListDataclass(AclEntry, acl_response)
        if not result:
            return  # Empty list is valid
        # All entries should have same-length from_ports list
        expected_length = len(result[0].from_ports)
        for entry in result:
            assert isinstance(entry.from_ports, list)
            assert len(entry.from_ports) == expected_length
            assert all(isinstance(p, bool) for p in entry.from_ports)

    def test_each_entry_has_mac_fields_str(self, acl_response):
        result = readListDataclass(AclEntry, acl_response)
        for entry in result:
            assert isinstance(entry.mac_src, str)
            assert isinstance(entry.mac_dst, str)
            assert isinstance(entry.mac_src_mask, str)
            assert isinstance(entry.mac_dst_mask, str)

    def test_each_entry_has_ip_fields_str(self, acl_response):
        result = readListDataclass(AclEntry, acl_response)
        for entry in result:
            assert isinstance(entry.ip_src, str)
            assert isinstance(entry.ip_dst, str)

    def test_each_entry_has_vlan_match(self, acl_response):
        result = readListDataclass(AclEntry, acl_response)
        vlan_options = get_args(VlanMatch)
        for entry in result:
            assert entry.vlan in vlan_options

    def test_each_entry_has_account_as(self, acl_response):
        result = readListDataclass(AclEntry, acl_response)
        account_options = get_args(AccountAs)
        for entry in result:
            assert entry.account_as in account_options

    def test_each_entry_has_drop_bool(self, acl_response):
        result = readListDataclass(AclEntry, acl_response)
        for entry in result:
            assert isinstance(entry.drop, bool)


class TestAclEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, acl_response, acl_expected):
        if acl_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = readListDataclass(AclEntry, acl_response)
        result_dicts = [asdict(entry) for entry in result]
        assert len(result_dicts) == len(acl_expected), (
            f"Entry count mismatch: expected {len(acl_expected)}, got {len(result_dicts)}"
        )
        for i, (actual, expected) in enumerate(zip(result_dicts, acl_expected)):
            assert actual == expected, (
                f"Entry {i}: expected {expected!r}, got {actual!r}"
            )


class TestAclEndpointEmptyList:
    """Test that empty arrays return empty list."""

    def test_empty_array_returns_empty_list(self):
        result = readListDataclass(AclEntry, "[]")
        assert result == []

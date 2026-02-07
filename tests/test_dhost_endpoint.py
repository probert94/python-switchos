"""Tests for DynamicHostEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/!dhost.b/. Expected values
come from companion .expected files (Python dict literals).
"""

import pytest
from dataclasses import asdict
from python_switchos.endpoint import readListDataclass
from python_switchos.endpoints.host import DynamicHostEndpoint, HostEntry


class TestDynamicHostEndpointParsing:
    """Generic parsing tests that run against all !dhost.b fixtures."""

    def test_parses_to_list(self, dhost_response):
        result = readListDataclass(HostEntry, dhost_response)
        assert isinstance(result, list)

    def test_entries_are_host_entry(self, dhost_response):
        result = readListDataclass(HostEntry, dhost_response)
        assert all(isinstance(entry, HostEntry) for entry in result)

    def test_each_entry_has_port_int(self, dhost_response):
        result = readListDataclass(HostEntry, dhost_response)
        for entry in result:
            assert isinstance(entry.port, int)

    def test_each_entry_has_mac_str(self, dhost_response):
        result = readListDataclass(HostEntry, dhost_response)
        for entry in result:
            assert isinstance(entry.mac, str)

    def test_fixture_has_entries(self, dhost_response):
        """The fixture data should have at least one dynamic host entry."""
        result = readListDataclass(HostEntry, dhost_response)
        assert len(result) >= 1


class TestDynamicHostEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, dhost_response, dhost_expected):
        if dhost_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = readListDataclass(HostEntry, dhost_response)
        result_dicts = [asdict(entry) for entry in result]
        assert len(result_dicts) == len(dhost_expected), (
            f"Entry count mismatch: expected {len(dhost_expected)}, got {len(result_dicts)}"
        )
        for i, (actual, expected) in enumerate(zip(result_dicts, dhost_expected)):
            assert actual == expected, (
                f"Entry {i}: expected {expected!r}, got {actual!r}"
            )

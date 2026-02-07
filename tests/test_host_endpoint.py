"""Tests for HostEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/host_b/. Expected values
come from companion .expected files (Python dict literals).
"""

import pytest
from dataclasses import asdict
from python_switchos.endpoint import readListDataclass
from python_switchos.endpoints.host import HostEntry, HostEndpoint


class TestHostEndpointParsing:
    """Generic parsing tests that run against all host.b fixtures."""

    def test_parses_to_list(self, host_response):
        result = readListDataclass(HostEntry, host_response)
        assert isinstance(result, list)

    def test_entries_are_host_entry(self, host_response):
        result = readListDataclass(HostEntry, host_response)
        assert all(isinstance(entry, HostEntry) for entry in result)

    def test_each_entry_has_port_int(self, host_response):
        result = readListDataclass(HostEntry, host_response)
        for entry in result:
            assert isinstance(entry.port, int)

    def test_each_entry_has_mac_str(self, host_response):
        result = readListDataclass(HostEntry, host_response)
        for entry in result:
            assert isinstance(entry.mac, str)

    def test_mac_format(self, host_response):
        """MAC addresses should be in AA:BB:CC:DD:EE:FF format."""
        result = readListDataclass(HostEntry, host_response)
        for entry in result:
            parts = entry.mac.split(":")
            assert len(parts) == 6, f"MAC {entry.mac} does not have 6 parts"
            for part in parts:
                assert len(part) == 2, f"MAC part {part} is not 2 chars"


class TestHostEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, host_response, host_expected):
        if host_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = readListDataclass(HostEntry, host_response)
        result_dicts = [asdict(entry) for entry in result]
        assert len(result_dicts) == len(host_expected), (
            f"Entry count mismatch: expected {len(host_expected)}, got {len(result_dicts)}"
        )
        for i, (actual, expected) in enumerate(zip(result_dicts, host_expected)):
            assert actual == expected, (
                f"Entry {i}: expected {expected!r}, got {actual!r}"
            )


class TestHostEndpointEmptyList:
    """Test that empty arrays return empty list."""

    def test_empty_array_returns_empty_list(self):
        result = readListDataclass(HostEntry, "[]")
        assert result == []

    def test_none_equivalent_returns_empty_list(self):
        """Empty JSON object should return empty list."""
        result = readListDataclass(HostEntry, "{}")
        assert result == []

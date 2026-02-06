"""Tests for SnmpEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/snmp_b/. Expected values
come from companion .expected files (Python dict literals).
"""

import pytest
from dataclasses import asdict
from python_switchos.endpoint import readDataclass
from python_switchos.endpoints.snmp import SnmpEndpoint


class TestSnmpEndpointParsing:
    """Generic parsing tests that run against all snmp.b fixtures."""

    def test_parses_to_snmp_endpoint(self, snmp_response):
        result = readDataclass(SnmpEndpoint, snmp_response)
        assert isinstance(result, SnmpEndpoint)

    def test_enabled_is_bool(self, snmp_response):
        result = readDataclass(SnmpEndpoint, snmp_response)
        assert isinstance(result.enabled, bool)

    def test_community_is_str(self, snmp_response):
        result = readDataclass(SnmpEndpoint, snmp_response)
        assert isinstance(result.community, str)

    def test_contact_info_is_str(self, snmp_response):
        result = readDataclass(SnmpEndpoint, snmp_response)
        assert isinstance(result.contact_info, str)

    def test_location_is_str(self, snmp_response):
        result = readDataclass(SnmpEndpoint, snmp_response)
        assert isinstance(result.location, str)


class TestSnmpEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, snmp_response, snmp_expected):
        if snmp_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = asdict(readDataclass(SnmpEndpoint, snmp_response))
        for field, expected in snmp_expected.items():
            assert result[field] == expected, (
                f"Field {field!r}: expected {expected!r}, got {result[field]!r}"
            )

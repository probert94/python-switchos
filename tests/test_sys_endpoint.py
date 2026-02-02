"""Tests for SystemEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/sys_b/. Expected values
come from companion .expected files (Python dict literals).
"""

import re
import pytest
from dataclasses import asdict
from python_switchos.endpoint import readDataclass
from python_switchos.endpoints.sys import SystemEndpoint, AddressAcquisition


class TestSystemEndpointParsing:
    """Generic parsing tests that run against all sys.b fixtures."""

    def test_parses_to_system_endpoint(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        assert isinstance(result, SystemEndpoint)

    def test_address_acquisition_is_valid(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        assert result.address_acquisition in ("DHCP_FALLBACK", "STATIC", "DHCP")

    def test_static_ip_format(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        assert isinstance(result.static_ip, str)
        assert re.match(r"^\d+\.\d+\.\d+\.\d+$", result.static_ip)

    def test_ip_format(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        assert isinstance(result.ip, str)
        assert re.match(r"^\d+\.\d+\.\d+\.\d+$", result.ip)

    def test_identity_is_str(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        assert isinstance(result.identity, str)
        assert len(result.identity) > 0

    def test_serial_is_str(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        assert isinstance(result.serial, str)
        assert len(result.serial) > 0

    def test_mac_format(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        assert isinstance(result.mac, str)
        assert re.match(r"^[0-9A-F]{2}(:[0-9A-F]{2}){5}$", result.mac)

    def test_model_is_str(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        assert isinstance(result.model, str)
        assert len(result.model) > 0

    def test_version_is_str(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        assert isinstance(result.version, str)
        assert len(result.version) > 0

    def test_uptime_is_int(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        assert isinstance(result.uptime, int)
        assert result.uptime >= 0

    def test_cpu_temp_is_int(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        assert isinstance(result.cpu_temp, int)
        assert -40 <= result.cpu_temp <= 125


class TestSystemEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, sys_response, sys_expected):
        if sys_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = asdict(readDataclass(SystemEndpoint, sys_response))
        for field, expected in sys_expected.items():
            assert result[field] == expected, (
                f"Field {field!r}: expected {expected!r}, got {result[field]!r}"
            )


class TestSystemEndpointMissingFields:
    """Document fields present in engine.js sys.b but missing from SystemEndpoint."""

    @pytest.mark.parametrize("field_id,field_name", [
        ("i08", "mikrotik_discovery_protocol"),
        ("i12", "allow_from_ports"),
        ("i13", "dhcp_snooping_trusted_ports"),
        ("i14", "dhcp_snooping_add_info_option"),
        ("i17", "igmp_snooping"),
        ("i19", "allow_from_ip"),
        ("i1a", "allow_from_mask"),
        ("i1b", "allow_from_vlan"),
        ("i27", "igmp_fast_leave"),
        ("i28", "igmp_version"),
        ("i29", "igmp_querier"),
        ("i2a", "forward_reserved_multicast"),
        ("i0b", "build_number"),
        ("i0e", "bridge_priority"),
        ("i0f", "port_cost_mode"),
        ("i10", "root_bridge_priority"),
        ("i11", "root_bridge_mac"),
    ])
    def test_sys_missing_fields(self, field_id, field_name):
        pytest.skip(
            f"MISSING: {field_name} ({field_id}) exists in engine.js sys.b "
            f"but not in SystemEndpoint"
        )

"""Tests for SystemEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/sys_b/. Expected values
come from companion .expected files (Python dict literals).
"""

import re
import pytest
from dataclasses import asdict
from python_switchos.endpoint import readDataclass
from python_switchos.endpoints.sys import SystemEndpoint, AddressAcquisition, PortCostMode, IgmpVersion


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

    # -- RSTP General fields --

    def test_bridge_priority(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.bridge_priority is None:
            pytest.skip("bridge_priority not present in this fixture")
        assert isinstance(result.bridge_priority, int)
        assert 0 <= result.bridge_priority <= 65535

    def test_forward_reserved_multicast(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.forward_reserved_multicast is None:
            pytest.skip("forward_reserved_multicast not present in this fixture")
        assert isinstance(result.forward_reserved_multicast, bool)

    def test_port_cost_mode(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.port_cost_mode is None:
            pytest.skip("port_cost_mode not present in this fixture")
        assert result.port_cost_mode in ("short", "long")

    def test_root_bridge_priority(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.root_bridge_priority is None:
            pytest.skip("root_bridge_priority not present in this fixture")
        assert isinstance(result.root_bridge_priority, int)
        assert 0 <= result.root_bridge_priority <= 65535

    def test_root_bridge_mac(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.root_bridge_mac is None:
            pytest.skip("root_bridge_mac not present in this fixture")
        assert isinstance(result.root_bridge_mac, str)
        assert re.match(r"^[0-9A-F]{2}(:[0-9A-F]{2}){5}$", result.root_bridge_mac)

    # -- Access Control fields --

    def test_allow_from_ip(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.allow_from_ip is None:
            pytest.skip("allow_from_ip not present in this fixture")
        assert isinstance(result.allow_from_ip, str)
        assert re.match(r"^\d+\.\d+\.\d+\.\d+$", result.allow_from_ip)

    def test_allow_from_mask(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.allow_from_mask is None:
            pytest.skip("allow_from_mask not present in this fixture")
        assert isinstance(result.allow_from_mask, int)
        assert 0 <= result.allow_from_mask <= 32

    def test_allow_from_ports(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.allow_from_ports is None:
            pytest.skip("allow_from_ports not present in this fixture")
        assert isinstance(result.allow_from_ports, list)
        assert all(isinstance(v, bool) for v in result.allow_from_ports)

    def test_allow_from_vlan(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.allow_from_vlan is None:
            pytest.skip("allow_from_vlan not present in this fixture")
        assert isinstance(result.allow_from_vlan, int)
        assert 0 <= result.allow_from_vlan <= 4095

    # -- IGMP fields --

    def test_igmp_snooping(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.igmp_snooping is None:
            pytest.skip("igmp_snooping not present in this fixture")
        assert isinstance(result.igmp_snooping, bool)

    def test_igmp_querier(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.igmp_querier is None:
            pytest.skip("igmp_querier not present in this fixture")
        assert isinstance(result.igmp_querier, bool)

    def test_igmp_fast_leave(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.igmp_fast_leave is None:
            pytest.skip("igmp_fast_leave not present in this fixture")
        assert isinstance(result.igmp_fast_leave, list)
        assert all(isinstance(v, bool) for v in result.igmp_fast_leave)

    def test_igmp_version(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.igmp_version is None:
            pytest.skip("igmp_version not present in this fixture")
        assert result.igmp_version in ("v2", "v3")

    # -- MDP field --

    def test_mikrotik_discovery_protocol(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.mikrotik_discovery_protocol is None:
            pytest.skip("mikrotik_discovery_protocol not present in this fixture")
        assert isinstance(result.mikrotik_discovery_protocol, list)
        assert all(isinstance(v, bool) for v in result.mikrotik_discovery_protocol)

    # -- DHCP Snooping fields --

    def test_dhcp_snooping_trusted_ports(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.dhcp_snooping_trusted_ports is None:
            pytest.skip("dhcp_snooping_trusted_ports not present in this fixture")
        assert isinstance(result.dhcp_snooping_trusted_ports, list)
        assert all(isinstance(v, bool) for v in result.dhcp_snooping_trusted_ports)

    def test_dhcp_snooping_add_info_option(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.dhcp_snooping_add_info_option is None:
            pytest.skip("dhcp_snooping_add_info_option not present in this fixture")
        assert isinstance(result.dhcp_snooping_add_info_option, bool)

    # -- Build number --

    def test_build_number(self, sys_response):
        result = readDataclass(SystemEndpoint, sys_response)
        if result.build_number is None:
            pytest.skip("build_number not present in this fixture")
        assert isinstance(result.build_number, int)
        assert result.build_number >= 0


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

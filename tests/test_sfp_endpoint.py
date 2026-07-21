"""Tests for SfpEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/sfp_b/. Expected values
come from companion .expected files (Python dict literals).
"""

import pytest
from dataclasses import asdict
from python_switchos.endpoint import readDataclass
from python_switchos.endpoints.sfp import SfpEndpoint


class TestSfpEndpointParsing:
    """Generic parsing tests that run against all sfp.b fixtures."""

    def test_parses_to_sfp_endpoint(self, sfp_response):
        result = readDataclass(SfpEndpoint, sfp_response)
        assert isinstance(result, SfpEndpoint)

    def test_vendor_is_str_list(self, sfp_response):
        result = readDataclass(SfpEndpoint, sfp_response)
        assert isinstance(result.vendor, list)
        assert all(isinstance(v, str) for v in result.vendor)

    def test_temperature_is_int_list(self, sfp_response):
        result = readDataclass(SfpEndpoint, sfp_response)
        assert isinstance(result.temperature, list)
        assert all(isinstance(v, int) for v in result.temperature)

    def test_voltage_is_float_list(self, sfp_response):
        result = readDataclass(SfpEndpoint, sfp_response)
        assert isinstance(result.voltage, list)
        assert all(isinstance(v, float) for v in result.voltage)

    def test_tx_power_is_float_list(self, sfp_response):
        result = readDataclass(SfpEndpoint, sfp_response)
        assert isinstance(result.tx_power, list)
        assert all(isinstance(v, float) for v in result.tx_power)

    def test_rx_power_is_float_list(self, sfp_response):
        result = readDataclass(SfpEndpoint, sfp_response)
        assert isinstance(result.rx_power, list)
        assert all(isinstance(v, float) for v in result.rx_power)

    def test_type_decodes_wavelength(self, sfp_response):
        """Type strings should not contain raw {hex} patterns."""
        result = readDataclass(SfpEndpoint, sfp_response)
        assert isinstance(result.type, list)
        for t in result.type:
            assert "{" not in t, f"Type '{t}' contains undecoded {{hex}} pattern"

    def test_all_sfp_lists_same_length(self, sfp_response):
        """All per-SFP fields should have the same number of entries."""
        result = readDataclass(SfpEndpoint, sfp_response)
        lengths = {
            len(result.vendor), len(result.part_number), len(result.revision),
            len(result.serial), len(result.date), len(result.type),
            len(result.temperature), len(result.voltage), len(result.tx_bias),
            len(result.tx_power), len(result.rx_power),
        }
        assert len(lengths) == 1, f"Inconsistent SFP port counts: {lengths}"


class TestSfpEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, sfp_response, sfp_expected):
        if sfp_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = asdict(readDataclass(SfpEndpoint, sfp_response))
        for field, expected in sfp_expected.items():
            assert result[field] == expected, (
                f"Field {field!r}: expected {expected!r}, got {result[field]!r}"
            )

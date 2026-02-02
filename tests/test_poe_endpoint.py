"""Tests for PoEEndpoint parsing and pattern consistency.

Structure tests always run (no fixtures needed). Parsing and expected-value
tests run against every fixture file discovered in tests/fixtures/poe_b/.
"""

import pytest
from dataclasses import fields, asdict
from typing import get_args
from python_switchos.endpoint import readDataclass
from python_switchos.endpoints.poe import PoEEndpoint, PoEOut, VoltageLevel, State


class TestPoEEndpointStructure:
    """Verify PoEEndpoint follows the same metadata patterns as other endpoints."""

    def test_is_dataclass(self):
        assert hasattr(PoEEndpoint, "__dataclass_fields__")

    def test_endpoint_path(self):
        assert PoEEndpoint.endpoint_path == "poe.b"

    def test_fields_have_required_metadata(self):
        for f in fields(PoEEndpoint):
            assert "name" in f.metadata, f"Field {f.name} missing 'name' metadata"
            assert "type" in f.metadata, f"Field {f.name} missing 'type' metadata"

    def test_name_metadata_is_list(self):
        for f in fields(PoEEndpoint):
            assert isinstance(f.metadata["name"], list), (
                f"Field {f.name} 'name' should be a list"
            )

    def test_name_metadata_has_aliases(self):
        for f in fields(PoEEndpoint):
            assert len(f.metadata["name"]) >= 1, (
                f"Field {f.name} needs at least one name alias"
            )

    def test_option_fields_have_options(self):
        for f in fields(PoEEndpoint):
            if f.metadata.get("type") == "option":
                assert "options" in f.metadata, (
                    f"Option field {f.name} missing 'options' metadata"
                )

    def test_scale_values_are_numeric(self):
        for f in fields(PoEEndpoint):
            if "scale" in f.metadata:
                assert isinstance(f.metadata["scale"], (int, float)), (
                    f"Field {f.name} scale should be numeric, "
                    f"got {type(f.metadata['scale'])}"
                )

    def test_has_expected_field_count(self):
        """PoEEndpoint should have 9 fields."""
        assert len(fields(PoEEndpoint)) == 9

    def test_type_values_are_valid(self):
        valid_types = {"bool", "int", "str", "option", "mac", "ip", "bitshift_option"}
        for f in fields(PoEEndpoint):
            assert f.metadata["type"] in valid_types, (
                f"Field {f.name} has unexpected type '{f.metadata['type']}'"
            )


class TestPoEEndpointParsing:
    """Generic parsing tests that run against all poe.b fixtures."""

    def test_parses_to_poe_endpoint(self, poe_response):
        result = readDataclass(PoEEndpoint, poe_response)
        assert isinstance(result, PoEEndpoint)

    def test_out_values_are_valid(self, poe_response):
        result = readDataclass(PoEEndpoint, poe_response)
        if result.out is None:
            pytest.skip("out field not in response")
        valid = set(get_args(PoEOut)) | {None}
        assert all(v in valid for v in result.out)

    def test_voltage_level_values_are_valid(self, poe_response):
        result = readDataclass(PoEEndpoint, poe_response)
        if result.voltage_level is None:
            pytest.skip("voltage_level field not in response")
        valid = set(get_args(VoltageLevel)) | {None}
        assert all(v in valid for v in result.voltage_level)

    def test_state_values_are_valid(self, poe_response):
        result = readDataclass(PoEEndpoint, poe_response)
        if result.state is None:
            pytest.skip("state field not in response")
        valid = set(get_args(State)) | {None}
        assert all(v in valid for v in result.state)

    def test_lldp_enabled_is_bool_list(self, poe_response):
        result = readDataclass(PoEEndpoint, poe_response)
        if result.lldp_enabled is None:
            pytest.skip("lldp_enabled field not in response")
        assert isinstance(result.lldp_enabled, list)
        assert all(isinstance(v, bool) for v in result.lldp_enabled)

    def test_scaled_fields_are_float(self, poe_response):
        result = readDataclass(PoEEndpoint, poe_response)
        for name in ("lldp_power", "voltage", "power"):
            val = getattr(result, name)
            if val is None:
                continue
            assert isinstance(val, list), f"{name} should be a list"
            assert all(isinstance(v, (int, float)) for v in val), (
                f"{name} values should be numeric"
            )

    def test_int_fields_are_int_list(self, poe_response):
        result = readDataclass(PoEEndpoint, poe_response)
        for name in ("priority", "current"):
            val = getattr(result, name)
            if val is None:
                continue
            assert isinstance(val, list), f"{name} should be a list"
            assert all(isinstance(v, int) for v in val), (
                f"{name} values should be int"
            )


class TestPoEEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, poe_response, poe_expected):
        if poe_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = asdict(readDataclass(PoEEndpoint, poe_response))
        for field, expected in poe_expected.items():
            assert result[field] == expected, (
                f"Field {field!r}: expected {expected!r}, got {result[field]!r}"
            )

"""Tests for StatsEndpoint parsing against fixture data.

Generic type/structure tests and expected-value tests both run against
every fixture file discovered in tests/fixtures/!stats_b/. Expected values
come from companion .expected files (Python dict literals).
"""

import pytest
from dataclasses import asdict
from python_switchos.endpoint import readDataclass
from python_switchos.endpoints.stats import StatsEndpoint


# Rate fields return float
RATE_FIELDS = ["rx_rate", "tx_rate", "rx_packet_rate", "tx_packet_rate"]

# All counter fields return int (31 fields total)
COUNTER_FIELDS = [
    # Byte counters (2)
    "rx_bytes", "tx_bytes",
    # Packet counters (8)
    "rx_total_packets", "tx_total_packets",
    "rx_unicasts", "tx_unicasts",
    "rx_broadcasts", "tx_broadcasts",
    "rx_multicasts", "tx_multicasts",
    # Error counters (15)
    "rx_pauses", "rx_errors", "rx_fcs_errors", "rx_jabber", "rx_runts",
    "rx_fragments", "rx_too_long", "tx_pauses", "tx_fcs_errors",
    "tx_collisions", "tx_single_collisions", "tx_multiple_collisions",
    "tx_excessive_collisions", "tx_late_collisions", "tx_deferred",
    # Histogram counters (6)
    "hist_64", "hist_65_127", "hist_128_255", "hist_256_511",
    "hist_512_1023", "hist_1024_max",
]


class TestStatsEndpointParsing:
    """Generic parsing tests that run against all !stats.b fixtures."""

    def test_parses_to_stats_endpoint(self, stats_response):
        result = readDataclass(StatsEndpoint, stats_response)
        assert isinstance(result, StatsEndpoint)

    def test_rate_fields_are_float_lists(self, stats_response):
        result = readDataclass(StatsEndpoint, stats_response)
        for field_name in RATE_FIELDS:
            field_value = getattr(result, field_name)
            assert isinstance(field_value, list), f"{field_name} should be a list"
            assert len(field_value) > 0, f"{field_name} should not be empty"
            assert all(isinstance(v, (int, float)) for v in field_value), (
                f"{field_name} values should be numeric"
            )

    def test_counter_fields_are_int_lists(self, stats_response):
        result = readDataclass(StatsEndpoint, stats_response)
        for field_name in COUNTER_FIELDS:
            field_value = getattr(result, field_name)
            assert isinstance(field_value, list), f"{field_name} should be a list"
            assert len(field_value) > 0, f"{field_name} should not be empty"
            assert all(isinstance(v, int) for v in field_value), (
                f"{field_name} values should be integers"
            )

    def test_all_port_lists_same_length(self, stats_response):
        """All per-port fields should have the same number of entries."""
        result = readDataclass(StatsEndpoint, stats_response)
        all_fields = RATE_FIELDS + COUNTER_FIELDS
        lengths = {len(getattr(result, f)) for f in all_fields}
        assert len(lengths) == 1, f"Inconsistent port counts: {lengths}"


class TestStatsEndpointExpectedValues:
    """Compare parsed results against expected values from .expected files."""

    def test_expected_values(self, stats_response, stats_expected):
        if stats_expected is None:
            pytest.skip("No .expected file for this fixture")
        result = asdict(readDataclass(StatsEndpoint, stats_response))
        for field, expected in stats_expected.items():
            assert result[field] == expected, (
                f"Field {field!r}: expected {expected!r}, got {result[field]!r}"
            )

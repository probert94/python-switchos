"""Unit tests for python_switchos.utils conversion functions."""

from typing import Literal

from python_switchos.utils import (
    hex_to_bool_list,
    hex_to_str,
    hex_to_option,
    hex_to_mac,
    hex_to_ip,
    process_int,
    str_to_json,
)


# --- hex_to_bool_list ---

class TestHexToBoolList:
    def test_all_true(self):
        """0x3ff with 10 bits = all True."""
        result = hex_to_bool_list(0x03FF, 10)
        assert result == [True] * 10

    def test_all_false(self):
        """Zero value produces all False."""
        result = hex_to_bool_list(0, 10)
        assert result == [False] * 10

    def test_basic_conversion(self):
        """Binary 1010 = bit0=0, bit1=1, bit2=0, bit3=1 (LSB-first)."""
        result = hex_to_bool_list(0b1010, 4)
        assert result == [False, True, False, True]

    def test_single_bit_lsb(self):
        """0x200 (bit 9 set) with 10 bits.
        LSB-first: bit 9 maps to index 9 (last port)."""
        result = hex_to_bool_list(0x200, 10)
        assert result[9] is True
        assert all(v is False for v in result[:9])

    def test_returns_correct_length(self):
        result = hex_to_bool_list(0xFF, 8)
        assert len(result) == 8

    def test_padding(self):
        """Value 1 = only bit 0 set. LSB-first: first element is True."""
        result = hex_to_bool_list(1, 8)
        assert len(result) == 8
        assert result[0] is True
        assert all(v is False for v in result[1:])

    def test_high_low_array_more_than_32_ports(self):
        """[high, low] arrays are used for >32 ports (e.g. css354, 60 ports).

        Ports 0-31 come from low, ports 32+ from high."""
        result = hex_to_bool_list([0x1, 0x1], 40)
        assert result[0] is True
        assert all(v is False for v in result[1:32])
        assert result[32] is True
        assert all(v is False for v in result[33:])


# --- hex_to_str ---

class TestHexToStr:
    def test_basic_decode(self):
        """'506f727431' decodes to 'Port1'."""
        assert hex_to_str("506f727431") == "Port1"

    def test_empty_string(self):
        assert hex_to_str("") == ""

    def test_ascii_characters(self):
        """'48656c6c6f' decodes to 'Hello'."""
        assert hex_to_str("48656c6c6f") == "Hello"

    def test_stops_at_nul_byte(self):
        """Decoding stops at the first 00 byte, ignoring anything after it."""
        assert hex_to_str("506f727431004242") == "Port1"

    def test_non_utf8_byte_does_not_raise(self):
        """SwOS Lite may send raw non-UTF-8 bytes; decoding must not crash."""
        hex_to_str("ff")


# --- hex_to_option ---

class TestHexToOption:
    def test_first_option(self):
        TestLiteral = Literal["a", "b", "c"]
        assert hex_to_option(0, TestLiteral) == "a"

    def test_last_option(self):
        TestLiteral = Literal["a", "b", "c"]
        assert hex_to_option(2, TestLiteral) == "c"

    def test_out_of_range(self):
        TestLiteral = Literal["a", "b", "c"]
        assert hex_to_option(5, TestLiteral) is None

    def test_negative_one(self):
        """-1 must not silently wrap around to the last option (Python list semantics)."""
        TestLiteral = Literal["a", "b", "c"]
        assert hex_to_option(-1, TestLiteral) is None

    def test_middle_option(self):
        TestLiteral = Literal["a", "b", "c"]
        assert hex_to_option(1, TestLiteral) == "b"


# --- hex_to_mac ---

class TestHexToMac:
    def test_basic_mac(self):
        assert hex_to_mac("001122334455") == "00:11:22:33:44:55"

    def test_lowercase_input(self):
        """Input lowercase hex should produce uppercase MAC."""
        assert hex_to_mac("aabbccddeeff") == "AA:BB:CC:DD:EE:FF"


# --- hex_to_ip ---

class TestHexToIp:
    def test_private_ip(self):
        """Little-endian 0x0101a8c0 -> 192.168.1.1."""
        assert hex_to_ip(0x0101A8C0) == "192.168.1.1"

    def test_localhost(self):
        """Little-endian 0x0100007f -> 127.0.0.1."""
        assert hex_to_ip(0x0100007F) == "127.0.0.1"

    def test_zero(self):
        assert hex_to_ip(0) == "0.0.0.0"


# --- process_int ---

class TestProcessInt:
    def test_signed_defaults_to_16_bits(self):
        """Per the docs, signed properties default to a 16-bit width."""
        assert process_int(0xFFFF, signed=True) == -1
        assert process_int(0x8000, signed=True) == -32768

    def test_signed_explicit_bits(self):
        assert process_int(0xFF, signed=True, bits=8) == -1

    def test_unsigned_positive_value(self):
        assert process_int(0x7FFF, signed=True) == 0x7FFF

    def test_scale(self):
        assert process_int(100, scale=10) == 10

    def test_signed_and_scale_combined(self):
        """Signed conversion happens before scaling."""
        assert process_int(0xFFFF, signed=True, scale=10) == -0.1

    def test_list_of_values(self):
        assert process_int([0xFFFF, 1], signed=True) == [-1, 1]


# --- str_to_json ---

class TestStrToJson:
    def test_basic_object(self):
        result = str_to_json("{i01:0x03ff}")
        assert isinstance(result, dict)
        assert "i01" in result

    def test_with_array(self):
        result = str_to_json("{i01:[1,2,3]}")
        assert isinstance(result, dict)
        assert result["i01"] == [1, 2, 3]

    def test_hex_value_parsed(self):
        result = str_to_json("{i01:0x03ff}")
        assert result["i01"] == 0x03FF

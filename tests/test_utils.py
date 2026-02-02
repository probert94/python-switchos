"""Unit tests for python_switchos.utils conversion functions."""

from typing import Literal

from python_switchos.utils import (
    hex_to_bool_list,
    hex_to_str,
    hex_to_option,
    hex_to_mac,
    hex_to_ip,
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

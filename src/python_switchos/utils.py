import re
import demjson3
from typing import List, Type, get_args

def hex_to_bool_list(value: int, length: int = 24) -> List[bool]:
    """Converts an integer into a list of booleans.

    Args:
        value: The integer to convert.
        length: Number of bits to represent (pads with leading zeros if needed).

    Returns:
        List of booleans of the specified length.
    """
    return [c == "1" for c in f"{value:0{length}b}"][::-1]

def hex_to_str(value: str) -> str:
    """Converts a hex-encoded string to a UTF-8 decoded string.

    Args:
        value: Hex string representing bytes.

    Returns:
        The UTF-8 decoded string.
    """
    return bytes.fromhex(value).decode().rstrip("\x00")

def hex_to_option(value: int, type: Type) -> str | None:
    """Converts an integer into an option of a given Literal type.

    Args:
        value: The integer index representing the option.
        type: A Literal type containing the possible options.

    Returns:
        The option corresponding to the index, or None if index is out of range.
    """
    options = get_args(type)
    idx = value
    return None if idx >= len(options) else options[idx]

def hex_to_mac(value: str) -> str:
    """Converts a hex string to a colon-separated MAC address.

    Args:
        value: Hex string representing the MAC address.

    Returns:
        The MAC address formatted with colons.
    """
    return ":".join(re.findall("..", value.upper()))

def hex_to_ip(value: int) -> str:
    """Converts an integer into its corresponding IPv4 address string.

    Args:
        value: Integer representing the IPv4 address (byteorder=little).

    Returns:
        The IPv4 address in dotted-decimal notation.
    """
    ip_bytes = value.to_bytes(4, byteorder="little")
    return ".".join(str(b) for b in ip_bytes)

def str_to_json(value: str) -> dict | None:
    """Parses a JSON-like string using demjson3 for tolerant decoding.

    Args:
        value: JSON-like string to parse.

    Returns:
        Parsed JSON as a dictionary, or None if parsing fails.
    """
    return demjson3.decode(value)

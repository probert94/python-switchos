import re
import demjson3
from typing import List, Type, get_args

def hex_to_bool_list(value: int | List[int], length: int = 24) -> List[bool]:
    """Converts an integer into a list of booleans.

    Args:
        value: The integer to convert. For more than 32 ports (SwOS only) the wire
            value is an array of two 32-bit numbers ``[high, low]``, with ports 0-31
            in ``low`` and ports 32+ in ``high``.
        length: Number of bits to represent (pads with leading zeros if needed).

    Returns:
        List of booleans of the specified length.
    """
    if isinstance(value, list):
        high, low = value
        value = (high << 32) | low
    return [c == "1" for c in f"{value:0{length}b}"][::-1]

def hex_to_str(value: str) -> str:
    """Converts a hex-encoded string to a decoded string.

    Args:
        value: Hex string representing bytes.

    Returns:
        The decoded string, truncated at the first NUL byte.
    """
    raw = bytes.fromhex(value).split(b"\x00", 1)[0]
    # SwOS Lite encodes non-ASCII characters as raw bytes (charCodeAt & 0xFF)
    # rather than UTF-8 sequences, so a strict UTF-8 decode can raise here.
    return raw.decode("utf-8", errors="replace")

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
    # Negative indices must not silently wrap around to the end of the list
    # (Python list semantics), they are just as out-of-range as idx >= len(options).
    return None if idx < 0 or idx >= len(options) else options[idx]

def hex_to_mac(value: str) -> str:
    """Converts a hex string to a colon-separated MAC address.

    Args:
        value: Hex string representing the MAC address.

    Returns:
        The MAC address formatted with colons.
    """
    return ":".join(re.findall("..", value.upper()))

def process_int(value: int | List[int], signed: bool = False, bits: int = None, scale: int | float = None) -> int | float | List[int] | List[float]:
    """Processes integer values with optional signed conversion and scaling.

    Args:
        value: The integer or list of integers to process.
        signed: Whether to treat the value as signed.
        bits: Number of bits for signed conversion (8, 16 or 32). Defaults to 16,
            matching the device's own default width for signed properties.
        scale: Divisor for scaling the value.

    Returns:
        The processed value(s).
    """
    if signed:
        bits = bits or 16
        half = 1 << (bits - 1)
        full = 1 << bits
        if isinstance(value, list):
            value = [v - full if v >= half else v for v in value]
        elif value >= half:
            value = value - full
    if scale is not None:
        if isinstance(value, list):
            value = [v / scale for v in value]
        else:
            value = value / scale
    return value

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

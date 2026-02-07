from dataclasses import fields, is_dataclass
from typing import ClassVar, List, Literal, Type, TypeVar, cast

from python_switchos.utils import (
    hex_to_bitshift_option,
    hex_to_bool_list,
    hex_to_bool_option,
    hex_to_dbm,
    hex_to_ip,
    hex_to_mac,
    hex_to_option,
    hex_to_partner_ip,
    hex_to_partner_mac,
    hex_to_sfp_type,
    hex_to_str,
    process_int,
    str_to_json,
)


def endpoint(path: str, *alternates: str):
    """Decorator to add an endpoint path and optional alternates to a class.

    Args:
        path: Primary endpoint path (e.g., "!stats.b")
        *alternates: Optional alternate paths (e.g., "stats.b")

    Example:
        @endpoint("!stats.b", "stats.b")  # Primary path with one alternate
        @endpoint("link.b")                # Primary path only
    """
    def decorator(cls):
        cls.endpoint_path = path
        cls.endpoint_alternates = list(alternates)
        return cls
    return decorator


class SwitchOSDataclass:
    """Base class for SwitchOS data structures."""
    pass


class SwitchOSEndpoint(SwitchOSDataclass):
    """Represents an endpoint of SwitchOS Lite with a path.

    Attributes:
        endpoint_path: Primary endpoint path (e.g., "!stats.b")
        endpoint_alternates: Optional list of alternate paths (e.g., ["stats.b"])
                            for devices that use different conventions.
                            SwOS Lite uses ! prefix, SwOS full 2.17+ omits it.
    """
    endpoint_path: ClassVar[str]
    endpoint_alternates: ClassVar[List[str]] = []


T = TypeVar("T", bound=SwitchOSEndpoint)
E = TypeVar("E", bound=SwitchOSDataclass)

FieldType = Literal["bool", "scalar_bool", "int", "uint64", "str", "option", "bool_option", "bitshift_option", "mac", "partner_mac", "ip", "partner_ip", "sfp_type", "dbm"]


def _parse_dict(cls: Type[E], json_data: dict, port_count: int) -> E:
    """Parse a dict into a dataclass instance, applying type transformations."""
    result = {}
    for f in fields(cls):
        metadata = f.metadata
        names = metadata.get("name")
        value = next((json_data.get(name) for name in names if name in json_data), None)
        if value is None:
            continue

        field_type: FieldType = cast(FieldType, metadata.get("type"))
        match field_type:
            case "bool":
                length = metadata.get("ports", port_count)
                value = hex_to_bool_list(value, length)
            case "scalar_bool":
                value = bool(value)
            case "int":
                value = process_int(value, metadata.get("signed"), metadata.get("bits"), metadata.get("scale"))
            case "uint64":
                high_name = metadata.get("high")
                high_value = json_data.get(high_name, 0)
                if isinstance(value, list):
                    high_list = high_value if isinstance(high_value, list) else [0] * len(value)
                    value = [lo + hi * (2**32) for lo, hi in zip(value, high_list)]
                else:
                    value = value + high_value * (2**32)
            case "str":
                if isinstance(value, list):
                    value = [hex_to_str(v) for v in value]
                else:
                    value = hex_to_str(value)
            case "option":
                options = metadata.get("options")
                if isinstance(value, list):
                    value = [hex_to_option(v, options) for v in value]
                else:
                    value = hex_to_option(value, options)
            case "bool_option":
                options = metadata.get("options")
                length = metadata.get("ports", port_count)
                value = hex_to_bool_option(value, options, length)
            case "bitshift_option":
                pair_name = metadata.get("pair")
                pair_value = json_data.get(pair_name, 0)
                options = metadata.get("options")
                length = metadata.get("ports", port_count)
                value = hex_to_bitshift_option(value, pair_value, options, length)
            case "mac":
                value = hex_to_mac(value)
            case "partner_mac":
                if isinstance(value, list):
                    value = [hex_to_partner_mac(v) for v in value]
                else:
                    value = hex_to_partner_mac(value)
            case "ip":
                value = hex_to_ip(value)
            case "partner_ip":
                if isinstance(value, list):
                    value = [hex_to_partner_ip(v) for v in value]
                else:
                    value = hex_to_partner_ip(value)
            case "sfp_type":
                if isinstance(value, list):
                    value = [hex_to_sfp_type(v) for v in value]
                else:
                    value = hex_to_sfp_type(value)
            case "dbm":
                scale = metadata.get("scale", 10000)
                if isinstance(value, list):
                    value = [hex_to_dbm(v, scale) for v in value]
                else:
                    value = hex_to_dbm(value, scale)

        result[f.name] = value
    return cls(**result)


def readDataclass(cls: Type[T], data: str) -> T:
    """Parse a JSON-like string into an endpoint dataclass instance."""
    if not is_dataclass(cls):
        raise TypeError(f"{cls} is not a dataclass")

    json_data = str_to_json(data)
    first_arr = next((v for v in json_data.values() if isinstance(v, list)), None)
    port_count = len(first_arr) if first_arr else 10

    return _parse_dict(cls, json_data, port_count)


def readListDataclass(cls: Type[E], data: str) -> List[E]:
    """Parse a JSON array string into a list of dataclass instances.

    Used for endpoints that return arrays of objects (e.g., host tables, VLANs).
    Entry classes should inherit from SwitchOSDataclass.
    Port count is auto-detected from array field lengths in the first entry.
    """
    if not is_dataclass(cls):
        raise TypeError(f"{cls} is not a dataclass")

    json_array = str_to_json(data)
    if not json_array:
        return []

    # Auto-detect port count from first entry's arrays (same as readDataclass)
    first_arr = next((v for v in json_array[0].values() if isinstance(v, list)), None)
    port_count = len(first_arr) if first_arr else 10

    return [_parse_dict(cls, item, port_count) for item in json_array]

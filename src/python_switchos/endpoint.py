from dataclasses import fields, is_dataclass
from typing import ClassVar, Literal, cast, List, Type, TypeVar
from python_switchos.utils import hex_to_bool_list, hex_to_ip, hex_to_mac, hex_to_option, hex_to_str, str_to_json

def endpoint(path: str):
    """Decorator to add an endpoint path to a class."""
    def decorator(cls):
        cls.endpoint_path = path
        return cls
    return decorator

class SwitchOSEndpoint:
    """Represents an abstract endpoint of SwitchOS Lite."""
    endpoint_path: ClassVar[str]

T = TypeVar("T", bound=SwitchOSEndpoint)

FieldType = Literal["bool", "str"]

def readDataclass(cls: Type[T], data: str) -> T:
    """Parses the given JSON-Like string and returns an instance of the given endpoint class."""
    if not is_dataclass(cls):
        raise TypeError(f"{cls} is not a dataclass")
    dict = {}
    jsonData = str_to_json(data)
    firstArrValue = next((v for v in jsonData.values() if isinstance(v, list)), None)
    portCount: int = len(firstArrValue) if isinstance(firstArrValue, list) else 0
    for f in fields(cls):
        metadata = f.metadata
        names = metadata.get("name")
        value = next((jsonData.get(name) for name in names if name in jsonData), None)
        if value is None:
            continue
        type: FieldType = cast(FieldType, metadata.get("type"))
        match type:
            case "bool":
                value = hex_to_bool_list(value, portCount)
            case "int":
                if metadata.get("signed") and metadata.get("bits"):
                    bits = metadata["bits"]
                    half = 1 << (bits - 1)
                    full = 1 << bits
                    if isinstance(value, list):
                        value = [v - full if v >= half else v for v in cast(List[int], value)]
                    elif value >= half:
                        value = value - full
                if isinstance(metadata.get("scale"), (int, float)):
                    if isinstance(value, list):
                        value = list(map(lambda v: v / metadata.get("scale"), cast(List[int], value)))
                    else:
                        value = value / metadata.get("scale")
            case "str":
                if isinstance(value, list):
                    value = list(map(hex_to_str, cast(List[str], value)))
                else:
                    value = hex_to_str(value)
            case "option":
                if isinstance(value, list):
                    value = list(map(lambda v: hex_to_option(v, metadata.get("options")), cast(List[int], value)))
                else:
                    value = hex_to_option(value, metadata.get("options"))
            case "bitshift_option":
                options = metadata.get("options")
                pair_id = metadata.get("pair")
                pair_value = jsonData.get(pair_id, 0) if pair_id else 0
                result = []
                v1, v2 = value, pair_value
                for _ in range(portCount):
                    idx = (v1 & 1) | ((v2 & 1) << 1)
                    result.append(options[idx] if idx < len(options) else None)
                    v1 >>= 1
                    v2 >>= 1
                value = result
            case "mac":
                value = hex_to_mac(value)
            case "ip":
                value = hex_to_ip(value)
        dict[f.name] = value
    return cls(**dict)

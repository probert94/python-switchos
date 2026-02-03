from dataclasses import fields, is_dataclass
from typing import ClassVar, Literal, cast, List, Type, TypeVar
from python_switchos.utils import hex_to_bool_list, hex_to_ip, hex_to_mac, hex_to_option, hex_to_str, process_int, str_to_json

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
                value = process_int(value, metadata.get("signed"), metadata.get("bits"), metadata.get("scale"))
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
            case "mac":
                value = hex_to_mac(value)
            case "ip":
                value = hex_to_ip(value)
        dict[f.name] = value
    return cls(**dict)

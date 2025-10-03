from dataclasses import dataclass, field
from typing import List, Literal
from python_switchos.endpoint import SwitchOSEndpoint, endpoint

# PoE output options matching the API’s integer order
PoEOut = Literal["on", "off", "auto"]

# Voltage level options matching the API’s integer order
VoltageLevel = Literal["auto", "low", "high"]

# State options matching the API’s integer order
State = Literal[
    None,
    "disabled",
    "waiting_for_load",
    "powered_on",
    "overload",
    "short_circuit",
    "voltage_too_low",
    "current_too_low",
    "power_cycle",
    "voltage_too_high",
    "controller_error"
]

@endpoint("poe.b")
@dataclass
class PoEEndpoint(SwitchOSEndpoint):
    """Represents the endpoint providing POE information for each individual port."""
    out: List[PoEOut] = field(metadata={"name": ["poe", "i01"], "type": "option", "options": PoEOut}, default=None)
    priority: List[int] = field(metadata={"name": ["prio", "i02"], "type": "int"}, default=None)
    voltage_level: List[VoltageLevel] = field(metadata={"name": ["lvl", "i03"], "type": "option", "options": VoltageLevel}, default=None)
    lldp_enabled: List[bool] = field(metadata={"name": ["lldp", "i0a"], "type": "bool"}, default=None)
    lldp_power: List[float] = field(metadata={"name": ["ldpw", "i0b"], "type": "int", "scale": 10}, default=None)
    state: List[State] = field(metadata={"name": ["poes", "i04"], "type": "option", "options": State}, default=None)
    current: List[int] = field(metadata={"name": ["curr", "i05"], "type": "int"}, default=None)
    voltage: List[float] = field(metadata={"name": ["volt", "i06"], "type": "int", "scale": 10}, default=None)
    power: List[float] = field(metadata={"name": ["pwr", "i07"], "type": "int", "scale": 10}, default=None)

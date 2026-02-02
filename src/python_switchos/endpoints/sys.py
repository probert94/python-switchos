from dataclasses import dataclass, field
from typing import Literal
from python_switchos.endpoint import SwitchOSEndpoint, endpoint

# Address acquisition options matching the API's integer order
AddressAcquisition = Literal["DHCP_FALLBACK", "STATIC", "DHCP"]

@endpoint("sys.b")
@dataclass
class SystemEndpoint(SwitchOSEndpoint):
    """Represents the endpoint with system information."""

    # General
    address_acquisition: AddressAcquisition = field(metadata={"name": ["iptp", "i0a"], "type": "option", "options": AddressAcquisition})
    static_ip: str = field(metadata={"name": ["ip", "i09"], "type": "ip"})
    ip: str = field(metadata={"name": ["cip", "i02"], "type": "ip"})
    identity: str = field(metadata={"name": ["id", "i05"], "type": "str"})
    serial: str = field(metadata={"name": ["sid", "i04"], "type": "str"})
    mac: str = field(metadata={"name": ["mac", "i03"], "type": "mac"})
    model: str = field(metadata={"name": ["brd", "i07"], "type": "str"})
    version: str = field(metadata={"name": ["ver", "i06"], "type": "str"})
    revision: str = field(metadata={"name": ["rev"], "type": "str"}, default=None)
    uptime: int = field(metadata={"name": ["upt", "i01"], "type": "int"}, default=None)

    # Health
    cpu_temp: int = field(metadata={"name": ["temp", "i22"], "type": "int", "signed": True, "bits": 16}, default=None)
    psu1_current: int = field(metadata={"name": ["p1c", "i16"], "type": "int"}, default=None)
    psu1_voltage: int = field(metadata={"name": ["p1v", "i15"], "type": "int", "scale": 100}, default=None)
    psu2_current: int = field(metadata={"name": ["p2c", "i1f"], "type": "int"}, default=None)
    psu2_voltage: int = field(metadata={"name": ["p2v", "i1e"], "type": "int", "scale": 100}, default=None)
    psu1_power: int = field(metadata={"name": ["p1p"], "type": "int", "scale": 10}, default=None)
    psu2_power: int = field(metadata={"name": ["p2p"], "type": "int", "scale": 10}, default=None)
    power_consumption: int = field(metadata={"name": ["i26"], "type": "int", "scale": 10}, default=None)

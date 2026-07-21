from dataclasses import dataclass, field
from typing import List

from python_switchos.endpoint import SwitchOSDataclass, SwitchOSEndpoint, endpoint


@dataclass
class HostEntry(SwitchOSDataclass):
    """A single entry in a host table (static or dynamic).

    Attributes:
        port: Switch port number (0-indexed)
        mac: MAC address in AA:BB:CC:DD:EE:FF format
    """
    port: int = field(metadata={"name": ["i02"], "type": "int"})
    mac: str = field(metadata={"name": ["i01"], "type": "mac"})


@endpoint("host.b")
@dataclass
class HostEndpoint(SwitchOSEndpoint):
    """Static host table endpoint.

    Contains statically configured MAC address entries.
    """
    entries: List[HostEntry] = field(default_factory=list)


@endpoint("!dhost.b")
@dataclass
class DynamicHostEndpoint(SwitchOSEndpoint):
    """Dynamic host table endpoint.

    Contains dynamically learned MAC address entries.
    """
    entries: List[HostEntry] = field(default_factory=list)

from dataclasses import dataclass, field
from typing import List
from python_switchos.endpoint import SwitchOSDataclass, SwitchOSEndpoint, endpoint


@dataclass
class VlanEntry(SwitchOSDataclass):
    """Represents a single VLAN configuration entry.

    Fields:
        vlan_id: VLAN ID number
        igmp_snooping: Whether IGMP snooping is enabled for this VLAN
        members: Port membership list (index=port, True=member)
    """
    vlan_id: int = field(metadata={"name": ["i01"], "type": "int"})
    igmp_snooping: bool = field(metadata={"name": ["i03"], "type": "scalar_bool"})
    members: List[bool] = field(metadata={"name": ["i02"], "type": "bool"})


@endpoint("vlan.b")
@dataclass
class VlanEndpoint(SwitchOSEndpoint):
    """Represents the VLAN configuration endpoint.

    Contains a list of configured VLANs with their port membership.
    """
    entries: List[VlanEntry] = field(default_factory=list)

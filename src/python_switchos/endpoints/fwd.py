"""Forwarding configuration endpoint for port isolation, mirroring, rate limits, and VLANs."""

from dataclasses import dataclass, field
from typing import List, Literal

from python_switchos.endpoint import SwitchOSEndpoint, endpoint


VlanMode = Literal["disabled", "optional", "strict"]
VlanReceive = Literal["any", "only tagged", "only untagged"]


@endpoint("fwd.b")
@dataclass
class ForwardingEndpoint(SwitchOSEndpoint):
    """Forwarding configuration from the fwd.b endpoint.

    Contains per-port forwarding settings in six categories:

    Port isolation matrix (10 fields):
        from_port_1 through from_port_10: Which ports can receive traffic
        from each source port (bitmask decoded to bool list)

    Port lock (2 fields):
        port_lock: Lock port MAC table
        lock_on_first: Lock on first learned MAC

    Mirroring (3 fields):
        mirror_ingress: Mirror incoming traffic
        mirror_egress: Mirror outgoing traffic
        mirror_to: Port is a mirror destination

    Rate limiting (3 fields):
        storm_rate: Broadcast storm rate limit
        ingress_rate: Ingress rate limit
        egress_rate: Egress rate limit

    Flood/limit (2 fields):
        limit_unknown_unicast: Limit unknown unicast flooding
        flood_unknown_multicast: Flood unknown multicast

    VLAN (4 fields):
        vlan_mode: VLAN mode (disabled/optional/strict)
        vlan_receive: VLAN receive filter (any/only tagged/only untagged)
        default_vlan_id: Default VLAN ID
        force_vlan_id: Force VLAN ID on ingress
    """

    # Port isolation matrix (10 source ports)
    from_port_1: List[bool] = field(metadata={"name": ["i01"], "type": "bool"})
    from_port_2: List[bool] = field(metadata={"name": ["i02"], "type": "bool"})
    from_port_3: List[bool] = field(metadata={"name": ["i03"], "type": "bool"})
    from_port_4: List[bool] = field(metadata={"name": ["i04"], "type": "bool"})
    from_port_5: List[bool] = field(metadata={"name": ["i05"], "type": "bool"})
    from_port_6: List[bool] = field(metadata={"name": ["i06"], "type": "bool"})
    from_port_7: List[bool] = field(metadata={"name": ["i07"], "type": "bool"})
    from_port_8: List[bool] = field(metadata={"name": ["i08"], "type": "bool"})
    from_port_9: List[bool] = field(metadata={"name": ["i09"], "type": "bool"})
    from_port_10: List[bool] = field(metadata={"name": ["i0a"], "type": "bool"})

    # Port lock fields
    port_lock: List[bool] = field(metadata={"name": ["i10"], "type": "bool"})
    lock_on_first: List[bool] = field(metadata={"name": ["i11"], "type": "bool"})

    # Port mirroring fields
    mirror_ingress: List[bool] = field(metadata={"name": ["i12"], "type": "bool"})
    mirror_egress: List[bool] = field(metadata={"name": ["i13"], "type": "bool"})
    mirror_to: List[bool] = field(metadata={"name": ["i14"], "type": "bool"})

    # Rate limiting fields
    storm_rate: List[int] = field(metadata={"name": ["i1a"], "type": "int"})
    ingress_rate: List[int] = field(metadata={"name": ["i1d"], "type": "int"})
    egress_rate: List[int] = field(metadata={"name": ["i1e"], "type": "int"})

    # Flood/limit fields
    limit_unknown_unicast: List[bool] = field(metadata={"name": ["i1b"], "type": "bool"})
    flood_unknown_multicast: List[bool] = field(metadata={"name": ["i1c"], "type": "bool"})

    # VLAN fields
    vlan_mode: List[str] = field(metadata={"name": ["i15"], "type": "option", "options": VlanMode})
    vlan_receive: List[str] = field(metadata={"name": ["i17"], "type": "option", "options": VlanReceive})
    default_vlan_id: List[int] = field(metadata={"name": ["i18"], "type": "int"})
    force_vlan_id: List[bool] = field(metadata={"name": ["i19"], "type": "bool"})

from dataclasses import dataclass, field
from typing import List, Literal
from python_switchos.endpoint import SwitchOSDataclass, SwitchOSEndpoint, endpoint


VlanMatch = Literal["any", "present", "not present"]
AccountAs = Literal["none", "#1", "#2", "#3", "#4"]


@dataclass
class AclEntry(SwitchOSDataclass):
    """Represents a single ACL rule entry.

    Fields:
        Port matching:
            from_ports: Source port mask (index=port, True=match)

        L2 matching:
            mac_src: Source MAC address ("" for any)
            mac_src_mask: Source MAC mask
            mac_dst: Destination MAC address ("" for any)
            mac_dst_mask: Destination MAC mask
            ethertype: Ethernet type value (0 for any)

        VLAN matching:
            vlan: VLAN presence match criteria
            vlan_id: VLAN ID to match (0 for any)
            priority: 802.1p priority to match

        IP matching:
            ip_src: Source IP address ("" for any)
            ip_src_prefix: Source IP prefix length
            ip_src_port: Source port number (0 for any)
            ip_dst: Destination IP address ("" for any)
            ip_dst_prefix: Destination IP prefix length
            ip_dst_port: Destination port number (0 for any)
            protocol: IP protocol number (0 for any)
            dscp: DSCP value to match

        Actions:
            drop: Whether to drop matching packets
            mirror_to: Port to mirror matching packets to (0 for none)
            redirect_to: Port to redirect matching packets to (0 for none)
            set_vlan_id: VLAN ID to set (0 for no change)
            set_priority: Priority to set
            set_dscp: DSCP to set

        Accounting:
            account_as: Counter to account packets to
    """
    # Port matching
    from_ports: List[bool] = field(metadata={"name": ["i01"], "type": "bool"})

    # L2 matching
    mac_src: str = field(metadata={"name": ["i02"], "type": "partner_mac"})
    mac_src_mask: str = field(metadata={"name": ["i03"], "type": "mac"})
    mac_dst: str = field(metadata={"name": ["i04"], "type": "partner_mac"})
    mac_dst_mask: str = field(metadata={"name": ["i05"], "type": "mac"})
    ethertype: int = field(metadata={"name": ["i06"], "type": "int"})

    # VLAN matching
    vlan: VlanMatch = field(metadata={"name": ["i07"], "type": "option", "options": VlanMatch})
    vlan_id: int = field(metadata={"name": ["i08"], "type": "int"})
    priority: int = field(metadata={"name": ["i09"], "type": "int"})

    # IP matching
    ip_src: str = field(metadata={"name": ["i0a"], "type": "partner_ip"})
    ip_src_prefix: int = field(metadata={"name": ["i0b"], "type": "int"})
    ip_src_port: int = field(metadata={"name": ["i0c"], "type": "int"})
    ip_dst: str = field(metadata={"name": ["i0d"], "type": "partner_ip"})
    ip_dst_prefix: int = field(metadata={"name": ["i0e"], "type": "int"})
    ip_dst_port: int = field(metadata={"name": ["i0f"], "type": "int"})
    protocol: int = field(metadata={"name": ["i10"], "type": "int"})
    dscp: int = field(metadata={"name": ["i11"], "type": "int"})

    # Actions
    drop: bool = field(metadata={"name": ["i12"], "type": "scalar_bool"})
    mirror_to: int = field(metadata={"name": ["i13"], "type": "int"})
    redirect_to: int = field(metadata={"name": ["i14"], "type": "int"})
    set_vlan_id: int = field(metadata={"name": ["i15"], "type": "int"})
    set_priority: int = field(metadata={"name": ["i16"], "type": "int"})
    set_dscp: int = field(metadata={"name": ["i17"], "type": "int"})

    # Accounting
    account_as: AccountAs = field(metadata={"name": ["i18"], "type": "option", "options": AccountAs})


@endpoint("acl.b")
@dataclass
class AclEndpoint(SwitchOSEndpoint):
    """Represents the ACL configuration endpoint.

    Contains a list of configured ACL rules with match criteria and actions.
    """
    entries: List[AclEntry] = field(default_factory=list)


@endpoint("!aclstats.b", "aclstats.b")
@dataclass
class AclStatsEndpoint(SwitchOSEndpoint):
    """ACL statistics from the !aclstats.b endpoint.

    Contains 4 counter arrays corresponding to the 4 ACL accounting buckets (#1-#4).
    Each counter is a list of 10 integers (one per port).

    Note: SwOS full uses aclstats.b (without ! prefix).

    Fields:
        counter_1: Packets matched by ACL rules with account_as="#1"
        counter_2: Packets matched by ACL rules with account_as="#2"
        counter_3: Packets matched by ACL rules with account_as="#3"
        counter_4: Packets matched by ACL rules with account_as="#4"
    """

    counter_1: List[int] = field(metadata={"name": ["i01"], "type": "int"})
    counter_2: List[int] = field(metadata={"name": ["i02"], "type": "int"})
    counter_3: List[int] = field(metadata={"name": ["i03"], "type": "int"})
    counter_4: List[int] = field(metadata={"name": ["i04"], "type": "int"})

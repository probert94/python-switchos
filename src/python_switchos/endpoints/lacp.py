"""LACP trunk configuration endpoint."""

from dataclasses import dataclass, field
from typing import List, Literal

from python_switchos.endpoint import SwitchOSEndpoint, endpoint

# LACP mode options from engine.js (line 1746): ["passive", "active", "static"]
LacpMode = Literal["passive", "active", "static"]


@endpoint("lacp.b")
@dataclass
class LacpEndpoint(SwitchOSEndpoint):
    """Represents the LACP trunk configuration for each port.

    Fields:
        mode: LACP mode per port (passive, active, or static trunk).
        group: LACP group number per port (0-15).
        trunk: Current trunk assignment per port (read-only).
        partner: Partner MAC address per port (empty string if no partner).
    """
    mode: List[LacpMode] = field(metadata={"name": ["i01"], "type": "option", "options": LacpMode})
    group: List[int] = field(metadata={"name": ["i03"], "type": "int"})
    trunk: List[int] = field(metadata={"name": ["i02"], "type": "int"})
    partner: List[str] = field(metadata={"name": ["i04"], "type": "partner_mac"})

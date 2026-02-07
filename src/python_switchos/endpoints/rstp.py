"""RSTP spanning tree state endpoint."""

from dataclasses import dataclass, field
from typing import List, Literal

from python_switchos.endpoint import SwitchOSEndpoint, endpoint

# RSTP Literal types from engine.js (lines 1867-1902)
RstpRole = Literal["disabled", "alternate", "root", "designated", "backup"]
RstpType = Literal["shared", "point-to-point", "edge"]
RstpState = Literal["discarding", "learning", "forwarding"]
RstpMode = Literal["STP", "RSTP"]


@endpoint("rstp.b")
@dataclass
class RstpEndpoint(SwitchOSEndpoint):
    """Represents the RSTP spanning tree state for each port.

    Fields:
        rstp: RSTP enabled per port (from bitmask i01).
        mode: STP/RSTP mode per port - "STP" if bit=0, "RSTP" if bit=1.
        role: Port role in spanning tree (disabled, alternate, root, designated, backup).
        root_path_cost: Root path cost per port.
        type: Port type (shared, point-to-point, edge) from combined i06/i07 bitmasks.
        state: Port state (discarding, learning, forwarding) from combined i08/i09 bitmasks.
    """
    rstp: List[bool] = field(metadata={"name": ["i01"], "type": "bool"})
    mode: List[str] = field(metadata={"name": ["i05"], "type": "bool_option", "options": RstpMode})
    role: List[RstpRole] = field(metadata={"name": ["i02"], "type": "option", "options": RstpRole})
    root_path_cost: List[int] = field(metadata={"name": ["i03"], "type": "int"})
    type: List[str] = field(metadata={"name": ["i06"], "type": "bitshift_option", "pair": "i07", "options": RstpType})
    state: List[str] = field(metadata={"name": ["i08"], "type": "bitshift_option", "pair": "i09", "options": RstpState})

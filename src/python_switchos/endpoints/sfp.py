from dataclasses import dataclass, field
from typing import List
from python_switchos.endpoint import SwitchOSEndpoint, endpoint


@endpoint("sfp.b")
@dataclass
class SfpEndpoint(SwitchOSEndpoint):
    """Represents the endpoint providing SFP module information and diagnostics.

    Each field is a list with one value per SFP port.
    """
    # Info fields
    vendor: List[str] = field(metadata={"name": ["i01"], "type": "str"})
    part_number: List[str] = field(metadata={"name": ["i02"], "type": "str"})
    revision: List[str] = field(metadata={"name": ["i03"], "type": "str"})
    serial: List[str] = field(metadata={"name": ["i04"], "type": "str"})
    date: List[str] = field(metadata={"name": ["i05"], "type": "str"})
    type: List[str] = field(metadata={"name": ["i06"], "type": "sfp_type"})

    # Diagnostic fields
    temperature: List[int] = field(metadata={"name": ["i08"], "type": "int"})
    voltage: List[float] = field(metadata={"name": ["i09"], "type": "int", "scale": 1000})
    tx_bias: List[int] = field(metadata={"name": ["i0a"], "type": "int"})
    tx_power: List[float] = field(metadata={"name": ["i0b"], "type": "dbm", "scale": 10000})
    rx_power: List[float] = field(metadata={"name": ["i0c"], "type": "dbm", "scale": 10000})

# `sfp.b` — SFP Module Information & Diagnostics

Backs the **SFP** page. Read-only; polled every 1 s. One record with one array element per
SFP/SFP+ cage (SwOS: `sfp` cages reported by `link.b`; Lite: compiled in — css610*/css606: 2–3,
ftc11xg/ftc21/gpen21: 1). The response may additionally contain a `nm` key (port-name
overrides, SwOS).

| Label | SwOS id | Lite id | Type | Access | Notes |
|---|---|---|---|---|---|
| Vendor | `vnd` | `i01` | str | RO | |
| Part Number | `pnr` | `i02` | str | RO | |
| Revision | `rev` | `i03` | str | RO | |
| Serial | `ser` | `i04` | str | RO | |
| Date | `dat` | `i05` | str | RO | manufacturing date as encoded in the module |
| Type | `typ` | `i06` | str | RO | module type; the firmware abbreviates and the UI expands: `&mmf` → `multi-mode fiber`, `&smf` → `single-mode fiber`, `&f` → `fiber`. SwOS Lite uses `{xx}` numeric escapes instead |
| Temperature | `tmp` | `i08` | int (32-bit SwOS / 8-bit-style Lite), °C | RO | `-128` = not available |
| Voltage | `vcc` | `i09` | uint, mV (scale 1000 → V) | RO | |
| Tx Bias | `tbs` | `i0a` | uint, mA | RO | |
| Tx Power | `tpw` | `i0b` | uint, 0.1 µW units, displayed as dBm (`10·log10(wire/10⁴)`) | RO | |
| Rx Power | `rpw` | `i0c` | uint, 0.1 µW units, displayed as dBm | RO | |

Notes:

* `i07` is unused/not exposed in any analyzed SwOS Lite build.
* On multi-cage devices every property is an array indexed by SFP cage (not by switch port);
  the cage-to-port mapping follows the port layout in [models.md](../models.md).
* gper14i has no SFP page.

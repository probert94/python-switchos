# `link.b` — Port Status & Configuration

Backs the **Link** page. One record; per-port values (see
[protocol.md](../protocol.md#per-port-values-inside-one-record)). Polled every 3 s.

Reading also returns the port-inventory keys used at boot time (read-only, SwOS only —
SwOS Lite compiles the port layout into the build):

| Key | Type | Meaning |
|---|---|---|
| `prt` | uint | total number of switch ports |
| `sfp` | uint | number of SFP/SFP+ cages |
| `sfpo` | uint | index of the first SFP port (defaults to `prt − sfp`) |
| `comb` | bool mask | ports that are combo ports |
| `qsfp` | bool mask | ports that are QSFP+ lanes |
| `qsfo` | uint | index of the first QSFP+ lane |
| `nm` (Lite: `i0a`) | str array | current per-port names (also a RW property below) |

## Properties

Access: RW = writable via POST, RO = status only.
Types: see [types.md](../types.md). "flag" values list their state strings.

| Label | SwOS id | Lite id | Type | Access | Availability / notes |
|---|---|---|---|---|---|
| Enabled | `en` | `i01` | bool (mask) | RW | all |
| Name | `nm` | `i0a` | str array | RW | all |
| Link Status | `lnk` (+ `paus`) | `i06` (+ `i15`) | flag: `no link`, `link on`, `no link`, `link paused` | RO | all. css106: `lnk` only (2 states: `no link`, `link on`) |
| PoE In | `poe` | `i0b` | flag: `off`/`on` (SwOS), `no power`/`power in` (Lite) | RO | SwOS: css318fi only (copper ports). Lite: css610 only (ports 1–7) |
| Block On No Power | `blkp` | `i0c` | bool (mask) | RW | SwOS: css318fi (copper ports). Lite: css610 (ports 1–7) |
| Combo Mode | `cm` | – | enum: `auto`, `copper`, `sfp` | RW | SwOS, only on combo ports (`comb` mask): CRS328-4C-20S-4S+, CRS312, css326xg |
| Type (QSFP+ mode) | `qtyp` | – | enum: `auto`, `40G`, `4x10G` | RW | SwOS, only on QSFP+ lanes (`qsfp` mask): css326q, css326xg, css354 |
| Auto Negotiation | `an` | `i02` | bool (mask) | RW | all |
| Speed (negotiated) | `spd` | `i08` | enum array | RO | all; shown while auto-negotiation is on |
| Speed (configured) | `spdc` | `i05` | enum array | RW | all; effective when auto-negotiation is off |
| Full Duplex (negotiated) | `dpx` | `i07` | flag: `no`, `yes` | RO | all; shown while auto-negotiation is on |
| Full Duplex (configured) | `dpxc` | `i03` | bool (mask) | RW | all; effective when auto-negotiation is off |
| Flow Control Tx (config) | `fctc` | `i16` | bool (mask) | RW | all except css354 and Lite ftc21/gpen21/gper14i. css106: single `fct` bool instead of the four flow-control properties |
| Flow Control Rx (config) | `fctr` | `i12` | bool (mask) | RW | ditto |
| Flow Control status | `tfct` (+ `rfct`) | `i13` (+ `i14`) | flag: `off`, `tx only`, `rx only`, `on` | RO | ditto |
| SFP Rate Select | `sfpr` | `i17` | enum: `low`, `high` | RW | SwOS: builds with SFP cages (hidden on QSFP lanes). Lite: css606 (SFP ports 4–6), css610out (SFP+ ports 9–10) |
| Hops | `hop` | `i0d` | uint array | RO (cable test) | SwOS: css318fi. Lite: css610, css610g, gpen21, gper14i |
| Last Hop | `hops` | `i0e` | enum: ``(none)``, `link ok`, `no link` | RO (cable test) | ditto |
| Length | `len` | `i0f` | uint array, meters | RO (cable test) | ditto |
| Fault At | `flt` | `i10` | uint array, meters | RO (cable test) | ditto |
| Cable Pairs | `pair` | `i11` | flags: 4 fields × 4 bits; `0` ok, `1` Short, `2` Open, `3` Reversed Polarity | RO (cable test) | ditto |

### Speed enumeration values

| Index | SwOS 2.18 | SwOS Lite | css106 |
|---|---|---|---|
| 0 | 10M | 10M | 10 |
| 1 | 100M | 100M | 100 |
| 2 | 1G | 1G | 1000 |
| 3 | 10G | 10G | – |
| 4 | 5G | 200M | – |
| 5 | 2.5G | 2.5G | – |
| 6 | 40G | 5G | – |

(The UI hides some entries per port medium; the wire values are the indices above.)

### Property relationships

* `spd`/`spdc` and `dpx`/`dpxc` are [combine](../types.md#combine--alternative-displayedit-pair-ui-level)
  pairs switched by `an` (auto-negotiation).
* `lnk`+`paus`, `tfct`+`rfct` are two-bit [flag](../types.md#flag--read-only-status-bit--bit-pair)
  pairs.
* Writing `nm` also changes the port labels used by every other page (and the `From Port…`
  row labels of Port Isolation).
* css106 PoE-out properties live on this endpoint instead of `poe.b` — see
  [poe.md](poe.md#css106-poe-on-linkb).

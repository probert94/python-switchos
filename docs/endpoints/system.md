# `sys.b` — System Settings, RSTP Bridge, Health

The largest endpoint. One record backing the **System** page, the bridge half of the
**RSTP** page and the **Health** page. Polled every 1 s while any of those pages is open.

## Boot / identification keys

Returned on every read; the UI reads them once at load time:

| Meaning | SwOS id | Lite id | Type | Access |
|---|---|---|---|---|
| Board name (e.g. `CSS326`) | `brd` | `i07` | str | RO |
| Firmware version (e.g. `2.18`) | `ver` | `i06` | str | RO |
| Build timestamp (unix) | `bld` | `i0b` | uint | RO |
| Hardware revision | `rev` | – | str | RO (present on some boards) |
| Marketing name | `mrkt` | `i2b` | str | RO (SwOS: some boards; Lite: css606/css610/css610out only) |
| PoE hardware indicator | `npoe` | – | uint | RO (SwOS; also selects fan/temp-sensor count on css354) |

## System page

| Label | SwOS id | Lite id | Type | Access | Availability / notes |
|---|---|---|---|---|---|
| Address Acquisition | `iptp` | `i0a` | enum: `DHCP with fallback`, `static`, `DHCP only` | RW | all |
| Static IP Address | `ip` | `i09` | ip | RW | all. **css106 id: `sip`** |
| Identity | `id` | `i05` | str | RW | all |
| Allow From (network) | `alla` | `i19` | ip | RW | composite `alla/allm` = allowed management network |
| Allow From (prefix) | `allm` | `i1a` | uint ≤ 32 | RW | |
| ETH/BOOT Port Enabled | `mgmt` | – | bool | RW | SwOS builds with a dedicated management port: CRS312 (runtime), css326q, css326xg, css354 |
| Allow From Ports | `allp` | `i12` | bool (port mask) | RW | all |
| Allow From VLAN | `avln` | `i1b` | uint ≤ 4095 | RW | all |
| Independent VLAN Lookup | `ivl` | – | bool | RW | SwOS & css106 only |
| IGMP Snooping | `igmp` | `i17` | bool | RW | not Lite ftc21/gpen21/gper14i |
| IGMP Querier | `igmq` | `i29` | bool | RW | ditto; UI clears it when snooping is off |
| IGMP Fast Leave | `igfl` | `i27` | bool (port mask) | RW | ditto |
| IGMP Version | `igve` | `i28` | enum: `v2`, `v3` | RW | ditto |
| Mikrotik Discovery Protocol | `pdsc` | `i08` | bool (port mask) | RW | all |
| Port1 PoE In Long Cable | `lcbl` | – | bool | RW | css106 (RB260GSP) only |
| Dark Mode | – | `i21` | bool | RW | gpen21 only (UI theme) |
| Power I/O | – | `i20` | enum: `in`, `out` | RO | gper14i only |
| Alarm | – | `i23` | enum: `inactive`, `active` | RO | css610out only |
| Serial Number | `sid` | `i04` | str | RO | all |
| MAC Address | `mac` | `i03` | mac | RO | all |
| Uptime | `upt` | `i01` | uptime — SwOS: centiseconds, Lite: seconds | RO | all |
| Trusted Ports (DHCP & PPPoE snooping) | `dtrp` | `i13` | bool (port mask) | RW | not css106, not Lite ftc21/gpen21/gper14i |
| Add Information Option | `ainf` | `i14` | bool | RW | ditto (DHCP option 82) |

### PoE Out (single-output devices)

On devices with one PoE output the mode/status live here instead of a PoE page:

| Label | SwOS id | Lite id | Type | Access | Availability |
|---|---|---|---|---|---|
| PoE Out Mode | `poe` | `i1c` | enum: `auto on`, `force on`, `off` | RW | Lite css610, gpen21 (present but compiled out in all SwOS 2.18 builds) |
| PoE Out Status | `poes` | `i1d` | enum: `waiting for load`, `powered on`, `overload`, `no load`, `powered on`, `overload`, `no load`, `has load`, `invalid load`, then 3 × `psu failed` (2.21; ≤ 2.20: `bat. low`) | RO | ditto |

## RSTP bridge settings

Shown on the **RSTP** page together with [`rstp.b`](rstp.md).

| Label | SwOS id | Lite id | Type | Access | Notes |
|---|---|---|---|---|---|
| Bridge Priority (hex) | `prio` | `i0e` | uint, UI radix 16, 4 digits | RW | |
| Port Cost Mode | `cost` | `i0f` | enum: `short`, `long` | RW | |
| Forward Reserved Multicast | `frmc` | `i2a` | bool | RW | disables per-port RSTP editing while set |
| Root Bridge | `rpr` + `rmac` | `i10` + `i11` | composite: uint (hex) + "." + mac | RO | current root bridge priority.MAC |

## Health page

All read-only except *Fan Target Temp*. Availability: see the per-build feature tables in
[models.md](../models.md).

| Label | SwOS id | Lite id | Type | Availability |
|---|---|---|---|---|
| CPU Temperature | `temp` | `i22` | int (32-bit), °C | all builds with Health |
| Board Temperature 1 / 2 | `btm1`, `btm2` | – | int, °C | SwOS, count per build (`fc` flag) |
| PHY Temperature | `phyt` | – | int, °C | css310g, css312, css326xg |
| FAN1–FAN4 | `fan1`…`fan4` | – | uint, RPM | SwOS, count per build/board |
| PSU1 / PSU2 (current @ voltage) | `p1c`+`p1v`, `p2c`+`p2v` | `i16`+`i15`, `i1f`+`i1e` | composite: uint mA @ uint 0.01 V | SwOS css318p, css328p, css354 (non-PoE); Lite css610pi (css610out: voltage `i15` only) |
| PSU1 / PSU2 status | `p1s`, `p2s` | – | enum: `failed`, `ok` | CSS317 & CRS328-4C-20S-4S+ (runtime), css312, css320p, css326xg, css354 |
| PSU1 / PSU2 voltage | `p1v`, `p2v` | – | uint, mV (css310, css326q) or 0.01 V (css320p) | per build |
| PSU1 / PSU2 fan | `p1f`, `p2f` | – | uint, RPM | css320p |
| PSU1 / PSU2 power | `p1p`, `p2p` | – | uint, 0.1 W | css320p |
| PSU1 / PSU2 temperature | `p1t`, `p2t` | – | int, 0.1 °C | css320p |
| Power Consumption | – | `i26` | uint, 0.1 W | Lite css610pi, css610out |
| Fan Target Temp (C) | `ftt` | – | int (32-bit), −273…65, **RW** | css310, css310g |
| Voltage | `volt` | – | uint, 0.1 V | css106 (RB260GSP) |
| Temperature | `temp` | – | int, °C | css106 (RB260GSP) |

css610out additionally has the battery/charger endpoint [`ups.b`](ups.md) on its Health page.

### Relationships

* `iptp` = `DHCP only` disables the *Static IP Address* field; on fallback mode the static
  address is used when DHCP fails.
* `alla`/`allm`, `allp` and `avln` combine into the management-access filter (network, ports
  and VLAN).
* The IGMP settings here control the snooping whose result appears in
  [`!igmp.b`](igmp.md).

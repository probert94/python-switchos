# Models, Builds & Port Layouts

Each firmware `.js` build targets one hardware model (or a small family). The build id is the
file name prefix (also used as the upgrade channel on `upgrade.mikrotik.com`). Where the
marketing name is not contained in the files, it is inferred from the hardware layout and
marked *(inferred)*; layouts themselves are taken directly from the code (port-name functions,
label overrides, visibility bounds and page definitions).

Port indices are 0-based on the wire; the UI labels them 1-based (`Port1`, `SFP2`, …).
Ports can be renamed by the user (`link.b` name array); the labels below are the defaults.

## SwOS 2.18

SwOS builds learn the port count at runtime from `link.b` (`prt`, `sfp`, `sfpo`, `comb`,
`qsfp`, `qsfo`) and the board name from `sys.b` (`brd`). The **generic build** (files
`css305`, `css309`, `css317`, `css326` are byte-identical) serves several boards and switches
features by board name at runtime.

| Build | Board(s) | Port layout (index → default label) |
|---|---|---|
| css106 | CSS106-5G-1S (RB260GS); CSS106-1G-4P-1S (RB260GSP) | 0–4 `Port1–5` (GbE), 5 `SFP`. RB260GSP: PoE out on ports 2–5 (indices 1–4), PoE in on Port1 |
| generic (css305/309/317/326) | CSS305/CRS305-1G-4S+ | 0 `ETH/BOOT` (GbE), 1–4 `SFP+1–4` *(SFP indices at runtime via `sfpo`)* |
| | CRS309-1G-8S+ | 0–7 `SFP+1–8`, 8 `ETH/BOOT` (GbE) |
| | CRS317-1G-16S+ | 0–15 `SFP+1–16`, 16 `ETH/BOOT`; 2 fans, Health |
| | CSS326-24G-2S+ / CRS326-24G-2S+ | 0–23 `Port1–24` (GbE), 24–25 `SFP1–2` (SFP+) |
| | CRS328-4C-20S-4S+ | 0–19 `SFP1–20`, 20–23 `COMBO1–4`, 24–27 `SFP+1–4` |
| | CRS312-4C+8XG | 0–7 `Port1–8` (10G copper), 8–11 `COMBO1–4` (10G/SFP+); separate mgmt `ETH/BOOT` port toggle; Health |
| css305r2 | CRS305-1G-4S+ rev. 2 | as CSS305 (build differs only in upgrade file prefix) |
| css310 | CRS310-1G-5S-4S+ *(inferred)* | 0 `ETH/BOOT` (GbE), 1–5 `SFP1–5`, 6–9 `SFP+1–4`; Health, PSU voltages, writable *Fan Target Temp* |
| css310g | CRS310-8G+2S+ *(inferred)* | 0–7 `Port1–8` (2.5G), 8–9 `SFP+1–2`; PHY temperature, writable *Fan Target Temp* |
| css312 | CRS312-4C+8XG (dedicated build) | as above; 4 fans, PHY temperature, PSU status |
| css318fi | CRS318-1Fi-15Fr-2S-OUT *(inferred)* | 0–15 copper (`Port1–16`; 15 reverse-PoE "Fr" + 1 "Fi"), 16–17 SFP; per-port **PoE In** status, *Block On No Power*, cable-test fields enabled |
| css318g | CSS318-16G-2S+ *(inferred)* | 0–15 `Port1–16` (GbE), 16–17 `SFP+1–2` |
| css318p | CRS318-16P-2S+OUT / netPower 16P *(inferred)* | 0–15 `Port1–16` (GbE, PoE out), 16–17 `SFP+1–2`; PoE page; PSU current@voltage in Health |
| css320p | CRS320-8P-8B-4S+ *(inferred)* | 0–15 `Port1–16` (PoE out; 8×af/at + 8×bt), 16 `ETH/BOOT`, 17–20 `SFP+1–4`; numeric PoE priority, **PoE Standard** field, PoE LLDP; 3 fans; PSU voltage/fan/power/temperature |
| css326q | CRS326-24S+2Q+ *(inferred)* | 0–23 `SFP+…` (via runtime names), 24–31 `QSFP+1.1–2.4` (2 × 4 lanes); 3 fans; PSU voltages |
| css326xg | CRS326-4C+20G+2Q+ *(inferred)* | 0–19 copper, 20–23 `COMBO1–4`, 24–31 `QSFP+1.1–2.4`; mgmt `ETH/BOOT` toggle; 2 fans, 2 board temps, PHY temp, PSU status |
| css328 | CRS328-4C-20S-4S+ (dedicated build) | as generic CRS328 layout; 2 fans, Health |
| css328p | CRS328-24P-4S+ *(inferred)* | 0–23 `Port1–24` (GbE, PoE out), 24–27 `SFP+1–4`; PoE LLDP; 2 fans; PSU current@voltage |
| css354 | CRS354-48G-4S+2Q+ / CRS354-48P-4S+2Q+ *(inferred)* | 0–47 `Port1–48` (GbE; "P": PoE out), 48–51 `SFP+…`, 52–59 `QSFP+1.1–2.4`; numeric PoE priority; flow-control fields disabled; 4 fans (3 on PoE variant), mgmt `ETH/BOOT` toggle, PSU status |

Ports > 32 (css354): port bitmasks become `[high, low]` arrays, see
[types.md](types.md#bool--boolean--port-bitmask).

### SwOS feature flags per build

The 2.18 builds only differ in which properties are compiled in/out (everything else is
identical):

| Build | Health tab | PoE page (`poe.b`) | PoE LLDP | PoE In/cable-test on Link | Extra Health fields |
|---|---|---|---|---|---|
| generic, css305r2, css318g | runtime (CSS317/CSS312: yes) | no | – | no | PSU status (CSS317 & CRS328-4C-20S-4S+ at runtime) |
| css310 | yes | no | – | no | PSU1/2 voltage (mV), Fan Target Temp (RW) |
| css310g | yes | no | – | no | PHY temp, Fan Target Temp (RW) |
| css312 | yes | no | – | no | PHY temp, PSU1/2 status |
| css318fi | yes¹ | yes | no | **yes** (PoE In, Block On No Power, Hops, Last Hop, Length, Fault At, Cable Pairs) | – |
| css318p | yes¹ | yes | no | no | PSU1/2 current @ voltage |
| css320p | yes | yes (numeric priority, no voltage level, + PoE Standard) | yes | no | PSU1/2 status, voltage (0.01 V), fan, power, temperature |
| css326q | yes | no | – | no | PSU1/2 voltage (mV) |
| css326xg | yes | no | – | no | PHY temp, PSU1/2 status |
| css328 | yes | no | – | no | – |
| css328p | yes | yes | yes | no | PSU1/2 current @ voltage |
| css354 | yes | yes (numeric priority) | no | no | PSU1/2 current @ voltage (non-PoE variant), PSU status |

¹ Health tab is enabled whenever the build/board has fans or PoE.

The `poe.b` page is created only when `sys.b` reports `npoe == 0` **and** the build has PoE
support (on `npoe > 0` hardware the UI variant differs; css354 uses `npoe` to pick fan/temp
counts).

## SwOS Lite (2.19 – 2.21)

Port counts are compiled into each build. In dynamic-host and ACL contexts, port values
`0x81`–`0x8F` mean `Trunk1`–`Trunk15` (LAG groups).

| Build | Marketing name | Ports (index → default label) | PoE / power features |
|---|---|---|---|
| css606 (2.21 only) | not embedded in files (3×GbE + 3×SFP+ outdoor unit) | 0–2 `Port1–3` (GbE), 3–5 `SFP+1–3` | PoE out on ports 2–3 (`poeoutports.b`), 3 DC outputs (`dco.b`), SFP rate select |
| css610 | CSS610-8G-2S+(IN) | 0–7 `Port1–8` (GbE), 8–9 `SFP+1–2` | PoE In status on ports 1–7; single PoE Out (mode/status on `sys.b`) |
| css610g | CSS610-8G-2S+ variant *(inferred)* | 0–7 `Port1–8`, 8–9 `SFP+1–2` | none |
| css610out (2.21 only) | not embedded (outdoor 8-port PoE unit with battery/UPS) | 0–7 `Port1–8` (GbE, PoE out), 8–9 `SFP+1–2` | Full `poe.b` (8 ports), SFP rate select, UPS/charger (`ups.b`), alarm, PSU voltage & power consumption |
| css610pi | CSS610-8P-2S+(IN) *(inferred)* | 0–7 `Port1–8` (GbE, PoE out), 8–9 `SFP+1–2` | Full `poe.b` (8 ports); dual PSU health |
| ftc11xg | FTC11XG (10G fiber-to-copper converter) | 0–1 `Port1–2` (copper), 2 `SFP+1` | none |
| ftc21 | FTC21 (GbE fiber-to-copper converter) | 0–1 `Port1–2`, 2 `SFP1` | none |
| gpen21 | GPEN21 (Gigabit passive-ethernet injector) | 0–1 `Port1–2`, 2 `SFP1` | single PoE Out (mode/status on `sys.b`); *Dark Mode* UI setting |
| gper14i | not embedded (4-port PoE repeater, GPeR family) | 0–3 `Port1–4` (GbE) | PoE out on ports 2–4 (`poeoutports.b`); *Power I/O* direction field |

### SwOS Lite page availability per build

| Page (endpoint) | css606 | css610 | css610g | css610out | css610pi | ftc11xg | ftc21 | gpen21 | gper14i |
|---|---|---|---|---|---|---|---|---|---|
| Link (`link.b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| PoE (`poe.b`/`poeoutports.b`) | ✔ (pop) | – | – | ✔ (poe) | ✔ (poe) | – | – | – | ✔ (pop) |
| DC Out (`dco.b`) | ✔ | – | – | – | – | – | – | – | – |
| SFP (`sfp.b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | – |
| Port Isolation (`fwd.b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | – | – | – |
| LAG (`lacp.b`) | ✔ | ✔ | ✔ | ✔ | ✔ | – | – | – | – |
| Forwarding (`fwd.b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| RSTP (`sys.b`+`rstp.b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | – | – | – |
| Stats/Errors/Hist (`!stats.b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| VLAN (`fwd.b`) / VLANs (`vlan.b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| Hosts (`host.b`/`!dhost.b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| IGMP (`!igmp.b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | – | – | – |
| SNMP (`snmp.b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |
| ACL (`acl.b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ (reduced) | ✔ (reduced) | ✔ (reduced) |
| ACL Stats (`!aclstats.b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | – | – | – |
| Health (`sys.b`) | ✔ | ✔ | ✔ | ✔ (+`ups.b`) | ✔ | ✔ | – | – | – |
| System (`sys.b`) | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |

"reduced" ACL: ftc21/gpen21/gper14i lack *Account as*, *Redirect To*, *Mirror To* and the
DSCP set-action (see [endpoints/acl.md](endpoints/acl.md)).

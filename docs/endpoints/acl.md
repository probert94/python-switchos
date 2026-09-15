# `acl.b` / `!aclstats.b` — Access Control Lists

Backs the **ACL** page. `acl.b` is a **list endpoint** (max 32 rules); rule order matters.
Polled every 1 s on SwOS (for the hit counters); SwOS Lite polls the separate `!aclstats.b`
instead.

Each rule consists of **match** conditions and **actions**. Unset matches use sentinel
defaults (see notes below the table).

## Rule properties (`acl.b`)

| Label | SwOS id | Lite id | Type | Access | Availability / notes |
|---|---|---|---|---|---|
| From (ports) | `frm` | `i01` | bool (port mask) | RW | default: all ports |
| Hits | `pkts` | – | uint | RO | SwOS 2.18 only (per-rule packet counter; reset via `POST /resetacl`) |
| Account as | – | `i18` | enum: `none`, `#1`, `#2`, `#3`, `#4` | RW | Lite (not ftc21/gpen21/gper14i); selects the [`!aclstats.b`](#aclstatsb--acl-counters) counter fed by this rule |
| MAC Src | `smac` | `i02` | mac | RW | with mask `smsk` / `i03` (default `ffffffffffff`) |
| MAC Src Mask | `smsk` | `i03` | mac | RW | |
| MAC Dst | `dmac` | `i04` | mac | RW | with mask `dmsk` / `i05` |
| MAC Dst Mask | `dmsk` | `i05` | mac | RW | |
| Ethertype | `et` | `i06` | uint (UI: hex) | RW | |
| VLAN | `vtag` | `i07` | enum: `any`, `present`, `not present` | RW | css106 id: `vlan` |
| VLAN ID | `vlan` | `i08` | uint ≤ 4095 | RW | css106: range `vidl`–`vidh` |
| Priority | `prio` | `i09` | uint ≤ 7, default 8 = any | RW | |
| IP Src | `sip` | `i0a` | ip | RW | composite `ip/mask:port` |
| IP Src Mask | `sipm` | `i0b` | uint ≤ 32 (prefix len) | RW | |
| Src Port (L4) | `sprt` | `i0c` | uint ≤ 65535 | RW | css106: range `sptl`–`spth` |
| IP Dst | `dip` | `i0d` | ip | RW | |
| IP Dst Mask | `dipm` | `i0e` | uint ≤ 32 | RW | |
| Dst Port (L4) | `dprt` | `i0f` | uint ≤ 65535 | RW | css106: range `dptl`–`dpth` |
| Protocol | `prot` | `i10` | uint ≤ 255 | RW | IP protocol number |
| DSCP (match) | `dscp` | `i11` | uint ≤ 63, default 64 = any | RW | |
| **Actions** | | | | | |
| Redirect (enable) | `redr` | – | bool | RW | SwOS 2.18; css106: `snde` |
| Redirect To | `rdto` | `i14` | SwOS: enum (port); Lite: enum (port list + `none`, default = `none`); css106: port mask `snd` | RW | not Lite ftc21/gpen21/gper14i |
| Mirror | `mirr` | – | bool | RW | SwOS & css106 (mirrors to the `fwd.b` mirror target) |
| Mirror To | – | `i13` | enum (port list + `none`, default `none`) | RW | Lite (not ftc21/gpen21/gper14i) |
| Drop | `drop` | `i12` | bool | RW | not css106 |
| Rate | `rate` | – | uint, kbit/s (UI accepts `k/M/G`) | RW | SwOS & css106 only |
| Set VLAN ID | `svid` | `i15` | uint ≤ 4095 | RW | |
| Set Priority | `spri` | `i16` | uint ≤ 7, default 8 = don't set | RW | |
| Set DSCP | – | `i17` | uint ≤ 63, default 64 = don't set | RW | Lite (not ftc21/gpen21/gper14i) |

### Sentinel defaults ("not used" values)

| Property | Default (= match anything / action off) |
|---|---|
| `smsk`, `dmsk` | `ffffffffffff` (only in combination with all-zero `smac`/`dmac` = no MAC match) |
| `prio`, `spri` | `8` |
| `dscp`, set-DSCP | `64` |
| `frm` | all-ports mask |
| Lite `i13`/`i14` | index = port count (the extra `none` entry) |
| everything else | `0` = unset |

## `!aclstats.b` — ACL counters

SwOS Lite only (not ftc21/gpen21/gper14i). Read-only; polled every 1 s; reset via
`POST /resetstats`.

| Label | Lite id | Type | Notes |
|---|---|---|---|
| Counter #1–#4 | `i01`–`i04` | uint array (per port) | packets matched by rules whose *Account as* is `#1`…`#4` |

SwOS 2.18 instead exposes a per-rule `pkts` counter directly in `acl.b` and resets it with
`POST /resetacl` (body `*`).

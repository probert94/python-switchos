# `fwd.b` — Forwarding, Port Isolation, Rate Limits, Per-Port VLAN

One endpoint backing **three** UI pages: *Port Isolation*, *Forwarding* and *VLAN*
(the per-port VLAN settings — the VLAN *table* is [`vlan.b`](vlans.md)). One record; per-port
bitmasks/arrays. Not polled (read once, then written on Apply).

## Port isolation matrix

| Label | SwOS id | Lite id | Type | Access | Notes |
|---|---|---|---|---|---|
| From Port *n* (n = 1…N) | `fp1` … `fpN` | `i01` … `i0N` (hex: port 10 → `i0a`) | bool (mask) | RW | `fpn` bit *p* = forwarding allowed from port *n* (1-based) to port *p* (0-based). Default: everything allowed except the port itself |

The full matrix is N properties × N bits. css106 exposes the same `fp1`–`fp6` ids on its
*Forwarding* page. Not available on Lite ftc21/gpen21/gper14i.

## Forwarding page

| Label | SwOS id | Lite id | Type | Access | Availability / notes |
|---|---|---|---|---|---|
| Port Lock | `lck` | `i10` | bool (mask) | RW | all |
| Lock On First | `lckf` | `i11` | bool (mask) | RW | all |
| Set As Uplink Port | – | `i1f` | bool, radio (single port bit) | RW | Lite ftc21, gpen21, gper14i only |
| Mirror Ingress | `imr` | `i12` | bool (mask) | RW | not on Lite ftc21/gpen21/gper14i |
| Mirror Egress | `omr` | `i13` | bool (mask) | RW | ditto |
| Mirror To | `mrto` | `i14` | bool, radio (single port bit) | RW | ditto |
| Storm Rate | `srt` | `i1a` | SwOS: uint 1–100 (**percent**). Lite: uint, unit 100 kbit/s, max 65535 | RW | not css106 |
| Limit Unknown Unicast | `suni` | `i1b` | bool (mask) | RW | not css106 |
| Flood Unknown Multicast | `fmc` | `i1c` | bool (mask) | RW | not css106, not Lite ftc21/gpen21/gper14i |
| Ingress Rate | `ir` | `i1d` | SwOS: uint, kbit/s (UI accepts `k/M/G`). Lite: uint, unit 100 kbit/s, max 65535 | RW | not css106 |
| Egress Rate | `or` (css106) | `i1e` | css106: uint, metric. Lite: uint, unit 100 kbit/s | RW | **not** in SwOS 2.18 (css106 and Lite only) |

## VLAN page (per-port VLAN behaviour)

| Label | SwOS id | Lite id | Type | Access | Notes |
|---|---|---|---|---|---|
| VLAN Mode | `vlan` | `i15` | enum — SwOS/css106: `disabled`, `optional`, `enabled`, `strict`; Lite: `disabled`, `optional`, `strict` | RW | per port |
| VLAN Receive | `vlni` | `i17` | enum: `any`, `only tagged`, `only untagged` | RW | per port |
| Default VLAN ID | `dvid` | `i18` | uint array, 1–4095 | RW | per port |
| Force VLAN ID | `fvid` | `i19` | bool (mask) | RW | per port |
| VLAN Header (egress) | `vlnh` | – | enum: `leave as is`, `always strip`, `add if missing` | RW | **css106 only** — newer firmware moves egress tagging to the VLAN table membership (`vlan.b`) |

### Relationships

* `dvid` is applied to untagged ingress traffic; `fvid` forces it even on tagged traffic.
* `mrto`/`i14` (and `i1f`) are radio-style bitmasks: exactly one bit set.
* The ACL action *Mirror* ([acl.md](acl.md)) sends to the same `mrto` mirror target.

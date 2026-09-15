# `vlan.b` — VLAN Table

Backs the **VLANs** page. **List endpoint**: `GET` returns `[{...},{...}]`, `POST` replaces
the whole table (max 250 entries). Not polled.

| Label | SwOS id | Lite id | Type | Access | Availability / notes |
|---|---|---|---|---|---|
| VLAN ID | `vid` | `i01` | uint, 1–4094 | RW | key column (client-side unique check) |
| Name | `nm` | – | str | RW | SwOS 2.18 only |
| Port Isolation | `piso` | – | bool | RW | SwOS 2.18 only; default on |
| Learning | `lrn` | – | bool | RW | SwOS 2.18 only; default on |
| Mirror | `mrr` | – | bool | RW | SwOS 2.18 only |
| IGMP Snooping | `igmp` | `i03` | bool | RW | SwOS 2.18, css106, Lite (not ftc21/gpen21/gper14i) |
| IVL | `ivl` | – | bool | RW | css106 only (independent VLAN lookup per VLAN) |
| Members | `mbr` | `i02` | bool (port mask) | RW | default `0x0FFFFFFF` (all ports); SwOS 2.18 & Lite |
| Members / tagging | `prt` | – | enum array per port: `leave as is`, `always strip`, `add if missing`, `not a member` | RW | **css106 only** — combines membership and egress tagging per port |

### Relationships

* Which traffic lands in a VLAN is controlled per port on
  [`fwd.b`](forwarding.md#vlan-page-per-port-vlan-behaviour) (`vlan` mode, `vlni` receive,
  `dvid` default VLAN, `fvid` force).
* On css106, egress tagging is per VLAN/port here (`prt`); on the newer firmware `mbr` is a
  plain membership mask.
* `unique` on *VLAN ID* is client-side validation only; the device accepts what it is sent
  (rows are positional).

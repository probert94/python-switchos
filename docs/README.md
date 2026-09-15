# MikroTik SwOS / SwOS Lite Web API Documentation

## About

This documentation was reverse-engineered by Claude Code **exclusively** using the frontend files contained in the following MikroTik firmware builds:

| Family | Firmware versions analyzed | Builds |
|---|---|---|
| **SwOS** | 2.18 | css106, css305, css305r2, css309, css310, css310g, css312, css317, css318fi, css318g, css318p, css320p, css326, css326q, css326xg, css328, css328p, css354 |
| **SwOS Lite** | 2.19, 2.20, 2.21 | css606 (2.21), css610, css610g, css610out (2.21), css610pi, ftc11xg, ftc21, gpen21, gper14i |

The web UI is a single-page application: it downloads the device state as one object per
*endpoint* (`GET /link.b`, `GET /sys.b`, …) and applies configuration by `POST`ing a partial
object back to the same endpoint. There is **no REST semantics** — each endpoint is a flat
key/value record (or a list of records) covering one functional area.

## Document index

| Document | Contents |
|---|---|
| [protocol.md](protocol.md) | Transport, serialization format, authentication, maintenance/action endpoints, password-change hash algorithm |
| [types.md](types.md) | Property data types and exactly how values are encoded/decoded (bitmasks, enums, scaled numbers, MAC, IP, strings, 64-bit counters, combined properties) |
| [models.md](models.md) | Per-model port layout (Ethernet/SFP/SFP+/QSFP+/combo/PoE/DC out) and feature matrix |
| [endpoints/link.md](endpoints/link.md) | `link.b` — port status & configuration |
| [endpoints/poe.md](endpoints/poe.md) | `poe.b`, `poeoutports.b`, `dco.b` — PoE out & DC out |
| [endpoints/sfp.md](endpoints/sfp.md) | `sfp.b` — SFP module info & DDM |
| [endpoints/forwarding.md](endpoints/forwarding.md) | `fwd.b` — port isolation, lock, mirroring, rate limits, per-port VLAN settings |
| [endpoints/lag.md](endpoints/lag.md) | `lacp.b` — link aggregation |
| [endpoints/rstp.md](endpoints/rstp.md) | `rstp.b` — (R)STP per-port status/config |
| [endpoints/statistics.md](endpoints/statistics.md) | `stats.b` / `!stats.b` — counters, error counters, histograms |
| [endpoints/vlans.md](endpoints/vlans.md) | `vlan.b` — VLAN table |
| [endpoints/hosts.md](endpoints/hosts.md) | `host.b`, `!dhost.b` — static and learned MAC hosts |
| [endpoints/igmp.md](endpoints/igmp.md) | `!igmp.b` — IGMP snooping groups |
| [endpoints/snmp.md](endpoints/snmp.md) | `snmp.b` — SNMP agent settings |
| [endpoints/acl.md](endpoints/acl.md) | `acl.b`, `!aclstats.b` — access control list rules & counters |
| [endpoints/system.md](endpoints/system.md) | `sys.b` — system settings, identity/IP, IGMP, RSTP bridge settings, health |
| [endpoints/ups.md](endpoints/ups.md) | `ups.b` — battery/charger status (css610out only) |
| [endpoints/maintenance.md](endpoints/maintenance.md) | Action endpoints: reboot, reset, backup, firmware upgrade, counter resets, logout |

## The two firmware families in one page

Both families share the same architecture and (mostly) the same functionality, but they differ
in one crucial way:

* **SwOS** uses **readable property ids** (`en`, `nm`, `lnk`, `vid`, …).
* **SwOS Lite** uses **opaque, per-endpoint numbered ids** (`i01`, `i02`, … `i2c`). The same id
  means *different things on different endpoints* (e.g. `i01` is *Enabled* on `link.b` but
  *Uptime* on `sys.b`).

Every property table in [endpoints/](endpoints/) therefore has two id columns — one for SwOS
and one for SwOS Lite.

A second difference: within SwOS 2.18, the build `css106` (CSS106-5G-1S / RB260GS,
CSS106-1G-4P-1S / RB260GSP) is an older UI generation. It shares the readable SwOS ids but has a
few deviating ids and endpoint shapes; these deviations are called out explicitly in the tables
(*"css106:"* notes).

## How the UI pages map to endpoints

One endpoint often backs several UI pages, and one UI page may combine two endpoints:

| UI page (tab) | SwOS endpoint(s) | SwOS Lite endpoint(s) |
|---|---|---|
| Link | `link.b` | `link.b` |
| PoE | `poe.b` | `poe.b` (css610pi/css610out), `poeoutports.b` (css606/gper14i) |
| DC Out | – | `dco.b` (css606) |
| SFP | `sfp.b` | `sfp.b` |
| Port Isolation | `fwd.b` | `fwd.b` |
| LAG | `lacp.b` | `lacp.b` |
| Forwarding | `fwd.b` | `fwd.b` |
| RSTP | `sys.b` (bridge part) + `rstp.b` (per-port part) | same |
| Stats / Errors / Hist | `stats.b` (read + reset flags) | `!stats.b` (read-only) |
| VLAN (per port) | `fwd.b` | `fwd.b` |
| VLANs (table) | `vlan.b` | `vlan.b` |
| Hosts | `host.b` (static) + `!dhost.b` (learned) | same |
| IGMP | `!igmp.b` | `!igmp.b` |
| SNMP | `snmp.b` | `snmp.b` |
| ACL | `acl.b` | `acl.b` (+ `!aclstats.b` counters) |
| System / Health | `sys.b` | `sys.b` (+ `ups.b` on css610out) |
| Upgrade / Backup / Password | action endpoints, see [maintenance.md](endpoints/maintenance.md) | same |

Endpoints whose name starts with `!` (`!stats.b`, `!dhost.b`, `!igmp.b`, `!aclstats.b`,
`!pwd.b`) are treated as **read-only data feeds** by the UI (`!pwd.b` being the exception — it
is a write-only action, see [maintenance.md](endpoints/maintenance.md)).

## Firmware version differences (SwOS Lite 2.19 → 2.21)

The page/property definitions are **identical** across 2.19, 2.20 and 2.21 with only two
exceptions:

1. **2.20 → 2.21** — the *PoE Out Status* enumeration on `sys.b` (css610, gpen21) renamed its
   last three states from `bat. low` to `psu failed`.
2. **2.20 → 2.21 (gper14i)** — the PoE page (`poeoutports.b`) gained *PoE LLDP Enabled* (`i03`)
   and *PoE LLDP Power* (`i04`).

css606 and css610out only exist as 2.21 builds in the analyzed set. All remaining differences
between version files are JavaScript minifier renames without functional impact.

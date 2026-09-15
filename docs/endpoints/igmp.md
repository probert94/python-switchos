# `!igmp.b` — IGMP Snooping Groups

Backs the **IGMP** page (css106: *IGMP Groups*). Read-only **list endpoint**; polled every
5 s. Not available on Lite ftc21/gpen21/gper14i.

| Label | SwOS id | Lite id | Type | Notes |
|---|---|---|---|---|
| Group Address | `addr` | `i01` | ip | multicast group |
| VLAN | `vlan` | `i03` | uint | |
| Member Ports | `prts` | `i02` | bool (port mask) | |

IGMP snooping itself is enabled globally on [`sys.b`](system.md) (`igmp`/`i17`, plus querier,
fast-leave and version settings) and per VLAN on [`vlan.b`](vlans.md).

# `lacp.b` — Link Aggregation (LAG)

Backs the **LAG** page. One record; per-port arrays/masks. Polled every 3 s.
Not available on css106 and Lite ftc11xg/ftc21/gpen21/gper14i.

| Label | SwOS id | Lite id | Type | Access | Notes |
|---|---|---|---|---|---|
| Mode | `mode` | `i01` | enum: `passive`, `active`, `static` | RW | per port |
| Group | `sgrp` | `i03` | uint array, 0–15 | RW | static-LAG group; only meaningful when Mode = `static` |
| Trunk | `grp` | `i02` | uint array | RO | trunk/aggregation group the port currently belongs to |
| Partner | `mac` | `i04` | mac array | RO | LACP partner system MAC (all-zero = none) |

### Relationships

* Trunk numbers appear elsewhere as pseudo-port values `0x80 + n` (`Trunk1`–`Trunk15`), e.g.
  in the dynamic host table ([hosts.md](hosts.md)).
* The UI shows *Group* only for ports whose Mode is `static`; `passive`/`active` use LACP
  negotiation instead.

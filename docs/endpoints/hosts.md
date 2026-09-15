# `host.b` / `!dhost.b` — MAC Host Table

Backs the **Hosts** page: static entries (`host.b`, RW list) and the learned/dynamic table
(`!dhost.b`, read-only list, polled 1 s SwOS / 2 s Lite).

## `host.b` — static hosts (list endpoint)

Max 12 entries on SwOS Lite. `POST` replaces the whole list.

| Label | SwOS id | Lite id | Type | Access | Notes |
|---|---|---|---|---|---|
| Port | `prt` | `i02` | enum (port index) | RW | css106: bool port **mask** instead of an index |
| MAC | `adr` | `i01` | mac | RW | |
| VLAN ID | `vid` | – | uint, 1–4095 (default 1) | RW | SwOS & css106 only |
| Drop | `drp` | – | bool | RW | SwOS & css106 only |
| Mirror | `mir` | – | bool | RW | SwOS & css106 only |

## `!dhost.b` — dynamic (learned) hosts (read-only list)

| Label | SwOS id | Lite id | Type | Notes |
|---|---|---|---|---|
| Port | `prt` | `i02` | enum (port index) | values `0x80 + n` = `Trunk n` (LAG), see [lag.md](lag.md) |
| MAC | `adr` | `i01` | mac | |
| VLAN ID | `vid` | – | uint | SwOS & css106 only |

Notes:

* SwOS 2.18 paginates the dynamic table client-side (64 rows per page); SwOS Lite shows at
  most the first 128 hosts (the UI displays a note when the response contains ≥ 128 rows).
* SwOS Lite tolerates parse errors on `!dhost.b` silently (the endpoint may briefly return
  malformed data while the table changes).

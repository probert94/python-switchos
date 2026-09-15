# `snmp.b` — SNMP Agent Settings

Backs the **SNMP** page. One record. Not polled.

| Label | SwOS id | Lite id | Type | Access | Notes |
|---|---|---|---|---|---|
| Enabled | `en` | `i01` | bool | RW | |
| Community | `com` | `i02` | str (max 64 SwOS / 63 Lite) | RW | |
| Contact Info | `ci` | `i03` | str (max 64 / 63) | RW | |
| Location | `loc` | `i04` | str (max 64 / 63) | RW | |

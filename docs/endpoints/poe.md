# PoE & DC Power Endpoints

Three endpoints, depending on hardware generation:

| Endpoint | Used by | Scope |
|---|---|---|
| `poe.b` | SwOS PoE models (css318fi, css318p, css320p, css328p, css354); SwOS Lite css610pi, css610out | full PoE controller, one entry per copper port |
| `poeoutports.b` | SwOS Lite css606 (ports 2–3), gper14i (ports 2–4) | simple PoE-out on selected ports |
| `dco.b` | SwOS Lite css606 | 3 DC output channels |

All are polled every 1 s. Values are per-port arrays / bitmasks over the **copper (PoE) ports
only** (SwOS: `prt − sfp` ports).

## `poe.b`

| Label | SwOS id | Lite id | Type | Access | Availability / notes |
|---|---|---|---|---|---|
| PoE Out | `poe` | `i01` | enum: `off`, `on`, `auto` | RW | all `poe.b` users |
| PoE Priority | `prio` | `i02` | enum `1`…`8` (wire 0–7) | RW | SwOS css318fi/css318p/css328p, Lite css610pi/css610out |
| PoE Priority (numeric) | `prio` | – | uint, 0 … copper-ports−1 | RW | css320p, css354 (replaces the enum variant) |
| Voltage Level | `lvl` | `i03` | enum: `auto`, `low`, `high` | RW | all except css320p |
| PoE LLDP Enabled | `lldp` | `i0a` | bool (mask) | RW | SwOS css320p, css328p; Lite css610pi, css610out |
| PoE LLDP Power | `ldpw` | `i0b` | uint, 0.1 W units ("W allocated") | RO | same as PoE LLDP Enabled |
| PoE Standard | `std` | – | enum: `af`, `af/at`, `af/at/bt` | RO | css320p only |
| PoE Status | `poes` | `i04` | enum, see below | RO | all |
| PoE Current | `curr` | `i05` | uint, mA | RO | all |
| PoE Voltage | `volt` | `i06` | uint, 0.1 V units | RO | all |
| PoE Power | `pwr` | `i07` | uint, 0.1 W units | RO | all |

**PoE Status enumeration** (wire value = index):

| # | State |
|---|---|
| 0 | *(empty)* |
| 1 | disabled |
| 2 | waiting for load |
| 3 | powered on |
| 4 | overload |
| 5 | short circuit |
| 6 | voltage too low |
| 7 | current too low |
| 8 | power cycle |
| 9 | voltage too high |
| 10 | controller error |

### Relationships

* `curr` × `volt` ≈ `pwr` (all measured).
* `ldpw` is the power granted via LLDP negotiation when `lldp` is enabled.
* SwOS only creates the PoE page when `sys.b` reports `npoe == 0` (see
  [models.md](../models.md)).

## `poeoutports.b` (SwOS Lite css606, gper14i)

One record; arrays over the PoE-capable ports only (css606: ports 2–3 → 2 entries;
gper14i: ports 2–4 → 3 entries).

| Label | Lite id | Type | Access | Notes |
|---|---|---|---|---|
| PoE Out | `i01` | enum: `auto on`, `force on`, `off` | RW | |
| PoE Status | `i02` | enum: `waiting for load`, `powered on`, `no load`, `powered on`, `no load`, `has load` | RO | |
| PoE LLDP Enabled | `i03` | bool (mask) | RW | css606; gper14i since 2.21 |
| PoE LLDP Power | `i04` | uint, 0.1 W units | RO | css606; gper14i since 2.21 |

## `dco.b` (SwOS Lite css606)

One record; arrays over the 3 DC output channels (`DC Out1`–`DC Out3`).

| Label | Lite id | Type | Access |
|---|---|---|---|
| Enable | `i01` | enum: `off`, `on` | RW |

## css106 PoE (on `link.b`)

The RB260GSP (CSS106-1G-4P-1S) exposes PoE on the **Link** endpoint instead, ports 2–5:

| Label | id | Type | Access |
|---|---|---|---|
| PoE Out | `poe` | enum: `off`, `auto`, `on`, `calibr` | RW |
| PoE Priority | `prio` | enum `1`…`4` | RW |
| PoE Status | `poes` | enum (same 10 states as above) | RO |
| PoE Current | `curr` | uint, mA | RO |
| PoE Power | `pwr` | uint, 0.1 W units | RO |

Single-output devices (SwOS Lite css610, gpen21) put *PoE Out Mode*/*PoE Out Status* on
[`sys.b`](system.md#poe-out-single-output-devices) instead.

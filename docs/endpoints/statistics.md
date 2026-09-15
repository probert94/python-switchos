# `stats.b` / `!stats.b` — Counters, Errors, Histograms

Backs the **Stats**, **Errors** and **Hist** pages (all three read the same endpoint).
One record; every property is a per-port array. Polled every 1 s (css106: 3 s).

* **SwOS 2.18** uses `stats.b` (no `!` prefix) because the page also **writes** the
  reset-selection masks (`resc`, `rese`, `resh`) before calling the reset actions.
* **SwOS Lite** and **css106** use the read-only `!stats.b`; resets go through
  `POST /resetstats` only (see [maintenance.md](maintenance.md)).

64-bit counters are `counter64` pairs — "SwOS id (+high id)"; value = low + 2³²·high
(see [types.md](../types.md#counter64--64-bit-counter)).

## Rates (computed by the device)

Display value = wire ÷ scale (bits/s resp. packets/s).

| Label | SwOS id | Lite id | css106 id | Scale SwOS / Lite / css106 | Access |
|---|---|---|---|---|---|
| Rx Rate | `rrb` | `i21` | `rrb` | 0.01 / 0.32 / 0.08 | RO |
| Tx Rate | `trb` | `i22` | `trb` | 0.01 / 0.32 / 0.08 | RO |
| Rx Packet Rate | `rrp` | `i25` | `rrp` | 1.28 / 2.56 / 0.64 | RO |
| Tx Packet Rate | `trp` | `i26` | `trp` | 1.28 / 2.56 / 0.64 | RO |

## Traffic counters (Stats page)

| Label | SwOS id | Lite id | Type | Access | Notes |
|---|---|---|---|---|---|
| Rx Bytes | `rb` (+`rbh`) | `i01` (+`i02`) | counter64 | RO | |
| Tx Bytes | `tb` (+`tbh`) | `i0f` (+`i10`) | counter64 | RO | |
| Rx Total Packets | `rtp` | `i23` | uint | RO | |
| Tx Total Packets | `ttp` | `i24` | uint | RO | |
| Rx Unicasts | `rup` (+`ruph`) | `i05` (+`i27`) | counter64 | RO | |
| Tx Unicasts | `tup` (+`tuph`) | `i11` (+`i28`) | counter64 | RO | |
| Rx Broadcasts | `rbp` (+`rbph`) | `i07` (+`i29`) | counter64 | RO | |
| Tx Broadcasts | `tbp` (+`tbph`) | `i14` (+`i2a`) | counter64 | RO | |
| Rx Multicasts | `rmp` (+`rmph`) | `i08` (+`i2b`) | counter64 | RO | |
| Tx Multicasts | `tmp` (+`tmph`) | `i13` (+`i2c`) | counter64 | RO | |
| Tx Queue | `tq` / `tqb` | – | uint pair (packets / kB) | RO | SwOS except css354 |
| Reset Counters (selector) | `resc` | – | bool (mask) | **WO** | SwOS 2.18 only: POSTed to `stats.b` before `POST /resetstats` |

## Error counters (Errors page)

| Label | SwOS id | Lite id | Notes |
|---|---|---|---|
| Rx Pauses | `rpp` | `i17` | |
| Rx MAC Errors / Rx Errors | `rte` | `i1d` | css106 label: *Total Errors* |
| Rx FCS Errors | `rfcs` | `i1e` | |
| Rx Jabber | `rae` | `i1c` | css106 label: *Align Errors* |
| Rx Runts | `rr` | `i19` | |
| Rx Fragments | `fr` | `i1a` | |
| Rx Too Long | `rtl` (css106) | `i1b` | not in SwOS 2.18 tables |
| Rx Overruns | `rov` | – | SwOS; css106 label: *Overflows* |
| Tx Pauses | `tpp` | `i16` | |
| Tx FCS Errors | – | `i04` | Lite only |
| Tx Underruns | `tur` | – | SwOS/css106 |
| Tx Too Long | `ttl` (css106) | – | css106 only |
| Tx Collisions | `tcl` | `i1f` | |
| Tx Single Collisions | `tsc` (css106) | `i15` | not in SwOS 2.18 tables |
| Tx Multiple Collisions | `tmc` | `i18` | |
| Tx Excessive Collisions | `tec` | `i12` | |
| Tx Late Collisions | `tlc` | `i20` | |
| Tx Excessive Deferred | `ted` (css106) | – | css106 only |
| Tx Deferred | `tdf` | `i06` | |
| Tx Total Errors | `tte` (css106) | – | css106 only |
| Reset Errors (selector) | `rese` | – | **WO**, SwOS 2.18 only (then `POST /reseterrs`) |

All error counters are RO uint arrays.

## Frame-size histogram (Hist page)

| Label (frame size) | SwOS id | Lite id | css106 ids (Rx / Tx) |
|---|---|---|---|
| 64 | `p64` | `i09` | `r64` / `t64` |
| 65–127 | `p65` | `i0a` | `r65` / `t65` |
| 128–255 | `p128` | `i0b` | `r128` / `t128` |
| 256–511 | `p256` | `i0c` | `r256` / `t256` |
| 512–1023 | `p512` | `i0d` | `r512` / `t512` |
| 1024–max | `p1k` | `i0e` | `r1k`+`rmax` / `t1k`+`tmax` (css106 splits 1024–1518 and 1519–max) |
| Reset Histograms (selector) | `resh` | – | **WO**, SwOS 2.18 only (then `POST /resethist`) |

SwOS 2.18 counts the combined Rx+Tx histogram (`p…` ids); css106 has separate Rx/Tx
histograms on its *Statistics* page.

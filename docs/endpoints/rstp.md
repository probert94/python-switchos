# `rstp.b` — (R)STP Per-Port Status

Backs the per-port half of the **RSTP** page (the bridge-level half lives on
[`sys.b`](system.md#rstp-bridge-settings)). One record; per-port values. Polled every 1 s.
Available on all SwOS builds (including css106); not available on Lite ftc21/gpen21/gper14i.

| Label | SwOS id | Lite id | Type | Access | Notes |
|---|---|---|---|---|---|
| RSTP | `ena` | `i01` | bool (mask) | RW | enable (R)STP on the port; the UI disables editing while *Forward Reserved Multicast* (`frmc`, sys.b) is set |
| Mode | `rstp` | `i05` | flag: `STP`, `RSTP` | RO | negotiated protocol |
| Role | `role` | `i02` | enum: `disabled`, `alternate`, `root`, `designated`, `backup` | RO | |
| Root Path Cost | `rpc` | `i03` | uint array | RO | |
| Type | `p2p` (+ `edge`) | `i06` (+ `i07`) | flag: `shared`, `point-to-point`, `edge`, `edge` | RO | two-bit pair |
| State | `lrn` (+ `fwd`) | `i08` (+ `i09`) | flag: `discarding`, `learning`, `forwarding`, `forwarding` | RO | two-bit pair |

css106 uses the same ids (`ena`, `rstp`, `role`, `rpc`, `p2p`+`edge`, `lrn`+`fwd`) and shows
the page together with the bridge settings from `sys.b` (`prio`, `cost`, `frmc`,
`rpr`+`rmac`).

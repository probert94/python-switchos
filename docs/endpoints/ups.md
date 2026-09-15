# `ups.b` — Battery / Charger (css610out only)

Backs the second half of the **Health** page on the SwOS Lite css610out build (outdoor unit
with battery backup). One record; polled every 1 s.

| Label | Lite id | Type | Access | Notes |
|---|---|---|---|---|
| PSU | `i0d` | enum: `failed`, `ok`, `checking` | RO | |
| Battery | `i11` | enum: `not connected`, `unknown`, `normal`, `low`, `depleted`, `temp. out of range` | RO | |
| Battery Voltage | `i14` + `i13` | composite: uint mA @ uint 0.01 V | RO | current @ voltage |
| Time On Battery | `i12` | uptime (seconds) | RO | |
| Cutoff Voltage | `i17` | int, 0.01 V units (float input), 19–26 V | RW | |
| Temperature | `i16` | int (8-bit), °C | RO | battery temperature sensor |
| **Charger group** | | | | |
| Charger | `i01` | enum: `resetting`, `disabled`, `charging`, `float`, `done`, `unstable power`, `no power`, `no battery`, `temp. out of range`, `overload`, `invalid profile`, `charging limited`, `controller error`, `invalid battery` | RO | |
| Mode | `i05` | enum: `disabled`, `standby`, `cyclic`, `no float` | RW | |
| Voltage Preset | `i04` | enum: `flooded`, `AGM`, `gel`, `LFP`, `custom` | RW | selecting a preset adjusts the voltage fields |
| Charge Voltage | `i06` | int, 0.01 V (float input), 23–30 V, default 29.3 | RW | |
| Float Voltage | `i07` | int, 0.01 V (float input), 23–30 V, default 26.5 | RW | |
| Voltage Offset (−mV/°C) | `i08` | uint ≤ 100 | RW | temperature compensation |
| Temperature Range | `i0a` | enum: `0~40C`, `-10~50C` | RW | |
| Temperature Override | `i03` | int (8-bit), −30…40, default −127 = off | RW | |
| Capacity (Ah) | `i09` | uint, 1–255 | RW | |
| Current (mA) | `i0b` | uint, 200–1600 | RW | charge current |
| EoC Current | `i0c` | enum: `20mA`, `0.01C`, `0.02C`, `0.05C`, `0.1C` | RW | end-of-charge threshold |

# Property Data Types — Encoding & Decoding

Every property in the endpoint tables references one of the types below. "Wire value" means
the value inside the serialized object (after parsing the `0x…` hex number or the quoted hex
string, see [protocol.md](protocol.md#serialization-format)).

The type names used throughout this documentation are canonical names assigned by this
documentation; the firmware itself only has minified constructor names (SwOS 2.18 css326:
`E`=bool, `F`=enum, `G`=uint, `H`=int, `I`=mac, `J`=ip, `L`=str, `Ha`=uptime, `M`=combine,
`N`=composite, `Fa`=flags / SwOS Lite css610-2.21: `D`=bool, `E`=enum, `F`=uint, `za`=int,
`G`=mac, `I`=ip, `J`=str, `Ba`=uptime, `N`=combine, `O`=composite, `ya`=flags).

---

## `bool` — boolean / port bitmask

A flag, or one flag per port packed into a single integer.

* **Decode:** port *p* (0-based) is enabled ⇔ bit *p* of the wire value is `1`
  (LSB = first port). A record-level (non-per-port) bool uses bit 0.
* **Encode:** identical — set bit *p* for each enabled port.
* **More than 32 ports** (SwOS only, e.g. css354 with 60 ports): the wire value is an
  **array of two 32-bit numbers `[high, low]`** — ports 0–31 in `low`, ports 32+ in `high`.

Used for: `en`, `an`, per-port members (`mbr`, `prts`, `allp`, `pdsc`, `igfl`, `dtrp`,
`fp1…fpN`, ACL `frm`), all on/off settings.

## `flag` — read-only status bit / bit-pair

Read-only per-port state built from **one or two** `bool` bitmask properties. The state index
of port *p* is:

```
state = bit_p(prop) | bit_p(second_prop) << 1     # second_prop only where listed
```

The index selects a display string from the property's state list. Examples: *Link Status*
(`lnk` + `paus` → `no link`, `link on`, `no link`, `link paused`), *Full Duplex* (`dpx`),
*Flow Control status* (`tfct` + `rfct`), RSTP *Type* (`p2p` + `edge`) and *State*
(`lrn` + `fwd`), RSTP *Mode* (`rstp`).

## `enum` — selection

An integer index into a fixed option list (documented per property). Per-port enums are
transferred as an **array** with one integer per port. Encode: the index; Decode: the index.
Out-of-range/`-1` is treated as `0`.

## `uint` — unsigned number

32-bit unsigned number (per-port: array of numbers). Modifiers, when listed on a property:

| Modifier | Meaning |
|---|---|
| `scale: s` | wire = display × *s*; display = wire ÷ *s*. E.g. voltages with `scale: 10` are transferred in 0.1 V units. |
| `radix: 16` | The UI displays/parses the number as hex (e.g. Bridge Priority, Ethertype). The wire value is a normal number. |
| `min`/`max` | Client-side validation bounds. |
| `metric` | UI accepts/produces `k`, `M`, `G` suffixes (decimal, ×10³/10⁶/10⁹). |
| `dB` | Display = `10·log10(wire ÷ scale)` (used for SFP Tx/Rx power: wire is in 0.1 µW units, display in dBm). |
| default *d* | Sentinel: if the wire value equals *d*, the UI shows an empty field; an empty input writes *d*. E.g. ACL *Priority* uses default `8` (= "any", valid range 0–7), *DSCP* uses `64`. |

## `int` — signed number

Like `uint` but two's-complement signed with a **width** of 8, 16 (default) or 32 bits:

* **Decode:** `if wire >= 2^(width-1): value = wire - 2^width`
* **Encode:** `if value < 0: wire = value + 2^width`

Some `int` properties accept fractional input (parsed as float, then multiplied by `scale`
and rounded). Used for temperatures (°C, width 32 or 8) and UPS voltages.

## `counter64` — 64-bit counter

Two `uint` properties combined: `value = low + 2^32 × high`. The tables list them as
"`rb` (+`rbh`)" — the first id is the low word, the id in parentheses the high word.
Per-port: both are arrays. Read-only.

## `mac` — MAC address

Transferred as a **string of 12 hex digits** (quoted-hex string whose *content* is the MAC,
e.g. `'d401c3a61b00'` = `D4:01:C3:A6:1B:00`). Encode: strip separators, lower-case hex.
An all-`0` MAC means "unset" for most properties (ACL masks default to all-`f`).

## `ip` — IPv4 address

32-bit number, **little-endian octet order**: `a.b.c.d` ⇔ `a | b<<8 | c<<16 | d<<24`.
Example: `192.168.88.1` → `0x0158a8c0`. `0` = unset/empty.

## `str` — string

Quoted hex string; each byte pair is one character. Decoding stops at a `00` byte.

* **SwOS**: characters > 127 are encoded as UTF-8-style multibyte sequences.
* **SwOS Lite**: plain single bytes (`charCodeAt & 0xFF`); the UI only guarantees ASCII.

Maximum length (UI-enforced): SwOS 16 chars, SwOS Lite 15 chars; SNMP fields 64 (SwOS) /
63 (Lite) chars.

## `uptime` — time duration

`uint` displayed as `[D days ]HH:MM:SS`. Wire unit differs: **SwOS = centiseconds**
(`upt`, scale 100), **SwOS Lite = seconds** (`i01` on `sys.b`). Read-only.

## `flags` — nibble-state display

Read-only. The wire value is split into *n* fields of *w* bits (documented per property);
each field is a state index. Only used for *Cable Pairs* (4 fields × 4 bits, states:
`0` ok, `1` short, `2` open, `3` reversed polarity; fields = wire pairs).

## `composite` — joined sub-properties (UI-level)

Several independently-encoded properties displayed as one field with separators. On the wire
each part is a separate key. Examples:

* *Root Bridge* = `rpr` (uint, hex) + "." + `rmac` (mac)
* *Allow From* = `alla` (ip) + "/" + `allm` (uint, prefix length)
* ACL *IP Src/Dst* = `ip`/`mask`:`port` (three properties)
* Health *PSU* = current + " @ " + voltage

## `combine` — alternative display/edit pair (UI-level)

Two properties for the same logical setting: a read-only *status* (`flag`/`uint`) and a
writable *config* (`enum`/`bool`). The UI shows one or the other depending on context (e.g.
with auto-negotiation on, *Speed* shows negotiated `spd`; with it off, the editable `spdc`).
Both are always present on the wire. Examples: `spd`/`spdc`, `dpx`/`dpxc`,
`tfct`+`rfct` (status) vs `fctc`/`fctr` (config).

---

## Worked examples

**Port bitmask** — enable ports 1, 2 and 10 of a CSS326 (26 ports): bits 0, 1, 9 →
`en = 0x0203`.

**VLAN members default** — `mbr` default `268435455` = `0x0FFFFFFF` = all 28 possible ports.

**Speed enum** — `spdc:[0x02,0x02,…]`: option list `10M,100M,1G,10G,5G,2.5G,40G` (SwOS 2.18)
→ `2` = 1G. SwOS Lite list: `10M,100M,1G,10G,200M,2.5G,5G`. css106: `10,100,1000`.

**SFP Rx power** — `rpw: 0x1234` → 4660/10⁴ mW → `10·log10(0.466)` ≈ −3.32 dBm.

**Rates** (read-only, Stats page): display b/s = wire ÷ scale. SwOS `rrb` scale `0.01`
(wire unit 100 bit/s), packet rate scale `1.28`; Lite scale `0.32` / `2.56`; css106 `0.08`
/ `0.64`.

**Rate limits** (writable): SwOS `ir`/ACL `rate` scale `0.001` → wire unit = kbit/s
(UI input `10M` → wire `0x2710` = 10000). SwOS Lite `i1a`/`i1d`/`i1e` scale `1E-5`,
max 65535 → wire unit = 100 kbit/s.

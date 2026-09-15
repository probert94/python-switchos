# Protocol & Serialization

## Transport

Everything is plain HTTP on the device's IP.

* **Read**: `GET /<endpoint>` (e.g. `GET /link.b`). Response body is a single object (or array
  of objects for list endpoints) in the serialization described below. A `200` with an empty
  body means "no data" (the UI retries after 1 s).
* **Write**: `POST /<endpoint>` with `Content-Type: text/plain` and the serialized
  (partial) object as body. The device answers `200` on success. The UI always posts the
  complete set of writable properties of the page being applied.
* **Actions**: `POST /<action>` with the literal body `*` (a single asterisk), e.g.
  `POST /reboot`. See [endpoints/maintenance.md](endpoints/maintenance.md).

HTTP status codes observed in the frontend logic:

| Status | Meaning |
|---|---|
| `200` | OK |
| `401` | Not authenticated — UI shows "Refresh page to log in" (authentication is handled by the browser/HTTP layer, not by the JS) |
| `405` | Wrong old password on `/!pwd.b` |
| `0` (no response) | Connection lost |

## Serialization format

The payload looks like JSON but is **not** JSON. The UI parses responses with JavaScript
`eval()` and produces requests with a small serializer. Rules:

* Object: `{key:value,key:value,...}` — keys are **unquoted**.
* Array: `[value,value,...]`.
* List endpoints (`vlan.b`, `host.b`, `!dhost.b`, `!igmp.b`, `acl.b`) transfer an **array of
  objects**: `[{...},{...}]`.
* **Number**: hexadecimal with `0x` prefix, lower-case, always an **even number of digits**
  (a leading `0` is added if needed). Values are 32-bit; the serializer masks accordingly:

  ```js
  s = (v >> 4 & 0x0FFFFFFF).toString(16) + (v & 0xF).toString(16);
  if (s.length % 2 == 1) s = "0" + s;
  emit("0x" + s);
  ```

  Examples: `10` → `0x0a`, `255` → `0xff`, `4095` → `0x0fff`.
* **String**: single-quoted **hex string** (`'774c414e31'`), i.e. the string content is
  hex-encoded bytes, not the text itself. See [types.md](types.md#string-str) for character
  encoding details (SwOS ≠ SwOS Lite for non-ASCII).
* Booleans do not exist — flags are bits inside numbers (see
  [types.md](types.md#boolean--port-bitmask-bool)).
* `null`/missing: absent keys simply don't appear.

### Example

`GET /sys.b` (SwOS, shortened):

```
{iptp:0x00,ip:0x0158a8c0,id:'737769746368',alla:0x00,allm:0x00,allp:0x03ffffff,
 avln:0x00,ivl:0x00,igmp:0x00,brd:'435353333236',ver:'322e3138',mac:'d401c3a61b00',
 upt:0x00058a1f,...}
```

(`id:'737769746368'` is the hex encoding of `switch`.)

`POST /sys.b` to change the identity:

```
{iptp:0x00,ip:0x0158a8c0,id:'6e65772d6e616d65',...}
```

### Per-port values inside one record

Endpoints that describe ports (`link.b`, `poe.b`, `sfp.b`, `rstp.b`, `!stats.b`/`stats.b`,
parts of `fwd.b`) still return **one object**. A property is either:

* a **bitmask** — one bit per port (boolean-per-port values, e.g. `en`, `an`, `lnk`), or
* an **array** — one element per port (numeric/enum/string values, e.g. `nm`, `spdc`, `poes`),
  in port order.

Which of the two applies is listed per property in the endpoint docs (`Type` column: *bool* =
bitmask, everything else in a per-port context = array).

## Boot-time discovery

The UI determines the device model and port count at load time:

1. `GET /sys.b` → SwOS: `brd` (board name string, e.g. `CSS326`), `ver` + `bld`
   (firmware version + build timestamp), `rev` (hardware revision), `mrkt` (marketing name),
   `npoe` (PoE hardware indicator). SwOS Lite: `i06` (version) + `i0b` (build timestamp).
2. `GET /link.b` → SwOS: `prt` (total port count), `sfp` (SFP cage count), `sfpo` (index of
   first SFP port; defaults to `prt - sfp`), `comb` (bitmask of combo ports), `qsfp` (bitmask
   of QSFP+ lanes), `qsfo` (QSFP offset), `nm` (per-port name array). SwOS Lite: port count is
   compiled into the build; only `i0a` (names) is used.
3. SwOS additionally probes `GET /fan.b` (`ver` > 0 → fan controller present) and
   `GET /sfp.b` (may also carry `nm` name overrides).

## Authentication

The JS contains no credential handling: reads/writes rely on the HTTP layer (the device uses
standard HTTP authentication; a `401` tells the UI the session is gone). Log out with
`POST /logout` (body `*`), after which the device invalidates the session and the UI reloads.

## Password change (`/!pwd.b`)

`POST /!pwd.b` with body `{pwd:'<64 hex digits>'}` (SwOS) or `{i01:'<64 hex digits>'}`
(SwOS Lite). Passwords are limited to 15 ASCII characters. The 32-byte payload is the
new+old password obfuscated with an RC4 keystream derived from the old password:

```text
buf = bytes(old_password) + [0x00] + bytes(new_password)   # then zero-pad to 32 bytes

key = old_password (or "*" if empty), repeated until >= 16 chars, cut to 16
S   = RC4 key-schedule(key)                                # standard 256-byte KSA
ks  = 64 bytes of RC4 keystream from S

for i in 0..63:
    buf[i & 31] ^= ks[i]                                   # every byte XORed twice

payload = hex(buf)                                         # 64 hex chars
```

Responses: `200` OK (UI reloads → new login), `405` incorrect old password.

## Polling intervals used by the UI

| Endpoint | Interval |
|---|---|
| `link.b`, `lacp.b` | 3 s |
| `poe.b`, `poeoutports.b`, `dco.b`, `sfp.b`, `rstp.b`, `sys.b` (RSTP/System/Health), `stats.b`/`!stats.b`, `acl.b`, `!aclstats.b`, `ups.b` | 1 s |
| `!dhost.b` | 1 s (SwOS) / 2 s (SwOS Lite) |
| `!igmp.b` | 5 s |
| css106: `!stats.b` | 3 s |

## Applying changes to list endpoints

For list endpoints the UI posts the **whole table** as an array of records; rows are matched by
position, not by key (the `unique:1` marker on *VLAN ID* is only client-side validation).
Sending fewer records deletes rows; appending records creates rows. Limits enforced by the UI:
VLANs ≤ 250, ACL rules ≤ 32, static hosts ≤ 12 (SwOS Lite).

# Maintenance / Action Endpoints

Unless noted otherwise these are `POST` requests with the literal body `*` and
`Content-Type: text/plain`; success = HTTP `200`.

| Endpoint | Method | Family | Effect |
|---|---|---|---|
| `/reboot` | POST `*` | all | reboot the device (UI reloads after ~3 s) |
| `/bootros` | POST `*` | SwOS, CRS boards only | reboot into RouterOS |
| `/reset` | POST `*` | all | reset configuration to defaults (then reboots) |
| `/logout` | POST `*` | all | invalidate the web session |
| `/resetstats` | POST `*` | all | SwOS: reset the counters whose `resc` bits were just posted to `stats.b`; SwOS Lite/css106: reset all counters (also used by Errors/Hist/ACL-Stats pages) |
| `/reseterrs` | POST `*` | SwOS 2.18 | reset error counters selected via `rese` on `stats.b` |
| `/resethist` | POST `*` | SwOS 2.18 | reset histograms selected via `resh` on `stats.b` |
| `/resetacl` | POST `*` | SwOS 2.18 | reset the per-rule ACL hit counters (`pkts` in `acl.b`) |
| `/!pwd.b` | POST object | all | change password — body `{pwd:'…'}` (SwOS) / `{i01:'…'}` (Lite); see [protocol.md](../protocol.md#password-change-pwdb) |
| `/backup.swb` | GET | all | download the configuration backup (binary). The UI names it `<board>_<version>.swb`. Empty response = default configuration ("nothing to save") |
| `/backup.swb` | POST multipart, field `file` | all | restore a backup; device reboots afterwards |
| `/pboot` | POST `*` | all | prepare the bootloader for a firmware upload |
| `/upgrade` | POST multipart, field `blob` | all | upload the firmware image (after `/pboot`); on `200` the device flashes and reboots |

## Firmware upgrade flow (as implemented by the "Upgrade" page)

1. `POST /pboot` body `*`
2. `POST /upgrade` as `multipart/form-data` with the image in field `blob`
3. Wait for `200`, then `POST /reboot` (the UI reloads the page ~3 s later)

### Online upgrade sources

The UI fetches version info and images from MikroTik (plain HTTP):

* SwOS: `http://upgrade.mikrotik.com/swos2/<board>/LATEST` (newer scheme) or
  `http://upgrade.mikrotik.com/swos/<board>.LATEST` (fallback), changelog at `…/CHANGELOG`,
  image `swos-<board>-<version>.bin`.
* SwOS Lite: `http://upgrade.mikrotik.com/swoslite/<build>/LATEST`, `…/CHANGELOG`,
  image `…/swos-<build>-<version>.bin` — `<build>` is the file-name prefix (css610, gpen21, …).

`LATEST` contains `«version».«unix-build-timestamp»`.

## Backup restore flow

1. `POST /backup.swb` (multipart, field `file`)
2. On completion the UI calls `POST /reboot`.

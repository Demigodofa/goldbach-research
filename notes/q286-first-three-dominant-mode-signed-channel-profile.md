# q286 dominant-mode signed channel profile

Status: finite signed-channel profile.  Goldbach is not proved.

The `25` real q286 dominant channels are too large for plain independent
`Linf`/`L2` smallness to certify the active rows.  This note keeps the exact
character-channel identity and asks what the signed positive/negative ledger
actually does.

Receipt:
`evidence/q286-first-three-dominant-mode-signed-channel-profile.json`

## Ledger

For each target, write:

```text
dominant_sum = positive_channel_offset - negative_channel_pressure
```

The floor is `dominant_sum >= -0.3`.

| target | dominant sum/P | positive offset | negative pressure | required positive offset | slack |
| --- | ---: | ---: | ---: | ---: | ---: |
| `1222142` | `-0.30883317956053014` | `0.06313382289502988` | `0.37196700245556` | `0.07196700245556004` | `-0.00883317956053016` |
| `1242118` | `-0.2834710865332554` | `0.05996824017570475` | `0.34343932670896016` | `0.04343932670896017` | `0.01652891346674458` |
| `1240888` | `-0.2728134266190817` | `0.013711748649337881` | `0.2865251752684196` | `0.0` | `0.013711748649337881` |

The tail `1222142` has the largest negative pressure and not enough positive
offset.  The clear row `1242118` clears because positive offset beats the
required offset.  The clear row `1240888` clears mostly because negative
pressure is already below `0.3`, even though positive offset is small.

## Consequence

The next theorem target has two visible branches:

- control the negative-channel pressure below `0.3`, or
- when pressure is above `0.3`, prove enough positive-channel offset.

This does not prove either branch.  It only identifies the signed structure
that the previous norm budget hid.

# q286 dominant-mode channel norm budget

Status: sufficient-condition budget and finite stress.  Goldbach is not
proved.

The dominant `mode_1 + mode_2` theorem has been reduced to `25` real q286
character channels.  This note quantifies the simplest independent channel
norm route:

- an `Linf` bound on every normalized representative channel sum, or
- an `L2` bound across the `25` normalized representative channel sums.

These are sufficient conditions only.  They are useful as a scale check, not
as necessary conditions.

## Budget

Receipt:
`evidence/q286-first-three-dominant-mode-channel-norm-budget.json`

For tail threshold `tau=.3`, the sufficient independent channel budgets are:

```text
max_chi |S_chi(N)|/T_N <= 0.009312260360507715
sqrt(sum_chi |S_chi(N)|^2)/T_N <= 0.046390507527336665
```

The coefficient sizes behind these budgets are:

- real-channel `L1/principal_mean`: `32.215594107770805`,
- real-channel `L2/principal_mean`: `6.466840222069529`.

## Sample Stress

None of the three near-boundary sample rows is certified by either generic
budget.

| target | dominant sum/P | Linf utilization | L2 utilization | floor passes |
| --- | ---: | ---: | ---: | --- |
| `1222142` | `-0.3088331795605278` | `3.661464047083634` | `2.0930749450275714` | no |
| `1242118` | `-0.2834710865332539` | `2.920352965188215` | `2.0551735456902227` | yes |
| `1240888` | `-0.27281342661908214` | `2.950247050646688` | `1.7027510931802834` | yes |

The two near-clear rows fail both independent channel-norm budgets while their
signed dominant sums still clear the `-.3` floor.  Therefore independent
channel smallness is too blunt at the active scale.

The companion signed profile
`q286-first-three-dominant-mode-signed-channel-profile.md` shows what the norm
budget hides: one clear row is rescued by enough positive offset, and the
other clears because its negative channel pressure is already below `.3`.

## Remaining Route

The next theorem cannot merely make every real channel small enough by a
generic norm bound unless the eventual scale improves substantially.  It needs
one of:

- signed cancellation among the `25` real channels,
- arithmetic structure correlating channels with the coefficient signs,
- a stronger fixed-modulus binary-prime character-sum theorem, or
- complement/lower-support rescue when the dominant channel sum is too
  negative.

This does not refute character-sum methods.  It refutes only the current
active-scale shortcut that treats the `25` channels independently through a
plain `Linf` or `L2` smallness bound.

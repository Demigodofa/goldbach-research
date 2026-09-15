# q286-WBSS Mod-286 Bandlimited Residual Audit

Status: finite residual diagnostic. Goldbach is not proved.

Receipt:

```text
tools/build_q286_wbss_mod286_bandlimited_residual_audit.py
evidence/q286-wbss-mod286-bandlimited-residual-audit.json
```

## Question

The Fourier interaction audit demoted a tiny-character explanation but left a
sharper possible proof shape: top `20` Fourier conjugacy groups supply a
sign-stable negative interaction main term, while the remaining five groups
must be absorbed as residual. This audit asks whether the residual needs a
symmetric absolute-value bound, or whether the actual theorem target is
one-sided: control only positive residual pushback against the top-20 drag.

## Result

The coefficient split is:

```text
nonzero conjugacy groups:                 25
top group count:                          20
residual group count:                     5
top-20 coefficient-energy share:          0.870213154434473
residual coefficient-energy share:        0.129786845565527
```

On the same `196` post-discovery rows:

```text
top-20 bandlimited component:             196 / 196 negative
total interaction component:              196 / 196 negative
residual five-group component negative:   172 / 196
residual five-group component positive:    24 / 196
residual component range:                 -0.1967819286124881..0.057893218751199974
positive pushback / main-drag range:      0.0..0.12566677703853088
absolute residual / main-drag range:      0.0006303342108321785..0.9879886701050115
rows passing pushback < 0.13:             196 / 196
rows passing pushback <= 1/8:             195 / 196
rows with absolute residual < main drag:  196 / 196
```

The symmetric residual bound technically passes on this fixture, but it is
nearly sharp because large residuals are often helpful negative residuals. The
cleaner one-sided target is much less stressed: only positive residual
pushback matters for preserving the negative total interaction drag.

## Decision

Preserve the top-20 bandlimited route, but state it one-sided:

```text
top20_drag(N) > 0
and
positive_residual_pushback(N) <= theta * top20_drag(N)
for some fixed theta < 1.
```

The checked fixture supports `theta = 0.13`; the more elegant `theta = 1/8`
is already slightly too strong. The next proof attempt should explain why the
remaining five Fourier groups rarely push upward and why, when they do, their
pushback is bounded by the top-20 drag. A symmetric absolute residual theorem
is possible but probably the wrong target because it spends effort controlling
helpful residual drag.

## Boundary

This audit proves no band-limited character theorem, no signed projection
theorem, no q286 threshold theorem, no strict-central Goldbach theorem, and no
Goldbach proof. It only turns the finite top-20 Fourier split into a sharper
one-sided residual theorem obligation.

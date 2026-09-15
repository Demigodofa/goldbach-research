# q286-WBSS four-modulus component-envelope horizon audit

## Question

The adverse-drag horizon audit showed that each checked row survives after
discarding all helpful projected terms in that same row.  Does an even stricter
finite envelope survive if each modulus contributes its own worst observed
adverse value, even when those four worst values occur on different rows?

## Mechanism

Read the `232`-row adverse-drag horizon receipt and compute

```text
A_d = max_row max(0, -E_d(row))
```

for each projected modulus `d` in `70`, `130`, `154`, and `286`.  Then test
the disconnected finite envelope

```text
local_main(row) - (A_70 + A_130 + A_154 + A_286) > 0
```

on every checked horizon row.

## Receipt

```text
tools/build_q286_wbss_four_modulus_component_envelope_horizon_audit.py
evidence/q286-wbss-four-modulus-component-envelope-horizon-audit.json
```

## Result

```text
horizon targets:                             232
target range:                    1036248..1115822
component-envelope positive rows:            232 / 232
component-envelope nonpositive rows:           0 / 232
A_70:                         0.11808088288936758
A_130:                       0.00932108976691037
A_154:                       0.08239931832908774
A_286:                       0.12228599640255161
component adverse supremum sum: 0.3320872873879173
tightest target:                         1038176
tightest local main:          0.717245423802844
tightest component envelope:  0.38515813641492663
largest envelope ratio:       0.4630037032891566
```

The component suprema occur at different targets:

```text
70  -> 1076288
130 -> 1074592
154 -> 1055452
286 -> 1070252
```

So this test is stricter than the rowwise adverse-drag certificate.  It allows
the four worst observed adverse components to be combined even though that
combined worst row was not observed in the horizon.

## Decision

The disconnected componentwise finite envelope survives the checked horizon.
This strengthens the theorem-shaped target: instead of only proving a rowwise
one-sided adverse-drag bound, a possible route is to prove per-modulus adverse
supremum bounds whose sum remains below the local main term.

This is still finite horizon evidence only.  The component suprema are fitted
to the checked `232` rows.  No per-modulus supremum theorem, one-sided signed
concentration theorem, fixed-modulus equidistribution theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof is established.
The residual absorption constants `.125`, `.126`, and `.13` remain finite
fixture fits only; no universal residual absorption bound is established.

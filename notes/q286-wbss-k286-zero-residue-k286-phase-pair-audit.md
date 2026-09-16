# q286-WBSS K286 zero-residue K286 phase-pair audit

## Question

The component-phase audit found that modulus `286` carries the Cauchy threat
on all `18` zero-lane rows where the aggregate active-character `L2` cap
fails.  Does the `K_286` phase story collapse to one fixed dominant conjugate
phase-pair?

## Mechanism

For the modulus `286 = 2 * 11 * 13` unit group, the active character grid has
shape `(10, 12)`.  Pair each frequency `(a, b)` with its conjugate
`(-a mod 10, -b mod 12)` and sum the real contribution of the pair.  Then
record which conjugate pair is the top adverse pair, top rescue pair, and top
absolute pair on each of the `18` aggregate-`L2` violating rows.

Receipt:

```text
tools/build_q286_wbss_k286_zero_residue_k286_phase_pair_audit.py
evidence/q286-wbss-k286-zero-residue-k286-phase-pair-audit.json
```

## Result

```text
L2-cap-violating zero-lane rows:       18
K286 adverse component rows:            8
K286 rescue component rows:            10

most common top adverse pair:     3,7|7,5 on 4 / 18 rows
most common top rescue pair:      3,5|7,7 on 4 / 18 rows
most common top absolute pair:    3,5|7,7 on 3 / 18 rows

unique top adverse pairs:              11
unique top rescue pairs:               10
unique top absolute pairs:             13

pair reconstruction error max:  < 5e-17
pair cancellation ratio mean:    0.15132464895023304
top absolute pair fraction min:  0.08285344480352641
top absolute pair fraction mean: 0.11575000686804238
top absolute pair fraction max:  0.16161053354457436
```

The largest single-pair fraction occurs at target `1173172`, residue
`2002 mod 10010`, and is only `0.16161053354457436` of that row's real-pair
absolute envelope.

## Decision

`DIAGNOSTIC_k286_phase_pair_single_mode_falsified`.

The `K_286` component remains the right place to look, but the finite data does
not support a single fixed conjugate phase-pair theorem.  The leading adverse,
rescue, and absolute phase-pairs move across target residues, and no individual
top pair locally carries a large fraction of the real-pair envelope.

The next theorem-shaped target is target-residue-dependent oscillation or a
band estimate over moving `K_286` phase pairs.  A universal proof would still
need a pointwise, unnormalized analytical estimate showing raw adverse drag
below local main for every sufficiently large `N`.

No phase-pair theorem, target-residue oscillation theorem, coefficient-
direction nonalignment theorem, universal pointwise raw bound, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof is established.

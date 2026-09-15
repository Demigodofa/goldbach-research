# q286 later-tail complement source decomposition

Status: finite complement-source diagnostic.  This is not a threshold theorem,
signed correlation theorem, pointwise character-sum theorem, or Goldbach proof.

Receipt:

```text
tools/build_q286_later_tail_complement_source_decomposition.py
evidence/q286-later-tail-complement-source-decomposition.json
```

## Question

The later full-block scan found `73` first-three-tail rows and no failures.
This receipt asks which arithmetic components supply the rescue margin:
principal baseline, lower CRT-support terms, q286 local action, q286 modes
`4..6`, or the q286 residual tail.

## Mechanism

For each later tail target, re-evaluate the optimized q286 row action and split
the identity

```text
full/principal = first_three_modes + complement
```

into

```text
first_three_modes = q286_mode_1 + q286_mode_2 + q286_mode_3
complement = principal_baseline
           + lower CRT-support components
           + q286_local
           + q286_mode_4 + q286_mode_5 + q286_mode_6
           + q286_tail_residual
```

Then test component removals and smallest fixed component subsets.

## Result

`evidence/q286-later-tail-complement-source-decomposition.json` shows:

```text
tail targets decomposed: 73
principal-only keeps all rows positive: true
principal-only minimum margin: 0.557444316517158
removing principal failure count: 72
nonprincipal-only keeps all rows positive: false
nonprincipal-only minimum margin: -0.656649759138451
smallest subset size with principal allowed: 1
smallest subset size with principal excluded: none
principal-excluded subsets checked: 4095
maximum identity error: 4.44089209850063e-16
```

The principal baseline is the only one-component passing subset.  Excluding it,
even the full collection of nonprincipal rescue components cannot keep all
tail rows positive.

Largest net component sums over the `73` rows:

```text
principal_baseline: +73.00
support_7_11:       -1.27
support_5_7:        -1.24
support_7:          -0.74
q286_local:         +0.61
support_5:          +0.59
support_13:         +0.32
support_11:         +0.18
```

Interpretation: in this finite later window, the rescue mechanism is
principal-baseline surplus plus control of nonprincipal drag.  It is not a
positive lower-support cone by itself.

# q286 centered (3,1) same-residue fresh-population audit

Status: finite same-residue fresh-window audit only.  This is not a proof of
a stress-classifier theorem, signed correlation theorem, pointwise
character-sum theorem, or Goldbach.

## Source

The generated audit is:

```text
evidence/q286-centered-3-1-same-residue-fresh-population-audit.json
```

The builder is:

```text
tools/build_q286_centered_3_1_same_residue_fresh_population_audit.py
```

It uses the same local singular source and LP vector as the earlier q286
channel audits, then recomputes centered `(3,1)` rows for the five selected
deficit references and the `606` fresh predeclared targets.

## Question

Could the same-residue collision result be an artifact of the selected
clear-control rows?

This audit widens the comparison from same-residue selected clears to the
fresh predeclared windows.  Within a fixed residue modulo `143`, the local
q286 channel vector is identical, so the remaining centered `(3,1)` gap is
empirical/correlation-side.

## Result

Every selected deficit reference has six same-residue fresh targets in the
predeclared windows.  Every one of those same-residue fresh targets is above
the selected deficit in weighted centered `(3,1)`.

| deficit | residue mod 143 | same-residue fresh count | nearest fresh target | deficit value | nearest fresh value | minimum gap |
|---:|---:|---:|---:|---:|---:|---:|
| 13822 | 94 | 6 | 28000066 | -0.028592853507 | -0.017164951448 | 0.011427902060 |
| 24424 | 114 | 6 | 44000070 | -0.027096410497 | 0.005523420207 | 0.032619830704 |
| 55864 | 94 | 6 | 28000066 | -0.045760282348 | -0.017164951448 | 0.028595330900 |
| 164598 | 5 | 6 | 40000108 | -0.019648712262 | -0.012390377755 | 0.007258334507 |
| 1222142 | 64 | 6 | 40000024 | -0.028279567375 | -0.007041578659 | 0.021237988716 |

Summary:

```text
all selected deficits pass same-residue fresh population: true
fresh failures: none
fresh comparisons per selected deficit: 6
```

## Interpretation

This strengthens the non-local reading:

```text
selected deficit references are low in centered (3,1) even against fresh
predeclared targets with the same local residue vector
```

The result does not prove a broad stress class.  It says the observed
selected-deficit `(3,1)` separation is not merely a local residue effect and
not merely an artifact of the selected clear-control rows.  The remaining
open obligation is still to define a non-post-hoc stress family or prove a
signed/correlation estimate that forces these same-residue gaps.

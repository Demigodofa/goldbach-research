# q286 centered (3,1) available same-residue population audit

Status: finite population audit only.  This is not a selected-stress theorem,
signed correlation theorem, pointwise character-sum theorem, or Goldbach
proof.

## Source

The generated receipt is:

```text
evidence/q286-centered-3-1-available-same-residue-population-audit.json
```

The builder is:

```text
tools/build_q286_centered_3_1_available_same_residue_population_audit.py
```

It reuses the same local q286 channel coordinates, LP vector, same-window
target generators, and fresh-window target generators used by the earlier
`(3,1)` audits.  The expensive profile call is residue-filtered to the
selected-reference residues `5`, `64`, `94`, and `114`.

## Question

The previous signed-gap receipt showed that fresh predeclared same-residue
targets stay above the selected deficit references in weighted centered
`(3,1)`.  This audit asks whether that is only a fresh-window artifact by
testing the already available same-window nonselection rows, separated into:

- `12` zero-local seed targets from residues `38` and `64`;
- `594` same-window nonseed targets;
- `606` fresh predeclared targets.

Only rows whose residue modulo `143` can compare with a selected reference are
profiled and retained.

## Result

No available same-residue nonselection row falsifies the selected-reference
ordering.  Across the filtered fixture:

```text
profile target count after residue filter: 58
same-residue all-available nonselection comparisons: 60
failure count: 0
minimum all-available weighted gap: 0.0003925287417802202
```

Per-reference tightest all-available same-residue weighted gaps:

| reference | residue mod 143 | tightest comparison | comparison scope | min weighted gap |
|---:|---:|---:|---|---:|
| 13822 | 94 | 6000088 | same-window nonseed | 0.011314508835 |
| 24424 | 114 | 8000106 | same-window nonseed | 0.030089672469 |
| 55864 | 94 | 6000088 | same-window nonseed | 0.028481937675 |
| 164598 | 5 | 8000140 | same-window nonseed | 0.000392528742 |
| 1222142 | 64 | 8000056 | zero-local seed | 0.019293871352 |

The new tightest gate is much thinner than the fresh-window-only gate:
`164598` is only `0.0003925287417802202` below same-window nonseed target
`8000140` in weighted centered `(3,1)`.

## Interpretation

This strengthens the finite `(3,1)` evidence beyond the fresh predeclared
windows and beyond handpicked same-residue clear controls.  It does not prove
a theorem.  It sharpens the proof obligation: any analytic or structural
explanation must survive the near-collision at reference `164598`, residue
`5`, comparison target `8000140`.

## Falsifier

Any future available or predeclared same-residue nonselection target `T` with:

```text
weighted_centered_3_1(T) <= weighted_centered_3_1(R)
```

for a selected deficit reference `R` falsifies the corresponding finite or
proposed uniform signed-gap claim.

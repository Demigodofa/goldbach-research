# q286-WBSS K286 quarter-residual lift-depth stress

## Question

The `280`-row quarter-residual companion audit left a fragile finite
candidate:

```text
A_other(N) <= (1/4) * (M(N) - H_286(N)).
```

Does that quarter candidate survive if the zero-residue lift depth is doubled
from `8` to `16` lifts for all `35` period classes?

## Receipt

```text
tools/build_q286_wbss_k286_quarter_residual_lift_depth_stress.py
evidence/q286-wbss-k286-quarter-residual-lift-depth-stress.json
```

## Finite Stress Result

```text
rows:                                      560
target range:                   1156012..1315886
quarter-residual surviving rows:          560 / 560
quarter-residual nonpositive rows:          0 / 560
residual-payment route failed rows:         0 / 560

H_286/M max:                    0.7254295025978773
A_other/M max:                  0.10230465175850566
A_other/(M-H_286) max:          0.24495753331096648
quarter margin ratio min:       0.0013845125869415692
```

The tight row did not move:

```text
target:                         1201486
target residue:                     286
period residue index:                 1
lift index:                           4
H_286/M:             0.7254295025978773
A_other/M:           0.0672581117635891
A_other/(M-H_286):   0.24495753331096648
quarter margin:      0.0013845125869415692
```

The deeper stress does expose a larger raw companion adverse ratio
`A_other/M = 0.10230465175850566`, but not on a row with a small enough
post-`H_286` residual budget to beat the previous quarter-residual maximum.

## Decision

`PROBE_k286_quarter_residual_survives_lift_depth_stress`.

The quarter-residual companion candidate survives this changed-condition
`560`-row finite stress.  This is useful because it failed to find the obvious
nearby falsifier: deeper zero-residue lifts did not worsen the tight
`A_other/(M-H_286)` row.

The next theorem-shaped obligation is unchanged and sharper than a finite
fit: prove a universal pointwise analytic estimate

```text
A_other(N) <= c(N) * (M(N)-H_286(N))
```

with `c(N)<1` for every sufficiently large covered target after proving
`H_286(N)<M(N)`, plus a finite remainder.  The finite value `1/4` remains a
calibration and falsifier target only, not a theorem constant.

This proves no quarter-residual theorem, no `K_286` absolute-envelope theorem,
no companion adverse-drag theorem, no same-row tradeoff theorem, no universal
pointwise raw bound, no q286 threshold theorem, no strict-central Goldbach
theorem, and no Goldbach proof.

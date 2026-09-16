# q286-WBSS K286 quarter-residual companion obligation

## Question

After paying the `K_286` absolute envelope, does the companion adverse drag fit
inside one quarter of the remaining local-main budget on the finite
lift-depth fixture?

## Candidate Inequality

The tested finite shape is

```text
A_other(N) <= (1/4) * (M(N) - H_286(N)).
```

Equivalently,

```text
A_other(N) / (M(N) - H_286(N)) <= 1/4.
```

This is meaningful only after `H_286(N)<M(N)` leaves positive residual budget.

## Receipt

```text
tools/build_q286_wbss_k286_quarter_residual_companion_obligation.py
evidence/q286-wbss-k286-quarter-residual-companion-obligation.json
```

## Finite Calibration

The receipt reads the `280`-row zero-residue lift-depth probe.

```text
rows:                                    280
target range:                   1156012..1235806
quarter-residual surviving rows:         280 / 280
quarter-residual nonpositive rows:         0 / 280

residual after H_286: min 0.2745704974021227
residual after H_286: mean 0.692196021998406
residual after H_286: max 0.87129663381704

A_other / residual: min 0.0
A_other / residual: mean 0.031684529803067824
A_other / residual: max 0.24495753331096648

quarter margin ratio: min 0.0013845125869415692
quarter margin ratio: mean 0.1524564936839005
quarter margin ratio: max 0.21400834184099196
```

The tight row is again target `1201486`, residue `286`, lift `4`:

```text
H_286/M:                       0.7254295025978773
A_other/M:                     0.0672581117635891
residual after H_286:          0.2745704974021227
A_other / residual:            0.24495753331096648
quarter margin ratio:          0.0013845125869415692
```

So the quarter candidate survives the finite fixture, but barely.  The small
slack makes it a useful falsifier target, not a theorem constant.

## Decision

`TARGET_k286_quarter_residual_companion_theorem_candidate`.

The finite `280`-row fixture supports a sharper companion target: after paying
`H_286`, `A_other` consumes less than one quarter of the remaining local-main
budget.  A proof would still need a source-backed theorem, or a different
constant `c<1`, plus a finite remainder.

This proves no quarter-residual theorem, no `K_286` absolute-envelope theorem,
no companion adverse-drag theorem, no same-row tradeoff theorem, no universal
pointwise raw bound, no q286 threshold theorem, no strict-central Goldbach
theorem, and no Goldbach proof.

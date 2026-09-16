# Mobius moment-square degree-5 weak-prime phase-curve sweep

## Question

The active-window translation stress found that the weakest checked row moved
to active row start `36`, prime `181`, component `(00,12)`.  Does a broader
local sweep of the same weakest prime expose a concrete active/full dominance
failure?

## Mechanism

Keep the weak scale `M=167`, row count `35`, coefficient freeze
`ell_freeze=52`, divisor range `[3,16]`, and the weakest prime `181`.  Sweep
the active row start through

```text
0, 1, 2, ..., 70
```

For each start, test the three degree-`5` component rows `(00,12)`,
`(01,02)`, and `(01,11)` and their degree-`5` total.  Under the negative
signed-full premise, the target is

```text
active/full > 1/2
```

for every checked row.

This is not a full period theorem.  The phase periods are controlled by the
reduced denominators inside the exact residue expansion, not by the prime or
the row count alone.

## Receipt

```text
tools/build_mobius_moment_square_degree5_weak_prime_phase_curve_sweep.py
evidence/mobius-moment-square-degree5-weak-prime-phase-curve-sweep.json
```

## Result

```text
status:                      SWEEP_degree5_weak_prime_active_window_phase_curve
scale:                       M=167
prime:                       181
ell_freeze:                  52
tested active row starts:    0..70
component rows:              213
degree-5 total rows:         71
all dominance rows:          284
dominance slacks:            +284 / 0 / 0
failure rows:                0
weakest row:                 start=44, p=181, (00,12)
weakest active/full ratio:   0.5370450115638492
weakest slack above 1/2:     0.037045011563849206
```

## Decision

The weakest-prime extended local phase-curve sweep survives.  Every component
and degree-`5` total row for active row starts `0..70` retains positive
active/full dominance slack above one half.  The broader sweep is materially
tighter than the five-start translation stress: the weakest start moves from
`36` to `44`, and the weakest slack falls from about `0.04905` to about
`0.03705`.

This is useful curve-shape evidence for the active-window theorem target, but
it is still finite perturbation evidence only.  It proves no phase-curve
theorem, active-window translation theorem, checked-scale dominance theorem,
primewise dominance theorem, degree-`5` coefficient theorem, robust-margin
universal theorem, coefficient-family theorem, universal Sturm-certificate
theorem, half-frame curve-positivity theorem, uniform active/full lower-frame
theorem, Mobius covariance theorem, signed prime-correlation estimate, q286
theorem, strict-central Goldbach theorem, or Goldbach proof.

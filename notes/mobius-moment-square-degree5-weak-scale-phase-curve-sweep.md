# Mobius moment-square degree-5 weak-scale phase-curve sweep

## Question

The weakest-prime phase-curve sweep found a tighter trough at active row start
`44`, prime `181`, component `(00,12)`.  Does the same extended local row-start
sweep expose any degree-`5` active/full dominance failure when applied to every
prime in the weak scale?

## Mechanism

Keep the weak scale `M=167`, row count `35`, coefficient freeze
`ell_freeze=52`, divisor range `[3,16]`, and every prime in `[167,334]`.
Sweep each prime's active row start through

```text
0, 1, 2, ..., 70
```

For each prime and start, test the three degree-`5` component rows
`(00,12)`, `(01,02)`, and `(01,11)` and their degree-`5` total.  Under the
negative signed-full premise, the target is

```text
active/full > 1/2
```

for every checked row.

This is not a full period theorem.  The phase periods are controlled by the
reduced denominators inside the exact residue expansion, not by the prime or
the row count alone.

## Receipt

```text
tools/build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep.py
evidence/mobius-moment-square-degree5-weak-scale-phase-curve-sweep.json
```

## Result

```text
status:                      SWEEP_degree5_weak_scale_active_window_phase_curve
scale:                       M=167
ell_freeze:                  52
primes checked:              29
tested active row starts:    0..70
component rows:              6177
degree-5 total rows:         2059
all dominance rows:          8236
dominance slacks:            +8236 / 0 / 0
failure rows:                0
weakest row:                 start=44, p=181, (00,12)
weakest active/full ratio:   0.5370450115638492
weakest slack above 1/2:     0.037045011563849206
```

## Decision

The weak-scale extended local phase-curve sweep survives.  Every component and
degree-`5` total row for every weak-scale prime and active row start `0..70`
retains positive active/full dominance slack above one half.

This is useful curve-family evidence for the active-window theorem target, but
it is still finite perturbation evidence only.  It proves no phase-curve
theorem, active-window translation theorem, checked-scale dominance theorem,
primewise dominance theorem, degree-`5` coefficient theorem, robust-margin
universal theorem, coefficient-family theorem, universal Sturm-certificate
theorem, half-frame curve-positivity theorem, uniform active/full lower-frame
theorem, Mobius covariance theorem, signed prime-correlation estimate, q286
theorem, strict-central Goldbach theorem, or Goldbach proof.

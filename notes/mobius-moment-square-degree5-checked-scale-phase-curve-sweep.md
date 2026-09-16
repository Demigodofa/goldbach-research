# Mobius moment-square degree-5 checked-scale phase-curve sweep

## Question

The weak-scale phase-curve sweep survived all weak-scale primes and active row
starts `0..70`.  Does the same active-window phase-curve stress survive across
all six checked degree-`5` scales?

## Mechanism

For each checked scale

```text
127, 149, 167, 191, 211, 227
```

use the scale's own row count `A`, coefficient freeze, divisor range, and every
prime row in `[M,2M]`.  Sweep active row starts `0..2A`.  For each scale,
prime, and start, test the three degree-`5` component rows `(00,12)`,
`(01,02)`, and `(01,11)` and their degree-`5` total.  Under the negative
signed-full premise, the target is

```text
active/full > 1/2
```

for every checked row.

This is not a full period theorem.  The phase periods are controlled by the
reduced denominators inside the exact residue expansion, not by the scale,
prime, or row count alone.

## Receipt

```text
tools/build_mobius_moment_square_degree5_checked_scale_phase_curve_sweep.py
evidence/mobius-moment-square-degree5-checked-scale-phase-curve-sweep.json
```

## Result

```text
status:                      SWEEP_degree5_checked_scale_active_window_phase_curve
scales:                      127, 149, 167, 191, 211, 227
total primes checked:        189
component rows:              42507
degree-5 total rows:         14169
all dominance rows:          56676
dominance slacks:            +56675 / 0 / -1
failure rows:                1
falsifier row:               M=149, start=1, p=163, (00,12)
falsifier active/full ratio:  0.4980466670754268
falsifier slack above 1/2:    -0.0019533329245732256
```

Scale row counts:

```text
M=127:  24 primes, 57 starts,  5472 dominance rows
M=149:  28 primes, 65 starts,  7280 dominance rows
M=167:  29 primes, 71 starts,  8236 dominance rows
M=191:  33 primes, 77 starts, 10164 dominance rows
M=211:  36 primes, 83 starts, 11952 dominance rows
M=227:  39 primes, 87 starts, 13572 dominance rows
```

## Decision

The broad checked-scale active-window phase-curve extension is falsified
finitely.  The single failing row is `M=149`, prime `163`, active row start
`1`, component `(00,12)`, with active/full ratio `0.4980466670754268`, just
below the signed `1/2` threshold.

This does not refute the original source-window checked-scale dominance audit,
the weak-scale phase-curve sweep, or Goldbach.  It refutes the broader
quantifier tested here: active-window dominance cannot be promoted as
surviving every checked scale, prime, and local active row start `0..2A`.
The next theorem-shaped target must either use the source-window geometry more
specifically, restrict admissible row starts, or prove a different analytic
margin that does not require this broad phase-curve dominance statement.

This is finite falsifier evidence only.  It proves no phase-curve theorem,
active-window translation theorem, checked-scale dominance theorem, primewise
dominance theorem, degree-`5` coefficient theorem, robust-margin universal
theorem, coefficient-family theorem, universal Sturm-certificate theorem,
half-frame curve-positivity theorem, uniform active/full lower-frame theorem,
Mobius covariance theorem, signed prime-correlation estimate, q286 theorem,
strict-central Goldbach theorem, or Goldbach proof.

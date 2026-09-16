# Mobius moment-square half-frame curve audit

## Question

The payment-margin audit checked the moment-square active/full minimizer and
the diagonal-equilibrated full-soft parameter.  Does the stronger whole-curve
statement survive: is

```text
y(t)^T(active - 0.5*full)y(t) > 0
```

for every real moment-square parameter `t` on the checked scales?

## Receipt

```text
tools/build_mobius_moment_square_half_frame_curve_audit.py
evidence/mobius-moment-square-half-frame-curve-audit.json
```

## Mechanism

For `y(t) = (t^4,t^3,t^2,t^2,t,1)`, form the explicit degree-8 polynomial

```text
P_M(t) = y(t)^T(active_M - 0.5*full_M)y(t).
```

Then compute its real stationary parameters and evaluate the polynomial there
and at `t=0`.  With positive leading coefficient, a nonpositive real-line
minimum would be a finite falsifier for the half-frame curve target.

## Result

```text
status: TARGET_moment_square_half_frame_curve_positivity
checked scales:                    127, 149, 167, 191, 211, 227
all curve minima positive:          true
minimum half-frame curve value:     0.427001953125
weakest scale:                      167
weakest parameter:                  0.26983489124712867
weakest leading coefficient:        122048235269918.23
```

Per-scale minima:

```text
M=127  min P_M(t) = 0.9832426309585571    at t=0.2761636698862329
M=149  min P_M(t) = 0.6679186820983887    at t=0.26969967515077853
M=167  min P_M(t) = 0.427001953125        at t=0.26983489124712867
M=191  min P_M(t) = 113.0789680480957     at t=0.2670275343507519
M=211  min P_M(t) = 61.90129852294922     at t=0.2611749300409263
M=227  min P_M(t) = 46.85480499267578     at t=0.2601269275971193
```

## Decision

The checked half-frame payment is positive on the entire moment-square curve,
not merely at the previously selected soft directions.  This gives a sharper
analytic target: prove positivity of the explicit degree-8 form
`P_M(t) = y(t)^T(active_M - 0.5*full_M)y(t)` in the intended universal
regime, or find a legitimate scale where the real-line minimum is
nonpositive.

This remains finite diagnostic evidence only.  No half-frame curve-positivity
theorem, moment-square half-frame payment theorem, uniform active/full
lower-frame theorem, Mobius covariance theorem, signed prime-correlation
estimate, q286 theorem, strict-central Goldbach theorem, or Goldbach proof is
established.

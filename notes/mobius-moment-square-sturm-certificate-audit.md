# Mobius moment-square Sturm certificate audit

## Question

The half-frame curve audit used floating polynomial minimization.  Can the
recorded checked polynomials be certified positive by an algebraic
Sturm/root-count certificate?

## Receipt

```text
tools/build_mobius_moment_square_sturm_certificate_audit.py
evidence/mobius-moment-square-sturm-certificate-audit.json
```

## Mechanism

For each recorded degree-8 polynomial

```text
P_M(t) = y(t)^T(active_M - 0.5*full_M)y(t)
```

from `evidence/mobius-moment-square-half-frame-curve-audit.json`, convert the
decimal coefficients to exact rational numbers and test

```text
P_M(t) - 427/1000.
```

If the shifted polynomial has positive leading coefficient, positive value at
`t=0`, and zero real roots by Sturm/root counting, then it is positive on the
entire real line.

## Result

```text
status: CERTIFY_checked_moment_square_half_frame_curve_margin
certified margin:                    427/1000
checked scales:                      127, 149, 167, 191, 211, 227
all shifted polynomials root-free:   true
all certificates pass:               true
weakest source scale:                167
weakest source curve minimum:        0.427001953125
weakest source parameter:            0.26983489124712867
```

Each checked shifted polynomial has real-root count `0`, Sturm sequence length
`9`, positive leading coefficient, and positive value at `t=0`.

## Decision

The checked half-frame curve positivity has now been upgraded from optimizer
evidence to an algebraic certificate for the recorded rationalized
polynomials.  This still does not prove the universal theorem; the coefficients
themselves came from finite checked frames.

The next theorem-shaped target is no longer just "minimize a degree-8 curve."
It is:

```text
derive the coefficient family for P_M(t), then prove a uniform Sturm/sign
certificate or find a legitimate scale where the certificate fails.
```

This is a finite polynomial certificate only.  No universal Sturm-certificate
theorem, half-frame curve-positivity theorem, uniform active/full lower-frame
theorem, Mobius covariance theorem, signed prime-correlation estimate, q286
theorem, strict-central Goldbach theorem, or Goldbach proof is established.

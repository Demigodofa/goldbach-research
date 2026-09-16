# Mobius moment-square nullspace audit

## Question

The rank-aware lower-frame receipt isolated `M=167` as the only checked
nonvacuous scale with full Gram rank deficiency and a visible null-coupling
attention term.  Is that null direction generic, or does it have structure?

## Receipt

```text
mobius_moment_square_nullspace.py
tools/build_mobius_moment_square_nullspace_audit.py
evidence/mobius-moment-square-nullspace-audit.json
```

## Result

The original-coordinate full-null direction at `M=167` is:

```text
(0.00489332, 0.01830422, 0.06851065,
 0.06850900, 0.25657256, 0.96146989)
```

This is almost the symmetric square of the moment-curve vector
`(t^2, t, 1)`:

```text
t = 0.26688993201398403
(t^4,t^3,t^2,t^2,t,1) projective distance = 5.6622814065029987e-05
projective correlation = 0.9999999983969288
```

As a symmetric `3 x 3` matrix, the null direction is nearly rank one:

```text
eigenvalues = (4.047736e-09, 4.939719e-05, 1.034823)
second / largest = 4.773492818229947e-05
smallest / largest = 3.9115257750081936e-09
```

The active coupling that triggered attention is:

```text
active-positive/null coupling norm = 3.4467540535129906e-08
active null energy = 1.0452667763081322e-12
```

## Decision

The checked nullspace issue is not generic nullspace chaos.  It points back to
moment-square geometry.  The next theorem target should analyze support
activation and active coupling near moment-square null directions, not merely
state abstract nullspace control.

This is finite diagnostic evidence only.  No support-activation theorem,
uniform active/full lower-frame theorem, Mobius covariance theorem, signed
prime-correlation estimate, q286 theorem, strict-central Goldbach theorem, or
Goldbach proof is established.

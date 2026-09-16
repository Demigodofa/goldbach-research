# Mobius moment-square metric audit

## Question

The `M=167` nullspace audit showed a near moment-square direction.  Is that
direction a raw full-energy support failure, or is it soft only in the
diagonal-equilibrated metric used by the rank-aware lower-frame quotient?

## Receipt

```text
mobius_moment_square_metric.py
tools/build_mobius_moment_square_metric_audit.py
evidence/mobius-moment-square-metric-audit.json
```

## Result

On checked nonvacuous scales, the raw Euclidean moment-square energy is
positive:

```text
M=127  raw minimum = 2.1869115326511652
M=149  raw minimum = 1.3031066231016835
M=167  raw minimum = 0.9381026269590562
M=191  raw minimum = 192.357186548757
```

But the same moment-square curve is extremely soft in the diagonal-equilibrated
quotient metric:

```text
M=127  equilibrated minimum = 3.399727863609262e-11
M=149  equilibrated minimum = 5.318977967228153e-12
M=167  equilibrated minimum = 3.2957447749809375e-12
M=191  equilibrated minimum = 6.394855572842169e-11
```

The minimizing parameters stay in a narrow band:

```text
0.27603534765337445
0.2698749461997662
0.2698106456761942
0.2678068447008048
```

## Decision

Moment-square support activation is metric-aware.  A raw Euclidean support
lower bound is not the right target: raw energy is positive, while the
diagonal-equilibrated quotient still has near-null moment-square directions.
The proof target must control this equilibrated soft direction.

This is finite diagnostic evidence only.  No support-activation theorem,
uniform active/full lower-frame theorem, Mobius covariance theorem, signed
prime-correlation estimate, q286 theorem, strict-central Goldbach theorem, or
Goldbach proof is established.

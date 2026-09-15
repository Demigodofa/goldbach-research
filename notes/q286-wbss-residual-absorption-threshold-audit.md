# q286-WBSS Residual Absorption Threshold Audit

Status: finite threshold diagnostic. Goldbach is not proved.

Receipt:

```text
tools/build_q286_wbss_residual_absorption_threshold_audit.py
evidence/q286-wbss-residual-absorption-threshold-audit.json
```

## Question

Kevin asked whether `.13` is too strict, and whether `.125` works, for the
one-sided residual absorption target left by the top-20 Fourier split.

The target is:

```text
positive_residual_pushback(N) <= theta * top20_drag(N).
```

Here the diagnostic only tests the current `196` post-discovery q286-WBSS rows.
It does not prove any universal residual theorem.

## Result

The worst checked row is:

```text
target:                          365578
target residue:                  5218
target mod 286:                  70
pair count:                      1111
top-20 component:               -0.3420907424756105
five-group residual component:   0.04298944106162803
pushback / top-20 drag:          0.12566677703853088
```

Therefore:

```text
theta = 0.125 = 1/8   fails, by one row
theta = 0.126         passes this fixture
theta = 0.127         passes this fixture
theta = 0.13          passes this fixture
```

The `.13` cap has absolute slack

```text
0.13 - 0.12566677703853088 = 0.00433322296146912
```

which is about `3.45%` of the observed maximum ratio. That is finite slack,
not theorem slack.

## Decision

Retire the exact `1/8` cap for this q286-WBSS fixture. Preserve `.126` and
`.13` only as constants that fit the current finite data. The universal
residual absorption bound is open. For any proof attempt, keep the statement
symbolic as `theta < 1` until a uniform signed residual estimate justifies a
specific constant.

## Boundary

This audit proves no residual absorption theorem, no signed projection theorem,
no q286 threshold theorem, no strict-central Goldbach theorem, and no Goldbach
proof. It only answers the current finite threshold question.

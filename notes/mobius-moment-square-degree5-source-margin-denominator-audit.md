# Mobius moment-square degree-5 source-margin denominator audit

## Question

For the tightest checked source-start prime blocks, is the positive
unnormalized theorem margin

```text
full/2 - active > 0
```

denominator-local, diffuse, or cancellation-dependent?

## Mechanism

For the tightest prime block at each checked source scale, decompose the
weakest label's margin by reduced denominator:

```text
M=229, p=379, label (00,12)
M=251, p=379, label (00,12)
M=293, p=461, label (00,12)
M=331, p=599, label (00,12)
M=353, p=599, label (00,12)
M=379, p=599, label (00,12)
```

For each reduced denominator `q`, compute:

```text
margin_q = full_q/2 - active_q
```

and compare the positive denominator sum against the adverse denominator sum.

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_margin_denominator_audit.py
evidence/mobius-moment-square-degree5-source-margin-denominator-audit.json
```

## Result

```text
reduced denominator counts:              28..77
minimum adverse/positive ratio:          0.00034280843897457745
maximum adverse/positive ratio:          0.000878341064244336
```

The tightest `M=379`, `p=599`, `(00,12)` ledger is:

```text
total margin:              267181208856715.3
positive denominator sum:  267329631995333.88
negative denominator sum: -148423138618.55527
adverse/positive ratio:    0.0005552064599450985
largest positive q:        156009
largest negative q:         52003
```

So the checked tight margins are not a fragile cancellation of comparable
positive and negative denominator masses.  The adverse denominator mass is
small relative to the positive denominator mass in all six tight blocks.

## Decision

The next theorem subtarget should be a signed reduced-denominator margin
ledger:

```text
sum_q (full_q/2 - active_q) > 0
```

after grouping denominators into stable families.  It is probably too strong
to require every individual reduced denominator to be positive, but the finite
data says the adverse ledger is small enough that a positive-family dominance
theorem is a plausible target.

This is finite denominator-decomposition evidence only.  It proves no
denominator-margin theorem, no prime-block theorem, no source-start theorem,
no source-window theorem, no strict-central Goldbach theorem, and no Goldbach
proof.

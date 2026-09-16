# Mobius moment-square payment-margin audit

## Question

The active/full ratio audit showed that the metric-soft moment-square
direction is not adverse on the checked scales.  But ratio evidence alone is
not the theorem target.  What exact unnormalized inequality would have to be
proved?

## Receipt

```text
tools/build_mobius_moment_square_payment_margin_audit.py
evidence/mobius-moment-square-payment-margin-audit.json
```

## Mechanism

For each checked scale, test the two theorem-relevant directions:

```text
moment_square_active_over_full_minimizer
diagonal_equilibrated_full_soft_parameter
```

For each direction `y`, record the raw quadratic values

```text
active = y^T A y
full   = y^T F y
```

and the half-frame payment margin

```text
active - 0.5 * full
```

This is the unnormalized pointwise shape a theorem would need to prove for
the metric-soft moment-square channel.

## Result

```text
status: TARGET_moment_square_half_frame_payment_margin
checked scales:                       127, 149, 167, 191, 211, 227
checked directions:                   12
all half-frame margins positive:      true
minimum half-frame margin/full:       0.4122467414896579
minimum raw half-frame margin:        0.4270438141147679
most negative active-full/full:      -0.08775325851034213
```

The weakest normalized half-frame margin occurs at `M=127`, at the
diagonal-equilibrated full-soft parameter:

```text
t:                       0.27603534765337445
full:                    2.3861329393694177
active:                  2.1767419987008907
active/full:             0.9122467414896579
active - 0.5*full:       0.9836755290161818
(active - 0.5*full)/full 0.4122467414896579
active - full:          -0.20939094066852704
```

The weakest raw half-frame margin occurs at `M=167`, also at the
diagonal-equilibrated full-soft parameter:

```text
t:                       0.2698106456761942
full:                    1.0183856931216724
active:                  0.9362366606756041
active/full:             0.9193340666498803
active - 0.5*full:       0.4270438141147679
(active - 0.5*full)/full 0.41933406664988027
active - full:          -0.0821490324460683
```

## Decision

The checked moment-square soft directions are active-paid relative to the
one-half full-frame target in unnormalized quadratic form.  However, active
does not always exceed full, so the proof target must not be promoted to
`active >= full`.

The theorem-shaped target is:

```text
active(y_N, N) - 0.5 * full(y_N, N) > 0
```

for the metric-soft moment-square channel, uniformly or for every sufficiently
large `N` in the intended lower-frame regime.  A falsifier is any legitimate
large-scale row where this half-frame margin is nonpositive.

This remains finite diagnostic evidence only.  No moment-square half-frame
payment theorem, uniform active/full lower-frame theorem, Mobius covariance
theorem, signed prime-correlation estimate, q286 theorem, strict-central
Goldbach theorem, or Goldbach proof is established.

# q286 anti-landing mass-balance audit

Status: finite derived diagnostic.  This is not a mass-balance theorem,
coefficient-weighted anti-landing theorem, signed prime-correlation theorem,
q286 threshold theorem, strict-central Goldbach theorem, or Goldbach proof.

## Question

The edge-minorant obstruction showed that the dual-edge rescue coefficient

```text
gap-required
```

has both positive and negative regions.  This audit asks whether the rescue
can be reduced to a simple mass-majority cone:

```text
mass(positive rescue coefficients)
  >
mass(negative rescue coefficients).
```

If that were true on every rescued tail row, the next theorem might ignore
coefficient magnitudes and only prove a coarse distributional bias away from
the negative region.

## Result

`tools/build_q286_anti_landing_mass_balance_audit.py` generated
`evidence/q286-anti-landing-mass-balance-audit.json`.

On the `196` post-discovery rows:

```text
mass-majority pass count:              178 / 196
mass-majority fail count:               18 / 196
weighted-landing pass count:           196 / 196
rescued without mass majority:          18 / 196
positive mass range:                   0.42889930876228677..0.672699487987144
negative mass range:                   0.32730051201285604..0.5711006912377132
coefficient lift ratio range:          0.8172153202913576..2.4374947926389594
required lift ratio range:             0.48654788335309557..1.3315495725227204
coefficient lift surplus range:        0.01681775158832699..1.568503471168754
positive/negative rescue ratio range:  1.0191444227555964..3.167398344085266
```

Thus mass majority is not the theorem.  Eighteen checked post-discovery rows
rescue despite carrying more actual mass on negative pointwise rescue
coefficients than on positive ones.

## The surviving inequality

For a checked row, write:

```text
M+ = actual mass on {gap-required > 0}
M- = actual mass on {gap-required < 0}
A+ = average positive rescue coefficient
A- = average negative drag coefficient
```

The signed rescue inequality is:

```text
M+ * A+ > M- * A-.
```

Equivalently, when both masses are positive:

```text
A+ / A- > M- / M+.
```

All `196` post-discovery rows satisfy this weighted inequality, and the
minimum checked lift surplus is `0.01681775158832699`.

## Decision

Demote the simple mass-majority cone.  The q286 bridge cannot be:

```text
actual pair mass lands more often on positive rescue coefficients.
```

It must be coefficient-sensitive:

```text
actual pair mass may land more often on the negative side,
but the average positive landing strength must beat the average negative drag.
```

This is sharper and closer to a signed binary-prime correlation theorem.  It
also explains why repeated label, subset, and unweighted-cone audits were not
closing the hole: the live object is not just support; it is signed landing
quality.

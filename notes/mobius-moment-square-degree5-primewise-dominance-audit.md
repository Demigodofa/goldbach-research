# Mobius moment-square degree-5 primewise dominance audit

## Question

The weak-block primewise sign-localization audit showed that every prime in
the `M=167` block has negative degree-`5` half-frame contributions for
`(00,12)`, `(01,02)`, and `(01,11)`.  How far is that sign pass from the
actual threshold?

## Mechanism

For each component row, compute

```text
active_over_full = active_contribution / full_contribution
dominance_slack = active_over_full - 1/2
```

When both active and full contributions are negative, the observed inequality

```text
active - (1/2) full < 0
```

is equivalent to

```text
active_over_full > 1/2.
```

## Receipt

```text
tools/build_mobius_moment_square_degree5_primewise_dominance_audit.py
evidence/mobius-moment-square-degree5-primewise-dominance-audit.json
```

## Result

```text
status: MEASURE_degree5_primewise_dominance_slack
scale:                                      M=167
prime count:                                29
component rows:                             87
component dominance slacks:                 positive 87, zero 0, negative 0
degree-5 total dominance slacks:            positive 29, zero 0, negative 0
all component ratios exceed 1/2:            true
all degree-5 total ratios exceed 1/2:       true
```

Weakest component row:

```text
prime:                                      181
component:                                  (00,12)
active/full ratio:                          0.5563677490893767
slack above 1/2:                            0.056367749089376695
```

Weakest degree-`5` total row:

```text
prime:                                      181
active/full ratio:                          0.5696364991895461
slack above 1/2:                            0.06963649918954606
```

## Decision

The weak-block sign-localization result is not merely barely negative in this
finite fixture.  The weakest component has about `0.05637` active/full slack
above the signed `1/2` threshold, and the weakest degree-`5` total has about
`0.06964` slack.

This turns the next theorem-shaped target into a quantitative dominance
claim: prove, under the weak-block parameter rules, that each local one-prime
degree-`5` active/full component ratio for `(00,12)`, `(01,02)`, and
`(01,11)` stays above `1/2`, preferably with a structural margin.

This is finite weak-block dominance evidence only.  No primewise dominance
theorem, primewise sign theorem, degree-`5` coefficient theorem,
robust-margin universal theorem, coefficient-family theorem, universal Sturm
certificate, half-frame curve-positivity theorem, uniform active/full
lower-frame theorem, Mobius covariance theorem, signed prime-correlation
theorem, q286 theorem, or Goldbach proof is established.

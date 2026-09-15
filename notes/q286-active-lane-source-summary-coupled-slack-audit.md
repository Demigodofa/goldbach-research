# q286 active-lane source-summary coupled-slack audit

## Question

The 11-row post-discovery stress view suggested that strict-closure pass/fail
is governed by a channel-payment ratio: channel contribution divided by driver
deficit.  Is that only a tautological description of the selected stress rows,
or does the same coordinate describe a broader active source-summary fixture?

## Fixture

Use every unique active row already present in the
`q286-principal-rescue-obstruction-audit` source summaries:

```text
worst_full_rows
tightest_principal_only_rows
first_full_failure_rows
```

An active row satisfies:

```text
first_two_modes_to_principal_ratio < -0.2
first_three_modes_to_principal_ratio < -0.3
```

This gives `226` unique active source-summary rows.  The calibration constants
remain frozen from the selected-late targets
`14138, 1222142, 1323632, 1379072`.

## Receipt

```text
tools/build_q286_active_lane_source_summary_coupled_slack_audit.py
evidence/q286-active-lane-source-summary-coupled-slack-audit.json
```

## Result

```text
unique active source-summary rows:       226
positive coupled slack rows:              83
nonpositive coupled slack rows:          143
driver floor condition met:                9
driver floor condition failed:           217
channel Linf condition met:              171
channel Linf condition failed:            55
negative-driver rows with payment ratio: 217
payment ratio above 1:                    74
payment ratio at or below 1:             143
nonnegative-driver positive rows:          9
ratio/sign mismatches on negative-driver rows: 0
```

Worst and tightest rows:

```text
worst strict margin:          N=95066   -1.3064058812318107
best strict margin:           N=775426   0.6449778835184072
tightest positive margin:     N=395102   0.004360504169358126
nearest nonpositive margin:   N=495086  -0.0016456439616709395
```

Block summary:

```text
block  active  positive  nonpositive
1      36      0         36
2      34      2         32
3      36      10        26
4      32      16        16
5      30      16        14
6      31      16        15
7      17      13        4
8      1       1         0
9      5       5         0
10     3       3         0
11     1       1         0
```

## Interpretation

The payment-ratio hinge is real as a diagnostic coordinate on the
negative-driver subpopulation: there are no finite mismatches between
`channel_payment_ratio_to_driver_deficit > 1` and positive strict closure
among the `217` rows with negative driver margin.  The other `9` positive rows
are driver-carried because their driver margin is already nonnegative.

But the widened fixture also blocks a finite pass claim.  Only `83/226`
source-summary active rows have positive coupled slack, and `143/226` fail the
frozen endpoint.  The 11-row viewer hinge was a good locator, not a theorem.

## Decision

Preserve the coupled payment coordinate, but demote it from "finite evidence
that the active population passes" to "diagnostic coordinate for what an
analytic theorem must pay."  The next theorem-shaped target is still a coupled
pointwise tradeoff or direct unnormalized signed estimate.  The finite source
summary now gives sharper requirements:

- either prove a phase/scale transition that excludes early failing active
  rows beyond a finite boundary;
- or prove a direct signed estimate strong enough to cover the `143`
  nonpositive source-summary rows;
- or replace the frozen selected-late constants/decomposition with a
  non-fixture theorem.

## Boundary

Finite source-summary coupled-slack audit only.  The source-summary rows are
compact representative rows from the principal-rescue receipt, not all active
targets.  This proves no universal active-lane theorem, pointwise adverse-drag
theorem, q286 threshold theorem, strict-central Goldbach theorem, or Goldbach
proof.

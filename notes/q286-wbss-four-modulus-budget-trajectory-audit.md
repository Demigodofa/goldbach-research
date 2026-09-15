# q286-WBSS Four-Modulus Budget-Trajectory Audit

Status: finite diagnostic algebra. This is not a recurrence theorem,
fixed-modulus equidistribution theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

## Question

After the positivity-budget audit identifies `lambda_phi < 1` as the live
target, this receipt asks whether the stress is a monotone residue-class
trajectory or a row-local signed fluctuation. It groups the two four-lift
holdouts into `29` source-residue trajectories with eight period lifts each.

## Receipt

```text
tools/build_q286_wbss_four_modulus_budget_trajectory_audit.py
evidence/q286-wbss-four-modulus-budget-trajectory-audit.json
```

This receipt reuses the `232` rows from the positivity-budget audit and does
not recompute prime-orbit measures.

## Result

```text
trajectories checked:                 29
rows per trajectory:                   8
monotone nondecreasing trajectories:   0
trajectories with positive ratios:    28
trajectories with negative ratios:    29
trajectories with sign changes:       28
worst trajectory residue/source:   1478 / 251728
worst target:                    1002478
worst combined lift index:             4
maximum signed budget ratio: 0.29444884696113977
```

Worst-lift positions are spread across all eight checked indexes, with counts
`0:5, 1:3, 2:5, 3:4, 4:6, 5:2, 6:1, 7:3`. The worst trajectory is not
monotone: its signed budget ratios are approximately
`[-0.3113, 0.1361, -0.1423, -0.2959, 0.2944, 0.0342, -0.0930, 0.1473]`.

## Decision

The finite evidence does not support a simple monotone residue-class drift
theorem. The next theorem target should stay rowwise signed concentration or a
residue-class supremum bound for `lambda_phi < 1`, not a monotone recurrence.
Goldbach remains open.

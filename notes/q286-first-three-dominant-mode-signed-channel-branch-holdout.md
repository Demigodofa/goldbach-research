# q286 dominant-mode signed-channel branch holdout

Status: finite deterministic branch-denominator evidence only.  This is not
an eventual signed-channel branch theorem, not a pointwise character-sum
estimate, not a signed-projection theorem, and not a Goldbach proof.

## Mechanism

The selected signed-channel branch sample split the dominant two-mode floor
into the exact alternatives

```text
negative_pressure <= 0.3
or
positive_offset >= negative_pressure - 0.3
```

using the same `25` real q286 character channels.  This holdout freezes that
branch rule and applies it to the next nonoverlapping deterministic target
window after the recorded `1242000` stress-neighborhood window.

The falsifier for this finite check is a new unresolved deficit row in the
holdout window.  Such a row would become a named finite target for the
signed-channel branch theorem or a complement/lower-support rescue.  If no
deficit appears, the result is denominator evidence only.

## Receipt

- Function:
  `q286_first_three_dominant_mode_signed_channel_branch_holdout_receipt`
- Builder:
  `tools/build_q286_first_three_dominant_mode_signed_channel_branch_holdout.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-signed-channel-branch-holdout.json`
- Focused regression:
  `test_q286_first_three_dominant_mode_signed_channel_branch_holdout`

## Checked Window

```text
start: 1243000
target count: 101
targets: 1243000..1243200 by 2
```

Observed branch counts:

```text
tested targets with prime pairs: 101
dominant floor passes:           101
dominant floor failures:           0
pressure branch only:              0
offset branch only:                0
pressure and offset branches:    101
unresolved deficits:               0
```

The tightest clear row in this holdout is target `1243130`, with positive
offset slack about `0.0340510877`.  The maximum-pressure clear row is
target `1243018`, with negative pressure about `0.2586239309`; it is still
below the `0.3` pressure branch threshold.

## Interpretation

This window supplies clean denominator evidence for the branch mechanism:
after the selected near-boundary fixture, the next deterministic holdout
window contains no new unresolved deficit and every checked row clears both
branches.

It does not prove the branch theorem.  The missing proof input remains an
arithmetic estimate forcing either low negative pressure or enough positive
offset for actual binary-prime q286 character channels, or a separate
classification/rescue of all true deficit rows.

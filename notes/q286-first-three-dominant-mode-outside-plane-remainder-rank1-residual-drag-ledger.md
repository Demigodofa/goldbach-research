# q286 outside-plane rank-1 residual-drag ledger

Date: 2026-09-14

Status: finite residual-drag ledger only.  This is not a residual-bound
theorem, rank-`1` theorem, signed projection theorem, or Goldbach proof.

The previous Octave receipt found that rank `1` is already all-positive on the
`71 by 17` clear-minus-stress outside-channel delta matrix.  This receipt
measures the remaining obstruction: the negative row-sum residual after rank
`1`.

The evidence is:

```text
tools/build_q286_first_three_dominant_mode_outside_plane_remainder_rank1_residual_drag_ledger.py
evidence/q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-ledger.json
```

For each checked clear row, the builder verifies the identity:

```text
exact outside delta = rank-1 reconstructed outside delta + residual row-sum
```

It then measures residual drag as `max(0, -residual)` and tests simple caps of
the form:

```text
residual drag <= c * rank-1 reconstructed outside delta
```

On the checked `71` clear rows, the three-quarter cap holds.  The maximum
drag/rank-`1` ratio is about `0.7421344693`, at the exact closest clear
`1242118`.

The lower caps fail:

```text
c = 0.70   fails at 1242118
c = 0.50   fails at 1242118 and 1222048
c = 0.25   fails at 1242118, 1222048, and 1220056
```

This makes the loop tighter but also sharper: the surviving finite statement
is close to the data boundary.  A proof route cannot simply say the residual
is small.  It needs a non-post-hoc arithmetic reason that the negative
residual row-sum stays below the positive rank-`1` outside margin, with a
constant at least as weak as this checked three-quarter scale unless a stronger
decomposition replaces the SVD proxy.

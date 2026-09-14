# q286 outside-plane rank-1 residual-drag full-window audit

Date: 2026-09-14

Status: finite full-window audit only.  This is not a residual-bound theorem,
rank-`1` theorem, signed projection theorem, or Goldbach proof.

The previous expanded holdout widened the six near-boundary windows to the
closest `20` rows per window.  This receipt removes that closest-row filter
entirely and tests every evaluated target in the same six windows.

The evidence is:

```text
tools/build_q286_first_three_dominant_mode_outside_plane_remainder_rank1_residual_drag_full_window_audit.py
evidence/q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-full-window-audit.json
```

The full denominator has `716` targets.  The lone deficit is still stress row
`1222142`; the other `715` checked rows are clears.

The frozen Octave rank-`1` outside direction remains positive on all `715`
clear-minus-stress outside-channel vectors.  The exact outside delta is also
positive for every checked clear.  The `0.75` residual-drag cap survives:

```text
residual drag <= 0.75 * rank-1 reconstructed outside delta
```

The worst row is unchanged: `1242118`, with drag/rank-`1` about
`0.7421344693`.  The exact outside-delta minimum is also `1242118`, about
`0.0398241886`; the rank-`1` reconstructed minimum remains `1240160`, about
`0.1016883950`.

Lower caps remain refuted.  The `0.7` cap fails at `1242118`; the half-drag
cap fails at `1242118` and `1222048`; the quarter cap now fails at
`1242118`, `1222048`, `1220056`, and `1200254`; and the `0.2` cap fails at
ten checked rows.

This materially strengthens the finite stability of the rank-`1` plus
residual-drag shape.  It is now not just a closest-row effect inside the six
windows.  The theorem obligation remains: give a non-post-hoc arithmetic
meaning for the frozen rank-`1` outside direction and prove a residual-drag
inequality, or replace the SVD proxy with a stronger signed aggregate theorem.

# q286 outside-plane rank-1 residual-drag expanded holdout

Date: 2026-09-14

Status: finite expanded-holdout audit only.  This is not a residual-bound
theorem, rank-`1` theorem, signed projection theorem, or Goldbach proof.

The previous residual-drag ledger found a near-sharp finite cap on the
original `72`-row denominator:

```text
residual drag <= 0.75 * rank-1 reconstructed outside delta
```

This receipt widens the same six near-boundary windows from the closest `12`
rows per window to the closest `20` rows per window.  It then applies the
frozen Octave rank-`1` outside direction from the prior receipt without
refitting it.

The evidence is:

```text
tools/build_q286_first_three_dominant_mode_outside_plane_remainder_rank1_residual_drag_expanded_holdout.py
evidence/q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-expanded-holdout.json
```

The expanded denominator has `120` targets.  The lone deficit is still stress
row `1222142`; the other `119` checked rows are clears.

The frozen rank-`1` outside direction remains positive on all `119`
clear-minus-stress outside-channel vectors.  The `0.75` residual-drag cap also
survives the expansion.  The worst row is unchanged: `1242118`, with
drag/rank-`1` about `0.7421344693`.

Lower caps still fail:

```text
c = 0.70   fails at 1242118
c = 0.50   fails at 1242118 and 1222048
c = 0.25   fails at 1242118, 1222048, and 1220056
c = 0.20   fails at nine checked rows
```

This is a useful stability check.  The rank-`1` plus residual-drag shape is
not merely an artifact of retaining only the closest `12` rows per window.
But the bound remains close to the finite data boundary.  A proof still has to
give a non-post-hoc arithmetic explanation for the positive frozen rank-`1`
outside direction and for why residual drag cannot exceed the surviving cap.

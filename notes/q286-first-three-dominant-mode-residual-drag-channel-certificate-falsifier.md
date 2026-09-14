# q286 residual-drag channel-certificate falsifier

Date: 2026-09-14

Status: finite full-window diagnostic and falsifier for one proof shortcut.
This is not a residual-bound theorem, signed projection theorem, or Goldbach
proof.

The evidence is:

```text
tools/build_q286_first_three_dominant_mode_residual_drag_channel_certificate_falsifier.py
evidence/q286-first-three-dominant-mode-residual-drag-channel-certificate-falsifier.json
```

The candidate was that the negative residual row-sum after the frozen Octave
rank-`1` outside direction might have a small fixed channel certificate: a
single subset of at most five outside labels carrying at least `75%` of the
negative residual mass in every high-drag full-window row.

The falsifier recomputes the exact q286 full-window signed channel rows,
subtracts stress row `1222142` on the `17` outside labels, subtracts the frozen
Octave rank-`1` reconstruction, and brute-forces all fixed outside-label
subsets of sizes `1..5` on the high-drag rows
`residual_drag / rank1 >= 0.2`.

The small fixed-channel certificate is refuted.  There are `73` rows with
negative residual drag and `10` high-drag rows:

```text
1200254, 1200482, 1220056, 1220124, 1221052,
1222030, 1222048, 1222072, 1242070, 1242118
```

The best fixed five-label subset is:

```text
(1,9), (2,2), (2,8), (4,8), (5,1)
```

but its worst-row coverage is only about `0.3570706202`, at target `1200482`,
far below the `0.75` certificate threshold.  The high-drag rows also have no
common top-three negative-residual label.

This does not damage the previous finite `0.75` residual-drag cap; that cap
still survives the full-window denominator.  It does close the simplest sparse
proof explanation.  The next theorem route should not target a tiny static
bad-channel list.  It needs either a row-dependent arithmetic balance, a
larger signed cone with explicit coefficients, or a replacement aggregate
theorem that avoids the SVD residual altogether.

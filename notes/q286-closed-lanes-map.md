# q286 closed-lanes map

Status: finite research map, not a proof of Goldbach.
Last updated after the 2026-09-13 three-target component-pair probe.

This note indexes which q286 proof lanes have been closed, which components
survive as reusable structure, and what theorem obligation remains.  It is a
navigation aid for future work; the detailed evidence lives in
`q286-complement-alignment-theorem-obligation.md`, `RESEARCH_GOAL.md`, and
the executable receipts in `lcm_sawtooth_goldbach_transfer.py`.

Machine-readable graph data with typed nodes, edges, statuses, and evidence
metadata is stored beside this file:
`q286-closed-lanes-map.graph.json`.

The component-pair theorem obligation is stated explicitly in
`q286-component-pair-theorem-obligation.md`.

## Active theorem target

The current non-circular target is:

```text
After finite boundary exceptions, prove that targets satisfying
L_12/P < -.2 and F_3/P < -.3 cannot have simultaneous strongly negative
centered action in both lower-support channels (5,7) and (7,11).
```

If this cannot be proved from accessible structure, record the needed result
as a fixed-modulus pointwise binary Goldbach-in-progressions correlation
theorem, not as a finite diagnostic success.

Current executable receipts:

- `q286_lower_support_package_component_local_discrepancy_receipt`
- `q286_lower_support_component_pair_tail_window_receipt`
- `_q286_lower_support_component_rows_for_targets`
- `q286_lower_support_component_pair_coefficient_geometry_receipt`
- `q286_lower_support_component_pair_cone_projection_receipt`
- `q286_lower_support_component_pair_support_geometry_obstruction_receipt`
- `q286_lower_support_component_pair_character_mixture_receipt`

## Closed or falsified lanes

These routes should not be reopened without a genuinely new mechanism,
prediction, and falsifier.

| Lane | Disposition | Reason |
| --- | --- | --- |
| Whole-tail threshold ladders | Demoted/closed as proof engine | More thresholds only restate finite tail behavior unless tied to a new theorem. |
| Independent first-three lower envelope | Falsified | First-three values go far below candidate floors, including `10664`. |
| Support + nonnegativity + total mass implication | Falsified in the weak projection | Actual witness weights `10664` and `14138` satisfy the projected constraints but fail lower-support rescue. |
| Generic max-residue discrepancy | Falsified as sufficient route | Actual residue deviations exceed the tiny sufficient epsilon while some targets remain positive. |
| Raw package L2/Cauchy discrepancy | Falsified at measured scale | Late targets need roughly `0.0072..0.0075` relative discrepancy; actual is about `0.0157..0.0164`. |
| Raw 99-character norm bound | Falsified as already sufficient | Selected stress targets are not certified by triangle or plain vector-L2 bounds. |
| Rank-three internal cancellation | Falsified as explanation | The leading q286 mode contributions are mostly same-sign negative on stress targets. |
| Sign-quadrant exclusion | Falsified as theorem route | Both-negative mode-1/mode-2 quadrant is a strong tail selector but too common to exclude wholesale. |
| q70-only rescue | Demoted | Late targets remain rescued after removing q70; boundary cases show q70 alone is not the mechanism. |
| Component-pair support geometry | Falsified as sufficient route | Artificial same-mass nonnegative admissible weights make both `(5,7)` and `(7,11)` actions negative for every even residue modulo `10010`. |

Important nuance: the support/mass witnesses do not refute every possible
geometric proof.  They refute only the weak projection that forgets additional
constraints such as residue moments, symmetry, adjacency, signed coefficient
cones, or actual residue-weight arithmetic.

## Surviving structure

- The `.2` first-two / `.3` first-three subcone remains the active conditioned
  set.
- The exact rescue identity remains:

```text
G/P = F_3/P + 1 + Q_tail/P + H/P
rescue iff H/P > -1 - Q_tail/P - F_3/P.
```

- For late selected subcone targets `1222142`, `1323632`, and `1379072`, the
  local admissible mean of the lower-support package already clears the
  required floor by about `0.899..0.930` principal.
- Boundary failures are not diffuse.  They are dominated by simultaneous
  negative centered actions in `(5,7)` and `(7,11)`.
- Late selected targets avoid that simultaneous strong negative pair:
  `1222142` is led by positive `(7,11)`, `1323632` by positive `(5,7)`, and
  `1379072` by positive `(7,11)` despite mildly negative `(5,7)`.
- A selected-target receipt over all three late sparse-tail targets completed
  in `64.878s`; it found `both_negative ()`, with pair sums
  `0.013743`, `0.087495`, and `0.046724` respectively.
- The `(5,7)` and `(7,11)` centered coefficient vectors are nearly orthogonal
  across all `5005` even target residues modulo `10010`: the executable
  coefficient-geometry receipt gives cosine range
  `-0.0381940494499906 .. 0.0419660251672338`.  This rules out a pure
  coefficient-geometry explanation for the late no-both-negative pattern.
- The actual discrepancy-vector projection onto the two dangerous component
  directions is small in the checked selected targets: the bad boundary target
  `14138` has only `0.083979` of discrepancy L2 in the span, and the late
  targets have `0.011300..0.070320`.
- Pure component-pair support geometry is closed: the obstruction receipt
  constructs nonnegative admissible same-mass artificial weights with both
  `(5,7)` and `(7,11)` actions negative for all `5005` even residues modulo
  `10010`.
- The active component-pair cone is an exact `31`-character twisted
  binary-prime problem modulo `10010`: `(5,7)` uses `8` character rows,
  `(7,11)` uses `23`, and their union has `31`.

## Current boundary examples

`10664` and `14138` are finite boundary failures for the lower-support rescue
inequality.  They are useful witnesses against weak proof strategies, not
Goldbach counterexamples.

`1222142`, `1323632`, and `1379072` are late sparse-tail successes used as the
current comparison set.

## Next useful work

1. Keep the selected-target path in
   `q286_lower_support_component_pair_tail_window_receipt`; it avoids the
   slow extra window selector when testing explicit candidates.  The
   component-pair measurement now uses direct lower-support component rows
   rather than the full component-local/package receipt.
2. The fixed lower-support component decomposition is cached by
   `_q286_lower_support_component_data`.  The focused component-local
   regression now calls the receipt twice and verifies a cache hit; the latest
   rerun passed in `167.910s`.  This caches the fixed character/component
   setup, not the target-specific prime-pair or package work.
3. The component-pair receipt now uses
   `q286_first_two_mode_lower_tail_receipt` directly for window selection
   rather than the heavier subcone-complement wrapper.  The focused regression
   passed in `96.155s` and asserts this dependency boundary.
4. A compact unselected window probe at `1222142` passed in `102.025s`,
   returned the same tail target, found no simultaneous negative pair action,
   and attached lower-tail provenance without subcone-complement provenance.
5. The reduced-envelope receipt now stores the q286 singular-mode rows it
   already computes; lower-tail consumes those rows directly instead of running
   a second singular-mode target sweep.  The focused component-pair regression
   passed in `67.676s`, and the compact unselected window probe at `1222142`
   passed in `66.231s` with unchanged measured values.
6. The component-pair receipt now opts into sparse strict-central
   residue-weight rows from lower-tail, so lower-support component rows do not
   run a second prime-pair sweep.  The focused component-pair regression passed
   in `63.162s`; the unselected `1222142` probe passed in `68.886s` with
   `1337` sparse residue-weight rows.
7. A selected three-target component-pair probe over
   `1222142,1323632,1379072` passed in `64.878s`; all three were in the
   `.2` first-two / `.3` first-three subcone, all reused sparse lower-tail
   weights, and no target had simultaneous negative `(5,7)` and `(7,11)`
   centered action.
8. A modest broader finite window test of the component-pair theorem target is
   now more reasonable, but it remains a finite diagnostic and should be
   bounded.
9. In parallel, attempt a proof or reduction for simultaneous `(5,7)` and
   `(7,11)` negativity on the active subcone.
10. The direct coefficient geometry probe shows that the two active component
   vectors are almost orthogonal, not oppositely constrained.  This is now
   executable as `q286_lower_support_component_pair_coefficient_geometry_receipt`;
   its focused regression passed in `32.897s`.  The remaining proof must use
   actual binary prime-pair discrepancy arithmetic or record that obligation
   as fixed-modulus pointwise Goldbach-in-progressions input.
11. The cone-projection receipt shows the dangerous two-dimensional component
   span captures only a small fraction of measured discrepancy L2.  The next
   non-circular theorem target is therefore signed cone avoidance for that
   small projection, not a global discrepancy-size bound.
12. The support-geometry obstruction receipt passed in `36.947s` and closes
   the pure support/nonnegativity/total-mass/coefficient-geometry proof lane
   for the component-pair exclusion.  A surviving proof must use actual
   prime-pair arithmetic.
13. The character-mixture receipt passed in `62.503s` and reduces the
   surviving arithmetic obligation from full residue occupancy to signed
   control of `31` fixed twisted binary-prime character sums modulo `10010`.

## Still open

- Eventual q286 first-three alignment theorem.
- Eventual complement or lower-support lower-bound theorem.
- Pointwise signed binary-prime residue correlation estimate.
- Boundary finite check and outer assembly.
- Goldbach.

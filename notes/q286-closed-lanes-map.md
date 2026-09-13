# q286 closed-lanes map

Status: finite research map, not a proof of Goldbach.
Last updated after the 2026-09-13 q286 real-channel conductor profile.

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
- `q286_lower_support_component_pair_channel_pressure_profile_receipt`
- `q286_lower_support_component_pair_channel_conductor_profile_receipt`
- `q286_lower_support_component_pair_fixed_conductor_reduction_receipt`
- `q286_lower_support_component_pair_fixed_conductor_residue_pressure_receipt`
- `q286_lower_support_component_pair_fixed_conductor_character_cancellation_receipt`
- `q286_lower_support_component_pair_fixed_conductor_reflection_orbit_receipt`
- `q286_lower_support_component_pair_fixed_conductor_residual_orbit_cancellation_receipt`
- `q286_lower_support_component_pair_fixed_conductor_orbit_polygon_receipt`
- `q286_lower_support_component_pair_fixed_conductor_orbit_phase_profile_receipt`
- `q286_lower_support_component_pair_fixed_conductor_phase_bin_compression_receipt`
- `q286_lower_support_component_pair_fixed_conductor_phase_antipodal_compression_receipt`
- `q286_lower_support_component_pair_fixed_conductor_phase_antipodal_pair_balance_receipt`
- `q286_lower_support_component_pair_fixed_conductor_phase_antipodal_threshold_envelope_receipt`
- `q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_exception_receipt`
- `q286_lower_support_component_pair_fixed_conductor_phase_antipodal_exception_budget_receipt`
- `q286_lower_support_component_pair_fixed_conductor_phase_antipodal_nonthin_ratio_receipt`
- `q286_lower_support_component_pair_fixed_conductor_phase_antipodal_sector_geometry_receipt`
- `q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_budget_receipt`
- `q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_support_receipt`
- `q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_edge_support_receipt`
- `q286_lower_support_component_pair_fixed_inequality_stress_receipt`

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
| Component-pair support geometry | Falsified as sufficient route | Artificial same-mass nonnegative admissible weights make both `(5,7)` and `(7,11)` actions negative for every even residue modulo `10010`; this remains true with reflection symmetry `w(r)=w(N-r)`. |

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
- This closure survives actual ordered-pair reflection symmetry.  The reflected
  obstruction receipt passed in `34.893s`, has maximum reflection weight error
  `0`, and still obstructs all `5005` even residues.
- The active component-pair cone is an exact `31`-character twisted
  binary-prime problem modulo `10010`: `(5,7)` uses `8` character rows,
  `(7,11)` uses `23`, and their union has `31`.
- Those `31` characters lie in two adjacent factor-label blocks:
  `(a,b,0,0)` for `(5,7)` and `(0,b,c,0)` for `(7,11)`.
- Complex conjugation collapses the active target to `16` real conjugacy
  channels: `4` for `(5,7)`, `12` for `(7,11)`, with one self-conjugate
  active label `(0,3,5,0)`.  The receipt now records coefficient-bearing
  formulas: `2*Re(c*S_chi)` for conjugate pairs and `Re(c*S_chi)` for the
  self-conjugate channel.
- The action-decomposition receipt evaluates those formulas on selected
  actual prime-pair weights.  For `14138`, the real-channel pair sum is
  `-1.152543267627036`; the three late comparison targets have positive sums
  `0.01374295170801024`, `0.08749508122821215`, and
  `0.046724251505156425`; maximum reconstruction error is about `1.13e-15`.
- The rescue-margin receipt rewrites the selected lower-support rescue
  condition as a centered real-channel pair-sum floor.  The boundary target
  `14138` misses its floor by `-0.8769412734408442`; the three late comparison
  targets clear their floors by about `0.945716`, `1.024219`, and `0.944999`.
  Over the late comparison set, the strongest selected uniform sufficient
  floor is `-0.8982746156725305`, still leaving observed margin
  `0.9120175673805407`.
- The real-channel bound-budget receipt translates that late floor into an
  analytic target: an eventual normalized `Linf` bound below
  `0.05885324711081062`, or normalized `L2` bound below
  `0.2155408076755675`, would be sufficient for the selected late floor.
  The boundary target `14138` has actual maximum normalized channel sum
  `0.2659059415120284`, while the late comparison targets are about
  `0.0250..0.0272`.
- The conditional norm-closure receipt splits the remaining theorem into two
  pieces: eventual floor stability at
  `required_centered_pair_sum_to_rescue <= -0.8982746156725305`, and eventual
  active real-channel `Linf` control at `0.05885324711081062`.  The late
  comparison targets satisfy both selected conditions; `14138` satisfies
  neither.
- The floor-stability decomposition receipt splits the floor half again:
  selected stability follows from lower-support required floor
  `<= -0.6751407665271594` and fixed offset
  `non_pair_lower_support_actual + component_pair_local_mean >=
  0.2231338491453711`.  The late comparison targets satisfy both term
  conditions; `14138` satisfies neither.
- The floor-identity receipt removes the remaining bookkeeping slack:
  floor stability is exactly the combined-driver lower bound
  `first_three + q286_after_first_three + non_pair_lower_support_actual +
  component_pair_local_mean >= -0.1017253843274695` on the selected rows.
  `14138` is far below this at `-0.7243980058138082`.
- The combined-driver/channel-closure receipt packages the current clean
  sufficient theorem: combined driver `>= -0.1017253843274695` plus active
  real-channel normalized `Linf <= 0.05885324711081062` forces selected
  centered-pair rescue.  The late comparison targets satisfy both; `14138`
  satisfies neither.
- The action-identity receipt verifies the direct recombination
  `full_action/P = 1 + combined_driver + centered_pair_sum` with reconstruction
  error below `1e-12`.  Thus the q286 component-pair target is now a positivity
  split: driver floor plus centered-pair floor.
- The closure-margin profile shows the selected late positives have different
  pressure points: `1379072` is binding on the driver floor, while `1323632`
  is closest to the active-channel Linf bound.  `14138` fails both assumptions
  by large margins.

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
13. The character-mixture receipt passed in `68.299s` and reduces the
   surviving arithmetic obligation from full residue occupancy to signed
   control of `31` fixed twisted binary-prime character sums modulo `10010`.
14. The focused regression now freezes the exact active labels, so future
   theorem attempts can target the two explicit adjacent character-label
   blocks instead of rediscovering the support.
15. The real-channel regression passed in `30.401s` and reduces the signed
   character target from `31` complex rows to `16` coefficient-bearing real
   conjugacy channels.
16. The reflection-symmetric support obstruction passed in `34.893s`; support,
   nonnegativity, total mass, and pair-swap symmetry still do not exclude
   simultaneous negative `(5,7)` and `(7,11)` component actions.
17. The real-channel action regression passed in `73.676s` and decomposes
   selected actual component-pair sums into the `16` real channel
   contributions with reconstruction error about `1.13e-15`.
18. The real-channel rescue-margin regression passed in `119.854s` and turns
   the selected rescue condition into an exact centered pair-sum floor.
19. The real-channel bound-budget regression passed in `121.411s` and turns
   the late selected floor into explicit normalized channel-norm thresholds:
   `0.05885324711081062` in `Linf` and `0.2155408076755675` in `L2`.
20. The conditional norm-closure regression passed in `116.123s` and splits
   the surviving proof target into floor stability plus active-channel
   pointwise norm control.
21. The floor-stability decomposition regression passed in `121.972s` and
   splits the floor half into a required lower-support package ceiling plus a
   non-pair/pair-local offset floor.
22. The floor-identity regression passed in `118.879s` and rewrites selected
   floor stability as one combined-driver lower bound.
23. The combined-driver/channel-closure regression passed in `121.404s` and
   packages the q286 component-pair lane as two explicit unproved assumptions.
24. The action-identity regression passed in `114.284s` and reconstructs full
   action from principal, combined driver, and centered pair sum.
25. The closure-margin profile regression passed in `118.798s` and identifies
   the selected driver-bound and channel-bound pressure points.
26. The channel-pressure profile regression passed in `124.495s` and shows
   that boundary target `14138` is dominated by real-channel label
   `(1,1,0,0)`, while the largest late-positive single-channel pressure is
   target `1379072` at label `(0,3,3,0)`.
27. The channel-conductor profile regression passed in `118.119s` and shows
   that all `16` active real channels have conductor `35` or `77`; no active
   channel uses factor `13`.  The missing pointwise theorem can therefore be
   stated over adjacent fixed conductors, not the whole period `10010`.
28. The fixed-conductor reduction regression passed in `162.840s` and
   reconstructs every selected active period-`10010` channel sum from
   discrepancy aggregated modulo its own conductor (`35` or `77`), with
   character reduction error below `1e-8`.
29. The fixed-conductor residue-pressure regression passed in `208.170s`.
   It falsifies a plain residue-Linf proof at the measured scale: even
   late-positive `1379072` at conductor `77` has triangle bound
   `0.2187090564566816`, above the needed channel bound
   `0.05885324711081062`, while its actual active channel sum is only
   `0.027155981994015317`.
30. The fixed-conductor character-cancellation regression passed in
   `180.890s` and quantifies the surviving mechanism: late-positive
   `1379072`'s worst channel is only `0.12416487197179206` of the crude
   residue-Linf triangle envelope, enough to clear the channel bound.
31. The fixed-conductor reflection-orbit regression passed in `217.106s`.
   Reflection pairing clears late positives `1222142` and `1323632`, but
   misses `1379072` by `0.0015406171514715863`, leaving a residual
   cross-orbit cancellation target.
32. The residual-orbit cancellation regression records that the positive
   reflection-envelope failures are exactly two `1379072` conductor-`77`
   labels, `(0,1,5,0)` and `(0,2,6,0)`, and both are rescued by signed
   cross-orbit cancellation.
33. The orbit-polygon regression passed in `351.969s` and turns those two
   residual failures into exact `38`-edge complex polygons.  Their perimeters
   slightly exceed the channel bound, but their resultants are only
   `0.0053525925011552716` and `0.01746105205795644`.
34. The orbit-phase profile regression passed in `283.200s`.  The two
   residual polygons occupy `11` and `10` of `12` phase bins; the harder
   `(0,2,6,0)` row has largest-bin fraction `0.26794815278810286`, suggesting
   phase-bin balance as the next geometric theorem target.
35. The phase-bin compression regression passed in `209.826s`.  Signed
   phase-bin compression clears residual label `(0,1,5,0)` with margin
   `0.000087887837272945`, but still misses `(0,2,6,0)` by
   `0.001296756190866699`.  Thus phase-bin compression alone is not the final
   channel theorem; the remaining hard row needs inter-bin signed cancellation
   or a sharper phase-balance estimate.
36. The phase-antipodal compression regression passed in `218.344s`.  Pairing
   opposite phase bins clears both residual conductor-`77` rows: label
   `(0,1,5,0)` has antipodal-pair L1 `0.009229827584054894`, and the hard
   label `(0,2,6,0)` has antipodal-pair L1 `0.03657040255445905`, below the
   channel bound `0.05885324711081062`.  The geometric theorem target is now
   antipodal phase-sector cancellation, not undirected phase-bin mass balance.
37. The phase-antipodal pair-balance regression passed in `252.478s`.  It
   falsifies a uniform per-pair cancellation strengthening: the hard
   `(0,2,6,0)` row has weighted antipodal cancellation ratio
   `0.6079867090121881`, largest pair cancellation ratio
   `0.9711661073614952`, and `2` high-ratio pairs at threshold `0.75`.
   The surviving theorem target is a weighted six-pair antipodal L1 bound.
38. The phase-antipodal threshold-envelope regression passed in `395.264s`.
   With threshold `0.75`, explicit high-ratio exceptions plus
   `0.75` times remaining pair mass clears both residual rows.  The hard
   `(0,2,6,0)` row has thresholded envelope `0.049789406359944485`, below the
   channel bound by `0.009063840750866137`.  This is now the sharpest
   proof-shaped split of the residual conductor-`77` visual route.
39. The phase-antipodal thin-exception regression passed in `210.678s`.
   All selected high-ratio antipodal exceptions have small/large side ratio at
   most `0.05`; the hard `(0,2,6,0)` row has maximum ratio
   `0.046829417626061014` and high-ratio exception abs sum
   `0.024020095646099474`.  The high-ratio exception target is now thin
   opposite-sector mass control.
40. The phase-antipodal exception-budget regression passed in `391.565s`.
   After paying `0.75` times non-thin pair mass, the hard `(0,2,6,0)` row may
   spend `0.033083936396965614` on high-ratio thin exceptions, spends
   `0.024020095646099474`, and has margin `0.00906384075086614`.  The current
   proof target is an explicit two-part inequality: non-thin pair cancellation
   plus thin-exception absolute-mass control.
41. The phase-antipodal non-thin-ratio regression passed in `210.885s`.
   Non-thin antipodal pairs clear the `0.75` ratio bound in the selected
   fixture.  The hard `(0,2,6,0)` row has worst non-thin ratio
   `0.6626326478324716`, leaving margin `0.08736735216752844`.  Both halves
   of the two-part antipodal inequality are now separately measured.
42. The phase-antipodal sector-geometry regression passed in `240.891s`.
   The selected non-thin `0.75` bound follows from coarse opposite-sector
   geometry: with `12` bins, opposite sectors are separated by at least
   `5*pi/6`; the hard `(0,2,6,0)` row has worst sector-envelope ratio
   `0.6862033816719031`, still below `0.75` by `0.06379661832809691`.
43. The phase-antipodal thin-large-side-budget regression passed in
   `614.609s`.  Selected high-ratio thin exceptions clear the allowed
   exception budget after replacing their mass by `(1.05) * large-side mass`.
   The hard `(0,2,6,0)` row has large-side mass `0.02490542589058863`,
   envelope `0.026150697185118062`, and margin `0.006933239211847552`.
   The surviving proof target is now uniform large-side mass control for thin
   opposite-sector exceptions, plus the already-stated residual polygon setup.
44. The phase-antipodal thin-large-side-support regression passed in
   `403.837s`.  The selected thin large-side mass sits only in bins `4,5,7`,
   but orientations are mixed: `(0,1,5,0)` uses opposite bin `7`, while hard
   row `(0,2,6,0)` uses primary bins `4,5`.  This closes a one-orientation
   large-side proof shortcut and leaves explicit thin exception bin-pair mass
   control as the sharper support target.
45. The phase-antipodal thin-large-side-edge-support regression passed in
   `415.057s`.  The selected thin large-side bins are not single-edge:
   exception edge counts are `3`, `5`, and `2`, and the hard `(4,10)` bin has
   five reflection-orbit edges with largest-edge ratio `0.4406627296301651`.
   This closes a one-edge large-side shortcut and leaves small explicit
   reflection-orbit mass/cancellation control as the sharper support target.
46. The fixed-inequality stress regression passed in `282.271s` and now
   checks both a passing active pair and a premise-empty pair.  The full
   `21`-pair component census is recorded in
   `evidence/q286-fixed-inequality-21pair-census.json`: exactly one pair,
   `((5,7),(7,11))`, is applicable; it passes with two residual polygon rows,
   zero failures, and worst margin `0.006933239211847554`.  The other `20`
   component pairs are `not_applicable_no_residual_polygons`.  This finds no
   counterexample to the fixed inequality where the premise fires, but it also
   shows the inequality is narrow rather than broadly reinforced.
47. The fixed-inequality target-census regression passed in `278.805s` and
   adds a target-denominator receipt for the active pair.  The compact
   selector-driven evidence in
   `evidence/q286-fixed-inequality-target-window-census.json` scanned the
   fixed window `1379072,1379074,1379076,1379078,1379080`, selected all
   targets with `first_two < -0.2` and `first_three < -0.3`, found exactly
   one tail target (`1379072`), and stressed it with zero failures and zero
   errors.  This is a useful anti-cherry-pick audit of the target denominator,
   but only for a tiny local window; it does not provide broad sample support.
48. The tail-selector grid regression passed in `35.441s` and separates broad
   denominator scanning from the expensive fixed-inequality stress stack.
   `evidence/q286-tail-selector-grid-6x25.json` scanned `150` predeclared
   targets across starts `1000000,1010010,1020020,1030030,1040040,1050050`
   and found zero active tail targets.  This is not support for the fixed
   inequality; it shows only that these neutral windows had no stressable
   active-lane rows.
49. The active-residue selector holdout
   `evidence/q286-tail-selector-active-residue-holdout-6x5.json` scanned the
   next six same-residue q286-period shifts after the known `1379072` hit,
   five targets per window.  It found zero active tail targets across `30`
   scanned targets.  This falsifies simple immediate same-residue repetition
   of the known local active row, but no fixed-inequality rows were stressed.

## Still open

- Eventual q286 first-three alignment theorem.
- Eventual complement or lower-support lower-bound theorem.
- Pointwise signed binary-prime residue correlation estimate.
- Boundary finite check and outer assembly.
- Goldbach.

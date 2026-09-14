# q286 closed-lanes map

Status: finite research map, not a proof of Goldbach.
Last updated after the q286 dominant signed-channel branch sample.

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
- `q286_first_three_reflection_orbit_signed_cancellation_receipt`
- `q286_first_three_reflection_orbit_ratio_certificate_receipt`
- `q286_first_three_reflection_orbit_ratio_cycle_horizon_receipt`
- `q286_first_three_reflection_orbit_dual_rectangle_receipt`
- `tools/build_q286_first_three_reflection_orbit_refined_staircase.py`
- `tools/build_q286_first_three_boundary_pair_autopsy.py`
- `q286_first_three_positive_orbit_landing_profile_receipt`
- `q286_first_three_positive_mass_threshold_falsifier_receipt`
- `q286_first_three_singular_mode_residue_obligation_receipt`
- `q286_first_three_dominant_mode_reflection_support_obstruction_receipt`
- `q286_first_three_dominant_mode_character_sum_obligation_receipt`
- `q286_first_three_dominant_mode_channel_norm_budget_receipt`
- `q286_first_three_dominant_mode_signed_channel_profile_receipt`
- `q286_first_three_dominant_mode_signed_channel_branch_sample_receipt`
- `q286_first_three_dominant_mode_channel_swing_pair_receipt`
- `q286_first_three_dominant_mode_helpful_portfolio_receipt`

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
| Dominant mode support/reflection geometry | Falsified as sufficient route | Every even target residue modulo `286` admits a positive reflected synthetic support weight with `mode_1+mode_2 < -.3`. |
| Dominant mode independent channel norms | Demoted as too blunt | Plain `Linf`/`L2` smallness of the `25` real channels certifies none of the near-boundary samples; clear rows still pass by signed structure. |
| Dominant tail as monotone reserve | Demoted | The residual staircase shows an intermediate tail channel can knock clear target `13556` below the floor before later repair; tail control is signed cumulative bookkeeping, not a simple positive add-on. |
| Dominant staircase from weak reflected geometry | Falsified as sufficient route | Synthetic nonnegative reflected weights with the same local admissible support and total mass can break every selected full-stage pass and over-rescue every selected full-stage deficit. |
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
25. The closure-margin profile regression passed in `139.808s` and now
   records the strict conditional closure scalar
   `driver_margin + L * channel_margin`.  Boundary `14138` is negative
   (`-3.782909118497761`), while selected late positives have positive
   margins, with `1379072` still positive at `0.48379401372791037`.
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
48a. The larger selector-only holdout
   `evidence/q286-tail-selector-grid-12x25.json` scanned `300` predeclared
   targets across starts `1000000 + 10010*k` for `k=0..11` and found zero
   active tail targets.  Its minimum first-two/first-three row was target
   `1010026`, with first-two `-0.20990264929935676` and first-three
   `-0.21213063260679105`.  This broadens the denominator evidence but still
   creates no fixed-inequality or strict-closure stress row.
48b. The fast necessary-condition scout
   `evidence/q286-first-three-tail-scout-4x12x25.json` scanned `1200` new
   targets across starts `1120120`, `1240240`, `1500500`, and `2001000`,
   with `12` cycles and `25` targets per cycle at each start.  It found zero
   first-three hits below `-0.3`, so these windows contain no active-selector
   rows.  This is only a necessary-condition exclusion; no fixed-inequality or
   strict-closure row was stressed.
48c. The later fast necessary-condition scout
   `evidence/q286-first-three-tail-scout-8x12x25-late.json` scanned `2400`
   targets at global-cycle starts `250,350,500,800,1200,1600,2200,3000` and
   again found zero first-three hits below `-0.3`.  The worst block minimum
   was `-0.1282544626188415` at target `2562584`.  These windows also contain
   no active-selector rows, but this remains finite denominator evidence.
49. The active-residue selector holdout
   `evidence/q286-tail-selector-active-residue-holdout-6x5.json` scanned the
   next six same-residue q286-period shifts after the known `1379072` hit,
   five targets per window.  It found zero active tail targets across `30`
   scanned targets.  This falsifies simple immediate same-residue repetition
   of the known local active row, but no fixed-inequality rows were stressed.
50. The active-lane strict closure-margin census regression passed in
   `321.226s`.  It freezes the closure constants from
   `14138,1222142,1323632,1379072` and applies
   `driver_margin + L * channel_margin` to selected active-window targets.
   The compact evidence file
   `evidence/q286-active-lane-strict-closure-margin-census-selected-late.json`
   scanned selected late windows around `1222142`, `1323632`, and `1379072`,
   selected exactly those three active starts, and measured positive strict
   margins `0.5506633762515991`, `0.546820393849208`, and
   `0.48379401372791037`.  In all three rows, the channel-margin contribution
   dominates the driver-margin contribution, so this selected strict slack is
   channel-carried.
51. `evidence/q286-active-lane-sampling-denominator-map.json` now records the
   sampling posture explicitly.  The strict closure margin has only been
   stressed on the three selected late active rows.  The broader neutral
   selector holdout scanned `300` targets and found zero active tail rows; the
   necessary-condition scouts scanned `3600` targets and found zero
   first-three hits below `-0.3`; the same-residue holdout scanned `30`
   targets and found zero active tail rows.
   These are denominator facts, not strict-closure successes.  The
   sample-size/cherry-pick concern remains open.
52. `notes/q286-active-selector-rarity-theorem-obligation.md` separates the
   theorem target from the finite scouts.  The target is a pointwise lower
   bound on the fixed q286 first-three singular-mode residue-discrepancy
   functional modulo `286`: prove `first_three >= -0.3` outside a finite
   checked set, or stress any unchanged-selector failures with the full active
   selector and strict-closure receipts.
53. The same rarity note now quantifies the conservative norm certificate
   supplied by `q286_first_three_weighted_discrepancy_norm_receipt` at the
   active `.3` threshold.  The sufficient relative-delta ranges are
   `0.0012438599030454018..0.002451362294448365` in `L_infinity` and
   `0.005955161523943415..0.017908306132142508` in `L2`; residue `0 mod 286`
   is the worst class for both criteria.  This sharpens the theorem target
   but does not prove the needed pointwise prime-pair discrepancy estimate.
54. `evidence/q286-tail-alignment-complement-window-233-264.json` records the
   next adjacent post-232 denominator block.  Global cycles `233..264`
   scanned `160160` targets with the unchanged `.4` alignment ceiling; the
   `.2` near-tail alignment window and the `.3` alignment/complement window
   both found zero first-three tail rows.  This supports finite tail thinning
   in that block only and supplies no stress-row theorem evidence.
55. `notes/q286-conditional-proof-stack.md` consolidates the surviving q286
   route into three conditional theorem shapes: rarity plus complement floor,
   `.4` alignment plus complement on the first-three tail, and active-lane
   strict closure via the calibrated scalar margin.  It makes explicit that
   all three still require finite boundary verification, endpoint/noncentral
   control, outer assembly, and a pointwise signed prime-correlation theorem.
56. `evidence/q286-evidence-glow-map.json`, generated by
   `tools/build_q286_evidence_glow_map.py`, is the first stacked evidence
   visualization layer.  It overlays graph roles and structured q286 evidence
   receipts into target, mechanism, and theorem-gap stacks.  Brightness means
   repeated evidence layers overlap, not that the target or theorem is proved.
57. `evidence/q286-target-vector-overlay.json`, generated by
   `tools/build_q286_target_vector_overlay.py`, adds selected target
   coordinates for shape/vector visualization: first-three, complement, full
   action, `.4` certificate margin, `(5,7)/(7,11)` centered component actions,
   and strict-closure driver/channel coordinates where available.  The
   visualization note now explicitly separates evidence glow from attention
   glow.
58. `evidence/q286-target-vector-pca.json`, generated by
   `tools/build_q286_target_vector_pca.py`, runs selected-target PCA/SVD on
   the vector overlay.  In both the alignment/complement coordinates and the
   lower-support component coordinates, PC1 explains about `0.89` of selected
   variance and separates boundary failures from late/rescued targets.  This
   is a visualization axis only, not a population theorem.
59. `evidence/q286-visual-summary.svg`, generated by
   `tools/build_q286_visual_summary_svg.py`, is the first static visual
   superposition of q286 evidence layers: selected PCA positions, role shapes,
   glow-scaled target sizes, component-vector arrows, and mechanism/theorem
   glow bars.  It also preserves the intended order from finite selector to
   vector coordinates to PCA/shape view to theorem obligation.  This is
   deterministic navigation output, not proof evidence.
60. `evidence/q286-filter-order-audit.json`, generated by
   `tools/build_q286_filter_order_audit.py` from
   `q286_first_three_filter_order_audit_receipt`, freezes the first
   q286 predicate-order audit.  On the eight-period fixture, `first_three_tail`
   has `4406` targets and the full active selector has `4405`; after the
   first-three tail, `first_two_active` removes exactly one target.  The fine
   residual filter is `full_nonpositive`, with `89` targets globally and `86`
   inside the first-three tail.  This is an `aha-candidate` for theorem
   navigation, not a theorem.
61. `evidence/q286-filter-order-holdout-8-15.json`, generated by
   `tools/build_q286_filter_order_holdout.py`, applies the unchanged
   filter-order audit to the next contiguous eight q286 periods starting at
   `90080`.  It tested `40040` targets; `first_three_tail` and
   `active_selector` both had exactly `891` targets, with zero
   `first_three_tail_not_first_two_active`, zero `full_nonpositive`, zero
   `nonrescued_first_three_tail`, and zero `first_three_tail_below_complement_floor`.
   This strengthens the finite filter-order navigation claim, but because the
   holdout has no stress rows it does not prove active-selector rarity,
   strict closure, complement floor, signed prime-correlation control, or
   Goldbach.
62. `q286_first_three_reflection_support_obstruction_receipt`, with compact
   evidence in
   `evidence/q286-first-three-reflection-support-obstruction.json`, refutes a
   support/nonnegativity/total/reflection-only proof of the first-three rarity
   bound.  For all `143` even target residues modulo `286`, there is a
   strictly positive reflected synthetic residue-weight vector with
   first-three ratio below `-0.3`.  The least-negative extremal residue is
   still about `-2.5675553132435125`, so the missing rarity theorem must use
   actual binary prime-pair distribution or a stronger arithmetic constraint.
63. `q286_first_three_reflection_orbit_cap_receipt`, with compact evidence in
   `evidence/q286-first-three-reflection-orbit-cap.json`, quantifies the
   next stronger geometric sufficient condition.  To force
   `first_three >= -0.3` from a uniform reflection-orbit mass cap alone, the
   cap would need to be only `0.016823304298596065..0.026762977396728494`
   across even q286 target residues.  Actual first-period strict-central
   prime-pair weights violate that sufficient cap on all `5005` tested
   targets, with maximum orbit mass `0.12026969709166307` and worst
   actual/cap ratio about `5.923169478623975`.  The remaining route is signed
   orbit cancellation or arithmetic distribution, not a pure orbit-cap proof.
64. `q286_first_three_reflection_orbit_dual_rectangle_receipt`, with compact
   evidence in
   `evidence/q286-first-three-reflection-orbit-staircase-certificate.json`,
   tests the three-branch rational staircase
   `(B<=1,R>=7/10)`, `(B<=21/20,R>=5/7)`, `(B<=5/4,R>=19/25)`.  Each branch
   directly implies `first_three >= -0.3`.  On early cycles `0..15` from
   start `10000`, all `5297` first-three tails remain outside the staircase,
   with `1682` additional clear outside rows.  On late cycles `0..7` from
   start `1120120`, all `40040` targets are certified, including the prior
   old/new rectangle intersection row `1157462` via the middle branch.  The
   unchanged holdout from start `1200200`, cycles `0..7`, tests another
   `40040` targets and leaves exactly two rows outside: tail `1222142` and
   clear `1242118`.  This is an `aha-candidate` for a refined eventual
   staircase-occupancy or exact-curve theorem, not a theorem.
65. `evidence/q286-first-three-reflection-orbit-refined-staircase.json` adds
   the post-hoc exact step `(B<=101/100,R>=71/101)` between the first two
   staircase branches.  The step is safe because
   `(1-71/101)*(101/100)=3/10`.  On the same holdout from start `1200200`,
   it certifies clear row `1242118` and leaves only tail `1222142` outside.
   On early cycles it reduces uncertified clear rows by `13` but leaves all
   `5297` tails outside.  This preserves the exact-curve/staircase theorem
   target while exposing that a proof must explain why rows eventually clear
   these near-curve steps, not merely fit one observed clear exception.
66. `evidence/q286-first-three-boundary-pair-autopsy.json` subtracts the
   holdout tail `1222142` from the two clear near-threshold rows `1242118`
   and `1240888`.  The first clear row improves by about `0.021161`, split
   between reduced negative pressure and increased positive compensation.  The
   second clear row has worse negative pressure by about `0.004649`, but gains
   about `0.037553` positive compensation.  This rejects a single-factor
   pressure-only explanation and points to classifying positive orbit-mass
   landing near the exact curve.  The q286 first-three character layer has
   support `(11,13)` on modulus `286`; conductor `77` is not native to this
   receipt.
67. `q286_first_three_positive_orbit_landing_profile_receipt`, with evidence
   in `evidence/q286-first-three-positive-orbit-landing-profile.json`,
   refines the boundary autopsy by writing `first_three=-B+P` and splitting
   `B` and `P` into orbit-class mass fractions and landing means.  On the
   same holdout near-boundary rows, both clear rows improve positive
   compensation because more mass sits on positive orbit classes; their
   positive landing means actually decrease relative to tail `1222142`.
   Thus the live mechanism is positive-class mass allocation near the exact
   curve, not higher positive-orbit average coefficients.
68. `q286_first_three_positive_mass_threshold_falsifier_receipt`, with
   evidence in
   `evidence/q286-first-three-positive-mass-threshold-falsifier.json`,
   falsifies the standalone rule that near-boundary rows with
   `positive_orbit_mass_fraction >= .49` are clear.  The rule happens to
   split the three-row `1200200` holdout, but early cycles `0..15` contain
   `265` high-positive-mass tails and `896` low-positive-mass clear rows;
   cycles `8..15` from start `90080` contain `64` high-positive-mass tails
   and `294` low-positive-mass clear rows.  This leaves mass allocation as a
   coordinate in the exact-curve problem, not a one-dimensional certificate.
69. `q286_first_three_mass_matched_pair_decomposition_receipt`, with evidence
   in `evidence/q286-first-three-mass-matched-pair-decomposition.json`,
   reuses the four mass-threshold windows and decomposes mass-nearest
   clear-minus-tail pairs by exact midpoint products.  Early cycles `0..15`
   yield `1024` same-residue/sign-mask pairs, cycles `8..15` yield `283`
   pairs with `264` same-residue/sign-mask, the late `1120120` window has no
   near-boundary tails, and the `1200200` holdout has one fallback pair.
   Across all `1308` pairs, positive landing quality is positive in `865`
   pairs and dominant in `769`; positive mass transfer is nearly
   sign-balanced.  The holdout pair shows a different cancellation pattern in
   which helpful mass terms are mostly offset by worse landing quality.  This
   refines the surviving exact-curve route toward a coupled mass/landing
   arithmetic estimate, not a new threshold theorem.
70. `q286_first_three_mass_landing_obligation_receipt`, with evidence in
   `evidence/q286-first-three-mass-landing-obligation.json`, states the exact
   pointwise first-three rarity obligation in mass/landing variables:
   `m_plus(N)*ell_plus(N)+tau >= m_minus(N)*ell_minus(N)` for `tau=.3`.
   On holdout samples, tail `1222142` has slack about
   `-0.00758776037087916`, while clear rows `1242118` and `1240888` have
   positive slacks about `0.013573256731567618` and
   `0.025315898499383316`; reconstruction errors are below `2.3e-16`.  This
   is an exact theorem-obligation artifact only.  The missing proof input is
   a pointwise arithmetic estimate for actual binary-prime residue weights on
   q286 reflection-orbit sign classes.
71. `q286_first_three_orbit_uniformity_budget_receipt`, with evidence in
   `evidence/q286-first-three-orbit-uniformity-budget.json`, works backward to
   a valid conditional theorem: if `||mu_N-u_a||_1 <= tau/||c_a||_infinity`
   or `||mu_N-u_a||_2 <= tau/||c_a||_2`, then `first_three(N) >= -tau`.
   For `tau=.3`, sufficient L1 budgets range from about
   `0.0093982579157629` to `0.07455426391330403`; sufficient L2 budgets range
   from about `0.007916843497532824` to `0.03539182086849026`.  The route is
   too blunt at the active scale: clear rows `1242118` and `1240888` fail the
   sufficient budgets while still clearing the threshold.  This demotes
   generic orbit uniformity as the main proof engine and preserves the
   coefficient-sensitive mass/landing target.
72. `q286_first_three_signed_projection_obligation_receipt`, with evidence in
   `evidence/q286-first-three-signed-projection-obligation.json`, states the
   sharper backward theorem target.  With orbit-mass deviation
   `delta_N=mu_N-u_a` and q286 coefficient vector `c_a`, the exact identity is
   `first_three(N)=<delta_N,c_a>`.  Thus the target theorem is the
   anti-alignment bound `<delta_N,c_a> >= -tau`, or equivalently the cosine
   floor `cos(delta_N,c_a) >= -tau/(||delta_N||_2||c_a||_2)`.  On the holdout
   samples, tail `1222142` fails this condition with cosine margin about
   `-0.012059483057299869`, while clear rows `1242118` and `1240888` pass it
   despite failing generic uniformity budgets.  This is now the sharpest
   q286 first-three theorem target, but it remains an unproved pointwise
   signed prime-correlation estimate.
73. `notes/q286-proof-fixture-stack.md`, with structured evidence in
   `evidence/q286-proof-fixture-stack.json`, records the route as a proof
   fixture: exact identities are bolted anchors, unresolved theorem
   obligations are tacks, and condensation into a proof is forbidden until the
   tacks are proved.  The current tacks are signed-projection anti-alignment,
   conditioned complement/lower-support rescue, the required pointwise
   binary-prime residue-correlation input, and finite/endpoint/outer assembly.
   This is navigation discipline, not proof evidence.
74. `q286_first_three_residue_pair_correlation_obligation_receipt`, with
   note `notes/q286-residue-pair-correlation-obligation.md` and evidence in
   `evidence/q286-first-three-residue-pair-correlation-obligation.json`,
   identifies the exact fixed-modulus arithmetic theorem backing the
   signed-projection tack.  For `M=286`, admissible residues
   `A_a={u in U : a-u in U}`, centered coefficient `gamma_a(u)`,
   strict-central binary-prime weights `W_N(u)`, and
   `T_N=sum_u W_N(u)`, the missing theorem is
   `sum_{u in A_a}(W_N(u)-T_N/|A_a|)*gamma_a(u) >= -tau*T_N`.
   The receipt verifies the algebra against the prior signed-projection
   sample rows below `5.6e-17` and records the residual ledger: tail
   `1222142` is dominated by named residues such as `133` and `153`.
   This closes only the ambiguity of the required residue-correlation input;
   it does not prove that input.
75. `notes/q286-residue-pair-external-theorem-comparison.md`, with evidence
   in `evidence/q286-residue-pair-external-theorem-comparison.json`, compares
   the q286 residue-pair obligation against public arXiv AP-Goldbach source
   locators.  Checked average, almost-all, level-of-distribution, and
   upper-bound results do not supply the every-sufficiently-large-`N`
   one-sided q286 inequality.  A full uniform fixed-modulus AP asymptotic
   would imply the q286 tack, and a positive pointwise AP asymptotic is
   Goldbach-strength for the strict-central AP problem.  The remaining
   possible narrowing is a Dirichlet-character decomposition of the specific
   one-sided projection against `gamma_a`.
76. `tools/build_q286_residue_pair_character_mode_narrowing.py`, with note
   `notes/q286-residue-pair-character-mode-narrowing.md` and evidence in
   `evidence/q286-residue-pair-character-mode-narrowing.json`, reuses the
   existing first-three character-mixture and singular-coordinate receipts on
   the near-boundary samples `1222142`, `1242118`, and `1240888`.  The q286
   first-three channel remains broad in the `99` character-product space, but
   the active approximation is rank three.  In the three tested rows, the
   rank-three mode ledger is almost perfectly same-sign negative; the tail
   `1222142` has contributions about `-0.226941309`, `-0.081891871`, and
   `+0.001245419`, while both clear rows are same-sign negative in all three
   modes.  This finite evidence demotes internal character-mode cancellation
   as the rescue mechanism for these rows and points to controlling the first
   two dominant singular coordinates or using a separate rescue theorem.
77. `q286_first_three_singular_mode_residue_obligation_receipt`, with note
   `notes/q286-first-three-singular-mode-residue-obligation.md` and evidence
   in `evidence/q286-first-three-singular-mode-residue-obligation.json`,
   bolts the character-mode narrowing to actual residue weights.  For each
   singular mode `j`, it verifies
   `mode_j(N)=sum_u (W_N(u)-T_N/|A_a|)*gamma_{a,j}(u)/T_N`.  On samples
   `1222142`, `1242118`, and `1240888`, modes `1` and `2` are same-sign
   negative on all three rows, but their sum falls below `-.3` only on tail
   `1222142`.  This makes the next residual theorem a pointwise lower bound
   or structural exclusion for the dominant two-mode projection, not another
   threshold receipt.
78. `q286_first_three_dominant_mode_reflection_support_obstruction_receipt`,
   with note
   `notes/q286-first-three-dominant-mode-reflection-support-obstruction.md`
   and evidence in
   `evidence/q286-first-three-dominant-mode-reflection-support-obstruction.json`,
   closes the support/reflection-only version of that residual theorem.  All
   `143` even residues modulo `286` admit strictly positive nonnegative
   reflected synthetic support weights with `mode_1+mode_2 < -.3`; the
   least-negative extremal row is still about `-2.5799705631335383`.
   Therefore the dominant two-mode lower bound requires actual prime-pair
   arithmetic, a stronger residue-weight constraint, complement/lower-support
   rescue, or a fixed-modulus character-sum theorem.
79. `q286_first_three_dominant_mode_character_sum_obligation_receipt`, with
   note `notes/q286-first-three-dominant-mode-character-sum-obligation.md`
   and evidence in
   `evidence/q286-first-three-dominant-mode-character-sum-obligation.json`,
   states that fixed-modulus theorem exactly.  The dominant `mode_1+mode_2`
   residual uses `50` active complex q286 character products, which reduce by
   conjugacy to `25` real channels and no active self-conjugate channel.  The
   focused regression reconstructs the prior residue-obligation sample ratios
   below `1e-9`; this is narrower than the full `99`-character product space,
   but it is not a single-character or tiny-channel proof.
80. `q286_first_three_dominant_mode_channel_norm_budget_receipt`, with note
   `notes/q286-first-three-dominant-mode-channel-norm-budget.md` and evidence
   in `evidence/q286-first-three-dominant-mode-channel-norm-budget.json`,
   quantifies independent `Linf`/`L2` sufficient bounds for those `25` real
   channels.  The thresholds are about `0.009312260360507715` and
   `0.046390507527336665`.  None of the three near-boundary samples is
   certified; clear rows `1242118` and `1240888` fail both budgets while
   passing the signed dominant floor.  Thus generic channel smallness is too
   blunt at the active scale.
81. `q286_first_three_dominant_mode_signed_channel_profile_receipt`, with
   note `notes/q286-first-three-dominant-mode-signed-channel-profile.md` and
   evidence in
   `evidence/q286-first-three-dominant-mode-signed-channel-profile.json`,
   splits the `25` real-channel sum into positive offset and negative
   pressure.  Tail `1222142` has the largest negative pressure and not enough
   positive offset.  Clear `1242118` has pressure above `.3` but enough
   positive offset, while clear `1240888` clears because its negative pressure
   is already below `.3`.  This points to a two-branch signed-channel theorem
   target rather than independent channel smallness.
82. `q286_first_three_dominant_mode_signed_channel_branch_sample_receipt`,
   with note
   `notes/q286-first-three-dominant-mode-signed-channel-branch-sample.md` and
   evidence in
   `evidence/q286-first-three-dominant-mode-signed-channel-branch-sample.json`,
   applies the same exact branch split to deterministic near-boundary
   mass-matched samples.  Among ten selected rows, five are unresolved
   deficits `24424,13822,55864,164598,1222142`; four clear by the offset
   branch `13556,40420,129706,1242118`; one clears by both pressure and
   offset `1240888`; and none clear by pressure alone.  This demotes a
   pressure-ceiling-only explanation for the selected rows and sharpens the
   live theorem target to positive-offset forcing under pressure, plus
   classification or finite handling of true deficits.
83. `q286_first_three_dominant_mode_channel_swing_pair_receipt`, with note
   `notes/q286-first-three-dominant-mode-channel-swing-pairs.md` and evidence
   in `evidence/q286-first-three-dominant-mode-channel-swing-pairs.json`,
   decomposes six selected deficit-to-clear swings into exact deltas across
   the same `25` real q286 channels.  Channels `(2,6)` and `(3,1)` are helpful
   in all six checked pairs, but a tiny-channel lemma is demoted: reaching
   `80%` of positive delta takes `5` to `9` helpful channels.  The live target
   is now a portfolio-level offset estimate under pressure or a classification
   of true deficit rows.
84. `q286_first_three_dominant_mode_helpful_portfolio_receipt`, with note
   `notes/q286-first-three-dominant-mode-helpful-portfolio.md` and evidence in
   `evidence/q286-first-three-dominant-mode-helpful-portfolio.json`, freezes
   those helpful labels into fixed portfolios.  The universal two-channel
   portfolio and the `11`-channel recurrent portfolio both separate selected
   clear rows from selected deficits by portfolio contribution, but the
   two-channel portfolio captures only about `0.053365192147409486` of the
   positive delta on pair `(164598,129706)`, and the recurrent portfolio still
   leaves a nonportfolio residual.  The surviving target is a recurrent
   portfolio lower bound under pressure plus residual control.
85. `q286_first_three_dominant_mode_portfolio_residual_obligation_receipt`,
   with note
   `notes/q286-first-three-dominant-mode-portfolio-residual-obligation.md`
   and evidence in
   `evidence/q286-first-three-dominant-mode-portfolio-residual-obligation.json`,
   bolts on the `11`-channel recurrent portfolio and subtracts it exactly
   from the selected dominant rows.  The remaining floor condition is the
   exact rowwise obligation
   `portfolio_sum >= -0.3 - nonportfolio_residual_sum`, with maximum row
   identity error `0` and maximum floor-identity error about `2.78e-17`.  The
   worst selected miss is target `55864` by about `0.0992285758`; the tightest
   selected clear is target `13556` by about `0.0095640903`.  The surviving
   target is now a recurrent-portfolio lower bound against this residual
   requirement, or a residual-channel theorem that keeps the requirement in a
   provable range.
86. `q286_first_three_dominant_mode_residual_channel_profile_receipt`, with
   note `notes/q286-first-three-dominant-mode-residual-channel-profile.md`
   and evidence in
   `evidence/q286-first-three-dominant-mode-residual-channel-profile.json`,
   profiles the `14` channels left after the recurrent portfolio is removed.
   No individual residual channel separates selected clears from selected
   deficits, and the residual delta is negative in every selected
   deficit-to-clear pair.  The harshest residual pressure and harshest
   residual sum both occur at passing target `13556`.  This demotes a small
   residual-channel classifier; the recurrent portfolio must overcome adverse
   residual requirements unless a genuine residual-channel theorem is proved.
87. `q286_first_three_dominant_mode_portfolio_ablation_receipt`, with note
   `notes/q286-first-three-dominant-mode-portfolio-ablation.md` and evidence
   in `evidence/q286-first-three-dominant-mode-portfolio-ablation.json`,
   ablates the fixed recurrent portfolio.  Removing any one of the `11`
   recurrent channels changes the selected pass/fail classification; removing
   one of five channels `(2,6),(3,1),(4,8),(5,5),(5,3)` makes at least one
   selected clear row fail.  A four-channel prefix keeps every selected clear
   row passing but over-rescues every selected failing row.  This demotes a
   tiny exact classifier and splits the live theorem into a clear-side
   lower-bound package plus a separate deficit exclusion/rescue problem.
88. `q286_first_three_dominant_mode_prefix_tail_classification_receipt`, with
   note
   `notes/q286-first-three-dominant-mode-prefix-tail-classification.md` and
   evidence in
   `evidence/q286-first-three-dominant-mode-prefix-tail-classification.json`,
   makes the ablation split exact.  The four-channel prefix
   `(2,6),(3,1),(4,8),(4,2)` keeps selected clears passing and over-rescues
   selected deficits.  The seven-channel tail
   `(3,11),(5,5),(4,4),(1,3),(5,3),(2,4),(4,6)` restores all selected
   deficits and preserves all selected clears.  The exact tail obligation is
   `tail_sum >= -prefix_slack`.
89. `q286_first_three_dominant_mode_tail_ablation_receipt`, with note
   `notes/q286-first-three-dominant-mode-tail-ablation.md` and evidence in
   `evidence/q286-first-three-dominant-mode-tail-ablation.json`, tests whether
   the seven-channel classification tail can be compressed.  Removing any one
   tail channel loses the selected tail classification, and the first tail
   prefix that restores all overrescued failures while preserving all clears
   is the full seven-channel tail.  This demotes a one-channel or proper
   prefix tail-correction route on the selected fixture.
90. `q286_first_three_dominant_mode_residual_staircase_receipt`, with note
   `notes/q286-first-three-dominant-mode-residual-staircase.md` and evidence
   in `evidence/q286-first-three-dominant-mode-residual-staircase.json`,
   freezes the prefix/tail order and records the exact remaining rowwise
   requirement after each cumulative channel.  The four-channel prefix first
   clears every selected clear row but still over-rescues the five selected
   deficits `24424,13822,55864,164598,1222142`; the first stage matching the
   selected classification is the full eleven-channel portfolio.  The tail is
   signed: `(1,3)` temporarily makes clear target `13556` fail before `(5,3)`
   repairs it, while `(4,6)` eliminates the last overrescued deficits
   `24424` and `1222142`.  This demotes treating the tail as a monotone
   positive reserve and sharpens the target to cumulative signed portfolio
   control or a replacement deficit-exclusion/complement theorem.
91. `q286_first_three_dominant_mode_staircase_geometry_obstruction_receipt`,
   with note
   `notes/q286-first-three-dominant-mode-staircase-geometry-obstruction.md`
   and evidence in
   `evidence/q286-first-three-dominant-mode-staircase-geometry-obstruction.json`,
   tests the residual staircase against weak support geometry.  For each
   cumulative stage it minimizes and maximizes the partial-channel action over
   synthetic weights with nonnegative local admissible q286 support, total mass
   one, and pair-swap reflection symmetry.  At the full stage, no selected
   classification is forced: pass rows
   `13556,40420,129706,1242118,1240888` are breakable and deficit rows
   `24424,13822,55864,164598,1222142` can be over-rescued.  This closes the
   weak-geometry staircase shortcut while leaving actual prime-pair arithmetic
   and stronger residue-weight constraints open.
92. `q286_first_three_dominant_mode_staircase_arithmetic_gap_receipt`, with
   note
   `notes/q286-first-three-dominant-mode-staircase-arithmetic-gap.md` and
   evidence in
   `evidence/q286-first-three-dominant-mode-staircase-arithmetic-gap.json`,
   measures where actual strict-central prime-pair rows sit inside those weak
   geometry intervals.  Full-stage pass rows lie around
   `0.2166..0.3528` through the weak interval and deficit rows around
   `0.2887..0.4044`, while actual one-sided margins are only
   `0.008833..0.099229` and weak-geometry missing margins are
   `3.313..9.972`.  This sharpens the surviving theorem target to one-sided
   arithmetic placement of actual prime-pair residue weights inside a broad
   weak cone.
93. `q286_first_three_dominant_mode_staircase_orbit_mass_gap_receipt`, with
   note
   `notes/q286-first-three-dominant-mode-staircase-orbit-mass-gap.md` and
   evidence in
   `evidence/q286-first-three-dominant-mode-staircase-orbit-mass-gap.json`,
   measures actual prime-pair mass on the extremal reflected orbit that would
   break each selected staircase row under the weak-geometry obstruction.  At
   the full stage, breaker-orbit mass ranges from `0` to about
   `0.0246193103`, with mean about `0.0106450121`, while top actual orbit
   mass ranges from about `0.0256818041` to `0.0831971135`.  The breaker orbit
   is never the top actual mass orbit on the selected fixture.  This narrows
   the surviving theorem target to dangerous reflected-orbit mass control, or
   a signed aggregate replacement.
94. `q286_first_three_dominant_mode_staircase_hinge_decomposition_receipt`,
   with note
   `notes/q286-first-three-dominant-mode-staircase-hinge-decomposition.md`
   and evidence in
   `evidence/q286-first-three-dominant-mode-staircase-hinge-decomposition.json`,
   decomposes each selected staircase row into exact above-floor positive
   hinge minus below-floor negative hinge.  The maximum identity error is
   about `3.33e-16`.  At the full stage, supporting mass ranges about
   `0.4456..0.5748`, opposing mass about `0.4252..0.5544`, and the selected
   rows split between mass-driven and landing-driven classifications.  This
   demotes a one-dimensional mass-cap or landing-floor route and refines the
   surviving target to a mixed hinge-balance theorem.
95. `q286_first_three_dominant_mode_staircase_hinge_threshold_receipt`, with
   note
   `notes/q286-first-three-dominant-mode-staircase-hinge-threshold.md` and
   evidence in
   `evidence/q286-first-three-dominant-mode-staircase-hinge-threshold.json`,
   rewrites the mixed hinge balance as
   `supporting_mass >= opposing_landing/(supporting_landing+opposing_landing)`.
   The full-stage support-mass surplus ranges from about `0.0028592222` to
   `0.0330812983`, with tightest row `1222142`, and the maximum threshold
   reconstruction error is about `3.19e-16`.  This is an exact obligation
   form, but the support side remains inherited from the finite classification
   and must be defined arithmetically before it can become a non-circular
   theorem.
96. `q286_first_three_dominant_mode_staircase_above_floor_threshold_receipt`,
   with note
   `notes/q286-first-three-dominant-mode-staircase-above-floor-threshold.md`
   and evidence in
   `evidence/q286-first-three-dominant-mode-staircase-above-floor-threshold.json`,
   replaces the post-hoc support side with the arithmetically defined
   above-floor orbit set.  At the full stage, above-floor signed surplus is
   positive on selected passes and negative on selected deficits; pass surplus
   ranges about `0.0034397689..0.0186843046`, deficit surplus about
   `-0.0330812983..-0.0028592222`, and the maximum reconstruction error is
   about `5.41e-16`.  The empty stage has ten sign errors, so this is a
   full-stage target, not an all-prefix theorem.
97. `q286_first_three_dominant_mode_above_floor_holdout_census_receipt`, with
   note
   `notes/q286-first-three-dominant-mode-above-floor-holdout-census.md` and
   evidence in
   `evidence/q286-first-three-dominant-mode-above-floor-holdout-census.json`,
   freezes the same eleven-channel full-stage q286 dominant staircase and
   applies it unchanged to deterministic target blocks.  The fresh primary
   holdout block beginning at `1200200` has `211` passes, no deficits, and
   minimum absolute surplus about `0.0436374645`.  Separate
   stress-neighborhood checks recover known near-boundary rows `1222142` and
   `1242118`.  This turns the next question into a selector or arithmetic
   placement theorem for sparse tiny margins, not another raw threshold scan.
98. `q286_first_three_dominant_mode_near_boundary_selector_audit_receipt`,
   with note
   `notes/q286-first-three-dominant-mode-near-boundary-selector-audit.md` and
   evidence in
   `evidence/q286-first-three-dominant-mode-near-boundary-selector-audit.json`,
   falsifies q286 residue-only and one-scalar interval selectors on the checked
   near-boundary rows.  At the `.005` band, residues `20` and `64` contain the
   two near rows but also `8` safer false positives; residual/floor/mass
   scalar intervals also have false positives at every checked band.  The
   selector theorem must use finer actual prime-pair distribution or be
   replaced by a signed aggregate or rescue theorem.
99. `q286_first_three_dominant_mode_signed_channel_branch_holdout_receipt`,
   with note
   `notes/q286-first-three-dominant-mode-signed-channel-branch-holdout.md`
   and evidence in
   `evidence/q286-first-three-dominant-mode-signed-channel-branch-holdout.json`,
   applies the exact dominant two-mode pressure-or-offset branch split to the
   next nonoverlapping deterministic window after the recorded `1242000`
   stress neighborhood.  All `101` targets from `1243000..1243200` pass the
   dominant floor, all `101` clear by both the pressure and offset branches,
   and no unresolved deficit is found.  The tightest clear row is `1243130`,
   with positive offset slack about `0.0340510877`, and the
   maximum-pressure clear row is `1243018`, with negative pressure about
   `0.2586239309`.  This is finite branch-denominator evidence only; it does
   not prove the eventual branch theorem or the pointwise character-sum input.
100. `q286_first_three_dominant_mode_signed_channel_branch_holdout_receipt`,
   reused by
   `tools/build_q286_first_three_dominant_mode_signed_channel_pressure_horizon.py`,
   with note
   `notes/q286-first-three-dominant-mode-signed-channel-pressure-horizon.md`
   and evidence in
   `evidence/q286-first-three-dominant-mode-signed-channel-pressure-horizon.json`,
   checks sparse post-`1243000` pressure-horizon windows
   `(1244000,51)`, `(1245000,51)`, and `(1246000,51)`.  All `153`
   checked targets pass the dominant floor, all `153` clear the direct
   pressure branch and also have offset slack, and no unresolved deficit is
   found.  The maximum-pressure row is `1244072`, with negative pressure
   about `0.2349931112`, and the tightest slack row is `1244094`, with
   positive offset slack about `0.0341459076`.  This is finite sampled
   pressure-horizon evidence only, not a pressure-branch theorem.
101. `q286_first_three_dominant_mode_signed_channel_profile_receipt`, reused
   by `tools/build_q286_first_three_dominant_mode_pressure_channel_autopsy.py`,
   with note
   `notes/q286-first-three-dominant-mode-pressure-channel-autopsy.md` and
   evidence in
   `evidence/q286-first-three-dominant-mode-pressure-channel-autopsy.json`,
   compares named near-boundary and post-stress pressure rows.  Only
   `1222142` fails among the named rows, with pressure about `0.3719670025`;
   the post-stress maximum pressure is `1243018` at about `0.2586239309`.
   Across the top-three negative real channels of the seven named rows, there
   are `15` distinct labels; `(1,11)` is the most common and appears in three
   rows.  This demotes a one-channel pressure theorem on current evidence and
   sharpens the pressure route to a multi-channel or residue-dependent
   negative-channel envelope.
102. `q286_first_three_dominant_mode_signed_channel_profile_receipt`, reused
   by `tools/build_q286_first_three_dominant_mode_pressure_bulk_share.py`,
   with note
   `notes/q286-first-three-dominant-mode-pressure-bulk-share.md` and evidence
   in `evidence/q286-first-three-dominant-mode-pressure-bulk-share.json`,
   measures how much named-row negative pressure is carried by each row's top
   negative real channels.  The top-one share ranges from about `0.1042376170`
   to `0.1883703993`, the top-three share ranges from about `0.2725197862` to
   `0.4453824162`, the top-five share ranges from about `0.4237604469` to
   `0.6607281866`, and the top-ten share ranges from about `0.7114630603` to
   `0.9523322684`.  Only `1222142` fails among the named rows.  This demotes a
   tiny top-k pressure theorem on current evidence and keeps the live pressure
   target in the bulk multi-channel or residue-dependent envelope class.
103. `q286_first_three_dominant_mode_signed_channel_profile_receipt`, reused
   by
   `tools/build_q286_first_three_dominant_mode_pressure_offset_scalar_falsifier.py`,
   with note
   `notes/q286-first-three-dominant-mode-pressure-offset-scalar-falsifier.md`
   and evidence in
   `evidence/q286-first-three-dominant-mode-pressure-offset-scalar-falsifier.json`,
   tests scalar rescue simplifications after the top-k pressure route was
   demoted.  The named fixture has `4` positive-offset floor counterexamples:
   tail `1222142` has `P=0.0631338229`, more positive offset than clear
   high-pressure row `1242118` with `P=0.0599682402`.  It also has one global
   ratio-floor counterexample: tail `1222142` has `R=0.1697296332`, while clear
   pressure-branch row `1240888` has `R=0.0478553015`.  The exact coupled curve
   `P >= B - 0.3` has no named-row mismatch, but that is algebraic.  This
   demotes scalar offset floors and global scalar ratio floors; the live scalar
   target is coupled pressure/offset curve control or a split theorem implying
   it.
104. `q286_first_three_dominant_mode_signed_channel_profile_receipt`, reused
   by `tools/build_q286_first_three_dominant_mode_pairwise_channel_swing.py`,
   with note
   `notes/q286-first-three-dominant-mode-pairwise-channel-swing.md` and
   evidence in
   `evidence/q286-first-three-dominant-mode-pairwise-channel-swing.json`,
   compares the tail `1222142` against clear rows `1242118` and `1240888`
   channel by channel.  For `1222142 -> 1242118`, the net swing is about
   `0.0253620930`, built from positive swing about `0.2115579838` and negative
   drag about `-0.1861958908`; the largest helpful channel carries only about
   `0.1798138641` of the helpful swing and the top three carry about
   `0.4209404597`.  For `1222142 -> 1240888`, the largest helpful channel
   carries about `0.2027927818` and the top three about `0.4963203849`.  This
   demotes a one-channel tail-to-clear swing theorem; the live route remains a
   coupled aggregate, pressure-subregion, or lower-support/complement theorem.

## Still open

- q286 signed-projection anti-alignment theorem.
- Conditioned complement or lower-support rescue theorem.
- Pointwise binary-prime residue-correlation theorem backing those estimates.
  Its exact q286 form is now identified, but not proved.
- Pointwise lower bounds or structural exclusion for the `25` real q286
  character channels that make up the first two dominant first-three singular
  coordinates, now sharpened to the `11`-channel recurrent portfolio versus
  `14`-channel residual obligation
  `portfolio_sum >= -0.3 - nonportfolio_residual_sum`.  The geometry-only,
  generic norm, pressure-ceiling-only, tiny-channel, and small
  residual-channel classifier, and tiny exact-classifier routes are demoted
  on current evidence; the live target is a recurrent-portfolio or clear-side
  prefix lower bound, tail classification or a separate deficit
  exclusion/complement theorem, a genuine residual-channel bound, or an
  external theorem strong enough to imply the same pointwise inequality.  The
  tested tail-classification package is not visibly compressible, and its
  cumulative action is not monotone-positive under the frozen channel order.
  Weak support/nonnegative/total/reflection geometry also does not force the
  frozen staircase classifications.  The current sharpened target is
  pointwise arithmetic placement inside that broad weak cone: lower bounds for
  pass rows and upper bounds, exclusion, or complement/lower-support rescue
  for deficit rows.  The newest subtarget is to bound actual mass on the
  dangerous reflected breaker orbits that make the weak synthetic witnesses
  possible, then prove the mixed hinge-balance inequality, or replace both
  with a signed aggregate theorem.  The current narrowest formulation is a
  positive support-mass surplus over the landing-dependent hinge threshold,
  plus a non-circular arithmetic definition of the intended support side.  The
  non-post-hoc version uses the full-stage above-floor signed surplus; prefix
  failures remain open and must not be hidden.  The holdout census says the
  frozen full-stage surplus is comfortably positive on one fresh block and
  sparse in the checked stress neighborhoods, so the next useful target is a
  near-boundary selector/arithmetic-placement theorem rather than another raw
  threshold scan.  The simple-selector audit further says this theorem cannot
  be just q286 residue membership, one scalar residual interval, a scalar
  positive-offset floor, or a global scalar positive/negative pressure ratio
  floor on the checked rows.  The pairwise channel-swing diagnostic further
  demotes a one-channel rescue swing on the named tail-to-clear pairs.
- Boundary finite check, endpoint/noncentral terms, and outer assembly.
- Goldbach.

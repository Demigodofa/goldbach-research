# q286 Evidence Glow Map

Status: visualization/data-navigation aid only. This is not a proof of
Goldbach.

## Purpose

Kevin's "stacked numbers/vectors/shapes that light up brighter" idea is now
represented as a generated data layer:

```text
evidence/q286-evidence-glow-map.json
```

The first vector-coordinate overlay is:

```text
evidence/q286-target-vector-overlay.json
```

The first static visual summary is:

```text
evidence/q286-visual-summary.svg
```

The first filter-order audit is:

```text
evidence/q286-filter-order-audit.json
```

They are built by:

```text
python tools/build_q286_evidence_glow_map.py
python tools/build_q286_target_vector_overlay.py
python tools/build_q286_target_vector_pca.py
python tools/build_q286_visual_summary_svg.py
python tools/build_q286_filter_order_audit.py
```

The map overlays existing q286 graph roles, finite evidence receipts, selected
target stress rows, denominator windows, and conditional theorem branches.
Repeated independent hits add to a stack.  The normalized stack weight is
called `glow`.

## Reading Rule

Glow means:

```text
more repo-backed evidence layers overlap here
```

Glow does not mean:

```text
this is proved
```

Every generated record keeps a `boundary` or `status_boundary` field for that
reason.  Bright nodes are good places to inspect mechanisms and falsifiers;
they are not theorem certificates.

## Anti-Attention-Bias Rule

There are two different reasons a point can glow:

```text
evidence glow: independent frozen receipts keep hitting the same mechanism
attention glow: humans/agents kept selecting the same row
```

Only evidence glow is useful.  To avoid confusing them:

- keep denominator counts beside every selected-row stress result;
- keep selected fixtures labeled as selected fixtures;
- do not let repeated manual inspection add weight by itself;
- prefer unchanged selectors on new windows before increasing confidence;
- treat boundary failures as separate shapes, not as dim successes.

The current map already shows this distinction: `1379072` is bright because
several structured evidence layers hit it, but the sample-size/cherry-pick
risk remains explicitly open.

## Current Bright Spots

The regenerated map after the rank-`1` residual/full-window branch highlights:

- `1222142`: still the brightest target.  This is partly evidence glow and
  partly attention glow: it is the stress row, the lone full-window deficit,
  and the row many later receipts subtract against.  Read it as the anchor of
  the obstruction, not as proof that the whole problem is local.
- `1242118`: now becomes the important second-tier hotspot.  It is the closest
  clear in the outside-plane remainder, the worst residual-drag ratio row, and
  a high-drag row in the fixed-channel certificate falsifier.  This is the
  strongest visual sign that the live q286 bottleneck is not merely the deficit
  row; it is the gap between the deficit and the nearest rescued clear.
- `13822`, `164598`, `24424`, and `55864`: remain bright because many earlier
  selected staircase/portfolio layers overlap there.  They matter as repeated
  mechanism fixtures, but they are not the current rank-`1` edge.
- `1220056`, `1222048`, `1220124`, `1221052`, `1200224`, `1221042`, and nearby
  rows now light up as the broader high-drag/residual neighborhood.

The current mechanism stacks highlight:

- `channel-carried-strict-slack`: all three selected late active rows have
  strict closure dominated by channel margin.
- `rank1-cap-survives-full-window`: the frozen Octave rank-`1` direction and
  `0.75` residual-drag cap survived all `715` checked clears in the six-window
  denominator.
- `small-fixed-channel-certificate-refuted`: the simplest sparse explanation
  for residual drag is now visibly closed.
- `near-sharp-rank1-residual-drag-cap` and
  `positive-rank1-outside-direction`: the map now separates the two rank-`1`
  facts: positivity of the SVD shadow, and the near-sharp residual-drag
  inequality still needing proof.

The theorem-gap heat now puts `portfolio-residual-lower-bound` first and
`rank1-residual-drag-bound` second.  That is the current "step back" reading:
two independent-looking bottlenecks keep recurring.  The first is the older
portfolio/residual lower-bound family; the second is the newer rank-`1`
outside-direction plus residual-drag family.  The proof route should look for
a bridge between those two heat islands before spending much more effort on
single-row threshold squeezing.

## Useful Next Extension

The first map deliberately uses only already-structured graph/evidence JSON.
A stronger version should add vector-valued fields directly from q286 receipts:

- first-three, complement, and full-action coordinates;
- `L2` negative-bound utilization;
- strict closure driver and channel margins;
- `(5,7)` and `(7,11)` centered component actions;
- boundary/failure signs as a separate shape channel rather than just a role.

That would make the visualization closer to a true stacked vector field:
targets that share the same mechanism would glow and point in the same
direction, while boundary failures would glow in a different shape/color lane.

The first vector overlay now adds selected target coordinates:

- `first_three`, `complement`, and `full`;
- `.4` alignment/complement certificate margin;
- `(5,7)` and `(7,11)` centered component actions where available;
- strict-closure driver/channel/margin coordinates for active rows;
- role-based shapes: boundary failures as down-triangles, late active
  successes as circles, and alignment-stress successes as diamonds.

## Visualization Roadmap

The next visual layers should be added in this order:

1. Heat/shape map: already started.  Use glow for stacked evidence and shape
   for role/failure/success type.
2. PCA/SVD on selected vector coordinates: ask whether boundary failures and
   late successes separate along a real low-dimensional direction.
3. Complex phase plot: use only after the vector overlay shows a stable
   character/component direction worth viewing as an angle.
4. Convex optimization/cone search: use as a falsifier for geometric claims,
   not as a proof substitute.  Ask whether nonnegative admissible weights can
   reproduce a bad pattern after adding each proposed constraint.

The first selected PCA/SVD layer is now generated:

```text
evidence/q286-target-vector-pca.json
```

It is built by:

```text
python tools/build_q286_target_vector_pca.py
```

On the selected alignment/complement coordinates, PC1 explains about `0.891`
of selected variance and separates boundary failures from rescued/stress
targets.  On the selected lower-support component coordinates, PC1 explains
about `0.897` of selected variance and again separates boundary failures from
late active successes.  This is a useful visualization axis, not a theorem or
population claim.

The static SVG summary superimposes selected component PCA positions, selected
alignment/complement PCA positions, role shapes, glow-scaled target sizes,
`(5,7)/(7,11)` component-vector arrows, and mechanism/theorem glow bars.  It
is deterministic so future commits can be compared directly.  It is also
ordered: selection and finite receipts feed vector coordinates, vector
coordinates feed PCA/shape views, and the views point back to theorem
obligations rather than replacing them.

The filter-order audit answers which predicates are acting as coarse or fine
cloth in the current q286 lane.  On the eight-period fixture, the
`first_three_tail` filter has `4406` targets while the full active selector has
`4405`; after the first-three tail, `first_two_active` removes exactly one
target.  The truly fine residual filter is `full_nonpositive`, with `89`
targets globally and `86` inside the first-three tail.  This is an
`aha-candidate` for theorem navigation only: first-three is the main coarse
separator in this fixture, while the nonrescued/full-nonpositive minority is
where proof pressure remains.

The lift-project dictionary audit adds the first method-transfer layer:

```text
evidence/q286-lift-project-dictionary-audit.json
```

It demotes simple static label-only lifts as the immediate explanation for
the q286 rank-`1` outside direction.  The best low-frequency lift has cosine
about `0.8324697829` with the frozen Octave rank-`1` direction and recovers
`6/10` high-drag rows, which is a partial signal but below the predeclared
hole-tightening gate.  Claude's order-weight proposal is also scored there:
the parity observation is real but not separating, and the order-weight vector
has cosine about `0.304375` with `0/10` high-drag overlap.

The next heldout layer is:

```text
evidence/q286-low-frequency-lift-holdout.json
```

It freezes `full_low_frequency_lift` and replays it on `606` fresh targets
around `1260000` and `1280000`.  The lift survives this heldout with no
nonpositive reconstructed deltas, no `0.75` cap failures, and `8/10` overlap
with the heldout frozen-rank1 high-drag rows.

The target-residue tensor extension is:

```text
evidence/q286-target-residue-lift-holdout.json
```

It adds predeclared `N mod 11/13` row features to the low-frequency channel
basis, trains only on the original full-window rows, and scores the same
heldout denominator.  It fails to improve the static low-frequency lift:
heldout cosine drops from about `0.8302450384` to `0.8259350681`, and
high-drag overlap drops from `8/10` to `7/10`, while positivity and the
`0.75` cap remain intact.

The second low-frequency horizon layer is:

```text
evidence/q286-low-frequency-lift-horizon-holdout.json
```

It keeps the frozen static low-frequency lift on six farther windows,
including stress-marker neighborhoods.  All `606` horizon targets clear,
exact/rank-`1`/low-frequency outside deltas stay positive, both `0.75` caps
survive, and the matrix cosine to the frozen rank-`1` reference is about
`0.8311579645`.  The tight horizon row is `1426262`, which now glows as the
farther stress edge with low-frequency residual-drag ratio about
`0.6419474570`.

The Frobenius/common-divisor claim audit is:

```text
evidence/q286-frobenius-lattice-claim-audit.json
```

It closes one arithmetic-sounding shortcut.  The true `C10 x C12` character
setting is preserved, but the claimed Frobenius formula, `gcd(17,120)` rank
projection, parity-axis split, and cyclotomic unit-rank bridge do not force
the observed rank-`1` vector.  This should glow as a closed shortcut, not as
negative evidence against richer character-sum lifts.

The low-frequency LP cone layer is:

```text
evidence/q286-low-frequency-lp-cone-audit.json
```

It treats the surviving low-frequency DFT features as a finite cone and solves
a bounded LP for the residual-drag cap.  The selected vector survives
training, heldout, and horizon rows with zero nonpositive deltas and zero
`0.75` cap failures.  Worst residual-drag ratios are `0.5000` on training,
`0.3395` on heldout, and `0.4259` on horizon.  Its rank-`1` cosine is only
about `0.6019`, so this glows as a residual-cap certificate candidate, not as
an explanation of the Octave rank-`1` direction.

The DFT/closed-graph/pigeonhole reading is theorem-shaping only: a future proof
would need to replace this finite LP by a bounded Fourier/cone or finite-box
argument on actual admissible prime-pair residue measures.

The far stress LP cone holdout is:

```text
evidence/q286-low-frequency-lp-cone-stress-holdout.json
```

It freezes the selected LP vector from the previous receipt and replays it
without refitting on six farther q286 windows: `6000000`, `8000000`,
`10000000`, `12000000`, `16000000`, and `20000000`.  All `606` targets clear;
there are no dominant-floor deficits, no nonpositive exact/rank-`1`/
low-frequency/LP deltas, and no `0.75` cap failures.  The LP residual drag is
`0.0` on this far holdout because every LP reconstructed delta stays below the
full outside delta.  This strengthens the residual-cap certificate candidate,
but it still does not explain the rank-`1` direction or prove a uniform cone
theorem.

The Riesz-Thorin/logistic/Laplace reading is now recorded as theorem-shaping
only.  A proof route would need an actual operator and arithmetic endpoint
bounds; the finite LP cone is only a measured shadow of that possible
interpolation/cone argument.

The local singular/admissible cone audit is:

```text
evidence/q286-lp-cone-local-singular-audit.json
```

It pushes each locally admissible `N mod 143` residue measure through the same
`17` outside real-character coordinates and compares it with the stress row.
The frozen LP vector has nonnegative local action on all `143` target
residues; the only zero-action residues are `38,64,79,105` modulo `143`.
This is a useful orientation floor for the LP cone.

It is not the missing theorem.  On the `606` far stress rows, empirical LP
deltas and local LP actions have Pearson about `0.00227` and Spearman about
`0.00862`, and `12` rows have zero local action but positive empirical LP
delta.  The glow map therefore adds a new theorem gap:
`ap-count-to-17-channel-bridge` / `fixed-modulus-binary-prime-discrepancy`.
Local admissibility is not enough; the remaining work is quantitative
binary-prime discrepancy inside the admissible cone.

BMOR source lookup for `q=286` is now recorded with the audit:

```text
c_pi = 0.0008772, x_pi = 86,891,851
c_psi = 0.0008379, x_psi = 85,882,271
c_theta = 0.0008411, x_theta = 85,881,413
```

The simpler BMOR Corollary 1.6 threshold for raw AP counts is
`50*286^2 = 4,089,800`.  These are AP prime-count inputs, not direct
certificates for the signed `17`-channel LP/rank-`1` object.

The zero-local target channel decomposition is:

```text
evidence/q286-zero-local-target-channel-decomposition.json
```

This corrects the "12 cases" wording: the `12` cases are target integers, not
neutral channels.  They are the far rows with zero local LP action but positive
empirical LP delta.  After subtracting the corresponding zero local vectors for
residues `38` and `64` modulo `143`, all `12` targets still have positive full
outside and LP-weighted deltas.  Across the `204` channel entries, `138` are
positive and `66` are negative, so the after-local positivity is a signed
17-channel balance rather than all-channel positivity.

The zero-local channel margin audit is:

```text
evidence/q286-zero-local-channel-margin-audit.json
```

It summarizes one row per outside channel for all `12` zero-local targets and
separately for residues `38` and `64`.  Its smallest-subset test is a useful
falsifier: one-channel fixed subsets already keep all `12` targets positive,
with `(5,5)` the best singleton by minimum target margin.  Thus these rows
remain non-local/correlation-sourced, but they do not support the stronger
claim that no small fixed subset works under the LP-weighted positivity metric.

The same-window singleton stability audit is:

```text
evidence/q286-far-singleton-channel-stability-audit.json
```

It separates `12` zero-local seed targets from the other `594` non-seed far
targets.  Kevin's watchlist was `(5,5), (3,1), (3,11), (3,7)`.  All four pass
on the seed targets; only `(5,5)` and `(3,1)` pass on the other `594` targets.

The fresh-window watchlist audit is:

```text
evidence/q286-fresh-window-channel-watchlist-audit.json
```

It replays the watchlist on `606` fresh predeclared targets from starts
`24M,28M,32M,36M,40M,44M`.  Under the same stress reference `1222142`,
`(5,5)`, `(3,1)`, and `(3,7)` pass everywhere; `(3,11)` fails once at
`28000004`.  The remaining glow-map obligation is an alternate-stress or
alternate-deficit reference audit.

The alternate-reference channel audit is:

```text
evidence/q286-alternate-reference-channel-audit.json
```

It replays those `606` fresh targets against selected deficit references
`24424,13822,55864,164598,1222142` and clear-control references
`13556,40420,129706,1242118,1240888`, rebasing the local subtraction for each
reference.  `(3,1)` passes all selected deficit references.  `(5,5)` fails for
deficit references `13822`, `55864`, and `164598`.  Clear controls do not
preserve the live candidates.  The glow map should therefore treat `(3,1)` as
the stronger selected-deficit-reference singleton candidate and demote the
two-channel reference-independent reading.

The centered channel scalar-order audit is:

```text
evidence/q286-centered-channel-scalar-order-audit.json
```

It reduces the alternate-reference result to one scalar per row and channel:
`lp_weight * (empirical channel - local channel)`.  In this centered order,
`(3,1)` puts all five selected deficit references below every one of the
`606` fresh predeclared targets.  Reference `13822` is second-lowest overall
for `(3,1)`, behind only `55864`, with value
`-0.028592853507378977`.  `(5,5)` fails the same check because `13822` is high
there, with centered weighted value `0.009715830696077645`.

The glow-map reading is now narrower and cleaner: `(3,1)` is a finite
selected-deficit scalar separator after local subtraction.  It is not yet a
stress-classifier theorem because the selected deficit references are not a
proved complete or predeclared stress population.

The centered `(3,1)` stress-class audit is:

```text
evidence/q286-centered-3-1-stress-class-audit.json
```

It tests the predeclared `full_nonpositive` class from the baseline
filter-order fixture, independent of `(3,1)`.  That class contains `89` rows.
Centered `(3,1)` fails to classify it: `56/89` rows are at or above the frozen
fresh-window minimum, and the active/nonrescued subclass also fails with
`54/86` rows at or above the fresh minimum.  The next contiguous eight-period
holdout has `0` full-nonpositive rows, so this is a baseline-class falsifier,
not a populated holdout confirmation.

This closes the broad version:

```text
centered (3,1) classifies full_nonpositive q286 stress rows
```

The selected-deficit separator remains a narrower finite fact.  The next
useful class must be defined without `(3,1)` and must actually contain the
selected deficit references, or the route should return to signed/correlation
estimates instead of scalar classification.

The AP-count bridge-gap audit is:

```text
evidence/q286-ap-count-bridge-gap-audit.json
```

It closes the simplest pigeonhole bridge from AP marginals to residue-pair
existence.  For BMOR Corollary 1.6, the count-only ratio
`2q/(phi(q)*log x)` exceeds `1` only below `x = 117.526832200411...`, while
the theorem starts at `4,089,800`.  At the q-specific BMOR `pi` threshold
`86,891,851`, the marginal-pigeonhole ratio is only about `0.249469`, leaving
enough residue-slot room for disjoint reflected sets satisfying the same
counts.  The glow map should therefore treat `raw-ap-count-pigeonhole-bridge`
as a closed shortcut and keep `ap-count-to-17-channel-bridge` open.

## Boundary

This artifact helps navigate hypotheses.  It does not prove rarity, strict
closure, complement lower bounds, pointwise signed prime correlation, outer
assembly, or Goldbach.

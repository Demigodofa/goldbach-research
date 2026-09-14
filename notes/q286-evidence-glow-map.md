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

## Boundary

This artifact helps navigate hypotheses.  It does not prove rarity, strict
closure, complement lower bounds, pointwise signed prime correlation, outer
assembly, or Goldbach.

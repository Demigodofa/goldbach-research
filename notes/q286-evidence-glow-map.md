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

They are built by:

```text
python tools/build_q286_evidence_glow_map.py
python tools/build_q286_target_vector_overlay.py
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

The current generated target stacks highlight:

- `1379072`: graph late-success role, fixed-inequality stress, and positive
  strict-closure margin all overlap.
- `1222142` and `1323632`: graph late-success role plus positive strict
  closure margin.
- `10664` and `14138`: boundary-failure roles remain visible but are not
  bright under this first generated layer because only graph-role evidence is
  currently counted there.

The current mechanism stacks highlight:

- `channel-carried-strict-slack`: all three selected late active rows have
  strict closure dominated by channel margin.
- `tail-thinning-after-cycle-232`: the adjacent cycles `233..264` denominator
  window has zero `.2` near-tail and zero `.3` deep-tail rows.
- `active-selector-rarity`: denominator and scout receipts support the
  question but still leave the theorem open.

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

## Boundary

This artifact helps navigate hypotheses.  It does not prove rarity, strict
closure, complement lower bounds, pointwise signed prime correlation, outer
assembly, or Goldbach.

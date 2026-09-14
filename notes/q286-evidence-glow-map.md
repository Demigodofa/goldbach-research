# q286 Evidence Glow Map

Status: visualization/data-navigation aid only. This is not a proof of
Goldbach.

## Purpose

Kevin's "stacked numbers/vectors/shapes that light up brighter" idea is now
represented as a generated data layer:

```text
evidence/q286-evidence-glow-map.json
```

It is built by:

```text
python tools/build_q286_evidence_glow_map.py
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

## Boundary

This artifact helps navigate hypotheses.  It does not prove rarity, strict
closure, complement lower bounds, pointwise signed prime correlation, outer
assembly, or Goldbach.

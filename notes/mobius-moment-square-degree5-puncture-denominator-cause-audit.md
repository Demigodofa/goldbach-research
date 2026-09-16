# Degree-5 puncture denominator-cause audit

## Question

The translated puncture audit showed that start `1` fails while starts `0`,
`2`, and source start `32` pass for `M=149`, `p=163`, component `(00,12)`.
Can that isolated puncture be localized to reduced-denominator contributions,
or is it diffuse across the active-window Gram?

## Mechanism

For the puncture profile, decompose the `(00,12)` signed half-frame
contribution

```text
active_contribution - (1/2) full_contribution
```

by reduced denominator.  Compare failure start `1` against left neighbor
start `0`, right neighbor start `2`, and source start `32`.

```text
tools/build_mobius_moment_square_degree5_puncture_denominator_cause_audit.py
evidence/mobius-moment-square-degree5-puncture-denominator-cause-audit.json
```

## Result

Only four reduced denominators contribute to this component:

```text
6006, 10010, 15015, 30030
```

The half-frame totals are:

```text
start 0:   -26177271852.077156    passes
start 1:      595626329.758812    fails
start 2:    -5063730056.479225    passes
start 32: -259493747123.1459      passes
```

The failure relative to the left neighbor is dominated by denominator `30030`:

```text
start1 - start0 half-frame delta at q=30030:
19921005797.544876
```

The failure relative to the right neighbor is not the same single-denominator
story:

```text
q=10010 worsens by 4244153577.419586
q=6006  worsens by 2575530739.718094
q=30030 improves by -1099884470.825592
```

## Decision

The puncture is denominator-local enough to change the next theorem target:
source-window/admissible-window work should inspect reduced-denominator phase
structure, not just distance from the source start.  But this finite audit
also blocks a too-simple one-denominator explanation, because the left and
right neighbor comparisons have different dominant denominators.

Candidate mechanism: denominator-phase source admissibility.  Passing source
windows may be governed by phase alignment among a small reduced-denominator
family rather than by monotone distance from the source start.

This is finite diagnostic evidence only.  No denominator-phase theorem,
source-window implication theorem, source-admissible window theorem,
phase-curve theorem, pointwise universal adverse-drag estimate, q286
threshold theorem, strict-central Goldbach theorem, or Goldbach proof is
established.

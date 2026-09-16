# Degree-5 puncture endpoint-swap audit

## Question

The denominator-cause audit localized the translated puncture to a small
reduced-denominator ledger.  Because adjacent active windows differ by one
outgoing row and one incoming row, can the puncture be sharpened further to an
endpoint-swap mechanism?

## Mechanism

For a window of length `A=32`, the shift from start `0` to start `1` removes
row `0` and adds row `32`.  The comparison between start `1` and start `2`
removes row `33` and adds row `1` if written as `start1 - start2`.

Compute the `(00,12)` contribution of each single row by reduced denominator
and check that the adjacent-window deltas are exactly these endpoint swaps.

```text
tools/build_mobius_moment_square_degree5_puncture_endpoint_swap_audit.py
evidence/mobius-moment-square-degree5-puncture-endpoint-swap-audit.json
```

## Result

For `M=149`, `p=163`, component `(00,12)`:

```text
start1 - start0 = row32 - row0
total half-frame delta: 26772898181.83592
dominant q:             30030
q=30030 delta:          19921005797.544834

start1 - start2 = row1 - row33
total half-frame delta: 5659356386.238037
dominant q:             10010
q=10010 delta:          4244153577.4195795
q=6006 delta:           2575530739.718102
q=30030 delta:          -1099884470.8255944
```

So the puncture is not just a whole-window bulk phenomenon.  The adjacent
failure deltas are accounted for by explicit incoming/outgoing endpoint rows
inside the reduced-denominator phase ledger.

## Decision

The adjacent translated-window deltas are explained by endpoint swaps, so the
puncture is not just a whole-window bulk phenomenon.  However, the later
reachability audit shows that start `1` is not reachable from the original
checked-scale source mapping: the canonical source start is `32`.

Thus endpoint-swap denominator-phase structure remains useful for artificial
translated-window diagnostics, but it is not by itself a source-admissible
window theorem target unless a separate arithmetic mapping makes the translated
start source-admissible.

This is finite diagnostic evidence only.  No endpoint-swap theorem,
denominator-phase theorem, source-window implication theorem,
source-admissible window theorem, phase-curve theorem, q286 theorem,
strict-central Goldbach theorem, or Goldbach proof is established.

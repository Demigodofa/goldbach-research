# q286 Dominant-Mode Volatile Boundary-Cut Graph

Status: finite volatile boundary-cut diagnostic only.  This is not a
volatile-rim theorem, stable-core theorem, selected-fixture classifier theorem,
pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The undo-repair receipt is local to fragile clauses plus adverse additions.
This receipt asks whether that repair symmetry persists across the whole
eight-channel volatile Boolean cube.

For each selected row, it enumerates all `256` volatile subsets and all `1024`
one-channel addition edges.  It keeps exactly the edges that cross the
classification boundary:

```text
correct classification -> wrong classification
wrong classification    -> correct classification
```

Then it counts the crossing-channel labels by direction.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_boundary_cut_graph.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-boundary-cut-graph.json`
- Source subset ablation:
  `evidence/q286-first-three-dominant-mode-volatile-subset-ablation.json`
- Source undo-repair channels:
  `evidence/q286-first-three-dominant-mode-volatile-undo-repair-channels.json`

## Results

For the hardest disjunctive row `1222142`, the global volatile-cube boundary
has a clean polarity.  The only one-channel correct-to-wrong additions are:

```text
(1,7): 16 boundary edges
(4,4): 16 boundary edges
```

The wrong-to-correct side uses the complementary six volatile channels:

```text
(1,1):  16
(1,3):  20
(1,5):  22
(2,4):  16
(3,3):  22
(4,10): 20
```

Across the three hard deficit rows, there are `37` correct-to-wrong boundary
edges and `271` wrong-to-correct boundary edges.  Across all selected deficit
rows, there are `172` correct-to-wrong boundary edges and `424`
wrong-to-correct boundary edges.

The selected clear rows behave differently: they have `191` correct-to-wrong
boundary edges and `149` wrong-to-correct boundary edges.  Clear row `1240888`
is boundary-free on this fixture: all `256` volatile subsets classify it
correctly.

## Interpretation

The finite q286 hole tightens again.  The `1222142` adverse side is not merely
locally two-channel near minimal clauses; it is globally two-channel across
the volatile Boolean boundary.  The repair side is spread over the other six
volatile channels.

So the symmetry Kevin remembered is real in this finite fixture, but it is not
yet a proof.  It is now a signed boundary-polarity theorem target: prove that
actual binary-prime residue weights land on the correct side of this volatile
cut uniformly, or replace the Boolean cut picture with a full signed aggregate
arithmetic-placement theorem.

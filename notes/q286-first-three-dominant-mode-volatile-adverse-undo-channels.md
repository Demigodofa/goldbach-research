# q286 Dominant-Mode Volatile Adverse Undo Channels

Status: finite volatile adverse undo-channel diagnostic only.  This is not a
volatile-rim theorem, stable-core theorem, selected-fixture classifier theorem,
pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The clause-stability receipt shows that most minimal deficit clauses are
fragile under extra volatile channels.  This receipt extracts the inclusion-
minimal added channel sets that undo each fragile clause.

For each fragile minimal clause, it enumerates failing supersets and keeps only
the inclusion-minimal added-channel sets.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_adverse_undo_channels.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-adverse-undo-channels.json`
- Source minimal clauses:
  `evidence/q286-first-three-dominant-mode-volatile-minimal-clause-structure.json`
- Source clause stability:
  `evidence/q286-first-three-dominant-mode-volatile-clause-stability.json`

## Results

For `13822`, there is one fragile minimal clause.  Its single minimal adverse
addition is:

```text
(1,5)
```

For `164598`, there is one fragile minimal clause.  Its single minimal adverse
addition is the two-channel set:

```text
(1,1), (1,3)
```

For `1222142`, all ten minimal clauses are fragile.  Across those ten clauses
there are twenty minimal adverse additions, all of size `1`.  They collapse to
the same two one-channel additions repeated for every clause:

```text
(1,7)
(4,4)
```

Thus every `1222142` minimal clause is vulnerable to adding either `(1,7)` or
`(4,4)` alone.

Across the hard rows, the minimal adverse-channel frequencies are:

```text
(1,7): 10
(4,4): 10
(1,1):  1
(1,3):  1
(1,5):  1
```

## Interpretation

The non-undo obstruction is not arbitrary on this fixture.  The hardest
disjunctive row `1222142` has a two-channel undo pattern: every minimal clause
is vulnerable to `(1,7)` or `(4,4)`.

This keeps the clause route alive but narrower.  A proof must pair clause
forcing with signed control of these named adverse additions, or replace the
Boolean-clause route with a full signed aggregate arithmetic-placement
theorem.  The receipt is finite undo-channel evidence only.

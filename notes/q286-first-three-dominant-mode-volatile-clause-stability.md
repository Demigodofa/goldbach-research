# q286 Dominant-Mode Volatile Clause Stability

Status: finite volatile clause-stability diagnostic only.  This is not a
volatile-rim theorem, stable-core theorem, selected-fixture classifier theorem,
pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The minimal-clause receipt extracts inclusion-minimal volatile subsets that
satisfy selected deficit-row thresholds.  This receipt checks whether those
clauses remain valid after adding arbitrary remaining volatile channels.

For each minimal satisfying clause, it enumerates every volatile superset and
counts which supersets still satisfy the same deficit-row classification.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_clause_stability.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-clause-stability.json`
- Source subset ablation:
  `evidence/q286-first-three-dominant-mode-volatile-subset-ablation.json`
- Source minimal clauses:
  `evidence/q286-first-three-dominant-mode-volatile-minimal-clause-structure.json`

## Results

Across the three hard selected deficit rows, there are `14` minimal clauses.
Only `2` are stable under all volatile supersets; `12` are fragile.

For `13822`, one of two minimal clauses is stable:

```text
stable clause:
(1,1), (1,3), (1,7), (2,4), (3,3), (4,4)

fragile clause:
(1,1), (1,3), (1,7), (2,4), (3,3), (4,10)
```

The fragile `13822` clause has one failing superset.  The nearest failing
superset adds `(1,5)` and has margin about `0.0084624530` above the floor.

For `164598`, one of two minimal clauses is stable:

```text
stable clause:
(1,5), (1,7), (4,4)

fragile clause:
(1,5), (2,4), (4,4)
```

The fragile `164598` clause has two failing supersets.  The nearest failing
superset has margin about `0.0013262929` above the floor.

For `1222142`, all ten minimal clauses are fragile.  Each has `16` supersets:
`11` remain satisfying and `5` fail.  The nearest failing superset margins are
small, beginning around `0.0021056957` to `0.0052135929` above the floor.

## Interpretation

Minimality alone is not a theorem.  A proof cannot merely force one minimal
volatile clause unless it also controls the extra volatile channels that can
undo the deficit classification.

This turns the next target into a non-undo problem: pair clause forcing with
signed control of adverse extra channels, or replace the Boolean-clause view
with a signed aggregate arithmetic-placement theorem.  The receipt is finite
stability evidence only.

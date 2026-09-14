# q286 Dominant-Mode Volatile Minimal-Clause Structure

Status: finite volatile minimal-clause structure only.  This is not a
volatile-rim theorem, stable-core theorem, selected-fixture classifier theorem,
pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The forced-channel attribution identifies hard-row obligations inside the
full volatile rim.  This receipt extracts the inclusion-minimal volatile
subsets that satisfy each selected deficit-row threshold after the stable core
is fixed.

Equivalently, it rewrites each hard deficit row as a finite DNF-like clause
family over the eight volatile channels.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_minimal_clause_structure.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-minimal-clause-structure.json`
- Source subset ablation:
  `evidence/q286-first-three-dominant-mode-volatile-subset-ablation.json`
- Source row thresholds:
  `evidence/q286-first-three-dominant-mode-volatile-row-thresholds.json`
- Source forced-channel attribution:
  `evidence/q286-first-three-dominant-mode-volatile-forced-channel-attribution.json`

## Results

The hard selected deficit rows remain:

```text
13822, 1222142, 164598
```

Row `13822` has exactly two inclusion-minimal satisfying clauses.  Both have
six channels.  They are the common five-channel core:

```text
(1,1), (1,3), (1,7), (2,4), (3,3)
```

plus either `(4,4)` or `(4,10)`:

```text
core + (4,4):   margin to floor -0.0448533087
core + (4,10):  margin to floor -0.0045101475
```

Row `164598` also has exactly two inclusion-minimal satisfying clauses.  Both
have three channels.  They are the common two-channel core:

```text
(1,5), (4,4)
```

plus either `(1,7)` or `(2,4)`:

```text
core + (1,7):  margin to floor -0.0101101721
core + (2,4):  margin to floor -0.0049525021
```

Row `1222142` is different.  It has `10` inclusion-minimal satisfying clauses,
all of size `4`, and it has no individually necessary volatile channel across
all satisfying subsets.  The nearest minimal clause is:

```text
(1,1), (1,3), (3,3), (4,10)
margin to floor -0.0001305906
```

The other selected deficit rows are already deficits with the empty volatile
subset, so they do not drive the hard volatile clause structure.

## Interpretation

This refines the volatile theorem target from a full-package obligation into
three finite clause families:

```text
13822:   five-channel core plus one of two alternatives
164598:  two-channel core plus one of two alternatives
1222142: one of ten four-channel alternatives
```

The first two rows have compact row-forced structure.  The `1222142` row is
more disjunctive: no single volatile channel is necessary, even though the
combined hard-row fixture ultimately forces the full rim.

A proof route can now target these exact clause families from actual
binary-prime residue arithmetic, explain why the `1222142` alternatives are
forced in the combined setting, or replace the clause view with a stronger
signed aggregate theorem.  The receipt is finite clause evidence only.

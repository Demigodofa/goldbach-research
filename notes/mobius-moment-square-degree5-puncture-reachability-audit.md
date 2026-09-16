# Mobius moment-square degree-5 puncture reachability audit

## Question

For the translated puncture at `M=149`, `p=163`, component `(00,12)`, is
active-row start `1` reachable from the original checked-scale source mapping,
or only from the artificial translated sweep?

## Receipt

```text
tools/build_mobius_moment_square_degree5_puncture_reachability_audit.py
evidence/mobius-moment-square-degree5-puncture-reachability-audit.json
```

## Calculation

The checked-scale construction uses:

```text
row_count = int((M**(1/.59))**.41)
ell_freeze = row_count + row_count//2
canonical source start = row_count
translated sweep starts = 0..2*row_count
```

For `M=149`:

```text
row_count = 32
ell_freeze = 48
canonical source start = 32
translated sweep starts = 0..64
puncture start = 1
```

Therefore:

```text
start 1 != source start 32
```

The start-`1` active window covers rows `1..32`, while the source active window
covers rows `32..63`.  The prime `p=163` enters the residue-cell phase
calculation, but `p-M=14` is not used as the source-start selector in this
checked-scale construction.

## Answer

```text
UNREACHABLE
```

The start-`1` puncture is a valid translated-sweep falsifier for the broad
all-start quantifier, but it is not a reachable original source-construction
row.

## Decision

Future source-window statements should not treat the start-`1` puncture as a
failure of the original source mapping.  It should be recorded as an
unreachable translated start unless a separate arithmetic mapping makes it
source-admissible.

This is a reachability audit only.  It proves no source-admissible-window
theorem, endpoint-swap theorem, strict-central Goldbach theorem, or Goldbach
proof.

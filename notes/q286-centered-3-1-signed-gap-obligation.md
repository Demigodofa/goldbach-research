# q286 centered (3,1) signed-gap obligation

Status: finite theorem-obligation extraction only.  This is not a proof of a
signed correlation theorem, stress-class theorem, pointwise character-sum
theorem, or Goldbach.

## Source

The generated receipt is:

```text
evidence/q286-centered-3-1-signed-gap-obligation.json
```

The builder is:

```text
tools/build_q286_centered_3_1_signed_gap_obligation.py
```

It reads:

```text
evidence/q286-centered-3-1-same-residue-fresh-population-audit.json
evidence/q286-centered-3-1-residue-collision-audit.json
evidence/q286-centered-3-1-reference-lemma-audit.json
```

## Exact Inequality

For same-residue comparisons modulo `143`, the local q286 channel vector is
identical.  Therefore:

```text
centered_3_1(T) - centered_3_1(R)
  = empirical_3_1(T) - empirical_3_1(R)
```

and the LP-weighted version is the same inequality multiplied by the fixed
positive `(3,1)` LP weight.

The theorem-shaped obligation is:

```text
For a non-post-hoc selected stress-reference family S and future comparison
targets T with T == R mod 143, prove

    empirical_3_1(T) - empirical_3_1(R) > 0

for every R in S, or prove a stronger residue-uniform lower bound that
implies it.
```

## Finite Gates

The checked same-residue fresh-population fixture has `30` gaps: five selected
deficit references, each with six same-residue fresh predeclared targets.
All local gaps are exactly `0.0`.

| reference | residue mod 143 | fresh count | min empirical gap | min weighted gap |
|---:|---:|---:|---:|---:|
| 13822 | 94 | 6 | 0.013241973691 | 0.011427902060 |
| 24424 | 114 | 6 | 0.037797921066 | 0.032619830704 |
| 55864 | 94 | 6 | 0.033134569888 | 0.028595330900 |
| 164598 | 5 | 6 | 0.008410526629 | 0.007258334507 |
| 1222142 | 64 | 6 | 0.024609319047 | 0.021237988716 |

Global checked gap summary:

```text
empirical gaps: count 30, min 0.008410526628774508,
                mean 0.027972535775710735,
                max 0.04200647681997524

weighted gaps:  count 30, min 0.007258334506941435,
                mean 0.02414046475673295,
                max 0.03625183935264326
```

The tightest checked gate is reference `164598` at residue `5`, not `13822`.
Reference `13822` remains a strong witness, but the proof target must survive
the smaller `164598` margin.

## Falsifier

Any same-residue fresh or future target `T` with:

```text
weighted_centered_3_1(T) <= weighted_centered_3_1(R)
```

for a selected stress reference `R` falsifies the corresponding finite or
proposed uniform signed-gap claim.

## Decision

The next theorem path is no longer a local-residue claim.  It is a signed
empirical/correlation gap claim for centered `(3,1)`.  The broad
`full_nonpositive` classifier remains falsified; this obligation needs either
a non-post-hoc stress family containing the selected references or an analytic
estimate that controls the same-residue `(3,1)` empirical gap.

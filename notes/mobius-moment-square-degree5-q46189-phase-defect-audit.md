# Mobius moment-square degree-5 Q46189 phase-defect audit

## Question

Does the `Q=46189` exception reduce to a coordinate proportionality and a
finite-window energy defect?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_phase_defect_audit.py
evidence/mobius-moment-square-degree5-q46189-phase-defect-audit.json
```

## Result

For the target `(00,12)` component, coordinate `12` is a fixed negative scalar
multiple of coordinate `00` on the `Q=46189` residue cells, to numerical
precision:

```text
best scalar right/left:       -0.07475328212536138
relative scalar residual:      2.577250390614836e-16
scalar phase:                  pi
active/full cross ratio:       0.4973090372347702
half-threshold defect:         0.0026909627652297874
```

So the adverse denominator is not caused by uncontrolled coordinate geometry.
It is an aligned finite-window energy defect: the one-coordinate active/full
energy ratio is below the one-half threshold.

The other two component pairs are also adverse at this denominator:

```text
00,12  active/full=0.4973090372347702  defect=0.0026909627652297874
01,02  active/full=0.4982797262153668  defect=0.0017202737846331861
01,11  active/full=0.4968228166894951  defect=0.0031771833105049274
```

## Decision

`FALSIFIER_q46189_per_denominator_nonadversity`.

The `Q=46189` exception is a finite falsifier for any theorem requiring every
middle/far denominator to be nonadverse.  The surviving theorem target is
group payment for aligned negative finite-window phase defects.

Smallest next test: compute the positive denominator rows in the
`M=229`, `p=379` middle/far ledger that share the `11*13*17*19` tail or add
one missing small prime, then test whether their surplus dominates the
`Q=46189` phase defect without using total positivity.

This is finite phase-defect evidence only.  It proves no per-denominator
nonadversity theorem, phase-defect payment theorem, near-adverse upper bound,
middle/far lower bound, clearance-family theorem, source-start theorem,
strict-central Goldbach theorem, or Goldbach proof.

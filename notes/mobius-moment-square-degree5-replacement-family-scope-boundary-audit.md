# Mobius moment-square degree-5 replacement-family scope boundary audit

## Question

After the `Q=46189` replacement-family payment audit, how broad is the
current checked support for middle/far adverse replacement families?

## Receipt

```text
tools/build_mobius_moment_square_degree5_replacement_family_scope_boundary_audit.py
evidence/mobius-moment-square-degree5-replacement-family-scope-boundary-audit.json
```

## Result

```text
source-start checked blocks:                 6
source near negative denominators:           17
source middle/far negative rows:             1
band checked blocks:                         4
band near negative denominators:             17
band middle/far negative rows:               1
same middle/far exception:                   True
Q46189 replacement payment / defect:         1740.1304948156007
Q46189 minimum row payment / defect:         36.74165224066973
```

The only checked middle/far adverse row in both receipts is the same
`M=229`, `p=379`, `label=00,12`, `Q=46189` exception.  All other
adverse denominator rows in these receipts are near-threshold.

## Decision

Replacement-family payment remains a live theorem target, but it is narrow:
the current checked middle/far adverse support is one exemplar.  Do not
promote it as a broad finite holdout pattern.  The universal pointwise
route still needs an independent near-threshold leakage upper bound, plus
either a symbolic `Q=46189` replacement-family inequality or additional
middle/far adverse examples.

This proves no replacement-family payment theorem, phase-defect payment
theorem, near-adverse upper bound, middle/far lower bound, clearance-family
theorem, source-start theorem, strict-central Goldbach theorem, or Goldbach
proof.

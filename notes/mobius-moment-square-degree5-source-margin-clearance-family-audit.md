# Mobius moment-square degree-5 source-margin clearance-family audit

## Question

For the tightest checked source-start prime blocks, how does adverse
denominator mass split by clearance above the cutoff `p*A`, where `A` is the
source row count?  Is low-clearance leakage dominated by higher-clearance
mass?

## Mechanism

Read the prime-block theorem-obligation receipt, recompute the exact
source-start reduced-denominator ledger for each tight block, and group each
weakest-label denominator `Q` into:

```text
near_1_to_2    p*A < Q < 2*p*A
middle_2_to_3  2*p*A <= Q < 3*p*A
far_3_plus     Q >= 3*p*A
```

Then compare near-threshold adverse mass with the positive and net
middle-plus-far higher-clearance families.

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_margin_clearance_family_audit.py
evidence/mobius-moment-square-degree5-source-margin-clearance-family-audit.json
```

## Result

```text
status:                                      AUDIT_degree5_source_margin_clearance_family
scales:                                      229, 251, 293, 331, 353, 379
tight blocks:                                (229,379), (251,379), (293,461), (331,599), (353,599), (379,599)
negative denominator family counts:
  near_1_to_2:                               17
  middle_2_to_3:                              1
  far_3_plus:                                 0
near-threshold negative fraction:             0.9444444444444444
all negative denominators near threshold:     false
all middle/far positive dominates near leak:  true
all middle/far net dominates near leak:       true
max near negative / middle-far positive:      0.0009319007678001933
```

The attractive stronger guess, "all adverse denominators are near-threshold,"
is false.  The only exception in this six-block fixture is at `M=229`,
`p=379`, `Q=46189`, with `Q/(p*A)=2.8342026139780327`.

The weaker and more useful finite fact survives: the net middle-plus-far
higher-clearance margin dominates the absolute near-threshold adverse leakage
on all six tight blocks.

## Decision

This sharpens the next theorem-shaped denominator target.  Do not try to prove
individual denominator positivity, and do not claim that all adverse mass is
forced into `p*A < Q < 2*p*A`.  A more realistic route is to prove a
clearance-family ledger: low-clearance leakage is paid by net middle/far
higher-clearance mass.

This is finite clearance-family evidence only.  It proves no clearance-family
theorem, denominator-margin theorem, prime-block theorem, source-start theorem,
strict-central Goldbach theorem, or Goldbach proof.

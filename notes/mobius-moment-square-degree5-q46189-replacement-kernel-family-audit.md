# Mobius moment-square degree-5 Q46189 replacement kernel family audit

## Question

Across all ten `Q=46189` replacement rows, is the previously selected
weakest replacement also worst by residue-gap kernel metrics, and do
all rows survive off-diagonal drag?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_replacement_kernel_family_audit.py
evidence/mobius-moment-square-degree5-q46189-replacement-kernel-family-audit.json
```

## Result

```text
replacement rows:              10
weakest replacement q:         38038
minimum ratio minus half:      0.07635340770691468
minimum half-margin:           4380137469743.5
minimum offdiag/diag-half:     -0.8472931845861708
max active reconstruction err: 0.6484375
max ledger active-energy err:  1.0859375
max relative energy err:       1.6333201630305224e-14
all rows positive after drag:  true
kernel identities verified:    true within recorded roundoff tolerance
strict abs<1 flags all pass:   false
```

## Decision

The weakest replacement row was not cherry-picked: `q=38038` is worst
across the checked replacement family by ratio gap, margin, and
off-diagonal pressure.  The theorem-shaped target narrows to a
replacement residue-gap lower bound.

This is finite diagnostic evidence only.  It proves no replacement
residue-gap bound theorem, coordinate-00 residue-gap sign theorem,
symbolic coordinate-00 energy ratio theorem, one-coordinate
active/full ratio theorem, strict-central Goldbach theorem, or
Goldbach proof.

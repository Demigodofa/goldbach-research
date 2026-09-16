# q286-WBSS K286 zero-residue phase-pair lift-drift audit

## Question

The `K_286` phase-pair audit falsified a single fixed dominant conjugate-pair
explanation.  Are the moving leading phase-pairs at least determined by target
residue modulo `10010` on the finite zero-lane `L2`-violating rows?

## Mechanism

Read the checked `K_286` phase-pair receipt and raw zero-lane probe.  For each
of the `18` aggregate-`L2` violating rows, record:

```text
target residue
lift index
K286 component sign
top adverse conjugate phase-pair
top rescue conjugate phase-pair
top absolute conjugate phase-pair
```

Then restrict to target residues that appear on two violating lifts and ask
whether those labels are stable across the two lifts.

Receipt:

```text
tools/build_q286_wbss_k286_zero_residue_phase_pair_lift_drift_audit.py
evidence/q286-wbss-k286-zero-residue-phase-pair-lift-drift-audit.json
```

## Result

```text
L2-cap-violating zero-lane rows:              18
distinct target residues:                     14
repeated target residues:                      4
singleton target residues:                    10
rows in repeated residue classes:              8

stable top adverse pair across two lifts:      1 / 4 residues
stable top rescue pair across two lifts:       0 / 4 residues
stable top absolute pair across two lifts:     1 / 4 residues
stable K286 component sign across two lifts:   2 / 4 residues
```

The repeated residues are `286`, `3718`, `4576`, and `7722`.

Only residue `4576` keeps the same top adverse and top absolute phase-pair
across its two checked lifts.  No repeated residue keeps the same top rescue
phase-pair.  The `K_286` component sign itself flips on residues `4576` and
`7722`.

## Decision

`DIAGNOSTIC_k286_phase_pair_residue_only_rule_falsified`.

Target residue alone does not determine the leading `K_286` phase-pair labels
on the finite repeated-lift rows.  The next theorem-shaped target is therefore
lift-sensitive: either a phase-band estimate over moving pairs, or an
extended-lift falsifier showing that even small phase bands do not stabilize.

No lift-dependent phase theorem, phase-band theorem, coefficient-direction
nonalignment theorem, universal pointwise raw bound, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof is established.

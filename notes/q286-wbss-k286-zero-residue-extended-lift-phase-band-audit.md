# q286-WBSS K286 zero-residue extended-lift phase-band audit

## Question

The lift-drift audit showed that target residue alone does not determine the
leading `K_286` phase-pair labels across the first two violating lifts.  If
we extend just those repeated residue classes, does the first-two-lift phase
band cover later lifts?

## Mechanism

Take the four repeated zero-lane target residues from the lift-drift audit:

```text
286, 3718, 4576, 7722
```

For each residue, evaluate the first `8` lifts after the raw horizon.  For each
row, recompute the `K_286` conjugate phase-pairs and record the top adverse,
top rescue, and top absolute pairs.  Then ask whether the phase-pair labels
seen in the first two lifts cover the six later lifts.

Receipt:

```text
tools/build_q286_wbss_k286_zero_residue_extended_lift_phase_band_audit.py
evidence/q286-wbss-k286-zero-residue-extended-lift-phase-band-audit.json
```

## Result

```text
extended residues:                              4
lifts per residue:                              8
extended rows:                                 32
future rows after first two lifts:             24

future top-absolute rows covered by first two:  3 / 24
future top-adverse rows covered by first two:   5 / 24
future top-rescue rows covered by first two:    4 / 24

max unique top-absolute pairs in one residue:   7
max unique top-adverse pairs in one residue:    5
max unique top-rescue pairs in one residue:     7

top absolute pair fraction mean:                0.11641633995627859
top absolute pair fraction max:                 0.16050600038977816
pair cancellation ratio mean:                   0.1837093859655672
```

Residue-level top-absolute coverage:

```text
286  -> first-two band covers 1 / 6 later lifts; 7 unique top-absolute pairs
3718 -> first-two band covers 0 / 6 later lifts; 7 unique top-absolute pairs
4576 -> first-two band covers 0 / 6 later lifts; 6 unique top-absolute pairs
7722 -> first-two band covers 2 / 6 later lifts; 5 unique top-absolute pairs
```

## Decision

`DIAGNOSTIC_k286_small_phase_band_not_stable`.

The finite extended-lift check falsifies the small phase-band shortcut seeded
by the first two lifts.  The leading `K_286` phase-pair labels keep moving;
even the top absolute pair is not well covered by the first-two-lift band.

The next theorem-shaped target should stop chasing fixed labels and test a
phase-envelope metric: for each row, how many conjugate pairs are needed to
cover fixed fractions such as `50%`, `75%`, and `90%` of the `K_286` real
absolute envelope?

No moving-band phase theorem, phase-envelope theorem, coefficient-direction
nonalignment theorem, universal pointwise raw bound, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof is established.

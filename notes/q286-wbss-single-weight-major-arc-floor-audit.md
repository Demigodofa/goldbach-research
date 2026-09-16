# q286-WBSS single-weight major-arc floor audit

## Question

Does the combined raw q286 single-weight witness have a positive coefficient
floor on every admissible left-prime residue, so support alone could imply
`W_phi(N)>0`?

## Receipt

```text
tools/build_q286_wbss_single_weight_major_arc_floor_audit.py
evidence/q286-wbss-single-weight-major-arc-floor-audit.json
```

## Result

No.  The normalized combined residue weight

```text
phi(u)=full_q286_wbss_unit_coefficient(u)/principal_mean
```

has global mean `1.0`, but it is not pointwise positive:

```text
unit residues:          2880
negative residues:      1228
zero residues:             0
positive residues:      1652
minimum phi:     -11.747067126163136
maximum phi:      40.228810300155935
```

Every even target residue has at least one admissible left-prime residue with
negative weight:

```text
even target residues:                    5005
rows with negative admissible weight:    5005
rows with pointwise positive floor:         0
minimum local-uniform mean:   0.6039353780830684
maximum negative fraction:    0.47205387205387206
```

The weakest local-uniform rows still have positive average weight:

```text
target residue  target mod 286  mean weight       min weight
4124            120             0.603935378083    -11.747067126163
5886            166             0.603935378083    -11.747067126163
6224            218             0.615983835971    -10.089065110068
3786             68             0.615983835971    -10.089065110069
```

So the local-uniform major term is positive, but individual admissible
residues can be strongly adverse.

## Decision

`FALSIFIER_pointwise_positive_single_weight_floor`.

The support-only shortcut is falsified.  Existence of some strict-central prime
pair would not by itself imply a positive q286 witness, because the pair could
land on a negative-weight admissible residue.  The surviving route must prove a
universal pointwise signed distribution estimate, a one-sided adverse-drag
envelope below local main, or a direct major/minor arc estimate for
`W_phi(N)>0`.

This proves no signed distribution theorem, adverse-drag theorem, major/minor
arc estimate, q286 threshold theorem, strict-central Goldbach theorem, or
Goldbach proof.

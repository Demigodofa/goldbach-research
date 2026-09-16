# Mobius moment-square degree-5 Q46189 residue-gap pressure separation audit

## Question

Which normalized residue-gap pressure components separate the adverse
`Q=46189` row from all source-admissible replacement rows?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_residue_gap_pressure_separation_audit.py
evidence/mobius-moment-square-degree5-q46189-residue-gap-pressure-separation-audit.json
```

## Result

```text
Q far+tail / diag:                 -0.5836029061666043
min replacement far+tail / diag:   -0.26234837388449833
far+tail separator midpoint:       -0.4229756400255513
far+tail separation gap:           0.32125453228210593
Q non-middle / diag:               -0.721340442056593
min replacement non-middle / diag: -0.3390532066023492
non-middle separator midpoint:     -0.5301968243294711
non-middle separation gap:         0.38228723545424376
```

The tempting simpler statistics fail as separators:

```text
Q middle / diag:                   -0.2840414834738627
min replacement middle / diag:     -0.939992990438763
Q top negative gap / diag:         -0.09990152182661793
min replacement top gap / diag:    -0.4983022129718098
```

## Decision

The first useful finite separator is broad pressure, not a top gap.
`Q=46189` has far+tail and non-middle pressure below every checked
source-admissible replacement row.  But the middle bucket alone and
the single largest negative residue gap point in the wrong direction:
`q=38038` is worse by both of those local statistics and still
survives.

The next theorem-shaped target is therefore a source-admissible
far-tail or non-middle lower bound.  This is finite selected-family
diagnostic evidence only.  It proves no far-tail pressure theorem,
non-middle pressure theorem, replacement residue-gap bound theorem,
coordinate-00 residue-gap sign theorem, strict-central Goldbach
theorem, or Goldbach proof.

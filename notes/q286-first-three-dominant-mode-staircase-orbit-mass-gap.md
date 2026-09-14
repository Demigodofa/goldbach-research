# q286 dominant-mode staircase orbit-mass gap

Status: finite orbit-mass diagnostic.  Goldbach is not proved.

This note measures how much actual strict-central prime-pair mass lands on the
extremal q286 reflection orbit that would break each selected staircase row
under the weak-geometry obstruction.

Receipt:
`evidence/q286-first-three-dominant-mode-staircase-orbit-mass-gap.json`

## Mechanism Tested

The weak-geometry obstruction can break any selected full-stage classification
by concentrating synthetic mass on an extremal reflected q286 orbit:

- for a selected pass row, the breaking orbit is the minimum-action orbit;
- for a selected deficit row, the breaking orbit is the maximum-action orbit.

This receipt asks whether the actual prime-pair weights are concentrated on
those breaker orbits.

## Measured Shape

At the full eleven-channel stage, actual mass on the breaker orbit is small:

```text
minimum 0
mean    0.0106450121
maximum 0.0246193103
```

The top actual reflection-orbit masses are larger:

```text
minimum 0.0256818041
mean    0.0446350676
maximum 0.0831971135
```

The breaker orbit is never the top actual mass orbit on the selected fixture:

```text
breaking_orbit_top_actual_count = 0
```

Several breaker orbits have zero actual mass, including selected rows
`24424`, `13556`, `13822`, and `55864`.  The largest breaker-orbit actual mass
is at clear row `1242118`, about `0.0246193103`, only about `1.2187` times its
uniform reflected-orbit share.

## Consequence

The weak synthetic obstruction works by placing mass on an extremal orbit, but
actual prime-pair mass does not visibly concentrate there in the selected
rows.  The next theorem target can therefore be sharpened:

```text
bound actual prime-pair mass on dangerous q286 reflection orbits,
or prove a signed aggregate replacement that makes such concentration
unnecessary.
```

This does not prove the staircase theorem.  It only identifies one concrete
arithmetic structure missing from the weak-geometry model: actual
strict-central prime-pair mass is spread away from the extremal breaker orbits.

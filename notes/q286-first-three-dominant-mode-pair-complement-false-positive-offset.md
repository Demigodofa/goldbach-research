# q286 Pair/Complement False-Positive Offset Autopsy

Status: finite false-positive autopsy only.  This explains why the first clear
row inside the expanded `.02` pair/complement box clears; it is not an
arithmetic placement theorem, signed projection theorem, or Goldbach proof.

## Mechanism

The expanded window holdout found that clear row `1200302` lies inside the
`.02` stress-centered pair/complement square around deficit row `1222142`.
This receipt compares the full dominant first-three sum with the two-coordinate
volatile pair/complement total:

```text
outside-plane dominant contribution
  = dominant_sum_to_principal - volatile_pair_complement_total
```

The goal is to determine whether the clear false positive is rescued by the
pair/complement plane itself or by omitted dominant-channel mass outside that
plane.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_pair_complement_false_positive_offset.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-pair-complement-false-positive-offset.json`
- Sources:
  `evidence/q286-first-three-dominant-mode-near-boundary-selector-audit.json`,
  `evidence/q286-first-three-dominant-mode-pair-complement-window-holdout.json`

## Results

The first expanded false positive is:

```text
1200302   clear
pair sum            0.0101025261
complement sum     -0.0789977905
plane L1 distance   0.0195523595
plane Linf distance 0.0115203663
```

Relative to stress row `1222142`, this clear row is slightly worse in the
two-coordinate volatile plane:

```text
volatile pair/complement total delta: -0.0034883731
```

But it is much better outside that plane:

```text
outside-plane dominant delta:  0.2158368813
full dominant-sum delta:       0.2123485082
outside/full delta share:      1.0164275847
```

The above-floor surplus difference is also positive:

```text
above-floor signed surplus delta: 0.0676989195
```

## Interpretation

The `.02` pair/complement box did not fail because the plane was useless; it
failed because the plane is incomplete.  The first false positive is close to
the stress row in the named pair/complement coordinates, and its volatile
plane total is slightly worse, but the omitted dominant-channel contribution
more than supplies the full dominant rescue.

The next theorem obligation is therefore a three-part balance: named pair,
repair complement, and the outside-plane dominant remainder.  Any proof route
has to control that remainder arithmetically from actual binary-prime residue
weights, or replace the whole decomposition with a stronger signed aggregate
estimate.

# q286-WBSS K286 zero-residue directional-slack audit

## Question

The observed character-moment audit falsified a plain aggregate `L2` bridge:
`18/70` targeted zero-lane rows exceed the sufficient local aggregate `L2` cap
while the raw adverse gate remains positive.  Is the finite survival explained
by directional slack between the Cauchy `L2` threat and the actual adverse
coefficient direction?

## Mechanism

For each row, compute

```text
cauchy_l2_threat_ratio = aggregate_character_moment_l2 / local_l2_cap
directional_efficiency = raw_adverse_drag_ratio / cauchy_l2_threat_ratio
```

The first ratio is the normalized worst-case Cauchy threat.  The second ratio
measures how much of that threat is actually realized as raw adverse drag.

Receipt:

```text
tools/build_q286_wbss_k286_zero_residue_directional_slack_audit.py
evidence/q286-wbss-k286-zero-residue-directional-slack-audit.json
```

## Result

```text
finite zero-lane rows:                      70
local aggregate L2 cap violations:          18 / 70
raw adverse gate positive rows:             70 / 70
positive raw adverse rows:                  68 / 70
zero raw adverse rows:                       2 / 70

all-row directional efficiency min:          0.0
all-row directional efficiency mean:         0.05215378602893012
all-row directional efficiency max:          0.21423128828054358

violating-row Cauchy threat mean:            1.1189916481072606
violating-row raw adverse mean:              0.06125731999751208
violating-row directional efficiency mean:   0.05468085899942172
violating-row directional efficiency min:    0.0007566063462656461
violating-row directional efficiency max:    0.19440538748390473

largest L2-threat target:                    1171456
largest L2-threat residue:                   286 mod 10010
largest L2-threat ratio:                     1.354153874306624
largest L2-threat actual adverse ratio:      0.024989313695990587
largest L2-threat directional efficiency:    0.018453821364123796
```

## Decision

`DIAGNOSTIC_zero_residue_directional_slack_observed`.

This is a useful candidate, not a proof.  The finite data says the failed
aggregate `L2` route should be replaced by a coefficient-direction
nonalignment target: even when aggregate active-character `L2` is too large
for the blunt Cauchy payment, the actual adverse projection can remain small.

The next evidence-bearing step is to decompose the directional efficiency by
modulus and character phase on the `18` cap-violating rows.  A universal proof
would still need a pointwise, unnormalized analytical estimate showing raw
adverse drag below local main for every sufficiently large `N`.

No coefficient-direction nonalignment theorem, signed/phase-aware character
theorem, universal pointwise raw bound, q286 threshold theorem, strict-central
Goldbach theorem, or Goldbach proof is established.

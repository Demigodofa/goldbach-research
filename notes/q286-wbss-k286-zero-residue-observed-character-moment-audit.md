# q286-WBSS K286 zero-residue observed character-moment audit

## Question

The `K_286` zero-residue budget schedule computed sufficient aggregate
active-character `L2` caps for `N == 0 mod 286`.  Does the observed finite
zero-lane probe actually stay below those caps, so that aggregate character
`L2` could be treated as the live bridge?

## Mechanism

Recompute the active-character moments on the `70` targeted zero-residue raw
probe rows from
`evidence/q286-wbss-k286-zero-residue-raw-horizon-probe.json`, using the same
active-character masks as the multiplicative-character moment audit and the
local caps from
`evidence/q286-wbss-k286-zero-residue-character-budget-schedule.json`.

The test compares each observed aggregate active-character `L2` value against
the sufficient local cap for that row's period residue.

## Result

```text
finite zero-lane rows:                 70
raw adverse gate positive rows:        70 / 70
zero pair-count rows:                   0
local aggregate L2 cap violations:     18 / 70
global aggregate L2 cap violations:    66 / 70
aggregate L2 minimum:       0.09541894855503372
aggregate L2 mean:          0.15214146088103925
aggregate L2 maximum:       0.19292792994833513
ratio-to-local-cap minimum: 0.5008426004951454
ratio-to-local-cap mean:    0.8570306512967532
ratio-to-local-cap maximum: 1.354153874306624
worst target:                         1171456
worst target residue:                     286 mod 10010
worst aggregate L2:       0.17499545077585937
worst local L2 cap:       0.1292286305834065
```

Receipt:

```text
tools/build_q286_wbss_k286_zero_residue_observed_character_moment_audit.py
evidence/q286-wbss-k286-zero-residue-observed-character-moment-audit.json
```

## Decision

`DIAGNOSTIC_zero_residue_plain_character_l2_not_observed_bridge`.

Plain aggregate active-character `L2` is not the observed finite bridge.  The
raw zero-lane adverse gate survives on all checked rows, but `18/70` rows exceed
the sufficient local aggregate `L2` cap.  That means the finite survival is not
explained by norm size alone.

The next theorem-shaped move is signed or phase-aware: measure and then try to
prove control in the actual coefficient direction of the adverse projection, or
prove a direct raw witness theorem.  A universal result would need a pointwise,
unnormalized analytical estimate of the adverse drag below the local main term
for every sufficiently large `N`; this audit does not provide that estimate.

No zero-residue raw adverse-drag theorem, aggregate character-moment theorem,
signed/phase-aware character theorem, universal pointwise raw bound, q286
threshold theorem, strict-central Goldbach theorem, or Goldbach proof is
established.

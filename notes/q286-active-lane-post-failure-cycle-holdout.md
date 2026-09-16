# q286 active-lane post-failure cycle holdout

## Question

The source-summary phase audit found a pass-only suffix after target `647392`,
but the suffix had only `11` rows.  If we stop relying on source-summary rows
and scan full q286 denominator cycles, do active rows beyond the failure edge
reintroduce a nonpositive frozen coupled-slack margin?

## Receipt

```text
tools/build_q286_active_lane_post_failure_cycle_holdout.py
evidence/q286-active-lane-post-failure-cycle-holdout.json
```

The predeclared windows are:

```text
first full cycle after largest source-summary failure: 647394..657402
first full cycle after source-summary maximum:         955834..965842
targets per cycle:                                    5005
```

The selector remains:

```text
first_two_modes_to_principal_ratio < -0.2
first_three_modes_to_principal_ratio < -0.3
```

Every active-selector hit is direct-validated against the original mode
receipt, then checked with the same frozen component-pair coupled-slack scalar
used by the previous audits.

## Result

```text
scanned targets:                    10010
first-three tail rows:                  1
active-selector rows:                   1
active target:                     650476
active targets already in source summary: [650476]
active targets not in source summary:    []
positive coupled-slack active rows:      1
nonpositive coupled-slack active rows:   0
later full-cycle active rows:            0
```

For the active row:

```text
target:                              650476
first two / principal:              -0.3407986748203168
first three / principal:            -0.3387236396415376
full action / principal:             0.850347883440006
driver margin:                       0.046220272287445185
channel contribution:                0.35037194097924085
strict coupled-slack margin:         0.39659221326668603
```

The later cycle after the source-summary maximum is support-starved:

```text
start:                              955834
end:                                965842
first-three tail rows:                   0
active-selector rows:                    0
minimum first-three target:          957722
minimum first-three ratio:          -0.26659716030658176
```

## Decision

This finite audit gives no fresh nonpositive strict-slack falsifier.  The
first post-failure full cycle has exactly one active row and it survives the
frozen coupled-slack scalar.  But that active row, `650476`, was already
present in the source-summary suffix; the genuinely later full cycle adds
zero-hit denominator evidence, not a new strict-slack row.

So the phase story remains unproved.  The result points more toward
active-selector rarity as the next theorem obligation than toward promoting a
phase-transition closure theorem.

## Boundary

Finite predeclared cycle audit only.  This proves no phase transition theorem,
active-lane theorem, pointwise adverse-drag theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.  A real acceptance
condition would still require a universal, pointwise, non-circular analytic
estimate, not another finite scan.

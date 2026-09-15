# q286 active-lane strict-closure post-discovery stress

## Question

The selected-late strict-closure receipt tested only three late active rows.
If the same frozen closure constants are applied to one worst unchanged
active-lane sample row from every post-discovery block, does the endpoint
certificate still stay positive?

## Selection

Source:

```text
evidence/q286-principal-rescue-obstruction-audit.json
```

For each post-discovery block `1..11`, select the source-summary row satisfying

```text
first_two_modes_to_principal_ratio < -0.2
first_three_modes_to_principal_ratio < -0.3
```

with the smallest `full_action_to_principal_ratio`, breaking ties by target.
The selected targets are:

```text
94856, 194384, 255704, 383486, 480614, 548666,
594112, 658598, 805682, 846632, 955832
```

## Result

Receipt:

```text
tools/build_q286_active_lane_strict_closure_post_discovery_stress.py
evidence/q286-active-lane-strict-closure-post-discovery-stress.json
tools/build_q286_active_lane_strict_closure_phase_space_html.py
evidence/q286-active-lane-strict-closure-phase-space.html
```

The frozen selected-late strict-closure endpoint does **not** survive this
stronger stress selection.

```text
scanned targets:                 11
tail targets:                    11
positive strict margins:          5
nonpositive strict margins:       6
minimum strict closure margin:   -1.1917268781786845
maximum strict closure margin:    0.36289434822899685
```

The nonpositive endpoint rows are:

```text
94856   -1.1917268781786845
194384  -0.8293645485665107
255704  -0.677466024381995
383486  -0.2897194485643967
480614  -0.3757038899754628
548666  -0.13996577772655594
```

The positive endpoint rows are:

```text
594112   0.014533522125448173
658598   0.23785879449550051
805682   0.3183458978526243
846632   0.36289434822899685
955832   0.1327432030991093
```

## Decision

This is a finite falsifier for the current calibrated selected-late
strict-closure endpoint as a universal active-lane certificate.  It is not a
Goldbach falsifier: the source rows still have positive full action.  The
failure says that the selected-late scalar is too narrow and cannot be promoted
to a pointwise active-lane theorem.

The next theorem-shaped target must become one of:

- a genuinely pointwise, unnormalized analytic estimate for the adverse term
  below the local main;
- a proved phase/scale condition explaining why early post-discovery stress
  rows fail this scalar while later stress rows pass;
- a replacement decomposition with constants calibrated independently of a
  selected-late finite fixture.

## Visualization Schema

The receipt includes `phase_space_points` using the following non-circular
encoding:

```text
x          = log(target)
y          = driver_margin_to_calibrated_floor
z          = strict_closure_margin_to_calibrated_endpoint
color      = target_mod_286 or target_mod_143
brightness = absolute distance from the zero strict-closure boundary
animation  = block_index_after_discovery, with global_cycle as a secondary key
```

This is a hypothesis and falsifier locator only.  Any visual pattern must be
reduced back to an analytic inequality, an explicit obstruction, or a
predeclared finite test.  The picture is allowed to suggest a route; it is not
allowed to become the proof.

The generated HTML viewer links the 3D scatter and table.  Selecting a point
shows exact `N`, block index, residues modulo `13`, `143`, and `286`,
first-two/first-three ratios, driver margin, channel margin, channel
contribution, strict closure margin, full action, derived maximum normalized
channel, fixed conductor pair `35,77`, and the raw JSON row.

## Validation

```text
py -3 tools/build_q286_active_lane_strict_closure_post_discovery_stress.py
py -3 tools/build_q286_active_lane_strict_closure_phase_space_html.py
py -3 -m unittest test_q286_active_lane_strict_closure_post_discovery_stress.py
```

The HTML viewer was also opened through a local `127.0.0.1` evidence server
and checked visually: the canvas rendered the red/green split, the table
loaded all `11` rows, and selecting target `594112` updated the selected
label and exact detail panel.

## Boundary

Finite post-discovery stress diagnostic only.  No universal active-lane
theorem, adverse-drag theorem, signed prime-correlation theorem,
strict-central Goldbach theorem, or Goldbach proof is established.

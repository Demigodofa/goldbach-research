# q286 active-lane conditional theorem

Status: conditional theorem target and proof bookkeeping only.  This is not a
proof of Goldbach.

## Purpose

The recent q286 work has two different kinds of evidence:

- denominator receipts, which say which targets enter the active tail lane;
- fixed-inequality stress receipts, which test one finite inequality only after
  the residual-polygon premise fires.

This note records the strongest current theorem-shaped statement connecting
the q286 active lane to a positive recombined action.  It is meant to prevent
the finite scans from becoming the theorem by accident.

## Active Lane

For the current q286 component-pair route, the active target lane is:

```text
first_two_modes_to_principal_ratio < -0.2
first_three_modes_to_principal_ratio < -0.3
component_pair = ((5,7),(7,11))
```

The selected finite receipts show that the obstruction concentrates in the
`(5,7)/(7,11)` pair, but the universal active-lane theorem remains open.

## Conditional Closure

The receipts
`q286_lower_support_component_pair_action_identity_receipt` and
`q286_lower_support_component_pair_combined_driver_channel_closure_receipt`
measure the identity

```text
full_action / principal = 1 + D(N) + C(N),
```

where:

- `D(N)` is the combined floor driver:

```text
first_three_plus_q286_tail_to_principal_ratio
+ floor_offset_to_principal_ratio
```

- `C(N)` is the centered real-channel pair contribution for
  `((5,7),(7,11))`.

The selected finite receipts give the following constants:

```text
driver floor d0 = -0.1017253843274695
active real-channel L1/principal mean L = 15.262957606760951
normalized channel Linf bound B = 0.05885324711081062
L * B = 0.898274615672529
1 + d0 - L * B ~= 0
```

Thus the proof-shaped implication is:

```text
If D(N) >= d0 + eta_D
and every active normalized real-channel sum is <= B - eta_B
and eta_D + L * eta_B > 0,
then full_action(N) / principal > 0.
```

The weak endpoint `D(N) >= d0` and channel `<= B` only gives a nonnegative
budget at the rounded constants.  A Goldbach-useful theorem must either prove
strict slack, prove a positive discrete lower quantum for the action, or pass
the equality/boundary cases to an independently checked finite computation.

## What Is Closed

The following finite and formal parts are now repo-backed:

- The action identity reconstructs selected full action as `1 + D(N) + C(N)`
  with error below `1e-12`.
- On the selected fixture `14138,1222142,1323632,1379072`, the three late
  positive targets satisfy the conditional closure, while boundary target
  `14138` fails both driver and channel assumptions.
- The strict closure margin
  `D(N) - d0 + L * (B - max_channel(N))` is now executable in
  `q286_lower_support_component_pair_closure_margin_profile_receipt`.
  Focused regression
  `test_q286_lower_support_component_pair_closure_margin_profile` passed in
  `139.808s`.  Boundary target `14138` has margin
  `-3.782909118497761`, while selected late positives have margins
  `0.5506633762515991`, `0.546820393849208`, and
  `0.48379401372791037`.
- The active channel reduction has only fixed conductors `35` and `77`, not
  the whole period `10010`.
- The residual conductor-`77` visual route has been reduced, on the selected
  rows, to thin opposite-sector large-side mass control.
- The component-pair denominator was audited across all `21` unordered
  lower-support component pairs on the selected target fixture.
- The target denominator has only tiny selector evidence so far: one active
  five-target window around `1379072`, one neutral `6x25` selector grid with
  zero active rows, and one same-residue `6x5` holdout with zero active rows.

## What Remains Open

To turn this into a usable theorem for the active lane, one must prove one of
the following, with exact quantifiers over the active target set:

1. `D(N) >= d0 + eta_D` uniformly, plus a fixed-conductor real-channel bound
   `max_channel(N) <= B - eta_B`, with `eta_D + L * eta_B > 0`.
2. The endpoint version `D(N) >= d0` and `max_channel(N) <= B`, plus a proved
   discrete positivity or a complete finite equality-case check.
3. A sharper replacement decomposition that lowers `L`, lowers the needed
   `B`, or proves the centered pair sum directly without the crude L1/Linf
   endpoint.

Any of these still needs the outer assembly: finite boundary cases, endpoint
terms, noncentral terms, and the final translation from this q286 lane to
Goldbach coverage.

## Current Best Next Step

The most theorem-relevant next step is not another threshold ladder.  It is a
strict-slack audit:

```text
For every target that enters the active selector,
measure D(N) - d0, B - max_channel(N), and
D(N) - d0 + L * (B - max_channel(N)).
```

This scalar is the conditional closure margin.  A negative value falsifies the
current constants.  A positive value on more predeclared active targets would
not prove the theorem, but it would identify which of the two universal
assumptions is actually carrying the slack.

`q286_active_lane_strict_closure_margin_census_receipt` now implements this
audit with calibration constants frozen from
`14138,1222142,1323632,1379072`.  The focused regression
`test_q286_active_lane_strict_closure_margin_census` passed in `259.586s`.
The compact active-window evidence in
`evidence/q286-active-lane-strict-closure-margin-census-1379072-window.json`
scanned `1379072,1379074,1379076,1379078,1379080`, selected `1379072`, and
measured strict closure margin `0.48379401372791037`.

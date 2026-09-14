# q286 dominant-mode above-floor holdout census

Status: finite diagnostic and theorem-shaping evidence only.  This is not a
uniform margin theorem, not a signed prime-correlation theorem, and not a
Goldbach proof.

## Mechanism

Freeze the full eleven-channel q286 dominant-mode staircase from the selected
stress fixture:

```text
(2,6),(3,1),(4,8),(4,2),(3,11),(5,5),(4,4),(1,3),(5,3),(2,4),(4,6)
```

Then apply it unchanged to fresh target rows.  For each target, keep the
nonportfolio residual explicit, compute the row floor for the frozen portfolio,
split reflected q286 orbits into those whose full-stage action is above that
floor and below that floor, and record

```text
above_mass - below_landing/(above_landing + below_landing).
```

The sign reconstructs the fixed-stage slack algebraically.  The useful evidence
is therefore not "the identity works", but the holdout distribution of margins:
how close to zero, which residues, and whether sparse hard rows recur.

## Receipt

- Function:
  `q286_first_three_dominant_mode_above_floor_holdout_census_receipt`
- Builder:
  `tools/build_q286_first_three_dominant_mode_above_floor_holdout_census.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-above-floor-holdout-census.json`
- Focused regression:
  `test_q286_first_three_dominant_mode_above_floor_holdout_census`

## Primary Holdout

The primary independent holdout is the contiguous block beginning at
`1200200`, with `211` even targets.

Observed:

- evaluated targets: `211`
- full-stage pass count: `211`
- full-stage deficit count: `0`
- signed surplus range:
  `0.043637464512128576..0.16021112388937347`
- mean signed surplus: about `0.09669949661574788`
- no rows with absolute surplus below `.03`
- maximum threshold reconstruction error:
  about `7.77e-16`

Closest primary-holdout row:

```text
N = 1200224
N mod 286 = 168
above-floor surplus = 0.043637464512128576
dominant sum = -0.15028340975129342
nonportfolio residual = -0.09810936623750449
```

This fresh block gives no near-zero random hit.  It also cannot prove a
uniform margin: it is one finite block.

## Stress-Neighborhood Comparison

The builder also records deterministic `101`-target stress-neighborhood
censuses.  These are labelled separately because some windows include
previously selected near-boundary targets.

Summary:

```text
start 1220000: 101 pass, 0 deficit, min abs surplus 0.04023311644888955
start 1221000: 101 pass, 0 deficit, min abs surplus 0.044915700209767595
start 1222000: 100 pass, 1 deficit, min abs surplus 0.002859222244159798
start 1240000: 101 pass, 0 deficit, min abs surplus 0.0525379332055963
start 1242000: 101 pass, 0 deficit, min abs surplus 0.0047979812823502055
```

The only deficit in these small stress-neighborhood checks is the already-known
selected stress row:

```text
N = 1222142
N mod 286 = 64
above-floor surplus = -0.002859222244159798
```

The `1242000` window similarly recovers the known tight clear row:

```text
N = 1242118
N mod 286 = 20
above-floor surplus = 0.0047979812823502055
```

## Interpretation

This supports a narrower working picture:

1. The frozen full-stage portfolio is not visibly producing random near-zero
   failures across an adjacent fresh block.
2. The scary tiny margins are sparse in the tested stress neighborhoods and
   reappear at already-known selected rows.
3. A proof cannot rely on a comfortable universal surplus buffer, because the
   selected fixture still has margins near `0.003`.

The next non-circular theorem target is therefore a selector or arithmetic
placement theorem for sparse near-boundary rows, plus the existing
complement/lower-support or fixed-modulus prime-pair input.  More threshold
receipts without a selector mechanism would be circular exploration.

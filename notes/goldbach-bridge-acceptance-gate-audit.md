# Goldbach bridge acceptance-gate audit

## Question

What is currently accepted as a logical bridge toward Goldbach, and what
remains only finite arithmetic or theorem-shaped but unproved evidence?

## Receipt

```text
tools/build_goldbach_bridge_acceptance_gate_audit.py
evidence/goldbach-bridge-acceptance-gate-audit.json
```

## Result

The current bridge classification is:

```text
q286 raw adverse-drag:             live theorem target, unproved
q286 normalized/aggregate L2:      HOLD, bridge not confirmed
metric-soft source window:         finite diagnostic, not a bridge alone
```

The zero-mass/L2 status is:

```text
checked-row zero-mass sanity:      confirmed on 348 checked rows
raw strict L2 shape non-circular:  true
L2 logical bridge confirmed:       false
row-local L2 cap violations:       120
global-min L2 cap violations:      301
```

So the answer to the zero-mass question is precise:

```text
zero-mass arithmetic audit: good, finite only
raw strict L2 shape: non-circular theorem shape
actual L2 bridge: not confirmed
```

The live acceptance target remains:

```text
adverse_drag(N) < local_main(N)
```

or in raw form:

```text
A_raw_-(N) < L_raw(N)
```

for every sufficiently large covered even `N`, followed by independent finite
remainder verification.

The current finite q286 adverse-drag calibration has `348/348` checked rows
with adverse drag below local main, with worst checked adverse ratio
`0.23148438379145228` at target `1124642`.  This is calibration and falsifier
evidence only; it is not acceptance.

The metric-soft source-admissible window audit remains useful because it
falsifies the broad all-translation row-start quantifier while keeping the
canonical source windows unobstructed.  But it is not a Goldbach bridge unless
paired with a separate implication theorem.

## Decision

`TARGET_pointwise_unnormalized_bridge_not_finite_acceptance`.

The current accepted bridge target is universal, pointwise, and raw or
unnormalized.  `L2` remains a HOLD unless it proves a strict raw theorem.
Finite zero-mass, observed `L2`, finite adverse-drag, and metric-soft
source-window receipts cannot close the problem by themselves.

This proves no aggregate `L2` theorem, source-window theorem, raw
adverse-drag theorem, q286 threshold theorem, strict-central Goldbach theorem,
or Goldbach proof.

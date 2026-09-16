# q286 anti-landing source-budget audit

## Question

The q286 edge-minorant route reduced one direct-witness bridge to a
coefficient-weighted anti-landing inequality:

```text
positive_rescue_contribution > negative_rescue_drag.
```

If a future source-backed binary-prime theorem tries to prove that inequality,
how sharp does it have to be?

## Receipt

```text
tools/build_q286_anti_landing_source_budget_audit.py
evidence/q286-anti-landing-source-budget-audit.json
```

## Mechanism

Write the exact finite inequality as:

```text
P > D
R = P/D.
```

Then the allowable relative theorem error is:

```text
positive-side loss only:     eps < 1 - 1/R
negative-side inflation only: eps < R - 1
symmetric relative error:     eps < (R - 1)/(R + 1)
```

The symmetric case models a source theorem that proves:

```text
P_theorem >= (1-eps) * P_actual
D_theorem <= (1+eps) * D_actual.
```

## Result

On the `196` post-discovery rows:

```text
tightest target:                         94856
tightest P/D:              1.0191444227555964
tightest positive-loss budget: 0.018784773474983696
tightest negative-inflation budget: 0.019144422755596365
tightest symmetric budget: 0.009481452906409388
rows needing sub-1% symmetric control:      1 / 196
rows needing sub-5% symmetric control:      2 / 196
mass-majority failures:                    18 / 196
```

So the route is not only signed; it is near-sharp on the tightest row.

## Decision

`HOLD_anti_landing_requires_near_sharp_source_control`.

Broad uniformity, mass-majority, and loose AP-count inputs cannot pay this
bridge.  A proof following this route needs a sharp coefficient-weighted
signed binary-prime landing estimate, or the project should pivot to a
different direct witness argument.

## Boundary

Finite source-theorem budget audit only.  This proves no anti-landing theorem,
signed binary-prime correlation theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

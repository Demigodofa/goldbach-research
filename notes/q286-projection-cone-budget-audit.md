# q286 projection-cone budget audit

Status: finite theorem-shaping audit.  This is not a projection-uniformity
theorem, signed binary-prime correlation theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

## Question

After the raw direct sign split failed as an escape from near-sharp
anti-landing, can lower-dimensional projection uniformity supply a cleaner
non-circular bridge?

## Receipt

```text
tools/build_q286_projection_cone_budget_audit.py
evidence/q286-projection-cone-budget-audit.json
```

The LP bad branch is frozen as:

```text
first_three <= -0.3
full_action <= 0
```

and is tested on the seven frozen signed-pair operator targets.

## Result

```text
selected targets:                                   7
prime-factor exact marginal bad feasible:           7 / 7
exact q286 projection-uniform bad feasible:          0 / 7
actual TV exceeds minimum bad TV:                    7 / 7
actual Linf exceeds minimum bad Linf:                7 / 7

minimum bad q286 projection TV:
  min  0.008069873564730923
  mean 0.012850389915227595
  max  0.015018926601606888

actual q286 projection TV:
  min  0.0644180024489798
  mean 0.16819236588095426
  max  0.404040404040404

minimum bad q286 projection Linf:
  min  0.0014957059014651004
  mean 0.001627009773103809
  max  0.0017323472323253607

actual q286 projection Linf:
  min  0.0039569145231730515
  mean 0.012279820131445077
  max  0.03004848667223886
```

The tightest total-variation row is target `1379072`, with minimum bad q286
projection TV `0.008069873564730923`.  Its actual q286 projection TV is
`0.06531704035236255`.

## Decision

Prime-factor projection data is too weak.  Even exact uniform marginals modulo
`2`, `5`, `7`, `11`, and `13` allow synthetic bad measures on all seven frozen
targets.

Exact q286 projection uniformity is sufficient on these rows, but the
quantitative budget is much stronger than the actual checked prime-pair
projection deviations.  Therefore plain q286 projection uniformity is a
sufficient algebraic cone, not a good acceptance condition for the observed
rows.

The next proof object still has to be coefficient-sensitive signed
binary-prime correlation: not raw AP counts, not prime-factor marginals, not
plain q286 projection TV/Linf uniformity, and not raw positive/negative
sign-split landing.

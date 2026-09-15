# q286-WBSS pointwise adverse-drag theorem target

## Question

Finite evidence is no longer the acceptance condition for the q286-WBSS route.
What would count as a real theorem-shaped bridge?

## Answer

The current acceptance target is a universal, pointwise, unnormalized analytic
estimate:

```text
adverse_drag(N) < local_main(N)
```

for every sufficiently large covered even target `N`, followed by independent
finite verification below the threshold.

Here

```text
local_main(N) = M(N) = <u_a, phi_a>
adverse_drag(N) = A_-(N) = sum_d max(0, -E_d(N))
d in {70,130,154,286}
```

where `a = N mod 10010`, `u_a` is the local uniform strict-central orbit
measure, `mu_N` is the actual strict-central binary-prime orbit measure, and
`E_d(N)` is the signed projected error for modulus `d`.

The sufficient pointwise implication is:

```text
A_-(N) < M(N)
  => M(N) + E_70(N) + E_130(N) + E_154(N) + E_286(N) > 0.
```

So the raw q286-WBSS signed witness is positive for that `N`.

## Receipt

```text
tools/build_q286_wbss_pointwise_adverse_drag_theorem_target.py
evidence/q286-wbss-pointwise-adverse-drag-theorem-target.json
```

## Finite calibration

The receipt combines the `232` adverse-drag horizon rows and the `116` fresh
component-envelope holdout rows, for `348` checked rows from `1036248` through
`1155862`.

```text
checked rows:                         348
actual positive rows:                 348 / 348
adverse_drag < local_main rows:       348 / 348
lambda_phi < 1 rows:                  348 / 348
tightest known adverse-drag target:   1124642
tightest adverse-drag ratio:          0.23148438379145228
tightest adverse-only expectation:    0.6835668462365216
```

This finite population is calibration and falsifier evidence only.  It is not
an acceptance condition.

## What is not enough

These are no longer sufficient closeout gates:

```text
another finite horizon pass
a fitted decimal residual absorption constant
a fixed list of per-modulus constants copied from checked rows
lambda_phi < 1 on checked rows without a source-backed estimate
agreement between normalized finite ratios and local intuition
```

The fresh holdout already falsified the literal fixed per-modulus constants:
modulus `286` exceeded its horizon-fitted adverse supremum on two fresh rows.

## Proof obligations

The remaining bridge has four parts:

```text
1. Define the covered even-target class without post-hoc reference to checked rows.
2. Prove M(N)>0 on that class.
3. Prove A_-(N)<M(N) pointwise for every sufficiently large covered even N.
4. Give an explicit threshold N0 and independently verify the finite remainder below N0.
```

The third item is the hard one.  It likely requires a fixed-modulus
binary-prime correlation theorem, a coefficient-aligned signed-discrepancy
estimate, or an equivalent pointwise analytic estimate.  More finite data can
falsify a proposed statement or calibrate constants, but it cannot replace
that theorem.

## Decision

The active q286-WBSS target is now the unnormalized pointwise inequality
`adverse_drag(N) < local_main(N)` for every sufficiently large covered even
`N`, plus finite remainder verification.  Goldbach remains open.

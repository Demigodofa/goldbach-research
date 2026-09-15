# q286-WBSS four-modulus lambda horizon holdout

## Question

The residual absorption constants and the `11,13`-led residual-budget split
fit finite source rows but failed on fresh lifted rows.  The direct
four-modulus q286-WBSS witness remained positive, so the surviving finite
target is the aggregate condition

```text
lambda_phi = -signed_projection_error / local_main < 1.
```

Does that aggregate target survive farther fresh lifts after the prior
far-lift maximum, without requiring rowwise `11,13` negativity or a fixed
residual absorption constant?

## Mechanism

Reuse the same `29` stressed source residues from the residual-absorption
population.  Start after the previous far-lift maximum target `1035742`, and
evaluate eight fresh period-lifts of each residue.  For each new target,
recompute strict-central binary-prime orbit masses and the same explicit
four-modulus coefficient formula.

## Receipt

```text
tools/build_q286_wbss_four_modulus_lambda_horizon_holdout.py
evidence/q286-wbss-four-modulus-lambda-horizon-holdout.json
```

## Result

The horizon contains `232` fresh targets, from `1036248` through `1115822`.

```text
source positive-pushback residues:          29
lift count per residue:                      8
holdout targets:                           232
direct witness positive rows:              232 / 232
direct witness nonpositive rows:             0 / 232
lambda_phi >= 1 failures:                    0
maximum lambda_phi:          0.18121406011311555
largest lambda target:                 1059514
maximum adverse iid-scale z:  1.9123648886316162
largest adverse z target:              1113078
tightest expectation target:           1059514
tightest expectation:         0.609620382302563
```

The previous far-lift maximums were not exceeded:

```text
previous maximum lambda_phi:          0.29444884696113977
current maximum lambda_phi:           0.18121406011311555
previous maximum adverse iid z:       3.5107558040930176
current maximum adverse iid z:        1.9123648886316162
```

## Decision

The farther horizon preserves the aggregate four-modulus lambda target on
every checked row.  Unlike the failed residual and `11,13`-led splits, this
target does not require rowwise edge negativity.  This is still finite
holdout evidence only: it proves no signed concentration theorem, no
fixed-modulus equidistribution theorem, no q286 threshold theorem, no
strict-central Goldbach theorem, and no Goldbach proof.

The next theorem target remains a source-backed signed concentration or
fixed-modulus equidistribution estimate proving `lambda_phi < 1`, not another
decimal residual absorption constant.

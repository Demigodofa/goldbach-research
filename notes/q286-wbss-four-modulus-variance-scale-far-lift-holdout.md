# q286-WBSS Four-Modulus Variance-Scale Far-Lift Holdout

Status: finite diagnostic. This is not an independence theorem,
fixed-modulus equidistribution theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

## Question

The first variance-scale audit showed the aggregate four-modulus signed load
was moderate on the `116` lifted rows inherited from the residual-absorption
falsifier. This receipt asks whether that finite behavior survives a changed
condition: the same stressed source residue classes, lifted to the next four
period positions after the previous holdout maximum.

## Receipt

```text
tools/build_q286_wbss_four_modulus_variance_scale_far_lift_holdout.py
evidence/q286-wbss-four-modulus-variance-scale-far-lift-holdout.json
```

The source residue denominator remains the `29` positive-pushback residue
classes from the `230`-row dual-edge population. Only the target values are
fresh.

## Result

```text
far lifted rows checked:                    116
target range:                           996208..1035742
direct witness positive rows:               116 / 116
positive local variance-scale rows:         116 / 116
minimum full action:             0.5992532517007266
maximum lambda_phi:              0.29444884696113977
maximum adverse iid-scale z-score: 3.5107558040930176
largest adverse z target:                1002478
tightest positivity target:              1001554
maximum formula reconstruction error: 4.11e-15
```

The direct witness still survives this farther targeted holdout. However, the
earlier finite observation that adverse iid-scale z stayed below `3` does not
survive: target `1002478` has aggregate signed error
`-0.2542394844196001`, local main `0.8634419426106758`, and adverse z-score
`3.5107558040930176`.

## Decision

Preserve the variance-scale route only in its weaker, theorem-shaped form:
seek a source-backed signed concentration or equidistribution estimate strong
enough to keep the aggregate error below the local main term. Do not promote a
fixed adverse `z < 3` cap. Residual absorption constants still fit finite data
only; the universal bound is open, and Goldbach is not proved.

# q286-WBSS Four-Modulus Variance-Scale Audit

Status: finite diagnostic. This is not an independence theorem,
fixed-modulus equidistribution theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

## Question

The residual absorption constants fit finite data only, and the universal
bound is open. After the direct witness survived the lifted holdout through
the aggregate four-modulus formula,

```text
A(N) = M(N) + E_70(N) + E_130(N) + E_154(N) + E_286(N),
```

the next useful question is whether the signed aggregate error is naturally
variance-sized. This receipt normalizes the aggregate error by the local
uniform variance of the same explicit coefficient function and the actual
strict-central prime-pair count.

## Receipt

```text
tools/build_q286_wbss_four_modulus_variance_scale_audit.py
evidence/q286-wbss-four-modulus-variance-scale-audit.json
```

The denominator is the same `116` lifted rows used by the direct witness and
four-modulus decomposition receipts.

## Result

```text
lifted rows checked:                         116
direct witness positive rows:                116 / 116
positive local variance-scale rows:          116 / 116
minimum local coefficient standard deviation: 3.30655315466526
maximum adverse iid-scale z-score:             2.696050693399999
largest adverse z target:                 992374
tightest positivity target:               965362
tightest row iid-scale z-score:              -2.318536356607163
maximum absolute iid-scale z-score:            3.448614443301592
```

The largest adverse variance-scaled row is not the tightest positivity row.
Target `992374` has aggregate signed error `-0.22179938574571406`, local main
`1.0679535327667407`, and adverse z-score `2.696050693399999`. The tightest
row `965362` has aggregate signed error `-0.18260126305241958`, local main
`0.8566735950666425`, and z-score `-2.318536356607163`.

## Decision

This preserves a sharper theorem-shaped target than residual absorption:
prove a source-backed fixed-modulus signed concentration or equidistribution
estimate for the explicit four-modulus coefficient function. The finite
holdout says the aggregate signed load is variance-sized on these rows; it
does not prove independence, equidistribution, a universal lambda bound, or
Goldbach.

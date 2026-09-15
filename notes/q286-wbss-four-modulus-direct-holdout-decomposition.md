# q286-WBSS Four-Modulus Direct-Holdout Decomposition

Status: finite diagnostic. This is not a binary-prime projection theorem,
signed discrepancy theorem, q286 threshold theorem, strict-central Goldbach
theorem, or Goldbach proof.

## Question

The direct q286-WBSS witness stayed positive on the targeted residue-lift
holdout, even though the top-20 Fourier plus residual absorption split lost
pointwise sign stability. This receipt asks how that surviving direct witness
looks through the existing four-modulus projection formula:

```text
A(N) = M(N) + E_70(N) + E_130(N) + E_154(N) + E_286(N)
```

where `M(N)` is the local-uniform main term and `E_d(N)` is the signed
weighted projected-residue error at modulus `d`.

## Receipt

```text
tools/build_q286_wbss_four_modulus_direct_holdout_decomposition.py
evidence/q286-wbss-four-modulus-direct-holdout-decomposition.json
```

The denominator is unchanged from the direct-witness lift holdout: `116`
lifted rows obtained from the `29` source residue classes with positive
residual pushback in the `230`-row dual-edge population.

## Result

```text
lifted rows checked:                         116
raw q286-WBSS positive rows:                 116 / 116
raw q286-WBSS nonpositive rows:                0 / 116
top-20 nonnegative rows from failed split:     70 / 116
top-20 nonnegative but raw-positive rows:      70 / 116
minimum local-uniform main term: 0.717245423802844
minimum raw full action:        0.674072332014222
mean raw full action:           0.916312249457876
maximum lambda_phi:             0.213151501463302
tightest row:                                965362
maximum reconstruction error:      4.33e-15
```

At the tightest row `965362`, the decomposition is:

```text
local main:          0.856673595066643
total signed error: -0.182601263052420
full action:         0.674072332014222
lambda_phi:          0.213151501463302
E_70:                0.004300161683148
E_130:              -0.000904295642486
E_154:              -0.059755521954175
E_286:              -0.126241607138907
```

Every modulus has mixed signed behavior across the holdout. Removing any one
modulus leaves all `116` rows positive, and local main plus any single modulus
term is also positive on all `116` rows. Thus this receipt does not promote a
single-modulus rescue story.

## Decision

The surviving object is the aggregate signed load, not pointwise top-20
Fourier sign stability and not a one-modulus rescue. The theorem target should
be stated as direct coefficient-aligned anti-alignment:

```text
E_70(N) + E_130(N) + E_154(N) + E_286(N) > -M(N)
```

or equivalently `lambda_phi(N) < 1`, with a source-backed fixed-modulus
binary-prime correlation estimate strong enough to imply it. The observed
maximum load `0.213151501463302` is finite holdout evidence only; no universal
bound is proved.

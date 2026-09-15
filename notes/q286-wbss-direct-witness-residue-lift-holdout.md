# q286-WBSS Direct-Witness Residue-Lift Holdout

Status: finite targeted diagnostic. This is not a q286-WBSS theorem, signed
projection theorem, q286 threshold theorem, strict-central Goldbach theorem,
or Goldbach proof.

## Question

The prior residue-lift holdout demoted the top-20 Fourier plus five-group
residual absorption split: the top-20 component lost its required negative sign
on many fresh lifted rows, and the fitted `.126`/`.13` residual caps failed.

This receipt asks a different question on the exact same lifted denominator:
does the unsplit raw q286-WBSS signed witness still have positive full action?

## Receipt

```text
tools/build_q286_wbss_direct_witness_residue_lift_holdout.py
evidence/q286-wbss-direct-witness-residue-lift-holdout.json
```

The receipt regenerates the `116` lifted targets from the previous holdout:
the `29` source residue classes with positive residual pushback in the
`230`-row dual-edge population, lifted through the next four period shifts.
It recomputes actual strict-central binary-prime orbit mass, evaluates the
full q286-WBSS coefficient directly, and checks reconstruction against the
optimized q286 row verifier.

## Result

```text
lifted rows checked:                         116
raw q286-WBSS positive rows:                 116 / 116
raw q286-WBSS nonpositive rows:                0 / 116
top-20 nonnegative rows from split:            70 / 116
top-20 nonnegative but raw-positive rows:       70 / 116
minimum raw full action:        0.674072332014227
mean raw full action:           0.916312249457879
maximum lambda_phi:             0.213151501463301
tightest row:                                965362
maximum full reconstruction error:       < 1e-12
maximum first-three reconstruction error: < 1e-12
```

## Decision

The split failed, but the raw witness did not fail on this targeted fresh
holdout. Every row where the top-20 decomposition lost sign still has positive
unsplit q286-WBSS full action.

Therefore the finite evidence now separates two claims:

- Demoted: pointwise top-20 negative drag plus residual absorption constant.
- Still alive: direct coefficient-aligned q286-WBSS signed witness.

The next theorem target should avoid pointwise top-20 sign stability and focus
on direct signed anti-alignment, an aggregate projection inequality, or a
source-backed fixed-modulus binary-prime correlation theorem. The universal
bound remains open, and Goldbach is not proved.

# q286-WBSS Residual Absorption Residue-Lift Holdout

Status: finite targeted holdout. Goldbach is not proved.

Receipt:

```text
tools/build_q286_wbss_residual_absorption_residue_lift_holdout.py
evidence/q286-wbss-residual-absorption-residue-lift-holdout.json
```

## Question

The full dual-edge population audit showed that `.126` and `.13` fit all `230`
available lower-face dual-edge rows. This holdout asks whether those fits
survive fresh target values when the source residues are chosen adversarially:
take the unique residue classes that had positive residual pushback in the
dual-edge population, then test their next four period-lifts beyond the old
maximum target.

The coefficient geometry is unchanged modulo `10010`; the strict-central
binary-prime orbit measures are recomputed at fresh targets.

## Result

The holdout tests `116` lifted rows:

```text
source dual-edge rows:                         230
source positive-pushback rows:                  29
fresh lifts per source residue:                  4
fresh lifted targets tested:                   116
target range:                              955902..995618
positive pushback rows:                         69 / 116
top-20 nonnegative rows:                        70 / 116
```

The top-20 Fourier component therefore loses its required negative sign on
most of the targeted lifted rows. This defeats the first condition in the
top-20 plus residual-absorption theorem skeleton before decimal constants
matter.

Even on rows where the top-20 component remains negative, the positive
pushback ratio is no longer small:

```text
maximum positive pushback/top20-drag ratio: 3.69343889977089
worst target:                               971524
worst target residue:                          554
worst target mod 286:                          268
source positive target:                      10564
source ratio:                    0.1187884461709314
```

Thus:

```text
theta = 1/8 = 0.125   fails on the fresh residue-lift holdout
theta = 0.126         fails on the fresh residue-lift holdout
theta = 0.13          fails on the fresh residue-lift holdout
```

## Decision

Demote the top-20 Fourier plus five-group residual absorption split as a
portable theorem skeleton. It remains a useful diagnostic for the original
dual-edge population, but its sign-stability and small residual-ratio behavior
do not survive targeted fresh residue lifts.

The next theorem route should switch to a direct raw q286-WBSS signed-witness
estimate or a different aggregate inequality that does not require the top-20
Fourier component to stay pointwise negative.

## Boundary

This holdout is finite and targeted, not an unbiased sample or asymptotic
estimate. It proves no residual absorption theorem, no signed projection
theorem, no q286 threshold theorem, no strict-central Goldbach theorem, and no
Goldbach proof. It only blocks this unchanged top-20/residual absorption route
outside the original dual-edge fixture.

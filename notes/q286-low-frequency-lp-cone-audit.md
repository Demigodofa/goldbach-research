# q286 low-frequency LP cone audit

Status: finite linear-programming cone diagnostic.  This is not a proof of
Goldbach, an LP theorem, a low-frequency theorem, a rank-`1` theorem, or a
residual-drag theorem.

## Purpose

Kevin asked whether linear programming should be used.  The useful version is
not "solve Goldbach by LP."  It is:

```text
Can the surviving low-frequency DFT/character-label basis supply a bounded
finite cone certificate for the residual-drag cap?
```

The generated evidence is:

```text
evidence/q286-low-frequency-lp-cone-audit.json
```

The builder is:

```text
tools/build_q286_low_frequency_lp_cone_audit.py
```

## Method

Use the same `13` low-frequency real Fourier features on the `C10 x C12`
outside-channel label lattice as `full_low_frequency_lift`:

```text
constant,
cos/sin a, cos/sin 2a,
cos/sin b, cos/sin 2b,
cos/sin(a+b), cos/sin(a-b)
```

The LP fixes the total effective vector scale to the frozen low-frequency
replay scale and bounds coefficient `L1` size by a predeclared ladder of
multiples of the original frozen-vector coefficient `L1`:

```text
1.0, 1.5, 2.0, 4.0, 8.0
```

For each original training clear row, it maximizes the common slack in:

```text
reconstructed_delta >= slack
reconstructed_delta <= 4 * exact_outside_delta - slack
```

The second inequality is the `0.75` residual-drag cap written without the
piecewise drag expression, assuming reconstructed delta is positive.  The
selected vector is then frozen and replayed on the prior heldout denominator
and the farther horizon denominator.

## Result

The LP is feasible already at the base `L1` multiplier `1.0`; larger
multipliers return the same optimum.  The selected vector has:

```text
training minimum slack:        0.0796483772796952
coefficient L1:                3.5698104293761475
cosine to rank-1 vector:       0.6019078700529527
cosine to low-frequency vector 0.7230387005616671
```

It survives the training and both heldout denominators:

```text
training cap failures: 0
heldout cap failures:  0
horizon cap failures:  0

training nonpositive deltas: 0
heldout nonpositive deltas:  0
horizon nonpositive deltas:  0
```

Worst residual-drag ratios:

```text
training: 0.5000000000000002 at 1242118
heldout:  0.33946759079383754 at 1282186
horizon:  0.42590751493414414 at 1426262
```

This is a substantial finite improvement over the frozen low-frequency replay
for the cap problem, especially on the tight horizon row `1426262`.

## Interpretation

The LP did **not** explain the Octave rank-`1` direction.  Its cosine to the
rank-`1` vector is only about `0.602`, while the earlier static low-frequency
projection was about `0.832`.  The LP has instead found a different
low-frequency vector that is better for the residual-drag cap inequality.

That splits the route cleanly:

```text
rank-1 explanation problem: still open
residual-drag cap certificate problem: finite LP candidate survives
```

The DFT connection is real: this is a small Fourier-band certificate on the
`C10 x C12` channel-label torus.  The closed-graph/box-principle intuition is
only theorem-shaping at this stage: a future proof would need to replace the
finite LP by a bounded linear-functional or finite-cone argument on actual
admissible prime-pair residue measures.

Riesz-Thorin interpolation is a useful next analogy for that future proof
target.  The current q286 evidence has endpoint flavors: crude `L1` or
triangle estimates are rigorous but too weak, while `L2`/SVD/Fourier structure
is strong on the measured rows but not pointwise enough.  A real theorem would
need to define the operator from admissible residue-weight measures to the
outside-channel residual action, prove two endpoint bounds from arithmetic,
and interpolate to the norm that controls the residual-drag cap.  The LP
certificate is only the finite-dimensional shadow of that possible route.

## Boundary

This is an optimization certificate on checked finite denominators only.  It
does not prove a uniform cone theorem, does not identify the rank-`1` vector
arithmetically, does not prove a pointwise signed prime-correlation estimate,
and does not prove Goldbach.

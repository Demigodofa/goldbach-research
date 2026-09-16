# Mobius moment-square degree-5 adjacent-scale dominance stress

## Question

The checked-scale dominance audit showed that the degree-`5` active/full
dominance pattern survives the six moment-square scales
`127,149,167,191,211,227`.  Does the pattern survive the next adjacent prime
scale modulus `229`, or does the first step beyond the checked fixture produce
a finite falsifier?

## Mechanism

At scale `M=229`, rebuild every prime row in `[229,458]`, compute the
degree-`5` component entries `(00,12)`, `(01,02)`, `(01,11)`, and their
degree-`5` total, then test

```text
active / full > 1/2
```

for each signed row.  A single row at or below `1/2` would be a concrete
finite falsifier for this adjacent-scale extension.

## Receipt

```text
tools/build_mobius_moment_square_degree5_forward_scale_dominance_stress.py
evidence/mobius-moment-square-degree5-adjacent-scale-dominance-stress.json
```

## Result

```text
status: STRESS_degree5_forward_scale_primewise_dominance
scale:                                      M=229
prime count:                                39
component rows:                             117
degree-5 total rows:                        39
dominance rows:                             156
dominance slacks:                           positive 156, zero 0, negative 0
failure rows:                               0
```

Weakest adjacent-scale row:

```text
scale:                                      M=229
prime:                                      379
label:                                      (00,12)
active/full ratio:                          0.9018909662403138
slack above 1/2:                            0.40189096624031384
```

## Decision

The adjacent-scale stress pass survives.  The first prime scale modulus after
the six checked moment-square scales has no component or degree-`5` total row
at or below the signed `1/2` threshold.

This is a useful falsifier miss, not a theorem.  It extends the finite evidence
one scale beyond the Sturm fixture and suggests the next meaningful route is
to derive a symbolic one-prime dominance lemma, or deliberately search for a
parameter transition where the dominance fails.

This is finite adjacent-scale dominance evidence only.  No adjacent-scale
dominance theorem, checked-scale dominance theorem, primewise dominance
theorem, degree-`5` coefficient theorem, robust-margin universal theorem,
coefficient-family theorem, universal Sturm certificate, half-frame
curve-positivity theorem, uniform active/full lower-frame theorem, Mobius
covariance theorem, signed prime-correlation theorem, q286 theorem, or
Goldbach proof is established.

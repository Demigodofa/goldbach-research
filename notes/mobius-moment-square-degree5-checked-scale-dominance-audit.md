# Mobius moment-square degree-5 checked-scale dominance audit

## Question

The weak `M=167` block showed primewise degree-`5` active/full dominance
above the signed `1/2` threshold.  Does that local dominance pattern survive
across all six checked moment-square scales, or does one checked scale falsify
the extension?

## Mechanism

For every prime in each checked scale

```text
127, 149, 167, 191, 211, 227
```

rebuild the lifted endpoint frame and compute the active/full dominance slack

```text
active_over_full - 1/2
```

for the three degree-`5` component entries `(00,12)`, `(01,02)`, `(01,11)`,
and for their degree-`5` total.

## Receipt

```text
tools/build_mobius_moment_square_degree5_checked_scale_dominance_audit.py
evidence/mobius-moment-square-degree5-checked-scale-dominance-audit.json
```

## Result

```text
status: CHECK_degree5_checked_scale_primewise_dominance
scales:                                      127, 149, 167, 191, 211, 227
total primes checked:                        189
component rows:                              567
degree-5 total rows:                         189
dominance rows:                              756
component dominance slacks:                  positive 567, zero 0, negative 0
degree-5 total dominance slacks:             positive 189, zero 0, negative 0
all dominance slacks:                        positive 756, zero 0, negative 0
```

Global weakest row:

```text
scale:                                      M=167
prime:                                      181
label:                                      (00,12)
active/full ratio:                          0.5563677490893767
slack above 1/2:                            0.056367749089376695
```

Scale-wise weakest slacks:

```text
M=127: 0.20758734929764133
M=149: 0.1905059738826077
M=167: 0.056367749089376695
M=191: 0.3396056234839627
M=211: 0.3211806699762235
M=227: 0.3429887125059675
```

## Decision

The checked-scale extension survives.  Every checked degree-`5` component and
total row across the six scales has active/full dominance slack above `1/2`.
The global weakest row remains the already identified weak-block component
`M=167`, prime `181`, `(00,12)`.

This strengthens the theorem-shaped target from a one-block diagnostic to a
six-scale finite fixture: prove a local one-prime active/full dominance lemma
for the three degree-`5` components, or find a scale/parameter regime where
that dominance breaks.

This is finite checked-scale dominance evidence only.  No checked-scale
dominance theorem, primewise dominance theorem, degree-`5` coefficient
theorem, robust-margin universal theorem, coefficient-family theorem,
universal Sturm certificate, half-frame curve-positivity theorem, uniform
active/full lower-frame theorem, Mobius covariance theorem, signed
prime-correlation theorem, q286 theorem, or Goldbach proof is established.

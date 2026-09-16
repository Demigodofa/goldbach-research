# Mobius moment-square degree-5 Q46189 exact log-polynomial identity audit

## Question

Do the six source-conductor scalar formulas become exactly identical
after rebuilding the coefficient polynomials over formal prime-log
variables?

## Mechanism

The previous checkpoint used floating coefficients.  This audit
rebuilds those coefficients over formal symbols `l2`, `l3`, ...
for prime logarithms.  After removing the common `L^-3` factor, it
checks whether

```text
(b_d c_e + c_d b_e) / (a_d a_e)
```

is exactly identical across the six ordered source pairs.

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_exact_log_polynomial_identity_audit.py
evidence/mobius-moment-square-degree5-q46189-exact-log-polynomial-identity-audit.json
```

## Result

```text
Q=46189 common numerator:     -l11*l13*l17 - l11*l13*l19 - l11*l17*l19 - l13*l17*l19
replacement rows:             10
max numeric substitution err: 2.7755575615628914e-17
all pair differences zero:    true
```

For `Q=46189`, the common numerator is

```text
-l11*l13*l17 - l11*l13*l19 - l11*l17*l19 - l13*l17*l19
```

So the common scalar is that numerator divided by `L^3`.

## Decision

The finite source-conductor scalar formula is no longer merely a
floating coincidence for this selected family: the six pair formulas
are exactly equal as formal log-polynomials.  The remaining gap is the
one-coordinate active/full ratio inequality and any universal
extension beyond the checked family.

This proves only a selected-family exact log-polynomial identity.  It
proves no universal source-conductor scalar formula theorem,
one-coordinate active/full ratio theorem, symbolic replacement ratio
theorem, source-start theorem, strict-central Goldbach theorem, or
Goldbach proof.

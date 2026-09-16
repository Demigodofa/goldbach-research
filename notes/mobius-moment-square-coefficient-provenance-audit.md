# Mobius moment-square coefficient provenance audit

## Question

The Sturm certificate proves positivity for the recorded rationalized
half-frame polynomials.  Which active/full Gram entries create those
coefficients, and is their structure stable enough to suggest a real
coefficient-family theorem?

## Receipt

```text
tools/build_mobius_moment_square_coefficient_provenance_audit.py
evidence/mobius-moment-square-coefficient-provenance-audit.json
```

## Mechanism

For the moment-square coordinate vector

```text
y(t) = (t^4,t^3,t^2,t^2,t,1)
```

use coordinate labels

```text
00, 01, 02, 11, 12, 22
```

with degrees

```text
4, 3, 2, 2, 1, 0.
```

For each checked scale, recompute the aggregate active and full Gram matrices,
form `H = active - 0.5*full`, and decompose each coefficient of

```text
P_M(t) = y(t)^T H y(t)
```

as the sum of all unordered Gram-entry contributions whose coordinate degrees
add to the polynomial degree.  Then compare the reconstructed coefficients
against `evidence/mobius-moment-square-half-frame-curve-audit.json`.

## Result

```text
status: TARGET_moment_square_coefficient_provenance
checked scales:                                  127, 149, 167, 191, 211, 227
all reconstructed coefficients match source:     true
maximum relative source coefficient delta:       1.7413985025615276e-16
all alternating degree sign patterns hold:       true
stable top contributor signature:                true
```

The stable dominant Gram-entry signature by polynomial degree is:

```text
degree 0 -> 22,22
degree 1 -> 12,22
degree 2 -> 12,12
degree 3 -> 11,12
degree 4 -> 01,12
degree 5 -> 01,11
degree 6 -> 01,01
degree 7 -> 00,01
degree 8 -> 00,00
```

The coefficient signs alternate on every checked scale:

```text
+ - + - + - + - +
```

from degree `0` through degree `8`.

## Decision

The checked half-frame polynomial coefficients are not opaque optimizer
artifacts.  They are exactly reproduced by degree-wise sums of
`active - 0.5*full` Gram entries, and the sign/top-contributor pattern is
stable across the checked scales.

This does not prove positivity universally.  It identifies the next theorem
target: derive the active/full Gram-entry coefficient family and prove that it
retains the stable alternating sign and Sturm/sign certificate, or find a
legitimate scale where the coefficient provenance pattern fails.

This is finite coefficient-provenance evidence only.  No coefficient-family
theorem, universal Sturm-certificate theorem, half-frame curve-positivity
theorem, uniform active/full lower-frame theorem, Mobius covariance theorem,
signed prime-correlation estimate, q286 theorem, strict-central Goldbach
theorem, or Goldbach proof is established.

# Mobius moment-square degree-5 Q46189 group-payment audit

## Question

For the `M=229`, `p=379`, `Q=46189` adverse denominator, do
structured middle/far positive rows sharing three of the four high
primes `11,13,17,19` pay the defect without using total positivity?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_group_payment_audit.py
evidence/mobius-moment-square-degree5-q46189-group-payment-audit.json
```

## Result

```text
Q=46189 adverse margin:        8444721229.472412
replacement rows:              10
replacement positive sum:       14694916931621.637
replacement payment / defect:   1740.1304948156007
minimum row payment / defect:   36.74165224066973
```

Omitted-high-prime family payment ratios:

```text
missing 11: 653.9359290761917
missing 13: 466.9478641031054
missing 17: 320.0147481014071
missing 19: 299.23195353489666
```

## Decision

The finite payment pattern is sharper than generic group payment:
three-of-four high-prime replacement families pay the `Q=46189`
defect.  This narrows the possible theorem target to replacement-family
phase-defect payment.

This is still finite ledger evidence only.  It proves no replacement
family payment theorem, phase-defect payment theorem, near-adverse
upper bound, middle/far lower bound, clearance-family theorem,
source-start theorem, strict-central Goldbach theorem, or Goldbach
proof.

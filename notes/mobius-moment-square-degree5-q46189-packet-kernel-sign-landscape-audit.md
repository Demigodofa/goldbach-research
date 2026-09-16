# Mobius moment-square degree-5 Q46189 packet-kernel sign landscape audit

## Question

Across the `Q=46189` same-source packet landscape, is the sign of
the coordinate-00 active/full half-margin explained by whether
off-diagonal Dirichlet-kernel mass overpays the diagonal half?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_packet_kernel_sign_landscape_audit.py
evidence/mobius-moment-square-degree5-q46189-packet-kernel-sign-landscape-audit.json
```

## Identity

```text
ratio_minus_half = 0.5 * (1 + off_diagonal_total / diagonal_half)
below half <=> off_diagonal_total / diagonal_half <= -1
```

## Result

```text
same-source denominators:                    35
below-half denominators:                      [46189]
off-diagonal overpayment count:               1
nonadverse overpayment count:                 0
Q=46189 off/diagonal-half:                    -1.0053819255304557
minimum nonadverse off/diagonal-half:         -0.8472931845861708
minimum nonadverse off/diagonal denominator:  38038
minimum nonadverse ratio-minus-half:          0.07635340770691464
```

Tight rows:

```text
Q=46189: off/diag_half=-1.0053819255304557, ratio_minus_half=-0.002690962765227888
q=38038: off/diag_half=-0.8472931845861708, ratio_minus_half=0.07635340770691464
```

## Decision

`Q=46189` is the only checked row where off-diagonal
Dirichlet-kernel mass overpays the diagonal half.  Every nonadverse
packet keeps `off_diagonal_total / diagonal_half > -1`; the tight
survivor is still `q=38038` at about `-0.847293`.

This is a cleaner theorem-shaped target than `50A..60A`: prove an
off-diagonal-overpayment exclusion bound for source-admissible
replacement packets.  This remains finite diagnostic evidence only.
It proves no coordinate-00 residue-gap sign theorem, active/full ratio
theorem, packet-landscape theorem, strict-central Goldbach theorem, or
Goldbach proof.

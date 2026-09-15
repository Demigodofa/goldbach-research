# q286 orthogonal residual norm certificate

Status: coefficient-sensitive norm diagnostic and demotion.  This is not an
orthogonal residual bound, signed pair-correlation theorem, q286 threshold
theorem, or Goldbach proof.

## Question

The orthogonal-rescue decomposition reduced q286 closure to:

```text
full = aligned_only + <nu_N,h_a>.
```

Could a simple coefficient-sensitive norm bound on the centered measure
`nu_N` prevent the orthogonal residual from erasing the positive aligned-only
margin?

Executable receipt:

```text
tools/build_q286_orthogonal_residual_norm_certificate.py
evidence/q286-orthogonal-residual-norm-certificate.json
```

## Certificate

Use the uniform-weighted reflection-orbit inner product.  By Cauchy-Schwarz:

```text
|<nu,h_a>| <= ||nu||_{u^-1} ||h_a||_u.
```

Therefore, if:

```text
aligned_only > 0
||nu||_{u^-1} < aligned_only / ||h_a||_u
```

then the residual cannot overturn the aligned-only full-action margin, and
`full > 0`.

This is a valid sufficient certificate.  The question is whether it is strong
enough to describe the actual rows.

## Evidence

On the seven frozen selected targets:

```text
certified targets: 0 / 7
actual full-positive targets: 5 / 7
actual full-positive but not norm-certified:
  94856
  1222142
  1240888
  1242118
  1379072
```

Norm scales:

```text
actual chi-square norm ||nu||_{u^-1}:
  minimum 0.6060646213177469
  mean    1.7875547691729226
  maximum 4.335942226316056

required certificate radius:
  minimum 0.026560344128917553
  mean    0.21750301514906625
  maximum 0.3787851289964279

actual / required ratio:
  minimum 1.6660773272322653
  mean    32.19998822008032
  maximum 144.83391860419633
```

The closest measured miss is `1222142`, whose actual norm is still about
`1.666` times the sufficient radius:

```text
target 1222142:
  chi-square norm 0.6310853153136975
  required radius 0.3787851289964279
  full/P          0.9457162662139126
```

The boundary failures miss by much larger factors:

```text
14138 ratio 40.815797563573966
14996 ratio 144.83391860419633
```

## Decision

The norm certificate is mathematically valid but too blunt as the main proof
route.  It asks for total chi-square control of the whole centered residue
measure, while the actual successful rows survive by signed residual landing,
not by small global norm.

This demotes an unchanged Cauchy/chi-square cone in the same way the earlier
L1 cone was demoted:

```text
global norm control is sufficient, but not the observed mechanism.
```

## Surviving theorem target

The next live target is a signed lower-tail theorem for the residual statistic
itself:

```text
<nu_N,h_a> > -aligned_only(N)
```

The proof should now look for one of:

- a sign/landing decomposition of `h_a`;
- a residual-specific mass/landing inequality;
- an explicit formula estimate for this one character combination;
- a large-sieve-style bound that controls the signed residual statistic, not
  total norm;
- a finite boundary split plus eventual signed lower-tail bound.

## Falsifier for future cones

Any proposed residual cone is falsified if it certifies fewer actual
full-positive rows than the direct residual inequality, or if LP produces a
reflected nonnegative synthetic measure satisfying the cone while:

```text
<nu,h_a> <= -aligned_only.
```

Do not retry generic L1, chi-square, or variance cones unless the changed
condition is a theorem that controls this specific residual functional.

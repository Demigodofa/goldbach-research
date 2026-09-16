# Mobius moment-square degree-5 Q46189 far-band slice balance audit

## Question

Inside the far band `10A..100A`, do smaller `A`-scaled distance
slices already separate `Q=46189` from every source-admissible
replacement row?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_far_band_slice_balance_audit.py
evidence/mobius-moment-square-degree5-q46189-far-band-slice-balance-audit.json
```

## Result

```text
slices separating by share and total: 50A_to_60A, 80A_to_90A
best slice:                          50A_to_60A
best distance range:                 [2151, 2580]
Q positive share in best slice:      0.3704750044709434
min replacement positive share:      0.41193052224841337
positive-share gap:                  0.041455517777469975
Q total / diag in best slice:        -0.08597078804878477
min replacement total / diag:        -0.019836945709586308
total gap:                           0.06613384233919847
```

## Decision

The far-band signed-balance separator has local witnesses.  The
`50A..60A` slice separates by both positive share and total pressure
with the largest positive-share gap; `80A..90A` also separates.
Several other slices fail, so the statement is not a uniform
all-slice phenomenon.

The next theorem-shaped target is a `50A..60A` signed-balance
witness, with `80A..90A` preserved as a robustness check.  This is
finite selected-family diagnostic evidence only.  It proves no
distance-slice positive-share theorem, distance-slice pressure
theorem, far-band theorem, replacement residue-gap bound theorem,
coordinate-00 residue-gap sign theorem, strict-central Goldbach
theorem, or Goldbach proof.

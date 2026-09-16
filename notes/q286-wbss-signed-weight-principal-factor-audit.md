# q286-WBSS signed-weight principal-factor audit

## Question

Does the q286 signed-weight major-arc local factor give an independent raw
positive term, or does it factor through the ordinary strict-central pair mass
`T_N`?

## Receipt

```text
tools/build_q286_wbss_signed_weight_principal_factor_audit.py
evidence/q286-wbss-signed-weight-principal-factor-audit.json
```

## Result

```text
status:                               HOLD_signed_weight_principal_factor_TN_dependent
even target residues:                 5005
positive principal factors:           5005 / 5005
nonpositive principal factors:           0 / 5005
M(a) minimum:                         0.6039353780830684
M(a) mean:                            1.0
M(a) maximum:                         1.5716524655081634
independent principal surplus found:  false
rows with negative admissible weight: 5005
rows with pointwise positive floor:      0
```

The extreme rows are:

```text
minimum M(a):              residue 4124, target mod 286 = 120
maximum M(a):              residue 8856, target mod 286 = 276
largest negative fraction: residue 1146
tightest shape margin:     residue 3144
```

## Decision

The local q286 principal factor is positive for every even target residue.
That is useful, but it is not a new source of strict-central support.  The
principal term has shape

```text
Principal_q286(N) = T_N * M(a).
```

So if `T_N=0`, the q286 principal term is also zero.  Local-factor positivity
alone cannot cross the zero-mass barrier.

The route survives only if a raw pointwise analytic estimate is proved for
the signed weighted binary-prime sum itself, such as `W_phi(N)>0` or
`adverse_drag_raw(N)<local_main_raw(N)`, for every sufficiently large covered
target, plus a finite remainder.  If a proof first proves or assumes `T_N>0`
and then uses q286 only as normalized signed-shape control, q286 has collapsed
to conditional decoration after a Goldbach-strength positive-mass input.

This proves no signed-weight major/minor arc estimate, no raw weighted witness
theorem, no signed negative-region distribution theorem, no positive-mass
theorem, no q286 threshold theorem, no strict-central Goldbach theorem, and no
Goldbach proof.

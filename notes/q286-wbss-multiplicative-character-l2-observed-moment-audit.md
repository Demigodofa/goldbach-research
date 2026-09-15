# q286-WBSS multiplicative character L2 observed-moment audit

## Question

The aggregate character `L2` payment audit produced a sharper theorem target.
Do the existing checked rows satisfy that aggregate `L2` cap, and are any
failures caused by zero strict-central mass?

## Mechanism

For each checked row, compute the actual-minus-local-uniform projected residue
distribution for moduli `70`, `130`, `154`, and `286`, transform it into the
same active multiplicative-character coordinates as the coefficient audit, and
measure

```text
sqrt(sum_d ||D_d(N)||_2^2).
```

Compare it both to the global minimum-local-main cap and to the row-local cap:

```text
row_local_l2_cap = LocalMain(N) / sqrt(sum_d ||c_hat_d||_2^2).
```

## Result

```text
checked rows:                         348
zero strict-central pair rows:          0
zero actual-mass rows:                  0
nonunit actual-mass rows:               0
nonunit uniform-mass rows:              0
rows exceeding global minimum cap:    301
rows exceeding row-local cap:         120
largest target exceeding row-local cap: 1155862
```

Worst row-local ratio:

```text
target:                         1089544
observed aggregate L2:   0.20982859176041493
row-local L2 cap:        0.13475610600578378
ratio:                   1.5570989543984672
```

## Decision

The zero-mass check passes: the finite cap failures are not caused by missing
strict-central mass or bad normalization.  But the checked population falsifies
any claim that the aggregate `L2` cap already holds at this scale.

The aggregate `L2` theorem shape remains a useful asymptotic target only with
an explicit finite-boundary split, a threshold beyond the observed violations,
or a stronger structured signed moment theorem than plain aggregate `L2`.

This audit confirms coefficient arithmetic and finite obstruction only.  It
does not confirm a non-circular analytic bridge, aggregate character-moment
theorem, pointwise adverse-drag theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

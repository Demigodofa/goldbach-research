# q286-WBSS K_286 two-mode singular target

## Question

What exact two singular moment functionals replace generic `K_286` character
control?

## Identity

In principal-normalized coordinates, index the active coefficient matrix by
nontrivial mod-`11` character exponent `alpha=1..9` and nontrivial mod-`13`
character exponent `beta=1..11`.

Let

```text
delta_{alpha,beta}(N)=D^P_{alpha,beta}(N)/P0_a(N).
```

The coefficient matrix has exact SVD

```text
kappa_{alpha,beta}
  = sum_j sigma_j * u_j(alpha) * vh_j(beta),
```

so the normalized `K_286` functional is

```text
Re sum_{alpha,beta} kappa_{alpha,beta} delta_{alpha,beta}(N)
  = Re sum_j sigma_j * mu_j(N)
```

with

```text
mu_j(N)
  = sum_{alpha,beta} u_j(alpha) * vh_j(beta)
    * delta_{alpha,beta}(N).
```

## Pinned Values

```text
sigma_1:                         3.597046733129315
sigma_2:                         2.8233430589589674
top-two coefficient L2:          4.572746573875274
residual coefficient L2:         0.7164353938945424
total coefficient L2:            4.628530101718351
top-two energy fraction:         0.9760410444893588
```

Using the previous aggregate cap

```text
||delta||_2 <= 0.038004233097145394
```

the residual singular tail would cost at most

```text
0.02722757770861337
```

of the `0.1759037368828583` budget, leaving the sufficient two-mode floor

```text
Re(sigma_1*mu_1(N)+sigma_2*mu_2(N))
  >= -0.14867615917424493.
```

This split is sufficient, not necessary.

## Decision

`TARGET_k286_two_mode_singular_target_unproved`.

The next proof-shaped target is now exact: prove a one-sided lower bound for
the two singular moment functionals, plus a residual cap, instead of paying
all active `K_286` characters independently.

No twisted binary-prime moment estimate, `K_286` lower bound, major/minor arc
estimate, pointwise centered-error estimate, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof is established.

## Receipt

```text
tools/build_q286_wbss_k286_two_mode_singular_target.py
evidence/q286-wbss-k286-two-mode-singular-target.json
test_q286_wbss_k286_two_mode_singular_target.py
```

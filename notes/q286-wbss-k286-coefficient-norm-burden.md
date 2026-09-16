# q286-WBSS K_286 coefficient/norm burden

## Question

What exact coefficient burden must a raw analytic theorem pay for the dominant
`K_286` bucket?

## Result

The nominal `11x13` character space has `99` available nonprincipal characters.
The actual natural-modulus coefficient vector has only `50` nonzero entries
above tolerance.

In principal-normalized coordinates,

```text
kappa_chi = c_{a,chi}^{286} / principal_mean
delta_chi(N) = D_chi^P(N) / P0_a(N)
```

the target is

```text
Re sum_chi kappa_chi * delta_chi(N) >= -0.1759037368828583.
```

Pinned norms:

```text
available character count:          99
active nonzero character count:     50
principal-normalized L1:            32.42815568567079
principal-normalized L2:            4.628530101718351
principal-normalized Linf:          0.8166661291234342
```

Sufficient caps:

```text
uniform |delta_chi| cap:             0.00542441385158965
aggregate ||delta||_2 cap:           0.038004233097145394
```

These are sufficient theorem targets, not observed universal estimates.

## Structure

The `9 x 11` coefficient matrix has numerical rank `9`, but the first two
singular directions carry

```text
0.9760410444893588
```

of coefficient energy.  That gives a sharper next proof target: separate the
first two singular moment combinations from the residual seven directions
instead of treating the nominal `99` characters independently.

## Decision

`TARGET_k286_coefficient_norm_burden_unproved`.

The dominant bucket is now a precise coefficient/norm burden:

1. direct signed target:
   `Re sum_chi kappa_chi*delta_chi(N) >= -0.1759037368828583`;
2. strong uniform cap:
   `max_chi |delta_chi(N)| <= 0.00542441385158965`;
3. aggregate cap:
   `sqrt(sum_chi |delta_chi(N)|^2) <= 0.038004233097145394`;
4. sharper candidate:
   control the two leading singular moment directions plus a small residual.

No twisted binary-prime moment estimate, `K_286` lower bound, major/minor arc
estimate, pointwise centered-error estimate, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof is established.

## Receipt

```text
tools/build_q286_wbss_k286_coefficient_norm_burden.py
evidence/q286-wbss-k286-coefficient-norm-burden.json
test_q286_wbss_k286_coefficient_norm_burden.py
```

# Mobius moment-square degree-5 primewise sign audit

## Question

The weak `M=167` degree-`5` burden audit localized the coefficient loss to
three same-sign aggregate Gram entries: `(00,12)`, `(01,02)`, and `(01,11)`.
Is that aggregate adverse sign hiding cancellation among individual primes in
the block, or does each prime already push those entries in the adverse
direction?

## Mechanism

For each prime modulus `p` in `[167,334]`, rebuild its lifted endpoint frame
with the same weak-block parameters:

```text
row_count:     35
ell_freeze:    52
divisor range: 3..16
```

For each prime, compute the three degree-`5` half-frame contributions

```text
2 * (active[i,j] - (1/2) full[i,j])
```

for `(00,12)`, `(01,02)`, and `(01,11)`.

## Receipt

```text
tools/build_mobius_moment_square_degree5_primewise_sign_audit.py
evidence/mobius-moment-square-degree5-primewise-sign-audit.json
```

## Result

```text
status: CHECK_degree5_primewise_sign_localization
scale:                                      M=167
prime count:                                29
all prime degree-5 totals negative:         true
all prime component contributors negative:  true
degree-5 total sign counts:                 positive 0, zero 0, negative 29
```

Component sign counts:

```text
(00,12): positive 0, zero 0, negative 29
(01,02): positive 0, zero 0, negative 29
(01,11): positive 0, zero 0, negative 29
```

Component totals match the prior aggregate burden within ordinary float
summation tolerance:

```text
(00,12): -17833463267559.574
(01,02): -36071645892875.484
(01,11): -72179970258478.0
maximum delta from prior burden receipt: 0.015625
```

The least adverse prime row is `p=181`:

```text
degree-5 total: -163275425149.23624
```

The most adverse prime row is `p=241`:

```text
degree-5 total: -10722072932468.744
```

## Decision

The weak-block aggregate degree-`5` burden is not explained by cancellation
between favorable and adverse prime rows.  Every checked prime in the weak
block already has all three degree-`5` component contributions negative.

This sharpens the theorem-shaped route: before proving a full robust
`21/50` Sturm certificate, try to derive a local one-prime sign or dominance
lemma for the `(00,12)`, `(01,02)`, and `(01,11)` entries under the
weak-block parameter rules.

This is finite weak-block evidence only.  No primewise sign theorem,
degree-`5` coefficient theorem, robust-margin universal theorem,
coefficient-family theorem, universal Sturm certificate, half-frame
curve-positivity theorem, uniform active/full lower-frame theorem, Mobius
covariance theorem, signed prime-correlation theorem, q286 theorem, or
Goldbach proof is established.

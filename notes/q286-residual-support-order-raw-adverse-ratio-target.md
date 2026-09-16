# q286 residual support-order raw adverse-ratio target

## Question

The raw phase-space locator showed small finite values of

```text
D_high_minus_raw(N) / B_low_raw(N).
```

Can that be promoted into a cleaner theorem target?

## Receipt

```text
tools/build_q286_residual_support_order_raw_adverse_ratio_target.py
evidence/q286-residual-support-order-raw-adverse-ratio-target.json
```

## Theorem Shape

Let

```text
D_high_minus_raw(N) = max(0, -T_high_raw(N))
rho_raw(N) = D_high_minus_raw(N) / B_low_raw(N).
```

A sufficient theorem shape is:

```text
B_low_raw(N) > 0
rho_raw(N) <= rho_* < 1
```

for every sufficiently large eligible `N` in the named q286 support-order
period classes.  Then

```text
R_raw(N) = B_low_raw(N) * (1 - rho_raw(N)) > 0.
```

## Zero-Support Boundary

This is not a denominator shortcut.  If strict-central support is empty, all
raw prime-pair sums in this witness vanish.  Then `B_low_raw(N)=0`, and the
ratio is undefined rather than helpful.  A theorem proving `B_low_raw(N)>0`
is already support/existence-strength for this witness family.

So the ratio route is valid only together with an independent raw positive
low-order theorem, or as part of one direct raw lower-bound theorem.

## Finite Calibration

```text
checked rows:                         224
positive low-order rows:              224
nonpositive low-order targets:          0
zero adverse-drag rows:               124
nonzero adverse-drag rows:            100
ratio < 1 rows:                       224
ratio >= 1 targets:                     0
largest adverse-ratio target:      164926
largest adverse / low: 0.13266261119465184
ratio slack to 1:      0.8673373888053482
smallest low-order target:          24148
smallest raw low:       494408133.6057817
tightest raw-margin target:         44168
```

## Decision

`TARGET_raw_adverse_ratio_plus_positive_low_order`.

The finite adverse-ratio statistic is useful and theorem-shaped, but it does
not avoid the support problem by itself.  The clean route remains a direct
raw lower-bound theorem unless we can prove both a raw positive low-order lower
bound and a same-scale adverse-ratio upper bound without dividing by unproved
mass.

This proves no raw adverse-ratio theorem, positive low-order theorem, raw
lower-bound theorem, q286 threshold theorem, strict-central Goldbach theorem,
or Goldbach proof.

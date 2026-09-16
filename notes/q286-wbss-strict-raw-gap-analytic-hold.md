# q286-WBSS strict raw-gap analytic HOLD

## Question

Finite evidence is no longer an acceptance condition.  After the strict
raw-gap correction, what analytical estimate would actually prove the bridge?

## Bridge

The non-circular q286-WBSS target is

```text
G_raw(N) = L_raw(N) - A_raw_-(N) > 0.
```

Here

```text
L_raw(N) = T_N * M(a)
E_raw_d(N) = T_N * E_d(N)
A_raw_-(N) = sum_d max(0, -E_raw_d(N)).
```

If strict-central support is empty, then `T_N=0`, `L_raw(N)=0`, every
`E_raw_d(N)=0`, and `G_raw(N)=0`.  So the proof has to create a strict positive
raw quantity.  A homogeneous or normalized estimate that remains true at zero
mass is not enough.

## Receipt

```text
tools/build_q286_wbss_strict_raw_gap_analytic_hold.py
evidence/q286-wbss-strict-raw-gap-analytic-hold.json
```

## Sufficient Analytic Routes

Direct signed binary-pair sum:

```text
W_phi(N)>0
```

or the stronger

```text
G_raw(N)>=eta(N)>0
```

for every sufficiently large covered even `N`.  This is non-circular because
the raw sum is zero on a zero-support row.

Mass plus one-sided projection control:

```text
T_N >= P(N) > 0
max(0, -E_raw_d(N)) <= B_d(N)
sum_d B_d(N) < M(a) * P(N)
```

This also proves `G_raw(N)>0`, but the positive mass input is already
strict-central existence strength.

Normalized projection discrepancy can only be used after an independent
positive-mass theorem.  It does not cross the zero-mass barrier by itself.

## Inherited Coefficient Budget

From the four-modulus coefficient budget:

```text
moduli:             70, 130, 154, 286
total L1 norm:      372.962002076135
minimum local main: 0.6039353780830684
equal eta cap:      0.0016192946592982506
```

This per-residue discrepancy cap is a sufficient corollary, not a necessary
condition.  It still requires pointwise binary-prime pair control rather than
one-dimensional AP marginals.

## Rejected Substitutes

The following are not acceptance conditions:

```text
more finite q286 rows
fitted residual absorption constants such as .125, .126, or .13
normalized L2 or L1 discrepancy alone
one-dimensional AP prime estimates alone
almost-all or averaged estimates with unnamed exceptions
```

## Decision

`HOLD_for_strict_raw_binary_pair_estimate`.

The repository currently has no theorem proving the needed direct signed raw
sum, positive mass plus one-sided projection control, or fixed-modulus
binary-prime convolution bound.  Future finite rows are useful only as
falsifiers or calibration for a predeclared theorem implication.

No direct raw signed binary-prime theorem, positive-mass theorem, one-sided
projection theorem, q286 threshold theorem, strict-central Goldbach theorem, or
Goldbach proof is established.

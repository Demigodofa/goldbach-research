# q286 signed support-tail control definition

Status: theorem-definition and evidence-synthesis receipt.  This is not a
signed tail-control theorem, q286 threshold theorem, strict-central Goldbach
theorem, or proof of Goldbach.

## Purpose

The known-extremals audit falsified the simplification that the support tail
can be ignored after keeping the dominant supports `286`, `154`, and `70`.
The observed sign flips also correct the language: in the known-extremals
receipt the support tail is not rescuing rows.  It is negatively killing
positive principal-plus-top-three partial sums.

Executable receipt:

```text
tools/build_q286_signed_support_tail_control_definition.py
evidence/q286-signed-support-tail-control-definition.json
```

## Fixed Action Identity

Use the support-action decomposition

```text
A_N = P_N + D_N + R_N,
```

where

```text
P_N = principal action,
D_N = E_286(N)+E_154(N)+E_70(N),
R_N = E_14(N)+E_26(N)+E_130(N)+E_10(N)+E_22(N).
```

Since `P_N` is positive on the current strict-central weighted rows, write

```text
A_N/P_N = 1 + d_N + r_N.
```

The Goldbach-useful signed-witness route is therefore:

```text
1 + d_N > 0
r_N > -(1+d_N)
```

for every sufficiently large even `N` in each residue modulo `10010`, plus a
finite verification below the threshold and for any declared exceptions.

If `A_N>0`, then the strict-central weighted prime-pair mass `T_N` is positive:
with no prime pairs, every weighted signed action is zero.  Thus `A_N>0`
implies a strict-central Goldbach representation, hence a Goldbach
representation.

## Evidence Synthesis

The centered character-burden audit shows the dominant support compression is
real but incomplete:

```text
E_286, E_154, E_70 energy fraction: 0.9960328792226287
tail energy fraction:               about 0.0039671207773713
tail supports:                       14, 26, 130, 10, 22
```

The known-extremals audit shows why energy size is not enough:

```text
known-extremal targets:              113
tail sign-decision changes:          16
positive-tail rescue flips:          0
negative-tail kill flips:            16
fresh holdout cycle-minimum flips:   0
```

The existing later-tail complement-source decomposition is compatible with a
range split: on its `73` later tail rows, the principal baseline alone keeps
the rows positive, while nonprincipal-only components do not.

## Resulting Problem

Candidate theorem, not proved:

```text
For each even residue a mod 10010, there are explicit N0(a) and eta_a(N)>0
such that every even N>=N0(a), N==a mod 10010, satisfies

1+d_N >= eta_a(N)
and
r_N > -eta_a(N).
```

This is the signed support-tail control problem.  It is narrower than
Goldbach, but it is still a genuine pointwise signed binary-prime correlation
estimate.  It cannot be obtained from the finite q286 receipts alone.

## Next Falsifier

Freeze the above inequalities before scanning.  Then classify support-tail
kill events on the already checked positive suffix and on one fresh later
block using the optimized row verifier.  Recurrent negative-tail kills in
predeclared later windows falsify a clean later tail-stable threshold and keep
the tail inside the main analytic theorem at all ranges.

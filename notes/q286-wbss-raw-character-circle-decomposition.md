# q286-WBSS raw character circle-method decomposition

## Question

Can the raw q286-WBSS character target be written as an exact circle-method
object whose strict positivity would be genuinely non-circular, and what
collapses the route?

## Receipt

```text
tools/build_q286_wbss_raw_character_circle_decomposition.py
evidence/q286-wbss-raw-character-circle-decomposition.json
```

## Exact Identity

Use the prime-only weight

```text
P(n)=log(n) if n is prime, and P(n)=0 otherwise.
```

For the strict-central interval `I_N={n: N/3<n<2N/3}`,

```text
P_N(alpha)=sum_{n in I_N} P(n)e(alpha n)
P_{d,chi,N}(alpha)=sum_{n in I_N} P(n)chi_d(n)e(alpha n).
```

Then

```text
C_0(N)=int_0^1 P_N(alpha)P_N(alpha)e(-alpha N)dalpha = T_N
```

and

```text
C_{d,chi}(N)
  = int_0^1 P_{d,chi,N}(alpha)P_N(alpha)e(-alpha N)dalpha
  = sum_{p in I_N, N-p prime} log(p)log(N-p)chi_d(p).
```

With

```text
U_{a,d,chi}=sum_s chi_d(s)U_{a,d}(s),
```

the raw character moment is exactly

```text
D_raw_{d,chi}(N)=C_{d,chi}(N)-U_{a,d,chi}C_0(N).
```

The whole witness can also be treated as one signed binary-prime convolution:

```text
W_phi(N)
  = C_0(N)M(a)
    + sum_{d,chi} c_hat_{d,chi}(C_{d,chi}(N)-U_{a,d,chi}C_0(N)).
```

Equivalently,

```text
W_phi(N)=int_0^1 Q_{a,N}(alpha)P_N(alpha)e(-alpha N)dalpha,
```

where

```text
Q_{a,N}(alpha)
  = sum_{n in I_N}P(n)
    [M(a)+sum_{d,chi}c_hat_{d,chi}(chi_d(n)-U_{a,d,chi})]e(alpha n).
```

## Zero-Mass Check

If `T_N=0`, then there are no strict-central prime pairs.  Therefore
`C_0(N)=0`, every `C_{d,chi}(N)=0`, every `D_raw_{d,chi}(N)=0`, every
`E_raw_d(N)=0`, and both `W_phi(N)` and `G_raw(N)` are zero.

So the strict raw `L2` target

```text
C2*sqrt(sum |D_raw|^2) < T_N*M(a)
```

becomes `0<0`, which is false.  Likewise `W_phi(N)>0` is false.

That means the strict unnormalized raw targets are non-circular theorem shapes:
if proved for every sufficiently large covered `N`, they force strict-central
prime-pair support.  But this decomposition does not prove them.

## Required Universal Estimate

The acceptance condition is now a universal, pointwise, unnormalized analytical
estimate, for example

```text
adverse_drag_raw(N) < local_main_raw(N)
```

for every sufficiently large covered `N`, plus an explicit finite remainder.
Finite windows, fitted constants, and visual patterns are diagnostics only.

## Collapse Classifier

The q286 route survives as a proof engine only if the same circle-method
argument proves `W_phi(N)>0`, `G_raw(N)>0`, or
`adverse_drag_raw(N)<local_main_raw(N)` without first assuming pointwise
`T_N>0`.

It collapses if the proof first establishes or assumes

```text
T_N>0
```

for every sufficiently large `N`, and q286 is then used only as a conditional
distribution or normalized `L2` estimate.  That would be strict-central
Goldbach-strength input plus q286 decoration.

## Visualization Candidate

A linked 3D scatterplot plus table is reasonable as an exploratory tool, not
as evidence.  The receipt records the useful layout:

```text
x = log(N)
y = a genuinely ordered analytic quantity, such as local main or driver margin
z = strict closure margin or adverse-drag margin
color = conductor, modulus family, or residue class
brightness = distance from failure
animation = successive N-windows or modulus/character changes
```

The linked table should expose exact `N`, residues, active channels, `C_0`,
`C_{d,chi}`, `D_raw`, `E_raw_d`, local main, adverse drag, and coefficients.

## Decision

`TARGET_raw_character_circle_method_decomposition_bridge_unproved`.

The arithmetic decomposition is confirmed.  The logical bridge is not proved.
The raw q286 target is non-circular only as a strict unnormalized theorem
shape; the accepted result would need a universal pointwise estimate.  A proof
that first imports pointwise `T_N>0` collapses to strict-central
Goldbach-strength input plus q286 decoration.

This proves no major/minor arc estimate, raw character moment theorem,
adverse-drag theorem, strict raw-gap theorem, positive-mass theorem, q286
threshold theorem, strict-central Goldbach theorem, or Goldbach proof.

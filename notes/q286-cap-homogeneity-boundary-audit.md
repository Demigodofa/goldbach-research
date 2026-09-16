# q286 cap homogeneity boundary audit

## Question

Does a universal per-modulus cap such as max(0,-U_d)<=k*T_N cross the zero-mass barrier, or is it only a conditional homogeneous estimate?

## Receipt

```text
tools/build_q286_cap_homogeneity_boundary_audit.py
evidence/q286-cap-homogeneity-boundary-audit.json
```

## Result

The cap-sensitivity window remains useful, but the theorem form matters.

```text
observed cap floor:        0.12228599640255161
strict equal-cap ceiling:  0.179311355950711
```

A normalized cap

```text
max(0,-E_d(N)) <= k for each d, with E_d=U_d/T_N.
```

is conditional on existing mass.  A raw homogeneous cap

```text
max(0,-U_d(N)) <= k*T_N for each d, with sum_d k_d < M(a).
```

is well-defined at zero support, but that is exactly the problem: at
`T_N=0` every component cap reads `0<=0`, while the needed strict gap
`A_raw_-(N)<L_raw(N)` reads `0<0` and does not follow.

The standalone non-circular targets remain

```text
A_raw_-(N) < L_raw(N).
W_phi(N)>0.
```

or else an explicitly labeled two-theorem bridge: first prove positive
strict-central mass, then apply cap/control estimates.

## Decision

Universal per-modulus caps remain useful theorem-shaping data, but a homogeneous cap max(0,-U_d)<=k*T_N is not a standalone Goldbach bridge.  At zero support the cap is true while the strict raw gap is false.  The cap route must therefore be labeled either as a component of a direct strict raw-gap proof or as a two-theorem package with independent positive mass.

This is a logic-boundary audit only.  It proves no homogeneous cap
bridge, per-modulus supremum theorem, positive-mass theorem, raw
adverse-envelope theorem, strict-central Goldbach theorem, or Goldbach
proof.

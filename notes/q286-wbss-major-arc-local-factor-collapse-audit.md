# q286-WBSS major-arc local-factor collapse audit

Clarification, 2026-09-16: the decomposition below is exact centering around
observed mass `T_N`; it is not an evaluation of a major-arc integral. An
independent local-density candidate `M(a)*S(N)*N/3` exists. See
[the CRT derivation and missing mass direction](q286-independent-local-density-and-mass-direction.md).
The historical receipt does not rule that candidate out. Its missing error
estimate and zero-support warning remain valid.

## Question

Does the signed q286 weight produce an independent raw major-arc surplus, or
does its principal local factor depend on ordinary strict-central binary-prime
mass?

## Receipt

```text
tools/build_q286_wbss_major_arc_local_factor_collapse_audit.py
evidence/q286-wbss-major-arc-local-factor-collapse-audit.json
```

## Exact Local Factor

For `a=N mod 10010`, let

```text
A_a={u in U_10010: gcd(a-u,10010)=1}
T_N=sum_{u in A_a} W_N(u)
m_a=|A_a|^-1 sum_{u in A_a} Phi_a(u)
Phi_a^0(u)=Phi_a(u)-m_a
```

Then the raw signed witness decomposes as

```text
W_phi(N)=m_a*T_N
  + sum_{u in A_a}(W_N(u)-T_N/|A_a|)*Phi_a^0(u).
```

So the coefficient-side principal term is a positive local factor times the
ordinary strict-central binary-prime mass.  It is not an independent q286 source
term.  If `T_N=0`, both terms vanish and `W_phi(N)=0`.

## Finite Coefficient Facts

```text
even target residues:                  5005
local means positive:                  5005 / 5005
local mean ratio range:                0.6039353780830684..1.5716524655081636
weakest target residue:                4124
rows with negative admissible weight:  5005 / 5005
rows with pointwise positive floor:    0 / 5005
```

The centered character burden descends to lower natural moduli, not the full
`10010` support.  The dominant supports are:

```text
286: 0.70082890257693
154: 0.15893232135172436
70:  0.13627165529397434
```

Together those three supports carry `0.9960328792226287` of the centered energy.

## Decision

`LOCAL_FACTOR_principal_term_is_T_N_dependent_centered_error_open`.

The q286 signed-weight route survives only as a raw centered-error theorem
target: prove the positive local factor beats the lower-modulus centered
signed correlations in a pointwise, unnormalized circle-method estimate.  If
the proof first imports `T_N>0`, then q286 has collapsed to conditional
distribution control.

This is a symbolic local-factor decomposition and collapse classifier only.  It
proves no major/minor arc estimate, pointwise centered-error estimate, signed
prime-correlation theorem, positive-mass theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

# q286-WBSS rawization obligation audit

## Question

Does the surviving pointwise adverse-drag gate avoid the positive-mass problem,
or does it still need rawization?

## Answer

It still needs rawization or a separate positive-mass theorem.

The current q286-WBSS pointwise gate is written with the normalized actual
strict-central orbit measure:

```text
E_d(N)=<mu_N-u_a,phi_{a,d}>
```

and the local main is the local-uniform normalized mean:

```text
M(N)=<u_a,phi_a>
```

So `A_-(N)<M(N)` is a distribution or anti-alignment theorem once `mu_N`
exists.  It does not by itself prove that strict-central prime-pair mass
exists.

## Receipt

```text
tools/build_q286_wbss_rawization_obligation_audit.py
evidence/q286-wbss-rawization-obligation-audit.json
```

## Finite Calibration

The checked rows do have mass:

```text
checked rows:             348
zero pair-count rows:       0
zero actual-mass rows:      0
positive expectation rows: 348
```

That makes the normalized diagnostics meaningful on the checked rows.  It does
not prove a universal positive-mass theorem.

## Corrected Paths

There are three honest theorem paths:

```text
Path A:
  Prove a direct raw weighted witness W_Phi(N)>0.

Path B:
  Prove T_N>0, then prove normalized A_-(N)<M(N).

Path C:
  Rawize the adverse-drag decomposition using an independent raw mass lower
  bound, then prove raw adverse drag is below raw local main.
```

Path A is the cleanest bridge: if no strict-central prime pair exists, every
raw summand is absent and `W_Phi(N)=0`; strict raw positivity therefore forces
nonempty support.

## Decision

Correct the bridge boundary.  The current pointwise adverse-drag inequality is
a valid conditional distribution target, not a standalone Goldbach bridge.  The
next proof object should be a raw unnormalized witness theorem `W_Phi(N)>0`,
or a two-theorem package consisting of positive strict-central mass plus
normalized adverse-drag control.

No positive-mass theorem, raw witness theorem, pointwise adverse-drag theorem,
q286 threshold theorem, strict-central Goldbach theorem, or Goldbach proof is
established.

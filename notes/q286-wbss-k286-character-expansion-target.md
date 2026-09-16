# q286-WBSS K_286 character expansion target

## Question

Finite evidence is no longer the acceptance condition.  What exact universal,
pointwise, unnormalized analytic estimate would pay the dominant `286` bucket
in the centered-support ledger?

## Target

The dominant bucket is the `11x13` support component.  It descends to natural
modulus `286` and is spanned by the `99` characters that are nontrivial on the
`11` and `13` factors.

The required theorem shape is:

```text
For every sufficiently large covered even N,
K_286(N) >= -0.1759037368828583*P0_a(N),
where a = N mod 10010.
```

Here `P0_a(N)` is the ordinary strict-central principal scale created inside
the same raw analytic argument.  It is not actual observed mass `T_N` used as a
normalizing denominator.

## Expansion

Let

```text
X_286(11x13) = {characters mod 286 trivial on 2,
                nontrivial on 11 and nontrivial on 13}.
```

Then

```text
Phi_{286,a}(r)
  = sum_{chi in X_286(11x13)} c_{a,chi}^{286} chi(r)

C_chi(N)
  = sum_{p in I_N, N-p prime} log(p)log(N-p)chi(p mod 286)

U_{a,chi}^{286}
  = |A_a|^{-1} sum_{r in A_a} chi(r mod 286)

D_chi^P(N)
  = C_chi(N) - U_{a,chi}^{286}*P0_a(N)

K_286(N)
  = sum_{chi in X_286(11x13)} c_{a,chi}^{286} D_chi^P(N)
```

No standalone positive principal term lives in `K_286`.  The principal/local
main is outside this bucket; this bucket is a nonprincipal signed correction.

## Numbers

```text
support label:                         11x13
natural modulus:                         286
character count:                          99
unit residue count:                       120
energy fraction:            0.70082890257693
allocated beta:            0.1759037368828583
required lower bound: K_286(N) >= -0.1759037368828583*P0_a(N)
```

## Boundary

The L2 target is not confirmed as a logical bridge.  It remains a possible
raw theorem shape only if proved pointwise before importing `T_N>0`.

If a route first proves or assumes `T_N>0` and then studies normalized residue
distribution, the route collapses to strict-central Goldbach-strength input
plus q286 decoration.

Using `P0_a(N)` rather than actual `C_0(N)` is a proof-scale target.  A
circle-method proof must create `P0_a(N)` and control the `C_0(N)-P0_a(N)`
mismatch inside the same raw argument.

## Receipt

```text
tools/build_q286_wbss_k286_character_expansion_target.py
evidence/q286-wbss-k286-character-expansion-target.json
test_q286_wbss_k286_character_expansion_target.py
```

## Decision

This is now the sharpest active nonfinite target for the dominant bucket:
prove the `99`-character modulus-`286` raw lower bound pointwise for every
sufficiently large covered even `N`, or falsify it.

No `K_286` lower bound, major/minor arc estimate, pointwise centered-error
estimate, signed prime-correlation theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof is established.

# q286-WBSS Four-Modulus Factor-ANOVA Audit

Status: finite coefficient-algebra evidence only. Goldbach is not proved.

## Question

The minimality audit showed that no proper subfamily of
`{70,130,154,286}` reconstructs the q286-WBSS unit coefficient. This audit
asks for the structural reason, not just another least-squares residual.

## Mechanism

CRT identifies units modulo `10010` with the product:

```text
(Z/5Z)^* x (Z/7Z)^* x (Z/11Z)^* x (Z/13Z)^*
```

Under the uniform product measure, decompose the q286-WBSS unit coefficient
into orthogonal factor-ANOVA interactions. A projection to a modulus can only
carry interactions whose factor support lies inside that modulus.

The four target moduli carry these factor edges:

```text
70  -> 5,7
130 -> 5,13
154 -> 7,11
286 -> 11,13
```

## Receipt

```text
tools/build_q286_wbss_four_modulus_factor_anova_audit.py
evidence/q286-wbss-four-modulus-factor-anova-audit.json
```

The receipt uses the unit coefficient only. It computes all `16` CRT
factor-ANOVA components and compares every projection-family residual with
the prior rowspace minimality audit.

## Result

The nonzero ANOVA supports are exactly:

```text
empty
5
7
11
13
5,7
5,13
7,11
11,13
```

There are no nonzero three-factor or four-factor interactions at the audit
tolerance. The full family `70,130,154,286` covers all nonzero interaction
supports. No proper family does.

The best proper family is:

```text
70,154,286
```

It misses exactly the `5,13` interaction, matching the dropped modulus `130`.
Its ANOVA residual matches the span-minimality residual
`0.025284174723626925`.

Across all `16` projection families, the maximum absolute difference between
the ANOVA residual and the earlier projection-rowspace residual is below
`4e-16`.

## Decision

This explains the previous minimality result structurally: the coefficient
side really is a four-edge CRT interaction object. Fourier/projection
sparsification does not produce a smaller theorem target unless a future
changed mechanism replaces the coefficient itself.

The remaining theorem is still not coefficient algebra. It is strict-central
binary-prime projection control for the four moduli, or direct eventual
positivity of the raw q286-WBSS signed witness.

No binary-prime projection-control theorem, signed discrepancy theorem, q286
threshold theorem, strict-central Goldbach theorem, or Goldbach proof is
established here.

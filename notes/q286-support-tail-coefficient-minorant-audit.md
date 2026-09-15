# q286 support-tail coefficient minorant audit

Status: finite coefficient-side shortcut audit.  This is not a signed
prime-correlation estimate, q286 threshold theorem, strict-central Goldbach
theorem, or proof of Goldbach.

## Question

The row-level tail-stability audit supports a possible later theorem of the
form

```text
A_N/P_N = 1 + d_N + r_N > 0.
```

This audit asks whether the prime-correlation theorem can be avoided by a
stronger coefficientwise shortcut: for every even residue `a mod 10010`, are
the relevant coefficients positive on every admissible unit residue
`r in A_a`?

## Result

`tools/build_q286_support_tail_coefficient_minorant_audit.py` generated
`evidence/q286-support-tail-coefficient-minorant-audit.json`.

Across all `5005` even target residues:

```text
partial coefficients all positive:       0
full coefficients all positive:          0
separated tail-control passes:           0
```

Global unit coefficient ratios:

```text
principal+dominant min/max:  -11.64548630338637..39.29608368571964
support-tail min/max:        -0.7126246050853711..0.9350883353360848
full min/max:                -11.747067126163127..40.22881030015595
```

The worst full-ratio residue is `0 mod 10010`; its admissible support is the
entire unit group and contains:

```text
full negative coefficients:     1228
full positive coefficients:     1652
partial negative coefficients:  1240
partial positive coefficients:  1640
tail negative coefficients:     1488
tail positive coefficients:     1392
```

## Interpretation

This cleanly falsifies the coefficientwise nonnegative-weight shortcut.  The
q286 signed-witness route cannot be proved by saying the fixed coefficient is
positive on every admissible residue cell, nor by separating a pointwise
positive `1+d(r)` margin from a uniformly bounded tail `r_tail(r)`.

The remaining theorem must use actual prime-pair distribution: how the
strict-central prime-pair weight lands on the positive and negative coefficient
cells.  In other words, the problem is genuinely a signed binary-prime
correlation/cone problem, not only coefficient bookkeeping.

Useful surviving pieces:

```text
local mean over every A_a remains positive;
post-90080 row-level tail kills did not recur in the checked window;
coefficientwise arbitrary nonnegative mass is too broad.
```

Next theorem shape:

```text
For actual W_N, not arbitrary nonnegative W:
sum_r W_N(r) * (P+D)(r) > 0
and
sum_r W_N(r) * R(r) > -sum_r W_N(r) * (P+D)(r).
```

Any proposed cone or AP theorem must constrain landing on the negative cells
strongly enough to imply those two inequalities.

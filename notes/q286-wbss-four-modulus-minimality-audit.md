# q286-WBSS Four-Modulus Minimality Audit

Status: finite coefficient-algebra evidence only. Goldbach is not proved.

## Question

The four-modulus span identity narrowed the q286-WBSS coefficient side to
total mass plus projections to:

```text
70, 130, 154, 286
```

This audit asks whether Fourier/projection sparsification can produce an even
smaller theorem target by dropping at least one of those moduli.

## Receipt

```text
tools/build_q286_wbss_four_modulus_minimality_audit.py
evidence/q286-wbss-four-modulus-minimality-audit.json
```

The receipt enumerates all `16` subfamilies of `{70,130,154,286}` at the
unit-coefficient span level. It uses no prime counts and no target scans.

## Result

No proper subfamily reconstructs the q286-WBSS unit coefficient at
numerical-zero residual. The best proper family is:

```text
70, 154, 286
```

with relative L2 residual:

```text
0.025284174723626925
```

and maximum absolute residual above `0.25`. The full four-modulus family has
relative L2 residual below `1e-12`.

## Decision

Fourier/projection sparsification does not produce a smaller coefficient
theorem target at this algebraic level. The narrowed target remains strict
central binary-prime projection control for all four moduli
`70,130,154,286`, or a direct proof that the raw q286-WBSS signed witness is
eventually positive.

This proves no universal projection-control theorem, no signed discrepancy
theorem, no q286 threshold theorem, no strict-central Goldbach theorem, and no
Goldbach proof.

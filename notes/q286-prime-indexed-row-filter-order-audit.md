# q286 prime-indexed row filter-order audit

Status: finite optimized row-level verifier integration audit.  This is not a
full later-block scan, threshold theorem, signed correlation theorem,
pointwise character-sum theorem, or Goldbach proof.

Receipt:

```text
tools/build_q286_prime_indexed_row_filter_order_audit.py
evidence/q286-prime-indexed-row-filter-order-audit.json
```

## Question

The prime-indexed residue kernel matched direct residue sums.  This receipt
tests the next gate: can those residue weights reproduce the existing q286
row-level first-two, first-three, complement, full, and predicate outputs?

## Mechanism

The optimized verifier reuses the same q286 support/mode linear action as the
direct receipt, but feeds it strict-central residue weights computed by the
validated prime-indexed kernel.

## Result

`evidence/q286-prime-indexed-row-filter-order-audit.json` validates the route:

```text
validation targets: 40
predicate mismatches: 0
max first-two delta: 6.43582409587395e-16
max first-three delta: 6.48786580015326e-16
max complement delta: 6.66133814775094e-16
max full delta: 8.88178419700125e-16
optimized benchmark: 0.112419599987334 seconds for 101 targets
projected six-block runtime: 4.45671364702261 minutes
```

Interpretation rules:

- A pass validates the optimized path as row-level equivalent on the finite
  validation fixture.
- It does not itself run the exhaustive later full blocks.
- The next finite computation is the six-block later q286 receipt using the
  optimized verifier.

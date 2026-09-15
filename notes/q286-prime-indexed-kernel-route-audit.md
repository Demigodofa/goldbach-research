# q286 prime-indexed kernel route audit

Status: finite optimized-kernel route audit.  This is not a full-block
verification, threshold theorem, signed correlation theorem, pointwise
character-sum theorem, or Goldbach proof.

Receipt:

```text
tools/build_q286_prime_indexed_kernel_route_audit.py
evidence/q286-prime-indexed-kernel-route-audit.json
```

## Question

The sampled suffix holdout exposed a practical bottleneck: direct later
full-block q286 verification by scanning every integer in every strict-central
interval is too opaque and slow.  This receipt tests the first safe
optimization layer: compute strict-central pair weights by iterating only
precomputed primes, while preserving residue-weight sums.

## Mechanism

For each target `N`, both kernels compute:

```text
sum log(p) log(N-p)
```

over strict-central prime pairs, grouped by residue class.  The q286 action and
support decomposition are linear in these residue weights.  Therefore exact
agreement of residue weights is the necessary input validation for any later
optimized q286 verifier.

## Result

The prime-indexed residue kernel matched the direct integer-loop kernel on all
validation targets and both tested moduli:

```text
validation targets:                 34
validated moduli:                   286, 10010
maximum pair-count delta:             0
maximum total-weight delta:           0
maximum residue-weight delta:         0
prime-indexed kernel validated:    true
```

Benchmark on `101` later targets `490480..490680` modulo `10010`:

```text
direct integer-loop seconds:        0.5489822000090498
prime-indexed seconds:              0.03170959999260958
speedup:                            17.312807482182013
mean central prime-pair count:      2135.5247524752476
projected six full later blocks:    1.2570815680238492 minutes
```

The projection is only a routing estimate for residue-weight computation.  The
full q286 verifier is not ready until this kernel is integrated into the
support/mode action and row-level ratios are checked against the existing
direct receipt.

Interpretation rules:

- A match validates the prime-indexed residue kernel as a safe first
  optimization layer.
- It does not yet validate a full q286 row-level verifier.
- Full later-block verification still needs this kernel integrated into the
  support/mode action, or a stronger window-convolution implementation.

## Next Obligation

Build a drop-in q286 filter-order receipt that consumes the validated
prime-indexed residue weights, then compare row-level first-two, first-three,
complement, and full ratios against the existing direct receipt before using it
for exhaustive later full-block scans.

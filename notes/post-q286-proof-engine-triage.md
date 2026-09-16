# Post-q286 proof-engine triage

## Question

After the active-character and signed-weight q286 proof engines were put to
sleep, what is the next evidence-bearing analytical proof engine?  More finite
q286 horizon evidence and tighter fitted constants are not an acceptance
condition.

## Receipt

```text
tools/build_post_q286_proof_engine_triage.py
evidence/post-q286-proof-engine-triage.json
```

## Decision

Status:

```text
TARGET_mobius_incomplete_prime_row_covariance_after_q286_sleep
```

The selected non-q286 theorem target is the Mobius incomplete prime-row
covariance.  This target asks for a universal analytical estimate, not another
finite fit: prove a local signed covariance or boundary-operator estimate for
the actual Mobius-log coefficients on prime rows, strong enough to beat the
`N^(1499/1000+epsilon)` benchmark uniformly over the surviving long dyadic
blocks.

## Exact Gates

The short and medium dyadic blocks are already paid uniformly in location:

```text
paid length threshold: 1499/2000 = 0.7495
target exponent:       1499/1000 = 1.499
family margin there:   301/2000  = 0.1505
```

The first clean unpaid balanced probe is already beyond the benchmark:

```text
block length y:        3/4
collision exponent:    3/2
target exponent:       1499/1000
factor-Cauchy route:   false
```

The balanced finite-field trilinear source gate at `y=3/4`, `alpha=1/2` does
not close the gap.  Petridis-Shparlinski Theorem 1.3 is worse than Parseval by
`729/1600 = 0.455625`, and the Wright 2.2 upper range is impossible at the
unchanged prime-companion exponent `59/100`.

## Sleep Or Reservoir

Keep the following out of the active proof-engine slot unless a changed
condition appears:

```text
q286 active-character finite receipts
q286 componentwise finite envelopes
balanced semiprime signed-total route without a T_kappa lower bound
generic cofactor averaging source plug-ins
large-modulus bare exponent matches
```

## Next Test

Derive the exact incomplete-row boundary operator after the complete-period
conductor closure, then test whether its operator norm factors through the
actual arithmetic row spacing with only subpower loss.

Falsifiers:

```text
generic absolute values or Cauchy reproduce the long-block Y^2 collision loss
max-norm active-band source bounds miss the needed L2-normalized band energy
Wright/BV prime-exponent rebalance has no source range in the unpaid window
```

No Mobius covariance theorem, source theorem application, strict-central
Goldbach theorem, q286 theorem, or Goldbach proof is established.

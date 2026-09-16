# Goldbach three-candidate synthesis audit

## Question

Can three new-to-this-task arithmetic or statistical objects be assembled from the current patterns, and do any earn a next test?

## Receipt

```text
tools/build_goldbach_three_candidate_synthesis_audit.py
evidence/goldbach-three-candidate-synthesis-audit.json
```

## Attempts

### Attempt 1: raw adverse-envelope margin

State: `live_candidate_unproved`.

Formula: Delta_raw(N) = L_raw(N) - sum_d max(0, -E_raw,d(N)); target Delta_raw(N) > 0 for all sufficiently large N.

Mechanism: Separate each projected modulus' harmful signed contribution, throw away helpful terms, and ask whether raw local main still beats the disconnected adverse envelope.

Falsifier: A correctly raw row with Delta_raw(N) <= 0, or a proof that E_raw,d cannot be bounded independently of the unknown prime-pair mass, kills this as a standalone bridge.

Next test: Define the raw E_raw,d and L_raw objects explicitly and check whether the existing finite component envelope is an artifact of normalization.

### Attempt 2: source-gap curvature sign rule

State: `falsified_as_universal_sign_rule`.

Formula: For ordered mirror source blocks (u_i,v_i), set g_i=v_i-u_i and kappa=g_1-2*g_2+g_3.  Trial rule: sign(first cross-block non-middle) = -sign(kappa).

Mechanism: The q=38038 versus q=41990 split suggested that accelerating or decelerating contraction of source gaps might control whether the first off-diagonal block pays or drags.

Falsifier: All-row mismatch rate materially above noise; observed 19 mismatches among 32 valid rows.

Next test: Do not promote kappa alone.  Use it only, if at all, as one feature inside the fuller source-block interaction audit.

### Attempt 3: route-closure pressure score

State: `triage_statistic_only`.

Formula: score(route)=raw_pointwise + input_side_invariant + predeclared_falsifier + finite_margin - normalization_dependency - fitted_constant - high_mode_diffusion - posthoc_selector.

Mechanism: The research record has a repeated failure mode: a route looks good finitely, then loses theorem value when it depends on normalization, fitted constants, many hidden Fourier modes, or post-hoc selectors.  This score keeps that penalty explicit while choosing the next test.

Falsifier: If this score repeatedly selects lanes that add no new falsifier, no sharper theorem obligation, and no failed candidate to retire, it is bookkeeping rather than math.

Next test: Use the score to justify the all-row source-block interaction audit over another scalar or visual map.

## Decision

Attempt 1 remains the clean q286 proof-shaped target but still requires raw definitions and a universal theorem.  Attempt 2 was a real new arithmetic statistic and failed as a universal one-number sign rule, which is useful because it blocks a cheap overfit.  Attempt 3 is only a route-selection statistic; it says to spend the next work on raw pointwise estimates or input-side matrix invariants, not more fitted scalar dots.

This is finite candidate synthesis only.  It proves no universal raw
pointwise theorem, source-gap curvature theorem, route-closure theorem,
strict-central Goldbach theorem, or Goldbach proof.

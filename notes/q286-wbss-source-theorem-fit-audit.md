# q286-WBSS source theorem fit audit

## Question

After the strict raw-gap analytic HOLD, can any currently named source-backed
AP or Goldbach-in-progressions theorem directly pay the pointwise raw
binary-prime estimate?

## Receipt

```text
tools/build_q286_wbss_source_theorem_fit_audit.py
evidence/q286-wbss-source-theorem-fit-audit.json
```

## Required Theorem Shape

The q286-WBSS bridge needs:

```text
every sufficiently large covered even N
an unnormalized raw sum
the exact q286-WBSS coefficient or equivalent four-modulus/character expansion
strict-central p range N/3 < p < 2N/3
an explicit threshold N0 plus finite verification below N0
```

Zero-support rows have raw value zero, so the theorem must create a strict
positive raw quantity.  Normalized, averaged, or almost-all statements do not
pay this bridge by themselves.

## Source Fit

`BMOR_2018_AP_prime_counts`

Useful one-dimensional AP input, but insufficient as a direct q286 bridge.  It
controls marginal prime occupancy by residue class, not the reflected binary
convolution `p+(N-p)` or the signed q286 coefficient direction.  The existing
`q286-ap-count-bridge-gap-audit` already falsifies the count-only pigeonhole
bridge in the valid `q=286` range.

`Salmensuu_2021_binary_AP_Goldbach_almost_all`

Relevant binary AP-Goldbach literature, but insufficient as a direct bridge.
The q286 route needs every sufficiently large covered target, an explicit finite
remainder threshold, the strict-central interval, and a signed weighted
coefficient sum.  Almost-all or exceptional-set theorems leave unnamed targets.

`Halupczok_2012_AP_Goldbach_mean_value`

Relevant circle-method and L-function setting, but insufficient as a direct
bridge.  Mean-value or averaged representation information does not give a
pointwise raw lower bound for the signed q286-WBSS witness for every covered
target.

`q286_active_character_L2_payment`

This is the best current internal theorem target, not a source theorem.  The
aggregate active-character moment cap is materially looser than per-residue
control, but the required pointwise twisted binary-prime moment theorem is still
missing and must be rawized or paired with positive mass.

## Candidate Next Route

Candidate: fixed-finite-modulus weighted circle-method bridge.

Mechanism: expand the q286-WBSS coefficient into a finite active character
package and try to prove a pointwise raw major-arc main term with
minor-arc/twisted-character error smaller than the positive local main.

Prediction: a real proof will produce an explicit raw lower bound for the
signed q286-WBSS witness, not merely almost-all AP occupancy or normalized
distribution.

Falsifier: if the argument needs an unproved pointwise lower bound for the
unweighted strict-central binary Goldbach count before the signed witness is
positive, then the route remains Goldbach-strength and cannot be accepted as an
easier bridge.

Smallest next test: write the exact raw character-expanded target `B_phi(N)`
and separate which terms would be principal main, nonprincipal twisted moments,
strict-central truncation error, and finite remainder.

## Decision

`SOURCE_FIT_no_existing_direct_pointwise_bridge`.

No currently named source theorem fits the q286 strict raw-gap payment as a
direct bridge.  The next evidence-bearing move is an exact raw
character-expanded theorem target for a bespoke fixed-modulus weighted
circle-method estimate, or a sleep decision if that target collapses to
ordinary pointwise binary Goldbach.

This proves no external pointwise bridge theorem, no strict raw-gap theorem, no
q286 threshold theorem, no strict-central Goldbach theorem, and no Goldbach
proof.

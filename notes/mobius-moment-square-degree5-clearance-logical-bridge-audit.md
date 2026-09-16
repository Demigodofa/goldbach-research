# Mobius moment-square degree-5 clearance logical bridge audit

## Question

Does the sigma-band clearance evidence already provide a non-circular theorem
bridge, or only a finite decomposition of the same signed margin ledger?

## Receipt

```text
tools/build_mobius_moment_square_degree5_clearance_logical_bridge_audit.py
evidence/mobius-moment-square-degree5-clearance-logical-bridge-audit.json
```

## Answer

Only the finite decomposition is confirmed.  A non-circular bridge would
require independent pointwise estimates bounding near-threshold adverse
leakage above and middle/far clearance margin below, uniformly in the moving
prime block.

The finite structure is still useful:

```text
band-minimum blocks checked:                         4
tight source blocks checked:                         6
finite decomposition confirmed:                      true
logical bridge confirmed:                            false
finite evidence is acceptance condition:             false
max near negative / middle-far positive:             0.0016400172796714467
false all-negative-near shortcut confirmed:          true
```

## Pointwise Target

For source scale `M`, moving prime `p in [M,2M]`, row count
`A=int((M**(1/.59))**.41)`, component label `ell`, and reduced denominator
`Q`, define

```text
m_Q(M,p,ell) = full_Q(M,p,ell)/2 - active_Q(M,p,ell)
A_near       = sum_{p*A < Q < 2*p*A} max(0,-m_Q(M,p,ell))
G_middle_far = sum_{Q >= 2*p*A} m_Q(M,p,ell)
```

A sufficient unnormalized pointwise bridge would prove

```text
G_middle_far(M,p,ell) > A_near(M,p,ell)
```

for every sufficiently large source-admissible row, with finite remainder
checked separately.

This is stronger than merely reusing total margin positivity because
near-positive terms are discarded.  If proved from independent estimates, it
would imply positive total margin without assuming it.

## Required Independent Obligations

```text
1. moving_prime_sigma_coverage
   Cover every sufficiently large source-admissible prime block p in [M,2M]
   by sigma bands, including endpoints.

2. near_adverse_upper_bound
   Prove a pointwise upper bound for A_near(M,p,ell) without using total
   margin positivity.

3. middle_far_lower_bound
   Prove a pointwise lower bound for G_middle_far(M,p,ell) without reusing
   the target positivity claim.

4. comparison_margin
   Show lower_bound(G_middle_far) exceeds upper_bound(A_near) by an explicit
   positive margin.

5. finite_remainder
   After a threshold theorem, verify all smaller source scales by exact
   computation.
```

Invalid substitutes include finite clearance ratios, the false
all-negative-near shortcut, total denominator margin already known positive,
fitted residual constants, or a normalized estimate that assumes positive
Goldbach mass first.

## Decision

`HOLD_clearance_logical_bridge_not_confirmed`.  The clearance family split is
useful finite structure, but the theorem bridge requires independent
pointwise unnormalized estimates.  Future work should target near-adverse
upper bounds and middle/far lower bounds, not broader finite scans or the
false all-negative-near shortcut.

The smallest next test is the `M=229`, `p=379` middle-band exception: derive
an exact symbolic or interval upper bound for the lone adverse middle-family
denominator `Q=46189` and compare it to the positive middle/far ledger without
using total positivity.

This is a logical bridge audit only.  It proves no source-start theorem,
prime-block theorem, moving-prime theorem, sigma-band theorem,
clearance-family theorem, strict-central Goldbach theorem, or Goldbach proof.

# q286 direct-witness sign-split budget audit

## Question

The anti-landing route is near-sharp.  Can we escape that sharpness by proving
the direct q286-WBSS witness `B_Phi(N)>0` through the raw positive/negative
coefficient split instead?

For a coefficient `phi`, write:

```text
P_phi(N) = E_mu max(phi,0)
D_phi(N) = E_mu max(-phi,0)
B_phi(N) = P_phi(N) - D_phi(N).
```

If this direct split has a looser source-theorem budget than anti-landing, it
should lead.  If it is equally sharp or sharper, it is not an escape hatch.

## Receipt

```text
tools/build_q286_direct_witness_sign_split_budget_audit.py
evidence/q286-direct-witness-sign-split-budget-audit.json
```

## Result

On the same `196` post-discovery rows:

```text
anti-landing tight symmetric budget: 0.009481452906409388

full coefficient direct sign split:
  tightest target:                 94856
  tightest P/D:       1.0145084566730913
  tightest symmetric budget: 0.007201983503733535

edge-beta direct sign split:
  tightest target:                 94856
  tightest P/D:       1.0191444227555964
  tightest symmetric budget: 0.009481452906409388
```

The full raw coefficient split is even tighter than the anti-landing split.
The edge-beta split reproduces the anti-landing budget because it is the same
edge-rescue coefficient.

## Decision

`HOLD_direct_sign_split_not_escape_from_sharp_correlation`.

A naive positive-versus-negative coefficient landing proof of direct
`B_Phi(N)>0` is not easier than anti-landing.  The next proof object must be a
more adapted signed binary-prime correlation estimate, not broad `L1`,
mass-majority, AP counts, or raw sign-split landing.

## Boundary

Finite theorem-budget audit only.  This proves no direct witness theorem,
signed binary-prime correlation theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

# q286-WBSS L1-budget obstruction audit

Status: finite obstruction to one proof route.  This is not a binary
distribution theorem, signed correlation theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

## Question

The main-term sign audit showed that the q286 weighted binary-prime sign-sum
problem has a favorable local-uniform mean.  A tempting next theorem would be:

```text
||mu_N-u_a||_1
  <
mean_u(Phi_a)/||Phi_a-mean_u(Phi_a)||_infty.
```

This is sufficient for signed positivity, but it may be much too strong.  This
audit compares that sufficient L1 budget against the actual checked
strict-central binary-prime orbit measures.

## Result

`tools/build_q286_wbss_l1_budget_obstruction_audit.py` generated
`evidence/q286-wbss-l1-budget-obstruction-audit.json`.

On the `196` post-discovery rows:

```text
actual L1 distance from local uniform:       0.5533526980785324..1.574410774410774
full coefficient L1 budget:                 0.020711496156757627..0.06441548422792709
edge beta L1 budget:                        0.026797640365636533..0.18715353351948102
full rows inside sufficient L1 budget:      0 / 196
edge beta rows inside sufficient L1 budget: 0 / 196
full L1/budget ratio range:                 10.615378246364296..58.85757007200199
edge beta L1/budget ratio range:            3.3936673457437085..55.73635115717084
```

Despite that, the actual signed expectations remain positive on `196/196`
post-discovery rows for both the full coefficient and the edge beta
coefficient.

## Decision

Demote blunt total-L1 uniformity as the q286-WBSS bridge.  The checked rows are
successful while very far from the local-uniform admissible orbit measure, so
a theorem of the form "actual binary-prime mass is close to uniform in L1" is
not describing the observed mechanism.

The surviving theorem target must be coefficient-specific:

```text
<mu_N-u_a, Phi_a> > -mean_u(Phi_a)
```

or directly:

```text
B_Phi(N) > 0.
```

That is a signed correlation or signed norm theorem, not ordinary uniformity.
The q286 answer has now created a more precise problem: prove that the actual
large binary-prime deviations, although large in total variation, do not align
too strongly against the specific q286 coefficient.

## Consequence for strategy

This is a stop sign for another broad heat-map or L1-uniformity audit.  It is
not a stop sign for q286-WBSS itself.  The favorable mean survived; the blunt
error norm failed.  The next proof attempt should either:

- construct a signed discrepancy estimate for the explicit q286 coefficients;
- find a smaller norm adapted to the coefficient family;
- prove a Farkas certificate from source-backed binary-prime inequalities; or
- abandon q286 as a proof engine and preserve it as finite structure.

# q286-WBSS Four-Modulus Positivity-Budget Audit

Status: finite diagnostic algebra. This is not an independence theorem,
fixed-modulus equidistribution theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

## Question

The far-lift holdout falsified the finite shortcut `adverse iid-scale z < 3`.
This receipt asks what normalization survived. The answer is the row's
available main-term sigma budget:

```text
positivity_budget_sigma = local_uniform_main_term / iid_standard_error
positivity_margin_sigma = actual_formula_expectation / iid_standard_error
signed_budget_ratio     = -iid_z_score / positivity_budget_sigma
```

The last ratio equals `lambda_phi`, so positivity is exactly
`signed_budget_ratio < 1`.

## Receipt

```text
tools/build_q286_wbss_four_modulus_positivity_budget_audit.py
evidence/q286-wbss-four-modulus-positivity-budget-audit.json
```

The receipt combines the initial `116`-row variance-scale holdout and the
farther `116`-row holdout. It performs no new prime-orbit recomputation.

## Result

```text
combined rows checked:                       232
direct witness positive rows:                232 / 232
fixed adverse z < 3 failures:                  1
budget failures:                               0
signed ratio >= 1 failures:                    0
maximum signed budget ratio:      0.29444884696113977
largest signed-ratio target:              1002478
tightest sigma-margin target:             1001554
```

The failed `z < 3` row is not a positivity threat under the correct
normalization. At target `1002478`, adverse z is `3.5107558040930176`, but the
signed budget ratio is only `0.29444884696113977`.

## Decision

Do not revive a fixed adverse-z cap. The useful theorem target is the exact
budget-ratio condition `lambda_phi < 1`, equivalently adverse z below the
row's local main-term sigma budget. This is still finite algebraic evidence
only; no universal bound or Goldbach proof is established.

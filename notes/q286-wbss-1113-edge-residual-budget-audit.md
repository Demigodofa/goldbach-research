# q286-WBSS 11,13 Edge Residual-Budget Audit

Status: finite row-budget diagnostic only. Goldbach is not proved.

## Question

The finite edge-character load audit found that `11,13` is the dominant
absolute edge on `227/230` available dual-edge rows and on all `196`
post-discovery rows. This audit asks whether that dominance supports a
theorem-shaped split:

```text
11,13 edge drag + residual from 5,7 / 5,13 / 7,11
```

The tested finite inequality is:

```text
max(0, residual_edge_signed_sum) < theta * (-(11,13 signed contribution))
```

This is a signed positive-pushback budget. It is deliberately not an absolute
residual-load budget, because the other edges often help the `11,13` drag
instead of opposing it.

## Receipt

```text
tools/build_q286_wbss_1113_edge_residual_budget_audit.py
evidence/q286-wbss-1113-edge-residual-budget-audit.json
```

## Result

The `11,13` edge contribution is negative on every checked row:

```text
all dual-edge rows:  230 / 230
post-discovery rows: 196 / 196
```

After adding the other three edges, the total edge contribution remains
negative on every row. The other edges have positive net pushback on `32`
rows and negative net help on `198` rows.

The observed finite positive-pushback ratio is:

```text
minimum: 0
mean:    0.013928821952078015
maximum: 0.3895519069948021
```

The worst row is target `374048`, where the other three edges push back by
`0.14302279399336443` against `0.3671469486485477` of `11,13` drag. The
remaining lead margin is `0.22412415465518326`.

Threshold checks on the finite fixture:

```text
theta = 1/4: fails 3 rows
theta = 1/2: passes all rows
theta = 1:   passes all rows
```

The absolute residual-load ratio is not small; its maximum is
`2.561969334773402`, because many residual edge contributions are negative
help. That confirms the theorem target should be one-sided and signed.

## Decision

The finite rows support using `11,13` as the lead analytic edge and treating
`5,7`, `5,13`, and `7,11` as a signed residual budget. The finite data
suggests a one-sided residual theta below `1`, with `.5` passing the present
fixture and `.25` failing it.

This does not prove a universal theta, a residual theorem, or a character-sum
bound. It also does not permit dropping the residual edges. A future proof
would need a source-backed signed estimate for the `11,13` edge and a
theorem-level one-sided residual bound for the other edges.

No 11,13 edge theorem, residual theorem, character-sum bound, binary-prime
projection-control theorem, signed discrepancy theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof is established
here.

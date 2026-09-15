# q286 unnormalized dual-edge witness audit

Status: finite raw-witness diagnostic and `new-to-this-task`
changed-under-evidence result.  This is not an unnormalized witness theorem,
signed prime-correlation estimate, q286 threshold theorem, strict-central
Goldbach theorem, or Goldbach proof.

Receipt:

```text
tools/build_q286_unnormalized_dual_edge_witness_audit.py
evidence/q286-unnormalized-dual-edge-witness-audit.json
```

## Question

The dual-edge audit states the rescue inequality in normalized measure form:

```text
E_mu_N[g_a,t] > -ell_a,t(t).
```

But `mu_N` is defined only after the strict-central pair mass `T_N` is
positive.  The bridge question is:

```text
Can the edge rescue be restated as a raw signed prime-pair sum?
```

## Result

For the `196` checked post-discovery rows:

```text
observed strict-central pair rows:      196 / 196
positive raw signed witness rows:       196 / 196
pair count:                             318..2454
total log-weight T_N:                   36745.77894545931..418330.55338799115
raw edge gap:                           183790.79817980513..2815344.667600736
raw required edge gap:                  179737.27622328722..2570679.1059527574
raw signed margin after rescue:         490.7620118705381..361940.33348482125
raw identity error:                     0.0..2.3283064365386963e-10
normalized edge-gap rescue ratio:       1.0021652272515458..1.3070973629998075
```

The tightest raw margin is again target `94856`:

```text
pair count:                             338
T_N:                                    39022.250002965484
raw edge gap:                           227146.88391323725
raw required edge gap:                  226656.1219013667
raw signed margin after rescue:         490.7620118705381
```

## Interpretation

Multiplying by `T_N` gives the exact raw identity:

```text
raw_edge_gap - raw_required_edge_gap
  = T_N * Full(mu_N).
```

A future theorem can aim directly at a raw signed sum:

```text
sum_orbits W_N(orbit) * g_a,t(orbit)
  > -T_N * ell_a,t(t).
```

That is closer to Goldbach than the normalized statement because if a raw
signed prime-pair sum is proved strictly positive without assuming `T_N>0`,
then at least one strict-central prime pair exists.  However, this finite
receipt does not prove such a theorem.  It uses rows where the pair mass and
pair counts were already computed, so it remains downstream of existence.

## Decision

The normalization gap is not closed, but it is now sharply located.  The next
analytic proof obligation is one of:

- prove `raw_full_signed_witness > 0` directly as a signed binary-prime
  correlation estimate;
- produce a coefficientwise nonnegative minorant below the raw witness;
- or supply an independent lower bound for `T_N>0` before normalized q286
  geometry is invoked.

The first option is the cleanest route if it can be made source-backed.  The
second is stronger than necessary but would be decisive.  The third risks
using Goldbach-like input as a premise.


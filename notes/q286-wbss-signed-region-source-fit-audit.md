# q286-WBSS signed-region source-fit audit

## Question

Does any currently named source-shaped theorem pay the q286 raw signed-region
obligation?

## Receipt

```text
tools/build_q286_wbss_signed_region_source_fit_audit.py
evidence/q286-wbss-signed-region-source-fit-audit.json
```

## Required Shape

The needed theorem is pointwise, raw, strict-central, binary, and weighted:

```text
for every sufficiently large covered even N,
sum_{u:phi(u)>0} P_N(u)phi(u)
  > sum_{u:phi(u)<0} P_N(u)(-phi(u)).
```

Here `P_N(u)` is raw strict-central log-pair mass with left prime residue `u`,
using `N/3<p<2N/3` and requiring both `p` and `N-p` to be prime.

Normalized negative-region mass statements are useful diagnostics, but they do
not prove support unless they are embedded in a raw strict positivity proof or
paired with an independently proved positive-mass theorem.

## Fit Table

```text
BMOR_2018_AP_prime_counts:
  insufficient.  Marginal AP prime counts do not control the reflected
  binary-prime convolution or where pair mass lands inside q286 signed regions.

Salmensuu_2021_binary_AP_Goldbach_almost_all:
  insufficient as a direct bridge.  The q286 target needs every covered target,
  strict-central truncation, log weights, and the exact signed finite-modulus
  inequality; almost-all or exceptional-set quantifiers leave possible targets.

Halupczok_2012_AP_Goldbach_mean_value:
  insufficient as a direct bridge.  Mean-value or averaged AP representation
  information does not prove the pointwise signed-region inequality.

q286_active_character_L2_payment:
  related unproved target.  It could imply signed-region control if a raw
  pointwise character-moment theorem were proved, but the theorem is missing.

q286_signed_region_shape_target:
  exact target, not theorem.  The negative-region threshold audit names the
  right inequality but does not prove prime-pair mass has the needed shape.
```

## Decision

`SOURCE_FIT_no_existing_signed_region_pointwise_bridge`.

The signed-region obligation is exact, but no currently named external source
theorem pays it directly.  The next useful work is a bespoke fixed-modulus
signed circle-method target, a raw active-character moment theorem, or a
collapse classifier if that target first requires `T_N>0`.

This proves no external pointwise bridge theorem, signed negative-region
distribution theorem, raw adverse-drag theorem, positive-mass theorem, q286
threshold theorem, strict-central Goldbach theorem, or Goldbach proof.

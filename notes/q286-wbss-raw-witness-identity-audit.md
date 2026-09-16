# q286-WBSS raw witness identity audit

## Question

The pointwise q286-WBSS adverse-drag gate is stated through the normalized
actual strict-central orbit measure `mu_N`.  That is not a complete Goldbach
bridge unless strict-central mass is already known.  Can the current checked
rows be re-expressed as an unnormalized raw witness identity whose strict
positivity would force actual strict-central support?

## Mechanism

For each checked row, recompute the strict-central log-pair mass

```text
T_N = sum log(p)log(N-p)
```

over prime pairs with `N/3 < p < 2N/3`.  Then scale the normalized q286-WBSS
quantities by `T_N`:

```text
W_phi(N)          = T_N * <mu_N,phi_N>
raw_local_main(N) = T_N * M(N)
raw_error_d(N)    = T_N * E_d(N)
raw_gate_gap(N)   = T_N * (M(N)-A_-(N))
```

If `T_N=0`, the raw witness is an empty signed sum and equals `0`.  Therefore a
direct theorem `W_phi(N)>0` is non-circular: it forces at least one
strict-central prime pair.

## Receipt

```text
tools/build_q286_wbss_raw_witness_identity_audit.py
evidence/q286-wbss-raw-witness-identity-audit.json
```

## Result

```text
checked rows:                    348
target range:        1036248..1155862
zero pair-count rows:              0
zero total-weight rows:            0
positive raw witness rows:       348 / 348
positive raw adverse-gap rows:   348 / 348
pair-count mismatches:             0
```

Tightest finite rows:

```text
minimum total weight target:       1042424
minimum total weight:   443620.45738706784
minimum raw witness target:        1059514
minimum raw witness:    286929.1729900493
minimum raw adverse gap target:    1059514
minimum raw adverse gap:286929.1729900494
```

The raw reconstruction errors are numerical roundoff only:

```text
max |W_phi - (raw_main + raw_errors)| < 1e-8
max |raw_gap - (raw_main - raw_drag)| < 1e-8
```

## Decision

Rawization repairs the logical target but does not prove it.  The checked
finite rows confirm that the existing normalized q286-WBSS witness and
adverse-gap data scale to positive raw witnesses under the exact strict-central
log-pair mass.

The live theorem target is now:

```text
Prove W_phi(N)>0 for every sufficiently large covered even N,
then verify the finite remainder below the threshold.
```

The alternate route remains:

```text
Prove T_N>0 first, then prove the normalized pointwise adverse-drag gate.
```

No raw witness theorem, positive-mass theorem, pointwise adverse-drag theorem,
q286 threshold theorem, strict-central Goldbach theorem, or Goldbach proof is
established.

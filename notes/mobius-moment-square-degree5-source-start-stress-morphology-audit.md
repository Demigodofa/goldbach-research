# Mobius moment-square degree-5 source-start stress morphology audit

## Question

After the complete `M=331` sweep moved the weakest row from the sentinel prime
`p=461` to `p=599`, what should guide the next source-start target: a fixed
attention prime, a component label, endpoint position, or a prime-level stress
block?

## Mechanism

Read the complete fresh-scale source-start sweeps:

```text
M=229
M=251
M=293
M=331
```

For every dominance row, record:

```text
scale M
prime p
component label
active/full ratio
slack above 1/2
p/M
(2M-p)/M
```

Then group rows by prime and inspect whether the tightest rows are isolated
components or coherent prime blocks.

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_start_stress_morphology_audit.py
evidence/mobius-moment-square-degree5-source-start-stress-morphology-audit.json
```

## Result

All four complete fresh-scale sweeps pass signed dominance:

```text
M=229  prime rows 39  weakest p=379  label (00,12)  slack 0.40189096624031384
M=251  prime rows 42  weakest p=379  label (00,12)  slack 0.43435333637430296
M=293  prime rows 45  weakest p=461  label (00,12)  slack 0.4257305726250574
M=331  prime rows 55  weakest p=599  label (00,12)  slack 0.40479256047704726
```

The fixed-prime rule fails:

```text
weakest prime counts:
379 -> 2
461 -> 1
599 -> 1
```

But two patterns survive the four complete sweeps:

```text
weakest label is always (00,12)
tightest four rows always form one coherent prime block
```

For example, the tightest `M=331` block is:

```text
p=599  (00,12)  slack 0.40479256047704726
p=599  TOTAL    slack 0.40554758560116755
p=599  (01,11)  slack 0.4056228223122137
p=599  (01,02)  slack 0.40577058624032636
```

## Decision

The evidence supports prime-block stress tracking, not a single fixed-prime
predictor.  The next theorem-shaped target is:

```text
source-start prime-block lower-frame control
```

Mechanism: bound the source-start active/full ratio first by prime block, then
treat component labels as a secondary spread inside each block.

Prediction: the next complete source-start sweep should either produce a new
coherent prime block of weak rows, or expose the first split-block falsifier.

Falsifier: a future complete scale whose tightest rows are split across
unrelated primes, or whose weakest row is an isolated component far below its
prime companions.

This is a finite morphology audit only.  It proves no prime-block theorem, no
source-start theorem, no source-window theorem, no strict-central Goldbach
theorem, and no Goldbach proof.

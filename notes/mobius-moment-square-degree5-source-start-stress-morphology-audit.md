# Mobius moment-square degree-5 source-start stress morphology audit

## Question

After the full `M=379` sweep preserved the `p=599` stress block, what should
guide the next source-start target: a fixed attention prime, a component label,
endpoint position, or a prime-level stress block?

## Mechanism

Read the complete fresh-scale source-start sweeps:

```text
M=229
M=251
M=293
M=331
M=353
M=379
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

All six complete fresh-scale sweeps pass signed dominance:

```text
M=229  prime rows 39  weakest p=379  label (00,12)  slack 0.40189096624031384
M=251  prime rows 42  weakest p=379  label (00,12)  slack 0.43435333637430296
M=293  prime rows 45  weakest p=461  label (00,12)  slack 0.4257305726250574
M=331  prime rows 55  weakest p=599  label (00,12)  slack 0.40479256047704726
M=353  prime rows 56  weakest p=599  label (00,12)  slack 0.41096324474219414
M=379  prime rows 60  weakest p=599  label (00,12)  slack 0.4246854972346972
```

The fixed-prime rule fails:

```text
weakest prime counts:
379 -> 2
461 -> 1
599 -> 3
```

But two patterns survive the six complete sweeps:

```text
weakest label is always (00,12)
tightest four rows always form one coherent prime block
```

For example, the tightest `M=379` block is:

```text
p=599  (00,12)  slack 0.4246854972346972
p=599  TOTAL    slack 0.42504843582069374
p=599  (01,11)  slack 0.42506099800075414
p=599  (01,02)  slack 0.42520294413353943
```

## Decision

The evidence supports prime-block stress tracking, not a single fixed-prime
predictor.  The next theorem-shaped target is:

```text
source-start prime-block lower-frame control
```

Mechanism: bound the source-start active/full ratio first by prime block, then
treat component labels as a secondary spread inside each block.

Prediction: the next complete source-start sweep, likely `M=383` or larger,
should either produce a new coherent prime block of weak rows, preserve the
current `p=599` diagnostic, or expose the first split-block falsifier.

Falsifier: a future complete scale whose tightest rows are split across
unrelated primes, or whose weakest row is an isolated component far below its
prime companions.

The prime `p=599` now persists across `M=331`, `M=353`, and `M=379`, but it is
still a finite current diagnostic rather than a fixed-prime rule.

This is a finite morphology audit only.  It proves no prime-block theorem, no
source-start theorem, no source-window theorem, no strict-central Goldbach
theorem, and no Goldbach proof.

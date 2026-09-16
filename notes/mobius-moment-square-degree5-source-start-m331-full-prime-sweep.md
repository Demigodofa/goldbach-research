# Mobius moment-square degree-5 source-start M=331 full prime sweep

## Question

The `M=331` sentinel audit survived, but its checked primes were too sparse to
promote a full-scale conclusion.  Does the complete canonical source-start
prime interval `[331, 662]` survive, and was the sentinel weak row `p=461`
actually global?

## Mechanism

The runner computes every prime `p` in `[331, 662]` using the original
source-start construction:

```text
row_count = int((331**(1/.59))**.41) = 56
ell_freeze = row_count + row_count//2 = 84
canonical source start = row_count = 56
```

The row condition remains:

```text
full < 0 and active/full > 1/2
```

Because each row is expensive, the builder writes a partial checkpoint after
each prime row and resumes from the completed prefix if interrupted.

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_start_m331_full_prime_sweep.py
evidence/mobius-moment-square-degree5-source-start-m331-full-prime-sweep.json
```

## Result

```text
scale:                            331
prime interval:                   331..662
prime rows checked:               55
component rows:                   165
degree-5 total rows:              55
dominance rows:                   220
all rows pass signed dominance:   true
minimum slack above one half:     0.40479256047704726
weakest row:                      M=331, p=599, (00,12)
weakest active/full ratio:        0.9047925604770473
p=461 weakest-row slack:          0.4702648688514812
total elapsed seconds:            1998.0527602999937
resumable runner used:            true
checkpoint removed after success: true
```

The four tightest prime/component rows are:

```text
p=599  (00,12)  ratio 0.9047925604770473  slack 0.40479256047704726
p=599  TOTAL    ratio 0.9055475856011675  slack 0.40554758560116755
p=599  (01,11)  ratio 0.9056228223122137  slack 0.4056228223122137
p=599  (01,02)  ratio 0.9057705862403264  slack 0.40577058624032636
```

The next non-`599` stress primes are `647`, `347`, and `479`; all still have
positive slack.

## Decision

The full `M=331` source-start prime-row sweep survives.  This promotes
`M=331` from sentinel evidence to one complete finite fresh-scale sweep.

The full sweep also downgrades the sentinel interpretation: `p=461` is not
the global weak row at `M=331`.  The true weakest checked row is `p=599`,
component `(00,12)`.  Future source-start stress tracking should include the
high-tail interior cluster around `p=599` and `p=647`, not only the earlier
`p=379`/`p=461` attention primes.

This is finite evidence only.  It is not a source-start theorem, not a
source-window theorem, not a strict-central Goldbach theorem, and not a
Goldbach proof.

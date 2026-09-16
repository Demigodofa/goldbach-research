# Mobius moment-square degree-5 source-start M=293 full prime sweep

## Question

The full sweeps for `M=229` and `M=251` survived, and the fixed-prime audit
made `p=379` a lower-scale attention point.  Does the next fresh scale,
`M=293`, also survive when every prime `p` in `[293, 586]` is checked at the
canonical source start, and is the weakest row still near `p=379`?

## Mechanism

For `M=293`, use the original source-start construction:

```text
row_count = int((293**(1/.59))**.41) = 51
ell_freeze = row_count + row_count//2 = 76
canonical source start = row_count = 51
```

Then compute the three degree-5 component rows and the degree-5 total row for
every prime `p` in `[293, 586]`, testing:

```text
full < 0 and active/full > 1/2
```

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_start_m293_full_prime_sweep.py
evidence/mobius-moment-square-degree5-source-start-m293-full-prime-sweep.json
```

## Result

```text
scale:                            293
prime interval:                   293..586
prime rows:                       45
component rows:                   135
degree-5 total rows:              45
dominance rows:                   180
all rows pass signed dominance:   true
minimum slack above one half:     0.4257305726250574
weakest row:                      M=293, p=461, (00,12)
weakest active/full ratio:        0.9257305726250574
maximum slack above one half:     0.6453957570433406
p=379 weakest-row slack:          0.4715916000491919
```

The checked primes are:

```text
293, 307, 311, 313, 317, 331, 337, 347, 349,
353, 359, 367, 373, 379, 383, 389, 397, 401,
409, 419, 421, 431, 433, 439, 443, 449, 457,
461, 463, 467, 479, 487, 491, 499, 503, 509,
521, 523, 541, 547, 557, 563, 569, 571, 577
```

## Decision

The full `M=293` prime-row source-start sweep survives.  This gives three
complete fresh scales beyond the original fixture: `M=229`, `M=251`, and
`M=293`.

The sweep also downgrades the `p=379` attention point as a controlling stress
channel at this scale.  The global weakest row moves to `p=461`, component
`(00,12)`, while `p=379` remains positive with a larger slack.  So `p=379`
is useful lower-scale stress evidence, not a durable predictor of the weakest
row across all nearby scales.

This is still finite evidence only.  It is not a source-start theorem, not a
source-window theorem, and not a Goldbach proof.

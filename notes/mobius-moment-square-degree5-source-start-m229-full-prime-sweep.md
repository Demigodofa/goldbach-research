# Mobius moment-square degree-5 source-start M=229 full prime sweep

## Question

The fresh prime-span holdout showed that an interior sampled row,
`M=229`, `p=347`, was weaker than the first-prime rows.  Does the whole
fresh `M=229` canonical source-start scale survive when every prime
`p` in `[229, 458]` is checked?

## Mechanism

For `M=229`, use the original source-start construction:

```text
row_count = int((229**(1/.59))**.41) = 43
ell_freeze = row_count + row_count//2 = 64
canonical source start = row_count = 43
```

Then compute the three degree-5 component rows and the degree-5 total row for
every prime `p` in `[229, 458]`, testing:

```text
full < 0 and active/full > 1/2
```

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_start_m229_full_prime_sweep.py
evidence/mobius-moment-square-degree5-source-start-m229-full-prime-sweep.json
```

## Result

```text
scale:                            229
prime interval:                   229..458
prime rows:                       39
component rows:                   117
degree-5 total rows:              39
dominance rows:                   156
all rows pass signed dominance:   true
minimum slack above one half:     0.40189096624031384
weakest row:                      M=229, p=379, (00,12)
weakest active/full ratio:        0.9018909662403138
maximum slack above one half:     0.6203257748420008
```

The checked primes are:

```text
229, 233, 239, 241, 251, 257, 263, 269, 271, 277,
281, 283, 293, 307, 311, 313, 317, 331, 337, 347,
349, 353, 359, 367, 373, 379, 383, 389, 397, 401,
409, 419, 421, 431, 433, 439, 443, 449, 457
```

## Decision

The full `M=229` prime-row source-start sweep survives.  This is stronger than
the low/mid/high span sample because it checks every prime row in the first
fresh scale beyond the original checked fixture.  The new weakest row is
`p=379`, not one of the sampled low/mid/high rows, so future source-start work
should treat interior-prime search as evidence-bearing.

This remains one finite scale only.  It is not a source-start theorem, not a
source-window theorem, and not a Goldbach proof.

# Mobius moment-square degree-5 source-start fresh prime-span holdout

## Question

The fresh first-prime-row holdout passed, but that could be a low-prime-row
artifact.  Do fresh canonical source-start rows still pass when each fresh
scale samples low, mid, and high prime rows?

## Mechanism

For each fresh scale `M` in `229`, `251`, and `293`, select:

```text
low  = first prime p in [M, 2M]
mid  = prime p in [M, 2M] closest to floor(3M/2), lower prime on ties
high = last prime p in [M, 2M]
```

Use the original source-start construction:

```text
row_count = int((M**(1/.59))**.41)
ell_freeze = row_count + row_count//2
canonical source start = row_count
```

Then compute the three degree-5 component rows and the degree-5 total row, and
test the same signed active/full condition:

```text
full < 0 and active/full > 1/2
```

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_start_fresh_prime_span_holdout.py
evidence/mobius-moment-square-degree5-source-start-fresh-prime-span-holdout.json
```

## Result

```text
fresh scales:                     229, 251, 293
prime rows:                       9
component rows:                   27
degree-5 total rows:              9
dominance rows:                   36
all rows pass signed dominance:   true
minimum slack above one half:     0.44127127965726143
weakest row:                      M=229, p=347, (00,12)
weakest active/full ratio:        0.9412712796572614
```

Selected prime rows:

```text
M=229: low 229, mid 347, high 457
M=251: low 251, mid 373, high 499
M=293: low 293, mid 439, high 577
```

## Decision

The fresh prime-span source-start holdout survives.  This is stronger than the
first-prime-only holdout because it samples interior and upper prime rows in
each fresh scale.  The mid row `M=229`, `p=347` is the new weakest sample, so
future source-start work should not assume the first prime row is worst.

This remains finite evidence only.  It is not a full fresh-scale sweep, not a
source-start theorem, and not a Goldbach proof.

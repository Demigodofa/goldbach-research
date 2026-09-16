# Mobius moment-square degree-5 source-start fresh prime-row holdout

## Question

After the translated start-`1` puncture was proved unreachable from the
original source mapping, does the narrowed canonical source-start lane survive
fresh scales beyond the six checked scales?

## Mechanism

For each fresh scale `M` in `229`, `251`, and `293`, take the first prime row
`p >= M` and use the original source-start construction:

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
tools/build_mobius_moment_square_degree5_source_start_fresh_prime_row_holdout.py
evidence/mobius-moment-square-degree5-source-start-fresh-prime-row-holdout.json
```

## Result

```text
fresh scales:                     229, 251, 293
prime rows:                       3
component rows:                   9
degree-5 total rows:              3
dominance rows:                   12
all rows pass signed dominance:   true
minimum slack above one half:     0.49593901217024683
weakest row:                      M=251, p=251, (01,02)
weakest active/full ratio:        0.9959390121702468
```

## Decision

The fresh first-prime-row source-start holdout survives.  This is useful
because it tests the narrowed reachable lane after the unreachable start-`1`
puncture, rather than spending more proof effort on a translated start that the
source construction does not produce.

This is still a thin finite holdout only.  It is not a full fresh-scale sweep,
not a source-start theorem, and not a Goldbach proof.

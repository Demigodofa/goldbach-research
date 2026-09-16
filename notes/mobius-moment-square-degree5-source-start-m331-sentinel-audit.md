# Mobius moment-square degree-5 source-start M=331 sentinel audit

## Question

The full `M=293` sweep survived and moved the weakest row from the earlier
`p=379` attention point to `p=461`.  Before paying for a long opaque full
`M=331` sweep, do bounded sentinel rows at `M=331` survive, and does `p=461`
remain locally tight?

## Mechanism

For `M=331`, the full prime interval is `[331, 662]` and contains `55` primes.
In the current endpoint-frame implementation, one `M=331` row takes about
`30` to `40` seconds, so the full sweep needs progress and resume support
before promotion.

This finite sentinel audit checks:

```text
low       p=331
attention p=461
mid       p=499
high      p=661
```

Each row uses the original source-start construction:

```text
row_count = int((331**(1/.59))**.41) = 56
ell_freeze = row_count + row_count//2 = 84
canonical source start = row_count = 56
```

The row condition remains:

```text
full < 0 and active/full > 1/2
```

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_start_m331_sentinel_audit.py
evidence/mobius-moment-square-degree5-source-start-m331-sentinel-audit.json
```

## Result

```text
scale:                            331
prime interval:                   331..662
sentinel prime rows:              4
component rows:                   12
degree-5 total rows:              4
dominance rows:                   16
all rows pass signed dominance:   true
minimum slack above one half:     0.4702648688514812
weakest sentinel row:             M=331, p=461, (00,12)
weakest active/full ratio:        0.9702648688514812
total elapsed seconds:            142.65569730001152
full sweep completed:             false
```

Selected row timings:

```text
p=331  low        38.88259449999896 seconds
p=461  attention  36.39864269999089 seconds
p=499  mid        36.55819939999492 seconds
p=661  high       30.81600210000761 seconds
```

## Decision

The `M=331` sentinel audit survives, and the `p=461` attention row is the
tightest row among the bounded sentinel set.  This supports `p=461` as a
local stress marker worth checking in a future full `M=331` sweep.

This is not a full `M=331` sweep.  A full sweep over all `55` primes in
`[331, 662]` remains open and should use a progress-logged/resumable runner
before promotion.  This is finite sentinel evidence only, not a source-start
theorem, not a source-window theorem, and not a Goldbach proof.

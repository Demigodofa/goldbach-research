# Mobius moment-square degree-5 source-start M379 full prime sweep

## Question

After the five-scale morphology audit identified `M=379` as the next finite
prime-block falsifier, do all canonical source-start prime rows in `[379,758]`
survive signed dominance, and do the tightest rows remain a coherent prime
block?

## Mechanism

Use the canonical source-start construction:

```text
canonical source start = row_count
row_count = int((M**(1/.59))**.41) = 61
ell_freeze = row_count + row_count//2 = 91
```

For every prime `p` in `[379,758]`, compute the three degree-5 component rows
and the degree-5 total row at the canonical source start.  The sweep writes a
partial checkpoint after each completed row and can resume.

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_start_m379_full_prime_sweep.py
evidence/mobius-moment-square-degree5-source-start-m379-full-prime-sweep.json
```

## Result

```text
status:                         SWEEP_degree5_source_start_m379_full_prime_rows
scale:                          379
prime interval:                 379..758
prime rows checked:             60
component rows:                 180
degree-5 total rows:            60
dominance rows:                 240
all rows pass signed dominance: true
minimum slack above one half:   0.4246854972346972
weakest row:                    M=379, p=599, (00,12)
weakest active/full ratio:      0.9246854972346972
tightest prime block:           p=599
```

The tightest block is:

```text
p=599  (00,12)  slack 0.4246854972346972
p=599  TOTAL    slack 0.42504843582069374
p=599  (01,11)  slack 0.42506099800075414
p=599  (01,02)  slack 0.42520294413353943
```

The next tightest prime blocks are:

```text
p=727  weakest (01,02)  slack 0.4279439424781626
p=691  weakest (00,12)  slack 0.43200116006753375
p=659  weakest (00,12)  slack 0.44140799509911166
```

## Decision

The next finite morphology falsifier did not fire.  The full `M=379` sweep
survives signed dominance, and the tightest four rows remain a coherent
`p=599` prime block.  This strengthens the current finite diagnostic that
`p=599` controls the tightest prime block across `M=331`, `M=353`, and
`M=379`.

This is still finite sweep evidence only.  It proves no fixed-prime rule, no
prime-block theorem, no source-start theorem, no source-window theorem, no
strict-central Goldbach theorem, and no Goldbach proof.

# Mobius moment-square degree-5 source-start M=353 full prime sweep

## Question

The stress-morphology audit across `M=229`, `251`, `293`, and `331` suggested
that the right finite object is a coherent prime block rather than a fixed
attention prime.  Does the next fresh full sweep, `M=353`, preserve signed
dominance and the prime-block morphology?

## Mechanism

The runner computes every prime `p` in `[353, 706]` using the original
source-start construction:

```text
row_count = int((353**(1/.59))**.41)
ell_freeze = row_count + row_count//2
canonical source start = row_count
```

The row condition remains:

```text
full < 0 and active/full > 1/2
```

The builder writes a partial checkpoint after each prime row and resumes from
the completed prefix if interrupted.  It also records prior stress-prime
diagnostics for `379`, `461`, `599`, and `647`.

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_start_m353_full_prime_sweep.py
evidence/mobius-moment-square-degree5-source-start-m353-full-prime-sweep.json
```

## Result

```text
scale:                            353
prime interval:                   353..706
prime rows checked:               56
component rows:                   168
degree-5 total rows:              56
dominance rows:                   224
all rows pass signed dominance:   true
minimum slack above one half:     0.41096324474219414
weakest row:                      M=353, p=599, (00,12)
weakest active/full ratio:        0.9109632447421941
total elapsed seconds:            1924.4648416000127
resumable runner used:            true
checkpoint removed after success: true
```

The tightest prime blocks are:

```text
p=599  min slack 0.41096324474219414  labels (00,12), TOTAL, (01,11), (01,02)
p=691  min slack 0.42344857003531877  labels (00,12), TOTAL, (01,11), (01,02)
p=647  min slack 0.42860074504794     labels (00,12), TOTAL, (01,02), (01,11)
p=601  min slack 0.44223687010496004  labels (00,12), TOTAL, (01,11), (01,02)
```

Prior stress-prime diagnostics:

```text
p=379  weakest slack 0.497583046646055
p=461  weakest slack 0.4749215357712916
p=599  weakest slack 0.41096324474219414
p=647  weakest slack 0.42860074504794
```

## Decision

The full `M=353` source-start sweep survives.  It also supports the finite
prime-block morphology: the top four stress rows form one coherent `p=599`
block containing `(00,12)`, `TOTAL`, `(01,11)`, and `(01,02)`.

This is the first prospective check after the morphology audit, and it did not
produce the split-block falsifier.  Fixed-prime tracking remains downgraded
for `p=379` and `p=461`; `p=599` persists from `M=331` to `M=353` as the
tightest prime block.

This is finite evidence only.  It is not a prime-block theorem, not a
source-start theorem, not a source-window theorem, not a strict-central
Goldbach theorem, and not a Goldbach proof.

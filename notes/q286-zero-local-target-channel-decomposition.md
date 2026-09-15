# q286 zero-local target channel decomposition

Status: finite 12-target channel decomposition.  This is not a proof of a
binary-prime correlation theorem, a signed projection theorem, or Goldbach.

## Correction

The `12` cases in the local singular audit are target integers, not `12`
neutral channels.  They are the far stress rows where the local LP action is
zero but the empirical LP delta is positive.

The generated evidence is:

```text
evidence/q286-zero-local-target-channel-decomposition.json
```

The builder is:

```text
tools/build_q286_zero_local_target_channel_decomposition.py
```

## Targets

The `12` zero-local target integers are:

```text
6000032, 6000058, 8000030, 8000056, 10000028, 10000054,
12000026, 12000052, 16000022, 16000048, 20000018, 20000044
```

They occupy two zero-local residues:

```text
N mod 143 = 38 or 64
```

For each target, the audit subtracts the stored local stress-relative delta
vector for its residue, then decomposes the remaining empirical vector across
all `17` outside labels.

## Result

The local vectors are numerical zero at this scale, but the after-local
empirical vectors remain positive in both total outside sum and LP-weighted
sum:

```text
all after-local full sums positive: true
all after-local LP sums positive:   true
minimum after-local full sum:       0.183333351766597
minimum after-local LP sum:         0.134489398894505
```

The channel-level decomposition is signed, not all-positive:

```text
after-local channel entries: 204
positive entries:            138
negative entries:            66
zero entries:                0
minimum entry:              -0.0239537756244868
```

Per-row summary:

```text
target    mod143  after-local full  after-local LP  pos  neg
6000032   38      0.210617303       0.134489399     12   5
6000058   64      0.261789147       0.176334240     11   6
8000030   38      0.183333352       0.137906700     12   5
8000056   64      0.239996654       0.164014818     12   5
10000028  38      0.244904419       0.172202135     11   6
10000054  64      0.244410858       0.170118071     11   6
12000026  38      0.247803362       0.161293803     11   6
12000052  64      0.221978898       0.144981832     11   6
16000022  38      0.257541442       0.153648102     11   6
16000048  64      0.245944022       0.153803127     12   5
20000018  38      0.249149582       0.153402551     12   5
20000044  64      0.244253950       0.152515796     12   5
```

The most common worst negative channel is `(3,5)`.  The largest LP-weighted
positive contributor is usually `(5,5)`, with occasional `(3,1)` or `(3,11)`.

## Interpretation

This confirms the local-singular audit's boundary in the intended form:

```text
local contribution = numerical zero
empirical after-local 17-channel vector = positive in full and LP projection
```

The positive mass is therefore not supplied by local admissible support.  It is
a signed balance across the actual prime-pair/correlation deltas in the `17`
outside channels.

## Boundary

This is finite evidence on the `12` zero-local far targets only.  It does not
prove that the same channel balance holds universally, and it does not prove a
fixed-modulus binary Goldbach-in-progressions theorem.

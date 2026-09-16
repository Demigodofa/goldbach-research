# Mobius moment-square degree-5 fixed-prime horizon obstruction

## Question

Can the persistent finite `p=599` stress diagnostic be promoted into a
fixed-prime theorem target for all sufficiently large source scales `M`?

## Mechanism

Use the elementary interval condition for the source-start prime block:

```text
p in [M, 2M]
```

For a fixed prime `p0`, this holds exactly when:

```text
ceil(p0 / 2) <= M <= p0
```

So every fixed prime has a finite admissible scale horizon.

## Receipt

```text
tools/build_mobius_moment_square_degree5_fixed_prime_horizon_obstruction.py
evidence/mobius-moment-square-degree5-fixed-prime-horizon-obstruction.json
```

## Result

The seven-scale morphology audit has weakest prime counts:

```text
379 -> 2
461 -> 1
599 -> 4
```

The persistent observed `p=599` weak scales are:

```text
331, 353, 379, 383
```

But the exact fixed-prime horizon is:

```text
p=599 admissible integer scales: 300..599
first impossible integer scale:  600
```

Calculation:

```text
p=599 in [M,2M]
iff M <= 599 <= 2M
iff ceil(599/2)=300 <= M <= 599
```

## Decision

`p=599` remains useful finite morphology, but it cannot be a universal
fixed-prime theorem target.  Any sufficiently-large source-start theorem must
either control every prime block `p in [M,2M]` or control a moving stress block
`p=p(M)`.

This proves only the elementary fixed-prime horizon obstruction.  It proves no
moving-prime theorem, prime-block theorem, source-start theorem, strict-central
Goldbach theorem, or Goldbach proof.

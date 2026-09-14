# q286 Frobenius lattice claim audit

Status: finite audit of a pasted rank-`1` explanation.  This is not a proof
of Goldbach, a replacement rank-`1` theorem, or a residual-drag theorem.

## Purpose

Kevin pasted a candidate claiming that the q286 rank-`1` outside direction is
arithmetically forced by:

```text
Frobenius coin structure
gcd(17, 120) = 1
parity/conjugacy on C10 x C12
ray-class or cyclotomic unit-group rank
```

The generated evidence is:

```text
evidence/q286-frobenius-lattice-claim-audit.json
```

The builder is:

```text
tools/build_q286_frobenius_lattice_claim_audit.py
```

## Accepted Part

The underlying character setting is real:

```text
q = 286 = 2 * 11 * 13
phi(q) = 120
(Z/286Z)^* ~= C10 x C12
```

The current outside-channel audit uses `17` folded real character-channel
labels, and the removed volatile set has `8` labels.

## Rejected Parts

The Frobenius formula in the pasted claim is not a standard Frobenius-number
calculation:

```text
286 * (1/2 - 1/17) = 126.17647058823529
```

For comparison:

```text
g(2, 17)   = 15
g(17, 286) = 4559
g(286)     is not defined as a one-denomination Frobenius number
```

This supplies no rank-`1` vector and no residual-drag inequality.

The `gcd(17,120)=1` observation is also not a rank theorem.  It says only that
the selected count has no common divisor with the character-group order.  It
does not define a projection, a coefficient vector, or a singular direction.

Parity is not a discriminator here.  All `17` outside labels and all `8`
volatile labels have even `a+b` parity:

```text
outside even parity count:  17/17
volatile even parity count: 8/8
all even parity count:      25/25
```

The existing numeric dictionary audit also rejects parity-like explanations as
the observed rank-`1` direction:

```text
constant-sum rank1 cosine:        0.5129804484842019
edge/parity lift rank1 cosine:    0.5798423118379537
Gemini Legendre-sign rank1 cosine 0.3552346438331256
Gemini Legendre-sign mismatches:  11/17
```

The ray-class/unit-rank language in the pasted claim is not a valid bridge to
the observed `17`-channel vector.  For `Q(zeta_286)`, the Dirichlet unit rank
is `59`, not `119`, because the field has no real embeddings and `60` complex
pairs.

## Decision

Reject the Frobenius/common-divisor/parity explanation as stated.  The true
`C10 x C12` character-lattice structure remains relevant, but it does not by
itself force the observed q286 rank-`1` outside direction.

The surviving route remains:

```text
low-frequency label-lattice finite signal
+ actual character-sum magnitudes or row-dependent signed cone
+ residual-drag inequality
```

## Boundary

This closes one tempting shortcut.  It proves no universal no-go for richer
arithmetic lifts, no low-frequency theorem, no signed projection theorem, and
no Goldbach theorem.

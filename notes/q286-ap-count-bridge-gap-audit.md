# q286 AP-count bridge gap audit

Status: finite combinatorial falsifier for one bridge shortcut.  This is not
a proof of Goldbach, not a binary Goldbach-in-progressions theorem, and not a
criticism of the Bennett-Martin-O'Bryant-Rechnitzer AP bounds.

## Purpose

The previous local singular audit pinned useful q286 AP constants from BMOR
and showed that the frozen LP vector has nonnegative local admissible-cone
orientation.  The remaining question is whether raw AP prime-count lower
bounds can bridge that local support into an actual prime-pair or signed
`17`-channel statement.

This audit tests the simplest possible bridge:

```text
Can AP count floors alone force an intersection between primes p in one
residue class and reflected primes N-p in the complementary residue class?
```

The generated evidence is:

```text
evidence/q286-ap-count-bridge-gap-audit.json
```

The builder is:

```text
tools/build_q286_ap_count_bridge_gap_audit.py
```

## Mechanism

Fix a residue class `r mod 286`.  A Goldbach pair in this residue-pair channel
is an intersection between two subsets of the same residue-slot universe:

```text
A = {p <= N : p prime, p == r mod 286}
B = {p <= N : N-p prime, p == r mod 286}
```

AP theorems give marginal lower bounds for `|A|` and `|B|`.  But marginal
counts force an intersection only if:

```text
lower(|A|) + lower(|B|) > slot_count
```

If instead `2*ceil(lower) <= slot_count`, then two disjoint subsets can satisfy
the same AP marginals while producing zero Goldbach pairs in that residue
channel.  That is a count-only countermodel.

## Result

The raw count-only bridge fails throughout the valid q286 BMOR range.

For BMOR Corollary 1.6:

```text
pi(x;286,a) > x/(phi(286)*log x)
valid from x >= 50*286^2 = 4,089,800
```

The count-only pigeonhole ratio is:

```text
2q/(phi(q)*log x)
```

For `q=286`, that ratio exceeds `1` only for:

```text
x < exp(2*286/120) = 117.526832200411...
```

This is far below the valid threshold `4,089,800`.

At the simple Corollary 1.6 threshold:

```text
x = 4,089,800
lower count per reduced residue: 2238.6791796366165
largest residue-slot count:      14300
two marginal integer floors:     4478
unused slot capacity:            9822
ratio:                           0.31310198316596033
```

At the q-specific BMOR `pi` threshold:

```text
x = 86,891,851
BMOR lower count per residue:    37896.58859682715
largest residue-slot count:      303818
two marginal integer floors:     75794
unused slot capacity:            228024
ratio:                           0.24946901498151622
```

A log-spaced sample from `x_pi=86,891,851` through `1e40` found its largest
BMOR q-specific ratio at the left endpoint, still only about `0.249469`.

## Decision

Demote the raw AP-count pigeonhole bridge.  The AP count floors are simply too
sparse to force a reflected residue-pair collision by marginal counts alone.

This is not surprising: primes in a single q286 residue class have density
around `q/(phi(q)*log x)` inside their residue-slot universe.  Two such sparse
sets can easily be disjoint without violating either marginal count.

## What Survives

BMOR remains useful source-backed endpoint data:

```text
c_pi = 0.0008772, x_pi = 86,891,851
c_psi = 0.0008379, x_psi = 85,882,271
c_theta = 0.0008411, x_theta = 85,881,413
```

The failed conjunction is only:

```text
BMOR AP counts + pigeonhole marginals alone => q286 prime-pair/sign bridge
```

A viable bridge must use more structure: binary convolution, character-sum
correlation, dispersion, circle-method major/minor arc control, or a
coefficient-specific signed estimate for the actual `17`-channel functional.

## Boundary

This audit closes one tempting lower-bound shortcut.  It does not rule out AP
methods, singular-series methods, BMOR-style endpoint inputs, character sums,
dispersion, or a future q286 convolution theorem.  It proves no uniform
Goldbach result.

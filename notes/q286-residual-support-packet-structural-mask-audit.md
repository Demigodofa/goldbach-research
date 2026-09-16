# q286 residual support-packet structural-mask audit

Status: finite theorem-budget audit.  This is not a structural-mask theorem,
support-packet theorem, character-sum theorem, signed binary-prime correlation
theorem, q286 threshold theorem, strict-central Goldbach theorem, or Goldbach
proof.

## Question

The minimal five-packet rescue core is unique but near-sharp.  Is it a
support-lattice structure that a theorem might naturally see, or is it a
hand-selected finite mask?

## Mechanism

Represent each support packet by four Boolean factors:

```text
5, 7, 11, 13
```

Enumerate simple support-lattice masks:

```text
one-subcube DNF
two-subcube DNF
three-subcube DNF
support-size threshold masks
```

For each mask `M`, test

```text
aligned(N) + sum_{g in M} A_g(N)
  - sum_{h not in M} sup_positive_rows max(0, -A_h) > 0
```

on the five actual full-positive frozen rows.

## Receipt

```text
tools/build_q286_residual_support_packet_structural_mask_audit.py
evidence/q286-residual-support-packet-structural-mask-audit.json
```

## Result

The unique five-packet finite rescue core is not closure-natural:

```text
downward closure violations: 5
upward closure violations:  16
five-core tight margin:     0.0005798995134771445
```

No nontrivial one-subcube mask certifies all five positive rows.  The only
one-subcube certificate is the full `15`-packet mask.

A two-subcube structural mask does certify:

```text
(7=0 and 11=1) OR (11=0 and 13=0)
```

It keeps seven packets:

```text
11
11x13
5
5x11
5x11x13
5x7
7
```

Its tight row is again `94856`:

```text
tight margin:                  0.005504640544899547
relative mask budget:          0.09076413199496625
tail adverse envelope:         0.16918918294282279
```

The more symmetric support-size threshold

```text
support size <= 2
```

also certifies:

```text
mask size:                     10
tight margin:                  0.004018492886067315
relative mask budget:          0.022998983525494825
tail adverse envelope:         0.04969241094998337
```

## Decision

The next finite theorem-shaped object should not be the unique five-packet
core.  It is too closure-unnatural and too near-sharp.  A broader structural
support-lattice mask is more plausible:

```text
(7=0 and 11=1) OR (11=0 and 13=0)
```

or, more symmetrically but with a smaller relative budget:

```text
support size <= 2.
```

This is still finite evidence only.  The adverse tail is fitted to the five
positive rows, and no source-backed signed binary-prime correlation estimate
has been proved.  The next proof object is a source theorem for a structural
support-lattice mask plus a universal adverse-tail estimate, or else a broader
signed support-packet package.  Goldbach remains open.

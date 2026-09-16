# q286 residual support-packet rescue-core audit

Status: finite theorem-budget audit.  This is not a rescue-core theorem,
support-packet theorem, character-sum theorem, signed binary-prime correlation
theorem, q286 threshold theorem, strict-central Goldbach theorem, or Goldbach
proof.

## Question

The support-packet audit showed that a `15`-packet signed dictionary is much
smaller than the full `2880`-character triangle route, but that adverse-only
packet envelopes fail on the tight row.

Can an even smaller fixed signed rescue core certify the positive rows if every
omitted packet is paid by a finite adverse-tail envelope?

## Mechanism

For a fixed packet core `C`, test

```text
aligned(N) + sum_{g in C} A_g(N)
  - sum_{h not in C} sup_positive_rows max(0, -A_h) > 0
```

on the five actual full-positive frozen rows.

The core is brute-forced over all subsets of the `15` support packets.  No row
dependent core is allowed.

## Receipt

```text
tools/build_q286_residual_support_packet_rescue_core_audit.py
evidence/q286-residual-support-packet-rescue-core-audit.json
```

## Result

No fixed core of size `0`, `1`, `2`, `3`, or `4` certifies all five positive
rows.  Exactly one fixed size-`5` core certifies them:

```text
11x13
5
5x7
5x7x13
7
```

Its tight row is again `94856`:

```text
aligned action:                 0.1140460717392141
core signed action:             0.05669981666180788
tail adverse envelope:          0.17016598888754483
rescue-core margin:             0.0005798995134771445
relative core budget:           0.010227537717379533
tail packet count:              10
```

The best margins by core size through `5` are:

```text
size 0: -0.09568220367997388
size 1: -0.043441542406603334
size 2: -0.028831757055877733
size 3: -0.015763885936926042
size 4: -0.004182077772250659
size 5:  0.0005798995134771445
```

## Decision

The rescue-core structure is real enough to preserve, but not robust enough to
promote.  It narrows the signed packet route to a possible theorem of the form:

```text
lower-bound the fixed positive rescue core
and upper-bound the omitted adverse packet tail.
```

However, the certificate is near-sharp and finite-fit.  The omitted-tail
envelope is fitted to the five positive checked rows, and the tight row leaves
only about `0.00058` absolute margin, or about `1.02%` relative room on the
core.  This is not materially safer than the earlier near-sharp routes unless
the core packets have a source-backed reason to be lower-bounded and the tail
has a universal adverse estimate.

The next proof object is either a source-backed lower bound for this five-packet
rescue core plus a universal adverse-tail bound, or a broader signed
support-packet package.  Goldbach remains open.

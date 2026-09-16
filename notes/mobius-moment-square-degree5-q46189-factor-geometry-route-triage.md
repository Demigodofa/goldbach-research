# Mobius moment-square degree-5 Q46189 factor-geometry route triage

## Question

After the `50A..60A` selector is demoted and low-order bucket
co-occurrence fails, which source/factor geometry signals remain
useful for the `Q=46189` overpayment-exclusion route?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_factor_geometry_route_triage.py
evidence/mobius-moment-square-degree5-q46189-factor-geometry-route-triage.json
```

## Result

```text
row count:                                  35
all-high/no-small rows:                     1
replacement rows:                           34
all replacement rows keep surplus:          True
Q=46189 raw scalar:                         -0.07475328212536138
raw-scalar false positives:                 7
most negative raw-scalar denominator:       67830
most negative raw scalar:                   -0.08346040426201057
weakest replacement denominator:            38038
weakest replacement off/diag-half:          -0.8472931845861708
weakest middle A..10A contribution:         -0.939992990438763
weakest non-middle compensation:            0.09269980585259228
weakest margin above -1:                    0.15270681541382924
```

## Decision

The all-high/no-small factor packet is the finite separator in this
landscape, but that is only a route locator, not a theorem.  It
identifies the natural class split: the adverse packet is
`11*13*17*19`, while the checked replacement packets contain small
prime support.

A scalar source-pair coefficient does not explain the boundary.
Several nonadverse packets have raw scalar at least as negative as
`Q=46189`; the most negative raw-scalar row is `q=67830`, which
still stays far above the `-1` kernel boundary.

The tight survivor `q=38038` is the useful theorem target.  It has a
large adverse `middle_A_to_10A` contribution, but near/far/tail
terms compensate enough to keep the total at
`-0.8472931845861708`.  The next theorem-shaped route is therefore
replacement-packet bucket compensation, beginning with symbolic
`q=38038` versus `Q=46189` source-conductor terms.

This is finite diagnostic evidence only.  It proves no factor
separator theorem, scalar coefficient theorem, replacement-packet
compensation theorem, strict-central Goldbach theorem, or Goldbach
proof.

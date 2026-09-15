# q286 far singleton channel stability audit

Status: finite replay over the original far-stress fixture.  This is not a
proof of a singleton-channel theorem, distributed cone theorem, binary-prime
correlation theorem, signed projection theorem, or Goldbach.

## Source

The generated audit is:

```text
evidence/q286-far-singleton-channel-stability-audit.json
```

The builder is:

```text
tools/build_q286_far_singleton_channel_stability_audit.py
```

It uses the same stress reference as the previous q286 audits:

```text
stress target = 1222142
```

For each far target, the audit subtracts the target residue's local vector and
then measures each outside channel by:

```text
lp_effective_weight * after_local_delta
```

## Scopes

The audit keeps the scope split explicit:

```text
seed zero-local targets:       12
other non-seed far targets:   594
all far clear targets:        606
```

The `12` seed targets are the zero-local rows that selected the live watchlist.
The other `594` targets come from the same far windows but were not the
zero-local seed rows.

## Watchlist

Kevin named the active channels:

```text
(5,5), (3,1), (3,11), (3,7)
```

All four pass on the `12` seed zero-local targets:

| channel | positive | negative | min | avg | +margin % |
|---|---:|---:|---:|---:|---:|
| (5,5) | 12 | 0 | 0.023851031 | 0.034224570 | 20.83 |
| (3,1) | 12 | 0 | 0.019293871 | 0.031510309 | 19.18 |
| (3,11) | 12 | 0 | 0.009853824 | 0.020351738 | 12.39 |
| (3,7) | 12 | 0 | 0.006841372 | 0.017182800 | 10.46 |

On the other `594` non-seed far targets, only `(5,5)` and `(3,1)` remain
singleton-positive everywhere:

| channel | positive | negative | min | avg | +margin % | first failures |
|---|---:|---:|---:|---:|---:|---|
| (5,5) | 594 | 0 | 0.006630207 | 0.028246087 | 21.24 | none |
| (3,1) | 594 | 0 | 0.006064142 | 0.025674732 | 19.30 | none |
| (3,11) | 584 | 10 | -0.006380196 | 0.015187564 | 11.45 | 6000044, 6000062, 6000130, 6000138, 6000198 |
| (3,7) | 587 | 7 | -0.007679179 | 0.014018140 | 10.58 | 6000088, 6000092, 8000072, 8000086, 8000166 |

On all `606` far clear targets:

```text
singleton passing channels: 5
smallest fixed subset size: 1
```

The best singleton certificates are:

```text
(5,5):  min 0.006630207, avg 0.028364472
(3,1):  min 0.006064142, avg 0.025790288
(1,11): min 0.005933003, avg 0.009857171
(4,8):  min 0.003588763, avg 0.008476146
(3,9):  min 0.001056450, avg 0.002878653
```

## Interpretation

This narrows the live channel hypothesis:

```text
(5,5) and (3,1) generalize from the 12 zero-local seed rows to the 594
non-seed far rows under the same stress reference.
```

The other two named channels, `(3,11)` and `(3,7)`, do not generalize as
singletons across the broader far fixture.  Their seed success is real but
scope-limited.

The result still does not prove a theorem, because every row uses the same
stress reference `1222142`.  A consistently positive channel can partly mean
that the stress reference has an unusually low value in that channel.  A fresh
selection-bias gate is therefore needed: replay the watchlist on windows not
used for channel selection, and later test alternate stress or deficit
references.

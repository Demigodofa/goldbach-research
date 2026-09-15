# q286 centered (3,1) reference-lemma audit

Status: finite selected-reference audit only.  This is not a proof of a
stress-classifier theorem, selected-deficit classifier theorem, signed
projection theorem, binary-prime correlation theorem, or Goldbach.

## Source

The generated audit is:

```text
evidence/q286-centered-3-1-reference-lemma-audit.json
```

The builder is:

```text
tools/build_q286_centered_3_1_reference_lemma_audit.py
```

It consolidates existing checked receipts:

```text
evidence/q286-centered-channel-scalar-order-audit.json
evidence/q286-alternate-reference-channel-audit.json
evidence/q286-centered-3-1-stress-class-audit.json
evidence/q286-selected-deficit-provenance-audit.json
```

## Candidate

Kevin's hunch was that `(3,1)` might be a stress-classifier lemma because
reference `13822` is strongly negative in that channel.

The finite candidate that survives is narrower:

```text
centered (3,1) is a selected-deficit stress-reference separator
```

For every selected stable/volatile dominant-floor failure reference, the `606`
fresh predeclared targets have strictly positive LP-weighted locally centered
`(3,1)` margin against that reference.

## Result

The selected deficit references all pass:

| reference | residue mod 143 | + | - | min fresh margin | avg fresh margin |
|---:|---:|---:|---:|---:|---:|
| 24424 | 114 | 606 | 0 | 0.009261016140 | 0.024360616292 |
| 13822 | 94 | 606 | 0 | 0.010757459151 | 0.025857059303 |
| 55864 | 94 | 606 | 0 | 0.027924887991 | 0.043024488143 |
| 164598 | 5 | 606 | 0 | 0.001813317905 | 0.016912918057 |
| 1222142 | 64 | 606 | 0 | 0.010444173018 | 0.025543773170 |

The selected clear-control references all fail the same singleton pass:

| reference | residue mod 143 | + | - | min fresh margin | avg fresh margin |
|---:|---:|---:|---:|---:|---:|
| 13556 | 114 | 0 | 606 | -0.148683440920 | -0.133583840768 |
| 40420 | 94 | 0 | 606 | -0.051539285337 | -0.036439685184 |
| 129706 | 5 | 604 | 2 | -0.000039110962 | 0.015060489190 |
| 1242118 | 20 | 457 | 149 | -0.009575217654 | 0.005524382498 |
| 1240888 | 77 | 451 | 155 | -0.009936254068 | 0.005163346085 |

## Reference 13822

Reference `13822` is a strong witness for the narrow reading:

```text
target mod 143:                94
dominant margin to floor:      -0.03674434602428933
stable-core margin to floor:    0.3023670686383121
volatile rim to principal:     -0.3391114146626045
centered (3,1) rank:            2
centered (3,1) weighted value: -0.028592853507378977
fresh-min gap against 13822:    0.010757459150664062
```

This is exactly the shape of a selected stress witness: the stable core alone
does not explain the failure, while the volatile/correlation layer supplies a
large negative push.

## Broad Falsifier

The broader promotion is already false:

```text
centered (3,1) classifies all full_nonpositive q286 stress rows
```

On the independent baseline `full_nonpositive` class, only `33/89` rows sit
below the fresh `(3,1)` minimum.  The other `56/89` are at or above it, with
maximum target `11902` at weighted centered value `0.23016925898905402`.

## Decision

The useful lemma target is:

```text
centered (3,1) separates selected stable/volatile dominant-floor failure
references from fresh predeclared targets after local subtraction
```

The failed promotions are:

```text
centered (3,1) is an arbitrary-reference positive channel
centered (3,1) classifies the whole full_nonpositive stress class
```

Before theorem-shaped promotion, the next gate needs either a non-post-hoc
class containing the selected deficit references and a fresh holdout, or a
return to signed/correlation estimates that explain why the `(3,1)` coordinate
is so low on this selected stress-reference family.

# q286 centered channel scalar order audit

Status: finite scalar-order reduction of the alternate-reference channel
audit. This is not a proof of a stress-classifier theorem, binary-prime
correlation theorem, signed projection theorem, or Goldbach.

## Source

The generated audit is:

```text
evidence/q286-centered-channel-scalar-order-audit.json
```

The builder is:

```text
tools/build_q286_centered_channel_scalar_order_audit.py
```

Channels tested:

```text
(3,1), (5,5)
```

Rows compared:

```text
selected deficit references: 24424, 13822, 55864, 164598, 1222142
selected clear-control references: 13556, 40420, 129706, 1242118, 1240888
same-window far targets: 606
fresh predeclared targets: 606
```

## Scalar

For a fixed channel `L`, the alternate-reference weighted margin against a
reference `R` is exactly:

```text
lp_weight[L] * ((empirical_L(target) - local_L(target))
                - (empirical_L(R) - local_L(R)))
```

So the finite alternate-reference pass for one channel is equivalent to a
scalar order statement: selected deficit references must sit below every fresh
target in the weighted locally centered channel value.

## Result

For `(3,1)`, all five selected deficit references lie below the minimum fresh
predeclared target after local centering.  The minimum fresh target is
`24000008`, with weighted centered `(3,1)` value
`-0.017835394356714915`.  The highest selected deficit reference is `164598`,
with value `-0.0196487122614909`, leaving a positive gap of
`0.001813317904775985`.

The selected deficit reference `13822` is not just slightly low in `(3,1)`.
It ranks second-lowest in the combined ordered set, behind only `55864`, with
weighted centered `(3,1)` value `-0.028592853507378977`.  Its margin below the
fresh minimum is `0.010757459150664062`.

For `(5,5)`, the same scalar order fails.  The minimum fresh target is
`24000146`, with weighted centered `(5,5)` value
`-0.023944926855061086`, but `13822` has value
`0.009715830696077645`.  Thus `13822` is high, not low, in the `(5,5)`
centered scalar order, and `(5,5)` cannot explain the selected
deficit-reference gate.

## Interpretation

Kevin's stress-classifier hunch for `(3,1)` is supported under this finite
fixture: `(3,1)` acts as a selected-deficit-reference scalar separator after
the local residue contribution is removed.  The evidence is stronger than
"reference `1222142` was unusually low" because the same ordered separation
holds for all five selected deficit references.

The boundary remains important.  This audit does not identify all stress rows,
does not prove that every future deficit row is low in `(3,1)`, and does not
explain why the ordered separation should persist.  The next theorem-shaped
gate is to define a non-post-hoc deficit/stress class and test whether `(3,1)`
orders that class below fresh clear targets without selecting the references
after the fact.

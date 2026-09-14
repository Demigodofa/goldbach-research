# q286 dominant-mode channel swing pairs

Status: finite channel-swing diagnostic.  Goldbach is not proved.

This note compares selected deficit-to-clear near-boundary pairs after the
signed-channel branch split.  It asks where the clear-minus-deficit swing
lands among the `25` real q286 dominant channels.

Receipt:
`evidence/q286-first-three-dominant-mode-channel-swing-pairs.json`

## Mechanism Tested

If the offset-under-pressure route has a small arithmetic core, then the
helpful channel deltas should concentrate in a recurrent subset of real
channels.  If the helpful deltas are diffuse or pair-specific, then a
one-channel or two-channel offset theorem is probably the wrong next target.

For each pair, the receipt decomposes:

```text
right_dominant_sum - left_dominant_sum
  = sum_channels (right_channel - left_channel).
```

The checked pairs are:

```text
(24424,13556), (13822,40420), (55864,40420),
(164598,129706), (1222142,1242118), (1222142,1240888)
```

All six are deficit-to-clear pairs for the dominant `mode_1+mode_2` floor.

## Measured Shape

The swing reconstruction error is below `8.2e-15`.

Two channels are helpful in every checked pair:

- `(2,6)`: positive delta sum about `0.5758302749811214`;
- `(3,1)`: positive delta sum about `0.4003828170751664`.

Several other channels are recurrent but not universal, including `(4,8)`,
`(4,2)`, `(3,11)`, `(5,5)`, `(4,4)`, `(1,3)`, `(5,3)`, and `(2,4)`.

However, the helpful swing is not a one- or two-channel phenomenon.  Across
the six pairs, the number of helpful channels needed to reach `80%` of the
positive delta ranges from `5` to `9`.  The weakest top-helpful concentration
is the pair `(164598,129706)`, where the top recorded helpful channels carry
about `0.6466916175343709` of the positive delta.

Most helpful mass is either sign-flip-to-positive or negative-pressure
reduction.  The late pair `(1222142,1242118)` is more pressure-relief driven:
negative-pressure reduction contributes about `0.13959357593233135`, while
sign-flip-to-positive contributes about `0.06483476921211201`.

## Consequence

This supports a recurrent helpful-channel portfolio, but it demotes a tiny
one-channel or two-channel offset lemma.  The next theorem target is a
portfolio-level arithmetic estimate for helpful channel deltas under high
negative pressure, or a classification of the true deficit rows as finite or
boundary phenomena.

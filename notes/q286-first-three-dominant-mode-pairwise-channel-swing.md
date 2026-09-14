# q286 Dominant-Mode Pairwise Channel Swing

Status: finite named-pair channel-swing diagnostic only.  This is not a
pairwise recurrence theorem, one-channel swing theorem, coupled
pressure/offset curve theorem, pointwise character-sum estimate, or Goldbach
proof.

## Mechanism

The pressure/offset scalar falsifier leaves the exact coupled curve

```text
P >= B - 0.3
```

as the live scalar target, where `B` is dominant-mode negative real-channel
pressure and `P` is dominant-mode positive real-channel offset.  The next
tempting simplification is that a tail-to-clear rescue near this curve might
come from one dominant real channel, or from a tiny set of channel swings.

This diagnostic compares the known tail `1222142` against two named clear
near-boundary rows, channel by channel.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_pairwise_channel_swing.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-pairwise-channel-swing.json`
- Source receipt:
  `q286_first_three_dominant_mode_signed_channel_profile_receipt`
- Pairs:
  `1222142 -> 1242118`, `1222142 -> 1240888`

## Results

For `1222142 -> 1242118`:

```text
net dominant swing:        0.0253620930272739
positive swing sum:        0.21155798383387
negative drag sum:        -0.186195890806595
helpful channels:          14
harmful channels:          11
top1 helpful share:        0.179813864137732
top3 helpful share:        0.420940459691155
top5 helpful share:        0.637046312912331
top helpful label:         (2,6)
top helpful delta:         0.0380410585623561
reconstruction error:      below 9e-16
```

For `1222142 -> 1240888`:

```text
net dominant swing:        0.0360197529414457
positive swing sum:        0.214511452023912
negative drag sum:        -0.178491699082464
helpful channels:          14
harmful channels:          11
top1 helpful share:        0.202792781817407
top3 helpful share:        0.496320384863379
top5 helpful share:        0.68521185077658
top helpful label:         (4,8)
top helpful delta:         0.0435013740876203
reconstruction error:      below 3e-15
```

## Interpretation

Both named rescues are signed multi-channel balances.  The helpful swing is
not explained by one channel, and even the top three helpful channels do not
carry half the helpful swing on both pairs.

This demotes a one-channel tail-to-clear swing theorem on current evidence.
The live route remains a coupled aggregate theorem, a pressure-subregion split
with additional arithmetic structure, or a lower-support/complement rescue.
Future top-k swing claims need a changed condition and a predeclared
denominator; this note does not rule out such a theorem in a narrower region.

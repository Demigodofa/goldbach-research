# q286 dominant-mode pressure-channel autopsy

Status: finite named-row pressure-channel diagnostic only.  This is not a
one-channel pressure theorem, not a multi-channel pressure envelope theorem,
not a pointwise character-sum estimate, not a signed-projection theorem, and
not a Goldbach proof.

## Mechanism

The pressure horizon suggests a post-stress region where the direct pressure
branch

```text
negative_pressure <= 0.3
```

clears sampled rows.  This autopsy asks whether that pressure behavior is
explained by one stable dangerous negative real channel, or whether the top
negative channels rotate by target residue.

The falsifier for a one-channel route is rotating top-negative labels across
the named pressure rows.  That would demote a proof based on bounding one
recurring channel and point instead to a multi-channel or residue-dependent
pressure envelope.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_pressure_channel_autopsy.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-pressure-channel-autopsy.json`
- Source receipt:
  `q286_first_three_dominant_mode_signed_channel_profile_receipt`

## Named Rows

The checked rows are:

```text
1222142, 1242118, 1240888, 1243018, 1243130, 1244072, 1244094
```

Only `1222142` fails the dominant floor in this named set.  It has negative
pressure about `0.3719670025`.  Among the post-stress rows, the maximum
negative pressure is `1243018`, with pressure about `0.2586239309`, below
the `0.3` pressure branch threshold.

Across the top three negative real channels of the seven named rows, there
are `15` distinct channel labels.  The most common top-three negative label is
`(1,11)`, appearing in three rows:

```text
1222142: -0.0377829312
1240888: -0.0249154177
1244072: -0.0442657462
```

Other repeated top-three labels appear only twice, including `(5,5)`,
`(5,1)`, `(1,7)`, and `(3,7)`.

## Interpretation

The post-stress pressure-easy rows are not explained by the disappearance of
one single dangerous channel.  Their pressure ledger still has nontrivial
negative channels, but the top labels rotate.

This demotes a one-channel pressure theorem on this evidence.  The surviving
pressure route is a multi-channel or residue-dependent envelope for the
negative real q286 channel ledger, or a separate classification/rescue of
pressure failures.

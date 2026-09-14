# q286 Dominant-Mode Pressure Bulk Share

Status: finite named-row pressure bulk-share diagnostic only.  This is not a
top-k theorem, multi-channel envelope theorem, pointwise character-sum
estimate, signed-projection theorem, or Goldbach proof.

## Mechanism

After the one-channel pressure route was demoted, the next question was whether
the pressure rows are at least controlled by a tiny top-k set of negative real
channels.  If the top one, three, or five negative channels carried nearly all
negative pressure on the named rows, the live proof target could narrow toward a
small fixed channel theorem.  If not, the target remains a broader bulk
multi-channel or residue-dependent pressure envelope.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_pressure_bulk_share.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-pressure-bulk-share.json`
- Source receipt:
  `q286_first_three_dominant_mode_signed_channel_profile_receipt`
- Named rows:
  `1222142`, `1242118`, `1240888`, `1243018`, `1243130`, `1244072`,
  `1244094`

## Observed Share Ranges

The shares below are the fraction of each row's total negative real-channel
pressure captured by its largest negative-pressure channels.

```text
top1 share range:  0.1042376170 .. 0.1883703993
top3 share range:  0.2725197862 .. 0.4453824162
top5 share range:  0.4237604469 .. 0.6607281866
top10 share range: 0.7114630603 .. 0.9523322684
```

The maximum top-three share row is `1244072`, with share about
`0.4453824162`.  The minimum top-three share row is `1242118`, with share
about `0.2725197862`.  The only dominant-floor failure among the named rows is
still `1222142`.

## Interpretation

The pressure is bulk distributed rather than concentrated in one tiny fixed
channel group.  The top one channel explains only about `10%` to `19%` of the
negative pressure, the top three explain only about `27%` to `45%`, and the
top five still leave substantial tail pressure on multiple rows.

This demotes a tiny top-k pressure theorem on current evidence.  The live
pressure route should be treated as a bulk multi-channel, residue-dependent,
or complementary classification problem unless a new mechanism explains why a
small channel set becomes universal outside this finite diagnostic.

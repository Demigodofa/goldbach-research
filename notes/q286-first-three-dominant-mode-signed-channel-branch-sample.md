# q286 dominant-mode signed channel branch sample

Status: finite branch-sample diagnostic.  Goldbach is not proved.

This note widens the three-row signed-channel profile without changing the
algebra.  It reuses deterministic near-boundary rows from the mass-matched
fixture: the five lowest first-three tail rows recorded there, their paired
clear rows, the late holdout pair, and the second late clear row.

Receipt:
`evidence/q286-first-three-dominant-mode-signed-channel-branch-sample.json`

## Exact split

For the `25` real dominant q286 channels, write:

```text
dominant_sum = positive_offset - negative_pressure.
```

At threshold `tau = 0.3`, a row clears the dominant floor exactly when either:

```text
negative_pressure <= tau
```

or

```text
positive_offset >= negative_pressure - tau.
```

The receipt classifies the selected targets by this exact branch split.  It
does not prove either branch eventually.

## Sample outcome

The ten selected targets are:

```text
24424, 13556, 13822, 40420, 55864, 164598, 129706,
1222142, 1242118, 1240888
```

Measured classification:

- unresolved deficits: `24424, 13822, 55864, 164598, 1222142`;
- offset branch clears: `13556, 40420, 129706, 1242118`;
- pressure-and-offset branch clear: `1240888`;
- pressure-only branch clears: none.

The largest clear negative pressure is at `13556`, with pressure about
`0.9544512968249877`; it clears only because its positive offset is about
`0.6640153871706468`, leaving slack about `0.009564090345658971`.

The largest deficit is at `55864`: dominant sum about
`-0.39922857579168886`, negative pressure about `0.8325378135259056`,
positive offset about `0.43330923773421653`, and deficit to the `-.3` floor
about `0.09922857579168887`.

The late holdout tail `1222142` remains a small true deficit, missing by about
`0.00883317956053016`.

## Consequence

This demotes a simple negative-pressure ceiling as the visible explanation for
the selected near-boundary rows: most clear rows in the sample still have
pressure above `0.3`.  The live theorem target is therefore more specifically
an offset-forcing theorem under pressure, plus a classification or finite
handling of the unresolved deficit rows.

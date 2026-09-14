# q286 dominant-mode prefix/tail classification

Status: finite exact prefix/tail diagnostic.  Goldbach is not proved.

This note splits the recurrent helpful-channel portfolio into the first prefix
that keeps every selected clear row passing and the remaining tail that
restores the selected deficit classification.

Receipt:
`evidence/q286-first-three-dominant-mode-prefix-tail-classification.json`

## Exact Split

The recurrent portfolio has `11` channels.  The first prefix that keeps all
selected clear rows passing has `4` channels:

```text
(2,6), (3,1), (4,8), (4,2)
```

The remaining `7` channels form the classification tail:

```text
(3,11), (5,5), (4,4), (1,3), (5,3), (2,4), (4,6)
```

For each row:

```text
full_portfolio = prefix + tail
```

and once the prefix is fixed, recovering the full floor is equivalent to:

```text
tail_sum >= -prefix_slack.
```

The maximum reconstruction error and tail-floor identity error are both about
`5.55e-17`.

## Measured Shape

The selected clear rows are:

```text
13556, 40420, 129706, 1242118, 1240888
```

The selected deficit rows are:

```text
24424, 13822, 55864, 164598, 1222142
```

The prefix over-rescues every selected deficit and keeps every selected clear
above the floor.  The tail restores every selected deficit and preserves every
selected clear.

Target table:

```text
target   prefix_slack   tail_sum       required_tail   tail_slack
24424    +0.1795125243  -0.1929711969 -0.1795125243   -0.0134586727
13556    +0.0439492731  -0.0343851828 -0.0439492731   +0.0095640903
13822    +0.4200674535  -0.4568117995 -0.4200674535   -0.0367443460
40420    +0.2559232556  -0.2069848521 -0.2559232556   +0.0489384035
55864    +0.1519396874  -0.2511682632 -0.1519396874   -0.0992285758
164598   +0.0490463428  -0.0681981352 -0.0490463428   -0.0191517925
129706   +0.0095074933  +0.0489214329 -0.0095074933   +0.0584289263
1222142  +0.0792869595  -0.0881201391 -0.0792869595   -0.0088331796
1242118  +0.0828090801  -0.0662801666 -0.0828090801   +0.0165289135
1240888  +0.0999747434  -0.0727881700 -0.0999747434   +0.0271865734
```

Here `tail_slack` is exactly the full portfolio floor slack.

## Consequence

The current q286 dominant-mode portfolio target has two distinct theorem
jobs:

```text
1. Prefix lower-bound theorem:
   prove that the four-channel prefix gives enough positive slack on rows
   that should clear.

2. Tail classification/exclusion theorem:
   prove that the seven-channel tail, or a companion complement/lower-support
   mechanism, prevents prefix-overrescued deficit rows from becoming false
   positives.
```

This is stronger than the previous vague portfolio statement because it gives
each side an exact inequality.  It is still finite selected-fixture evidence,
not a uniform theorem and not a proof of Goldbach.

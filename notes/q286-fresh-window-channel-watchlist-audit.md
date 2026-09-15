# q286 fresh-window channel watchlist audit

Status: finite selection-bias gate over fresh predeclared windows.  This is
not a proof of a channel theorem, binary-prime correlation theorem, signed
projection theorem, or Goldbach.

## Source

The generated audit is:

```text
evidence/q286-fresh-window-channel-watchlist-audit.json
```

The builder is:

```text
tools/build_q286_fresh_window_channel_watchlist_audit.py
```

The windows were fixed in the script before the run and were not used to
select the watchlist:

```text
24,000,000; 28,000,000; 32,000,000; 36,000,000; 40,000,000; 44,000,000
```

Each window contributes `101` even targets, for `606` fresh targets total.
Every row still uses the same stress reference:

```text
stress target = 1222142
```

## Watchlist

Kevin's watchlist was:

```text
(5,5), (3,1), (3,11), (3,7)
```

For each target, the audit subtracts the target residue's local vector and
measures:

```text
lp_effective_weight * after_local_delta
```

Fresh-window result:

| channel | passes fresh singleton? | positive | negative | min | avg | +margin % | failures |
|---|---|---:|---:|---:|---:|---:|---|
| (5,5) | yes | 606 | 0 | 0.012921749 | 0.028531928 | 21.39 | none |
| (3,1) | yes | 606 | 0 | 0.010444173 | 0.025543773 | 19.15 | none |
| (3,11) | no | 605 | 1 | -0.000132302 | 0.015729926 | 11.79 | 28000004 |
| (3,7) | yes | 606 | 0 | 0.002106132 | 0.013929395 | 10.44 | none |

The smallest positive fixed subset on the fresh windows still has size `1`,
with `6` passing singleton channels:

```text
(5,5):  min 0.012921749, avg 0.028531928
(3,1):  min 0.010444173, avg 0.025543773
(1,11): min 0.006600795, avg 0.010072551
(4,8):  min 0.004221423, avg 0.008327763
(3,7):  min 0.002106132, avg 0.013929395
(3,9):  min 0.001130275, avg 0.002877037
```

## Interpretation

The fresh-window gate supports `(5,5)` and `(3,1)` as same-stress singleton
channels beyond the zero-local seed rows and beyond the first far windows.
It also revives `(3,7)` on this fresh fixture, although `(3,7)` failed on
seven targets in the earlier `594` non-seed replay.  Channel `(3,11)` is
weaker: it failed once at `28000004`.

The scope remains same-stress only.  A consistently positive channel can
partly reflect the fixed reference row `1222142` having unusually low value in
that channel.  Before any theorem-shaped promotion, the next gate should test
the same watchlist against alternate stress or deficit references.

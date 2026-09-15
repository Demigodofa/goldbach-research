# q286 residue-5 multichannel horizon

Status: finite multichannel rescue of the scalar `(3,1)` residue-5 horizon
failure.  This is not a selected-stress theorem, signed-correlation theorem,
pointwise character-sum theorem, or Goldbach proof.

## Source

The generated receipt is:

```text
evidence/q286-centered-3-1-residue5-multichannel-horizon.json
```

The builder is:

```text
tools/build_q286_centered_3_1_residue5_multichannel_horizon.py
```

## Mechanism

The scalar `(3,1)` horizon used the same residue-5 micro-neighborhood:

```text
8000140 + 286*k,  -50 <= k <= 50
```

with reference target `164598`.  Every target has the same residue modulo
`143` as the reference, so the local q286 channel vector cancels in the
same-residue comparison.  The scalar `(3,1)` channel failed on five targets,
with worst weighted gap `-0.0073386462295386805`.

This audit keeps the same reference, same horizon, and same zero-local setup,
but sums frozen LP-weighted after-local channel gaps across pre-existing
channel sets:

- scalar `(3,1)`;
- Kevin's watchlist `(5,5), (3,1), (3,11), (3,7)`;
- the same watchlist with `(3,1)` removed;
- the frozen full 17-channel LP vector.

## Result

The scalar channel fails, but the multichannel pre-existing objects pass this
finite horizon.

| subset | labels | target failures | minimum weighted gap |
|---|---:|---:|---:|
| scalar `(3,1)` | 1 | 5 | -0.007338646230 |
| Kevin watchlist | 4 | 0 | 0.026187595110 |
| Kevin watchlist without `(3,1)` | 3 | 0 | 0.021108340505 |
| frozen full 17 LP | 17 | 0 | 0.055956206789 |

This means `(3,1)` should be treated as a stress/reference classifier
coordinate, not as the scalar closure mechanism for the residue-5
micro-horizon.

## Channel Diagnostic

Seven individual channels are positive on all `101` horizon targets in this
post-hoc diagnostic scan:

| channel | positive | negative | minimum weighted contribution | average |
|---|---:|---:|---:|---:|
| `(5,1)` | 101 | 0 | 0.016706925617 | 0.027411108152 |
| `(3,11)` | 101 | 0 | 0.006106023257 | 0.026771742756 |
| `(2,8)` | 101 | 0 | 0.005701959304 | 0.015017313669 |
| `(1,11)` | 101 | 0 | 0.004372370499 | 0.007196532029 |
| `(3,7)` | 101 | 0 | 0.003918435863 | 0.015237625645 |
| `(3,9)` | 101 | 0 | 0.001521462889 | 0.002545821402 |
| `(2,6)` | 101 | 0 | 0.000639867220 | 0.008340019722 |

The smallest passing fixed subset over all 17 labels has size `1`, but this is
explicitly post-hoc and cannot be promoted into a theorem without a
non-post-hoc rule selecting the channel before seeing the horizon result.  The
best post-hoc singleton by minimum margin is `(5,1)`.

## Decision

The residue-5 hole did not close through the scalar `(3,1)` loop.  It did close
finitely through the pre-existing multichannel watchlist and the frozen full
17-channel LP vector on this exact horizon.

The next live proof route is therefore a distributed signed-correlation/cone
obligation:

```text
prove a non-post-hoc multichannel positive margin,
or falsify it on fresh predeclared windows and alternate stress references
```

The result also supports Kevin's hunch that `(3,1)` may function as a
stress-reference classifier lemma.  Reference `13822` remains a strong witness
in earlier receipts, but this residue-5 audit shows that classifier evidence
must not be confused with scalar positivity closure.

## Falsifier Boundary

This confirms only the finite horizon:

```text
same reference 164598,
same targets 8000140 + 286*k for -50 <= k <= 50,
same frozen channel weights,
same zero-local residue-5 comparison
```

It does not test alternate stress references, fresh unseen windows, or an
asymptotic theorem.

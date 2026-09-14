# q286 low-frequency lift horizon holdout

Status: finite horizon holdout for a frozen q286 low-frequency lift.  This is
not a proof of Goldbach, a low-frequency theorem, a rank-`1` theorem, or a
residual-drag theorem.

## Purpose

The first heldout kept the frozen `full_low_frequency_lift` vector alive on
fresh windows near `1260000` and `1280000`.  The target-residue tensor then
failed to improve it.  This receipt asks a different question:

```text
Does the static low-frequency lift survive farther q286 windows, including
neighborhoods of previously named stress-marker targets, with no refit?
```

The generated evidence is:

```text
evidence/q286-low-frequency-lift-horizon-holdout.json
```

The builder is:

```text
tools/build_q286_low_frequency_lift_horizon_holdout.py
```

## Fixture

The frozen vector comes from:

```text
evidence/q286-lift-project-dictionary-audit.json
```

It is replayed on six later windows:

```text
(1426162, 101)
(1500000, 101)
(2200000, 101)
(3305100, 101)
(4304218, 101)
(5000000, 101)
```

The windows include the marker targets:

```text
1426262, 3305200, 4304318
```

The stress row remains `1222142`, and the same `17` outside real channels are
used.  No heldout projection, target-specific fitting, or row-feature tensor is
introduced.

## Result

The horizon denominator has `606` targets and no dominant-floor deficits:

```text
horizon targets: 606
horizon clears:  606
horizon deficits: 0
```

Exact outside deltas, frozen rank-`1` reconstructed deltas, and frozen
low-frequency reconstructed deltas remain positive on every row:

```text
exact outside nonpositive count:       0
rank1 reconstructed nonpositive count: 0
low-frequency nonpositive count:       0
```

Both the frozen rank-`1` replay and the frozen low-frequency replay retain the
`0.75` residual-drag cap:

```text
rank1 cap failures:         0
low-frequency cap failures: 0
```

Horizon low-frequency summaries:

```text
matrix cosine to rank1 reference: 0.8311579645183356
high-drag overlap:               2/3
max low-frequency drag ratio:    0.6419474569885669 at target 1426262
max rank1 drag ratio:            0.6778685566389991 at target 1426262
minimum full outside delta:      0.04463793369291936 at target 1426262
```

The marker `1426262` is the tight row.  It is a clear row, not a deficit, but
it carries the maximum residual-drag ratio for both the frozen rank-`1` replay
and the frozen low-frequency replay.

## Decision

The frozen low-frequency lift survives a second, farther denominator and is
therefore still useful as a finite q286 hole-tightening tool.  This strengthens
the representation-shift lane after the coarse target-residue tensor failed.

It does not close the loop.  The survival depends on exact row arithmetic, and
the tight row `1426262` shows the cap can still be meaningfully stressed.  The
next proof route should use actual character-sum magnitudes, row-dependent
signed cones, or a stronger signed aggregate theorem rather than another
coarse target-residue tensor.

## Boundary

This receipt proves no uniform estimate, no asymptotic theorem, no pointwise
Goldbach-in-progressions theorem, and no Goldbach theorem.  It only records
that the frozen low-frequency q286 lift remains stable on this predeclared
horizon denominator.

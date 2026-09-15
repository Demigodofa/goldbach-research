# q286 complement-rescue suffix sampled holdout

Status: finite frozen-suffix sampled holdout.  This is not a full-block
verification, threshold theorem, signed correlation theorem, pointwise
character-sum theorem, or Goldbach proof.

Receipt:

```text
tools/build_q286_complement_rescue_suffix_holdout.py
evidence/q286-complement-rescue-suffix-holdout.json
```

## Question

The threshold-candidate audit selected
`block_index_after_discovery >= 1` as the smallest supported finite
post-discovery rescue suffix in blocks `0..5`.  This sampled holdout freezes
that candidate and tests six later q286 block-start windows beyond the last
selected start `410400`.

## Fixture

```text
frozen candidate:       block_index_after_discovery >= 1
holdout block indices:  6, 7, 8, 9, 10, 11
holdout starts:         490480, 570560, 650640, 730720, 810800, 890880
cycles per start:       1
targets per cycle:      101
total sampled targets:  606
```

The candidate fails this finite holdout if any first-three-tail or
active-selector row has nonpositive `full_action_to_principal_ratio`.

## Result

The sampled holdout did not produce a rescue pass or a rescue falsifier,
because it found no first-three-tail support in either sampled cohort:

```text
block-start first-101 targets:    606 tested, 0 first-three-tail rows
prior-tail offset replay:          72 tested, 0 first-three-tail rows
offsets replayed from old tails:   12
predicate full_nonpositive rows:    0
status: untested_no_tail_support
```

This changes the reading of the later sampled window: in this finite sample,
tail pressure disappears before complement rescue is needed.  That does not
contradict the earlier post-discovery full-block schedule, where tail rows
persisted and were rescued.  It says only that the sampled later block starts
do not currently support a rescue-margin falsifier.

Interpret this as a support-starved finite holdout, not as a full-block claim
or an asymptotic theorem.  The proof still needs either an optimized full-block
verifier or a non-circular condition that forces:

```text
complement_to_principal_ratio
  > -first_three_modes_to_principal_ratio
```

on the intended q286 class.

Full later-block verification should use an optimized convolution or caching
route before it is treated as exhaustively checked; direct prime-pair looping
is too opaque for these larger all-block windows.

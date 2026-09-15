# q286 prime-indexed later full-block scan

Status: finite predeclared later full-block scan.  This is not a threshold
theorem, signed correlation theorem, pointwise character-sum theorem, or
Goldbach proof.

Receipt:

```text
tools/build_q286_prime_indexed_later_full_block_scan.py
evidence/q286-prime-indexed-later-full-block-scan.json
```

## Question

The suffix sampled holdout tested the later starts `490480, 570560, 650640,
730720, 810800, 890880`, but found no first-three-tail support in either the
first-101 sample or the replayed prior-tail offsets.  This receipt scans the
full six later q286 blocks with the validated prime-indexed row verifier.

## Mechanism

Each block uses `8` q286 cycles and `5005` even targets per cycle.  The scan
classifies first-three-tail rows as:

- `rescued_with_tail_support` when tail rows exist and every one has positive
  full recombined action;
- `support_starved_no_first_three_tail_rows` when no first-three-tail rows
  appear;
- `falsified_by_nonpositive_tail_rows` when any first-three-tail row has
  nonpositive full action.

## Result

`evidence/q286-prime-indexed-later-full-block-scan.json` classifies the
predeclared later full blocks as `rescued_with_tail_support`:

```text
tested targets: 240240
first-three-tail rows: 73
active-selector rows: 73
tail/full-nonpositive failures: 0
full-nonpositive predicate rows: 0
minimum rescue margin: 0.343350240861549
minimum complement/required ratio: 1.99072616313582
maximum identity error: 1.11022302462516e-16
elapsed seconds: 342.040064200002
```

Per-block tail/failure counts:

```text
block 6 start 490480: tail 46, fail 0
block 7 start 570560: tail 17, fail 0
block 8 start 650640: tail 1, fail 0
block 9 start 730720: tail 5, fail 0
block 10 start 810800: tail 3, fail 0
block 11 start 890880: tail 1, fail 0
```

Interpretation rules:

- A rescue pass is a finite later-block result, not an eventual theorem.
- A support-starved result means the predeclared window still did not test the
  complement-rescue class.
- A falsifier preserves the exact rows and closes this frozen candidate unless
  a changed-condition split is named before rerun.

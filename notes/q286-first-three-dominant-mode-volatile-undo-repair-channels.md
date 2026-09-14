# q286 Dominant-Mode Volatile Undo-Repair Channels

Status: finite volatile undo-repair diagnostic only.  This is not a
volatile-rim theorem, stable-core theorem, selected-fixture classifier theorem,
pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The adverse-undo receipt identifies inclusion-minimal volatile additions that
undo fragile deficit-row clauses.  This receipt asks the next finite question:
after a fragile clause has been undone by an adverse addition, can another
volatile addition repair the deficit classification again?

For each adverse event, it starts from:

```text
minimal clause + minimal adverse addition
```

Then it enumerates the remaining volatile channels and keeps the
inclusion-minimal additions that restore the row classification.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_volatile_undo_repair_channels.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-volatile-undo-repair-channels.json`
- Source adverse undo channels:
  `evidence/q286-first-three-dominant-mode-volatile-adverse-undo-channels.json`
- Source subset ablation:
  `evidence/q286-first-three-dominant-mode-volatile-subset-ablation.json`

## Results

Across the selected deficit fixture, there are `26` adverse events.  Every one
has at least one minimal repair.  There are `52` minimal repairs total: `50`
are single-channel additions and `2` are three-channel additions.  The three
hard deficit rows `13822`, `164598`, and `1222142` account for `22` adverse
events, and all of their minimal repairs are single-channel additions.

For `13822`, the adverse addition `(1,5)` is repaired by adding:

```text
(4,4)
```

For `164598`, the adverse pair `(1,1),(1,3)` is repaired by adding either:

```text
(1,7)
(4,10)
```

For `1222142`, the `20` adverse events each have exactly two one-channel
repairs.  Their repair-channel frequencies are:

```text
(1,1):  10
(2,4):  10
(1,3):   6
(4,10):  6
(1,5):   4
(3,3):   4
```

Across all selected deficit rows, the repair-channel frequencies are:

```text
(1,1):  12
(2,4):  12
(4,10): 10
(1,3):   7
(3,3):   7
(1,5):   5
(4,4):   2
(1,7):   1
```

The two size-three selected-fixture repairs occur at `24424`, not in the three
hard deficit rows.

## Interpretation

The finite q286 hole is tightening, but it is not closed.  The previous
adverse-channel result made the non-undo target look like named channel
control.  This receipt shows those adverse additions are not terminal in the
finite Boolean ledger: every adverse event can be repaired by a small named
channel set, and in the hard rows every minimal repair is a single channel.

That demotes pure non-undo as a complete explanation.  The live Boolean route
is now an ordered clause/adverse/repair theorem: prove that the actual
binary-prime residue weights enforce the right ordered balance, or replace the
Boolean ledger with a full signed aggregate arithmetic-placement theorem.
The receipt is finite repair-channel evidence only.

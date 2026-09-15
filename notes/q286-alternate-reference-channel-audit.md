# q286 alternate-reference channel audit

Status: finite alternate-reference replay over the fresh predeclared windows.
This is not a proof of a reference-independent channel theorem, binary-prime
correlation theorem, signed projection theorem, or Goldbach.

## Source

The generated audit is:

```text
evidence/q286-alternate-reference-channel-audit.json
```

The builder is:

```text
tools/build_q286_alternate_reference_channel_audit.py
```

Fresh target windows:

```text
24,000,000; 28,000,000; 32,000,000; 36,000,000; 40,000,000; 44,000,000
```

Each window contributes `101` even targets, for `606` fresh targets per
reference.

## References

Selected deficit references:

```text
24424, 13822, 55864, 164598, 1222142
```

Selected clear-control references:

```text
13556, 40420, 129706, 1242118, 1240888
```

For each reference `R`, the empirical channel delta is `target - R`, and the
local subtraction is rebased as:

```text
local(target residue) - local(R residue)
```

The live singleton candidates tested were:

```text
(5,5), (3,1)
```

## Deficit Reference Results

| reference | mod 143 | (5,5) pass? | (3,1) pass? | smallest subset | net LP margin |
|---:|---:|---|---|---:|---:|
| 24424 | 114 | yes | yes | 1 | 39.230026005 |
| 13822 | 94 | no | yes | 1 | -44.661094794 |
| 55864 | 94 | no | yes | 1 | 49.208712306 |
| 164598 | 5 | no | yes | 1 | 66.243973693 |
| 1222142 | 64 | yes | yes | 1 | 74.854116402 |

Decision for deficit references:

```text
(3,1) passes all five selected deficit references.
(5,5) fails for references 13822, 55864, and 164598.
```

So `(5,5)` is not reference-independent under this finite deficit-reference
gate.  `(3,1)` remains the stronger same-watchlist singleton candidate.

## Clear-Control Results

| reference | mod 143 | (5,5) pass? | (3,1) pass? | smallest subset | net LP margin |
|---:|---:|---|---|---:|---:|
| 13556 | 114 | no | no | 1 | 13.803192200 |
| 40420 | 94 | yes | no | 1 | 67.064512919 |
| 129706 | 5 | no | no | 1 | 7.212381001 |
| 1242118 | 20 | no | no | 1 | 44.315457638 |
| 1240888 | 77 | no | no | 1 | 26.659156635 |

Clear controls are diagnostic, not stress references.  Their failures show the
positive singleton statement is not an arbitrary-reference property.

## Watchlist Notes

The broader watchlist channels `(3,11)` and `(3,7)` remain reference-sensitive.
Examples:

```text
reference 13822:  (3,11) passes all 606, (3,7) fails all 606
reference 164598: (3,11) passes all 606, (3,7) has 79 negatives
reference 1222142: (3,7) passes all 606, (3,11) fails once
```

## Interpretation

This audit falsifies the broad claim that both live same-stress singleton
channels are reference-independent.  The refined result is:

```text
(3,1) survives all selected deficit references on the fresh windows.
(5,5) survives the base stress reference but fails several alternate deficit
references.
```

The next theorem-shaped target should focus on why `(3,1)` is consistently
positive relative to selected deficit rows after local subtraction.  It is
still finite evidence only, and the selected deficit-reference set is not a
universal class of all possible stress rows.

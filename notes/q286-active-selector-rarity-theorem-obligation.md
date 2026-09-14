# q286 Active-Selector Rarity Theorem Obligation

Status: theorem-obligation bookkeeping only. This is not a proof of Goldbach.

## Selector

The current q286 active lane is:

```text
first_two_modes_to_principal_ratio < -0.2
first_three_modes_to_principal_ratio < -0.3
```

Therefore a theorem proving

```text
first_three_modes_to_principal_ratio >= -0.3
```

on a target range excludes the active selector on that range before any
fixed-inequality or strict-closure stress is needed.

## Exact Quantity

The fast scanner in `_q286_first_three_tail_fast_scan_receipt` computes the
same first-three singular-mode quantity as the direct mode-only receipt, but
as a fixed linear functional of strict-central prime-pair residue weights
modulo `286`.

For an even target `N`, let:

- `U_286` be the reduced residue classes modulo `286`;
- `A_N` be the admissible unit residues `u` with `(N-u,286)=1`;
- `w_N(u)` be the strict-central weighted prime-pair mass with first prime
  congruent to `u mod 286`;
- `W_N = sum_u w_N(u)`;
- `m_N = W_N / |A_N|`;
- `delta_N(u) = w_N(u) - m_N` on `A_N` and `0` off `A_N`;
- `ell` be the fixed q286 first-three singular-mode linear coefficient vector;
- `P` be the fixed principal mean per unit weight.

Then the measured quantity is:

```text
first_three(N) = Re(sum_u ell(u) delta_N(u)) / (P W_N).
```

The active-selector rarity theorem is therefore a pointwise signed
prime-pair residue discrepancy estimate:

```text
Re(sum_u ell(u) delta_N(u)) >= -0.3 P W_N
```

for all targets outside a finite checked set, or for the specific outer
target family being assembled.

## Current Evidence

Finite denominator evidence so far:

- `evidence/q286-tail-selector-grid-12x25.json`: `300` neutral selector
  targets, zero active-tail hits.
- `evidence/q286-first-three-tail-scout-4x12x25.json`: `1200` targets, zero
  first-three hits below `-0.3`.
- `evidence/q286-first-three-tail-scout-8x12x25-late.json`: `2400` later
  targets, zero first-three hits below `-0.3`; worst block minimum
  `-0.1282544626188415` at target `2562584`.
- `evidence/q286-tail-selector-active-residue-holdout-6x5.json`: `30`
  same-residue holdout targets after `1379072`, zero active-tail hits.

Strict closure has still only been stressed on the selected late active rows
`1222142`, `1323632`, and `1379072`. The finite rarity evidence must not be
counted as strict-closure support.

## Falsifier

Any unchanged-selector holdout that finds a target with:

```text
first_three(N) < -0.3
```

falsifies a naive finite rarity extrapolation and must be escalated to the
full active selector. If it also satisfies `first_two < -0.2`, the strict
closure receipt must be run with unchanged constants. A nonpositive strict
closure margin would falsify the current conditional constants.

## Proof Routes

1. Prove the pointwise residue-discrepancy inequality above by analytic means.
   This is a binary prime-pair distribution estimate modulo `286` with a
   signed q286 test vector; it is close to known hard territory around
   Goldbach in arithmetic progressions and L-function zero control.
2. Prove a weaker eventual theorem: after a finite bound `N0`, the
   first-three ratio is above `-0.3`, then check all active-selector targets
   below `N0` by exact receipts.
3. Abandon rarity as the main path if new holdouts produce repeated active
   rows, and instead use those rows to stress the fixed strict-closure
   inequality or identify a new channel-bound obstruction.

## Boundary

This obligation would close only the current q286 active selector. It would
not by itself prove Goldbach. The outer assembly, finite boundary cases,
endpoint/noncentral terms, and signed prime-correlation control remain open.

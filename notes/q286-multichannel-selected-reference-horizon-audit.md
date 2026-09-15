# q286 multichannel selected-reference horizon audit

Status: finite alternate-reference strengthening for Kevin's pre-existing
four-channel watchlist, and finite falsifier for the frozen full 17-channel LP
as an all-selected-reference horizon rescue.  This is not a selected-stress
theorem, signed-correlation theorem, pointwise character-sum theorem, or
Goldbach proof.

## Source

The generated receipt is:

```text
evidence/q286-multichannel-selected-reference-horizon-audit.json
```

The builder is:

```text
tools/build_q286_multichannel_selected_reference_horizon_audit.py
```

## Mechanism

For each selected stable/volatile dominant-floor failure reference, this audit
takes the tightest same-residue available comparison from the previous
centered `(3,1)` population receipt as a horizon center, then scans:

```text
center + 286*k,  -50 <= k <= 50
```

The selected references and centers are:

| reference | residue mod 143 | horizon center | source `(3,1)` gap |
|---:|---:|---:|---:|
| 13822 | 94 | 6000088 | 0.011314508835 |
| 24424 | 114 | 8000106 | 0.030089672469 |
| 55864 | 94 | 6000088 | 0.028481937675 |
| 164598 | 5 | 8000140 | 0.000392528741 |
| 1222142 | 64 | 8000056 | 0.019293871352 |

Every target in a reference horizon has the same residue modulo `143` as the
reference, so the stored local q286 vector cancels inside each comparison.
The tested margins are frozen LP-weighted after-local channel gaps.  No channel
weights are refit.

## Result

Across all `505` reference-target comparisons:

| subset | target failures | minimum weighted gap | mean weighted gap |
|---|---:|---:|---:|
| scalar `(3,1)` | 5 | -0.007338646230 | 0.022319769449 |
| Kevin watchlist `(5,5),(3,1),(3,11),(3,7)` | 0 | 0.010449868156 | 0.072119690289 |
| watchlist without `(3,1)` | 18 | -0.019656416725 | 0.049799920839 |
| frozen full 17 LP | 101 | -0.136747074246 | 0.061189120646 |

Per-reference result:

| reference | scalar `(3,1)` | watchlist | no `(3,1)` watchlist | full 17 LP |
|---:|---|---|---|---|
| 13822 | pass | pass | pass | fail 101 |
| 24424 | pass | pass | pass | pass |
| 55864 | pass | pass | fail 18 | pass |
| 164598 | fail 5 | pass | pass | pass |
| 1222142 | pass | pass | pass | pass |

The best aggregate pre-existing object is Kevin's four-channel watchlist.  It
passes all five selected-reference horizons and keeps the worst margin above
`0.010449868155660333`.

## Interpretation

This is a strong finite sign that the live object is not simply "all 17 LP
channels" and not scalar `(3,1)`.  The watchlist looks like a more stable
distributed cone for these selected references.

Reference `13822` is especially important: the frozen full 17 LP fails every
row in its horizon, while the four-channel watchlist passes with a large
minimum margin `0.08971939021326615`.  That supports Kevin's intuition that
`(3,1)` belongs in a stress-reference classifier story, but the classifier is
not the same thing as scalar closure.  The channel interaction matters.

Reference `55864` shows why `(3,1)` should not be casually removed from the
watchlist: the watchlist without `(3,1)` fails `18` rows there, while the full
watchlist passes.

## Post-Hoc Diagnostic

The smallest fixed subset over all 17 labels that passes all `505`
comparisons has size `2`, but this is post-hoc only.  The two passing pairs at
minimum size are:

```text
(2,6),(3,1)     minimum margin 0.002837209083
(2,10),(3,9)    minimum margin 0.000036126721
```

These pairs cannot be promoted without a non-post-hoc arithmetic or
correlation rule selecting them before this receipt.

## Decision

The residue-5 multichannel rescue generalizes across alternate selected
deficit references through Kevin's pre-existing four-channel watchlist.  The
frozen full 17-channel LP vector does not generalize to reference `13822`.

The next theorem obligation is therefore narrower and cleaner:

```text
prove or falsify a non-post-hoc positive-margin cone for
{(5,5),(3,1),(3,11),(3,7)}
against selected stress references, then test fresh unseen windows and
alternate stress/deficit predicates.
```

## Falsifier Boundary

This confirms only the finite selected-reference horizon family above.  It
does not test arbitrary stress references, unseen future windows, a broad
stress predicate, an asymptotic signed-correlation estimate, or Goldbach.

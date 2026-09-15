# q286 watchlist fresh unseen window audit

Status: finite fresh-window strengthening for scalar `(3,1)` and Kevin's
four-channel watchlist against the five selected deficit references.  It is
also another finite falsifier for the frozen full 17-channel LP vector as the
right selected-reference cone.  This is not a selected-stress theorem,
signed-correlation theorem, pointwise character-sum theorem, or Goldbach proof.

## Source

The generated receipt is:

```text
evidence/q286-watchlist-fresh-unseen-window-audit.json
```

The builder is:

```text
tools/build_q286_watchlist_fresh_unseen_window_audit.py
```

## Mechanism

The prior watchlist fresh-window lane used:

```text
24M, 28M, 32M, 36M, 40M, 44M
```

This audit uses later windows that were not used to select or replay the
watchlist:

```text
48M, 52M, 56M, 60M, 64M, 68M
```

Each window contributes `101` even targets.  For every fresh target and every
selected deficit reference `24424, 13822, 55864, 164598, 1222142`, the receipt
computes:

```text
(target empirical - reference empirical)
  - (target local q286 vector - reference local q286 vector)
```

then applies the frozen LP channel weights.  No channel selection or refitting
is performed.

## Result

There are `606` fresh unseen targets and `3030` selected-reference
comparisons.  No fresh unseen target is itself a dominant-floor deficit in the
checked q286 profile.

| subset | target failures | minimum weighted gap | mean weighted gap |
|---|---:|---:|---:|
| scalar `(3,1)` | 0 | 0.003510955559 | 0.027029683597 |
| Kevin watchlist `(5,5),(3,1),(3,11),(3,7)` | 0 | 0.002034556533 | 0.072437956033 |
| watchlist without `(3,1)` | 67 | -0.018376824958 | 0.045408272436 |
| frozen full 17 LP | 611 | -0.143214427823 | 0.060637979235 |

Per selected reference:

| reference | scalar `(3,1)` | watchlist | no `(3,1)` watchlist | full 17 LP |
|---:|---|---|---|---|
| 24424 | pass | pass | fail 15 | fail 5 |
| 13822 | pass | pass | pass | fail 606 |
| 55864 | pass | pass | fail 47 | pass |
| 164598 | pass | pass | fail 5 | pass |
| 1222142 | pass | pass | pass | pass |

## Interpretation

This strengthens Kevin's `(3,1)` stress-reference classifier hunch on fresh
unseen windows.  Scalar `(3,1)` failed the local residue-5 micro-horizon, but
it passes this broader unseen fresh-window comparison against all selected
deficit references.  So the right statement is not "scalar `(3,1)` closes
every local neighborhood"; it is closer to:

```text
selected stress references are low in centered (3,1)
against fresh clear target windows
```

The watchlist remains the more robust cone object because it also rescued the
residue-5 local horizon where scalar `(3,1)` failed.  However, `(3,1)` is
structurally important: removing it from the watchlist fails `67` unseen-window
comparisons.

The frozen full 17 LP vector fails badly again, with `611` failures.  All `606`
targets fail for reference `13822`, and five more fail for reference `24424`.
This says "more channels" is not the theorem route; the route is a selected
low-dimensional signed-correlation cone.

## Post-Hoc Diagnostic

The post-hoc smallest fixed subset across all `3030` comparisons has size `1`:

```text
(3,1)    minimum margin 0.003510955559
```

This is diagnostic only.  It can inform the next proof obligation, but it is
not a non-post-hoc theorem unless the selected-stress/fresh-window predicate is
defined independently and survives future falsifiers.

## Decision

Keep two live but distinct statements:

1. Scalar `(3,1)` is a strong selected-stress fresh-window classifier
   coordinate.
2. Kevin's watchlist `(5,5),(3,1),(3,11),(3,7)` is the stronger local-horizon
   rescue cone.

The next falsifier should test alternate non-post-hoc stress predicates and
additional fresh windows.  A theorem route must explain why selected deficit
references are low in centered `(3,1)` and why the four-channel cone repairs
the residue-local failures.

## Falsifier Boundary

This confirms only the finite fixture:

```text
selected deficit references:
  24424, 13822, 55864, 164598, 1222142
fresh unseen windows:
  48M, 52M, 56M, 60M, 64M, 68M
targets per window:
  101
```

It does not test arbitrary references, an independent stress predicate, all
future windows, an asymptotic signed-correlation estimate, or Goldbach.

# q286 selected-stress subclass audit

Status: finite selected-stress subclass audit only.  This is not a
selected-stress theorem, signed correlation theorem, pointwise character-sum
theorem, or Goldbach proof.

## Source

The generated receipt is:

```text
evidence/q286-selected-stress-subclass-audit.json
```

The builder is:

```text
tools/build_q286_selected_stress_subclass_audit.py
```

It derives from the existing checked receipts:

```text
evidence/q286-selected-deficit-provenance-audit.json
evidence/q286-centered-3-1-stress-classifier-boundary.json
evidence/q286-watchlist-fresh-unseen-window-audit.json
```

No references or channel coefficients are refit.

## Predicate

The tested non-post-hoc predicate is the natural stable/volatile
``volatile-overturn'' condition:

```text
stable_core_margin_to_floor >= 0
and the volatile rim is negative enough that dominant_margin_to_floor < 0
```

This asks whether the selected stress references are exactly rows whose
stable core would clear the q286 dominant floor, but whose volatile rim pulls
them below it.

## Result

The predicate is real but not complete.  It splits the five selected deficit
references into two subclasses:

| subclass | references |
|---|---|
| volatile_overturn | 13822, 164598, 1222142 |
| stable_core_deficit | 24424, 55864 |

Thus volatile-overturn is falsified as the whole selected-stress predicate.
Selected stress has at least two mechanisms in the checked fixture.

## Fresh Unseen Margins

Both subclasses still support `(3,1)` and Kevin's four-channel watchlist on
fresh unseen selected-reference comparisons:

| subclass | comparisons | scalar `(3,1)` failures | scalar min | watchlist failures | watchlist min |
|---|---:|---:|---:|---:|---:|
| stable_core_deficit | 1212 | 0 | 0.010958653794 | 0 | 0.005033538595 |
| volatile_overturn | 1818 | 0 | 0.003510955559 | 0 | 0.002034556533 |

The watchlist without `(3,1)` fails both subclasses: `62` failures on
stable-core-deficit rows and `5` failures on volatile-overturn rows.  The
frozen full 17 LP also fails both subclasses: `5` failures on
stable-core-deficit rows and `606` failures on volatile-overturn rows.

## Decision

The next theorem branch should not look for one scalar classifier named
``stress''.  A more honest shape is a two-subclass selected-stress problem:

```text
stable-core-deficit references: 24424, 55864
volatile-overturn references:  13822, 164598, 1222142
```

The shared finite signal is that scalar `(3,1)` and the four-channel
watchlist separate both subclasses from the checked fresh unseen rows.  The
missing proof is still a signed empirical/correlation estimate or a
non-post-hoc arithmetic predicate that predicts these subclasses before
looking at fresh margins.


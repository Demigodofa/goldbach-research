# q286 Selected-Stable Fixture Family Boundary Audit

Status: finite family-boundary audit.  This compares existing checked receipts
and fits no new channel coefficients.  It proves no selected-stress theorem,
broad stress theorem, signed correlation theorem, pointwise character-sum
theorem, or Goldbach theorem.

Receipt:

```text
tools/build_q286_selected_stable_fixture_family_boundary_audit.py
evidence/q286-selected-stable-fixture-family-boundary-audit.json
```

## Question

Could centered `(3,1)` be a stress-classifier lemma, with `13822` as one
large-negative witness?

## Result

Yes, but only in the selected-reference sense currently checked.

```text
selected references:                 5
fresh-unseen comparisons:            3,030
scalar (3,1) selected failures:      0
watchlist without (3,1) failures:    67
additional full_nonpositive refs:    89
scalar (3,1) broad failures:         32,661
selected/broad overlap:              0
```

The focus reference `13822` is a volatile-overturn witness:

```text
target:                              13822
subclass:                            volatile_overturn
centered (3,1) rank low-to-high:     2
centered (3,1) weighted value:       -0.028592853507378977
dominant margin to floor:            -0.03674434602428933
stable-core margin to floor:          0.3023670686383121
volatile rim sum to principal:       -0.3391114146626045
```

The selected five do not collapse into either subclass alone:

```text
stable_core_deficit:                 24424, 55864
volatile_overturn:                   13822, 164598, 1222142
```

A single residue class is also insufficient: modulo `143`, the selected targets
occupy residues `114`, `94`, `94`, `5`, and `64`.

## Interpretation

The supported finite statement is:

> Centered `(3,1)` is a selected-reference stress-classifier coordinate for the
> five checked selected-stable fixture deficits.

The rejected statement is:

> Centered `(3,1)` is a broad stress classifier for the baseline
> `full_nonpositive` population.

The live next step is to freeze a prospective selected-stable reference family
or bottom-rank candidate before seeing new rows.  Without that prospective
rule, the correct language is a finite selected-reference/correlation signal,
not a theorem.

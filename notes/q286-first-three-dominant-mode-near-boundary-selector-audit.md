# q286 dominant-mode near-boundary selector audit

Status: finite selector falsifier and theorem-shaping evidence only.  This is
not a selector theorem, not a signed prime-correlation theorem, and not a
Goldbach proof.

## Mechanism

The previous holdout census showed that the frozen eleven-channel full-stage
q286 dominant staircase is comfortably positive on one fresh block, while
known stress neighborhoods contain sparse tiny margins.  This audit asks the
next non-circular question:

```text
Can the near-boundary rows be selected by a simple arithmetic feature?
```

The checked simple selectors are deliberately modest:

- `N mod 286` residue membership among near-boundary rows.
- `N mod 10010` residue membership among near-boundary rows.
- scalar interval selectors induced by near-boundary rows for:
  `nonportfolio_residual_sum_to_principal`,
  `required_portfolio_for_floor`,
  `above_floor_mass_fraction`, and
  `above_floor_mass_threshold`.

The falsifier is a false positive: if the selector contains a near-boundary row
but also contains safer rows outside the same near-boundary band, that selector
does not isolate the checked near-boundary event.

## Receipt

- Function:
  `q286_first_three_dominant_mode_near_boundary_selector_audit_receipt`
- Builder:
  `tools/build_q286_first_three_dominant_mode_near_boundary_selector_audit.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-near-boundary-selector-audit.json`
- Focused regression:
  `test_q286_first_three_dominant_mode_near_boundary_selector_audit`

## Checked Windows

The full evidence evaluates `716` targets from the primary holdout and five
stress-neighborhood windows:

```text
(1200200, 211)
(1220000, 101)
(1221000, 101)
(1222000, 101)
(1240000, 101)
(1242000, 101)
```

Observed absolute surplus summary:

```text
count   = 716
minimum = 0.002859222244159798
mean    = 0.09692677451732067
maximum = 0.17012993045983027
```

There is one deficit in these checked rows: known stress target `1222142`.

## Selector Falsifiers

For near-boundary bands `.005`, `.01`, `.03`, and `.05`, the q286 residue-only
selector is falsified on the checked rows:

```text
.005 band: 2 near rows, residues 20 and 64, 8 residue false positives
.01  band: 2 near rows, residues 20 and 64, 8 residue false positives
.03  band: 3 near rows, residues 20, 64, 256, 14 residue false positives
.05  band: 8 near rows, 8 residues, 33 residue false positives
```

The `.005` near rows are:

```text
1222142 mod 286 = 64, surplus -0.002859222244159798
1242118 mod 286 = 20, surplus  0.0047979812823502055
```

But the same q286 residues also contain safer checked rows, including:

```text
1240160 mod 286 = 64, abs surplus 0.0525379332055963
1242162 mod 286 = 64, abs surplus 0.052833147281108384
1200362 mod 286 = 20, abs surplus 0.05675540221763353
```

Thus q286 residue alone cannot be the selector, even in this finite checked
dataset.

The scalar interval selectors are also falsified for every checked band.  At
the `.005` band:

```text
nonportfolio residual interval false positives: 10
required portfolio interval false positives:    10
above-floor mass interval false positives:      34
above-floor threshold interval false positives: 92
```

At the `.03` band:

```text
nonportfolio residual interval false positives: 9
required portfolio interval false positives:    9
above-floor mass interval false positives:      61
above-floor threshold interval false positives: 296
```

## Interpretation

This closes the easy selector story for the checked windows.  The sparse
near-boundary rows are not explained by `N mod 286` alone, nor by a one-scalar
residual interval.  The surviving theorem must use finer actual prime-pair
distribution inside the q286 residue classes, a signed aggregate theorem, or a
complement/lower-support rescue that makes exact near-boundary selection
unnecessary.

This falsifies only these simple selector forms on these checked rows.  It
does not refute every possible geometric or arithmetic selector.

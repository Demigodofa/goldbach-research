# q286 Dominant-Mode Pair/Complement Window Holdout

Status: finite expanded-window holdout only.  This falsifies the top-`20`
`.02` stress-box isolation as a stable checked selector on the predeclared
`72`-row window-closest denominator; it is not an arithmetic placement
theorem, signed projection theorem, or Goldbach proof.

## Mechanism

The pair/complement plane audit showed that stress-centered boxes around
`1222142` isolated the deficit on the top-`20` closest rows through epsilon
`.02`.  This receipt asks whether that local isolation survives a wider but
still predeclared denominator: the twelve closest-margin rows from each of the
six windows in the near-boundary selector audit.

For those `72` rows, it recomputes the exact q286 signed-channel profile,
sums the named pair `(1,7),(4,4)`, sums the six-channel complement, and tests
square neighborhoods around the stress row in that two-coordinate plane.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_pair_complement_window_holdout.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-pair-complement-window-holdout.json`
- Sources:
  `evidence/q286-first-three-dominant-mode-near-boundary-selector-audit.json`,
  `evidence/q286-first-three-dominant-mode-pair-complement-plane-audit.json`

## Results

The expanded `72`-row denominator still has exactly one dominant-floor
deficit, `1222142`.  The `.005` and `.01` stress-centered squares still select
only that finite deficit.

The `.02` square no longer isolates it.  Clear row `1200302` enters the same
box:

```text
1222142   deficit   pair 0.0216228924   complement -0.0870297837
1200302   clear     pair 0.0101025261   complement -0.0789977905
```

The clear row is close to the stress row in the plane:

```text
stress-plane L1 distance:   0.0195523595
stress-plane Linf distance: 0.0115203663
above-floor surplus:        0.0648396973
```

At `.03`, the square contains seven rows: the deficit plus clear rows
`1200598`, `1200302`, `1222048`, `1240136`, `1242118`, and `1242136`.

## Interpretation

The hole did not close, but it became more honest.  The pair/complement plane
is still a good microscope: `.01` isolation survives this expanded finite
holdout.  But fixed-width stress boxes are not a stable selector route, because
the `.02` top-`20` isolation breaks on a predeclared wider denominator.

The remaining theorem target is arithmetic placement of actual binary-prime
residue weights, or a signed aggregate estimate that explains why the stress
row is near the dangerous plane region without relying on a tuned box.

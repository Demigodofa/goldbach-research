# q286-WBSS K286 zero-residue raw-coverage audit

## Question

Does the current raw adverse-drag calibration horizon sample the `K_286`
target residue where reflection gives no two-mode discount?

## Answer

No.

The `K_286` two-mode reflection/parity audit found exactly one no-discount
residue at threshold `0.95`:

```text
target residue:                    0 mod 286
reflection-even energy fraction:   1.0
reflection-odd energy fraction:    1.8822507657823637e-28
centered full L2:                  50.09192896531902
reflection-even L2:                50.09192896531902
reflection-odd L2:                 6.872369429658946e-13
```

The current raw adverse-drag finite calibration has:

```text
raw calibration rows:              348
sampled mod-286 residue classes:   27
rows with target_mod_286 = 0:      0
missing no-discount residues:      [0]
```

The finite raw stress classes are different:

```text
highest raw adverse ratio class:   90 mod 286
highest raw adverse ratio:         0.23148438379145228
tightest gap/N class:              134 mod 286
tightest gap/N:                    0.26310340793692394
```

These are useful finite stress facts, but they do not calibrate the unique
`K_286` no-reflection-discount lane.

## Receipt

```text
tools/build_q286_wbss_k286_zero_residue_raw_coverage_audit.py
evidence/q286-wbss-k286-zero-residue-raw-coverage-audit.json
```

## Necessary Subtheorem

The universal raw adverse-drag theorem must include the sublane

```text
N == 0 mod 286.
```

A sufficient statement for that lane is:

```text
For every sufficiently large covered even N with N == 0 mod 286,
A_raw_-(N) < L_raw(N),
```

or an equivalent direct raw witness lower bound `W_phi(N)>0`.

## Decision

`AUDIT_zero_residue_no_discount_lane_uncovered_by_raw_finite_calibration`.

The universal raw adverse-drag theorem now has a sharper necessary sublane:
`N == 0 mod 286`.  Existing raw finite calibration does not sample that lane,
while `K_286` reflection geometry says it is the unique no-discount two-mode
residue.

Do not use the `348`-row raw margin summary as evidence that the hard `K_286`
no-discount lane has been calibrated.  A targeted zero-residue raw horizon
could be useful as a falsifier or calibration, but finite evidence remains
non-acceptance.  The proof target is still a universal pointwise unnormalized
analytic estimate.

No zero-residue raw adverse-drag theorem, universal pointwise raw estimate,
binary-prime moment theorem, q286 threshold theorem, strict-central Goldbach
theorem, or Goldbach proof is established.

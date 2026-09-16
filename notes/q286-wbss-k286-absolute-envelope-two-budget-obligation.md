# q286-WBSS K286 absolute-envelope two-budget obligation

## Question

What universal theorem obligations are exposed by the surviving finite
`K_286` absolute-envelope payment probe?

## Answer

The successful finite inequality

```text
M(N) - A_other(N) - H_286(N) > 0
```

contains two separate theorem obligations:

```text
H_286(N)   <= h(N) M(N)
A_other(N) <= a(N) M(N)
h(N) + a(N) < 1
```

for every sufficiently large covered target, plus finite remainder.

Here `H_286(N)` is the absolute real `K_286` conjugate phase-pair envelope,
and `A_other(N)` is the one-sided adverse drag from moduli `70`, `130`, and
`154`.

## Receipt

```text
tools/build_q286_wbss_k286_absolute_envelope_two_budget_obligation.py
evidence/q286-wbss-k286-absolute-envelope-two-budget-obligation.json
```

## Finite Calibration

The receipt reads the `280`-row zero-residue lift-depth probe and computes the
relative budgets:

```text
rows:                                      280
target range:                     1156012..1235806
positive two-budget margins:              280 / 280
nonpositive two-budget margins:             0 / 280

H_286 / M:       min 0.12870336618295997
H_286 / M:      mean 0.3078039780015939
H_286 / M:       max 0.7254295025978773

A_other / M:     min 0.0
A_other / M:    mean 0.02059251181570102
A_other / M:     max 0.09287286305792383

same-row sum:    min 0.13870558064782657
same-row sum:   mean 0.32839648981729497
same-row sum:    max 0.7926876143614664

same-row margin: min 0.2073123856385336
same-row margin:mean 0.671603510182705
same-row margin: max 0.8612944193521734
```

The largest `H_286/M` row and largest same-row sum are target `1201486`,
residue `286`, lift `4`:

```text
H_286/M:          0.7254295025978773
A_other/M:        0.0672581117635891
same-row sum:     0.7926876143614664
same-row margin:  0.2073123856385336
```

The largest `A_other/M` occurs elsewhere, at target `1192048`, residue `858`,
lift `3`:

```text
H_286/M:          0.3492636346726725
A_other/M:        0.09287286305792383
same-row sum:     0.4421364977305964
same-row margin:  0.5578635022694036
```

The separate finite maxima sum to `0.8183023656558012`, still below `1` on
this fixture.  That is calibration only.  A proof still needs source-backed
same-row control, or source-backed individual bounds whose sum is strictly
below `1`.

## Decision

`TARGET_k286_absolute_envelope_two_budget_theorem_required`.

The lift-depth probe exposes two separate universal obligations: bound
`H_286` relative to local main and bound `A_other` relative to local main with
strict same-row sum below `1`.  Finite fitted ratios are not theorem constants.

This proves no `K_286` absolute-envelope theorem, no companion adverse-drag
theorem, no same-row tradeoff theorem, no universal pointwise raw bound, no
q286 threshold theorem, no strict-central Goldbach theorem, and no Goldbach
proof.

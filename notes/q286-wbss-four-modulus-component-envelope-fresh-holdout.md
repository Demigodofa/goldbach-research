# q286-WBSS four-modulus component-envelope fresh holdout

## Question

The component-envelope horizon audit fitted one adverse supremum for each
projected modulus on `232` rows.  If those values are frozen, do they survive
the next fresh residue-lifts?

There are two separate claims:

```text
local_main > A_70 + A_130 + A_154 + A_286
```

and

```text
max(0, -E_d(row)) <= A_d  for each fixed d.
```

The first is a frozen sum-envelope claim.  The second is the stronger literal
per-modulus constant claim.

## Mechanism

Freeze the component adverse suprema from
`q286-wbss-four-modulus-component-envelope-horizon-audit.json`, then test the
next four period-lifts of the same `29` stressed source residues after target
`1115822`.  This gives `116` fresh rows from `1116328` through `1155862`.

## Receipt

```text
tools/build_q286_wbss_four_modulus_component_envelope_fresh_holdout.py
evidence/q286-wbss-four-modulus-component-envelope-fresh-holdout.json
```

## Result

```text
fresh targets:                              116
target range:                    1116328..1155862
actual positive rows:                       116 / 116
lambda failures:                              0
frozen sum-envelope positive rows:          116 / 116
frozen sum-envelope nonpositive rows:         0 / 116
rows with any component exceeding frozen A_d: 2
```

The frozen component supremum sum remains

```text
A_70 + A_130 + A_154 + A_286 = 0.3320872873879173.
```

The tightest frozen-envelope row is target `1118256`:

```text
local_main:        0.717245423802844
frozen envelope:   0.38515813641492663
envelope ratio:    0.4630037032891566
```

But the literal individual supremum route is falsified.  Modulus `286`
exceeds its frozen horizon value on two fresh rows.  The worst row is target
`1124642`:

```text
fresh A_286(row):  0.12551431368886537
frozen A_286:      0.12228599640255161
excess:            0.003228317286313759
```

The same row has the largest rowwise adverse-drag ratio:

```text
negative_drag_ratio:       0.23148438379145228
lambda_phi:                0.18795270138709522
adverse-only expectation:  0.6835668462365216
```

## Decision

The frozen sum-envelope survives the fresh holdout, but the literal
per-modulus frozen-constant theorem target does not.  The next theorem target
should not be a fixed list of component constants copied from the horizon.
The surviving shape is a local-main-relative adverse-drag sum bound, or a
per-modulus bound with explicit slack that can move with the target range.

This is finite targeted holdout evidence only.  It proves no per-modulus
supremum theorem, one-sided signed concentration theorem, fixed-modulus
equidistribution theorem, q286 threshold theorem, strict-central Goldbach
theorem, or Goldbach proof.  The residual absorption constants `.125`,
`.126`, and `.13` remain finite fixture fits only; no universal residual
absorption bound is established.

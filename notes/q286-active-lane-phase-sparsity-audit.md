# q286 active-lane phase/sparsity audit

## Question

The broadened source-summary coupled-slack audit found `143/226`
nonpositive rows.  Are those failures organized enough to suggest a
phase/scale theorem target, or does the apparent later success mostly reflect
sparse later source-summary rows?

## Receipt

```text
tools/build_q286_active_lane_phase_sparsity_audit.py
evidence/q286-active-lane-phase-sparsity-audit.json
```

This is derived from
`evidence/q286-active-lane-source-summary-coupled-slack-audit.json`; it does
not recompute the heavy `226` target identities.

## Result

```text
rows:                         226
positive rows:                 83
nonpositive rows:             143
target range:             90236..955832
nonpositive target range:  90236..647392
positive target range:    180208..955832
target-order sign changes:     77
pass-only suffix after:    647392
first suffix target:       650476
pass-only suffix rows:         11
blocks 8+ all positive:       yes
blocks 8+ row count:           10
block 7 mixed:                yes
```

The pass-only suffix is:

```text
650476, 658598, 733126, 741976, 775426, 782336,
805682, 818528, 828418, 846632, 955832
```

Block summary:

```text
block  rows  positive  nonpositive  max failing target
1      36    0         36           156304
2      34    2         32           237224
3      36    10        26           321326
4      32    16        16           392494
5      30    16        14           480614
6      31    16        15           568496
7      17    13        4            647392
8      1     1         0            none
9      5     5         0            none
10     3     3         0            none
11     1     1         0            none
```

The strict margin correlates with `log(N)` on this finite source-summary
fixture:

```text
corr(log target, strict margin):          0.7494686331045737
corr(log target, channel contribution):   0.7073559773555494
corr(log target, driver margin):          0.5344157614420254
corr(log target, full action):            0.5309414829961353
corr(log target, payment ratio):          0.2755034378561538
```

Residue class alone does not explain the split:

```text
mod 286 classes represented: 78
pure positive classes:       12
pure nonpositive classes:    32
mixed-sign classes:          34
```

## Decision

There is a finite pass-only suffix after target `647392`, but it is too sparse
to promote into a phase theorem.  Before the suffix, the target-ordered signs
change `77` times, block `7` is still mixed, and `34` represented mod-286
classes are mixed-sign.  Blocks `8` and later are all positive, but they
contain only `10` source-summary rows.

Decision:
`HOLD_phase_transition_supported_only_as_sparse_finite_candidate`.

The next useful theorem target is not "all large active rows pass" as a claim.
It is one of:

- prove an active-selector rarity theorem strong enough to explain why later
  source-summary rows are sparse;
- run a predeclared fresh active-row search beyond `647392` and stress every
  found active row with the frozen coupled slack scalar;
- or bypass the phase story with a direct unnormalized pointwise signed
  estimate that pays the `143` known nonpositive source-summary rows.

## Boundary

Finite phase/sparsity diagnostic only.  This proves no phase transition
theorem, active-lane theorem, pointwise adverse-drag theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof.

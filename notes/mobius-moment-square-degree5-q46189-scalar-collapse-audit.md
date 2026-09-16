# Mobius moment-square degree-5 Q46189 scalar-collapse audit

## Question

Is the negative-real scalar alignment for `Q=46189` and its
replacement family already cellwise after reduced-residue aggregation,
so the cross-ratio problem reduces to one coordinate?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_scalar_collapse_audit.py
evidence/mobius-moment-square-degree5-q46189-scalar-collapse-audit.json
```

## Result

```text
Q=46189 scalar:                    -0.07475328212536139
Q=46189 ratio minus half:          -0.0026909627652297874
replacement rows:                  10
max cellwise scalar deviation:     3.7533634042488167e-13
max ratio-reduction abs error:     8.881784197001252e-16
all replacement rows collapse:     true
all replacement rows above half:   true
```

Omitted-high-prime family scalar summaries:

```text
missing 11: rows=3 min_ratio_minus_half=0.23349735557232576 max_scalar_dev=3.7533634042488167e-13 max_ratio_error=4.440892098500626e-16
missing 13: rows=3 min_ratio_minus_half=0.4262452298052626 max_scalar_dev=2.450020888008561e-13 max_ratio_error=4.440892098500626e-16
missing 17: rows=2 min_ratio_minus_half=0.07635340770691146 max_scalar_dev=7.096046390572797e-14 max_ratio_error=8.881784197001252e-16
missing 19: rows=2 min_ratio_minus_half=0.3564899239156273 max_scalar_dev=1.1567470840626833e-13 max_ratio_error=2.220446049250313e-16
```

## Decision

The replacement-family phase-ratio checkpoint tightens to a cellwise
scalar-collapse checkpoint.  For this finite family, coordinate `12`
is a constant negative-real multiple of coordinate `00` in every
reduced-residue cell, and the cross-ratio sign reduces to the
one-coordinate active/full energy ratio.

The next theorem-shaped object is an exact divisor-pair scalar identity
plus a one-coordinate active/full ratio inequality.  This is finite
diagnostic evidence only.  It proves no exact scalar identity theorem,
symbolic replacement ratio theorem, replacement-family payment theorem,
phase-defect payment theorem, near-adverse upper bound, middle/far
lower bound, clearance-family theorem, source-start theorem,
strict-central Goldbach theorem, or Goldbach proof.

# Mobius moment-square degree-5 Q46189 source-conductor scalar formula audit

## Question

Does the explicit source-conductor coefficient formula reproduce the
common raw scalar for `Q=46189` and every replacement row?

## Formula

For source conductor `d`, write

```text
B_d = (a_d L^2, b_d L, c_d)
```

Then for an ordered source pair `(d,e)`, the checked scalar is

```text
(B_d[1] B_e[2] + B_d[2] B_e[1]) / (B_d[0] B_e[0])
= (b_d c_e + c_d b_e) / (a_d a_e L^3).
```

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_source_conductor_scalar_formula_audit.py
evidence/mobius-moment-square-degree5-q46189-source-conductor-scalar-formula-audit.json
```

## Result

```text
Q=46189 formula scalar:          -0.07475328212536136
Q=46189 raw scalar:              -0.07475328212536138
Q=46189 formula pair deviation:  2.7755575615628914e-17
replacement rows:                10
max formula-minus-raw error:     2.7755575615628914e-17
max formula pair deviation:      2.7755575615628914e-17
all replacement rows verified:   true
```

## Decision

The raw scalar identity has an explicit source-conductor formula.  The
remaining proof gap is exactness: the current coefficient pipeline is
floating/logarithmic, so the next step is exact log-polynomial
reconstruction, not more numerical aggregation.

This is finite diagnostic evidence only.  It proves no source-conductor
scalar formula theorem, exact log-polynomial identity theorem, raw
scalar identity theorem, symbolic replacement ratio theorem,
source-start theorem, strict-central Goldbach theorem, or Goldbach
proof.

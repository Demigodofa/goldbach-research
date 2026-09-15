# q286 Low (3,1) Independent Descriptor Audit

Status: finite independent-descriptor audit.  This proves no stress theorem,
signed correlation theorem, pointwise character-sum theorem, or Goldbach
theorem.

Receipt:

```text
tools/build_q286_low_3_1_independent_descriptor_audit.py
evidence/q286-low-3-1-independent-descriptor-audit.json
```

## Question

Can the scalar-selected q286 broad low-`(3,1)` groups be described by small
independent arithmetic/filter/correlation features without using centered
`(3,1)`?

## Descriptor Dictionary

The audit works inside the `89` broad `full_nonpositive` references.  The low
labels are imported from the frozen threshold receipt:

```text
low-33 selected-max threshold group:    33
strict low-24 selected-min group:       24
```

The tested atoms are independent of centered `(3,1)`:

- source filter predicates such as `first_two_active`, `first_three_tail`,
  `complement_positive`, and `complement_floor`;
- round numeric thresholds for the q286 filter ratios;
- CRT residues modulo `11`, `13`, `22`, and `26`;
- quadratic-character signs from the `11` and `13` factors;
- exploratory exact residues modulo `143`, marked post-hoc.

One- and two-atom descriptors with support at least `5` were tested.

## Result

For the low-33 group, there is a small predeclared independent pocket:

```text
descriptor:       target_mod_13 == 4
support:          6 references
low count:        6
above-threshold:  0
precision:        1.0
recall:           0.18181818181818182
references:       10664, 13810, 16748, 26056, 30164, 43268
```

This is real but small.  It captures only `6/33` of the low-33 family, and no
predeclared low-33 zero-failure descriptor has support in the later-cycle
holdout rows.

For the strict low-24 group:

```text
predeclared zero-failure descriptors:   0
best predeclared descriptor:            target_mod_13==2 AND first_two>=-0.8
support:                                5
strict-low count:                       4
above-threshold count:                  1
precision:                              0.8
recall:                                 0.16666666666666666
```

Cycle support is uneven:

```text
cycle 0: 75 broad refs, 21 low-33, 14 strict-low
cycle 1:  3 broad refs,  3 low-33,  2 strict-low
cycle 2:  5 broad refs,  4 low-33,  4 strict-low
cycle 3:  4 broad refs,  4 low-33,  3 strict-low
cycle 7:  2 broad refs,  1 low-33,  1 strict-low
```

## Interpretation

The `mod 13 == 4` pocket is a useful candidate to freeze for a future test, but
it does not define the whole low-`(3,1)` stress family.  The strict low-24 group
is even less explained by the tested independent dictionary.

So this narrows the route rather than closing it: either freeze the
`mod 13 == 4` pocket prospectively and test it on new windows/references, or
move away from classifier language and aim at a signed correlation estimate for
centered `(3,1)`.

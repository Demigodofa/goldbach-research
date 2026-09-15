# q286 three-support action decomposition

Status: finite selected-row support-action diagnostic.  This is not a
pointwise signed-prime correlation theorem, q286 threshold theorem,
strict-central Goldbach theorem, or proof of Goldbach.

## Question

The centered character-burden audit found that three lower CRT supports carry
`0.9960328792226287` of the centered coefficient energy:

```text
11x13 -> 286
7x11  -> 154
5x7   -> 70
```

This audit asks whether that coefficient-side compression is also useful on
actual hard rows.  The tested rows include early raw-action failures, the last
observed nonpositive raw action, the checked suffix start, the tight suffix
row, the fresh holdout worst row, and selected older q286 stress/control
markers.

## Result

`tools/build_q286_three_support_action_decomposition.py` generated
`evidence/q286-three-support-action-decomposition.json`.

The receipt decomposes each actual raw action as

```text
RawFull(N)
  = Principal(N)
  + E_286(N)
  + E_154(N)
  + E_70(N)
  + E_tail(N).
```

The top-three supports are action-level useful on this hard-row fixture if
`Principal+E_286+E_154+E_70` preserves the full-action sign and `E_tail` does
not decide many rows.  On this selected hard-row fixture:

```text
tested targets:                         10
full-action positive count:              7
principal+top-three positive count:      7
tail sign-decision changes:              0
full nonpositive targets:                14138, 14996, 88346
top-three nonpositive targets:           14138, 14996, 88346
tail/principal ratio range:              -0.09817000756761152..0.09363293903366753
top-three centered/principal range:      -1.9465152681346343..0.288029587486139
full/principal range:                    -0.8769412734408429..1.2597528143704648
support reconstruction relative error:   1.0369421778275708e-13
```

## Interpretation

This supports the three-support theorem target as action-level useful on the
hard-row fixture: the small-energy tail changes no sign decisions, while the
same three early raw-action failures remain nonpositive before and after the
tail is restored.

The next theorem can therefore prioritize the three dominant supports and keep
the remaining supports as an explicit small tail.  This does not mean the tail
may be discarded; it means the tail should be bounded separately after the
dominant signed-correlation terms are understood.

Either way, this is only a selected-row diagnostic.  A proof still needs
pointwise estimates for actual binary prime-pair sums.

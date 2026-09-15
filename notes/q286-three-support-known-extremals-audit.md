# q286 three-support known-extremals audit

Status: finite known-extremal support-action diagnostic.  This is not a
pointwise signed-prime correlation theorem, q286 threshold theorem,
strict-central Goldbach theorem, or proof of Goldbach.

## Question

The prior selected-row audit showed that

```text
RawFull(N)
  = Principal(N)
  + E_286(N)
  + E_154(N)
  + E_70(N)
  + E_tail(N)
```

had the same sign decisions after dropping `E_tail` on a `10`-target hard-row
fixture.  This audit asks whether that survives a stronger known-extremal
fixture: every recorded raw-action failure from the first q286 census, every
census cycle minimum, every fresh holdout cycle minimum, the fresh global
minimum, and the frozen selected hard rows.

## Result

`tools/build_q286_three_support_known_extremals_audit.py` generated
`evidence/q286-three-support-known-extremals-audit.json`.

The deduplicated fixture contains `113` targets.  On this fixture:

```text
tested targets:                         113
full-action positive count:              24
principal+top-three positive count:      40
tail sign-decision changes:              16
tail/principal ratio range:              -0.12674411748961492..0.09363293903366753
top-three centered/principal range:      -1.9465152681346343..0.288029587486139
full/principal range:                    -0.8769412734408429..1.2597528143704648
support reconstruction relative error:   1.0369421778275708e-13
```

The tail-changed targets are:

```text
10464, 10934, 11192, 11486, 11894, 12020, 14774, 14988,
15308, 18626, 22744, 24844, 30164, 30610, 34084, 40676
```

All `16` sign changes occur inside the recorded census raw-action failure
source.  The fresh holdout cycle minima have `0` tail sign-decision changes.

## Interpretation

This falsifies the stronger simplification that the small-energy tail can be
demoted to a harmless secondary term for all known q286 extremals.  The three
dominant supports remain a real spectral compression of the fixed coefficient,
and they still preserve the selected hard fixture and the fresh holdout
minima.  But on the early raw-action failures the tail is decisive often
enough that it must remain inside the proof-facing rescue inequality.

The theorem target should therefore be stated as a signed support-rescue
problem, not as a pure three-support theorem:

```text
LocalMain_a(N) + E_286(N) + E_154(N) + E_70(N) + E_tail(N) > 0.
```

A possible next candidate is to split the problem by range:

```text
early/boundary rows:  dominant supports plus signed tail rescue;
later rows:           prove a tail-stable threshold, then control top supports.
```

This is a new-to-this-task frequency-stress skeleton idea that failed in its
strongest form and survived only as a sharper boundary/correlation problem.

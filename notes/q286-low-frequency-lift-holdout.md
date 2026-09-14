# q286 low-frequency lift holdout

Status: finite held-out diagnostic.  This is not a proof of Goldbach, a
rank-`1` theorem, a lifted-dictionary theorem, or a residual-drag theorem.

## Purpose

The first lift-project dictionary audit demoted simple label-only dictionaries
as full explanations for the frozen Octave rank-`1` direction.  It preserved
one partial signal:

```text
full_low_frequency_lift
```

This holdout freezes that vector and replays it on fresh windows without
re-projecting, refitting, or using target-specific coefficients.

The generated evidence is:

```text
evidence/q286-low-frequency-lift-holdout.json
```

The builder is:

```text
tools/build_q286_low_frequency_lift_holdout.py
```

## Fixture

Fresh windows:

```text
(1260000, 101)
(1261000, 101)
(1262000, 101)
(1280000, 101)
(1281000, 101)
(1282000, 101)
```

The stress row remains `1222142`, and the same `17` outside real channels are
used.  The frozen low-frequency dictionary vector comes from
`evidence/q286-lift-project-dictionary-audit.json`; it is not recomputed from
the held-out rows.

## Result

The heldout denominator has `606` targets and no dominant-floor deficits:

```text
heldout targets: 606
heldout clears:  606
heldout deficits: 0
```

Both the frozen Octave rank-`1` direction and the frozen low-frequency lift
remain positive on every held-out clear:

```text
exact outside nonpositive count:       0
rank1 reconstructed nonpositive count: 0
low-frequency nonpositive count:       0
```

Both retain the `0.75` residual-drag cap:

```text
rank1 cap failures:         0
low-frequency cap failures: 0
```

The low-frequency lift improves on its training-window high-drag overlap:

```text
training overlap: 6/10
heldout overlap:  8/10
```

Heldout low-frequency summaries:

```text
max residual-drag ratio:       0.459721250831413 at target 1282052
mean residual-drag ratio:      0.011677508522059798
mean dictionary/full ratio:    0.836853683701855
minimum dictionary/full ratio: 0.5146117405070348
maximum dictionary/full ratio: 1.8508964151169363
minimum dictionary delta:      0.11530139784843761 at target 1280012
```

The heldout rank-`1` high-drag targets at threshold `0.2` are:

```text
1261082, 1261196, 1262162, 1280026, 1280086,
1281148, 1282052, 1282108, 1282142, 1282186
```

The low-frequency lift's top-`10` predicted high-drag targets are:

```text
1282052, 1282186, 1280086, 1281148, 1260058,
1261196, 1280026, 1282142, 1262162, 1261180
```

The overlap is `8/10`.

## External-Critique Context

Claude corrected its earlier parity claim after Kevin pasted the volatile
labels.  The corrected statement is accepted: even parity describes the
ambient `25`-label real-channel family, not the `17` outside versus `8`
volatile split.

Gemini proposed a Legendre-product sign vector
`(-1)^(floor(a/5)+floor(b/6))`.  The training-window dictionary audit scores
that vector as a falsified simple explanation: cosine about `0.355235`, one
nonpositive reconstructed delta, one `0.75` cap failure, and only `1/10`
high-drag overlap.

## Interpretation

This is the best evidence so far that the OpenAI-style representation-shift
idea is useful as a local tool, not as a solved theorem.  The low-frequency
label-lattice lift still does not explain the frozen rank-`1` direction at
the predeclared `0.9` cosine gate.  But it survives a fresh denominator with
stronger high-drag overlap than the training fixture, so it should not be
discarded as mere training-window noise.

The next useful version should add target residue or splitting data up front,
then freeze a richer dictionary and test it on another held-out denominator.
Do not retune the low-frequency coefficients on the heldout rows.

The first target-residue extension is now recorded in:

```text
notes/q286-target-residue-lift-holdout.md
```

It does not improve the static low-frequency lift.  Heldout matrix cosine
drops from about `0.8302450384` to `0.8259350681`, and high-drag overlap
drops from `8/10` to `7/10`, while positivity and the `0.75` cap still
survive.  That demotes coarse `N mod 11/13` phase features alone.

## Boundary

This holdout tightens the method-transfer lane by preserving a partial
low-frequency signal on fresh data.  It does not prove a uniform estimate, an
asymptotic theorem, any pointwise Goldbach-in-progressions theorem, or
Goldbach.

# q286 target-residue lift holdout

Status: finite heldout falsifier for one residue-augmented lift.  This is not
a proof of Goldbach, a lifted-dictionary theorem, a rank-`1` theorem, or a
residual-drag theorem.

## Purpose

The low-frequency label-lattice lift survived a fresh holdout as a local
hole-tightening tool.  The next proposed lift was to add target-residue
information up front:

```text
row features from N mod 11 and N mod 13
tensor
low-frequency channel-label features on the 17 outside q286 channels
```

The generated evidence is:

```text
evidence/q286-target-residue-lift-holdout.json
```

The builder is:

```text
tools/build_q286_target_residue_lift_holdout.py
```

## Method

The model uses only predeclared row features:

- first two Fourier harmonics of `N mod 11`;
- first two Fourier harmonics of `N mod 13`;
- Legendre symbols mod `11` and `13`;
- Legendre product;
- sum and difference phase features.

Those row features are tensored with the same low-frequency channel-label
features used by `full_low_frequency_lift`.  Ridge coefficients are fit only
on the original q286 full-window rows and then frozen.  Heldout scoring uses
the same `606` fresh targets from the low-frequency holdout.

## Result

The target-residue tensor does not improve the static low-frequency lift:

```text
training static cosine: 0.8301028273691563
training tensor cosine: 0.8254616182037086

heldout static cosine:  0.8302450383501551
heldout tensor cosine:  0.8259350681493004

heldout static high-drag overlap: 8/10
heldout tensor high-drag overlap: 7/10
```

Both models keep the `0.75` residual-drag cap and positivity alive on heldout:

```text
heldout tensor cap failures:        0
heldout tensor nonpositive deltas:  0
heldout tensor max drag ratio:      0.5198973825744712
heldout tensor mean drag ratio:     0.01731247012475308
heldout tensor mean delta/full:     0.8173438561343506
```

This is not catastrophic failure; it is a failure to improve the better
static tool.

## Decision

Demote the simple target-residue phase tensor as the next explanation for the
q286 rank-`1` shadow.  The static `full_low_frequency_lift` remains the better
finite local tool.

A farther horizon replay is now recorded in:

```text
notes/q286-low-frequency-lift-horizon-holdout.md
```

It keeps the static low-frequency lift alive on six later windows, including
stress-marker neighborhoods, with no new deficits, no positivity failures, and
no `0.75` cap failures.  The next representation shift should therefore not
merely add coarse `N mod 11/13` phase features.  It should use actual
row-dependent character-sum magnitudes, splitting/correlation data, or a
larger signed cone with explicit arithmetic coefficients.

## Boundary

This receipt refutes one residue-augmented model as an improvement over the
static low-frequency lift.  It does not refute richer number-field,
ray-class, character-sum-magnitude, or row-dependent lifts.  It proves no
uniform estimate, no asymptotic theorem, no pointwise
Goldbach-in-progressions theorem, and no Goldbach theorem.

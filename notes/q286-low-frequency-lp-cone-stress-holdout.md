# q286 low-frequency LP cone far stress holdout

Status: finite far-denominator holdout for the frozen LP cone vector.  This
is not a proof of Goldbach, an LP theorem, a Riesz-Thorin theorem, a rank-`1`
theorem, or a residual-drag theorem.

## Purpose

The previous LP cone receipt fit a bounded low-frequency vector on the
original q286 training denominator and replayed it on two heldout
denominators.  This receipt asks the next falsifier:

```text
Does that same frozen LP vector still satisfy the residual-drag cap on much
farther q286 windows, without refitting?
```

The generated evidence is:

```text
evidence/q286-low-frequency-lp-cone-stress-holdout.json
```

The builder is:

```text
tools/build_q286_low_frequency_lp_cone_stress_holdout.py
```

## Method

The selected vector is copied from:

```text
evidence/q286-low-frequency-lp-cone-audit.json
```

No coefficient is changed.  The receipt recomputes q286 signed channel
profiles on six predeclared far windows:

```text
6000000, 8000000, 10000000, 12000000, 16000000, 20000000
```

Each window contributes `101` even targets.  The same stress row `1222142` is
subtracted from the same `17` outside channels.  The replay then checks:

- exact outside delta positivity;
- rank-`1`, low-frequency, and LP reconstructed delta positivity;
- zero failures of the `0.75` residual-drag cap.

## Result

The far holdout passes:

```text
far targets:                     606
dominant-floor deficits:         0
exact nonpositive deltas:         0
LP nonpositive deltas:            0
LP 0.75 cap failures:             0
static LP cone survives holdout:  true
```

The strongest part of the result is that the LP residual drag is zero on this
far holdout: the reconstructed LP delta stays below the full outside delta on
all `606` rows.

```text
LP reconstructed delta min:  0.112824576695152 at 8000116
LP reconstructed delta mean: 0.153753329105315
LP reconstructed delta max:  0.201316015258748

full outside delta min:      0.169776829781052 at 6000008
full outside delta mean:     0.23989915510056
full outside delta max:      0.306371956392633

LP residual-drag max:        0.0
rank-1 residual-drag max:    0.086045031830256 at 10000076
low-frequency drag max:      0.157832586561158 at 10000076
```

## Interpretation

This makes the loop look tighter for the residual-cap certificate problem.  It
does **not** explain the Octave rank-`1` direction and does **not** prove a
uniform cone theorem.  It says that the frozen LP vector, selected only on the
original training rows, remains conservative and positive on a much farther
finite denominator.

The Riesz-Thorin/logistic/Laplace analogies remain theorem-shaping only.  A
real interpolation route would need an actual operator from admissible
prime-pair residue measures to residual action, plus arithmetic endpoint
bounds.  The finite LP cone is the measured shadow of that possible route, not
the theorem.

## Boundary

This is finite checked evidence.  It does not prove a pointwise signed
prime-correlation estimate, a uniform low-frequency cone, a residual-drag
bound, a rank-`1` arithmetic explanation, or Goldbach.

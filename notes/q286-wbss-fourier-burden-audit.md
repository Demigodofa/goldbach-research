# q286-WBSS Fourier burden audit

## Question

The known-theorem adequacy audit left one possible non-finite route: maybe the
WBSS adverse coefficient budget is concentrated in a few character/Fourier
modes, so a narrow signed estimate could be easier than full fixed-modulus
Goldbach in progressions.

Does the coefficient geometry support that hope?

## Method

For each projected modulus `d in {70,130,154,286}`, take the coefficient vector
`c_d(s)` from the four-modulus projection formula, subtract its mean, discard
the principal additive mode, and compute finite additive Fourier energy:

```text
energy_d(k) = |hat c_d(k)|^2 / d
```

This is a finite coefficient diagnostic only.  It is not a prime-pair
character estimate.

## Result

Global nonprincipal additive Fourier burden:

```text
nonprincipal modes:        636
total centered energy:     2965.516872883532
modes for 50 percent:        64
modes for 75 percent:       123
modes for 90 percent:       187
modes for 95 percent:       232
modes for 99 percent:       308
```

Energy by projected modulus:

```text
70:    100.8784302362658     0.03401714930664896
130:     1.6048697546301371  0.00054117707752903
154:   291.9430866202629     0.09844593679090788
286:  2571.0904862723723     0.8669957368249142
```

The dominant modulus is `286`, but it is itself not few-mode:

```text
mod 286 nonprincipal modes: 285
mod 286 modes for 90 percent: 135
mod 286 modes for 99 percent: 188
largest single mode fraction: < 0.013
```

Within modulus `286`, almost all energy sits in high conductor buckets:

```text
conductor 143: 0.49994752357905275
conductor 286: 0.49994752357905076
```

Low conductor `13` carries less than `0.00005` of the modulus-286 energy.

## Decision

The few-mode signed-character shortcut is not supported by the coefficient
geometry.  The surviving theorem target is a broad high-conductor signed
binary-prime correlation estimate, not a small character-mode lemma.

This receipt proves no signed character estimate, fixed-modulus binary-prime
discrepancy theorem, pointwise adverse-drag theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

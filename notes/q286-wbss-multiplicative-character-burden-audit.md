# q286-WBSS multiplicative-character burden audit

## Question

The additive Fourier burden audit showed that the WBSS coefficient load is not
a few additive modes.  But fixed-modulus prime AP theorems naturally use
Dirichlet/multiplicative characters on unit groups.  Does that natural basis
make the burden small enough to revive a narrow signed-character route?

## Method

Use primitive-root exponent coordinates on the unit groups:

```text
70  -> (Z/5Z)^*  x (Z/7Z)^*
130 -> (Z/5Z)^*  x (Z/13Z)^*
154 -> (Z/7Z)^*  x (Z/11Z)^*
286 -> (Z/11Z)^* x (Z/13Z)^*
```

For each projected coefficient vector, subtract the unit-group mean and take
the normalized finite Fourier transform on the exponent grid.  This is the
multiplicative character expansion of the projected coefficient vector.

## Result

Multiplicative characters compress the burden compared with additive modes,
but not to a tiny theorem:

```text
global nonprincipal characters: 248
characters for 90 percent energy: 60
characters for 95 percent energy: 65
characters for 99 percent energy: 77
```

Energy by projected modulus:

```text
70:    4.202303256501615     0.13765946911395388
130:   0.033203298015735544  0.00108767694730429
154:   4.86557474436001      0.15938698265209394
286:  21.425719970586837     0.7018658712866479
```

The dominant modulus `286` is still broad:

```text
mod 286 nonprincipal characters: 119
mod 286 characters for 90 percent energy: 43
mod 286 characters for 99 percent energy: 50
largest mod-286 character fraction: < 0.032
```

Comparison with additive burden:

```text
additive global modes for 99 percent:          308
multiplicative global characters for 99 percent: 77
additive mod-286 modes for 99 percent:          188
multiplicative mod-286 characters for 99 percent: 50
```

## Decision

Multiplicative characters are the right language and they meaningfully compress
the finite coefficient burden.  But the small signed-character shortcut still
does not survive: the theorem target is a broad multiplicative-character
binary-prime correlation package, not a one-character or few-character lemma.

This receipt proves no multiplicative-character theorem, fixed-modulus
binary-prime discrepancy theorem, pointwise adverse-drag theorem, q286
threshold theorem, strict-central Goldbach theorem, or Goldbach proof.

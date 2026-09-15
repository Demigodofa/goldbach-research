# q286-WBSS Four-Modulus Edge-Character Audit

Status: finite coefficient-algebra evidence only. Goldbach is not proved.

## Question

The CRT factor-ANOVA audit explains why the coefficient target needs the four
moduli `70,130,154,286`. Fourier sparsification did not produce a smaller
coefficient theorem. This audit asks a different question: once the four
edges are accepted, what exact character-sum obligations would a future
binary-prime theorem need to control?

## Mechanism

For each nonzero ANOVA component, order each unit group `(Z/pZ)^*` by a
primitive-root exponent and take the normalized finite Fourier transform.
This is the multiplicative character expansion on the active CRT factors.

The receipt verifies both inverse reconstruction and Parseval energy, so the
translation is an exact finite change of basis for the existing coefficient
components.

## Receipt

```text
tools/build_q286_wbss_four_modulus_edge_character_audit.py
evidence/q286-wbss-four-modulus-edge-character-audit.json
```

## Result

The nonzero supports remain exactly the factor-ANOVA supports:

```text
empty
5
7
11
13
5,7
5,13
7,11
11,13
```

There are no three-factor or four-factor character obligations. The edge
obligations have no nonzero principal-axis terms at audit tolerance. The
fully nonprincipal edge-character counts are:

```text
5,7    ->  8
5,13   -> 17
7,11   -> 23
11,13  -> 50
total  -> 98
```

The singleton/AP side has `12` nonzero character terms, for `110` nonconstant
terms total. The maximum Parseval error is below `2e-15`; the maximum inverse
reconstruction error is below `5e-15`.

## Decision

This is a sharper analytic obligation list, not a smaller coefficient
theorem. A future proof route would need to control the signed binary-prime
correlations against the listed fully nonprincipal edge characters, plus the
singleton/AP and constant terms already separated by the coefficient
decomposition.

The residual absorption constants `.126` and `.13` remain finite fixture fits
only. They are not universal bounds.

No character-sum bound, binary-prime projection-control theorem, signed
discrepancy theorem, q286 threshold theorem, strict-central Goldbach theorem,
or Goldbach proof is established here.

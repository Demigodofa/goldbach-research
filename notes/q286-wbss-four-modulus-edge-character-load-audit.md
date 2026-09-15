# q286-WBSS Four-Modulus Edge-Character Load Audit

Status: finite row-load diagnostic only. Goldbach is not proved.

## Question

The edge-character audit named `98` fully nonprincipal edge-character
obligations across the four CRT edges. This audit asks how the existing
strict-central binary-prime rows load those obligations.

This is not a theorem-reduction step. It is a prioritization test: if the
finite data is concentrated on one edge or a small prefix of character groups,
that may identify the next analytic target, but omitted terms cannot be
discarded without a universal bound.

## Mechanism

For each of the `230` available lower-face dual-edge rows, compute the
actual-minus-local-uniform strict-central prime-pair distribution on each CRT
edge:

```text
5,7
5,13
7,11
11,13
```

Then replay the exact edge-character basis from
`q286-wbss-four-modulus-edge-character-audit.json` against those row
discrepancies. The receipt groups conjugate character modes so each grouped
contribution is real.

## Receipt

```text
tools/build_q286_wbss_four_modulus_edge_character_load_audit.py
evidence/q286-wbss-four-modulus-edge-character-load-audit.json
```

## Result

The edge-character basis reconstructs the row loads with maximum error below
`2e-14` on all rows.

Across all `230` rows, the sum of the four edge signed contributions is
negative on every row:

```text
minimum: -2.0365751016482774
mean:    -0.5529256424042925
maximum: -0.21377190910116042
```

The dominant absolute edge is:

```text
11,13 -> 227 rows
7,11  ->   2 rows
5,7   ->   1 row
5,13  ->   0 rows
```

On the `196` post-discovery rows, `11,13` is the dominant absolute edge on
all `196` rows, and the edge signed contribution sum is negative on all
`196` rows.

The coefficient obligations have `50` conjugate character groups in total.
Finite absolute row-load concentration is not tiny:

```text
rank needed for 50% absolute load: 16 groups
rank needed for 80% absolute load: 29 groups
rank needed for 90% absolute load: 33 groups
```

The top finite-load group is on edge `11,13` at representative frequency
`(3,7)`, carrying about `4.07%` of the total absolute group load.

## Decision

The finite data strongly points to the `11,13` edge as the first analytic
stress target. It does not justify dropping the other edges or most character
groups. A tiny character shortcut is not supported by this fixture.

The next theorem-shaped target is a signed binary-prime estimate for the
`11,13` edge-character family, with enough residual control for the remaining
edge groups. Without that theorem-level residual control, this audit is only
finite prioritization evidence.

No character-sum bound, binary-prime projection-control theorem, signed
discrepancy theorem, q286 threshold theorem, strict-central Goldbach theorem,
or Goldbach proof is established here.

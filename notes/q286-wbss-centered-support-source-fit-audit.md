# q286-WBSS centered-support source-fit audit

## Question

Do currently named source-shaped theorem families pay the four q286
centered-support raw bucket inequalities?

## Receipt

```text
tools/build_q286_wbss_centered_support_source_fit_audit.py
evidence/q286-wbss-centered-support-source-fit-audit.json
```

## Required Shape

For every sufficiently large covered even `N`, before any division by actual
`T_N`, prove

```text
K_B(N) >= -beta_B * P0_a(N)
```

for each bucket

```text
dominant_286
dominant_154
dominant_70
tail
```

with the ledger budget from
`q286-wbss-centered-support-inequality-ledger.json`.

An ordinary positive-mass theorem proving `P0_a(N)>0` or `T_N>0` is not enough
unless it also supplies the signed centered bucket lower bounds.  The combined
coefficient is sign-indefinite on every target support, so mass can exist
without landing in a favorable signed shape.

## Source Fit

No named source family currently pays the four raw bucket inequalities.

```text
BMOR explicit AP prime counts:
  one-dimensional AP marginals; no reflected binary-pair correlation.

Bhowmik-Halupczok-Matsumoto-Suzuki:
  average AP Goldbach information; not pointwise every covered N.

Salmensuu:
  almost-all AP Goldbach; exceptional targets remain unpaid.

Halupczok:
  mean-value AP Goldbach information; not the bucket lower bounds.

Lichtman:
  distribution/upper-bound context; not positive one-sided bucket control.

ordinary positive mass:
  creates support but does not control signed centered placement.
```

## Decision

`SOURCE_FIT_no_existing_centered_bucket_bridge`.

The next evidence-bearing step is a character-expanded `K_286` target, or a
sharper combined ledger that reduces the source theorem required.  This is a
source-fit audit only.  It proves no source theorem fit, major/minor arc
estimate, pointwise centered-error estimate, signed prime-correlation theorem,
positive-mass theorem, q286 threshold theorem, strict-central Goldbach theorem,
or Goldbach proof.

# Mobius moment-square degree-5 ell-freeze perturbation stress

## Question

The weak-block degree-`5` active/full dominance check had its smallest margin
at `M=167`, prime `181`, component `(00,12)`, using the source active-window
choice `ell_freeze=52`.  Does that dominance survive a small perturbation of
the logarithmic coefficient freeze, or is it an exact fitted-coefficient
artifact?

## Mechanism

Keep the weak scale `M=167`, row count `35`, divisor range `[3,16]`, and the
same prime rows in `[167,334]`.  In this implementation `ell_freeze` enters
the lifted polynomial coordinates through `log(modulus * ell_freeze)`; it does
not translate the active row set, which remains determined by `row_count`.
Replace the source `ell_freeze=52` by

```text
50, 51, 52, 53, 54
```

For each `ell_freeze`, test the three degree-`5` component rows
`(00,12)`, `(01,02)`, and `(01,11)` and their degree-`5` total.  Under the
negative signed-full premise, the target is

```text
active/full > 1/2
```

for every checked row.

## Receipt

```text
tools/build_mobius_moment_square_degree5_ell_freeze_perturbation_stress.py
evidence/mobius-moment-square-degree5-ell-freeze-perturbation-stress.json
```

## Result

```text
status:                      STRESS_degree5_ell_freeze_perturbation_dominance
scale:                       M=167
base ell_freeze:             52
tested ell_freezes:          50, 51, 52, 53, 54
prime count per ell:         29
component rows:              435
degree-5 total rows:         145
all dominance rows:          580
dominance slacks:            +580 / 0 / 0
failure rows:                0
weakest row:                 ell=53, p=181, (00,12)
weakest active/full ratio:   0.5563677490893759
weakest slack above 1/2:     0.05636774908937592
```

## Decision

The weak-scale ell-freeze perturbation stress survives the checked window.
Every component and degree-`5` total row for `ell_freeze=50..54` retains
positive active/full dominance slack above one half.  This reduces the concern
that the finite weak-block result is only an exact logarithmic
`ell_freeze=52` coefficient fit.  It does not test translations of the active
row window itself.

This is still finite perturbation evidence only.  It proves no ell-freeze
dominance theorem, checked-scale dominance theorem, primewise dominance
theorem, degree-`5` coefficient theorem, robust-margin universal theorem,
coefficient-family theorem, universal Sturm-certificate theorem,
half-frame curve-positivity theorem, uniform active/full lower-frame theorem,
Mobius covariance theorem, signed prime-correlation estimate, q286 theorem,
strict-central Goldbach theorem, or Goldbach proof.

# Mobius moment-square degree-5 active-window translation stress

## Question

The weak-block degree-`5` active/full dominance check had its smallest margin
at `M=167`, prime `181`, component `(00,12)`, using the source active row
window `[35,70)`.  Does that dominance survive a small translation of the
actual active row interval, or is it an exact fitted-window artifact?

## Mechanism

Keep the weak scale `M=167`, row count `35`, coefficient freeze
`ell_freeze=52`, divisor range `[3,16]`, and the same prime rows in
`[167,334]`.  Replace the source active row start `35` by

```text
33, 34, 35, 36, 37
```

For each active row start, test the three degree-`5` component rows
`(00,12)`, `(01,02)`, and `(01,11)` and their degree-`5` total.  Under the
negative signed-full premise, the target is

```text
active/full > 1/2
```

for every checked row.

## Receipt

```text
tools/build_mobius_moment_square_degree5_active_window_translation_stress.py
evidence/mobius-moment-square-degree5-active-window-translation-stress.json
```

## Result

```text
status:                      STRESS_degree5_active_window_translation_dominance
scale:                       M=167
ell_freeze:                  52
tested active row starts:    33, 34, 35, 36, 37
prime count per window:      29
component rows:              435
degree-5 total rows:         145
all dominance rows:          580
dominance slacks:            +580 / 0 / 0
failure rows:                0
weakest row:                 start=36, p=181, (00,12)
weakest active/full ratio:   0.5490505738773274
weakest slack above 1/2:     0.049050573877327364
```

## Decision

The weak-scale active-window translation stress survives the checked window.
Every component and degree-`5` total row for active row starts `33..37`
retains positive active/full dominance slack above one half.  This reduces the
concern that the finite weak-block result is only an exact active interval
fit.  Unlike the logarithmic coefficient-freeze perturbation, this row-window
translation changes the weakest margin: the tightest checked row moves to
active start `36`, still at prime `181`, component `(00,12)`.

This is still finite perturbation evidence only.  It proves no active-window
translation theorem, ell-freeze dominance theorem, checked-scale dominance
theorem, primewise dominance theorem, degree-`5` coefficient theorem,
robust-margin universal theorem, coefficient-family theorem, universal
Sturm-certificate theorem, half-frame curve-positivity theorem, uniform
active/full lower-frame theorem, Mobius covariance theorem, signed
prime-correlation estimate, q286 theorem, strict-central Goldbach theorem, or
Goldbach proof.

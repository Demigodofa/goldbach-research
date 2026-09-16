# Mobius moment-square active/full ratio audit

## Question

The previous metric audit showed that the moment-square curve is nearly null
in the diagonal-equilibrated full metric.  Does that soft direction actually
damage the active/full lower-frame comparison?

## Receipt

```text
tools/build_mobius_moment_square_active_ratio_audit.py
evidence/mobius-moment-square-active-ratio-audit.json
```

## Result

The moment-square active/full ratio stays above one-half on all checked
scales:

```text
M=127  curve minimum = 0.9550886746317355
M=149  curve minimum = 1.0532480893102447
M=167  curve minimum = 0.9441389892658896
M=191  curve minimum = 1.0095242944137615
M=211  curve minimum = 1.003155174351695
M=227  curve minimum = 1.0141489569542175
```

At the diagonal-equilibrated full-soft parameter from the metric audit, the
active/full ratio also stays above one-half:

```text
M=127  ratio = 0.9122467414896579
M=149  ratio = 0.9731344451400642
M=167  ratio = 0.9193340666498803
M=191  ratio = 1.0446330408914968
M=211  ratio = 1.056847133906995
M=227  ratio = 1.052376135179263
```

## Decision

The metric-soft moment-square direction is not an adverse lower-frame
direction on the checked scales.  The next theorem target is therefore not
merely raw support activation; it is to prove that the metric-soft
moment-square channel remains active-paid.

This is finite diagnostic evidence only.  No moment-square active-payment
theorem, uniform active/full lower-frame theorem, Mobius covariance theorem,
signed prime-correlation estimate, q286 theorem, strict-central Goldbach
theorem, or Goldbach proof is established.

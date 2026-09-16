# Mobius moment-square degree-5 Q46189 exception bound audit

## Question

For the `M=229`, `p=379`, `Q=46189` middle-family exception, can a simple
row-independent Cauchy or triangle estimate provide the independent bound
needed by the clearance logical bridge?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_exception_bound_audit.py
evidence/mobius-moment-square-degree5-q46189-exception-bound-audit.json
```

## Fixture

```text
M:                         229
p:                         379
A:                          43
p*A:                     16297
Q:                       46189
Q factorization:       11*13*17*19
Q/(p*A):       2.8342026139780327
residue cells:             34560
target label:              00,12
```

## Result

The exact target contribution is adverse:

```text
active contribution:              -1560644479591.6313
full contribution:                -3138178401642.2075
full/2 - active margin:              -8444721229.472412
adverse / |full/2|:                 0.0053819255304627
```

But the simple Cauchy route is far too weak:

```text
active / active Cauchy bound:       -1.0000000000000002
full / full Cauchy bound:           -1.000000000000004
Cauchy adverse budget / actual:    370.61420920442464
simple Cauchy proves nonadverse:    false
```

So the exception is not a large uncontrolled term.  It is a small gap between
two very large, nearly perfectly aligned negative terms:

```text
|active_Q| - |full_Q|/2 = 8444721229.472412
```

In the full clearance ledger this adverse denominator is small relative to
available middle/far positive mass:

```text
Q46189 adverse / middle-far positive = 0.00035683847866709636
Q46189 adverse / all negative margin = 0.34560555171301166
```

## Decision

`HOLD_q46189_simple_cauchy_bound_insufficient`.  The denominator exception is
localized and small in the finite ledger, but generic Cauchy/triangle control
is much too weak.  Future work should seek a phase-defect or
neighboring-denominator payment estimate before promoting the clearance route.

Smallest next test: derive a symbolic expression for the active/full
saturation defect of `Q=46189` and test whether it factors through the missing
small primes `2,3,5,7` or through row-window endpoint phases.

This is a finite exception audit only.  It proves no simple Cauchy theorem,
phase-defect theorem, near-adverse upper bound, middle/far lower bound,
clearance-family theorem, source-start theorem, strict-central Goldbach
theorem, or Goldbach proof.

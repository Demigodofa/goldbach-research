# Degree-5 translated puncture audit

## Question

After the broad active-window translation statement was finitely falsified,
does the lone translated failure behave like a monotone edge-distance effect,
or like an isolated arithmetic puncture?

## Mechanism

Read the source-admissible audit and the checked-scale phase-curve sweep.  For
each broad failure row, recompute the same scale, prime, and component across
all translated active row starts.  Then check whether the failing start is a
boundary band or a puncture surrounded by passing starts.

```text
tools/build_mobius_moment_square_degree5_translated_puncture_audit.py
evidence/mobius-moment-square-degree5-translated-puncture-audit.json
```

## Result

The lone broad translated failure is an isolated puncture:

```text
scale:                         M=149
prime:                         p=163
component:                     (00,12)
source active row start:       32
active row start range:        0..64
failing active row starts:     1
passing intervals:             0..0 and 2..64
failure slack above 1/2:       -0.0019533329245732256
source start passes:           true
left far edge start 0 passes:  true
right neighbor start 2 passes: true
```

So the failure is not simply the far-left boundary becoming too distant from
the source.  Start `0` is farther from the source start `32` than start `1`,
but start `0` passes while start `1` fails.  The source-connected passing
interval remains `2..64`.

## Decision

The source-window/admissible-window route remains alive, but a future theorem
should not model the translated pass set as a simple centered interval around
the source.  The next theorem-shaped target needs an arithmetic
source-admissibility condition or a source-window implication theorem, not a
distance-only translated-window rule.

This is finite diagnostic evidence only.  No source-window implication
theorem, source-admissible window theorem, phase-curve theorem,
active-window translation theorem, pointwise universal adverse-drag estimate,
q286 threshold theorem, strict-central Goldbach theorem, or Goldbach proof is
established.

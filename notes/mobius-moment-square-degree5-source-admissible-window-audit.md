# Mobius moment-square degree-5 source-admissible window audit

## Question

The broad checked-scale phase-curve sweep found a finite falsifier when every
translated active row start `0..2A` was admitted.  Does the same evidence
still support a narrower source-admissible theorem target around the canonical
source window?

## Mechanism

This is a derived audit from two validated receipts:

```text
evidence/mobius-moment-square-degree5-checked-scale-phase-curve-sweep.json
evidence/mobius-moment-square-degree5-checked-scale-dominance-audit.json
```

The broad sweep checked every active row start for the six checked scales and
found exactly one failing dominance row.  This audit converts that row-level
falsifier into a scale-wise start map, then checks whether each canonical
source start

```text
active_row_start = row_count
```

still lies inside a passing interval.

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_admissible_window_audit.py
evidence/mobius-moment-square-degree5-source-admissible-window-audit.json
```

## Result

```text
status:                         DERIVE_degree5_source_admissible_window_audit
total active row starts:         440
passing active row starts:       439
failing active row starts:         1
source starts failing:             0
broad failure row count:           1
```

The single failing translated start is:

```text
M=149, active_row_start=1, p=163, (00,12)
```

The canonical source start for `M=149` is `32`, and the source-connected
passing interval is:

```text
2..64
```

So the failing translated start is not in the source-connected interval.  The
nearest failing start is distance `31` away from the canonical source start.

The weakest canonical source-start scale remains the original checked-scale
weak row:

```text
M=167, p=181, (00,12)
active/full ratio: 0.5563677490893767
slack above 1/2:   0.056367749089376695
```

## Decision

The broad all-translation statement is dead, but the checked source-window
statement is not.  The finite evidence now points to a narrower theorem-shaped
target:

```text
prove source-window or admissible-window control,
not dominance for every translated window 0..2A.
```

This matters because a universal pointwise adverse-drag estimate must know
which local window is logically connected to the Goldbach target.  A translated
window can be a useful stress test, but the finite falsifier shows it is not a
valid theorem quantifier by itself.

This is finite source-admissible-window evidence only.  It proves no
source-admissible window theorem, pointwise universal adverse-drag estimate,
L2 logical bridge, phase-curve theorem, checked-scale dominance theorem,
primewise dominance theorem, robust-margin universal theorem, signed
prime-correlation theorem, q286 theorem, strict-central Goldbach theorem, or
Goldbach proof.

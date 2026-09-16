# q286 residual structural-mask tail-stress audit

Status: finite theorem-budget audit.  This is not a structural-mask theorem,
tail-bound theorem, support-packet theorem, character-sum theorem, signed
binary-prime correlation theorem, q286 threshold theorem, strict-central
Goldbach theorem, or Goldbach proof.

## Question

The structural-mask audit found a seven-packet two-subcube mask that certifies
the five positive rows when the omitted tail is bounded by an adverse envelope
fit only on those same positive rows.

Does that adverse-tail bound survive a harsher envelope taken over all seven
frozen signed-pair operator targets?

## Mechanism

Compare two omitted-tail envelopes:

```text
positive-row envelope: sup over the five actual full-positive rows
all-row envelope:      sup over all seven frozen rows
```

Then evaluate the positive rows with each envelope.

## Receipt

```text
tools/build_q286_residual_structural_mask_tail_stress_audit.py
evidence/q286-residual-structural-mask-tail-stress-audit.json
```

## Result

The seven-packet two-subcube mask fails the all-row adverse-tail stress:

```text
positive-row tail envelope: 0.16918918294282279
positive-row tight margin:  0.005504640544899547
all-row tail envelope:      0.513201992453516
all-row tight margin:      -0.3385081689657937
tight target:               94856
```

The symmetric `support size <= 2` mask also fails:

```text
positive-row tail envelope: 0.04969241094998337
positive-row tight margin:  0.004018492886067315
all-row tail envelope:      0.240935485957854
all-row tight margin:      -0.18722458212180332
```

The full `15`-packet signed package remains the control: it has no omitted
tail and its tight positive-row margin is the actual full action at `94856`,
about `0.012576466293799798`.

## Decision

The structural support masks do not survive an unqualified all-row adverse-tail
envelope.  The earlier structural-mask candidate remains useful only if one of
the following becomes a theorem:

```text
1. a mathematically defined positive/stable class whose tail envelope is small;
2. signed control of the omitted tail instead of adverse supremum control;
3. a broader signed support-packet package, possibly the full 15-packet object.
```

This is a sharper HOLD, not a theorem.  It rejects the unqualified adverse-tail
version of the structural-mask route on the frozen seven-row stress fixture.
Goldbach remains open.

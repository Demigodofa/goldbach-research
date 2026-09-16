# Mobius moment-square degree-5 Q46189 middle-loss condition gap audit

## Question

Does the checked replacement landscape support a nontrivial
middle-loss conditional compensation principle, or only the singleton
`q=38038` locator?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_middle_loss_condition_gap_audit.py
evidence/mobius-moment-square-degree5-q46189-middle-loss-condition-gap-audit.json
```

## Result

```text
replacement rows:                  34
worst middle-loss row:             38038
worst middle A..10A:               -0.939992990438763
worst non-middle sum:              0.09269980585259228
second middle-loss row:            41990
second middle A..10A:              -0.43222079205102754
second non-middle sum:             -0.10078449680431602
middle-loss isolation gap:          0.5077721983877355
first prefix failure size:          2
first prefix failure denominator:   41990
middle/non-middle Pearson:          -0.07010130361032416
```

The second-worst middle-loss row is already a counterexample to a
plain threshold principle: `q=41990` has negative non-middle
contribution.  Thus the checked condition that works is singleton
unless an input-side source-factor invariant explains why `q=38038`
is isolated.

## Decision

The live target should not be a bare middle-loss threshold.  It must
be a source-factor isolation explanation that distinguishes the
missing-17 small-(2,7) packet `q=38038` from the missing-11
small-(2,5) packet `q=41990` before making a compensation claim.

This is finite diagnostic evidence only.  It proves no middle-loss
compensation theorem, source-factor isolation theorem, replacement
packet compensation theorem, strict-central Goldbach theorem, or
Goldbach proof.

# Mobius moment-square degree-5 Q46189 all-replacement mirror compensation audit

## Question

Across all `34` replacement packets, is the `q=38038` mirror-block
non-middle compensation pattern a universal replacement-packet theorem
target?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_all_replacement_mirror_compensation_audit.py
evidence/mobius-moment-square-degree5-q46189-all-replacement-mirror-compensation-audit.json
```

## Result

```text
replacement rows:                         34
weakest total row:                        38038
weakest middle-loss row:                  38038
q=38038 off/diag-half:                    -0.8472931845861708
q=38038 middle A..10A:                    -0.939992990438763
q=38038 non-middle sum:                   0.09269980585259228
q=38038 strongest mirror block:           0.07765412336759717
q=38038 strongest mirror rank:            9
negative non-middle rows:                 15
nonpositive best-mirror rows:             7
```

## Decision

The broad mirror-block theorem target is refuted on the checked
replacement landscape.  Fifteen replacement rows have nonpositive
aggregate non-middle contribution, and seven have nonpositive best
mirror-block non-middle contribution.

`q=38038` is still special, but in a narrower way: it remains both
the weakest total row and the most severe `middle_A_to_10A` loss row,
and that tight row has positive non-middle compensation.  The live
theorem target should therefore be conditional compensation in the
tight middle-loss regime, not universal mirror-block positivity
across all replacement packets.

This is finite diagnostic evidence only.  It proves no universal
mirror-block theorem, tight-middle-loss theorem, replacement-packet
compensation theorem, strict-central Goldbach theorem, or Goldbach
proof.

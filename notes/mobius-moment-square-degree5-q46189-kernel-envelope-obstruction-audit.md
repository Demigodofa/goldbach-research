# Mobius moment-square degree-5 Q46189 kernel-envelope obstruction audit

## Question

Could the finite nonadverse bound
`off_diagonal_total / diagonal_half > -1` be proved by independent
per-bucket or per-ranked-gap lower bounds?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_kernel_envelope_obstruction_audit.py
evidence/mobius-moment-square-degree5-q46189-kernel-envelope-obstruction-audit.json
```

## Result

```text
true weakest nonadverse q:                  38038
true weakest nonadverse off/diag-half:      -0.8472931845861708
target lower bound:                         -1.0
disconnected bucket-minimum sum:            -1.8966400770509377
disconnected top-negative rank-minimum sum: -1.4111403765125132
```

Worst bucket contributors:

```text
near_1_to_A: q=21318 value=-0.41527096393053714
middle_A_to_10A: q=38038 value=-0.939992990438763
far_10A_to_100A: q=67830 value=-0.3917777860671962
tail_over_100A: q=19019 value=-0.14959833661444127
```

## Decision

Simple independent component bounds are too weak.  The true checked
same-row minimum is still safely above `-1`, but disconnected bucket
and ranked-gap worst cases both fall below `-1`.  The theorem target
must therefore use co-occurrence, factor geometry, or another
structured correlation between adverse components.

This is finite diagnostic evidence only.  It proves no simple bucket
bound theorem, simple rank bound theorem, co-occurrence kernel bound
theorem, coordinate-00 residue-gap sign theorem, strict-central
Goldbach theorem, or Goldbach proof.

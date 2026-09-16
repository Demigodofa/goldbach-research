# Mobius moment-square degree-5 source-start M=383 full prime sweep

## Question

Does the next complete source-start sweep after `M=379` preserve signed
active/full dominance and the coherent prime-block stress morphology?

## Mechanism

Use the canonical source-start construction at `M=383` and evaluate every
prime `p` in `[383,766]`.  The runner writes a partial checkpoint while
computing and removes it after a complete successful receipt.

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_start_m383_full_prime_sweep.py
evidence/mobius-moment-square-degree5-source-start-m383-full-prime-sweep.json
```

## Result

```text
status:                         SWEEP_degree5_source_start_m383_full_prime_rows
prime rows:                     60
dominance rows:                 240
all rows dominate 1/2 signed:   true
minimum slack:                  0.4215742230435717
tightest prime block:           p=599
weakest row:                    p=599, (00,12)
top-four labels:                (00,12), TOTAL, (01,11), (01,02)
top-four single prime block:    true
second tightest block:          p=691
checkpoint removed:             true
```

## Decision

The full `M=383` source-start sweep survives signed dominance.  The tightest
rows remain a coherent `p=599` prime block, so this is not a split-block
falsifier of the finite morphology candidate.

This is one complete fresh scale only.  It proves no prime-block theorem,
source-start theorem, source-window theorem, strict-central Goldbach theorem,
or Goldbach proof.

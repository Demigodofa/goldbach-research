# Mobius moment-square degree-5 Q46189 far-tail sign-budget audit

## Question

Does the `Q=46189` broad far-tail/non-middle separator come from a
larger negative envelope or from signed balance inside the broad
residue-gap budget?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_far_tail_sign_budget_audit.py
evidence/mobius-moment-square-degree5-q46189-far-tail-sign-budget-audit.json
```

## Result

```text
Q far-tail positive share:              0.46018216105950077
min replacement far-tail positive share:0.4744728648999872
far-tail positive-share gap:            0.014290703840486418
Q non-middle positive share:            0.4536488257511242
min replacement non-middle positive share:0.4562706474233753
non-middle positive-share gap:          0.0026218216722511123
```

The negative-envelope shortcut fails:

```text
Q far-tail negative / diag:             -3.9560065034797907
min replacement far-tail negative / diag:-4.043709440655922
Q non-middle negative / diag:           -4.2512968003219544
min replacement non-middle negative / diag:-4.243502046248286
```

## Decision

The broad pressure separator is a signed-balance effect.  The negative
far-tail envelope alone does not separate `Q=46189` from the
replacements; `q=53295` is slightly worse by that metric.  The finite
separator is the positive share of the broad absolute budget,
especially in far+tail.

The next theorem-shaped target is a broad signed-balance lower bound.
This is finite selected-family diagnostic evidence only.  It proves no
far-tail positive-share theorem, non-middle positive-share theorem,
far-tail pressure theorem, replacement residue-gap bound theorem,
coordinate-00 residue-gap sign theorem, strict-central Goldbach
theorem, or Goldbach proof.

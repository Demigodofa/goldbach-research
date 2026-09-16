# Mobius moment-square degree-5 Q46189 replacement phase profile

## Question

Do the `Q=46189` replacement-family payment rows share the same
coordinate phase structure while moving to the paying side of the
one-half active/full cross-ratio threshold?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_replacement_phase_profile_audit.py
evidence/mobius-moment-square-degree5-q46189-replacement-phase-profile-audit.json
```

## Result

```text
M, p, label:                         229, 379, 00,12
Q=46189 ratio minus half:            -0.0026909627652297874
Q=46189 margin:                      -8444721229.472412
replacement rows:                    10
replacement ratio-minus-half min:    0.07635340770691146
replacement ratio-minus-half max:    0.5735414442150175
replacement positive margin sum:     14694916931621.637
replacement payment / defect:        1740.1304948156007
max replacement scalar residual:     6.049037211162891e-16
```

Omitted-high-prime family phase summaries:

```text
missing 11: rows=3 min_ratio_minus_half=0.23349735557232576 payment/defect=653.9359290761917 max_scalar_residual=5.789106817647642e-16
missing 13: rows=3 min_ratio_minus_half=0.4262452298052626 payment/defect=466.9478641031054 max_scalar_residual=2.419467554750184e-16
missing 17: rows=2 min_ratio_minus_half=0.07635340770691146 payment/defect=320.0147481014071 max_scalar_residual=6.049037211162891e-16
missing 19: rows=2 min_ratio_minus_half=0.3564899239156273 payment/defect=299.23195353489666 max_scalar_residual=2.634435187289472e-16
```

## Decision

The finite group-payment result has a phase-ratio explanation:
`Q=46189` is below the one-half threshold, while every checked
replacement denominator is above it.  This is evidence for a symbolic
replacement ratio inequality as the next theorem target.

This remains finite diagnostic evidence only.  It proves no symbolic
replacement ratio theorem, replacement-family payment theorem,
phase-defect payment theorem, near-adverse upper bound, middle/far
lower bound, clearance-family theorem, source-start theorem,
strict-central Goldbach theorem, or Goldbach proof.

# q286-WBSS raw adverse-drag theorem target

## Question

Can the q286-WBSS adverse-drag gate be stated as a genuinely raw, pointwise,
unnormalized theorem target, so that it does not assume strict-central mass
before proving a witness?

## Mechanism

Use the raw witness identity audit to define, for each covered even `N`,

```text
T_N       = sum log(p)log(N-p)
L_raw(N) = T_N * M(N)
U_d(N)   = T_N * E_d(N)
A_raw_-(N) = sum_d max(0,-U_d(N))
```

where the sum defining `T_N` is over strict-central prime pairs
`N/3 < p < 2N/3`, and `d` runs over `70`, `130`, `154`, and `286`.

The sufficient theorem target is:

```text
A_raw_-(N) < L_raw(N)
```

for every sufficiently large covered even `N`, followed by finite remainder
verification below the threshold.

## Zero-Support Boundary

If strict-central support is empty, then `T_N=0`.  Consequently
`L_raw(N)=0`, every `U_d(N)=0`, and `A_raw_-(N)=0`.  The strict inequality
cannot hold.  Therefore a proved theorem of this form would force
strict-central support without first normalizing by the actual measure `mu_N`.

## Receipt

```text
tools/build_q286_wbss_raw_adverse_drag_theorem_target.py
evidence/q286-wbss-raw-adverse-drag-theorem-target.json
```

## Finite Calibration

```text
checked rows:                              348
target range:                  1036248..1155862
positive total-weight rows:                348
zero total-weight rows:                      0
raw adverse below raw local rows:          348 / 348
raw adverse not below raw local rows:        0
positive raw gate-gap rows:                348 / 348
```

Stress rows:

```text
largest raw adverse ratio target:        1124642
largest raw adverse ratio:     0.23148438379145228
tightest raw gate-gap target:            1059514
tightest raw gate gap:         286929.1729900494
minimum raw local-main target:           1038176
minimum raw local main:        323194.9984858959
```

## Decision

`TARGET_raw_q286_WBSS_adverse_drag_theorem`.

The route now has a non-circular raw sufficient inequality:

```text
A_raw_-(N) < L_raw(N).
```

The checked rows satisfy it, but finite rows are calibration and falsifier
evidence only.  A Goldbach-yielding bridge still needs a universal pointwise
raw adverse-drag theorem, or another direct raw lower bound for `W_phi(N)>0`.

No raw adverse-drag theorem, raw witness theorem, positive-mass theorem, q286
threshold theorem, strict-central Goldbach theorem, or Goldbach proof is
established.

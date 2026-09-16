# Mobius moment-square degree-5 moving-prime band audit

## Question

After fixed-prime stress is obstructed, where do the moving source-start
prime-block stresses sit in the normalized coordinate `sigma=p/M`?  Can the
endpoint bands be treated as irrelevant?

## Mechanism

Read the seven complete source-start sweeps:

```text
M=229, 251, 293, 331, 353, 379, 383
```

For every prime block `p in [M,2M]`, compute `sigma=p/M` and group it into:

```text
sigma_1_00_1_25:  1.00 <= sigma < 1.25
sigma_1_25_1_50:  1.25 <= sigma < 1.50
sigma_1_50_1_75:  1.50 <= sigma < 1.75
sigma_1_75_2_00:  1.75 <= sigma <= 2.00
```

Then take the minimum signed dominance slack by band, both at block level and
row level.

## Receipt

```text
tools/build_mobius_moment_square_degree5_moving_prime_band_audit.py
evidence/mobius-moment-square-degree5-moving-prime-band-audit.json
```

## Result

```text
prime blocks: 357
dominance rows: 1428
all bands positive: true

sigma_1_00_1_25: blocks 97, rows 388, min slack 0.4168496626998832 at M=229, p=283
sigma_1_25_1_50: blocks 83, rows 332, min slack 0.426291195360443  at M=331, p=479
sigma_1_50_1_75: blocks 93, rows 372, min slack 0.40189096624031384 at M=229, p=379
sigma_1_75_2_00: blocks 84, rows 336, min slack 0.40479256047704726 at M=331, p=599
```

The global weakest block is still:

```text
M=229, p=379, sigma=1.6550218340611353, label (00,12), slack 0.40189096624031384
```

But the endpoint bands are not so loose that they can be ignored.  The high
endpoint band minimum `0.40479256047704726` is close to the global minimum.

## Decision

The seven-sweep fixture does not support a fixed-prime theorem target or an
endpoint-only simplification.  The next analytic target should be
sigma-banded moving prime-block lower-frame control across the full interval
`sigma in [1,2]`.

This is finite band evidence only.  It proves no sigma-band theorem,
moving-prime theorem, prime-block theorem, source-start theorem, strict-central
Goldbach theorem, or Goldbach proof.

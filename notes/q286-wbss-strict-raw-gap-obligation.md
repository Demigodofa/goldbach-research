# q286-WBSS strict raw-gap obligation

## Question

After rawizing the q286-WBSS adverse-drag target, what exact theorem obligation
still carries the proof bridge?  Is a homogeneous ratio bound enough, or do we
need a strict positive raw gap?

## Mechanism

Define

```text
G_raw(N) = L_raw(N) - A_raw_-(N).
```

The strict raw adverse-drag target is exactly

```text
G_raw(N) > 0.
```

A homogeneous estimate such as

```text
A_raw_-(N) <= rho * L_raw(N), rho < 1
```

is not by itself a Goldbach bridge.  If strict-central support is empty, then
`T_N=0`, `L_raw(N)=0`, and `A_raw_-(N)=0`; the homogeneous estimate is still
true.  It only gives `G_raw(N)>=0`, not a witness.

Thus a proof route must either:

```text
prove G_raw(N)>0 directly,
```

or prove a ratio estimate together with an independent positive raw-local-main
or positive-mass theorem.

## Receipt

```text
tools/build_q286_wbss_strict_raw_gap_obligation.py
evidence/q286-wbss-strict-raw-gap-obligation.json
```

## Finite Calibration

```text
checked rows:                        348
positive strict raw-gap rows:        348 / 348
nonpositive strict raw-gap rows:       0
tightest strict raw-gap target:  1059514
tightest strict raw gap:        286929.1729900494
smallest G_raw/N target:        1141274
smallest G_raw/N:               0.26310340793692394
smallest G_raw/T_N target:      1141274
smallest G_raw/T_N:             0.5992601478393073
```

These scale constants are fitted to the checked rows.  They are not universal
bounds.

## Decision

`TARGET_strict_raw_q286_WBSS_gap_lower_bound`.

The next theorem obligation is strict raw gap, not homogeneous raw adverse-ratio
control alone.  A direct theorem

```text
G_raw(N) >= eta(N) > 0
```

for every sufficiently large covered even `N`, followed by finite remainder
verification, would imply `W_phi(N)>0` and force strict-central support.

No strict raw-gap theorem, raw adverse-drag theorem, positive-mass theorem, q286
threshold theorem, strict-central Goldbach theorem, or Goldbach proof is
established.

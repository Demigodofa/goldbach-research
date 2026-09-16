# q286-WBSS K286 zero-residue raw-horizon probe

## Question

After finding that `N == 0 mod 286` was absent from the raw finite calibration,
does a targeted near-horizon zero-residue probe immediately falsify the raw
adverse-drag route?

## Mechanism

The coverage audit identified `N == 0 mod 286` as the unique `K_286`
two-mode no-reflection-discount residue.  This probe takes all `35` period
residues modulo `10010` that lie over `0 mod 286`:

```text
0, 286, 572, ..., 9724
```

and evaluates the first `2` lifts of each residue after the existing raw
adverse-drag horizon maximum.

## Receipt

```text
tools/build_q286_wbss_k286_zero_residue_raw_horizon_probe.py
evidence/q286-wbss-k286-zero-residue-raw-horizon-probe.json
```

## Result

```text
target_mod_286:                         0
period residues checked:               35
lifts per period residue:               2
finite probe rows:                     70
target range:             1156012..1175746
zero pair-count rows:                   0
zero total-weight rows:                 0
positive raw witness rows:             70 / 70
positive raw adverse-gap rows:         70 / 70
raw adverse below raw local rows:      70 / 70
raw adverse not below raw local rows:   0 / 70
largest raw adverse ratio:              0.22064948972651888
tightest raw adverse gap:          423543.19091507455
smallest gap / N:                       0.3646688618455568
```

Tight rows:

```text
tightest raw gap target:      1161446
tightest raw gap residue:         286 mod 10010
tightest raw gap pair count:     3640

largest raw ratio target:     1158872
largest raw ratio residue:       7722 mod 10010
largest raw ratio pair count:    3522
```

Comparison to prior raw calibration:

```text
prior largest raw adverse ratio:  0.23148438379145228
probe largest raw adverse ratio:  0.22064948972651888

prior tightest raw gap:      286929.1729900494
probe tightest raw gap:      423543.19091507455
```

## Decision

`PROBE_zero_residue_raw_horizon_survives_finite_check_not_proof`.

The targeted zero-residue finite probe survives.  No checked row has zero
mass, nonpositive raw witness, or `A_raw_-(N) >= L_raw(N)`.

This removes the immediate finite falsifier for the previously unsampled
no-discount lane, but it does not promote finite evidence into proof.  The
necessary theorem lane remains:

```text
For every sufficiently large covered even N with N == 0 mod 286,
prove A_raw_-(N) < L_raw(N),
```

or prove an equivalent raw witness lower bound.

No zero-residue raw adverse-drag theorem, universal pointwise raw estimate,
binary-prime moment theorem, q286 threshold theorem, strict-central Goldbach
theorem, or Goldbach proof is established.

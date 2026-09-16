# q286-WBSS K286 zero-residue absolute-envelope payment probe

## Question

Does the `K_286` absolute-envelope payment diagnostic survive all `35`
zero-residue period classes for the first two lifts after the raw adverse-drag
horizon?

## Mechanism

For each checked row, compute

```text
M(N)       = local main
H_286(N)   = sum of absolute real K_286 conjugate phase-pair contributions
A_other(N) = adverse drag from moduli 70, 130, and 154 only
```

Then test the finite payment margin

```text
M(N) - A_other(N) - H_286(N) > 0.
```

This is the same payment as the `32`-row extended-lift audit, widened to the
`70` near-horizon rows from all `35` period residues with `N == 0 mod 286`.

## Receipt

```text
tools/build_q286_wbss_k286_zero_residue_absolute_envelope_payment_probe.py
evidence/q286-wbss-k286-zero-residue-absolute-envelope-payment-probe.json
```

## Result

```text
zero-residue period classes:          35
lifts per period class:                2
probe rows:                           70
target range:                1156012..1175746
payment-positive rows:                70 / 70
payment-nonpositive rows:              0 / 70

absolute payment ratio: min 0.1391434905460112
absolute payment ratio: mean 0.32253127748212546
absolute payment ratio: max 0.6081499594276282

payment margin:         min 0.2797816892333873
payment margin:        mean 0.6841891086572599
payment margin:         max 1.0643924645355805

K286 envelope:          min 0.14007084949178422
K286 envelope:         mean 0.29575063273564195
K286 envelope:          max 0.44805263755269226

required K286 cap:      min 1.7073955330000075
required K286 cap:     mean 3.548773669530584
required K286 cap:      max 7.688686822924483
```

The tightest row is target `1170884`, residue `9724`, period-residue index
`34`, lift `1`:

```text
local main:                 0.7140019401930207
other-moduli adverse drag:  0.03871070052911857
K286 absolute envelope:     0.3955095504305148
absolute payment:           0.43422025095963335
payment margin:             0.2797816892333873
payment ratio:              0.6081499594276282
```

## Decision

`PROBE_k286_zero_residue_absolute_envelope_payment_survives`.

The absolute-envelope payment route survives a wider `70`-row finite probe
over all zero-residue period classes near the raw horizon.  This strengthens
the theorem-shaped direction toward a `K_286` absolute-envelope bound plus
companion one-sided bounds for the other moduli.  It also suggests that the
next finite stress should extend lift depth, not merely add near-horizon
period residues.

This is finite probe evidence only.  It proves no `K_286`
absolute-envelope theorem, no companion adverse-drag theorem, no
phase-cancellation theorem, no universal pointwise raw bound, no q286
threshold theorem, no strict-central Goldbach theorem, and no Goldbach proof.

# q286-WBSS K286 absolute-envelope payment audit

## Question

The `K_286` phase envelope is broad, so a tiny phase-label shortcut is not the
right theorem object.  On the extended zero-lane rows, can the local main pay
the entire `K_286` absolute phase envelope plus the actually adverse drag from
the other three projected moduli?

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

This pays the whole absolute `K_286` envelope.  It deliberately does not use
signed cancellation inside the `K_286` phase sum.

## Receipt

```text
tools/build_q286_wbss_k286_absolute_envelope_payment_audit.py
evidence/q286-wbss-k286-absolute-envelope-payment-audit.json
```

## Result

```text
extended rows:                            32
target range:                   1158872..1235806
payment-positive rows:                   32 / 32
payment-nonpositive rows:                 0 / 32

absolute payment ratio: min 0.23855937004298816
absolute payment ratio: mean 0.41306853497816054
absolute payment ratio: max 0.7926876143614664

payment margin:         min 0.1480214455719575
payment margin:        mean 0.49468209609724717
payment margin:         max 0.6694413649537231

K286 envelope:          min 0.20065300258921384
K286 envelope:         mean 0.32482274937825234
K286 envelope:          max 0.5179580723281451

required K286 cap:      min 1.2857788177846576
required K286 cap:     mean 2.636017528088691
required K286 cap:      max 4.336313717289516
```

The tightest row is target `1201486`, residue `286`, lift `4`:

```text
local main:                 0.7140019401930244
other-moduli adverse drag:  0.048022422292921904
K286 absolute envelope:     0.5179580723281451
absolute payment:           0.5659804946210669
payment margin:             0.1480214455719575
payment ratio:              0.7926876143614664
```

## Decision

`DIAGNOSTIC_k286_absolute_envelope_payment_survives`.

On the finite extended zero-lane rows, local main pays the entire `K_286`
absolute phase envelope plus actual adverse drag from the other projected
moduli.  This demotes delicate `K_286` signed cancellation as the immediate
sublane target.  The sharper theorem-shaped target is now an absolute
`K_286` envelope bound plus companion one-sided bounds for the other moduli,
with total below local main.

This is finite diagnostic evidence only.  It proves no `K_286`
absolute-envelope theorem, no companion adverse-drag theorem, no
phase-cancellation theorem, no universal pointwise raw bound, no q286
threshold theorem, no strict-central Goldbach theorem, and no Goldbach proof.

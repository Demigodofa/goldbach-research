# q286-WBSS K286 zero-residue absolute-envelope lift-depth probe

## Question

Does the `K_286` absolute-envelope payment diagnostic survive all `35`
zero-residue period classes through `8` lifts after the raw adverse-drag
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

This is the same payment as the previous probes, widened to all `35`
zero-residue period classes and deepened to `8` lifts each.

## Receipt

```text
tools/build_q286_wbss_k286_zero_residue_absolute_envelope_lift_depth_probe.py
evidence/q286-wbss-k286-zero-residue-absolute-envelope-lift-depth-probe.json
```

## Result

```text
zero-residue period classes:          35
lifts per period class:                8
probe rows:                          280
target range:                1156012..1235806
payment-positive rows:               280 / 280
payment-nonpositive rows:              0 / 280

absolute payment ratio: min 0.1387055806478266
absolute payment ratio: mean 0.32839648981729497
absolute payment ratio: max 0.7926876143614664

payment margin:         min 0.1480214455719575
payment margin:        mean 0.6780208445210824
payment margin:         max 1.0951587951686008

K286 envelope:          min 0.14007084949178422
K286 envelope:         mean 0.3015570812320769
K286 envelope:          max 0.5179580723281451

required K286 cap:      min 1.2857788177846576
required K286 cap:     mean 3.446371907120119
required K286 cap:      max 7.688686822924483
```

The tightest payment row is target `1201486`, residue `286`,
period-residue index `1`, lift `4`:

```text
local main:                 0.7140019401930244
other-moduli adverse drag:  0.048022422292921904
K286 absolute envelope:     0.5179580723281451
absolute payment:           0.5659804946210669
payment margin:             0.1480214455719575
payment ratio:              0.7926876143614664
```

The largest observed signed-adverse fraction of the `K_286` envelope is not
the tight payment row.  It occurs at target `1198626`, residue `7436`, lift
`4`, where the signed adverse fraction is `0.6863544499659987` but the
absolute payment margin is still `0.7439341864038584`.

## Decision

`PROBE_k286_zero_residue_absolute_envelope_payment_survives_lift_depth`.

The absolute-envelope payment route survives a `280`-row finite lift-depth
probe over all zero-residue period classes.  This strengthens the
theorem-shaped direction and keeps the next useful stress on either deeper
lift behavior or separating `H_286(N)` and `A_other(N)` into analytic theorem
targets.

This is finite probe evidence only.  It proves no `K_286`
absolute-envelope theorem, no companion adverse-drag theorem, no
phase-cancellation theorem, no universal pointwise raw bound, no q286
threshold theorem, no strict-central Goldbach theorem, and no Goldbach proof.

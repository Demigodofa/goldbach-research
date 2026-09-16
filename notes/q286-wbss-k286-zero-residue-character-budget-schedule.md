# q286-WBSS K286 zero-residue character-budget schedule

## Question

After crude residue-`L1` failed to explain the `K_286` zero lane, what active
character-moment payments would be sufficient on `N == 0 mod 286`?

## Mechanism

Reuse the exact zero-lane local-main schedule and pay it in active
multiplicative-character coordinates:

```text
character Linf cap for a = local_main(a) / total_character_L1
aggregate character L2 cap for a = local_main(a) / aggregate_character_L2
```

These are sufficient theorem-payment caps.  They do not prove any character
moment estimate.

## Receipt

```text
tools/build_q286_wbss_k286_zero_residue_character_budget_schedule.py
evidence/q286-wbss-k286-zero-residue-character-budget-schedule.json
```

## Result

Global active-character package:

```text
active complex characters:         122
active real channels:               64
total character L1:                 49.153988812629684
aggregate character L2:              5.525106448699807
global character Linf cap:           0.012286599575574883
global aggregate L2 cap:             0.10930746469603118
```

Zero-lane schedule:

```text
period residues checked:            35
character Linf cap range:            0.014525818909930746
                                  .. 0.025868228930402082
aggregate character L2 cap range:    0.12922863058340583
                                  .. 0.2301361335303773
tightest zero-lane residue:          9724 mod 10010
loosest zero-lane residue:           1716 mod 10010
tightest/global cap factor:          1.1822489062642942
aggregate L2 / residue L1 factor:   67.50313420004822
```

## Decision

`TARGET_zero_residue_character_moment_budget_schedule_unproved`.

The zero-lane active-character payment schedule is now pinned.  Like the
residue-`L1` schedule, it shows the `K_286` no-reflection lane is not worse
than the global all-residue coefficient payment.

Therefore the live obstruction is not coefficient-norm size alone.  The proof
pressure now belongs on a pointwise raw signed/character binary-prime estimate,
or a direct raw witness theorem, not more coefficient-size accounting.

No zero-residue raw adverse-drag theorem, aggregate character-moment theorem,
universal pointwise raw estimate, binary-prime moment theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof is established.

# q286-WBSS K286 zero-residue raw-budget schedule

## Question

For the necessary `N == 0 mod 286` lane, what exact uniform
residue-discrepancy payment would be sufficient for the raw adverse-drag
theorem?

## Mechanism

For each of the `35` period residues modulo `10010` above `0 mod 286`, compute

```text
eta_a = local_main(a) / sum_d ||c_d||_1.
```

If every projected residue discrepancy in the four-modulus package is bounded
by `eta_a` for that period class, then the crude residue-`L1` payment gives

```text
A_raw_-(N) < L_raw(N)
```

after raw scaling by `T_N`.

This is a sufficient theorem-payment schedule.  It is not necessary, and it is
not finite acceptance.

## Receipt

```text
tools/build_q286_wbss_k286_zero_residue_raw_budget_schedule.py
evidence/q286-wbss-k286-zero-residue-raw-budget-schedule.json
```

## Result

```text
period residues checked:            35
total coefficient L1:                372.962002076135
global all-residue cap:              0.0016192946592982506

zero-lane local-main minimum:        0.7140019401930207
zero-lane local-main mean:           0.9999999999999963
zero-lane local-main maximum:        1.2715266354475274

zero-lane cap minimum:               0.0019144093398749697
zero-lane cap mean:                  0.002681238288172478
zero-lane cap maximum:               0.0034092658993930512

tightest zero-lane residue:          9724 mod 10010
loosest zero-lane residue:           1716 mod 10010
tightest/global cap factor:          1.1822489062642942
```

The global all-residue worst local-main row is not in the zero lane.  Under the
crude residue-`L1` sufficient condition, the zero lane is looser than the
global all-residue budget.

## Decision

`TARGET_zero_residue_raw_discrepancy_budget_schedule_unproved`.

The exact zero-residue `L1` payment schedule is now pinned.  It does not prove
any prime-pair discrepancy theorem, but it shows that the `K_286`
no-reflection-discount lane is not worse than the global all-residue cap under
the crude residue-`L1` sufficient condition.

Therefore the `K_286` no-reflection-discount difficulty is not captured by
plain total-`L1` size.  A proof still needs sharper signed/character moment
control or a direct raw witness estimate for the zero lane.

No zero-residue raw adverse-drag theorem, universal pointwise raw estimate,
binary-prime moment theorem, q286 threshold theorem, strict-central Goldbach
theorem, or Goldbach proof is established.

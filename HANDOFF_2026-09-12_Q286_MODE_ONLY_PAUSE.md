# Handoff: q286 Mode-Only Tail Recurrence Scan

Date: 2026-09-12.

Owner: Kevin. Lead agent: Rill (`agent.rill`).

Status: paused cleanly at Kevin's request.  Goldbach is not proved.  RH is not
proved.  No prize-level or eventual theorem claim is established.

## Current Repo State

Before this handoff commit, `main` was aligned with `origin/main` at:

```text
fb60fb2 Record q286 far-band floor candidate probe
```

All active scan worker processes were interrupted and stopped before writing
this handoff.  No background scan session is intentionally left running.

## Current Code Change

`q286_first_three_tail_mode_only_horizon_receipt` was added to
`lcm_sawtooth_goldbach_transfer.py`.

Purpose: scan the q286 first-three tail threshold without recomputing the full
action or complement-rescue data.  It measures only first-three mode sums and
tail counts.  It explicitly does not measure complement rescue or full action
negativity.

Test added:

```text
test_q286_first_three_tail_mode_only_horizon
```

The test compares the new mode-only receipt against the older
`q286_first_three_tail_threshold_horizon_receipt` on a five-target window.

## Validation Already Run

Focused unittest passed:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -m unittest test_lcm_sawtooth_goldbach_transfer.EvenEvenGoldbachTransferTests.test_q286_first_three_tail_mode_only_horizon -v
```

Result:

```text
Ran 1 test in 158.092s
OK
```

No-bytecode compile passed:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
python -B -m py_compile lcm_sawtooth_goldbach_transfer.py test_lcm_sawtooth_goldbach_transfer.py
```

A prior compile attempt without `-B` hit a Windows `__pycache__` rename race:

```text
[WinError 5] Access is denied: '__pycache__\test_lcm_sawtooth_goldbach_transfer.cpython-311.pyc...'
```

Treat that as an environment/bytecode-write issue, not a known syntax failure.

## Partial Gap-Scan Evidence Collected

These cycle rows were collected before the clean pause:

```text
cycle 65: tail 0, min_first_three -0.297132521004334, min_target 661874
cycle 66: tail 0, min_first_three -0.2556952763516359, min_target 677366
cycle 67: tail 0, min_first_three -0.27878022793784435, min_target 683042
cycle 68: tail 0, min_first_three -0.2606186682723109, min_target 698212
cycle 69: tail 0, min_first_three -0.2497797437822001, min_target 707656
cycle 70: tail 0, min_first_three -0.28512129966814553, min_target 710926
cycle 71: tail 0, min_first_three -0.28681340018305573, min_target 727226
cycle 72: tail 1, min_first_three -0.3215492897967754, min_target 733126
cycle 73: tail 1, min_first_three -0.3183278779198759, min_target 741976
cycle 77: tail 1, min_first_three -0.3351606547038982, min_target 782336
cycle 78: tail 0, min_first_three -0.23784785071411937, min_target 796736
cycle 79: tail 1, min_first_three -0.32984168711159817, min_target 805682
cycle 80: tail 1, min_first_three -0.30973201334501105, min_target 818528
cycle 85: tail 0, min_first_three -0.2731567957103434, min_target 865742
cycle 86: tail 0, min_first_three -0.2972215111537993, min_target 875822
cycle 87: tail 0, min_first_three -0.25212698808500167, min_target 883592
cycle 88: tail 0, min_first_three -0.2890465352245365, min_target 895772
cycle 93: tail 0, min_first_three -0.2286634516120356, min_target 941836
cycle 94: tail 1, min_first_three -0.34548559053695327, min_target 955832
cycle 95: tail 0, min_first_three -0.22671539911332203, min_target 963868
cycle 96: tail 0, min_first_three -0.26272566581700657, min_target 971590
```

Missing cycles from the gap scan:

```text
74, 75, 76, 81, 82, 83, 84, 89, 90, 91, 92
```

Cycles `97..104` were already checked by the floor-candidate receipt and had
zero `.3` first-three tail targets.

## Interpretation Boundary

The sparse hits at cycles `72`, `73`, `77`, `79`, `80`, and `94` falsify the
too-strong interpretation that the `.3` first-three tail permanently
disappears after cycle `64`.

The better next question is whether these sparse recurrences are rescued by
the complement and whether they satisfy the `.63/.3/.47` floor candidate.

This remains finite evidence only.

## Resume Instructions

Start here:

```powershell
cd C:\Users\benja\source\repos\Demigodofa\goldbach-research
git status --short --branch
$env:PYTHONDONTWRITEBYTECODE='1'
python -B -m py_compile lcm_sawtooth_goldbach_transfer.py test_lcm_sawtooth_goldbach_transfer.py
python -m unittest test_lcm_sawtooth_goldbach_transfer.EvenEvenGoldbachTransferTests.test_q286_first_three_tail_mode_only_horizon -v
```

Complete the missing mode-only gap cycles:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; @'
from lcm_sawtooth_goldbach_transfer import q286_first_three_tail_mode_only_horizon_receipt as f
period = 10010
for global_cycle in (74, 75, 76, 81, 82, 83, 84, 89, 90, 91, 92):
    start = 10000 + global_cycle * period
    print('begin', global_cycle, start, flush=True)
    r = f(start=start, cycle_count=1, targets_per_cycle=5005,
          negative_tail_thresholds=(.3,), tolerance=1e-9)
    row = r['cycle_rows'][0]
    print('cycle', global_cycle,
          'tail', row['threshold_counts'][.3],
          'min_first_three', row['minimum_first_three_to_principal_ratio'],
          'min_target', row['minimum_first_three_target'],
          flush=True)
'@ | python -
```

Stress-test recurrence cycles with the floor candidate:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'; @'
from lcm_sawtooth_goldbach_transfer import q286_first_three_tail_rescue_floor_candidate_receipt as f
period = 10010
for global_cycle in (72, 73, 77, 79, 80, 94):
    start = 10000 + global_cycle * period
    print('begin', global_cycle, start, flush=True)
    r = f(start=start, cycle_count=1, targets_per_cycle=5005,
          threshold=.3, complement_floor=.63,
          rescue_margin_floor=.3, deficit_ceiling=.47)
    row = r['cycle_rows'][0]
    print('cycle', global_cycle,
          'tail', r['tail_target_count'],
          'nonrescued', r['nonrescued_tail_target_count'],
          'passed', r['candidate_floor_passed'],
          'min_comp', row['minimum_complement_to_principal_ratio'],
          'min_margin', row['minimum_rescue_margin_to_principal_ratio'],
          'max_deficit', row['maximum_deficit_to_principal_ratio'],
          'violations', r['violating_targets'],
          flush=True)
'@ | python -
```

After recording results:

```powershell
git diff --check
git status --short --branch
git add .
git commit -m "<concise q286 checkpoint message>"
git push
```

Do not claim Goldbach, RH, an eventual theorem, or a prize-level result from
these finite diagnostics.

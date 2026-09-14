"""Build a q286 rank-1 outside-remainder residual-drag ledger.

The Octave rank-1 audit leaves a precise finite theorem target: positive
rank-1 outside direction plus a bound on negative residual row-sum drag.
This derived receipt tests simple drag caps on the checked 71 clear rows.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RANK1_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-octave-rank1-audit.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-ledger.json")
CAPS = (0.25, 0.5, 0.7, 0.75, 1.0)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set)):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def summarize(values):
    values = tuple(float(value) for value in values)
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def cap_record(rows, cap):
    failures = tuple(
        row for row in rows if row["residual_drag_to_rank1_ratio"] > cap)
    return {
        "cap": cap,
        "passes": len(failures) == 0,
        "failing_count": len(failures),
        "failing_targets": tuple(row["target"] for row in failures),
        "maximum_excess": max(
            (row["residual_drag_to_rank1_ratio"] - cap for row in failures),
            default=0.0),
    }


def main():
    rank1_payload = json.loads(RANK1_SOURCE.read_text(encoding="utf-8"))
    rows = []
    for source in rank1_payload["rows_by_full_outside_delta"]:
        target = int(source["target"])
        rank1 = float(source["rank1_reconstructed_outside_delta"])
        residual = float(source["residual_after_rank1_row_sum"])
        full = float(source["full_outside_delta_to_stress"])
        if rank1 <= 0:
            raise AssertionError(f"rank-1 margin not positive for {target}")
        if abs((rank1 + residual) - full) > 1e-10:
            raise AssertionError(
                f"rank1 + residual identity drifted for {target}")
        drag = max(0.0, -residual)
        rows.append({
            "target": target,
            "window_start": int(source["window_start"]),
            "window_role": source["window_role"],
            "target_mod_286": int(source["target_mod_286"]),
            "target_mod_10010": int(source["target_mod_10010"]),
            "full_outside_delta_to_stress": full,
            "rank1_reconstructed_outside_delta": rank1,
            "residual_after_rank1_row_sum": residual,
            "residual_drag": drag,
            "residual_drag_to_rank1_ratio": drag / rank1,
            "full_delta_to_rank1_ratio": full / rank1,
        })

    rows_by_drag_ratio = tuple(sorted(
        rows,
        key=lambda row: (
            row["residual_drag_to_rank1_ratio"],
            row["residual_drag"],
            -row["target"]),
        reverse=True))
    worst = rows_by_drag_ratio[0]
    if worst["target"] != 1242118:
        raise AssertionError("worst residual-drag target drifted")
    max_ratio = worst["residual_drag_to_rank1_ratio"]
    if not (0.7 < max_ratio < 0.75):
        raise AssertionError("max residual-drag ratio left expected bracket")

    cap_records = tuple(cap_record(rows_by_drag_ratio, cap) for cap in CAPS)
    by_cap = {record["cap"]: record for record in cap_records}
    if by_cap[0.75]["failing_count"] != 0:
        raise AssertionError("three-quarter residual-drag cap failed")
    if by_cap[0.7]["failing_targets"] != (1242118,):
        raise AssertionError("0.7 residual-drag cap failures drifted")
    if by_cap[0.5]["failing_targets"] != (1242118, 1222048):
        raise AssertionError("half residual-drag cap failures drifted")
    if by_cap[0.25]["failing_targets"] != (1242118, 1222048, 1220056):
        raise AssertionError("quarter residual-drag cap failures drifted")

    negative_residual_rows = tuple(
        row for row in rows if row["residual_after_rank1_row_sum"] < 0)
    nonnegative_residual_rows = tuple(
        row for row in rows if row["residual_after_rank1_row_sum"] >= 0)
    if len(negative_residual_rows) != 36:
        raise AssertionError("negative residual row count drifted")
    if len(nonnegative_residual_rows) != 35:
        raise AssertionError("nonnegative residual row count drifted")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_outside_plane_remainder_octave_rank1_audit": str(
            RANK1_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite rank-1 residual-drag ledger only; the checked 3/4 cap "
            "and lower-cap falsifiers are not residual-bound theorems, "
            "signed projection theorems, or a Goldbach proof"),
        "candidate": (
            "The negative residual row-sum after the positive rank-1 outside "
            "direction might be uniformly bounded by a fixed fraction of the "
            "rank-1 reconstructed outside margin on the checked denominator."),
        "mechanism": (
            "Use the Octave rank-1 receipt's identity full_delta = rank1 + "
            "residual.  Measure residual drag as max(0, -residual) and test "
            "simple caps drag <= c * rank1 for fixed c."),
        "prediction": (
            "If the surviving finite route is a positive rank-1 direction "
            "plus residual-drag control, then at least one nontrivial fixed "
            "cap below 1 should survive, while overly strong caps may fail on "
            "the closest clear rows."),
        "falsifier": (
            "A checked row with residual drag greater than 0.75 times its "
            "rank-1 reconstructed outside delta would falsify the finite "
            "three-quarter cap.  The half-drag and 0.7 caps are already "
            "falsified on this denominator."),
        "novelty_label": "new-to-this-task",
        "stress_target": rank1_payload["stress_target"],
        "clear_count": rank1_payload["clear_count"],
        "rank1_energy_fraction": rank1_payload["rank1_energy_fraction"],
        "negative_residual_row_count": len(negative_residual_rows),
        "nonnegative_residual_row_count": len(nonnegative_residual_rows),
        "maximum_residual_drag_to_rank1_ratio": max_ratio,
        "worst_residual_drag_row": worst,
        "cap_records": cap_records,
        "residual_drag_summary": summarize(
            row["residual_drag"] for row in rows),
        "residual_drag_to_rank1_ratio_summary": summarize(
            row["residual_drag_to_rank1_ratio"] for row in rows),
        "full_delta_to_rank1_ratio_summary": summarize(
            row["full_delta_to_rank1_ratio"] for row in rows),
        "rows_by_residual_drag_ratio": rows_by_drag_ratio,
        "summary": {
            "three_quarter_cap": (
                "On the checked 71 clear rows, residual drag is always below "
                "0.75 times the rank-1 reconstructed outside delta."),
            "worst_row": (
                "The sharp row is 1242118, with drag/rank1 about "
                "0.7421344693; the 3/4 cap is close, not comfortable."),
            "lower_caps_fail": (
                "The 0.7 cap fails at 1242118, the half-drag cap fails at "
                "1242118 and 1222048, and the quarter cap also fails at "
                "1220056."),
            "theorem_shape": (
                "The live theorem target is a positive arithmetic rank-1 "
                "outside direction plus a residual-drag inequality; the "
                "tested finite 3/4 cap is only a candidate shape."),
        },
        "interpretation": {
            "hole_status": (
                "The loop tightened into a near-sharp finite inequality: "
                "rank-1 positivity survives, and the remaining negative "
                "residual drag stays below three quarters of that margin on "
                "the checked denominator."),
            "route_status": (
                "Do not promote the 3/4 constant to a theorem without a "
                "non-post-hoc arithmetic proof and an external stress test; "
                "the lower-cap failures mark how tight the bound is."),
        },
        "rank1_residual_drag_ledger_measured": True,
        "three_quarter_residual_drag_cap_holds_on_checked_rows": True,
        "half_residual_drag_cap_refuted_on_checked_rows": True,
        "seven_tenths_residual_drag_cap_refuted_on_checked_rows": True,
        "rank1_residual_bound_theorem_proved": False,
        "outside_remainder_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }

    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

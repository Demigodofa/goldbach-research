"""Diagnose the q286 strict-closure stress split as a coupled slack budget.

The post-discovery stress receipt falsified the selected-late endpoint as a
universal active-lane certificate.  This derived receipt asks what failed: an
independent driver floor, an independent channel bound, or the coupled tradeoff

    driver_margin + L * channel_margin > 0.

Finite diagnostic only.  It proves no strict-closure theorem, pointwise
adverse-drag theorem, q286 threshold theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = (
    EVIDENCE / "q286-active-lane-strict-closure-post-discovery-stress.json")
OUT = (
    EVIDENCE
    / "q286-active-lane-strict-closure-coupled-slack-diagnosis.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def finite_summary(values):
    vals = [float(value) for value in values]
    if not vals:
        return {"count": 0, "minimum": None, "mean": None, "maximum": None}
    return {
        "count": len(vals),
        "minimum": min(vals),
        "mean": sum(vals) / len(vals),
        "maximum": max(vals),
    }


def diagnose_row(row, channel_l1):
    driver_margin = float(row["driver_margin_to_calibrated_floor"])
    channel_margin = float(row["channel_margin_to_calibrated_linf_bound"])
    channel_contribution = float(
        row["channel_margin_contribution_to_strict_closure"])
    strict_margin = float(row[
        "strict_closure_margin_to_calibrated_endpoint"])
    driver_deficit = max(0.0, -driver_margin)
    channel_payment_ratio = (
        channel_contribution / driver_deficit
        if driver_deficit > 0.0 else None)
    required_channel_margin_to_pay_driver = (
        driver_deficit / channel_l1 if channel_l1 else None)
    return {
        "target": int(row["target"]),
        "block_index_after_discovery": int(
            row["block_index_after_discovery"]),
        "target_mod_286": int(row["source_target_mod_286"]),
        "target_mod_143": int(row["source_target_mod_143"]),
        "driver_margin": driver_margin,
        "driver_floor_condition_met": driver_margin >= 0.0,
        "driver_deficit_to_calibrated_floor": driver_deficit,
        "channel_margin": channel_margin,
        "channel_linf_condition_met": channel_margin >= 0.0,
        "channel_contribution": channel_contribution,
        "required_channel_margin_to_pay_driver": (
            required_channel_margin_to_pay_driver),
        "channel_margin_surplus_after_driver_deficit": (
            channel_margin - required_channel_margin_to_pay_driver
            if required_channel_margin_to_pay_driver is not None else None),
        "channel_payment_ratio_to_driver_deficit": channel_payment_ratio,
        "strict_closure_margin": strict_margin,
        "coupled_slack_positive": strict_margin > 0.0,
        "additional_channel_contribution_needed": max(0.0, -strict_margin),
        "additional_normalized_channel_margin_needed": (
            max(0.0, -strict_margin) / channel_l1 if channel_l1 else None),
        "full_action_to_principal_ratio": float(
            row["full_action_to_principal_ratio"]),
    }


def build_receipt():
    source = load_json(SOURCE)
    channel_l1 = float(source["calibrated_real_channel_l1_to_principal_mean"])
    rows = [
        diagnose_row(row, channel_l1)
        for row in sorted(
            source["target_rows"].values(),
            key=lambda item: item["block_index_after_discovery"])
    ]
    driver_pass = [row for row in rows if row["driver_floor_condition_met"]]
    channel_pass = [row for row in rows if row["channel_linf_condition_met"]]
    coupled_pass = [row for row in rows if row["coupled_slack_positive"]]
    channel_pass_coupled_fail = [
        row for row in rows
        if row["channel_linf_condition_met"]
        and not row["coupled_slack_positive"]]
    payment_ratios = [
        row["channel_payment_ratio_to_driver_deficit"]
        for row in rows
        if row["channel_payment_ratio_to_driver_deficit"] is not None]
    return {
        "schema_version": 1,
        "receipt": (
            "q286-active-lane-strict-closure-coupled-slack-diagnosis"),
        "generated_from_commit": source_commit(),
        "sources": {
            "post_discovery_stress": str(SOURCE.relative_to(ROOT)),
            "post_discovery_stress_commit": source[
                "generated_from_commit"],
        },
        "calibrated_constants": {
            "driver_floor": source[
                "calibrated_combined_floor_driver_floor"],
            "normalized_real_channel_linf_bound": source[
                "calibrated_normalized_real_channel_linf_bound"],
            "real_channel_l1_to_principal_mean": channel_l1,
        },
        "row_count": len(rows),
        "driver_floor_condition_met_count": len(driver_pass),
        "channel_linf_condition_met_count": len(channel_pass),
        "coupled_slack_positive_count": len(coupled_pass),
        "coupled_slack_nonpositive_count": len(rows) - len(coupled_pass),
        "both_independent_conditions_met_count": sum(
            1 for row in rows
            if row["driver_floor_condition_met"]
            and row["channel_linf_condition_met"]),
        "channel_pass_but_coupled_fail_count": len(
            channel_pass_coupled_fail),
        "driver_floor_fails_on_every_stress_row": not driver_pass,
        "separate_driver_floor_theorem_target_falsified_on_stress_set": (
            not driver_pass),
        "first_channel_bound_pass_target": (
            channel_pass[0]["target"] if channel_pass else None),
        "first_coupled_slack_pass_target": (
            coupled_pass[0]["target"] if coupled_pass else None),
        "channel_payment_ratio_summary": finite_summary(payment_ratios),
        "passing_channel_payment_ratio_summary": finite_summary(
            row["channel_payment_ratio_to_driver_deficit"]
            for row in coupled_pass),
        "failing_channel_payment_ratio_summary": finite_summary(
            row["channel_payment_ratio_to_driver_deficit"]
            for row in rows if not row["coupled_slack_positive"]),
        "tightest_passing_row": min(
            coupled_pass,
            key=lambda row: row["strict_closure_margin"]),
        "strongest_failing_row": max(
            (row for row in rows if not row["coupled_slack_positive"]),
            key=lambda row: row["strict_closure_margin"]),
        "rows": rows,
        "candidate": {
            "name": "coupled driver-channel slack theorem target",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Replace independent selected-late driver-floor and channel "
                "bounds with the aggregate tradeoff "
                "driver_margin + L*channel_margin > 0."),
            "prediction": (
                "On the stress rows, pass/fail is exactly the channel payment "
                "ratio crossing 1: channel surplus must exceed the driver "
                "deficit."),
            "falsifier": (
                "A row whose coupled slack is positive while channel_payment/"
                "driver_deficit <= 1, or nonpositive while the ratio > 1, "
                "would falsify this diagnosis."),
            "smallest_test": (
                "Replay the post-discovery stress rows and count driver-floor "
                "passes, channel-bound passes, coupled passes, and payment "
                "ratios."),
        },
        "decision": (
            "The selected-late strict-closure failure is not primarily a bad "
            "channel-only story and cannot be repaired by proving the frozen "
            "driver floor independently: the driver floor fails on all 11 "
            "stress rows.  The five passing rows are exactly the rows where "
            "channel surplus pays more than 100 percent of the driver deficit. "
            "The next theorem target should be a coupled pointwise tradeoff "
            "or direct unnormalized signed estimate, not separate finite-fit "
            "driver and channel suprema."),
        "status_boundary": (
            "Finite coupled-slack diagnosis only.  It proves no universal "
            "active-lane theorem, pointwise adverse-drag theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof."),
        "goldbach_proved": False,
        "strict_closure_theorem_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

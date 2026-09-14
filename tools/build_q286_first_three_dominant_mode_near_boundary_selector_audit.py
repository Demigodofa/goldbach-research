"""Build q286 dominant-mode near-boundary selector audit evidence."""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-near-boundary-selector-audit.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_near_boundary_selector_audit_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_ready(item) for item in value]
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def main():
    receipt = (
        q286_first_three_dominant_mode_near_boundary_selector_audit_receipt())
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite selector audit only; it falsifies simple checked "
            "selectors for near-boundary above-floor margins and proves no "
            "selector theorem, signed prime-correlation theorem, or Goldbach "
            "theorem"),
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "window_specs": receipt["window_specs"],
        "target_step": receipt["target_step"],
        "near_thresholds": receipt["near_thresholds"],
        "evaluated_target_count": receipt["evaluated_target_count"],
        "window_rows": receipt["window_rows"],
        "absolute_surplus_summary": receipt["absolute_surplus_summary"],
        "signed_surplus_summary": receipt["signed_surplus_summary"],
        "deficit_count": receipt["deficit_count"],
        "closest_overall_rows": receipt["closest_overall_rows"],
        "threshold_rows": receipt["threshold_rows"],
        "residue_only_refuted_thresholds": (
            receipt["residue_only_refuted_thresholds"]),
        "scalar_interval_refuted_thresholds": (
            receipt["scalar_interval_refuted_thresholds"]),
        "interpretation": {
            "mechanism_tested": (
                "Treat the frozen full-stage above-floor tiny margins as "
                "near-boundary events and test whether simple selectors such "
                "as q286 residue or scalar residual intervals isolate them."),
            "falsifier": (
                "A selector is falsified on the checked rows when it selects "
                "a near-boundary row but also selects safer rows outside the "
                "same near-boundary band."),
            "boundary": (
                "False positives here refute only these simple checked "
                "selector forms.  They do not refute every possible arithmetic "
                "selector or any complement/lower-support rescue theorem."),
            "next_theorem": (
                "A viable selector theorem must use finer actual prime-pair "
                "distribution than q286 residue alone or a single scalar "
                "residual interval, or it must be replaced by a signed "
                "aggregate theorem."),
        },
        "near_boundary_selector_audit_measured": True,
        "q286_residue_only_selector_theorem_proved": False,
        "scalar_residual_selector_theorem_proved": False,
        "near_boundary_selector_theorem_proved": False,
        "above_floor_threshold_theorem_proved": False,
        "fixed_modulus_binary_ap_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

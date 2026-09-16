"""Audit the M=229, p=379, Q=46189 middle-family exception.

The clearance logical bridge named Q=46189 as the smallest next test.  This
receipt asks whether a simple row-independent Cauchy/triangle estimate can
control that adverse denominator, or whether the exception requires a sharper
phase-defect estimate.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    PAIRS,
    THRESHOLD,
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_source_margin_denominator_audit import (  # noqa: E402
    label_rows_from_denominator,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-exception-bound-audit.json")
SOURCE_CLEARANCE = (
    Path("evidence")
    / "mobius-moment-square-degree5-source-margin-clearance-family-audit.json")
SCALE = 229
PRIME = 379
DENOMINATOR = 46189
TARGET_LABEL = "00,12"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def factor_integer(value):
    n = value
    factors = {}
    divisor = 2
    while divisor * divisor <= n:
        while n % divisor == 0:
            factors[str(divisor)] = factors.get(str(divisor), 0) + 1
            n //= divisor
        divisor += 1 if divisor == 2 else 2
    if n > 1:
        factors[str(n)] = factors.get(str(n), 0) + 1
    return factors


def denominator_matrices(cells, row_count, active_row_start):
    full_gram = np.zeros((6, 6), dtype=float)
    for _, value in cells:
        full_gram += DENOMINATOR * np.outer(
            value, np.conjugate(value)).real

    rows_window = np.arange(
        active_row_start, active_row_start + row_count, dtype=np.int64)
    residues = np.asarray([cell[0] for cell in cells], dtype=np.int64)
    values = np.asarray([cell[1] for cell in cells], dtype=complex)
    transforms = np.zeros((row_count, 6), dtype=complex)
    for first in range(0, len(residues), 8192):
        selected_residues = residues[first:first + 8192]
        phases = np.exp(
            2j * np.pi
            * ((rows_window[:, None] * selected_residues[None, :])
               % DENOMINATOR)
            / DENOMINATOR)
        transforms += phases @ values[first:first + 8192]
    active_gram = (
        DENOMINATOR / row_count
        * (transforms.T @ np.conjugate(transforms)).real)
    return full_gram, active_gram


def cauchy_row(label, left, right, full_gram, active_gram):
    active = float(2 * active_gram[left, right])
    full = float(2 * full_gram[left, right])
    margin = float(THRESHOLD * full - active)
    adverse = max(0.0, -margin)
    active_cauchy = float(
        2 * math.sqrt(max(0.0, active_gram[left, left])
                      * max(0.0, active_gram[right, right])))
    full_cauchy = float(
        2 * math.sqrt(max(0.0, full_gram[left, left])
                      * max(0.0, full_gram[right, right])))
    lower_bound_using_exact_full_and_active_cauchy = (
        THRESHOLD * full - active_cauchy)
    cauchy_adverse_budget = (
        THRESHOLD * abs(full) + active_cauchy)
    return {
        "label": label,
        "active_contribution": active,
        "full_contribution": full,
        "margin_full_over_2_minus_active": margin,
        "adverse_margin": adverse,
        "adverse_over_abs_half_full": (
            adverse / (THRESHOLD * abs(full)) if full else None),
        "active_cauchy_bound": active_cauchy,
        "full_cauchy_bound": full_cauchy,
        "active_over_cauchy": (
            active / active_cauchy if active_cauchy else None),
        "full_over_cauchy": (
            full / full_cauchy if full_cauchy else None),
        "lower_bound_using_exact_full_and_active_cauchy": (
            lower_bound_using_exact_full_and_active_cauchy),
        "cauchy_bound_proves_nonadverse": (
            lower_bound_using_exact_full_and_active_cauchy > 0),
        "cauchy_adverse_budget": cauchy_adverse_budget,
        "cauchy_budget_over_actual_adverse": (
            cauchy_adverse_budget / adverse if adverse else None),
        "active_minus_half_full_magnitude_gap": (
            abs(active) - THRESHOLD * abs(full)),
    }


def source_clearance_context():
    receipt = json.loads(
        SOURCE_CLEARANCE.read_text(encoding="utf-8"))
    row = next(
        item for item in receipt["scale_summaries"]
        if item["scale_modulus"] == SCALE and item["prime_modulus"] == PRIME)
    middle = row["family_summaries"]["middle_2_to_3"]
    return {
        "near_negative_abs": row["near_negative_abs"],
        "middle_positive_margin_sum": middle["positive_margin_sum"],
        "middle_negative_margin_sum": middle["negative_margin_sum"],
        "middle_total_margin": middle["total_margin"],
        "far_positive_margin_sum": (
            row["family_summaries"]["far_3_plus"]["positive_margin_sum"]),
        "middle_far_positive_margin_sum": (
            row["middle_far_positive_margin_sum"]),
        "middle_far_total_margin_sum": row["middle_far_total_margin_sum"],
        "q46189_middle_adverse_over_middle_far_positive": (
            abs(middle["negative_margin_sum"])
            / row["middle_far_positive_margin_sum"]),
        "q46189_middle_adverse_over_all_negative_margin": (
            abs(middle["negative_margin_sum"])
            / abs(row["total_summary"]["negative_margin_sum"])),
    }


def build_receipt():
    parameters = scale_parameters(SCALE)
    row_count = parameters["row_count"]
    threshold = PRIME * row_count
    _, cells_by_denominator = _residue_cells_by_denominator(
        PRIME,
        row_count,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    cells = cells_by_denominator[DENOMINATOR]
    full_gram, active_gram = denominator_matrices(
        cells, row_count, row_count)
    exact_rows = {
        row["label"]: row
        for row in label_rows_from_denominator(
            DENOMINATOR, cells, row_count, row_count)
    }
    component_rows = [
        cauchy_row(label, left, right, full_gram, active_gram)
        for left, right, left_label, right_label in PAIRS
        for label in [f"{left_label},{right_label}"]
    ]
    target = next(
        row for row in component_rows if row["label"] == TARGET_LABEL)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "HOLD_q46189_simple_cauchy_bound_insufficient",
        "source_clearance_family_audit": str(SOURCE_CLEARANCE),
        "question": (
            "For the M=229, p=379, Q=46189 middle-family exception, can a "
            "simple row-independent Cauchy/triangle estimate provide the "
            "needed independent bound?"),
        "answer": (
            "No.  The exact Q=46189 contribution is adverse but tiny compared "
            "with its half-full scale, while both active and full cross terms "
            "are essentially negative Cauchy saturating.  A Cauchy-only "
            "adverse budget is hundreds of times larger than the actual "
            "adverse margin, so the next proof target must be a phase-defect "
            "or cancellation estimate, not a generic magnitude bound."),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "reduced_denominator": DENOMINATOR,
            "reduced_denominator_factorization": factor_integer(DENOMINATOR),
            "row_count_A": row_count,
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "threshold_p_times_A": threshold,
            "clearance_ratio_q_over_pA": DENOMINATOR / threshold,
            "residue_cell_count": len(cells),
            "target_label": TARGET_LABEL,
        },
        "target_component": target,
        "exact_denominator_rows": exact_rows,
        "component_cauchy_rows": component_rows,
        "clearance_context": source_clearance_context(),
        "classification": {
            "simple_cauchy_bound_proves_nonadverse": (
                target["cauchy_bound_proves_nonadverse"]),
            "active_cross_term_cauchy_saturated_negative": (
                target["active_over_cauchy"] < -0.999999999999),
            "full_cross_term_cauchy_saturated_negative": (
                target["full_over_cauchy"] < -0.999999999999),
            "phase_defect_estimate_required": True,
            "finite_exact_exception_analyzed": True,
        },
        "candidate_next_action": {
            "name": "q46189 phase-defect bound",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Exploit the small gap between |active_Q| and |full_Q|/2 "
                "for the negative aligned cross term, rather than bounding "
                "active_Q by magnitude alone."),
            "prediction": (
                "A useful theorem will prove a positive lower bound for "
                "|full_Q|/2-|active_Q| or show this adverse aligned case is "
                "paid uniformly by neighboring middle/far denominators."),
            "falsifier": (
                "If aligned negative denominators can make |active_Q| exceed "
                "|full_Q|/2 by an amount not uniformly paid elsewhere, this "
                "clearance proof route fails."),
            "smallest_next_test": (
                "Derive a symbolic expression for the active/full saturation "
                "defect of Q=46189 and test whether it factors through the "
                "missing small primes 2,3,5,7 or through row-window endpoint "
                "phases."),
        },
        "decision": (
            "HOLD_q46189_simple_cauchy_bound_insufficient.  The denominator "
            "exception is localized and small in the finite ledger, but "
            "generic Cauchy/triangle control is much too weak.  Future work "
            "should seek a phase-defect or neighboring-denominator payment "
            "estimate before promoting the clearance route."),
        "finite_q46189_exception_audit_only": True,
        "finite_diagnostic_only": True,
        "simple_cauchy_theorem_proved": False,
        "phase_defect_theorem_proved": False,
        "near_adverse_upper_bound_proved": False,
        "middle_far_lower_bound_proved": False,
        "clearance_family_theorem_proved": False,
        "source_start_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "target_adverse_margin": (
            receipt["target_component"]["adverse_margin"]),
        "cauchy_budget_over_actual_adverse": (
            receipt["target_component"][
                "cauchy_budget_over_actual_adverse"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

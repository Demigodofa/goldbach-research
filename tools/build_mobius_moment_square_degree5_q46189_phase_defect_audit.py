"""Reduce the Q=46189 exception to a finite-window phase defect.

The Q=46189 Cauchy audit showed that simple magnitude control is useless
because the relevant cross terms are Cauchy-saturating.  This receipt checks
whether that saturation comes from a coordinate proportionality and records
the exact finite-window energy defect that makes the denominator adverse.
"""

from __future__ import annotations

import cmath
import json
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    PAIRS,
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_q46189_exception_bound_audit import (  # noqa: E402
    DENOMINATOR,
    PRIME,
    SCALE,
    TARGET_LABEL,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-phase-defect-audit.json")
SOURCE_EXCEPTION = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-exception-bound-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def cell_arrays():
    parameters = scale_parameters(SCALE)
    _, cells_by_denominator = _residue_cells_by_denominator(
        PRIME,
        parameters["row_count"],
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    cells = cells_by_denominator[DENOMINATOR]
    residues = np.asarray([cell[0] for cell in cells], dtype=np.int64)
    values = np.asarray([cell[1] for cell in cells], dtype=complex)
    return parameters, residues, values


def active_transforms(residues, values, row_count, active_row_start):
    rows_window = np.arange(
        active_row_start, active_row_start + row_count, dtype=np.int64)
    transforms = np.zeros((row_count, values.shape[1]), dtype=complex)
    for first in range(0, len(residues), 8192):
        selected_residues = residues[first:first + 8192]
        phases = np.exp(
            2j * np.pi
            * ((rows_window[:, None] * selected_residues[None, :])
               % DENOMINATOR)
            / DENOMINATOR)
        transforms += phases @ values[first:first + 8192]
    return transforms


def coordinate_pair_summary(values, transforms, row_count, left, right, label):
    x = values[:, left]
    y = values[:, right]
    tx = transforms[:, left]
    ty = transforms[:, right]
    scalar = np.vdot(x, y) / np.vdot(x, x)
    scalar_residual = np.linalg.norm(y - scalar * x) / np.linalg.norm(y)
    full_x = DENOMINATOR * float(np.vdot(x, x).real)
    full_y = DENOMINATOR * float(np.vdot(y, y).real)
    full_xy = DENOMINATOR * float(np.vdot(y, x).real)
    active_x = DENOMINATOR / row_count * float(np.vdot(tx, tx).real)
    active_y = DENOMINATOR / row_count * float(np.vdot(ty, ty).real)
    active_xy = DENOMINATOR / row_count * float(np.vdot(ty, tx).real)
    ratio = active_xy / full_xy
    defect = 0.5 - ratio
    return {
        "label": label,
        "best_scalar_right_over_left_real": float(scalar.real),
        "best_scalar_right_over_left_imag": float(scalar.imag),
        "best_scalar_abs": float(abs(scalar)),
        "best_scalar_phase": float(cmath.phase(scalar)),
        "relative_scalar_residual": float(scalar_residual),
        "full_left_energy": full_x,
        "full_right_energy": full_y,
        "full_cross": full_xy,
        "active_left_energy": active_x,
        "active_right_energy": active_y,
        "active_cross": active_xy,
        "active_over_full_cross_ratio": ratio,
        "half_threshold_defect": defect,
        "per_denominator_nonadversity": ratio > 0.5,
    }


def build_receipt():
    parameters, residues, values = cell_arrays()
    row_count = parameters["row_count"]
    transforms = active_transforms(residues, values, row_count, row_count)
    pair_summaries = [
        coordinate_pair_summary(
            values,
            transforms,
            row_count,
            left,
            right,
            f"{left_label},{right_label}",
        )
        for left, right, left_label, right_label in PAIRS
    ]
    target = next(row for row in pair_summaries if row["label"] == TARGET_LABEL)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "FALSIFIER_q46189_per_denominator_nonadversity",
        "source_exception_bound_audit": str(SOURCE_EXCEPTION),
        "question": (
            "Does the Q=46189 exception reduce to a coordinate "
            "proportionality and a finite-window energy defect?"),
        "answer": (
            "Yes.  For the target 00,12 component, coordinate 12 is a fixed "
            "negative scalar multiple of coordinate 00 to numerical "
            "precision.  The denominator is adverse because the resulting "
            "one-coordinate active/full energy ratio is 0.497309..., below "
            "the one-half threshold.  Thus per-denominator nonadversity is "
            "false for Q=46189; the clearance route must prove group payment "
            "or a phase-defect compensation theorem."),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "reduced_denominator": DENOMINATOR,
            "row_count_A": row_count,
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "residue_cell_count": int(values.shape[0]),
            "target_label": TARGET_LABEL,
        },
        "target_pair_summary": target,
        "pair_summaries": pair_summaries,
        "classification": {
            "target_coordinate_proportionality_confirmed": (
                target["relative_scalar_residual"] < 1e-12),
            "target_scalar_is_negative_real": (
                target["best_scalar_right_over_left_real"] < 0
                and abs(target["best_scalar_right_over_left_imag"]) < 1e-12),
            "target_window_energy_ratio_below_half": (
                target["active_over_full_cross_ratio"] < 0.5),
            "per_denominator_nonadversity_falsified": (
                not target["per_denominator_nonadversity"]),
            "group_payment_required": True,
        },
        "candidate_next_action": {
            "name": "q46189 group-payment phase defect",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Treat Q=46189 as a known negative aligned denominator and "
                "prove that adjacent or related middle/far denominators pay "
                "its finite-window energy defect."),
            "prediction": (
                "The paying denominators should share the high-prime tail or "
                "differ by inserting one of the missing small primes 2,3,5,7, "
                "rather than being arbitrary large positive terms."),
            "falsifier": (
                "If Q=46189-style aligned negative defects can occur without "
                "nearby middle/far payment in the same source-admissible "
                "block, the clearance proof route fails."),
            "smallest_next_test": (
                "Compute the positive denominator rows in the M=229,p=379 "
                "middle/far ledger that share the 11*13*17*19 tail or add "
                "one missing small prime, then test whether their surplus "
                "dominates the Q=46189 phase defect without using total "
                "positivity."),
        },
        "decision": (
            "The Q=46189 exception is a finite falsifier for any theorem "
            "requiring every middle/far denominator to be nonadverse.  The "
            "surviving theorem target is group payment for aligned negative "
            "finite-window phase defects."),
        "finite_phase_defect_audit_only": True,
        "finite_diagnostic_only": True,
        "per_denominator_nonadversity_theorem_proved": False,
        "phase_defect_payment_theorem_proved": False,
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
        "target_ratio": receipt["target_pair_summary"][
            "active_over_full_cross_ratio"],
        "target_defect": receipt["target_pair_summary"][
            "half_threshold_defect"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

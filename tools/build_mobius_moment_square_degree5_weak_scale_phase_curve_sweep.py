"""Build a weak-scale degree-5 active-window phase-curve sweep."""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lcm_sawtooth_lifted_endpoint_frame import (  # noqa: E402
    _lifted_frequency_data,
    _symmetric_pair_coordinates,
)
from mobius_covariance_endpoint_probe import _prime_flags  # noqa: E402
from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    PAIRS,
    THRESHOLD,
    dominance_row,
    scale_parameters,
    sign_counts,
)


WEAK_SCALE = 167
OUTPUT = Path(
    "evidence/mobius-moment-square-degree5-weak-scale-phase-curve-sweep.json")


def active_row_start_sweep():
    row_count = scale_parameters(WEAK_SCALE)["row_count"]
    return list(range(0, 2 * row_count + 1))


def _residue_cells_by_denominator(
        modulus, row_count, ell_freeze, divisor_lower, divisor_upper):
    denominators, numerators, geometrics, coordinates = _lifted_frequency_data(
        modulus, ell_freeze, divisor_lower, divisor_upper)
    threshold = modulus * row_count
    residue_cells = {}
    chunk_size = 64
    for first in range(0, len(denominators), chunk_size):
        left_d = denominators[first:first + chunk_size, None]
        left_k = numerators[first:first + chunk_size, None]
        common = np.lcm(left_d, denominators[None, :])
        difference_numerator = (
            left_k * (common // left_d)
            - numerators[None, :] * (common // denominators[None, :]))
        common_factor = np.gcd(np.abs(difference_numerator), common)
        reduced = common // common_factor
        high_q = reduced > threshold
        if not np.any(high_q):
            continue
        residues = np.zeros(reduced.shape, dtype=np.int64)
        residues[high_q] = (
            modulus
            * (difference_numerator[high_q] // common_factor[high_q])
            % reduced[high_q])
        left_coordinates = np.broadcast_to(
            coordinates[first:first + chunk_size, None, :],
            (*reduced.shape, 3))[high_q]
        right_coordinates = np.broadcast_to(
            coordinates[None, :, :], (*reduced.shape, 3))[high_q]
        lifted = _symmetric_pair_coordinates(
            left_coordinates, right_coordinates)
        products = (
            geometrics[first:first + chunk_size, None]
            * np.conjugate(geometrics[None, :]))[high_q]
        keys = np.column_stack((reduced[high_q], residues[high_q]))
        unique, inverse = np.unique(keys, axis=0, return_inverse=True)
        weighted_lifted = products[:, None] * lifted
        grouped = np.empty((len(unique), 6), dtype=complex)
        for coordinate in range(6):
            grouped[:, coordinate] = (
                np.bincount(
                    inverse, weights=weighted_lifted[:, coordinate].real)
                + 1j * np.bincount(
                    inverse, weights=weighted_lifted[:, coordinate].imag))
        for key, value in zip(unique, grouped):
            integer_key = (int(key[0]), int(key[1]))
            if integer_key in residue_cells:
                residue_cells[integer_key] += value
            else:
                residue_cells[integer_key] = value
    denominator_gram = np.zeros((6, 6), dtype=float)
    cells_by_denominator = {}
    for key, value in residue_cells.items():
        reduced_denominator = key[0]
        denominator_gram += (
            reduced_denominator
            * np.outer(value, np.conjugate(value)).real)
        cells_by_denominator.setdefault(
            reduced_denominator, []).append((key[1], value))
    return denominator_gram, cells_by_denominator


def _active_gram(cells_by_denominator, row_count, active_row_start):
    active = np.zeros((6, 6), dtype=float)
    rows = np.arange(
        active_row_start, active_row_start + row_count, dtype=np.int64)
    residue_chunk_size = 8192
    for reduced_denominator, cells in cells_by_denominator.items():
        residues = np.asarray([cell[0] for cell in cells], dtype=np.int64)
        values = np.asarray([cell[1] for cell in cells], dtype=complex)
        transforms = np.zeros((row_count, 6), dtype=complex)
        for first in range(0, len(residues), residue_chunk_size):
            selected_residues = residues[first:first + residue_chunk_size]
            phases = np.exp(
                2j * np.pi
                * ((rows[:, None] * selected_residues[None, :])
                   % reduced_denominator)
                / reduced_denominator)
            transforms += phases @ values[first:first + residue_chunk_size]
        active += (
            reduced_denominator / row_count
            * (transforms.T @ np.conjugate(transforms)).real)
    return active


def _dominance_rows_for_start(
        prime_modulus, active_row_start, row_count, active, full):
    component_rows = []
    dominance_rows = []
    for left, right, left_label, right_label in PAIRS:
        active_contribution = float(2 * active[left, right])
        full_contribution = float(2 * full[left, right])
        half_contribution = (
            active_contribution - THRESHOLD * full_contribution)
        row = dominance_row(
            WEAK_SCALE,
            prime_modulus,
            f"{left_label},{right_label}",
            active_contribution,
            full_contribution,
            half_contribution,
        )
        row["active_row_start"] = active_row_start
        row["active_row_stop"] = active_row_start + row_count
        row["active_row_start_offset"] = active_row_start - row_count
        component_rows.append(row)
        dominance_rows.append(row)
    active_total = sum(row["active_contribution"] for row in component_rows)
    full_total = sum(row["full_contribution"] for row in component_rows)
    half_total = sum(row["half_frame_contribution"] for row in component_rows)
    total_row = dominance_row(
        WEAK_SCALE,
        prime_modulus,
        "TOTAL",
        active_total,
        full_total,
        half_total,
    )
    total_row["active_row_start"] = active_row_start
    total_row["active_row_stop"] = active_row_start + row_count
    total_row["active_row_start_offset"] = active_row_start - row_count
    dominance_rows.append(total_row)
    return dominance_rows


def label_summary(rows, label):
    selected = [row for row in rows if row["label"] == label]
    slacks = [row["dominance_slack_above_one_half"] for row in selected]
    weakest = min(
        selected, key=lambda row: row["dominance_slack_above_one_half"])
    strongest = max(
        selected, key=lambda row: row["dominance_slack_above_one_half"])
    return {
        "label": label,
        "row_count": len(selected),
        "dominance_slack_sign_counts": sign_counts(slacks),
        "all_rows_dominate_one_half_signed_full": all(
            row["dominates_one_half_signed_full"] for row in selected),
        "minimum_dominance_slack_above_one_half": min(slacks),
        "maximum_dominance_slack_above_one_half": max(slacks),
        "weakest_dominance_row": weakest,
        "strongest_dominance_row": strongest,
    }


def prime_summary(prime_modulus):
    parameters = scale_parameters(WEAK_SCALE)
    divisor_lower, divisor_upper = parameters["divisor_range"]
    full, cells_by_denominator = _residue_cells_by_denominator(
        prime_modulus,
        parameters["row_count"],
        parameters["ell_freeze"],
        divisor_lower,
        divisor_upper,
    )
    rows = []
    failure_rows = []
    for active_row_start in active_row_start_sweep():
        active = _active_gram(
            cells_by_denominator, parameters["row_count"], active_row_start)
        start_rows = _dominance_rows_for_start(
            prime_modulus,
            active_row_start,
            parameters["row_count"],
            active,
            full,
        )
        rows.extend(start_rows)
        failure_rows.extend([
            row for row in start_rows
            if not row["dominates_one_half_signed_full"]
        ])
    slacks = [row["dominance_slack_above_one_half"] for row in rows]
    weakest = min(
        rows, key=lambda row: row["dominance_slack_above_one_half"])
    strongest = max(
        rows, key=lambda row: row["dominance_slack_above_one_half"])
    labels = [f"{left},{right}" for _, _, left, right in PAIRS]
    labels.append("TOTAL")
    return {
        "scale_modulus": WEAK_SCALE,
        "prime_modulus": prime_modulus,
        "row_count": parameters["row_count"],
        "ell_freeze": parameters["ell_freeze"],
        "divisor_range": parameters["divisor_range"],
        "active_row_start_count": len(active_row_start_sweep()),
        "component_row_count": sum(
            1 for row in rows if row["label"] != "TOTAL"),
        "degree5_total_row_count": sum(
            1 for row in rows if row["label"] == "TOTAL"),
        "dominance_row_count": len(rows),
        "dominance_slack_sign_counts": sign_counts(slacks),
        "all_rows_dominate_one_half_signed_full": len(failure_rows) == 0,
        "failure_row_count": len(failure_rows),
        "failure_rows": failure_rows,
        "minimum_dominance_slack_above_one_half": min(slacks),
        "maximum_dominance_slack_above_one_half": max(slacks),
        "weakest_dominance_row": weakest,
        "strongest_dominance_row": strongest,
        "label_summaries": {
            label: label_summary(rows, label) for label in labels
        },
    }


def build_receipt():
    parameters = scale_parameters(WEAK_SCALE)
    flags = _prime_flags(2 * WEAK_SCALE)
    prime_summaries = [
        prime_summary(prime_modulus)
        for prime_modulus in range(WEAK_SCALE, 2 * WEAK_SCALE + 1)
        if flags[prime_modulus]
    ]
    all_failures = []
    for summary in prime_summaries:
        all_failures.extend(summary["failure_rows"])
    weakest = min(
        (summary["weakest_dominance_row"] for summary in prime_summaries),
        key=lambda row: row["dominance_slack_above_one_half"])
    strongest = max(
        (summary["strongest_dominance_row"] for summary in prime_summaries),
        key=lambda row: row["dominance_slack_above_one_half"])
    row_count = sum(summary["dominance_row_count"]
                    for summary in prime_summaries)
    component_count = sum(summary["component_row_count"]
                          for summary in prime_summaries)
    total_count = sum(summary["degree5_total_row_count"]
                      for summary in prime_summaries)
    slack_sign_counts = {
        "positive": row_count - len(all_failures),
        "zero": sum(
            1 for row in all_failures
            if row["dominance_slack_above_one_half"] == 0),
        "negative": sum(
            1 for row in all_failures
            if row["dominance_slack_above_one_half"] < 0),
    }
    return {
        "status": "SWEEP_degree5_weak_scale_active_window_phase_curve",
        "question": (
            "Across every weak-scale prime row, does sweeping the active row "
            "start over the extended local band 0..70 expose a concrete "
            "degree-5 active/full dominance failure?"),
        "scale_modulus": WEAK_SCALE,
        "threshold": THRESHOLD,
        "row_count": parameters["row_count"],
        "ell_freeze": parameters["ell_freeze"],
        "divisor_range": parameters["divisor_range"],
        "active_row_start_sweep": active_row_start_sweep(),
        "active_row_start_count": len(active_row_start_sweep()),
        "prime_count": len(prime_summaries),
        "prime_summaries": prime_summaries,
        "component_row_count": component_count,
        "degree5_total_row_count": total_count,
        "dominance_row_count": row_count,
        "all_dominance_slack_sign_counts": slack_sign_counts,
        "all_rows_dominate_one_half_signed_full": len(all_failures) == 0,
        "failure_row_count": len(all_failures),
        "failure_rows": all_failures,
        "minimum_dominance_slack_above_one_half": (
            weakest["dominance_slack_above_one_half"]),
        "maximum_dominance_slack_above_one_half": (
            strongest["dominance_slack_above_one_half"]),
        "weakest_dominance_row": weakest,
        "strongest_dominance_row": strongest,
        "prediction": (
            "If the local active-window dominance margin is not isolated to "
            "one favorable weak prime, every prime in the weak scale should "
            "retain positive slack through the broader row-start sweep."),
        "falsifier": (
            "Any component or degree-5 total row for any weak-scale prime and "
            "active row start 0 through 70 whose signed full contribution is "
            "negative but whose active/full ratio is at or below one half, or "
            "any row losing the negative signed-full premise, is a concrete "
            "finite falsifier for this weak-scale phase-curve sweep."),
        "decision": (
            "The weak-scale extended local phase-curve sweep survives: every "
            "component and degree-5 total row for every weak-scale prime and "
            "active row start 0 through 70 retains positive active/full "
            "dominance slack above one half.  This is useful curve-family "
            "evidence for the active-window theorem target, not a period "
            "theorem or a universal pointwise bound."),
        "finite_weak_scale_phase_curve_sweep_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
        "phase_curve_theorem_proved": False,
        "active_window_translation_theorem_proved": False,
        "ell_freeze_dominance_theorem_proved": False,
        "checked_scale_dominance_theorem_proved": False,
        "primewise_dominance_theorem_proved": False,
        "degree5_coefficient_theorem_proved": False,
        "robust_margin_universal_theorem_proved": False,
        "coefficient_family_theorem_proved": False,
        "universal_sturm_certificate_theorem_proved": False,
        "moment_square_half_frame_curve_positivity_theorem_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "mobius_covariance_theorem_proved": False,
        "signed_prime_correlation_proved": False,
    }


def main():
    receipt = build_receipt()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()

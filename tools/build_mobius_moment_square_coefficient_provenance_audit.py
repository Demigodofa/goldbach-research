"""Build the coefficient provenance audit for half-frame curve polynomials."""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lcm_sawtooth_lifted_endpoint_frame import (  # noqa: E402
    project_prime_block_lifted_endpoint_scan,
)


CURVE_AUDIT = Path("evidence/mobius-moment-square-half-frame-curve-audit.json")
OUTPUT = Path("evidence/mobius-moment-square-coefficient-provenance-audit.json")
SCALES = (127, 149, 167, 191, 211, 227)
LABELS = ("00", "01", "02", "11", "12", "22")
DEGREES = (4, 3, 2, 2, 1, 0)
EXPECTED_SIGNS = {
    degree: ("positive" if degree % 2 == 0 else "negative")
    for degree in range(9)
}


def sign_name(value, tolerance=0.0):
    if value > tolerance:
        return "positive"
    if value < -tolerance:
        return "negative"
    return "zero"


def degree_contributions(active, full):
    """Return degree-wise coefficient provenance for y^T(A-.5F)y."""
    active = np.asarray(active, dtype=float)
    full = np.asarray(full, dtype=float)
    if active.shape != (6, 6) or full.shape != (6, 6):
        raise ValueError("active and full must be 6 by 6")
    active = (active + active.T) / 2
    full = (full + full.T) / 2
    half_frame = active - 0.5 * full

    rows = []
    for degree in range(9):
        contributors = []
        active_coefficient = 0.0
        full_coefficient = 0.0
        half_frame_coefficient = 0.0
        for left in range(6):
            for right in range(left, 6):
                if DEGREES[left] + DEGREES[right] != degree:
                    continue
                multiplicity = 1 if left == right else 2
                active_part = float(multiplicity * active[left, right])
                full_part = float(multiplicity * full[left, right])
                half_part = float(multiplicity * half_frame[left, right])
                active_coefficient += active_part
                full_coefficient += full_part
                half_frame_coefficient += half_part
                contributors.append({
                    "left_label": LABELS[left],
                    "right_label": LABELS[right],
                    "multiplicity": multiplicity,
                    "active_contribution": active_part,
                    "full_contribution": full_part,
                    "half_frame_contribution": half_part,
                })
        top = max(
            contributors,
            key=lambda item: abs(item["half_frame_contribution"]))
        rows.append({
            "degree": degree,
            "expected_sign": EXPECTED_SIGNS[degree],
            "active_coefficient": active_coefficient,
            "full_coefficient": full_coefficient,
            "half_frame_coefficient": half_frame_coefficient,
            "half_frame_sign": sign_name(half_frame_coefficient),
            "active_over_full_coefficient_ratio": (
                active_coefficient / full_coefficient
                if full_coefficient else None),
            "top_abs_contributor": top,
            "contributor_count": len(contributors),
        })
    return rows


def scale_receipt(scale_modulus, source_coefficients):
    frame = project_prime_block_lifted_endpoint_scan(scale_modulus)
    active = np.asarray(frame["aggregate_active_window_residue_energy_gram"])
    active = (active + active.T) / 2
    full = np.asarray(frame["aggregate_full_residue_energy_gram"])
    full = (full + full.T) / 2

    degrees = degree_contributions(active, full)
    coefficient_deltas = []
    for degree_row, source_coefficient in zip(degrees, source_coefficients):
        delta = degree_row["half_frame_coefficient"] - source_coefficient
        scale = max(1.0, abs(source_coefficient))
        coefficient_deltas.append(abs(delta) / scale)
        degree_row["source_curve_coefficient"] = source_coefficient
        degree_row["source_curve_coefficient_delta"] = delta

    signs_match = all(
        row["half_frame_sign"] == row["expected_sign"]
        for row in degrees)
    top_signature = tuple(
        (
            row["degree"],
            row["top_abs_contributor"]["left_label"],
            row["top_abs_contributor"]["right_label"],
        )
        for row in degrees)
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        "degree_coefficients": degrees,
        "alternating_degree_sign_pattern_holds": signs_match,
        "top_abs_contributor_signature": top_signature,
        "maximum_relative_source_coefficient_delta": (
            max(coefficient_deltas)),
    }


def build_receipt():
    source = json.loads(CURVE_AUDIT.read_text(encoding="utf-8"))
    source_by_scale = {
        row["scale_modulus"]: row["polynomial_coefficients_low_to_high"]
        for row in source["scale_results"]
    }
    rows = [
        scale_receipt(scale, source_by_scale[scale])
        for scale in SCALES
    ]
    signatures = {
        tuple(tuple(item) for item in row["top_abs_contributor_signature"])
        for row in rows
    }
    return {
        "status": "TARGET_moment_square_coefficient_provenance",
        "question": (
            "Which active/full Gram entries produce the recorded "
            "half-frame degree-8 coefficients, and is the sign/top-entry "
            "structure stable across checked scales?"),
        "source_curve_audit": str(CURVE_AUDIT),
        "scales": SCALES,
        "coordinate_labels": LABELS,
        "coordinate_degrees": DEGREES,
        "expected_alternating_signs": EXPECTED_SIGNS,
        "scale_results": rows,
        "all_reconstructed_coefficients_match_source": all(
            row["maximum_relative_source_coefficient_delta"] <= 1e-12
            for row in rows),
        "all_alternating_degree_sign_patterns_hold": all(
            row["alternating_degree_sign_pattern_holds"] for row in rows),
        "stable_top_abs_contributor_signature": len(signatures) == 1,
        "top_abs_contributor_signature": (
            rows[0]["top_abs_contributor_signature"] if len(signatures) == 1
            else None),
        "maximum_relative_source_coefficient_delta": max(
            row["maximum_relative_source_coefficient_delta"] for row in rows),
        "decision": (
            "The recorded half-frame polynomial coefficients are exactly "
            "reproduced by degree-wise sums of active minus one-half full "
            "Gram entries.  On checked scales the coefficient signs alternate "
            "by degree and the dominant unordered Gram-entry contributor for "
            "each degree is stable.  This does not prove positivity "
            "universally; it identifies the coefficient-family structure a "
            "real theorem must derive and bound."),
        "finite_coefficient_provenance_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
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

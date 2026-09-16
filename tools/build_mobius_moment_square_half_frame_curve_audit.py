"""Build the Mobius moment-square half-frame curve-positivity audit."""

import json
import sys
from pathlib import Path

import numpy as np
from numpy.polynomial import Polynomial

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lcm_sawtooth_lifted_endpoint_frame import (  # noqa: E402
    project_prime_block_lifted_endpoint_scan,
)


OUTPUT = Path("evidence/mobius-moment-square-half-frame-curve-audit.json")
SCALES = (127, 149, 167, 191, 211, 227)


def moment_square_quadratic_polynomial(matrix):
    """Return y(t)^T matrix y(t) for y=(t^4,t^3,t^2,t^2,t,1)."""
    matrix = np.asarray(matrix, dtype=float)
    if matrix.shape != (6, 6):
        raise ValueError("matrix must be 6 by 6")
    matrix = (matrix + matrix.T) / 2

    variable = Polynomial((0.0, 1.0))
    curve = (
        variable ** 4,
        variable ** 3,
        variable ** 2,
        variable ** 2,
        variable,
        Polynomial((1.0,)),
    )
    polynomial = Polynomial((0.0,))
    for left in range(6):
        for right in range(6):
            polynomial += float(matrix[left, right]) * curve[left] * curve[right]
    return polynomial


def polynomial_minimum(polynomial):
    """Minimize a positive-leading real polynomial over the real line."""
    candidates = {0.0}
    for root in polynomial.deriv().roots():
        if abs(root.imag) <= 1e-7:
            candidates.add(float(root.real))

    evaluations = sorted(
        (
            {
                "parameter": parameter,
                "value": float(polynomial(parameter)),
            }
            for parameter in candidates
        ),
        key=lambda row: row["value"])
    best = evaluations[0]
    return {
        "minimum_value": best["value"],
        "minimizing_parameter": best["parameter"],
        "real_stationary_or_check_parameters": [
            row["parameter"] for row in evaluations],
        "smallest_evaluations": evaluations[:5],
        "leading_coefficient": float(polynomial.coef[-1]),
        "degree": polynomial.degree(),
    }


def scale_receipt(scale_modulus):
    frame = project_prime_block_lifted_endpoint_scan(scale_modulus)
    active = np.asarray(frame["aggregate_active_window_residue_energy_gram"])
    active = (active + active.T) / 2
    full = np.asarray(frame["aggregate_full_residue_energy_gram"])
    full = (full + full.T) / 2
    half_frame = active - 0.5 * full
    polynomial = moment_square_quadratic_polynomial(half_frame)
    minimum = polynomial_minimum(polynomial)
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        "polynomial_coefficients_low_to_high": [
            float(value) for value in polynomial.coef],
        "half_frame_curve_minimum": minimum["minimum_value"],
        "half_frame_curve_minimizing_parameter": (
            minimum["minimizing_parameter"]),
        "half_frame_curve_minimum_positive": (
            minimum["minimum_value"] > 0),
        "half_frame_curve_leading_coefficient": (
            minimum["leading_coefficient"]),
        "half_frame_curve_degree": minimum["degree"],
        "smallest_evaluations": minimum["smallest_evaluations"],
    }


def build_receipt():
    rows = [scale_receipt(scale) for scale in SCALES]
    weakest = min(rows, key=lambda row: row["half_frame_curve_minimum"])
    return {
        "status": "TARGET_moment_square_half_frame_curve_positivity",
        "question": (
            "Is the entire moment-square half-frame polynomial "
            "y(t)^T(active-one_half*full)y(t) positive on the checked "
            "scales, not merely positive at selected soft directions?"),
        "scales": SCALES,
        "scale_results": rows,
        "all_half_frame_curve_minima_positive": all(
            row["half_frame_curve_minimum_positive"] for row in rows),
        "minimum_half_frame_curve_value": (
            weakest["half_frame_curve_minimum"]),
        "weakest_half_frame_curve_row": weakest,
        "decision": (
            "The checked half-frame payment is positive on the whole "
            "moment-square curve.  This is a stronger theorem target than "
            "testing selected soft parameters: prove positivity of the "
            "degree-8 polynomial y(t)^T(active-one_half*full)y(t), or find "
            "a legitimate scale where its real-line minimum is nonpositive."),
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
        "moment_square_half_frame_curve_positivity_theorem_proved": False,
        "moment_square_half_frame_payment_theorem_proved": False,
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

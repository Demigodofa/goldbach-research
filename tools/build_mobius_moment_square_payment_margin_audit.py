"""Build the Mobius moment-square half-frame payment-margin audit."""

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
from mobius_moment_square_metric import (  # noqa: E402
    diagonal_equilibration_metric,
    moment_square_quadratic_quotient_minimum,
)
from mobius_moment_square_nullspace import moment_square_vector  # noqa: E402


OUTPUT = Path("evidence/mobius-moment-square-payment-margin-audit.json")
SCALES = (127, 149, 167, 191, 211, 227)


def _moment_vector(parameter):
    if parameter is None:
        return np.array((1.0, 0.0, 0.0, 0.0, 0.0, 0.0))
    return moment_square_vector(parameter)


def payment_row(label, parameter, active, full):
    vector = _moment_vector(parameter)
    active_value = float(vector @ active @ vector)
    full_value = float(vector @ full @ vector)
    ratio = float(active_value / full_value) if full_value > 0 else None
    half_margin = float(active_value - 0.5 * full_value)
    full_margin = float(active_value - full_value)
    return {
        "direction": label,
        "parameter": parameter,
        "full_value": full_value,
        "active_value": active_value,
        "active_over_full_ratio": ratio,
        "half_frame_margin": half_margin,
        "half_frame_margin_over_full": (
            float(half_margin / full_value) if full_value > 0 else None),
        "active_minus_full": full_margin,
        "active_minus_full_over_full": (
            float(full_margin / full_value) if full_value > 0 else None),
        "half_frame_margin_positive": half_margin > 0,
    }


def scale_receipt(scale_modulus):
    frame = project_prime_block_lifted_endpoint_scan(scale_modulus)
    active = np.asarray(frame["aggregate_active_window_residue_energy_gram"])
    active = (active + active.T) / 2
    full = np.asarray(frame["aggregate_full_residue_energy_gram"])
    full = (full + full.T) / 2

    active_over_full = moment_square_quadratic_quotient_minimum(
        active, full)
    metric, _ = diagonal_equilibration_metric(full)
    full_soft = moment_square_quadratic_quotient_minimum(full, metric)

    directions = [
        payment_row(
            "moment_square_active_over_full_minimizer",
            active_over_full["minimizing_parameter"],
            active,
            full),
        payment_row(
            "diagonal_equilibrated_full_soft_parameter",
            full_soft["minimizing_parameter"],
            active,
            full),
    ]
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        "directions": directions,
    }


def build_receipt():
    rows = [scale_receipt(scale) for scale in SCALES]
    all_directions = [
        dict(direction, scale_modulus=row["scale_modulus"])
        for row in rows
        for direction in row["directions"]
    ]
    weakest_half_margin_ratio = min(
        all_directions,
        key=lambda row: row["half_frame_margin_over_full"])
    weakest_raw_half_margin = min(
        all_directions,
        key=lambda row: row["half_frame_margin"])
    most_negative_full_margin = min(
        all_directions,
        key=lambda row: row["active_minus_full_over_full"])
    return {
        "status": "TARGET_moment_square_half_frame_payment_margin",
        "question": (
            "At the moment-square active/full minimizer and at the "
            "diagonal-equilibrated full-soft parameter, is the unnormalized "
            "active payment margin active - one_half*full positive?"),
        "scales": SCALES,
        "scale_results": rows,
        "direction_count": len(all_directions),
        "all_half_frame_margins_positive": all(
            row["half_frame_margin_positive"] for row in all_directions),
        "minimum_half_frame_margin_over_full": (
            weakest_half_margin_ratio["half_frame_margin_over_full"]),
        "weakest_half_frame_margin_ratio_row": weakest_half_margin_ratio,
        "minimum_raw_half_frame_margin": (
            weakest_raw_half_margin["half_frame_margin"]),
        "weakest_raw_half_frame_margin_row": weakest_raw_half_margin,
        "most_negative_active_minus_full_over_full": (
            most_negative_full_margin["active_minus_full_over_full"]),
        "most_negative_active_minus_full_row": most_negative_full_margin,
        "decision": (
            "The checked moment-square directions are active-paid relative "
            "to the one-half full-frame target in unnormalized quadratic "
            "form.  Some directions still have active below full, so the "
            "right theorem target is not active>=full.  The proof-shaped "
            "target is a universal pointwise estimate proving "
            "active(y_N,N) - one_half*full(y_N,N) > 0 for the metric-soft "
            "moment-square channel, or a direct falsifier where that margin "
            "turns nonpositive."),
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
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

"""Build the Mobius moment-square active/full ratio audit."""

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


OUTPUT = Path("evidence/mobius-moment-square-active-ratio-audit.json")
SCALES = (127, 149, 167, 191, 211, 227)


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
    soft_parameter = full_soft["minimizing_parameter"]
    soft_vector = moment_square_vector(soft_parameter)
    ratio_at_full_soft = float(
        soft_vector @ active @ soft_vector
        / (soft_vector @ full @ soft_vector))
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        "moment_square_active_over_full_minimum": active_over_full[
            "minimum_value"],
        "active_over_full_minimizing_parameter": active_over_full[
            "minimizing_parameter"],
        "ratio_at_equilibrated_full_soft_parameter": ratio_at_full_soft,
        "equilibrated_full_soft_parameter": soft_parameter,
        "equilibrated_full_soft_minimum": full_soft["minimum_value"],
    }


def build_receipt():
    rows = [scale_receipt(scale) for scale in SCALES]
    return {
        "status": "FALSIFY_moment_square_soft_direction_as_adverse_drag",
        "question": (
            "Does the diagonal-equilibrated moment-square soft direction "
            "create an active/full lower-frame obstruction?"),
        "scales": SCALES,
        "scale_results": rows,
        "minimum_moment_square_active_over_full": min(
            row["moment_square_active_over_full_minimum"] for row in rows),
        "minimum_ratio_at_equilibrated_full_soft_parameter": min(
            row["ratio_at_equilibrated_full_soft_parameter"]
            for row in rows),
        "all_moment_square_curve_ratios_above_one_half": all(
            row["moment_square_active_over_full_minimum"] >= .5
            for row in rows),
        "all_full_soft_ratios_above_one_half": all(
            row["ratio_at_equilibrated_full_soft_parameter"] >= .5
            for row in rows),
        "decision": (
            "The metric-soft moment-square direction is not an adverse "
            "lower-frame direction on the checked scales.  The active/full "
            "ratio stays well above one-half both at the curve minimum and "
            "at the diagonal-equilibrated full-soft parameter.  The theorem "
            "target shifts from proving raw support to proving that the "
            "metric-soft moment-square channel remains active-paid."),
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
        "mobius_covariance_theorem_proved": False,
        "uniform_active_full_lower_frame_proved": False,
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

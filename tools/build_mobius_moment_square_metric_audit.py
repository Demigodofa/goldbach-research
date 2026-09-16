"""Build the Mobius metric-aware moment-square support audit."""

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


OUTPUT = Path("evidence/mobius-moment-square-metric-audit.json")
SCALES = (127, 149, 167, 191)


def scale_receipt(scale_modulus):
    frame = project_prime_block_lifted_endpoint_scan(scale_modulus)
    full = np.asarray(frame["aggregate_full_residue_energy_gram"])
    full = (full + full.T) / 2
    raw = moment_square_quadratic_quotient_minimum(full, np.eye(6))
    metric, coordinate_scale = diagonal_equilibration_metric(full)
    equilibrated = moment_square_quadratic_quotient_minimum(full, metric)
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        "raw_moment_square_minimum": raw["minimum_value"],
        "raw_moment_square_parameter": raw["minimizing_parameter"],
        "equilibrated_moment_square_minimum": equilibrated[
            "minimum_value"],
        "equilibrated_moment_square_parameter": equilibrated[
            "minimizing_parameter"],
        "equilibrated_over_raw_minimum": (
            equilibrated["minimum_value"] / raw["minimum_value"]
            if raw["minimum_value"] else float("inf")),
        "full_diagonal_minimum": float(np.min(np.diag(full))),
        "full_diagonal_maximum": float(np.max(np.diag(full))),
        "coordinate_scale_minimum": float(np.min(coordinate_scale)),
        "coordinate_scale_maximum": float(np.max(coordinate_scale)),
    }


def build_receipt():
    rows = [scale_receipt(scale) for scale in SCALES]
    return {
        "status": "TARGET_metric_aware_moment_square_soft_direction",
        "question": (
            "Is moment-square support activation a raw Euclidean support "
            "problem, or does it depend on the diagonal-equilibrated metric "
            "used by the rank-aware lower-frame quotient?"),
        "scales": SCALES,
        "scale_results": rows,
        "maximum_equilibrated_moment_square_minimum": max(
            row["equilibrated_moment_square_minimum"] for row in rows),
        "minimum_raw_moment_square_minimum": min(
            row["raw_moment_square_minimum"] for row in rows),
        "maximum_equilibrated_over_raw_minimum": max(
            row["equilibrated_over_raw_minimum"] for row in rows),
        "equilibrated_parameters": tuple(
            row["equilibrated_moment_square_parameter"] for row in rows),
        "decision": (
            "Moment-square support activation is metric-aware.  The raw "
            "Euclidean moment-square energy is positive on the checked "
            "nonvacuous scales, but the diagonal-equilibrated quotient has "
            "near-null minima throughout.  A proof must control this "
            "equilibrated soft direction, not only raw full-energy support."),
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

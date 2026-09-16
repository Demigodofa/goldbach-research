"""Build the Mobius moment-square nullspace audit."""

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
from mobius_moment_square_nullspace import (  # noqa: E402
    moment_square_projective_fit,
    symmetric_matrix_rank_shape,
)


OUTPUT = Path("evidence/mobius-moment-square-nullspace-audit.json")
SCALE = 167


def _equilibrated_forms(frame):
    active = np.asarray(frame["aggregate_active_window_residue_energy_gram"])
    full = np.asarray(frame["aggregate_full_residue_energy_gram"])
    active = (active + active.T) / 2
    full = (full + full.T) / 2
    diagonal = np.diag(full)
    diagonal_scale = max(float(np.max(diagonal)), 1.0)
    active_diagonal = diagonal > (
        diagonal_scale * np.finfo(float).eps * 100)
    coordinate_scale = np.ones(len(diagonal))
    coordinate_scale[active_diagonal] = (
        diagonal[active_diagonal] ** -.5)
    scaling = np.outer(coordinate_scale, coordinate_scale)
    return active * scaling, full * scaling, coordinate_scale


def build_receipt():
    frame = project_prime_block_lifted_endpoint_scan(SCALE)
    active, full, coordinate_scale = _equilibrated_forms(frame)
    full_values, full_vectors = np.linalg.eigh(full)
    null_vector = full_vectors[:, 0]
    original_null = coordinate_scale * null_vector
    original_null = original_null / float(np.linalg.norm(original_null))
    if original_null[-1] < 0:
        original_null = -original_null
        null_vector = -null_vector

    positive_vectors = full_vectors[:, 1:]
    coupling = positive_vectors.T @ active @ null_vector
    fit = moment_square_projective_fit(original_null)
    shape = symmetric_matrix_rank_shape(original_null)
    return {
        "status": "TARGET_moment_square_nullspace_support_activation",
        "question": (
            "Is the M=167 null-coupling attention point generic nullspace "
            "noise, or does its full-null direction have moment-square "
            "structure?"),
        "scale_modulus": SCALE,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        "full_eigenvalues": tuple(float(value) for value in full_values),
        "equilibrated_full_null_vector": tuple(
            float(value) for value in null_vector),
        "original_coordinate_full_null_vector": tuple(
            float(value) for value in original_null),
        "full_null_energy": float(null_vector @ full @ null_vector),
        "active_null_energy": float(null_vector @ active @ null_vector),
        "active_positive_null_coupling_vector": tuple(
            float(value) for value in coupling),
        "active_positive_null_coupling_norm": float(
            np.linalg.norm(coupling)),
        **fit,
        **shape,
        "decision": (
            "The checked M=167 full-null direction is almost a rank-one "
            "symmetric square on the moment-square curve.  The next theorem "
            "target is not generic nullspace control alone; it should analyze "
            "support activation and coupling near moment-square null "
            "directions."),
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

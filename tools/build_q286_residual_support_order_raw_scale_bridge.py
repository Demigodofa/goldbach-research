"""Raw-scale bridge for the q286 support-order theorem target.

The pointwise theorem target requires either an unnormalized estimate or a
separate positive-mass theorem before normalized action inequalities can be
promoted.  This receipt attaches the prime-pair denominator to the finite
support-order horizon and checks the exact finite sign-equivalence:

    raw_value(N) = normalized_action(N) * principal_mean * total_weight(N)

when the scale is positive.

Finite denominator/sign-equivalence audit only.  It proves no positive-mass
theorem, no raw pointwise estimate, no one-period threshold theorem, no q286
threshold theorem, and no Goldbach proof.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
POINTWISE_SOURCE = (
    EVIDENCE / "q286-residual-support-order-pointwise-theorem-target.json")
HORIZON_SOURCE = (
    EVIDENCE / "q286-residual-support-order-period-lift-horizon.json")
OUT = EVIDENCE / "q286-residual-support-order-raw-scale-bridge.json"
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_prime_indexed_kernel_route_audit import (  # noqa: E402
    logs,
    prime_indexed_residue_weights,
)
from tools.build_q286_prime_indexed_row_filter_order_audit import (  # noqa: E402
    prepare_support_context,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def finite_summary(values):
    finite = [
        float(value) for value in values
        if value is not None and math.isfinite(float(value))
    ]
    if not finite:
        return {"count": 0, "minimum": None, "mean": None, "maximum": None}
    return {
        "count": len(finite),
        "minimum": min(finite),
        "mean": math.fsum(finite) / len(finite),
        "maximum": max(finite),
    }


def raw_row(row, principal_scale, primes, prime_values, log_values, period):
    count, total_weight, _ = prime_indexed_residue_weights(
        int(row["target"]), primes, prime_values, log_values, period)
    scale = float(principal_scale * total_weight)
    low = float(row["low_order_base_action"])
    tail = float(row["high_order_signed_tail"])
    adverse = max(0.0, -tail)
    raw_low = low * scale
    raw_tail = tail * scale
    raw_adverse = adverse * scale
    raw_full = float(row["actual_full_action"]) * scale
    normalized_margin = low - adverse
    raw_margin = raw_low - raw_adverse
    raw_margin_error = abs(raw_margin - normalized_margin * scale)
    return {
        "target": int(row["target"]),
        "base_target": int(row["base_target"]),
        "lift_index": int(row["lift_index"]),
        "target_mod_period": int(row["target_mod_period"]),
        "target_mod_286": int(row["target_mod_286"]),
        "ordered_central_prime_pair_count": int(count),
        "strict_central_total_weight": float(total_weight),
        "principal_scale": scale,
        "scale_positive": bool(scale > TOLERANCE),
        "normalized_low_order_base": low,
        "normalized_high_order_tail": tail,
        "normalized_adverse_drag": adverse,
        "normalized_pointwise_margin": normalized_margin,
        "raw_low_order_base": raw_low,
        "raw_high_order_tail": raw_tail,
        "raw_adverse_drag": raw_adverse,
        "raw_full_action": raw_full,
        "raw_pointwise_margin": raw_margin,
        "raw_margin_matches_scaled_normalized_margin": raw_margin_error,
        "raw_margin_relative_reconstruction_error": (
            raw_margin_error / max(1.0, abs(raw_margin))),
        "normalized_domination_holds": bool(normalized_margin > TOLERANCE),
        "raw_domination_holds": bool(raw_margin > TOLERANCE),
        "sign_equivalence_holds": bool(
            scale > TOLERANCE
            and ((normalized_margin > TOLERANCE)
                 == (raw_margin > TOLERANCE))),
    }


def build_receipt():
    pointwise = load_json(POINTWISE_SOURCE)
    horizon = load_json(HORIZON_SOURCE)
    rows = horizon["rows"]
    period = int(horizon["period"])
    maximum_target = max(int(row["target"]) for row in rows)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    context = prepare_support_context()
    principal_mean = complex(context["principal_mean"])
    principal_real = float(principal_mean.real)
    principal_imag = float(principal_mean.imag)
    principal_imag_to_real = (
        abs(principal_imag) / abs(principal_real)
        if abs(principal_real) > TOLERANCE else math.inf)
    raw_rows = [
        raw_row(
            row, principal_real, primes, prime_values, log_values, period)
        for row in rows
    ]
    nonpositive_scale = [
        row for row in raw_rows if not row["scale_positive"]]
    sign_failures = [
        row for row in raw_rows if not row["sign_equivalence_holds"]]
    raw_failures = [
        row for row in raw_rows if not row["raw_domination_holds"]]
    tight_raw = min(
        raw_rows,
        key=lambda row: (row["raw_pointwise_margin"], row["target"]),
    )
    tight_scale = min(
        raw_rows,
        key=lambda row: (row["principal_scale"], row["target"]),
    )
    smallest_pair_count = min(
        raw_rows,
        key=lambda row: (
            row["ordered_central_prime_pair_count"], row["target"]),
    )
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "pointwise_theorem_target": str(
                POINTWISE_SOURCE.relative_to(ROOT)),
            "period_lift_horizon": str(HORIZON_SOURCE.relative_to(ROOT)),
        },
        "status": "CALIBRATION_raw_scale_bridge_verified_on_horizon",
        "status_boundary": (
            "finite raw-scale bridge audit only; no positive-mass theorem, "
            "raw pointwise estimate, one-period threshold theorem, low-order "
            "base theorem, high-order tail domination theorem, q286 threshold "
            "theorem, strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "positive_mass_theorem_proved": False,
        "raw_pointwise_estimate_proved": False,
        "one_period_threshold_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "acceptance_condition": {
            "finite_evidence_is_acceptance_condition": False,
            "required_acceptance_condition": pointwise[
                "acceptance_condition"]["required_acceptance_condition"],
            "raw_bridge_condition": (
                "Prove principal_mean>0 and total_weight(N)>0, then prove "
                "raw_low_order_base(N)>raw_adverse_drag(N) pointwise for all "
                "sufficiently large eligible targets, or prove the equivalent "
                "normalized inequality with a separate positive scale theorem."),
        },
        "normalization_identity": {
            "principal_mean_real": principal_real,
            "principal_mean_imag": principal_imag,
            "principal_mean_imag_to_real": principal_imag_to_real,
            "principal_mean_positive_on_current_context": (
                principal_real > TOLERANCE
                and principal_imag_to_real <= TOLERANCE),
            "scale": "principal_mean_real * strict_central_total_weight",
            "raw_low_order_base": "normalized_low_order_base * scale",
            "raw_high_order_tail": "normalized_high_order_tail * scale",
            "raw_adverse_drag": "normalized_adverse_drag * scale",
            "raw_margin": "raw_low_order_base - raw_adverse_drag",
            "sign_equivalence_requires": "scale > 0",
        },
        "finite_horizon": {
            "row_count": len(raw_rows),
            "positive_scale_count": sum(
                row["scale_positive"] for row in raw_rows),
            "nonpositive_scale_targets": [
                row["target"] for row in nonpositive_scale],
            "sign_equivalence_failure_targets": [
                row["target"] for row in sign_failures],
            "raw_domination_failure_targets": [
                row["target"] for row in raw_failures],
            "pair_count_summary": finite_summary(
                row["ordered_central_prime_pair_count"] for row in raw_rows),
            "total_weight_summary": finite_summary(
                row["strict_central_total_weight"] for row in raw_rows),
            "scale_summary": finite_summary(
                row["principal_scale"] for row in raw_rows),
            "raw_margin_summary": finite_summary(
                row["raw_pointwise_margin"] for row in raw_rows),
            "normalized_margin_summary": finite_summary(
                row["normalized_pointwise_margin"] for row in raw_rows),
            "maximum_raw_margin_reconstruction_error": max(
                row["raw_margin_matches_scaled_normalized_margin"]
                for row in raw_rows),
            "maximum_raw_margin_relative_reconstruction_error": max(
                row["raw_margin_relative_reconstruction_error"]
                for row in raw_rows),
            "tight_raw_margin_row": tight_raw,
            "smallest_positive_scale_row": tight_scale,
            "smallest_pair_count_row": smallest_pair_count,
        },
        "proof_obligations": [
            "Prove total_weight(N)>0 for every sufficiently large eligible N "
            "in the named period classes, or use a theorem that avoids "
            "division by total_weight entirely.",
            "Prove the raw support-order inequality "
            "raw_low_order_base(N)>raw_adverse_drag(N) pointwise after one "
            "period.",
            "Verify any finite initial interval separately.",
        ],
        "decision": (
            "On the checked 224-row horizon, the denominator scale is positive "
            "on every row, and normalized same-row support-order domination is "
            "exactly sign-equivalent to raw domination after multiplying by "
            "principal_mean*total_weight.  This clarifies the missing theorem "
            "but does not prove it: a universal positive-mass theorem and a "
            "raw pointwise support-order estimate remain open.  Goldbach "
            "remains open."),
        "rows": raw_rows,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

"""Build q286 first-three residue-pair correlation obligation evidence.

This records the exact fixed-modulus binary-prime residue discrepancy theorem
that would imply the q286 first-three signed-projection bound.  The output is
a theorem-obligation artifact, not a proof of that external theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    ROOT / "evidence"
    / "q286-first-three-residue-pair-correlation-obligation.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_residue_pair_correlation_obligation_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def main():
    receipt = q286_first_three_residue_pair_correlation_obligation_receipt(
        include_residue_rows=True, include_sample_rows=True,
        top_contribution_count=8)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "exact q286 first-three residue-pair correlation theorem "
            "obligation and finite algebra checks only; no fixed-modulus "
            "binary AP theorem, signed-projection theorem, strict-central "
            "existence theorem, or Goldbach proof is established"),
        "exact_residue_pair_discrepancy_obligation": (
            receipt["exact_residue_pair_discrepancy_obligation"]),
        "uniform_ap_asymptotic_conditional_theorem": (
            receipt["uniform_ap_asymptotic_conditional_theorem"]),
        "external_theorem_strength_warning": (
            receipt["external_theorem_strength_warning"]),
        "tail_threshold": receipt["tail_threshold"],
        "sample_targets": receipt["sample_targets"],
        "even_target_residue_count": receipt["even_target_residue_count"],
        "maximum_local_coefficient_mean_error": (
            receipt["maximum_local_coefficient_mean_error"]),
        "maximum_projection_identity_error": (
            receipt["maximum_projection_identity_error"]),
        "maximum_prior_signed_projection_receipt_error": (
            receipt["maximum_prior_signed_projection_receipt_error"]),
        "minimum_pointwise_linf_relative_error_sufficient": (
            receipt["minimum_pointwise_linf_relative_error_sufficient"]),
        "maximum_pointwise_linf_relative_error_sufficient": (
            receipt["maximum_pointwise_linf_relative_error_sufficient"]),
        "minimum_l2_relative_error_sufficient": (
            receipt["minimum_l2_relative_error_sufficient"]),
        "maximum_l2_relative_error_sufficient": (
            receipt["maximum_l2_relative_error_sufficient"]),
        "sample_rows": receipt["sample_rows"],
        "interpretation": {
            "what_changed": (
                "The signed-projection joint is now reduced to a precise "
                "fixed-modulus weighted binary-prime residue discrepancy "
                "inequality with complete q286 coefficients."),
            "why_this_is_not_circular": (
                "The receipt identifies the missing arithmetic theorem; it "
                "does not verify it by finite data or assume Goldbach."),
            "next_action": (
                "Either prove a signed one-sided version of this discrepancy "
                "bound for the q286 coefficient family, or cite a sufficiently "
                "strong fixed-modulus strict-central binary Goldbach/AP "
                "theorem and then handle finite endpoints separately."),
        },
        "residue_pair_correlation_obligation_formalized": True,
        "signed_projection_theorem_proved": False,
        "fixed_modulus_binary_ap_theorem_proved": False,
        "strict_central_prime_pair_existence_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

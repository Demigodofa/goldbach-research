"""Build the q286 first-three mass/landing theorem-obligation receipt.

This records the exact algebraic target suggested by the mass-matched pair
decomposition:

    m_plus(N) * ell_plus(N) + tau >= m_minus(N) * ell_minus(N)

for the actual strict-central binary-prime residue weights.  The output is a
proof-obligation artifact, not a proof of the inequality.
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
    / "q286-first-three-mass-landing-obligation.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_mass_landing_obligation_receipt,
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
    receipt = q286_first_three_mass_landing_obligation_receipt()
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "exact q286 first-three mass/landing proof obligation with finite "
            "sample rows; no mass/landing inequality, exact-curve theorem, "
            "signed prime-correlation estimate, or Goldbach proof is "
            "established"),
        "exact_pointwise_obligation": receipt["exact_pointwise_obligation"],
        "missing_arithmetic_input": receipt["missing_arithmetic_input"],
        "tail_threshold": receipt["tail_threshold"],
        "near_window": receipt["near_window"],
        "sample_windows": receipt["sample_windows"],
        "sample_targets": receipt["sample_targets"],
        "missing_sample_targets": receipt["missing_sample_targets"],
        "sample_window_summaries": receipt["sample_window_summaries"],
        "even_target_residue_count": receipt["even_target_residue_count"],
        "sign_count_histogram": receipt["sign_count_histogram"],
        "sample_rows": receipt["sample_rows"],
        "maximum_mass_landing_reconstruction_error": (
            receipt["maximum_mass_landing_reconstruction_error"]),
        "maximum_threshold_slack_identity_error": (
            receipt["maximum_threshold_slack_identity_error"]),
        "interpretation": {
            "changed_under_evidence": (
                "The mass-matched pair decomposition demoted scalar "
                "positive-mass thresholds.  The remaining exact first-three "
                "rarity target is a pointwise inequality coupling mass "
                "allocation and landing quality."),
            "proof_pressure": (
                "A proof must constrain actual binary-prime residue weights "
                "on q286 reflection-orbit sign classes; the recorded algebra "
                "is necessary bookkeeping, not an analytic estimate."),
        },
        "mass_landing_obligation_formalized": True,
        "mass_landing_inequality_proved": False,
        "eventual_exact_curve_theorem_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

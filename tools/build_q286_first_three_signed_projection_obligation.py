"""Build q286 first-three signed-projection obligation evidence.

Generic orbit uniformity is sufficient but too blunt.  This receipt records
the sharper backward theorem target:

    <mu_N - u_a, c_a> >= -tau

or, in cosine form, a lower bound on anti-alignment with the q286
first-three coefficient vector.  The output is a theorem-obligation and
finite stress artifact, not a proof of the signed projection estimate.
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
    / "q286-first-three-signed-projection-obligation.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_signed_projection_obligation_receipt,
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
    receipt = q286_first_three_signed_projection_obligation_receipt()
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "coefficient-sensitive signed-projection theorem obligation and "
            "finite sample stress only; no signed-projection theorem, "
            "mass/landing inequality, signed prime-correlation estimate, or "
            "Goldbach proof is established"),
        "signed_projection_conditional_theorem": (
            receipt["signed_projection_conditional_theorem"]),
        "tail_threshold": receipt["tail_threshold"],
        "sample_targets": receipt["sample_targets"],
        "signed_projection_failure_targets": (
            receipt["signed_projection_failure_targets"]),
        "generic_uniformity_fail_signed_projection_pass_targets": (
            receipt[
                "generic_uniformity_fail_signed_projection_pass_targets"]),
        "maximum_projection_identity_error": (
            receipt["maximum_projection_identity_error"]),
        "sample_rows": receipt["sample_rows"],
        "interpretation": {
            "backward_theorem": (
                "The exact weaker theorem after the failed generic "
                "uniformity route is a lower bound on the signed projection "
                "of the actual orbit-mass deviation onto the q286 coefficient "
                "vector."),
            "sample_stress": (
                "The clear holdout rows fail generic L1/L2 uniformity "
                "certificates but pass the signed-projection condition, so "
                "large deviation is acceptable when mostly orthogonal or "
                "favorably aligned."),
        },
        "signed_projection_is_weaker_than_generic_uniformity_on_samples": (
            receipt[
                "signed_projection_is_weaker_than_generic_uniformity_on_samples"]),
        "signed_projection_obligation_measured": True,
        "signed_projection_theorem_proved": False,
        "mass_landing_inequality_proved": False,
        "signed_prime_correlation_estimate_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

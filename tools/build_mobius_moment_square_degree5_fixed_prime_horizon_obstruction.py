"""Audit why fixed-prime stress diagnostics cannot be theorem targets.

The source-start morphology now has a persistent finite diagnostic: p=599 is
the weakest prime for M=331,353,379,383.  This receipt records the elementary
arithmetic obstruction to promoting any fixed prime p0 into a sufficiently-large
source-start theorem target: p0 belongs to the interval [M,2M] only for
ceil(p0/2) <= M <= p0.
"""

from __future__ import annotations

import json
import math
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (
    Path("evidence")
    / "mobius-moment-square-degree5-source-start-stress-morphology-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-fixed-prime-horizon-obstruction.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def admissible_scale_range_for_fixed_prime(prime):
    return {
        "prime_modulus": prime,
        "minimum_integer_scale_M": math.ceil(prime / 2),
        "maximum_integer_scale_M": prime,
        "integer_scale_count": prime - math.ceil(prime / 2) + 1,
        "first_impossible_integer_scale_M": prime + 1,
        "admissibility_condition": "ceil(p/2) <= M <= p",
        "calculation": (
            f"For fixed p={prime}, p in [M,2M] iff M <= {prime} <= 2M, "
            f"equivalently ceil({prime}/2)={math.ceil(prime / 2)} <= M "
            f"<= {prime}.  For every M >= {prime + 1}, p={prime} is outside "
            "the source-start prime interval.")
    }


def build_receipt():
    morphology = json.loads(SOURCE.read_text(encoding="utf-8"))
    weakest_sequence = morphology["weakest_sequence"]
    weakest_primes = [
        row["weakest_prime_modulus"] for row in weakest_sequence]
    prime_counts = Counter(weakest_primes)
    fixed_prime_horizons = {
        str(prime): admissible_scale_range_for_fixed_prime(prime)
        for prime in sorted(prime_counts)
    }
    p599_observations = [
        row for row in weakest_sequence
        if row["weakest_prime_modulus"] == 599
    ]
    p599_horizon = fixed_prime_horizons["599"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_degree5_fixed_prime_horizon_obstruction",
        "source_morphology_audit": str(SOURCE),
        "question": (
            "Can the persistent finite p=599 stress diagnostic be promoted "
            "into a fixed-prime theorem target for all sufficiently large "
            "source scales M?"),
        "answer": "NO",
        "weakest_sequence": weakest_sequence,
        "weakest_prime_counts": dict(prime_counts),
        "fixed_prime_horizons": fixed_prime_horizons,
        "p599_observed_weak_scales": [
            row["scale_modulus"] for row in p599_observations],
        "p599_observed_scale_span": [
            min(row["scale_modulus"] for row in p599_observations),
            max(row["scale_modulus"] for row in p599_observations),
        ],
        "p599_integer_admissible_scale_span": [
            p599_horizon["minimum_integer_scale_M"],
            p599_horizon["maximum_integer_scale_M"],
        ],
        "p599_first_impossible_integer_scale_M": (
            p599_horizon["first_impossible_integer_scale_M"]),
        "fixed_prime_universal_target_obstructed": True,
        "elementary_interval_obstruction_proved": True,
        "candidate_replacement_theorem_target": {
            "name": "moving source-start prime-block lower-frame control",
            "mechanism": (
                "Prove source-start dominance for every prime block p in "
                "[M,2M], or prove existence/control of a moving stress block "
                "p=p(M), instead of tracking one fixed prime."),
            "prediction": (
                "The persistent p=599 block can remain diagnostic only while "
                "M <= 599.  Any sufficiently-large theorem must either move "
                "the stress prime with M or control all prime blocks."),
            "falsifier": (
                "A proposed fixed-prime theorem target is false as a "
                "sufficiently-large statement once M exceeds that prime."),
            "novelty_label": "new-to-this-task",
        },
        "decision": (
            "The p=599 persistence is useful finite morphology but cannot be "
            "a universal fixed-prime theorem target: p=599 is admissible only "
            "for integer scales 300..599 and is impossible for every M>=600.  "
            "The live target must be moving prime-block control or all-prime-"
            "block control."),
        "finite_morphology_input_only": True,
        "goldbach_proved": False,
        "source_start_theorem_proved": False,
        "prime_block_theorem_proved": False,
        "fixed_prime_stress_theorem_proved": False,
        "moving_prime_block_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
    }


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()

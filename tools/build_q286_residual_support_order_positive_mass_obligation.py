"""Classify the positive-mass obligation in the support-order route.

The raw-scale bridge showed that normalized domination transfers to raw scale
when principal_mean * total_weight(N) is positive.  This receipt makes the
denominator theorem explicit: total_weight(N)>0 is equivalent to existence of
at least one strict-central prime pair in the checked window, because every
summand log(p)log(N-p) is positive.

Logical/theorem-obligation audit only.  It proves no positive-mass theorem,
raw pointwise estimate, one-period threshold theorem, q286 threshold theorem,
or Goldbach proof.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
RAW_SCALE_SOURCE = (
    EVIDENCE / "q286-residual-support-order-raw-scale-bridge.json")
OUT = (
    EVIDENCE
    / "q286-residual-support-order-positive-mass-obligation.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def finite_summary(values):
    values = [float(value) for value in values]
    return {
        "count": len(values),
        "minimum": min(values),
        "mean": sum(values) / len(values),
        "maximum": max(values),
    }


def build_receipt():
    raw = load_json(RAW_SCALE_SOURCE)
    rows = raw["rows"]
    zero_pair_rows = [
        row for row in rows
        if int(row["ordered_central_prime_pair_count"]) == 0]
    zero_weight_rows = [
        row for row in rows
        if float(row["strict_central_total_weight"]) <= 0.0]
    positive_weight_zero_pair_rows = [
        row for row in rows
        if (float(row["strict_central_total_weight"]) > 0.0
            and int(row["ordered_central_prime_pair_count"]) == 0)]
    positive_pair_zero_weight_rows = [
        row for row in rows
        if (int(row["ordered_central_prime_pair_count"]) > 0
            and float(row["strict_central_total_weight"]) <= 0.0)]
    smallest_pair_count = min(
        rows,
        key=lambda row: (
            int(row["ordered_central_prime_pair_count"]), int(row["target"])),
    )
    smallest_weight = min(
        rows,
        key=lambda row: (
            float(row["strict_central_total_weight"]), int(row["target"])),
    )
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "raw_scale_bridge": str(RAW_SCALE_SOURCE.relative_to(ROOT)),
        },
        "status": "TARGET_positive_mass_is_strict_central_existence_obligation",
        "status_boundary": (
            "logical positive-mass obligation audit only; no positive-mass "
            "theorem, raw pointwise estimate, one-period threshold theorem, "
            "low-order base theorem, high-order tail domination theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof"),
        "goldbach_proved": False,
        "positive_mass_theorem_proved": False,
        "strict_central_existence_theorem_proved": False,
        "raw_pointwise_estimate_proved": False,
        "one_period_threshold_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "theorem_obligation": {
            "positive_mass_statement": (
                "For every sufficiently large eligible N in the named period "
                "classes, strict_central_total_weight(N)>0."),
            "expanded_weight": (
                "strict_central_total_weight(N) = sum log(p)log(N-p) over "
                "strict-central prime pairs N/3 < p < 2N/3."),
            "equivalence": (
                "Because every summand log(p)log(N-p) is positive, "
                "strict_central_total_weight(N)>0 if and only if at least one "
                "strict-central prime pair exists for N."),
            "interpretation": (
                "The denominator condition is a strict-central Goldbach-in-"
                "window existence theorem for the named classes, not a cheap "
                "normalization lemma."),
        },
        "finite_calibration": {
            "row_count": len(rows),
            "positive_pair_count_rows": len(rows) - len(zero_pair_rows),
            "zero_pair_count_targets": [
                int(row["target"]) for row in zero_pair_rows],
            "positive_total_weight_rows": len(rows) - len(zero_weight_rows),
            "zero_or_negative_weight_targets": [
                int(row["target"]) for row in zero_weight_rows],
            "positive_weight_zero_pair_count_targets": [
                int(row["target"])
                for row in positive_weight_zero_pair_rows],
            "positive_pair_zero_weight_targets": [
                int(row["target"])
                for row in positive_pair_zero_weight_rows],
            "pair_count_summary": finite_summary(
                row["ordered_central_prime_pair_count"] for row in rows),
            "total_weight_summary": raw["finite_horizon"][
                "total_weight_summary"],
            "smallest_pair_count_row": {
                "target": int(smallest_pair_count["target"]),
                "ordered_central_prime_pair_count": int(
                    smallest_pair_count["ordered_central_prime_pair_count"]),
                "strict_central_total_weight": float(
                    smallest_pair_count["strict_central_total_weight"]),
            },
            "smallest_total_weight_row": {
                "target": int(smallest_weight["target"]),
                "ordered_central_prime_pair_count": int(
                    smallest_weight["ordered_central_prime_pair_count"]),
                "strict_central_total_weight": float(
                    smallest_weight["strict_central_total_weight"]),
            },
        },
        "route_decision": {
            "separate_positive_mass_lemma_is_goldbach_strength": True,
            "raw_inequality_route_avoids_normalized_division": True,
            "raw_inequality_route_still_implies_positive_mass_when_strict": (
                "A strict positive raw support-order witness cannot be "
                "produced from an empty strict-central pair set; if no pair "
                "exists, all raw prime-pair sums in this witness vanish."),
            "recommended_next_theorem_shape": (
                "Do not try to pay the denominator as a minor side condition. "
                "Either prove a single raw lower-bound theorem that already "
                "implies positive strict-central mass, or explicitly treat "
                "positive mass as the strict-central existence half of the "
                "problem."),
        },
        "decision": (
            "The positive-mass obligation is now classified.  On the checked "
            "224-row horizon, every row has at least one strict-central prime "
            "pair and positive total weight, with the minimum pair count 106 "
            "at target 24148.  Universally, however, total_weight(N)>0 is "
            "equivalent to strict-central prime-pair existence in the window, "
            "so it is not a solved denominator technicality.  Goldbach remains "
            "open."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

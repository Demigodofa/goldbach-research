"""Build q286 residue-pair character-mode narrowing evidence.

The residue-pair obligation asks for a one-sided projection against
``gamma_a``.  This receipt reuses the existing q286 first-three character
mixture and singular-mode coordinate diagnostics on the current near-boundary
sample rows.  It asks whether the obligation is plausibly narrower than full
fixed-modulus AP Goldbach.

The output is finite theorem-shaping evidence only.
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
    / "q286-residue-pair-character-mode-narrowing.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_character_mixture_norm_receipt,
    q286_first_three_character_mode_coordinate_receipt,
)


SAMPLE_TARGETS = (1222142, 1242118, 1240888)


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
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def compact_mixture_row(row):
    return {
        "target": row["target"],
        "target_mod_286": row["target_mod_286"],
        "first_three_to_principal_ratio": (
            row["first_three_to_principal_ratio"]),
        "triangle_character_bound_to_principal": (
            row["triangle_character_bound_to_principal"]),
        "vector_l2_character_bound_to_principal": (
            row["vector_l2_character_bound_to_principal"]),
        "triangle_to_sufficient_ratio": row["triangle_to_sufficient_ratio"],
        "vector_l2_to_sufficient_ratio": row[
            "vector_l2_to_sufficient_ratio"],
        "first_three_reconstruction_error": (
            row["first_three_reconstruction_error"]),
    }


def compact_mode_row(row):
    return {
        "target": row["target"],
        "target_mod_286": row["target_mod_286"],
        "first_three_to_principal_ratio": (
            row["first_three_to_principal_ratio"]),
        "mode_contribution_absolute_sum_to_principal": (
            row["mode_contribution_absolute_sum_to_principal"]),
        "signed_to_absolute_mode_contribution_ratio": (
            row["signed_to_absolute_mode_contribution_ratio"]),
        "dominant_mode_absolute_fraction": (
            row["dominant_mode_absolute_fraction"]),
        "mode_rows": tuple({
            "mode_index": mode["mode_index"],
            "singular_value": mode["singular_value"],
            "contribution_to_principal_ratio": (
                mode["contribution_to_principal_ratio"]),
            "absolute_contribution_to_principal_ratio": (
                mode["absolute_contribution_to_principal_ratio"]),
        } for mode in row["mode_rows"]),
        "mode_reconstruction_error": row["mode_reconstruction_error"],
    }


def main():
    mixture = q286_first_three_character_mixture_norm_receipt(
        targets=SAMPLE_TARGETS, theorem_threshold=.3)
    modes = q286_first_three_character_mode_coordinate_receipt(
        targets=SAMPLE_TARGETS)

    mode_rows = {
        str(target): compact_mode_row(row)
        for target, row in sorted(modes["rows"].items())
    }
    same_sign_mode_target_count = sum(
        1 for row in mode_rows.values()
        if abs(row["signed_to_absolute_mode_contribution_ratio"]) > .99)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite character-mode narrowing evidence only; no pointwise "
            "character-sum estimate, fixed-modulus AP theorem, q286 "
            "signed-projection theorem, or Goldbach proof is established"),
        "sample_targets": SAMPLE_TARGETS,
        "character_product_count": mixture["character_product_count"],
        "rank_three_singular_values": modes["first_three_singular_values"],
        "character_coefficient_l1_to_principal_mean": (
            mixture["character_coefficient_l1_to_principal_mean"]),
        "character_coefficient_l2_to_principal_mean": (
            mixture["character_coefficient_l2_to_principal_mean"]),
        "character_coefficient_linf_to_principal_mean": (
            mixture["character_coefficient_linf_to_principal_mean"]),
        "mixture_rows": {
            str(target): compact_mixture_row(row)
            for target, row in sorted(mixture["rows"].items())
        },
        "mode_rows": mode_rows,
        "same_sign_mode_target_count": same_sign_mode_target_count,
        "all_sample_rows_same_sign_by_rank_three_modes": (
            same_sign_mode_target_count == len(SAMPLE_TARGETS)),
        "interpretation": {
            "narrowing_result": (
                "The q286 gamma projection is broad in the underlying "
                "99-character product space, but the tested near-boundary "
                "rows are carried by the first three singular coordinates."),
            "pressure_result": (
                "The tested near-boundary rows have almost no cancellation "
                "among the rank-three mode contributions; mode contributions "
                "are same-sign negative up to tiny positive leakage."),
            "route_effect": (
                "This does not produce a proof, but it narrows the next "
                "theorem question: prove a one-sided lower bound for the "
                "three singular character coordinates, especially the first "
                "two dominant modes, or record that those coordinates require "
                "full pointwise binary-prime AP control."),
        },
        "pointwise_character_sum_estimate_proved": False,
        "fixed_modulus_binary_ap_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }

    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

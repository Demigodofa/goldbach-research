"""Build a rank-aware Mobius active/full lower-frame obligation receipt."""

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
from mobius_rank_aware_lower_frame import (  # noqa: E402
    rank_aware_lower_frame_receipt,
)


OUTPUT = Path("evidence/mobius-rank-aware-lower-frame-obligation.json")
SCALES = (83, 101, 127, 149, 167, 191)


def scale_receipt(scale_modulus):
    frame = project_prime_block_lifted_endpoint_scan(scale_modulus)
    active = np.asarray(frame["aggregate_active_window_residue_energy_gram"])
    full = np.asarray(frame["aggregate_full_residue_energy_gram"])
    receipt = rank_aware_lower_frame_receipt(active, full)
    return {
        "scale_modulus": scale_modulus,
        "prime_count": frame["prime_count"],
        "row_count": frame["row_count"],
        "divisor_range": frame["divisor_range"],
        **receipt,
    }


def build_receipt():
    rows = [scale_receipt(scale) for scale in SCALES]
    nonvacuous = [row for row in rows if row["positive_range_nonvacuous"]]
    certified = [
        row for row in nonvacuous
        if row[
            "one_half_lower_frame_certified_with_null_coupling_tolerance"]]
    quotient_above_target = [
        row for row in nonvacuous
        if row["quotient_minimum_exceeds_target"]]
    null_coupling_attention = [
        row for row in nonvacuous
        if (row["quotient_minimum_exceeds_target"]
            and not row[
                "one_half_lower_frame_certified_with_null_coupling_tolerance"])]
    rank_deficient = [
        row for row in nonvacuous if row["full_nullity"] > 0]
    return {
        "status": (
            "TARGET_rank_aware_positive_range_lower_frame_plus_"
            "support_activation"),
        "question": (
            "After axial compression failed, what is the exact finite "
            "linear-algebra theorem obligation for the Mobius active/full "
            "lower-frame route?"),
        "scales": SCALES,
        "scale_results": rows,
        "nonvacuous_scales": tuple(
            row["scale_modulus"] for row in nonvacuous),
        "vacuous_pre_support_scales": tuple(
            row["scale_modulus"] for row in rows
            if not row["positive_range_nonvacuous"]),
        "rank_deficient_nonvacuous_scales": tuple(
            row["scale_modulus"] for row in rank_deficient),
        "quotient_above_one_half_nonvacuous_scales": tuple(
            row["scale_modulus"] for row in quotient_above_target),
        "one_half_certified_nonvacuous_scales": tuple(
            row["scale_modulus"] for row in certified),
        "null_coupling_attention_scales": tuple(
            row["scale_modulus"] for row in null_coupling_attention),
        "minimum_checked_quotient_eigenvalue": min(
            row["schur_minimized_positive_range_minimum"]
            for row in nonvacuous),
        "minimum_raw_positive_range_eigenvalue": min(
            row["raw_positive_range_minimum"] for row in nonvacuous),
        "maximum_null_coupling_to_active_null_norm": max(
            row["null_coupling_to_active_null_norm"] for row in rows),
        "maximum_full_null_active_eigenvalue": max(
            row["full_null_active_maximum"] for row in rows),
        "one_half_survives_checked_nonvacuous_quotient_minima": (
            len(quotient_above_target) == len(nonvacuous)),
        "one_half_fully_certified_with_null_coupling_tolerance": (
            len(certified) == len(nonvacuous)),
        "theorem_obligation": (
            "Prove eventual support activation of the full Gram, prove any "
            "full-null directions and their active coupling are harmless, "
            "and prove a positive-range Schur-minimized quotient lower bound "
            "at least 1/2.  This is the rank-aware replacement for full-PD "
            "whitening."
        ),
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

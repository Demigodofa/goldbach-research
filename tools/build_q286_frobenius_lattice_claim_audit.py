"""Audit the pasted Frobenius/common-divisor explanation for q286 rank-1.

Kevin pasted a candidate claiming that the q286 rank-1 direction is forced by
Frobenius coin structure, gcd(17, 120), parity, and ray-class/unit-group
language.  This builder records the checkable arithmetic parts and separates
them from unsupported or false implications.

This is a finite claim audit only.  It proves no replacement explanation,
rank-1 theorem, residual-drag theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DICTIONARY_SOURCE = ROOT / "evidence" / "q286-lift-project-dictionary-audit.json"
RANK1_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-octave-rank1-audit.json")
OUT = ROOT / "evidence" / "q286-frobenius-lattice-claim-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def label_tuple(label):
    return tuple(int(part) for part in label)


def frobenius_number(a, b):
    if math.gcd(a, b) != 1:
        return None
    return a * b - a - b


def dictionary_row(payload, row_id):
    matches = [row for row in payload["dictionary_rows"] if row["id"] == row_id]
    if len(matches) != 1:
        raise AssertionError(f"missing dictionary row {row_id}")
    return matches[0]


def main():
    dictionary_payload = json.loads(
        DICTIONARY_SOURCE.read_text(encoding="utf-8"))
    rank1_payload = json.loads(RANK1_SOURCE.read_text(encoding="utf-8"))
    outside_labels = tuple(
        label_tuple(label) for label in dictionary_payload["outside_labels"])
    volatile_labels = tuple(
        label_tuple(label)
        for label in rank1_payload["volatile_labels_removed"])

    all_25_labels = outside_labels + volatile_labels
    outside_even = tuple(label for label in outside_labels
                         if (label[0] + label[1]) % 2 == 0)
    volatile_even = tuple(label for label in volatile_labels
                          if (label[0] + label[1]) % 2 == 0)
    all_even = tuple(label for label in all_25_labels
                     if (label[0] + label[1]) % 2 == 0)

    constant = dictionary_row(dictionary_payload, "constant_sum")
    edge_parity = dictionary_row(dictionary_payload, "edge_and_parity_lift")
    gemini = dictionary_row(dictionary_payload, "gemini_legendre_product_sign")
    claude_diag = dictionary_payload["claude_order_weight_diagnostic"]

    claimed_formula_value = 286 * (1 / 2 - 1 / 17)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_lift_project_dictionary_audit": str(
            DICTIONARY_SOURCE.relative_to(ROOT)),
        "source_octave_rank1_audit": str(RANK1_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite audit of a pasted Frobenius/common-divisor rank-1 claim "
            "only; this proves no replacement rank-1 explanation, "
            "residual-drag theorem, signed projection theorem, or Goldbach "
            "theorem."),
        "candidate_source": "manual external-model style claim pasted by Kevin",
        "candidate_claim_summary": (
            "The q286 rank-1 direction is claimed to be mathematically forced "
            "by a Frobenius coin/lattice common-divisor structure, gcd(17,120), "
            "and a parity/conjugacy axis on C10 x C12."),
        "accepted_arithmetic_parts": {
            "q": 286,
            "factorization": [2, 11, 13],
            "phi_q": 120,
            "unit_group_structure": "C10 x C12, with the mod-2 unit factor trivial",
            "outside_label_count": len(outside_labels),
            "volatile_label_count": len(volatile_labels),
        },
        "frobenius_claim_check": {
            "claim_value_q_times_half_minus_inverse_17": claimed_formula_value,
            "claim_value_rounded": round(claimed_formula_value),
            "valid_frobenius_input_requires_two_or_more_coprime_denominations": True,
            "frobenius_number_for_denominations_2_and_17": frobenius_number(2, 17),
            "frobenius_number_for_denominations_17_and_286": frobenius_number(17, 286),
            "frobenius_number_for_single_denominator_286": None,
            "claim_formula_is_standard_two_coin_frobenius_number": False,
            "frobenius_formula_supports_q286_rank1_direction": False,
        },
        "label_semantics_check": {
            "outside_labels_are_residue_classes_mod_286": False,
            "actual_role": (
                "The 17 labels are folded real Dirichlet-character channel "
                "labels from the q286 dominant-mode outside-channel audit, "
                "not a complete set of residue classes modulo 286."),
            "unit_residue_class_count_mod_286": 120,
            "active_real_channel_count_in_rank1_source": (
                rank1_payload.get("active_real_channel_count")),
            "outside_labels": outside_labels,
            "volatile_labels_removed": volatile_labels,
        },
        "parity_axis_check": {
            "outside_even_parity_count": len(outside_even),
            "volatile_even_parity_count": len(volatile_even),
            "all_25_even_parity_count": len(all_even),
            "outside_all_even_parity": len(outside_even) == len(outside_labels),
            "volatile_all_even_parity": (
                len(volatile_even) == len(volatile_labels)),
            "parity_separates_outside_from_volatile": False,
            "constant_sum_rank1_cosine": constant["rank1_direction_cosine"],
            "edge_and_parity_lift_rank1_cosine": (
                edge_parity["rank1_direction_cosine"]),
            "gemini_legendre_sign_rank1_cosine": (
                gemini["rank1_direction_cosine"]),
            "gemini_legendre_sign_mismatches": 11,
            "parity_axis_forces_rank1_direction": False,
        },
        "gcd_rank_claim_check": {
            "gcd_17_120": math.gcd(17, 120),
            "coprime_count_to_group_order": True,
            "coprimality_implies_one_dimensional_projection": False,
            "reason": (
                "gcd(17,120)=1 says the selected count has no common divisor "
                "with the character-group order.  It supplies no linear map, "
                "no coefficient vector, and no theorem forcing a singular "
                "vector or a one-dimensional projection on the chosen labels."),
        },
        "ray_class_unit_claim_check": {
            "cyclotomic_field_degree_phi_286": 120,
            "unit_rank_for_Q_zeta_286": 59,
            "unit_rank_note": (
                "For a cyclotomic field with phi(286)=120 and no real "
                "embeddings, Dirichlet unit rank is r1+r2-1=0+60-1=59, "
                "not 119."),
            "unit_group_rank_forces_observed_17_channel_rank1": False,
        },
        "related_prior_numeric_falsifiers": {
            "constant_sum": {
                "rank1_direction_cosine": (
                    constant["rank1_direction_cosine"]),
                "high_drag_overlap_count_at_reference_k": (
                    constant["high_drag_overlap_count_at_reference_k"]),
                "cap_failure_count": constant["cap_failure_count"],
            },
            "edge_and_parity_lift": {
                "rank1_direction_cosine": (
                    edge_parity["rank1_direction_cosine"]),
                "high_drag_overlap_count_at_reference_k": (
                    edge_parity["high_drag_overlap_count_at_reference_k"]),
                "cap_failure_count": edge_parity["cap_failure_count"],
            },
            "gemini_legendre_product_sign": {
                "rank1_direction_cosine": gemini["rank1_direction_cosine"],
                "high_drag_overlap_count_at_reference_k": (
                    gemini["high_drag_overlap_count_at_reference_k"]),
                "cap_failure_count": gemini["cap_failure_count"],
                "nonpositive_delta_count": (
                    gemini["nonpositive_dictionary_delta_count"]),
            },
            "claude_order_weight": {
                "outside_all_even_parity": (
                    claude_diag["outside_all_even_parity"]),
                "volatile_all_even_parity": (
                    claude_diag["volatile_all_even_parity"]),
                "spearman_rank1_vs_order_weight": (
                    claude_diag["spearman_rank1_vs_order_weight"]),
                "pearson_rank1_vs_order_weight": (
                    claude_diag["pearson_rank1_vs_order_weight"]),
            },
        },
        "decision": (
            "Reject the Frobenius/common-divisor/parity explanation as stated. "
            "The true C10 x C12 character-lattice setting remains relevant, "
            "but these claims do not produce a non-post-hoc rank-1 vector or "
            "a proof of the residual-drag cap."),
        "next_action": (
            "Preserve low-frequency label-lattice structure as finite evidence, "
            "but require actual character-sum magnitudes, row-dependent signed "
            "cones, or a stronger signed aggregate theorem for any promoted "
            "rank-1 explanation."),
        "frobenius_lattice_claim_audit_measured": True,
        "frobenius_lattice_rank1_claim_accepted": False,
        "low_frequency_lift_theorem_proved": False,
        "rank1_residual_bound_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

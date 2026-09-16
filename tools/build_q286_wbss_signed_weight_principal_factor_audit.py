"""Classify the principal local factor of the q286 signed-weight target.

The signed-weight circle target asks whether q286 can supply a raw positive
major-arc term, not merely a conditional normalized distribution statement.
This receipt checks the principal local-factor algebra for the combined
single weight Phi_a.

Conclusion preview: the principal term factors as ordinary strict-central
mass times a positive local q286 mean M(a).  That is a useful target, but not
an independent source of strict-central support.  Any proof using only this
principal factor still needs a raw circle-method estimate for the weighted
sum, or else it collapses to positive mass plus conditional q286 decoration.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SIGNED_TARGET = EVIDENCE / "q286-wbss-signed-weight-circle-target.json"
RAW_CIRCLE = EVIDENCE / "q286-wbss-raw-character-circle-decomposition.json"
FLOOR = EVIDENCE / "q286-wbss-single-weight-major-arc-floor-audit.json"
NEGATIVE = EVIDENCE / "q286-wbss-negative-region-mass-threshold-audit.json"
L2_LOGICAL = EVIDENCE / "q286-wbss-zero-mass-l2-logical-bridge-audit.json"
OUT = EVIDENCE / "q286-wbss-signed-weight-principal-factor-audit.json"

sys.path.insert(0, str(ROOT))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def finite_summary(values):
    items = [float(value) for value in values]
    return {
        "minimum": min(items),
        "mean": sum(items) / len(items),
        "maximum": max(items),
    }


def build_rows():
    from tools.build_q286_wbss_negative_region_mass_threshold_audit import (  # noqa: E501
        build_rows as build_negative_rows,
    )

    _principal, _units, _phi, rows = build_negative_rows()
    return rows


def build_receipt():
    signed = load_json(SIGNED_TARGET)
    circle = load_json(RAW_CIRCLE)
    floor = load_json(FLOOR)
    negative = load_json(NEGATIVE)
    l2_logical = load_json(L2_LOGICAL)
    rows = build_rows()

    local_factors = [
        row["local_uniform_expectation"]
        for row in rows
    ]
    local_factor_minus_one = [
        row["local_uniform_expectation"] - 1.0
        for row in rows
    ]
    min_local = min(
        rows,
        key=lambda row: (
            row["local_uniform_expectation"], row["target_residue"]))
    max_local = max(
        rows,
        key=lambda row: (
            row["local_uniform_expectation"], -row["target_residue"]))
    tight_shape = min(
        rows,
        key=lambda row: (
            row["uniform_margin_to_shape_threshold"],
            row["target_residue"]))
    largest_negative = max(
        rows,
        key=lambda row: (
            row["negative_weight_fraction"], -row["target_residue"]))

    positive_principal_factor_count = sum(
        row["local_uniform_expectation"] > 0.0 for row in rows)
    negative_admissible_count = sum(
        row["negative_weight_count"] > 0 for row in rows)

    return {
        "schema_version": 1,
        "receipt": "q286-wbss-signed-weight-principal-factor-audit",
        "source_commit": source_commit(),
        "sources": {
            "signed_weight_circle_target": str(
                SIGNED_TARGET.relative_to(ROOT)),
            "signed_weight_circle_status": signed["status"],
            "raw_character_circle_decomposition": str(
                RAW_CIRCLE.relative_to(ROOT)),
            "raw_character_circle_status": circle["status"],
            "single_weight_major_arc_floor_audit": str(
                FLOOR.relative_to(ROOT)),
            "single_weight_major_arc_floor_status": floor["status"],
            "negative_region_mass_threshold_audit": str(
                NEGATIVE.relative_to(ROOT)),
            "negative_region_mass_threshold_status": negative["status"],
            "zero_mass_l2_logical_bridge_audit": str(
                L2_LOGICAL.relative_to(ROOT)),
            "zero_mass_l2_logical_bridge_status": l2_logical["status"],
        },
        "status": "HOLD_signed_weight_principal_factor_TN_dependent",
        "question": (
            "Does the q286 signed-weight major-arc local factor give an "
            "independent raw positive term, or does it factor through the "
            "ordinary strict-central pair mass T_N?"),
        "answer": (
            "The principal local factor is positive for every even target "
            "residue, but it is T_N-dependent: the principal term has shape "
            "T_N*M(a).  Thus local factors alone do not create strict-central "
            "support.  q286 remains useful only if a raw weighted circle "
            "estimate proves W_phi(N)>0 directly, or if a separate positive-"
            "mass theorem is honestly imported before applying conditional "
            "signed-distribution control."),
        "principal_factorization": {
            "unweighted_strict_central_mass": (
                "T_N=sum_{N/3<p<2N/3, p and N-p prime} log(p)log(N-p)."),
            "signed_weight_principal_term": (
                "Principal_q286(N)=T_N*M(a), where "
                "M(a)=average of Phi_a over local-admissible left-prime "
                "unit residues for a=N mod 10010."),
            "if_T_N_zero": (
                "Principal_q286(N)=0 even though M(a)>0.  The local factor "
                "does not create support by itself."),
            "independent_principal_surplus_found": False,
            "support_creation_requires": (
                "a raw pointwise estimate for W_phi(N)>0, "
                "G_raw(N)>0, or adverse_drag_raw(N)<local_main_raw(N), "
                "not just a positive local factor M(a)"),
        },
        "local_factor_summary": {
            "even_target_residue_count": len(rows),
            "positive_principal_factor_count": positive_principal_factor_count,
            "nonpositive_principal_factor_count": (
                len(rows) - positive_principal_factor_count),
            "local_factor_M_summary": finite_summary(local_factors),
            "local_factor_M_minus_one_summary": finite_summary(
                local_factor_minus_one),
            "minimum_local_factor_row": min_local,
            "maximum_local_factor_row": max_local,
        },
        "signed_weight_obstruction_summary": {
            "rows_with_negative_admissible_weight": negative_admissible_count,
            "rows_with_pointwise_positive_floor": (
                floor["target_residue_summary"][
                    "rows_with_pointwise_positive_floor"]),
            "global_weight_minimum": floor["global_weight_summary"][
                "minimum"],
            "global_weight_maximum": floor["global_weight_summary"][
                "maximum"],
            "largest_negative_fraction_row": largest_negative,
            "tightest_shape_margin_row": tight_shape,
            "shape_threshold_minimum": negative["summary"][
                "shape_mass_threshold_summary"]["minimum"],
            "minimum_local_uniform_shape_margin": negative["summary"][
                "uniform_margin_to_shape_threshold_summary"]["minimum"],
            "local_uniform_shape_threshold_pass_count": negative["summary"][
                "local_uniform_shape_threshold_pass_count"],
            "local_uniform_robust_threshold_pass_count": negative["summary"][
                "local_uniform_robust_threshold_pass_count"],
        },
        "collapse_classifier": {
            "survives_if": (
                "The same analytic argument proves a strict raw inequality "
                "for the signed weighted binary-prime sum, such as "
                "W_phi(N)>0 or adverse_drag_raw(N)<local_main_raw(N), for "
                "every sufficiently large covered N."),
            "collapses_if": (
                "The proof first proves or assumes T_N>0, then uses the "
                "positive local factor M(a) or normalized signed-shape "
                "control only after support exists."),
            "current_classification": (
                "principal local-factor algebra alone is conditional on "
                "T_N; no independent q286 principal surplus is present"),
            "relation_to_l2_hold": (
                "Consistent with HOLD_l2_logical_bridge_not_confirmed: a raw "
                "strict theorem shape can be non-circular, but coefficient "
                "or local-factor algebra does not prove the required "
                "pointwise raw moment theorem."),
        },
        "candidate": {
            "name": "q286 signed-weight principal local-factor gate",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Separate the principal local q286 factor M(a) from the raw "
                "support-creating estimate.  This prevents positive local "
                "averages from being mistaken for a Goldbach bridge."),
            "prediction": (
                "M(a) is positive for all even residues, but the term remains "
                "multiplicative with T_N and therefore cannot create support "
                "without a raw pointwise estimate."),
            "falsifier": (
                "An explicit signed-weight major-arc theorem with a positive "
                "raw main and pointwise minor-arc error smaller than that "
                "main would move this lane out of HOLD."),
            "smallest_next_action": (
                "Either attempt a true raw major/minor arc estimate for "
                "W_phi(N), or sleep q286 as a proof engine if every path "
                "starts by importing T_N>0."),
        },
        "decision": (
            "HOLD_signed_weight_principal_factor_TN_dependent.  The local "
            "principal q286 factor M(a) is positive on all 5005 even target "
            "residues, with minimum 0.6039353780830684 and maximum "
            "1.5716524655081634.  But the principal term is T_N*M(a), so "
            "it vanishes on zero-support rows.  Since every target also has "
            "negative admissible weights and no pointwise positive floor, "
            "the useful remaining route is a raw signed-weight circle-method "
            "estimate or raw adverse-drag bound.  Local-factor positivity "
            "alone is conditional decoration after positive mass."),
        "status_boundary": (
            "Principal local-factor audit only.  No signed-weight "
            "major/minor arc estimate, raw weighted witness theorem, signed "
            "negative-region distribution theorem, positive-mass theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof is established."),
        "signed_weight_major_arc_estimate_proved": False,
        "raw_weighted_witness_theorem_proved": False,
        "signed_negative_region_distribution_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    summary = receipt["local_factor_summary"]
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "positive_principal_factor_count": summary[
            "positive_principal_factor_count"],
        "minimum_local_factor": summary["local_factor_M_summary"][
            "minimum"],
        "independent_principal_surplus_found": receipt[
            "principal_factorization"][
                "independent_principal_surplus_found"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

"""Quantify the q286 single-weight negative-region theorem obligation.

The single-weight floor audit falsified the support-only shortcut: every even
target has admissible negative-weight residues.  This derived receipt measures
what remains.  It separates a too-crude sign-mass theorem from the sharper
signed-shape/correlation theorem that could still pay the witness.

Finite coefficient algebra only.  No signed distribution theorem, positive
mass theorem, q286 threshold theorem, strict-central Goldbach theorem, or
Goldbach proof is established.
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
FLOOR_SOURCE = (
    EVIDENCE / "q286-wbss-single-weight-major-arc-floor-audit.json")
OUT = EVIDENCE / "q286-wbss-negative-region-mass-threshold-audit.json"
TOLERANCE = 1e-12

sys.path.insert(0, str(ROOT))

from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    period_full_unit_coefficients,
    prepare_support_context,
)
from tools.build_q286_wbss_four_modulus_projection_formula import (  # noqa: E402
    PERIOD,
    all_units,
    coefficient_vector,
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
    items = [float(value) for value in values]
    return {
        "minimum": min(items),
        "maximum": max(items),
        "mean": math.fsum(items) / len(items),
    }


def row_for_target(target_residue, units, phi):
    mask = np.asarray([
        math.gcd((target_residue - int(unit)) % PERIOD, PERIOD) == 1
        for unit in units
    ], dtype=bool)
    values = phi[mask]
    negative = values[values < -TOLERANCE]
    positive = values[values > TOLERANCE]
    negative_fraction = len(negative) / len(values)
    negative_mean = float(np.mean(negative))
    positive_mean = float(np.mean(positive))
    negative_minimum = float(np.min(negative))
    positive_minimum = float(np.min(positive))
    shape_threshold = positive_mean / (positive_mean - negative_mean)
    robust_threshold = (
        positive_minimum / (positive_minimum - negative_minimum))
    return {
        "target_residue": int(target_residue),
        "target_mod_286": int(target_residue % 286),
        "admissible_unit_count": int(len(values)),
        "local_uniform_expectation": float(np.mean(values)),
        "negative_weight_fraction": float(negative_fraction),
        "negative_weight_count": int(len(negative)),
        "positive_weight_count": int(len(positive)),
        "negative_minimum": negative_minimum,
        "negative_mean": negative_mean,
        "positive_minimum": positive_minimum,
        "positive_mean": positive_mean,
        "robust_sign_mass_threshold": float(robust_threshold),
        "shape_mass_threshold": float(shape_threshold),
        "uniform_margin_to_shape_threshold": float(
            shape_threshold - negative_fraction),
        "uniform_margin_to_robust_threshold": float(
            robust_threshold - negative_fraction),
        "local_uniform_passes_shape_threshold": bool(
            negative_fraction < shape_threshold),
        "local_uniform_passes_robust_threshold": bool(
            negative_fraction < robust_threshold),
    }


def build_rows():
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    principal = float(context["principal_mean"].real)
    units = np.asarray(all_units(), dtype=np.int64)
    phi = coefficient_vector(tuple(int(unit) for unit in units),
                             full_coefficients, principal)
    rows = [
        row_for_target(target_residue, units, phi)
        for target_residue in range(0, PERIOD, 2)
    ]
    return principal, units, phi, rows


def build_receipt():
    floor = load_json(FLOOR_SOURCE)
    principal, units, phi, rows = build_rows()
    shape_pass_count = sum(
        row["local_uniform_passes_shape_threshold"] for row in rows)
    robust_pass_count = sum(
        row["local_uniform_passes_robust_threshold"] for row in rows)
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-negative-region-mass-threshold-audit",
        "source_commit": source_commit(),
        "sources": {
            "single_weight_major_arc_floor_audit": str(
                FLOOR_SOURCE.relative_to(ROOT)),
            "single_weight_major_arc_floor_status": floor["status"],
        },
        "status": "TARGET_signed_negative_region_correlation_obligation",
        "question": (
            "After the pointwise positive floor fails, what negative-region "
            "mass or signed-shape control would still make the single q286 "
            "weight positive?"),
        "answer": (
            "A crude sign-mass theorem is far too strong: using only the "
            "most adverse negative coefficient and the smallest positive "
            "coefficient gives thresholds around 0.0007 to 0.0033, while the "
            "local-uniform negative fractions are about 0.297 to 0.472.  The "
            "surviving target is not 'almost no negative mass'; it is a "
            "signed-shape or correlation theorem.  Under local-uniform "
            "within-sign averages, the admissible negative-mass threshold is "
            "about 0.487 to 0.636, and every target has positive margin."),
        "normalization": {
            "period": PERIOD,
            "unit_count": int(len(units)),
            "principal_mean": principal,
            "normalized_weight": (
                "phi(u)=full_q286_wbss_unit_coefficient(u)/principal_mean"),
            "global_weight_minimum": float(np.min(phi)),
            "global_weight_maximum": float(np.max(phi)),
            "global_weight_mean": float(np.mean(phi)),
        },
        "definitions": {
            "negative_region": "R_-(a)={u admissible for a: phi(u)<0}.",
            "positive_region": "R_+(a)={u admissible for a: phi(u)>0}.",
            "robust_sign_mass_threshold": (
                "rho_robust(a)=min_positive_phi(a)/(min_positive_phi(a)-"
                "min_negative_phi(a)).  If all positive mass is allowed to "
                "sit at the smallest positive coefficient and all negative "
                "mass at the most negative coefficient, then negative mass "
                "fraction below rho_robust is sufficient."),
            "shape_mass_threshold": (
                "rho_shape(a)=mean_positive_phi_uniform(a)/("
                "mean_positive_phi_uniform(a)-mean_negative_phi_uniform(a)). "
                "This is the negative-mass cutoff if the within-sign "
                "conditional averages are no worse than their local-uniform "
                "averages."),
            "raw_witness_boundary": (
                "The theorem must ultimately be raw: W_phi(N)>0 or "
                "adverse_drag_raw(N)<local_main_raw(N).  Any normalized "
                "negative-mass statement is conditional on, or must be proved "
                "inside an argument that creates, strict-central mass."),
        },
        "summary": {
            "even_target_residue_count": len(rows),
            "local_uniform_shape_threshold_pass_count": shape_pass_count,
            "local_uniform_robust_threshold_pass_count": robust_pass_count,
            "negative_weight_fraction_summary": finite_summary(
                row["negative_weight_fraction"] for row in rows),
            "robust_sign_mass_threshold_summary": finite_summary(
                row["robust_sign_mass_threshold"] for row in rows),
            "shape_mass_threshold_summary": finite_summary(
                row["shape_mass_threshold"] for row in rows),
            "uniform_margin_to_shape_threshold_summary": finite_summary(
                row["uniform_margin_to_shape_threshold"] for row in rows),
            "uniform_margin_to_robust_threshold_summary": finite_summary(
                row["uniform_margin_to_robust_threshold"] for row in rows),
            "local_uniform_expectation_summary": finite_summary(
                row["local_uniform_expectation"] for row in rows),
            "tightest_shape_margin_rows": sorted(
                rows,
                key=lambda row: (
                    row["uniform_margin_to_shape_threshold"],
                    row["target_residue"]),
            )[:12],
            "tightest_robust_margin_rows": sorted(
                rows,
                key=lambda row: (
                    row["uniform_margin_to_robust_threshold"],
                    row["target_residue"]),
            )[:12],
            "largest_negative_fraction_rows": sorted(
                rows,
                key=lambda row: (
                    -row["negative_weight_fraction"],
                    row["target_residue"]),
            )[:12],
        },
        "theorem_obligation": {
            "crude_sign_mass_route_status": (
                "sleep unless a theorem can prove the actual negative-region "
                "prime-pair mass is under roughly 0.1 percent for every "
                "covered target; local-uniform itself does not satisfy this "
                "robust threshold."),
            "surviving_signed_shape_route": (
                "Prove W_+(N)>W_-(N) directly, or prove negative-region mass "
                "and within-region weighted averages strong enough to imply "
                "sum_u mu_N(u)phi(u)>0 for every sufficiently large covered "
                "N."),
            "raw_unormalized_form": (
                "Let P_N(u) be raw strict-central log-pair mass with left "
                "prime residue u.  A direct sufficient theorem is "
                "sum_{u:phi(u)>0} P_N(u)phi(u) > "
                "sum_{u:phi(u)<0} P_N(u)(-phi(u)) for every sufficiently "
                "large covered N."),
            "normalization_warning": (
                "Statements about fractions of mass in R_-(a) are useful "
                "diagnostics, but by themselves are conditional on T_N>0.  "
                "They do not prove strict-central support unless embedded in "
                "a raw strict positivity proof."),
        },
        "candidate": {
            "name": "negative-region signed-shape theorem target",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Replace the failed pointwise-positive floor with a two-sided "
                "signed-region comparison: positive coefficient mass must "
                "outweigh adverse negative coefficient mass."),
            "prediction": (
                "Local-uniform within-sign shape has substantial positive "
                "margin, while a robust sign-only theorem is too severe."),
            "falsifier": (
                "If a covered target has raw negative weighted mass at least "
                "as large as raw positive weighted mass, this q286 single-"
                "weight sufficient route fails for that target."),
            "smallest_test": (
                "Compute robust and shape-based negative mass thresholds for "
                "all 5005 even target residues."),
        },
        "decision": (
            "The pointwise floor failure does not force q286 to sleep, but it "
            "does sleep the crude support-only and robust sign-mass-only "
            "shortcuts.  The robust negative-mass thresholds are only about "
            "0.0007147..0.0033013, and local-uniform negative fractions exceed "
            "them on every target.  The meaningful surviving target is "
            "signed-shape/correlation control: local-uniform within-sign "
            "thresholds are about 0.487294..0.635585, and every target has "
            "positive margin of at least about 0.10534.  This is a theorem "
            "obligation, not a theorem."),
        "status_boundary": (
            "Finite coefficient threshold audit only; no signed negative-"
            "region distribution theorem, raw adverse-drag theorem, positive "
            "mass theorem, q286 threshold theorem, strict-central Goldbach "
            "theorem, or Goldbach proof is established."),
        "goldbach_proved": False,
        "signed_negative_region_distribution_theorem_proved": False,
        "raw_adverse_drag_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "universal_pointwise_bound_proved": False,
        "finite_evidence_acceptance_condition": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "shape_threshold_minimum": (
            receipt["summary"]["shape_mass_threshold_summary"]["minimum"]),
        "shape_margin_minimum": (
            receipt["summary"][
                "uniform_margin_to_shape_threshold_summary"]["minimum"]),
        "robust_threshold_maximum": (
            receipt["summary"][
                "robust_sign_mass_threshold_summary"]["maximum"]),
        "local_uniform_robust_pass_count": (
            receipt["summary"][
                "local_uniform_robust_threshold_pass_count"]),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

"""Audit the pointwise floor of the raw q286 single-weight witness.

The raw character circle decomposition suggested a smallest next test: combine
the q286-WBSS coefficients before integration and ask whether the resulting
left-prime residue weight has an easy positive floor on every admissible
residue.  If it did, any strict-central prime pair would land on a positive
coefficient.  If it does not, the proof obligation must remain a signed
distribution/correlation estimate, not a mere support argument.

This is exact finite coefficient algebra.  It proves no prime-distribution
theorem, major/minor arc estimate, strict-central Goldbach theorem, or
Goldbach proof.
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
CIRCLE_SOURCE = (
    EVIDENCE / "q286-wbss-raw-character-circle-decomposition.json")
FORMULA_SOURCE = EVIDENCE / "q286-wbss-four-modulus-projection-formula.json"
OUT = EVIDENCE / "q286-wbss-single-weight-major-arc-floor-audit.json"
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


def admissible_mask(target_residue, units):
    return np.asarray([
        math.gcd((target_residue - int(unit)) % PERIOD, PERIOD) == 1
        for unit in units
    ], dtype=bool)


def target_rows(units, phi):
    rows = []
    for target_residue in range(0, PERIOD, 2):
        mask = admissible_mask(target_residue, units)
        values = phi[mask]
        negative_count = int(np.sum(values < -TOLERANCE))
        positive_count = int(np.sum(values > TOLERANCE))
        zero_count = int(len(values) - negative_count - positive_count)
        rows.append({
            "target_residue": int(target_residue),
            "target_mod_286": int(target_residue % 286),
            "admissible_unit_count": int(len(values)),
            "admissible_weight_minimum": float(np.min(values)),
            "admissible_weight_mean": float(np.mean(values)),
            "admissible_weight_maximum": float(np.max(values)),
            "negative_weight_count": negative_count,
            "zero_weight_count": zero_count,
            "positive_weight_count": positive_count,
            "negative_weight_fraction": float(negative_count / len(values)),
            "pointwise_positive_floor_holds": bool(
                np.min(values) > TOLERANCE),
        })
    return rows


def build_receipt():
    circle = load_json(CIRCLE_SOURCE)
    formula = load_json(FORMULA_SOURCE)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    principal = float(context["principal_mean"].real)
    units = np.asarray(all_units(), dtype=np.int64)
    phi = coefficient_vector(tuple(int(unit) for unit in units),
                             full_coefficients, principal)
    rows = target_rows(units, phi)
    negative_rows = [
        row for row in rows
        if row["negative_weight_count"] > 0
    ]
    positive_floor_rows = [
        row for row in rows
        if row["pointwise_positive_floor_holds"]
    ]
    sign_split = {
        "negative_unit_count": int(np.sum(phi < -TOLERANCE)),
        "zero_unit_count": int(np.sum(np.abs(phi) <= TOLERANCE)),
        "positive_unit_count": int(np.sum(phi > TOLERANCE)),
    }
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-single-weight-major-arc-floor-audit",
        "source_commit": source_commit(),
        "sources": {
            "raw_character_circle_decomposition": str(
                CIRCLE_SOURCE.relative_to(ROOT)),
            "raw_character_circle_status": circle["status"],
            "four_modulus_projection_formula": str(
                FORMULA_SOURCE.relative_to(ROOT)),
            "four_modulus_projection_status_boundary": formula[
                "status_boundary"],
        },
        "status": "FALSIFIER_pointwise_positive_single_weight_floor",
        "question": (
            "Does the combined raw q286 single-weight witness have a "
            "positive coefficient floor on every admissible left-prime "
            "residue, so support alone could imply W_phi(N)>0?"),
        "answer": (
            "No.  The normalized combined residue weight has mean 1 but takes "
            "both negative and positive values.  Every even target residue has "
            "at least one admissible left-prime residue with negative weight. "
            "Therefore a proof cannot be only a support argument; it must "
            "prove enough signed distribution or correlation to keep prime "
            "pair mass away from the negative-weight region, or otherwise "
            "bound adverse drag below the local main."),
        "normalization": {
            "period": PERIOD,
            "unit_count": int(len(units)),
            "principal_mean": principal,
            "normalized_weight": (
                "phi(u)=full_q286_wbss_unit_coefficient(u)/principal_mean"),
            "global_weight_mean": float(np.mean(phi)),
        },
        "global_weight_summary": {
            "minimum": float(np.min(phi)),
            "maximum": float(np.max(phi)),
            "mean": float(np.mean(phi)),
            **sign_split,
        },
        "target_residue_summary": {
            "even_target_residue_count": len(rows),
            "rows_with_negative_admissible_weight": len(negative_rows),
            "rows_with_pointwise_positive_floor": len(positive_floor_rows),
            "admissible_weight_minimum_summary": finite_summary(
                row["admissible_weight_minimum"] for row in rows),
            "admissible_weight_mean_summary": finite_summary(
                row["admissible_weight_mean"] for row in rows),
            "admissible_weight_maximum_summary": finite_summary(
                row["admissible_weight_maximum"] for row in rows),
            "negative_weight_fraction_summary": finite_summary(
                row["negative_weight_fraction"] for row in rows),
            "worst_local_mean_rows": sorted(
                rows,
                key=lambda row: (
                    row["admissible_weight_mean"],
                    row["target_residue"]),
            )[:12],
            "worst_pointwise_floor_rows": sorted(
                rows,
                key=lambda row: (
                    row["admissible_weight_minimum"],
                    row["target_residue"]),
            )[:12],
            "largest_negative_fraction_rows": sorted(
                rows,
                key=lambda row: (
                    -row["negative_weight_fraction"],
                    row["target_residue"]),
            )[:12],
        },
        "logical_consequence": {
            "support_only_route_falsified": True,
            "why": (
                "Because every even target residue admits negative-weight "
                "left-prime residues, existence of some strict-central prime "
                "pair does not imply the pair contributes positively to the "
                "single-weight witness."),
            "surviving_requirement": (
                "Prove a universal pointwise signed distribution estimate, a "
                "one-sided adverse-drag envelope below local main, or a "
                "major/minor arc estimate for W_phi(N)>0 directly."),
            "collapse_warning": (
                "If the proof first obtains T_N>0 and then merely assumes "
                "prime-pair mass is locally uniform enough, q286 remains "
                "conditional decoration unless that uniformity/correlation is "
                "itself proved pointwise in unnormalized scale."),
        },
        "candidate": {
            "name": "single-weight pointwise positivity shortcut",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use the combined q286 coefficient as one residue weight; if "
                "all admissible coefficients were positive, support alone "
                "would imply positive witness."),
            "prediction": (
                "If the shortcut were alive, every target's admissible "
                "residue set would have positive minimum weight."),
            "falsifier": (
                "Any target residue with an admissible negative coefficient "
                "blocks the support-only shortcut.  The audit finds such "
                "residues for all even target residues."),
            "smallest_test": (
                "Compute min, mean, max, and negative fraction of the "
                "normalized combined weight over each admissible residue set."),
        },
        "decision": (
            "The single-weight support-only shortcut is falsified.  The q286 "
            "combined weight is not pointwise positive: globally it ranges "
            "from about -11.7470671262 to 40.2288103002, with 1228 negative "
            "unit residues and 1652 positive unit residues.  All 5005 even "
            "target residues have negative admissible weights.  The local "
            "uniform means remain positive, with minimum about "
            "0.603935378083, but positivity now depends on distribution of "
            "prime-pair mass, not just support."),
        "status_boundary": (
            "Finite coefficient-floor audit and shortcut falsifier only; no "
            "signed distribution theorem, adverse-drag theorem, major/minor "
            "arc estimate, q286 threshold theorem, strict-central Goldbach "
            "theorem, or Goldbach proof is established."),
        "goldbach_proved": False,
        "single_weight_pointwise_floor_theorem_proved": False,
        "signed_distribution_theorem_proved": False,
        "adverse_drag_theorem_proved": False,
        "major_arc_estimate_proved": False,
        "q286_threshold_theorem_proved": False,
        "universal_pointwise_bound_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "global_minimum": (
            receipt["global_weight_summary"]["minimum"]),
        "global_maximum": (
            receipt["global_weight_summary"]["maximum"]),
        "rows_with_negative_admissible_weight": (
            receipt["target_residue_summary"][
                "rows_with_negative_admissible_weight"]),
        "rows_with_pointwise_positive_floor": (
            receipt["target_residue_summary"][
                "rows_with_pointwise_positive_floor"]),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

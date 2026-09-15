"""Extract an explicit four-modulus formula for the q286-WBSS signed witness.

The four-modulus span audit showed that the normalized full q286-WBSS unit
coefficient f(u) descends to total mass plus residue projections modulo

    70, 130, 154, 286.

This receipt turns that span statement into a theorem-facing formula:

    f(u) = alpha_0 + sum_d sum_s alpha_{d,s} 1_{u == s mod d}.

Therefore the normalized strict-central signed witness equals a fixed linear
combination of projected binary-prime residue masses at those four moduli.

This is not a prime-distribution theorem and does not prove Goldbach.  It
names the exact projected quantities and coefficient-norm budgets that a
source-backed estimate would have to control.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.sparse import csr_matrix, vstack
from scipy.sparse.linalg import lsqr


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-wbss-four-modulus-projection-formula.json"
PERIOD = 10010
MODULI = (70, 130, 154, 286)
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    period_full_unit_coefficients,
    prepare_support_context,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402


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
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, np.generic):
        return json_ready(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def all_units():
    return tuple(
        residue for residue in range(PERIOD)
        if math.gcd(residue, PERIOD) == 1
    )


def design_matrix(units, moduli):
    matrices = [csr_matrix(np.ones((1, len(units)), dtype=np.float64))]
    labels = [{"kind": "total_mass", "modulus": None, "residue": None}]
    for modulus in moduli:
        residues = sorted({int(unit % modulus) for unit in units})
        residue_index = {residue: index for index, residue in enumerate(residues)}
        data = []
        row_indexes = []
        column_indexes = []
        for column, unit in enumerate(units):
            row_indexes.append(residue_index[int(unit % modulus)])
            column_indexes.append(column)
            data.append(1.0)
        matrices.append(csr_matrix(
            (data, (row_indexes, column_indexes)),
            shape=(len(residues), len(units)),
            dtype=np.float64,
        ))
        labels.extend(
            {"kind": "residue_projection", "modulus": modulus, "residue": residue}
            for residue in residues
        )
    return vstack(matrices, format="csr"), labels


def coefficient_vector(units, full_coefficients, principal):
    return np.asarray([
        full_coefficients[unit].real / principal
        for unit in units
    ], dtype=np.float64)


def solve_formula(rowspace, phi):
    solved = lsqr(rowspace.T, phi, atol=1e-13, btol=1e-13, iter_lim=5000)
    alpha = np.asarray(solved[0], dtype=np.float64)
    reconstructed = rowspace.T @ alpha
    residual = phi - reconstructed
    scale = max(1.0, float(np.linalg.norm(phi)))
    return {
        "alpha": alpha,
        "relative_l2_residual": float(np.linalg.norm(residual) / scale),
        "l2_residual": float(np.linalg.norm(residual)),
        "max_abs_residual": float(np.max(np.abs(residual))),
        "lsqr_iterations": int(solved[2]),
        "lsqr_stop_code": int(solved[1]),
        "lsqr_condition_estimate": float(solved[6]),
    }


def coefficient_table(labels, alpha):
    rows = []
    by_modulus = {}
    for label, value in zip(labels, alpha):
        row = {**label, "coefficient": float(value)}
        rows.append(row)
        if label["kind"] == "residue_projection":
            by_modulus.setdefault(str(label["modulus"]), []).append(row)
    modulus_summaries = {}
    for modulus, items in by_modulus.items():
        values = [item["coefficient"] for item in items]
        modulus_summaries[modulus] = {
            "coefficient_count": len(values),
            "positive_count": sum(value > TOLERANCE for value in values),
            "negative_count": sum(value < -TOLERANCE for value in values),
            "near_zero_count": sum(abs(value) <= TOLERANCE for value in values),
            "l1_norm": float(math.fsum(abs(value) for value in values)),
            "l2_norm": float(math.sqrt(math.fsum(value * value for value in values))),
            "linf_norm": float(max(abs(value) for value in values)),
            "sum": float(math.fsum(values)),
            "largest_abs_coefficients": sorted(
                items,
                key=lambda item: (-abs(item["coefficient"]), item["residue"]),
            )[:12],
        }
    nonconstant = [
        row["coefficient"] for row in rows
        if row["kind"] == "residue_projection"
    ]
    return {
        "rows": rows,
        "total_mass_coefficient": float(alpha[0]),
        "total_nonconstant_l1_norm": float(
            math.fsum(abs(value) for value in nonconstant)),
        "total_nonconstant_l2_norm": float(
            math.sqrt(math.fsum(value * value for value in nonconstant))),
        "total_nonconstant_linf_norm": float(
            max(abs(value) for value in nonconstant)),
        "modulus_summaries": modulus_summaries,
        "largest_abs_coefficients": sorted(
            [row for row in rows if row["kind"] == "residue_projection"],
            key=lambda item: (
                -abs(item["coefficient"]),
                item["modulus"],
                item["residue"],
            ),
        )[:24],
    }


def admissible_units_for_target(target_residue, units):
    return tuple(
        unit for unit in units
        if math.gcd((target_residue - unit) % PERIOD, PERIOD) == 1
    )


def local_main_rows(units, phi, rowspace, alpha):
    unit_array = np.asarray(units, dtype=np.int64)
    rows = []
    for target_residue in range(0, PERIOD, 2):
        mask = np.asarray([
            math.gcd(int((target_residue - unit) % PERIOD), PERIOD) == 1
            for unit in unit_array
        ], dtype=bool)
        admissible_count = int(np.sum(mask))
        probabilities = np.asarray(
            rowspace[:, mask].sum(axis=1), dtype=np.float64).ravel()
        probabilities /= admissible_count
        direct = float(np.mean(phi[mask]))
        formula = float(np.dot(alpha, probabilities))
        rows.append({
            "target_residue": int(target_residue),
            "target_mod_286": int(target_residue % 286),
            "admissible_unit_count": int(admissible_count),
            "local_uniform_main_term": direct,
            "formula_local_uniform_main_term": formula,
            "formula_abs_error": abs(direct - formula),
        })
    return rows


def projection_budget(local_rows, table):
    minimum = min(row["local_uniform_main_term"] for row in local_rows)
    l1_total = table["total_nonconstant_l1_norm"]
    by_modulus = {
        modulus: row["l1_norm"]
        for modulus, row in table["modulus_summaries"].items()
    }
    return {
        "minimum_local_uniform_main_term": minimum,
        "worst_local_uniform_row": min(
            local_rows,
            key=lambda row: (row["local_uniform_main_term"],
                             row["target_residue"]),
        ),
        "all_even_residue_local_main_terms_positive": bool(
            minimum > TOLERANCE),
        "sufficient_uniform_projection_error_bound": (
            minimum / l1_total if l1_total > TOLERANCE else None),
        "sufficient_bound_meaning": (
            "If every nonconstant projected residue probability error across "
            "all four moduli is bounded in absolute value by this epsilon, "
            "then the signed expectation is positive for every even residue. "
            "This is sufficient and usually pessimistic, not necessary."),
        "l1_norm_by_modulus": by_modulus,
        "per_modulus_equal_error_bound": (
            minimum / math.fsum(by_modulus.values())
            if by_modulus else None),
    }


def build_receipt():
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    principal = float(context["principal_mean"].real)
    units = all_units()
    phi = coefficient_vector(units, full_coefficients, principal)
    rowspace, labels = design_matrix(units, MODULI)
    solved = solve_formula(rowspace, phi)
    table = coefficient_table(labels, solved["alpha"])
    local_rows = local_main_rows(units, phi, rowspace, solved["alpha"])
    local_error_summary = finite_summary(
        row["formula_abs_error"] for row in local_rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "finite formula extraction only; it proves no binary-prime "
            "projection theorem, signed discrepancy theorem, q286 threshold "
            "theorem, strict-central Goldbach theorem, or Goldbach proof"
        ),
        "goldbach_proved": False,
        "four_modulus_projection_theorem_proved": False,
        "signed_discrepancy_theorem_proved": False,
        "formula": {
            "period": PERIOD,
            "moduli": list(MODULI),
            "normalized_unit_coefficient": (
                "f(u)=full_q286_wbss_unit_coefficient(u)/principal_mean"),
            "identity": (
                "f(u)=alpha_0+sum_{d in {70,130,154,286}} "
                "sum_s alpha_{d,s} 1_{u == s mod d}"),
            "normalized_witness": (
                "A(N)=alpha_0+sum_d sum_s alpha_{d,s} Pi_{N,d}(s), "
                "where Pi_{N,d}(s) is the strict-central binary-prime "
                "residue mass of the left prime modulo d."),
            "positivity_condition": "A(N)>0",
        },
        "candidate": {
            "name": "four-modulus projected binary-prime witness",
            "mechanism": (
                "Replace the 10010-unit signed coefficient by four projected "
                "residue tables.  The proof obligation becomes control of "
                "actual binary-prime projection probabilities at those "
                "moduli, not control of every unit residue separately."),
            "prediction": (
                "The formula reconstructs f(u) to numerical zero and every "
                "local-uniform main term over admissible residues is positive."
            ),
            "falsifier": (
                "A reconstruction residual above tolerance, or any even "
                "target residue with nonpositive local-uniform main term, "
                "would demote this as a global main-term bridge."
            ),
            "smallest_test": (
                "Extract one LSQR decomposition, replay all 2880 unit values, "
                "and compute all 5005 even-residue local-uniform main terms."
            ),
            "novelty_label": "new-to-this-task",
        },
        "unit_count": len(units),
        "coefficient_fit": {
            key: value for key, value in solved.items() if key != "alpha"
        },
        "coefficient_table": table,
        "local_main_term_summary": {
            "row_count": len(local_rows),
            "local_uniform_main_term_summary": finite_summary(
                row["local_uniform_main_term"] for row in local_rows),
            "formula_abs_error_summary": local_error_summary,
            "worst_rows": sorted(
                local_rows,
                key=lambda row: (
                    row["local_uniform_main_term"], row["target_residue"]),
            )[:20],
            "largest_formula_error_rows": sorted(
                local_rows,
                key=lambda row: (
                    -row["formula_abs_error"], row["target_residue"]),
            )[:12],
        },
        "projection_error_budget": projection_budget(local_rows, table),
        "decision": (
            "This receipt turns the four-modulus coefficient compression into "
            "a concrete projected binary-prime formula and a sufficient error "
            "budget.  The next proof step is to source or prove estimates for "
            "Pi_{N,d}(s)-U_{a,d}(s) strong enough for this budget, or to "
            "replace the pessimistic absolute-error budget with a signed "
            "correlation estimate."),
        "next_obligation": (
            "Compare the required four-modulus projection error budget with "
            "published fixed-modulus binary Goldbach-in-progressions or "
            "circle-method estimates, using strict-central intervals and "
            "log weights if available."),
    }


def main():
    OUT.write_text(
        json.dumps(json_ready(build_receipt()), indent=2, sort_keys=True)
        + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

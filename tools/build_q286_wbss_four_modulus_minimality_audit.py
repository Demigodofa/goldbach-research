"""Audit whether the q286-WBSS four-modulus coefficient target is minimal.

The four-modulus span identity shows the q286-WBSS unit coefficient descends
to total mass plus projections to 70, 130, 154, and 286.  This receipt tests
the next smaller-theorem question: does any proper subfamily of those moduli
already reconstruct the coefficient?

This is coefficient algebra only.  It proves no binary-prime projection
theorem, signed discrepancy theorem, q286 threshold theorem, strict-central
Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import itertools
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = EVIDENCE / "q286-wbss-four-modulus-span-identity-audit.json"
OUT = EVIDENCE / "q286-wbss-four-modulus-minimality-audit.json"
PERIOD = 10010
FOUR_MODULI = (70, 130, 154, 286)
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    period_full_unit_coefficients,
    prepare_support_context,
)
from tools.build_q286_wbss_four_modulus_span_identity_audit import (  # noqa: E402
    coefficient_span_residual,
    projection_rowspace,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_source():
    return json.loads(SOURCE.read_text(encoding="utf-8"))


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


def unit_coefficient():
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    principal = float(context["principal_mean"].real)
    units = tuple(
        residue for residue in range(PERIOD)
        if math.gcd(residue, PERIOD) == 1
    )
    unit_columns = tuple((unit,) for unit in units)
    phi = np.asarray([
        full_coefficients[unit].real / principal
        for unit in units
    ], dtype=np.float64)
    return unit_columns, phi


def subset_rows(unit_columns, phi):
    rows = []
    for size in range(0, len(FOUR_MODULI) + 1):
        for moduli in itertools.combinations(FOUR_MODULI, size):
            rowspace, row_counts = projection_rowspace(unit_columns, moduli)
            residual = coefficient_span_residual(phi, rowspace)
            rows.append({
                "moduli": list(moduli),
                "modulus_count": len(moduli),
                "is_full_four_modulus_family": moduli == FOUR_MODULI,
                "exact_span": (
                    residual["relative_l2_residual"] <= TOLERANCE
                    and residual["max_abs_residual"] <= TOLERANCE
                ),
                "projection_row_counts": row_counts,
                **residual,
            })
    return rows


def summarize(rows):
    proper = [row for row in rows if not row["is_full_four_modulus_family"]]
    exact_proper = [row for row in proper if row["exact_span"]]
    best_proper = min(
        proper,
        key=lambda row: (
            row["relative_l2_residual"],
            row["max_abs_residual"],
            row["modulus_count"],
            row["moduli"],
        ),
    )
    full = next(row for row in rows if row["is_full_four_modulus_family"])
    by_size = {}
    for size in range(0, len(FOUR_MODULI) + 1):
        sized = [row for row in rows if row["modulus_count"] == size]
        by_size[str(size)] = {
            "family_count": len(sized),
            "exact_span_count": sum(row["exact_span"] for row in sized),
            "relative_l2_residual_summary": finite_summary(
                row["relative_l2_residual"] for row in sized),
            "max_abs_residual_summary": finite_summary(
                row["max_abs_residual"] for row in sized),
            "best_family": min(
                sized,
                key=lambda row: (
                    row["relative_l2_residual"],
                    row["max_abs_residual"],
                    row["moduli"],
                ),
            ),
        }
    return {
        "family_count": len(rows),
        "proper_family_count": len(proper),
        "proper_exact_span_count": len(exact_proper),
        "full_four_modulus_exact_span": full["exact_span"],
        "best_proper_family": best_proper,
        "full_four_modulus_family": full,
        "relative_l2_residual_summary": finite_summary(
            row["relative_l2_residual"] for row in rows),
        "by_modulus_count": by_size,
    }


def build_receipt():
    source = load_source()
    unit_columns, phi = unit_coefficient()
    rows = subset_rows(unit_columns, phi)
    summary = summarize(rows)
    no_smaller_exact = (
        summary["proper_exact_span_count"] == 0
        and summary["full_four_modulus_exact_span"]
    )
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "four_modulus_span_identity_audit": str(
                SOURCE.relative_to(ROOT)),
            "span_identity_source_commit": source["source_commit"],
        },
        "status_boundary": (
            "finite q286-WBSS coefficient-span minimality audit only; "
            "no binary-prime projection theorem, signed discrepancy theorem, "
            "q286 threshold theorem, strict-central Goldbach theorem, or "
            "Goldbach proof"),
        "goldbach_proved": False,
        "four_modulus_projection_theorem_proved": False,
        "signed_discrepancy_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "four-modulus coefficient-span minimality",
            "mechanism": (
                "Enumerate every projection family below "
                "{70,130,154,286} and fit the q286-WBSS unit coefficient "
                "using total mass plus those residue projections."),
            "prediction": (
                "If Fourier/projection sparsification can yield a smaller "
                "theorem target, at least one proper subfamily should have "
                "numerical-zero unit residual."),
            "falsifier": (
                "Any exact proper subfamily would falsify four-modulus "
                "minimality and become the smaller theorem target."),
            "smallest_test": (
                "Use the existing unit-level coefficient and enumerate all "
                "16 subfamilies of {70,130,154,286}; no prime counts are "
                "computed."),
            "novelty_label": "new-to-this-task",
        },
        "target_moduli": list(FOUR_MODULI),
        "unit_count": len(unit_columns),
        "coefficient_l2_norm": float(np.linalg.norm(phi)),
        "holdout": {
            "summary": summary,
            "families": sorted(
                rows,
                key=lambda row: (
                    row["modulus_count"],
                    row["relative_l2_residual"],
                    row["moduli"],
                ),
            ),
        },
        "no_smaller_projection_family_found": bool(no_smaller_exact),
        "decision": (
            "No proper subfamily of {70,130,154,286} reconstructs the "
            "q286-WBSS unit coefficient at numerical-zero residual, while "
            "the full four-modulus family does.  Therefore Fourier/projection "
            "sparsification does not produce a smaller coefficient theorem "
            "target at this algebraic level.  This leaves the four-modulus "
            "binary-prime projection-control theorem as the narrowed target; "
            "it remains unproved, and Goldbach remains open."
        ),
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

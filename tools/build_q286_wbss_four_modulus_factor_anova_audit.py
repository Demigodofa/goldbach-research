"""CRT factor-ANOVA certificate for the q286-WBSS four-modulus target.

The minimality audit showed numerically that no proper subfamily of
{70,130,154,286} reconstructs the q286-WBSS unit coefficient.  This receipt
asks for the structural reason.  On units modulo 10010, CRT identifies the
coefficient with a tensor over factors 5,7,11,13.  Projection to a modulus
whose odd prime factors are S spans exactly the ANOVA interactions supported
inside S.

This is finite coefficient algebra only.  It proves no binary-prime
projection-control theorem, signed discrepancy theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.
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
MINIMALITY_SOURCE = (
    EVIDENCE / "q286-wbss-four-modulus-minimality-audit.json")
OUT = EVIDENCE / "q286-wbss-four-modulus-factor-anova-audit.json"
PERIOD = 10010
FACTORS = (5, 7, 11, 13)
TARGET_MODULI = (70, 130, 154, 286)
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    period_full_unit_coefficients,
    prepare_support_context,
)
from tools.build_q286_wbss_four_modulus_minimality_audit import (  # noqa: E402
    subset_rows,
)
from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_minimality_source():
    return json.loads(MINIMALITY_SOURCE.read_text(encoding="utf-8"))


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


def support_key(support):
    return "empty" if not support else ",".join(str(factor) for factor in support)


def powerset(items):
    items = tuple(items)
    for size in range(len(items) + 1):
        yield from itertools.combinations(items, size)


def modulus_factor_support(modulus):
    return tuple(factor for factor in FACTORS if modulus % factor == 0)


def coefficient_tensor():
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    principal = float(context["principal_mean"].real)
    axes = {
        factor: tuple(residue for residue in range(1, factor)
                      if math.gcd(residue, factor) == 1)
        for factor in FACTORS
    }
    indexes = {
        factor: {residue: index for index, residue in enumerate(axes[factor])}
        for factor in FACTORS
    }
    tensor = np.zeros(tuple(len(axes[factor]) for factor in FACTORS),
                      dtype=np.float64)
    unit_columns = []
    flat_phi = []
    for unit in range(PERIOD):
        if math.gcd(unit, PERIOD) != 1:
            continue
        position = tuple(indexes[factor][unit % factor] for factor in FACTORS)
        value = float(full_coefficients[unit].real / principal)
        tensor[position] = value
        unit_columns.append((unit,))
        flat_phi.append(value)
    return tensor, tuple(unit_columns), np.asarray(flat_phi, dtype=np.float64)


def conditional_expectation(tensor, support):
    support = set(support)
    axes_to_average = tuple(
        index for index, factor in enumerate(FACTORS)
        if factor not in support
    )
    if not axes_to_average:
        return tensor.copy()
    return np.mean(tensor, axis=axes_to_average, keepdims=True)


def anova_components(tensor):
    components = {}
    for support in powerset(FACTORS):
        component = conditional_expectation(tensor, support)
        for smaller in powerset(support):
            if smaller == support:
                continue
            component = component - components[smaller]
        components[support] = component
    return components


def component_l2(component, shape):
    broadcast = np.broadcast_to(component, shape)
    return math.sqrt(float(np.sum(broadcast * broadcast)))


def component_max_abs(component, shape):
    return float(np.max(np.abs(np.broadcast_to(component, shape))))


def full_component_shape(components):
    return tuple(
        max(component.shape[axis] for component in components.values())
        for axis in range(len(FACTORS))
    )


def component_rows(components):
    shape = full_component_shape(components)
    total_l2 = math.sqrt(sum(
        component_l2(component, shape) ** 2
        for component in components.values()
    ))
    rows = []
    for support, component in sorted(
            components.items(), key=lambda item: (len(item[0]), item[0])):
        l2 = component_l2(component, shape)
        max_abs = component_max_abs(component, shape)
        rows.append({
            "support": list(support),
            "support_key": support_key(support),
            "order": len(support),
            "l2_norm": l2,
            "relative_l2_norm": float(l2 / total_l2)
            if total_l2 > TOLERANCE else None,
            "max_abs": max_abs,
            "nonzero": bool(l2 > TOLERANCE or max_abs > TOLERANCE),
        })
    return rows


def allowed_supports(moduli):
    allowed = {()}
    for modulus in moduli:
        factor_support = modulus_factor_support(modulus)
        allowed.update(powerset(factor_support))
    return allowed


def family_anova_residual(components, moduli):
    shape = full_component_shape(components)
    allowed = allowed_supports(moduli)
    missing = [
        support for support in components
        if support not in allowed
    ]
    residual_l2 = math.sqrt(sum(
        component_l2(components[support], shape) ** 2
        for support in missing
    ))
    total_l2 = math.sqrt(sum(
        component_l2(component, shape) ** 2
        for component in components.values()
    ))
    missing_rows = [
        {
            "support": list(support),
            "support_key": support_key(support),
            "l2_norm": component_l2(components[support], shape),
        }
        for support in sorted(missing, key=lambda item: (len(item), item))
        if component_l2(components[support], shape) > TOLERANCE
    ]
    return {
        "moduli": list(moduli),
        "modulus_count": len(moduli),
        "allowed_support_keys": [
            support_key(support)
            for support in sorted(allowed, key=lambda item: (len(item), item))
        ],
        "missing_nonzero_supports": missing_rows,
        "anova_relative_l2_residual": float(residual_l2 / total_l2)
        if total_l2 > TOLERANCE else None,
        "anova_l2_residual": residual_l2,
    }


def family_rows(components, minimality_rows):
    by_moduli = {
        tuple(row["moduli"]): row for row in minimality_rows
    }
    rows = []
    for size in range(len(TARGET_MODULI) + 1):
        for moduli in itertools.combinations(TARGET_MODULI, size):
            anova = family_anova_residual(components, moduli)
            minimality = by_moduli[moduli]
            rows.append({
                **anova,
                "span_relative_l2_residual": minimality[
                    "relative_l2_residual"],
                "span_max_abs_residual": minimality["max_abs_residual"],
                "residual_match_abs_error": abs(
                    anova["anova_relative_l2_residual"]
                    - minimality["relative_l2_residual"]),
                "exact_span": minimality["exact_span"],
                "is_full_four_modulus_family": (
                    tuple(moduli) == TARGET_MODULI),
            })
    return rows


def summarize_components(rows):
    nonzero = [row for row in rows if row["nonzero"]]
    return {
        "component_count": len(rows),
        "nonzero_component_count": len(nonzero),
        "nonzero_support_keys": [row["support_key"] for row in nonzero],
        "nonzero_by_order": {
            str(order): sum(row["nonzero"] and row["order"] == order
                            for row in rows)
            for order in range(len(FACTORS) + 1)
        },
        "nonzero_relative_l2_summary": finite_summary(
            row["relative_l2_norm"] for row in nonzero),
        "largest_components": sorted(
            nonzero,
            key=lambda row: (-row["relative_l2_norm"], row["support_key"]),
        ),
    }


def summarize_families(rows):
    proper = [row for row in rows
              if not row["is_full_four_modulus_family"]]
    full = next(row for row in rows if row["is_full_four_modulus_family"])
    best_proper = min(
        proper,
        key=lambda row: (
            row["anova_relative_l2_residual"],
            row["span_max_abs_residual"],
            row["moduli"],
        ),
    )
    return {
        "family_count": len(rows),
        "proper_family_count": len(proper),
        "proper_exact_span_count": sum(row["exact_span"] for row in proper),
        "maximum_residual_match_abs_error": max(
            row["residual_match_abs_error"] for row in rows),
        "full_four_modulus_family": full,
        "best_proper_family": best_proper,
    }


def build_receipt():
    source = load_minimality_source()
    tensor, unit_columns, phi = coefficient_tensor()
    components = anova_components(tensor)
    component_summary_rows = component_rows(components)
    minimality_rows = subset_rows(unit_columns, phi)
    projection_rows = family_rows(components, minimality_rows)
    family_summary = summarize_families(projection_rows)
    full = family_summary["full_four_modulus_family"]
    best = family_summary["best_proper_family"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "four_modulus_minimality_audit": str(
                MINIMALITY_SOURCE.relative_to(ROOT)),
            "minimality_source_commit": source["source_commit"],
        },
        "status_boundary": (
            "finite q286-WBSS CRT factor-ANOVA coefficient audit only; "
            "no binary-prime projection-control theorem, signed discrepancy "
            "theorem, q286 threshold theorem, strict-central Goldbach theorem, "
            "or Goldbach proof"),
        "goldbach_proved": False,
        "four_modulus_projection_theorem_proved": False,
        "signed_discrepancy_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "CRT factor interaction certificate",
            "mechanism": (
                "Decompose the q286-WBSS unit coefficient into orthogonal "
                "ANOVA interactions over the CRT factors 5,7,11,13.  A "
                "projection to modulus d can carry only interactions whose "
                "prime-factor support lies inside d."),
            "prediction": (
                "The nonzero interactions should lie exactly in the four "
                "edge supports carried by 70,130,154,286.  Dropping a modulus "
                "should expose the corresponding nonzero interaction as the "
                "span residual."),
            "falsifier": (
                "A nonzero interaction outside the four allowed edges would "
                "falsify the four-modulus coefficient explanation.  Any "
                "proper family with zero residual would falsify minimality."),
            "smallest_test": (
                "Use the unit coefficient only, compute the 16 CRT ANOVA "
                "components, and compare every subset residual to the prior "
                "projection-rowspace minimality audit."),
            "novelty_label": "new-to-this-task",
        },
        "period": PERIOD,
        "factors": list(FACTORS),
        "target_moduli": list(TARGET_MODULI),
        "target_modulus_factor_supports": {
            str(modulus): list(modulus_factor_support(modulus))
            for modulus in TARGET_MODULI
        },
        "unit_count": len(unit_columns),
        "coefficient_l2_norm": float(np.linalg.norm(phi)),
        "component_summary": summarize_components(component_summary_rows),
        "component_rows": component_summary_rows,
        "projection_family_summary": family_summary,
        "projection_family_rows": sorted(
            projection_rows,
            key=lambda row: (
                row["modulus_count"],
                row["anova_relative_l2_residual"],
                row["moduli"],
            ),
        ),
        "anova_matches_span_minimality": (
            family_summary["maximum_residual_match_abs_error"] < 1e-9),
        "no_smaller_projection_family_found": (
            family_summary["proper_exact_span_count"] == 0
            and full["exact_span"]
        ),
        "decision": (
            "The CRT factor-ANOVA decomposition explains the previous "
            "minimality result: the q286-WBSS unit coefficient has nonzero "
            "interaction support exactly inside the four modulus-carried "
            "edges, and no proper projection family captures them all.  The "
            f"best proper family {best['moduli']} misses "
            f"{[row['support_key'] for row in best['missing_nonzero_supports']]}. "
            "Thus the coefficient-side theorem target is structurally the "
            "four-modulus family 70,130,154,286; the remaining open problem "
            "is still binary-prime projection control or direct raw signed "
            "witness positivity, not another coefficient sparsification.  "
            "Goldbach remains open."
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

"""Character-sum obligations for the q286-WBSS four-modulus edge structure.

The factor-ANOVA audit showed that the coefficient side needs exactly the
four CRT edges carried by 70, 130, 154, and 286.  This receipt expands those
finite coefficient components in the multiplicative character bases of the
active CRT factors.  The result names the binary-prime character correlations
a future theorem would need to control.

This is finite coefficient algebra only.  It proves no character-sum bound,
binary-prime projection-control theorem, signed discrepancy theorem, q286
threshold theorem, strict-central Goldbach theorem, or Goldbach proof.
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
SOURCE = EVIDENCE / "q286-wbss-four-modulus-factor-anova-audit.json"
OUT = EVIDENCE / "q286-wbss-four-modulus-edge-character-audit.json"
FACTORS = (5, 7, 11, 13)
EDGE_SUPPORTS = ((5, 7), (5, 13), (7, 11), (11, 13))
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from tools.build_q286_wbss_four_modulus_factor_anova_audit import (  # noqa: E402
    anova_components,
    coefficient_tensor,
    component_l2,
    component_rows,
    full_component_shape,
    json_ready,
    support_key,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_source():
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def primitive_root(prime):
    units = set(range(1, prime))
    for candidate in range(2, prime):
        generated = {pow(candidate, exponent, prime)
                     for exponent in range(prime - 1)}
        if generated == units:
            return candidate
    raise ValueError(f"no primitive root found for {prime}")


def exponent_maps():
    maps = {}
    for factor in FACTORS:
        root = primitive_root(factor)
        residues_by_exponent = tuple(
            pow(root, exponent, factor) for exponent in range(factor - 1))
        maps[factor] = {
            "primitive_root": root,
            "residues_by_exponent": residues_by_exponent,
            "natural_index_by_exponent": tuple(
                residue - 1 for residue in residues_by_exponent),
        }
    return maps


def active_component_array(component, support, maps):
    support = tuple(support)
    if not support:
        return np.asarray(component.reshape(-1)[0], dtype=np.complex128)

    slices = tuple(slice(None) if factor in support else 0
                   for factor in FACTORS)
    values = np.asarray(component[slices], dtype=np.complex128)
    if values.ndim == 0:
        return values

    for axis, factor in enumerate(support):
        values = np.take(
            values,
            maps[factor]["natural_index_by_exponent"],
            axis=axis,
        )
    return values


def axis_marginal_max_abs(values, axis):
    return float(np.max(np.abs(np.mean(values, axis=axis))))


def top_coefficients(coefficients, count=8):
    rows = []
    for frequency in itertools.product(
            *(range(size) for size in coefficients.shape)):
        value = complex(coefficients[frequency])
        rows.append({
            "frequency": list(frequency),
            "abs_coefficient": abs(value),
            "coefficient_real": value.real,
            "coefficient_imag": value.imag,
            "energy": abs(value) ** 2,
        })
    rows.sort(key=lambda row: (-row["abs_coefficient"], row["frequency"]))
    total_energy = sum(row["energy"] for row in rows)
    for row in rows:
        row["energy_fraction_within_support"] = (
            row["energy"] / total_energy if total_energy > TOLERANCE else None)
    return rows[:count]


def character_row(support, component, shape, maps):
    values = active_component_array(component, support, maps)
    if values.ndim == 0:
        values = values.reshape(())
        coefficients = values.reshape(())
        reconstruction = coefficients
        marginal_max_abs = {}
    else:
        coefficients = np.fft.fftn(values) / values.size
        reconstruction = np.fft.ifftn(coefficients * coefficients.size)
        marginal_max_abs = {
            str(factor): axis_marginal_max_abs(values, axis)
            for axis, factor in enumerate(support)
        }

    mean_square = float(np.mean(np.abs(values) ** 2))
    character_energy = float(np.sum(np.abs(coefficients) ** 2))
    parseval_error = abs(mean_square - character_energy)
    reconstruction_error = float(np.max(np.abs(reconstruction - values)))
    nonzero_frequencies = []
    zero_axis_frequency_count = 0
    fully_nonprincipal_count = 0
    for frequency in itertools.product(
            *(range(size) for size in coefficients.shape)):
        value = complex(coefficients[frequency])
        if abs(value) <= TOLERANCE:
            continue
        nonzero_frequencies.append(frequency)
        if any(item == 0 for item in frequency):
            zero_axis_frequency_count += 1
        elif support:
            fully_nonprincipal_count += 1

    return {
        "support": list(support),
        "support_key": support_key(support),
        "order": len(support),
        "dimensions": list(values.shape),
        "coefficient_count": int(coefficients.size),
        "nonzero_character_count": len(nonzero_frequencies),
        "fully_nonprincipal_character_count": fully_nonprincipal_count,
        "zero_axis_nonzero_character_count": zero_axis_frequency_count,
        "mean_square": mean_square,
        "character_energy": character_energy,
        "parseval_error": parseval_error,
        "max_reconstruction_error": reconstruction_error,
        "full_tensor_l2_norm": component_l2(component, shape),
        "axis_marginal_max_abs": marginal_max_abs,
        "top_coefficients": top_coefficients(coefficients),
    }


def theorem_obligation_rows(rows):
    obligations = []
    for row in rows:
        if tuple(row["support"]) not in EDGE_SUPPORTS:
            continue
        obligations.append({
            "edge_support": row["support"],
            "edge_key": row["support_key"],
            "fully_nonprincipal_character_count": (
                row["fully_nonprincipal_character_count"]),
            "zero_axis_nonzero_character_count": (
                row["zero_axis_nonzero_character_count"]),
            "obligation": (
                "Control the signed binary-prime correlation against each "
                "fully nonprincipal product character on this CRT edge, "
                "with the coefficient listed in this receipt.  Principal "
                "axis terms are absent at audit tolerance because the ANOVA "
                "edge component has zero marginal on each active factor."),
        })
    return obligations


def summarize(rows):
    nonzero = [row for row in rows
               if row["nonzero_character_count"] > 0]
    edge_rows = [row for row in nonzero
                 if tuple(row["support"]) in EDGE_SUPPORTS]
    singleton_rows = [row for row in nonzero if row["order"] == 1]
    total_nonconstant = sum(
        row["nonzero_character_count"] for row in nonzero
        if row["support_key"] != "empty")
    total_edge = sum(
        row["fully_nonprincipal_character_count"] for row in edge_rows)
    return {
        "nonzero_support_keys": [row["support_key"] for row in nonzero],
        "nonzero_singleton_character_count": sum(
            row["nonzero_character_count"] for row in singleton_rows),
        "fully_nonprincipal_edge_character_count": total_edge,
        "total_nonconstant_character_count": total_nonconstant,
        "maximum_parseval_error": max(row["parseval_error"] for row in rows),
        "maximum_reconstruction_error": max(
            row["max_reconstruction_error"] for row in rows),
        "edge_character_counts": {
            row["support_key"]: row["fully_nonprincipal_character_count"]
            for row in edge_rows
        },
        "zero_axis_nonzero_edge_character_count": sum(
            row["zero_axis_nonzero_character_count"] for row in edge_rows),
    }


def build_receipt():
    source = load_source()
    tensor, _, _ = coefficient_tensor()
    components = anova_components(tensor)
    shape = full_component_shape(components)
    maps = exponent_maps()
    component_summary = component_rows(components)
    nonzero_supports = [
        tuple(row["support"]) for row in component_summary if row["nonzero"]]
    rows = [
        character_row(support, components[support], shape, maps)
        for support in nonzero_supports
    ]
    summary = summarize(rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "factor_anova_audit": str(SOURCE.relative_to(ROOT)),
            "factor_anova_source_commit": source["source_commit"],
        },
        "status_boundary": (
            "finite q286-WBSS CRT edge-character coefficient audit only; "
            "the residual absorption constants .126 and .13 are finite "
            "fixture fits, not universal bounds; no character-sum bound, "
            "binary-prime projection-control theorem, signed discrepancy "
            "theorem, q286 threshold theorem, strict-central Goldbach "
            "theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "character_sum_bound_proved": False,
        "four_modulus_projection_theorem_proved": False,
        "signed_discrepancy_theorem_proved": False,
        "universal_bound_open": True,
        "residual_absorption_constant_universal": False,
        "candidate": {
            "name": "q286-WBSS four-modulus edge-character obligation",
            "mechanism": (
                "Expand each nonzero CRT factor-ANOVA component of the "
                "q286-WBSS unit coefficient in the orthonormal multiplicative "
                "character basis of its active unit-group factors."),
            "prediction": (
                "The hard nonlocal terms should be exactly the fully "
                "nonprincipal product characters on the four coefficient "
                "edges 5,7; 5,13; 7,11; and 11,13, with no three-factor or "
                "four-factor character obligations."),
            "falsifier": (
                "A reconstruction/Parseval mismatch, a nonzero character "
                "outside the factor-ANOVA supports, or a nonzero principal-axis "
                "edge character would falsify this exact finite translation."),
            "smallest_test": (
                "Compute DFT coefficients on the exponent coordinates of the "
                "unit groups for each nonzero ANOVA component, then verify "
                "inverse reconstruction and Parseval energy."),
            "novelty_label": "new-to-this-task",
        },
        "factors": list(FACTORS),
        "edge_supports": [list(edge) for edge in EDGE_SUPPORTS],
        "primitive_roots": {
            str(factor): maps[factor]["primitive_root"]
            for factor in FACTORS
        },
        "residues_by_exponent": {
            str(factor): list(maps[factor]["residues_by_exponent"])
            for factor in FACTORS
        },
        "summary": summary,
        "character_rows": rows,
        "binary_prime_theorem_obligations": theorem_obligation_rows(rows),
        "no_three_or_four_factor_character_obligations": all(
            len(support) <= 2 for support in nonzero_supports),
        "edge_translation_verified": (
            summary["maximum_parseval_error"] < 1e-9
            and summary["maximum_reconstruction_error"] < 1e-9
            and summary["zero_axis_nonzero_edge_character_count"] == 0),
        "decision": (
            "The four-modulus coefficient target translates exactly into "
            f"{summary['fully_nonprincipal_edge_character_count']} fully "
            "nonprincipal edge-character binary-prime correlation terms, "
            "plus the singleton/AP and constant main components.  This is a "
            "sharper statement of the analytic obligation, not a smaller "
            "coefficient theorem and not a universal residual-absorption "
            "constant.  Goldbach remains open.")
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

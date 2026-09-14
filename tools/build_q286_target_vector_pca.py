"""Run small selected-target PCA/SVD diagnostics for q286 vector overlays.

This is a visualization/navigation aid.  It asks whether the selected boundary
failures and late successes separate along simple measured coordinates.  It
does not infer a theorem from a tiny selected fixture.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def standardize(matrix):
    array = np.asarray(matrix, dtype=float)
    means = np.mean(array, axis=0)
    scales = np.std(array, axis=0, ddof=0)
    safe_scales = np.where(scales > 0, scales, 1.0)
    return (array - means) / safe_scales, means, safe_scales


def run_pca(row_specs, feature_names):
    matrix = [[spec["features"][name] for name in feature_names]
              for spec in row_specs]
    standardized, means, scales = standardize(matrix)
    _, singular_values, vt = np.linalg.svd(standardized, full_matrices=False)
    scores = standardized @ vt.T
    eigenvalues = (singular_values ** 2) / max(1, len(row_specs) - 1)
    total = float(np.sum(eigenvalues))
    explained = (
        [float(value / total) for value in eigenvalues]
        if total > 0 else [0.0 for _ in eigenvalues])
    rows = []
    for index, spec in enumerate(row_specs):
        rows.append({
            "target": spec["target"],
            "role": spec["role"],
            "shape": spec["shape"],
            "glow": spec["glow"],
            "pc1": float(scores[index, 0]) if scores.shape[1] >= 1 else 0.0,
            "pc2": float(scores[index, 1]) if scores.shape[1] >= 2 else 0.0,
            "features": spec["features"],
        })
    loadings = []
    for component_index in range(min(3, vt.shape[0])):
        loading = {
            feature_names[feature_index]: float(vt[component_index, feature_index])
            for feature_index in range(len(feature_names))
        }
        loadings.append({
            "component": component_index + 1,
            "explained_variance_fraction": explained[component_index],
            "loadings": loading,
            "dominant_positive_feature": max(
                loading, key=lambda key: loading[key]),
            "dominant_negative_feature": min(
                loading, key=lambda key: loading[key]),
        })
    return {
        "feature_names": feature_names,
        "feature_means": {
            name: float(means[index]) for index, name in enumerate(feature_names)},
        "feature_scales": {
            name: float(scales[index]) for index, name in enumerate(feature_names)},
        "explained_variance_fraction": explained,
        "component_loadings": loadings,
        "rows": rows,
    }


def selected_rows(overlay, targets, required_sections=()):
    rows = []
    for target in targets:
        row = overlay["target_rows"][str(target)]
        if any(section not in row for section in required_sections):
            continue
        rows.append(row)
    return rows


def alignment_feature_rows(rows):
    specs = []
    for row in rows:
        coordinates = row["coordinates"]
        specs.append({
            "target": row["target"],
            "role": row["role"],
            "shape": row["shape"],
            "glow": row["glow"],
            "features": {
                "first_three": coordinates["first_three"],
                "complement": coordinates["complement"],
                "full": coordinates["full"],
                "certificate_margin": coordinates["certificate_margin"],
                "l2_negative_bound_utilization": coordinates[
                    "l2_negative_bound_utilization"],
                "l2_to_sufficient_ratio": coordinates[
                    "l2_to_sufficient_ratio"],
            },
        })
    return specs


def component_feature_rows(rows):
    specs = []
    for row in rows:
        lower = row["lower_support"]
        component = row["component_actions"]
        specs.append({
            "target": row["target"],
            "role": row["role"],
            "shape": row["shape"],
            "glow": row["glow"],
            "features": {
                "first_three": row["coordinates"]["first_three"],
                "full": row["coordinates"]["full"],
                "visible_lower_package": lower["visible_lower_package"],
                "lower_package_rescue_margin": lower[
                    "lower_package_rescue_margin"],
                "component_57_centered": component["(5,7)_centered"],
                "component_711_centered": component["(7,11)_centered"],
                "centered_lower_support": component[
                    "centered_lower_support"],
            },
        })
    return specs


def role_separation(rows):
    if not rows:
        return {}
    by_role = {}
    for row in rows:
        by_role.setdefault(row["role"], []).append(row)
    centers = {}
    for role, values in by_role.items():
        centers[role] = {
            "count": len(values),
            "pc1_mean": math.fsum(value["pc1"] for value in values) / len(values),
            "pc2_mean": math.fsum(value["pc2"] for value in values) / len(values),
        }
    return centers


def main():
    overlay = load_json(EVIDENCE / "q286-target-vector-overlay.json")
    alignment_targets = overlay["targets"]
    component_targets = (10664, 14138, 1222142, 1323632, 1379072)

    alignment_specs = alignment_feature_rows(
        selected_rows(overlay, alignment_targets))
    component_specs = component_feature_rows(
        selected_rows(overlay, component_targets,
                      required_sections=("lower_support", "component_actions")))

    alignment_pca = run_pca(
        alignment_specs,
        (
            "first_three",
            "complement",
            "full",
            "certificate_margin",
            "l2_negative_bound_utilization",
            "l2_to_sufficient_ratio",
        ))
    component_pca = run_pca(
        component_specs,
        (
            "first_three",
            "full",
            "visible_lower_package",
            "lower_package_rescue_margin",
            "component_57_centered",
            "component_711_centered",
            "centered_lower_support",
        ))
    alignment_pca["role_centers"] = role_separation(alignment_pca["rows"])
    component_pca["role_centers"] = role_separation(component_pca["rows"])

    output = {
        "schema_version": 1,
        "receipt": "q286-target-vector-pca",
        "generated_from_commit": source_commit(),
        "purpose": (
            "Small selected-target PCA/SVD diagnostic for q286 visualization. "
            "It tests whether measured vector coordinates separate boundary "
            "failures from late/alignment successes."),
        "alignment_dataset": alignment_pca,
        "component_dataset": component_pca,
        "interpretation_boundary": (
            "This PCA uses selected finite targets only.  It can suggest a "
            "visual coordinate system or a falsifier direction, but it does "
            "not prove a distribution theorem, signed prime-correlation "
            "estimate, strict closure, outer assembly, or Goldbach."),
        "goldbach_proved": False,
    }
    out_path = EVIDENCE / "q286-target-vector-pca.json"
    with out_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(output, handle, indent=2)
        handle.write("\n")
    print(out_path.relative_to(ROOT))


if __name__ == "__main__":
    main()

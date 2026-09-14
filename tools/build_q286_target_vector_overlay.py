"""Build selected q286 target vector overlay data.

This complements the glow map.  The glow map says where evidence layers stack;
this overlay records selected target coordinates so stacked points can also
have direction and shape.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_lower_support_package_component_local_discrepancy_receipt,
    q286_selected_alignment_complement_certificate_receipt,
    q286_subcone_lower_support_package_receipt,
)

TARGETS = (10664, 14138, 70526, 1222142, 1323632, 1379072, 1426262, 3305200)
LOWER_COMPONENT_TARGETS = (10664, 14138, 1222142, 1323632, 1379072)


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def role_for_target(target):
    if target in (10664, 14138):
        return "boundary_failure"
    if target in (1222142, 1323632, 1379072):
        return "late_active_success"
    if target in (70526, 1426262, 3305200):
        return "alignment_stress_success"
    return "selected_target"


def shape_for_role(role):
    return {
        "boundary_failure": "down_triangle",
        "late_active_success": "circle",
        "alignment_stress_success": "diamond",
    }.get(role, "square")


def component_key(component_rows, support):
    support = tuple(support)
    if support in component_rows:
        return support
    text = str(support)
    if text in component_rows:
        return text
    compact_text = "(" + ", ".join(str(value) for value in support) + ")"
    if compact_text in component_rows:
        return compact_text
    raise KeyError(f"component support not found: {support}")


def main():
    glow = load_json(EVIDENCE / "q286-evidence-glow-map.json")
    strict = load_json(
        EVIDENCE / "q286-active-lane-strict-closure-margin-census-selected-late.json")
    fixed = load_json(EVIDENCE / "q286-fixed-inequality-target-window-census.json")

    alignment = q286_selected_alignment_complement_certificate_receipt(
        targets=TARGETS, alignment_ceiling=.4)
    package = q286_subcone_lower_support_package_receipt(
        targets=LOWER_COMPONENT_TARGETS)
    component = q286_lower_support_package_component_local_discrepancy_receipt(
        targets=LOWER_COMPONENT_TARGETS)

    glow_by_target = {
        int(row["id"]): row for row in glow["target_stacks"]}
    rows = {}
    for target in TARGETS:
        role = role_for_target(target)
        alignment_row = alignment["target_rows"][target]
        row = {
            "target": target,
            "role": role,
            "shape": shape_for_role(role),
            "glow": glow_by_target.get(target, {}).get("glow", 0.0),
            "stack_weight": glow_by_target.get(target, {}).get(
                "stack_weight", 0.0),
            "coordinates": {
                "first_three": alignment_row[
                    "first_three_to_principal_ratio"],
                "complement": alignment_row[
                    "complement_to_principal_ratio"],
                "full": alignment_row["full_action_to_principal_ratio"],
                "l2_bound": alignment_row["l2_bound_to_principal"],
                "alignment_bound_0_4": alignment_row[
                    "alignment_ceiling_bound_to_principal"],
                "certificate_margin": alignment_row[
                    "certificate_margin_to_principal"],
                "l2_negative_bound_utilization": alignment_row[
                    "l2_negative_bound_utilization"],
                "l2_to_sufficient_ratio": alignment_row[
                    "l2_to_sufficient_ratio"],
            },
            "signs": {
                "full_positive": alignment_row[
                    "actual_full_action_positive"],
                "alignment_complement_certified": alignment_row[
                    "certified_positive_by_alignment_complement"],
            },
            "boundary": (
                "Selected finite vector row only; not a universal theorem."),
        }
        if target in package["rows"]:
            package_row = package["rows"][target]
            row["lower_support"] = {
                "first_two": package_row[
                    "first_two_modes_to_principal_ratio"],
                "visible_lower_package": package_row[
                    "visible_lower_support_package_to_principal_ratio"],
                "required_lower_package": package_row[
                    "required_lower_support_package_to_rescue"],
                "lower_package_rescue_margin": package_row[
                    "lower_support_package_rescue_margin_to_principal_ratio"],
                "q70": package_row["q70_to_principal_ratio"],
                "q154": package_row["q154_to_principal_ratio"],
                "small_support": package_row[
                    "small_support_to_principal_ratio"],
                "subcone_member": package_row["subcone_member"],
                "rescued_without_q70": package_row["rescued_without_q70"],
            }
        if target in component["rows"]:
            component_row = component["rows"][target]
            components = component_row["component_rows"]
            support_57 = component_key(components, (5, 7))
            support_711 = component_key(components, (7, 11))
            row["component_actions"] = {
                "local_mean_lower_support": component_row[
                    "local_mean_lower_support_to_principal_ratio"],
                "centered_lower_support": component_row[
                    "centered_lower_support_action_to_principal_ratio"],
                "dominant_positive_centered_support": component_row[
                    "dominant_positive_centered_support"],
                "dominant_negative_centered_support": component_row[
                    "dominant_negative_centered_support"],
                "(5,7)_centered": components[support_57][
                    "centered_action_to_principal_ratio"],
                "(7,11)_centered": components[support_711][
                    "centered_action_to_principal_ratio"],
            }
        if str(target) in strict["target_rows"]:
            strict_row = strict["target_rows"][str(target)]
            row["strict_closure"] = {
                "driver_margin": strict_row[
                    "driver_margin_to_calibrated_floor"],
                "channel_margin_contribution": strict_row[
                    "channel_margin_contribution_to_strict_closure"],
                "strict_margin": strict_row[
                    "strict_closure_margin_to_calibrated_endpoint"],
                "dominant_margin_source": strict_row[
                    "dominant_strict_margin_source"],
            }
        if str(target) in fixed["target_rows"]:
            fixed_row = fixed["target_rows"][str(target)]
            row["fixed_inequality"] = {
                "status": fixed_row["status"],
                "worst_margin": fixed_row["worst_margin"],
                "polygon_row_count": fixed_row["polygon_row_count"],
            }
        rows[str(target)] = row

    output = {
        "schema_version": 1,
        "receipt": "q286-target-vector-overlay",
        "generated_from_commit": source_commit(),
        "purpose": (
            "Selected target vector coordinates for superimposed q286 evidence "
            "visualization.  Shapes encode role; glow is imported from the "
            "stacked evidence map; coordinates come from executable receipts."),
        "targets": TARGETS,
        "coordinate_legend": {
            "x_suggestion": "first_three",
            "y_suggestion": "complement or full",
            "radius_suggestion": "glow or stack_weight",
            "shape_suggestion": "shape",
            "color_lane_suggestion": "role",
            "vector_suggestion": (
                "Use (5,7)_centered and (7,11)_centered as component-plane "
                "arrows where present; use driver/channel strict-closure "
                "margins as a second vector field for active rows."),
            "attention_bias_warning": (
                "Do not infer importance from repeated manual attention.  "
                "Use denominator fields and independent receipt layers to "
                "separate evidence glow from attention glow."),
        },
        "target_rows": rows,
        "source_receipts": {
            "alignment_complement": (
                "q286_selected_alignment_complement_certificate_receipt"),
            "lower_support_package": (
                "q286_subcone_lower_support_package_receipt"),
            "component_local_discrepancy": (
                "q286_lower_support_package_component_local_discrepancy_receipt"),
            "strict_closure": (
                "evidence/q286-active-lane-strict-closure-margin-census-selected-late.json"),
            "fixed_inequality": (
                "evidence/q286-fixed-inequality-target-window-census.json"),
            "glow": "evidence/q286-evidence-glow-map.json",
        },
        "status_boundary": (
            "Finite selected target vectors only.  This helps visual comparison "
            "of mechanisms and falsifiers; it does not prove pointwise signed "
            "prime correlation, strict closure, outer assembly, or Goldbach."),
        "goldbach_proved": False,
    }

    out_path = EVIDENCE / "q286-target-vector-overlay.json"
    with out_path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(output, handle, indent=2)
        handle.write("\n")
    print(out_path.relative_to(ROOT))


if __name__ == "__main__":
    main()

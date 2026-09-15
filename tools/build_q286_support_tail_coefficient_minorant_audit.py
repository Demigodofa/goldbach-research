"""Audit coefficientwise q286 support-tail control.

The row evidence suggests a later support-tail stability threshold, but a
stronger shortcut would be much better: prove positivity for every nonnegative
prime-pair residue measure by showing the coefficient itself is positive on
each admissible support.

This receipt tests that coefficientwise shortcut for

    A = P + D + R,
    D = E_286 + E_154 + E_70,
    R = E_14 + E_26 + E_130 + E_10 + E_22.

It is a finite coefficient audit only.  It proves no signed prime-correlation
estimate, q286 threshold theorem, strict-central Goldbach theorem, or Goldbach.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-support-tail-coefficient-minorant-audit.json"
PERIOD = 10010
TOLERANCE = 1e-8

sys.path.insert(0, str(ROOT / "tools"))

from build_q286_three_support_action_decomposition import (  # noqa: E402
    build_components,
    json_ready,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def finite_summary(values):
    values = tuple(float(value) for value in values)
    if not values:
        return {
            "count": 0,
            "minimum": None,
            "maximum": None,
            "mean": None,
        }
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def admissible_units(target_residue, units):
    return tuple(
        unit for unit in units
        if math.gcd((target_residue - unit) % PERIOD, PERIOD) == 1)


def sign_counts(values):
    values = tuple(float(value) for value in values)
    return {
        "negative_count": sum(value < -TOLERANCE for value in values),
        "positive_count": sum(value > TOLERANCE for value in values),
        "zero_count": sum(abs(value) <= TOLERANCE for value in values),
    }


def build_receipt(tolerance=TOLERANCE):
    built = build_components(tolerance)
    units = built["units"]
    components = built["components"]
    top_three = tuple(built["top_three_labels"])
    principal = components["principal"]
    principal_real = np.asarray([value.real for value in principal])
    if float(np.min(principal_real)) <= tolerance:
        raise AssertionError("expected positive principal coefficient")
    dominant = np.zeros(len(units), dtype=np.complex128)
    for label in top_three:
        dominant += components[label]
    tail_labels = tuple(
        label for label in components
        if label not in ("principal", *top_three))
    tail = np.zeros(len(units), dtype=np.complex128)
    for label in tail_labels:
        tail += components[label]
    partial = principal + dominant
    full = partial + tail
    unit_index = {unit: index for index, unit in enumerate(units)}
    unit_rows = []
    for unit, p_value, d_value, r_value, full_value in zip(
            units, principal, dominant, tail, full):
        principal_scale = p_value.real
        unit_rows.append({
            "unit": int(unit),
            "principal_plus_dominant_to_principal_ratio": float(
                (p_value.real + d_value.real) / principal_scale),
            "dominant_to_principal_ratio": float(
                d_value.real / principal_scale),
            "support_tail_to_principal_ratio": float(
                r_value.real / principal_scale),
            "full_to_principal_ratio": float(
                full_value.real / principal_scale),
        })

    target_rows = []
    for target_residue in range(0, PERIOD, 2):
        support = admissible_units(target_residue, units)
        indices = [unit_index[unit] for unit in support]
        partial_ratios = [
            unit_rows[index][
                "principal_plus_dominant_to_principal_ratio"]
            for index in indices]
        tail_ratios = [
            unit_rows[index]["support_tail_to_principal_ratio"]
            for index in indices]
        full_ratios = [
            unit_rows[index]["full_to_principal_ratio"]
            for index in indices]
        partial_min = min(partial_ratios)
        tail_min = min(tail_ratios)
        full_min = min(full_ratios)
        separated_tail_control = (
            partial_min > tolerance
            and tail_min > -partial_min + tolerance)
        target_rows.append({
            "target_residue": int(target_residue),
            "admissible_support_size": len(indices),
            "partial_ratio_summary": finite_summary(partial_ratios),
            "tail_ratio_summary": finite_summary(tail_ratios),
            "full_ratio_summary": finite_summary(full_ratios),
            "partial_sign_counts": sign_counts(partial_ratios),
            "tail_sign_counts": sign_counts(tail_ratios),
            "full_sign_counts": sign_counts(full_ratios),
            "partial_coefficients_all_positive": all(
                value > tolerance for value in partial_ratios),
            "full_coefficients_all_positive": all(
                value > tolerance for value in full_ratios),
            "separated_tail_control_passes": separated_tail_control,
            "separated_tail_control_margin": (
                partial_min + tail_min),
        })

    partial_all_positive_count = sum(
        row["partial_coefficients_all_positive"] for row in target_rows)
    full_all_positive_count = sum(
        row["full_coefficients_all_positive"] for row in target_rows)
    separated_pass_count = sum(
        row["separated_tail_control_passes"] for row in target_rows)
    worst_full = min(
        target_rows, key=lambda row: row["full_ratio_summary"]["minimum"])
    worst_partial = min(
        target_rows, key=lambda row: row["partial_ratio_summary"]["minimum"])
    worst_separated = min(
        target_rows, key=lambda row: row["separated_tail_control_margin"])

    global_partial_ratios = [
        row["principal_plus_dominant_to_principal_ratio"]
        for row in unit_rows]
    global_tail_ratios = [
        row["support_tail_to_principal_ratio"] for row in unit_rows]
    global_full_ratios = [
        row["full_to_principal_ratio"] for row in unit_rows]
    shortcut_falsified = (
        full_all_positive_count < len(target_rows)
        and separated_pass_count < len(target_rows))

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "arithmetic_period": PERIOD,
        "unit_group_order": len(units),
        "even_target_residue_count": len(target_rows),
        "top_three_support_labels": top_three,
        "tail_support_labels": tail_labels,
        "question": (
            "Can the q286 signed support-tail control theorem be replaced by "
            "a coefficientwise nonnegative-weight certificate over every "
            "admissible residue support?"),
        "mechanism": (
            "Split the fixed coefficient into principal, dominant supports "
            "286/154/70, and lower-support tail.  For each even target "
            "residue a, inspect all admissible unit residues r in A_a."),
        "coefficientwise_sufficient_conditions": {
            "full_minorant": (
                "full coefficient ratio > 0 on every r in A_a"),
            "separated_tail_control": (
                "min_r(1+d(r)) > 0 and min_r r_tail(r) > "
                "-min_r(1+d(r))"),
        },
        "global_unit_ratio_summaries": {
            "principal_plus_dominant": finite_summary(
                global_partial_ratios),
            "support_tail": finite_summary(global_tail_ratios),
            "full": finite_summary(global_full_ratios),
        },
        "target_residue_counts": {
            "partial_coefficients_all_positive": partial_all_positive_count,
            "full_coefficients_all_positive": full_all_positive_count,
            "separated_tail_control_passes": separated_pass_count,
            "total_even_residues": len(target_rows),
        },
        "worst_rows": {
            "worst_full_ratio_row": worst_full,
            "worst_partial_ratio_row": worst_partial,
            "worst_separated_tail_control_margin_row": worst_separated,
        },
        "selected_target_residue_rows": [
            row for row in target_rows
            if row["target_residue"] in sorted({
                88346 % PERIOD,
                90080 % PERIOD,
                94856 % PERIOD,
                250240 % PERIOD,
                255704 % PERIOD,
            })
        ],
        "prediction": (
            "If the coefficientwise shortcut were viable, all 5005 even "
            "target residues would pass full_minorant or at least the "
            "separated tail-control condition."),
        "falsifier": (
            "Any target residue with an admissible unit where the full "
            "coefficient is nonpositive falsifies the full-minorant shortcut; "
            "any residue failing min-tail > -min-partial falsifies the "
            "separated coefficientwise tail-control shortcut."),
        "decision": (
            "The coefficientwise shortcut is falsified; actual prime-pair "
            "mass distribution is still required."
            if shortcut_falsified else
            "The coefficientwise shortcut survives this audit."),
        "status_boundary": (
            "finite coefficient-side audit only; no signed prime-correlation "
            "estimate, no q286 threshold theorem, no strict-central Goldbach "
            "theorem, and no Goldbach proof"),
        "coefficientwise_tail_control_shortcut_falsified": (
            shortcut_falsified),
        "signed_prime_pair_distribution_still_required": (
            shortcut_falsified),
        "signed_tail_control_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    receipt = build_receipt()
    OUT.write_text(
        json.dumps(json_ready(receipt), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(json.dumps(json_ready({
        "wrote": str(OUT.relative_to(ROOT)),
        "partial_coefficients_all_positive": receipt[
            "target_residue_counts"][
                "partial_coefficients_all_positive"],
        "full_coefficients_all_positive": receipt[
            "target_residue_counts"]["full_coefficients_all_positive"],
        "separated_tail_control_passes": receipt[
            "target_residue_counts"]["separated_tail_control_passes"],
        "coefficientwise_tail_control_shortcut_falsified": receipt[
            "coefficientwise_tail_control_shortcut_falsified"],
        "goldbach_proved": receipt["goldbach_proved"],
    }), sort_keys=True))


if __name__ == "__main__":
    main()

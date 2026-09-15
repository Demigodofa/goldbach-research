"""Audit the q286 LP cone against local singular/admissible structure.

Kevin's singular-series/good-cone framing suggests that the frozen LP cone
may be seeing the local admissible residue cone rather than only fitted data.
This receipt pushes the target-conditioned locally admissible residue measure
through the same C10 x C12 real character labels, subtracts the stress target,
and compares that local delta action with the frozen LP vector.

This is a finite local/empirical diagnostic only.  It proves no singular
series theorem, LP cone theorem, interpolation theorem, residual-bound theorem,
signed projection theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DICTIONARY_SOURCE = ROOT / "evidence" / "q286-lift-project-dictionary-audit.json"
LP_SOURCE = ROOT / "evidence" / "q286-low-frequency-lp-cone-audit.json"
STRESS_HOLDOUT_SOURCE = (
    ROOT / "evidence" / "q286-low-frequency-lp-cone-stress-holdout.json")
OUT = ROOT / "evidence" / "q286-lp-cone-local-singular-audit.json"
MODULUS = 286
ODD_MODULUS = 143
LOCAL_PRIMES = (11, 13)
STRESS_TARGET = 1222142
CAP_TO_TEST = 0.75
TOLERANCE = 1e-12
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_frequency_resolved_fourier import (  # noqa: E402
    _unit_character_table,
)
from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_above_floor_holdout_census_receipt,
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set)):
        return [json_ready(item) for item in value]
    if isinstance(value, np.ndarray):
        return json_ready(value.tolist())
    if isinstance(value, np.generic):
        return json_ready(value.item())
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def label_tuple(label):
    return tuple(int(part) for part in label)


def contribution_map(row):
    return {
        label_tuple(item["representative_label"]): float(
            item["contribution_to_principal_ratio"])
        for item in row["real_channel_contribution_rows"]
    }


def finite_summary(values):
    values = tuple(float(value) for value in values)
    finite = tuple(value for value in values if math.isfinite(value))
    if not finite:
        return {
            "count": len(values),
            "finite_count": 0,
            "nonfinite_count": len(values),
            "minimum": None,
            "maximum": None,
            "mean": None,
        }
    return {
        "count": len(values),
        "finite_count": len(finite),
        "nonfinite_count": len(values) - len(finite),
        "minimum": min(finite),
        "maximum": max(finite),
        "mean": math.fsum(finite) / len(finite),
    }


def min_record(rows, key):
    finite_rows = tuple(
        row for row in rows
        if row[key] is not None and math.isfinite(float(row[key])))
    if not finite_rows:
        return {"n_mod_143": None, "value": None}
    row = min(finite_rows, key=lambda item: (item[key], item["n_mod_143"]))
    return {"n_mod_143": row["n_mod_143"], "value": row[key]}


def max_record(rows, key):
    finite_rows = tuple(
        row for row in rows
        if row[key] is not None and math.isfinite(float(row[key])))
    if not finite_rows:
        return {"n_mod_143": None, "value": None}
    row = max(finite_rows, key=lambda item: (item[key], -item["n_mod_143"]))
    return {"n_mod_143": row["n_mod_143"], "value": row[key]}


def target_min_record(rows, key):
    row = min(rows, key=lambda item: (item[key], item["target"]))
    return {"target": row["target"], "value": row[key]}


def target_max_record(rows, key):
    row = max(rows, key=lambda item: (item[key], -item["target"]))
    return {"target": row["target"], "value": row[key]}


def cosine(a, b):
    a = np.asarray(a, dtype=np.float64).reshape(-1)
    b = np.asarray(b, dtype=np.float64).reshape(-1)
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    return None if denom <= TOLERANCE else float(np.dot(a, b) / denom)


def pearson(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    ac = a - float(np.mean(a))
    bc = b - float(np.mean(b))
    denom = float(np.linalg.norm(ac) * np.linalg.norm(bc))
    return None if denom <= TOLERANCE else float(np.dot(ac, bc) / denom)


def rankdata(values):
    values = np.asarray(values, dtype=np.float64)
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=np.float64)
    index = 0
    while index < len(values):
        end = index + 1
        while end < len(values) and values[order[end]] == values[order[index]]:
            end += 1
        rank = (index + end - 1) / 2.0
        ranks[order[index:end]] = rank
        index = end
    return ranks


def spearman(a, b):
    return pearson(rankdata(a), rankdata(b))


def locally_admissible_units(units, n_mod_143):
    return tuple(
        unit for unit in units
        if math.gcd((int(n_mod_143) - int(unit)) % ODD_MODULUS,
                    ODD_MODULUS) == 1)


def local_singular_multiplier(n_mod_143):
    value = 1.0
    for prime in LOCAL_PRIMES:
        if n_mod_143 % prime == 0:
            value *= (prime - 1) / (prime - 2)
    return value


def local_vector(n_mod_143, outside_labels, units, unit_to_column,
                 label_to_row, character_table):
    admissible = locally_admissible_units(units, n_mod_143)
    columns = tuple(unit_to_column[unit] for unit in admissible)
    reflected_columns = tuple(
        unit_to_column[(int(n_mod_143) - unit) % ODD_MODULUS]
        for unit in admissible)
    values = []
    symmetric_values = []
    for label in outside_labels:
        row = label_to_row[label]
        raw = np.real(character_table[row, columns])
        reflected = np.real(character_table[row, reflected_columns])
        values.append(float(np.mean(raw)))
        symmetric_values.append(float(np.mean((raw + reflected) / 2.0)))
    return (
        np.asarray(values, dtype=np.float64),
        np.asarray(symmetric_values, dtype=np.float64),
        len(admissible),
    )


def collect_targets(window_specs):
    targets = []
    metadata = {}
    seen = set()
    for window_index, (start, count) in enumerate(window_specs):
        census = q286_first_three_dominant_mode_above_floor_holdout_census_receipt(
            start=int(start), target_count=int(count), target_step=2,
            closest_count=min(20, int(count)), include_rows=True)
        for row in census["target_rows"]:
            target = int(row["target"])
            if target in seen:
                continue
            seen.add(target)
            targets.append(target)
            metadata[target] = {
                "target": target,
                "window_index": int(window_index),
                "window_start": int(start),
                "target_mod_286": int(row["target_mod_286"]),
                "target_mod_143": target % ODD_MODULUS,
                "target_mod_11": target % 11,
                "target_mod_13": target % 13,
                "dominant_floor_passes": bool(row["dominant_floor_passes"]),
            }
    return tuple(targets), metadata


def build_empirical_rows(targets, metadata, profile, outside_labels,
                         stress_contributions, rank1_vector,
                         low_frequency_effective_vector, lp_effective_vector,
                         local_rows_by_residue):
    rows = []
    deficits = []
    rank1_sum = float(np.sum(rank1_vector))
    for target in targets:
        profile_row = profile["target_rows"][target]
        if not profile_row["dominant_floor_passes"]:
            deficits.append(metadata[target])
            continue
        contributions = contribution_map(profile_row)
        outside_delta_vector = np.asarray([
            contributions[label] - stress_contributions[label]
            for label in outside_labels
        ], dtype=np.float64)
        full_delta = float(np.sum(outside_delta_vector))
        lp_delta = float(np.dot(outside_delta_vector, lp_effective_vector))
        rank1_delta = float(
            np.dot(outside_delta_vector, rank1_vector) * rank1_sum)
        low_delta = float(
            np.dot(outside_delta_vector, low_frequency_effective_vector))
        local = local_rows_by_residue[metadata[target]["target_mod_143"]]
        rows.append({
            **metadata[target],
            "full_outside_delta_to_stress": full_delta,
            "empirical_lp_reconstructed_delta": lp_delta,
            "empirical_rank1_reconstructed_delta": rank1_delta,
            "empirical_low_frequency_reconstructed_delta": low_delta,
            "empirical_lp_residual_drag_ratio": (
                max(0.0, -(full_delta - lp_delta)) / lp_delta
                if lp_delta > 0 else math.inf),
            "local_lp_delta_action": local["local_lp_delta_action"],
            "local_rank1_delta_action": local["local_rank1_delta_action"],
            "local_low_frequency_delta_action": (
                local["local_low_frequency_delta_action"]),
            "local_delta_l2": local["local_delta_l2"],
            "local_to_empirical_lp_delta_ratio": (
                local["local_lp_delta_action"] / lp_delta
                if lp_delta else math.inf),
        })
    return tuple(rows), tuple(deficits)


def main():
    dictionary_payload = json.loads(
        DICTIONARY_SOURCE.read_text(encoding="utf-8"))
    lp_payload = json.loads(LP_SOURCE.read_text(encoding="utf-8"))
    stress_payload = json.loads(
        STRESS_HOLDOUT_SOURCE.read_text(encoding="utf-8"))
    outside_labels = tuple(
        label_tuple(label) for label in dictionary_payload["outside_labels"])
    rank1_vector = np.asarray(
        dictionary_payload["reference_rank1_vector"], dtype=np.float64)
    low_frequency_vector = np.asarray(
        next(row for row in dictionary_payload["dictionary_rows"]
             if row["id"] == "full_low_frequency_lift")["dictionary_vector"],
        dtype=np.float64)
    low_frequency_effective_vector = (
        float(np.sum(low_frequency_vector)) * low_frequency_vector)
    lp_effective_vector = np.asarray(
        lp_payload["selected_lp_effective_vector"], dtype=np.float64)
    if len(outside_labels) != 17:
        raise AssertionError("outside label count drifted")

    units = tuple(
        residue for residue in range(1, ODD_MODULUS)
        if math.gcd(residue, ODD_MODULUS) == 1)
    _, labels, character_table = _unit_character_table(ODD_MODULUS, units)
    label_to_row = {label: index for index, label in enumerate(labels)}
    unit_to_column = {unit: index for index, unit in enumerate(units)}
    stress_residue = STRESS_TARGET % ODD_MODULUS
    stress_local_vector, stress_symmetric_vector, stress_count = local_vector(
        stress_residue, outside_labels, units, unit_to_column, label_to_row,
        character_table)

    local_rows = []
    max_symmetry_error = 0.0
    for n_mod_143 in range(ODD_MODULUS):
        vector, symmetric_vector, admissible_count = local_vector(
            n_mod_143, outside_labels, units, unit_to_column, label_to_row,
            character_table)
        delta = vector - stress_local_vector
        symmetric_delta = symmetric_vector - stress_symmetric_vector
        max_symmetry_error = max(
            max_symmetry_error,
            float(np.max(np.abs(delta - symmetric_delta))))
        local_rows.append({
            "n_mod_143": n_mod_143,
            "n_mod_11": n_mod_143 % 11,
            "n_mod_13": n_mod_143 % 13,
            "locally_admissible_residue_count": admissible_count,
            "local_singular_multiplier": local_singular_multiplier(n_mod_143),
            "local_delta_l2": float(np.linalg.norm(delta)),
            "local_lp_delta_action": float(np.dot(delta, lp_effective_vector)),
            "local_rank1_delta_action": float(np.dot(delta, rank1_vector)),
            "local_low_frequency_delta_action": float(
                np.dot(delta, low_frequency_effective_vector)),
            "local_delta_cosine_to_lp": cosine(delta, lp_effective_vector),
            "local_delta_cosine_to_rank1": cosine(delta, rank1_vector),
            "local_delta_cosine_to_low_frequency": cosine(
                delta, low_frequency_effective_vector),
            "local_delta_vector": tuple(float(value) for value in delta),
        })
    local_rows_by_residue = {
        row["n_mod_143"]: row for row in local_rows
    }

    window_specs = tuple(
        tuple(int(value) for value in spec)
        for spec in stress_payload["window_specs"])
    targets, metadata = collect_targets(window_specs)
    sample_targets = tuple(dict.fromkeys((STRESS_TARGET,) + targets))
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=sample_targets, dominant_modes=(1, 2),
        tail_threshold=.3, top_channel_count=40)
    stress_contributions = contribution_map(
        profile["target_rows"][STRESS_TARGET])
    empirical_rows, deficit_rows = build_empirical_rows(
        targets, metadata, profile, outside_labels, stress_contributions,
        rank1_vector, low_frequency_effective_vector, lp_effective_vector,
        local_rows_by_residue)

    local_lp_negative = tuple(
        row for row in local_rows
        if row["local_lp_delta_action"] < -TOLERANCE)
    local_lp_zero = tuple(
        row for row in local_rows
        if abs(row["local_lp_delta_action"]) <= TOLERANCE)
    local_rank1_negative = tuple(
        row for row in local_rows
        if row["local_rank1_delta_action"] < -TOLERANCE)
    local_low_negative = tuple(
        row for row in local_rows
        if row["local_low_frequency_delta_action"] < -TOLERANCE)
    far_residues = tuple(sorted({
        row["target_mod_143"] for row in empirical_rows
    }))
    far_local_lp_negative = tuple(
        row for row in local_rows
        if row["n_mod_143"] in far_residues
        and row["local_lp_delta_action"] < -TOLERANCE)
    far_zero_local_empirical_positive = tuple(
        row for row in empirical_rows
        if abs(row["local_lp_delta_action"]) <= TOLERANCE
        and row["empirical_lp_reconstructed_delta"] > TOLERANCE)

    empirical_lp = tuple(
        row["empirical_lp_reconstructed_delta"] for row in empirical_rows)
    empirical_full = tuple(
        row["full_outside_delta_to_stress"] for row in empirical_rows)
    local_lp = tuple(row["local_lp_delta_action"] for row in empirical_rows)
    empirical_summary = {
        "far_clear_count": len(empirical_rows),
        "far_deficit_count": len(deficit_rows),
        "far_distinct_target_mod_143_count": len(far_residues),
        "empirical_lp_delta_summary": finite_summary(empirical_lp),
        "empirical_full_delta_summary": finite_summary(empirical_full),
        "local_lp_action_on_far_rows_summary": finite_summary(local_lp),
        "empirical_lp_vs_local_lp_pearson": pearson(empirical_lp, local_lp),
        "empirical_lp_vs_local_lp_spearman": spearman(empirical_lp, local_lp),
        "empirical_full_vs_local_lp_pearson": pearson(empirical_full, local_lp),
        "empirical_full_vs_local_lp_spearman": spearman(empirical_full, local_lp),
        "minimum_empirical_lp_delta": target_min_record(
            empirical_rows, "empirical_lp_reconstructed_delta"),
        "minimum_local_lp_action_on_far_rows": target_min_record(
            empirical_rows, "local_lp_delta_action"),
        "maximum_local_lp_action_on_far_rows": target_max_record(
            empirical_rows, "local_lp_delta_action"),
        "zero_local_action_but_positive_empirical_count": len(
            far_zero_local_empirical_positive),
        "zero_local_action_but_positive_empirical_targets": tuple(
            row["target"] for row in far_zero_local_empirical_positive[:80]),
        "rows_by_low_local_lp_action": tuple(sorted(
            empirical_rows,
            key=lambda row: (
                row["local_lp_delta_action"],
                row["empirical_lp_reconstructed_delta"],
                row["target"]))[:40]),
    }

    local_gate_passes = (
        len(local_lp_negative) == 0
        and len(far_local_lp_negative) == 0
        and len(empirical_rows) == stress_payload["far_stress_clear_count"])

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_lift_project_dictionary_audit": str(
            DICTIONARY_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lp_cone_audit": str(
            LP_SOURCE.relative_to(ROOT)),
        "source_low_frequency_lp_cone_stress_holdout": str(
            STRESS_HOLDOUT_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite local singular/admissible character-moment audit only; "
            "it compares target-conditioned local residue support with the "
            "frozen LP vector and far empirical rows. It proves no singular "
            "series theorem, LP theorem, interpolation theorem, signed "
            "projection theorem, residual-bound theorem, or Goldbach theorem."),
        "candidate": (
            "The frozen LP cone vector may be aligned with the local "
            "singular/admissible cone after pushing locally admissible q286 "
            "prime-pair residue classes into the same C10 x C12 real "
            "character-channel coordinates."),
        "mechanism": (
            "For each N mod 143, average each outside character label over "
            "unit residues r with N-r also a unit. Subtract the stress target "
            "1222142 local moment vector and test the resulting local delta "
            "against the frozen LP, rank-1, and low-frequency vectors."),
        "prediction": (
            "If local admissibility is part of the LP-good cone, then the "
            "stress-subtracted local character moment should have nonnegative "
            "action under the frozen LP vector on every target residue, and "
            "on the far empirical residues in particular."),
        "falsifier": (
            "Any target residue with negative local LP action, or far "
            "empirical rows whose local action has the wrong sign, demotes "
            "the local singular/admissible cone as an explanation for the "
            "frozen LP certificate."),
        "novelty_label": "new-to-this-task",
        "modulus": MODULUS,
        "odd_modulus": ODD_MODULUS,
        "local_primes": LOCAL_PRIMES,
        "stress_target": STRESS_TARGET,
        "stress_target_mod_143": stress_residue,
        "stress_locally_admissible_residue_count": stress_count,
        "outside_labels": outside_labels,
        "local_character_moment_definition": (
            "mean real chi_(a,b)(r) over r in (Z/143Z)^* with N-r also a "
            "unit; q=2 contributes only odd parity for even N"),
        "reflection_symmetry_max_abs_error": max_symmetry_error,
        "local_residue_rows": local_rows,
        "local_lp_delta_action_summary": finite_summary(
            row["local_lp_delta_action"] for row in local_rows),
        "local_rank1_delta_action_summary": finite_summary(
            row["local_rank1_delta_action"] for row in local_rows),
        "local_low_frequency_delta_action_summary": finite_summary(
            row["local_low_frequency_delta_action"] for row in local_rows),
        "local_lp_negative_count": len(local_lp_negative),
        "local_lp_negative_residues": tuple(
            row["n_mod_143"] for row in local_lp_negative),
        "local_lp_zero_count": len(local_lp_zero),
        "local_lp_zero_residues": tuple(
            row["n_mod_143"] for row in local_lp_zero),
        "local_rank1_negative_count": len(local_rank1_negative),
        "local_rank1_negative_residues": tuple(
            row["n_mod_143"] for row in local_rank1_negative),
        "local_low_frequency_negative_count": len(local_low_negative),
        "local_low_frequency_negative_residues": tuple(
            row["n_mod_143"] for row in local_low_negative),
        "minimum_local_lp_action": min_record(
            local_rows, "local_lp_delta_action"),
        "maximum_local_lp_action": max_record(
            local_rows, "local_lp_delta_action"),
        "maximum_local_delta_cosine_to_lp": max_record(
            local_rows, "local_delta_cosine_to_lp"),
        "far_window_specs": window_specs,
        "far_empirical_summary": empirical_summary,
        "far_local_lp_negative_count": len(far_local_lp_negative),
        "far_local_lp_negative_residues": tuple(
            row["n_mod_143"] for row in far_local_lp_negative),
        "interpretation": {
            "local_singular_cone_sign_supports_lp_vector": local_gate_passes,
            "what_survives": (
                "Local admissibility pushed through the character dictionary "
                "has the correct nonnegative LP orientation for all target "
                "residues modulo 143."),
            "what_does_not_follow": (
                "The local layer alone does not prove the empirical LP "
                "deltas, rank-1 direction, residual cap, or Goldbach; zero "
                "local-action residues can still have positive empirical LP "
                "delta, so quantitative prime-pair distribution remains "
                "necessary."),
            "next_if_passes": (
                "Try to turn the nonnegative local LP action into an exact "
                "finite character identity or cone lemma, then isolate the "
                "centered discrepancy needed beyond local support."),
            "next_if_fails": (
                "Demote local singular/admissible support as the LP cone "
                "mechanism and return to higher-order signed discrepancy."),
        },
        "local_singular_admissible_audit_measured": True,
        "local_singular_cone_sign_supports_lp_vector": local_gate_passes,
        "singular_series_theorem_proved": False,
        "lp_certificate_theorem_proved": False,
        "riesz_thorin_interpolation_theorem_connected": False,
        "rank1_residual_bound_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

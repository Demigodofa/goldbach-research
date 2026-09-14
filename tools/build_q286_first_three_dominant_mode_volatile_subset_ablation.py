"""Build q286 volatile-rim subset ablation evidence.

The stable core preserves selected clears but over-rescues three selected
deficits.  This builder searches every subset of the eight volatile channels
to see whether a smaller volatile package restores exact selected-fixture
classification.
"""

from __future__ import annotations

from itertools import combinations
import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIGN_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-pairwise-swing-sign-stability.json")
CLASSIFICATION_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-stable-core-selected-classification.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-subset-ablation.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    q286_first_three_dominant_mode_signed_channel_profile_receipt,
)


SAMPLE_TARGETS = (
    24424,
    13556,
    13822,
    40420,
    55864,
    164598,
    129706,
    1222142,
    1242118,
    1240888,
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
    if isinstance(value, (tuple, list)):
        return [json_ready(item) for item in value]
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def label_tuple(label):
    return tuple(int(part) for part in label)


def channel_map(row):
    return {
        label_tuple(channel["representative_label"]): (
            channel["contribution_to_principal_ratio"])
        for channel in row["real_channel_contribution_rows"]
    }


def summarize(values):
    values = tuple(values)
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def subset_rows(subset, target_rows, clear_targets, failure_targets):
    subset = tuple(subset)
    pass_targets = []
    failed_targets = []
    false_positive_targets = []
    false_negative_targets = []
    margins = {}

    for target, row in target_rows.items():
        subset_sum = math.fsum(
            row["volatile_channel_contributions"].get(label, 0.0)
            for label in subset)
        margin = row["stable_core_sum_to_principal"] + subset_sum + .3
        passes = margin >= 0.0
        margins[target] = margin
        if passes:
            pass_targets.append(target)
        else:
            failed_targets.append(target)
        if target in failure_targets and passes:
            false_positive_targets.append(target)
        if target in clear_targets and not passes:
            false_negative_targets.append(target)

    return {
        "subset_labels": subset,
        "subset_size": len(subset),
        "pass_targets": tuple(pass_targets),
        "failure_targets": tuple(failed_targets),
        "false_positive_targets": tuple(false_positive_targets),
        "false_negative_targets": tuple(false_negative_targets),
        "false_positive_count": len(false_positive_targets),
        "false_negative_count": len(false_negative_targets),
        "exact_selected_classification": bool(
            not false_positive_targets and not false_negative_targets),
        "preserves_all_selected_clears": bool(not false_negative_targets),
        "restores_all_selected_failures": bool(not false_positive_targets),
        "margin_summary": summarize(margins.values()),
        "margins_by_target": margins,
    }


def all_subsets(labels):
    labels = tuple(labels)
    for size in range(len(labels) + 1):
        for combo in combinations(labels, size):
            yield combo


def main():
    sign_payload = json.loads(SIGN_SOURCE.read_text(encoding="utf-8"))
    prior_payload = json.loads(
        CLASSIFICATION_SOURCE.read_text(encoding="utf-8"))
    stable_positive = tuple(
        label_tuple(label) for label in sign_payload["stable_positive_labels"])
    stable_negative = tuple(
        label_tuple(label) for label in sign_payload["stable_negative_labels"])
    volatile = tuple(
        label_tuple(label) for label in sign_payload["sign_flip_labels"])
    stable_core = stable_positive + stable_negative

    receipt = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=SAMPLE_TARGETS,
        dominant_modes=(1, 2),
        tail_threshold=.3,
        top_channel_count=25)

    target_rows = {}
    clear_targets = set()
    failure_targets = set()
    for target in SAMPLE_TARGETS:
        row = receipt["target_rows"][target]
        channels = channel_map(row)
        stable_sum = math.fsum(channels.get(label, 0.0)
                               for label in stable_core)
        volatile_contributions = {
            label: channels.get(label, 0.0)
            for label in volatile
        }
        if row["dominant_floor_passes"]:
            clear_targets.add(target)
        else:
            failure_targets.add(target)
        target_rows[target] = {
            "target": target,
            "target_mod_286": row["target_mod_286"],
            "dominant_floor_passes": row["dominant_floor_passes"],
            "stable_core_sum_to_principal": stable_sum,
            "volatile_channel_contributions": volatile_contributions,
            "full_volatile_sum_to_principal": math.fsum(
                volatile_contributions.values()),
            "dominant_sum_to_principal": (
                row["dominant_character_sum_to_principal_ratio"]),
        }

    scored = [
        subset_rows(subset, target_rows, clear_targets, failure_targets)
        for subset in all_subsets(volatile)
    ]
    exact_subsets = tuple(
        row for row in scored if row["exact_selected_classification"])
    exact_subsets_by_size = {}
    for row in exact_subsets:
        exact_subsets_by_size.setdefault(str(row["subset_size"]), 0)
        exact_subsets_by_size[str(row["subset_size"])] += 1
    minimum_exact_size = (
        min(row["subset_size"] for row in exact_subsets)
        if exact_subsets else None)
    minimal_exact_subsets = tuple(
        row for row in exact_subsets
        if row["subset_size"] == minimum_exact_size)

    clear_preserving = tuple(
        row for row in scored if row["preserves_all_selected_clears"])
    best_nonexact = sorted(
        (row for row in scored if not row["exact_selected_classification"]),
        key=lambda row: (
            row["false_positive_count"] + row["false_negative_count"],
            row["subset_size"],
            row["false_negative_count"],
            row["false_positive_count"],
            row["subset_labels"]),
    )[:12]

    full_subset = subset_rows(volatile, target_rows, clear_targets,
                              failure_targets)
    full_reconstruction_errors = tuple(
        abs(
            row["stable_core_sum_to_principal"]
            + row["full_volatile_sum_to_principal"]
            - row["dominant_sum_to_principal"])
        for row in target_rows.values())

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_evidence": str(SIGN_SOURCE.relative_to(ROOT)),
        "source_selected_classification": str(
            CLASSIFICATION_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite volatile-subset ablation only; no volatile-rim theorem, "
            "stable-core theorem, selected-fixture classifier theorem, "
            "pointwise character-sum estimate, or Goldbach proof is "
            "established"),
        "mechanism": (
            "Search all subsets of the eight volatile q286 channels after "
            "the stable core is fixed."),
        "prediction": (
            "A small exact subset would narrow the volatile/exclusion theorem "
            "target; absence of a proper exact subset would make the tested "
            "volatile package less compressible on this fixture."),
        "falsifier": (
            "Any proper subset with exact selected classification falsifies "
            "the claim that the full volatile rim is needed on this fixture."),
        "arithmetic_modulus": receipt["arithmetic_modulus"],
        "support": receipt["support"],
        "dominant_modes": receipt["dominant_modes"],
        "tail_threshold": receipt["tail_threshold"],
        "active_real_channel_count": receipt["active_real_channel_count"],
        "sample_targets": SAMPLE_TARGETS,
        "clear_targets": tuple(sorted(clear_targets)),
        "failure_targets": tuple(sorted(failure_targets)),
        "stable_core_channel_count": len(stable_core),
        "volatile_labels": volatile,
        "volatile_channel_count": len(volatile),
        "tested_subset_count": len(scored),
        "exact_subset_count": len(exact_subsets),
        "exact_subsets_by_size": exact_subsets_by_size,
        "minimum_exact_subset_size": minimum_exact_size,
        "minimal_exact_subsets": minimal_exact_subsets,
        "proper_exact_subset_exists": bool(
            minimum_exact_size is not None and minimum_exact_size < len(volatile)),
        "full_volatile_subset_row": full_subset,
        "clear_preserving_subset_count": len(clear_preserving),
        "best_nonexact_subsets": tuple(best_nonexact),
        "maximum_full_reconstruction_error": max(full_reconstruction_errors),
        "target_rows": target_rows,
        "previous_stable_core_false_positives": tuple(
            prior_payload["stable_core_overrescued_failure_targets"]),
        "interpretation": {
            "compression": (
                "If proper_exact_subset_exists is false, no tested proper "
                "volatile subpackage replaces the full rim on this fixture."),
            "remaining_theorem": (
                "Use the minimal exact subset if one exists; otherwise treat "
                "the full volatile package as the current finite theorem "
                "target or seek a different arithmetic/exclusion structure."),
        },
        "volatile_subset_ablation_measured": True,
        "volatile_subpackage_theorem_proved": False,
        "stable_core_theorem_proved": False,
        "selected_fixture_classifier_theorem_proved": False,
        "pointwise_character_sum_estimate_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

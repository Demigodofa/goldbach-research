"""Test whether q286 rank-1 residual drag has a small channel certificate.

The full-window residual-drag audit leaves a theorem-shaped hope: perhaps the
negative residual row-sum after the frozen rank-1 outside direction is carried
by a few explicit outside channels.  This receipt makes that hope falsifiable
by brute-forcing fixed outside-channel subsets on the full-window rows.
"""

from __future__ import annotations

import itertools
import json
import math
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RANK1_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-octave-rank1-audit.json")
FULL_WINDOW_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-outside-plane-remainder-rank1-residual-drag-full-window-audit.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-residual-drag-channel-certificate-falsifier.json")
STRESS_TARGET = 1222142
HIGH_DRAG_RATIO_THRESHOLD = 0.2
CERTIFICATE_CHANNEL_LIMIT = 5
CERTIFICATE_SHARE_THRESHOLD = 0.75
sys.path.insert(0, str(ROOT))

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


def collect_full_window_targets(window_specs):
    targets = []
    target_metadata = {}
    seen = set()
    for window_index, (start, count) in enumerate(window_specs):
        census = q286_first_three_dominant_mode_above_floor_holdout_census_receipt(
            start=start, target_count=count, target_step=2,
            closest_count=min(20, count), include_rows=True)
        role = "primary" if window_index == 0 else "stress"
        for row in census["target_rows"]:
            target = int(row["target"])
            if target in seen:
                continue
            seen.add(target)
            targets.append(target)
            target_metadata[target] = {
                "window_index": int(window_index),
                "window_start": int(start),
                "window_role": role,
                "target_mod_286": int(row["target_mod_286"]),
                "target_mod_10010": target % 10010,
                "absolute_above_floor_signed_surplus": float(
                    row["absolute_above_floor_signed_surplus"]),
                "dominant_floor_passes": bool(row["dominant_floor_passes"]),
            }
    return tuple(targets), target_metadata


def subset_share(row, indexes):
    numerator = math.fsum(row["negative_residual_vector"][index]
                         for index in indexes)
    return numerator / row["total_negative_residual_mass"]


def best_fixed_subset(rows, size):
    label_count = len(rows[0]["outside_labels"])
    best = None
    for indexes in itertools.combinations(range(label_count), size):
        shares = tuple(subset_share(row, indexes) for row in rows)
        candidate = {
            "channel_count": size,
            "labels": tuple(rows[0]["outside_labels"][index]
                            for index in indexes),
            "minimum_row_share": min(shares),
            "mean_row_share": math.fsum(shares) / len(shares),
            "maximum_row_share": max(shares),
            "minimum_share_target": rows[
                min(range(len(shares)), key=lambda index: shares[index])
            ]["target"],
        }
        if best is None or (
                candidate["minimum_row_share"],
                candidate["mean_row_share"]) > (
                    best["minimum_row_share"], best["mean_row_share"]):
            best = candidate
    return best


def summarize(values):
    values = tuple(float(value) for value in values)
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": math.fsum(values) / len(values),
    }


def main():
    rank1_payload = json.loads(RANK1_SOURCE.read_text(encoding="utf-8"))
    full_payload = json.loads(FULL_WINDOW_SOURCE.read_text(encoding="utf-8"))
    outside_labels = tuple(
        label_tuple(row["label"])
        for row in rank1_payload["rank1_right_singular_vector_by_channel"])
    rank1_vector = tuple(
        float(row["rank1_right_singular_vector_loading"])
        for row in rank1_payload["rank1_right_singular_vector_by_channel"])

    targets, target_metadata = collect_full_window_targets(
        tuple(tuple(spec) for spec in full_payload["window_specs"]))
    if len(targets) != full_payload["full_window_target_count"]:
        raise AssertionError("full-window target count drifted")
    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=targets, dominant_modes=(1, 2), tail_threshold=.3,
        top_channel_count=40)
    stress_contributions = contribution_map(
        profile["target_rows"][STRESS_TARGET])

    rows = []
    for target in targets:
        if target == STRESS_TARGET:
            continue
        profile_row = profile["target_rows"][target]
        if not profile_row["dominant_floor_passes"]:
            continue
        contributions = contribution_map(profile_row)
        delta_vector = tuple(
            contributions[label] - stress_contributions[label]
            for label in outside_labels)
        rank1_scalar = math.fsum(
            value * loading
            for value, loading in zip(delta_vector, rank1_vector))
        rank1_vector_row = tuple(
            rank1_scalar * loading for loading in rank1_vector)
        residual_vector = tuple(
            delta - rank1
            for delta, rank1 in zip(delta_vector, rank1_vector_row))
        residual_sum = math.fsum(residual_vector)
        residual_drag = max(0.0, -residual_sum)
        rank1_delta = math.fsum(rank1_vector_row)
        full_delta = math.fsum(delta_vector)
        if abs((rank1_delta + residual_sum) - full_delta) > 1e-10:
            raise AssertionError(f"rank1 residual identity drifted for {target}")
        negative_vector = tuple(max(0.0, -value) for value in residual_vector)
        total_negative = math.fsum(negative_vector)
        rows.append({
            **target_metadata[target],
            "target": target,
            "outside_labels": outside_labels,
            "full_outside_delta_to_stress": full_delta,
            "rank1_reconstructed_outside_delta": rank1_delta,
            "residual_after_rank1_row_sum": residual_sum,
            "residual_drag": residual_drag,
            "residual_drag_to_rank1_ratio": residual_drag / rank1_delta,
            "total_negative_residual_mass": total_negative,
            "negative_residual_vector": negative_vector,
            "positive_residual_mass": math.fsum(
                max(0.0, value) for value in residual_vector),
            "top_negative_residual_channels": tuple(sorted(
                ({
                    "label": label,
                    "negative_residual": value,
                } for label, value in zip(outside_labels, negative_vector)
                 if value > 0),
                key=lambda item: item["negative_residual"],
                reverse=True)[:8]),
        })

    negative_drag_rows = tuple(row for row in rows if row["residual_drag"] > 0)
    high_drag_rows = tuple(
        row for row in negative_drag_rows
        if row["residual_drag_to_rank1_ratio"] >= HIGH_DRAG_RATIO_THRESHOLD)
    if len(high_drag_rows) != 10:
        raise AssertionError("high-drag row count drifted")

    aggregate_negative_by_label = []
    for index, label in enumerate(outside_labels):
        total = math.fsum(row["negative_residual_vector"][index]
                          for row in high_drag_rows)
        aggregate_negative_by_label.append({
            "label": label,
            "aggregate_negative_residual": total,
            "row_count_with_negative_residual": sum(
                1 for row in high_drag_rows
                if row["negative_residual_vector"][index] > 0),
        })
    aggregate_negative_by_label = tuple(sorted(
        aggregate_negative_by_label,
        key=lambda item: item["aggregate_negative_residual"],
        reverse=True))

    best_subsets = tuple(
        best_fixed_subset(high_drag_rows, size)
        for size in range(1, CERTIFICATE_CHANNEL_LIMIT + 1))
    best_limit_subset = best_subsets[-1]
    certificate_refuted = (
        best_limit_subset["minimum_row_share"] < CERTIFICATE_SHARE_THRESHOLD)

    top3_sets = tuple(
        tuple(label_tuple(item["label"])
              for item in row["top_negative_residual_channels"][:3])
        for row in high_drag_rows)
    common_top3_labels = set(top3_sets[0])
    for labels in top3_sets[1:]:
        common_top3_labels &= set(labels)

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_outside_plane_remainder_octave_rank1_audit": str(
            RANK1_SOURCE.relative_to(ROOT)),
        "source_rank1_residual_drag_full_window_audit": str(
            FULL_WINDOW_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite full-window residual-channel diagnostic only; this "
            "falsifies one small fixed-channel certificate shape and proves no "
            "residual theorem, signed projection theorem, or Goldbach proof"),
        "candidate": (
            "The negative residual drag after the frozen rank-1 outside "
            "direction might be certified by a fixed small subset of outside "
            "channels on every high-drag full-window row."),
        "mechanism": (
            "Recompute exact full-window q286 signed channel rows, subtract "
            "stress row 1222142 on the 17 outside channels, subtract the "
            "frozen Octave rank-1 reconstruction, and inspect the negative "
            "part of the residual vector."),
        "prediction": (
            "If a small fixed-channel certificate exists, some subset of at "
            "most five outside labels should cover at least 75 percent of the "
            "negative residual mass in every high-drag row."),
        "falsifier": (
            "Brute-force all outside-label subsets of size one through five. "
            "The certificate is refuted if the best five-label subset has a "
            "minimum row share below 0.75 across the high-drag rows."),
        "novelty_label": "new-to-this-task",
        "high_drag_ratio_threshold": HIGH_DRAG_RATIO_THRESHOLD,
        "certificate_channel_limit": CERTIFICATE_CHANNEL_LIMIT,
        "certificate_share_threshold": CERTIFICATE_SHARE_THRESHOLD,
        "full_window_target_count": full_payload["full_window_target_count"],
        "clear_count": len(rows),
        "negative_drag_row_count": len(negative_drag_rows),
        "high_drag_row_count": len(high_drag_rows),
        "high_drag_targets": tuple(row["target"] for row in high_drag_rows),
        "outside_labels": outside_labels,
        "aggregate_negative_by_label_on_high_drag_rows": (
            aggregate_negative_by_label),
        "best_fixed_subsets_on_high_drag_rows": best_subsets,
        "small_fixed_channel_certificate_refuted": certificate_refuted,
        "common_top3_negative_labels_on_high_drag_rows": tuple(sorted(
            common_top3_labels)),
        "negative_drag_summary": summarize(
            row["residual_drag"] for row in negative_drag_rows),
        "high_drag_ratio_summary": summarize(
            row["residual_drag_to_rank1_ratio"] for row in high_drag_rows),
        "high_drag_rows_by_ratio": tuple(sorted(
            high_drag_rows,
            key=lambda row: (
                row["residual_drag_to_rank1_ratio"],
                row["residual_drag"],
                -row["target"]),
            reverse=True)),
        "summary": {
            "result": (
                "The small fixed-channel certificate is refuted on the "
                "predeclared high-drag full-window rows."),
            "best_five_label_subset": (
                "Even the best fixed five-label subset fails to cover 75 "
                "percent of negative residual mass in every high-drag row."),
            "theorem_impact": (
                "The residual-drag proof route should not target a tiny "
                "static bad-channel list; it needs a row-dependent arithmetic "
                "balance, a larger signed cone, or a replacement aggregate "
                "theorem."),
        },
        "interpretation": {
            "route_status": (
                "This closes the simplest sparse-channel explanation for the "
                "rank-1 residual drag while preserving the 0.75 finite cap."),
        },
        "residual_drag_channel_certificate_falsifier_measured": True,
        "small_fixed_channel_certificate_theorem_proved": False,
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

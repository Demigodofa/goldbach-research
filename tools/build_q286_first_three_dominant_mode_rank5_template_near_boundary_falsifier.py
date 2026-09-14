"""Test the selected-fixture rank-5 SVD template on nearby q286 rows.

The rank-5 Octave autopsy showed that the fifth SVD component rescues the
selected rank-4 failures, but its channel shape is mixed.  This receipt checks
whether the fixed rank-5 channel template nevertheless acts as a simple
near-boundary selector on the existing closest-margin rows.
"""

from __future__ import annotations

import csv
import json
import math
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
NEAR_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-near-boundary-selector-audit.json")
RANK5_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-octave-rank5-autopsy.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-rank5-template-near-boundary-falsifier.json")
sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
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
    if isinstance(value, complex):
        return {"real": value.real, "imag": value.imag}
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def label_tuple(label):
    return tuple(int(part) for part in label)


def posix_path(path):
    return str(path).replace("\\", "/")


def write_csv_matrix(path, rows):
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerows(rows)


def run_octave_projection(oriented_rows, template_vector, signed_surpluses):
    with tempfile.TemporaryDirectory(prefix="q286_rank5_template_") as temp:
        temp_path = Path(temp)
        matrix_path = temp_path / "oriented_rows.csv"
        vector_path = temp_path / "rank5_template.csv"
        surplus_path = temp_path / "signed_surplus.csv"
        write_csv_matrix(matrix_path, oriented_rows)
        write_csv_matrix(vector_path, [template_vector])
        write_csv_matrix(surplus_path, ([value] for value in signed_surpluses))
        code = f"""
M = dlmread('{posix_path(matrix_path)}');
v = dlmread('{posix_path(vector_path)}')(:);
s = dlmread('{posix_path(surplus_path)}')(:);
projection = M * v;
estimated_increment = projection * sum(v);
row_norm = sqrt(sum(M .^ 2, 2));
cosine = projection ./ (row_norm * norm(v));
function r = pearson(x, y)
  x = x(:);
  y = y(:);
  xc = x - mean(x);
  yc = y - mean(y);
  denom = sqrt(sum(xc .^ 2) * sum(yc .^ 2));
  if denom == 0
    r = NaN;
  else
    r = sum(xc .* yc) / denom;
  endif
endfunction
out = struct(
  'octave_version', OCTAVE_VERSION(),
  'rank5_template_sum', sum(v),
  'rank5_projection', projection',
  'rank5_estimated_row_sum_increment', estimated_increment',
  'rank5_alignment_cosine', cosine',
  'pearson_signed_surplus_vs_increment', pearson(s, estimated_increment),
  'pearson_abs_surplus_vs_abs_increment', pearson(abs(s), abs(estimated_increment)),
  'pearson_signed_surplus_vs_cosine', pearson(s, cosine),
  'pearson_abs_surplus_vs_abs_cosine', pearson(abs(s), abs(cosine))
);
disp(jsonencode(out));
"""
        completed = subprocess.run(
            ["octave", "--quiet", "--eval", code],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True)
        return json.loads(completed.stdout)


def summarize(values):
    values = tuple(float(value) for value in values)
    if not values:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "maximum": max(values),
        "mean": float(math.fsum(values) / len(values)),
    }


def sign_label(value, tolerance=1e-12):
    if value > tolerance:
        return "positive"
    if value < -tolerance:
        return "negative"
    return "zero"


def compact_near_row(row):
    return {
        "target": int(row["target"]),
        "window_start": int(row["window_start"]),
        "window_role": row["window_role"],
        "target_mod_286": int(row["target_mod_286"]),
        "target_mod_10010": int(row["target_mod_10010"]),
        "above_floor_signed_surplus_to_threshold": float(
            row["above_floor_signed_surplus_to_threshold"]),
        "absolute_above_floor_signed_surplus": float(
            row["absolute_above_floor_signed_surplus"]),
        "dominant_sum_to_principal": float(
            row["dominant_sum_to_principal"]),
        "nonportfolio_residual_sum_to_principal": float(
            row["nonportfolio_residual_sum_to_principal"]),
        "required_portfolio_for_floor": float(
            row["required_portfolio_for_floor"]),
        "above_floor_mass_fraction": float(row["above_floor_mass_fraction"]),
        "above_floor_mass_threshold": float(row["above_floor_mass_threshold"]),
    }


def main():
    near_payload = json.loads(NEAR_SOURCE.read_text(encoding="utf-8"))
    rank5_payload = json.loads(RANK5_SOURCE.read_text(encoding="utf-8"))
    closest_rows = tuple(near_payload["closest_overall_rows"][:20])
    targets = tuple(dict.fromkeys(int(row["target"]) for row in closest_rows))
    if len(targets) != len(closest_rows):
        raise AssertionError("closest rows unexpectedly contain duplicates")

    profile = q286_first_three_dominant_mode_signed_channel_profile_receipt(
        sample_targets=targets, dominant_modes=(1, 2), tail_threshold=.3,
        top_channel_count=40)
    labels = tuple(label_tuple(row["label"]) for row in rank5_payload[
        "rank5_right_singular_vector_by_channel"])
    template_vector = tuple(float(row["right_singular_vector_loading"])
                            for row in rank5_payload[
                                "rank5_right_singular_vector_by_channel"])

    near_by_target = {int(row["target"]): row for row in closest_rows}
    oriented_rows = []
    signed_surpluses = []
    raw_rows = []
    for target in targets:
        profile_row = profile["target_rows"][target]
        if not profile_row["has_strict_central_prime_pairs"]:
            raise AssertionError(f"target {target} lacks strict pairs")
        channel_map = {
            label_tuple(row["representative_label"]): float(
                row["contribution_to_principal_ratio"])
            for row in profile_row["real_channel_contribution_rows"]
        }
        volatile_vector = tuple(channel_map[label] for label in labels)
        orientation = 1 if profile_row["dominant_floor_passes"] else -1
        oriented_rows.append(tuple(orientation * value
                                   for value in volatile_vector))
        signed_surplus = float(near_by_target[target][
            "above_floor_signed_surplus_to_threshold"])
        signed_surpluses.append(signed_surplus)
        raw_rows.append({
            "target": target,
            "near_boundary_row": compact_near_row(near_by_target[target]),
            "dominant_floor_passes": bool(
                profile_row["dominant_floor_passes"]),
            "orientation": orientation,
            "dominant_character_sum_to_principal_ratio": float(
                profile_row[
                    "dominant_character_sum_to_principal_ratio"]),
            "threshold_slack": float(profile_row["threshold_slack"]),
            "volatile_channel_vector": tuple({
                "label": label,
                "contribution_to_principal_ratio": value,
                "oriented_contribution_to_principal_ratio": (
                    orientation * value),
            } for label, value in zip(labels, volatile_vector)),
        })

    octave_payload = run_octave_projection(
        oriented_rows, template_vector, signed_surpluses)
    projections = [float(value) for value in octave_payload[
        "rank5_projection"]]
    increments = [float(value) for value in octave_payload[
        "rank5_estimated_row_sum_increment"]]
    cosines = [float(value) for value in octave_payload[
        "rank5_alignment_cosine"]]
    row_records = []
    for raw, projection, increment, cosine in zip(
            raw_rows, projections, increments, cosines):
        row = dict(raw)
        row.update({
            "rank5_template_projection": projection,
            "rank5_template_estimated_row_sum_increment": increment,
            "rank5_template_alignment_cosine": cosine,
            "rank5_template_increment_sign": sign_label(increment),
        })
        row_records.append(row)

    positive_increment_rows = tuple(
        row for row in row_records
        if row["rank5_template_estimated_row_sum_increment"] > 0)
    nonpositive_increment_rows = tuple(
        row for row in row_records
        if row["rank5_template_estimated_row_sum_increment"] <= 0)
    deficit_rows = tuple(
        row for row in row_records if not row["dominant_floor_passes"])
    clear_rows = tuple(
        row for row in row_records if row["dominant_floor_passes"])

    threshold_sign_audits = {}
    for threshold in near_payload["near_thresholds"]:
        near_targets = tuple(int(row["target"]) for row in near_payload[
            "threshold_rows"][str(threshold)]["near_rows"])
        missing = set(near_targets).difference(targets)
        if missing:
            raise AssertionError(
                f"near threshold {threshold} missing targets {missing}")
        selected_rows = tuple(
            row for row in row_records if row["target"] in near_targets)
        signs = tuple(row["rank5_template_increment_sign"]
                      for row in selected_rows)
        threshold_sign_audits[str(threshold)] = {
            "near_threshold": float(threshold),
            "near_targets": near_targets,
            "rank5_template_increment_signs": signs,
            "mixed_signs_on_near_rows": bool(len(set(signs)) > 1),
            "rows": tuple({
                "target": row["target"],
                "dominant_floor_passes": row["dominant_floor_passes"],
                "absolute_above_floor_signed_surplus": row[
                    "near_boundary_row"][
                        "absolute_above_floor_signed_surplus"],
                "rank5_template_estimated_row_sum_increment": row[
                    "rank5_template_estimated_row_sum_increment"],
                "rank5_template_increment_sign": row[
                    "rank5_template_increment_sign"],
            } for row in selected_rows),
        }

    positive_false_positive_clears = tuple(
        row for row in positive_increment_rows
        if row["dominant_floor_passes"])
    if len(deficit_rows) != 1 or deficit_rows[0]["target"] != 1222142:
        raise AssertionError("top-20 closest row deficit set drifted")
    if len(positive_false_positive_clears) < 1:
        raise AssertionError(
            "rank-5 positive-increment selector unexpectedly has no clear false positives")
    if not threshold_sign_audits["0.005"]["mixed_signs_on_near_rows"]:
        raise AssertionError(
            "tightest near-boundary rank-5 signs unexpectedly stopped mixing")
    stress = next(row for row in row_records if row["target"] == 1222142)
    source_stress_increment = rank5_payload["stress_target_1222142"][
        "rank5_row_sum_increment"]
    if abs(stress["rank5_template_estimated_row_sum_increment"]
           - source_stress_increment) > 1e-10:
        raise AssertionError("rank-5 template replay drifted on 1222142")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_near_boundary_selector_audit": str(
            NEAR_SOURCE.relative_to(ROOT)),
        "source_rank5_autopsy": str(RANK5_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite rank-5 template near-boundary falsifier only; it "
            "refutes this simple fixed-template selector on the checked "
            "rows and proves no selector theorem, rank-5 theorem, pointwise "
            "character-sum estimate, or Goldbach proof"),
        "candidate": (
            "The selected-fixture rank-5 volatile SVD template might act as "
            "a near-boundary selector or tail/clear separator on nearby q286 "
            "rows."),
        "mechanism": (
            "Replay the fixed rank-5 right singular vector against the eight "
            "volatile-channel contributions of the 20 closest rows from the "
            "near-boundary audit.  Each row is oriented by its actual finite "
            "dominant-floor classification, and Octave computes the row "
            "projection, estimated row-sum increment, cosine, and simple "
            "correlations."),
        "prediction": (
            "If the rank-5 mode is a reusable theorem handle, its fixed "
            "template should give a coherent sign or magnitude pattern on "
            "the tight near-boundary rows, especially separating the known "
            "deficit 1222142 from nearby clears."),
        "falsifier": (
            "The template is refuted as a simple selector if tight rows have "
            "mixed increment signs or if the sign that selects the deficit "
            "also selects nearby clear rows."),
        "novelty_label": "new-to-this-task",
        "octave": {
            "used": True,
            "version": octave_payload["octave_version"],
            "operation": (
                "fixed rank-5 template projection, estimated row-sum "
                "increment, cosine, and Pearson correlations"),
        },
        "arithmetic_modulus": near_payload["arithmetic_modulus"],
        "support": near_payload["support"],
        "closest_row_count": len(row_records),
        "target_order": targets,
        "volatile_labels": labels,
        "rank5_template_vector": template_vector,
        "rank5_template_sum": float(octave_payload[
            "rank5_template_sum"]),
        "row_records": tuple(row_records),
        "sign_summary": {
            "deficit_count": len(deficit_rows),
            "clear_count": len(clear_rows),
            "positive_increment_count": len(positive_increment_rows),
            "nonpositive_increment_count": len(nonpositive_increment_rows),
            "positive_increment_clear_false_positive_count": len(
                positive_false_positive_clears),
            "nonpositive_increment_clear_count": sum(
                1 for row in nonpositive_increment_rows
                if row["dominant_floor_passes"]),
            "positive_increment_targets": tuple(
                row["target"] for row in positive_increment_rows),
            "nonpositive_increment_targets": tuple(
                row["target"] for row in nonpositive_increment_rows),
        },
        "increment_summary": summarize(increments),
        "absolute_increment_summary": summarize(
            abs(value) for value in increments),
        "alignment_cosine_summary": summarize(cosines),
        "correlations": {
            "pearson_signed_surplus_vs_increment": float(
                octave_payload[
                    "pearson_signed_surplus_vs_increment"]),
            "pearson_abs_surplus_vs_abs_increment": float(
                octave_payload[
                    "pearson_abs_surplus_vs_abs_increment"]),
            "pearson_signed_surplus_vs_cosine": float(
                octave_payload["pearson_signed_surplus_vs_cosine"]),
            "pearson_abs_surplus_vs_abs_cosine": float(
                octave_payload["pearson_abs_surplus_vs_abs_cosine"]),
        },
        "threshold_sign_audits": threshold_sign_audits,
        "summary": {
            "selector_result": (
                "The fixed rank-5 template is not a simple near-boundary "
                "selector on the checked top-20 rows."),
            "tightest_rows": (
                "The two tightest rows, deficit 1222142 and clear 1242118, "
                "have opposite rank-5 template increment signs."),
            "false_positive_result": (
                "The sign selecting the deficit also selects nearby clear "
                "rows, so rank-5 sign alone cannot classify the checked "
                "near-boundary rows."),
        },
        "interpretation": {
            "hole_status": (
                "The q286 hole is still tightening, but the rank-5 mode is "
                "now bounded as a local diagnostic rather than a reusable "
                "selector theorem."),
            "route_status": (
                "Do not reopen the fixed rank-5 template as a simple "
                "near-boundary selector without a changed mechanism, such as "
                "row-dependent arithmetic weights or a proven aggregate "
                "inequality."),
            "remaining_theorem": (
                "The live route remains signed adverse-pair absorption from "
                "actual binary-prime residue weights, or a stronger signed "
                "aggregate arithmetic-placement theorem."),
        },
        "rank5_template_near_boundary_falsifier_measured": True,
        "rank5_template_simple_selector_refuted": True,
        "rank5_template_selector_theorem_proved": False,
        "rank5_low_rank_theorem_proved": False,
        "volatile_threshold_theorem_proved": False,
        "volatile_rim_theorem_proved": False,
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

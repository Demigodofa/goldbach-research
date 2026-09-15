"""Convert the q286 dual-edge rescue into unnormalized weighted sums.

The normalized edge audit proves a finite identity after dividing by the
strict-central pair mass T_N.  A Goldbach bridge cannot start by assuming that
T_N is positive.  This receipt multiplies the checked identities back by the
observed total log-weight T_N and records the exact raw witness shape:

    raw_edge_gap = sum_orbits W_N(orbit) * g_a,t(orbit)
    raw_required = -T_N * ell_a,t(t)
    raw_margin = raw_edge_gap - raw_required = T_N * Full(mu_N).

As a theorem target, proving raw_margin > 0 directly would imply at least one
strict-central prime pair, because all W_N are nonnegative and vanish when no
prime pair exists.  The finite receipt itself remains downstream of computed
pairs and proves no Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
DUAL_SOURCE = EVIDENCE / "q286-lower-face-dual-edge-audit.json"
OVERLAP_SOURCE = EVIDENCE / "q286-lower-face-overlap-audit.json"
OUT = EVIDENCE / "q286-unnormalized-dual-edge-witness-audit.json"
TOLERANCE = 1e-8


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def finite_summary(values):
    finite = tuple(
        float(value) for value in values
        if value is not None and math.isfinite(float(value)))
    if not finite:
        return {"count": 0, "minimum": None, "mean": None, "maximum": None}
    return {
        "count": len(finite),
        "minimum": min(finite),
        "mean": math.fsum(finite) / len(finite),
        "maximum": max(finite),
    }


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_row(edge_row, overlap_row):
    total_weight = float(overlap_row["total_weight"])
    raw_edge_gap = total_weight * float(edge_row["actual_edge_gap"])
    raw_required = total_weight * float(
        edge_row["required_edge_gap_for_positivity"])
    raw_margin = raw_edge_gap - raw_required
    raw_full = total_weight * float(edge_row["actual_full"])
    return {
        "target": int(edge_row["target"]),
        "target_residue": int(edge_row["target_residue"]),
        "target_mod_286": int(edge_row["target_mod_286"]),
        "block_index_after_discovery": int(
            edge_row["block_index_after_discovery"]),
        "pair_count": int(overlap_row["pair_count"]),
        "total_weight": total_weight,
        "actual_full": float(edge_row["actual_full"]),
        "normalized_edge_gap": float(edge_row["actual_edge_gap"]),
        "normalized_required_edge_gap": float(
            edge_row["required_edge_gap_for_positivity"]),
        "normalized_edge_gap_margin": float(
            edge_row["edge_gap_margin_after_rescue"]),
        "edge_gap_rescue_ratio": float(edge_row["edge_gap_rescue_ratio"]),
        "raw_edge_gap": raw_edge_gap,
        "raw_required_edge_gap": raw_required,
        "raw_margin_after_rescue": raw_margin,
        "raw_full_signed_witness": raw_full,
        "raw_margin_identity_error": abs(raw_margin - raw_full),
        "strict_central_pair_witness_observed": (
            int(overlap_row["pair_count"]) > 0 and total_weight > 0.0),
        "raw_signed_witness_positive": raw_full > TOLERANCE,
    }


def build_receipt():
    dual = load_json(DUAL_SOURCE)
    overlap = load_json(OVERLAP_SOURCE)
    overlap_by_target = {int(row["target"]): row
                         for row in overlap["target_rows"]}
    rows = [
        build_row(row, overlap_by_target[int(row["target"])])
        for row in dual["target_rows"]
        if row["edge_success"]
    ]
    post = [row for row in rows if row["block_index_after_discovery"] >= 1]
    discovery = [row for row in rows if row["block_index_after_discovery"] < 1]

    def summarize(bucket):
        return {
            "row_count": len(bucket),
            "pair_count_summary": finite_summary(
                row["pair_count"] for row in bucket),
            "total_weight_summary": finite_summary(
                row["total_weight"] for row in bucket),
            "raw_edge_gap_summary": finite_summary(
                row["raw_edge_gap"] for row in bucket),
            "raw_required_edge_gap_summary": finite_summary(
                row["raw_required_edge_gap"] for row in bucket),
            "raw_margin_after_rescue_summary": finite_summary(
                row["raw_margin_after_rescue"] for row in bucket),
            "raw_full_signed_witness_summary": finite_summary(
                row["raw_full_signed_witness"] for row in bucket),
            "normalized_edge_gap_rescue_ratio_summary": finite_summary(
                row["edge_gap_rescue_ratio"] for row in bucket),
            "raw_margin_identity_error_summary": finite_summary(
                row["raw_margin_identity_error"] for row in bucket),
            "positive_raw_signed_witness_rows": sum(
                row["raw_signed_witness_positive"] for row in bucket),
            "observed_strict_central_pair_rows": sum(
                row["strict_central_pair_witness_observed"] for row in bucket),
        }

    tightest = sorted(
        post,
        key=lambda row: (
            row["raw_margin_after_rescue"],
            row["target"]))[:20]

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "lower_face_dual_edge_audit": str(DUAL_SOURCE.relative_to(ROOT)),
            "lower_face_overlap_audit": str(OVERLAP_SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite unnormalized dual-edge witness diagnostic only; computed "
            "rows already have observed strict-central pairs, so this is not "
            "an existence proof, q286 threshold theorem, signed "
            "prime-correlation theorem, or Goldbach proof"
        ),
        "goldbach_proved": False,
        "unnormalized_edge_witness_theorem_proved": False,
        "normalization_gap_closed": False,
        "curiosity_status": "changed-under-evidence",
        "novelty_label": "new-to-this-task",
        "candidate": {
            "mechanism": (
                "Multiplying the dual-edge identity by T_N converts the "
                "normalized rescue inequality into a raw signed sum over "
                "strict-central prime-pair weights."
            ),
            "prediction": (
                "The weakest normalized edge rescue should correspond to the "
                "smallest raw signed margin among post-discovery rows, "
                "exposing the scale a direct analytic proof must beat."
            ),
            "falsifier": (
                "If raw_margin_after_rescue differs from T_N*Full(mu_N), or "
                "if the raw formulation cannot be stated without already "
                "assuming T_N>0, this bridge is only notation and should not "
                "be promoted."
            ),
            "smallest_next_test": (
                "Use the existing 230 lower-face rows and verify the raw "
                "identity plus the weakest raw margin."
            ),
        },
        "decision": (
            "The normalized edge result has a clean raw signed-witness form, "
            "but the finite receipt is still computed from rows with observed "
            "prime pairs.  The next theorem must prove raw_full_signed_witness "
            "> 0 directly, or supply an independent T_N>0 lower bound before "
            "normalized q286 geometry can imply Goldbach."
        ),
        "summary": {
            "target_row_count": len(rows),
            "post_discovery_target_count": len(post),
            "discovery_target_count": len(discovery),
            "all_rows": summarize(rows),
            "post_discovery_rows": summarize(post),
            "discovery_rows": summarize(discovery),
            "tightest_post_discovery_raw_margin_rows": tightest,
        },
        "target_rows": rows,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

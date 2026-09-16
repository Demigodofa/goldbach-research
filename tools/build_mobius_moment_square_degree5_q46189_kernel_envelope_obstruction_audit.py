"""Test naive envelope routes for the Q46189 kernel sign boundary.

The packet-kernel sign audit reduced the finite active/full sign condition to
``off_diagonal_total / diagonal_half > -1`` for nonadverse packets.  This
receipt asks whether simple componentwise envelopes could prove that bound:
take each distance bucket or ranked negative gap independently at its worst
observed nonadverse value, then sum those disconnected worst cases.

If the disconnected envelope already falls below -1, then a theorem cannot be
only a separate per-bucket or per-rank lower bound.  It must use co-occurrence,
correlation, factor geometry, or a sharper structured decomposition.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


SOURCE = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-packet-kernel-sign-landscape-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-kernel-envelope-obstruction-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-kernel-envelope-obstruction-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def min_by(rows, value_fn):
    return min(rows, key=value_fn)


def bucket_by_name(row, name):
    return next(
        bucket for bucket in row["distance_bucket_contributions"]
        if bucket["bucket"] == name)


def bucket_envelope(nonadverse_rows):
    names = [
        bucket["bucket"]
        for bucket in nonadverse_rows[0]["distance_bucket_contributions"]
    ]
    envelope_rows = []
    for name in names:
        row = min_by(
            nonadverse_rows,
            lambda item: bucket_by_name(
                item, name)["contribution_over_diagonal_half"],
        )
        bucket = bucket_by_name(row, name)
        envelope_rows.append({
            "bucket": name,
            "worst_denominator": row["reduced_denominator"],
            "worst_role": row["role"],
            "worst_contribution_over_diagonal_half": (
                bucket["contribution_over_diagonal_half"]),
            "distance_range": bucket["distance_range"],
        })
    return {
        "bucket_count": len(envelope_rows),
        "rows": envelope_rows,
        "disconnected_worst_sum": sum(
            row["worst_contribution_over_diagonal_half"]
            for row in envelope_rows),
    }


def top_negative_rank_envelope(nonadverse_rows, rank_count):
    envelope_rows = []
    for index in range(rank_count):
        row = min_by(
            nonadverse_rows,
            lambda item: item["top_negative_gap_pairs"][index][
                "contribution_over_diagonal_half"],
        )
        gap = row["top_negative_gap_pairs"][index]
        envelope_rows.append({
            "rank": index + 1,
            "worst_denominator": row["reduced_denominator"],
            "worst_role": row["role"],
            "circular_distance": gap["circular_distance"],
            "deltas": gap["deltas"],
            "worst_contribution_over_diagonal_half": (
                gap["contribution_over_diagonal_half"]),
        })
    return {
        "rank_count": rank_count,
        "rows": envelope_rows,
        "disconnected_worst_sum": sum(
            row["worst_contribution_over_diagonal_half"]
            for row in envelope_rows),
    }


def prefix_summaries(nonadverse_rows):
    summaries = []
    for count in (1, 2, 3, 5, 8):
        row = min_by(
            nonadverse_rows,
            lambda item: sum(
                gap["contribution_over_diagonal_half"]
                for gap in item["top_negative_gap_pairs"][:count]),
        )
        summaries.append({
            "prefix_count": count,
            "worst_denominator": row["reduced_denominator"],
            "worst_prefix_sum": sum(
                gap["contribution_over_diagonal_half"]
                for gap in row["top_negative_gap_pairs"][:count]),
        })
    return summaries


def build_receipt():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    nonadverse = [
        row for row in source["rows"]
        if row["reduced_denominator"] != source["fixture"]["adverse_denominator"]
    ]
    bucket = bucket_envelope(nonadverse)
    rank = top_negative_rank_envelope(nonadverse, 8)
    weakest = source["weakest_nonadverse_off_diagonal_row"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_kernel_envelope_obstruction",
        "source_packet_kernel_sign_landscape_audit": str(SOURCE),
        "question": (
            "Could the finite nonadverse bound off_diagonal/diagonal_half > "
            "-1 be proved by independent per-bucket or per-ranked-gap lower "
            "bounds?"),
        "fixture": source["fixture"],
        "observed_true_nonadverse_boundary": {
            "minimum_nonadverse_denominator": (
                weakest["reduced_denominator"]),
            "minimum_nonadverse_off_diagonal_over_diagonal_half": (
                weakest["off_diagonal_over_diagonal_half"]),
            "target_bound": -1.0,
        },
        "bucket_componentwise_envelope": bucket,
        "top_negative_rank_componentwise_envelope": rank,
        "top_negative_same_row_prefix_summaries": prefix_summaries(nonadverse),
        "classification": {
            "bucket_componentwise_envelope_refutes_simple_bucket_bound": (
                bucket["disconnected_worst_sum"] <= -1.0),
            "top_negative_rank_envelope_refutes_simple_rank_bound": (
                rank["disconnected_worst_sum"] <= -1.0),
            "true_rows_survive_but_disconnected_envelopes_fail": (
                weakest["off_diagonal_over_diagonal_half"] > -1.0
                and bucket["disconnected_worst_sum"] <= -1.0
                and rank["disconnected_worst_sum"] <= -1.0),
            "cooccurrence_or_structured_correlation_required": True,
            "finite_obstruction_audit_only": True,
        },
        "candidate_next_action": {
            "name": "co-occurrence constrained kernel envelope",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The per-component minima occur on different denominators; "
                "a useful theorem must constrain which adverse buckets or "
                "gap ranks can be simultaneously bad inside one packet."),
            "prediction": (
                "A same-row or factor-geometry constrained envelope should "
                "stay above -1, unlike the disconnected componentwise "
                "envelopes."),
            "falsifier": (
                "A source-admissible nonadverse packet whose co-occurring "
                "bucket/gap profile reaches <= -1 would falsify the "
                "overpayment-exclusion theorem target."),
            "smallest_next_test": (
                "Build a co-occurrence matrix over bucket contributions and "
                "top negative ranks, then test whether the convex same-row "
                "envelope stays above -1."),
        },
        "decision": (
            "Simple independent component bounds are too weak.  The worst "
            "nonadverse row is q=38038 at about -0.847293, but disconnected "
            "bucket minima sum to a value below -1 and disconnected ranked "
            "negative-gap minima also fall below -1.  Any theorem route must "
            "use co-occurrence, factor geometry, or another structured "
            "correlation; it cannot just prove separate bucket or rank lower "
            "bounds."),
        "finite_kernel_envelope_obstruction_audit_only": True,
        "finite_diagnostic_only": True,
        "simple_bucket_bound_theorem_proved": False,
        "simple_rank_bound_theorem_proved": False,
        "cooccurrence_kernel_bound_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    bucket = receipt["bucket_componentwise_envelope"]
    rank = receipt["top_negative_rank_componentwise_envelope"]
    observed = receipt["observed_true_nonadverse_boundary"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 kernel-envelope obstruction audit",
        "",
        "## Question",
        "",
        "Could the finite nonadverse bound",
        "`off_diagonal_total / diagonal_half > -1` be proved by independent",
        "per-bucket or per-ranked-gap lower bounds?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_kernel_envelope_obstruction_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-kernel-envelope-obstruction-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"true weakest nonadverse q:                  {observed['minimum_nonadverse_denominator']}",
        f"true weakest nonadverse off/diag-half:      {observed['minimum_nonadverse_off_diagonal_over_diagonal_half']}",
        f"target lower bound:                         {observed['target_bound']}",
        f"disconnected bucket-minimum sum:            {bucket['disconnected_worst_sum']}",
        f"disconnected top-negative rank-minimum sum: {rank['disconnected_worst_sum']}",
        "```",
        "",
        "Worst bucket contributors:",
        "",
        "```text",
    ]
    for row in bucket["rows"]:
        lines.append(
            "{}: q={} value={}".format(
                row["bucket"],
                row["worst_denominator"],
                row["worst_contribution_over_diagonal_half"],
            ))
    lines.extend([
        "```",
        "",
        "## Decision",
        "",
        "Simple independent component bounds are too weak.  The true checked",
        "same-row minimum is still safely above `-1`, but disconnected bucket",
        "and ranked-gap worst cases both fall below `-1`.  The theorem target",
        "must therefore use co-occurrence, factor geometry, or another",
        "structured correlation between adverse components.",
        "",
        "This is finite diagnostic evidence only.  It proves no simple bucket",
        "bound theorem, simple rank bound theorem, co-occurrence kernel bound",
        "theorem, coordinate-00 residue-gap sign theorem, strict-central",
        "Goldbach theorem, or Goldbach proof.",
        "",
    ])
    NOTE.write_text("\n".join(lines), encoding="utf-8")


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    write_note(receipt)
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "bucket_envelope_sum": receipt[
            "bucket_componentwise_envelope"]["disconnected_worst_sum"],
        "rank_envelope_sum": receipt[
            "top_negative_rank_componentwise_envelope"][
                "disconnected_worst_sum"],
        "true_minimum_nonadverse": receipt[
            "observed_true_nonadverse_boundary"][
                "minimum_nonadverse_off_diagonal_over_diagonal_half"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

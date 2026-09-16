"""Audit the exact-distance profile inside the Q46189 50A..60A witness.

The far-band slice audit found that 50A..60A separates Q=46189 from all
source-admissible replacement rows.  This receipt checks whether that local
witness can be sharpened to exact distances, or whether the useful structure
still needs short distance blocks.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_q46189_coordinate00_kernel_decomposition_audit import (  # noqa: E402
    component_vector,
)
from tools.build_mobius_moment_square_degree5_q46189_exception_bound_audit import (  # noqa: E402
    DENOMINATOR,
    PRIME,
    SCALE,
    TARGET_LABEL,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


SOURCE_LEDGER = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-one-coordinate-ratio-ledger-audit.json")
SOURCE_SLICE = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-far-band-slice-balance-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-50a60a-distance-profile-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-50a60a-distance-profile-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def paired_distance_values(reduced_denominator, cells, row_count,
                           active_row_start):
    vector = component_vector(reduced_denominator, cells)
    transform = np.fft.fft(vector)
    autocorrelation = np.fft.ifft(transform * np.conjugate(transform))
    deltas = np.arange(reduced_denominator, dtype=np.int64)
    active_rows = np.arange(
        active_row_start, active_row_start + row_count, dtype=np.int64)
    kernel = np.exp(
        2j * np.pi
        * np.outer(active_rows, deltas)
        / reduced_denominator).mean(axis=0)
    contributions = (2 * reduced_denominator * autocorrelation * kernel).real
    diagonal_half = 0.5 * float(contributions[0])
    values = {}
    used = {0}
    for delta in range(1, reduced_denominator):
        if delta in used:
            continue
        mate = (-delta) % reduced_denominator
        if mate == delta:
            normalized = float(contributions[delta] / diagonal_half)
            deltas_for_distance = [delta]
        else:
            normalized = float(
                (contributions[delta] + contributions[mate])
                / diagonal_half)
            deltas_for_distance = [delta, mate]
            used.add(mate)
        used.add(delta)
        values[min(delta, reduced_denominator - delta)] = {
            "normalized_contribution": normalized,
            "deltas": deltas_for_distance,
        }
    return values, diagonal_half


def band_metric(values, lower, upper):
    selected = [
        values[distance]["normalized_contribution"]
        for distance in range(lower, upper + 1)
    ]
    positive = sum(value for value in selected if value > 0)
    negative = sum(value for value in selected if value < 0)
    total = sum(selected)
    absolute = positive - negative
    return {
        "distance_range": [int(lower), int(upper)],
        "distance_count": len(selected),
        "total_over_diagonal": total,
        "positive_over_diagonal": positive,
        "negative_over_diagonal": negative,
        "absolute_over_diagonal": absolute,
        "positive_fraction_of_absolute": (
            positive / absolute if absolute else None),
    }


def row_summary(reduced_denominator, role, values, diagonal_half, lower, upper):
    band = band_metric(values, lower, upper)
    distance_rows = [
        {
            "circular_distance": int(distance),
            "normalized_contribution": values[distance][
                "normalized_contribution"],
            "deltas": values[distance]["deltas"],
        }
        for distance in range(lower, upper + 1)
    ]
    positives = [
        row for row in distance_rows
        if row["normalized_contribution"] > 0
    ]
    negatives = [
        row for row in distance_rows
        if row["normalized_contribution"] < 0
    ]
    return {
        "role": role,
        "reduced_denominator": reduced_denominator,
        "diagonal_half_contribution": diagonal_half,
        "band_metric": band,
        "positive_distance_count": len(positives),
        "negative_distance_count": len(negatives),
        "top_positive_distances": sorted(
            positives,
            key=lambda row: row["normalized_contribution"],
            reverse=True)[:10],
        "top_negative_distances": sorted(
            negatives,
            key=lambda row: row["normalized_contribution"])[:10],
        "positive_concentration": concentration(
            [row["normalized_contribution"] for row in positives]),
        "negative_abs_concentration": concentration(
            [-row["normalized_contribution"] for row in negatives]),
    }


def concentration(values):
    ordered = sorted(values, reverse=True)
    total = sum(ordered)
    return {
        f"top_{count}_fraction": (
            sum(ordered[:count]) / total if total else None)
        for count in (1, 3, 5, 10, 25, 50)
    }


def summarize_block(name, lower, upper, adverse_q, replacement_qs, values_by_q):
    adverse = band_metric(values_by_q[adverse_q], lower, upper)
    replacement_metrics = [
        (q, band_metric(values_by_q[q], lower, upper))
        for q in replacement_qs
    ]
    min_share_q, min_share = min(
        replacement_metrics,
        key=lambda item: item[1]["positive_fraction_of_absolute"])
    min_total_q, min_total = min(
        replacement_metrics,
        key=lambda item: item[1]["total_over_diagonal"])
    share_gap = (
        min_share["positive_fraction_of_absolute"]
        - adverse["positive_fraction_of_absolute"])
    total_gap = (
        min_total["total_over_diagonal"]
        - adverse["total_over_diagonal"])
    return {
        "block_name": name,
        "distance_range": [int(lower), int(upper)],
        "distance_count": int(upper - lower + 1),
        "adverse_positive_fraction": (
            adverse["positive_fraction_of_absolute"]),
        "minimum_replacement_positive_fraction": (
            min_share["positive_fraction_of_absolute"]),
        "minimum_replacement_positive_fraction_denominator": min_share_q,
        "positive_fraction_gap": share_gap,
        "positive_fraction_separator": 0.5 * (
            adverse["positive_fraction_of_absolute"]
            + min_share["positive_fraction_of_absolute"]),
        "positive_fraction_separates": share_gap > 0,
        "adverse_total_over_diagonal": adverse["total_over_diagonal"],
        "minimum_replacement_total_over_diagonal": (
            min_total["total_over_diagonal"]),
        "minimum_replacement_total_denominator": min_total_q,
        "total_gap": total_gap,
        "total_separator": 0.5 * (
            adverse["total_over_diagonal"]
            + min_total["total_over_diagonal"]),
        "total_pressure_separates": total_gap > 0,
        "separates_by_both_share_and_total": (
            share_gap > 0 and total_gap > 0),
    }


def build_receipt():
    ledger = json.loads(SOURCE_LEDGER.read_text(encoding="utf-8"))
    parameters = scale_parameters(SCALE)
    row_count = parameters["row_count"]
    active_row_start = row_count
    lower = 50 * row_count + 1
    upper = 60 * row_count
    _, cells_by_denominator = _residue_cells_by_denominator(
        PRIME,
        row_count,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    replacement_qs = [
        row["reduced_denominator"]
        for row in ledger["replacement_one_coordinate_rows"]
    ]
    denominator_rows = [
        (DENOMINATOR, "q46189_adverse"),
        *((q, "replacement") for q in replacement_qs),
    ]
    values_by_q = {}
    diagonal_by_q = {}
    for q, _role in denominator_rows:
        values_by_q[q], diagonal_by_q[q] = paired_distance_values(
            q, cells_by_denominator[q], row_count, active_row_start)

    row_summaries = [
        row_summary(
            q, role, values_by_q[q], diagonal_by_q[q], lower, upper)
        for q, role in denominator_rows
    ]

    pointwise_rows = []
    for distance in range(lower, upper + 1):
        adverse_value = values_by_q[DENOMINATOR][distance][
            "normalized_contribution"]
        replacement_items = [
            (q, values_by_q[q][distance]["normalized_contribution"])
            for q in replacement_qs
        ]
        min_replacement_q, min_replacement = min(
            replacement_items, key=lambda item: item[1])
        pointwise_rows.append({
            "circular_distance": int(distance),
            "adverse_contribution": adverse_value,
            "minimum_replacement_contribution": min_replacement,
            "minimum_replacement_denominator": min_replacement_q,
            "pointwise_min_replacement_minus_adverse": (
                min_replacement - adverse_value),
        })
    pointwise_gap_sum = sum(
        row["pointwise_min_replacement_minus_adverse"]
        for row in pointwise_rows)
    pointwise_positive = [
        row for row in pointwise_rows
        if row["pointwise_min_replacement_minus_adverse"] > 0
    ]
    pointwise_nonpositive = [
        row for row in pointwise_rows
        if row["pointwise_min_replacement_minus_adverse"] <= 0
    ]

    micro_slices = []
    for start in range(50, 60):
        micro_slices.append(summarize_block(
            f"{start}A_to_{start + 1}A",
            start * row_count + 1,
            (start + 1) * row_count,
            DENOMINATOR,
            replacement_qs,
            values_by_q,
        ))

    contiguous_blocks = []
    for start in range(50, 60):
        for stop in range(start + 1, 61):
            contiguous_blocks.append(summarize_block(
                f"{start}A_to_{stop}A",
                start * row_count + 1,
                stop * row_count,
                DENOMINATOR,
                replacement_qs,
                values_by_q,
            ))
    separating_blocks = [
        block for block in contiguous_blocks
        if block["separates_by_both_share_and_total"]
    ]
    minimum_width = min(
        block["distance_count"] for block in separating_blocks)
    minimal_separating = [
        block for block in separating_blocks
        if block["distance_count"] == minimum_width
    ]
    two_a_witness = next(
        block for block in contiguous_blocks
        if block["block_name"] == "56A_to_58A")
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_50a60a_distance_profile",
        "source_one_coordinate_ledger": str(SOURCE_LEDGER),
        "source_far_band_slice_balance_audit": str(SOURCE_SLICE),
        "question": (
            "Inside the Q=46189 50A..60A signed-balance witness, does "
            "the replacement advantage live at exact distances or in "
            "short aggregate distance blocks?"),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": row_count,
            "active_row_start": active_row_start,
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "distance_range_50A_to_60A": [lower, upper],
            "replacement_row_count": len(replacement_qs),
        },
        "row_summaries": row_summaries,
        "micro_slice_summaries": micro_slices,
        "contiguous_micro_block_summaries": contiguous_blocks,
        "separating_contiguous_micro_blocks": separating_blocks,
        "exact_distance_pointwise_envelope": {
            "distance_count": len(pointwise_rows),
            "pointwise_positive_gap_count": len(pointwise_positive),
            "pointwise_nonpositive_gap_count": len(pointwise_nonpositive),
            "adverse_total_over_diagonal": row_summaries[0][
                "band_metric"]["total_over_diagonal"],
            "componentwise_min_replacement_total_over_diagonal": (
                row_summaries[0]["band_metric"]["total_over_diagonal"]
                + pointwise_gap_sum),
            "componentwise_min_replacement_minus_adverse_total_gap": (
                pointwise_gap_sum),
            "top_pointwise_advantages": sorted(
                pointwise_rows,
                key=lambda row: (
                    row["pointwise_min_replacement_minus_adverse"]),
                reverse=True)[:10],
            "top_pointwise_failures": sorted(
                pointwise_rows,
                key=lambda row: (
                    row["pointwise_min_replacement_minus_adverse"]))[:10],
            "exact_distance_pointwise_separator_survives": (
                len(pointwise_nonpositive) == 0),
            "componentwise_exact_distance_envelope_survives": (
                pointwise_gap_sum > 0),
        },
        "classification": {
            "exact_distance_pointwise_theorem_target_falsified": (
                len(pointwise_nonpositive) > 0),
            "componentwise_exact_distance_envelope_falsified": (
                pointwise_gap_sum <= 0),
            "micro_slices_separating_by_both": [
                block["block_name"] for block in micro_slices
                if block["separates_by_both_share_and_total"]
            ],
            "separating_contiguous_micro_block_count": (
                len(separating_blocks)),
            "minimal_width_separating_micro_blocks": [
                block["block_name"] for block in minimal_separating],
            "two_a_witness_block": two_a_witness["block_name"],
            "two_a_witness_distance_range": (
                two_a_witness["distance_range"]),
            "finite_selected_family_diagnostic_only": True,
        },
        "candidate_next_action": {
            "name": "56A-to-58A short-block signed-balance witness",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The 50A..60A separator is not a pointwise exact-distance "
                "phenomenon.  It survives after aggregating the short "
                "56A..58A block, where Q=46189 has lower positive share and "
                "more adverse total pressure than every replacement row."),
            "prediction": (
                "A useful theorem target should control short distance-block "
                "phase balance, not individual circular distances.  Exact "
                "distance componentwise envelopes are too strict on this "
                "fixture."),
            "falsifier": (
                "A source-admissible replacement row at or below the 56A..58A "
                "share or total separator, or a proof that the block is a "
                "finite artifact with no source-admissible stability, "
                "falsifies this narrowed witness."),
            "smallest_next_test": (
                "Check whether the same 56A..58A short-block separator "
                "appears in the robustness slice 80A..90A or in a fresh "
                "source-admissible replacement holdout."),
        },
        "decision": (
            "The exact-distance sharpening is too strict: only 83 of 430 "
            "distances have a positive pointwise min-replacement gap, and "
            "the disconnected exact-distance envelope is below the adverse "
            "Q=46189 total.  The useful local structure is a short aggregate "
            "block: 56A..58A separates by both positive share and total "
            "pressure, while the one-A blocks 56A..57A and 57A..58A are the "
            "minimal separating micro-slices."),
        "finite_50a60a_distance_profile_audit_only": True,
        "finite_diagnostic_only": True,
        "exact_distance_pointwise_theorem_proved": False,
        "short_block_positive_share_theorem_proved": False,
        "short_block_pressure_theorem_proved": False,
        "distance_slice_positive_share_theorem_proved": False,
        "distance_slice_pressure_theorem_proved": False,
        "replacement_residue_gap_bound_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    envelope = receipt["exact_distance_pointwise_envelope"]
    two_a = next(
        block for block in receipt["contiguous_micro_block_summaries"]
        if block["block_name"] == "56A_to_58A")
    lines = [
        "# Mobius moment-square degree-5 Q46189 50A..60A distance profile audit",
        "",
        "## Question",
        "",
        "Inside the `50A..60A` signed-balance witness, does the replacement",
        "advantage live at exact circular distances, or does it require short",
        "aggregate distance blocks?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_50a60a_distance_profile_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-50a60a-distance-profile-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"distance range:                         {receipt['fixture']['distance_range_50A_to_60A']}",
        f"exact distances checked:                {envelope['distance_count']}",
        f"pointwise positive gaps:                {envelope['pointwise_positive_gap_count']}",
        f"pointwise nonpositive gaps:             {envelope['pointwise_nonpositive_gap_count']}",
        f"Q 50A..60A total / diag:                {envelope['adverse_total_over_diagonal']}",
        f"componentwise min-replacement envelope: {envelope['componentwise_min_replacement_total_over_diagonal']}",
        f"componentwise envelope gap:             {envelope['componentwise_min_replacement_minus_adverse_total_gap']}",
        f"micro-slices separating by both:        {', '.join(receipt['classification']['micro_slices_separating_by_both'])}",
        f"minimal separating micro-slices:        {', '.join(receipt['classification']['minimal_width_separating_micro_blocks'])}",
        f"2A witness:                             {two_a['block_name']} {two_a['distance_range']}",
        f"2A Q positive share:                    {two_a['adverse_positive_fraction']}",
        f"2A min replacement positive share:      {two_a['minimum_replacement_positive_fraction']}",
        f"2A positive-share gap:                  {two_a['positive_fraction_gap']}",
        f"2A Q total / diag:                      {two_a['adverse_total_over_diagonal']}",
        f"2A min replacement total / diag:        {two_a['minimum_replacement_total_over_diagonal']}",
        f"2A total gap:                           {two_a['total_gap']}",
        "```",
        "",
        "## Decision",
        "",
        "The exact-distance sharpening is too strict.  Only `83` of `430`",
        "distances have a positive pointwise min-replacement gap, and the",
        "disconnected exact-distance envelope is worse than the adverse",
        "`Q=46189` total.",
        "",
        "The useful local structure is a short aggregate block.  The",
        "`56A..58A` block separates by both positive share and total pressure,",
        "while `56A..57A` and `57A..58A` are the minimal one-`A` separating",
        "micro-slices.  This narrows the next theorem-shaped target to",
        "short-block signed balance, not pointwise exact-distance dominance.",
        "",
        "This is finite selected-family diagnostic evidence only.  It proves",
        "no exact-distance pointwise theorem, short-block positive-share",
        "theorem, short-block pressure theorem, replacement residue-gap bound",
        "theorem, coordinate-00 residue-gap sign theorem, strict-central",
        "Goldbach theorem, or Goldbach proof.",
        "",
    ]
    NOTE.write_text("\n".join(lines), encoding="utf-8")


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    write_note(receipt)
    two_a = next(
        block for block in receipt["contiguous_micro_block_summaries"]
        if block["block_name"] == "56A_to_58A")
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "pointwise_positive_gap_count": (
            receipt["exact_distance_pointwise_envelope"][
                "pointwise_positive_gap_count"]),
        "pointwise_nonpositive_gap_count": (
            receipt["exact_distance_pointwise_envelope"][
                "pointwise_nonpositive_gap_count"]),
        "two_a_witness": two_a["block_name"],
        "two_a_positive_fraction_gap": two_a["positive_fraction_gap"],
        "two_a_total_gap": two_a["total_gap"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

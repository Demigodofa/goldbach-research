"""Audit distance slices inside the Q46189 far-band separator.

The previous audit narrowed the signed-balance target to the far band
10A..100A.  This receipt splits that band into A-scaled slices and records
which slices already separate Q=46189 from every source-admissible replacement
row, and which slices fail.
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
    ledger_rows,
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
SOURCE_SUBBAND = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-far-tail-subband-balance-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-far-band-slice-balance-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-far-band-slice-balance-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def active_contributions(reduced_denominator, cells, row_count,
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
    distance = np.minimum(deltas, reduced_denominator - deltas)
    diagonal_half = 0.5 * float(contributions[0])
    return contributions, distance, diagonal_half


def slice_metric(contributions, distance, diagonal_half, lower, upper):
    mask = (distance >= lower) & (distance <= upper)
    selected = contributions[mask]
    positive = float(np.sum(selected[selected > 0])) / diagonal_half
    negative = float(np.sum(selected[selected < 0])) / diagonal_half
    total = float(np.sum(selected)) / diagonal_half
    absolute = positive - negative
    return {
        "distance_range": [int(lower), int(upper)],
        "delta_count": int(np.count_nonzero(mask)),
        "total_over_diagonal": total,
        "positive_over_diagonal": positive,
        "negative_over_diagonal": negative,
        "absolute_over_diagonal": absolute,
        "positive_fraction_of_absolute": (
            positive / absolute if absolute else None),
    }


def row_slices(reduced_denominator, role, cells, row_count, active_row_start):
    contributions, distance, diagonal_half = active_contributions(
        reduced_denominator, cells, row_count, active_row_start)
    slices = []
    for start in range(10, 100, 10):
        lower = start * row_count + 1
        upper = (start + 10) * row_count
        metric = slice_metric(
            contributions, distance, diagonal_half, lower, upper)
        metric["slice_name"] = f"{start}A_to_{start + 10}A"
        slices.append(metric)
    return {
        "role": role,
        "reduced_denominator": reduced_denominator,
        "diagonal_half_contribution": diagonal_half,
        "far_slice_metrics": slices,
    }


def midpoint(a, b):
    return 0.5 * (a + b)


def build_receipt():
    ledger = json.loads(SOURCE_LEDGER.read_text(encoding="utf-8"))
    parameters = scale_parameters(SCALE)
    row_count = parameters["row_count"]
    active_row_start = row_count
    _, cells_by_denominator = _residue_cells_by_denominator(
        PRIME,
        row_count,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    by_q = ledger_rows(ledger)
    adverse = row_slices(
        DENOMINATOR,
        "q46189_adverse",
        cells_by_denominator[DENOMINATOR],
        row_count,
        active_row_start)
    replacements = [
        row_slices(
            ledger_row["reduced_denominator"],
            "replacement",
            cells_by_denominator[ledger_row["reduced_denominator"]],
            row_count,
            active_row_start)
        for ledger_row in ledger["replacement_one_coordinate_rows"]
    ]
    slice_summaries = []
    for index, adverse_slice in enumerate(adverse["far_slice_metrics"]):
        repl_slices = [
            (row["reduced_denominator"], row["far_slice_metrics"][index])
            for row in replacements
        ]
        min_share_q, min_share = min(
            repl_slices,
            key=lambda item: item[1]["positive_fraction_of_absolute"])
        min_total_q, min_total = min(
            repl_slices,
            key=lambda item: item[1]["total_over_diagonal"])
        share_gap = (
            min_share["positive_fraction_of_absolute"]
            - adverse_slice["positive_fraction_of_absolute"])
        total_gap = (
            min_total["total_over_diagonal"]
            - adverse_slice["total_over_diagonal"])
        share_sep = share_gap > 0
        total_sep = total_gap > 0
        slice_summaries.append({
            "slice_name": adverse_slice["slice_name"],
            "distance_range": adverse_slice["distance_range"],
            "adverse_positive_fraction": (
                adverse_slice["positive_fraction_of_absolute"]),
            "minimum_replacement_positive_fraction": (
                min_share["positive_fraction_of_absolute"]),
            "minimum_replacement_positive_fraction_denominator": (
                min_share_q),
            "positive_fraction_gap": share_gap,
            "positive_fraction_separator": midpoint(
                adverse_slice["positive_fraction_of_absolute"],
                min_share["positive_fraction_of_absolute"]),
            "positive_fraction_separates": share_sep,
            "adverse_total_over_diagonal": (
                adverse_slice["total_over_diagonal"]),
            "minimum_replacement_total_over_diagonal": (
                min_total["total_over_diagonal"]),
            "minimum_replacement_total_denominator": min_total_q,
            "total_gap": total_gap,
            "total_separator": midpoint(
                adverse_slice["total_over_diagonal"],
                min_total["total_over_diagonal"]),
            "total_pressure_separates": total_sep,
            "separates_by_both_share_and_total": share_sep and total_sep,
        })
    both = [
        row for row in slice_summaries
        if row["separates_by_both_share_and_total"]
    ]
    best_share = max(
        slice_summaries, key=lambda row: row["positive_fraction_gap"])
    best_total = max(slice_summaries, key=lambda row: row["total_gap"])
    best_both = max(
        both,
        key=lambda row: (
            row["positive_fraction_gap"], row["total_gap"]))
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_far_band_slice_balance",
        "source_one_coordinate_ledger": str(SOURCE_LEDGER),
        "source_far_tail_subband_balance_audit": str(SOURCE_SUBBAND),
        "question": (
            "Inside the far band 10A..100A, do smaller A-scaled distance "
            "slices already separate Q=46189 from every source-admissible "
            "replacement row?"),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": row_count,
            "active_row_start": active_row_start,
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "replacement_row_count": len(replacements),
        },
        "adverse_row": adverse,
        "replacement_rows": replacements,
        "slice_summaries": slice_summaries,
        "best_single_slice_by_positive_share_gap": best_share,
        "best_single_slice_by_total_gap": best_total,
        "best_single_slice_separating_by_both": best_both,
        "classification": {
            "single_slices_separating_by_both_count": len(both),
            "single_slices_separating_by_both": [
                row["slice_name"] for row in both],
            "best_slice_is_50A_to_60A": (
                best_both["slice_name"] == "50A_to_60A"),
            "finite_selected_family_diagnostic_only": True,
        },
        "candidate_next_action": {
            "name": "50A-to-60A signed-balance witness",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The far-band separation has a local witness: distances "
                "50A..60A already have enough positive share and total "
                "pressure in every replacement row, while Q=46189 is "
                "more adverse there."),
            "prediction": (
                "A structural residue-distance theorem may be easier in the "
                "50A..60A slice than in the whole far band, but the second "
                "witness slice 80A..90A should be preserved as a robustness "
                "check."),
            "falsifier": (
                "A source-admissible replacement row at or below the 50A..60A "
                "share or total separator falsifies this local witness."),
            "smallest_next_test": (
                "Inspect the positive and negative residue-distance profile "
                "inside 50A..60A to see which exact distances carry the "
                "replacement advantage."),
        },
        "decision": (
            "The far-band signed-balance separator has local witnesses.  The "
            "50A..60A slice separates by both positive share and total "
            "pressure with the largest positive-share gap; 80A..90A also "
            "separates.  Several other slices fail, so the statement is not "
            "a uniform all-slice phenomenon."),
        "finite_far_band_slice_balance_audit_only": True,
        "finite_diagnostic_only": True,
        "distance_slice_positive_share_theorem_proved": False,
        "distance_slice_pressure_theorem_proved": False,
        "far_band_positive_share_theorem_proved": False,
        "far_band_pressure_theorem_proved": False,
        "replacement_residue_gap_bound_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    best = receipt["best_single_slice_separating_by_both"]
    both = receipt["classification"]["single_slices_separating_by_both"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 far-band slice balance audit",
        "",
        "## Question",
        "",
        "Inside the far band `10A..100A`, do smaller `A`-scaled distance",
        "slices already separate `Q=46189` from every source-admissible",
        "replacement row?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_far_band_slice_balance_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-far-band-slice-balance-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"slices separating by share and total: {', '.join(both)}",
        f"best slice:                          {best['slice_name']}",
        f"best distance range:                 {best['distance_range']}",
        f"Q positive share in best slice:      {best['adverse_positive_fraction']}",
        f"min replacement positive share:      {best['minimum_replacement_positive_fraction']}",
        f"positive-share gap:                  {best['positive_fraction_gap']}",
        f"Q total / diag in best slice:        {best['adverse_total_over_diagonal']}",
        f"min replacement total / diag:        {best['minimum_replacement_total_over_diagonal']}",
        f"total gap:                           {best['total_gap']}",
        "```",
        "",
        "## Decision",
        "",
        "The far-band signed-balance separator has local witnesses.  The",
        "`50A..60A` slice separates by both positive share and total pressure",
        "with the largest positive-share gap; `80A..90A` also separates.",
        "Several other slices fail, so the statement is not a uniform",
        "all-slice phenomenon.",
        "",
        "The next theorem-shaped target is a `50A..60A` signed-balance",
        "witness, with `80A..90A` preserved as a robustness check.  This is",
        "finite selected-family diagnostic evidence only.  It proves no",
        "distance-slice positive-share theorem, distance-slice pressure",
        "theorem, far-band theorem, replacement residue-gap bound theorem,",
        "coordinate-00 residue-gap sign theorem, strict-central Goldbach",
        "theorem, or Goldbach proof.",
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
    best = receipt["best_single_slice_separating_by_both"]
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "best_slice": best["slice_name"],
        "positive_fraction_gap": best["positive_fraction_gap"],
        "total_gap": best["total_gap"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

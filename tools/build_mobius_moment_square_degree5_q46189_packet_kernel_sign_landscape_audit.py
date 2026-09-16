"""Audit packet-wide coordinate-00 kernel signs around Q46189.

The packet-ratio landscape showed that Q=46189 is the unique checked
same-source denominator with coordinate-00 active/full ratio below one half.
This receipt expands every same-source denominator into the same finite
Dirichlet-kernel identity used for the Q46189-vs-weakest-replacement audit.
The normalized sign test is

    ratio_minus_half = 0.5 * (1 + off_diagonal / diagonal_half).

Thus a row is below one half exactly when its off-diagonal Dirichlet-kernel
mass is less than ``-diagonal_half``.
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
    distance_buckets,
    paired_gap_contributions,
)
from tools.build_mobius_moment_square_degree5_q46189_exception_bound_audit import (  # noqa: E402
    DENOMINATOR,
    PRIME,
    SCALE,
    TARGET_LABEL,
)
from tools.build_mobius_moment_square_degree5_q46189_group_payment_audit import (  # noqa: E402
    HIGH_PRIMES,
    factor_integer,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


SOURCE_PACKET_RATIO = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-packet-ratio-landscape-audit.json")
SOURCE_KERNEL_PAIR = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-coordinate00-kernel-decomposition-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-packet-kernel-sign-landscape-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-packet-kernel-sign-landscape-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def arithmetic_profile(reduced_denominator):
    factors = factor_integer(reduced_denominator)
    support = {int(prime) for prime in factors}
    return {
        "factorization": factors,
        "high_prime_support": sorted(support & set(HIGH_PRIMES)),
        "missing_high_primes": sorted(set(HIGH_PRIMES) - support),
        "small_prime_support": sorted(support - set(HIGH_PRIMES)),
    }


def normalized_bucket_rows(row_count, active_contributions, diagonal_half):
    rows = []
    for bucket in distance_buckets(row_count, active_contributions):
        rows.append({
            **bucket,
            "contribution_over_diagonal_half": (
                bucket["component_active_contribution"] / diagonal_half),
            "positive_over_diagonal_half": (
                bucket["positive_contribution_sum"] / diagonal_half),
            "negative_over_diagonal_half": (
                bucket["negative_contribution_sum"] / diagonal_half),
        })
    return rows


def compact_gap_rows(rows, diagonal_half, count=8):
    compact = []
    for row in rows[:count]:
        compact.append({
            **row,
            "contribution_over_diagonal_half": (
                row["component_active_contribution"] / diagonal_half),
        })
    return compact


def decompose_denominator(
        reduced_denominator, role, cells, row_count, active_row_start):
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
    active_contributions = (
        2 * reduced_denominator * autocorrelation * kernel).real
    component_full_energy = float(active_contributions[0])
    diagonal_half = 0.5 * component_full_energy
    off_diagonal = float(np.sum(active_contributions[1:]))
    half_margin = diagonal_half + off_diagonal
    off_over_diagonal_half = off_diagonal / diagonal_half
    paired = paired_gap_contributions(active_contributions)
    top_negative = sorted(
        paired, key=lambda row: row["component_active_contribution"])
    top_positive = sorted(
        paired,
        key=lambda row: row["component_active_contribution"],
        reverse=True,
    )
    return {
        "role": role,
        "reduced_denominator": reduced_denominator,
        **arithmetic_profile(reduced_denominator),
        "residue_cell_count": len(cells),
        "component_full_energy": component_full_energy,
        "diagonal_half_contribution": diagonal_half,
        "off_diagonal_total_contribution": off_diagonal,
        "off_diagonal_over_diagonal_half": off_over_diagonal_half,
        "component_half_margin_active_minus_half_full": half_margin,
        "coordinate_00_active_over_full_ratio": (
            half_margin / component_full_energy + 0.5),
        "ratio_minus_half": half_margin / component_full_energy,
        "below_half": half_margin <= 0,
        "off_diagonal_overpays_diagonal_half": (
            off_over_diagonal_half <= -1.0),
        "distance_bucket_contributions": normalized_bucket_rows(
            row_count, active_contributions, diagonal_half),
        "top_negative_gap_pairs": compact_gap_rows(
            top_negative, diagonal_half),
        "top_positive_gap_pairs": compact_gap_rows(
            top_positive, diagonal_half),
    }


def finite_summary(values):
    ordered = sorted(values)
    return {
        "count": len(ordered),
        "minimum": ordered[0] if ordered else None,
        "maximum": ordered[-1] if ordered else None,
    }


def build_receipt():
    packet_ratio = json.loads(SOURCE_PACKET_RATIO.read_text(encoding="utf-8"))
    original_qs = set(
        packet_ratio["fixture"]["original_replacement_denominators"])
    parameters = scale_parameters(SCALE)
    row_count = parameters["row_count"]
    active_row_start = row_count
    _, cells_by_denominator = _residue_cells_by_denominator(
        PRIME,
        row_count,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    rows = []
    for q, cells in sorted(cells_by_denominator.items()):
        if q == DENOMINATOR:
            role = "q46189_adverse"
        elif q in original_qs:
            role = "original_replacement"
        else:
            role = "unused_same_source_denominator"
        rows.append(decompose_denominator(
            q, role, cells, row_count, active_row_start))

    q_row = next(row for row in rows if row["reduced_denominator"] == DENOMINATOR)
    nonadverse = [row for row in rows if row["reduced_denominator"] != DENOMINATOR]
    below_half = [row for row in rows if row["below_half"]]
    nonadverse_overpays = [
        row for row in nonadverse
        if row["off_diagonal_overpays_diagonal_half"]]
    weakest_nonadverse = min(
        nonadverse, key=lambda row: row["off_diagonal_over_diagonal_half"])
    strongest_nonadverse = max(
        nonadverse, key=lambda row: row["off_diagonal_over_diagonal_half"])
    min_margin_nonadverse = min(
        nonadverse, key=lambda row: row["ratio_minus_half"])
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_packet_kernel_sign_landscape",
        "source_packet_ratio_landscape_audit": str(SOURCE_PACKET_RATIO),
        "source_coordinate00_kernel_pair_audit": str(SOURCE_KERNEL_PAIR),
        "question": (
            "Across the Q46189 same-source packet landscape, is the sign of "
            "the coordinate-00 active/full half-margin exactly explained by "
            "whether off-diagonal Dirichlet-kernel mass overpays the diagonal "
            "half?"),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": row_count,
            "active_row_start": active_row_start,
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "adverse_denominator": DENOMINATOR,
            "sign_identity": (
                "ratio_minus_half = 0.5 * "
                "(1 + off_diagonal_total / diagonal_half)"),
        },
        "landscape_summary": {
            "same_source_denominator_count": len(rows),
            "below_half_count": len(below_half),
            "below_half_denominators": [
                row["reduced_denominator"] for row in below_half],
            "off_diagonal_overpayment_count": len([
                row for row in rows
                if row["off_diagonal_overpays_diagonal_half"]]),
            "nonadverse_off_diagonal_overpayment_count": (
                len(nonadverse_overpays)),
            "q46189_off_diagonal_over_diagonal_half": (
                q_row["off_diagonal_over_diagonal_half"]),
            "minimum_nonadverse_off_diagonal_over_diagonal_half": (
                weakest_nonadverse["off_diagonal_over_diagonal_half"]),
            "minimum_nonadverse_off_diagonal_denominator": (
                weakest_nonadverse["reduced_denominator"]),
            "maximum_nonadverse_off_diagonal_over_diagonal_half": (
                strongest_nonadverse["off_diagonal_over_diagonal_half"]),
            "maximum_nonadverse_off_diagonal_denominator": (
                strongest_nonadverse["reduced_denominator"]),
            "minimum_nonadverse_ratio_minus_half": (
                min_margin_nonadverse["ratio_minus_half"]),
            "minimum_nonadverse_ratio_denominator": (
                min_margin_nonadverse["reduced_denominator"]),
            "nonadverse_off_diagonal_over_diagonal_half_summary": (
                finite_summary([
                    row["off_diagonal_over_diagonal_half"]
                    for row in nonadverse])),
        },
        "q46189_row": q_row,
        "weakest_nonadverse_off_diagonal_row": weakest_nonadverse,
        "rows": rows,
        "classification": {
            "q46189_unique_below_half_by_kernel_overpayment": (
                len(below_half) == 1
                and below_half[0]["reduced_denominator"] == DENOMINATOR
                and q_row["off_diagonal_overpays_diagonal_half"]),
            "all_nonadverse_rows_keep_diagonal_surplus": (
                len(nonadverse_overpays) == 0),
            "tight_nonadverse_row_matches_packet_ratio_audit": (
                min_margin_nonadverse["reduced_denominator"]
                == packet_ratio["landscape_summary"][
                    "minimum_nonadverse_ratio_denominator"]),
            "finite_packet_kernel_sign_landscape_only": True,
            "universal_kernel_sign_theorem_proved": False,
        },
        "candidate_next_action": {
            "name": "off-diagonal-overpayment exclusion theorem candidate",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Prove a source-packet class bound "
                "off_diagonal_total/diagonal_half > -1 for all replacement "
                "packets, while allowing Q46189-style all-high packets to "
                "cross below -1."),
            "prediction": (
                "The sign boundary should be visible in normalized bucket and "
                "top-gap-pair terms: Q46189 is just past -1, while q=38038 is "
                "the closest surviving nonadverse packet at about -0.847."),
            "falsifier": (
                "A source-admissible nonadverse packet with normalized "
                "off-diagonal total <= -1 falsifies this theorem target."),
            "smallest_next_test": (
                "Build a bucket-envelope audit asking whether any natural "
                "bucket or top-pair cap implies the observed nonadverse "
                "off-diagonal lower bound."),
        },
        "decision": (
            "The packet landscape has a sharper sign boundary than the "
            "distance-window selector: Q46189 is the only checked row where "
            "off-diagonal Dirichlet-kernel mass overpays the diagonal half. "
            "Every nonadverse packet keeps off_diagonal/diagonal_half above "
            "-1, with the tight row q=38038 at about -0.847293.  This remains "
            "finite diagnostic evidence; no universal kernel sign theorem or "
            "Goldbach proof is established."),
        "finite_packet_kernel_sign_landscape_audit_only": True,
        "finite_diagnostic_only": True,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "one_coordinate_active_full_ratio_theorem_proved": False,
        "packet_landscape_ratio_theorem_proved": False,
        "universal_kernel_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    summary = receipt["landscape_summary"]
    q_row = receipt["q46189_row"]
    weakest = receipt["weakest_nonadverse_off_diagonal_row"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 packet-kernel sign landscape audit",
        "",
        "## Question",
        "",
        "Across the `Q=46189` same-source packet landscape, is the sign of",
        "the coordinate-00 active/full half-margin explained by whether",
        "off-diagonal Dirichlet-kernel mass overpays the diagonal half?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_packet_kernel_sign_landscape_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-packet-kernel-sign-landscape-audit.json",
        "```",
        "",
        "## Identity",
        "",
        "```text",
        "ratio_minus_half = 0.5 * (1 + off_diagonal_total / diagonal_half)",
        "below half <=> off_diagonal_total / diagonal_half <= -1",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"same-source denominators:                    {summary['same_source_denominator_count']}",
        f"below-half denominators:                      {summary['below_half_denominators']}",
        f"off-diagonal overpayment count:               {summary['off_diagonal_overpayment_count']}",
        f"nonadverse overpayment count:                 {summary['nonadverse_off_diagonal_overpayment_count']}",
        f"Q=46189 off/diagonal-half:                    {summary['q46189_off_diagonal_over_diagonal_half']}",
        f"minimum nonadverse off/diagonal-half:         {summary['minimum_nonadverse_off_diagonal_over_diagonal_half']}",
        f"minimum nonadverse off/diagonal denominator:  {summary['minimum_nonadverse_off_diagonal_denominator']}",
        f"minimum nonadverse ratio-minus-half:          {summary['minimum_nonadverse_ratio_minus_half']}",
        "```",
        "",
        "Tight rows:",
        "",
        "```text",
        f"Q=46189: off/diag_half={q_row['off_diagonal_over_diagonal_half']}, ratio_minus_half={q_row['ratio_minus_half']}",
        f"q={weakest['reduced_denominator']}: off/diag_half={weakest['off_diagonal_over_diagonal_half']}, ratio_minus_half={weakest['ratio_minus_half']}",
        "```",
        "",
        "## Decision",
        "",
        "`Q=46189` is the only checked row where off-diagonal",
        "Dirichlet-kernel mass overpays the diagonal half.  Every nonadverse",
        "packet keeps `off_diagonal_total / diagonal_half > -1`; the tight",
        "survivor is still `q=38038` at about `-0.847293`.",
        "",
        "This is a cleaner theorem-shaped target than `50A..60A`: prove an",
        "off-diagonal-overpayment exclusion bound for source-admissible",
        "replacement packets.  This remains finite diagnostic evidence only.",
        "It proves no coordinate-00 residue-gap sign theorem, active/full ratio",
        "theorem, packet-landscape theorem, strict-central Goldbach theorem, or",
        "Goldbach proof.",
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
    summary = receipt["landscape_summary"]
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "below_half_denominators": summary["below_half_denominators"],
        "q46189_off_diagonal_over_diagonal_half": (
            summary["q46189_off_diagonal_over_diagonal_half"]),
        "minimum_nonadverse_off_diagonal_denominator": (
            summary["minimum_nonadverse_off_diagonal_denominator"]),
        "minimum_nonadverse_off_diagonal_over_diagonal_half": (
            summary["minimum_nonadverse_off_diagonal_over_diagonal_half"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

"""Audit the Q46189 packet landscape after the 50A..60A selector failed.

The reachable q=16302 packet falsified the broad frozen distance-window
selector.  This receipt asks whether the older one-coordinate active/full
energy-ratio target survives on the broader local packet landscape: is
Q=46189 the unique row below one half while every other same-source
denominator is above one half?
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lcm_sawtooth_lifted_endpoint_frame import (  # noqa: E402
    _lifted_frequency_data,
    _symmetric_pair_coordinates,
)
from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_q46189_50a60a_distance_profile_audit import (  # noqa: E402
    band_metric,
    paired_distance_values,
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
from tools.build_mobius_moment_square_degree5_q46189_replacement_phase_profile_audit import (  # noqa: E402
    active_transforms,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


SOURCE_LEDGER = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-one-coordinate-ratio-ledger-audit.json")
SOURCE_REACHABILITY = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-counterexample-reachability-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-packet-ratio-landscape-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-packet-ratio-landscape-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def one_coordinate_ratio(reduced_denominator, cells, row_count, active_start):
    residues = np.asarray([cell[0] for cell in cells], dtype=np.int64)
    values = np.asarray([cell[1] for cell in cells], dtype=complex)
    left = values[:, 0]
    tx = active_transforms(
        reduced_denominator, residues, values, row_count, active_start)[:, 0]
    full_00 = reduced_denominator * float(np.vdot(left, left).real)
    active_00 = (
        reduced_denominator / row_count * float(np.vdot(tx, tx).real))
    return {
        "coordinate_00_full_energy": full_00,
        "coordinate_00_active_energy": active_00,
        "one_coordinate_active_over_full_ratio": active_00 / full_00,
        "ratio_minus_half": active_00 / full_00 - 0.5,
    }


def raw_packets(parameters, target_denominators):
    denominators, numerators, _, coordinates = _lifted_frequency_data(
        PRIME,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    target_set = set(target_denominators)
    pairs_by_q = defaultdict(Counter)
    ratios_by_q = defaultdict(list)
    residues_by_q = defaultdict(set)
    zero_left_by_q = Counter()
    chunk_size = 64

    for first in range(0, len(denominators), chunk_size):
        left_d = denominators[first:first + chunk_size, None]
        left_k = numerators[first:first + chunk_size, None]
        common = np.lcm(left_d, denominators[None, :])
        difference_numerator = (
            left_k * (common // left_d)
            - numerators[None, :] * (common // denominators[None, :]))
        common_factor = np.gcd(np.abs(difference_numerator), common)
        reduced = common // common_factor
        selected = np.isin(reduced, list(target_set))
        if not np.any(selected):
            continue

        selected_residues = np.zeros(reduced.shape, dtype=np.int64)
        selected_residues[selected] = (
            PRIME
            * (difference_numerator[selected] // common_factor[selected])
            % reduced[selected])
        left_coordinates = np.broadcast_to(
            coordinates[first:first + chunk_size, None, :],
            (*reduced.shape, 3))[selected]
        right_coordinates = np.broadcast_to(
            coordinates[None, :, :], (*reduced.shape, 3))[selected]
        lifted = _symmetric_pair_coordinates(
            left_coordinates, right_coordinates)
        selected_q = reduced[selected]
        selected_left = np.broadcast_to(left_d, reduced.shape)[selected]
        selected_right = np.broadcast_to(
            denominators[None, :], reduced.shape)[selected]
        nonzero_left = np.abs(lifted[:, 0]) > 1e-30

        for q in sorted(set(int(value) for value in selected_q)):
            mask = selected_q == q
            zero_left_by_q[q] += int(np.count_nonzero(mask & ~nonzero_left))
            nonzero_mask = mask & nonzero_left
            if np.any(nonzero_mask):
                ratios_by_q[q].extend(
                    lifted[nonzero_mask, 4] / lifted[nonzero_mask, 0])
            residues_by_q[q].update(
                int(value) for value in selected_residues[selected][mask])
            for left, right in zip(selected_left[mask], selected_right[mask]):
                pairs_by_q[q][(int(left), int(right))] += 1

    packets = {}
    for q in target_denominators:
        ratio_array = np.asarray(ratios_by_q[q], dtype=complex)
        scalar = ratio_array.mean()
        deviations = np.abs(ratio_array - scalar)
        packets[q] = {
            "raw_frequency_pair_count": int(len(ratio_array)),
            "raw_reduced_residue_count": len(residues_by_q[q]),
            "zero_left_raw_pair_count": int(zero_left_by_q[q]),
            "ordered_source_conductor_pair_count": len(pairs_by_q[q]),
            "ordered_source_conductor_pairs": [
                {
                    "left_source_conductor": left,
                    "right_source_conductor": right,
                    "raw_frequency_pair_count": count,
                }
                for (left, right), count in sorted(pairs_by_q[q].items())
            ],
            "raw_scalar_real": float(scalar.real),
            "raw_scalar_imag": float(scalar.imag),
            "max_abs_raw_scalar_deviation": float(np.max(deviations)),
            "max_abs_raw_scalar_imag": float(
                np.max(np.abs(ratio_array.imag))),
            "raw_scalar_identity_holds_to_tolerance": bool(
                float(np.max(deviations)) < 1e-13
                and float(np.max(np.abs(ratio_array.imag))) < 1e-14
                and int(zero_left_by_q[q]) == 0),
        }
    return packets


def arithmetic_profile(reduced_denominator):
    factors = factor_integer(reduced_denominator)
    support = {int(prime) for prime in factors}
    return {
        "factorization": factors,
        "high_prime_support": sorted(support & set(HIGH_PRIMES)),
        "missing_high_primes": sorted(set(HIGH_PRIMES) - support),
        "small_prime_support": sorted(support - set(HIGH_PRIMES)),
    }


def finite_summary(values):
    ordered = sorted(values)
    return {
        "count": len(ordered),
        "minimum": ordered[0] if ordered else None,
        "maximum": ordered[-1] if ordered else None,
    }


def build_receipt():
    ledger = json.loads(SOURCE_LEDGER.read_text(encoding="utf-8"))
    parameters = scale_parameters(SCALE)
    row_count = parameters["row_count"]
    active_start = row_count
    lower = 50 * row_count + 1
    upper = 60 * row_count
    _, cells_by_denominator = _residue_cells_by_denominator(
        PRIME,
        row_count,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    denominators = sorted(cells_by_denominator)
    original_replacement_qs = {
        row["reduced_denominator"]
        for row in ledger["replacement_one_coordinate_rows"]
    }
    packets = raw_packets(parameters, denominators)
    adverse_values, _diagonal = paired_distance_values(
        DENOMINATOR,
        cells_by_denominator[DENOMINATOR],
        row_count,
        active_start,
    )
    adverse_distance_metric = band_metric(adverse_values, lower, upper)

    rows = []
    for q in denominators:
        ratio = one_coordinate_ratio(
            q, cells_by_denominator[q], row_count, active_start)
        distance_metric = None
        share_gap = None
        total_gap = None
        if q // 2 >= upper:
            distance_values, _diagonal = paired_distance_values(
                q, cells_by_denominator[q], row_count, active_start)
            distance_metric = band_metric(distance_values, lower, upper)
            share_gap = (
                distance_metric["positive_fraction_of_absolute"]
                - adverse_distance_metric["positive_fraction_of_absolute"])
            total_gap = (
                distance_metric["total_over_diagonal"]
                - adverse_distance_metric["total_over_diagonal"])
        rows.append({
            "reduced_denominator": q,
            "role": (
                "q46189_adverse"
                if q == DENOMINATOR
                else "original_replacement"
                if q in original_replacement_qs
                else "unused_same_source_denominator"),
            **arithmetic_profile(q),
            **ratio,
            **packets[q],
            "frozen_50A_to_60A_metric": distance_metric,
            "frozen_50A_to_60A_positive_fraction_gap_vs_q46189": share_gap,
            "frozen_50A_to_60A_total_gap_vs_q46189": total_gap,
        })

    q46189 = next(row for row in rows if row["reduced_denominator"] == DENOMINATOR)
    nonadverse = [row for row in rows if row["reduced_denominator"] != DENOMINATOR]
    nonadverse_below_half = [
        row for row in nonadverse if row["ratio_minus_half"] <= 0]
    six_pair_rows = [
        row for row in rows if row["ordered_source_conductor_pair_count"] == 6]
    scalar_identity_rows = [
        row for row in rows if row["raw_scalar_identity_holds_to_tolerance"]]
    distance_share_failures = [
        row for row in nonadverse
        if row["frozen_50A_to_60A_positive_fraction_gap_vs_q46189"] is not None
        and row["frozen_50A_to_60A_positive_fraction_gap_vs_q46189"] <= 0
    ]
    weakest_ratio = min(nonadverse, key=lambda row: row["ratio_minus_half"])
    strongest_ratio = max(nonadverse, key=lambda row: row["ratio_minus_half"])
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_packet_ratio_landscape",
        "source_one_coordinate_ratio_ledger": str(SOURCE_LEDGER),
        "source_counterexample_reachability_audit": str(SOURCE_REACHABILITY),
        "question": (
            "After q=16302 falsifies the broad frozen 50A..60A selector, "
            "does the one-coordinate active/full ratio target survive on the "
            "broader same-source packet landscape?"),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": row_count,
            "active_row_start": active_start,
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "adverse_denominator": DENOMINATOR,
            "original_replacement_denominators": sorted(
                original_replacement_qs),
            "frozen_distance_range_for_comparison": [lower, upper],
        },
        "landscape_summary": {
            "same_source_denominator_count": len(rows),
            "nonadverse_denominator_count": len(nonadverse),
            "six_pair_packet_count": len(six_pair_rows),
            "raw_scalar_identity_count": len(scalar_identity_rows),
            "nonadverse_ratio_above_half_count": (
                len(nonadverse) - len(nonadverse_below_half)),
            "nonadverse_ratio_below_or_equal_half_count": (
                len(nonadverse_below_half)),
            "q46189_ratio_minus_half": q46189["ratio_minus_half"],
            "minimum_nonadverse_ratio_minus_half": (
                weakest_ratio["ratio_minus_half"]),
            "minimum_nonadverse_ratio_denominator": (
                weakest_ratio["reduced_denominator"]),
            "maximum_nonadverse_ratio_minus_half": (
                strongest_ratio["ratio_minus_half"]),
            "maximum_nonadverse_ratio_denominator": (
                strongest_ratio["reduced_denominator"]),
            "frozen_50A_to_60A_positive_fraction_failure_count": (
                len(distance_share_failures)),
            "frozen_50A_to_60A_positive_fraction_failures": [
                row["reduced_denominator"] for row in distance_share_failures],
            "ratio_minus_half_summary_nonadverse": finite_summary(
                [row["ratio_minus_half"] for row in nonadverse]),
        },
        "q46189_row": q46189,
        "weakest_nonadverse_ratio_row": weakest_ratio,
        "rows": rows,
        "classification": {
            "q46189_unique_below_half_in_checked_landscape": (
                q46189["ratio_minus_half"] < 0
                and len(nonadverse_below_half) == 0),
            "q16302_distance_selector_failure_but_ratio_positive": any(
                row["reduced_denominator"] == 16302
                and row["ratio_minus_half"] > 0
                and row[
                    "frozen_50A_to_60A_positive_fraction_gap_vs_q46189"] < 0
                for row in rows),
            "distance_window_selector_demoted": True,
            "one_coordinate_ratio_landscape_survives_finite_check": (
                q46189["ratio_minus_half"] < 0
                and len(nonadverse_below_half) == 0),
            "finite_landscape_audit_only": True,
            "universal_ratio_theorem_proved": False,
        },
        "candidate_next_action": {
            "name": "symbolic active/full ratio inequality over packets",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Distance-window localization was too brittle, but the "
                "coordinate-00 active/full ratio may be controlled by the "
                "source-packet Dirichlet kernel across the same local "
                "denominator landscape."),
            "prediction": (
                "A symbolic or interval proof should show Q=46189 sits just "
                "below one half while every same-source packet in this local "
                "landscape sits above one half, including q=16302."),
            "falsifier": (
                "A same-source nonadverse packet with active/full ratio at or "
                "below one half would falsify the broad ratio target."),
            "smallest_next_test": (
                "Decompose the weakest positive nonadverse denominator "
                "q=38038 and Q=46189 into exact active-minus-half kernel terms "
                "to identify the sign-deciding term."),
        },
        "decision": (
            "The reachable q=16302 packet demotes the 50A..60A selector, but "
            "it does not demote the one-coordinate active/full ratio target. "
            "In the checked same-source landscape, Q=46189 is the unique row "
            "below one half; all 34 nonadverse denominators are above one "
            "half.  The theorem-shaped target shifts from distance-window "
            "selection to a symbolic active/full energy-ratio inequality."),
        "finite_packet_ratio_landscape_audit_only": True,
        "finite_diagnostic_only": True,
        "natural_selector_theorem_proved": False,
        "distance_slice_positive_share_theorem_proved": False,
        "one_coordinate_active_full_ratio_theorem_proved": False,
        "packet_landscape_ratio_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    summary = receipt["landscape_summary"]
    weakest = receipt["weakest_nonadverse_ratio_row"]
    qrow = receipt["q46189_row"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 packet-ratio landscape audit",
        "",
        "## Question",
        "",
        "After `q=16302` falsifies the broad frozen `50A..60A` selector, does",
        "the one-coordinate active/full ratio target survive on the broader",
        "same-source packet landscape?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_packet_ratio_landscape_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-packet-ratio-landscape-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"same-source denominators:              {summary['same_source_denominator_count']}",
        f"nonadverse denominators:               {summary['nonadverse_denominator_count']}",
        f"six-pair packets:                      {summary['six_pair_packet_count']}",
        f"raw scalar-identity rows:              {summary['raw_scalar_identity_count']}",
        f"Q=46189 ratio minus half:              {summary['q46189_ratio_minus_half']}",
        f"nonadverse ratio-above-half count:     {summary['nonadverse_ratio_above_half_count']} / {summary['nonadverse_denominator_count']}",
        f"nonadverse ratio <= half count:        {summary['nonadverse_ratio_below_or_equal_half_count']}",
        f"weakest nonadverse denominator:        {summary['minimum_nonadverse_ratio_denominator']}",
        f"weakest nonadverse ratio minus half:   {summary['minimum_nonadverse_ratio_minus_half']}",
        f"strongest nonadverse denominator:      {summary['maximum_nonadverse_ratio_denominator']}",
        f"strongest nonadverse ratio minus half: {summary['maximum_nonadverse_ratio_minus_half']}",
        f"50A..60A share failures still present: {summary['frozen_50A_to_60A_positive_fraction_failures']}",
        "```",
        "",
        "The weakest positive nonadverse row is:",
        "",
        "```text",
        f"q:                         {weakest['reduced_denominator']}",
        f"factorization:             {weakest['factorization']}",
        f"role:                      {weakest['role']}",
        f"ratio minus half:          {weakest['ratio_minus_half']}",
        f"ordered source pairs:      {weakest['ordered_source_conductor_pair_count']}",
        f"raw scalar:                {weakest['raw_scalar_real']}",
        "```",
        "",
        "For comparison, the adverse row is:",
        "",
        "```text",
        f"q:                         {qrow['reduced_denominator']}",
        f"ratio minus half:          {qrow['ratio_minus_half']}",
        f"ordered source pairs:      {qrow['ordered_source_conductor_pair_count']}",
        f"raw scalar:                {qrow['raw_scalar_real']}",
        "```",
        "",
        "## Decision",
        "",
        "The `50A..60A` selector remains demoted: `q=16302` is still a",
        "positive-share failure for that frozen distance window.  But the",
        "one-coordinate active/full ratio target survives the broader finite",
        "landscape.  `Q=46189` is the unique row below one half, while all",
        "`34/34` nonadverse same-source denominators are above one half.",
        "",
        "This changes the useful theorem target.  Do not rescue the distance",
        "selector; aim at a symbolic active/full energy-ratio inequality for",
        "the packet landscape, starting with the tight pair `Q=46189` versus",
        "`q=38038`.",
        "",
        "This is finite diagnostic evidence only.  It proves no one-coordinate",
        "active/full ratio theorem, packet-landscape theorem, strict-central",
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
    summary = receipt["landscape_summary"]
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "q46189_ratio_minus_half": summary["q46189_ratio_minus_half"],
        "nonadverse_ratio_above_half_count": (
            summary["nonadverse_ratio_above_half_count"]),
        "nonadverse_denominator_count": (
            summary["nonadverse_denominator_count"]),
        "weakest_nonadverse_denominator": (
            summary["minimum_nonadverse_ratio_denominator"]),
        "distance_selector_failures": (
            summary["frozen_50A_to_60A_positive_fraction_failures"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

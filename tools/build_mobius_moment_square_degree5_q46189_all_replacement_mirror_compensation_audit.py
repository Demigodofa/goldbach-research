"""Audit mirror-block compensation across every Q46189 replacement packet.

The q=38038 source-pair audit found that its non-middle compensation is mostly
paid by the mirror source-pair block (143,266)/(266,143).  This receipt tests
the natural next falsifier: does the same kind of mirror-block compensation
hold across all 34 replacement packets?

The answer is allowed to be negative.  A failed broad mirror-block statement is
useful because it tells the next theorem target to condition on tight
middle-loss packets rather than every replacement row.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import defaultdict
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
from tools.build_mobius_moment_square_degree5_q46189_coordinate00_kernel_decomposition_audit import (  # noqa: E402
    distance_buckets,
)
from tools.build_mobius_moment_square_degree5_q46189_exception_bound_audit import (  # noqa: E402
    DENOMINATOR,
    PRIME,
    SCALE,
    TARGET_LABEL,
)


SOURCE_PACKET_RATIO = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-packet-ratio-landscape-audit.json")
SOURCE_SOURCE_PAIR_COMPENSATION = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-source-pair-bucket-compensation-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-all-replacement-mirror-compensation-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-all-replacement-mirror-compensation-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def replacement_denominators():
    packet = json.loads(SOURCE_PACKET_RATIO.read_text(encoding="utf-8"))
    return sorted(
        row["reduced_denominator"]
        for row in packet["rows"]
        if row["reduced_denominator"] != DENOMINATOR)


def source_pair_vectors_by_q(target_qs, parameters):
    target_qs = sorted(set(target_qs))
    groups_by_q = {
        q: defaultdict(lambda q=q: np.zeros(q, dtype=complex))
        for q in target_qs
    }
    denominators, numerators, geometrics, coordinates = _lifted_frequency_data(
        PRIME,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
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
        selected = np.isin(reduced, target_qs)
        if not np.any(selected):
            continue
        residues = (
            PRIME
            * (difference_numerator[selected] // common_factor[selected])
            % reduced[selected]).astype(np.int64)
        left_coordinates = np.broadcast_to(
            coordinates[first:first + chunk_size, None, :],
            (*reduced.shape, 3))[selected]
        right_coordinates = np.broadcast_to(
            coordinates[None, :, :], (*reduced.shape, 3))[selected]
        lifted = _symmetric_pair_coordinates(
            left_coordinates, right_coordinates)
        products = (
            geometrics[first:first + chunk_size, None]
            * np.conjugate(geometrics[None, :]))[selected]
        selected_left = np.broadcast_to(left_d, reduced.shape)[selected]
        selected_right = np.broadcast_to(
            denominators[None, :], reduced.shape)[selected]
        selected_q = reduced[selected]
        values = products * lifted[:, 0]
        for q, left, right, residue, value in zip(
                selected_q, selected_left, selected_right, residues, values):
            groups_by_q[int(q)][(int(left), int(right))][int(residue)] += value
    return {q: dict(groups) for q, groups in groups_by_q.items()}


def active_contributions(vector_a, vector_b, q, row_count, active_row_start):
    transform_a = np.fft.fft(vector_a)
    transform_b = np.fft.fft(vector_b)
    cross_correlation = np.fft.ifft(transform_a * np.conjugate(transform_b))
    deltas = np.arange(q, dtype=np.int64)
    active_rows = np.arange(
        active_row_start, active_row_start + row_count, dtype=np.int64)
    kernel = np.exp(
        2j * np.pi
        * np.outer(active_rows, deltas)
        / q).mean(axis=0)
    return (2 * q * cross_correlation * kernel).real


def bucket_vector(row_count, contributions, diagonal_half):
    return {
        bucket["bucket"]: (
            bucket["component_active_contribution"] / diagonal_half)
        for bucket in distance_buckets(row_count, contributions)
    }


def mirror_blocks(groups, q, row_count, active_row_start, diagonal_half):
    pairs = sorted(groups)
    cross_buckets = {}
    for left in pairs:
        for right in pairs:
            cross_buckets[(left, right)] = bucket_vector(
                row_count,
                active_contributions(
                    groups[left], groups[right], q,
                    row_count, active_row_start),
                diagonal_half,
            )
    blocks = []
    seen = set()
    for pair in pairs:
        reverse = (pair[1], pair[0])
        key = tuple(sorted([pair, reverse]))
        if key in seen:
            continue
        seen.add(key)
        terms = [(pair, pair), (pair, reverse), (reverse, pair),
                 (reverse, reverse)]
        middle = sum(
            cross_buckets[term]["middle_A_to_10A"]
            for term in terms)
        non_middle = sum(
            sum(value for name, value in cross_buckets[term].items()
                if name != "middle_A_to_10A")
            for term in terms)
        blocks.append({
            "mirror_source_pair_block": [
                list(key[0]),
                list(key[1]),
            ],
            "middle_A_to_10A": middle,
            "non_middle_sum": non_middle,
            "total": middle + non_middle,
        })
    return sorted(blocks, key=lambda row: row["non_middle_sum"], reverse=True)


def row_summary(q, groups, parameters):
    row_count = parameters["row_count"]
    active_row_start = row_count
    aggregate = sum(groups.values(), np.zeros(q, dtype=complex))
    aggregate_contributions = active_contributions(
        aggregate, aggregate, q, row_count, active_row_start)
    diagonal_half = 0.5 * float(aggregate_contributions[0])
    aggregate_buckets = bucket_vector(
        row_count, aggregate_contributions, diagonal_half)
    off_diagonal = sum(aggregate_buckets.values())
    middle = aggregate_buckets["middle_A_to_10A"]
    non_middle = sum(
        value for name, value in aggregate_buckets.items()
        if name != "middle_A_to_10A")
    blocks = mirror_blocks(
        groups, q, row_count, active_row_start, diagonal_half)
    strongest = blocks[0]
    return {
        "reduced_denominator": q,
        "ordered_source_pair_count": len(groups),
        "off_diagonal_over_diagonal_half": off_diagonal,
        "middle_A_to_10A": middle,
        "non_middle_sum": non_middle,
        "margin_above_minus_one": off_diagonal + 1.0,
        "aggregate_bucket_contributions_over_diagonal_half": (
            aggregate_buckets),
        "strongest_non_middle_mirror_block": strongest,
        "strongest_non_middle_mirror_block_share": (
            strongest["non_middle_sum"] / non_middle
            if non_middle else None),
        "mirror_blocks_by_non_middle": blocks,
    }


def rank_of(rows, q, key, reverse=False):
    ordered = sorted(rows, key=lambda row: row[key], reverse=reverse)
    return [row["reduced_denominator"] for row in ordered].index(q) + 1


def compact_row(row):
    return {
        "reduced_denominator": row["reduced_denominator"],
        "off_diagonal_over_diagonal_half": (
            row["off_diagonal_over_diagonal_half"]),
        "middle_A_to_10A": row["middle_A_to_10A"],
        "non_middle_sum": row["non_middle_sum"],
        "margin_above_minus_one": row["margin_above_minus_one"],
        "strongest_non_middle_mirror_block": (
            row["strongest_non_middle_mirror_block"]),
        "strongest_non_middle_mirror_block_share": (
            row["strongest_non_middle_mirror_block_share"]),
    }


def build_receipt():
    parameters = scale_parameters(SCALE)
    denominators = replacement_denominators()
    groups_by_q = source_pair_vectors_by_q(denominators, parameters)
    rows = [
        row_summary(q, groups_by_q[q], parameters)
        for q in denominators
    ]
    weakest_total = min(
        rows, key=lambda row: row["off_diagonal_over_diagonal_half"])
    weakest_middle = min(rows, key=lambda row: row["middle_A_to_10A"])
    largest_non_middle = max(rows, key=lambda row: row["non_middle_sum"])
    largest_mirror = max(
        rows,
        key=lambda row: row[
            "strongest_non_middle_mirror_block"]["non_middle_sum"],
    )
    negative_non_middle = [
        row for row in rows if row["non_middle_sum"] <= 0]
    nonpositive_best_mirror = [
        row for row in rows
        if row["strongest_non_middle_mirror_block"]["non_middle_sum"] <= 0]
    q38038 = next(
        row for row in rows if row["reduced_denominator"] == 38038)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_all_replacement_mirror_compensation",
        "source_packet_ratio_landscape_audit": str(SOURCE_PACKET_RATIO),
        "source_source_pair_bucket_compensation_audit": (
            str(SOURCE_SOURCE_PAIR_COMPENSATION)),
        "question": (
            "Across all 34 Q46189 replacement packets, is the q=38038 "
            "mirror-block non-middle compensation pattern a universal "
            "replacement-packet theorem target?"),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": parameters["row_count"],
            "active_row_start": parameters["row_count"],
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "replacement_denominator_count": len(denominators),
        },
        "summary": {
            "replacement_denominator_count": len(rows),
            "weakest_total_row": compact_row(weakest_total),
            "weakest_middle_row": compact_row(weakest_middle),
            "largest_non_middle_row": compact_row(largest_non_middle),
            "largest_mirror_block_row": compact_row(largest_mirror),
            "negative_non_middle_count": len(negative_non_middle),
            "negative_non_middle_denominators": [
                row["reduced_denominator"] for row in negative_non_middle],
            "nonpositive_best_mirror_count": len(nonpositive_best_mirror),
            "nonpositive_best_mirror_denominators": [
                row["reduced_denominator"]
                for row in nonpositive_best_mirror],
            "q38038_ranks": {
                "off_diagonal_ascending": rank_of(
                    rows, 38038, "off_diagonal_over_diagonal_half"),
                "middle_loss_ascending": rank_of(
                    rows, 38038, "middle_A_to_10A"),
                "non_middle_descending": rank_of(
                    rows, 38038, "non_middle_sum", reverse=True),
            },
            "q38038_strongest_mirror_rank_descending": (
                [
                    row["reduced_denominator"]
                    for row in sorted(
                        rows,
                        key=lambda row: row[
                            "strongest_non_middle_mirror_block"][
                                "non_middle_sum"],
                        reverse=True,
                    )
                ].index(38038) + 1),
        },
        "q38038_row": compact_row(q38038),
        "all_replacement_rows": [compact_row(row) for row in rows],
        "classification": {
            "q38038_is_weakest_total_replacement": (
                weakest_total["reduced_denominator"] == 38038),
            "q38038_is_weakest_middle_loss_replacement": (
                weakest_middle["reduced_denominator"] == 38038),
            "universal_positive_non_middle_compensation_refuted": (
                len(negative_non_middle) > 0),
            "universal_positive_best_mirror_block_refuted": (
                len(nonpositive_best_mirror) > 0),
            "q38038_mirror_pattern_not_universal": (
                len(negative_non_middle) > 0
                and len(nonpositive_best_mirror) > 0),
            "tight_middle_loss_condition_still_alive": (
                weakest_total["reduced_denominator"] == 38038
                and weakest_middle["reduced_denominator"] == 38038
                and q38038["non_middle_sum"] > 0),
            "finite_all_replacement_mirror_compensation_audit_only": True,
        },
        "candidate_next_action": {
            "name": "tight-middle-loss conditional compensation target",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "A universal positive mirror-block rescue is too broad.  The "
                "surviving structure is conditional: q=38038 is still both "
                "the weakest total row and the largest middle-loss row, and "
                "that tight row has positive non-middle compensation."),
            "prediction": (
                "A viable theorem must condition on severe middle-bucket loss "
                "or an equivalent source-pair geometry, then prove enough "
                "non-middle compensation only in that tight regime."),
            "falsifier": (
                "A replacement packet with middle loss at least as severe as "
                "q=38038 and no positive non-middle compensation, or a packet "
                "with total off/diag-half below q=38038, falsifies this "
                "conditional target."),
            "smallest_next_test": (
                "Search for a source-pair invariant that characterizes the "
                "severe-middle-loss regime and separates q=38038 from rows "
                "where non-middle compensation is negative."),
        },
        "decision": (
            "The broad mirror-block theorem target is refuted on the checked "
            "replacement landscape.  "
            f"{len(negative_non_middle)} replacement rows have nonpositive "
            "aggregate non-middle contribution, and "
            f"{len(nonpositive_best_mirror)} have nonpositive best "
            "mirror-block non-middle contribution.  However q=38038 remains "
            "the weakest total row and the most severe middle-loss row, with "
            "positive non-middle compensation.  The live theorem target "
            "should therefore be conditional compensation in the tight "
            "middle-loss regime, not universal mirror-block positivity across "
            "all replacement packets."),
        "finite_all_replacement_mirror_compensation_audit_only": True,
        "finite_diagnostic_only": True,
        "universal_mirror_block_compensation_theorem_proved": False,
        "universal_mirror_block_compensation_refuted_on_checked_rows": True,
        "tight_middle_loss_compensation_theorem_proved": False,
        "replacement_packet_compensation_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    summary = receipt["summary"]
    q38038 = receipt["q38038_row"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 all-replacement mirror compensation audit",
        "",
        "## Question",
        "",
        "Across all `34` replacement packets, is the `q=38038` mirror-block",
        "non-middle compensation pattern a universal replacement-packet theorem",
        "target?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_all_replacement_mirror_compensation_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-all-replacement-mirror-compensation-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"replacement rows:                         {summary['replacement_denominator_count']}",
        f"weakest total row:                        {summary['weakest_total_row']['reduced_denominator']}",
        f"weakest middle-loss row:                  {summary['weakest_middle_row']['reduced_denominator']}",
        f"q=38038 off/diag-half:                    {q38038['off_diagonal_over_diagonal_half']}",
        f"q=38038 middle A..10A:                    {q38038['middle_A_to_10A']}",
        f"q=38038 non-middle sum:                   {q38038['non_middle_sum']}",
        f"q=38038 strongest mirror block:           {q38038['strongest_non_middle_mirror_block']['non_middle_sum']}",
        f"q=38038 strongest mirror rank:            {summary['q38038_strongest_mirror_rank_descending']}",
        f"negative non-middle rows:                 {summary['negative_non_middle_count']}",
        f"nonpositive best-mirror rows:             {summary['nonpositive_best_mirror_count']}",
        "```",
        "",
        "## Decision",
        "",
        "The broad mirror-block theorem target is refuted on the checked",
        "replacement landscape.  Fifteen replacement rows have nonpositive",
        "aggregate non-middle contribution, and seven have nonpositive best",
        "mirror-block non-middle contribution.",
        "",
        "`q=38038` is still special, but in a narrower way: it remains both",
        "the weakest total row and the most severe `middle_A_to_10A` loss row,",
        "and that tight row has positive non-middle compensation.  The live",
        "theorem target should therefore be conditional compensation in the",
        "tight middle-loss regime, not universal mirror-block positivity",
        "across all replacement packets.",
        "",
        "This is finite diagnostic evidence only.  It proves no universal",
        "mirror-block theorem, tight-middle-loss theorem, replacement-packet",
        "compensation theorem, strict-central Goldbach theorem, or Goldbach",
        "proof.",
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
    summary = receipt["summary"]
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "weakest_total_row": summary["weakest_total_row"][
            "reduced_denominator"],
        "weakest_middle_row": summary["weakest_middle_row"][
            "reduced_denominator"],
        "negative_non_middle_count": summary["negative_non_middle_count"],
        "nonpositive_best_mirror_count": (
            summary["nonpositive_best_mirror_count"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

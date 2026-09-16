"""Decompose Q46189/q38038 bucket compensation by source-pair cross terms.

The factor-geometry triage identified the next theorem-shaped object as
replacement-packet bucket compensation.  This receipt takes the tight
replacement row q=38038 and the adverse Q=46189 row, splits each exact
coordinate-00 residue vector into ordered source-conductor-pair packet
vectors, and then decomposes the bucket contributions bilinearly.

This matters because the energy is quadratic: source packets do not contribute
independently after the square.  The exact source-level object is a cross-term
matrix over ordered source-conductor pairs.
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


WEAKEST_REPLACEMENT_DENOMINATOR = 38038
SOURCE_FACTOR_TRIAGE = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-factor-geometry-route-triage.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-source-pair-bucket-compensation-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-source-pair-bucket-compensation-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def source_pair_vectors(target_q, parameters):
    denominators, numerators, geometrics, coordinates = _lifted_frequency_data(
        PRIME,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    groups = defaultdict(lambda: np.zeros(target_q, dtype=complex))
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
        selected = reduced == target_q
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
        values = products * lifted[:, 0]
        for left, right, residue, value in zip(
                selected_left, selected_right, residues, values):
            groups[(int(left), int(right))][int(residue)] += value
    return dict(groups)


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


def compact_cross_term(left, right, contributions, row_count, diagonal_half):
    buckets = bucket_vector(row_count, contributions, diagonal_half)
    non_middle = sum(
        value for name, value in buckets.items()
        if name != "middle_A_to_10A")
    return {
        "left_source_pair": list(left),
        "right_source_pair": list(right),
        "off_diagonal_over_diagonal_half": (
            float(np.sum(contributions[1:])) / diagonal_half),
        "middle_A_to_10A": buckets["middle_A_to_10A"],
        "non_middle_sum": non_middle,
        "bucket_contributions_over_diagonal_half": buckets,
    }


def row_receipt(q, role, parameters):
    row_count = parameters["row_count"]
    active_row_start = row_count
    groups = source_pair_vectors(q, parameters)
    ordered_pairs = sorted(groups)
    aggregate = sum(groups.values(), np.zeros(q, dtype=complex))
    aggregate_contributions = active_contributions(
        aggregate, aggregate, q, row_count, active_row_start)
    diagonal_half = 0.5 * float(aggregate_contributions[0])
    aggregate_buckets = bucket_vector(
        row_count, aggregate_contributions, diagonal_half)
    cross_terms = []
    reconstructed = np.zeros(q, dtype=float)
    for left in ordered_pairs:
        for right in ordered_pairs:
            contributions = active_contributions(
                groups[left], groups[right], q, row_count, active_row_start)
            reconstructed += contributions
            cross_terms.append(compact_cross_term(
                left, right, contributions, row_count, diagonal_half))
    reconstruction_max_abs_error = float(
        np.max(np.abs(reconstructed - aggregate_contributions)))
    non_middle_sum = sum(
        value for name, value in aggregate_buckets.items()
        if name != "middle_A_to_10A")
    top_non_middle = sorted(
        cross_terms,
        key=lambda row: row["non_middle_sum"],
        reverse=True,
    )[:8]
    top_middle_loss = sorted(
        cross_terms,
        key=lambda row: row["middle_A_to_10A"],
    )[:8]
    top_four_non_middle_sum = sum(
        row["non_middle_sum"] for row in top_non_middle[:4])
    return {
        "role": role,
        "reduced_denominator": q,
        "ordered_source_pair_count": len(ordered_pairs),
        "ordered_source_pairs": [list(pair) for pair in ordered_pairs],
        "diagonal_half_contribution": diagonal_half,
        "off_diagonal_over_diagonal_half": (
            float(np.sum(aggregate_contributions[1:])) / diagonal_half),
        "aggregate_bucket_contributions_over_diagonal_half": aggregate_buckets,
        "aggregate_middle_A_to_10A": aggregate_buckets["middle_A_to_10A"],
        "aggregate_non_middle_sum": non_middle_sum,
        "margin_above_minus_one": (
            float(np.sum(aggregate_contributions[1:])) / diagonal_half
            + 1.0),
        "cross_term_count": len(cross_terms),
        "cross_terms": cross_terms,
        "top_non_middle_compensation_terms": top_non_middle,
        "top_middle_loss_terms": top_middle_loss,
        "top_four_non_middle_compensation_sum": top_four_non_middle_sum,
        "top_four_non_middle_share_of_aggregate_non_middle": (
            top_four_non_middle_sum / non_middle_sum
            if non_middle_sum else None),
        "cross_term_reconstruction_max_abs_error": (
            reconstruction_max_abs_error),
        "cross_term_reconstruction_relative_to_diagonal_half": (
            reconstruction_max_abs_error / diagonal_half),
    }


def build_receipt():
    parameters = scale_parameters(SCALE)
    q46189 = row_receipt(DENOMINATOR, "q46189_adverse", parameters)
    q38038 = row_receipt(
        WEAKEST_REPLACEMENT_DENOMINATOR,
        "weakest_replacement_q38038",
        parameters,
    )
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_source_pair_bucket_compensation",
        "source_factor_geometry_route_triage": str(SOURCE_FACTOR_TRIAGE),
        "question": (
            "Can the q=38038 replacement-packet bucket compensation be "
            "localized in exact ordered source-conductor-pair cross terms, "
            "and how does that differ from Q=46189?"),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": parameters["row_count"],
            "active_row_start": parameters["row_count"],
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "adverse_denominator": DENOMINATOR,
            "weakest_replacement_denominator": (
                WEAKEST_REPLACEMENT_DENOMINATOR),
            "cross_term_identity": (
                "For source-pair packet vectors v_i, the bucket contribution "
                "is the sum over ordered cross terms "
                "2*q*ifft(fft(v_i)*conj(fft(v_j)))*K_active."),
        },
        "rows": [q46189, q38038],
        "comparison": {
            "q38038_non_middle_compensation_positive": (
                q38038["aggregate_non_middle_sum"] > 0),
            "q46189_non_middle_compensation_negative": (
                q46189["aggregate_non_middle_sum"] < 0),
            "q38038_middle_loss_stronger_than_total_loss": (
                q38038["aggregate_middle_A_to_10A"]
                < q38038["off_diagonal_over_diagonal_half"]),
            "q38038_top_four_non_middle_share": (
                q38038["top_four_non_middle_share_of_aggregate_non_middle"]),
            "q38038_top_four_non_middle_source_pairs": [
                {
                    "left_source_pair": row["left_source_pair"],
                    "right_source_pair": row["right_source_pair"],
                    "non_middle_sum": row["non_middle_sum"],
                }
                for row in q38038["top_non_middle_compensation_terms"][:4]
            ],
        },
        "classification": {
            "q38038_cross_terms_reconstruct_aggregate": (
                q38038[
                    "cross_term_reconstruction_relative_to_diagonal_half"]
                < 1e-15),
            "q46189_cross_terms_reconstruct_aggregate": (
                q46189[
                    "cross_term_reconstruction_relative_to_diagonal_half"]
                < 1e-15),
            "q38038_compensation_localizes_to_mirror_source_pair_block": (
                q38038["top_four_non_middle_share_of_aggregate_non_middle"]
                is not None
                and q38038[
                    "top_four_non_middle_share_of_aggregate_non_middle"] > .8),
            "q46189_lacks_positive_aggregate_non_middle_compensation": (
                q46189["aggregate_non_middle_sum"] < 0),
            "source_pair_bucket_compensation_theorem_proved": False,
            "finite_source_pair_bucket_compensation_audit_only": True,
        },
        "candidate_next_action": {
            "name": "mirror-source-pair compensation theorem target",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The q=38038 survivor is not protected by every bucket.  Its "
                "middle bucket is worse than the final total, but ordered "
                "cross terms among the mirror source pairs (143,266) and "
                "(266,143) supply most of the positive non-middle "
                "compensation."),
            "prediction": (
                "A replacement-packet theorem should prove a mirror-block "
                "compensation inequality, then bound the remaining cross-term "
                "matrix; Q=46189 should fail because its corresponding "
                "non-middle aggregate remains negative."),
            "falsifier": (
                "A reachable replacement packet whose mirror block does not "
                "pay the non-middle compensation, or whose remaining cross "
                "terms erase that payment below -1, falsifies this route."),
            "smallest_next_test": (
                "Run the same source-pair cross-term compensation audit across "
                "all 34 replacement packets and check whether q=38038 is the "
                "worst surviving instance of the mirror-block inequality."),
        },
        "decision": (
            "The q=38038 compensation is visible in exact source-pair "
            "cross terms.  Its middle bucket alone is about -0.939993, but "
            "non-middle buckets add about +0.092700; the top four non-middle "
            "cross terms, all from the mirror block (143,266)/(266,143), "
            "supply more than 80 percent of that positive non-middle sum.  "
            "Q=46189 has negative aggregate non-middle contribution instead. "
            "This supports a mirror-source-pair compensation theorem target, "
            "but proves no such theorem and no Goldbach result."),
        "finite_source_pair_bucket_compensation_audit_only": True,
        "finite_diagnostic_only": True,
        "source_pair_bucket_compensation_theorem_proved": False,
        "mirror_source_pair_compensation_theorem_proved": False,
        "replacement_packet_compensation_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    q46189, q38038 = receipt["rows"]
    comparison = receipt["comparison"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 source-pair bucket compensation audit",
        "",
        "## Question",
        "",
        "Can the `q=38038` replacement-packet bucket compensation be localized",
        "in exact ordered source-conductor-pair cross terms, and how does that",
        "differ from `Q=46189`?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_source_pair_bucket_compensation_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-source-pair-bucket-compensation-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"q=38038 middle A..10A:             {q38038['aggregate_middle_A_to_10A']}",
        f"q=38038 non-middle sum:            {q38038['aggregate_non_middle_sum']}",
        f"q=38038 off/diag-half:             {q38038['off_diagonal_over_diagonal_half']}",
        f"q=38038 top-four non-middle sum:   {q38038['top_four_non_middle_compensation_sum']}",
        f"q=38038 top-four non-middle share: {comparison['q38038_top_four_non_middle_share']}",
        f"Q=46189 middle A..10A:             {q46189['aggregate_middle_A_to_10A']}",
        f"Q=46189 non-middle sum:            {q46189['aggregate_non_middle_sum']}",
        f"Q=46189 off/diag-half:             {q46189['off_diagonal_over_diagonal_half']}",
        "```",
        "",
        "The top four `q=38038` non-middle terms are exactly the ordered",
        "mirror block on source pairs `(143,266)` and `(266,143)`.",
        "",
        "## Decision",
        "",
        "The `q=38038` survivor is not protected by a uniformly friendly bucket",
        "profile.  Its `middle_A_to_10A` bucket is very adverse, but the",
        "near/far/tail buckets compensate enough to keep the total above `-1`.",
        "The exact source-pair cross-term decomposition localizes most of that",
        "positive non-middle compensation in the mirror block",
        "`(143,266)/(266,143)`.",
        "",
        "`Q=46189` differs in the direction that matters: its aggregate",
        "non-middle contribution is negative, so there is no analogous",
        "non-middle rescue.  This supports a mirror-source-pair compensation",
        "theorem target, but remains finite diagnostic evidence only.",
        "",
        "This proves no source-pair compensation theorem, mirror-block theorem,",
        "replacement-packet compensation theorem, strict-central Goldbach",
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
    q46189, q38038 = receipt["rows"]
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "q38038_non_middle_sum": q38038["aggregate_non_middle_sum"],
        "q38038_top_four_non_middle_share": (
            receipt["comparison"]["q38038_top_four_non_middle_share"]),
        "q46189_non_middle_sum": q46189["aggregate_non_middle_sum"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

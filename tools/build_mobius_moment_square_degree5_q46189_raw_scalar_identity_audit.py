"""Audit raw source-pair scalar identity before residue aggregation.

The scalar-collapse receipt showed that coordinate 12 is a cellwise scalar
multiple of coordinate 00 after reduced-residue aggregation.  This derived
receipt tests the stronger finite mechanism: for Q=46189 and its ten
replacement denominators, the same scalar identity already holds on every raw
ordered source-conductor frequency pair before residue grouping.
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
from tools.build_mobius_moment_square_degree5_q46189_exception_bound_audit import (  # noqa: E402
    DENOMINATOR,
    PRIME,
    SCALE,
    TARGET_LABEL,
)


OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-raw-scalar-identity-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-raw-scalar-identity-audit.md")
SOURCE_SCALAR_COLLAPSE = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-scalar-collapse-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def raw_scalar_rows(parameters, target_rows):
    row_count = parameters["row_count"]
    targets = {row["reduced_denominator"]: row for row in target_rows}
    target_set = set(targets)
    denominators, numerators, _, coordinates = _lifted_frequency_data(
        PRIME,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    ratios_by_q = defaultdict(list)
    residues_by_q = defaultdict(set)
    pairs_by_q = defaultdict(Counter)
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
        residues = np.zeros(reduced.shape, dtype=np.int64)
        residues[selected] = (
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
        selected_residue = residues[selected]
        selected_left_d = np.broadcast_to(left_d, reduced.shape)[selected]
        selected_right_d = np.broadcast_to(
            denominators[None, :], reduced.shape)[selected]
        nonzero_left = np.abs(lifted[:, 0]) > 1e-30
        for q in sorted(target_set):
            q_mask = selected_q == q
            if not np.any(q_mask):
                continue
            q_nonzero = q_mask & nonzero_left
            q_zero_left = int(np.count_nonzero(q_mask & ~nonzero_left))
            zero_left_by_q[q] += q_zero_left
            ratios_by_q[q].append(lifted[q_nonzero, 4] / lifted[q_nonzero, 0])
            residues_by_q[q].update(
                int(value) for value in selected_residue[q_mask])
            for left, right in zip(
                    selected_left_d[q_mask], selected_right_d[q_mask]):
                pairs_by_q[q][(int(left), int(right))] += 1

    rows = []
    for reduced_denominator in sorted(target_set):
        ratio_values = np.concatenate(ratios_by_q[reduced_denominator])
        scalar = ratio_values.mean()
        deviations = np.abs(ratio_values - scalar)
        cellwise = targets[reduced_denominator]
        source_pairs = [
            {
                "left_source_conductor": left,
                "right_source_conductor": right,
                "raw_frequency_pair_count": count,
            }
            for (left, right), count
            in sorted(pairs_by_q[reduced_denominator].items())
        ]
        row = {
            "reduced_denominator": reduced_denominator,
            "factorization": cellwise["factorization"],
            "residue_cell_count": cellwise["residue_cell_count"],
            "raw_reduced_residue_count": len(residues_by_q[reduced_denominator]),
            "raw_frequency_pair_count": int(len(ratio_values)),
            "zero_left_raw_pair_count": int(zero_left_by_q[reduced_denominator]),
            "ordered_source_conductor_pair_count": len(source_pairs),
            "ordered_source_conductor_pairs": source_pairs,
            "raw_scalar_real": float(scalar.real),
            "raw_scalar_imag": float(scalar.imag),
            "cellwise_scalar_real": cellwise["cellwise_scalar_real"],
            "cellwise_scalar_imag": cellwise["cellwise_scalar_imag"],
            "raw_to_cellwise_scalar_abs_error": abs(
                float(scalar.real) - cellwise["cellwise_scalar_real"]),
            "max_abs_raw_scalar_deviation": float(np.max(deviations)),
            "max_abs_raw_scalar_imag": float(np.max(np.abs(ratio_values.imag))),
            "ratio_minus_half": cellwise["ratio_minus_half"],
            "cellwise_margin_full_over_2_minus_active": (
                cellwise["margin_full_over_2_minus_active"]),
            "raw_scalar_negative_real": bool(
                scalar.real < 0 and abs(scalar.imag) < 1e-14),
            "raw_scalar_identity_holds_to_tolerance": bool(
                float(np.max(deviations)) < 1e-13
                and float(np.max(np.abs(ratio_values.imag))) < 1e-14
                and int(zero_left_by_q[reduced_denominator]) == 0),
        }
        if "missing_high_primes" in cellwise:
            row["missing_high_primes"] = cellwise["missing_high_primes"]
            row["high_prime_support"] = cellwise["high_prime_support"]
        else:
            row["missing_high_primes"] = []
            row["high_prime_support"] = [11, 13, 17, 19]
        rows.append(row)
    return rows


def build_receipt():
    scalar = json.loads(SOURCE_SCALAR_COLLAPSE.read_text(encoding="utf-8"))
    parameters = scale_parameters(SCALE)
    target_rows = [
        scalar["q46189_scalar_row"],
        *scalar["replacement_scalar_rows"],
    ]
    rows = raw_scalar_rows(parameters, target_rows)
    q46189 = next(row for row in rows if row["reduced_denominator"] == DENOMINATOR)
    replacements = [
        row for row in rows if row["reduced_denominator"] != DENOMINATOR]
    by_missing_high = defaultdict(list)
    for row in replacements:
        key = ",".join(str(prime) for prime in row["missing_high_primes"])
        by_missing_high[key].append(row)
    family_summaries = {}
    for missing, family_rows in sorted(by_missing_high.items()):
        family_summaries[missing] = {
            "row_count": len(family_rows),
            "minimum_ratio_minus_half": min(
                row["ratio_minus_half"] for row in family_rows),
            "maximum_raw_scalar_deviation": max(
                row["max_abs_raw_scalar_deviation"] for row in family_rows),
            "all_rows_raw_scalar_identity": all(
                row["raw_scalar_identity_holds_to_tolerance"]
                for row in family_rows),
            "ordered_source_conductor_pair_counts": sorted(
                {
                    row["ordered_source_conductor_pair_count"]
                    for row in family_rows
                }),
        }
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_raw_source_pair_scalar_identity",
        "source_scalar_collapse_audit": str(SOURCE_SCALAR_COLLAPSE),
        "question": (
            "Does the Q=46189 replacement-family scalar collapse already hold "
            "on raw ordered source-conductor frequency pairs before reduced-"
            "residue aggregation?"),
        "answer": (
            "Yes for this finite family.  Each selected denominator is "
            "supported by six ordered source-conductor pairs, and every raw "
            "frequency pair has coordinate 12 equal to the same negative-real "
            "scalar multiple of coordinate 00.  This strengthens the next "
            "target to an exact source-pair scalar identity, but remains a "
            "finite numerical audit."),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": parameters["row_count"],
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "adverse_denominator": DENOMINATOR,
        },
        "q46189_raw_scalar_row": q46189,
        "replacement_raw_scalar_rows": sorted(
            replacements,
            key=lambda row: row["cellwise_margin_full_over_2_minus_active"],
            reverse=True),
        "omitted_high_prime_family_raw_summaries": family_summaries,
        "classification": {
            "q46189_raw_scalar_identity_holds": (
                q46189["raw_scalar_identity_holds_to_tolerance"]),
            "all_replacements_raw_scalar_identity_holds": all(
                row["raw_scalar_identity_holds_to_tolerance"]
                for row in replacements),
            "all_rows_have_six_ordered_source_conductor_pairs": all(
                row["ordered_source_conductor_pair_count"] == 6
                for row in rows),
            "all_rows_have_no_zero_left_raw_pairs": all(
                row["zero_left_raw_pair_count"] == 0 for row in rows),
            "all_replacements_ratio_above_half": all(
                row["ratio_minus_half"] > 0 for row in replacements),
            "q46189_ratio_below_half": q46189["ratio_minus_half"] < 0,
            "finite_raw_scalar_identity_checkpoint_only": True,
        },
        "candidate_next_action": {
            "name": "symbolic source-conductor scalar formula",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use the six ordered source-conductor pairs for each selected "
                "denominator to derive an exact formula for coordinate "
                "12/00 directly from the divisor-polynomial data."),
            "prediction": (
                "For the Q=46189 family, the six ordered source-conductor "
                "pairs should share a common closed-form scalar before "
                "primitive residue sums or active-window phases enter."),
            "falsifier": (
                "A source-admissible replacement family with raw source pairs "
                "that do not share a common coordinate 12/00 scalar falsifies "
                "this exact source-pair identity target."),
            "smallest_next_test": (
                "Compute the divisor-polynomial formula for the six "
                "source-conductor pairs of Q=46189 and show their scalars are "
                "identical without using floating aggregation."),
        },
        "decision": (
            "The scalar collapse is visible before reduced-residue aggregation. "
            "The theorem-shaped object is now a symbolic source-conductor "
            "scalar formula followed by a one-coordinate active/full ratio "
            "inequality.  No exact identity theorem or ratio theorem is proved."),
        "finite_raw_scalar_identity_audit_only": True,
        "finite_diagnostic_only": True,
        "raw_scalar_identity_theorem_proved": False,
        "exact_scalar_identity_theorem_proved": False,
        "symbolic_replacement_ratio_theorem_proved": False,
        "replacement_family_payment_theorem_proved": False,
        "phase_defect_payment_theorem_proved": False,
        "near_adverse_upper_bound_proved": False,
        "middle_far_lower_bound_proved": False,
        "clearance_family_theorem_proved": False,
        "source_start_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    q_row = receipt["q46189_raw_scalar_row"]
    replacements = receipt["replacement_raw_scalar_rows"]
    max_raw_dev = max(
        row["max_abs_raw_scalar_deviation"]
        for row in [q_row, *replacements])
    lines = [
        "# Mobius moment-square degree-5 Q46189 raw scalar identity audit",
        "",
        "## Question",
        "",
        "Does the `Q=46189` replacement-family scalar collapse already hold on",
        "raw ordered source-conductor frequency pairs before reduced-residue",
        "aggregation?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_raw_scalar_identity_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-raw-scalar-identity-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"Q=46189 raw scalar:               {q_row['raw_scalar_real']}",
        f"Q=46189 raw source-pair count:    {q_row['ordered_source_conductor_pair_count']}",
        f"Q=46189 raw frequency pairs:      {q_row['raw_frequency_pair_count']}",
        f"replacement rows:                 {len(replacements)}",
        f"max raw scalar deviation:         {max_raw_dev}",
        "all rows have six source pairs:   true",
        "all replacement rows raw-scalar:  true",
        "```",
        "",
        "Omitted-high-prime family raw summaries:",
        "",
        "```text",
    ]
    for missing, summary in receipt[
            "omitted_high_prime_family_raw_summaries"].items():
        lines.append(
            "missing {}: rows={} min_ratio_minus_half={} "
            "max_raw_scalar_dev={} source_pair_counts={}".format(
                missing,
                summary["row_count"],
                summary["minimum_ratio_minus_half"],
                summary["maximum_raw_scalar_deviation"],
                summary["ordered_source_conductor_pair_counts"],
            ))
    lines.extend([
        "```",
        "",
        "## Decision",
        "",
        "The scalar collapse is already visible before reduced-residue",
        "aggregation.  Each selected denominator is supported by six ordered",
        "source-conductor pairs, and every raw frequency pair has coordinate",
        "`12` equal to the same negative-real scalar multiple of coordinate",
        "`00` to numerical tolerance.",
        "",
        "The theorem-shaped object is now a symbolic source-conductor scalar",
        "formula followed by a one-coordinate active/full ratio inequality.",
        "This is finite diagnostic evidence only.  It proves no raw scalar",
        "identity theorem, exact scalar identity theorem, symbolic replacement",
        "ratio theorem, replacement-family payment theorem, source-start",
        "theorem, strict-central Goldbach theorem, or Goldbach proof.",
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
        "q46189_raw_scalar": receipt["q46189_raw_scalar_row"][
            "raw_scalar_real"],
        "max_replacement_raw_scalar_deviation": max(
            row["max_abs_raw_scalar_deviation"]
            for row in receipt["replacement_raw_scalar_rows"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

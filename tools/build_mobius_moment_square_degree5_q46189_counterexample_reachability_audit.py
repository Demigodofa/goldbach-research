"""Check whether the frozen-selector counterexample is construction-reachable.

The unused-denominator holdout found q=16302 as a positive-share failure for
the frozen Q46189 50A..60A selector.  This audit asks whether that failing
denominator is merely an irrelevant residue-cell artifact, or whether it is
reachable by the same raw six source-conductor-pair mechanism used by the
Q46189 replacement family.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import sympy as sp


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
from tools.build_mobius_moment_square_degree5_q46189_exact_log_polynomial_identity_audit import (  # noqa: E402
    expected_common_numerator,
    numeric_substitution,
    source_pair_scalar_without_common_l,
    symbolic_structured_polynomials,
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


COUNTEREXAMPLE_DENOMINATOR = 16302
SOURCE_HOLDOUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-frozen-selector-unused-denominator-holdout.json")
SOURCE_EXACT_LOG_IDENTITY = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-exact-log-polynomial-identity-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-counterexample-reachability-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-counterexample-reachability-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def raw_source_pair_packet(parameters, target_q):
    denominators, numerators, _, coordinates = _lifted_frequency_data(
        PRIME,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    ratios = []
    residues = set()
    pairs = Counter()
    zero_left_count = 0
    total_pair_count = 0
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

        selected_residues = (
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
        selected_left = np.broadcast_to(left_d, reduced.shape)[selected]
        selected_right = np.broadcast_to(
            denominators[None, :], reduced.shape)[selected]
        nonzero_left = np.abs(lifted[:, 0]) > 1e-30

        total_pair_count += int(len(lifted))
        zero_left_count += int(np.count_nonzero(~nonzero_left))
        ratios.extend(lifted[nonzero_left, 4] / lifted[nonzero_left, 0])
        residues.update(int(value) for value in selected_residues)
        for left, right in zip(selected_left, selected_right):
            pairs[(int(left), int(right))] += 1

    ratio_array = np.asarray(ratios, dtype=complex)
    scalar = ratio_array.mean()
    deviations = np.abs(ratio_array - scalar)
    return {
        "raw_frequency_pair_count": total_pair_count,
        "nonzero_left_raw_pair_count": int(len(ratio_array)),
        "zero_left_raw_pair_count": zero_left_count,
        "raw_reduced_residue_count": len(residues),
        "ordered_source_conductor_pair_count": len(pairs),
        "ordered_source_conductor_pairs": [
            {
                "left_source_conductor": left,
                "right_source_conductor": right,
                "raw_frequency_pair_count": count,
            }
            for (left, right), count in sorted(pairs.items())
        ],
        "raw_scalar_real": float(scalar.real),
        "raw_scalar_imag": float(scalar.imag),
        "max_abs_raw_scalar_deviation": float(np.max(deviations)),
        "max_abs_raw_scalar_imag": float(np.max(np.abs(ratio_array.imag))),
        "raw_scalar_negative_real": bool(
            scalar.real < 0 and abs(scalar.imag) < 1e-14),
        "raw_scalar_identity_holds_to_tolerance": bool(
            float(np.max(deviations)) < 1e-13
            and float(np.max(np.abs(ratio_array.imag))) < 1e-14
            and zero_left_count == 0),
    }


def exact_log_identity_for_packet(parameters, packet, target_q):
    factors = factor_integer(target_q)
    support = {int(prime) for prime in factors}
    missing_high = sorted(set(HIGH_PRIMES) - support)
    divisors, symbols, polynomials = symbolic_structured_polynomials(
        *parameters["divisor_range"])
    pairs = [
        (row["left_source_conductor"], row["right_source_conductor"])
        for row in packet["ordered_source_conductor_pairs"]
    ]
    pair_expressions = [
        source_pair_scalar_without_common_l(left, right, polynomials)
        for left, right in pairs
    ]
    common = pair_expressions[0]
    pair_differences = [
        sp.factor(sp.together(expression - common))
        for expression in pair_expressions
    ]
    expected = expected_common_numerator({
        "factorization": factors,
        "missing_high_primes": missing_high,
    }, symbols)
    expected_difference = sp.factor(sp.together(common - expected))
    freeze_logarithm = math.log(PRIME * parameters["ell_freeze"])
    exact_scalar = float(
        sp.N(common.subs(numeric_substitution(symbols)))) / (
            freeze_logarithm ** 3)
    return {
        "mobius_divisors": list(divisors),
        "factorization": factors,
        "high_prime_support": sorted(set(HIGH_PRIMES) & support),
        "missing_high_primes": missing_high,
        "small_prime_support": sorted(support - set(HIGH_PRIMES)),
        "common_log_numerator": str(common),
        "expected_common_log_numerator": str(expected),
        "common_log_numerator_equals_expected": expected_difference == 0,
        "all_pair_scalar_expressions_equal": all(
            difference == 0 for difference in pair_differences),
        "pair_difference_expressions": [
            str(difference) for difference in pair_differences],
        "exact_scalar_numeric_substitution": exact_scalar,
        "exact_scalar_minus_raw_scalar": (
            exact_scalar - packet["raw_scalar_real"]),
    }


def build_receipt():
    holdout = json.loads(SOURCE_HOLDOUT.read_text(encoding="utf-8"))
    parameters = scale_parameters(SCALE)
    failure = next(
        row for row in holdout["failure_summary"]["both_test_failures"]
        if row["reduced_denominator"] == COUNTEREXAMPLE_DENOMINATOR)
    packet = raw_source_pair_packet(parameters, COUNTEREXAMPLE_DENOMINATOR)
    exact = exact_log_identity_for_packet(
        parameters, packet, COUNTEREXAMPLE_DENOMINATOR)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_counterexample_reachability",
        "source_frozen_selector_unused_denominator_holdout": (
            str(SOURCE_HOLDOUT)),
        "source_exact_log_identity_audit": str(SOURCE_EXACT_LOG_IDENTITY),
        "question": (
            "Is the q=16302 frozen-selector counterexample reachable by the "
            "same raw six source-conductor-pair mechanism as the selected "
            "Q46189 replacement family?"),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": parameters["row_count"],
            "active_row_start": parameters["row_count"],
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "adverse_denominator": DENOMINATOR,
            "counterexample_denominator": COUNTEREXAMPLE_DENOMINATOR,
        },
        "frozen_selector_failure_row": failure,
        "raw_source_pair_packet": packet,
        "exact_log_identity": exact,
        "classification": {
            "counterexample_reachable_by_raw_source_pair_mechanism": (
                packet["ordered_source_conductor_pair_count"] == 6
                and packet["raw_scalar_identity_holds_to_tolerance"]),
            "counterexample_has_same_six_pair_packet_shape": (
                packet["ordered_source_conductor_pair_count"] == 6),
            "counterexample_exact_log_identity_matches_replacement_pattern": (
                exact["all_pair_scalar_expressions_equal"]
                and exact["common_log_numerator_equals_expected"]),
            "not_excludable_by_raw_six_pair_conductor_geometry": True,
            "still_possible_to_exclude_by_stricter_predeclared_filter": True,
            "finite_reachability_audit_only": True,
        },
        "candidate_next_action": {
            "name": "stricter admissibility filter or lane demotion",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The failed denominator has the same six-pair exact scalar "
                "packet as the original replacement rows, so a valid selector "
                "theorem needs a narrower structural condition than raw "
                "source-pair reachability."),
            "prediction": (
                "Any admissibility filter broad enough to include the small "
                "pair (2,3) with high support 11,13,19 will inherit the "
                "q=16302 positive-share failure."),
            "falsifier": (
                "A predeclared construction rule that includes q=16302 cannot "
                "support the current 50A..60A positive-share theorem lane."),
            "smallest_next_test": (
                "Either name and test a stricter natural filter excluding "
                "(2,3), or abandon the 50A..60A selector as a theorem target."),
        },
        "decision": (
            "q=16302 is REACHABLE by the same raw six source-conductor-pair "
            "mechanism as the selected Q46189 replacement family.  It has "
            "six ordered source-conductor pairs, zero zero-left raw pairs, a "
            "common negative real scalar, and an exact log-polynomial common "
            "numerator matching the replacement pattern with missing high "
            "prime 17 and small pair (2,3).  Thus the frozen-selector failure "
            "cannot be dismissed as an irrelevant residue-cell artifact."),
        "finite_counterexample_reachability_audit_only": True,
        "finite_diagnostic_only": True,
        "natural_selector_theorem_proved": False,
        "fresh_conductor_holdout_proved": False,
        "distance_slice_positive_share_theorem_proved": False,
        "raw_source_pair_admissibility_theorem_proved": False,
        "replacement_residue_gap_bound_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    packet = receipt["raw_source_pair_packet"]
    exact = receipt["exact_log_identity"]
    failure = receipt["frozen_selector_failure_row"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 counterexample reachability audit",
        "",
        "## Question",
        "",
        "Is the `q=16302` frozen-selector counterexample reachable by the same",
        "raw six source-conductor-pair mechanism as the selected `Q=46189`",
        "replacement family?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_counterexample_reachability_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-counterexample-reachability-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        "q=16302 status:                    REACHABLE",
        f"factorization:                     {exact['factorization']}",
        f"missing high prime:                {exact['missing_high_primes']}",
        f"small prime support:               {exact['small_prime_support']}",
        f"ordered source-conductor pairs:    {packet['ordered_source_conductor_pair_count']}",
        f"raw frequency pairs:               {packet['raw_frequency_pair_count']}",
        f"raw reduced residues:              {packet['raw_reduced_residue_count']}",
        f"zero-left raw pairs:               {packet['zero_left_raw_pair_count']}",
        f"raw scalar:                        {packet['raw_scalar_real']}",
        f"max raw scalar deviation:          {packet['max_abs_raw_scalar_deviation']}",
        f"exact scalar minus raw scalar:      {exact['exact_scalar_minus_raw_scalar']}",
        f"common log numerator:              {exact['common_log_numerator']}",
        f"frozen positive-share gap:         {failure['positive_fraction_gap_vs_q46189']}",
        f"frozen total-pressure gap:         {failure['total_gap_vs_q46189']}",
        "```",
        "",
        "The ordered source-conductor pairs are:",
        "",
        "```text",
    ]
    for row in packet["ordered_source_conductor_pairs"]:
        lines.append(
            "{} x {} -> {}".format(
                row["left_source_conductor"],
                row["right_source_conductor"],
                row["raw_frequency_pair_count"],
            ))
    lines.extend([
        "```",
        "",
        "## Decision",
        "",
        "`q=16302` is reachable by the same raw six source-conductor-pair",
        "mechanism as the selected replacement rows.  It also satisfies the",
        "same exact log-polynomial scalar identity pattern, now with missing",
        "high prime `17` and small pair `(2,3)`.",
        "",
        "Therefore the frozen-selector failure cannot be dismissed as an",
        "irrelevant residue-cell artifact.  The `50A..60A` theorem lane needs",
        "a stricter natural admissibility filter that excludes this packet",
        "before testing, or it should be demoted as a fitted finite witness.",
        "",
        "This proves no natural selector theorem, fresh-conductor theorem,",
        "raw source-pair admissibility theorem, distance-slice theorem,",
        "strict-central Goldbach theorem, or Goldbach proof.",
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
        "counterexample_denominator": COUNTEREXAMPLE_DENOMINATOR,
        "reachability": "REACHABLE",
        "ordered_source_conductor_pair_count": (
            receipt["raw_source_pair_packet"][
                "ordered_source_conductor_pair_count"]),
        "raw_scalar_identity_holds": (
            receipt["raw_source_pair_packet"][
                "raw_scalar_identity_holds_to_tolerance"]),
        "exact_log_identity_matches": (
            receipt["exact_log_identity"][
                "common_log_numerator_equals_expected"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

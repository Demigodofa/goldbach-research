"""Validate a prime-indexed q286 row-level filter-order verifier.

The previous kernel-route audit showed that prime-indexed residue weights match
the direct integer loop.  This receipt integrates those weights into the q286
support/mode action and compares row-level first-two, first-three, complement,
and full ratios against the existing direct filter-order receipt.

Finite verifier-integration audit only: this is not a full later-block scan,
threshold theorem, signed correlation theorem, pointwise character-sum theorem,
or Goldbach proof.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
import time
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
OUT = EVIDENCE / "q286-prime-indexed-row-filter-order-audit.json"
SUFFIX_HOLDOUT = EVIDENCE / "q286-complement-rescue-suffix-holdout.json"
KERNEL_ROUTE = EVIDENCE / "q286-prime-indexed-kernel-route-audit.json"

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_goldbach_transfer import (  # noqa: E402
    _complex_fsum,
    _prime_table,
    _unit_character_table,
    combined_fixed_strict_central_coefficient_receipt,
    q286_first_two_mode_lower_tail_receipt,
)
from tools.build_q286_mod13_4_prospective_descriptor_audit import (  # noqa: E402
    COMPLEMENT_FLOOR,
    TAIL_THRESHOLD,
)
from tools.build_q286_prime_indexed_kernel_route_audit import (  # noqa: E402
    DISCOVERY_TARGETS,
    LATER_FIRST_101_SAMPLE,
    prime_indexed_residue_weights,
    logs,
)


SUPPORT_ORDER = (
    (13,), (11,), (11, 13), (7,), (7, 11), (5,), (5, 13), (5, 7))
FACTOR_PRIMES = (5, 7, 11, 13)
Q286_MODE_COUNT = 6
VALIDATION_TARGET_LIMIT = 40
BENCHMARK_TARGETS = tuple(490480 + 2 * index for index in range(101))
TOLERANCE = 1e-7


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def prepare_support_context(tolerance=TOLERANCE):
    coefficient = combined_fixed_strict_central_coefficient_receipt(
        tolerance=tolerance)
    period = coefficient["arithmetic_period"]
    period_units = tuple(
        residue for residue in range(period)
        if math.gcd(residue, period) == 1)
    aggregate_values = np.asarray(tuple(
        coefficient["aggregate_coefficient_by_unit_residue"][unit]
        for unit in period_units), dtype=np.complex128)
    principal_mean = complex(np.mean(aggregate_values))
    centered = aggregate_values - principal_mean
    _, period_labels, period_character_table = _unit_character_table(
        period, period_units)
    period_character_coefficients = (
        np.conjugate(period_character_table) @ centered / len(period_units))

    support_indices = {}
    for index, label in enumerate(period_labels):
        support = tuple(
            prime for prime, exponent in zip(FACTOR_PRIMES, label)
            if exponent != 0)
        support_indices.setdefault(support, []).append(index)

    support_data = {}
    for support in SUPPORT_ORDER:
        masked = np.zeros_like(period_character_coefficients)
        masked[support_indices[support]] = period_character_coefficients[
            support_indices[support]]
        component = period_character_table.T @ masked
        modulus = 2
        for prime in support:
            modulus *= prime
        grouped = {}
        for unit, value in zip(period_units, component):
            grouped.setdefault(unit % modulus, []).append(value)
        lower_values = {
            residue: _complex_fsum(values) / len(values)
            for residue, values in grouped.items()}
        data = {
            "natural_modulus": modulus,
            "units": tuple(sorted(lower_values)),
            "lower_values": lower_values,
        }
        if support == (11, 13):
            units = data["units"]
            coefficient_values = np.asarray(tuple(
                lower_values[unit] for unit in units), dtype=np.complex128)
            _, labels, character_table = _unit_character_table(
                modulus, units)
            character_coefficients = (
                np.conjugate(character_table) @ coefficient_values
                / len(units))
            matrix = np.zeros((10, 12), dtype=np.complex128)
            for label, value in zip(labels, character_coefficients):
                matrix[label] = value
            q286_matrix = matrix[1:, 1:]
            left, singular_values, right = np.linalg.svd(
                q286_matrix, full_matrices=False)
            q286_mode_matrices = tuple(
                singular_values[index]
                * np.outer(left[:, index], right[index, :])
                for index in range(Q286_MODE_COUNT))
            truncated = (
                (left[:, :Q286_MODE_COUNT]
                 * singular_values[:Q286_MODE_COUNT])
                @ right[:Q286_MODE_COUNT, :])
            data.update({
                "unit_index": {
                    unit: index for index, unit in enumerate(units)},
                "coefficient_values": coefficient_values,
                "character_table": character_table,
                "q286_mode_matrices": q286_mode_matrices,
                "q286_tail_matrix": q286_matrix - truncated,
                "q286_singular_values": singular_values,
            })
        support_data[support] = data
    return {
        "period": period,
        "principal_mean": principal_mean,
        "support_data": support_data,
    }


def residue_cache_for_target(target, primes, prime_values, log_values):
    cache = {}

    def weights_for(modulus):
        if modulus not in cache:
            cache[modulus] = prime_indexed_residue_weights(
                target, primes, prime_values, log_values, modulus)
        return cache[modulus]

    return weights_for


def optimized_reduced_row(
        target, context, primes, prime_values, log_values,
        tolerance=TOLERANCE):
    support_data = context["support_data"]
    principal_mean = context["principal_mean"]
    weights_for = residue_cache_for_target(
        target, primes, prime_values, log_values)
    _, total_weight, _ = weights_for(context["period"])
    principal_contribution = principal_mean * total_weight
    exact_non_q286_support = 0j
    q286_actual = 0j
    q286_local = 0j
    q286_modeled_deviation = 0j
    q286_tail = 0j
    small_support_contribution = 0j
    support_rows = {}
    for support in SUPPORT_ORDER:
        data = support_data[support]
        modulus = data["natural_modulus"]
        _, _, residue_weights = weights_for(modulus)
        lower_values = data["lower_values"]
        actual = _complex_fsum(
            lower_values[residue] * residue_weights[residue]
            for residue in data["units"])
        if support == (11, 13):
            units = data["units"]
            weights = np.asarray(tuple(
                residue_weights[unit] for unit in units), dtype=np.float64)
            admissible_mask = np.asarray(tuple(
                math.gcd((target - unit) % modulus, modulus) == 1
                for unit in units), dtype=bool)
            mean_weight = total_weight / int(np.sum(admissible_mask))
            local = complex(np.sum(
                data["coefficient_values"][admissible_mask])
                * mean_weight)
            weight_delta = np.zeros(len(units), dtype=np.float64)
            weight_delta[admissible_mask] = (
                weights[admissible_mask] - mean_weight)
            imbalance_matrix = (
                data["character_table"] @ weight_delta).reshape(10, 12)[
                    1:, 1:]
            mode_contributions = tuple(
                complex(np.sum(mode_matrix * imbalance_matrix))
                for mode_matrix in data["q286_mode_matrices"])
            modeled_deviation = _complex_fsum(mode_contributions)
            tail = complex(np.sum(
                data["q286_tail_matrix"] * imbalance_matrix))
            q286_actual = actual
            q286_local = local
            q286_modeled_deviation = modeled_deviation
            q286_tail = tail
            q286_deviation = q286_actual - q286_local
            singular_values = data["q286_singular_values"]
            mode_rows = tuple({
                "mode_index": index + 1,
                "singular_value": float(singular_values[index]),
                "contribution": contribution,
                "contribution_to_principal_ratio": float(
                    contribution.real / principal_contribution.real
                    if abs(principal_contribution.real) > tolerance
                    else math.nan),
                "contribution_to_deviation_ratio": float(
                    contribution.real / q286_deviation.real
                    if abs(q286_deviation.real) > tolerance
                    else math.nan),
            } for index, contribution in enumerate(mode_contributions))
            support_rows[support] = {
                "actual_contribution": actual,
                "local_prediction": local,
                "modeled_deviation": modeled_deviation,
                "tail": tail,
                "mode_rows": mode_rows,
            }
        else:
            exact_non_q286_support += actual
            if support not in ((7, 11), (5, 7)):
                small_support_contribution += actual
            support_rows[support] = {"actual_contribution": actual}
    full_action = (
        principal_contribution + exact_non_q286_support + q286_actual)
    reduced_model = (
        principal_contribution + exact_non_q286_support
        + q286_local + q286_modeled_deviation)
    return {
        "ordered_central_prime_pair_weight": total_weight,
        "principal_contribution": principal_contribution,
        "support_rows": support_rows,
        "full_action": full_action,
        "reduced_model": reduced_model,
        "q286_tail": q286_tail,
        "q286_deviation": q286_actual - q286_local,
        "q286_mode_rows": support_rows[(11, 13)]["mode_rows"],
        "full_action_to_principal_ratio": float(
            full_action.real / principal_contribution.real
            if abs(principal_contribution.real) > tolerance else math.nan),
        "reduced_model_to_principal_ratio": float(
            reduced_model.real / principal_contribution.real
            if abs(principal_contribution.real) > tolerance else math.nan),
        "small_support_to_principal_ratio": float(
            small_support_contribution.real / principal_contribution.real
            if abs(principal_contribution.real) > tolerance else math.nan),
    }


def optimized_filter_row(
        target, context, primes, prime_values, log_values,
        tolerance=TOLERANCE):
    row = optimized_reduced_row(
        target, context, primes, prime_values, log_values,
        tolerance=tolerance)
    mode_ratios = tuple(
        mode_row["contribution_to_principal_ratio"]
        for mode_row in row["q286_mode_rows"])
    first_two = mode_ratios[0] + mode_ratios[1]
    first_three = first_two + mode_ratios[2]
    complement = row["full_action_to_principal_ratio"] - first_three
    predicates = {
        "first_two_active": first_two < -0.2,
        "first_three_tail": first_three < -TAIL_THRESHOLD,
        "complement_positive": complement > tolerance,
        "complement_floor": complement > COMPLEMENT_FLOOR,
        "full_positive": row["full_action_to_principal_ratio"] > tolerance,
        "full_nonpositive": row["full_action_to_principal_ratio"] <= tolerance,
    }
    return {
        "target": int(target),
        "first_two_modes_to_principal_ratio": float(first_two),
        "first_three_modes_to_principal_ratio": float(first_three),
        "complement_to_principal_ratio": float(complement),
        "full_action_to_principal_ratio": (
            row["full_action_to_principal_ratio"]),
        "small_support_to_principal_ratio": (
            row["small_support_to_principal_ratio"]),
        "passed_predicates": tuple(
            name for name, passed in predicates.items() if passed),
    }


def compare_to_direct(targets, context, primes, prime_values, log_values):
    direct = q286_first_two_mode_lower_tail_receipt(
        selected_targets=targets,
        tolerance=TOLERANCE,
        include_residue_weights=False)
    rows = []
    maxima = {
        "first_two": 0.0,
        "first_three": 0.0,
        "complement": 0.0,
        "full": 0.0,
    }
    predicate_mismatch_count = 0
    for target in targets:
        opt = optimized_filter_row(
            target, context, primes, prime_values, log_values)
        ref = direct["rows"][target]
        deltas = {
            "first_two": abs(
                opt["first_two_modes_to_principal_ratio"]
                - ref["first_two_modes_to_principal_ratio"]),
            "first_three": abs(
                opt["first_three_modes_to_principal_ratio"]
                - ref["first_three_modes_to_principal_ratio"]),
            "complement": abs(
                opt["complement_to_principal_ratio"]
                - ref["full_without_first_three_to_principal_ratio"]),
            "full": abs(
                opt["full_action_to_principal_ratio"]
                - ref["full_action_to_principal_ratio"]),
        }
        for key, value in deltas.items():
            maxima[key] = max(maxima[key], value)
        direct_predicates = set()
        first_two = ref["first_two_modes_to_principal_ratio"]
        first_three = ref["first_three_modes_to_principal_ratio"]
        complement = ref["full_without_first_three_to_principal_ratio"]
        full = ref["full_action_to_principal_ratio"]
        for name, passed in {
            "first_two_active": first_two < -0.2,
            "first_three_tail": first_three < -TAIL_THRESHOLD,
            "complement_positive": complement > TOLERANCE,
            "complement_floor": complement > COMPLEMENT_FLOOR,
            "full_positive": full > TOLERANCE,
            "full_nonpositive": full <= TOLERANCE,
        }.items():
            if passed:
                direct_predicates.add(name)
        predicate_match = set(opt["passed_predicates"]) == direct_predicates
        if not predicate_match:
            predicate_mismatch_count += 1
        rows.append({
            "target": int(target),
            "deltas": deltas,
            "optimized": opt,
            "direct": {
                "first_two_modes_to_principal_ratio": first_two,
                "first_three_modes_to_principal_ratio": first_three,
                "complement_to_principal_ratio": complement,
                "full_action_to_principal_ratio": full,
                "passed_predicates": tuple(sorted(direct_predicates)),
            },
            "predicate_match": predicate_match,
        })
    return {
        "target_count": len(targets),
        "rows": rows,
        "maximum_ratio_deltas": maxima,
        "predicate_mismatch_count": predicate_mismatch_count,
        "matches_within_tolerance": (
            predicate_mismatch_count == 0
            and max(maxima.values(), default=0.0) <= TOLERANCE),
    }


def benchmark_optimized(targets, context, primes, prime_values, log_values):
    start = time.perf_counter()
    rows = [
        optimized_filter_row(
            target, context, primes, prime_values, log_values)
        for target in targets
    ]
    seconds = time.perf_counter() - start
    first_three_tail = sum(
        1 for row in rows if "first_three_tail" in row["passed_predicates"])
    full_nonpositive = sum(
        1 for row in rows if "full_nonpositive" in row["passed_predicates"])
    return {
        "target_count": len(targets),
        "first_target": targets[0],
        "last_target": targets[-1],
        "optimized_seconds": seconds,
        "targets_per_second": len(targets) / seconds if seconds else math.inf,
        "first_three_tail_count": first_three_tail,
        "full_nonpositive_count": full_nonpositive,
    }


def main():
    suffix = load_json(SUFFIX_HOLDOUT)
    kernel = load_json(KERNEL_ROUTE)
    replay_targets = tuple(
        int(row["target"])
        for row in suffix["prior_tail_offset_replay_holdout"]["target_rows"])
    validation_targets = tuple(dict.fromkeys(
        DISCOVERY_TARGETS
        + LATER_FIRST_101_SAMPLE
        + replay_targets[:18]))[:VALIDATION_TARGET_LIMIT]
    maximum_target = max(validation_targets + BENCHMARK_TARGETS)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    context = prepare_support_context()

    start = time.perf_counter()
    comparison = compare_to_direct(
        validation_targets, context, primes, prime_values, log_values)
    comparison_seconds = time.perf_counter() - start
    benchmark = benchmark_optimized(
        BENCHMARK_TARGETS, context, primes, prime_values, log_values)
    full_later_target_count = 6 * 8 * 5005
    projected_seconds = (
        benchmark["optimized_seconds"]
        * full_later_target_count / benchmark["target_count"])

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "kernel_route": str(KERNEL_ROUTE.relative_to(ROOT)),
            "suffix_sampled_holdout": str(SUFFIX_HOLDOUT.relative_to(ROOT)),
            "direct_receipt":
                "q286_first_two_mode_lower_tail_receipt",
        },
        "status_boundary": (
            "finite row-level verifier integration audit only; validates "
            "sampled row-ratio equivalence but does not run exhaustive later "
            "full blocks, prove a threshold theorem, prove a signed "
            "correlation theorem, or prove Goldbach."),
        "question": (
            "Can prime-indexed residue weights reproduce the existing q286 "
            "row-level first-two, first-three, complement, full, and predicate "
            "outputs?"),
        "mechanism": (
            "Reuse the exact q286 support/mode linear action from the direct "
            "receipt, but feed it residue weights computed by the validated "
            "prime-indexed central-pair kernel."),
        "prediction": (
            "The optimized row verifier should match direct row ratios and "
            "predicate classifications within floating tolerance on validation "
            "targets."),
        "falsifier": (
            "Any validation target with predicate mismatch or ratio delta "
            f"above {TOLERANCE} falsifies the drop-in optimized verifier."),
        "upstream_kernel_validated": (
            kernel["decision_metrics"]["prime_indexed_kernel_validated"]),
        "validation_targets": list(validation_targets),
        "comparison": comparison,
        "benchmark": benchmark,
        "projection": {
            "full_later_block_target_count": full_later_target_count,
            "projected_full_later_block_seconds": projected_seconds,
            "projected_full_later_block_minutes": projected_seconds / 60.0,
            "projection_boundary": (
                "Linear projection from the optimized 101-target benchmark; "
                "not a completed exhaustive verification."),
        },
        "decision_metrics": {
            "optimized_row_verifier_validated": (
                comparison["matches_within_tolerance"]),
            "validation_target_count": comparison["target_count"],
            "predicate_mismatch_count": (
                comparison["predicate_mismatch_count"]),
            "maximum_first_two_delta": (
                comparison["maximum_ratio_deltas"]["first_two"]),
            "maximum_first_three_delta": (
                comparison["maximum_ratio_deltas"]["first_three"]),
            "maximum_complement_delta": (
                comparison["maximum_ratio_deltas"]["complement"]),
            "maximum_full_delta": (
                comparison["maximum_ratio_deltas"]["full"]),
            "comparison_seconds": comparison_seconds,
            "benchmark_optimized_seconds": benchmark["optimized_seconds"],
            "benchmark_targets_per_second": benchmark["targets_per_second"],
            "projected_full_later_block_minutes": projected_seconds / 60.0,
            "ready_for_exhaustive_later_full_block_receipt": (
                comparison["matches_within_tolerance"]),
            "goldbach_proved": False,
        },
        "decision": (
            "If optimized_row_verifier_validated is true, the prime-indexed "
            "path is now row-level equivalent on the validation fixture and "
            "ready for an exhaustive later full-block receipt. That future "
            "receipt remains finite computation, not an asymptotic theorem."),
        "next_obligation": (
            "Run the optimized row verifier over the six later full q286 "
            "blocks and record whether the frozen post-discovery threshold is "
            "falsified, rescued with support, or support-starved at full-block "
            "scale."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

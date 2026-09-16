"""Audit support-packet budgets for the q286 residual character route.

The full-character triangle audit showed that bounding all 2880 period
characters independently is too broad.  This receipt keeps the same exact
character expansion, but aggregates characters by CRT conductor support before
testing source budgets.

Finite theorem-budget audit only.  It proves no packet theorem, character-sum
theorem, signed binary-prime correlation theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
TRIANGLE_SOURCE = (
    EVIDENCE / "q286-residual-character-triangle-budget-audit.json")
OUT = EVIDENCE / "q286-residual-character-support-packet-budget-audit.json"
PERIOD = 10010
TOLERANCE = 1e-10

sys.path.insert(0, str(ROOT))

from lcm_sawtooth_frequency_resolved_fourier import (  # noqa: E402
    _unit_character_table,
)
from lcm_sawtooth_goldbach_transfer import _prime_table  # noqa: E402
from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    SELECTED_TARGETS,
    combined_fixed_strict_central_coefficient_receipt,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
)
from tools.build_q286_lower_face_overlap_audit import (  # noqa: E402
    actual_orbit_measure,
)
from tools.build_q286_orthogonal_residual_norm_certificate import (  # noqa: E402
    residual_operator,
)
from tools.build_q286_prime_indexed_kernel_route_audit import logs  # noqa: E402
from tools.build_q286_residual_character_triangle_budget_audit import (  # noqa: E402
    actual_unit_discrepancy,
    finite_summary,
    residual_unit_values,
    support_label,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def packet_rows(coefficients, labels, channel_discrepancies):
    packets = {}
    for coefficient, label, discrepancy in zip(
            coefficients, labels, channel_discrepancies):
        if abs(coefficient) <= TOLERANCE:
            continue
        key = support_label(label)
        row = packets.setdefault(
            key,
            {
                "support_label": key,
                "character_count": 0,
                "coefficient_l1": 0.0,
                "coefficient_l2_square": 0.0,
                "coefficient_linf": 0.0,
                "character_triangle_bound": 0.0,
                "signed_packet_action": 0.0,
            },
        )
        magnitude = abs(coefficient)
        row["character_count"] += 1
        row["coefficient_l1"] += float(magnitude)
        row["coefficient_l2_square"] += float(magnitude * magnitude)
        row["coefficient_linf"] = max(row["coefficient_linf"], float(magnitude))
        row["character_triangle_bound"] += float(
            magnitude * abs(discrepancy))
        row["signed_packet_action"] += float(
            np.real(coefficient * discrepancy))
    rows = []
    for row in packets.values():
        row["coefficient_l2"] = math.sqrt(row.pop("coefficient_l2_square"))
        row["packet_cancellation_factor"] = (
            abs(row["signed_packet_action"])
            / row["character_triangle_bound"]
            if row["character_triangle_bound"] > TOLERANCE else 0.0)
        rows.append(row)
    rows.sort(key=lambda row: abs(row["signed_packet_action"]), reverse=True)
    return rows


def row_budget(target, operator, units, labels, character_table, primes,
               prime_values, log_values):
    residual_values = residual_unit_values(operator, units)
    coefficients = (
        np.conjugate(character_table) @ residual_values / len(units))
    active = np.abs(coefficients) > TOLERANCE

    discrepancy = actual_unit_discrepancy(
        target, units, primes, prime_values, log_values)
    channel_discrepancies = character_table @ discrepancy
    packets = packet_rows(coefficients, labels, channel_discrepancies)
    signed_packet_sum = math.fsum(
        row["signed_packet_action"] for row in packets)
    packet_abs_sum = math.fsum(
        abs(row["signed_packet_action"]) for row in packets)
    packet_adverse_sum = math.fsum(
        max(0.0, -row["signed_packet_action"]) for row in packets)
    packet_positive_sum = math.fsum(
        max(0.0, row["signed_packet_action"]) for row in packets)
    packet_triangle_sum = math.fsum(
        row["character_triangle_bound"] for row in packets)

    orbit_data = operator["orbit_data"]
    actual = actual_orbit_measure(
        target,
        {
            "orbits": orbit_data["orbits"],
            "first_three": orbit_data["first_three_coefficients"],
            "full": orbit_data["full_coefficients"],
        },
        primes,
        prime_values,
        log_values,
    )
    masses = np.asarray(actual["masses"], dtype=np.float64)
    first_three = float(np.dot(operator["first_three"], masses))
    aligned = operator["uniform_full"] + operator["alpha"] * first_three
    full = float(np.dot(operator["full"], masses))
    reconstruction_error = abs(full - (aligned + signed_packet_sum))
    signed_budget = (
        full / packet_abs_sum
        if full > TOLERANCE and packet_abs_sum > TOLERANCE else 0.0)
    return {
        "target": int(target),
        "target_residue": int(target % PERIOD),
        "target_mod_286": int(target % 286),
        "actual_full_action": full,
        "actual_full_positive": bool(full > TOLERANCE),
        "aligned_only_full_action": aligned,
        "signed_packet_residual_action": signed_packet_sum,
        "packet_reconstruction_error": reconstruction_error,
        "support_packet_count": len(packets),
        "active_character_count": int(np.sum(active)),
        "signed_packet_abs_sum": packet_abs_sum,
        "signed_packet_positive_sum": packet_positive_sum,
        "signed_packet_adverse_sum": packet_adverse_sum,
        "signed_packet_error_budget_with_aligned_exact": signed_budget,
        "rowwise_adverse_packet_margin": aligned - packet_adverse_sum,
        "rowwise_adverse_packet_certifies": bool(
            aligned > packet_adverse_sum + TOLERANCE),
        "packet_triangle_bound": packet_triangle_sum,
        "packet_triangle_to_packet_abs_ratio": (
            packet_triangle_sum / packet_abs_sum
            if packet_abs_sum > TOLERANCE else None),
        "packet_rows": packets,
    }


def add_envelope(rows, selected_rows, field_prefix):
    labels = sorted({
        packet["support_label"]
        for row in selected_rows
        for packet in row["packet_rows"]
    })
    adverse = {}
    for label in labels:
        adverse[label] = max(
            max(
                0.0,
                -next(
                    (
                        packet["signed_packet_action"]
                        for packet in row["packet_rows"]
                        if packet["support_label"] == label
                    ),
                    0.0,
                ),
            )
            for row in selected_rows
        )
    total = math.fsum(adverse.values())
    for row in rows:
        row[f"{field_prefix}_component_adverse_sum"] = total
        row[f"{field_prefix}_component_envelope_margin"] = (
            row["aligned_only_full_action"] - total)
        row[f"{field_prefix}_component_envelope_certifies"] = bool(
            row[f"{field_prefix}_component_envelope_margin"] > TOLERANCE)
    return {
        "packet_adverse_suprema": adverse,
        "component_adverse_sum": total,
        "positive_certified_targets": [
            row["target"] for row in rows
            if row["actual_full_positive"]
            and row[f"{field_prefix}_component_envelope_certifies"]
        ],
        "tightest_positive_margin_row": min(
            (row for row in rows if row["actual_full_positive"]),
            key=lambda row: (
                row[f"{field_prefix}_component_envelope_margin"],
                row["target"],
            ),
        ),
    }


def summarize(rows):
    positive_rows = [row for row in rows if row["actual_full_positive"]]
    tight_signed = min(
        positive_rows,
        key=lambda row: (
            row["signed_packet_error_budget_with_aligned_exact"],
            row["target"],
        ),
    )
    return {
        "selected_target_count": len(rows),
        "actual_full_positive_count": len(positive_rows),
        "actual_full_nonpositive_count": len(rows) - len(positive_rows),
        "support_packet_count_summary": finite_summary(
            row["support_packet_count"] for row in rows),
        "active_character_count_summary": finite_summary(
            row["active_character_count"] for row in rows),
        "signed_packet_error_budget_summary_on_positive_rows":
            finite_summary(
                row["signed_packet_error_budget_with_aligned_exact"]
                for row in positive_rows),
        "rowwise_adverse_packet_certified_positive_count": sum(
            row["rowwise_adverse_packet_certifies"] for row in positive_rows),
        "packet_triangle_to_packet_abs_ratio_summary": finite_summary(
            row["packet_triangle_to_packet_abs_ratio"]
            for row in positive_rows),
        "maximum_packet_reconstruction_error": max(
            row["packet_reconstruction_error"] for row in rows),
        "tightest_positive_signed_packet_budget_row": tight_signed,
    }


def build_receipt():
    triangle = load_json(TRIANGLE_SOURCE)
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    units = tuple(
        residue for residue in range(PERIOD)
        if math.gcd(residue, PERIOD) == 1)
    _, labels, character_table = _unit_character_table(PERIOD, units)
    maximum_target = max(SELECTED_TARGETS)
    primes = np.asarray(_prime_table(maximum_target), dtype=bool)
    prime_values = np.flatnonzero(primes)
    log_values = logs(maximum_target)
    operators = {
        int(target % PERIOD): residual_operator(
            int(target % PERIOD),
            context,
            full_coefficients,
            first_three_coefficients,
        )
        for target in SELECTED_TARGETS
    }
    rows = [
        row_budget(
            int(target), operators[int(target % PERIOD)], units, labels,
            character_table, primes, prime_values, log_values)
        for target in SELECTED_TARGETS
    ]
    positive_rows = [row for row in rows if row["actual_full_positive"]]
    all_envelope = add_envelope(rows, rows, "all_rows")
    positive_envelope = add_envelope(rows, positive_rows, "positive_rows")
    summary = summarize(rows)
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "residual_character_triangle_budget": str(
                TRIANGLE_SOURCE.relative_to(ROOT)),
            "residual_character_triangle_source_commit": (
                triangle["source_commit"]),
        },
        "status": (
            "HOLD_adverse_packet_route_fails_signed_packet_route_survives_budget"),
        "status_boundary": (
            "finite support-packet theorem-budget audit only; no support-"
            "packet theorem, character-sum theorem, signed binary-prime "
            "correlation theorem, q286 threshold theorem, strict-central "
            "Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "support_packet_theorem_proved": False,
        "character_sum_theorem_proved": False,
        "signed_binary_prime_correlation_theorem_proved": False,
        "universal_bound_open": True,
        "candidate": {
            "name": "residual character support-packet signed landing",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Aggregate the exact U_10010 character expansion of h_a by "
                "CRT conductor support.  This preserves cancellation inside "
                "each support packet and asks for a signed packet estimate "
                "instead of independent bounds for every character."),
            "prediction": (
                "If the smaller dictionary is meaningful, the signed packet "
                "budget on the tight row should be materially looser than "
                "raw residual sign landing, while one-sided adverse-packet "
                "envelopes should expose whether the route still needs signed "
                "structure."),
            "falsifier": (
                "If the packet signed budget remains sub-percent or packet "
                "aggregation gives no compression over the full-character "
                "triangle route, then this dictionary does not earn its keep."),
            "smallest_test": (
                "Compute exact signed contributions for the 15 nonprincipal "
                "conductor-support packets on the seven frozen signed-pair "
                "operator targets, and compare signed budgets, rowwise "
                "adverse budgets, and disconnected adverse envelopes."),
        },
        "packet_convention": {
            "period": PERIOD,
            "dictionary": (
                "characters grouped by nonempty support among the prime "
                "factors 5,7,11,13 of the U_10010 character labels"),
            "signed_packet_budget": (
                "With aligned exact and packet actions A_g estimated with "
                "relative signed error eps, full>0 follows when "
                "eps < full_actual / sum_g |A_g|."),
            "rowwise_adverse_packet_test": (
                "aligned(N) - sum_g max(0,-A_g(N)) > 0"),
            "component_envelope_test": (
                "replace each max(0,-A_g(N)) by the worst observed adverse "
                "value for that packet on the selected finite rows"),
        },
        "summary": summary,
        "all_rows_component_envelope": all_envelope,
        "positive_rows_component_envelope": positive_envelope,
        "decision": (
            "The support-packet dictionary earns a narrow next test: it "
            "reduces the tight positive row from a 2880-character triangle "
            "budget to a 15-packet signed landing budget about 0.05545.  "
            "That is materially looser than the prior sub-percent residual "
            "sign-split budget.  However, the same data also falsify the "
            "one-sided adverse-packet route: target 94856 is positive only "
            "because favorable packets offset adverse packets, and both the "
            "rowwise adverse-packet test and disconnected component envelopes "
            "fail there.  The next proof object is therefore a signed support-"
            "packet binary-prime correlation estimate, not an adverse-only "
            "packet supremum bound and not a full-character triangle bound.  "
            "Goldbach remains open."),
        "target_rows": rows,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

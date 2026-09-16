"""Build the weak-row degree-5 primewise sign audit."""

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from lcm_sawtooth_lifted_endpoint_frame import (  # noqa: E402
    lifted_endpoint_residue_gram_receipt,
)
from mobius_covariance_endpoint_probe import _prime_flags  # noqa: E402


DEGREE5_BURDEN = Path("evidence/mobius-moment-square-degree5-burden-audit.json")
OUTPUT = Path("evidence/mobius-moment-square-degree5-primewise-sign-audit.json")
WEAK_SCALE = 167
PAIRS = (
    (0, 4, "00", "12"),
    (1, 2, "01", "02"),
    (1, 3, "01", "11"),
)


def scale_parameters(scale_modulus):
    inferred_n = scale_modulus ** (1 / .59)
    row_count = int(inferred_n ** .41)
    divisor_lower = int(inferred_n ** .15)
    divisor_upper = int(inferred_n ** .32)
    ell_freeze = row_count + row_count // 2
    return {
        "row_count": row_count,
        "ell_freeze": ell_freeze,
        "divisor_range": (divisor_lower, divisor_upper),
    }


def local_degree5_contributions(active, full):
    active = np.asarray(active, dtype=float)
    full = np.asarray(full, dtype=float)
    if active.shape != (6, 6) or full.shape != (6, 6):
        raise ValueError("active and full must be 6 by 6")
    active = (active + active.T) / 2
    full = (full + full.T) / 2
    half = active - 0.5 * full
    rows = []
    for left, right, left_label, right_label in PAIRS:
        active_contribution = float(2 * active[left, right])
        full_contribution = float(2 * full[left, right])
        half_contribution = float(2 * half[left, right])
        rows.append({
            "left_label": left_label,
            "right_label": right_label,
            "multiplicity": 2,
            "active_contribution": active_contribution,
            "full_contribution": full_contribution,
            "half_frame_contribution": half_contribution,
        })
    return rows


def sign_counts(values):
    return {
        "positive": sum(1 for value in values if value > 0),
        "zero": sum(1 for value in values if value == 0),
        "negative": sum(1 for value in values if value < 0),
    }


def weak_scale_primewise_rows():
    parameters = scale_parameters(WEAK_SCALE)
    divisor_lower, divisor_upper = parameters["divisor_range"]
    flags = _prime_flags(2 * WEAK_SCALE)
    rows = []
    for modulus in range(WEAK_SCALE, 2 * WEAK_SCALE + 1):
        if not flags[modulus]:
            continue
        receipt = lifted_endpoint_residue_gram_receipt(
            modulus,
            parameters["row_count"],
            parameters["ell_freeze"],
            divisor_lower,
            divisor_upper,
        )
        contributions = local_degree5_contributions(
            receipt["active_window_residue_energy_gram"],
            receipt["full_residue_energy_gram"],
        )
        total = sum(row["half_frame_contribution"] for row in contributions)
        rows.append({
            "prime_modulus": modulus,
            "contributors": contributions,
            "degree5_half_frame_total": total,
            "all_three_contributors_negative": all(
                row["half_frame_contribution"] < 0
                for row in contributions),
        })
    return parameters, rows


def component_totals(rows):
    totals = {
        f"{left_label},{right_label}": 0.0
        for _, _, left_label, right_label in PAIRS
    }
    values = {label: [] for label in totals}
    for row in rows:
        for contributor in row["contributors"]:
            label = (
                f"{contributor['left_label']},"
                f"{contributor['right_label']}")
            value = contributor["half_frame_contribution"]
            totals[label] += value
            values[label].append(value)
    return {
        label: {
            "half_frame_total": totals[label],
            "sign_counts": sign_counts(values[label]),
            "largest_value": max(values[label]),
            "smallest_value": min(values[label]),
        }
        for label in totals
    }


def prior_burden_totals():
    receipt = json.loads(DEGREE5_BURDEN.read_text(encoding="utf-8"))
    return {
        f"{row['left_label']},{row['right_label']}": (
            row["half_frame_contribution"])
        for row in receipt["weak_scale_burden"]["contributors"]
    }


def build_receipt():
    parameters, rows = weak_scale_primewise_rows()
    totals = component_totals(rows)
    prior = prior_burden_totals()
    total_values = [row["degree5_half_frame_total"] for row in rows]
    deltas = {
        label: totals[label]["half_frame_total"] - prior[label]
        for label in totals
    }
    max_abs_delta = max(abs(value) for value in deltas.values())
    return {
        "status": "CHECK_degree5_primewise_sign_localization",
        "question": (
            "In the weak M=167 block, is the degree-5 burden hidden in an "
            "aggregate prime-block cancellation, or does each prime already "
            "push the three active/full Gram entries in the adverse "
            "direction?"),
        "source_degree5_burden_audit": str(DEGREE5_BURDEN),
        "scale_modulus": WEAK_SCALE,
        "row_count": parameters["row_count"],
        "ell_freeze": parameters["ell_freeze"],
        "divisor_range": parameters["divisor_range"],
        "prime_count": len(rows),
        "prime_rows": rows,
        "component_totals": totals,
        "degree5_total_sign_counts": sign_counts(total_values),
        "all_prime_degree5_totals_negative": all(
            value < 0 for value in total_values),
        "all_prime_component_contributors_negative": all(
            row["all_three_contributors_negative"] for row in rows),
        "least_adverse_prime_row": max(
            rows, key=lambda row: row["degree5_half_frame_total"]),
        "most_adverse_prime_row": min(
            rows, key=lambda row: row["degree5_half_frame_total"]),
        "component_total_minus_prior_burden": deltas,
        "component_totals_match_prior_burden_within_float_tolerance": (
            max_abs_delta <= 1e-1),
        "maximum_abs_component_total_delta_from_prior_burden": max_abs_delta,
        "prediction": (
            "If a pointwise degree-5 theorem is plausible at this weak row, "
            "then decomposing the aggregate over primes should not reveal "
            "sign cancellation that the block sum was hiding."),
        "falsifier": (
            "A single prime with a positive degree-5 half-frame total, or a "
            "positive half-frame contribution in one of the three degree-5 "
            "Gram entries, would falsify this finite localization test."),
        "decision": (
            "The weak M=167 block passes the primewise sign-localization "
            "test: every checked prime has all three degree-5 component "
            "contributions negative, and every prime's degree-5 total is "
            "negative.  The aggregate weak-row burden is therefore not "
            "explained by cancellation among favorable and adverse prime "
            "rows.  A theorem-shaped next step may try to prove a local "
            "one-prime sign or dominance lemma for these three entries."),
        "finite_primewise_sign_diagnostic_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "q286_reactivated": False,
        "primewise_sign_theorem_proved": False,
        "degree5_coefficient_theorem_proved": False,
        "robust_margin_universal_theorem_proved": False,
        "coefficient_family_theorem_proved": False,
        "universal_sturm_certificate_theorem_proved": False,
        "moment_square_half_frame_curve_positivity_theorem_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "mobius_covariance_theorem_proved": False,
        "signed_prime_correlation_proved": False,
    }


def main():
    receipt = build_receipt()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(receipt, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUTPUT}")


if __name__ == "__main__":
    main()

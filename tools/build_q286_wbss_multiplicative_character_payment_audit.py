"""Character-moment payment budget for the q286-WBSS adverse-drag target.

The residual schedule showed that coefficient-energy truncation is not enough.
This receipt asks the next theorem-facing question: if we keep the full active
multiplicative-character package, how strong must a universal pointwise
character-moment estimate be to pay the local main?

This is exact finite coefficient algebra.  It does not prove the needed
character-moment estimate, a pointwise adverse-drag theorem, or Goldbach.
"""

from __future__ import annotations

import itertools
import json
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
MULTIPLICATIVE_SOURCE = (
    EVIDENCE / "q286-wbss-multiplicative-character-burden-audit.json")
RESIDUAL_SOURCE = (
    EVIDENCE / "q286-wbss-multiplicative-residual-schedule-audit.json")
COEFFICIENT_HOLD = (
    EVIDENCE / "q286-wbss-coefficient-discrepancy-budget-hold.json")
OUT = EVIDENCE / "q286-wbss-multiplicative-character-payment-audit.json"
TOLERANCE = 1e-20

sys.path.insert(0, str(ROOT))

from tools.build_q286_wbss_multiplicative_character_burden_audit import (  # noqa: E402
    FORMULA_SOURCE,
    MODULUS_FACTORS,
    coefficient_grid,
    coefficient_rows_by_modulus,
    exponent_map,
    load_json,
)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def active_character_rows():
    formula = load_json(FORMULA_SOURCE)
    coefficients = coefficient_rows_by_modulus(formula)
    maps = {
        factor: exponent_map(factor)
        for factors in MODULUS_FACTORS.values()
        for factor in factors
    }
    rows_by_modulus = {}
    for modulus, factors in MODULUS_FACTORS.items():
        grid = coefficient_grid(modulus, factors, coefficients[modulus], maps)
        centered = grid - np.mean(grid)
        transform = np.fft.fftn(centered) / centered.size
        shape = transform.shape
        rows = []
        for frequency in itertools.product(*(range(size) for size in shape)):
            if all(item == 0 for item in frequency):
                continue
            value = complex(transform[frequency])
            abs_coefficient = abs(value)
            energy = abs_coefficient * abs_coefficient
            if energy <= TOLERANCE:
                continue
            conjugate_frequency = [
                (-item) % size
                for item, size in zip(frequency, shape)
            ]
            rows.append({
                "frequency": list(frequency),
                "conjugate_frequency": conjugate_frequency,
                "self_conjugate": list(frequency) == conjugate_frequency,
                "coefficient_real": value.real,
                "coefficient_imag": value.imag,
                "abs_coefficient": abs_coefficient,
                "energy": energy,
                "zero_axis": any(item == 0 for item in frequency),
            })
        rows.sort(key=lambda row: row["abs_coefficient"], reverse=True)
        rows_by_modulus[str(modulus)] = {
            "modulus": modulus,
            "unit_count": int(grid.size),
            "active_character_count": len(rows),
            "character_l1": sum(row["abs_coefficient"] for row in rows),
            "character_l2": sum(row["energy"] for row in rows) ** 0.5,
            "real_channel_count": real_channel_count(rows, shape),
            "self_conjugate_count": sum(1 for row in rows
                                        if row["self_conjugate"]),
            "top_abs_characters": rows[:10],
        }
    return rows_by_modulus


def real_channel_count(rows, shape):
    active = {tuple(row["frequency"]) for row in rows}
    seen = set()
    count = 0
    for frequency in sorted(active):
        if frequency in seen:
            continue
        conjugate = tuple((-item) % size
                          for item, size in zip(frequency, shape))
        seen.add(frequency)
        seen.add(conjugate)
        count += 1
    return count


def build_receipt():
    multiplicative = load_json(MULTIPLICATIVE_SOURCE)
    residual = load_json(RESIDUAL_SOURCE)
    coefficient_hold = load_json(COEFFICIENT_HOLD)
    rows_by_modulus = active_character_rows()
    minimum_local_main = coefficient_hold["coefficient_budget"][
        "minimum_local_main_over_even_residues"]
    residue_l1 = coefficient_hold["coefficient_budget"]["total_l1_norm"]
    residue_equal_cap = coefficient_hold["coefficient_budget"][
        "global_equal_residue_error_cap"]
    total_character_l1 = sum(
        row["character_l1"] for row in rows_by_modulus.values())
    equal_character_moment_cap = minimum_local_main / total_character_l1
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "multiplicative_character_burden_audit": str(
                MULTIPLICATIVE_SOURCE.relative_to(ROOT)),
            "multiplicative_character_burden_status": multiplicative[
                "status"],
            "multiplicative_residual_schedule_audit": str(
                RESIDUAL_SOURCE.relative_to(ROOT)),
            "multiplicative_residual_schedule_status": residual["status"],
            "coefficient_discrepancy_budget_hold": str(
                COEFFICIENT_HOLD.relative_to(ROOT)),
            "coefficient_discrepancy_hold_status": coefficient_hold["status"],
        },
        "status": "HOLD_character_moment_payment_bound_required",
        "status_boundary": (
            "finite character-coordinate coefficient payment audit only; it "
            "proves no character-moment estimate, residual character theorem, "
            "pointwise adverse-drag theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"),
        "goldbach_proved": False,
        "character_moment_bound_proved": False,
        "residual_character_bound_proved": False,
        "pointwise_adverse_drag_theorem_proved": False,
        "fixed_modulus_binary_prime_discrepancy_theorem_proved": False,
        "universal_bound_open": True,
        "acceptance_condition": {
            "finite_evidence_is_acceptance_condition": False,
            "required_acceptance_condition": (
                "a universal pointwise unnormalized analytic estimate"),
            "sufficient_character_moment_statement": (
                "For every sufficiently large eligible even N, prove active "
                "multiplicative-character moment bounds strong enough that "
                "sum_{d,chi} |c_hat_{d,chi}| * theta_{d,chi}(N) < "
                "LocalMain(N)."),
            "target": "AdverseDrag(N) < LocalMain(N)",
        },
        "method": {
            "character_moment_normalization": (
                "With c_d(s)=sum_chi c_hat_{d,chi} chi(s), write the "
                "projected error as E_d(N)=sum_chi c_hat_{d,chi} "
                "D_{d,chi}(N), where D_{d,chi}(N)=sum_s chi(s) "
                "Delta_{d,s}(N) in the same unnormalized residue-mass scale."),
            "sufficient_uniform_cap": (
                "If every active |D_{d,chi}(N)| is at most theta(N), then "
                "adverse_drag(N) <= total_character_l1 * theta(N)."),
            "interpretation_boundary": (
                "The cap is a payment target for an analytic theorem.  It is "
                "not inferred from the finite checked rows."),
        },
        "minimum_local_main": minimum_local_main,
        "residue_budget": {
            "total_residue_l1": residue_l1,
            "equal_residue_error_cap": residue_equal_cap,
        },
        "character_budget": {
            "active_character_count": sum(
                row["active_character_count"]
                for row in rows_by_modulus.values()),
            "active_real_channel_count": sum(
                row["real_channel_count"]
                for row in rows_by_modulus.values()),
            "self_conjugate_channel_count": sum(
                row["self_conjugate_count"]
                for row in rows_by_modulus.values()),
            "total_character_l1": total_character_l1,
            "equal_character_moment_cap": equal_character_moment_cap,
            "cap_relaxation_factor_vs_residue_cap": (
                equal_character_moment_cap / residue_equal_cap),
            "per_modulus": {
                modulus: {
                    "active_character_count": row[
                        "active_character_count"],
                    "real_channel_count": row["real_channel_count"],
                    "self_conjugate_count": row["self_conjugate_count"],
                    "character_l1": row["character_l1"],
                    "character_l2": row["character_l2"],
                    "equal_cap_if_this_modulus_paid_alone": (
                        minimum_local_main / row["character_l1"]),
                    "top_abs_characters": row["top_abs_characters"],
                }
                for modulus, row in rows_by_modulus.items()
            },
        },
        "candidate": {
            "name": "full active multiplicative-character payment theorem",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use the full active nonzero multiplicative-character "
                "package so coefficient residual is zero, then prove "
                "pointwise bounds for the resulting fixed finite set of "
                "twisted binary-prime character moments."),
            "prediction": (
                "Character coordinates should give a looser analytic cap than "
                "per-residue L1 control, but still require a genuine "
                "pointwise theorem."),
            "falsifier": (
                "If the character L1 payment is no better than residue L1, "
                "or if no source-backed pointwise character-moment theorem "
                "can pay the displayed cap, this route remains a HOLD."),
            "smallest_test": (
                "Compute the full active character L1 payment cap and compare "
                "it to the existing per-residue discrepancy cap."),
        },
        "decision": (
            "The full active multiplicative-character package improves the "
            "payment geometry but does not prove the theorem.  The active "
            "package has 122 nonzero character coefficients, collapsing to "
            "64 real conjugacy channels, with total character L1 about "
            "49.154.  A uniform active character-moment cap below about "
            "0.0122866 would pay the minimum local main, about 7.59 times "
            "looser than the per-residue cap 0.0016193.  This may be a "
            "better analytic target, but it is still a universal pointwise "
            "fixed-modulus twisted binary-prime correlation theorem, not "
            "finite evidence or a Goldbach proof."),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

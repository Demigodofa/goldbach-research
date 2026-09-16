"""Decompose Q46189 coordinate-00 margins by Dirichlet-kernel residue gaps.

The one-coordinate ledger reduced the selected Q=46189 lane to signs of
active/full ratios for coordinate 00.  This receipt expands the coordinate-00
half-margin into the exact finite Dirichlet-kernel autocorrelation identity for
Q=46189 and the weakest positive replacement row.
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
from tools.build_mobius_moment_square_degree5_q46189_exception_bound_audit import (  # noqa: E402
    DENOMINATOR,
    PRIME,
    SCALE,
    TARGET_LABEL,
)
from tools.build_mobius_moment_square_degree5_weak_scale_phase_curve_sweep import (  # noqa: E402
    _residue_cells_by_denominator,
)


OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-coordinate00-kernel-decomposition-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-coordinate00-kernel-decomposition-audit.md")
SOURCE_LEDGER = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-one-coordinate-ratio-ledger-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def ledger_rows(receipt):
    rows = [
        receipt["q46189_one_coordinate_row"],
        *receipt["replacement_one_coordinate_rows"],
    ]
    return {row["reduced_denominator"]: row for row in rows}


def weakest_replacement(receipt):
    return min(
        receipt["replacement_one_coordinate_rows"],
        key=lambda row: row["ratio_minus_half"])


def component_vector(reduced_denominator, cells):
    vector = np.zeros(reduced_denominator, dtype=complex)
    for residue, values in cells:
        vector[residue] = values[0]
    return vector


def active_transforms_direct(reduced_denominator, cells, row_count,
                             active_row_start):
    residues = np.asarray([cell[0] for cell in cells], dtype=np.int64)
    values = np.asarray([cell[1][0] for cell in cells], dtype=complex)
    rows = np.arange(
        active_row_start, active_row_start + row_count, dtype=np.int64)
    transforms = np.zeros(row_count, dtype=complex)
    for index, row in enumerate(rows):
        transforms[index] = np.sum(
            values
            * np.exp(
                2j * np.pi
                * ((row * residues) % reduced_denominator)
                / reduced_denominator))
    return transforms


def paired_gap_contributions(contributions):
    q = len(contributions)
    paired = []
    used = {0}
    for delta in range(1, q):
        if delta in used:
            continue
        mate = (-delta) % q
        if mate == delta:
            value = contributions[delta]
            deltas = [delta]
        else:
            value = contributions[delta] + contributions[mate]
            deltas = [delta, mate]
            used.add(mate)
        used.add(delta)
        paired.append({
            "circular_distance": min(delta, q - delta),
            "deltas": deltas,
            "component_active_contribution": float(value),
        })
    return paired


def distance_buckets(row_count, contributions):
    q = len(contributions)
    deltas = np.arange(q, dtype=np.int64)
    distance = np.minimum(deltas, q - deltas)
    specs = [
        ("near_1_to_A", 1, row_count),
        ("middle_A_to_10A", row_count + 1, 10 * row_count),
        ("far_10A_to_100A", 10 * row_count + 1, 100 * row_count),
        ("tail_over_100A", 100 * row_count + 1, q // 2),
    ]
    rows = []
    for name, lower, upper in specs:
        mask = (distance >= lower) & (distance <= upper)
        selected = contributions[mask]
        rows.append({
            "bucket": name,
            "distance_range": [lower, upper],
            "delta_count": int(np.count_nonzero(mask)),
            "component_active_contribution": float(np.sum(selected)),
            "positive_contribution_sum": float(np.sum(
                selected[selected > 0])),
            "negative_contribution_sum": float(np.sum(
                selected[selected < 0])),
        })
    return rows


def decompose_row(reduced_denominator, cells, row_count, active_row_start,
                  ledger_row, role):
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
    # Factor 2 because the saved component is the symmetric 00,12 pair.
    active_contributions = (
        2 * reduced_denominator * autocorrelation * kernel).real
    component_full_energy = float(active_contributions[0])
    component_active_energy = float(np.sum(active_contributions))
    component_half_margin = (
        component_active_energy - 0.5 * component_full_energy)
    off_diagonal_total = float(np.sum(active_contributions[1:]))
    diagonal_half_contribution = 0.5 * component_full_energy

    direct_transforms = active_transforms_direct(
        reduced_denominator, cells, row_count, active_row_start)
    direct_active = float(
        2 * reduced_denominator / row_count
        * np.vdot(direct_transforms, direct_transforms).real)

    paired = paired_gap_contributions(active_contributions)
    top_negative = sorted(
        paired, key=lambda row: row["component_active_contribution"])[:8]
    top_positive = sorted(
        paired, key=lambda row: row["component_active_contribution"],
        reverse=True)[:8]
    scalar_margin = (
        ledger_row["positive_scalar_magnitude"] * component_half_margin)

    return {
        "role": role,
        "reduced_denominator": reduced_denominator,
        "factorization": ledger_row["factorization"],
        "residue_cell_count": len(cells),
        "active_row_start": active_row_start,
        "active_row_stop": active_row_start + row_count - 1,
        "component_full_energy": component_full_energy,
        "component_active_energy": component_active_energy,
        "component_active_energy_direct": direct_active,
        "active_reconstruction_abs_error": abs(
            component_active_energy - direct_active),
        "coordinate_00_active_over_full_ratio": (
            component_active_energy / component_full_energy),
        "ratio_minus_half": (
            component_active_energy / component_full_energy - 0.5),
        "component_half_margin_active_minus_half_full": (
            component_half_margin),
        "ledger_coordinate_00_full_energy": (
            ledger_row["coordinate_00_full_energy"]),
        "ledger_coordinate_00_active_energy": (
            ledger_row["coordinate_00_active_energy"]),
        "ledger_scalar_cancelled_margin": (
            ledger_row[
                "scalar_cancelled_margin_full_over_2_minus_active"]),
        "scalar_cancelled_margin_from_kernel": scalar_margin,
        "scalar_cancelled_margin_abs_error": abs(
            scalar_margin
            - ledger_row[
                "scalar_cancelled_margin_full_over_2_minus_active"]),
        "diagonal_half_contribution": diagonal_half_contribution,
        "off_diagonal_total_contribution": off_diagonal_total,
        "off_diagonal_over_diagonal_half": (
            off_diagonal_total / diagonal_half_contribution),
        "distance_bucket_contributions": distance_buckets(
            row_count, active_contributions),
        "top_negative_gap_pairs": top_negative,
        "top_positive_gap_pairs": top_positive,
        "finite_dirichlet_kernel_identity_verified": (
            abs(component_active_energy - direct_active) < 1.0
            and abs(component_full_energy
                    - ledger_row["coordinate_00_full_energy"]) < 1.0
            and abs(component_active_energy
                    - ledger_row["coordinate_00_active_energy"]) < 1.0),
    }


def build_receipt():
    ledger = json.loads(SOURCE_LEDGER.read_text(encoding="utf-8"))
    parameters = scale_parameters(SCALE)
    row_count = parameters["row_count"]
    active_row_start = row_count
    _, cells_by_denominator = _residue_cells_by_denominator(
        PRIME,
        row_count,
        parameters["ell_freeze"],
        *parameters["divisor_range"],
    )
    by_q = ledger_rows(ledger)
    weakest = weakest_replacement(ledger)
    selected = [
        (DENOMINATOR, "q46189_adverse"),
        (weakest["reduced_denominator"], "weakest_positive_replacement"),
    ]
    rows = [
        decompose_row(
            denominator,
            cells_by_denominator[denominator],
            row_count,
            active_row_start,
            by_q[denominator],
            role)
        for denominator, role in selected
    ]
    q_row = rows[0]
    weakest_row = rows[1]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_coordinate00_kernel_decomposition",
        "source_one_coordinate_ledger": str(SOURCE_LEDGER),
        "question": (
            "Can the coordinate-00 half-margin for Q=46189 and the weakest "
            "replacement row be decomposed into finite Dirichlet-kernel "
            "autocorrelation terms that identify the sign-deciding residue "
            "gap structure?"),
        "answer": (
            "Yes as a finite decomposition.  The component active energy "
            "matches the direct active-window transform, and the half-margin "
            "splits into a positive diagonal half plus off-diagonal "
            "Dirichlet-kernel residue-gap terms.  Q=46189 is negative because "
            "its off-diagonal total slightly overcomes the diagonal half; "
            "the weakest replacement remains positive because the same split "
            "does not erase the diagonal half."),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": row_count,
            "active_row_start": active_row_start,
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "adverse_denominator": DENOMINATOR,
            "weakest_replacement_denominator": weakest[
                "reduced_denominator"],
            "kernel_identity": (
                "active_00 = 2*q*sum_delta C_delta*K_delta, "
                "full_00 = 2*q*C_0, "
                "half_margin = full_00/2 + "
                "2*q*sum_{delta!=0} C_delta*K_delta"),
        },
        "decomposition_rows": rows,
        "classification": {
            "q46189_kernel_identity_verified": (
                q_row["finite_dirichlet_kernel_identity_verified"]),
            "weakest_replacement_kernel_identity_verified": (
                weakest_row[
                    "finite_dirichlet_kernel_identity_verified"]),
            "q46189_negative_sign_from_off_diagonal_overpayment": (
                q_row["component_half_margin_active_minus_half_full"] < 0
                and q_row["off_diagonal_total_contribution"]
                < -q_row["diagonal_half_contribution"]),
            "weakest_replacement_positive_after_off_diagonal": (
                weakest_row[
                    "component_half_margin_active_minus_half_full"] > 0
                and weakest_row["off_diagonal_total_contribution"]
                > -weakest_row["diagonal_half_contribution"]),
            "finite_kernel_decomposition_only": True,
        },
        "candidate_next_action": {
            "name": "coordinate-00 residue-gap sign theorem candidate",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Turn the finite residue-gap decomposition into structural "
                "bounds: control the off-diagonal Dirichlet-kernel total "
                "relative to the diagonal half for the replacement family, "
                "while allowing rare Q-style overpayment defects."),
            "prediction": (
                "For replacement rows, grouped residue-gap buckets should "
                "retain enough diagonal half after adverse off-diagonal "
                "terms; for Q-style adverse rows, a small set of circular gap "
                "pairs should account for the sign reversal."),
            "falsifier": (
                "If future source-admissible replacements have off-diagonal "
                "totals below negative diagonal half, or if Q-style defects "
                "are not localized in residue-gap pairs, this theorem target "
                "does not generalize."),
            "smallest_next_test": (
                "Run the same kernel-gap decomposition across all ten "
                "replacement rows and test whether the weakest-row gap "
                "structure is the worst case by bucket and top-pair metrics."),
        },
        "decision": (
            "The one-coordinate obstruction has a concrete finite kernel "
            "shape: diagonal half-energy competes with off-diagonal "
            "Dirichlet-kernel residue-gap mass.  The next theorem-shaped "
            "object is a residue-gap sign bound, not another phase-scalar "
            "identity.  No universal coordinate-00 ratio theorem or Goldbach "
            "proof is established."),
        "finite_coordinate00_kernel_decomposition_audit_only": True,
        "finite_diagnostic_only": True,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "symbolic_coordinate_00_energy_ratio_theorem_proved": False,
        "one_coordinate_active_full_ratio_theorem_proved": False,
        "replacement_family_payment_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    q_row, weakest = receipt["decomposition_rows"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 coordinate-00 kernel decomposition audit",
        "",
        "## Question",
        "",
        "Can the coordinate-00 half-margin for `Q=46189` and the weakest",
        "replacement row be decomposed into finite Dirichlet-kernel",
        "autocorrelation terms that identify the sign-deciding residue-gap",
        "structure?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_coordinate00_kernel_decomposition_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-coordinate00-kernel-decomposition-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"Q=46189 half-margin:          {q_row['component_half_margin_active_minus_half_full']}",
        f"Q=46189 diagonal half:        {q_row['diagonal_half_contribution']}",
        f"Q=46189 off-diagonal total:   {q_row['off_diagonal_total_contribution']}",
        f"weakest replacement q:        {weakest['reduced_denominator']}",
        f"weakest replacement margin:   {weakest['component_half_margin_active_minus_half_full']}",
        f"weakest replacement diagonal: {weakest['diagonal_half_contribution']}",
        f"weakest replacement offdiag:  {weakest['off_diagonal_total_contribution']}",
        "```",
        "",
        "## Decision",
        "",
        "The one-coordinate obstruction has a concrete finite kernel shape:",
        "diagonal half-energy competes with off-diagonal Dirichlet-kernel",
        "residue-gap mass.  `Q=46189` is negative because the off-diagonal",
        "total slightly overcomes the diagonal half; the weakest replacement",
        "remains positive because the off-diagonal total does not erase the",
        "diagonal half.",
        "",
        "This is finite diagnostic evidence only.  It proves no coordinate-00",
        "residue-gap sign theorem, symbolic coordinate-00 energy ratio theorem,",
        "one-coordinate active/full ratio theorem, replacement-family payment",
        "theorem, strict-central Goldbach theorem, or Goldbach proof.",
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
    q_row, weakest = receipt["decomposition_rows"]
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "q46189_half_margin": q_row[
            "component_half_margin_active_minus_half_full"],
        "weakest_replacement_denominator": weakest["reduced_denominator"],
        "weakest_replacement_half_margin": weakest[
            "component_half_margin_active_minus_half_full"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

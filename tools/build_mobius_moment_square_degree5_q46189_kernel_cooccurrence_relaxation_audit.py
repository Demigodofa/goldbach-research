"""Audit co-occurrence relaxations for the Q46189 kernel boundary.

The disconnected bucket envelope is too loose.  This receipt asks whether
observed pairwise or three-way bucket co-occurrence constraints are already
strong enough to imply the nonadverse bound

    off_diagonal_total / diagonal_half > -1.

They are tested as linear relaxations over the four normalized distance-bucket
contributions.  Passing such a relaxation would point to a theorem target based
on low-order co-occurrence.  Failure means the route needs full packet geometry
or a sharper invariant.
"""

from __future__ import annotations

import itertools
import json
import subprocess
import sys
from pathlib import Path

from scipy.optimize import linprog


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


SOURCE = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-packet-kernel-sign-landscape-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-kernel-cooccurrence-relaxation-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-kernel-cooccurrence-relaxation-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def bucket_names(row):
    return [
        bucket["bucket"]
        for bucket in row["distance_bucket_contributions"]
    ]


def bucket_vector(row, names):
    return [
        next(
            bucket for bucket in row["distance_bucket_contributions"]
            if bucket["bucket"] == name
        )["contribution_over_diagonal_half"]
        for name in names
    ]


def subset_bounds(vectors, subset):
    values = [sum(vector[index] for index in subset) for vector in vectors]
    minimum = min(values)
    maximum = max(values)
    return minimum, maximum


def subset_bound_rows(rows, vectors, names, subset_size):
    output = []
    for subset in itertools.combinations(range(len(names)), subset_size):
        values = [sum(vector[index] for index in subset) for vector in vectors]
        min_index = min(range(len(values)), key=values.__getitem__)
        max_index = max(range(len(values)), key=values.__getitem__)
        output.append({
            "bucket_subset": [names[index] for index in subset],
            "minimum_sum": values[min_index],
            "minimum_denominator": rows[min_index]["reduced_denominator"],
            "maximum_sum": values[max_index],
            "maximum_denominator": rows[max_index]["reduced_denominator"],
        })
    return output


def relaxation(names, vectors, subset_sizes, include_upper):
    dimension = len(names)
    bounds = [
        (
            min(vector[index] for vector in vectors),
            max(vector[index] for vector in vectors),
        )
        for index in range(dimension)
    ]
    a_ub = []
    b_ub = []
    for subset_size in subset_sizes:
        for subset in itertools.combinations(range(dimension), subset_size):
            lower, upper = subset_bounds(vectors, subset)
            lower_row = [0.0] * dimension
            for index in subset:
                lower_row[index] = -1.0
            a_ub.append(lower_row)
            b_ub.append(-lower)
            if include_upper:
                upper_row = [0.0] * dimension
                for index in subset:
                    upper_row[index] = 1.0
                a_ub.append(upper_row)
                b_ub.append(upper)
    result = linprog(
        c=[1.0] * dimension,
        A_ub=a_ub or None,
        b_ub=b_ub or None,
        bounds=bounds,
        method="highs",
    )
    if not result.success:
        raise RuntimeError(result.message)
    return {
        "subset_sizes": list(subset_sizes),
        "include_upper_bounds": include_upper,
        "minimum_relaxed_total": float(result.fun),
        "relaxed_bucket_vector": {
            name: float(value) for name, value in zip(names, result.x)
        },
        "passes_target_minus_one": float(result.fun) > -1.0,
    }


def build_receipt():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    adverse = source["fixture"]["adverse_denominator"]
    nonadverse_rows = [
        row for row in source["rows"]
        if row["reduced_denominator"] != adverse
    ]
    names = bucket_names(nonadverse_rows[0])
    vectors = [bucket_vector(row, names) for row in nonadverse_rows]
    true_totals = [sum(vector) for vector in vectors]
    true_min_index = min(range(len(true_totals)), key=true_totals.__getitem__)
    relaxations = {
        "box_only": relaxation(names, vectors, (), False),
        "pair_lower": relaxation(names, vectors, (2,), False),
        "pair_lower_upper": relaxation(names, vectors, (2,), True),
        "pair_and_triple_lower": relaxation(names, vectors, (2, 3), False),
        "pair_and_triple_lower_upper": relaxation(
            names, vectors, (2, 3), True),
    }
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_kernel_cooccurrence_relaxation",
        "source_packet_kernel_sign_landscape_audit": str(SOURCE),
        "question": (
            "Do observed pairwise or three-way distance-bucket co-occurrence "
            "constraints imply the nonadverse off-diagonal bound > -1?"),
        "fixture": source["fixture"],
        "bucket_names": names,
        "observed_true_nonadverse_boundary": {
            "minimum_denominator": nonadverse_rows[true_min_index][
                "reduced_denominator"],
            "minimum_total": true_totals[true_min_index],
            "target_bound": -1.0,
        },
        "pair_subset_bounds": subset_bound_rows(
            nonadverse_rows, vectors, names, 2),
        "triple_subset_bounds": subset_bound_rows(
            nonadverse_rows, vectors, names, 3),
        "relaxations": relaxations,
        "classification": {
            "box_relaxation_fails": (
                relaxations["box_only"]["minimum_relaxed_total"] <= -1.0),
            "pair_cooccurrence_relaxation_fails": (
                relaxations["pair_lower"]["minimum_relaxed_total"] <= -1.0),
            "triple_cooccurrence_relaxation_fails": (
                relaxations["pair_and_triple_lower"][
                    "minimum_relaxed_total"] <= -1.0),
            "low_order_cooccurrence_insufficient": all(
                relaxations[key]["minimum_relaxed_total"] <= -1.0
                for key in (
                    "box_only",
                    "pair_lower",
                    "pair_lower_upper",
                    "pair_and_triple_lower",
                    "pair_and_triple_lower_upper",
                )),
            "full_packet_geometry_or_stronger_invariant_required": True,
            "finite_relaxation_audit_only": True,
        },
        "candidate_next_action": {
            "name": "full packet geometry invariant",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Pairwise and three-way bucket constraints remain too loose; "
                "the surviving bound likely depends on the arithmetic packet "
                "shape, such as high-prime support, small-prime replacement "
                "pair, or exact source-conductor pair geometry."),
            "prediction": (
                "A feature tied to packet arithmetic should separate the "
                "all-high Q46189 overpayment packet from every nonadverse "
                "replacement packet more directly than low-order bucket "
                "relaxations."),
            "falsifier": (
                "If a source-admissible nonadverse packet has full bucket "
                "geometry reaching <= -1, the overpayment-exclusion route "
                "fails."),
            "smallest_next_test": (
                "Group rows by high-prime support and replacement small-prime "
                "pair, then test whether those factor-geometry classes "
                "explain the off-diagonal minimum."),
        },
        "decision": (
            "Low-order bucket co-occurrence is still insufficient.  The true "
            "finite rows have minimum q=38038 at about -0.847293, but the "
            "pairwise relaxation reaches about -1.283873 and the pair+triple "
            "relaxation reaches about -1.046482.  The next route needs full "
            "packet geometry or a sharper arithmetic invariant."),
        "finite_kernel_cooccurrence_relaxation_audit_only": True,
        "finite_diagnostic_only": True,
        "pairwise_cooccurrence_bound_theorem_proved": False,
        "triple_cooccurrence_bound_theorem_proved": False,
        "full_packet_geometry_bound_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    observed = receipt["observed_true_nonadverse_boundary"]
    relax = receipt["relaxations"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 kernel co-occurrence relaxation audit",
        "",
        "## Question",
        "",
        "Do observed pairwise or three-way distance-bucket co-occurrence",
        "constraints imply the nonadverse off-diagonal bound `> -1`?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_kernel_cooccurrence_relaxation_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-kernel-cooccurrence-relaxation-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"true weakest nonadverse q:           {observed['minimum_denominator']}",
        f"true weakest nonadverse total:       {observed['minimum_total']}",
        f"target lower bound:                  {observed['target_bound']}",
        f"box relaxation minimum:              {relax['box_only']['minimum_relaxed_total']}",
        f"pair lower relaxation minimum:       {relax['pair_lower']['minimum_relaxed_total']}",
        f"pair lower+upper relaxation minimum: {relax['pair_lower_upper']['minimum_relaxed_total']}",
        f"pair+triple lower minimum:           {relax['pair_and_triple_lower']['minimum_relaxed_total']}",
        f"pair+triple lower+upper minimum:     {relax['pair_and_triple_lower_upper']['minimum_relaxed_total']}",
        "```",
        "",
        "## Decision",
        "",
        "Low-order bucket co-occurrence is still insufficient.  Pairwise",
        "constraints relax to about `-1.283873`, and pair-plus-triple",
        "constraints still relax to about `-1.046482`, below the required",
        "`-1` boundary.  The true finite rows survive, so the missing",
        "constraint is not just low-order bucket co-occurrence.",
        "",
        "The next route must use full packet geometry or a sharper arithmetic",
        "invariant, such as high-prime support, small-prime replacement pair,",
        "or exact source-conductor pair geometry.",
        "",
        "This is finite diagnostic evidence only.  It proves no pairwise",
        "co-occurrence bound theorem, triple co-occurrence bound theorem,",
        "full packet geometry theorem, coordinate-00 residue-gap sign theorem,",
        "strict-central Goldbach theorem, or Goldbach proof.",
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
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "true_minimum": receipt[
            "observed_true_nonadverse_boundary"]["minimum_total"],
        "pair_relaxation_minimum": receipt[
            "relaxations"]["pair_lower"]["minimum_relaxed_total"],
        "pair_triple_relaxation_minimum": receipt[
            "relaxations"]["pair_and_triple_lower"][
                "minimum_relaxed_total"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

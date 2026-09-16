"""Audit selector provenance for the Q46189 50A..60A witness.

Kevin correctly flagged that choosing 50A..60A after inspecting slices is
post-hoc.  This receipt records that provenance and runs an internal
leave-one-replacement-denominator-out check: select a slice or block using
the other replacement conductors, then test the held-out conductor.
"""

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_q46189_50a60a_distance_profile_audit import (  # noqa: E402
    band_metric,
    paired_distance_values,
    summarize_block,
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


SOURCE_LEDGER = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-one-coordinate-ratio-ledger-audit.json")
SOURCE_SLICE = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-far-band-slice-balance-audit.json")
SOURCE_DISTANCE_PROFILE = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-50a60a-distance-profile-audit.json")
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-q46189-selector-provenance-holdout-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-q46189-selector-provenance-holdout-audit.md")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def candidate_blocks(row_count):
    coarse = [
        {
            "block_name": f"{start}A_to_{start + 10}A",
            "distance_range": [start * row_count + 1,
                               (start + 10) * row_count],
            "selector_family": "coarse_10A_far_band_slices",
        }
        for start in range(10, 100, 10)
    ]
    micro = [
        {
            "block_name": f"{start}A_to_{stop}A",
            "distance_range": [start * row_count + 1, stop * row_count],
            "selector_family": "contiguous_microblocks_inside_50A_to_60A",
        }
        for start in range(50, 60)
        for stop in range(start + 1, 61)
    ]
    return coarse, micro


def heldout_metric(block, heldout_q, adverse_q, values_by_q):
    lower, upper = block["distance_range"]
    adverse = band_metric(values_by_q[adverse_q], lower, upper)
    heldout = band_metric(values_by_q[heldout_q], lower, upper)
    share_gap = (
        heldout["positive_fraction_of_absolute"]
        - adverse["positive_fraction_of_absolute"])
    total_gap = (
        heldout["total_over_diagonal"]
        - adverse["total_over_diagonal"])
    return {
        "heldout_denominator": heldout_q,
        "heldout_positive_fraction": (
            heldout["positive_fraction_of_absolute"]),
        "heldout_total_over_diagonal": heldout["total_over_diagonal"],
        "heldout_positive_fraction_gap": share_gap,
        "heldout_total_gap": total_gap,
        "heldout_passes_selected_block": share_gap > 0 and total_gap > 0,
    }


def select_on_training(candidates, train_qs, adverse_q, values_by_q):
    summaries = [
        summarize_block(
            candidate["block_name"],
            candidate["distance_range"][0],
            candidate["distance_range"][1],
            adverse_q,
            train_qs,
            values_by_q,
        )
        | {"selector_family": candidate["selector_family"]}
        for candidate in candidates
    ]
    separating = [
        row for row in summaries
        if row["separates_by_both_share_and_total"]
    ]
    if not separating:
        return None
    return max(
        separating,
        key=lambda row: (row["positive_fraction_gap"], row["total_gap"]))


def leave_one_out(selector_family, candidates, replacement_qs, values_by_q):
    rows = []
    for heldout_q in replacement_qs:
        train_qs = [q for q in replacement_qs if q != heldout_q]
        selected = select_on_training(
            candidates, train_qs, DENOMINATOR, values_by_q)
        if selected is None:
            rows.append({
                "heldout_denominator": heldout_q,
                "selected_block": None,
                "heldout_passes_selected_block": False,
            })
            continue
        heldout = heldout_metric(
            selected, heldout_q, DENOMINATOR, values_by_q)
        rows.append({
            "heldout_denominator": heldout_q,
            "selected_block": selected["block_name"],
            "selected_distance_range": selected["distance_range"],
            "training_positive_fraction_gap": (
                selected["positive_fraction_gap"]),
            "training_total_gap": selected["total_gap"],
            "training_min_share_denominator": (
                selected["minimum_replacement_positive_fraction_denominator"]),
            "training_min_total_denominator": (
                selected["minimum_replacement_total_denominator"]),
            **heldout,
        })
    pass_rows = [
        row for row in rows
        if row["heldout_passes_selected_block"]
    ]
    selected_counts = Counter(
        row["selected_block"] for row in rows if row["selected_block"])
    return {
        "selector_family": selector_family,
        "candidate_count": len(candidates),
        "heldout_row_count": len(rows),
        "heldout_pass_count": len(pass_rows),
        "all_heldout_rows_pass": len(pass_rows) == len(rows),
        "selected_block_counts": dict(sorted(selected_counts.items())),
        "minimum_heldout_positive_fraction_gap": min(
            row["heldout_positive_fraction_gap"] for row in pass_rows),
        "minimum_heldout_total_gap": min(
            row["heldout_total_gap"] for row in pass_rows),
        "rows": rows,
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
    replacement_qs = [
        row["reduced_denominator"]
        for row in ledger["replacement_one_coordinate_rows"]
    ]
    values_by_q = {}
    for q in [DENOMINATOR, *replacement_qs]:
        values_by_q[q], _diagonal = paired_distance_values(
            q, cells_by_denominator[q], row_count, active_row_start)

    coarse, micro = candidate_blocks(row_count)
    coarse_holdout = leave_one_out(
        "coarse_10A_far_band_slices", coarse, replacement_qs, values_by_q)
    micro_holdout = leave_one_out(
        "contiguous_microblocks_inside_50A_to_60A",
        micro,
        replacement_qs,
        values_by_q,
    )
    selected_50a60a = summarize_block(
        "50A_to_60A",
        50 * row_count + 1,
        60 * row_count,
        DENOMINATOR,
        replacement_qs,
        values_by_q,
    )
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q46189_selector_provenance_holdout",
        "source_one_coordinate_ledger": str(SOURCE_LEDGER),
        "source_far_band_slice_balance_audit": str(SOURCE_SLICE),
        "source_distance_profile_audit": str(SOURCE_DISTANCE_PROFILE),
        "question": (
            "Was 50A..60A a post-hoc selector, and does a leave-one-"
            "replacement-denominator-out audit support or weaken it?"),
        "fixture": {
            "scale_modulus": SCALE,
            "prime_modulus": PRIME,
            "target_label": TARGET_LABEL,
            "row_count_A": row_count,
            "active_row_start": active_row_start,
            "ell_freeze": parameters["ell_freeze"],
            "divisor_range": list(parameters["divisor_range"]),
            "replacement_denominators": replacement_qs,
        },
        "selector_provenance": {
            "coarse_10A_slice_boundaries_natural_from_active_scale_A": True,
            "coarse_10A_slice_choice_was_post_hoc": True,
            "selected_coarse_slice": "50A_to_60A",
            "selected_coarse_slice_not_predeclared_acceptance_condition": True,
            "microblock_choice_inside_50A_to_60A_was_nested_post_hoc": True,
            "natural_conductor_geometry_selector_proved": False,
            "heldout_conductors_available": True,
            "heldout_conductor_count": len(replacement_qs),
        },
        "selected_50A_to_60A_full_family_metric": selected_50a60a,
        "leave_one_denominator_out": {
            "coarse_10A_far_band_slices": coarse_holdout,
            "contiguous_microblocks_inside_50A_to_60A": micro_holdout,
        },
        "classification": {
            "post_hoc_selector": True,
            "coarse_selector_leave_one_out_survives": (
                coarse_holdout["all_heldout_rows_pass"]
                and coarse_holdout["selected_block_counts"]
                == {"50A_to_60A": len(replacement_qs)}),
            "nested_microblock_leave_one_out_survives": (
                micro_holdout["all_heldout_rows_pass"]),
            "selector_supported_only_as_finite_hypothesis": True,
            "natural_selector_theorem_proved": False,
            "finite_selected_family_diagnostic_only": True,
        },
        "candidate_next_action": {
            "name": "predeclared natural selector or fresh-conductor holdout",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "The 50A..60A slice was selected post-hoc, but it is stable "
                "under leave-one-replacement-denominator-out selection in "
                "the finite replacement family.  A theorem route still needs "
                "a predeclared selector from active-kernel, conductor, or "
                "residual geometry, or fresh conductors not used in the "
                "slice discovery."),
            "prediction": (
                "If the 50A..60A effect is real structure, a predeclared "
                "geometry rule or fresh source-admissible conductors should "
                "select or pass a nearby short block without reusing the "
                "original slice scan."),
            "falsifier": (
                "A fresh source-admissible replacement denominator that "
                "fails the predeclared 50A..60A separator, or a natural "
                "geometry rule that selects a failing slice, demotes this "
                "lane to a fitted artifact."),
            "smallest_next_test": (
                "Freeze a non-post-hoc selector rule before looking at new "
                "conductors, then run a fresh replacement-denominator holdout."),
        },
        "decision": (
            "Kevin's objection is correct: 50A..60A is post-hoc because it "
            "was chosen after examining slices.  The finite evidence does "
            "not become a theorem.  However, it is not merely supported by "
            "the weakest included replacement row: in leave-one-denominator-"
            "out selection, the coarse 10A selector chooses 50A..60A in all "
            "10 folds and every held-out denominator clears the selected "
            "share and total tests.  This supports 50A..60A only as a finite "
            "hypothesis requiring a predeclared natural selector or fresh "
            "held-out conductors."),
        "finite_selector_provenance_holdout_audit_only": True,
        "finite_diagnostic_only": True,
        "natural_selector_theorem_proved": False,
        "fresh_conductor_holdout_proved": False,
        "distance_slice_positive_share_theorem_proved": False,
        "distance_slice_pressure_theorem_proved": False,
        "replacement_residue_gap_bound_theorem_proved": False,
        "coordinate00_residue_gap_sign_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    coarse = receipt["leave_one_denominator_out"][
        "coarse_10A_far_band_slices"]
    micro = receipt["leave_one_denominator_out"][
        "contiguous_microblocks_inside_50A_to_60A"]
    selected = receipt["selected_50A_to_60A_full_family_metric"]
    lines = [
        "# Mobius moment-square degree-5 Q46189 selector provenance holdout audit",
        "",
        "## Question",
        "",
        "Was `50A..60A` a post-hoc selector, and does a",
        "leave-one-replacement-denominator-out audit support or weaken it?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_q46189_selector_provenance_holdout_audit.py",
        "evidence/mobius-moment-square-degree5-q46189-selector-provenance-holdout-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        "post-hoc selector:                         yes",
        "natural conductor selector proved:          no",
        f"selected coarse slice:                      {receipt['selector_provenance']['selected_coarse_slice']}",
        f"selected slice positive-share gap:          {selected['positive_fraction_gap']}",
        f"selected slice total gap:                   {selected['total_gap']}",
        f"coarse leave-one-out pass count:            {coarse['heldout_pass_count']} / {coarse['heldout_row_count']}",
        f"coarse selected-block counts:               {coarse['selected_block_counts']}",
        f"coarse min heldout positive-share gap:      {coarse['minimum_heldout_positive_fraction_gap']}",
        f"coarse min heldout total gap:               {coarse['minimum_heldout_total_gap']}",
        f"nested microblock leave-one-out pass count: {micro['heldout_pass_count']} / {micro['heldout_row_count']}",
        f"nested microblock selected-block counts:    {micro['selected_block_counts']}",
        f"nested microblock min heldout share gap:    {micro['minimum_heldout_positive_fraction_gap']}",
        f"nested microblock min heldout total gap:     {micro['minimum_heldout_total_gap']}",
        "```",
        "",
        "## Decision",
        "",
        "Kevin's objection is correct: `50A..60A` is post-hoc because it was",
        "chosen after examining slices.  The finite evidence does not become a",
        "theorem, and the slice must not be treated as a predeclared acceptance",
        "condition.",
        "",
        "The selector is nevertheless more stable than a single fitted row.  In",
        "leave-one-denominator-out selection over the coarse `10A` far-band",
        "slices, the training set chooses `50A..60A` in all `10/10` folds, and",
        "every held-out denominator clears both the selected positive-share and",
        "total-pressure comparisons.  The nested microblock selector also",
        "passes all held-out denominators, but its choice varies and remains",
        "conditioned on the post-hoc `50A..60A` region.",
        "",
        "The next theorem-shaped route therefore needs either a natural",
        "predeclared selector from active-kernel, conductor, or residual",
        "geometry, or a fresh-conductor holdout frozen before inspection.",
        "This proves no natural selector theorem, distance-slice theorem,",
        "replacement residue-gap theorem, strict-central Goldbach theorem, or",
        "Goldbach proof.",
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
    coarse = receipt["leave_one_denominator_out"][
        "coarse_10A_far_band_slices"]
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "post_hoc_selector": receipt["classification"]["post_hoc_selector"],
        "coarse_selected_block_counts": coarse["selected_block_counts"],
        "coarse_heldout_pass_count": coarse["heldout_pass_count"],
        "natural_selector_theorem_proved": (
            receipt["natural_selector_theorem_proved"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

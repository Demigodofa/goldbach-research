"""Targeted search for additional middle/far adverse denominator examples.

The replacement-family boundary currently has one middle/far adverse exemplar:
M=229, p=379, Q=46189.  This audit selects the weakest prime rows already
identified by full source-start sweeps and checks whether any selected row
adds another middle/far adverse denominator.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-targeted-middle-far-adverse-search.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-targeted-middle-far-adverse-search.md")
SOURCE_CLEARANCE = (
    Path("evidence")
    / "mobius-moment-square-degree5-source-margin-clearance-family-audit.json")
M383_HOLDOUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-source-margin-m383-clearance-holdout.json")
SCOPE_EXTENSION = (
    Path("evidence")
    / "mobius-moment-square-degree5-clearance-scope-extension-audit.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_full_sweeps():
    return [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted(
            (Path("evidence")).glob(
                "mobius-moment-square-degree5-source-start-m*-full-prime-sweep.json"))
    ]


def candidate_rows(limit=7):
    candidates = []
    for sweep in load_full_sweeps():
        scale = sweep["scale_modulus"]
        scale_result = sweep["scale_result"]
        for block in sweep.get("tightest_prime_blocks", [])[:4]:
            candidates.append({
                "selection_source": "tightest_prime_blocks",
                "scale_modulus": scale,
                "prime_modulus": block["prime_modulus"],
                "weakest_label": block["weakest_label"],
                "minimum_slack": block["minimum_slack"],
                "prime_over_scale": block.get(
                    "prime_over_scale", block["prime_modulus"] / scale),
            })
        weakest = (
            sweep.get("weakest_dominance_row")
            or scale_result.get("weakest_dominance_row"))
        if weakest:
            candidates.append({
                "selection_source": "global_weakest_row",
                "scale_modulus": scale,
                "prime_modulus": weakest["prime_modulus"],
                "weakest_label": weakest["label"],
                "minimum_slack": weakest["dominance_slack_above_one_half"],
                "prime_over_scale": weakest["prime_modulus"] / scale,
            })
    unique = {}
    for row in candidates:
        key = (
            row["scale_modulus"],
            row["prime_modulus"],
            row["weakest_label"],
        )
        if key not in unique or row["minimum_slack"] < unique[key][
                "minimum_slack"]:
            unique[key] = row
    return sorted(
        unique.values(), key=lambda row: row["minimum_slack"])[:limit]


def family_counts(summary):
    return {
        family: summary["family_summaries"][family]["negative_count"]
        for family in ("near_1_to_2", "middle_2_to_3", "far_3_plus")
    }


def compact_summary(summary, source):
    counts = family_counts(summary)
    return {
        "summary_source": source,
        "scale_modulus": summary["scale_modulus"],
        "prime_modulus": summary["prime_modulus"],
        "weakest_label": summary["weakest_label"],
        "row_count_A": summary["row_count_A"],
        "threshold_p_times_A": summary["threshold_p_times_A"],
        "negative_denominator_family_counts": counts,
        "middle_far_negative_count": (
            counts["middle_2_to_3"] + counts["far_3_plus"]),
        "largest_middle_negative": (
            summary["family_summaries"]["middle_2_to_3"][
                "largest_negative"]),
        "largest_far_negative": (
            summary["family_summaries"]["far_3_plus"]["largest_negative"]),
        "largest_near_negative": (
            summary["family_summaries"]["near_1_to_2"][
                "largest_negative"]),
        "near_negative_abs": summary["near_negative_abs"],
        "middle_far_positive_margin_sum": (
            summary["middle_far_positive_margin_sum"]),
        "middle_far_total_margin_sum": summary["middle_far_total_margin_sum"],
        "near_negative_over_middle_far_positive": (
            summary["near_negative_abs"]
            / summary["middle_far_positive_margin_sum"]
            if summary["middle_far_positive_margin_sum"] else None),
    }


def existing_summary_map():
    source = json.loads(SOURCE_CLEARANCE.read_text(encoding="utf-8"))
    m383 = json.loads(M383_HOLDOUT.read_text(encoding="utf-8"))
    mapping = {}
    for summary in source["scale_summaries"]:
        key = (
            summary["scale_modulus"],
            summary["prime_modulus"],
            summary["weakest_label"],
        )
        mapping[key] = compact_summary(
            summary, str(SOURCE_CLEARANCE))
    m383_summary = m383["scale_summary"]
    key = (
        m383_summary["scale_modulus"],
        m383_summary["prime_modulus"],
        m383_summary["weakest_label"],
    )
    mapping[key] = compact_summary(m383_summary, str(M383_HOLDOUT))
    return mapping


def compute_missing_summary(candidate):
    from tools.build_mobius_moment_square_degree5_source_margin_clearance_family_audit import (  # noqa: E501
        scale_clearance_summary,
    )

    row = {
        "scale_modulus": candidate["scale_modulus"],
        "top_prime_block": {
            "prime_modulus": candidate["prime_modulus"],
            "weakest_label": candidate["weakest_label"],
        },
    }
    summary = scale_clearance_summary(row)
    return compact_summary(summary, "computed_in_targeted_search")


def build_receipt():
    scope = json.loads(SCOPE_EXTENSION.read_text(encoding="utf-8"))
    existing = existing_summary_map()
    selected = candidate_rows(limit=7)
    rows = []
    computed_count = 0
    for candidate in selected:
        key = (
            candidate["scale_modulus"],
            candidate["prime_modulus"],
            candidate["weakest_label"],
        )
        if key in existing:
            summary = existing[key]
        else:
            summary = compute_missing_summary(candidate)
            computed_count += 1
        rows.append({
            **candidate,
            "clearance_summary": summary,
        })
    middle_far_rows = [
        row for row in rows
        if row["clearance_summary"]["middle_far_negative_count"] > 0]
    new_middle_far_rows = [
        row for row in middle_far_rows
        if not (
            row["scale_modulus"] == 229
            and row["prime_modulus"] == 379
            and row["weakest_label"] == "00,12"
            and row["clearance_summary"]["largest_middle_negative"]
            and row["clearance_summary"]["largest_middle_negative"][
                "reduced_denominator"] == 46189)
    ]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_targeted_middle_far_adverse_search",
        "source_scope_extension_audit": str(SCOPE_EXTENSION),
        "question": (
            "Among the weakest selected prime rows from existing full "
            "source-start sweeps, is there another middle/far adverse "
            "denominator besides Q=46189?"),
        "answer": (
            "No in this bounded targeted search.  The top seven selected weak "
            "prime rows contain the known M=229,p=379,Q=46189 middle/far "
            "adverse example, and the other six selected rows have only "
            "near-threshold adverse denominators.  This strengthens the HOLD: "
            "more adjacent or weak-row finite checks are not yet a theorem "
            "substitute; the route should move to symbolic Q=46189 or a "
            "different targeted search criterion."),
        "selection_rule": (
            "Select unique (M,p,label) rows by increasing dominance slack from "
            "each full source-start sweep's global weakest row and top four "
            "tightest prime blocks; check the first seven."),
        "selected_row_count": len(rows),
        "computed_missing_summary_count": computed_count,
        "selected_rows": rows,
        "middle_far_adverse_selected_row_count": len(middle_far_rows),
        "new_middle_far_adverse_selected_row_count": len(new_middle_far_rows),
        "middle_far_adverse_rows": middle_far_rows,
        "new_middle_far_adverse_rows": new_middle_far_rows,
        "prior_extended_scope": scope["extended_source_scope"],
        "classification": {
            "known_q46189_recovered": any(
                row["scale_modulus"] == 229
                and row["prime_modulus"] == 379
                and row["clearance_summary"]["middle_far_negative_count"] > 0
                for row in rows),
            "additional_middle_far_adverse_example_found": (
                bool(new_middle_far_rows)),
            "all_new_selected_adverse_mass_near_threshold": (
                not new_middle_far_rows),
            "targeted_search_supports_symbolic_q46189_next": (
                not new_middle_far_rows),
        },
        "candidate_next_action": {
            "name": "symbolic Q46189 replacement-family inequality",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Stop treating nearby finite clearance extensions as the main "
                "source of progress; use the single recovered middle/far "
                "adverse example to derive a symbolic replacement-family "
                "payment inequality."),
            "prediction": (
                "A symbolic expression should explain why replacing one high "
                "prime in 11*13*17*19 by the observed small-prime factors "
                "pays the finite-window defect."),
            "falsifier": (
                "If the symbolic family inequality cannot be expressed "
                "without importing total positivity, the replacement-family "
                "route remains finite-only and should be demoted."),
            "smallest_next_test": (
                "Express Q=46189 and its ten replacement rows as omitted-"
                "high-prime families and compare their active/full defect "
                "terms algebraically, before adding more broad finite scans."),
        },
        "decision": (
            "The targeted weak-row search found no second middle/far adverse "
            "denominator.  It recovers Q=46189 and otherwise adds only "
            "near-threshold adverse rows.  This is a precise HOLD against "
            "more same-style finite extension: next progress should be "
            "symbolic Q=46189 replacement-family work or a materially "
            "different search criterion."),
        "finite_targeted_search_only": True,
        "finite_diagnostic_only": True,
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
    lines = [
        "# Mobius moment-square degree-5 targeted middle/far adverse search",
        "",
        "## Question",
        "",
        "Among the weakest selected prime rows from existing full source-start",
        "sweeps, is there another middle/far adverse denominator besides",
        "`Q=46189`?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_targeted_middle_far_adverse_search.py",
        "evidence/mobius-moment-square-degree5-targeted-middle-far-adverse-search.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"selected rows:                         {receipt['selected_row_count']}",
        f"computed missing summaries:            {receipt['computed_missing_summary_count']}",
        f"middle/far adverse selected rows:      {receipt['middle_far_adverse_selected_row_count']}",
        f"new middle/far adverse selected rows:  {receipt['new_middle_far_adverse_selected_row_count']}",
        f"known Q46189 recovered:                {receipt['classification']['known_q46189_recovered']}",
        "```",
        "",
        "The selected rows recover the known `M=229`, `p=379`, `Q=46189`",
        "middle/far adverse example.  The other selected weak rows add only",
        "near-threshold adverse denominators.",
        "",
        "## Decision",
        "",
        "This is a precise HOLD against more same-style finite extension.  Next",
        "progress should be symbolic `Q=46189` replacement-family work or a",
        "materially different search criterion, not another adjacent weak-row",
        "receipt.",
        "",
        "This proves no replacement-family payment theorem, phase-defect payment",
        "theorem, near-adverse upper bound, middle/far lower bound, clearance-family",
        "theorem, source-start theorem, strict-central Goldbach theorem, or Goldbach",
        "proof.",
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
        "selected_rows": receipt["selected_row_count"],
        "new_middle_far_adverse_rows": (
            receipt["new_middle_far_adverse_selected_row_count"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

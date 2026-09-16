"""Extend the replacement-family scope boundary with the M=383 holdout.

The previous scope-boundary audit counted the six source-start clearance
blocks and the four sigma-band blocks.  A later M=383 clearance holdout already
exists and should be attached to the boundary: it checks the next full-sweep
tight block and determines whether it adds another middle/far adverse example.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = (
    Path("evidence")
    / "mobius-moment-square-degree5-clearance-scope-extension-audit.json")
NOTE = (
    Path("notes")
    / "mobius-moment-square-degree5-clearance-scope-extension-audit.md")
BOUNDARY = (
    Path("evidence")
    / "mobius-moment-square-degree5-replacement-family-scope-boundary-audit.json")
M383 = (
    Path("evidence")
    / "mobius-moment-square-degree5-source-margin-m383-clearance-holdout.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def family_counts_from_summary(summary):
    return {
        family: summary["family_summaries"][family]["negative_count"]
        for family in ("near_1_to_2", "middle_2_to_3", "far_3_plus")
    }


def build_receipt():
    boundary = json.loads(BOUNDARY.read_text(encoding="utf-8"))
    m383 = json.loads(M383.read_text(encoding="utf-8"))
    m383_counts = family_counts_from_summary(m383["scale_summary"])
    source_counts = boundary["source_scope"]["negative_denominator_family_counts"]
    extended_counts = {
        family: source_counts[family] + m383_counts[family]
        for family in ("near_1_to_2", "middle_2_to_3", "far_3_plus")
    }
    m383_middle_far = m383_counts["middle_2_to_3"] + m383_counts["far_3_plus"]
    extended_middle_far = (
        extended_counts["middle_2_to_3"] + extended_counts["far_3_plus"])
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_clearance_scope_extension_m383",
        "source_boundary_audit": str(BOUNDARY),
        "source_m383_holdout": str(M383),
        "question": (
            "When the fresh M=383 clearance holdout is attached to the "
            "replacement-family scope boundary, does it add another "
            "middle/far adverse denominator example?"),
        "answer": (
            "No.  The M=383 tight block has three near-threshold adverse "
            "denominators and zero middle/far adverse denominators.  Extending "
            "the source-start clearance coverage from six blocks to seven "
            "blocks keeps the current middle/far adverse support at the single "
            "M=229,p=379,Q=46189 exemplar."),
        "prior_source_scope": {
            "checked_block_count": (
                boundary["source_scope"]["checked_row_count"]),
            "negative_denominator_family_counts": source_counts,
            "middle_far_negative_row_count": (
                boundary["source_scope"]["middle_far_negative_row_count"]),
        },
        "m383_holdout_scope": {
            "scale_modulus": m383["scale_modulus"],
            "prime_modulus": m383["prime_modulus"],
            "weakest_label": m383["weakest_label"],
            "negative_denominator_family_counts": m383_counts,
            "middle_far_negative_row_count": m383_middle_far,
            "near_negative_abs": m383["near_negative_abs"],
            "middle_far_positive_margin_sum": (
                m383["middle_far_positive_margin_sum"]),
            "near_negative_over_middle_far_positive": (
                m383["near_negative_over_middle_far_positive"]),
            "largest_near_negative": (
                m383["scale_summary"]["family_summaries"]["near_1_to_2"][
                    "largest_negative"]),
        },
        "extended_source_scope": {
            "checked_block_count": (
                boundary["source_scope"]["checked_row_count"] + 1),
            "negative_denominator_family_counts": extended_counts,
            "middle_far_negative_row_count": extended_middle_far,
            "known_middle_far_exception": (
                boundary["source_scope"]["middle_far_negative_rows"][0]),
        },
        "classification": {
            "m383_adds_middle_far_adverse_example": m383_middle_far > 0,
            "extended_scope_middle_far_adverse_examples": extended_middle_far,
            "extended_scope_still_single_q46189_middle_far_exemplar": (
                extended_middle_far == 1
                and boundary["classification"][
                    "q46189_payment_is_single_current_middle_far_exemplar"]),
            "near_threshold_adverse_rows_increased": (
                m383_counts["near_1_to_2"] > 0),
        },
        "candidate_next_action": {
            "name": "symbolic Q46189 or targeted middle/far search",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Since the fresh M=383 tight block adds only near-threshold "
                "adverse mass, either prove the Q=46189 replacement-family "
                "inequality symbolically or search deliberately outside the "
                "current tight-block path for a second middle/far adverse "
                "example."),
            "prediction": (
                "More adjacent tight-block clearance holdouts may keep adding "
                "near-threshold adverse rows without producing a second "
                "middle/far adverse example."),
            "falsifier": (
                "A fresh tight block with a middle/far adverse denominator "
                "whose replacement families fail to pay would falsify the "
                "current replacement-family theorem target."),
            "smallest_next_test": (
                "Do not keep extending adjacent tight blocks by inertia; "
                "either derive the symbolic Q=46189 inequality or run a "
                "targeted search over selected weak prime rows for additional "
                "middle/far adverse denominators."),
        },
        "decision": (
            "The M=383 holdout extends the checked source-start clearance "
            "scope but does not broaden the replacement-family evidence: the "
            "single current middle/far adverse exemplar remains Q=46189.  "
            "Further progress should be symbolic Q=46189 work or a targeted "
            "middle/far adverse search, not another adjacent-block extension "
            "without a selection reason."),
        "finite_scope_extension_audit_only": True,
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
    prior = receipt["prior_source_scope"]
    m383 = receipt["m383_holdout_scope"]
    extended = receipt["extended_source_scope"]
    lines = [
        "# Mobius moment-square degree-5 clearance scope extension audit",
        "",
        "## Question",
        "",
        "When the fresh `M=383` clearance holdout is attached to the",
        "replacement-family scope boundary, does it add another middle/far",
        "adverse denominator example?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_mobius_moment_square_degree5_clearance_scope_extension_audit.py",
        "evidence/mobius-moment-square-degree5-clearance-scope-extension-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"prior source checked blocks:        {prior['checked_block_count']}",
        f"prior source near negatives:        {prior['negative_denominator_family_counts']['near_1_to_2']}",
        f"prior source middle/far negatives:  {prior['middle_far_negative_row_count']}",
        f"M383 near negatives:                {m383['negative_denominator_family_counts']['near_1_to_2']}",
        f"M383 middle/far negatives:          {m383['middle_far_negative_row_count']}",
        f"extended checked blocks:            {extended['checked_block_count']}",
        f"extended near negatives:            {extended['negative_denominator_family_counts']['near_1_to_2']}",
        f"extended middle/far negatives:      {extended['middle_far_negative_row_count']}",
        f"M383 near/middle-far positive ratio:{m383['near_negative_over_middle_far_positive']}",
        "```",
        "",
        "The fresh `M=383`, `p=599`, `label=00,12` holdout adds three",
        "near-threshold adverse denominators and zero middle/far adverse",
        "denominators.  The single current middle/far adverse exemplar remains",
        "`M=229`, `p=379`, `Q=46189`.",
        "",
        "## Decision",
        "",
        "Do not keep extending adjacent tight blocks by inertia.  The next useful",
        "route is either symbolic `Q=46189` replacement-family work or a targeted",
        "search over selected weak prime rows for additional middle/far adverse",
        "denominators.",
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
        "m383_middle_far_examples": (
            receipt["m383_holdout_scope"]["middle_far_negative_row_count"]),
        "extended_middle_far_examples": (
            receipt["extended_source_scope"]["middle_far_negative_row_count"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

"""Build the degree-5 translated puncture reachability audit.

The translated phase-curve sweep deliberately tests active-row starts beyond
the canonical source construction.  This receipt checks whether the unique
puncture at M=149, p=163, start 1 is reachable from the original checked-scale
mapping or only from the artificial translated sweep.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tools.build_mobius_moment_square_degree5_checked_scale_dominance_audit import (  # noqa: E402
    scale_parameters,
)
from tools.build_mobius_moment_square_degree5_checked_scale_phase_curve_sweep import (  # noqa: E402
    active_row_start_sweep,
)


TRANSLATED_PUNCTURE = Path(
    "evidence/mobius-moment-square-degree5-translated-puncture-audit.json")
OUTPUT = Path(
    "evidence/"
    "mobius-moment-square-degree5-puncture-reachability-audit.json")


def reachability_summary(puncture):
    scale_modulus = puncture["scale_modulus"]
    prime_modulus = puncture["prime_modulus"]
    parameters = scale_parameters(scale_modulus)
    row_count = parameters["row_count"]
    failure_start = puncture["failure_start"]
    source_start = row_count
    sweep = active_row_start_sweep(scale_modulus)
    start1_window = [failure_start, failure_start + row_count - 1]
    source_window = [source_start, source_start + row_count - 1]
    return {
        "scale_modulus": scale_modulus,
        "prime_modulus": prime_modulus,
        "label": puncture["label"],
        "inferred_n_formula": "M**(1/.59)",
        "row_count_formula": "int((M**(1/.59))**.41)",
        "row_count": row_count,
        "ell_freeze_formula": "row_count + row_count//2",
        "ell_freeze": parameters["ell_freeze"],
        "divisor_range": list(parameters["divisor_range"]),
        "failure_start": failure_start,
        "canonical_source_start_formula": "row_count",
        "canonical_source_start": source_start,
        "failure_start_in_translated_sweep": failure_start in sweep,
        "translated_sweep_start_range": [min(sweep), max(sweep)],
        "translated_sweep_start_count": len(sweep),
        "reachable_from_original_source_mapping": failure_start == source_start,
        "reachability": (
            "REACHABLE" if failure_start == source_start else "UNREACHABLE"),
        "failure_start_window_rows_inclusive": start1_window,
        "source_start_window_rows_inclusive": source_window,
        "prime_modulus_minus_scale_modulus": prime_modulus - scale_modulus,
        "p_minus_M_used_to_select_start": False,
        "calculation": (
            f"M={scale_modulus}: row_count=int((M**(1/.59))**.41)="
            f"{row_count}; original source start=row_count={source_start}; "
            f"translated sweep starts run {min(sweep)}..{max(sweep)}; "
            f"puncture start={failure_start}; since {failure_start}!="
            f"{source_start}, start {failure_start} is not reachable from "
            "the original source-start mapping."),
    }


def build_receipt():
    translated = json.loads(TRANSLATED_PUNCTURE.read_text(encoding="utf-8"))
    summaries = [
        reachability_summary(puncture)
        for puncture in translated["puncture_summaries"]
    ]
    unreachable = [
        row for row in summaries
        if row["reachability"] == "UNREACHABLE"
    ]
    return {
        "status": "AUDIT_degree5_puncture_source_reachability",
        "question": (
            "For M=149, p=163, component (00,12), is translated active-row "
            "start 1 reachable from the original checked-scale source mapping?"),
        "source_translated_puncture_audit": str(TRANSLATED_PUNCTURE),
        "puncture_summaries": summaries,
        "puncture_count": len(summaries),
        "unreachable_puncture_count": len(unreachable),
        "answer": summaries[0]["reachability"] if summaries else None,
        "decision": (
            "The start-1 puncture is a valid translated-sweep falsifier but "
            "not a reachable original source-construction row.  Future "
            "source-window statements should exclude unreachable translated "
            "starts unless a separate mapping makes them source-admissible."),
        "finite_reachability_audit_only": True,
        "finite_diagnostic_only": True,
        "goldbach_proved": False,
        "source_admissible_window_theorem_proved": False,
        "source_window_implication_theorem_proved": False,
        "endpoint_swap_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
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

"""Build the K_286 zero-residue active-character theorem-payment schedule.

The zero-residue raw L1 schedule showed that the no-reflection-discount lane is
not explained by blunt residue-L1 size.  This receipt sharpens the same lane in
the active multiplicative-character coordinates: for each period residue above
N == 0 mod 286, compute the uniform character Linf cap and aggregate character
L2 cap implied by its local main term.

This is coefficient algebra and theorem-target sharpening only.  It proves no
twisted binary-prime character-moment theorem and no Goldbach theorem.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
ZERO_L1_SOURCE = (
    EVIDENCE / "q286-wbss-k286-zero-residue-raw-budget-schedule.json")
CHAR_PAYMENT_SOURCE = (
    EVIDENCE / "q286-wbss-multiplicative-character-payment-audit.json")
CHAR_L2_SOURCE = (
    EVIDENCE / "q286-wbss-multiplicative-character-l2-payment-audit.json")
OUT = EVIDENCE / "q286-wbss-k286-zero-residue-character-budget-schedule.json"

sys.path.insert(0, str(ROOT))

from tools.build_q286_wbss_main_term_sign_audit import finite_summary  # noqa: E402


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    zero_l1 = load_json(ZERO_L1_SOURCE)
    char_payment = load_json(CHAR_PAYMENT_SOURCE)
    char_l2 = load_json(CHAR_L2_SOURCE)

    char_budget = char_payment["character_budget"]
    char_l2_budget = char_l2["character_l2_budget"]
    total_character_l1 = char_budget["total_character_l1"]
    aggregate_character_l2 = char_l2_budget["aggregate_character_l2"]
    global_character_linf_cap = char_budget["equal_character_moment_cap"]
    global_character_l2_cap = char_l2_budget[
        "aggregate_character_moment_l2_cap"]
    global_residue_l1_cap = zero_l1["coefficient_l1_budget"][
        "global_all_residue_uniform_cap"]

    rows = []
    for row in zero_l1["zero_residue_schedule"]["rows"]:
        local_main = row["local_uniform_main_term"]
        character_linf_cap = local_main / total_character_l1
        aggregate_l2_cap = local_main / aggregate_character_l2
        rows.append({
            "target_residue": row["target_residue"],
            "target_mod_286": row["target_mod_286"],
            "period_residue_index": row["period_residue_index"],
            "local_uniform_main_term": local_main,
            "character_linf_cap": character_linf_cap,
            "aggregate_character_l2_cap": aggregate_l2_cap,
            "character_linf_relaxation_vs_global": (
                character_linf_cap / global_character_linf_cap),
            "aggregate_l2_relaxation_vs_global": (
                aggregate_l2_cap / global_character_l2_cap),
            "residue_l1_cap_from_previous_schedule": (
                row["uniform_residue_error_cap"]),
            "aggregate_l2_relaxation_vs_residue_l1_cap": (
                aggregate_l2_cap / row["uniform_residue_error_cap"]),
            "probe_summary": row["probe_summary"],
        })

    tight_linf = min(
        rows, key=lambda row: (row["character_linf_cap"],
                              row["target_residue"]))
    tight_l2 = min(
        rows, key=lambda row: (row["aggregate_character_l2_cap"],
                              row["target_residue"]))
    loose_l2 = max(
        rows, key=lambda row: (row["aggregate_character_l2_cap"],
                              -row["target_residue"]))
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-k286-zero-residue-character-budget-schedule",
        "source_commit": source_commit(),
        "sources": {
            "zero_residue_raw_budget_schedule": str(
                ZERO_L1_SOURCE.relative_to(ROOT)),
            "zero_residue_raw_budget_source_commit": (
                zero_l1["source_commit"]),
            "multiplicative_character_payment_audit": str(
                CHAR_PAYMENT_SOURCE.relative_to(ROOT)),
            "multiplicative_character_payment_source_commit": (
                char_payment["source_commit"]),
            "multiplicative_character_l2_payment_audit": str(
                CHAR_L2_SOURCE.relative_to(ROOT)),
            "multiplicative_character_l2_source_commit": (
                char_l2["source_commit"]),
        },
        "status": "TARGET_zero_residue_character_moment_budget_schedule_unproved",
        "question": (
            "After crude residue-L1 failed to explain the K_286 zero lane, "
            "what active-character moment payments would be sufficient on "
            "N == 0 mod 286?"),
        "answer": (
            "The zero lane also has looser active-character payments than the "
            "global all-residue minimum.  Its tightest aggregate character L2 "
            "cap is about 0.1292282662, compared with the global cap "
            "0.1093074647.  The same tight residue is 9724 mod 10010.  This "
            "sharpens the theorem target but still leaves the needed "
            "pointwise twisted binary-prime moment theorem open."),
        "coefficient_character_budget": {
            "active_character_count": char_budget["active_character_count"],
            "active_real_channel_count": char_budget[
                "active_real_channel_count"],
            "total_character_l1": total_character_l1,
            "aggregate_character_l2": aggregate_character_l2,
            "global_character_linf_cap": global_character_linf_cap,
            "global_aggregate_character_l2_cap": global_character_l2_cap,
            "global_residue_l1_cap": global_residue_l1_cap,
            "character_l2_by_modulus": char_l2_budget[
                "character_l2_by_modulus"],
        },
        "zero_residue_character_schedule": {
            "target_mod_286": 0,
            "period": zero_l1["zero_residue_schedule"]["period"],
            "period_residue_count": len(rows),
            "character_linf_cap_summary": finite_summary(
                row["character_linf_cap"] for row in rows),
            "aggregate_character_l2_cap_summary": finite_summary(
                row["aggregate_character_l2_cap"] for row in rows),
            "aggregate_l2_vs_residue_l1_cap_summary": finite_summary(
                row["aggregate_l2_relaxation_vs_residue_l1_cap"]
                for row in rows),
            "tightest_character_linf_row": tight_linf,
            "tightest_aggregate_l2_row": tight_l2,
            "loosest_aggregate_l2_row": loose_l2,
            "rows": rows,
        },
        "comparison_to_global_character_budget": {
            "zero_lane_tightest_character_linf_cap": tight_linf[
                "character_linf_cap"],
            "global_character_linf_cap": global_character_linf_cap,
            "zero_lane_tightest_linf_relaxation_factor": tight_linf[
                "character_linf_relaxation_vs_global"],
            "zero_lane_tightest_aggregate_l2_cap": tight_l2[
                "aggregate_character_l2_cap"],
            "global_aggregate_l2_cap": global_character_l2_cap,
            "zero_lane_tightest_l2_relaxation_factor": tight_l2[
                "aggregate_l2_relaxation_vs_global"],
            "zero_lane_is_worse_than_global_character_budget": (
                tight_l2["aggregate_character_l2_cap"]
                < global_character_l2_cap),
            "interpretation": (
                "The zero-residue no-reflection-discount lane is not worse "
                "than the global all-residue active-character payment either. "
                "The live obstruction is therefore not coefficient-norm size "
                "alone; it is the missing pointwise signed/twisted binary-"
                "prime moment theorem."),
        },
        "candidate": {
            "name": "zero-residue active-character moment payment schedule",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Reuse the exact zero-lane local-main schedule but pay it in "
                "active multiplicative-character coordinates, including the "
                "aggregate Hilbert L2 theorem shape."),
            "prediction": (
                "If the zero lane is the coefficient-size bottleneck, its "
                "active-character caps should be tighter than the global "
                "all-residue caps."),
            "falsifier": (
                "If all zero-lane character caps are looser than the global "
                "caps, then coefficient norm size is not the bottleneck for "
                "the K_286 no-reflection lane."),
            "smallest_next_action": (
                "Stop refining coefficient-size payments for the zero lane "
                "unless a new signed structure appears; target the raw "
                "twisted binary-prime moment theorem itself."),
        },
        "decision": (
            "TARGET_zero_residue_character_moment_budget_schedule_unproved.  "
            "The zero-lane active-character payment schedule is now pinned. "
            "Like the residue-L1 schedule, it shows the no-reflection lane is "
            "not worse than the global all-residue coefficient payment.  "
            "This does not prove any moment theorem; it redirects the proof "
            "pressure to a pointwise raw signed/character binary-prime "
            "estimate rather than more coefficient-size accounting."),
        "status_boundary": (
            "Coefficient character-payment schedule only.  No zero-residue "
            "raw adverse-drag theorem, no aggregate character-moment theorem, "
            "no universal pointwise raw estimate, no binary-prime moment "
            "theorem, no q286 threshold theorem, no strict-central Goldbach "
            "theorem, and no Goldbach proof is established."),
        "zero_residue_raw_adverse_drag_theorem_proved": False,
        "aggregate_character_moment_theorem_proved": False,
        "universal_pointwise_raw_bound_proved": False,
        "binary_prime_moment_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    schedule = receipt["zero_residue_character_schedule"]
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "period_residue_count": schedule["period_residue_count"],
        "tightest_target_residue": schedule[
            "tightest_aggregate_l2_row"]["target_residue"],
        "tightest_aggregate_l2_cap": schedule[
            "tightest_aggregate_l2_row"]["aggregate_character_l2_cap"],
        "global_aggregate_l2_cap": receipt[
            "coefficient_character_budget"][
                "global_aggregate_character_l2_cap"],
        "zero_lane_is_worse_than_global_character_budget": receipt[
            "comparison_to_global_character_budget"][
                "zero_lane_is_worse_than_global_character_budget"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

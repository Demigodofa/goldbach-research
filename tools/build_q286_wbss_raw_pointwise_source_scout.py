"""Scout current source-shaped routes for the q286 raw pointwise trigger.

The q286 signed-weight proof engine is asleep until a changed condition
appears.  The strongest useful changed condition would be a pointwise raw
weighted binary-prime theorem for the exact signed q286 weight.  This receipt
records a bounded primary-source scout of nearby literature and classifies
whether any checked source reactivates the lane.

This is a source-scout HOLD only.  It promotes no external theorem to a q286
bridge and proves no Goldbach result.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SLEEP_HOLD = EVIDENCE / "q286-wbss-signed-weight-proof-engine-sleep-hold.json"
OUT = EVIDENCE / "q286-wbss-raw-pointwise-source-scout.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def source_rows():
    return [
        {
            "id": "Salmensuu_2021_summands_in_AP",
            "title": (
                "The Goldbach conjecture with summands in arithmetic "
                "progressions"),
            "authors": "Juho Salmensuu",
            "url": "https://arxiv.org/abs/2106.00778",
            "source_type": "primary arXiv source / published-paper locator",
            "checked_claim": (
                "Almost-all result for moduli r up to about "
                "N^(1/2)/log^O(1) N, almost all b2, and almost all eligible "
                "2n <= N."),
            "fit_to_q286_raw_pointwise_trigger": "insufficient",
            "mismatch": (
                "The q286 trigger needs every sufficiently large covered N, "
                "the exact fixed q286 signed weight, strict-central "
                "truncation, and no unnamed exceptional targets.  Almost-all "
                "quantifiers do not pay that pointwise raw bridge."),
            "reactivation_condition": (
                "Derive a no-exception corollary for the exact signed q286 "
                "weight, with explicit threshold and finite remainder."),
        },
        {
            "id": "Halupczok_2012_AP_and_short_intervals",
            "title": (
                "Goldbach's problem with primes in arithmetic progressions "
                "and in short intervals"),
            "authors": "Karin Halupczok",
            "url": "https://arxiv.org/abs/1212.4406",
            "source_type": "primary arXiv source / accepted-paper locator",
            "checked_claim": (
                "Mean-value theorems in Bombieri-Vinogradov style for "
                "binary and ternary additive problems, with a ternary "
                "short-interval application."),
            "fit_to_q286_raw_pointwise_trigger": "insufficient",
            "mismatch": (
                "Mean-value and ternary/short-interval results do not give a "
                "pointwise lower bound for the exact q286 signed weighted "
                "binary-prime convolution for every covered N."),
            "reactivation_condition": (
                "Derive a pointwise fixed finite-modulus weighted binary "
                "prime corollary matching the q286 weight."),
        },
        {
            "id": "Lichtman_2023_Goldbach_upper_bounds",
            "title": (
                "Primes in arithmetic progressions to large moduli, and "
                "Goldbach beyond the square-root barrier"),
            "authors": "Jared Duker Lichtman",
            "url": "https://arxiv.org/abs/2309.08522",
            "source_type": "primary arXiv source",
            "checked_claim": (
                "Improved level of distribution for primes and new upper "
                "bounds for Goldbach representations."),
            "fit_to_q286_raw_pointwise_trigger": "insufficient",
            "mismatch": (
                "Upper bounds for the number of Goldbach representations "
                "and distribution estimates do not provide the required "
                "positive pointwise lower bound for the exact signed q286 "
                "weighted witness."),
            "reactivation_condition": (
                "Use only if a lower-bound or signed-weighted pointwise "
                "corollary is actually derived, not from the upper-bound "
                "statement alone."),
        },
        {
            "id": "Bauer_Wang_2013_binary_AP_large_modulus",
            "title": (
                "The binary Goldbach conjecture with primes in arithmetic "
                "progressions with large modulus"),
            "authors": "Claus Bauer and Yonghui Wang",
            "url": "https://doi.org/10.4064/aa159-3-2",
            "source_type": (
                "bibliographic primary-paper locator; full text not promoted "
                "by this receipt"),
            "checked_claim": (
                "Relevant binary Goldbach in arithmetic progressions with "
                "large modulus, as cited by later AP-Goldbach literature."),
            "fit_to_q286_raw_pointwise_trigger": "not_promoted",
            "mismatch": (
                "The current scout did not verify a theorem statement strong "
                "enough to pay the exact signed q286 raw pointwise target.  "
                "It remains a candidate source to inspect, not an accepted "
                "bridge."),
            "reactivation_condition": (
                "Open and verify the exact theorem statement and constants; "
                "derive the exact signed q286 weighted strict-central "
                "corollary without almost-all exceptions."),
        },
    ]


def build_receipt():
    sleep = load_json(SLEEP_HOLD)
    rows = source_rows()
    direct = [
        row for row in rows
        if row["fit_to_q286_raw_pointwise_trigger"] == "sufficient"
    ]
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-raw-pointwise-source-scout",
        "source_commit": source_commit(),
        "sources": {
            "signed_weight_proof_engine_sleep_hold": str(
                SLEEP_HOLD.relative_to(ROOT)),
            "signed_weight_sleep_status": sleep["status"],
        },
        "status": "SOURCE_SCOUT_no_raw_pointwise_q286_bridge_found",
        "question": (
            "Does a nearby source-shaped theorem currently reactivate the "
            "q286 signed-weight lane by paying the exact raw pointwise "
            "weighted binary-prime target?"),
        "answer": (
            "No checked nearby source reactivates the lane.  Salmensuu gives "
            "almost-all AP-Goldbach information; Halupczok gives mean-value "
            "and ternary/short-interval context; Lichtman improves "
            "distribution and upper bounds for Goldbach representations; "
            "Bauer-Wang remains a relevant source to inspect but is not "
            "promoted here.  None is recorded as a universal pointwise raw "
            "theorem for the exact signed q286 weight."),
        "source_fit_table": rows,
        "fit_summary": {
            "checked_source_count": len(rows),
            "direct_raw_pointwise_bridge_count": len(direct),
            "reactivates_q286_signed_weight_lane": bool(direct),
            "best_current_disposition": (
                "keep q286 signed-weight proof engine asleep until a raw "
                "pointwise theorem or exact derived corollary is available"),
        },
        "required_bridge_shape": {
            "quantifier": "every sufficiently large covered even N",
            "weight": "exact signed q286 finite-modulus left-prime weight",
            "scale": "raw unnormalized log-prime pair sum",
            "support_boundary": (
                "must not normalize by T_N before support is created, unless "
                "a separate positive-mass theorem is explicitly imported"),
            "finite_remainder": (
                "explicit threshold N0 plus finite verification below N0"),
        },
        "candidate": {
            "name": "source-backed raw pointwise q286 bridge",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Reactivate q286 only if a primary source or exact derivation "
                "supplies the raw pointwise weighted binary-prime estimate "
                "the sleep/HOLD requires."),
            "prediction": (
                "Nearby AP-Goldbach literature will be relevant context but "
                "will usually miss the exact no-exception signed-weight "
                "target."),
            "falsifier": (
                "A verified no-exception theorem for the exact signed q286 "
                "weight, or an explicit derivation from a source theorem, "
                "would falsify this HOLD."),
            "smallest_next_action": (
                "Either inspect Bauer-Wang in full for an exact corollary, "
                "or move to a different proof engine rather than retrying "
                "q286 without a raw theorem."),
        },
        "decision": (
            "SOURCE_SCOUT_no_raw_pointwise_q286_bridge_found.  The current "
            "source scout does not reactivate the signed-weight q286 proof "
            "engine.  The lane remains dormant until a source-backed raw "
            "pointwise weighted binary-prime theorem, a materially new signed "
            "weight, a raw active-character moment theorem, or an explicitly "
            "labeled positive-mass theorem changes the condition."),
        "status_boundary": (
            "Source-scout HOLD only.  No external theorem is promoted to a "
            "q286 bridge, no signed-weight major/minor arc estimate, no raw "
            "weighted witness theorem, no active-character moment theorem, "
            "no positive-mass theorem, no q286 threshold theorem, no "
            "strict-central Goldbach theorem, and no Goldbach proof is "
            "established."),
        "external_pointwise_bridge_found": False,
        "signed_weight_major_arc_estimate_proved": False,
        "raw_weighted_witness_theorem_proved": False,
        "active_character_moment_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "checked_source_count": receipt["fit_summary"][
            "checked_source_count"],
        "direct_raw_pointwise_bridge_count": receipt["fit_summary"][
            "direct_raw_pointwise_bridge_count"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

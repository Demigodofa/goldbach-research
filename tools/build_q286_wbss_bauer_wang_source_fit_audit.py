"""Audit Bauer-Wang 2013 against the q286 raw pointwise trigger.

The previous raw pointwise source scout left Bauer-Wang as a relevant source
to inspect.  This receipt checks the source metadata/abstract-level theorem
shape against the exact q286 changed condition.  It is not a full-paper proof
review and it promotes no external theorem to a q286 bridge.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE_SCOUT = EVIDENCE / "q286-wbss-raw-pointwise-source-scout.json"
OUT = EVIDENCE / "q286-wbss-bauer-wang-source-fit-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    scout = load_json(SOURCE_SCOUT)
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-bauer-wang-source-fit-audit",
        "source_commit": source_commit(),
        "sources": {
            "raw_pointwise_source_scout": str(
                SOURCE_SCOUT.relative_to(ROOT)),
            "raw_pointwise_source_scout_status": scout["status"],
        },
        "status": "SOURCE_FIT_Bauer_Wang_not_q286_raw_pointwise_bridge",
        "question": (
            "Does Bauer-Wang 2013 provide the exact raw pointwise theorem "
            "needed to reactivate the q286 signed-weight proof engine?"),
        "answer": (
            "No.  The available PLDML/ICM source metadata describes an "
            "almost-all theorem over prime moduli, residue classes, and "
            "eligible targets.  That shape is relevant AP-Goldbach context "
            "but cannot pay the no-exception, exact signed q286 raw "
            "pointwise bridge."),
        "source_access": {
            "primary_locator": (
                "https://pldml.icm.edu.pl/pldml/element/"
                "bwmeta1.element.bwnjournal-article-doi-10_4064-aa159-3-2"),
            "doi": "10.4064/aa159-3-2",
            "journal": "Acta Arithmetica 159 (2013), 227-243",
            "publisher": (
                "Institute of Mathematics Polish Academy of Sciences"),
            "impam_pdf_redirect_observed": (
                "https://www.impan.pl/pl/download/pdf/aa159-3-2"),
            "access_boundary": (
                "The audit uses source metadata and abstract-level theorem "
                "shape.  It does not claim full-paper theorem extraction."),
        },
        "bauer_wang_theorem_shape_from_metadata": {
            "modulus_quantifier": (
                "almost all prime moduli k <= N^(1/4-epsilon)"),
            "residue_quantifier": (
                "fixed admissible b2 and almost all admissible b1"),
            "target_quantifier": (
                "almost all integers n in the matching congruence class"),
            "summand_requirement": (
                "p_i congruent to b_i mod k for i=1,2"),
            "method_note": (
                "new estimates for exponential sums over primes in "
                "arithmetic progressions"),
        },
        "q286_required_bridge_shape": {
            "target_quantifier": "every sufficiently large covered even N",
            "modulus": "exact fixed q286 finite-modulus package",
            "weight": "exact signed q286 left-prime coefficient",
            "scale": "raw unnormalized log-prime pair sum",
            "interval": "strict central range N/3 < p < 2N/3",
            "finite_remainder": "explicit N0 plus finite verification below N0",
            "support_boundary": (
                "the proof must create support and cannot divide by T_N "
                "before support is known"),
        },
        "mismatches": [
            {
                "id": "almost_all_targets",
                "why_it_blocks_q286_trigger": (
                    "The q286 trigger has no exceptional covered targets "
                    "above threshold; an almost-all target theorem leaves "
                    "exactly the pointwise gap open."),
            },
            {
                "id": "almost_all_moduli_and_residues",
                "why_it_blocks_q286_trigger": (
                    "The source theorem's quantifiers are not the exact fixed "
                    "q286 signed coefficient family."),
            },
            {
                "id": "positive_AP_pair_not_signed_q286_weight",
                "why_it_blocks_q286_trigger": (
                    "A positive AP pair representation theorem is not the "
                    "same object as a lower bound for the signed q286 raw "
                    "weighted convolution."),
            },
            {
                "id": "no_strict_central_or_finite_remainder_bridge",
                "why_it_blocks_q286_trigger": (
                    "The available source metadata does not provide the "
                    "strict-central q286 truncation, explicit threshold, and "
                    "finite-remainder package required by the route."),
            },
        ],
        "fit_summary": {
            "source": "Bauer_Wang_2013_binary_AP_large_modulus",
            "fit_to_q286_raw_pointwise_trigger": "insufficient",
            "reactivates_q286_signed_weight_lane": False,
            "external_pointwise_bridge_found": False,
            "remaining_use": (
                "Relevant AP-Goldbach context and possible ingredient for a "
                "bespoke derivation, not a direct bridge."),
        },
        "decision": (
            "Bauer-Wang closes as a direct q286 wake-up source.  Its "
            "metadata-level theorem shape is almost-all and AP-positive, "
            "whereas the q286 signed-weight trigger needs an every-N raw "
            "signed weighted convolution estimate for the exact fixed q286 "
            "package.  Future use requires a new derivation with those "
            "missing quantifiers supplied explicitly."),
        "next_evidence_bearing_move": (
            "Stop retrying named AP-Goldbach source fit for q286.  Either "
            "derive the raw active-character theorem target from scratch, or "
            "switch to a different proof engine whose first obligation is not "
            "already Goldbach-strength pointwise positivity."),
        "status_boundary": (
            "Source-fit HOLD only.  No Bauer-Wang theorem is promoted to a "
            "q286 bridge, no raw weighted witness theorem, no positive-mass "
            "theorem, no q286 threshold theorem, no strict-central Goldbach "
            "theorem, and no Goldbach proof is established."),
        "bauer_wang_direct_bridge_found": False,
        "external_pointwise_bridge_found": False,
        "raw_weighted_witness_theorem_proved": False,
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
        "fit_to_q286_raw_pointwise_trigger": (
            receipt["fit_summary"]["fit_to_q286_raw_pointwise_trigger"]),
        "reactivates_q286_signed_weight_lane": (
            receipt["fit_summary"]["reactivates_q286_signed_weight_lane"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

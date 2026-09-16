"""Build a compact route-pattern atlas from the current Goldbach receipts.

The atlas is not a visualization and not a proof attempt.  It is a durable
step-back map over the current evidence record: which route families have been
falsified, which remain finite diagnostics, and which universal theorem
obligations still look worth attacking.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = Path("evidence/goldbach-route-pattern-atlas.json")
NOTE = Path("notes/goldbach-route-pattern-atlas.md")

SOURCES = {
    "zero_mass_l2_bridge": (
        "evidence/q286-wbss-zero-mass-l2-logical-bridge-audit.json"),
    "strict_raw_gap_hold": (
        "evidence/q286-wbss-strict-raw-gap-analytic-hold.json"),
    "rawization_obligation": (
        "evidence/q286-wbss-rawization-obligation-audit.json"),
    "fourier_burden": "evidence/q286-wbss-fourier-burden-audit.json",
    "residual_absorption_threshold": (
        "evidence/q286-wbss-residual-absorption-threshold-audit.json"),
    "residual_absorption_population": (
        "evidence/q286-wbss-residual-absorption-population-audit.json"),
    "four_modulus_adverse_drag": (
        "evidence/q286-wbss-four-modulus-adverse-drag-horizon-audit.json"),
    "four_modulus_component_envelope": (
        "evidence/q286-wbss-four-modulus-component-envelope-horizon-audit.json"),
    "signed_weight_proof_engine_sleep": (
        "evidence/q286-wbss-signed-weight-proof-engine-sleep-hold.json"),
    "signed_weight_principal_factor": (
        "evidence/q286-wbss-signed-weight-principal-factor-audit.json"),
    "raw_adverse_drag_target": (
        "evidence/q286-wbss-raw-adverse-drag-theorem-target.json"),
    "post_q286_triage": "evidence/post-q286-proof-engine-triage.json",
    "q46189_factor_geometry": (
        "evidence/mobius-moment-square-degree5-q46189-factor-geometry-route-triage.json"),
    "q46189_all_replacement_mirror": (
        "evidence/mobius-moment-square-degree5-q46189-all-replacement-mirror-compensation-audit.json"),
    "q46189_middle_loss_gap": (
        "evidence/mobius-moment-square-degree5-q46189-middle-loss-condition-gap-audit.json"),
    "q46189_source_factor_pattern": (
        "evidence/mobius-moment-square-degree5-q46189-source-factor-pattern-map-audit.json"),
}


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_sources():
    loaded = {}
    for name, path in SOURCES.items():
        receipt_path = ROOT / path
        loaded[name] = json.loads(receipt_path.read_text(encoding="utf-8"))
    return loaded


def source_summary(name, path, data):
    return {
        "name": name,
        "path": path,
        "status": data.get("status"),
        "goldbach_proved": data.get("goldbach_proved", False),
        "decision": data.get("decision"),
    }


def build_receipt():
    data = load_sources()
    q46189 = data["q46189_source_factor_pattern"]
    raw_target = data["raw_adverse_drag_target"]
    component = data["four_modulus_component_envelope"]
    adverse = data["four_modulus_adverse_drag"]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_goldbach_route_pattern_atlas",
        "question": (
            "Looking across the accumulated Goldbach research record, which "
            "patterns look structural, which routes are dead ends, and what "
            "is the next evidence-bearing proof or disproof lens?"),
        "source_receipts": [
            source_summary(name, path, data[name])
            for name, path in SOURCES.items()
        ],
        "route_patterns": [
            {
                "name": "finite data is a falsifier and calibrator, not an acceptance condition",
                "classification": "boundary",
                "evidence": [
                    "q286 zero-mass arithmetic passed on checked rows, but the L2 bridge remains HOLD without a universal raw pointwise moment theorem.",
                    "strict raw-gap correction says future finite rows are useful only as falsifiers or calibration for a predeclared theorem implication.",
                    "q46189 replacement work repeatedly eliminates scalar shortcuts without promoting finite separators into theorem constants.",
                ],
                "implication": (
                    "A route is alive only if it names the universal theorem "
                    "it would prove or the concrete obstruction it would "
                    "falsify.  More checked rows alone cannot close Goldbach."),
            },
            {
                "name": "normalized or conditional mass routes collapse back to raw pointwise obligations",
                "classification": "retired_as_standalone",
                "evidence": [
                    data["rawization_obligation"]["decision"],
                    data["signed_weight_principal_factor"]["decision"],
                    data["signed_weight_proof_engine_sleep"]["decision"],
                ],
                "implication": (
                    "Do not treat local factors, normalized orbit measures, "
                    "or distributional anti-alignment as independent support. "
                    "They need either T_N>0 from elsewhere or a direct raw "
                    "witness inequality."),
            },
            {
                "name": "fitted constants are not theorem constants",
                "classification": "finite_fit_only",
                "evidence": [
                    data["residual_absorption_threshold"]["decision"],
                    data["residual_absorption_population"]["decision"],
                ],
                "implication": (
                    "The .125/.126/.13 absorption numbers are useful stress "
                    "targets, not universal constants.  A proof would need a "
                    "uniform signed residual estimate."),
            },
            {
                "name": "Fourier sparsification did not reduce the theorem burden",
                "classification": "retired_shortcut",
                "evidence": [data["fourier_burden"]["decision"]],
                "implication": (
                    "The route cannot honestly be a small-mode lemma.  If the "
                    "q286 Fourier side remains useful, it asks for broad "
                    "high-conductor signed binary-prime correlation control."),
            },
            {
                "name": "adverse drag has the strongest finite q286 shape, but still needs a raw theorem",
                "classification": "live_candidate",
                "evidence": [
                    adverse["decision"],
                    component["decision"],
                    raw_target["decision"],
                ],
                "implication": (
                    "The best q286 proof-shaped object is not another fitted "
                    "constant; it is a universal pointwise raw inequality such "
                    "as A_raw_-(N) < L_raw(N), or a per-modulus adverse "
                    "supremum theorem whose sum stays below local main."),
            },
            {
                "name": "Q46189 scalar dots died; source-block matrix topology survived",
                "classification": "live_candidate",
                "evidence": [
                    data["q46189_factor_geometry"]["decision"],
                    data["q46189_all_replacement_mirror"]["decision"],
                    data["q46189_middle_loss_gap"]["decision"],
                    q46189["decision"],
                ],
                "implication": (
                    "The replacement-packet lane should stop hunting single "
                    "scalar thresholds and test the input-side source-block "
                    "interaction sign invariant across all 34 rows."),
            },
        ],
        "proof_lens": {
            "current_strategy": (
                "Prove by finding a universal raw pointwise lower bound or "
                "adverse-drag bound that forces a positive strict-central "
                "prime-pair witness for all sufficiently large even N."),
            "surviving_targets": [
                "q286 raw adverse-drag theorem target A_raw_-(N) < L_raw(N)",
                "q286 direct raw signed witness theorem W_phi(N) > 0",
                "q286 per-modulus adverse supremum control below local main",
                "Q46189 source-block interaction sign invariant",
                "post-q286 Mobius incomplete-prime row covariance target",
            ],
        },
        "disproof_lens": {
            "current_strategy": (
                "Attack each proof route as if Goldbach were false: locate "
                "where local main, raw mass, source geometry, or signed "
                "correlation could fail."),
            "observed_result": (
                "No counterexample to Goldbach has been found in these "
                "receipts.  The disproof lens has instead falsified proposed "
                "proof mechanisms: normalized L2 acceptance, residual "
                "constant promotion, Fourier sparsification, scalar "
                "replacement thresholds, and universal mirror-block positivity."),
            "next_falsifiers": [
                "A row violating A_raw_-(N) < L_raw(N) after the raw quantities are defined universally.",
                "A replacement packet at least as tight as q=38038 whose source-block topology predicts compensation but non-middle payment is nonpositive.",
                "An input-side source-block invariant that cannot predict the first off-diagonal non-middle sign before output buckets are computed.",
            ],
        },
        "rill_read": (
            "The strongest shape across the record is not a pretty point "
            "cloud.  It is a narrowing of theorem type: finite data keeps "
            "killing scalar or normalized shortcuts, while the live routes "
            "ask for raw pointwise inequalities or exact input-side matrix "
            "invariants.  A linked plot/table may help inspect anomalies, "
            "but only if it is indexed by theorem obligation and falsifier, "
            "not by residue labels masquerading as geometry."),
        "candidate_next_action": {
            "name": "all-row source-block interaction sign audit",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Use the Q46189 source-block matrix as the next hard "
                "falsifier for the only newly surviving pattern."),
            "prediction": (
                "If the matrix topology is real, the first off-diagonal "
                "non-middle sign should be predictable from input-side "
                "source-factor partitions across all 34 replacement rows."),
            "falsifier": (
                "If the sign rule requires already knowing output buckets or "
                "fails on ordinary rows, the matrix pattern is descriptive "
                "only and should sleep."),
            "smallest_test": (
                "Build the ordered 3x3 source-block matrix for all 34 "
                "replacement rows and classify first off-diagonal non-middle "
                "signs by input-side factor partitions."),
        },
        "finite_atlas_only": True,
        "goldbach_counterexample_found": False,
        "goldbach_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "universal_raw_pointwise_theorem_proved": False,
        "source_block_interaction_sign_theorem_proved": False,
    }


def write_note(receipt):
    raw = receipt["proof_lens"]["surviving_targets"]
    dead = [
        item["name"] for item in receipt["route_patterns"]
        if item["classification"] in {"retired_as_standalone",
                                      "retired_shortcut",
                                      "finite_fit_only"}
    ]
    live = [
        item["name"] for item in receipt["route_patterns"]
        if item["classification"] == "live_candidate"
    ]
    lines = [
        "# Goldbach route pattern atlas",
        "",
        "## Question",
        "",
        "Looking across the accumulated Goldbach research record, which",
        "patterns look structural, which routes are dead ends, and what is",
        "the next evidence-bearing proof or disproof lens?",
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_goldbach_route_pattern_atlas.py",
        "evidence/goldbach-route-pattern-atlas.json",
        "```",
        "",
        "## Step-back read",
        "",
        receipt["rill_read"],
        "",
        "## Retired or demoted route shapes",
        "",
    ]
    for item in dead:
        lines.append(f"- {item}")
    lines.extend([
        "",
        "## Live route shapes",
        "",
    ])
    for item in live:
        lines.append(f"- {item}")
    lines.extend([
        "",
        "## Surviving proof targets",
        "",
    ])
    for item in raw:
        lines.append(f"- {item}")
    lines.extend([
        "",
        "## Disproof lens",
        "",
        receipt["disproof_lens"]["observed_result"],
        "",
        "## Next action",
        "",
        receipt["candidate_next_action"]["smallest_test"],
        "",
        "This is an atlas of route obligations and falsifiers, not a proof.",
        "It proves no universal raw pointwise theorem, source-block",
        "interaction sign theorem, strict-central Goldbach theorem, or",
        "Goldbach proof.",
        "",
    ])
    NOTE.write_text("\n".join(lines), encoding="utf-8")


def main():
    receipt = build_receipt()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    write_note(receipt)
    print(json.dumps({
        "out": str(OUT),
        "status": receipt["status"],
        "route_pattern_count": len(receipt["route_patterns"]),
        "candidate_next_action": receipt["candidate_next_action"]["name"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

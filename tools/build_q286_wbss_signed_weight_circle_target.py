"""Build the q286 signed-weight circle-method theorem target.

The signed-region source-fit audit left no named external bridge.  This receipt
records the exact bespoke target that would have to be proved: a raw weighted
binary-prime convolution for the single signed q286 weight, with a collapse
classifier for arguments that first assume T_N>0.

This is a theorem target and logical classifier only.  No major/minor arc
estimate, signed distribution theorem, positive-mass theorem, or Goldbach proof
is established.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SIGNED_SOURCE_FIT = EVIDENCE / "q286-wbss-signed-region-source-fit-audit.json"
CIRCLE_DECOMPOSITION = (
    EVIDENCE / "q286-wbss-raw-character-circle-decomposition.json")
NEGATIVE_REGION = (
    EVIDENCE / "q286-wbss-negative-region-mass-threshold-audit.json")
OUT = EVIDENCE / "q286-wbss-signed-weight-circle-target.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_receipt():
    signed_fit = load_json(SIGNED_SOURCE_FIT)
    circle = load_json(CIRCLE_DECOMPOSITION)
    negative = load_json(NEGATIVE_REGION)
    return {
        "schema_version": 1,
        "receipt": "q286-wbss-signed-weight-circle-target",
        "source_commit": source_commit(),
        "sources": {
            "signed_region_source_fit_audit": str(
                SIGNED_SOURCE_FIT.relative_to(ROOT)),
            "signed_region_source_fit_status": signed_fit["status"],
            "raw_character_circle_decomposition": str(
                CIRCLE_DECOMPOSITION.relative_to(ROOT)),
            "raw_character_circle_status": circle["status"],
            "negative_region_mass_threshold_audit": str(
                NEGATIVE_REGION.relative_to(ROOT)),
            "negative_region_mass_threshold_status": negative["status"],
        },
        "status": "TARGET_bespoke_signed_weight_circle_method_or_collapse",
        "question": (
            "What exact circle-method theorem would have to replace the "
            "missing signed-region source bridge, and when does it collapse "
            "to ordinary strict-central Goldbach support?"),
        "answer": (
            "The surviving q286 proof engine is a direct raw estimate for one "
            "signed weighted binary-prime convolution.  The route survives if "
            "major and minor arcs prove W_phi(N)>0 in raw scale for every "
            "sufficiently large covered N.  It collapses if the proof first "
            "requires T_N>0 and then only controls normalized landing or "
            "negative-region mass conditionally."),
        "signed_weight_definitions": {
            "strict_central_interval": "I_N={n integer: N/3<n<2N/3}.",
            "prime_log_weight": (
                "P(n)=log(n) if n is prime, and P(n)=0 otherwise."),
            "left_residue_weight": (
                "Phi_a(n)=phi_a(n mod 10010), the normalized q286-WBSS "
                "single signed residue weight for a=N mod 10010."),
            "raw_weighted_witness": (
                "W_phi(N)=sum_{n in I_N} P(n)P(N-n)Phi_a(n)."),
            "positive_negative_split": (
                "W_phi(N)=W_+(N)-W_-(N), where W_+ sums residues with "
                "Phi_a>0 and W_- sums -Phi_a over residues with Phi_a<0."),
            "circle_integral": (
                "W_phi(N)=int_0^1 Q_{a,N}(alpha)P_N(alpha)"
                "e(-alpha*N)dalpha."),
            "weighted_left_sum": (
                "Q_{a,N}(alpha)=sum_{n in I_N}P(n)Phi_a(n)e(alpha*n)."),
            "unweighted_right_sum": (
                "P_N(alpha)=sum_{n in I_N}P(n)e(alpha*n)."),
        },
        "exact_target": {
            "raw_pointwise_statement": (
                "For every sufficiently large covered even N, prove "
                "W_phi(N)>0 directly in raw scale."),
            "equivalent_signed_region_statement": signed_fit[
                "required_theorem_shape"]["raw_inequality"],
            "strict_central_support_consequence": (
                "If W_phi(N)>0 then at least one strict-central prime pair "
                "exists, because W_phi(N)=0 when no such pair exists."),
            "finite_remainder": (
                "The theorem must provide an explicit threshold N0 and a "
                "separate finite verification for covered even N<N0."),
        },
        "major_minor_arc_target": {
            "major_arc_required_output": (
                "A positive explicit main term for the exact signed weight "
                "Phi_a, including strict-central truncation and all local "
                "factors, not merely T_N times a conditional normalized mean."),
            "minor_arc_required_output": (
                "A pointwise error bound for every covered N>=N0 smaller "
                "than the signed major-arc surplus."),
            "character_equivalent": (
                "Equivalently, prove raw active-character moment bounds "
                "strong enough that the signed-region inequality or "
                "W_phi(N)>0 follows without assuming support first."),
            "finite_constants_to_preserve": {
                "shape_threshold_minimum": signed_fit["fit_summary"][
                    "shape_threshold_minimum"],
                "minimum_local_uniform_shape_margin": signed_fit[
                    "fit_summary"]["minimum_local_uniform_shape_margin"],
                "active_character_l2_related_but_unproved": signed_fit[
                    "fit_summary"]["internal_related_unproved_target"],
            },
        },
        "zero_mass_non_circularity_check": {
            "if_T_N_zero": (
                "No strict-central prime pairs imply P(n)P(N-n)=0 for every "
                "n in I_N, hence W_phi(N)=W_+(N)=W_-(N)=0."),
            "strict_target_at_zero_mass": "W_phi(N)>0 becomes 0>0, false.",
            "meaning": (
                "A proof of the raw strict statement would create support.  "
                "A normalized theorem about landing fractions cannot do that "
                "unless support is created inside the same proof."),
        },
        "collapse_classifier": {
            "survives_if": (
                "The argument proves W_phi(N)>0, W_+(N)>W_-(N), or an "
                "equivalent raw adverse-drag inequality directly for every "
                "sufficiently large covered N."),
            "collapses_if": (
                "The argument first assumes/proves T_N>0 by an independent "
                "strict-central Goldbach-strength theorem, then applies q286 "
                "only as conditional distribution control."),
            "invalid_substitutes": [
                "finite q286 windows",
                "local-uniform shape margin without pointwise prime-pair control",
                "almost-all or averaged AP Goldbach statements",
                "marginal AP prime counts",
                "normalizing by T_N before raw support exists",
            ],
            "sleep_condition": (
                "If every available route to W_phi(N)>0 requires T_N>0 first, "
                "sleep q286 as a proof engine and preserve it only as a "
                "coefficient/visual guide."),
        },
        "candidate": {
            "name": "bespoke signed q286 weighted circle-method target",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Treat q286 as one signed residue weight inside the binary "
                "prime convolution, so the proof target is direct raw "
                "positivity rather than post-support distribution."),
            "prediction": (
                "If q286 genuinely helps, the exact signed weight will have "
                "a positive major-arc surplus whose minor-arc error can be "
                "bounded pointwise."),
            "falsifier": (
                "If the only positive main term available is imported as "
                "T_N>0 before q286 enters, the q286 lane has not reduced the "
                "Goldbach-strength existence problem."),
            "smallest_next_test": (
                "Attempt a symbolic major-arc local-factor decomposition for "
                "the signed weight Phi_a and identify whether the positive "
                "term is independent raw singular-series mass or only "
                "T_N times a conditional mean."),
        },
        "decision": (
            "TARGET_bespoke_signed_weight_circle_method_or_collapse.  The "
            "exact surviving theorem target is a raw pointwise signed "
            "weighted binary-prime convolution W_phi(N)>0.  This target is "
            "non-circular as a strict raw statement because zero support gives "
            "W_phi(N)=0.  No major/minor arc estimate is proved.  The next "
            "evidence-bearing step is a symbolic major-arc local-factor "
            "decomposition for Phi_a, or a sleep decision if that decomposition "
            "only becomes positive after importing T_N>0."),
        "status_boundary": (
            "Theorem target and collapse classifier only; this is not a "
            "theorem.  No major/minor arc estimate, signed negative-region "
            "distribution theorem, raw adverse-drag theorem, positive-mass "
            "theorem, q286 threshold theorem, strict-central Goldbach "
            "theorem, or Goldbach proof is established."),
        "goldbach_proved": False,
        "major_minor_arc_estimate_proved": False,
        "signed_negative_region_distribution_theorem_proved": False,
        "raw_adverse_drag_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "universal_pointwise_bound_proved": False,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    receipt = load_json(OUT)
    print(json.dumps({
        "out": str(OUT.relative_to(ROOT)),
        "status": receipt["status"],
        "shape_threshold_minimum": (
            receipt["major_minor_arc_target"][
                "finite_constants_to_preserve"]["shape_threshold_minimum"]),
        "minimum_local_uniform_shape_margin": (
            receipt["major_minor_arc_target"][
                "finite_constants_to_preserve"][
                    "minimum_local_uniform_shape_margin"]),
        "major_minor_arc_estimate_proved": (
            receipt["major_minor_arc_estimate_proved"]),
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

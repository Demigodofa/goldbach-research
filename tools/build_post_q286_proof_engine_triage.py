"""Choose the next analytical proof-engine target after q286 sleep.

This derived receipt is not a proof.  It records why more finite q286 evidence
is no longer an acceptance condition, compares the older non-q286 source gates,
and selects the narrowest surviving theorem-shaped target.
"""

from __future__ import annotations

import json
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mobius_balanced_trilinear_source_gate import balanced_trilinear_budget
from mobius_covariance_dyadic_scale_gate import dyadic_scale_budget
from mobius_long_block_factor_gate import long_block_factor_budget
from mobius_prime_exponent_rebalance_gate import (
    prime_exponent_rebalance_budget,
    wright_factor_range,
)


EVIDENCE = ROOT / "evidence"
NOTES = ROOT / "notes"
OUT = EVIDENCE / "post-q286-proof-engine-triage.json"

Q286_ACTIVE_CHARACTER = EVIDENCE / "q286-wbss-active-character-collapse-audit.json"
Q286_SLEEP = EVIDENCE / "q286-wbss-signed-weight-proof-engine-sleep-hold.json"
Q286_TRIAGE = EVIDENCE / "q286-non-circular-route-triage-audit.json"


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def fraction_text(value):
    if isinstance(value, F):
        return {
            "fraction": f"{value.numerator}/{value.denominator}",
            "decimal": float(value),
        }
    if isinstance(value, tuple):
        return [fraction_text(item) for item in value]
    if isinstance(value, dict):
        return {key: fraction_text(item) for key, item in value.items()}
    return value


def build_receipt():
    q286_active = load_json(Q286_ACTIVE_CHARACTER)
    q286_sleep = load_json(Q286_SLEEP)
    q286_triage = load_json(Q286_TRIAGE)

    scale_gate = dyadic_scale_budget()
    first_long = long_block_factor_budget(F(3, 4), F(1, 2))
    balanced_source = balanced_trilinear_budget(F(3, 4), F(1, 2))
    rebalance = prime_exponent_rebalance_budget(F(59, 100))

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "q286_active_character_collapse": str(
                Q286_ACTIVE_CHARACTER.relative_to(ROOT)),
            "q286_signed_weight_sleep_hold": str(Q286_SLEEP.relative_to(ROOT)),
            "q286_non_circular_route_triage": str(Q286_TRIAGE.relative_to(ROOT)),
            "balanced_semiprime_budget": "balanced_semiprime_budget.py",
            "cofactor_averaging_budget": "cofactor_averaging_budget.py",
            "mobius_covariance_source_gate": "mobius_covariance_source_gate.py",
            "mobius_covariance_dyadic_scale_gate": (
                "mobius_covariance_dyadic_scale_gate.py"),
            "mobius_long_block_factor_gate": "mobius_long_block_factor_gate.py",
            "mobius_balanced_trilinear_source_gate": (
                "mobius_balanced_trilinear_source_gate.py"),
            "mobius_prime_exponent_rebalance_gate": (
                "mobius_prime_exponent_rebalance_gate.py"),
        },
        "status": "TARGET_mobius_incomplete_prime_row_covariance_after_q286_sleep",
        "status_boundary": (
            "proof-engine triage only; no finite q286 horizon result, fitted "
            "constant, normalized L2 diagnostic, source exponent match, or "
            "visual structure is accepted as a Goldbach bridge"),
        "goldbach_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "q286_reactivated": False,
        "mobius_covariance_theorem_proved": False,
        "source_theorem_directly_applies": False,
        "universal_pointwise_acceptance_condition": (
            "prove an unnormalized analytical estimate strong enough to put "
            "the relevant adverse/covariance term below the local main term "
            "for every sufficiently large N, plus a finite remainder"),
        "q286_state": {
            "active_character_status": q286_active["status"],
            "signed_weight_sleep_status": q286_sleep["status"],
            "component_pair_triage_status": q286_triage["status"],
            "decision": (
                "q286 remains a structured reservoir.  It is not accepted by "
                "more finite horizon evidence unless a changed condition "
                "supplies an independent raw pointwise estimate, a materially "
                "new signed weight, or a source-backed cone theorem."),
            "reactivation_triggers": q286_sleep["reactivation_triggers"],
        },
        "older_non_q286_route_triage": {
            "balanced_semiprime_budget": {
                "role": "reservoir_not_active_engine",
                "open_requirement": (
                    "a lower bound for the signed total T_kappa exceeding "
                    "the semiprime budget"),
                "decision": (
                    "useful rare-factor and support bookkeeping, but it "
                    "explicitly asserts no lower bound for T_kappa"),
            },
            "cofactor_averaging_budget": {
                "role": "negative_source_gate",
                "decision": (
                    "the unchanged Bettin-Chandee generic L2 plug-in fails "
                    "the exponent budget; only a structurally stronger "
                    "cofactor method would be a changed condition"),
            },
            "periodic_character_comparison": {
                "role": "conditional_component_not_prime_pair_engine",
                "decision": (
                    "retains a positive prime-versus-model comparison under "
                    "a zero hypothesis, but the old Type I insertion is "
                    "incompatible and gives no prime-prime positivity"),
            },
            "large_modulus_source_gate": {
                "role": "negative_source_gate",
                "decision": (
                    "the bare 3/5 exponent match is not licensed because the "
                    "fixed-residue, well-factorable, endpoint, and shifting "
                    "hypotheses are not matched"),
            },
        },
        "selected_non_q286_target": {
            "name": "Mobius incomplete prime-row covariance",
            "role": "next_analytical_proof_engine_candidate",
            "why_selected": (
                "It names a pointwise asymptotic estimate rather than another "
                "finite q286 fit: all short and medium dyadic blocks are paid, "
                "leaving a precise long-block incomplete prime-row covariance "
                "where signs, prime-modulus averaging, or a new local "
                "asymptotic-large-sieve theorem must enter before Cauchy."),
            "required_theorem_shape": (
                "a local signed covariance or boundary-operator estimate for "
                "the actual Mobius-log coefficients on prime rows, strong "
                "enough to beat the N^(1499/1000+epsilon) benchmark uniformly "
                "over the surviving long dyadic blocks"),
            "known_paid_part": fraction_text(scale_gate),
            "first_unpaid_balanced_block_probe": fraction_text(first_long),
            "balanced_source_gate_at_y_3_4_alpha_1_2": fraction_text(
                balanced_source),
            "prime_exponent_rebalance_gate_at_mu_59_100": fraction_text(
                rebalance),
            "wright_factor_range_at_mu_59_100": fraction_text(
                wright_factor_range(F(59, 100))),
            "falsifiers": [
                (
                    "any proposed theorem that first takes absolute values or "
                    "applies generic Cauchy reproduces the long-block Y^2 "
                    "collision loss"),
                (
                    "a source theorem whose hypotheses only see max-norm "
                    "active-band coefficients, not the L2-normalized band "
                    "energy, is too weak at the balanced block"),
                (
                    "a prime-exponent rebalance that needs Wright 2.2 or "
                    "classical BV in the unchanged unpaid range has an empty "
                    "source range"),
            ],
            "smallest_next_test": (
                "derive the exact incomplete-row boundary operator after the "
                "complete-period conductor closure, then test whether its "
                "operator norm factors through the actual arithmetic row "
                "spacing with only subpower loss"),
        },
        "route_decision": {
            "active_next_engine": "mobius_incomplete_prime_row_covariance",
            "sleep_or_reservoir": [
                "q286 active-character finite receipts",
                "q286 componentwise finite envelopes",
                "balanced semiprime signed-total route until a T_kappa lower bound exists",
                "generic cofactor averaging source plug-ins",
                "large-modulus bare exponent matches",
            ],
            "why_this_changes_next_action": (
                "The next work should not tighten .125/.126/.13 or add "
                "another finite q286 horizon.  It should either prove or "
                "falsify the Mobius incomplete-row covariance boundary "
                "operator, because that is a universal analytical estimate "
                "with an explicit obstruction and benchmark."),
        },
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

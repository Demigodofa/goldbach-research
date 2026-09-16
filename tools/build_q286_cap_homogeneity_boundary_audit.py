"""Audit the zero-mass boundary for q286 per-modulus cap targets.

The cap-sensitivity audit found useful finite constants for one-sided
per-modulus adverse control.  This audit prevents a logical over-promotion:
relative caps of the form max(0,-U_d) <= k*T_N are homogeneous and remain true
on zero-support rows, so they cannot by themselves prove Goldbach.  The
standalone bridge remains the strict raw gap or direct raw witness.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAP = Path("evidence/q286-one-sided-cap-sensitivity-audit.json")
RAW_LEDGER = Path("evidence/q286-raw-sum-expansion-ledger.json")
STRICT_HOLD = Path("evidence/q286-wbss-strict-raw-gap-analytic-hold.json")
OUT = Path("evidence/q286-cap-homogeneity-boundary-audit.json")
NOTE = Path("notes/q286-cap-homogeneity-boundary-audit.md")


def load(path: Path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def build_receipt():
    cap = load(CAP)
    ledger = load(RAW_LEDGER)
    strict_hold = load(STRICT_HOLD)
    window = cap["uniform_cap_window"]
    cap_rows = {
        str(row["cap"]): row for row in cap["cap_sensitivity"]
    }
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q286_cap_homogeneity_boundary",
        "source_receipts": {
            "one_sided_cap_sensitivity": str(CAP),
            "raw_sum_expansion_ledger": str(RAW_LEDGER),
            "strict_raw_gap_analytic_hold": str(STRICT_HOLD),
        },
        "question": (
            "Does a universal per-modulus cap such as max(0,-U_d)<=k*T_N "
            "cross the zero-mass barrier, or is it only a conditional "
            "homogeneous estimate?"),
        "cap_window_inherited": {
            "observed_floor": window[
                "observed_uniform_cap_floor_inclusive"],
            "strict_equal_cap_ceiling": window[
                "strict_equal_cap_theorem_ceiling_exclusive"],
            "finite_fit_examples": {
                ".125": cap_rows["0.125"],
                ".126": cap_rows["0.126"],
                ".13": cap_rows["0.13"],
            },
        },
        "logical_forms": {
            "normalized_cap": {
                "statement": (
                    "max(0,-E_d(N)) <= k for each d, with E_d=U_d/T_N."),
                "zero_mass_status": (
                    "undefined or conditional, because E_d is normalized by "
                    "T_N or mu_N."),
                "classification": "conditional_distribution_estimate",
                "bridge_status": "not_standalone_goldbach_bridge",
            },
            "raw_homogeneous_cap": {
                "statement": (
                    "max(0,-U_d(N)) <= k*T_N for each d, with sum_d k_d < "
                    "M(a)."),
                "zero_mass_status": (
                    "true but non-creative at T_N=0: both sides of every "
                    "component cap are zero, and A_raw_-(N)<L_raw(N) becomes "
                    "0<0, which does not follow."),
                "classification": "homogeneous_cap_control",
                "bridge_status": (
                    "useful only after positive mass, or as a component in a "
                    "separate proof of the strict raw gap"),
            },
            "strict_raw_gap": {
                "statement": "A_raw_-(N) < L_raw(N).",
                "zero_mass_status": (
                    "false at T_N=0 because both sides are zero; a proof of "
                    "this strict statement would force support."),
                "classification": "standalone_noncircular_theorem_shape",
                "bridge_status": "still_unproved",
            },
            "direct_raw_witness": {
                "statement": "W_phi(N)>0.",
                "zero_mass_status": (
                    "false at zero support because the raw witness sum is "
                    "empty and equals zero."),
                "classification": "standalone_noncircular_theorem_shape",
                "bridge_status": "still_unproved",
            },
            "positive_mass_plus_caps": {
                "statement": (
                    "Prove T_N>=P(N)>0, then prove homogeneous or normalized "
                    "one-sided caps whose sum is below M(a)."),
                "zero_mass_status": (
                    "crosses the barrier only through the independent "
                    "positive-mass theorem."),
                "classification": "two_theorem_bridge",
                "bridge_status": "unproved_and_mass_input_is_goldbach_strength",
            },
        },
        "decision_table": [
            {
                "route": "finite caps .125/.126/.13",
                "decision": "calibration_only",
                "reason": cap["interpretation_of_125_126_13"][
                    "proof_boundary"],
            },
            {
                "route": "universal homogeneous cap max(0,-U_d)<=k*T_N",
                "decision": "not_standalone",
                "reason": (
                    "It is compatible with T_N=0 and therefore cannot by "
                    "itself imply a strict positive raw quantity."),
            },
            {
                "route": "strict raw adverse gap",
                "decision": "standalone_target",
                "reason": ledger["logical_implication"][
                    "noncircular_conclusion"],
            },
            {
                "route": "positive mass plus cap control",
                "decision": "two_theorem_bridge",
                "reason": strict_hold["decision"],
            },
        ],
        "route_correction": {
            "cap_sensitivity_still_useful": True,
            "corrected_next_obligation": (
                "Either prove the strict raw gap A_raw_-(N)<L_raw(N) "
                "directly, prove W_phi(N)>0 directly, or explicitly label "
                "the cap route as positive-mass plus one-sided projection "
                "control.  Do not present homogeneous caps alone as a "
                "Goldbach-yielding bridge."),
            "what_changed": (
                "The cap window remains a useful finite target selector, but "
                "its theorem form must not silently normalize by T_N or rely "
                "on T_N>0."),
        },
        "decision": (
            "Universal per-modulus caps remain useful theorem-shaping data, "
            "but a homogeneous cap max(0,-U_d)<=k*T_N is not a standalone "
            "Goldbach bridge.  At zero support the cap is true while the "
            "strict raw gap is false.  The cap route must therefore be "
            "labeled either as a component of a direct strict raw-gap proof "
            "or as a two-theorem package with independent positive mass."),
        "finite_logic_audit_only": True,
        "homogeneous_cap_standalone_bridge_proved": False,
        "per_modulus_supremum_theorem_proved": False,
        "positive_mass_theorem_proved": False,
        "raw_adverse_envelope_theorem_proved": False,
        "raw_witness_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    forms = receipt["logical_forms"]
    lines = [
        "# q286 cap homogeneity boundary audit",
        "",
        "## Question",
        "",
        receipt["question"],
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_q286_cap_homogeneity_boundary_audit.py",
        "evidence/q286-cap-homogeneity-boundary-audit.json",
        "```",
        "",
        "## Result",
        "",
        "The cap-sensitivity window remains useful, but the theorem form matters.",
        "",
        "```text",
        f"observed cap floor:        {receipt['cap_window_inherited']['observed_floor']}",
        f"strict equal-cap ceiling:  {receipt['cap_window_inherited']['strict_equal_cap_ceiling']}",
        "```",
        "",
        "A normalized cap",
        "",
        "```text",
        forms["normalized_cap"]["statement"],
        "```",
        "",
        "is conditional on existing mass.  A raw homogeneous cap",
        "",
        "```text",
        forms["raw_homogeneous_cap"]["statement"],
        "```",
        "",
        "is well-defined at zero support, but that is exactly the problem: at",
        "`T_N=0` every component cap reads `0<=0`, while the needed strict gap",
        "`A_raw_-(N)<L_raw(N)` reads `0<0` and does not follow.",
        "",
        "The standalone non-circular targets remain",
        "",
        "```text",
        forms["strict_raw_gap"]["statement"],
        forms["direct_raw_witness"]["statement"],
        "```",
        "",
        "or else an explicitly labeled two-theorem bridge: first prove positive",
        "strict-central mass, then apply cap/control estimates.",
        "",
        "## Decision",
        "",
        receipt["decision"],
        "",
        "This is a logic-boundary audit only.  It proves no homogeneous cap",
        "bridge, per-modulus supremum theorem, positive-mass theorem, raw",
        "adverse-envelope theorem, strict-central Goldbach theorem, or Goldbach",
        "proof.",
        "",
    ]
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
        "homogeneous_cap_standalone_bridge_proved": (
            receipt["homogeneous_cap_standalone_bridge_proved"]),
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

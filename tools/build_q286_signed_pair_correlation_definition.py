"""Build the q286 signed pair-correlation theorem definition.

The AP-bound and L1-uniformity routes failed because they controlled the wrong
object.  This receipt freezes the actual operator that must be controlled:
the reflected strict-central binary-prime residue measure modulo 10010 pushed
through the q286 first-three and full-action coefficient functionals.

It is a definition/proof-obligation artifact, not a proof.
"""

from __future__ import annotations

import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evidence" / "q286-signed-pair-correlation-definition.json"
PERIOD = 10010
MODULUS = 286
TAIL_THRESHOLD = 0.3
SELECTED_TARGETS = (
    14138,
    14996,
    94856,
    1222142,
    1240888,
    1242118,
    1379072,
)

sys.path.insert(0, str(ROOT))

from tools.build_q286_cone_duality_l1_uniformity_candidate import (  # noqa: E402
    combined_fixed_strict_central_coefficient_receipt,
    orbit_coefficients,
    period_full_unit_coefficients,
    prepare_support_context,
    q286_first_three_unit_coefficients,
)


PRIOR_EVIDENCE = {
    "l1_cone": ROOT / "evidence" / "q286-cone-duality-l1-uniformity-candidate.json",
    "ap_comparison": ROOT / "evidence" / "q286-l1-uniformity-ap-bound-comparison.json",
    "mass_landing": ROOT / "evidence" / "q286-first-three-mass-landing-obligation.json",
}


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def finite_summary(values):
    finite = tuple(float(value) for value in values if math.isfinite(value))
    if not finite:
        return {"count": 0, "minimum": None, "maximum": None, "mean": None}
    return {
        "count": len(finite),
        "minimum": min(finite),
        "maximum": max(finite),
        "mean": math.fsum(finite) / len(finite),
    }


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def operator_row(target_residue, context, full_coefficients,
                 first_three_coefficients):
    orbit_data = orbit_coefficients(
        target_residue, context, full_coefficients, first_three_coefficients)
    uniform = orbit_data["uniform_orbit_mass"]
    first_three = orbit_data["first_three_coefficients"]
    full = orbit_data["full_coefficients"]
    full_uniform = float(np.dot(full, uniform))
    first_three_uniform = float(np.dot(first_three, uniform))
    centered_full = full - full_uniform
    negative_mask = first_three < 0
    positive_mask = first_three > 0
    return {
        "target_residue": int(target_residue),
        "target_mod_286": int(target_residue % MODULUS),
        "admissible_unit_count": len(orbit_data["admissible_units"]),
        "reflection_orbit_count": len(orbit_data["orbits"]),
        "uniform_first_three_to_principal": first_three_uniform,
        "uniform_full_action_to_principal": full_uniform,
        "bad_branch_centered_inequalities": {
            "first_three_centered_action_at_most": -TAIL_THRESHOLD,
            "full_centered_action_at_most": -full_uniform,
            "meaning": (
                "For nu=mu-u_a with sum nu=0, the bad branch is "
                "<nu,gamma_F3_a><=-0.3 and "
                "<nu,gamma_full_a><=-uniform_full_a."),
        },
        "first_three_coefficient_summary": finite_summary(first_three),
        "full_coefficient_summary": finite_summary(full),
        "centered_full_coefficient_summary": finite_summary(centered_full),
        "negative_first_three_orbit_count": int(np.sum(negative_mask)),
        "positive_first_three_orbit_count": int(np.sum(positive_mask)),
        "zero_first_three_orbit_count": int(
            len(first_three) - np.sum(negative_mask) - np.sum(positive_mask)),
        "negative_first_three_uniform_mass": float(np.sum(uniform[negative_mask])),
        "positive_first_three_uniform_mass": float(np.sum(uniform[positive_mask])),
        "coefficient_cosine_first_three_full_centered": cosine(
            first_three, centered_full),
        "minimum_first_three_coefficient": float(np.min(first_three)),
        "maximum_first_three_coefficient": float(np.max(first_three)),
        "minimum_full_coefficient": float(np.min(full)),
        "maximum_full_coefficient": float(np.max(full)),
    }


def cosine(a, b):
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return None
    return float(np.dot(a, b) / denom)


def main():
    prior = {key: load_json(path) for key, path in PRIOR_EVIDENCE.items()}
    residues = tuple(dict.fromkeys(target % PERIOD for target in SELECTED_TARGETS))
    context = prepare_support_context()
    context["coefficient"] = combined_fixed_strict_central_coefficient_receipt()
    full_coefficients = period_full_unit_coefficients(context)
    first_three_coefficients = q286_first_three_unit_coefficients(context)
    rows = [
        operator_row(
            residue, context, full_coefficients, first_three_coefficients)
        for residue in residues
    ]

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "definition and proof-obligation artifact only; it proves no "
            "signed pair-correlation estimate, no binary "
            "Goldbach-in-progressions theorem, no q286 threshold theorem, and "
            "no Goldbach theorem."),
        "creative_tool_state": {
            "pursue_curiosity": (
                "changed-under-evidence: the repeated audit loop exposed a "
                "geometry mismatch rather than a missing larger sample."),
            "inventive_synthesis": {
                "candidate": (
                    "Replace residue-uniformity cones with a signed "
                    "pair-correlation cone on the exact q286 operator image."),
                "novelty_label": "new-to-this-task",
                "falsifier": (
                    "Any proposed non-post-hoc cone is refuted if an LP finds "
                    "a reflected nonnegative synthetic measure satisfying the "
                    "cone and both bad-branch inequalities."),
            },
            "preserve_hypotheses": (
                "The AP and L1 components remain useful background, but the "
                "unchanged claim that they close the q10010 binary cone is "
                "blocked by the BMOR comparison."),
        },
        "definition": {
            "period": PERIOD,
            "q286_modulus": MODULUS,
            "target_residue": "a = N mod 10010",
            "admissible_support": (
                "A_a={r in (Z/10010Z)^*: gcd(a-r,10010)=1}"),
            "strict_central_weight": (
                "Strict-central W_N(r)=sum log(p)log(N-p) over primes "
                "N/3<p<2N/3 with p=r mod 10010"),
            "normalized_measure": "mu_N(r)=W_N(r)/sum_s W_N(s)",
            "uniform_measure": "u_a(r)=1/|A_a| on admissible residues",
            "centered_discrepancy": "nu_N=mu_N-u_a",
            "operators": {
                "first_three": (
                    "F3_a(mu)=<mu,gamma_F3_a>; by construction "
                    "<u_a,gamma_F3_a> is zero up to floating error."),
                "full": (
                    "A_a(mu)=<mu,gamma_full_a>; q286 closure on this lane "
                    "requires A_a(mu_N)>0."),
                "bad_branch": (
                    "F3_a(mu)<=-0.3 and A_a(mu)<=0, equivalently "
                    "<nu,gamma_F3_a><=-0.3 and "
                    "<nu,gamma_full_a><=-<u_a,gamma_full_a>."),
            },
        },
        "prior_evidence_digest": {
            "l1_nearest_bad_radius": (
                prior["l1_cone"]["summary"]["minimum_bad_l1_summary"]),
            "actual_l1_summary": prior["l1_cone"]["summary"]["actual_l1_summary"],
            "bmor_q10010_theta_probability_l1_proxy": next(
                row for row in prior["ap_comparison"]["modulus_rows"]
                if row["q"] == PERIOD
            )["theta_probability_l1_proxy_at_x_theta"],
            "bmor_q10010_pi_probability_l1_proxy": next(
                row for row in prior["ap_comparison"]["modulus_rows"]
                if row["q"] == PERIOD
            )["pi_probability_l1_proxy_at_x_pi"],
            "mass_landing_obligation": (
                prior["mass_landing"]["exact_pointwise_obligation"]),
        },
        "selected_operator_rows": rows,
        "summary": {
            "selected_residue_count": len(rows),
            "uniform_first_three_abs_error_summary": finite_summary(
                abs(row["uniform_first_three_to_principal"]) for row in rows),
            "uniform_full_action_summary": finite_summary(
                row["uniform_full_action_to_principal"] for row in rows),
            "first_three_full_centered_cosine_summary": finite_summary(
                row["coefficient_cosine_first_three_full_centered"]
                for row in rows
                if row["coefficient_cosine_first_three_full_centered"] is not None),
            "negative_first_three_uniform_mass_summary": finite_summary(
                row["negative_first_three_uniform_mass"] for row in rows),
            "positive_first_three_uniform_mass_summary": finite_summary(
                row["positive_first_three_uniform_mass"] for row in rows),
        },
        "decision": (
            "The next proof object is the signed pair-correlation theorem for "
            "nu_N against gamma_F3_a and gamma_full_a.  Further audits are "
            "useful only if they test a predeclared cone that implies the two "
            "bad-branch inequalities cannot hold together."),
        "next_obligation": (
            "Choose one non-post-hoc cone family for nu_N, preferably a "
            "signed moment/covariance inequality or a binary "
            "Goldbach-in-progressions estimate, then run the LP falsifier "
            "against these frozen operator rows."),
        "goldbach_proved": False,
    }
    OUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

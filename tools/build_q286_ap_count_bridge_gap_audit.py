"""Audit whether q286 AP prime-count bounds alone bridge to prime pairs.

BMOR gives explicit lower bounds for primes in each reduced residue class
modulo q=286.  This receipt asks a much narrower combinatorial question:
could those one-dimensional AP count floors, with no correlation input, force
an intersection between primes p in one residue class and reflected primes
N-p in the complementary class?

The answer is no in the valid BMOR ranges.  This does not weaken BMOR.  It
identifies the missing bridge as a binary convolution / residue-correlation
estimate rather than another raw AP count.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path

import mpmath as mp


ROOT = Path(__file__).resolve().parents[1]
LOCAL_SINGULAR_SOURCE = (
    ROOT / "evidence" / "q286-lp-cone-local-singular-audit.json")
OUT = ROOT / "evidence" / "q286-ap-count-bridge-gap-audit.json"

Q = 286
PHI_Q = 120
BMOR_C_PI = 0.0008772
BMOR_X_PI = 86_891_851
BMOR_C_PSI = 0.0008379
BMOR_X_PSI = 85_882_271
BMOR_C_THETA = 0.0008411
BMOR_X_THETA = 85_881_413
COROLLARY_1_6_THRESHOLD = 50 * Q * Q
TOLERANCE = 1e-12


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_ready(item) for item in value]
    if isinstance(value, mp.mpf):
        return float(value)
    return value


def li(x):
    return mp.li(mp.mpf(x))


def residue_slot_count_upper(x):
    """Largest possible count of integers <= x in one residue class mod q."""
    return math.ceil(float(x) / Q)


def corollary_lower_count(x):
    return mp.mpf(x) / (PHI_Q * mp.log(x))


def bmor_pi_lower_count(x):
    x = mp.mpf(x)
    return li(x) / PHI_Q - BMOR_C_PI * x / mp.log(x)


def bmor_pi_upper_count(x):
    x = mp.mpf(x)
    return li(x) / PHI_Q + BMOR_C_PI * x / mp.log(x)


def count_only_row(x, lower_source):
    x = mp.mpf(x)
    slot = residue_slot_count_upper(x)
    if lower_source == "BMOR Theorem 1.3 q-specific pi":
        lower = bmor_pi_lower_count(x)
        upper = bmor_pi_upper_count(x)
        valid_from = BMOR_X_PI
    elif lower_source == "BMOR Corollary 1.6 simple pi lower":
        lower = corollary_lower_count(x)
        upper = (
            mp.mpf(x) / (PHI_Q * mp.log(x))
            * (1 + mp.mpf("2.5") / mp.log(x)))
        valid_from = COROLLARY_1_6_THRESHOLD
    else:
        raise ValueError(lower_source)
    reflected_pair_floor = int(mp.ceil(lower))
    forced_by_pigeonhole = 2 * lower > slot
    integer_disjoint_model_exists = 2 * reflected_pair_floor <= slot
    return {
        "x": int(x),
        "valid_from": int(valid_from),
        "source": lower_source,
        "residue_slot_count_upper": int(slot),
        "lower_count_per_reduced_residue": float(lower),
        "upper_count_per_reduced_residue": float(upper),
        "integer_floor_used_for_countermodel": reflected_pair_floor,
        "two_marginal_floor_sum": int(2 * reflected_pair_floor),
        "two_lower_bounds_to_slot_ratio": float((2 * lower) / slot),
        "slot_minus_two_integer_floors": int(slot - 2 * reflected_pair_floor),
        "pigeonhole_would_force_intersection": bool(forced_by_pigeonhole),
        "disjoint_reflected_sets_can_satisfy_marginal_floor": bool(
            integer_disjoint_model_exists),
    }


def corollary_ratio_threshold_x():
    # 2*x/(phi log x) > x/q reduces to log x < 2q/phi.
    return mp.e ** (mp.mpf(2 * Q) / PHI_Q)


def sampled_rows():
    xs = (
        COROLLARY_1_6_THRESHOLD,
        BMOR_X_PI,
        10**9,
        10**12,
        10**16,
        10**20,
        10**30,
    )
    rows = []
    for x in xs:
        if x >= COROLLARY_1_6_THRESHOLD:
            rows.append(count_only_row(
                x, "BMOR Corollary 1.6 simple pi lower"))
        if x >= BMOR_X_PI:
            rows.append(count_only_row(
                x, "BMOR Theorem 1.3 q-specific pi"))
    return tuple(rows)


def logspace_max_bmor_ratio():
    rows = []
    start_log = mp.log(BMOR_X_PI)
    stop_log = mp.log(mp.mpf("1e40"))
    for index in range(201):
        t = start_log + (stop_log - start_log) * index / 200
        x = mp.e ** t
        row = count_only_row(int(mp.floor(x)), "BMOR Theorem 1.3 q-specific pi")
        rows.append(row)
    return max(rows, key=lambda row: row["two_lower_bounds_to_slot_ratio"])


def main():
    mp.mp.dps = 80
    local_singular = json.loads(
        LOCAL_SINGULAR_SOURCE.read_text(encoding="utf-8"))
    rows = sampled_rows()
    cor_threshold = corollary_ratio_threshold_x()
    max_bmor_sample = logspace_max_bmor_ratio()
    valid_rows = tuple(
        row for row in rows
        if row["disjoint_reflected_sets_can_satisfy_marginal_floor"])

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_local_singular_audit": str(
            LOCAL_SINGULAR_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite combinatorial bridge-gap audit only; BMOR AP count "
            "bounds are external source-backed input, but this receipt proves "
            "no binary Goldbach-in-progressions theorem, no 17-channel "
            "functional bound, and no Goldbach theorem."),
        "candidate": (
            "Use explicit AP prime-count lower bounds for q=286 as a "
            "pigeonhole bridge into the q286 17-channel LP/rank-1 object."),
        "mechanism": (
            "For a fixed residue pair r and N-r, AP counts provide marginal "
            "lower bounds for two subsets of the same residue-slot universe. "
            "A count-only bridge can force a prime pair only when the two "
            "marginal lower bounds are too large to be disjoint."),
        "prediction": (
            "If raw AP counts are strong enough, 2*lower_count_per_residue "
            "will exceed the largest residue-slot count in the valid BMOR "
            "range."),
        "falsifier": (
            "If 2*ceil(lower_count_per_residue) <= slot_count throughout the "
            "valid ranges, then disjoint reflected subsets can satisfy the "
            "AP marginals while containing no Goldbach pair in that residue "
            "pair.  Raw AP counts alone cannot be the bridge."),
        "novelty_label": "new-to-this-task",
        "modulus": Q,
        "phi_q": PHI_Q,
        "bmor_constants": {
            "c_pi": BMOR_C_PI,
            "x_pi": BMOR_X_PI,
            "c_psi": BMOR_C_PSI,
            "x_psi": BMOR_X_PSI,
            "c_theta": BMOR_C_THETA,
            "x_theta": BMOR_X_THETA,
            "source_data_page": "https://www.nt.math.ubc.ca/BeMaObRe/",
        },
        "corollary_1_6": {
            "simple_pi_lower_valid_from": COROLLARY_1_6_THRESHOLD,
            "formula": "pi(x;q,a) > x/(phi(q)*log(x)) for x >= 50*q^2",
            "count_only_pigeonhole_ratio_formula": (
                "2q/(phi(q)*log(x))"),
            "ratio_exceeds_1_only_for_x_less_than": cor_threshold,
            "ratio_exceeds_1_threshold_below_valid_range": bool(
                cor_threshold < COROLLARY_1_6_THRESHOLD),
        },
        "sampled_count_only_rows": rows,
        "bmor_logspace_sample": {
            "range": [BMOR_X_PI, "1e40"],
            "sample_count": 201,
            "maximum_sampled_ratio_row": max_bmor_sample,
            "maximum_sampled_ratio_still_below_one": (
                max_bmor_sample["two_lower_bounds_to_slot_ratio"] < 1.0),
        },
        "local_singular_context": {
            "local_lp_negative_count": local_singular["local_lp_negative_count"],
            "local_lp_zero_residues": local_singular["local_lp_zero_residues"],
            "far_empirical_lp_vs_local_lp_pearson": local_singular[
                "far_empirical_summary"]["empirical_lp_vs_local_lp_pearson"],
            "far_empirical_lp_vs_local_lp_spearman": local_singular[
                "far_empirical_summary"]["empirical_lp_vs_local_lp_spearman"],
        },
        "decision": (
            "Demote the raw AP-count pigeonhole bridge.  BMOR remains useful "
            "two-sided AP-count input, but it is too sparse to force a "
            "reflected residue-pair intersection by counts alone in its valid "
            "q=286 range."),
        "what_survives": (
            "The AP constants are valid external endpoint data for future "
            "work.  A successful bridge must use binary convolution, character "
            "sum correlation, dispersion, or another relation between p and "
            "N-p; marginal AP occupancy alone is insufficient."),
        "count_only_bridge_falsified": bool(len(valid_rows) == len(rows)),
        "ap_count_to_17_channel_bridge_proved": False,
        "binary_goldbach_in_progressions_theorem_proved": False,
        "rank1_residual_bound_theorem_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }
    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

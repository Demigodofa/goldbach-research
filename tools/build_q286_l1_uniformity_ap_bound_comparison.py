"""Compare BMOR arithmetic-progression bounds with q286 L1 cone radii.

This receipt answers a narrow pivot question: can published fixed-modulus
prime-in-AP bounds plausibly supply the L1 radius required by the q286
cone-duality candidate?

The comparison is deliberately conservative.  It treats the BMOR per-residue
error constants as a one-dimensional marginal probability L1 proxy.  That is
not a proof for the binary strict-central Goldbach residue measure, so a
successful proxy would still need a bridge theorem; a failed proxy is enough to
demote the blunt L1 route as the main strategy.
"""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
import sys
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
L1_CANDIDATE = ROOT / "evidence" / "q286-cone-duality-l1-uniformity-candidate.json"
OUT = ROOT / "evidence" / "q286-l1-uniformity-ap-bound-comparison.json"

BMOR_BASE = "http://www.nt.math.ubc.ca/BeMaObRe"
TABLES = {
    "constants": "c-psi-theta-pi/c_all_rounded.txt",
    "thresholds": "x-psi-theta-pi/x0-all-xm-xe.txt",
}
MODULI = (143, 286, 10010)


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def e_float(value):
    return float(value.replace("D", "E"))


def fetch_table(path):
    url = f"{BMOR_BASE}/{path}"
    with urllib.request.urlopen(url, timeout=60) as response:
        data = response.read()
    text = data.decode("utf-8", errors="replace")
    rows = {}
    headers = []
    for line in text.splitlines():
        if line.startswith("#"):
            headers.append(line)
            continue
        parts = line.split()
        if parts and parts[0].isdigit():
            q = int(parts[0])
            if q in MODULI:
                rows[q] = parts
    return {
        "url": url,
        "sha256": hashlib.sha256(data).hexdigest(),
        "headers": headers[:3],
        "rows": {str(q): rows.get(q) for q in MODULI},
    }


def phi(n):
    result = n
    remaining = n
    factor = 2
    while factor * factor <= remaining:
        if remaining % factor == 0:
            result -= result // factor
            while remaining % factor == 0:
                remaining //= factor
        factor += 1 if factor == 2 else 2
    if remaining > 1:
        result -= result // remaining
    return result


def load_l1_radii():
    receipt = json.loads(L1_CANDIDATE.read_text(encoding="utf-8"))
    summary = receipt["summary"]["minimum_bad_l1_summary"]
    return {
        "minimum": float(summary["minimum"]),
        "mean": float(summary["mean"]),
        "maximum": float(summary["maximum"]),
    }


def probability_l1_proxy(modulus, constant, x_start):
    """Union-bound proxy for normalized one-dimensional residue mass.

    BMOR gives |count_a-main_a| <= c*x/log(x) for theta and
    |pi_a-main_a| <= c*x/log(x)^2 for pi.  After normalizing by total mass
    x (theta) or x/log(x) (pi), both lead to the same first-order proxy
    phi(q)*c/log(x).  This is a marginal proxy, not a binary pair theorem.
    """

    return phi(modulus) * constant / math.log(x_start)


def threshold_for_radius(modulus, constant, x_start, radius):
    formula_threshold = math.exp(phi(modulus) * constant / radius)
    return max(float(x_start), formula_threshold)


def build_modulus_rows(constants_table, thresholds_table, radii):
    rows = []
    for q in MODULI:
        constant_parts = constants_table["rows"][str(q)]
        threshold_parts = thresholds_table["rows"][str(q)]
        if constant_parts is None or threshold_parts is None:
            raise RuntimeError(f"BMOR table row missing for q={q}")

        c_theta = e_float(constant_parts[5])
        c_pi = e_float(constant_parts[6])
        x_theta = e_float(threshold_parts[2])
        x_pi = e_float(threshold_parts[4])
        row = {
            "q": q,
            "phi_q": phi(q),
            "bmor_constants_row": constant_parts,
            "bmor_thresholds_row": threshold_parts,
            "c_theta": c_theta,
            "c_pi": c_pi,
            "x_theta": x_theta,
            "x_pi": x_pi,
            "theta_probability_l1_proxy_at_x_theta": probability_l1_proxy(
                q, c_theta, x_theta),
            "pi_probability_l1_proxy_at_x_pi": probability_l1_proxy(
                q, c_pi, x_pi),
            "theta_x_needed_for_l1_radius": {
                name: threshold_for_radius(q, c_theta, x_theta, radius)
                for name, radius in radii.items()
            },
            "pi_x_needed_for_l1_radius": {
                name: threshold_for_radius(q, c_pi, x_pi, radius)
                for name, radius in radii.items()
            },
        }
        rows.append(row)
    return rows


def main():
    if not L1_CANDIDATE.exists():
        raise FileNotFoundError(L1_CANDIDATE)
    tables = {name: fetch_table(path) for name, path in TABLES.items()}
    radii = load_l1_radii()
    rows = build_modulus_rows(tables["constants"], tables["thresholds"], radii)
    q10010 = next(row for row in rows if row["q"] == 10010)
    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status_boundary": (
            "source-backed AP-bound comparison only; it proves no AP "
            "uniformity theorem for the binary strict-central measure, no "
            "signed prime-correlation theorem, no q286 threshold theorem, and "
            "no Goldbach theorem."),
        "source": {
            "paper": (
                "Bennett, Martin, O'Bryant, Rechnitzer, Explicit bounds for "
                "primes in arithmetic progressions, Illinois J. Math. 62 "
                "(2018), 427-532; arXiv:1802.00085."),
            "data_index": BMOR_BASE + "/",
            "tables": tables,
        },
        "l1_candidate_source": str(L1_CANDIDATE.relative_to(ROOT)),
        "l1_bad_radius_summary": radii,
        "comparison_model": (
            "For a one-dimensional AP count bound at modulus q, normalize the "
            "per-class BMOR error by total prime mass and union-bound over "
            "phi(q) reduced classes, giving the proxy phi(q)*c/log(x).  This "
            "is only a marginal residue-distribution proxy; the q286 cone "
            "uses a binary reflected strict-central prime-pair measure modulo "
            "10010."),
        "modulus_rows": rows,
        "decision": (
            "BMOR directly supplies strong fixed-modulus AP count bounds, but "
            "not the needed binary strict-central L1 cone theorem.  At the "
            "assembled period q=10010, the marginal proxy at BMOR validity "
            "thresholds is about 0.15, larger than every computed nearest-bad "
            "L1 radius.  Closing even the minimum radius with this blunt "
            "one-dimensional union-bound proxy would require x around "
            f"{q10010['pi_x_needed_for_l1_radius']['minimum']:.3e} for pi "
            "or "
            f"{q10010['theta_x_needed_for_l1_radius']['minimum']:.3e} for "
            "theta, before paying any binary-pair convolution cost.  Therefore "
            "this does not close the route; it redirects the strategy toward "
            "coefficient-sensitive cones or a genuine Goldbach-in-progressions "
            "estimate for the signed functionals."),
        "next_obligation": (
            "Do not run more label-only or blunt L1 audits as the main lane. "
            "Define the actual operator/cone: coefficient-sensitive signed "
            "moments, q286 landing inequalities, or a binary in-progressions "
            "theorem that controls the same reflected pair measure."),
        "goldbach_proved": False,
    }
    OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    sys.exit(main())

"""Extract the coefficient-aligned q286-WBSS signed discrepancy problem.

The L1-budget obstruction audit showed that total variation from the local
uniform orbit measure is far too large to be the right proof bridge.  This
receipt turns that negative answer into the next exact problem:

    lambda_phi(N) = -<mu_N-u_a, phi_a-mean_u(phi_a)> / mean_u(phi_a) < 1.

Because mean_u(phi_a)>0 in the checked q286-WBSS rows, this scalar inequality
is equivalent to positive signed expectation <mu_N,phi_a> > 0.  It is not a
new theorem; it is the smallest coefficient-aligned inequality a proof must
obtain from source-backed binary-prime correlation input.

Finite problem-definition receipt only.  It proves no signed discrepancy
theorem, q286 threshold theorem, strict-central Goldbach theorem, or Goldbach
theorem.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = EVIDENCE / "q286-wbss-l1-budget-obstruction-audit.json"
OUT = EVIDENCE / "q286-wbss-signed-discrepancy-problem.json"
TOLERANCE = 1e-12


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def load_source():
    return json.loads(SOURCE.read_text(encoding="utf-8"))


def finite_summary(values):
    vals = [float(value) for value in values]
    return {
        "count": len(vals),
        "minimum": min(vals),
        "mean": sum(vals) / len(vals),
        "maximum": max(vals),
    }


def row_record(row, key):
    stats = row[key]
    mean = float(stats["uniform_mean"])
    signed_error = float(stats["signed_error_from_uniform_mean"])
    actual = float(stats["actual_expectation"])
    l1_load = float(stats["actual_l1_to_budget_ratio"])
    if mean <= TOLERANCE:
        raise ValueError(
            f"{key} row {row['target']} has nonpositive local mean {mean}"
        )
    lambda_phi = -signed_error / mean
    return {
        "target": int(row["target"]),
        "target_residue": int(row["target_residue"]),
        "target_mod_286": int(row["target_mod_286"]),
        "block_index_after_discovery": int(row["block_index_after_discovery"]),
        "uniform_mean": mean,
        "actual_expectation": actual,
        "signed_error_from_uniform_mean": signed_error,
        "lambda_phi": float(lambda_phi),
        "anti_alignment_load": float(max(0.0, lambda_phi)),
        "positivity_margin_ratio": float(1.0 - lambda_phi),
        "actual_over_uniform_mean": float(actual / mean),
        "l1_worst_case_load": l1_load,
        "l1_load_to_actual_anti_alignment_ratio": (
            float(l1_load / max(lambda_phi, TOLERANCE))
            if lambda_phi > 0.0 else None
        ),
        "passes_signed_problem_threshold": bool(lambda_phi < 1.0 - TOLERANCE),
        "would_pass_l1_budget": bool(stats["actual_l1_within_sufficient_budget"]),
    }


def summarize(records):
    tight = min(records, key=lambda row: row["positivity_margin_ratio"])
    largest_l1 = max(records, key=lambda row: row["l1_worst_case_load"])
    anti_records = [row for row in records if row["lambda_phi"] > 0.0]
    return {
        "row_count": len(records),
        "signed_threshold_pass_count": sum(
            row["passes_signed_problem_threshold"] for row in records),
        "l1_budget_pass_count": sum(row["would_pass_l1_budget"]
                                    for row in records),
        "lambda_phi_summary": finite_summary(
            row["lambda_phi"] for row in records),
        "anti_alignment_load_summary": finite_summary(
            row["anti_alignment_load"] for row in records),
        "positivity_margin_ratio_summary": finite_summary(
            row["positivity_margin_ratio"] for row in records),
        "actual_over_uniform_mean_summary": finite_summary(
            row["actual_over_uniform_mean"] for row in records),
        "l1_worst_case_load_summary": finite_summary(
            row["l1_worst_case_load"] for row in records),
        "l1_to_anti_alignment_ratio_summary": finite_summary(
            row["l1_load_to_actual_anti_alignment_ratio"]
            for row in anti_records),
        "tightest_signed_row": tight,
        "largest_l1_worst_case_row": largest_l1,
    }


def build_family(rows, key):
    records = [row_record(row, key) for row in rows]
    return {
        "definition": {
            "coefficient_family": key,
            "local_mean": "m_a = <u_a, phi_a>",
            "centered_discrepancy": (
                "delta_N = mu_N-u_a, with phi_a centered by m_a"),
            "lambda_phi": (
                "-<delta_N, phi_a-m_a> / m_a"),
            "positivity_equivalence": (
                "<mu_N,phi_a> > 0 iff lambda_phi(N) < 1, because m_a>0"),
        },
        "summary": summarize(records),
        "rows": records,
    }


def build_receipt():
    source = load_source()
    rows = [
        row for row in source["target_rows"]
        if row["block_index_after_discovery"] >= 1
    ]
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "l1_budget_obstruction": str(SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite q286-WBSS signed-discrepancy problem definition only; "
            "no signed discrepancy theorem, q286 threshold theorem, "
            "strict-central Goldbach theorem, or Goldbach proof"
        ),
        "goldbach_proved": False,
        "signed_discrepancy_theorem_proved": False,
        "q286_threshold_theorem_proved": False,
        "novelty_label": "new-to-this-task",
        "candidate": {
            "name": "q286-WBSS signed discrepancy problem",
            "target_bottleneck": (
                "The local main term is positive, but total-L1 uniformity "
                "requires much more distributional regularity than the "
                "checked prime-pair measures actually have."
            ),
            "mechanism": (
                "Project the binary-prime orbit discrepancy only onto the "
                "signed q286 coefficient direction that can erase the "
                "positive local mean."
            ),
            "prediction": (
                "Successful rows can have large total L1 deviation while "
                "maintaining lambda_phi(N)<1 with a small positive margin."
            ),
            "falsifier": (
                "If held-out positive rows reach lambda_phi>=1, this exact "
                "signed problem fails for the frozen coefficient family; if "
                "lambda remains below 1 but no source-backed theorem can "
                "bound it, the formulation is only an equivalent restatement."
            ),
            "smallest_test": (
                "Compute lambda_phi and compare it with the L1 worst-case "
                "load on the same post-discovery q286-WBSS rows."
            ),
        },
        "problem_statement": (
            "For each admissible target residue a, let u_a be the local "
            "uniform orbit measure, mu_N the normalized strict-central "
            "binary-prime orbit measure for even N congruent to a, and phi_a "
            "one of the frozen q286-WBSS coefficient functions with "
            "m_a=<u_a,phi_a>>0.  Prove an explicit threshold N0 and margin "
            "eta(N)>0 such that lambda_phi(N)<=1-eta(N) for every covered "
            "even N>=N0; then verify the finite remainder.  Equivalently, "
            "prove <mu_N,phi_a> > 0 directly as a signed binary-prime "
            "correlation estimate."
        ),
        "bridge_boundary": (
            "This is an answer-created problem, not a solved bridge.  The "
            "missing implication is a source-backed estimate for the signed "
            "projection <mu_N-u_a,phi_a-m_a>; without that estimate, the "
            "condition is equivalent to the positivity it names."
        ),
        "post_discovery_row_count": len(rows),
        "families": {
            "full": build_family(rows, "full"),
            "edge_beta": build_family(rows, "edge_beta"),
        },
        "decision": (
            "The q286-WBSS answer becomes a sharper problem: prove "
            "coefficient-aligned anti-correlation load lambda_phi(N)<1.  On "
            "the 196 post-discovery rows this scalar threshold passes for "
            "both full and edge-beta coefficients, while the ordinary L1 "
            "budget passes 0 rows.  Therefore the next theorem must be a "
            "signed discrepancy/correlation inequality, not total-uniformity "
            "or another static residue dictionary."
        ),
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

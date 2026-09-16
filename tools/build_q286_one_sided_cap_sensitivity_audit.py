"""Audit one-sided per-modulus adverse cap sensitivity for q286.

After the L2/adverse separation audit, the sharper theorem target is one-sided
adverse projection control.  This receipt turns the finite component envelope
into an explicit cap-sensitivity table: which uniform per-modulus constants
fit the observed horizon, which would be theorem-sufficient if proved
universally, and which are only finite calibrations.
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMPONENT = (
    Path("evidence")
    / "q286-wbss-four-modulus-component-envelope-horizon-audit.json"
)
L2_SEPARATION = (
    Path("evidence")
    / "q286-l2-vs-one-sided-adverse-separation-audit.json"
)
RAW_LEDGER = Path("evidence/q286-raw-sum-expansion-ledger.json")
OUT = Path("evidence/q286-one-sided-cap-sensitivity-audit.json")
NOTE = Path("notes/q286-one-sided-cap-sensitivity-audit.md")

MODULI = ("70", "130", "154", "286")
CAPS_TO_TEST = (0.12, 0.122, 0.125, 0.126, 0.13, 0.15, 0.175, 0.18)


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
    component = load(COMPONENT)
    l2_separation = load(L2_SEPARATION)
    ledger = load(RAW_LEDGER)

    rows = component["holdout"]["rows"]
    local_mains = [row["local_uniform_main_term"] for row in rows]
    min_local_main_row = min(rows, key=lambda row: (
        row["local_uniform_main_term"], row["target"]))
    observed_suprema = {
        d: float(component["component_adverse_suprema"][d])
        for d in MODULI
    }
    observed_sum = sum(observed_suprema.values())
    observed_max = max(observed_suprema.values())
    observed_max_modulus = max(
        MODULI, key=lambda d: (observed_suprema[d], d))
    min_local_main = min(local_mains)
    equal_cap_strict_ceiling = min_local_main / len(MODULI)
    observed_uniform_cap_floor = observed_max

    cap_rows = []
    for cap in CAPS_TO_TEST:
        observed_fit = all(value <= cap for value in observed_suprema.values())
        theorem_sufficient_equal_cap = len(MODULI) * cap < min_local_main
        cap_rows.append({
            "cap": cap,
            "observed_fit_on_232_rows": observed_fit,
            "universal_equal_cap_would_be_sufficient_if_proved": (
                theorem_sufficient_equal_cap),
            "sum_four_equal_caps": len(MODULI) * cap,
            "margin_to_min_local_main": min_local_main - len(MODULI) * cap,
            "classification": (
                "fits_finite_and_theorem_sufficient_if_universal"
                if observed_fit and theorem_sufficient_equal_cap
                else "too_strict_for_observed_horizon"
                if not observed_fit
                else "fits_finite_but_not_sufficient_as_equal_cap"),
        })

    asymmetric_slack = min_local_main - observed_sum
    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "status": "AUDIT_q286_one_sided_cap_sensitivity",
        "source_receipts": {
            "component_envelope_horizon": str(COMPONENT),
            "l2_vs_one_sided_adverse_separation": str(L2_SEPARATION),
            "raw_sum_expansion_ledger": str(RAW_LEDGER),
        },
        "question": (
            "For the one-sided q286 route, which uniform per-modulus adverse "
            "caps fit the checked component envelope, and which would be "
            "sufficient theorem targets if proved universally?"),
        "candidate": {
            "name": "uniform one-sided per-modulus adverse cap",
            "novelty_label": "new-to-this-task",
            "mechanism": (
                "Replace symmetric aggregate L2 by an upper bound on each "
                "modulus' harmful signed projected contribution.  A uniform "
                "cap k proves the component envelope whenever 4k is below "
                "the local main term."),
            "prediction": (
                "There should be a nonempty interval between the largest "
                "observed component adverse supremum and the strict "
                "equal-cap ceiling min(local_main)/4."),
            "falsifier": (
                "If the largest observed component adverse value is already "
                "at or above min(local_main)/4, then no uniform cap can both "
                "fit the finite horizon and certify the envelope."),
            "smallest_test": (
                "Compute max_d A_d^obs and min_row M(row)/4 on the 232-row "
                "component-envelope horizon, then classify selected caps."),
        },
        "component_horizon": {
            "row_count": len(rows),
            "moduli": list(MODULI),
            "component_adverse_suprema": observed_suprema,
            "component_adverse_supremum_sum": observed_sum,
            "min_local_main": min_local_main,
            "min_local_main_target": min_local_main_row["target"],
            "observed_max_component_adverse": observed_max,
            "observed_max_component_modulus": observed_max_modulus,
            "observed_sum_margin_to_min_local_main": asymmetric_slack,
        },
        "uniform_cap_window": {
            "observed_uniform_cap_floor_inclusive": (
                observed_uniform_cap_floor),
            "strict_equal_cap_theorem_ceiling_exclusive": (
                equal_cap_strict_ceiling),
            "nonempty_window": (
                observed_uniform_cap_floor < equal_cap_strict_ceiling),
            "window_width": (
                equal_cap_strict_ceiling - observed_uniform_cap_floor),
            "meaning": (
                "Any universal theorem proving every modulus adverse part "
                "is <= k with observed_floor <= k < strict_ceiling would both "
                "fit this finite horizon and imply the equal-cap component "
                "envelope on rows whose local main is at least the checked "
                "minimum.  It would still need a real universal proof and a "
                "finite remainder."),
        },
        "cap_sensitivity": cap_rows,
        "interpretation_of_125_126_13": {
            "point": (
                "For an upper-bound cap, smaller constants are stricter.  "
                "Thus .125 is stricter than .126, and both are stricter than "
                ".13."),
            "finite_horizon_result": (
                "On this 232-row component horizon, .125, .126, and .13 all "
                "fit the observed component suprema and all would be "
                "equal-cap sufficient if a universal theorem actually proved "
                "them."),
            "proof_boundary": (
                "They remain fitted finite cap candidates only.  No universal "
                "per-modulus supremum theorem or one-sided signed "
                "concentration theorem is established."),
        },
        "route_decision": {
            "uniform_cap_route_survives_finite_horizon": True,
            "preferred_next_obligation": (
                "Try to prove a universal one-sided per-modulus adverse cap, "
                "or replace the uniform cap by an asymmetric component bound "
                "whose sum stays below local main."),
            "why_this_is_sharper_than_l2": l2_separation["route_decision"][
                "why"],
            "acceptance_condition": ledger["acceptance_condition"][
                "required_universal_estimate"],
        },
        "decision": (
            "The one-sided per-modulus cap route has a nonempty finite window. "
            "The largest observed component adverse supremum is about "
            f"{observed_max}, while the strict equal-cap ceiling from the "
            f"minimum checked local main is about {equal_cap_strict_ceiling}. "
            "Thus .125, .126, and .13 are not too strict for this finite "
            "horizon and would be sufficient equal caps if proved "
            "universally.  They are still finite-fit candidates only; the "
            "universal theorem remains open."),
        "finite_cap_sensitivity_audit_only": True,
        "per_modulus_supremum_theorem_proved": False,
        "one_sided_signed_concentration_theorem_proved": False,
        "raw_adverse_envelope_theorem_proved": False,
        "universal_raw_pointwise_theorem_proved": False,
        "strict_central_goldbach_theorem_proved": False,
        "goldbach_proved": False,
    }


def write_note(receipt):
    horizon = receipt["component_horizon"]
    window = receipt["uniform_cap_window"]
    lines = [
        "# q286 one-sided cap sensitivity audit",
        "",
        "## Question",
        "",
        receipt["question"],
        "",
        "## Receipt",
        "",
        "```text",
        "tools/build_q286_one_sided_cap_sensitivity_audit.py",
        "evidence/q286-one-sided-cap-sensitivity-audit.json",
        "```",
        "",
        "## Result",
        "",
        "```text",
        f"component horizon rows:                  {horizon['row_count']}",
        f"A_70 observed supremum:                  {horizon['component_adverse_suprema']['70']}",
        f"A_130 observed supremum:                 {horizon['component_adverse_suprema']['130']}",
        f"A_154 observed supremum:                 {horizon['component_adverse_suprema']['154']}",
        f"A_286 observed supremum:                 {horizon['component_adverse_suprema']['286']}",
        f"observed supremum sum:                   {horizon['component_adverse_supremum_sum']}",
        f"minimum local main:                      {horizon['min_local_main']}",
        f"observed max component adverse:          {horizon['observed_max_component_adverse']}",
        f"strict equal-cap ceiling min(M)/4:       {window['strict_equal_cap_theorem_ceiling_exclusive']}",
        f"finite cap window nonempty:              {window['nonempty_window']}",
        f"finite cap window width:                 {window['window_width']}",
        "```",
        "",
        "For these caps, smaller is stricter because the cap is an upper bound.",
        "So `.125` is stricter than `.126`, and both are stricter than `.13`.",
        "",
        "## Cap Table",
        "",
        "```text",
        "cap      observed fit   equal-cap sufficient if universal   margin",
    ]
    for row in receipt["cap_sensitivity"]:
        lines.append(
            f"{row['cap']:<8} {str(row['observed_fit_on_232_rows']):<14} "
            f"{str(row['universal_equal_cap_would_be_sufficient_if_proved']):<36} "
            f"{row['margin_to_min_local_main']}")
    lines += [
        "```",
        "",
        "## Decision",
        "",
        receipt["decision"],
        "",
        "This is finite cap-sensitivity evidence only.  It proves no per-modulus",
        "supremum theorem, one-sided signed concentration theorem, raw adverse-",
        "envelope theorem, strict-central Goldbach theorem, or Goldbach proof.",
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
        "observed_floor": receipt["uniform_cap_window"][
            "observed_uniform_cap_floor_inclusive"],
        "strict_ceiling": receipt["uniform_cap_window"][
            "strict_equal_cap_theorem_ceiling_exclusive"],
        "goldbach_proved": receipt["goldbach_proved"],
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

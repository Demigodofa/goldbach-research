"""Build q286 volatile polarity-magnitude ledger evidence.

The volatile sign-polarity receipt shows that boundary directions match
channel contribution signs.  This derivative receipt converts that polarity
into the exact rowwise magnitude inequality that a theorem would need to
control.
"""

from __future__ import annotations

import json
import math
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SUBSET_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-subset-ablation.json")
SIGN_SOURCE = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-sign-polarity-profile.json")
OUT = (
    ROOT / "evidence"
    / "q286-first-three-dominant-mode-volatile-polarity-magnitude-ledger.json")


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def json_ready(value):
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set)):
        return [json_ready(item) for item in value]
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return value


def label_tuple(label):
    return tuple(int(part) for part in label)


def label_key(label):
    return str(tuple(label))


def signed_parts(row, labels):
    contributions = {
        label: float(row["volatile_channel_contributions"][label_key(label)])
        for label in labels
    }
    positive = tuple(
        label for label, value in contributions.items() if value > 0.0)
    negative = tuple(
        label for label, value in contributions.items() if value < 0.0)
    return contributions, positive, negative


def sum_labels(contributions, labels):
    return math.fsum(contributions[label] for label in labels)


def row_ledger(target, row, labels):
    contributions, positive, negative = signed_parts(row, labels)
    base_margin = float(row["stable_core_sum_to_principal"]) + .3
    positive_sum = sum_labels(contributions, positive)
    negative_sum = sum_labels(contributions, negative)
    full_margin = base_margin + positive_sum + negative_sum
    expected_pass = bool(row["dominant_floor_passes"])

    if expected_pass:
        repairing_channels = positive
        adverse_channels = negative
        repair_magnitude = positive_sum
        adverse_magnitude = -negative_sum
        required_repair = -base_margin - negative_sum
        required_adverse_bound = base_margin + positive_sum
        signed_surplus = repair_magnitude - required_repair
        if abs(signed_surplus - full_margin) > 1e-12:
            raise AssertionError(f"clear surplus mismatch for {target}")
        inequality = (
            "repair_magnitude > -base_margin - negative_sum")
    else:
        repairing_channels = negative
        adverse_channels = positive
        repair_magnitude = -negative_sum
        adverse_magnitude = positive_sum
        required_repair = base_margin + positive_sum
        required_adverse_bound = repair_magnitude - base_margin
        signed_surplus = repair_magnitude - required_repair
        if abs(signed_surplus + full_margin) > 1e-12:
            raise AssertionError(f"deficit surplus mismatch for {target}")
        inequality = (
            "repair_magnitude > base_margin + positive_sum")

    ratio = (
        repair_magnitude / required_repair
        if required_repair > 0.0 else None)
    return {
        "target": target,
        "target_mod_286": row["target_mod_286"],
        "dominant_floor_passes": expected_pass,
        "base_margin_without_volatile": base_margin,
        "positive_sum_to_principal": positive_sum,
        "negative_sum_to_principal": negative_sum,
        "full_margin_to_floor": full_margin,
        "positive_channels": positive,
        "negative_channels": negative,
        "sign_expected_repair_channels": repairing_channels,
        "sign_expected_adverse_channels": adverse_channels,
        "repair_magnitude": repair_magnitude,
        "adverse_magnitude": adverse_magnitude,
        "required_repair_magnitude": required_repair,
        "required_adverse_bound_given_repair": required_adverse_bound,
        "signed_magnitude_surplus": signed_surplus,
        "repair_to_required_ratio": ratio,
        "row_inequality": inequality,
        "volatile_channel_contributions": tuple({
            "label": label,
            "contribution_to_principal": contributions[label],
        } for label in labels),
    }


def extrema(rows):
    ratios = [row["repair_to_required_ratio"] for row in rows
              if row["repair_to_required_ratio"] is not None]
    return {
        "target_count": len(rows),
        "minimum_signed_magnitude_surplus": min(
            row["signed_magnitude_surplus"] for row in rows),
        "maximum_signed_magnitude_surplus": max(
            row["signed_magnitude_surplus"] for row in rows),
        "mean_signed_magnitude_surplus": math.fsum(
            row["signed_magnitude_surplus"] for row in rows) / len(rows),
        "minimum_repair_to_required_ratio": min(ratios) if ratios else None,
        "maximum_repair_to_required_ratio": max(ratios) if ratios else None,
        "tightest_surplus_target": min(
            rows, key=lambda row: row["signed_magnitude_surplus"])["target"],
    }


def main():
    subset_payload = json.loads(SUBSET_SOURCE.read_text(encoding="utf-8"))
    sign_payload = json.loads(SIGN_SOURCE.read_text(encoding="utf-8"))
    labels = tuple(label_tuple(label) for label in subset_payload[
        "volatile_labels"])
    rows = tuple(
        row_ledger(int(target), row, labels)
        for target, row in sorted(
            subset_payload["target_rows"].items(),
            key=lambda item: int(item[0])))
    by_target = {row["target"]: row for row in rows}
    hard_targets = tuple(sign_payload["hard_deficit_targets"])
    hard_rows = tuple(row for row in rows if row["target"] in hard_targets)
    deficit_rows = tuple(
        row for row in rows if not row["dominant_floor_passes"])
    clear_rows = tuple(row for row in rows if row["dominant_floor_passes"])

    if by_target[1222142]["positive_channels"] != ((1, 7), (4, 4)):
        raise AssertionError("1222142 positive pair changed")
    if by_target[1242118]["positive_channels"] != ((1, 7), (4, 4)):
        raise AssertionError("1242118 positive pair changed")
    if by_target[1240888]["positive_channels"] != ():
        raise AssertionError("1240888 unexpectedly has positive channels")
    if abs(by_target[1222142]["signed_magnitude_surplus"]
           - 0.008833179560530147) > 1e-12:
        raise AssertionError("1222142 surplus changed")
    if abs(by_target[13556]["signed_magnitude_surplus"]
           - 0.009564090345659026) > 1e-12:
        raise AssertionError("13556 surplus changed")
    if extrema(rows)["tightest_surplus_target"] != 1222142:
        raise AssertionError("tightest selected surplus target changed")
    if abs(by_target[1242118]["repair_to_required_ratio"]
           - 2.3522112653157228) > 1e-12:
        raise AssertionError("1242118 repair ratio changed")

    payload = {
        "schema_version": 1,
        "source_commit": source_commit(),
        "source_subset_ablation": str(SUBSET_SOURCE.relative_to(ROOT)),
        "source_sign_polarity_profile": str(SIGN_SOURCE.relative_to(ROOT)),
        "status_boundary": (
            "finite volatile polarity-magnitude ledger only; no volatile-rim "
            "theorem, stable-core theorem, selected-fixture classifier "
            "theorem, pointwise character-sum estimate, or Goldbach proof is "
            "established"),
        "candidate": (
            "The signed-polarity theorem target may be stated as an exact "
            "rowwise repair-magnitude inequality rather than a Boolean "
            "boundary condition."),
        "mechanism": (
            "Split the eight volatile channels into positive and negative "
            "contribution sums for each row.  For deficit rows, negative "
            "volatile magnitude must beat base plus positive pressure; for "
            "clear rows, positive volatile magnitude must beat the negative "
            "drag after the base margin is included."),
        "prediction": (
            "If the tight rows have small positive magnitude surplus, the "
            "proof target is a quantitative signed-channel margin theorem. "
            "If surplus is comfortably large or sign-free, the Boolean cut "
            "would not be the active obstruction."),
        "falsifier": (
            "A different tightest row, loss of the shared positive pair on "
            "1222142/1242118, or failure of the surplus identities would "
            "falsify this magnitude ledger."),
        "novelty_label": "new-to-this-task",
        "arithmetic_modulus": subset_payload["arithmetic_modulus"],
        "support": subset_payload["support"],
        "dominant_modes": subset_payload["dominant_modes"],
        "tail_threshold": subset_payload["tail_threshold"],
        "volatile_labels": labels,
        "volatile_channel_count": len(labels),
        "rows": rows,
        "hard_deficit_targets": hard_targets,
        "hard_rows": hard_rows,
        "aggregates": {
            "selected": extrema(rows),
            "deficit": extrema(deficit_rows),
            "clear": extrema(clear_rows),
            "hard_deficit": extrema(hard_rows),
        },
        "summary": {
            "tightest_selected_row": (
                "1222142 has the smallest signed magnitude surplus, about "
                "0.0088331796, with repair/required ratio about 1.112961."),
            "next_tightest_row": (
                "13556 is next, with surplus about 0.0095640903 and "
                "repair/required ratio about 1.179968."),
            "shared_positive_pair": (
                "1222142 and 1242118 share positive volatile channels "
                "(1,7),(4,4); for 1222142 that pair is adverse, while for "
                "1242118 it is repairing."),
            "target_1242118": (
                "1242118 has repair/required ratio about 2.352211, so the "
                "shared positive pair is not itself the tight margin there."),
            "target_1240888": (
                "1240888 has no positive volatile channel and remains clear "
                "because its base margin already absorbs all negative volatile "
                "drag."),
        },
        "interpretation": {
            "hole_status": (
                "The finite q286 hole is now a quantitative signed-margin "
                "problem: the tightest selected surplus is small and occurs "
                "at the known tail row 1222142."),
            "route_status": (
                "The symmetry has moved from Boolean boundary polarity to "
                "signed magnitude inequalities with explicit tight rows."),
            "remaining_theorem": (
                "Prove these signed volatile repair-versus-adverse magnitude "
                "inequalities from actual binary-prime residue weights "
                "uniformly, or replace them with a full signed aggregate "
                "arithmetic-placement theorem."),
        },
        "volatile_polarity_magnitude_ledger_measured": True,
        "volatile_threshold_theorem_proved": False,
        "volatile_rim_theorem_proved": False,
        "stable_core_theorem_proved": False,
        "selected_fixture_classifier_theorem_proved": False,
        "pointwise_character_sum_estimate_proved": False,
        "signed_projection_theorem_proved": False,
        "goldbach_proved": False,
    }

    OUT.write_text(
        json.dumps(json_ready(payload), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

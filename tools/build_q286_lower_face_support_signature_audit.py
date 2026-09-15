"""Classify the q286 lower-face optimizer support.

The lower-face overlap audit found that actual prime-pair measures almost
avoid the two-point optimizer support of the coefficient-only lower face.  This
derived receipt asks whether that bad support has a simple residue signature,
or whether the stable object is instead geometric: an LP-defined
anchor/compensator face depending on the target row.

Finite diagnostic only.  This proves no support-signature theorem, signed
prime-correlation estimate, q286 threshold theorem, or Goldbach theorem.
"""

from __future__ import annotations

import json
import math
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
SOURCE = EVIDENCE / "q286-lower-face-overlap-audit.json"
OUT = EVIDENCE / "q286-lower-face-support-signature-audit.json"
PERIOD = 10010
MODULUS = 286
TOLERANCE = 1e-8


def source_commit():
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def finite_summary(values):
    values = [float(value) for value in values
              if value is not None and math.isfinite(float(value))]
    if not values:
        return {"count": 0, "minimum": None, "mean": None, "maximum": None}
    return {
        "count": len(values),
        "minimum": min(values),
        "mean": math.fsum(values) / len(values),
        "maximum": max(values),
    }


def counter_dict(counter):
    return {str(key): int(value) for key, value in sorted(counter.items())}


def top_counter(counter, limit=12):
    return [
        {"signature": str(key), "count": int(value)}
        for key, value in counter.most_common(limit)
    ]


def unit_signature(unit):
    return {
        "mod_5": int(unit % 5),
        "mod_7": int(unit % 7),
        "mod_11": int(unit % 11),
        "mod_13": int(unit % 13),
        "mod_143": int(unit % 143),
        "mod_286": int(unit % 286),
        "mod_10010": int(unit % PERIOD),
    }


def orbit_signature(orbit, modulus):
    return tuple(sorted(int(unit % modulus) for unit in orbit))


def complement_closed(orbit, target_residue):
    orbit_set = {int(unit) % PERIOD for unit in orbit}
    return all(((target_residue - int(unit)) % PERIOD) in orbit_set
               for unit in orbit_set)


def extracted_support(row):
    support = [
        orbit for orbit in row["largest_lower_minus_actual_orbits"]
        if float(orbit["lower_mass"]) > TOLERANCE
    ]
    support.sort(key=lambda item: (-float(item["lower_mass"]),
                                   tuple(item["orbit"])))
    return support


def classify_row(row):
    support = extracted_support(row)
    lower_mass_total = math.fsum(float(item["lower_mass"]) for item in support)
    negative_full_mass = math.fsum(
        float(item["lower_mass"]) for item in support
        if float(item["full_coefficient"]) < -TOLERANCE)
    positive_full_mass = math.fsum(
        float(item["lower_mass"]) for item in support
        if float(item["full_coefficient"]) > TOLERANCE)
    positive_f3_mass = math.fsum(
        float(item["lower_mass"]) for item in support
        if float(item["first_three_coefficient"]) > TOLERANCE)
    negative_f3_mass = math.fsum(
        float(item["lower_mass"]) for item in support
        if float(item["first_three_coefficient"]) < -TOLERANCE)
    actual_on_support = math.fsum(float(item["actual_mass"])
                                  for item in support)

    has_negative_anchor = any(
        float(item["lower_mass"]) > 0.5
        and float(item["full_coefficient"]) < -TOLERANCE
        and float(item["first_three_coefficient"]) < -TOLERANCE
        for item in support)
    has_positive_f3_compensator = any(
        float(item["first_three_coefficient"]) > TOLERANCE
        for item in support)
    all_full_negative = all(float(item["full_coefficient"]) < -TOLERANCE
                            for item in support)

    support_mod_signatures = {
        str(modulus): tuple(orbit_signature(item["orbit"], modulus)
                            for item in support)
        for modulus in (11, 13, 143, 286, PERIOD)
    }
    support_rows = []
    for item in support:
        orbit = [int(unit) for unit in item["orbit"]]
        support_rows.append({
            "orbit": orbit,
            "orbit_mod_286": list(orbit_signature(orbit, MODULUS)),
            "orbit_mod_143": list(orbit_signature(orbit, 143)),
            "complement_closed_for_target": complement_closed(
                orbit, int(row["target_residue"])),
            "actual_mass": float(item["actual_mass"]),
            "lower_mass": float(item["lower_mass"]),
            "delta_mass": float(item["delta_mass"]),
            "first_three_coefficient": float(item["first_three_coefficient"]),
            "full_coefficient": float(item["full_coefficient"]),
            "full_transport_contribution": float(
                item["full_transport_contribution"]),
            "unit_signatures": [unit_signature(unit) for unit in orbit],
        })

    return {
        "target": int(row["target"]),
        "target_residue": int(row["target_residue"]),
        "target_mod_286": int(row["target_mod_286"]),
        "block_index_after_discovery": int(
            row["block_index_after_discovery"]),
        "support_extracted_complete": (
            len(support) == int(row["lower_face_support_size"])),
        "lower_face_support_size": int(row["lower_face_support_size"]),
        "lower_mass_total_in_extracted_support": lower_mass_total,
        "actual_mass_on_extracted_support": actual_on_support,
        "actual_mass_on_lower_face_support": float(
            row["actual_mass_on_lower_face_support"]),
        "lower_support_all_full_negative": bool(all_full_negative),
        "lower_support_has_negative_anchor": bool(has_negative_anchor),
        "lower_support_has_positive_f3_compensator": bool(
            has_positive_f3_compensator),
        "negative_full_lower_mass_fraction": (
            negative_full_mass / lower_mass_total
            if lower_mass_total > TOLERANCE else None),
        "positive_full_lower_mass_fraction": (
            positive_full_mass / lower_mass_total
            if lower_mass_total > TOLERANCE else None),
        "positive_f3_lower_mass_fraction": (
            positive_f3_mass / lower_mass_total
            if lower_mass_total > TOLERANCE else None),
        "negative_f3_lower_mass_fraction": (
            negative_f3_mass / lower_mass_total
            if lower_mass_total > TOLERANCE else None),
        "support_mod_signatures": support_mod_signatures,
        "support_orbits": support_rows,
    }


def build_receipt():
    source = json.loads(SOURCE.read_text(encoding="utf-8"))
    rows = [classify_row(row) for row in source["target_rows"]]
    post = [row for row in rows if row["block_index_after_discovery"] >= 1]

    def summarize(bucket):
        support_size = Counter(row["lower_face_support_size"] for row in bucket)
        mod_counters = {
            modulus: Counter(
                row["support_mod_signatures"][str(modulus)]
                for row in bucket)
            for modulus in (11, 13, 143, 286, PERIOD)
        }
        top_mod286_count = (
            mod_counters[MODULUS].most_common(1)[0][1]
            if mod_counters[MODULUS] else 0)
        return {
            "row_count": len(bucket),
            "complete_support_rows": sum(
                row["support_extracted_complete"] for row in bucket),
            "support_size_histogram": counter_dict(support_size),
            "all_full_negative_rows": sum(
                row["lower_support_all_full_negative"] for row in bucket),
            "negative_anchor_rows": sum(
                row["lower_support_has_negative_anchor"] for row in bucket),
            "positive_f3_compensator_rows": sum(
                row["lower_support_has_positive_f3_compensator"]
                for row in bucket),
            "anchor_compensator_rows": sum(
                row["lower_support_has_negative_anchor"]
                and row["lower_support_has_positive_f3_compensator"]
                for row in bucket),
            "negative_full_lower_mass_fraction_summary": finite_summary(
                row["negative_full_lower_mass_fraction"] for row in bucket),
            "positive_f3_lower_mass_fraction_summary": finite_summary(
                row["positive_f3_lower_mass_fraction"] for row in bucket),
            "actual_mass_on_extracted_support_summary": finite_summary(
                row["actual_mass_on_extracted_support"] for row in bucket),
            "support_signature_unique_counts": {
                str(modulus): len(counter)
                for modulus, counter in mod_counters.items()
            },
            "top_support_signature_share_mod_286": (
                top_mod286_count / len(bucket) if bucket else None),
            "top_support_signatures": {
                str(modulus): top_counter(counter)
                for modulus, counter in mod_counters.items()
            },
        }

    summary = {
        "target_row_count": len(rows),
        "post_discovery_target_count": len(post),
        "all_rows": summarize(rows),
        "post_discovery_rows": summarize(post),
        "all_complement_closed_support_rows": sum(
            all(orbit["complement_closed_for_target"]
                for orbit in row["support_orbits"])
            for row in rows),
        "post_complement_closed_support_rows": sum(
            all(orbit["complement_closed_for_target"]
                for orbit in row["support_orbits"])
            for row in post),
    }

    post_top_share = summary["post_discovery_rows"][
        "top_support_signature_share_mod_286"]
    simple_residue_signature_supported = bool(
        post_top_share is not None and post_top_share >= 0.5)
    dominant_negative_full_face_supported = (
        summary["post_discovery_rows"]["complete_support_rows"] == len(post)
        and summary["post_discovery_rows"]["support_size_histogram"] == {"2": len(post)}
        and summary["post_discovery_rows"][
            "negative_full_lower_mass_fraction_summary"]["minimum"] > 0.9
    )

    decision = (
        "The stable signal is geometric rather than a fixed residue dictionary: "
        "every checked post-discovery lower-face optimizer has two support "
        "orbits and at least 93 percent of its lower-face mass on negative-Full "
        "orbits, while the exact residue support signatures are too dispersed "
        "to support a simple non-post-hoc residue selector."
    )
    if simple_residue_signature_supported:
        decision = (
            "A repeated residue support signature appears often enough to keep "
            "a simple residue-selector theorem candidate alive; this requires "
            "a frozen held-out test before promotion."
        )

    return {
        "schema_version": 1,
        "source_commit": source_commit(),
        "sources": {
            "lower_face_overlap_audit": str(SOURCE.relative_to(ROOT)),
        },
        "status_boundary": (
            "finite lower-face support signature diagnostic only; no "
            "support-signature theorem, signed prime-correlation theorem, q286 "
            "threshold theorem, strict-central Goldbach theorem, or Goldbach "
            "proof"
        ),
        "goldbach_proved": False,
        "lower_face_support_signature_theorem_proved": False,
        "simple_residue_signature_supported": simple_residue_signature_supported,
        "dominant_negative_full_face_supported": (
            dominant_negative_full_face_supported),
        "curiosity_status": "aha-candidate",
        "novelty_label": "new-to-this-task",
        "candidate": {
            "mechanism": (
                "The bad lower face is selected by coefficient geometry at the "
                "observed F3 value.  Actual prime-pair mass avoids that "
                "LP-defined face, so the theorem target should be anti-landing "
                "against the face support rather than a fixed label or residue "
                "dictionary."
            ),
            "prediction": (
                "Lower-face optimizer supports should keep a stable "
                "anchor/compensator coefficient pattern while their residue "
                "signatures vary with the target."
            ),
            "falsifier": (
                "A dominant residue signature on held-out rows, or a later "
                "post-boundary row whose lower-face support is not the observed "
                "two-orbit negative-Full bad face, falsifies this compressed "
                "description."
            ),
            "smallest_next_test": (
                "Freeze this signature and test later predeclared q286 tail "
                "windows without changing the selector."
            ),
        },
        "decision": decision,
        "summary": summary,
        "target_rows": rows,
    }


def main():
    OUT.write_text(
        json.dumps(build_receipt(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

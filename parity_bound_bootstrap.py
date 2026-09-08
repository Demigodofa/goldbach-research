"""Canonical finite lower-bound recursion whose own outputs preserve prime parity.

Owner: Kevin's research; purpose: test a composable bound without exact G input.
For a cubic band, P=A-C is the odd-prime indicator. Set
  L(N)=[A*A]_N-2[A*C]_N+C(N/2).
The last term is zero unless N/2 is an odd C-entry. Then
  G(N)-L(N)=[C*C]_N-C(N/2)
is twice the number of unordered DISTINCT composite pairs. Thus L<=G and
L=G mod2. In particular L(2m)%2 is the prime flag of odd m, even for negative L.

The conditional batch requires correct input PARITIES; integer typing and
L(6)%2=1 do not establish that truth. The canonical generator starts with
L(6)=1 and proves each new stage using only earlier output parities. Positivity
never gates propagation. No exact-count bootstrap, full prime square, or
ordinary prime sieve is called in the production pipeline. The small-prime
square-start marking is the explicit arithmetic construction, not a prime oracle.
This proves finite lower bounds and their parity invariant, not that L>0
universally. Its external novelty has not been assessed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from time import perf_counter

from cubic_batch import _block_shape, _build_survivors, _extract, _pack_binary
from cubic_sieve import exact_floor_cuberoot


def _odd_floor(n: int) -> int:
    return n if n % 2 else n - 1


def recover_parity_primes(bounds: list[int]) -> tuple[int, int, list[int]]:
    """Conditional decoder: returns prefix end, classified odd end, prime list.

    The list is indexed by targets6,8,...; L(2m) has list index m-3.
    An arbitrary integer sequence passing these checks has no primality meaning.
    """
    if not isinstance(bounds, list) or not bounds:
        raise ValueError("nonempty contiguous integer bound prefix required")
    if any(type(value) is not int for value in bounds) or bounds[0] % 2 != 1:
        raise ValueError("exact integer values and the known odd parity at6 required")
    endpoint = 2 * len(bounds) + 4
    classified = _odd_floor(endpoint // 2)
    return endpoint, classified, [m for m in range(3, classified + 1, 2)
                                  if bounds[m - 3] % 2]


def parity_batch(bounds: list[int], first: int, count: int) -> dict:
    """Build a later finite band, conditional on truthful earlier parities."""
    started = perf_counter()
    last, high, z = _block_shape(first, count)
    endpoint, classified, small_primes = recover_parity_primes(bounds)
    cofactor_limit = _odd_floor(high // (z + 1))
    if first <= endpoint:
        raise ValueError("all batch targets must follow the supplied prefix")
    if z > classified or cofactor_limit > classified:
        raise ValueError("earlier parity prefix is too short for this cubic band")
    recovery_seconds = perf_counter() - started

    built_at = perf_counter()
    survivors, composites, _ = _build_survivors(small_primes, z, high)
    construction_seconds = perf_counter() - built_at
    multiplied_at = perf_counter()
    slots = len(survivors)
    digit_bytes = max(1, (slots.bit_length() + 7) // 8)  # base>slots
    a = _pack_binary(survivors, digit_bytes)
    c = _pack_binary(composites, digit_bytes)
    ms = _extract(a * a, first, count, digit_bytes)
    acs = _extract(a * c, first, count, digit_bytes)
    convolution_seconds = perf_counter() - multiplied_at
    rows = []
    for i, (m, ac) in enumerate(zip(ms, acs)):
        target = first + 2 * i
        center = target // 2
        diagonal = composites[(center - 3) // 2] if center % 2 else 0
        lower = m - 2 * ac + diagonal  # signed arithmetic after decoding
        rows.append({"target_even": target, "M": m, "AC": ac,
                     "composite_diagonal": diagonal, "L": lower})
    nonpositive = [row["target_even"] for row in rows if row["L"] <= 0]
    unresolved = [row["target_even"] for row in rows
                  if row["L"] <= 0 and row["L"] % 2 == 0]
    return {
        "first_even": first, "last_even": last, "target_count": count,
        "input_prefix_end": endpoint, "classified_last_odd": classified,
        "cubic_cutoff": z, "required_cofactor_limit": cofactor_limit,
        "minimum_row": min(rows, key=lambda row: row["L"]),
        "nonpositive_targets": nonpositive, "unresolved_targets": unresolved,
        "certified_target_count": count - len(unresolved), "rows": rows,
        "seconds": {"parity_recovery": recovery_seconds,
                    "construction": construction_seconds,
                    "convolution": convolution_seconds,
                    "pipeline_total": perf_counter() - started},
        "input_meaning": "conditional on correct G parity at every supplied earlier label",
        "scope": "finite parity-preserving lower bounds; universal positivity unproved",
    }


def generate_prefix(endpoint: int) -> dict:
    """Generate every L(6),L(8),...,L(endpoint), starting only with L(6)=1.

    End each stage at the cube-root band boundary or the current input limit.
    Cofactor odd-floor<=B is equivalent to H<(B+2)*(z+1), with B odd.
    This exact integer condition permits the first stage6 ->10.
    """
    if type(endpoint) is not int or endpoint < 6 or endpoint % 2:
        raise ValueError("endpoint must be an even exact integer at least6")
    started = perf_counter()
    bounds = [1]
    stages = []
    previous = 6
    while previous < endpoint:
        first = previous + 2
        z = exact_floor_cuberoot(first - 3)
        classified = _odd_floor(previous // 2)
        high = _odd_floor(min((z + 1) ** 3 - 1, (classified + 2) * (z + 1) - 1))
        last = min(endpoint, high + 3)
        if last < first:
            raise RuntimeError("well-founded recursion failed to advance")
        batch = parity_batch(bounds, first, (last - first) // 2 + 1)
        bounds.extend(row["L"] for row in batch["rows"])
        stages.append({"previous_end": previous, "target_end": last,
                       "cubic_cutoff": z, "classified_last_odd": classified,
                       "required_cofactor_limit": batch["required_cofactor_limit"]})
        previous = last
    return {
        "canonical_base": {"target_even": 6, "L": 1}, "final_end": endpoint,
        "lower_bounds": bounds, "stages": stages,
        "minimum_lower_bound": min(bounds),
        "nonpositive_targets": [6 + 2 * i for i, value in enumerate(bounds) if value <= 0],
        "unresolved_targets": [6 + 2 * i for i, value in enumerate(bounds)
                               if value <= 0 and value % 2 == 0],
        "lower_bounds_sha256": hashlib.sha256(
            ",".join(map(str, bounds)).encode("ascii")).hexdigest(),
        "seconds": perf_counter() - started,
        "input_meaning": "canonical induction from L(6)=1 using only earlier output parity",
    }


def canonical_experiment() -> dict:
    """Frozen same-range experiment; input generation is part of total cost."""
    started = perf_counter()
    prefix = generate_prefix(20000)
    result = parity_batch(prefix["lower_bounds"], 1002000, 1000)
    result["method"] = "canonical parity-preserving lower-bound bootstrap"
    result["input_meaning"] = prefix["input_meaning"]
    result["prefix_summary"] = {key: value for key, value in prefix.items()
                                if key not in ("lower_bounds", "input_meaning")}
    result["seconds"]["input_generation"] = prefix["seconds"]
    result["seconds"]["complete_total"] = perf_counter() - started
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check-controls", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = canonical_experiment()
    rows = {row["target_even"]: row for row in result.pop("rows")}
    # Read only the already-verified same-block baseline, outside production timing.
    baseline = json.loads(Path(__file__).with_name("evidence").joinpath(
        "cubic-batch-prefix.json").read_text(encoding="utf-8"))
    if (baseline["first_even"], baseline["last_even"]) != (
            result["first_even"], result["last_even"]):
        raise RuntimeError("baseline target range differs")
    previous_failures = set(baseline["nonpositive_targets"])
    result["comparison"] = {
        "baseline": "evidence/cubic-batch-prefix.json",
        "baseline_complete_seconds": baseline["seconds"]["complete_total"],
        "baseline_minimum_raw": baseline["minimum_row"]["raw"],
        "lost_certifications": [n for n in result["unresolved_targets"]
                                if n not in previous_failures],
        "scope": "same fixed block; single-run timings do not establish a speedup",
    }
    if args.check_controls:
        from cubic_sieve import cubic_sieve_count
        from redistribution import sieve
        validation_started = perf_counter()
        high = result["last_even"] - 3
        flags = sieve(high)  # independent full-range flags, VALIDATION ONLY
        z = result["cubic_cutoff"]
        rough = bytearray(b"\1") * (high + 1)
        for p in range(3, z + 1, 2):
            if flags[p]:
                rough[p * p::2 * p] = b"\0" * len(range(p * p, high + 1, 2 * p))
        result["independent_controls"] = []
        for target in sorted({result["first_even"], result["minimum_row"]["target_even"],
                              result["last_even"]}):
            m = ac = 0
            for a in range(3, target - 2, 2):
                if rough[a] and rough[target - a]:
                    m += 1
                    ac += not flags[a]
            center = target // 2
            diagonal = int(bool(center % 2 and rough[center] and not flags[center]))
            row = rows[target]
            reference = cubic_sieve_count(target)
            if (row["M"], row["AC"], row["composite_diagonal"], row["L"]) != (
                    m, ac, diagonal, m - 2 * ac + diagonal):
                raise RuntimeError(f"direct-array disagreement at {target}")
            if not row["L"] <= reference["union_bound_raw"] <= reference["result"]:
                raise RuntimeError(f"lower-bound disagreement at {target}")
            if (reference["result"] - row["L"]) % 2:
                raise RuntimeError(f"parity disagreement at {target}")
            result["independent_controls"].append({**row, "reference_G": reference["result"],
                "reference_raw": reference["union_bound_raw"],
                "bound_loss": reference["union_bound_raw"] - row["L"]})
        result["seconds"]["independent_validation"] = perf_counter() - validation_started
    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()

"""A coherent finite countermodel for a proposed route to uniform positivity.

These are artificial binary sets, NOT primes or Goldbach counterexamples.
Fix an even squarefree wheel Q and H divisible by 2Q. Among units 1..H-1,
pair a with H-a; independently select lower, upper, or neither with
probabilities p, p, 1-2p. All selected points obey the fixed wheel, but
their self-convolution vanishes at H. Away from H its expectation equals
the independent Bernoulli wheel model (including the diagonal correction).

Owner: Kevin's research; Rill's reusable adversarial experiment. Its purpose
is to test whether binary convolution and fixed congruence data prevent an
isolated missing sum. It does not model full primality or prove anything
about the actual exceptional set in Goldbach's conjecture.
"""
from __future__ import annotations

from fractions import Fraction
import argparse
import json
import math
import random

from redistribution import sieve


def reflection_orbits(center: int, wheel: int) -> list[tuple[int, int]]:
    if (type(center) is not int or type(wheel) is not int or wheel < 2
            or wheel % 2 or center < 2*wheel or center % (2*wheel)):
        raise ValueError("even wheel Q>=2 and center H a positive multiple of 2Q required")
    # Squarefreeness is not needed for the model; repeated factors give the
    # same unit set. The mathematical asymptotic can use squarefree Q.
    return [(a, center-a) for a in range(1, center//2)
            if math.gcd(a, wheel) == 1]


def sample_model(center: int, wheel: int, probability: Fraction,
                 seed: int = 0) -> tuple[bytearray, bytearray]:
    if not isinstance(probability, Fraction) or not 0 < probability <= Fraction(1, 2):
        raise ValueError("an exact rational probability in (0,1/2] is required")
    orbits = reflection_orbits(center, wheel)
    selected = bytearray(center)
    units = bytearray(center)
    rng = random.Random(seed)
    for a, b in orbits:
        units[a] = units[b] = 1
        draw = rng.randrange(probability.denominator)
        if draw < probability.numerator:
            selected[a] = 1
        elif draw < 2*probability.numerator:
            selected[b] = 1
    return selected, units


def ordered_counts(flags: bytearray) -> list[int]:
    """Exact binary odd-set self-convolution by carry-free integer squaring."""
    if (not isinstance(flags, bytearray) or len(flags) < 2
            or any(x not in (0, 1) for x in flags) or any(flags[::2])):
        raise ValueError("binary bytearray supported on positive odd indices required")
    slots = len(flags)//2
    digit_bytes = max(1, (slots.bit_length()+7)//8)
    encoded = bytearray(slots*digit_bytes)
    for index in range(slots):
        encoded[index*digit_bytes] = flags[2*index+1]
    packed = int.from_bytes(encoded, "little")
    squared = (packed*packed).to_bytes((2*slots-1)*digit_bytes, "little")
    counts = [0]*(2*len(flags)-1)
    for index in range(2*slots-1):
        offset = index*digit_bytes
        counts[2*index+2] = int.from_bytes(squared[offset:offset+digit_bytes], "little")
    return counts


def splice_prime_prefix(flags: bytearray, center: int, through: int) -> bytearray:
    """Preserve a real prime prefix while keeping the artificial missing sum.

    The returned set may contain 2; ordered_counts deliberately accepts only
    odd sets, so callers evaluating even targets handle the base 2+2 alone.
    This operation does not make the remaining selected points prime.
    """
    if (not isinstance(flags, bytearray)
            or type(center) is not int or type(through) is not int
            or center < 6 or center % 2 or len(flags) <= center
            or through < 2 or 2*through >= center
            or any(value not in (0, 1) for value in flags)):
        raise ValueError("binary flags through center, and 2<=prefix<center/2 required")
    if any(flags[a] and flags[center-a] for a in range(center+1)):
        raise ValueError("the input already represents the protected center")
    primes = sieve(through)
    result = flags.copy()
    result[:through+1] = primes
    for p in range(2, through+1):
        if primes[p]:
            result[center-p] = 0
    return result


def baseline_numerators(units: bytearray, probability: Fraction) -> list[int]:
    """Numerators over denominator p.denominator**2, including center H."""
    raw = ordered_counts(units)
    a, b = probability.numerator, probability.denominator
    result = []
    for target, count in enumerate(raw):
        diagonal = int(target % 2 == 0 and target//2 < len(units)
                       and bool(units[target//2]))
        result.append(a*a*count + a*(b-a)*diagonal)
    return result


def experiment(center: int, wheel: int, probability: Fraction,
               seed: int = 0) -> dict:
    selected, units = sample_model(center, wheel, probability, seed)
    counts = ordered_counts(selected)
    baseline = baseline_numerators(units, probability)
    denominator = probability.denominator**2
    energy_numerator = sum((denominator*r-b)**2 for r, b in zip(counts, baseline))
    central_targets = range(center//2, 3*center//2+1, 2)
    # H is a multiple of 2Q with Q even, so H/2 and both endpoints are even.
    missing = [k for k in central_targets if counts[k] == 0]
    noncenter = [counts[k] for k in central_targets if k != center]
    return {
        "scope": "artificial binary set, fixed wheel only; not actual primes",
        "center": center, "wheel": wheel, "seed": seed,
        "probability": str(probability),
        "eligible_count": sum(units), "selected_count": sum(selected),
        "selected_to_H_over_logH": sum(selected)*math.log(center)/center,
        "central_interval": [center//2, 3*center//2],
        "central_missing_even_sums": missing,
        "minimum_other_central_count": min(noncenter),
        "baseline_at_center": str(Fraction(baseline[center], denominator)),
        "squared_error_sum": str(Fraction(energy_numerator, denominator**2)),
        "center_squared_error": str(Fraction(baseline[center]**2, denominator**2)),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--center", type=int, default=120120)
    parser.add_argument("--wheel", type=int, default=210)
    parser.add_argument("--probability", type=Fraction, default=Fraction(3, 8))
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()
    print(json.dumps(experiment(args.center, args.wheel, args.probability, args.seed), indent=2))

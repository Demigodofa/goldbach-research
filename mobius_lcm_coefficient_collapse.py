"""Measure exact Mobius cancellation after grouping divisor pairs by lcm.

For squarefree ``q`` and ``L=log X``, the complete divisor cube satisfies

    sum_(lcm(a,b)=q) mu(a)mu(b) log(X/a)log(X/b)
      = mu(q) [L^2-sum_(p|q)(log p)^2].                 (1)

Indeed the bivariate local factor is
``-exp(u log p)-exp(v log p)+exp((u+v)log p)``.  At the origin its two first
derivatives vanish, while its mixed derivative contributes ``-(log p)^2``
relative to the local value ``-1``.  Formula (1) keeps the project polynomial
log weights and collapses a three-choice-per-prime pair sum to one coefficient.

The actual lower union ``V<a,b<=B`` truncates the divisor cube, especially
when ``q>B``.  The finite probe below groups that exact coefficient and
measures whether its L1 mass behaves more like the lcm count or the raw pair
count.  It is a falsifier, not an asymptotic Mobius estimate.

There is also an exact parametrization of every squarefree pair.  Put
``g=gcd(a,b)``, ``r=a/g``, and ``s=b/g``.  Then ``g,r,s`` are pairwise
coprime and squarefree,

    lcm(a,b) = g*r*s,       mu(a)mu(b) = mu(r)mu(s).       (2)

Thus the signed count error is a constrained trilinear reciprocal-sawtooth
sum.  Formula (2) removes the Mobius sign on the shared factor ``g`` but does
not by itself estimate the remaining bilinear ``mu(r)mu(s)`` sum.
"""

import math
import random

from mobius_covariance_lag_probe import _mobius_values
from mobius_covariance_endpoint_probe import _prime_flags


def _squarefree_prime_factors(value):
    factors = []
    remaining = value
    prime = 2
    while prime * prime <= remaining:
        if remaining % prime == 0:
            remaining //= prime
            factors.append(prime)
            if remaining % prime == 0:
                raise ValueError("q must be squarefree")
        prime += 1 if prime == 2 else 2
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def complete_lcm_log_coefficient(q, X):
    """Return the closed form (1)."""
    if type(q) is not int or q < 1:
        raise ValueError("q must be a positive integer")
    if isinstance(X, bool) or not isinstance(X, (int, float)) or X <= q:
        raise ValueError("X must be real and greater than q")
    factors = _squarefree_prime_factors(q)
    mobius = -1 if len(factors) % 2 else 1
    return mobius * (
        math.log(X) ** 2 - sum(math.log(prime) ** 2 for prime in factors))


def mobius_lcm_collapse_probe(X, divisor_lower, divisor_upper):
    """Group the exact truncated pair coefficient by its lcm."""
    if (isinstance(X, bool) or not isinstance(X, (int, float))
            or X <= divisor_upper):
        raise ValueError("X must be real and exceed the divisor range")
    if (type(divisor_lower) is not int or type(divisor_upper) is not int
            or divisor_lower < 1 or divisor_upper <= divisor_lower):
        raise ValueError("invalid divisor range")
    mobius = _mobius_values(divisor_upper)
    divisors = tuple(
        value for value in range(divisor_lower + 1, divisor_upper + 1)
        if mobius[value])
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")
    logarithms = {value: math.log(X / value) for value in divisors}
    groups = {}
    raw_pair_l1 = 0.0
    for left in divisors:
        left_coefficient = mobius[left] * logarithms[left]
        for right in divisors:
            coefficient = (left_coefficient * mobius[right]
                           * logarithms[right])
            q = math.lcm(left, right)
            groups[q] = groups.get(q, 0.0) + coefficient
            raw_pair_l1 += abs(coefficient)
    grouped_low_l1 = sum(
        abs(value) for q, value in groups.items() if q <= divisor_upper)
    grouped_high_l1 = sum(
        abs(value) for q, value in groups.items() if q > divisor_upper)
    grouped_l1 = grouped_low_l1 + grouped_high_l1
    log_scale = math.log(X) ** 2
    return {
        "X": float(X),
        "divisor_range": (divisor_lower, divisor_upper),
        "divisor_count": len(divisors),
        "raw_pair_l1": raw_pair_l1,
        "grouped_lcm_l1": grouped_l1,
        "grouped_lcm_l1_over_log_X_squared": grouped_l1 / log_scale,
        "grouped_lcm_l1_over_raw_pair_l1": grouped_l1 / raw_pair_l1,
        "grouped_low_lcm_l1": grouped_low_l1,
        "grouped_high_lcm_l1": grouped_high_l1,
        "grouped_high_lcm_l1_over_log_X_squared":
            grouped_high_l1 / log_scale,
        "high_lcm_fraction_of_grouped_l1": grouped_high_l1 / grouped_l1,
        "distinct_lcm_count": len(groups),
        "mobius_lcm_collapse_asymptotic_proved": False,
    }


def mobius_lcm_signed_count_probe(
        modulus, ell, divisor_lower, divisor_upper):
    """Correlate grouped Mobius coefficients with exact CRT count errors."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus):
        raise ValueError("invalid signed-count ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")
    X = modulus * ell
    mobius = _mobius_values(divisor_upper)
    divisors = tuple(
        value for value in range(divisor_lower + 1, divisor_upper + 1)
        if mobius[value])
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")
    logarithms = {value: math.log(X / value) for value in divisors}
    groups = {}
    frame_base = 0.0
    for value in divisors:
        phi = value
        remaining = value
        prime = 2
        while prime * prime <= remaining:
            if remaining % prime == 0:
                phi -= phi // prime
                while remaining % prime == 0:
                    remaining //= prime
            prime += 1 if prime == 2 else 2
        if remaining > 1:
            phi -= phi // remaining
        frame_base += phi * logarithms[value] ** 2 / value ** 2
    for left in divisors:
        left_coefficient = mobius[left] * logarithms[left]
        for right in divisors:
            q = math.lcm(left, right)
            groups[q] = groups.get(q, 0.0) + (
                left_coefficient * mobius[right] * logarithms[right])

    signed = absolute = 0.0
    cyclic_signed = cyclic_absolute = 0.0
    low_signed = high_signed = 0.0
    low_absolute = high_absolute = 0.0
    interval_right = modulus * (ell + 1) - 1
    for q, coefficient in groups.items():
        count = interval_right // q - X // q
        discrepancy = count - modulus / q
        cyclic_discrepancy = count - (modulus - 1) / q
        term = coefficient * discrepancy
        cyclic_term = coefficient * cyclic_discrepancy
        signed += term
        absolute += abs(term)
        cyclic_signed += cyclic_term
        cyclic_absolute += abs(cyclic_term)
        if q <= divisor_upper:
            low_signed += term
            low_absolute += abs(term)
        else:
            high_signed += term
            high_absolute += abs(term)
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "divisor_count": len(divisors),
        "signed_grouped_count_error": signed,
        "absolute_grouped_count_error": absolute,
        "signed_to_absolute_count_error_ratio": (
            signed / absolute if absolute else 0.0),
        "cyclic_signed_grouped_count_error": cyclic_signed,
        "cyclic_absolute_grouped_count_error": cyclic_absolute,
        "cyclic_signed_to_absolute_ratio": (
            cyclic_signed / cyclic_absolute if cyclic_absolute else 0.0),
        "low_lcm_signed_count_error": low_signed,
        "high_lcm_signed_count_error": high_signed,
        "low_lcm_absolute_count_error": low_absolute,
        "high_lcm_absolute_count_error": high_absolute,
        "frozen_count_error_over_totient_frame":
            signed / (modulus * frame_base),
        "signed_lcm_count_cancellation_proved": False,
    }


def mobius_lcm_trilinear_count_error(
        modulus, ell, divisor_lower, divisor_upper):
    """Recompute the two signed errors through the exact parametrization (2)."""
    pair_receipt = mobius_lcm_signed_count_probe(
        modulus, ell, divisor_lower, divisor_upper)
    X = modulus * ell
    interval_right = modulus * (ell + 1) - 1
    mobius = _mobius_values(divisor_upper)
    signed = 0.0
    cyclic_signed = 0.0
    triple_count = 0
    for g in range(1, divisor_upper + 1):
        if not mobius[g]:
            continue
        quotient_upper = divisor_upper // g
        for r in range(1, quotient_upper + 1):
            left = g * r
            if (not mobius[r] or math.gcd(g, r) != 1
                    or left <= divisor_lower):
                continue
            left_log = math.log(X / left)
            for s in range(1, quotient_upper + 1):
                right = g * s
                if (not mobius[s] or math.gcd(g, s) != 1
                        or math.gcd(r, s) != 1
                        or right <= divisor_lower):
                    continue
                q = g * r * s
                count = interval_right // q - X // q
                coefficient = mobius[r] * mobius[s] * left_log * math.log(
                    X / right)
                signed += coefficient * (count - modulus / q)
                cyclic_signed += coefficient * (count - (modulus - 1) / q)
                triple_count += 1
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "trilinear_tuple_count": triple_count,
        "trilinear_signed_grouped_count_error": signed,
        "trilinear_cyclic_signed_grouped_count_error": cyclic_signed,
        "pair_minus_trilinear_signed_error":
            pair_receipt["signed_grouped_count_error"] - signed,
        "pair_minus_trilinear_cyclic_error":
            pair_receipt["cyclic_signed_grouped_count_error"] - cyclic_signed,
        "trilinear_reparametrization_estimate_proved": False,
    }


def signed_count_random_sign_comparison(
        modulus, ell, divisor_lower, divisor_upper,
        random_trials=128, random_seed=20260910):
    """Compare Mobius signs with all-positive and random Rademacher signs."""
    if (type(random_trials) is not int or random_trials < 1
            or type(random_seed) is not int):
        raise ValueError("random controls must be integers with trials positive")
    base = mobius_lcm_signed_count_probe(
        modulus, ell, divisor_lower, divisor_upper)
    X = modulus * ell
    mobius = _mobius_values(divisor_upper)
    divisors = tuple(
        value for value in range(divisor_lower + 1, divisor_upper + 1)
        if mobius[value])
    logarithms = tuple(math.log(X / value) for value in divisors)
    interval_right = modulus * (ell + 1) - 1
    pair_data = tuple(
        (left_index, right_index, q,
         (interval_right // q - X // q) - modulus / q)
        for left_index, left in enumerate(divisors)
        for right_index, right in enumerate(divisors)
        for q in (math.lcm(left, right),))

    # Store one discrepancy per lcm so each trial does not search pair_data.
    discrepancies = {}
    for _, _, q, discrepancy in pair_data:
        discrepancies[q] = discrepancy

    def fast_absolute_ratio(signs):
        groups = {}
        for left, right, q, _ in pair_data:
            coefficient = (signs[left] * signs[right]
                           * logarithms[left] * logarithms[right])
            groups[q] = groups.get(q, 0.0) + coefficient
        terms = tuple(coefficient * discrepancies[q]
                      for q, coefficient in groups.items())
        absolute = sum(abs(term) for term in terms)
        return abs(sum(terms)) / absolute if absolute else 0.0

    mobius_signs = tuple(int(mobius[value]) for value in divisors)
    mobius_ratio = fast_absolute_ratio(mobius_signs)
    # Keep the direct signed-count path tied to the generic comparison.
    if abs(mobius_ratio - abs(
            base["signed_to_absolute_count_error_ratio"])) > 1e-11:
        raise ArithmeticError("generic and Mobius grouped ratios disagree")
    all_positive_ratio = fast_absolute_ratio((1,) * len(divisors))
    generator = random.Random(random_seed)
    random_ratios = sorted(
        fast_absolute_ratio(tuple(
            1 if generator.getrandbits(1) else -1 for _ in divisors))
        for _ in range(random_trials))
    middle = random_trials // 2
    random_median = (random_ratios[middle] if random_trials % 2
                     else (random_ratios[middle - 1]
                           + random_ratios[middle]) / 2)
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "divisor_count": len(divisors),
        "mobius_absolute_signed_to_grouped_l1_ratio": mobius_ratio,
        "all_positive_absolute_signed_to_grouped_l1_ratio":
            all_positive_ratio,
        "random_trial_count": random_trials,
        "random_ratio_minimum": random_ratios[0],
        "random_ratio_median": random_median,
        "random_ratio_maximum": random_ratios[-1],
        "fraction_random_ratios_at_most_mobius":
            sum(value <= mobius_ratio for value in random_ratios)
            / random_trials,
        "mobius_beats_random_signs_asymptotically_proved": False,
    }


if __name__ == "__main__":
    print(mobius_lcm_collapse_probe(123407, 5, 42))

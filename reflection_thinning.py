"""Exact block fixtures for reflection-thinned weights, not alternate primes.

Owner: Goldbach research. Analytical scope and concentration proof:
notes/reflection-thinning-linear-input-obstruction.md.
"""

from fractions import Fraction as F

from complementary_divisor_correlation import _coefficients, central_interval


def _measure(target, weights):
    central_interval(target)
    weights = _coefficients(weights)
    if any(n > target or value < 0 for n, value in weights.items()):
        raise ValueError("require nonnegative rational weights on 1,...,N")
    return weights


def collision_pairs(target, weights):
    """Distinct positive reflected pairs, excluding the fixed midpoint."""
    weights = _measure(target, weights)
    return tuple((n, target - n) for n in central_interval(target)
                 if n < target - n and weights.get(n, 0) > 0
                 and weights.get(target - n, 0) > 0)


def reflection_thin(target, weights, signs):
    """Keep/double one side of each collision and delete the midpoint."""
    weights = _measure(target, weights)
    pairs, signs = collision_pairs(target, weights), tuple(signs)
    if len(signs) != len(pairs) or any(type(s) is not int or s not in (-1, 1)
                                     for s in signs):
        raise ValueError("require one integer sign in {-1,1} per collision")
    result = dict(weights)
    for (n, m), sign in zip(pairs, signs):
        result[n], result[m] = (1 + sign) * weights[n], (1 - sign) * weights[m]
    result.pop(target // 2, None)
    return {n: value for n, value in result.items() if value}


def prefix_perturbation_form(target, weights, modulus, residue, prefix):
    """Return (sign coefficients, fixed bias) for one progression prefix."""
    weights = _measure(target, weights)
    if (type(modulus) is not int or modulus < 1 or type(residue) is not int
            or type(prefix) is not int or not 0 <= prefix <= target):
        raise ValueError("require integer q>=1, residue, and 0<=prefix<=N")

    def selected(n):
        return n <= prefix and (n - residue) % modulus == 0

    coefficients = tuple(weights[n] * selected(n) - weights[m] * selected(m)
                         for n, m in collision_pairs(target, weights))
    midpoint = target // 2
    bias = -weights.get(midpoint, F(0)) * selected(midpoint)
    return coefficients, bias

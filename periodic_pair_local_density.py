"""Exact finite local densities and the mass direction lost by centering.

These identities concern residue models and arbitrary nonnegative vectors.
They do not estimate prime correlations or major/minor arc integrals.
"""

from fractions import Fraction
from math import gcd, prod


def squarefree_factors(modulus):
    if not isinstance(modulus, int) or modulus < 1:
        raise ValueError("modulus must be a positive integer")
    remaining = modulus
    factors = []
    divisor = 2
    while divisor * divisor <= remaining:
        if remaining % divisor == 0:
            factors.append(divisor)
            remaining //= divisor
            if remaining % divisor == 0:
                raise ValueError("modulus must be squarefree")
        divisor += 1
    if remaining > 1:
        factors.append(remaining)
    return tuple(factors)


def admissible_residues(target, modulus):
    squarefree_factors(modulus)
    return tuple(s for s in range(modulus)
                 if gcd(s, modulus) == gcd(target - s, modulus) == 1)


def local_pair_product(target, modulus):
    factors = squarefree_factors(modulus)
    return prod((Fraction(p * (p - 1 if target % p == 0 else p - 2),
                          (p - 1) ** 2) for p in factors), start=Fraction(1))


def periodic_density(target, period, modulus, weight):
    """Return direct residue sum and CRT factorization, both exact.

    Weight is a complete period of rational values. Requiring squarefree
    modulus is deliberate: the proof fixture uses independent prime cells.
    """
    factors = squarefree_factors(modulus)
    squarefree_factors(period)
    if modulus % period or len(weight) != period:
        raise ValueError("period must divide modulus and match weight length")
    allowed = admissible_residues(target, period)
    if not allowed:
        raise ValueError("local mean is undefined on empty admissible support")
    weight = tuple(map(Fraction, weight))
    mean = sum((weight[s] for s in allowed), Fraction()) / len(allowed)
    totient = prod(p - 1 for p in factors)
    direct = Fraction(modulus, totient ** 2) * sum(
        (weight[x % period] for x in range(modulus)
         if gcd(x, modulus) == gcd(target - x, modulus) == 1), Fraction())
    return direct, mean * local_pair_product(target, modulus)


def affine_mass_split(mass, reference, baseline, weight):
    """Expose scalar and centered errors relative to baseline * reference."""
    mass, reference, weight = (tuple(map(Fraction, values))
                               for values in (mass, reference, weight))
    baseline = Fraction(baseline)
    if not mass or not (len(mass) == len(reference) == len(weight)):
        raise ValueError("vectors must have the same nonzero length")
    if min(mass) < 0 or min(reference) < 0 or sum(reference) != 1:
        raise ValueError("mass must be nonnegative and reference a probability")
    if baseline <= 0:
        raise ValueError("baseline must be positive")
    total = sum(mass)
    mean = sum(w * u for w, u in zip(weight, reference))
    error = tuple(r - baseline * u for r, u in zip(mass, reference))
    scalar_error = sum(error)
    centered = tuple(e - u * scalar_error for e, u in zip(error, reference))
    centered_action = sum(w * c for w, c in zip(weight, centered))
    witness = sum(w * r for w, r in zip(weight, mass))
    return {
        "total": total,
        "mean": mean,
        "error": error,
        "scalar_error": scalar_error,
        "centered": centered,
        "centered_action": centered_action,
        "witness": witness,
        "reconstructed_witness": mean * baseline + mean * scalar_error
        + centered_action,
    }

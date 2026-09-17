"""Exact factor-shape algebra for a main-scale adverse-mass obstruction.

The analytical proof is in notes/same-sign-six-factor-adverse-mass.md.
Rational shares are algebra fixtures, not asserted logarithms of primes.
No finite count here proves the asymptotic prime-product counting step.
"""

from fractions import Fraction as F

from polynomial_joint_majorant import polynomial_cofactor_samples


BALANCED = (F(1, 6),) * 6
SKEW = (F(1, 8),) * 5 + (F(3, 8),)


def cutoff_shape(shares, cutoff_share):
    """Return sum_S (-1)^|S| (t-sum_(i in S)u_i)_+ exactly.

    The shares need NOT sum to one: the physical normalization is log Y,
    while the actual argument can be anywhere in [Y, 11Y/10].
    """
    shares = tuple(shares)
    if not shares or type(cutoff_share) is not F or cutoff_share <= 0:
        raise ValueError('nonempty positive rational shares and cutoff required')
    if any(type(s) is not F or s <= 0 for s in shares):
        raise ValueError('positive exact rational shares required')
    return cutoff_share * polynomial_cofactor_samples(
        tuple(s / cutoff_share for s in shares), 1)


def shape_variation_bound(shares, other_shares, cutoff, other_cutoff):
    """Lipschitz budget obtained by charging every subset hinge separately."""
    shares, other_shares = tuple(shares), tuple(other_shares)
    cutoff_shape(shares, cutoff)
    cutoff_shape(other_shares, other_cutoff)
    if len(shares) != len(other_shares):
        raise ValueError('the two shapes must have equal dimension')
    dimension = len(shares)
    return (2**dimension * abs(cutoff - other_cutoff)
            + 2**(dimension - 1)
            * sum((abs(a - b) for a, b in zip(shares, other_shares)), F(0)))


def six_factor_parameters(theta):
    """Fixed analytic neighborhood, not an optimized or fitted constant."""
    if type(theta) is not F or not F(9, 20) < theta < F(1, 2):
        raise ValueError('fixed exact rational 9/20 < theta < 1/2 required')
    balanced_margin = 10 * theta - 4
    skew_margin = 5 * theta - F(9, 4)
    margin = min(balanced_margin, skew_margin)
    delta = min(F(1, 1000), margin / 768)
    return {
        'balanced_margin': balanced_margin,
        'skew_margin': skew_margin,
        'shape_radius': delta,
        'first_five_radius': delta / 12,
        'cutoff_drift': margin / 256,
        'pair_weight_floor': balanced_margin * skew_margin / 4,
    }

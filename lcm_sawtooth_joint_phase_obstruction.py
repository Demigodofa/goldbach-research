"""Show why a maximum-denominator joint phase bound stops at beta=1/4.

After primitive-frequency expansion, a boundary cross term between reduced
fractions ``k/d`` and ``h/e`` has phase-difference denominator as large as
``d*e``.  Both conductors may be of order ``B^2`` on the actual lcm support,
so the denominator can be of order ``B^4``.

The existing joint prime-row rotation bound contains

    sqrt(Q/(M*A)).

At the project scales ``M=N^.59`` and ``A=N^.41``, substituting ``Q=B^4``
costs ``N^(2*beta-1/2)``.  Taking the maximum difference denominator therefore
cannot reach the active ``beta=.32`` range.  A proof must average the
difference moduli or retain signed arithmetic cancellation.
"""

import math

from mobius_covariance_endpoint_probe import _prime_flags


def high_difference_modulus_witness(divisor_lower, divisor_upper):
    """Construct two supported conductors with coprime product near ``B^4``."""
    if (type(divisor_lower) is not int or type(divisor_upper) is not int
            or divisor_lower < 1 or divisor_upper <= divisor_lower):
        raise ValueError("invalid divisor range")
    flags = _prime_flags(divisor_upper)
    primes = tuple(
        value for value in range(divisor_upper // 2 + 1, divisor_upper + 1)
        if value > divisor_lower and flags[value])
    if len(primes) < 4:
        raise ValueError("need four retained primes above B/2")
    p1, p2, p3, p4 = primes[-4:]
    left_conductor = p1 * p2
    right_conductor = p3 * p4
    if math.gcd(left_conductor, right_conductor) != 1:
        raise ArithmeticError("witness conductors must be coprime")
    difference_numerator = right_conductor - left_conductor
    difference_denominator = left_conductor * right_conductor
    if math.gcd(difference_numerator, difference_denominator) != 1:
        raise ArithmeticError("frequency difference must already be reduced")
    return {
        "divisor_range": (divisor_lower, divisor_upper),
        "retained_primes": (p1, p2, p3, p4),
        "primitive_conductors": (left_conductor, right_conductor),
        "reduced_frequency_difference": (
            difference_numerator, difference_denominator),
        "difference_denominator_over_B_fourth": (
            difference_denominator / divisor_upper ** 4),
        # For d=p1*p2>B, only the ordered pairs (p1,p2),(p2,p1)
        # have lcm d.  Hence the quadratic coefficient of S_d is 2/d.
        "structured_quadratic_coefficients": (
            2 / left_conductor, 2 / right_conductor),
        "B_fourth_difference_denominator_witness_proved": True,
    }


def termwise_joint_phase_exponent_budget(divisor_exponent):
    """Return the three joint-phase exponents after ``Q<=B^4``."""
    if (isinstance(divisor_exponent, bool)
            or not isinstance(divisor_exponent, (int, float))
            or not 0 < divisor_exponent < .5):
        raise ValueError("divisor_exponent must lie in (0,.5)")
    beta = float(divisor_exponent)
    exponents = (-.205, 2 * beta - .5, -2 * beta)
    return {
        "divisor_exponent": beta,
        "A_inverse_square_root_exponent": exponents[0],
        "difference_modulus_square_root_exponent": exponents[1],
        "difference_modulus_inverse_square_root_exponent": exponents[2],
        "maximum_denominator_joint_bound_power_saving": max(exponents) < 0,
        "strict_maximum_denominator_threshold": .25,
        "weighted_difference_modulus_bound_proved": False,
        "signed_frequency_pair_cancellation_proved": False,
    }


if __name__ == "__main__":
    print(high_difference_modulus_witness(5, 50))
    for beta in (.245, .25, .295, .32, 49 / 150):
        print(termwise_joint_phase_exponent_budget(beta))

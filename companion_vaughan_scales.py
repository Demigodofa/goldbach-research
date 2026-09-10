"""Scale bookkeeping when Vaughan is applied to the actual long companion.

The residual has a_B(n)*Lambda(m), with n<N**.41 and m approximately N/n.
This file only records factor ranges; it proves no bilinear estimate.
"""
from fractions import Fraction as F

CORE = F(41, 100)
BALANCED = F(499, 2000)
COMPANION_MIN = 1 - CORE


def companion_range(n_exponent=CORE):
    if not isinstance(n_exponent, F) or not 0 < n_exponent < 1:
        raise ValueError("exact n exponent in (0,1) required")
    return 1 - n_exponent


def linear_combined_range(u= BALANCED, n_exponent=CORE,
                          companion_exponent=COMPANION_MIN):
    """Range of x=n*a and its free complementary factor at top block."""
    if not all(isinstance(x, F) and 0 <= x <= 1 for x in (u, n_exponent, companion_exponent)):
        raise ValueError("exact exponents in [0,1] required")
    return {"min": n_exponent, "max": n_exponent + u,
            "free_factor_min": companion_exponent - u,
            "free_factor_max": companion_exponent,
            "product_x_free": F(1)}


def type_ii_companion_range(u= BALANCED, v= BALANCED,
                            companion_exponent=COMPANION_MIN):
    """Ranges for a>V,b>U, ab=m in a Vaughan Type-II term."""
    if not all(isinstance(x, F) and 0 <= x <= 1 for x in (u, v, companion_exponent)):
        raise ValueError("exact exponents in [0,1] required")
    if u + v > companion_exponent:
        return {"nonempty": False}
    return {"nonempty": True, "a_min": v, "b_min": u,
            "a_max": companion_exponent - u,
            "b_max": companion_exponent - v,
            "n_times_a_min": CORE + v,
            "n_times_b_min": CORE + u}


def balanced_companion_diagnostic():
    linear = linear_combined_range()
    bilinear = type_ii_companion_range()
    return {
        "companion_min": COMPANION_MIN,
        "linear": linear,
        "bilinear": bilinear,
        "scope": "necessary scale bookkeeping only; no Type-II theorem is invoked",
    }

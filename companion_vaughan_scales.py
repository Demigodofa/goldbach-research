"""Diagnostic showing why Vaughan does not split the actual prime companion.

The residual has a_B(n)*Lambda(m), with n<N**.41 and m approximately N/n.
The interval ranges below apply only to hypothetical composite m=ab.  After
the already-paid power-small prime-only replacement, m is prime and has no
such factors.
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
            "product_x_free": n_exponent + companion_exponent}


def hypothetical_type_ii_range(u=BALANCED, v=BALANCED,
                               companion_exponent=COMPANION_MIN):
    """Composite-support ranges for a>V,b>U, ab=m; absent when m is prime."""
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
    bilinear = hypothetical_type_ii_range()
    return {
        "companion_min": COMPANION_MIN,
        "linear": linear,
        "bilinear": bilinear,
        "scope": "hypothetical composite support only; actual prime companion has no Type-II term",
    }


def actual_prime_vaughan_terms(prime, lambda_cutoff, mobius_cutoff):
    """Exact four Vaughan terms for an actual prime companion."""
    from major_arc_kernel import _factorization
    from unexceptional_vaughan_gate import vaughan_log_vectors
    if not isinstance(prime, int) or prime < 2 or _factorization(prime) != ((prime, 1),):
        raise ValueError("prime required")
    return vaughan_log_vectors(prime, lambda_cutoff, mobius_cutoff)


def actual_prime_diagnostic(prime=101, lambda_cutoff=7, mobius_cutoff=5):
    terms = actual_prime_vaughan_terms(prime, lambda_cutoff, mobius_cutoff)
    return {"low": terms[0], "linear": terms[1], "subtracted": terms[2],
            "type_ii": terms[3], "type_ii_empty": terms[3] == (),
            "mechanism": "only the trivial divisor a=1 supplies log(prime)"}

"""Exact guards for the actual composite-sector compensation theorem.

See notes/composite-sector-signed-compensation.md for the analytical proof.
Formal log vectors and rational substitutions do not certify its error rate.
"""

from fractions import Fraction as F

from cutoff_normalized_remainder import cutoff_log_vectors
from major_arc_kernel import _factorization
from unexceptional_vaughan_gate import _add, _clean, mangoldt_log_vector


def prime_composite_vectors(n, cutoff):
    """Separate actual primes, composites and proper powers with n>R."""
    short, residual = cutoff_log_vectors(n, cutoff)
    if cutoff >= n:
        raise ValueError('require n>R for the constant prime cutoff value')
    prime = int(_factorization(n) == ((n, 1),))
    composite_short = dict(short)
    _add(composite_short, _factorization(cutoff), -prime)
    return {
        'P': prime,
        'A': short,
        'D': residual,
        'B': _clean(composite_short),
        'Q': () if prime else mangoldt_log_vector(n),
        'D_prime': residual if prime else (),
        'D_composite': () if prime else residual,
        'Lambda_prime': mangoldt_log_vector(n) if prime else (),
    }


def power_free_sector_identity(aa, pa, lambda_prime_a, pair_count,
                               pair_log_sum, pair_log_product, log_cutoff):
    """Return PP, ONE ordered PC, and CC before proper-power corrections.

    Inputs are exact rational substitutions for the named correlations,
    not independently supplied asymptotic estimates or prime-pair bounds.
    """
    values = (aa, pa, lambda_prime_a, pair_count, pair_log_sum,
              pair_log_product, log_cutoff)
    if any(type(v) not in (int, F) for v in values):
        raise ValueError('exact rational correlation inputs required')
    a, z, m, t = log_cutoff, pair_count, pair_log_sum, pair_log_product
    return {
        'pp': t - 2*a*m + a*a*z,
        'pc': -lambda_prime_a + a*pa + a*m - a*a*z,
        'cc': aa - 2*a*pa + a*a*z,
    }


def composite_main_floor(theta, relative_log_width):
    """Lower bound for 1-6 log(R) J_N/N when width=log(3)/log(N).

    This bounds only the explicit main. It is not an effective onset for
    the analytical remainder or for Goldbach.
    """
    if type(theta) is not F or not 0 < theta < F(1, 2):
        raise ValueError('exact rational 0<theta<1/2 required')
    if type(relative_log_width) is not F or not 0 <= relative_log_width < 1:
        raise ValueError('exact rational relative log width in [0,1) required')
    return 1 - 2*theta/(1-relative_log_width)

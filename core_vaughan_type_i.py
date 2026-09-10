"""Bounded scale test for the exact Vaughan split in the Goldbach core.

This records a new limitation test, not a prime-pair estimate.  The core is
the reflected product p=N-d*k*m+r with d*k<N**.41 and m a prime companion.
"""
from fractions import Fraction as F


CORE = F(41, 100)


def balanced_cutoffs(epsilon=F(1, 1000)):
    """Return gamma,U,V exponents for the exact Vaughan identity."""
    if not isinstance(epsilon, F) or not (0 < epsilon < F(1, 12)):
        raise ValueError("epsilon must be an exact fraction in (0,1/12)")
    gamma = F(1, 2) - epsilon
    return gamma, gamma / 2, gamma / 2


def type_ii_support_exponent(epsilon=F(1, 1000)):
    """Smallest exponent of ab in the surviving exact Type-II term."""
    _, u, v = balanced_cutoffs(epsilon)
    return u + v


def type_ii_vanishes_on_core(epsilon=F(1, 1000)):
    """Whether a>V and b>U is impossible when ab<N**CORE."""
    return type_ii_support_exponent(epsilon) > CORE


def reflected_modulus_exponent(cofactor_exponent=CORE, companion_exponent=F(59, 100)):
    """Exponent of q=d*m when d<N**cofactor_exponent and m<N**companion_exponent."""
    if not all(isinstance(x, F) and 0 <= x <= 1 for x in (cofactor_exponent, companion_exponent)):
        raise ValueError("exact exponents in [0,1] required")
    return cofactor_exponent + companion_exponent


def type_i_bv_margin(bv_level=F(1, 2), cofactor_exponent=CORE,
                     companion_exponent=F(59, 100)):
    """BV level minus the worst reflected modulus exponent."""
    return bv_level - reflected_modulus_exponent(cofactor_exponent, companion_exponent)


def identity_terms(n, lambda_cutoff, mobius_cutoff):
    """Return the four exact Vaughan terms using the shared implementation."""
    from unexceptional_vaughan_gate import vaughan_log_vectors
    return vaughan_log_vectors(n, lambda_cutoff, mobius_cutoff)


def term_sum(terms):
    out = {}
    for term in terms:
        for p, c in term:
            out[p] = out.get(p, 0) + c
    return tuple((p, c) for p, c in sorted(out.items()) if c)


def type_i_obstruction(epsilon=F(1, 1000)):
    """Concrete falsifier: balanced Vaughan is Type-I-only but BV misses q."""
    gamma, u, v = balanced_cutoffs(epsilon)
    # In the linear Vaughan term d<=V; k carries the rest of the core.
    q = reflected_modulus_exponent(v, F(59, 100))
    return {
        "gamma": gamma, "U_exponent": u, "V_exponent": v,
        "core_exponent": CORE, "type_ii_support_exponent": u + v,
        "type_ii_vanishes": u + v > CORE, "worst_modulus_exponent": q,
        "BV_margin": F(1, 2) - q,
        "remaining_problem": "fixing d leaves simultaneous primality of m and N-d*k*m+r",
    }

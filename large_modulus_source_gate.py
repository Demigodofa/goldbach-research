"""Source gate for the tempting 3/5 large-modulus theorem.

Maynard's arXiv:2006.07088v1, Theorem 1.1, reaches Q<=x^(3/5-eps)
for a FIXED integer residue a and triply well-factorable lambda_q.  The
Goldbach top-core modulus has the right numerical size, but neither the
target-varying residues N+r nor the actual endpoint-coupled modulus weights
have been transferred to those hypotheses.  This file prevents an exponent
match from being cited as an actual prime-correlation estimate.
"""
from fractions import Fraction as F

SHORT_DIVISOR = F(9, 1000)
CORE_TOP = F(41, 100)
MAYNARD_LIMIT = F(3, 5)


def product_modulus_exponent(cofactor_exponent, short_divisor=SHORT_DIVISOR):
    """q=d*m with d<=N^short_divisor and m~N^(1-cofactor)."""
    if not all(isinstance(x, F) and 0 <= x <= 1
               for x in (cofactor_exponent, short_divisor)):
        raise ValueError("exact exponents in [0,1] required")
    return short_divisor + 1 - cofactor_exponent


def numerical_margin(cofactor_exponent=CORE_TOP):
    """Bare 3/5 exponent margin, before every source hypothesis."""
    return MAYNARD_LIMIT - product_modulus_exponent(cofactor_exponent)


def source_hypothesis_gate(*, fixed_bounded_residue, triply_well_factorable,
                           endpoint_coupling_transferred, shift_family_transferred):
    """Whether the named source theorem has actually been matched."""
    values = (fixed_bounded_residue, triply_well_factorable,
              endpoint_coupling_transferred, shift_family_transferred)
    if not all(type(value) is bool for value in values):
        raise ValueError("exact boolean source checks required")
    return all(values)


def balanced_triple_support_obstruction(modulus_exponent=F(599, 1000),
                                        prime_factor_exponent=F(59, 100)):
    """A prime factor above Q^(1/3) cannot fit the balanced Definition 2 split."""
    if not all(isinstance(x, F) and 0 <= x <= 1
               for x in (modulus_exponent, prime_factor_exponent)):
        raise ValueError("exact exponents in [0,1] required")
    return prime_factor_exponent > modulus_exponent / 3


def actual_top_core_gate():
    return {
        "q_exponent": product_modulus_exponent(CORE_TOP),
        "bare_margin_below_three_fifths": numerical_margin(),
        "fixed_bounded_residue": False,
        "triply_well_factorable": False,
        "endpoint_coupling_transferred": False,
        "shift_family_transferred": False,
        "licensed": False,
        "balanced_triple_support_obstruction": balanced_triple_support_obstruction(),
        "reason": "N+r varies with target/shift, and m>Q^(1/3) obstructs the required balanced triple factorization",
    }

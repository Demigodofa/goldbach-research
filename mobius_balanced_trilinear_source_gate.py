"""Source and exponent gate for the balanced Mobius trilinear transform.

Owner: Kevin's Goldbach research.  Purpose: test published finite-field
trilinear estimates against the exact d=1 balanced-factor band before using
Cauchy.  This is an exponent comparison, not a new exponential-sum estimate.

EXACT BLOCK AND DUAL FORM.
Put p~N^(59/100), H=N^(1/10), and let I_p have size N^(49/100+o(1)).
On a product block J of length Y=N^y, y>1499/2000, restrict

    a~N^alpha, b~N^(1-alpha), 41/100<alpha<59/100.

For any gamma=(gamma_h)_(h in I_p) with sum |gamma_h|^2=1, the oscillating
part of the dual band norm is, up to N^o(1),

 sum_(h in I_p) gamma_h sum_(a,b: ab in J) mu(a) log(b) e_p(-hab). (1)

Petridis--Shparlinski, arXiv:1604.08469v4, Theorem 1.3, applies EXACTLY to
(1) after dividing log(b) by log N: put the hard condition 1_(ab in J),
mu(a), and log(b)/log N in one pair weight and gamma_h in another.  Its
pair weights are allowed to be arbitrary of modulus at most one.  The phase
is its e_p(x*y*z), after changing a sign.  Source:

    https://arxiv.org/abs/1604.08469

The theorem gives, for support cardinality exponents x>=u>=z,

    p^(1/8) X^(7/8) U^(29/32) Z^(29/32).             (2)

Macourt--Petridis--Shkredov--Shparlinski,
arXiv:2003.03493v1, Theorem 6.1, improves the two 29/32 powers to 47/52
and adds X*U*Z^(3/4), but only when U,Z<=p^(1/2).  Source:

    https://arxiv.org/abs/2003.03493

ENDPOINT LOCALIZATION DOES NOT REPAIR THE BUDGET.
Split both factor intervals into relative N^(-lambda) cells.  The number of
cell pairs intersecting a relative N^(y-1) product strip has exponent

    k(lambda)=lambda+max(0,lambda+y-1).                (3)

The three support exponents in one cell are

    alpha-lambda, 1-alpha-lambda, 49/100.              (4)

At the natural localization lambda=1-y, (3) is 1-y.  Applying (2) to each
box and summing by the triangle inequality is ALWAYS worse than the existing
Parseval dual bound N^(y+o(1)): its excess is at least 1298/3200=.405625.
The refined Theorem 6.1, whenever its p^(1/2) support condition holds, is
worse by at least about .4063 in its first term and .41625 in its second.

Even the stronger separable-weight Theorem 1.1 bound

    p^(1/4) X^(3/4) U^(3/4) Z^(7/8)                   (5)

would remain at least N^.265 above Parseval after granting a cost-free
separation of the hard endpoint.  That grant is stronger than the actual
hypotheses, so (5) cannot rescue (1).

The newer nearly-balanced convolution theorem of Wright,
arXiv:2608.27732v1, Theorem 2.2, also does not enter this box.  In its
notation the modulus range must satisfy Q<=N_2*X^(-epsilon), where N_2 is
one of the two convolution lengths and X is their product.  Here
Q=N^(59/100), while BOTH balanced factor lengths are strictly below
N^(59/100).  The upper range condition therefore fails before addressing
its fixed-residue/Siegel--Walfisz hypotheses or converting our Fourier-band
energy to its L1 discrepancy.  Source:

    https://arxiv.org/abs/2608.27732

The reason is structural: duality gives ||gamma||_2=1, but these published
bounds use only max|gamma_h|<=1.  They therefore do not exploit the norm that
an active-band energy estimate needs.  The target energy N^(1499/1000+o(1))
requires a per-modulus dual exponent at most 1499/2000=.7495.

THE LOW-PROJECTOR TERM IS PAID.
The +(p-1)^(-1) term in the exact centered kernel contributes at most

  |sum_h gamma_h|/(p-1) * |sum_(ab in J)mu(a)log(b)|
       <= N^(y+49/200-59/100+o(1))=N^(y-.345+o(1)).    (6)

This is at most N^.655, below .7495.  Thus the source mismatch concerns the
oscillating term (1), not a dropped centering correction.

DISPOSITION.
Direct use of these finite-field trilinear theorems is rejected: even after
the natural endpoint localization their upper bounds are polynomially weaker
than the Parseval estimate already known to fail on long blocks.  This does
not show (1) is large and does not reject trilinear methods using the Mobius
signs, the prime-p average, or an L2-sensitive theorem.  The balanced factors,
the exact pair-weight encoding, and the paid rank term remain useful.
"""

from fractions import Fraction as F


MODULUS = F(59, 100)
BAND = F(49, 100)
DUAL_TARGET = F(1499, 2000)


def balanced_trilinear_budget(block_exponent, mobius_exponent,
                              localization_exponent=None):
    """Return exact source-bound exponents for a localized balanced block."""
    y, alpha = block_exponent, mobius_exponent
    if type(y) is not F or type(alpha) is not F:
        raise ValueError("exponents must be exact Fractions")
    if not DUAL_TARGET < y <= 1:
        raise ValueError("block exponent must satisfy .7495<y<=1")
    if not F(41, 100) < alpha < F(59, 100):
        raise ValueError("Mobius exponent must lie strictly between .41 and .59")
    lam = 1 - y if localization_exponent is None else localization_exponent
    if type(lam) is not F or not 0 <= lam <= min(alpha, 1 - alpha):
        raise ValueError("invalid exact localization exponent")

    box_count = lam + max(F(0), lam + y - 1)
    supports = sorted((alpha - lam, 1 - alpha - lam, BAND), reverse=True)
    x, u, z = supports

    ps_pairwise = (box_count + MODULUS / 8 + F(7, 8) * x
                   + F(29, 32) * (u + z))
    ps_separable = (box_count + MODULUS / 4 + F(3, 4) * (x + u)
                    + F(7, 8) * z)
    refined_applicable = u <= MODULUS / 2
    refined_first = (box_count + MODULUS / 8 + F(7, 8) * x
                     + F(47, 52) * (u + z))
    refined_second = box_count + x + u + F(3, 4) * z
    rank_term = y + BAND / 2 - MODULUS

    return {
        "block": y,
        "mobius_factor": alpha,
        "log_factor": 1 - alpha,
        "localization": lam,
        "box_count": box_count,
        "ordered_cell_supports": tuple(supports),
        "parseval_dual": y,
        "dual_target": DUAL_TARGET,
        "ps_theorem_1_3": ps_pairwise,
        "ps_1_3_excess_over_parseval": ps_pairwise - y,
        "optimistic_ps_theorem_1_1": ps_separable,
        "ps_1_1_excess_over_parseval": ps_separable - y,
        "mpss_theorem_6_1_applicable": refined_applicable,
        "mpss_6_1_first": refined_first,
        "mpss_6_1_second": refined_second,
        "mpss_6_1_first_excess_over_parseval": refined_first - y,
        "mpss_6_1_second_excess_over_parseval": refined_second - y,
        "low_projector_rank_term": rank_term,
        "low_projector_fits_target": rank_term <= DUAL_TARGET,
        "wright_2_2_upper_range_possible": (
            MODULUS < max(alpha, 1 - alpha)),
    }


if __name__ == "__main__":
    for alpha in (F(42, 100), F(1, 2), F(58, 100)):
        print(alpha, balanced_trilinear_budget(F(3, 4), alpha))

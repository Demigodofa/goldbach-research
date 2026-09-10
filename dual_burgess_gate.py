"""Exponent gate for applying Burgess on the dual shift band.

Grant optimistically the prime-modulus Burgess shape
 L^(1-1/r) q^((r+1)/(4r^2))
for the whole dual interval L=q/H.  The Gauss/Poisson transform contributes
H/sqrt(q).  At q=N^.599,H=N^.1, every licensed integer r>=2 is worse
than the direct length-H bound.  Formally extending the exponent formula
to r=1 only reproduces H; r=1 is a Polya--Vinogradov/trivial endpoint
benchmark, not a sourced Burgess case.  A naive split of the actual
composite q=d*m into d progressions costs extra, but a genuinely bilinear
use of CRT/induced characters is not ruled out.  This rejects the direct
single-character plug-in only.

Primary formula checked 2026-09-10: Kerr--Shparlinski--Yau,
arXiv:1711.10582.  Their refined theorem covers r>2; r=2 uses the
classical Burgess bound quoted there.
"""
from fractions import Fraction as F

Q = F(599, 1000)
H = F(1, 10)


def burgess_dual_exponent(r, q_exponent=Q, shift_exponent=H):
    if not isinstance(r, int) or r < 2:
        raise ValueError("licensed Burgess parameter r>=2 required")
    if not all(isinstance(x, F) and 0 < x < 1
               for x in (q_exponent, shift_exponent)):
        raise ValueError("exact exponents in (0,1) required")
    length = q_exponent - shift_exponent
    if length <= 0:
        raise ValueError("require q>H")
    burgess = length * F(r - 1, r) + q_exponent * F(r + 1, 4 * r * r)
    return shift_exponent - q_exponent / 2 + burgess


def formal_r1_exponent(q_exponent=Q, shift_exponent=H):
    """Algebraic r=1 continuation for comparison only, not a source claim."""
    return shift_exponent


def excess_numerator(r, q_exponent=Q, shift_exponent=H):
    """4r^2 times the exponent excess over the direct H bound."""
    if not isinstance(r, int) or r < 1:
        raise ValueError("positive integer r required")
    return ((2 * q_exponent - 4 * shift_exponent) * r * r
            + (-3 * q_exponent + 4 * shift_exponent) * r
            + q_exponent)


def direct_burgess_gate(max_r=32):
    if not isinstance(max_r, int) or max_r < 2:
        raise ValueError("max_r>=2 required")
    values = tuple((r, burgess_dual_exponent(r)) for r in range(2, max_r + 1))
    return {
        "direct_shift_exponent": H,
        "burgess_exponents": values,
        "formal_r1_matches_direct": formal_r1_exponent() == H,
        "every_licensed_r_worse": all(value > H for _, value in values),
        "saving_proved": False,
    }


def top_factorization_identity(r):
    """Exact factorization of the top-block excess numerator."""
    if not isinstance(r, int) or r < 1:
        raise ValueError("positive integer r required")
    return F(r - 1) * (F(399, 500) * r - F(599, 1000))

"""Exact CRT/Gauss structure of the high-conductor shift band.

For q=d*m with (d,m)=1 and m prime, every high character is
chi=chi_d*chi_m with chi_m nonprincipal.  If W_q is the full periodized
shift kernel and What its unnormalized DFT, then

 sum_a W_q(a-N) conjugate(chi(a))
 =q^-1 sum_h What(h)e(-hN/q) G_q(conjugate(chi),h),

and CRT factors the Gauss sum exactly as
 G_d(conj(chi_d),h*inverse(m,d))*G_m(conj(chi_m),h*inverse(d,m)).
The active band has h exponent .499<m exponent .59, so m does not divide
nonzero h and the prime-component Gauss sum has magnitude sqrt(m).  The
d-component, target phase, endpoint leakage and sums over characters remain.
No spectral cancellation is proved here.
"""
from fractions import Fraction as F
from math import gcd

from major_arc_kernel import _factorization


def crt_additive_numerators(d, m, h, a):
    """Numerators mod dm proving e_dm(ha)=e_d(...)*e_m(...)."""
    if not all(isinstance(x, int) for x in (d, m, h, a)) or d < 1 or m < 1:
        raise ValueError("positive integer moduli and integer h,a required")
    if gcd(d, m) != 1:
        raise ValueError("coprime CRT factors required")
    q = d * m
    lhs = h * a % q
    rhs = (h * (a % d) * pow(m, -1, d) * m
           + h * (a % m) * pow(d, -1, m) * d) % q
    return lhs, rhs


def prime_component_gauss_status(m, h):
    """For a nonprincipal character mod prime m, m|h means zero; else sqrt(m)."""
    if not isinstance(m, int) or m < 2 or _factorization(m) != ((m, 1),):
        raise ValueError("prime modulus required")
    if not isinstance(h, int):
        raise ValueError("integer frequency required")
    return {"zero": h % m == 0,
            "magnitude_squared": 0 if h % m == 0 else m}


def active_band_exponents(d_exponent=F(9, 1000), m_exponent=F(59, 100),
                          shift_exponent=F(1, 10)):
    if not all(isinstance(x, F) and 0 < x < 1
               for x in (d_exponent, m_exponent, shift_exponent)):
        raise ValueError("exact exponents in (0,1) required")
    q = d_exponent + m_exponent
    h = q - shift_exponent
    return {"q": q, "h": h, "m": m_exponent,
            "h_below_m_margin": m_exponent - h,
            "prime_gauss_magnitude": m_exponent / 2,
            "d_gauss_component_paid": False,
            "target_phase_retained": True,
            "spectral_saving_proved": False}

"""One exact active-band inequality, and its resonant-coefficient stress test.

This module states a concrete candidate energy input for the critical top
cofactor box. It is a CONJECTURAL prime-discrepancy estimate, not a theorem.
It becomes sufficient only after a separate transfer controls the actual
shift-dependent endpoints, kernel coefficients and mask leakage.

For an integer N tending to infinity, put

  H=floor(N^(1/10)), B=floor(2*N^(9/1000)),
  M=floor(N^(59/100)), L=log N,

and assume 2*B<H and 4*N^(599/1000)<N/8.  For every prime
M<m<=2M, choose one integer interval J_m=(U_m,V_m] satisfying

  N/8 <= U_m < V_m <= 7N/8,       V_m-U_m >= N/16.          (1)

The interval may depend on m.  For 1<=d<=B, mu(d)!=0, (d,m)=1, set
q=d*m.  For reduced p,a define the exact normalized high projector

  P_(d,m)(a,p)=1_(p=a mod q)-(m-1)^(-1)1_(p=a mod d).       (2)

With e_q(x)=exp(2*pi*i*x/q), define, for every 0<=h<q,

  F_(d,m)(h;J_m)
   =e_q(-h*N) sum_(p prime in J_m) log(p)
                    sum_(a mod q,(a,q)=1)P_(d,m)(a,p)e_q(-h*a).  (3)

The target phase is displayed even though it disappears from |F|.  Define

For 0<=h<q let h_tilde be its signed representative in (-q/2,q/2]. With
the saved angular convention
`C0(s)=2*pi*integral chi(t)^2 exp(i*s*t)dt`, `supp chi` contained in
`(1,2)`, and finite DFT `e_q(-h*r)`, put

  B_q={h: q/(2*pi*H)<|h_tilde|<q/(pi*H)}, A_q={0,...,q-1},

  E_S=sum_(d<=B) mu(d)^2 sum_(M<m<=2M,m prime)
       (log(m))^2/(d*m) sum_(h in S_(d*m)) |F_(d,m)(h;J_m)|^2. (4)

Exact proposed inequality: there is an absolute C such that, for all
sufficiently large N and every interval family satisfying (1),

                    E_B <= C*(log N)^20/H * E_A.            (P)

The exponent 20 is a fixed disposable logarithmic allowance. The power
H^(-1)=N^(-1/10+o(1)) is the essential assertion.  It would give H^(-1/2)
after Cauchy and change the inherited top-box loss N^.049 to N^(-.001),
IF a separate transfer lemma also retains the physical endpoint and mask
weights without a power loss. No such transfer is proved here.

For active h, 0<|h_tilde|<m because 2B<H. Hence m does not divide the
unsigned residue h (since q=d*m). Summing (2) over a gives the useful exact form

  F/e_q(-hN)=sum_(p prime in J_m)log(p)
       [e_q(-h*p)+(m-1)^(-1)e_d(-h*inverse(m,d)*p)],         (5)

where the second exponential is 1 when d=1.  The principal prime-density
terms in the two brackets cancel: c_(dm)(h)/phi(dm) equals
-c_d(h)/(phi(d)*(m-1)), while the correction contributes the opposite
quantity.  Thus the elementary Ramanujan resonance is absent.  This is
only centering; it gives no bound for the remaining discrepancy.

RESONANT STRESS TEST.  (P) cannot hold after replacing the fixed prime-log
coefficients by arbitrary complex coefficients of the same magnitude.  In
the d=1, q=m model, put one coefficient on each nonzero residue p and take
c_p=e_m(h0*p), where h0 is any member of B_m.  The high-projector Fourier
coefficient has magnitude

  m-1-1/(m-1) at h=h0,  m/(m-1) at every other nonzero h,
  and 0 at h=0.

Consequently the single resonant mode contains the fraction
(m-2)/(m-1) of the total energy.  This tends to 1, rather than H^(-1).
The counterexample falsifies a coefficient-uniform large-sieve version of
(P), but not (P) itself: the actual coefficients are the fixed positive
prime weights log(p), and their uniform reduced-residue main is annihilated
by (2).  Any proof must exploit that arithmetic centering or a comparable
prime input; norm bounds for arbitrary coefficients cannot suffice.
"""
from fractions import Fraction as F
from math import gcd, pi

from high_character_collapse import high_projector


def critical_exponent_receipt():
    """Exact powers in the critical d,m,h box."""
    shift = F(1, 10)
    divisor = F(9, 1000)
    companion = F(59, 100)
    modulus = divisor + companion
    frequency = modulus - shift
    return {
        "shift": shift,
        "short_divisor": divisor,
        "prime_companion": companion,
        "modulus": modulus,
        "active_frequency": frequency,
        "frequency_below_companion": companion - frequency,
        "old_loss": F(49, 1000),
        "conditional_net": F(49, 1000) - shift / 2,
        "prime_energy_inequality_proved": False,
    }


def active_modes(modulus, shift_length):
    """DFT indices in q/(2*pi*H)<|signed h|<q/(pi*H).

    Python's ``pi`` is used only to enumerate finite diagnostic fixtures; the
    mathematical statement above uses the exact constant pi.
    """
    if not all(type(value) is int for value in (modulus, shift_length)):
        raise ValueError("integer modulus and shift length required")
    if modulus < 2 or shift_length < 2:
        raise ValueError("modulus and shift length must be at least two")
    lower = modulus / (2 * pi * shift_length)
    upper = modulus / (pi * shift_length)
    modes = []
    for h in range(1, modulus):
        signed = h if h <= modulus // 2 else h - modulus
        if lower < abs(signed) < upper:
            modes.append(h)
    return tuple(modes)


def uniform_reduced_residue_output(d, m):
    """Apply the high projector to one equal coefficient per reduced residue."""
    q = d * m
    units = tuple(value for value in range(1, q + 1)
                  if gcd(value, q) == 1)
    return tuple(sum(high_projector(d, m, residue, p) for p in units)
                 for residue in units)


def _mobius(value):
    if type(value) is not int or value < 1:
        raise ValueError("positive integer required")
    result = 1
    prime = 2
    remainder = value
    while prime * prime <= remainder:
        if remainder % prime == 0:
            remainder //= prime
            result = -result
            if remainder % prime == 0:
                return 0
            while remainder % prime == 0:
                remainder //= prime
        prime += 1
    return -result if remainder > 1 else result


def _totient(value):
    result = value
    prime = 2
    remainder = value
    while prime * prime <= remainder:
        if remainder % prime == 0:
            result -= result // prime
            while remainder % prime == 0:
                remainder //= prime
        prime += 1
    if remainder > 1:
        result -= result // remainder
    return result


def ramanujan_sum(modulus, frequency):
    """Exact c_modulus(frequency)."""
    if type(modulus) is not int or modulus < 1 or type(frequency) is not int:
        raise ValueError("positive integer modulus and integer frequency required")
    common = gcd(modulus, frequency)
    quotient = modulus // common
    return _mobius(quotient) * _totient(modulus) // _totient(quotient)


def ramanujan_main_cancellation(d, m, h):
    """The two normalized uniform-prime main coefficients in (5)."""
    if type(h) is not int or h % m == 0:
        raise ValueError("require an integer frequency not divisible by m")
    # This validates d, prime m, coprimality, and the reduced-unit setting.
    high_projector(d, m, 1, 1)
    inverse_m = 0 if d == 1 else pow(m, -1, d)
    first = F(ramanujan_sum(d * m, h), _totient(d * m))
    correction = F(ramanujan_sum(d, h * inverse_m),
                   (m - 1) * _totient(d))
    return first, correction, first + correction


def resonant_energy_ratio(prime_modulus, shift_length, resonant_mode=None):
    """Exact band/all ratio for c_p=e_m(h0*p), one p per nonzero residue."""
    high_projector(1, prime_modulus, 1, 1)
    modes = active_modes(prime_modulus, shift_length)
    if not modes:
        raise ValueError("active band is empty")
    if resonant_mode is None:
        resonant_mode = modes[0]
    if resonant_mode not in modes:
        raise ValueError("resonant mode must lie in the active band")
    m = prime_modulus
    peak = F(m - 1) - F(1, m - 1)
    off_peak = F(m, m - 1)
    band = peak * peak + (len(modes) - 1) * off_peak * off_peak
    total = peak * peak + (m - 2) * off_peak * off_peak
    return {
        "band_energy": band,
        "all_energy": total,
        "ratio": band / total,
        "single_mode_fraction": peak * peak / total,
        "uniform_H_inverse_target": F(1, shift_length),
        "actual_prime_log_inequality_falsified": False,
        "arbitrary_coefficient_extension_falsified":
            band * shift_length > total,
    }

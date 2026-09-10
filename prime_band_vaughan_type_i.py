"""Vaughan Type I terms fit the absolute active-band energy budget.

Owner: Kevin's Goldbach research.  Purpose: average the exact Vaughan pieces
over the dense ``(d,m,h)`` family before taking absolute values.  This proves
the Type I pieces affordable for the associated absolute benchmark; it does
not prove ``active_band_energy_conjecture.py``, its relative ``E_band/E_all``
formulation, the remaining Type II estimate, or the endpoint/kernel transfer
to the Goldbach overlap.

SETUP AND THE ABSOLUTE BENCHMARK.
Keep exactly

  H=floor(N^(1/10)), B=floor(2*N^(9/1000)), M=floor(N^(59/100)),
  M<m<=2M prime, 1<=d<=B squarefree, (d,m)=1, q=dm,
  J_m=(U_m,V_m], N/8<=U_m<V_m<=7N/8, |J_m|>=N/16,
  B_q={h: q/(2*pi*H)<|h_tilde|<q/(pi*H)}.                 (1)

For active h, m does not divide h.  With e_s(x)=exp(2*pi*i*x/s) and
``mbar`` the inverse of m modulo d (with e_1=1), the exact full-minus-low
kernel from the high-character collapse is

  K_(d,m,h)(n)=e_q(-h*n)+(m-1)^(-1)e_d(-h*mbar*n).         (2)

The harmless target factor e_q(-hN) has absolute value one and is suppressed
below.  The application-level H^-1 absolute benchmark is

  N^(1+Bexp+Mexp-Hexp+o(1))=N^(1499/1000+o(1)).            (3)

This is the diagonal scale N times the number B*M of modulus pairs, divided
by H.  Equation (3) is an absolute sufficient budget used in the overlap
calculation.  An absolute bound does not by itself prove the stronger relative
statement E_band <= L^20 E_all/H when E_all happens to be smaller.

EXACT COPRIMALITY-TWISTED VAUGHAN IDENTITY.
For each q let f_q(n)=1_((n,q)=1), a completely multiplicative function.
Multiplying the exact Vaughan identity by f_q gives

 f_q*Lambda = (f_q*Lambda_<=U)
  +(f_q*mu_<=V)*(f_q*log)
  -(f_q*mu_<=V)*(f_q*Lambda_<=U)*(f_q*1)
  +(f_q*mu_>V)*(f_q*Lambda_>U)*(f_q*1),                   (4)

where every star displayed between parenthesized sequences is Dirichlet
convolution; the left side means pointwise multiplication f_q(n)Lambda(n).
The essential free convolution factor 1 is retained.  Take

                         U=V=floor(N^(3/40)).              (5)

Every prime in J_m exceeds q for large N, hence f_q(p)=1.  The first term in
(4) vanishes on J_m.  The next two Type I pieces are exactly

 I_1(h)=sum_(a<=V,(a,q)=1) mu(a)
          sum_(ab in J_m,(b,q)=1) log(b) K_(d,m,h)(ab),    (6)

 I_2(h)=-sum_(c<=UV,(c,q)=1) C_c
          sum_(ck in J_m,(k,q)=1) K_(d,m,h)(ck),           (7)

 C_c=sum_(ab=c,a<=V,b<=U)mu(a)Lambda(b),  |C_c|<=log c.   (8)

The remaining exact Type II term is

 T_II(h)=sum_(a>V,(a,q)=1)mu(a)
          sum_(b>U,(b,q)=1) B_U(b) 1_(ab in J_m)
                    K_(d,m,h)(ab),                         (9)
 B_U(b)=sum_(r|b,r>U)Lambda(r), 0<=B_U(b)<=log b.

No individual prime is being factored: (4) is applied to the full Lambda sum.

THE RESIDUE-ENERGY LEMMA.
Fix a short factor c coprime to q and let w be either 1 or log.  For unit
residues r modulo q put

 A_r=sum_(b in J_m/c, b=r mod q) w(b),
 Abar=phi(q)^(-1)sum_r A_r, delta_r=A_r-Abar.              (10)

Uniformly in the hard interval endpoints,

                   max_r |delta_r| << log N               (11)

for w=log, and <<1 for w=1.  Indeed two progressions have counts differing
by at most one.  Pair their ordered terms.  Paired arguments differ by less
than q, start above N/(8c), and there are O(N/(cq)+1) of them, so the sum of
their logarithmic differences is O(1); a possible unpaired endpoint costs
O(log N).  This proof uses c<=UV=N^(3/20) and q<=4N^(599/1000), so the lower
endpoint is much larger than q.  It retains both hard endpoints.

For every active h the Abar contribution cancels exactly:

 sum_(r mod q,(r,q)=1) K_(d,m,h)(c*r)
 =c_q(h)+(m-1)^(-1)(m-1)c_d(h)=0,                         (12)

because c is a unit, c_(dm)(h)=c_d(h)c_m(h), and c_m(h)=-1 when m does
not divide h.  This remains true when (h,d)>1.

Apply Parseval first to the q-transform of delta_r and then to the d-transform
in the low term.  Each unit class modulo d has m-1 unit lifts modulo q, so

 sum_(h mod q)|sum_r delta_r K_(d,m,h)(c*r)|^2
 <=2q sum_r|delta_r|^2
   +2*m*d/(m-1)^2 sum_(s mod d)|sum_(r=s mod d)delta_r|^2
 <=4q sum_r|delta_r|^2.                                  (13)

Thus the same sum over the active subset is O(q^2 log(N)^2) for w=log
and O(q^2) for w=1.  This is genuine averaging over h before absolute values.

TYPE I BUDGETS.
Cauchy only across the actual short factors gives, from (6),

 sum_(h in B_q)|I_1(h)|^2 << V^2 q^2 log(N)^2,             (14)

and from sum|C_c|^2<<UV log(N)^2 and (7),

 sum_(h in B_q)|I_2(h)|^2 << (UV)^2 q^2 log(N)^2.          (15)

Insert the exact outer weight mu(d)^2(log m)^2/q and sum q=dm.  Since
sum_(d<=B)d<<B^2 and sum_(M<m<=2M,m prime)m<<M^2, the power exponents are

 I_1: 2*(9/1000+59/100)+2*(3/40)=337/250=1.348,
 I_2: 2*(9/1000+59/100)+2*(3/20)=749/500=1.498.            (16)

Both are below 1499/1000; the harder term has the exact margin 1/1000.
All omitted factors are fixed powers of log N and fit the saved allowance.

Replacing Lambda by prime-only log weights introduces proper prime powers.
Their pointwise mass is N^(1/2+o(1)).  There are O(q/H) active modes, and
the q^-1 outer weight cancels q, so after all B*M modulus pairs their energy
is N^(1-1/10+9/1000+59/100+o(1))=N^(1499/1000+o(1)).       (17)
This reaches, but does not exceed, the benchmark.

DISPOSITION AND A CLEANER EXACT SPLIT.
The Type I terms are proved affordable in the full d,m family.  There is a
cleaner asymmetric specialization.  Take

                         U=1, V=floor(N^(3/20)).             (18)

Because Lambda_<=1 is identically zero, both the low-Lambda and grouped
subtraction terms vanish.  The sole Type I term is (6), now with
V=N^(3/20); its exponent is exactly 749/500=1.498.  The entire remainder is
the elementary Mobius-inversion tail

 T_mu(h)=sum_(a>V,(a,q)=1)mu(a)
          sum_(ab in J_m,(b,q)=1)log(b)K_(d,m,h)(ab).       (19)

Indeed Lambda=mu*log, split at a=V.  This retains the same 1/1000 margin,
removes B_U and every grouped Type II coefficient, and forces the Mobius
factor above N^(3/20), which is N^(1/20) longer than H.  It does not itself
prove cancellation when all a>V are recombined.

The remaining arithmetic question can therefore be narrowed to

 sum_(d<=B)mu(d)^2 sum_(M<m<=2M prime,(d,m)=1)(log m)^2/(dm)
   *sum_(h in B_(dm)) |T_mu(d,m,h;J_m)|^2
                         << N^(1499/1000+o(1)),             (20)

uniformly in every interval family (1), with T_mu exactly (19).  Its literal
coefficient diagonal is on the scale (3), up to logarithmic factors; the
Mobius-weighted off-diagonal congruences are still open.  Equations (13)--(19)
neither estimate them nor turn formal cancellation into a prime-correlation
bound.  The balanced B_U form (9) remains valid if it becomes useful with a
different arithmetic input; it is no longer the narrowest target.
"""

from fractions import Fraction as F
from math import gcd

from unexceptional_vaughan_gate import vaughan_log_vectors


def band_type_i_budgets():
    """Exact exponent ledger for the balanced and U=1 splittings."""
    b, m, h = F(9, 1000), F(59, 100), F(1, 10)
    u = v = F(3, 40)
    base_modulus_energy = 2 * (b + m)
    benchmark = 1 + b + m - h
    return {
        "short_lambda": u,
        "short_mobius": v,
        "modulus_pair_energy": base_modulus_energy,
        "linear_type_i": base_modulus_energy + 2 * v,
        "grouped_type_i": base_modulus_energy + 2 * (u + v),
        "proper_powers": benchmark,
        "absolute_band_benchmark": benchmark,
        "grouped_margin": benchmark - (base_modulus_energy + 2 * (u + v)),
        "mobius_split_lambda_cutoff": F(0),
        "mobius_split_mobius_cutoff": F(3, 20),
        "mobius_split_type_i": base_modulus_energy + 2 * F(3, 20),
        "mobius_split_grouped_term_zero": True,
        "type_ii_energy_proved": False,
        "relative_band_conjecture_proved": False,
    }


def unit_residue_deviations(modulus, low, high, weights=None):
    """Exact A_r-Abar on low<n<=high, indexed by unit residues modulo q.

    ``weights`` is either None (constant one) or a mapping containing an exact
    Fraction for every retained integer.  This finite helper checks the residue
    and Parseval algebra; the logarithmic discrepancy estimate is analytic.
    """
    if (type(modulus) is not int or type(low) is not int or type(high) is not int
            or modulus < 1 or not 0 <= low < high):
        raise ValueError("require an exact positive modulus and 0<=low<high")
    units = tuple(r for r in range(modulus) if gcd(r, modulus) == 1)
    totals = {r: F(0) for r in units}
    for n in range(low + 1, high + 1):
        if gcd(n, modulus) != 1:
            continue
        value = F(1) if weights is None else weights[n]
        if type(value) is not F:
            raise ValueError("every supplied weight must be an exact Fraction")
        totals[n % modulus] += value
    average = sum(totals.values(), F(0)) / len(units)
    return tuple((r, totals[r] - average) for r in units)


def continued_active_kernel_parseval_energy(d, prime_modulus, short_factor,
                                            deviations):
    """Full-h energy of (2)'s algebraic continuation, bounding active h.

    Formula (2) equals the high projector only when ``m`` does not divide h.
    At multiples of m the true high projector is zero.  Extending (2) to all
    h is used solely as a nonnegative Parseval majorant of its active subset.
    """
    if (type(d) is not int or type(prime_modulus) is not int
            or type(short_factor) is not int or d < 1 or prime_modulus < 2
            or gcd(d, prime_modulus) != 1):
        raise ValueError("positive coprime factors and an integer short factor required")
    q = d * prime_modulus
    if gcd(short_factor, q) != 1:
        raise ValueError("short factor must be a unit modulo q")
    values = dict(deviations)
    units = {r for r in range(q) if gcd(r, q) == 1}
    if set(values) != units or any(type(v) is not F for v in values.values()):
        raise ValueError("one exact Fraction deviation per unit residue required")
    if sum(values.values(), F(0)) != 0:
        raise ValueError("residue deviations must have mean zero")
    vector = [F(0) for _ in range(q)]
    inverse_m = 0 if d == 1 else pow(prime_modulus, -1, d)
    for residue, value in values.items():
        vector[(short_factor * residue) % q] += value
        low_location = (prime_modulus * inverse_m * short_factor * residue) % q
        vector[low_location] += value / (prime_modulus - 1)
    return q * sum((value * value for value in vector), F(0))


def twisted_vaughan_log_vectors(n, lambda_cutoff, mobius_cutoff, modulus):
    """Exact log-prime vectors in (4), including the f_q coprimality mask."""
    if (type(modulus) is not int or modulus < 1 or type(n) is not int or n < 1):
        raise ValueError("positive integer n and modulus required")
    if gcd(n, modulus) != 1:
        return ((), (), (), ())
    return vaughan_log_vectors(n, lambda_cutoff, mobius_cutoff)


def mobius_tail_log_vector(n, mobius_cutoff):
    """Exact log-prime vector of sum_(ab=n,a>V)mu(a)log(b)."""
    if type(n) is not int or n < 1 or type(mobius_cutoff) is not int or mobius_cutoff < 1:
        raise ValueError("positive integer n and Mobius cutoff required")
    return vaughan_log_vectors(n, 1, mobius_cutoff)[3]

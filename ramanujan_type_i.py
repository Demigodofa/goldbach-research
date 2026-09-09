"""Two-scale signed comparison: absolute Type I and a positive cross term.

Owner: Kevin's research. Purpose: retain the distribution-compatible
comparison and verify its exact progression and mixed-scale identities.
Finite rational tests verify algebra, not analytic estimates or prime counts.

Setup and scope:
Let I=(Y/2,Y], m even in [5Y/4,7Y/4], J_m={n:n,m-n in I}. Fix
0<eps<1/12 and a sufficiently small fixed delta>0, delta<=1/4800.
Put S=Y**delta, R=S**12, gamma=1/2-eps. Both scales eventually satisfy
the lower bound exp(log(Y)**(4/5)); R<=Y**(1/400). Use the same fixed
smooth nonnegative cutoff G of major_arc_kernel.py, equal to1 on[0,1]
and supported in[-2,2]. For T in {S,R}, write
  g_T(q)=G(log(q)/log(T)), Gamma_T=Lambda_{T,1},
  Xi_T(n)=chi_D(n)*D/phi(D)*Lambda_{T,D}(n),
  M_T(n)=1_I(n)*(Gamma_T(n)-n**(beta-1)*Xi_T(n)).
Use ONE common exceptional-zero alternative at level R**4 and fixed small
quality kappa. This result covers the unexceptional branch (omit Xi, mu=1)
and an actual exceptional primitive quadratic character with
  24<D<=S**(1/4), t=(1-beta)*log(Y), mu=min(1,t).
There is NO claim here for the other exceptional-conductor regimes.

The two conclusions, uniformly for these even m, are
  sum_{d<=Y**gamma} max_{interval K}
    |sum_{k in K, dk in J_m}(Lambda(m-dk)-M_S(m-dk))|
        <<_{A,eps,delta,G} Y/log(Y)**A                 (TI)
for every fixed A>0, and, with F(n)=1_I(n)*log(n)*1_prime(n),
  (F*M_S)(m) >>_{delta,G} Y*S_2(m)*mu.                (CROSS)
TI is ABSOLUTE, not a bound relative to mu. Its constants/onset can be
ineffective. CROSS is a prime-versus-SIGNED-model correlation: it is not
an actual prime-pair lower bound. A Type II estimate, a mu-relative transfer
on strongly suppressed classes, and the other conductor regimes remain open.
No new Goldbach coverage, numerical onset, actual zero, or priority claim.

Proof of TI:
1. Primitive additive frequencies give the exact complete-progression mean
     mean_k c_q(m-dk)=1_{q|d}*c_q(m).
   Each Gamma_S component has amplitude O_G(1), period<=q<=S**2.
   Thus its interval sum differs from its length times the mean by
   O_G(S**4), after summing components. Without truncation the mean is
     sum_{q|d}mu(q)*c_q(m)/phi(q)=d/phi(d)*1_{(d,m)=1}.
   This follows prime by prime, including nonreduced residues. The missing
   terms have q>S. Summing their length-weighted absolute values over d
   costs at most
     O_G(Y*log(Y)*sum_{q>S}mu(q)**2*|c_q(m)|/(q*phi(q)))
       << Y*log(Y)*S**(-1/2)*exp(O(sqrt(log(Y)))).
   For the last bound use Rankin with exponent1/2. Its local factor is
   1+|c_p(m)|/(sqrt(p)*(p-1)); the product converges away from p|m.
   The remaining factors are bounded by exp(O(sqrt(log(Y)))), uniformly
   in m, by the prime-divisor split used in signed_pair_main_term.py.
   The summed interval discrepancy is O_G(Y**gamma*S**4).
2. Bombieri--Vinogradov with maximum over reduced residues and endpoints,
   followed by log-Abel summation, compares Lambda with the full density.
   Ford, Sieve Methods2023, Theorem3.4 (printed p35):
   https://ford126.web.illinois.edu/sieve2023.pdf
   The fixed power gap eps permits any fixed logarithmic saving. For a
   short K retain the endpoint error; integer length versus real length
   costs O(sum_{d<=Y**gamma}d/phi(d)), also power-small. Nonreduced
   progressions in this range contain only proper prime powers, because
   m-dk>Y/2>d. Count divisors d of each nonzero m-p**j to bound their
   total weighted contribution by Y**(1/2+o(1)). This also allows F in
   place of Lambda in TI. No proper prime power is called a prime.
3. For (q,D)=1, chi_D(n)*c_q(n) has only primitive additive frequencies
   of denominator Dq, by primitivity and CRT. Its progression mean is zero
   unless Dq|d; when that holds it is chi_D(m)*c_q(m). Therefore the
   normalized Xi_S contribution can resonate only at these d. Component
   amplitudes sum to O_G(S**2), and periods are<=S**2, giving O_G(S**4)
   discrepancy per progression, also after Abel with n**(beta-1).
   The summed absolute resonant means are bounded by
     O_G(Y*log(Y)/phi(D)
             *sum_q mu(q)**2*|c_q(m)|/(q*phi(q)))
       << Y*log(Y)**2/phi(D).
   Here the full Euler product is at most a fixed constant times
   prod_{p|m}(1+1/p)<=sum_{d|m}1/d<<log(Y), not merely Y**o(1).
4. The level-R**4 exceptional quality gives
     1-beta <= kappa/(48*delta*log(Y)).
   Write beta=1-1/(eta*log(D)). Siegel's bound eta<<_a D**a for every
   fixed a>0 (ineffective), as in Matomaki--Merikoski equation(6), gives
     D >>_{A,delta} log(Y)**A for every fixed A.
   https://arxiv.org/html/2112.11412v2
   Absorb log(D) into an arbitrarily small D power when combining these
   inequalities. The elementary phi(D)>=sqrt(D/2) now makes step3 smaller
   than every fixed requested log saving. The principal and period errors
   are power-small. This proves TI in the stated branches.

Proof of CROSS:
5. The fine prime decomposition already checked in prime_pair_transfer.py
   is F=M_R+E_R+V_R, with
     |E_R(n)|<< e_R*Htilde_R(n), ||V_Rhat||inf<<Y*R**(-1/3),
   where e_R=exp(-c*kappa/(12*delta)) in the unexceptional branch and
   e_R=t*exp(-c/(12*delta)) in the exceptional branch. Its primary source
   is https://arxiv.org/html/2508.16400v2#S7.SS3 , Lemma7.4 and(7.10),
   with the explicitly repaired radical majorant in major_arc_kernel.py.
   That earlier proof charges endpoints and removes proper prime powers.
6. The complete-period identities of signed_pair_main_term.py apply with
   different left and right cutoffs: replace g(q)**2 by g_R(q)*g_S(q)
   and g(Dq)**2 by g_R(Dq)*g_S(Dq). They give respectively U0 and
   D*B/phi(D)**2*UD, D*C/phi(D)**2*UD for the mixed and quadratic terms.
   Since R>=S**2, g_R=1 at every nonzero coarse sample. Thus the products
   reduce to g_S, not g_S**2. The same Rankin tails and D<=S**(1/4) give
     M_R*M_S(m)=S_2(m)/A*sum_{n in J_m}P(v(n),v(m-n))
                  +O_G(Y*S**(-1/3)+R**4*S**4).
   The interval error follows from total component amplitudes O(R**2),
   O(S**2), and pair periods at most R**2*S**2, then Abel summation.
   A,B,C,P are the finite character quantities of exceptional_character_model.
   In the unexceptional branch the main term is |J_m|*S_2(m).
7. The proved inequality 5P>=3Splus and |C|<=A give
     P>=3/4*(A+u*v*C)>=3/4*A*(1-u*v).
   On J_m, n(m-n)>=Y for large Y, hence 1-u*v>=1-exp(-t)>=mu/2.
   With |J_m|>=Y/4-O(1), this gives the claimed positive main margin.
8. The coarse model has Fourier L1 norm O_G(S**2*log(Y)). For Gamma_S,
   each normalized Ramanujan component has total absolute additive
   coefficients |mu(q)|, and there are O(S**2) components. For Xi_S,
   primitive Gauss sums give character coefficient L1=phi(D)/sqrt(D),
   which is at most sqrt(D). Multiplying
   by D/phi(D) and summing q<=S**2/D gives at most
     O(S**2*sqrt(D)/phi(D))=O(S**2).
   An interval Dirichlet kernel has L1 O(log(Y)), and the weight v has
   bounded variation. Therefore
     |V_R*M_S|<<Y*R**(-1/3)*S**2*log(Y)=Y*S**(-2)*log(Y).
9. Directly from the corrected local factors, Htilde_R<=12*Htilde_S:
   the factors decrease with scale and log(R)=12*log(S). Also
   |M_S|<<_G Htilde_S. The checked Henriot correlation in
   radical_majorant_correlation.py therefore yields
     |E_R*M_S|<<_G e_R*delta**(-2)*Y*S_2(m).
   In the exceptional branch t/mu<=max(1,kappa/(48*delta)), so choosing
   fixed delta sufficiently small absorbs this error into the margin.
   This uses the corrected 2014 theorem, not the uncorrected Henriot source.
10. The effective elementary zero gap 1-beta>>D**(-1/2)/log(D)**2
   used in signed_pair_main_term.py gives mu>>S**(-1/7) eventually.
   Consequently Y*S**(-1/3), Y*S**(-2)*log(Y), and
   R**4*S**4=S**52 are o(Y*mu) for the chosen delta. This proves CROSS.

This repairs two prerequisites simultaneously, within the stated regime.
It does not justify treating the absolute TI error as o(Y*mu); nor does
it estimate the remaining prime-weighted or composite-bilinear residual.
The subsequent proof in relative_type_i.py now supplies the stronger
TI bound O_A(Y*mu/log(Y)**A), after decreasing the fixed delta upper
bound independently of A. That proof uses additional zero-repulsion and
large-sieve inputs, with ineffective onset. The remaining prime-weighted
or composite-bilinear residual is still unproved.
"""
from fractions import Fraction
from math import gcd

from exceptional_character_model import character_values, pair_moments
from major_arc_kernel import _mobius_phi, ramanujan


def _check_samples(samples: tuple[int | Fraction, ...]) -> None:
    if len(samples) < 2 or any(type(g) not in (int, Fraction) for g in samples):
        raise ValueError("samples must include index1 and contain exact rationals")


def _check_sign(conductor: int | None, two_sign: int) -> None:
    if type(two_sign) is not int or two_sign not in (-1, 1):
        raise ValueError("two_sign must be integer -1 or 1")
    if conductor is None and two_sign != 1:
        raise ValueError("two_sign=-1 needs a conductor with an 8-component")


def progression_means(target: int, step: int,
                      samples: tuple[int | Fraction, ...],
                      conductor: int | None = None, *, two_sign: int = 1
                      ) -> tuple[Fraction, Fraction]:
    """Exact means of Gamma(target-step*k), Xi(target-step*k) over k.

    The period is complete. Samples[k] is an arbitrary rational g(k), with
    index0 unused and zero samples beyond the supplied tuple. These are
    unweighted periodic means, not means of n**(beta-1)*Xi. A conductor
    specifies a primitive real character; no exceptional zero is assumed.
    Enumeration and factoring are intended for small algebra checks only.
    """
    if type(target) is not int or type(step) is not int or step < 1:
        raise ValueError("require integer target and positive integer step")
    _check_samples(samples)
    _check_sign(conductor, two_sign)
    if conductor is not None:
        chi = character_values(conductor, two_sign=two_sign)
        _, phi_d = _mobius_phi(conductor)
    principal, exceptional = Fraction(0), Fraction(0)
    for q in range(1, len(samples)):
        mu, phi = _mobius_phi(q)
        coefficient = Fraction(mu*ramanujan(q, target), phi)
        if step % q == 0:
            principal += coefficient*samples[q]
        if (conductor is not None and gcd(q, conductor) == 1
                and q*conductor < len(samples) and step % (q*conductor) == 0):
            exceptional += coefficient*samples[q*conductor]
    if conductor is not None:
        exceptional *= Fraction(conductor*chi[target % conductor], phi_d)
    return principal, exceptional


def mixed_pair_coefficients(target: int, left: tuple[int | Fraction, ...],
                            right: tuple[int | Fraction, ...],
                            conductor: int | None = None, *, two_sign: int = 1
                            ) -> tuple[Fraction, Fraction, Fraction]:
    """Exact Gamma-left/Gamma-right, Gamma-left/Xi-right, Xi-left/Xi-right.

    Xi-left/Gamma-right has the SAME mixed coefficient. Samples have the
    meaning in progression_means. Unequal lengths mean zero extension.
    Rational samples do not certify scale separation, smoothness, or any
    analytic error bound; all four complete-period correlations are exact.
    """
    if type(target) is not int or target % 2:
        raise ValueError("target must be an even integer")
    _check_samples(left)
    _check_samples(right)
    _check_sign(conductor, two_sign)
    if conductor is not None:
        _, b, c = pair_moments(conductor, target, two_sign=two_sign)
        _, phi_d = _mobius_phi(conductor)
    principal, restricted = Fraction(0), Fraction(0)
    end = min(len(left), len(right))
    for q in range(1, end):
        mu, phi = _mobius_phi(q)
        coefficient = Fraction(mu*mu*ramanujan(q, target), phi*phi)
        principal += coefficient*left[q]*right[q]
        if conductor is not None and gcd(q, conductor) == 1 and q*conductor < end:
            restricted += coefficient*left[q*conductor]*right[q*conductor]
    if conductor is None:
        return principal, Fraction(0), Fraction(0)
    return (principal, Fraction(conductor*b, phi_d*phi_d)*restricted,
            Fraction(conductor*c, phi_d*phi_d)*restricted)

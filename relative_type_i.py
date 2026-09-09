"""Character-relative Type I for the two-scale Ramanujan comparison.

Owner: Kevin's research. Purpose: close the relative-error prerequisite
left explicit in ramanujan_type_i.py. The exact helper checks character
lifting and normalization; it does not estimate primes or locate a zero.
Sol checked the deduction and actual files. Four focused exact tests passed
normally and with Python -O; they do not prove the analytic estimates.
Sol also checked the replacement bulk source deduction below; the executable
helpers were unchanged by that source repair.

Theorem, with the deduction independently checked by Sol:
Keep the setup, central band, common exceptional alternative and branches
of ramanujan_type_i.py. Decrease its fixed delta upper bound if necessary,
ONCE independently of A. Then for every fixed A>0,
  sum_{d<=Y**(1/2-eps)} max_{interval K}
    |sum_{k in K, dk in J_m}(Lambda(m-dk)-M_S(m-dk))|
      <<_{A,eps,delta,G} Y*mu/log(Y)**A.                 (RTI)
Here mu=1 in the unexceptional branch, and
mu=min(1,(1-beta)*log(Y)) when the actual exceptional conductor satisfies
24<D<=S**(1/4). Constants/onset are ineffective. This is the same signed
comparison, not a new positive sieve or an actual prime-pair estimate.
RTI and the proved positive CROSS still do NOT prove the required Type II
or fixed-coefficient prime-weighted residual estimate. Other exceptional
conductor regimes, numerical onsets and universal coverage remain open.

Source inputs:
* The needed bulk quantitative Linnik estimate is deduced below from
  Thorner--Zaman, Theorem2.1 and equation(4.2):
  https://arxiv.org/html/2108.10878#S2
  https://arxiv.org/html/2108.10878#S4
  For e=(1-beta)*log(q) sufficiently small, Y/2>=q**C, and I an interval
  in[Y/2,Y], the reduced progression sum has main
    integral_I (1-chi(a)*v**(beta-1))dv/phi(q)
  and error O((Y/phi(q))*(e**(c*log(Y)/log(q))+log(Y)**2/q)).
  Absolute c,C>0 are fixed. The log(1/e) gain remains essential.
  Tao's earlier exposition stated this type of estimate, but its proof of
  Proposition23 has an acknowledged unresolved gap. It is no longer the
  proof authority used here. Author correction:
  https://terrytao.wordpress.com/2015/02/22/254a-notes-7-linniks-theorem-on-primes-in-arithmetic-progressions/#comment-648901
* Drappeau--Fiorilli, The first moment of primes in arithmetic progressions:
  beyond the Siegel--Walfisz range, Lemma2.1:
  https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/tlm3.12030
  For 2<=W<=Q<=sqrt(Y), with an absolute fixed exponent C0,
    sum_{d<=Q}1/phi(d)*sum_{chi mod d, cond(chi)>W}
      max_{y<=Y}|psi(y,chi)|
      <<log(Y)**C0*(Y/W+Q*sqrt(Y)+Y**(5/6)).             (1)
  This is an estimate for ALL induced characters in the displayed range.
* The Siegel and exceptional-quality bounds already used in
  ramanujan_type_i.py imply, with L=log(Y),
    mu >>_a D**(-a) for every fixed a>0,
    D >>_H L**H for every fixed H>0.                    (2)
  Hence mu>=Y**(-h) eventually for each fixed h>0. This lower bound is
  uniform in the stated conductor range, but ineffective; no numerical
  expression or actual exceptional zero is supplied by (2).

Bulk source deduction, replacing the affected exposition:
Take density parameter3/5 and common height H=q^2 in Thorner--Zaman
Theorem2.1. For the sum over ALL characters modulo q, excluding beta,
  N_q^*(sigma,H)<<e*q**(24*(1-sigma)).
Put d0=min(1/4,log(1/e)/(48*log(q))). At sigma=1-d0 the last bound is
O(sqrt(e))<1 once e is small enough, so there are no other zeros there.
If d0=1/4, the high-zero range below is empty. Otherwise, for L=log(Y)
and Y>=q^48, integration of the density bound gives
  sum_{Re(rho)>3/4, |Im(rho)|<=H, rho!=beta}Y**(Re(rho)-1)
    << e*(q^24/Y)**d0
     = e**(1/2+L/(48*log(q))).
The integration factor L/(L-24*log(q)) is at most2, so no logarithm is lost.
Subtract (4.2) at the endpoints of I with the SAME height H. Constant
low-zero terms cancel; each remaining zero term is integral_I v**(rho-1)dv.
There are O(q^3*log(q)) zeros up to H, by the per-character unit-height
zero count also stated in Section4. Thus Re(rho)<=3/4 contributes at most
O(Y**(3/4)*q^3*log(q)/phi(q)). The explicit remainders, and the O(sqrt(Y))
cost of passing between primes and Lambda, are all absorbed by
  O((Y/phi(q))*L^2/q)
when Y/2>=q^C for a sufficiently large fixed C. In particular no individual
bound for a reflected zero near0 is needed. The high zeros give the claimed
e-power term, with the exceptional beta retained in the displayed main.
This proves exactly the bulk interval estimate used below and in
rare_prime_sieve.py and rare_twisted_bv.py. Decreasing the same fixed delta
if necessary supplies exponents8 and28 at every required lifted modulus;
it does not add a new hypothesis about the actual zero.

Proof:
1. Fix A. The branch mu=1 is already proved. If mu>=L**(-B), the earlier
   absolute TI with saving A+B proves RTI. B is fixed below and can depend
   on A. It remains to consider 0<mu<L**(-B), where mu=(1-beta)*L.
   Let K0=A+C0+5, Q=Y**(1/2-eps), W=ceil(mu**(-2)*L**K0).
   By (2), eventually W<=D**(1/4), 2<=W<=Q, and W=Y**o(1). To see
   the first inequality, bound mu**(-2) by an arbitrarily small fixed
   power of D and L**K0 by another such power, absorbing constants.
2. For each primitive character chi_r of conductor r<=W, including r=1,
   lift chi_r and chi_D to q=lcm(D,r). Then
     D<=q<=D*W<=D**(5/4)<=Y**(5*delta/16).
   Choose fixed delta small enough that y>=q**C and
   c*log(y)/log(q)>=8 for all y in[Y/2,Y], once Y is large.
   The zero remains a zero after inducing the character to q, and
     e=(1-beta)*log(q)<=5*delta*mu/16.
   It meets the smallness premise in the present branch. Apply the source
   progression formula and sum over the reduced residues with weight
   chi_r(a). The principal projection is 1 for r=1 and 0 otherwise.
   The exceptional projection is ZERO, because r<=W<D and the primitive
   character inducing chi_D differs from chi_r. This includes complex
   chi_r: orthogonality to the real chi_D is unchanged by conjugation.
   Each weight has modulus1, so the phi(q) terms cancel the normalization
   1/phi(q); there is no extra factor phi(q) in the error. Lifting removes
   only powers of primes dividing q, of total weight O(log(Y)**2). Thus
   directly on any interval I in[Y/2,Y],
     sum_{n in I}Lambda(n)*chi_r(n)=1_{r=1}*|I|
                +O(Y*(mu**8+L**2/D)+L**2).            (3)
   Here |I| is its real length. This is uniform for r<=W and does not
   assert a corresponding interval estimate reaching down to0.
3. Sort low-conductor characters modulo d<=Q by their primitive inducer.
   One has
     sum_{d<=Q,r|d}1/phi(d)<<L/phi(r),
   since phi(rk)>=phi(r)*phi(k) and sum_{k<=x}1/phi(k)<<log(2x).
   There are at most phi(r) primitive characters of conductor r. The
   weighted number of low-conductor characters is therefore O(W*L).
   The induction error O(L**2) for each character contributes at most
   O(Q*L**2) when summed with weights1/phi(d). Orthogonality and (3)
   bound their contribution to the reduced progression error by
     O(Y*W*L*(mu**8+L**2/D)+W*L**3+Q*L**2).           (4)
   For the remaining characters use (1). The total, centered at the
   ORDINARY reduced density |I|/phi(d), is bounded by (4) plus
     O(L**C0*(Y/W+Q*sqrt(Y)+Y**(5/6))).                (5)
   A large-conductor exceptional character is included in (5); it is not
   silently removed, and there is no exceptional main term in this bound.
4. Choose B>(A+K0+1)/5. The mu**8 term of (4) is
     O(Y*mu**6*L**(K0+1))=O(Y*mu/L**A).
   The D term also fits: its ratio to Y*mu/L**A is at most
     O(mu**(-3)*L**(A+K0+3)/D)=o(1),
   because (2) with a=1/12 gives mu**(-3)<<D**(1/4), and D exceeds
   every fixed power of L. In (5), Y/W costs at most
   Y*mu**2/L**(A+5); the other terms are power-small relative to Y*mu
   because mu>=Y**(-h) for every fixed h>0. The same applies to the last
   two terms of (4). We have proved the reduced progression bound, with
   maxima over residues and endpoints in[Y/2,Y], relative to mu.
5. For nonreduced residues m mod d with d<=Q<Y/2, the primes themselves
   cannot contribute; proper prime powers contribute Y**(1/2+o(1)) in
   total by counting divisors of each nonzero m-p**j. This is relative
   power-small by (2). The real-length versus integer-count endpoint
   discrepancy is also power-small. Removing proper powers allows F
   instead of Lambda in RTI.
6. Compare the model with the same ordinary reduced density. Its principal
   truncation tail and summed period errors, already explicitly bounded in
   ramanujan_type_i.py, have a fixed power saving for fixed delta. They
   are therefore smaller than Y*mu/L**A by (2). The character component
   has summed absolute means O(Y*L**2/phi(D)) and a power-small period
   error. Since phi(D)>=sqrt(D/2) and mu>>D**(-1/8),
     L**(A+2)/(mu*phi(D)) << L**(A+2)*D**(-3/8)=o(1).
   This closes RTI by subtraction. The choice of delta depended on the
   absolute source constants c,C, not on A,B,K0; only the onset depends
   on those fixed saving parameters.

The positive CROSS from ramanujan_type_i.py and RTI now concern the same
model and the same scale mu. The remaining bilinear correlation is still
unproved; these two inputs alone never identify M_S with the prime weight.
"""
from fractions import Fraction
from math import gcd, lcm

from exceptional_character_model import character_values


def lifted_character_projection(conductor: int, input_conductor: int = 1, *,
                                 two_sign: int = 1, input_two_sign: int = 1
                                 ) -> tuple[int, Fraction, Fraction]:
    """Return q=lcm(D,r), mean(chi_r), mean(chi_r*chi_D) over units mod q.

    r=1 means the principal character; otherwise both supplied conductors
    define primitive REAL characters by character_values. The analytic
    proof covers complex characters too, by ordinary orthogonality; this
    finite exact helper intentionally tests only real characters. The
    means contain the normalization1/phi(q), not a sum over all residues.
    Small conductors only: the helper enumerates a complete common period.
    An input r>=D is permitted to check the exceptional projection boundary.
    It is not asserted to be an admissible small conductor in the proof.
    """
    exceptional = character_values(conductor, two_sign=two_sign)
    if type(input_conductor) is not int or input_conductor < 1:
        raise ValueError("input_conductor must be a positive integer")
    if input_conductor == 1:
        if type(input_two_sign) is not int or input_two_sign != 1:
            raise ValueError("the principal input requires input_two_sign=1")
        incoming = (1,)
    else:
        incoming = character_values(input_conductor, two_sign=input_two_sign)
    period = lcm(conductor, input_conductor)
    units = [a for a in range(period) if gcd(a, period) == 1]
    principal = sum(incoming[a % input_conductor] for a in units)
    exceptional_projection = sum(incoming[a % input_conductor]*exceptional[a % conductor]
                                 for a in units)
    return period, Fraction(principal, len(units)), Fraction(exceptional_projection, len(units))

"""Explicit coefficients surviving the near-half sieve specialization.

Owner: Kevin's Goldbach research. Purpose: test whether its sufficient
arbitrary-coefficient Type II hypothesis can immediately be replaced by
an available structured estimate. The immediate separated-coefficient
shortcut fails. A further Type I estimate does reduce the surviving
cofactor to rough squarefree integers, preserving ordinary Mobius signs.

SETUP AND EXACT SUPPORT, NOT AN ESTIMATE BY REPARAMETRIZATION.
1. Reuse critical_factor_mass.py with N=2x, I=(x/2,x], L=logx,
   w_n=Lambda(N-n)-b_n, gamma=1/2-e, nu=1/3-2e, 0<e<=1/100.
   The g(empty)=1 specialization has
    H(n)=sum_(d|n,d<=n^gamma,P^+(d)<n^nu)mu(d).
   Write n=u v uniquely: u contains the FULL prime-power factors with
   p<n^nu, and P^-(v)>=n^nu. Put R=rad(u). Then exactly
    H(n)=sum_(d|R,d<=n^gamma)mu(d).                      (1)
   If u=1, H=1 and Omega(n)<=3. If u>1 and R<=n^gamma, H=0.
   Otherwise R>n^gamma implies u>n^gamma and v<n^(1-gamma).
   Since 2nu>1-gamma, this v is either1 or a SINGLE prime, not a
   proper prime power. Thus the nonrough contribution is confined to
   a large-radical smooth u, possibly times one rough prime. The pure
   smooth class v=1 MUST remain. These are necessary support conditions;
   H may still vanish by cancellation within the surviving class.
2. For u>1, complement divisors in the zero sum sum_(d|R)mu(d)=0:
    H(n)=-mu(R) sum_(t|R,t<R/n^gamma)mu(t).              (2)
   The upper bound on t is STRICT, including when n^gamma is an
   integer. In the single-prime class v>=n^nu, it gives
    t<R/n^gamma<=u/n^gamma<=n^(1-gamma-nu)=n^(1/6+3e).
   This exposes an actual short divisor, but the other coefficient is
   mu(rad u), not mu(u), and the cutoff still depends on both u and v.
   For example n=420 has u=60,v=7,R=30,H=1 although mu(u)=0.
   Discarding nonsquarefree u would discard a nonzero part of the sum.
3. Let T_nu be the rough COMPOSITES in I. Let S be the integers with
   u>1 and R>n^gamma (the other support conditions follow above), and set
    R_nu(w)=sum_(n in T_nu)w_n, S_e(w)=sum_(n in S)H(n)w_n.
   The already proved Type I estimate gives
    sum_(p in I prime)w_p+R_nu(w)+S_e(w)=O_A(x/L^A).     (3)
   To apply I to H, fix d: d<=n^gamma and P^+(d)<n^nu restrict
   n=dk to an interval. No new Type II estimate proves (3).
   On the source critical set K_e, H=1; on its nonrough complement
   inside N, H=0 by Lemma7.18. In particular any nonzero nonrough H
   term is outside N automatically. The remaining source complement is
    sum_(n in T_nu outside K_e)w_n + S_e(w).
   This removes an unnecessary N-mask from S, but its moving divisor
   cutoff remains. Calling (3) a prime estimate would assume its open
   signed composite contribution.
4. Even the single-prime class is not one separated coefficient product.
   With e=1/100, rows u=60,90 and columns v=11,13 all have exactly the
   required small/rough split. Their H-values form [[1,1],[1,0]],
   determinant -1. Thus H(uv) on that class cannot equal alpha(u)beta(v).
   This only excludes rank one; finite sums, Mellin separation and more
   detailed arithmetic structure remain possible. Source Prop7.22 uses
   polytope separation and splittability before its arbitrary II supremum;
   retaining these masks does not license the existing smooth-input kernel.

AN ACTUAL SAVING IN THE PRIME-DECOMPOSITION INPUT.
5. Before applying the source prime decomposition, every explicit prime
   slot m_h is >=(x/2)^nu, and there are at most3 slots. Replace
    1_(m prime) by Lambda(m)/logm
   in these slots, retaining all physical and factor-region masks.
   The discrepancy is supported on proper prime powers; it is 1/r at
   m=p^r. This replacement, including any fixed-divisor-weighted tuple
   expansion of H, has absolute error
    O_eta(x^(1-nu/2+eta)L^C).                           (4)
   Proof: coefficients and tuple multiplicities are bounded by fixed
   divisor powers times fixed logarithms; their product is O_eta(x^eta)
   times a fixed power of L. Also |w|<<L. The count of integer perfect
   powers <=T, even with exponent multiplicity, is O(sqrtT logT).
   Hence their reciprocal tail above Z is O(Z^(-1/2)logx), for Z<=x.
   For any distinguished perfect-power slot, count its remaining product
   with x/m_h and apply that tail. A union bound over at most3 slots
   proves (4). All fixed divisor orders are paid before selecting eta;
   this is not a claim of uniformity in an increasing decomposition depth.
   Since nu>=47/150, eta=1/100 gives the uniform power exponent64/75,
   apart from fixed logarithms. This concerns the ACTUAL w, not just b.
6. Now insert the SAVED Heath-Brown identity with J=4, z=floor(x^(1/4)):
    Lambda=sum_(j=1..4)(-1)^(j-1)binom(4,j)
                       mu_<=z^{*j}*1^{*(j-1)}*log
   on all m<=x. Thus the actual primitive coefficient family before
   separation consists only of truncated mu, free1 and log, with at most
   eight factors per slot; physical and ordering masks and 1/logm remain.
   The identity and its support range were already proved in
   multifactor_identity_gate.py. This application avoids the source's
   twelve-factor root-lifting device: its Lemma7.12 uses J=4 and3J
   factors to encode exact prime indicators for more general w.
   Equivalently, its r_h>=2 perfect-power branches may be bounded by (4)
   after paying their fixed divisor multiplicities and logarithmic count.
   A genuinely long free1/log factor still permits the saved weighted I
   bound. All-short free factors do not become long by this reduction.
   The old complete HB/all-short experiment is not repeated or reopened.

CALIBRATION: THE SMOOTH COFACTOR CANNOT SIMPLY BE DROPPED.
7. Apply (1)-(3) to the already reviewed CLASSICAL PARITY MODEL
    w_n^*=ell(n), b_n^*=1, a_n^*=1+ell(n), ell=(-1)^Omega.
   This is not the actual prime partner. The saved strong Liouville sum
   and ell(dk)=ell(d)ell(k) give sum ell(n)H(n)=O_A(x/L^A): the fixed-d
   intervals have k on scale x/d>=x^(1-gamma)/2 and sum1/d=O(L).
   Write B_0=pi(x)-pi(x/2)~x/(2L). Ordered prime-factor PNT gives
    R_nu(ell)=[J2(nu)-J3(nu)+o(1)]B_0,
    J2(nu)=log((1-nu)/nu),
    J3(nu)=integral_(nu<=t1<=t2<=1-t1-t2)dt1 dt2/[t1t2(1-t1-t2)].
   The ordered triprime region is also restricted by t3>=t2, as written;
   its area is (1-3nu)^2/12 and J3<=3e^2/nu^3. Repeated large factors
   have power-small count. Formula (3), with ell(p)=-1, now proves
    S_e(ell)=[1-J2(nu)+J3(nu)+o(1)]B_0
             =[1-log2+O(e)+o(1)]B_0.                    (5)
   In fact 1-J2>1/5 throughout e<=.01: (1-nu)/nu<=103/47,
   log(103/47)=log2+log(103/94)<7/10+9/94<4/5.
   This is an application of the saved free parity/factor laws, not a
   new generic parity obstruction or an estimate for Lambda(N-n).
   It pinpoints a main-scale contribution missed by deleting the large
   smooth cofactor, even after the obvious pointwise cancellations.

A FURTHER ACTUAL ESTIMATE: REMOVE SMALL PRIMES, THEN REPEATED FACTORS.
8. Let y=floor(exp(sqrtL)), the existing comparison cutoff. For every
   fixed A, the ACTUAL sequence satisfies
    sum_(n in I) w_n H(n)1_(P^-(n)>y)=O_(A,e)(x/L^A).   (6)
   Proof: take upper/lower fundamental-lemma weights lambda_a^+/- at
   level D=floor(x^(e/4)), supported on squarefree a|P(y), |lambda|<=1.
   Put delta(n)=sum_(a|n)(lambda_a^+-lambda_a^-). The sieve sandwich
   gives delta>=0 and delta<=2tau(n); its ordinary integer mean on I
   is O_B(x/L^B) for every fixed B. Indeed logD/logy is comparable
   to e sqrtL; the fundamental-lemma error is all-log small and the
   interval remainders total O(D). Since sum tau(n)^3<<xL^7,
    sum delta(n)tau(n)
      <=(sum delta)^1/2 (sum delta tau^2)^1/2
      <<_B x L^((7-B)/2).
   The difference between the upper sieve and the rough indicator lies
   between0 and delta. Thus |wH|<<L tau(n) makes its weighted error
   O_A(x/L^A) by requesting B>2A+9.
   Expand H and the upper sieve. Each term is a w-sum on multiples of
    r=lcm(a,d)<=D x^gamma<=x^(1/2-3e/4).
   Its moving d<=n^gamma and P^+(d)<n^nu conditions are interval
   restrictions in n. For each r there are at most tau(r)^2 pairs(a,d).
   The SAVED fixed-divisor Type I bound at gamma'=1/2-3e/4 controls
   the entire sum. This proves (6) without actual Type II.
9. The full H-pairing is already all-log small by (3). Primes and all
   nu-rough composites exceed y in every prime factor eventually. Hence
    S_e(w)=sum_(n in S,P^-(n)>y)H(n)w_n+O_A(x/L^A).
   Repeated factors in this remaining sum cost at most
    L sum_(p>y prime) sum_(m<=x/p^2)tau(p^2m)
       <=3L sum_(p>y)sum_(m<=x/p^2)tau(m)
       <<x L^2/y=O_A(x/L^A).
   We used tau(p^2m)<=3tau(m), not a maximum n^eta which would
   defeat a subpower cutoff. Thus S_e can be restricted to y-rough
   SQUAREFREE n with an actual all-log error. Only AFTER paying these
   two errors may rad(u) be replaced by u and mu(rad u) by mu(u).
   The nonsquarefree fixture in step2 remains a warning against doing
   this pointwise or before the small-prime localization.
10. Expanding the reflected divisor t on this restricted support yields
    S_e(w)=-M_e(w)+O_A(x/L^A),                           (7)
    M_e(w)=sum_(n=trv in I) mu(r) w_(trv),
   with ALL the following constraints retained:
    r>n^gamma, mu^2(tr)=1, every prime of tr is in (y,n^nu),
    v=1 OR v is prime with v>=n^nu.
   Here t=1 is allowed; in the v-prime branch t<n^(1/6+3e).
   The coefficient is -mu(u)mu(t)=-mu(r) since u=tr is squarefree.
   These conditions make u=tr the exact small-prime part of n; they
   also imply n squarefree since v cannot divide tr. Thus this is an
   equality with paid errors, not a changed coefficient or dropped mask.
   Formula (3) becomes
    sum_(p in I prime)a_p=B_P-R_nu(w)+M_e(w)+O_A(x/L^A).
   The explicit linked estimate remains open. Its outer arithmetic sign
   is now an ordinary long Mobius coefficient mu(r), with a
   cofactor and either no rough factor or one prime. Smoothness, the
   moving cutoff, squarefreeness and the prime condition remain coupled.
   This is a useful smaller concrete target, not a separated Type II
   theorem. The parity calibration (5) survives the same localization:
   it supplies no reason for M_e or S_e to vanish for the actual w.

DISPOSITION.
The immediate smaller-separable-coefficient hypothesis fails. Preserve
the exact radical support, short reflected divisor, power pruning and
ACTUAL small-prime/squarefree localization. These estimates license the
ordinary Mobius coefficient in (7). None proves the signed sum in (3)
or (7), nor the sufficient Type II
estimate of critical_factor_mass.py. That earlier conditional positivity
and its actual critical-mass bound remain valid. No new prime coverage.
Further formal decomposition alone is not the next evidence target.

Primary source read2026-09-09: Ford--Maynard author PDF July16,2024,
Lemma7.12 pp43-45, Lemma7.14 pp46-48, Prop7.22 pp54-60. Source masks
and the nonstrict rough boundary from Lemma7.18 are retained.
https://www.ford126.web.illinois.edu/wwwpapers/prime-producing-sieves.pdf
Ford2023 notes Theorem3.6, already checked, supplies the sieve sandwich
in step8; source constants are fixed while x grows:
https://ford126.web.illinois.edu/sieve2023.pdf
PNT, Liouville and HB inputs are the already checked sources in
prime_producing_comparison_gate.py, prime_factor_endpoint_gate.py,
rough_liouville_transfer_gate.py and multifactor_identity_gate.py.
Finite helpers check identities and coefficient obstructions, not (3)'s
still-unproved prime-correlation bound.
"""
from fractions import Fraction as F

from critical_factor_mass import critical_bands
from major_arc_kernel import _factorization, _mobius_phi
from unexceptional_vaughan_gate import _divisors, _positive


def specialized_state(n, e=F(1, 100)):
    """Exact moving-cutoff state; compare rational powers with integers."""
    _positive(n, 'n')
    if n < 2:
        raise ValueError('require n>=2')
    critical_bands(e)
    gamma, nu=F(1, 2)-e, F(1, 3)-2*e
    u=radical=1
    for p, multiplicity in _factorization(n):
        if p**nu.denominator < n**nu.numerator:
            u*=p**multiplicity
            radical*=p
    v=n//u
    cutoff_power=n**gamma.numerator
    h=sum(_mobius_phi(d)[0] for d in _divisors(radical)
          if d**gamma.denominator <= cutoff_power)
    reflected=None if u==1 else -_mobius_phi(radical)[0]*sum(
        _mobius_phi(t)[0] for t in _divisors(radical)
        if t**gamma.denominator*cutoff_power < radical**gamma.denominator)
    if u==1:
        category='rough'
    elif radical**gamma.denominator <= cutoff_power:
        category='vanishing'
    else:
        category='pure_smooth' if v==1 else 'prime_smooth'
    return {'u':u, 'v':v, 'radical':radical, 'h':h,
            'reflected':reflected, 'category':category}


def prime_slot_weight(n):
    """Exact Lambda(n)/logn for n>=2; its nonprime support must be paid."""
    _positive(n, 'n')
    if n < 2:
        raise ValueError('require n>=2')
    factors=_factorization(n)
    return F(1, factors[0][1]) if len(factors)==1 else F(0)


def parity_region_constants(e):
    """Exact logarithm argument for J2 and a rational upper bound for J3."""
    critical_bands(e)
    nu=F(1, 3)-2*e
    return (1-nu)/nu, 3*e*e/(nu**3)


def mobius_cofactor_terms(n, y, e=F(1, 100)):
    """Exact terms of M_e on its retained support, without the w multiplier.

    A toy integer y guards the identity. The analytic localization uses
    y=floor(exp(sqrt(logx))) and is not certified by a finite fixture.
    """
    _positive(y, 'y')
    state=specialized_state(n,e)
    factors=_factorization(n)
    if any(p<=y or k!=1 for p,k in factors) or state['u']==1:
        return ()
    gamma=F(1,2)-e
    u,v=state['u'],state['v']
    return tuple((u//r,r,v,_mobius_phi(r)[0]) for r in _divisors(u)
                 if r**gamma.denominator>n**gamma.numerator)

"""An actual balanced divisor convolution, with the short-free-variable gap.

Owner: Kevin's Goldbach research. Purpose: retain Vaughan's free variables
and a usable arithmetic-coefficient component for the open unexceptional
correlation. Proof and exact guards only; no manuscript or coverage claim.
Independent Sol theory and actual-file review: PASS. Eight exact guards
passed normally in0.003s and under Python -O in0.002s. These finite guards
do not replace the analytic proof or its primary-source prerequisite.

QUESTION AND REASSESSMENT.
Can keeping Vaughan's free factor1 make a legal reciprocal-sum estimate
possible without completing its Mobius/prime coefficients? YES for the
balanced product-coefficient, Type-II-by-Type-II component below. The FULL
unexceptional remainder is still OPEN. In particular, k=1 is an actual
term, and neither its disappearance nor cancellation is proved here.
This changes the grouping and uses two genuinely free variables. It does
not retry the failed smooth-model transfer or the old cofactor geometry.

EXACT REGROUPING AND THE REMAINING GAP.
1. Retain the unexceptional_vaughan_gate.py definitions, including
   W=floor(Y^(gamma/2)), gamma=1/2-eps, 0<eps<1/12, J and E. Define
    h_r=sum_(ad=r,a>W,d>W) mu(a) Lambda(d).
   Then |h_r|<=sum_(d|r)Lambda(d)=log r, and EXACTLY
    T=sum_(r>W^2,rk in J) h_r E(m-rk), k>=1.                  (1)
   Equivalently the Vaughan Type II sequence is A(n)=sum_(r|n)h_r.
   The floor strip W^2<r<=Y^gamma costs O(log(Y) D_TI), by the
   existing Type I input and the displayed coefficient bound. It is only
   a floor-boundary strip, not a positive-width exponent range. The rest
   r>Y^gamma still contains k=1 and all other short k.
2. Expanding a small-divisor piece of the partner gives the congruence
    ad*k = m (mod e).
   With g=gcd(ad,e), it is soluble only if g|m, and Poisson has phase
    e_(e/g)(h*(m/g)*inverse(ad/g)), length about (e/g)/K.
   The outside coefficients mu(a)Lambda(d) remain arithmetic. When K=1,
   this length can be the whole modulus. The saved smooth/short-period
   model theorem therefore does NOT become applicable just by naming k
   a free variable. No full transfer is claimed from this manipulation.

POSITIVE RESTRICTED COMPONENT, WITH ACTUAL COEFFICIENTS.
3. Fix gamma in(5/12,1/2), smooth F compactly supported in(1/2,1)^2,
   and central even m with tau=m/Y in[5/4,7/4]. Let coefficient supports
   be M in[R,2R], N in[S,2S], where
     Y^gamma <= R,S <= Y^(51/100),
   and |alpha_M|,|beta_N|<=log(2Y). Arbitrary complex separate
   coefficients are allowed, including the actual h_M,h_N of(1).
   Then, uniformly in these coefficients and m,
    C = sum_(M,N) alpha_M beta_N
                    sum_(k,l in Z, Mk+Nl=m) F(Mk/Y,Nl/Y)
      = Y I_F(tau) sum_(M,N; gcd(M,N)|m)
                    alpha_M beta_N gcd(M,N)/(MN)
        + O_(F,gamma,epsilon)(Y^(1983/2000+epsilon)),          (2)
   for every epsilon>0, where I_F(tau)=integral F(t,tau-t)dt.
   Positivity of k,l is automatic from F's support. There are no hidden
   sharp cutoffs on the free variables. Constants use bounded smooth
   seminorms of the FIXED F; this is not an arbitrarily sharp-cutoff
   estimate. Summing logarithmically many such boxes absorbs another
   Y^epsilon factor, with epsilon chosen smaller initially.
4. For fixed g=gcd(M,N)|m put M=gu,N=gv, (u,v)=1, X=Y/g,
   f_tau(t)=F(t,tau-t). The equation is uk+vl=m/g. With Fourier convention
   fhat(xi)=integral f(t)e(-xi*t)dt, Poisson on
    k=(m/g)*inverse(u) (mod v)
   gives EXACTLY
    sum_(Mk+Nl=m) F(Mk/Y,Nl/Y)
      = X/(uv) sum_(h in Z) fhat_tau(hX/(uv))
                         e_v(h*(m/g)*inverse(u)).             (3)
   The zero mode is Yg/(MN) I_F(tau), as in(2). All g|m remain;
   dropping g>1 would discard genuine arithmetic and parity factors.
   The natural nonzero frequency length is H0=uv/X=MN/(gY).
5. Primary source: Bettin--Chandee, Trilinear forms with Kloosterman
   fractions, Theorem1 equation(1.2), arXiv:1502.00769v1, checked2026-09-09:
   https://arxiv.org/html/1502.00769v1 . For separate sequences supported
   at u~U,v~V,h~H, and theta !=0, the source bounds the coprime sum
    sum alpha_u beta_v nu_h e_v(theta*h*inverse(u))
   by ||alpha||2 ||beta||2 ||nu||2 times
    (1+abs(theta)*H/(UV))^(1/2)
     *[(HUV)^(7/20+epsilon)(U+V)^(1/4)
       +(HUV)^(3/8+epsilon)(HU+HV)^(1/8)].                    (4)
   The bracket is a SUM: both exponents must pass. The source's nearby
   determinant corollary is not silently substituted for our PLUS
   equation. We derive(2) directly from Theorem1 and(3).
6. Here theta=m/g is comparable to X. Split nonzero h into positive and
   negative dyadic blocks; for negative h change theta's sign. Normalize
   the outside coefficients by L=log(2Y). They remain alpha_(gu)/L and
   beta_(gv)/L, supported on intervals of lengths O(U),O(V), and hence
   have L2 norms O(sqrt(U)),O(sqrt(V)). No Fourier completion of an
   arithmetic coefficient occurs. The h coefficient has norm O(sqrt(H)).
   The factor X/(uv) supplies the outside scale X/(UV); its remaining
   smooth u,v ratios can be separated together with the Fourier weight.
7. To justify that separation, insert fixed smooth cutoffs equal to1 on
   each dyadic u,v,h box. In logarithmic coordinates these lie in fixed
   compact boxes. The smooth factor is a constant scale times
    (UV/(uv))*fhat_tau((H/H0)*(h/H)*(U/u)*(V/v)),
   where H0=UV/X now denotes the box scale. Its log-Fourier expansion
   has absolutely summable coefficients, uniformly for H/H0<=1. For
   H/H0>1 the sum of absolute coefficients decays faster than any fixed
   power of H/H0, since fhat_tau is Schwartz with the same property
   for every derivative. Each expansion term supplies separate Mellin
   twists of modulus1 to all three sequences, preserving their L2 norms.
   Thus(4) applies termwise; the coupled weight is not declared free.
8. For any fixed small eta>0, boxes H0<Y^-eta are negligible directly:
   the absolute nonzero part of(3) per pair is O_B(H0^(B-1)); there
   are at most O(Y^(102/100)) pairs and coefficients cost L^2. Choose
   B large in terms of eta. For H0>=Y^-eta, sum dyadic h blocks using
   the Schwartz decay in step7. It suffices to budget H=max(1,H0),
   at a cost Y^O(eta) relative to H=H0. The phase factor is bounded
   at H=H0 because abs(theta)H0/(UV) is comparable to1. Padding
   H0<1 to1 is included in that Y^O(eta) cost. Unit reduced variables
   u=1 or v=1 have H0<<Y^(-49/100), because M,N<<Y^(51/100),
   and belong to the direct decay case. All sums over g|m cost only
   tau(m)<<_epsilon Y^epsilon; coprimality (u,v)=1 stays in(4).
9. Write R=Y^r,S=Y^s,g=Y^d, so U,V have exponents r-d,s-d,
   H0 has exponent kappa=r+s-d-1, and X/(UV) exponent1+d-r-s.
   Combining this prefactor, all THREE norms and BOTH source terms yields
    E1=3/20+7(r+s)/10+max(r,s)/4-9d/5,
    E2=7(r+s)/8+max(r,s)/8-15d/8.                            (5)
   These increase with r,s and decrease with d. At r=s=51/100,d=0:
    E1=1983/2000, E2=153/160.
   Choose eta and source epsilon sufficiently small for the desired final
   epsilon, and absorb L^2 and the divisor/dyadic losses. This proves(2),
   with a fixed saving17/2000 before those arbitrarily small losses.
   At r=s=1/2 the exponents are39/40 and15/16. A symmetric cap
   1/2+zeta has E1=39/40+33*zeta/20; this specific estimate requires
   zeta<1/66. That budget boundary is not an arithmetic impossibility.

WHAT THIS DOES AND DOES NOT CLOSE.
10. Inserting Vaughan on BOTH factors creates the actual term A*A, and
    (2) controls its indicated product-coefficient boxes with h_M,h_N.
    Its zero main is the SIGNED gcd-dependent coefficient sum displayed
    in(2), not a proved positive prime main. The mixed Vaughan/model
    terms, larger M or N, and possible cancellation of their zero modes
    against this one have not been evaluated here. A(n) itself is signed.
    Neither this restricted asymptotic nor the negligible covariance
    diagonal in unexceptional_vaughan_gate.py implies T=o(Y).
11. cofactor_averaging_budget.py's failed geometry has grouped exponent
    r=(1+b)/2>=3/5 and s=1/2, exceeding this successful balanced range.
    Its failure remains valid. Polynomial identities, exceptional-zero
    conditional coverage and the smooth reciprocal components also remain
    intact. The next mathematical test should target a named omitted
    region or a zero-mode composition, keeping the actual coefficients.

Finite helpers check logarithmic regrouping, solution congruences, gcd
density and exact error exponents. They are not numerical asymptotic tests,
independent proofs of Theorem1, or additional Goldbach range verification.
"""
from dataclasses import dataclass
from fractions import Fraction as F
from math import gcd

from major_arc_kernel import _mobius_phi
from unexceptional_vaughan_gate import (
    _add, _clean, _divisors, _positive, mangoldt_log_vector,
)


def product_log_vector(n, lambda_cutoff, mobius_cutoff):
    """Exact h_n before convolving with Vaughan's retained free factor1."""
    for value, name in ((n, 'n'), (lambda_cutoff, 'Lambda cutoff'),
                        (mobius_cutoff, 'Mobius cutoff')):
        _positive(value, name)
    vector = {}
    for d in _divisors(n):
        a = n//d
        if a > mobius_cutoff and d > lambda_cutoff:
            _add(vector, mangoldt_log_vector(d), _mobius_phi(a)[0])
    return _clean(vector)


def free_residue(first, second, target):
    """Return (g, reduced modulus, k residue) for first*k+second*l=target."""
    for value, name in ((first, 'first'), (second, 'second'), (target, 'target')):
        _positive(value, name)
    g = gcd(first, second)
    if target % g:
        return None
    u, v = first//g, second//g
    residue = (target//g)*pow(u, -1, v) % v if v > 1 else 0
    return g, v, residue


def free_solutions(first, second, target):
    """All strictly positive solutions, obtained from the reduced progression."""
    data = free_residue(first, second, target)
    if data is None:
        return ()
    _, v, residue = data
    initial = residue if residue > 0 else v
    return tuple((k, (target-first*k)//second)
                 for k in range(initial, (target-1)//first+1, v)
                 if target-first*k >= second)


def zero_density(first, second, target):
    """Exact h=0 coefficient BEFORE multiplication by Y*I_F(tau)."""
    data = free_residue(first, second, target)
    return F(data[0], first*second) if data is not None else F(0)


@dataclass(frozen=True)
class FreeCorrelationBudget:
    frequency: F
    prefactor: F
    norms: F
    first: F
    second: F


def free_correlation_budget(first_exponent, second_exponent, gcd_exponent=F(0)):
    """Natural-frequency source budget; outside the cap this is bookkeeping only."""
    r, s, d = first_exponent, second_exponent, gcd_exponent
    if any(type(value) is not F for value in (r, s, d)):
        raise ValueError('exact Fraction exponents required')
    if not 0 <= r <= 1 or not 0 <= s <= 1 or not 0 <= d <= min(r, s):
        raise ValueError('require r,s in[0,1] and 0<=d<=min(r,s)')
    u, v, k = r-d, s-d, r+s-d-1
    if k < 0:
        raise ValueError('negative frequency exponent belongs to the decay/padding case')
    prefactor = 1+d-r-s
    norms = (u+v+k)/2
    first = prefactor+norms+F(7, 20)*(k+u+v)+max(u, v)/4
    second = prefactor+norms+F(3, 8)*(k+u+v)+max(k+u, k+v)/8
    return FreeCorrelationBudget(k, prefactor, norms, first, second)

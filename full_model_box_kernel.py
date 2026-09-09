"""Full hyperbola-box coverage for the smooth ALL-INTEGER-modulus MODEL.

Owner: Kevin's Goldbach research. Purpose: test the exact envelope of the
retained model bounds and preserve the new grouped-period mechanism that
closes its residual strip. This is a proof and reusable verifier, not
publication packaging. It estimates the specified MODEL only. The original
sieve weights, signed prime correlation, and Goldbach remain OPEN.
Polynomial identities and every preceding useful component remain tools.

Theorem. Use EXACTLY E_q of composite_linear_kernel.py, with
 B=Y^b,A=Y^x,C=Y^y,K=BAC/Y, m an integer in[Y,2Y],
 1/5<=b<=13/25, 0<=x<=(1-b)/2, 0<=y<=1/2,
 1<=H,J0<=Y^(1/4096).
Sum over EVERY integer q in[C,2C], q>=2, arbitrary unit r_q, and arbitrary
bounded joint spatial period-J_q weights omega_(q,k), J_q<=J0, allowing
all k dependence and gcd(q,J_q)>1. Fixed smooth spatial W1,W2 have the
same support[1,2] and regularity as in that model. For every epsilon>0,
  sum_q |E_q| <<Y^(1-1/4096+epsilon).                       (1)
No assumption identifying actual sieve weights with these weights is made.

I. An exact covering of the domain, with two new transfers.
Write j=log_Y J0,h0=log_Y H. Empty positive-k ranges cost zero.
The retained pointwise bound handles y<=49/100, with off-axis exponent
2y+h0+4j. Integer axes and overlap always cost b+x+h0+j<77/100.
The linear bound handles min(b,x)<=31/128 with exponent<=4067/4096.
Reciprocal energy handles max(b,x)<=9/32 with the same exponent.

For 9/32<=d=max(b,x)<=15/32, interchange the two spatial variables
in the balanced argument as needed. Its three bare off-axis exponents are
  7y/4, 3y/2+d/2, 1/2+5y/4-d/2.                          (2)
All are <=63/64. The original coarse full-squarefull-part split at
Z=Y^(1/256) charges at most H*J0^8*Z^(13/4) on the small-part side,
and H*J0^4*Y^(2y)*Z^-1/2 on the other side. Both exponents are
<=1-3/4096. For y>=49/100 both dual scales grow since d<=15/32;
the grouped scale grows too. Thus the source support and Schwartz
steps in all_moduli_balanced_kernel.py apply throughout this region.
For smaller y the pointwise route already applies. Formula(2) follows
by keeping the dual of the coordinate of size Y^d separate, and grouping
the OTHER dual with k in squarefree_correlation_kernel.py equation(6).
This proves a regional extension, not an extrapolation from one box.

Everything left has
  b>15/32, 31/128<x<17/64, 49/100<y<=1/2.                 (3)
Indeed x<=2/5 globally, so max(b,x)>15/32 forces that maximum to be b;
then x<=(1-b)/2<17/64. Endpoints may be included in the following proof.
The fixed-h square-root padding used in the previous unbalanced proof
loses too much here. Instead keep the product of h and k as an actual
interval variable, with its coupled periodic coefficient fully retained.

II. Rectangular divisor shifts with a coupled periodic factor.
Let Q=r*s, gcd(r,s)=1, s squarefree, gcd(s,J)=1, and let W(a,n) be ANY
bounded function periodic modulo rJ in BOTH variables. For unit c mod s,
put T=sum alpha_a beta_n W(a,n) Z_s(c*a*n). Assume M<=N,
alpha,beta supported in[1,M],[1,N], and 4rJ<=N<=s. Then
 |T| <<Q^epsilon ||alpha||2||beta||2 sqrt(MN)
    *((rJ/N)^(1/4)+s^(1/8)/N^(1/4)
                       +s^(1/4)/(N^(1/4)*M^(1/2))).      (4)
Divisor-size bounds for W are absorbed in epsilon. A row at a nonunit
of s vanishes; no unit restriction on the r factor is needed.

Proof: Cauchy in beta gives correlations indexed by a1,a2. Their local
factor W(a1,n)*conj(W(a2,n)) is periodic in n mod rJ, so translations
by multiples of rJ preserve it exactly. The proof of divisor-shift
equations(4)--(6) in squarefree_unbalanced_kernel.py then gives
 |I(a1,a2)| <<(NrJ)^1/2+N^1/2*s^1/4*gcd(s,a1^2-a2^2)^1/4.
The same weighted signed-congruence graph bounds the pair average by
||alpha||2^2*(M+s^1/4). Substitution proves(4). The coefficient W need
not separate; its periodicity is the property actually used. Either
coordinate may be the longer shifted variable because W is periodic in
both. This is the first new mathematical transfer.

For the core alternative Q=t*R, with t<Q^(1/32) and R consisting of one
or two simple primes each>Q^(2/5), a kernel periodic mod tJ costs only
sqrt(tJ) in coefficient norms: fix the first variable's residue mod tJ,
absorb W into the second coefficient, and sum the restricted first norms
by Cauchy. The rectangular core bound is
 sqrt(tJ)*[sqrt(N)+sqrt(MN)/sqrt(p_min)
                         +R^(11/64)*(MN)^(5/16)].         (5)
For a prime use KMS Theorem1.1; the displayed extra terms are harmless.
For two primes the retained scalar amplification proof works with
 A0=(N/M)^1/2*R^(1/8), B0=(MN)^1/2*R^(-1/8),
 L=A0*M=(MN)^1/2*R^(1/8).
Choose fixed constants so A0*B0<=N. Under B0,A0<p_min, 2L<R, N<R and
MN<R^(5/4), the three fourth-moment terms are exactly bounded by
 (MN)^2*R, (MN)^(5/2)*R^(3/8), (MN)^2*R.
The middle is absorbed. Substituting into the retained MQW scalar
Holder inequality gives the norm R^(11/64)*(MN)^(5/16).
Nonunit differences give sqrt(N)+sqrt(MN)/sqrt(p_min), as shown in
two_prime_kl3_kernel.py. These are prime/two-prime inputs, never an
imported prime-power theorem. The already checked sources are
FKM1405.2293v2 Corollary3.4, KMS1511.01636v5 Theorem1.1/Lemma2.5/
Theorem4.11, and MQW2511.07550v1 section4.1. No new source claim is used.

III. Exact period grouping, including the shared-prime cases.
For a fixed q,J,k, expand its weight with Fourier labels a,b modJ.
The retained exact period lift is
 F_(qJ)(h,l;t)=J^2 sum_(a,b; J|h+qa,l+qb)
            c_ab(k)*F_q((h+qa)/J,(l+qb)/J;t), |c_ab(k)|<=1.
Expand F_q/q by the ALL-prime-power recursion in
all_moduli_unbalanced_kernel.py. A term has remaining Q=q/D, coefficient
c_D, and divisibilities Hdiv|h',Ldiv|l',Tdiv|m*k, where Hdiv,Ldiv divide D.
Write Kdiv=Tdiv/gcd(Tdiv,m). Since Hdiv,Ldiv also divide q, they divide
the ORIGINAL h,l. Set h=Hdiv*eta,l=Ldiv*lambda,k=Kdiv*kappa. Then
 h'/Hdiv=(eta+(q/Hdiv)*a)/J,
 l'/Ldiv=(lambda+(q/Ldiv)*b)/J.                            (6)
Both q/Hdiv and q/Ldiv are multiples of Q. The extra integrality
conditions in(6) are retained as masks in their respective coefficients.

Fix kappa modulo J, paying J classes, and group w=eta*kappa. For any
r|Q, the product (h'/Hdiv)*kappa modulo r is determined by
  (w+(q/Hdiv)*a*kappa)/J mod r.                           (7)
Its value depends only on w mod rJ and the fixed kappa modJ. The
second quotient in(6) depends only on lambda mod rJ. Thus the r-part
of natural K_Q is an actually bounded coupled periodic function W(w,lambda).
Integrality makes (7) well-defined on the coefficient support; extend
the periodic function by zero elsewhere. The grouped alpha_w is a
divisor convolution with the eta mask retained, not a free separation.

Choose r to contain every repeated prime factor of Q and every simple
Q-prime dividing J. Then the complement s is squarefree and coprime to J.
Modulo s, the two quotients in(6) reduce to eta/J and lambda/J, so its
factor is natural K_s(c*w*lambda), for a fixed multiplier c that may be
nonunit. The CRT unit scalings are absorbed into c and W. This proves
the second new transfer, and explains why arbitrary joint periods do not
force the expensive full-squarefull residue split in this strip.

For good q with U(q)<=q^(39/100), restrict first to D<=q^(1/256).
Then U(Q)*J<=Q^(2/5), with a strict margin throughout(3). The corrected
factorization argument of all_moduli_unbalanced_kernel.py starts from
U(Q)*gcd(Q/U(Q),rad(J)). It gives r in[Q^(1/32),Q^(69/160)] or a small
t<Q^(1/32) with one/two large simple primes left. The local kernel in
the two cases is periodic mod rJ or tJ respectively.

Only the complementary simple primes need a natural-to-zero partition.
Use the ordered gcd(c,s),gcd(w,s0),gcd(lambda,s1) partition already proved.
The removed product Ds gives the exact factor1/Ds. Separate coefficient
masks and substitutions preserve W's rJ period since gcd(Ds,rJ)=1.
If Ds<=q^(1/256), keep the SAME r and replace s by s/Ds in(4). Its two
s-dependent terms improve and the support margin below survives.
In the core case any nontrivial Ds contains a prime>Q^(2/5), hence is
already large. Large Ds are bounded using1/Ds and full volume.
Nonunits in r remain within its bounded natural K_r factor; they do not
need to be falsely called zero or to be discarded.

The grouped L2 mass differs from the fixed-h argument and must be paid:
  c_D/sqrt(Hdiv*Ldiv*Kdiv) <<Y^epsilon,                    (8)
while its full-volume mass is <=Y^epsilon/D. At a main local depth j0,
D=c_D=Hdiv=Ldiv=Tdiv=p^j0; the terminal prime correction cases listed
in all_moduli_unbalanced_kernel.py satisfy(8) as well, up to1+1/p.
Divisor convolution and Cauchy give
 ||alpha||2^2 <<Y^epsilon*(U0/Hdiv)*(W0/Kdiv),
 ||beta||2^2 <<V0/Ldiv,
where U0=qJ/B,V0=qJ/A,W0=HK. Nonzero Schwartz sums make these bounds
valid even at scales below1. There is NO assertion of D^-1/2 in(8).

Pad the two intervals to their ORIGINAL sizes U0*W0 and V0. The norm
product then pays (8). In (4)--(5) every remaining modulus/factor occurs
with a nonnegative exponent before the relative-saving shorthand;
replacing Q by q in the upper bounds is a safe weakening, not a lost
D^delta. If D>q^(1/256), use its full-volume1/D bound. The number of
recursion/partition terms is divisor-size. The Fourier labels, lift,
and kappa classes cost at most J^2*J^2*J=J^5 in total.

IV. Exact support and exponent accounting in the residual strip.
If U0 is smaller than an arbitrarily small negative power of Y, all
nonzero h modes are arbitrarily power-small by Schwartz decay. Otherwise
truncate with a tiny power of Y; signs of h,l are treated separately.
This gives positive interval variables and changes bounds only by
Y^epsilon. The two padded logarithmic lengths before ordering are
 v=y-x+j, w=x+2y-1+j+h0;
 P=v+w=3y-1+2j+h0, m0=min(v,w), n0=max(v,w).               (9)
Here j may be the actual log_Y J; bounds are uniform below the cap.
The normalized baseline after Poisson and O(C) moduli is
  Y^(2y+epsilon)*H*J0^5.                                 (10)

For small D,Ds their cumulative reduction exponent is at most2y/256.
In(3), m0>=31/128-1/50, n0<=17/64+j+h0. Also
 rJ<=Y^(69y/160+j),
 s/Ds>=Y^((255/256)*(91/160)*y-y/256).
Consequently 4rJ<=Y^n0<=s/Ds holds with strict exponent margins. The
prime/core parameters obey B0,A0<p_min, L<R, N<R, MN<R^(5/4): one may
use Q>=q^(255/256), R>=Q^(31/32), p_min>Q^(2/5) and(9). These are
checked as rational inequalities at the rectangle endpoints below.

Using n0>=P/2 in the first two divisor-shift terms, and
n0<=17/64+j+h0 in the third, their total exponents are bounded by
  E1=1109y/640+1/8+7h0/8+5j,
  E2=447y/256+1/8+7h0/8+19j/4,
  E3=95y/128+1/2+17/256+3h0/4+17j/4.                    (11)
The generic core term has upper exponent
  Ec=3317y/2048+3/16+13h0/16+41j/8.                     (12)
Indeed sqrt(tJ)*R^(11/64) is <=Q^(373/2048)*sqrt(J), so its relative
factor is Q^(373/2048)*sqrt(J)*(MN)^(-3/16).
The extra core error terms in(5) are <Y^(19/20) after all costs, using
the same strict lower bounds on m0 and p_min. At y=1/2 and full caps,
E2=1-(19/8)/4096, Ec=1-(81/16)/4096; E1,E3 are smaller.
Large D or Ds have exponent
  Ed=2y+h0+5j-y/256<=1-2/4096.                            (13)
Finally bad q with U(q)>q^(39/100) number O(C^(161/200)); the retained
pointwise estimate gives exponent361y/200+h0+4j<1-1/4096.
Together with the integer axes, this proves(1) in the residual strip.
The elementary covering in I now proves(1) throughout the full domain.

Reassessment: swapping the balanced grouping covered a broad region;
the residual strip required rectangular shifts and exact period grouping.
The former squarefull-residue budget failures remain valid for their
particular combinations. This full MODEL result still does not control
the original coupled arithmetic weights. The next meaningful test is
their exact structural identification, with all sieve-index costs kept.
Latest original-affine remains2b8cf98, and formal conservation6f9a77b
still leaves its signed difference unestimated. Finite tests below
guard algebra, support and a continuum-domain partition, not Goldbach.
"""
from fractions import Fraction as F
from itertools import product
from math import gcd

from all_moduli_unbalanced_kernel import local_mass_terms
from composite_linear_kernel import composite_linear_budget
from reciprocal_energy_kernel import energy_budget


CAP = F(1, 4096)


def box_route(b, x, y, period=0, frequencies=0):
    checked = composite_linear_budget(b, x, y, period, frequencies)
    if not checked.active:
        return 'empty'
    if y <= F(49, 100):
        return 'pointwise'
    if min(b, x) <= F(31, 128):
        return 'linear'
    if max(b, x) <= F(9, 32):
        return 'energy'
    if max(b, x) <= F(15, 32):
        return 'balanced'
    return 'grouped-period'


def full_box_budget(b, x, y, period=0, frequencies=0):
    route = box_route(b, x, y, period, frequencies)
    axes = F(b)+F(x)+F(period)+F(frequencies)
    if route == 'empty':
        power = F(0)
    elif route == 'pointwise':
        power = max(2*F(y)+F(frequencies)+4*F(period), axes)
    elif route == 'linear':
        power = composite_linear_budget(b, x, y, period, frequencies).total_exponent
    elif route == 'energy':
        power = energy_budget(b, x, y, period, frequencies).total
    elif route == 'balanced':
        power = max(axes, *balanced_region_budget(max(b, x), y, period, frequencies).values())
    else:
        values = grouped_region_budget(x, y, period, frequencies)
        power = max(axes, *(value for key, value in values.items() if not key.endswith('_margin')))
    return {'route': route, 'power': power, 'claimed': 1-CAP}


def balanced_region_budget(d, y, period=0, frequencies=0):
    if any(type(v) not in (int, F) for v in (d, y, period, frequencies)):
        raise ValueError('require exact exponents')
    if not (F(9, 32) <= d <= F(15, 32) and 0 <= y <= F(1, 2)
            and 0 <= period <= CAP and 0 <= frequencies <= CAP):
        raise ValueError('outside the regional theorem')
    bare = max(F(7, 4)*y, F(3, 2)*y+d/2, F(1, 2)+F(5, 4)*y-d/2)
    return {'head': bare+frequencies+8*period+F(13, 1024),
            'tail': 2*y+frequencies+4*period-F(1, 512)}


def grouped_region_budget(x, y, period=0, frequencies=0):
    if any(type(v) not in (int, F) for v in (x, y, period, frequencies)):
        raise ValueError('require exact exponents')
    x, y, j, h = map(F, (x, y, period, frequencies))
    if not (F(31, 128) <= x <= F(17, 64) and F(49, 100) <= y <= F(1, 2)
            and 0 <= j <= CAP and 0 <= h <= CAP):
        raise ValueError('outside the residual rectangle')
    v, w = y-x+j, x+2*y-1+j+h
    small, large = min(v, w), max(v, w)
    qmin = F(255, 256)*y
    rmin = F(31, 32)*qmin
    pmin = F(2, 5)*qmin
    baseline = 2*y+h+5*j
    return {
        'vd_first': F(1109, 640)*y+F(1, 8)+F(7, 8)*h+5*j,
        'vd_second': F(447, 256)*y+F(1, 8)+F(7, 8)*h+F(19, 4)*j,
        'vd_third': F(95, 128)*y+F(1, 2)+F(17, 256)+F(3, 4)*h+F(17, 4)*j,
        'core': F(3317, 2048)*y+F(3, 16)+F(13, 16)*h+F(41, 8)*j,
        'core_error_first': baseline+y/64+j/2-small/2,
        'core_error_second': baseline+y/64+j/2-pmin/2,
        'large_divisor': baseline-y/256,
        'bad_moduli': F(361, 200)*y+h+4*j,
        'period_support_margin': large-F(69, 160)*y-j,
        'complement_support_margin': F(91, 160)*qmin-y/256-large,
        'core_a_margin': pmin-(large-small)/2-y/8,
        'core_b_margin': pmin-(v+w)/2+rmin/8,
        'core_l_margin': rmin-(v+w)/2-y/8,
        'core_n_margin': rmin-large,
        'core_product_margin': F(5, 4)*rmin-v-w,
        'fullpart_margin': F(2, 5)*qmin-F(39, 100)*y-j,
    }


def grouped_period_sums(q, divisor, hd, ld, period, r, a, b, kclass,
                        eta_weights, kappa_weights, lambda_weights):
    """Exact integer toy-kernel sum before/after shared-period grouping.

    Arrays index positive eta,kappa,lambda. Nonconstant local kernels
    test algebra independent of analytic bounds or a Kl3 implementation.
    """
    if (q % divisor or divisor % hd or divisor % ld or (q//divisor) % r
            or gcd(r, (q//divisor)//r) != 1
            or gcd((q//divisor)//r, period) != 1):
        raise ValueError('invalid decomposition')
    remaining, s = q//divisor, (q//divisor)//r
    if s <= 1 or not 0 <= kclass < period:
        raise ValueError('require a nontrivial complement and residue')
    aa, bb = (q//hd)*a, (q//ld)*b
    def first_kernel(z):
        return (z % r)**2-2*(z % r)+3
    def second_kernel(z):
        return (z % s)**3-3*(z % s)+1
    direct = 0
    grouped = {}
    for eta, ew in enumerate(eta_weights, 1):
        if (eta+aa) % period:
            continue
        for kappa, kw in enumerate(kappa_weights, 1):
            if kappa % period != kclass:
                continue
            w = eta*kappa
            grouped[w] = grouped.get(w, 0)+ew*kw
            for lam, lw in enumerate(lambda_weights, 1):
                if (lam+bb) % period:
                    continue
                z = ((eta+aa)//period)*kappa*((lam+bb)//period)
                direct += ew*kw*lw*first_kernel(z)*second_kernel(z)
    after = 0
    for w, coefficient in grouped.items():
        wp = w % (r*period)
        numerator = wp+aa*kclass
        if numerator % period:
            raise ArithmeticError('lost integrality in grouped coefficient')
        for lam, lw in enumerate(lambda_weights, 1):
            if (lam+bb) % period:
                continue
            lp = lam % (r*period)
            local = (numerator//period)*((lp+bb)//period)
            complement = w*lam*pow(period*period, -1, s)
            after += coefficient*lw*first_kernel(local)*second_kernel(complement)
    return direct, after, sum(value != 0 for value in grouped.values())


def grouped_mass_squared(p, e, target_valuation):
    """Local norm/volume masses for the actual prime-power expansion."""
    result = []
    for d, coefficient, hd, ld, td, allowance in local_mass_terms(p, e):
        kd = td//gcd(td, p**target_valuation)
        result.append((F(coefficient**2, hd*ld*kd), allowance**2,
                       F(coefficient, hd*ld*kd), allowance/d))
    return tuple(result)

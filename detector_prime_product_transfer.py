"""Transfer a full detector-weighted zero field to actual prime products.

Owner: Kevin's Goldbach research. Purpose: test whether the common signed
detector can be used arithmetically, paying the small dilated scales and
retaining the obstacle to restriction to the surviving zero set. These
are full-field identities and bounds, not the missing paired estimate.

1. THE FULL-FIELD TRANSFER AND ITS UNIFORM COEFFICIENT CLASS.
Keep T=N^(9/10), V=N^(1/8), L=logN, fixed real chi in
C_c^infinity((1,2)), and the Fourier cutoff nu from the retained
unconditional Guinand formula. Put Q=2*N^(41/100). Suppose b(n)
is any finite complex coefficient list supported on 1<=n<=Q with
 |b(n)|<=A*tau(n),                                           (1)
where A>=0 may depend on N. Define
 B(s)=sum_n b(n)n^-s,
 S_B(x)=sum_(actual rho)chi(gamma/T)*B(rho)*x^(rho-1/2),
 d_B(k)=(b*Lambda)(k)=sum_(n*m=k)b(n)*Lambda(m).
All positive-height zero copies and actual real parts are retained.
Uniformly for x in[N/4,3N/4], we prove
 S_B(x)=-P_B(x)+O_chi(A*N^(41/200)*L^7),                       (2)
 P_B(x)=T/(2pi)*sum_(k>=2)d_B(k)/sqrt k
                 *hatChi(Tlog(k/x))*nu(Tlog(k/x)/V),
and, in the FIXED-target a measure,
 int_(1/4)^(3/4)|S_B(aN)|^2 da <<_chi A^2*N*L^5.              (3)
No prime-window width below one is treated as a prime interval with
the earlier positive-length mass bound. The product index k in(2),
unlike its separate factor m, still has window width N/T=N^(1/10).

The actual common detector H_N has coefficients
 h(n)=a_T(n)*exp(-n/Y)*1_bad(n),
 Y=sqrtT, a_T(n)=sum_(d|n,d<=2*T^(1/100))mu(d),
where 1_bad is the union of its allowed bad dyadic blocks. Those blocks
are disjoint and have n<=Q. Thus(1) holds with A=1, including its
signed coefficients and all four bad-length ranges. Equations(2)-(3)
apply to the FULL zero field weighted by this actual H_N.

2. A DENSITY BOUND UNIFORM AT ALL THE DILATED SCALES.
The finite zero sum has the EXACT dilation identity
 S_B(x)=sum_n b(n)*n^(-1/2)*S_T(x/n),                          (4)
where S_T(y)=sum chi(gamma/T)y^(rho-1/2). The factor n^-1/2
is necessary: n^-1/2*(x/n)^(rho-1/2)=x^(rho-1/2)n^-rho.
Every y=x/n lies in[N/(4Q),3N/4], so y>=N^(59/100)/8 and
logy is comparable to L. In much of this range T exceeds y.

Use the uniform classical Ingham bound with its LOG-POWER loss,
counting copies, as recorded in Yashiro1310.0765v2 printedp2,(1.1):
 M(sigma,2T)<<T^[D(u)]*L^5,
 D(u)=3u/(1+u), u=1-sigma, 0<=u<=1/2.
 https://arxiv.org/pdf/1310.0765v2
The primary display was rechecked2026-09-10. The elementary identity
 1-(4/3)*(1/2-u)-D(u)=(1-2u)^2/(3*(1+u))>=0                 (5)
shows, since y<=3N/4<T^(4/3), that
 y^(1/2-u)*T^D(u)<=T*(y/T^(4/3))^(1/2-u)<=T.
For beta<=1/2 use the total O(TL) count. Positive layer cake,
including its boundary, then gives uniformly at these dilated scales
 W_T(y)=sum_(T<=gamma<=2T)y^(beta-1/2)<<T*L^6.                (6)
This sharpens the older coarse N*L^6 first-moment bound for this
specific T=N9/10 regime; no zero-free region or RH is required here.

3. THE ENTIRE-TEST ERRORS REMAIN SMALL WHEN T>y.
Apply the retained Guinand formula to exp(itlogy)*chi_V(t/T).
Taylor-expand the ENTIRE chi_V at gamma/T-i*(beta-1/2)/T;
do not analytically continue the compactly supported chi. The localized
first correction costs W_T(y)/T=O(L^6), by(6). The global both-sign
Taylor and Fourier-tail errors cost
 sqrt y*T*L*(T^-2+V^-16)
                  <<(N^-2/5+N^-3/5)*L.                      (7)
Pole tests cost O(sqrt y*(T^-2+V^-16)). The Gamma-integral cutoff
tail is O(T L V^-16)=O(N^-11/10 L); on the original compact
support, integration by parts gives O(logT/logy)=O(1), uniformly.
The negative-frequency prime term vanishes: logy stays comparable
to L while the Fourier support radius2V/T tends to zero.
These are exactly the checked source conventions and complex-zero
argument in arithmetic_zero_moment.py and arithmetic_zero_energy.py.
They prove, uniformly for the WHOLE dilated range,
 S_T(y)=-T/(2pi)*sum_(m>=2)Lambda(m)/sqrt m
       *hatChi(Tlog(m/y))*nu(Tlog(m/y)/V)+O(L^6).              (8)
No upper bound for the size of the prime sum is needed to prove(8).

The elementary divisor sum gives
 sum_(n<=Q)tau(n)/sqrt n
 =sum_(d*r<=Q)(d*r)^(-1/2)
 <=2*sqrtQ*sum_(d<=Q)1/d<<sqrtQ*log(2Q).                     (9)
Insert(8) into(4), pay the error by(9), and group the finite terms
by k=n*m. This proves(2), including the minus sign and sqrt k.
Absolute convergence issues do not arise: b is finite and the Fourier
cutoff makes each prime sum finite before regrouping.

4. PRODUCT-INDEX SCHUR AND THE FULL-FIELD NORM.
The EXACT divisor identity 1*Lambda=log implies
 (tau*Lambda)(k)=(1*log)(k)=sum_(d|k)logd
                              =(tau(k)/2)*logk.              (10)
The last equality pairs complementary divisors; it includes square
integers and proper prime powers. Since Lambda>=0, (1) gives
 |d_B(k)|<=(A/2)*tau(k)*logk.                                 (11)
The retained elementary bound tau(k)^2<=tau_4(k), and
sum_(k<=X)tau_4(k)<=X*(1+logX)^3, therefore imply
 sum_(N/8<=k<=2N)|d_B(k)|^2/k<<A^2*L^5.                      (12)
The argument does not replace this actual convolution by arbitrary
primes or discard the signs of b in the exact identity.

Write the kernel in(2) as K(a,k). Its support has k~N, and Schwartz
decay gives |K(a,k)|<<_r(1+|k-aN|/(N/T))^-r. Integer summation
and the change v=Tlog(k/(aN)) give the two bounds
 sup_a sum_k |K(a,k)|<<N/T,
 sup_k int_(1/4)^(3/4)|K(a,k)|da<<1/T.                        (13)
Here N/T>=1. Weighted Cauchy followed by(13), with coefficients
d_B(k)/sqrt k, bounds the squared norm of their sum by
 O(N/T^2)*sum_k |d_B(k)|^2/k.
Restore T^2/(4pi^2), and use(12). Thus ||P_B||_2^2<<A^2 N L^5.
The squared error in(2) is A^2 N^(41/100)L^14=o(A^2 N L^5).
This proves(3), uniformly also for N-dependent A. If A=0 it is exact.
This is an arithmetic norm of the FULL weighted field, not an estimate
on every arbitrary subset of the zeta zeros.

5. REMOVE SMOOTHING IN THE FULL FIELD, KEEP THE LENGTH MASK.
Let h_0(n)=a_T(n)*1_bad(n). Since 0<=1-exp(-n/Y)<=n/Y,
 |h(n)-h_0(n)|<=(Q/Y)*tau(n)<<N^(-1/25)*tau(n).
Apply(2)-(3) to this difference. It follows that
 ||(S_H-S_H0)/sqrtN||_2<<N^(-1/25)*L^(5/2),                  (14)
with its separate normalized transfer error bounded by
 O(N^(-67/200)*L^7). The latter is smaller asymptotically.
This permits removal of damping on the FULL field. It is not a small
pointwise difference H(rho)-H_0(rho) on each surviving zero, nor does
it remove the dyadic length mask or justify a masked-field estimate.

Without any restriction, a_T=mu_<=B*1 gives the exact identity
 (a_T*Lambda)(k)=sum_(d|k,d<=B)mu(d)*log(k/d), B=2T^(1/100). (15)
To keep the distinction explicit, put r(n)=a_T(n)-delta_1(n)-h(n).
Then for EVERY positive integer k,
 Lambda(k)+(h*Lambda)(k)
       =(mu_<=B*log)(k)-(r*Lambda)(k).                       (16)
The residual contains the complementary length ranges and the damping
correction; it is not zero by (15). Even after(14), the complement of
the bad-length mask remains. For a prime p>Q, h(1)=0 implies
(h*Lambda)(p)=0, while (a_T*Lambda)(p)=logp. For distinct primes
p,q>B with p in a bad block and q>Q, (h*Lambda)(pq)=
exp(-p/Y)*logq, whereas the full value in(15) is log(pq).
These are exact coefficient identities conditional on the stated factor
locations, not claims of a main-scale lower bound at every target.

6. WHY THIS DOES NOT YET TRANSFER THE SURVIVING PAIR SUM.
The disk |1+H(rho)|<=3/4 is proved only on the surviving set R.
Writing the full field as the R field plus the removed W field is exact,
but (2) applies to the FULL field. To subtract H times W one needs
 E_(W,H)=sum_(rho in W)|chi|^2*N^(2beta-2)*|H(rho)|^2,
or another justified bound for that restricted weighted field. The
old small E_W alone does not supply it. For example, in the middle
strip beta>=a=16/25, the crude bound from the coefficients is
 |H(rho)|<<Q^(1-a)*L<<N^(369/2500)*L.
Its square loses369/1250 in the exponent. Combined with the earlier
G energy saving4/625, the attempted upper budget is N^(361/1250);
with the Type II saving6/125 it is N^(309/1250). These POSITIVE
upper exponents only show that this particular argument gives no
small bound. They are NOT lower bounds on the actual removed fields.

An aggregate fourth moment does not immediately repair this. H^2 has
upper support exponent .82 but also products at much shorter scales.
An upper support bound cannot replace their actual length in a norm
weighted by n^-2beta. For example a single allowed bad component with
length exponent m=7/20 has squared length p=7/10. At beta=19/25,
the T-term normalized energy exponent is
 9/10+p*(1-2beta)+2beta-2=7/125>0.                            (17)
Substituting the maximal exponent .82 would give a false saving.
This fourth-moment shortcut was proposed and explicitly RETRACTED
during independent review; no masked-energy improvement is promoted.

The full-field transfer, norm and damping removal are usable arithmetic
components. The signed survivor pair estimate, its weighted-mask bridge,
and the full Goldbach margin remain OPEN. We do not assert a weighted
finite-period J_N transfer: its endpoint and replacement errors would
need to be paid with the new weights. No numerical zero experiment,
new finite Goldbach run, or external novelty claim is made.
"""
from fractions import Fraction as F

from major_arc_kernel import _factorization, _mobius_phi
from unexceptional_vaughan_gate import _divisors, mangoldt_log_vector


def density_tangent_gap(u):
    if type(u) is not F or not 0 <= u <= F(1,2):
        raise ValueError('exact u in[0,1/2] required')
    return 1-F(4,3)*(F(1,2)-u)-3*u/(1+u)


def transfer_exponents():
    q=F(41,100)
    return {'dilated_lower':1-q, 'field_error':q/2,
            'normalized_error':(q-1)/2, 'damping':q-F(9,20),
            'damping_transfer':(q-1)/2+q-F(9,20)}


def middle_mask_budget(old_energy_exponent):
    if type(old_energy_exponent) is not F or old_energy_exponent >= 0:
        raise ValueError('negative exact previous energy exponent required')
    return old_energy_exponent+2*F(41,100)*(1-F(16,25))


def moment_time_exponent(beta, product_exponent):
    if (type(beta) is not F or type(product_exponent) is not F
            or not F(1,2) <= beta <= 1 or product_exponent <= 0):
        raise ValueError('exact beta and positive actual product exponent required')
    return F(9,10)+product_exponent*(1-2*beta)+2*beta-2


def truncated_mobius_coefficient(n, cutoff):
    if type(n) is not int or n < 1 or type(cutoff) is not int or cutoff < 1:
        raise ValueError('positive integer argument and cutoff required')
    return sum(_mobius_phi(d)[0] for d in _divisors(n) if d <= cutoff)


def convolution_log_vector(n, coefficients):
    """Exact prime-log coefficients of b*Lambda for finite rational b."""
    if type(n) is not int or n < 1:
        raise ValueError('positive integer argument required')
    if any(type(k) is not int or k < 1 or type(v) is not F
           for k,v in coefficients.items()):
        raise ValueError('positive integer keys and exact coefficients required')
    out={}
    for d in _divisors(n):
        for p,c in mangoldt_log_vector(n//d):
            out[p]=out.get(p,F(0))+coefficients.get(d,F(0))*c
    return tuple((p,c) for p,c in sorted(out.items()) if c)


def full_mobius_log_vector(n, cutoff):
    """Exact prime-log coefficients on the right side of(15)."""
    truncated_mobius_coefficient(n,cutoff)  # Validate shared input domain.
    out={}
    for d in _divisors(n):
        if d <= cutoff:
            mu=_mobius_phi(d)[0]
            for p,e in _factorization(n//d):
                out[p]=out.get(p,0)+mu*e
    return tuple((p,c) for p,c in sorted(out.items()) if c)

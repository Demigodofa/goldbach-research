"""Pay spectral pairs with one height below an almost-square-root cutoff.

Owner: Kevin's Goldbach research. Purpose: determine whether the low-height
axes can carry the remaining signed main-scale term. The answer is no in
the asymptotic region proved here. The large, separated-height correlation
and the Goldbach lower margin remain OPEN. Polynomial tools are preserved.

1. UNIFORM STATEMENT.
Use the finite-period kernel J_N of smooth_endpoint_cancellation.py, with
all positive-height nontrivial zeros rho=beta+i*gamma, sigma=beta'+i*eta.
Every sum counts multiplicities: locations contribute m(rho)m(sigma), also
when they coincide. For fixed K>0 and 1<=V<=sqrtN define
 A_K(N,V)=sum_(0<gamma,eta<=KN; min(gamma,eta)<=V) |J_N(rho,sigma)|.
There is a fixed c1>0 such that, uniformly in this V,
 A_K(N,V) <<_K (logN)^14 [N exp(-c1 sqrt(logN))+sqrtN*V].               (1)
Consequently the SINGLE cutoff
 V_N=sqrtN exp[-(loglogN)^2]                                          (2)
gives A_K(N,V_N)<<_(A,K)N/log^A N for every fixed A>0. It eventually
contains each fixed N^theta, theta<1/2. Its definition does not require a
numerical zero-free constant, although the proof still uses its existence.
No numerical onset is supplied. At V=sqrtN, (1) does NOT yield a small
relative error. A fixed V=sqrtN/log^B N gives only the rate displayed in
(1), not every logarithmic saving for that one fixed B.

2. RETAIN THE CORRECT UNEQUAL-HEIGHT GAMMA POWERS.
The reviewed general phase bound in spectral_near_height_bound.py gives
 |J_N(rho,sigma)|
 << N^(beta+beta'-1) gamma^(beta-1/2) eta^(beta'-1/2)
                                      *(gamma+eta)^(1/2-beta-beta').
On dyadic scales gamma~G<=H~eta this becomes
 |J_N(rho,sigma)| << N^(b+d-1)G^(b-1/2)H^(-b),                         (3)
where b=beta and d=beta'. The H exponent is -b, NOT -b-1/2. The latter
incorrect exponent appeared in a preliminary scratch idea and was removed
before any promotion; the missing half-power invalidates that crude idea.
The bound follows from the FINITE-PERIOD partial integral, including its
endpoint transition. No infinite-line kernel is substituted.

Use the first compact height band0<gamma<=2 with tagG=1, then tags
G=2,4,8,... for (G,2G]. Actual positive ordinates have a fixed positive
lower bound, so the same comparisons cover the first band with a fixed
constant. The finitely many low-height Gamma factors have already been
paid in the reviewed phase proof. No first-zero computation is assumed.

By symmetry, enlarge the axes to Cartesian band pairs with G<=H and
G<=V, paying a factor2. In a same-band pair no ordering inside the band
is needed. Set X=(K+2)N, L=logX. Replacing the N power in (3) by the
X power costs only a fixed K-dependent factor, since -1<b+d-1<1.
The tags satisfy1<=G<=H<=X. Put g=logG/L, h=logH/L, so
0<=g<=h<=1, g<=1/2, and rewrite the majorant as
 X^-1 G^-1/2 (XG/H)^b X^d.                                           (4)
Both real-part weights are nondecreasing, because1<=XG/H<=X.

3. APPLY TWO SINGLE-ZERO DENSITY ESTIMATES BEFORE DISCARDING WEIGHTS.
For s in[1/2,1] use the retained uniform Ingham density exponent
 D(s)=3(1-s)/(2-s),
 #{rho:0<gamma<=2G, beta>=s} << G^D(s) L^5.                           (5)
The source is arXiv2507.15184v2, Corollary1/Table1, as checked in
spectral_diagonal_bound.py. Its sufficiently-high-height bound extends
over the fixed compact remainder by increasing an absolute constant:
there are finitely many such zeros, G>=1, G^D(s)>=1, and L>=1.
This extension is uniform in s and supplies no numerical zero certificate.
The total count, including beta<1/2, is O(Glog(2G)) by Riemann-von
Mangoldt. Thus the collapsed baseline b=1/2 is bounded with D(1/2)=1.

The classical zero-free region gives for the smaller band
 beta<=1-c/log(2G+3), c>0 fixed.
After replacing beta<1/2 by1/2 in the NONDECREASING weight, the upper
limit is b<=1-tau_G, where tau_G=min(1/2,c/log(2G+3)). This preserves
the zero-free saving and handles a baseline consisting only of low beta.
We can ignore the zero-free restriction on the larger band.

For1<=t<=X and a capped real-part interval[1/2,B], layer cake reads
 sum_rho t^max(beta,1/2)
 =t^(1/2)*total_count +log(t) int_(1/2)^B t^s #{rho:beta>=s}ds,
with endpoint conventions immaterial to the integral. It gives the bound
 C L^6 max_(1/2<=s<=B) t^s G^D(s).
The baseline uses the total count, not just zeros to the right of1/2.
Apply this separately to the two factors in the enlarged Cartesian band.
Every product multiplicity is retained. No statistical independence or
zero-pair correlation assumption is involved. The box costs at most
 C_K L^12 X^(max E),
 E=b+d-1+g[b-1/2+D(b)]+h[-b+D(d)],                                   (6)
where b in[1/2,1-tau_G] and d in[1/2,1].

4. TWO ENDPOINT INEQUALITIES CONTROL EVERY HEIGHT RATIO.
Write u=1-b, v=1-d in[0,1/2], and D_u=3u/(1+u). For each fixed u,v,g,
E is affine in h, so it is bounded by the larger of its values at h=g
and h=1. The two elementary inequalities used are
 D_u<=2u+1/8,                 D_u-u<=1/2.                             (7)
The first has slack (16u^2-7u+1)/(8(1+u))>0: its numerator is
16(u-7/32)^2+15/64. The second has slack
(1/2-u)(1-u)/(1+u)>=0 on this interval.
At h=g, (6)-(7) give
 E<=1-(1-2g)(u+v)-g/4.                                               (8)
At h=1 they give
 E=D_v-v+g[1/2+D_u-u]<=1/2+g.                                        (9)
In particular (8) retains the zero-free loss from the smaller band.

Put alpha=min(1,sqrt c), and split G at exp(alpha sqrtL).
For G above this point, g>=alpha/sqrtL and1-2g>=0, so (8) gives
 X^E<=X exp[-(alpha/4)sqrtL].
For G below it, eventually1-2g>=1/2 and
 u>=tau_G>=c/(2alpha sqrtL).
The latter follows from log(2G+3)<=2alpha sqrtL and, eventually,
c/(2alpha sqrtL)<=1/2. Since alpha^2<=c, (8) again gives
 X^E<=X exp[-(alpha/4)sqrtL].
Meanwhile (9) gives X^E<=sqrtX*G at the other endpoint. Consequently
the entire box costs at most
 C_K L^12 [X exp[-(alpha/4)sqrtL]+sqrtX*G].                             (10)
There are O_K(L^2) band pairs and every G<=V. Summing and replacing
X by (K+2)N proves (1), safely with c1=alpha/5. All constants are uniform
in1<=V<=sqrtN; the first compact band was included, not silently omitted.

5. APPLY THE CUTOFF WITHOUT CLAIMING THE MISSING SIGNED ESTIMATE.
For V_N in (2), eventually1<=V_N<=sqrtN, and (1) gives
 N(logN)^14 {exp[-c1 sqrt(logN)]+exp[-(loglogN)^2]}.
This is O_A(N/log^A N) for every fixed A, since
exp[-(logL)^2]*L^(A+14) tends to0. Also (1/2-theta)logN eventually
exceeds (loglogN)^2 for every fixed theta<1/2.

For the fixed delta, Psi and W_N=exp[(alpha/30)sqrt(logN)] retained
in spectral_near_height_bound.py, take K=pi+2delta. The pointwise formula
now retains only the FINITE sum C_core over
 gamma,eta>V_N, |gamma-eta|>W_N, gamma+eta<=(pi+2delta)N,
with the original weight1-Psi((gamma+eta)/N) and product multiplicities.
Deleting the UNION of axes and near-height strip costs at most the sum of
their absolute bounds, so overlap creates no extra term. Thus
 R(N)=2psi(N-1)-N+C_core+O_(A,delta)(N/log^A N).                         (11)
The full error retains the earlier opposite-sign loss. The required
signed lower margin for C_core is still OPEN. There is no new prime-pair
coverage, RH, simple-zero claim, square-root full error or numerical onset.

Source authorities remain those checked in the predecessor modules:
https://arxiv.org/pdf/2507.15184v2 (uniform density),
https://arxiv.org/abs/2107.06506 (zero counting), and
https://arxiv.org/pdf/2212.06867v1 (classical zero-free region).
The helpers/tests are exact exponent and summation-budget guards, not
actual zero computations or proof by a finite grid. No novelty claim.
"""
from fractions import Fraction as F


def density_power(u):
    if type(u) is not F or not 0<=u<=F(1,2):
        raise ValueError('rational u=1-beta in[0,1/2] required')
    return 3*u/(1+u)


def unequal_kernel_powers(beta_small, beta_large):
    if any(type(b) is not F or not 0<b<=1 for b in (beta_small,beta_large)):
        raise ValueError('rational beta in(0,1], including envelope endpoint1, required')
    return {'N':beta_small+beta_large-1,'G':beta_small-F(1,2),'H':-beta_small}


def density_box_exponent(g, h, u, v):
    if any(type(t) is not F for t in (g,h,u,v)) or not 0<=g<=h<=1:
        raise ValueError('rational0<=g<=h<=1 required')
    return 1-u-v+g*(F(1,2)-u+density_power(u))+h*(-1+u+density_power(v))


def diagonal_endpoint_envelope(g, u, v):
    if type(g) is not F or not 0<=g<=F(1,2):
        raise ValueError('rational g in[0,1/2] required')
    density_power(u)
    density_power(v)
    return 1-(1-2*g)*(u+v)-g/4


def fixed_log_width_relative_power(width_log_power):
    """Only the second term at V=sqrtN/log^B N; first term is all-log."""
    if type(width_log_power) is not F or width_log_power<0:
        raise ValueError('nonnegative rational logarithmic width power required')
    return 14-width_log_power

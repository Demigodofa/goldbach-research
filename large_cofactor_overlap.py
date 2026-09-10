"""Pay large cofactors in the conjugated and reflected prime-window forms.

Owner: Kevin's Goldbach research. Purpose: determine whether the retained
complement can be shortened by actual prime distribution, with resonant
residue lattices and hard cofactor endpoints kept. This is a restricted
correlation estimate, not the missing full signed estimate or Goldbach.

1. STATEMENT AND THE PRECISE REMAINING COMPLEMENT.
Use exactly the cutoffs, P_v, K_N and C0 of short_divisor_overlap.py:
 T=N^(9/10), H=N/T=N^(1/10), V=N^(1/8), L=logN,
 B=2N^(9/1000), a_B(n)=sum_(d|n,d<=B)mu(d).
Fix eta with 509/1000<eta<1; the concrete choice here is eta=51/100.
Put Y0=N^eta and define the actual coefficient
 v_eta(k)=sum_(n*m=k,n>=Y0)a_B(n)*Lambda(m).
The inequality n>=Y0 is literal, so equality at an integer endpoint
is included. EVERY prime power remains in Lambda(m). Then
 C_eta=(1/N)*int theta(a)^2*P_(v_eta)(aN)
                                  *conj(P_Lambda(aN))da
          =O_A(L^-A) for every fixed A>0.                    (1)
This is a complex overlap bound at each sufficiently large target N;
there is no averaging over N and no claim of an effective onset.
Section7 proves the SAME saving for the actual NONCONJUGATED reflected
prime-window form, with all integer-target residue phases retained.

The original bad coefficient h is supported below2N^.41<Y0 eventually.
Consequently the previous complement r_B=a_B-delta_1-h splits EXACTLY
as r_< + a_B*1_(n>=Y0), where
 r_<(n)=a_B(n)*1_(n<Y0)-delta_1(n)-h(n).
The completed estimate therefore gives
 C_h+C_(r_<)=-E_Lambda+O_A(L^-A), E_Lambda>=0 and O(1).       (2)
Here C_(r_<) uses the coefficient r_<*Lambda, as before. Its support
as a COFACTOR is now belowN^.51; the product index is still comparable
to N. This shorter residual is not paid, has no established sign, and
is not the old good-polynomial sum. Its damping corrections persist.
The bad ranges themselves remain intact. Equation(2) is CONJUGATED;
the separate reflected reduction below also leaves its core open.

2. NORMS, PRIME POWERS AND THE EXACT MODULUS EXPANSION.
On the retained product annulus[N/8,2N], positivity of Lambda gives
 |v_eta(k)|<=(tau*Lambda)(k)=tau(k)*logk/2.
The earlier annular tau4 mean and product-window Schur bound imply
 ||theta*P_(v_eta)/sqrtN||_2<<L^(5/2).
Replace ONLY the opposite Lambda window by Lambda_pr. Its normalized
proper-power norm is O(N^-1/4 L^(3/2)), so the overlap error is
 O(N^-1/4 L^4).                                             (3)
No prime-power replacement is made inside v_eta.

In the exact window sum k~N, the cofactor condition forces
 m<=M0=2N^(1-eta), q=d*m<=Q0=B*M0=4N^(1-eta+.009).
For eta=.51, Q0=4N^.499. Expanding a_B before taking bounds gives
 v_eta(k)=sum_(d<=B,m<=M0)mu(d)Lambda(m)
                          *1_(q|k)*1_(k>=mY0).
Thus the opposite-prime overlap is exactly
 T^2/(4pi^2 N)*sum_(d<=B,m<=M0)mu(d)Lambda(m)*sum_(r in Z)
   sum_(k=0 mod q)Lambda_pr(k+r)*g_(m,r)(k),                 (4)
where g_(m,r)(k)=1_(k>=mY0)K_N(k,k+r)/sqrt(k(k+r)).
The usual fixed smooth buffers in k/N,(k+r)/N equal1 on the kernel's
support. They make the unmasked weight smooth and zero elsewhere.
The actual cofactor indicator is left as a hard cutoff, not smoothed.

3. BV WITH THE MODULUS MULTIPLICITY AND HARD ENDPOINT PAID.
The fixed-r kernel calculation in short_divisor_overlap.py, with its
log(k/d) factor omitted, gives uniformly for any fixed J
 ||g_(m,r)||_infinity+TV(g_(m,r))
       <<_J 1/(NT)*(1+|r|/H)^-J.                            (5)
Indeed use y=Tlog(k/(aN)) and s=Tlog((k+r)/k) before differentiating
the smooth weight. Its k derivative costs1/N, notT/N, since
|N ds/dk|<<|s| on the product annulus. The extra indicator contributes
one jump of size at most the same supremum. Stieltjes partial summation
includes both its value at the endpoint and the support endpoints.
The max-endpoint distribution error also bounds its left limit, so
even a prime exactly at the cofactor boundary is included in(5).

Primary input rechecked2026-09-10: Kevin Ford, Sieve Methods2023,
Theorem3.4, printedp35 (PDFp34):
 https://ford126.web.illinois.edu/sieve2023.pdf
Its pi-minus-li form, after log-Abel with one extra logarithm, yields
 sum_(q<=Q0) E(q)<<_D N*L^-D,
 E(q)=max_((a,q)=1) max_(u<=2N)
       |sum_(p<=u,p=a mod q)logp-u/phi(q)|.                 (6)
The fixed positive gap eta-509/1000 from the half-power level allows
every fixed log saving, with constants/onset depending on that gap.
We do not assert the same conclusion at eta=509/1000, where the
source's negative logarithmic factor in the level would be missing.

If(r,q)>1, the prime sum in(4) is zero because p~N>q. Otherwise
apply(6) to p=k+r with weight(5). At a fixed q the possible pairs
(d,m) have TOTAL discrepancy coefficient
 sum_(d*m=q,d<=B,m<=M0)|mu(d)|Lambda(m)
       <=sum_(m|q)Lambda(m)=logq.                           (7)
This includes prime-power m, and charges the multiplicity by L,
not by the number of candidate m. Different m-dependent cutoffs do
not obstruct(7), because E(q) already maximizes all endpoints.
The r envelope has total mass O(H). The normalized error is therefore
 (T^2/N)*(1/(NT))*(N L^(1-D))*H=O(L^(1-D)).                 (8)
The actual comparison main is
 T^2/(4pi^2 N)*sum_(d,m)mu(d)Lambda(m)/phi(q)
                  *sum_((r,q)=1)int g_(m,r)(k)dk.            (9)

4. FREEZE THE KERNEL; BOUND RESONANCES INSTEAD OF DELETING THEM.
The previous uniform kernel approximation, multiplied by the bounded
cofactor indicator, gives the main replacement
 g_(m,r)(k) --> 1_(k>=mY0)*theta(k/N)^2/(NT)*C0(Tr/k),
 C0(s)=int hatChi(y)*conj(hatChi(y+s))dy
      =2pi*int chi(t)^2 exp(ist)dt.
The pointwise error on the buffered annulus is at most
 C_(J,K)*(1/(NT^2)+V^-K/(NT))*(1+|r|/H)^-J.                (10)
The cofactor indicator is not approximated. Its jump does not enter
this pointwise error. The physical-r to full-Z extension, including
unphysical k+r<=0 and buffer endpoints, has |r|/H comparable to T
and is absorbed by the same arbitrary Schwartz tail as before.

For fixed k~N and q, the remaining exact reduced-residue sum is
 S_q(k)=sum_((r,q)=1)C0((T/k)r)
       =sum_(e|q)mu(e)*sum_(j in Z)C0((T/k)e*j).             (11)
For e<=pi*k/T, Poisson makes the inner sum EXACTLY zero: its zero
dual mode is absent and its first positive frequency is at least2,
outside the support(1,2) of hatC0=(2pi)^2 chi^2. For larger e the
lattice spacing Te/k exceeds pi; Schwartz decay bounds the direct
lattice sum by an absolute constant. Therefore, uniformly even when
q is at a resonant scale or much larger than H,
 |S_q(k)|<<tau(q).                                         (12)
S_q need NOT be zero for these larger q. No zero-lattice claim has
been extended past its allowed spacing. The dependence of the
cofactor cutoff on k,m remains outside(11), independent of r.

5. EVERY MAIN AND APPROXIMATION BUDGET IS SMALL.
Elementary prime-power factor inequalities give
 phi(dm)>=phi(d)phi(m), tau(dm)<=tau(d)tau(m),
 n/phi(n)<=tau(n), tau(n)^2<=tau_4(n).
Also sum_(n<=X)tau_j(n)/n<=(1+logX)^j: expand the j factors and
enlarge their product constraint to the box with each factor<=X.
Using only Lambda(m)<=log(2N), these prove the conservative bounds
 S0=sum_(d<=B,m<=M0)Lambda(m)/phi(dm)<<L^2*L^3=L^5,
 S1=sum_(d<=B,m<=M0)Lambda(m)tau(dm)/phi(dm)<<L^4*L^5=L^9.
The k integral has length O(N). Thus(12) bounds the normalized
main(9) by O((T/N)*S1)=O(N^-1/10 L^9).                      (13)
In(10), sum its r envelope with mass H, integrate k over length N,
and charge S0: the normalized error is
 O(T^-1 L^5+V^-K L^5).                                     (14)
Choose K=16. Combining(3),(8),(13),(14), for every fixed D,
 |C_eta|<<_D L^(1-D)+N^-1/10 L^9+N^-9/10 L^5
                         +N^-2 L^5+N^-1/4 L^4.             (15)
Taking D>A+1, with a margin if necessary, proves(1).

6. BOUNDARY OF THE CONJUGATED RESULT.
This step pays an ACTUAL restricted complementary overlap, not just
the prediction obtained by replacing primes by a mean. BV pays the
actual discrepancy; resonant means are bounded in(12)-(13). It does
not prove a small norm of P_(v_eta), and supplies no right to delete
an arbitrary zero mask or to replace the reflected Goldbach pairing
by this conjugated form. Equation(2) still has an uncontrolled core.
For the bad cofactors n<=2N^.41, the companion m can be of scale
N^.59 or larger, so q=dm need not lie inside the BV level. This is
a boundary of THIS argument, not a barrier to all polynomial tools
or all possible arithmetic estimates.

7. THE ACTUAL NONCONJUGATED REFLECTED FORM, PROVED SEPARATELY.
Let N be an integer and w a fixed smooth function compactly supported
in(1/4,3/4). For a cofactor coefficient b, define
 R_b=(1/N)*int w(a)P_(b*Lambda)(aN)*P_Lambda((1-a)N)da.
There is NO conjugation. Let b_eta=a_B*1_(n>=Y0). We also prove
 R_(b_eta)=O_A(L^-A).                                       (16)
The opposite proper powers cost(3) by Cauchy and a->1-a. All prime
powers in the left convolution remain. The exact reflected kernel is
 K^R_N(k,l)=int w(a)F(Tlog(k/(aN)))
                              *F(Tlog(l/((1-a)N)))da.
Write l=N-k+r, so the opposite prime satisfies p=l=N-k+r and
 p=N+r mod q when q=dm divides k.
Fixed buffers can be chosen with k,l in[N/8,7N/8]; they equal1
on the exact support eventually. In particular both k and N-k
are comparable to N. Put c=k/(N-k), s=Tr/(N-k). The substitution
y=Tlog(k/(aN)) gives the exact second window argument
 z=Tlog((N-k+r)/(N-k exp(-y/T))).
The central kernel divided by sqrt(kl) has leading term
 sqrt(c)/(NT)*w(k/N)*D_c(s),
 D_c(s)=int hatChi(y)*hatChi(s-c*y)dy.                       (17)
This follows since z=s-c*y+O((s^2+y^2)/T), and the Jacobian
k/(NT) divided by sqrt(k(N-k)) is sqrt(c)/(NT).

For completeness the fixed-r variation can be obtained directly,
before this approximation. On the smooth support,
 partial_k z=T*((N+r)exp(-y/T)-N)
                    /((N-k+r)*(N-k exp(-y/T))).
Hence |N partial_k z|<<|r|/H+|y|. When the two F factors are
nonzero, |r|/H<<|y|+|z|, since |y|,|z|<=2V=o(T).
Uniform Schwartz bounds therefore prove the same(5), with one
extra cofactor jump as before. Differentiating the slowly varying
parameter c also costs1/N. To justify(17) with the error(10), first
take |r|<=c0*N for a sufficiently small fixed c0. If |y| is a
fixed fraction of |s| or larger, the first Schwartz factor pays
the polynomial error. Otherwise the intermediate arguments between
z and s-c*y have size comparable to |s|, and the second factor pays
it. The remaining |r| range has arbitrary Schwartz decay. Taylor
expansion is used only on the compact F cutoffs; replacing their
polynomial moments/correlations by full hatChi expressions has the
same V^-K tail cost. Physical endpoints and the full-Z extension
are therefore paid as in(10), without altering the cofactor cutoff.

With the angular Fourier convention, direct integration gives
 hatD_c(xi)=(2pi)^2*chi(-c*xi)*chi(-xi).                     (18)
This support is contained in(-2,-1), and c ranges over a fixed
compact subset of positive reals. The Schwartz constants are uniform
in c, including where the support intersection becomes empty.
BV now compares the opposite primes in the REDUCED residues N+r
mod q. Its multiplicity and variation errors are still(7)-(8).
The frozen reduced-residue main is
 sum_((N+r,q)=1)D_c((T/(N-k))*r)
  =sum_(e|q)mu(e)*sum_j D_c((T/(N-k))*(e*j-N)).             (19)
These are SHIFTED lattices. Poisson includes the target-dependent
phases exp(-2pi*i*ell*N/e); they are not replaced by1. For
e<=pi*(N-k)/T every dual term vanishes, including the absent zero
mode. For larger e, a direct lattice estimate using spacing>pi
is O(1) uniformly in its shift. Thus(19) is O(tau(q)), regardless
of the value of N modulo e. The bounded factor sqrt(c)w(k/N)
changes only constants. All budgets(13)-(15) carry over and prove(16).

8. CONSEQUENCE FOR THE RETAINED ACTUAL GOLDBACH BAND.
Take the existing w(a)=2*zeta(a)/sqrt(a*(1-a)), where zeta is the
central cutoff in short_prime_window_energy.py. The completed field
estimate from short_divisor_overlap.py also pairs with this reflected
P_Lambda window. The same EXACT cofactor decomposition gives
 R_h+R_(r_<)=-R_(delta_1)+O_A(L^-A).                         (20)
Here R_(delta_1) is precisely the central full-prime reflected form;
it is not a positive energy and no sign is assigned to it.

The previously paid FULL-field Guinand, beta-endpoint and actual
finite-period-kernel errors in short_prime_window_energy.py yield
 (1/N)*sum_(actual rho,sigma)chi(gamma/T)chi(gamma'/T)
                         *J_N(rho,sigma)
       =R_(delta_1)+O_A(L^-A)
       =-R_h-R_(r_<)+O_A(L^-A).                             (21)
Specifically the unweighted J-minus-beta sum is O(N^.9 L12)
and the endpoint is O(N^-.7 L13), both all-log small after division
by N. The cited central formula is S_T=-P_Lambda+O(N^1/10 L6),
so its normalized cross error is O(N^-2/5 L6), using the retained
O(1) window norm; its square is O(N^-4/5 L12). These conservative
inherited rates already suffice. No new weighted J replacement is assumed:
first use the established full-field formula, then the arithmetic
cofactor decomposition. No arbitrary zero mask is inserted.
All zero copies and real parts in that full band remain present.

Equation(21) removes the large-cofactor tail from this actual band
reduction. It still does not bound the signed sum of R_h and R_(r_<),
does not cover all heights, and proves no Goldbach positivity or
universal coverage. Polynomial tools and all earlier source/runtime
corrections are retained.
"""
from fractions import Fraction as F

from detector_prime_product_transfer import (
    convolution_log_vector, truncated_mobius_coefficient,
)
from major_arc_kernel import _mobius_phi
from unexceptional_vaughan_gate import _divisors, mangoldt_log_vector


def large_cofactor_budgets(eta=F(51, 100), distribution_log_saving=12,
                          cutoff_decay=16):
    if type(eta) is not F or not F(509, 1000) < eta < 1:
        raise ValueError('a fixed exact cofactor exponent strictly above .509 is required')
    if (type(distribution_log_saving) is not int or distribution_log_saving < 2
            or type(cutoff_decay) is not int or cutoff_decay < 1):
        raise ValueError('positive fixed integer error budgets required')
    modulus = 1-eta+F(9, 1000)
    return {'companion_exponent': 1-eta, 'modulus_exponent': modulus,
            'bv_level_gap': F(1, 2)-modulus,
            'main_error': (-F(1, 10), 9),
            'freeze_error': (-F(9, 10), 5),
            'cutoff_error': (-F(1, 8)*cutoff_decay, 5),
            'opposite_prime_power_error': (-F(1, 4), 4),
            'distribution_log_error': 1-distribution_log_saving}


def large_cofactor_log_vector(k, lower_cofactor, cutoff):
    truncated_mobius_coefficient(k, cutoff)
    if type(lower_cofactor) is not int or lower_cofactor < 2:
        raise ValueError('integer cofactor threshold at least two required')
    coefficients = {n: F(truncated_mobius_coefficient(n, cutoff))
                    for n in _divisors(k) if n >= lower_cofactor}
    return convolution_log_vector(k, coefficients)


def modulus_weight_vector(q, divisor_cutoff, companion_cap):
    """Exact positive discrepancy weight, in the formal log(prime) basis."""
    if any(type(x) is not int or x < 1
           for x in (q, divisor_cutoff, companion_cap)):
        raise ValueError('positive integer modulus and cutoffs required')
    out = {}
    for m in _divisors(q):
        d = q//m
        if d <= divisor_cutoff and m <= companion_cap:
            for p, coefficient in mangoldt_log_vector(m):
                out[p] = out.get(p, 0)+abs(_mobius_phi(d)[0])*coefficient
    return tuple((p, coefficient) for p, coefficient in sorted(out.items()) if coefficient)


def coprimality_mobius_weight(q, shift):
    if type(q) is not int or q < 1 or type(shift) is not int:
        raise ValueError('positive modulus and integer shift required')
    return sum(_mobius_phi(e)[0] for e in _divisors(q) if shift % e == 0)


def reflected_frequency_support(ratio):
    """Support intersection for chi(-c*xi)*chi(-xi), with c=ratio."""
    if type(ratio) is not F or ratio <= 0:
        raise ValueError('an exact positive reflected ratio required')
    lo, hi = max(-F(2), -F(2)/ratio), min(-F(1), -F(1)/ratio)
    return (lo, hi) if lo < hi else None

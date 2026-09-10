"""Actual cancellation for a completed short-divisor prime-window overlap.

Owner: Kevin's Goldbach research. Purpose: test expanding the Mobius
coefficient before Cauchy in the new short-shift overlap. Completion
does yield an actual estimate, already by elementary window smoothing;
a second proof uses prime distribution and Poisson. The complementary
cofactor contribution is retained explicitly. This
does not estimate the original masked correlation or prove Goldbach.

1. ARITHMETIC STATEMENT, WITH THE COFACTOR MASK DISTINCTION.
Keep T=N^(9/10), Hwin=N/T, L=logN, V=N^(1/8), fixed real
chi in C_c^infinity((1,2)), the retained Fourier cutoff nu, and real
theta smooth compactly supported in(1/4,3/4). Write
 F(y)=hatChi(y)*nu(y/V),
 P_v(x)=T/(2pi)*sum_(k>=2)v(k)/sqrtk*F(Tlog(k/x)).
Each such window is a finite sum. Put B=2*N^(9/1000). For ANY
possibly N-dependent complex b_d with |b_d|<=1, d<=B, define
 v_b(k)=sum_(d|k,d<=B)b_d*log(k/d).
Then for every fixed A>0 the ACTUAL complex overlap satisfies
 C_b=(1/N)*int theta(a)^2*P_(v_b)(aN)*conj(P_Lambda(aN))da
                                     =O_A(N^-A).             (1)
Constants are uniform in b. This is not an estimate for arbitrary
short divisor coefficients multiplied by a cofactor-dependent mask.
In fact the completed FIELD itself is smaller than every fixed inverse
power of N on the central x interval, after division by sqrtN; see2A.

For the ACTUAL a_B(n)=sum_(d|n,d<=B)mu(d), the unrestricted identity
 (a_B*Lambda)(k)=(mu_<=B*log)(k)=v_mu(k)                     (2)
puts its completed window under(1). The left-hand convolution in(2)
uses ALL prime powers. We do not replace it globally by a_B*Lambda_pr.
Only in the alternative BV proof is the opposite Lambda window
replaced by its prime-only version, with a separately paid error.

Let h(n) be the retained actual damped BAD-cofactor coefficient, and set
 r_B(n)=a_B(n)-delta_1(n)-h(n).
Then, exactly,
 v_mu=Lambda+h*Lambda+r_B*Lambda.
Define C_h,C_r with these last two coefficient windows, using the
same opposite P_Lambda and the same normalization as in(1). Equation(1)
therefore proves the actual signed balance
 C_h+C_r=-E_Lambda+O_A(N^-A),
 E_Lambda=(1/N)*int theta^2*|P_Lambda|^2>=0.                 (3)
The norm bound is E_Lambda=O(1); no positive lower bound is claimed.
The earlier bridge identifies Re C_h with the actual survivor's mixed
CONJUGATED overlap up to all-log error. C_r is NOT paid by(1).
It contains complementary cofactor lengths, damping corrections and
cofactors beyond the original allowed detector list (up to the product
scale in each finite window). It is not merely the short good sum A_N.
Thus(3) determines no sign for C_h alone, and concerns a different form
from the NONCONJUGATED reflected Goldbach pairing.

2A. STRONGER ELEMENTARY PROOF: THE COMPLETED FIELD IS SMALL.
For x in[N/4,3N/4], define the smooth compactly supported function
 f_(d,x)(u)=log(u/d)/sqrtu*F(Tlog(u/x)).
Its support has u comparable to N. Uniform Schwartz bounds for F
give, for every fixed integer M>=2,
 int|f_(d,x)^(M)(u)|du<<_M L*N^-1/2*Hwin^(1-M).             (15)
Indeed d enters only through log(u/d); each derivative of the window
costs Hwin^-1, while the amplitude derivatives cost N^-1 and are
smaller. Integrating its Schwartz envelope costs Hwin. The compact
cutoff nu and all its derivatives have uniform Schwartz bounds.

Poisson on the progression dZ gives
 sum_j f_(d,x)(dj)=(1/d)*sum_ell hatf_(d,x)(2pi*ell/d).
Integrating by parts M times in every NONZERO dual frequency bounds
their sum by O_M(L*N^-1/2*(d/Hwin)^(M-1)). Multiplying by T/sqrtN
and summing all d<=B, with |b_d|<=1, gives
 O_M(L*(B/Hwin)^M).                                        (16)
The sum of d^(M-1) costs O_M(B^M), not an unrecorded modulus loss.
All physical indices are positive and >=2 eventually; extending to
the integer lattice changes no term because of the window support.

For the ZERO dual frequency use u=x*exp(y/T) exactly:
 int f_(d,x)(u)du=sqrtx/T*int[log(x/d)+y/T]
                                      *exp(y/(2T))*F(y)dy.
Every moment int y^j*hatChi(y)dy is zero: Fourier inversion expresses
it by a derivative of chi at0, and chi vanishes on a neighborhood of0.
Taylor-expand the exponential through degree M-1 on |y|<=2V; here
V/T tends0, so the remainder is bounded by C_M|y/T|^M. Replace F
by hatChi ONLY in the polynomial terms, whose tails cost V^-K for
any fixed K after choosing a sufficiently high Schwartz seminorm.
The normalized zero mode is therefore
 O_(M,K)((L/d)*(T^-M+V^-K)).
The term y/T in the amplitude has the same bound, using one extra
finite moment. Summing 1/d over d<=B costs O(L). Altogether,
 sup_(N/4<=x<=3N/4)|P_(v_b)(x)|/sqrtN
 <<_(M,K) L^2*(T^-M+V^-K)+L*(B/Hwin)^M.                    (17)
Since B/Hwin=2N^-91/1000, increasing FIXED M,K gives O_A(N^-A)
for every fixed A. Constants may depend on A and the fixed cutoffs,
not on b or N. Pair with the retained O(1) normalized P_Lambda norm
to obtain(1). This proof does NOT need prime distribution, and does
not use cancellation between the b_d. It is elementary suppression
of the completed short-divisor field, not a two-prime estimate.

2B. NORMS FOR AN ALTERNATIVE PRIME-DISTRIBUTION PROOF.
The following independent argument proves the weaker all-log version
of(1). It was the initial route;(17) shows that BV is not necessary.
All relevant product indices k lie in[N/8,2N] eventually. Since
 |v_b(k)|<=tau(k)*log(2N), tau(k)^2<=tau_4(k),
 sum_(k in[N/8,2N])|v_b(k)|^2/k
 <=(8/N)*log(2N)^2*sum_(k<=2N)tau_4(k)<<L^5.                (4)
This is one ANNULUS, not a harmonic sum down to1. The reviewed
product-window Schur estimate gives ||P_(v_b)/sqrtN||_2<<L^(5/2).
The normalized proper-prime-power Lambda window has norm
O(N^-1/4*L^(3/2)), as paid in detector_gram_coercivity.py. Replacing
only the opposite Lambda by Lambda_pr costs O(N^-1/4*L^4).

3. PRIMARY PRIME-DISTRIBUTION INPUT AND THE WEIGHTED APPLICATION.
Freshly checked2026-09-10: Kevin Ford, Sieve Methods lecture notes2023,
Theorem3.4, printedp35:
 https://ford126.web.illinois.edu/sieve2023.pdf
It states Bombieri--Vinogradov for pi(y;q,a)-li(y)/phi(q), maximized
over y and reduced residues, summed up to x^(1/2) times a negative
log power. Log-Abel summation costs one additional logarithm and gives
the prime-log version, with arbitrarily strong fixed log saving:
 sum_(d<=B) max_((a,d)=1) max_(u<=2N)
  |sum_(p<=u,p=a mod d)logp-u/phi(d)|<<_D N*L^-D.            (5)
Harmless lower-end constants are absorbed. The fixed gap between
B=2N^.009 and the source half-power level permits every fixed D,
after increasing the source log exponent and onset. No effective
numerical onset or exceptional-zero assumption is asserted.

Use the SAME complex overlap kernel already obtained for the actual
detector:
 K_N(k,l)=int theta(a)^2*F(Tlog(k/(aN)))
                         *conj(F(Tlog(l/(aN))))da.
After the opposite prime-power replacement, expand(1), write l=k+r,
and expand v_b BEFORE taking bounds. The exact expression is
 T^2/(4pi^2*N)*sum_(d<=B)b_d*sum_(r in Z)
  sum_(k=0 mod d) log(k/d)*Lambda_pr(k+r)/sqrt(k*(k+r))
                                             *K_N(k,k+r).   (6)
There is no assumed second-prime asymptotic in(6).

For fixed d,r define the smooth weight
 g_(d,r)(k)=log(k/d)/sqrt(k*(k+r))*K_N(k,k+r).
Insert fixed smooth buffers in k/N and(k+r)/N, equal1 on the exact
kernel support and supported in(1/8,2). They change no term for large
N and allow all weights to be extended by zero. Uniformly for any J,
 ||g_(d,r)||_infinity+int|g_(d,r)'(k)|dk
        <<_J L/(N*T)*(1+|r|/Hwin)^-J.                       (7)

To justify the essential SMALL variation in k, do not differentiate the
two F factors separately and pay T/N. Instead set
 y=Tlog(k/(aN)), s=Tlog((k+r)/k),
 K_N(k,k+r)=k/(N*T)*int exp(-y/T)
             *theta((k/N)*exp(-y/T))^2*F(y)*conj(F(y+s))dy.  (8)
The frozen-cutoff factor has k derivatives of scale1/N. When k,k+r
are comparable to N, |N*ds/dk|<<|s|, so differentiating the remaining
correlation still gives a Schwartz function of r/Hwin divided by N.
Uniform weighted Schwartz bounds for F and its derivatives prove(7).
Buffer derivatives have the same scale. Endpoint terms are included.

If (r,d)>1, no prime p=k+r comparable to N lies in that residue,
because p>d. Otherwise apply(5) to p=k+r and partial summation using
(7). Summing over d and then r, whose Schwartz weight has mass O(Hwin),
the error in(6) is
 (T^2/N)*[L/(N*T)]*[N*L^-D]*Hwin=O(L^(1-D)).                (9)
The surviving main is the ACTUAL distributional comparison
 T^2/(4pi^2*N)*sum_(d<=B)b_d/phi(d)
                *sum_((r,d)=1) int g_(d,r)(k)dk.             (10)
It is residue-periodic in r, not just a constant-density heuristic.

4. FREEZE THE KERNEL WITH A PAID ERROR.
Define the full Fourier correlation
 C0(s)=int hatChi(y)*conj(hatChi(y+s))dy
      =2pi*int chi(t)^2*exp(i*s*t)dt.                        (11)
For fixed arbitrary J,K, replacing F by hatChi, freezing the smooth
factor in(8), and linearizing Tlog(1+r/k) give
 g_(d,r)(k)=log(k/d)/(N*T)*theta(k/N)^2*C0(T*r/k)
  +O_(J,K)([L/(N*T^2)+L*V^-K/(N*T)]
                                     *(1+|r|/Hwin)^-J).     (12)
This display applies on the buffered product range. To check it, first
restrict |r|<=cN with fixed sufficiently small c. The changes of the
Jacobian, theta and square-root denominator cost O((1+|y|+|s|)/T).
Also Tlog(1+r/k)-Tr/k=O(s^2/T); the intermediate arguments remain
comparable, so the derivative of C0 absorbs the polynomial s loss by
Schwartz decay. Its weighted y-moments are finite. Outside this range
both the original kernel and its proposed replacement are arbitrarily
power small by decay at |r|/Hwin comparable to T. Replacing nu loses
V^-K in any chosen Schwartz seminorm, since hatChi is Schwartz.

Extending the replacement's r sum to ALL integers adds only these
Schwartz tails: unphysical k+r<=0 or indices outside the buffered
annulus have |Tr/k| comparable to T. No positive-index or endpoint
term is silently retained. The k integral stays in a fixed interval
of length O(N). Using the deliberately crude sum_(d<=B)1/phi(d)<=B,
the normalized total error from(12) is
 O(B*L/T+B*L*V^-K).                                         (13)
The first term is N^-891/1000*L. Taking K=16 makes the second
N^-1991/1000*L. Both are smaller than every fixed negative log power.

5. POISSON ANNIHILATES EACH RESIDUE LATTICE EXACTLY.
For fixed k comparable to N and d<=B, put lambda=T/k. The angular
Fourier transform of C0 is
 hatC0(xi)=(2pi)^2*chi(xi)^2,
supported inside(1,2). For each residue a modulo d, Poisson gives
 sum_(j in Z)C0(lambda*(a+j*d))
   =1/(lambda*d)*sum_(ell in Z)exp(2pi*i*ell*a/d)
                               *hatC0(2pi*ell/(lambda*d)).   (14)
The ell=0 term is zero. Every nonzero dual frequency has magnitude
at least2pi*k/(T*d)>2 eventually: indeed T*d/k<<N^-91/1000.
Thus(14) is EXACTLY zero for EACH residue, including every reduced
residue in(10). Summing those lattices proves that the leading term
in(12) contributes zero. Equations(9),(13) and the paid opposite
prime-power error prove the all-log version of(1). No cancellation between different b_d,
and in particular no unproved cancellation in mu(d), was needed.

6. WHAT THE TEST CHANGED AND WHAT IT DID NOT.
The completed coefficient has an actual norm and overlap estimate,
not merely a formal identity reproducing a main term. The elementary
proof(15)-(17) is stronger than the initially derived BV argument:
the height window removes the slowly varying mean, and the short
progressions sample it finely enough that their nonzero dual modes
are arbitrarily small. No new prime-correlation ingredient is supplied
by this estimate. The alternative proof(5)-(14) retains a checked
way to pay actual prime discrepancies if a later mask requires it.

The bad-cofactor mask prevents replacing its divisor convolution by
v_mu. Equation(3) is the exact remaining balance; the complementary
arithmetic overlap C_r has not been bounded. Its normalized window
norm is at most O(L^(5/2)), by the identity and the retained norms,
so the current direct upper budget for its overlap is O(L^(5/2)),
not a saving. The sign, original reflected pairing and Goldbach
remain OPEN. All earlier polynomial components, the disk correction,
source corrections and runtime restrictions remain in force.
"""
from fractions import Fraction as F

from detector_prime_product_transfer import truncated_mobius_coefficient
from major_arc_kernel import _factorization
from unexceptional_vaughan_gate import _divisors


def cancellation_budgets(distribution_log_saving, cutoff_decay=16):
    if (type(distribution_log_saving) is not int or distribution_log_saving < 2
            or type(cutoff_decay) is not int or cutoff_decay < 1):
        raise ValueError('fixed positive integer error budgets required')
    t, b, v = F(9, 10), F(9, 1000), F(1, 8)
    return {'window': 1-t, 'distribution_gap': F(1, 2)-b,
            'dual_frequency_gap': 1-t-b, 'freeze_error': b-t,
            'cutoff_error': b-v*cutoff_decay,
            'prime_power_error': -F(1, 4),
            'distribution_log_error': 1-distribution_log_saving}


def elementary_window_budgets(derivatives, cutoff_decay):
    if (type(derivatives) is not int or derivatives < 2
            or type(cutoff_decay) is not int or cutoff_decay < 1):
        raise ValueError('at least two derivatives and a positive cutoff budget required')
    return {'nonzero_modes': -F(91, 1000)*derivatives,
            'zero_mode_taylor': -F(9, 10)*derivatives,
            'cutoff_tail': -F(1, 8)*cutoff_decay}


def dual_support_indices(spacing, support=(F(1), F(2))):
    """Exact geometry; spacing represents 2pi*k/(T*d), not numerical zeta data."""
    lo, hi = support
    if (type(spacing) is not F or spacing <= 0
            or type(lo) is not F or type(hi) is not F or not 0 < lo < hi):
        raise ValueError('exact positive spacing and positive open support required')
    return tuple(j for j in range(int(hi/spacing)+1) if lo < j*spacing < hi)


def divisor_log_vector(n, divisor_coefficients):
    """Exact v_b coefficient in the formal basis log(prime)."""
    if type(n) is not int or n < 1:
        raise ValueError('positive integer argument required')
    if any(type(d) is not int or d < 1 or type(b) is not F
           for d, b in divisor_coefficients.items()):
        raise ValueError('positive integer divisors and rational coefficients required')
    out = {}
    for d in _divisors(n):
        for p, exponent in _factorization(n//d):
            out[p] = out.get(p, F(0))+divisor_coefficients.get(d, F(0))*exponent
    return tuple((p, value) for p, value in sorted(out.items()) if value)


def complement_cofactor_coefficients(n, cutoff, h):
    """The exact complement on divisors of n; h is a formal rational fixture."""
    truncated_mobius_coefficient(n, cutoff)
    if any(type(k) is not int or k < 1 or type(value) is not F
           for k, value in h.items()):
        raise ValueError('integer keys and rational cofactor coefficients required')
    return {d: F(truncated_mobius_coefficient(d, cutoff))
               -F(d == 1)-h.get(d, F(0)) for d in _divisors(n)}

"""Use the prime companion's conductor gap in actual window correlations.

Owner: Kevin's Goldbach research. Purpose: test whether the two genuine
prime conditions give more than the preceding unrestricted-modulus BV
bound. A low/high character decomposition pays the next cofactor range;
the small core and the original signed Goldbach estimate remain open.

1. RESULT, WITH THE ACTUAL COFACTOR RESTRICTION.
Keep T=N^.9, H=N/T=N^.1, V=N^.125, B=2N^.009, L=logN and
a_B(n)=sum_(d|n,d<=B)mu(d), with all windows and amplitudes from
large_cofactor_overlap.py. For alpha=.46, beta=.51, put
 b_mid(n)=a_B(n)*1_(N^alpha<=n<N^beta), v_mid=b_mid*Lambda.
Both the actual conjugated overlap
 (1/N)*int theta(a)^2 P_(v_mid)(aN)*conj(P_Lambda(aN))da
and the separately defined NONCONJUGATED reflected overlap
 R_mid=(1/N)*int w(a)P_(v_mid)(aN)*P_Lambda((1-a)N)da
are O_A(L^-A) for every fixed A. The reflected statement is for
integer N, with any fixed smooth w compactly supported in(.25,.75).
There is no target average, numerical onset, or sign assumption.
More generally any FIXED .459<alpha<.51 works in place of .46;
the equality alpha=.459 is not licensed by this bound.

The earlier theorem already pays n>=N^.51, with all prime powers.
Thus the actual whole tail a_B*1_(n>=N^.46) is now paid in both
forms. The retained full T=N^.9 zero-pair band consequently satisfies
 (1/N)*sum_(actual rho,sigma)chi(gamma/T)chi(gamma'/T)J_N(rho,sigma)
       =-R_h-R_(r_core)+O_A(L^-A),
 r_core=a_B*1_(n<N^.46)-delta_1-h,                           (1)
with the existing central weight w=2zeta/sqrt(a(1-a)). This reuses
the separately paid FULL-field bridge, not a masked or newly weighted
J estimate. The actual bad h, its damping and all smaller cofactor
terms persist. Their signed sum and other height ranges remain open.

2. BOTH PRIME-POWER REPLACEMENTS ARE PAID BEFORE CHARACTERS.
The earlier divisor-Cauchy proof applies to ANY |b(n)|<=tau(n)
supported on n<=Q_cof, including b_mid. Explicitly, for
d_pp=b_mid*Lambda_pp on k~N,
 |d_pp(k)|^2<=sum_(n*m=k,m proper power)
                              tau(n)^3*tau(m)*Lambda(m)^2.
The proper-power inner count costs sqrt(N/n)L4 and
sum_(n<=Q_cof)tau(n)^3/sqrtn<<sqrt(Q_cof)L7, since tau^3<=tau8.
Hence sum_(k~N)|d_pp(k)|^2/k<<N^-1/2 sqrt(Q_cof)L11.
For Q_cof=N^.51 this is N^-49/200 L11. Product-window Schur
therefore gives normalized norm N^-49/400 L^(11/2), also for the
reflected pairing against the full opposite O(1) Lambda window.
Removing opposite proper powers then costs N^-1/4 L4, using the
retained L^(5/2) norm for the remaining left coefficient.            (2)
All statements about characters below are made AFTER these errors
are charged. In particular BOTH m and the opposite p are primes.
Prime-power m would not have the conductor gap used below.

3. EXACT MODULI, RESIDUES AND WEIGHTS.
Expand a_B(n) before Cauchy. For each m prime and d<=B set q=dm;
the product k=n*m is a multiple of q and satisfies
 m*N^alpha<=k<m*N^beta.
For the conjugated form write p=k+r and a_r=r. For the reflected
form write p=N-k+r and a_r=N+r. In both cases p=a_r modq.
The exact sum has outer factor T^2/(4pi^2 N) and coefficient
mu(d)logm times the prime-log progression sum with weight g_(m,r)(k).
This g is the appropriate kernel divided by sqrt(kp), multiplied
by the ACTUAL cofactor interval indicator. Its two endpoints remain.
The already proved fixed-r variation, now with two bounded jumps, is
 ||g_(m,r)||_infinity+TV(g_(m,r))
             <<_J (NT)^-1 W_J(r/H), W_J(t)=(1+|t|)^-J.       (3)
The substitutions k=p-r and k=N+r-p preserve total variation.
The reflected kernel and all its target-dependent phases are retained.

Product indices lie in[N/8,2N]. Therefore
 N^.49/8<=m<=2N^.54, m>B eventually, and q<=4N^.549.
Partition m into O(L) dyadic blocks M<m<=2M, with harmless endpoint
pieces; put Q=2BM for that block. Then q>M and q<=Q=o(N).
For fixed q at most one representation q=dm has m prime>B,d<=B:
two distinct such large primes would force one to divide d<=B.
Thus the coefficient logm costs at most O(L), with no polynomial
representation multiplicity. Primes p in the central annulus exceed
q for sufficiently large N; nonreduced residues have no contribution.

4. THE SMALL CONDUCTORS: EXACT PROJECTION, NOT BLANKET VANISHING.
By CRT every character modulo q=dm is a character modulo d times
one modulo the prime m. Those whose conductor does not contain m
have conductor dividing d, and their m-component is principal.
Every other character has conductor f divisible by m, hence f>M.
No assumption that every divisor f is an actual conductor is needed.

Use the common coefficient sequence A_p=logp for prime
p in[N/8,2N], zero otherwise, and prefix endpoint u<=2N. Write
A_d(a;u)=sum_(p<=u,p=a mod d) A_p. The EXACT low-conductor
projection of the progression count modulo q is
 A_low(q,a;u)=1_(m does not divide a)/(m-1)*A_d(a;u).         (4)
For (a,d)>1 both sides are zero. Indeed p>q implies that every
central prime is coprime to dm; orthogonality of all d-characters
proves(4). The factor 1_(m does not divide a) is indispensable.

Apply Bombieri--Vinogradov ONLY to d<=B, with the already sourced
max-residue/max-endpoint prime-log error E(d):
 sum_(d<=B)E(d)<<_D N L^-D.
The primary Ford Sieve Methods2023 Theorem3.4, printedp35,
 https://ford126.web.illinois.edu/sieve2023.pdf
is a prime-count statement; log-Abel costs the retained extra log.
Restricting its prime sequence to the fixed central annulus costs
at most two endpoint errors. Formula(3) pays both actual cofactor
endpoints even when an endpoint itself is prime.

The factor (m-1)^-1 in(4) makes summing all companions harmless:
 sum_(m prime in range)logm/(m-1)<<L^2.
Using the full r envelope mass O(H), the normalized low discrepancy
is (T^2/N)(NT)^-1*(N L^-D)*H*L^2=O(L^(2-D)).              (5)
Its mean has EXACTLY the expected coefficient
 1_((a,q)=1)/(phi(d)*(m-1))=1_((a,q)=1)/phi(q).
Thus the previously paid frozen reduced-residue main applies: the
conjugated and shifted reflected lattice sums are O(tau(q)), even
at resonances. The harmonic divisor estimates cost L9 for the main
and L5 for approximation. Their errors are
 O(N^-1/10 L9+N^-9/10 L5+N^-2 L5).                         (6)
They remain valid for q up to N^.549; small-modulus annihilation is
not assumed at those q. All reflected phases and both endpoints persist.

5. LARGE CONDUCTORS: A MAXIMAL ALL-RESIDUE VARIANCE.
Let A_high(q,a;u) be the contribution of the remaining characters,
each with conductor f>M, in the exact character expansion of the
central prime count. We prove, for each companion block,
 V_high=sum_(structured q<=Q)sum_((a,q)=1)
                    max_(u<=2N)|A_high(q,a;u)|^2
       <<(NQ+N^2/M)*L8.                                   (7)
The maximum is INSIDE the residue sum. We do not replace it by a
maximum of the sum or interchange these operations without proof.

Primary input checked2026-09-10: Gergely Harcos, The additive and
multiplicative large sieve inequality, Theorem2, p1 (primitive
characters), with its proof onp2:
 https://www.renyi.hu/~gharcos/large_sieve.pdf
For any common coefficients A_j in an interval I,
 sum_(f<=F)f/phi(f)*sum_(chi primitive mod f)
             |sum_(j in I)A_j chi(j)|^2
       <<(|I|+F^2)*sum_(j in I)|A_j|^2.                    (8)
There is no prime-distribution hypothesis in this inequality.

To derive(7), place the sequence in a binary interval tree of integer
length between2N and4N. Every prefix is the disjoint union of O(L)
tree intervals. For each q,a, Cauchy bounds its maximum prefix
square by O(L) times the sum of squares over ALL tree intervals.
Only then sum over reduced residues and use character orthogonality:
each interval contributes
 (1/phi(q))*sum_(chi high mod q)|sum_(p in I)A_p chi(p)|^2.

If chi is induced from a primitive chi* of conductor f|q, then
chi(p)=chi*(p) EXACTLY on our common sequence, because p>q and p
is prime. This would not be automatic for arbitrary integers or for
an unremoved prime power. Each primitive character has at most one
lift to each multiple q. The total lift weight satisfies
 sum_(q<=Q,f|q)1/phi(q)
 <=(1/phi(f))*sum_(r<=Q/f)1/phi(r)<<L2/phi(f),               (9)
using phi(fr)>=phi(f)phi(r) and r/phi(r)<=tau(r).

On a dyadic conductor block R<f<=2R, divide(8) by R and use
1/phi(f)<=R^-1*f/phi(f). Summing the conductor blocks from M
to Q geometrically bounds the lifted interval contribution by
 <<L2*(|I|/M+Q)*sum_(p in I)|A_p|^2.                       (10)
At each tree level the intervals partition the sequence and their
length is O(N*2^-j); also sum_p|A_p|^2<=O(N L2).
The sums of interval lengths over levels are O(N), whereas the
Q term repeats O(L) times. Restoring the outer prefix-Cauchy factor
therefore gives O(N^2/M*L5+NQ*L6), which is bounded by(7).
The displayed L8 deliberately leaves a log margin. No small
primitive conductor was inserted into this high-conductor estimate.

6. THE SHIFT AVERAGE GIVES AN ACTUAL POWER SAVING.
Partial summation with(3) bounds the high contribution for each q,r
by (NT)^-1 W_J(r/H) max_u|A_high(q,a_r;u)|. Since q>M>>H,
for any residue a the PERIODIZED weight is bounded uniformly:
 sum_(r=a-a0 modq)W_J(r/H)<<_J 1,                           (11)
where a0=0 or N. To see this, choose a nearest representative and
sum the two tails at distances at least (j-1/2)q. This also covers
the infinitely many Schwartz tails; we do not pretend that every
integer shift is distinct modulo q. The total q,r weight is O(QH).
Thus Cauchy over q and r, followed by(7), gives the normalized bound
 L*(T^2/N)*(NT)^-1*sqrt(QH)*sqrt(V_high)
   <<L5*(Q/sqrt(NH)+sqrt(Q/(MH)))                           (12)
for one companion block. The L outside the variance is logm.
Sum the O(L) blocks. Since Q<=2BM, m<=2N^.54,
 Q/sqrt(NH)<<N^(.549-.55)=N^-1/1000,
 sqrt(Q/(MH))<<sqrt(B/H)<<N^-91/2000.
The total high error is therefore
 O(L6*(N^-1/1000+N^-91/2000)).                              (13)
For general alpha the first exponent is .459-alpha, explaining
the strict stated range. No unproved cancellation in mu(d) is used.

Combining(2),(5),(6),(13) proves the actual band overlap estimate:
 O_D(L^(2-D)+L6*(N^-1/1000+N^-91/2000)
     +N^-49/400 L^(11/2)+N^-1/4 L4
     +N^-1/10 L9+N^-9/10 L5+N^-2 L5).                     (14)
Choose D>A+2 with a margin. Every other term is power-small.

7. UNIFORM ENDPOINTS AND A RETAINED SMOOTH-PROFILE COMPONENT.
The proof is uniform for every literal interval[U,V0) with
N^.46<=U<V0<=N^.51: the same companion range and two endpoint
jumps apply. Combining with the earlier literal-threshold proof,
which only improves when its threshold exceeds N^.51, gives an
all-log overlap bound UNIFORMLY for a_B*1_(n>=U), U>=N^.46.
For U>2N the retained windows simply contain no such cofactor.

Let f be a right-continuous bounded-variation profile on[U,infinity)
with |f(U)|+Var(f)<=C, for a fixed C. Stieltjes superposition is
 f(n)1_(n>=U)=f(U)1_(n>=U)+int_(U,infinity)1_(n>=t)df(t).
Uniformity, linearity and finite total variation therefore pay
the actual a_B(n)f(n)1_(n>=U) overlap in both forms. A bound on
variation ALONE would be insufficient for arbitrary constant profiles;
the endpoint amplitude is part of the stated hypothesis.

For example put Y1=N^.47, U=N^.46 and f(n)=exp(-n/Y1)-1.
Above U its absolute value and total variation are at most1.
Below U it has |f(n)|<=N^-.01, so the coefficient is bounded by
N^-.01 tau(n). The ordinary annular convolution/Schur bound pays
its normalized window norm by N^-.01 L^(5/2). Compare with the
already power-small completed field a_B*Lambda. It follows that
the FULL coefficient a_B(n)exp(-n/N^.47), convolved with Lambda,
has both overlaps O_A(L^-A). This auxiliary smoothing scale is
explicitly N^.47; no substitution for the detector's original
N^.45 damping or masked-zero estimate follows without another proof.

8. WHAT THE PRIME CONDITION BOUGHT, AND WHAT REMAINS.
The primality of m supplies both the exact low projection(4) and
the absence of intermediate conductors between d<=B and m. The
other prime condition makes induction exact on the common central
sequence. The short r average can then be charged against the full
large-conductor residue variance. This is an ACTUAL estimate for
the restricted two-prime expression, not a formal mean cancellation.

It shortens the unpaid cofactor core from N^.51 to N^.46 in(1),
while leaving all actual bad ranges below2N^.41, damping, signed
interactions and the all-height Goldbach coverage requirement intact.
The large-sieve bound proved here does not license alpha<=.459,
but that is a limitation of this calculation, not an impossibility
result. No worldwide novelty, positive sign, or proof of Goldbach
is claimed. Prior source corrections and runtime restrictions persist.
"""
from fractions import Fraction as F
from major_arc_kernel import _factorization
from unexceptional_vaughan_gate import _divisors


def dispersion_budgets(lower=F(46, 100), upper=F(51, 100)):
    if (type(lower) is not F or type(upper) is not F
            or not F(459, 1000) < lower < upper <= F(51, 100)):
        raise ValueError('exact cofactor endpoints inside the proved range required')
    b, h = F(9, 1000), F(1, 10)
    q = 1-lower+b
    return {'largest_modulus': q, 'bv_gap_at_largest_modulus': F(1, 2)-q,
            'high_first': q-(1+h)/2, 'high_second': (b-h)/2,
            'left_power_energy': (upper-1)/2,
            'left_power_norm': (upper-1)/4,
            'opposite_power_error': -F(1, 4),
            'low_distribution_log_loss': 2}


def conductor_candidates(d, prime_companion):
    """Partition divisor candidates; not every divisor must occur as a conductor."""
    if type(d) is not int or d < 1:
        raise ValueError('positive small divisor required')
    factors = _factorization(prime_companion)
    if factors != ((prime_companion, 1),) or prime_companion <= d:
        raise ValueError('prime companion larger than the small divisor required')
    low, high = [], []
    for f in _divisors(d*prime_companion):
        (low if d % f == 0 else high).append(f)
    return tuple(low), tuple(high)


def low_projection_weight(d, prime_companion, residue, prime_value):
    """Exact low-character projection for one central prime p>dm."""
    conductor_candidates(d, prime_companion)
    if (type(residue) is not int or type(prime_value) is not int
            or prime_value <= d*prime_companion
            or _factorization(prime_value) != ((prime_value, 1),)):
        raise ValueError('integer residue and a central prime above the modulus required')
    if residue % prime_companion == 0 or (prime_value-residue) % d:
        return F(0)
    return F(1, prime_companion-1)


def dyadic_prefix_blocks(endpoint, tree_size):
    """Disjoint aligned half-open blocks forming [0, endpoint)."""
    if (type(endpoint) is not int or type(tree_size) is not int
            or tree_size < 1 or tree_size & (tree_size-1)
            or not 0 <= endpoint <= tree_size):
        raise ValueError('power-of-two tree size and an integer prefix endpoint required')
    blocks, start, width = [], 0, tree_size
    while width:
        if start+width <= endpoint:
            blocks.append((start, start+width))
            start += width
        width //= 2
    return tuple(blocks)

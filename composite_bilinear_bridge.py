"""A composite-supported sufficient condition; its key estimate is UNPROVED.

Owner: Kevin's research. Purpose: specify a joint arithmetic estimate that
would close the pointwise step, and verify the exact decomposition separately
from that missing analytic estimate. This is not a new Goldbach coverage claim
or a historical-novelty claim. Sol reviewed the deduction and actual files;
four focused tests passed normally and with Python -O. These checks do not
establish the explicitly unproved bilinear estimate below.

Comparison sequence and known inputs:
Let N=2x, x a large integer, I=(x/2,x], 0<eps<1/12 fixed, and
  y=floor(exp(sqrt(log x))), c_y=prod_{p<=y}(1-1/p)^(-1).
On I put a_n=Lambda(N-n), b_n=c_y*1_{(N-n,P(y))=1}, w_n=a_n-b_n;
put all three sequences zero outside I. P(y) is the product of primes<=y.
Lambda denotes von Mangoldt, including proper prime powers. The rough
comparison uses ordinary roughness, not the cubic square-start survivor set.
It satisfies c_y=O(sqrt(log x)) and involves only primes up to x**o(1).

The following two inputs are unconditional, uniformly for these N=2x:
  sum_{d<=x**(1/2-eps)} max_{interval J}|sum_{k in J}w_(dk)|
      <<_{A,eps} x/log(x)**A, for each fixed A>0;           (TI)
  sum_{n in I}Lambda(n)*b_n=(1+o(1))*S_2(N)*x/2.           (MAIN)
Their source tools are Ford, Sieve Methods Lecture Notes2023, Theorems3.4
and3.6 (printed pp35,38), read2026-09-08:
https://ford126.web.illinois.edu/sieve2023.pdf
The Type I/II framework in Ford--Maynard, pp1-2, motivated this test:
https://www.ford126.web.illinois.edu/wwwpapers/prime-producing-sieves.pdf
No result requiring that paper's additional b.1/b.2 hypotheses is imported;
the implication below follows directly from the displayed convolution identity.

Details of(TI):
Put gamma=1/2-eps. Bombieri--Vinogradov, with its maximum over reduced
residues and endpoints, and Abel summation give the progression main terms
for a at every (d,N)=1 in the summed range. The residue N mod d is allowed
to depend on N; the source maximum includes it. Logarithmic factors are
absorbed by starting with a larger fixed saving. Subtracting two endpoint
estimates handles the arbitrary interval J after intersecting dk with I.
For b on a progression, a prime p<=y dividing d removes no positions if
p does not divide N, and removes every position if p|N. Otherwise it
removes exactly one residue class. In the nonzero case the main density
per k, after multiplication by c_y, is
  prod_{p|d,p<=y}p/(p-1).
Apply the fundamental lemma with D0=floor(x**((1-gamma)/2)). Its local
densities are1/p or0, satisfying the sieve dimension upper bound with
fixed uniform constants even as d,N change. Each squarefree sieve modulus
has O(1) interval remainder. Summing these remainders over d costs
  O(c_y*x**gamma*D0)=x**((1+gamma)/2+o(1)),
and s=log(D0)/log(y) is comparable to sqrt(log x), so the relative sieve
error is smaller than every fixed power of1/log x. Both estimates are
uniform even for short J; an additive remainder is retained in that case.
Missing factors p>y of d alter d/phi(d) by O(log x/(y*log y)) relatively.
The reciprocal sum of moduli sharing a prime p>y with N is at most
O(log(x)*sum_{p|N,p>y}1/p); this has the same superlogarithmic saving.
These facts, sum_{d<=x**gamma}1/phi(d)=O(log x), and endpoint errors
handle the mismatch of local densities and all large nonreduced factors.
For nonreduced progressions, a can only see proper prime powers in
[x,3x/2]. Their total over d is O(x**(1/2+o(1))), by counting divisors
of each nonzero N-q**j. The same bound handles prime-power removal in
the reduced progressions. This proves(TI), including the small shared
factors for which b is identically zero.

Details of(MAIN):
Sieve primes n in I by N-n at level floor(x**(1/3)), using weighted
Bombieri--Vinogradov obtained by Abel summation. Here the local density
is1/(p-1) for p not dividing N and0 for p|N, including p=2. These have
fixed uniform dimension bounds. Prime powers cost O(c_y*sqrt(x)*log(x)**2)
and are removed explicitly. The fundamental lemma gives main mass x/2
times c_y*V_N(y). There is the exact product identity
  c_y*V_N(y)=2*prod_{2<p<=y}(1-1/(p-1)**2)
                       *prod_{2<p<=y,p|N}(p-1)/(p-2).
Its relative difference from S_2(N) is O(1/y+log x/(y*log y)), uniformly
in N. The sieve error and the normalized BV remainder are o(x*S_2(N)).
This proves(MAIN); it does not replace the comparison by actual prime pairs.

An explicitly UNPROVED sufficient bilinear estimate:
For all complex coefficient sequences with |alpha_m|<=tau(m) and
|beta_k|<=tau(k), suppose uniformly in the sequences and in N=2x that
  |sum_{x**(1/3-eps)<=m<=x**(1/2+eps), mk in I}
                  alpha_m*beta_k*w_(mk)| <<_eps x/log(x)**3. (BII)
Coefficients may depend on N. Both m and k exceed1 for sufficiently large
x, so this estimate only samples w at COMPOSITE indices mk. Arbitrary
constant, character, or prime-only coefficient checks do not establish(BII).

Why this would give actual prime pairs:
Use Dirichlet convolution and U=V=floor(cuberoot(x)). The exact identity is
  Lambda = Lambda_<=V + mu_<=U*log
           -mu_<=U*1*Lambda_<=V + mu_>U*1*Lambda_>V.       (1)
It follows by splitting mu*log=mu*(1*Lambda) and using mu*1=epsilon_1.
The first term vanishes on I for large x. The second is controlled by(TI)
and Abel summation. Combine d<=U and m<=V in the third term into r=dm;
its coefficient h_r has |h_r|<=sum_{m|r}Lambda(m)=log r and r<=U**2.
Terms with r<=x**(1/2-eps) use(TI). The remaining r first fall in the
left factor range of(BII). If r>x**(1/2+eps), exchange r,k: then
  x/(2*U**2)<k<x**(1/2-eps),
which lies inside that range for large x. All r restrictions are retained
by setting the corresponding coefficient to zero, not by discarding terms.
For the last term of(1), group k=d*l with d>U. Its coefficients are
Lambda(m), m>U, and j_k=sum_{d|k,d>U}mu(d), k>U, with |j_k|<=tau(k).
Split at m=x**(1/2+eps) and exchange m,k above that point. The other
factor is then >U and <x**(1/2-eps), again in the allowed left range.
Dividing the Lambda or h coefficient by log x permits(BII); restoring
that factor gives O(x/log(x)**2). Therefore
  sum_{n in I}Lambda(n)*w_n=O_eps(x/log(x)**2).
Together with(MAIN) this gives a weighted actual pair sum asymptotic to
S_2(N)*N/4. Positions involving a proper prime power contribute at most
O(sqrt(N)*log(N)**3)=o(N). Remaining pair weights are at most log(N)**2.
Thus(BII) would imply, for every sufficiently large even N,
  G(N)>=S_2(N)*N/(8*log(N)**2)>0.                          (2)
G is the ordered odd-prime count. No double counting of the center or
unjustified doubling of the restricted interval is used in this lower bound.

The narrower unresolved joint estimate:
Let M=x**(1/2-eps), h_r and j_k be as above. Define
  J_N=sum_{m>U,k>U,mk in I}Lambda(m)*j_k*w_(mk)
         -sum_{r>M,rk in I}h_r*w_(rk).
Here h_r=0 for r>U**2. By(TI) and(1),
  sum_I Lambda(n)*w_n=J_N+O_{A,eps}(x/log(x)**A)
for every fixed A. Proving J_N=o(x) would suffice; bounding every pair
of coefficients as in(BII) is stronger than necessary. Neither estimate
has been proved. This is a fixed-coefficient reformulation of the pointwise
correlation problem, not evidence that the remaining estimate is easier.
It does not transfer a finite bound into an infinite positivity proof.

Finite verifier scope:
The exact helpers below verify(1) for rational arithmetic functions using
ell=1*lambda, and the local normalization by direct residue counts. Rational
prime-power weights can check that powers are retained, but are not actual
logarithms. These finite identities prove neither(TI),(MAIN), nor(BII).
"""
from fractions import Fraction

from major_arc_kernel import _mobius_phi
from redistribution import trial_prime


def vaughan_parts(values: list[int | Fraction], u: int, v: int) -> tuple[list[Fraction], ...]:
    """Four exact parts of(1); combine as part0+part1-part2+part3.

    values[n] is an arbitrary rational lambda(n), NOT asserted to be Lambda.
    Entries0 and1 must be zero. ell=1*lambda is computed as a divisor sum.
    The finite cutoff identity is valid without any prime-distribution premise.
    """
    if (type(values) is not list or len(values) < 2
            or any(type(a) not in (int, Fraction) for a in values)
            or values[0] != 0 or values[1] != 0):
        raise ValueError("require a rational list indexed from0 with entries0,1 equal0")
    limit = len(values)-1
    if any(type(a) is not int or not 1 <= a <= limit for a in (u, v)):
        raise ValueError("require exact cutoffs in1..limit")
    lam = list(map(Fraction, values))
    ones = [Fraction(0)]+[Fraction(1)]*limit
    mu = [Fraction(0)]+[Fraction(_mobius_phi(n)[0]) for n in range(1, limit+1)]

    def convolve(left, right):
        result = [Fraction(0)]*(limit+1)
        for d in range(1, limit+1):
            if left[d]:
                for k in range(1, limit//d+1):
                    result[d*k] += left[d]*right[k]
        return result

    mu_low = [value if n <= u else Fraction(0) for n, value in enumerate(mu)]
    mu_high = [value if n > u else Fraction(0) for n, value in enumerate(mu)]
    lam_low = [value if n <= v else Fraction(0) for n, value in enumerate(lam)]
    lam_high = [value if n > v else Fraction(0) for n, value in enumerate(lam)]
    ell = convolve(ones, lam)
    return (lam_low, convolve(mu_low, ell), convolve(convolve(mu_low, ones), lam_low),
            convolve(convolve(mu_high, ones), lam_high))


def rough_normalization(target: int, cutoff: int) -> tuple[Fraction, Fraction, Fraction]:
    """Return exact(c_y,V_N(y),truncated S_2(N)); no distribution assumptions.

    Small-prime testing is finite verifier arithmetic, not a Goldbach pipeline.
    The cutoff is an integer parameter, not a floating approximation to y(x).
    """
    if type(target) is not int or target < 6 or target % 2:
        raise ValueError("require an exact even target at least6")
    if type(cutoff) is not int or cutoff < 2:
        raise ValueError("require an exact integer cutoff at least2")
    c = v = Fraction(1)
    singular = Fraction(2)
    for p in range(2, cutoff+1):
        if not trial_prime(p):
            continue
        c *= Fraction(p, p-1)
        if target % p:
            v *= Fraction(p-2, p-1)
        if p > 2:
            singular *= 1-Fraction(1, (p-1)**2)
            if target % p == 0:
                singular *= Fraction(p-1, p-2)
    return c, v, singular

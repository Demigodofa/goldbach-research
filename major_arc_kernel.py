"""Major-arc kernel checks and the rough-E2 Fourier model.

Owner: Kevin's research. Purpose: verify the source-dependent kernel algebra
and preserve the error bound needed for a future additive comparison.
The finite routines accept exact rational samples of a cutoff function;
they do not certify smoothness or numerical asymptotic constants.

Source-definition correction, independently checked by Sol, 2026-09-08:
Grimmelt--Teravainen, arXiv:2508.16400v2, Theorem 1.2 (PDF printed p.5)
defines h_xi to be supported on squarefree integers and defines
  H_R(n)=tau(n)*log(R)*integral h_xi(n)/(1+|xi|)**10 dxi,
  h_xi(p)=min(1,10*(1+|xi|)*log(p)/log(R)).
Lemma 4.11 (printed p.26) then bounds the major kernel for arbitrary n by
H_R(n). This is false with that literal support condition: if p>R**2,
  Lambda_{R,1}(p*p)=sum_q mu(q)**2/phi(q)*G(log(q)/log(R))>=1,
whereas H_R(p*p)=0. For R=2,p=5, the q=1,2 terms already give >=2.
The PDF and HTML have the same support wording. This is a counterexample
to that stated pointwise bound, not to the paper's main result or Goldbach.

Use the explicitly corrected majorant Htilde_R(n)=H_R(rad(n)). Indeed,
  Lambda_{R,r}(n)=Lambda_{R,r}(rad(n))
because mu(q) restricts its q-sum to squarefree integers, and c_q(n) for
squarefree q depends only on the prime divisors of n. The coprimality
indicator is also radical-invariant. The source's Euler-product proof,
applied to the squarefree integer rad(n), gives the valid bound
  1_{(n,r)=1}*r/phi(r)*|Lambda_{R,r}(n)| <<_G Htilde_R(n),
  Htilde_R(n)=2**omega(n)*log(R)*integral
    product_{p|n} h_xi(p)/(1+|xi|)**10 dxi.
Here each local factor |1-p**(-(1-i*xi)/log R)| is <=2*h_xi(p).
The implied constant depends on the fixed smooth cutoff G; a literal unit
constant is not asserted. The same source proof uses such implied constants.
No mean or correlation bound for the corrected majorant is assumed here;
those bounds are proved separately in radical_majorant_correlation.py.

Fourier-model theorem:
Let Y be sufficiently large, exp((log Y)**(4/5))<=R<=Y**(1/400),
Y**(1/4)<=z<=Y**(2/5), and I0=(Y/2,Y]. On I0 put f(n)=S_z(n)/k_z(n),
using the checked definitions in rough_semiprime_character.py; zero outside.
Let G be fixed, smooth, nonnegative, supported in [-2,2], and equal to 1
on [0,1]. Use the source's kernel
  Lambda_{R,r}(n)=sum_{(q,r)=1} mu(q)*c_q(n)/phi(q)*G(log(r*q)/log R).
Take the exceptional-zero alternative at level R**4 and fixed small quality
kappa. If an exceptional character chi_e has conductor D<=R**2 and zero
beta, set on I0
  M_R(n)=Lambda_{R,1}(n)
         +chi_e(n)*D/phi(D)*Lambda_{R,D}(n)*n**(beta-1).
Otherwise M_R(n)=Lambda_{R,1}(n). Set M_R=0 outside I0. There is a real
E supported in I0 for which
  sup_alpha |sum_n (f(n)-M_R(n)-E(n))*exp(2*pi*i*alpha*n)|
    <<_G Y*R**(-1/3),
  |E(n)| <<_G Htilde_R(n)*epsilon,
where epsilon=exp(-c*kappa*log Y/log R) in the unexceptional case and
epsilon=(1-beta)*log Y*exp(-c*log Y/log R) in the exceptional case.
If the exceptional conductor exceeds R**2, its model term is absent, but
the exceptional error alternative still applies. Constants/onset are not
numerical, and this model need not be nonnegative.

Proof:
1. Define h=Y/R**4 and
   b_R(t)=(1/(2h))*1_{|t|<=h}*sum_q c_q(t)*G(log q/log R).
   Source Lemma 4.6 extracts the major arcs for a bulk-supported f. Its
   arcs have width R/Y, whereas our previous minor lemma used 2R/Y.
   Apply that same bilinear proof with Dirichlet Q=floor(2Y/R): off the
   narrower arcs R<q<=2Y/R and |alpha-a/q|<=q**(-2), so the bound remains
   Y*R**(-1/3). Since ||f||_infinity=O(log Y) and ||f||_1<=O(Y*log Y),
   the other two errors of Lemma 4.6 are absorbed into that bound.
2. Every prime factor of f's support is >z>R**2, so source Lemma 4.10
   applies exactly, with no small-prime discrepancy. For n at distance
   >h from both endpoints of I0, its window lies inside the normalized
   weight's valid bulk range. Reconstruct f*b_R using primitive characters
   of conductor r<=R**2. Apply our normalized character lemma with parameter
   R**4 (<=Y**(1/100)); its interval denominator divided by 2h is 3/2.
   Restricting its nonnegative sum to r<=R**2 is legitimate. The corrected
   pointwise domination above bounds the weighted character errors by
   O_G(Htilde_R(n)*epsilon).
3. The principal continuous window average is exactly 1. The exceptional
   window average of t**(beta-1) differs from n**(beta-1) by
   O((1-beta)/R**4), by the mean value theorem. Its coefficient is again
   bounded by O_G(Htilde_R(n)), so the discrepancy is absorbed into epsilon.
   This yields f*b_R=M_R+E throughout the interior. Real endpoints cause
   no problem: closed-window estimates follow as limits of the checked
   half-open interval estimates. The reconstructed expression is real.
4. Define E=0 on the two endpoint strips. The proof of source Lemma 4.6
   gives |f*b_R|<<_G (log Y)*R**2*log R. Also |c_q(n)|<=phi(q) gives
   |Lambda_{R,r}(n)|<=O_G(R**2/r), hence |M_R(n)|<=O_G(R**2).
   The strips have O(Y/R**4+1) integer points. Their discarded L1 error
   is O_G((Y/R**2+R**2)*log Y*log R), absorbed into Y*R**(-1/3).
   Combine this with (1) to prove the asserted full Fourier norm estimate.

This closes a signed Heath--Brown Fourier model with a corrected pointwise
error majorant. Its mean, second moment, additive correlation, and resulting
signed pair-error bounds are now proved in radical_majorant_correlation.py.
The signed main terms and actual-prime transfer are now checked in
signed_pair_main_term.py and prime_pair_transfer.py. Their dyadic composition
proves a power-saving exceptional set for positivity of canonical L directly.
A nonnegative-model replacement is not needed for that result. Universal
coverage and a numerical onset remain open.
Source equations and prerequisites:
https://arxiv.org/html/2508.16400v2#S4 (Definitions 4.5,4.9; Lemmas 4.6,4.10;
the squarefree Euler-product argument in the proof of Lemma 4.11).
https://arxiv.org/pdf/2508.16400v2 (printed pp.5,26 for the support mismatch).
"""
from fractions import Fraction
from math import gcd


def _factorization(n: int) -> tuple[tuple[int, int], ...]:
    if type(n) is not int or n < 1:
        raise ValueError("require a positive integer")
    factors = []
    p = 2
    while p*p <= n:
        exponent = 0
        while n % p == 0:
            n //= p
            exponent += 1
        if exponent:
            factors.append((p, exponent))
        p = 3 if p == 2 else p+2
    if n > 1:
        factors.append((n, 1))
    return tuple(factors)


def radical(n: int) -> int:
    value = 1
    for p, _ in _factorization(n):
        value *= p
    return value


def _mobius_phi(n: int) -> tuple[int, int]:
    factors = _factorization(n)
    mu = 0 if any(e > 1 for _, e in factors) else (-1)**len(factors)
    phi = n
    for p, _ in factors:
        phi = phi//p*(p-1)
    return mu, phi


def ramanujan(q: int, n: int) -> int:
    """Exact divisor formula, including negative n and n=0."""
    _factorization(q)
    if type(n) is not int:
        raise ValueError("n must be an integer")
    common = gcd(q, n)
    return sum(d*_mobius_phi(q//d)[0] for d in range(1, common+1) if common % d == 0)


def sampled_kernel(n: int, conductor: int,
                   samples: tuple[int | Fraction, ...]) -> Fraction:
    """Evaluate Lambda using supplied rational samples g(k) at index k.

    samples[k] stands for G(log(k)/log(R)); index0 is unused and the tuple
    supplies the finite support. The exact algebra accepts any rational
    samples. It does not certify the smoothness, positivity, support scale,
    or derivative bounds required by the analytic theorem.
    """
    _factorization(n)
    _factorization(conductor)
    if len(samples) < 2 or any(type(g) not in (int, Fraction) for g in samples):
        raise ValueError("samples must include index1 and contain exact rational values")
    total = Fraction(0)
    for q in range(1, (len(samples)-1)//conductor+1):
        if gcd(q, conductor) == 1:
            mu, phi = _mobius_phi(q)
            total += Fraction(mu*ramanujan(q, n), phi)*samples[q*conductor]
    return total

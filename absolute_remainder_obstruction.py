"""Actual prime triples force main-scale ABSOLUTE Vaughan remainder mass.

Owner: Kevin's Goldbach research. Purpose: test whether the logarithmic
accumulation in polynomial_joint_majorant.py can disappear through a better
absolute bound. Preserve the exact obstruction and the usable signed tools.
Sol theory and actual-file review PASS, no correction required. No scan.

STATEMENT, QUANTIFIERS AND RESTRICTIONS.
1. Use gamma in(5/12,1/2), U=V=floor(Y^(gamma/2)), and the saved fixed
   smooth nonnegative G, equal to1 on[0,1], supported in[-2,2]. Put
    B=max(1,||G||_infinity),
    0<delta<=min(1/4800,1/(80B)), S=Y^delta, L=log Y,
    E=1_(Y/2,Y](Lambda-Gamma_S).
   The EXTRA explicit small-delta condition is essential to the argument
   below; it is not silently asserted for every G at delta=1/4800. It is
   automatic under that cap if B<=60, and is compatible with choosing a
   sufficiently small fixed delta in the earlier theorem.
   Fix a smooth nonnegative physical weight F, compactly supported in
   (1/2,1)^2, with F>=f0>0 on[7/10,4/5]^2. Such a weight is admissible.
   For ANY bounded real lambda, lambda(1)=1, supported on d<=V, let
    R_lambda=(mu-lambda)*Lambda_>U*1,
   with R_lambda,p its internal-prime restriction. Define the REGROUPED
   absolute mass
    A_lambda(m)=sum_n |R_lambda(n)F(n/Y,(m-n)/Y)E(m-n)|.       (1)
   For every sufficiently large Y there is a central even m, actually in
   (7Y/5,8Y/5], for which
    A_lambda(m)>=(f0/32000)Y S_2(m)                         (2)
   SIMULTANEOUSLY for all such lambda. The same m works for R_lambda,p,
   the original hard-cutoff A, and the tuplewise absolute prime/cofactor
   majorant. Lambda may even be chosen separately for each target.
   Constants are deliberately loose; the onset is not numerical.

   Therefore a UNIFORM o(Y S_2(m)) bound for these full absolute remainders
   is false in this stated family. This is stronger than failure of an
   upper-bound budget. It is NOT a lower bound on the absolute value of
   the SIGNED total, an all-target assertion, or a Goldbach counterexample.
   No exceptional-zero hypothesis is used in this arithmetic obstruction;
   the earlier TI transfer still has its unexceptional-branch hypothesis.

THE ACTUAL PARTNER ERROR IS POSITIVE ON LARGE PRIMES.
2. If q is prime and q>S^2, every r<=S^2 is coprime to q and
   c_r(q)=mu(r). Thus the saved kernel has the EXACT prime value
    Gamma_S(q)=B_S=sum_(r<=S^2)mu(r)^2 G(log r/log S)/phi(r). (3)
   It is nonnegative and independent of the prime q in this range.
   The elementary identity n/phi(n)=sum_(d|n)mu(d)^2/phi(d) gives
    sum_(n<=X)1/phi(n)<=(1+log X)sum_(d>=1)1/(d phi(d))
                         <5(1+log X).
   Indeed phi(d)>=sqrt(d/2), as checked prime-powerwise in the preceding
   work, and sum d^(-3/2)<=1+int_1^infinity t^(-3/2)dt=3, so the
   infinite constant is at most3sqrt2<5. Hence
    B_S<=5B(1+2delta L)<=L/4                              (4)
   once L>=40B, using delta<=1/(80B). For q in(7Y/10,4Y/5],
   one also has q>S^2 and log q>=3L/4 for sufficiently large Y. Therefore
    E(q)=log q-B_S>=L/2.                                  (5)
   These are actual prime values, not an assertion of independent primality.
   No corresponding sign for E on composite partners is inferred.

A COEFFICIENT THAT NO NORMALIZED CUTOFF CAN ALTER.
3. For any prime c>V, S_lambda(c)=sum_(d|c)lambda(d)=1. For distinct
   primes p,c>max(U,V), the only nonzero internal Lambda slots at n=pc
   are p and c. For the p slot, sum_(a|c)(mu(a)-lambda(a))=0-1=-1;
   for the c slot the same argument gives-1. Consequently, exactly,
    R_lambda(pc)=R_lambda,p(pc)=A_hard(pc)=-log(pc).         (6)
   There are no internal proper prime powers at this squarefree n.
   Thus even collecting ALL decomposition terms at the same n before
   taking absolute values does not remove the coefficient in(6).

COUNT PRIME TRIPLES WHILE VARYING THE TARGET.
4. Select actual primes satisfying
    Y^(3/10)<p<=Y^(2/5),
    7Y/10<pc<=4Y/5,
    7Y/10<q<=4Y/5.                                        (7)
   Then c is required to be prime as well. For sufficiently large Y,
   p,c>max(U,V), p<c, q>c, and m=pc+q is even in(7Y/5,8Y/5].
   Both coordinates lie in the rectangle where F>=f0. Distinct triples
   give distinct pairs(m,n=pc): n is a semiprime with its UNIQUE lower
   prime p in the selected range, and q=m-n is then determined.
   This injection is needed for the regrouped bound; no representation
   multiplicity is discarded. In addition p and c do not divide m, since
   q is a different prime, so the obstruction avoids the bad leading primes.
5. Only the ordinary prime number theorem is needed. Primary check:
   Tao, 254A Notes2, December9,2014, Corollary39 and Exercise40,
   https://terrytao.wordpress.com/2014/12/09/254a-notes-2-complex-analytic-multiplicative-number-theory/
   The source gives a uniform classical error; this is unrelated to the
   excluded Linnik proposition in Notes7. From PNT and partial summation,
   for all sufficiently large Y, uniformly in the selected p,
    #{c prime:7Y/(10p)<c<=4Y/(5p)} >= Y/(20pL),
    #{q prime:7Y/10<q<=4Y/5} >= Y/(20L),
    sum_(Y^.3<p<=Y^.4)log p/p >= L/20.                    (8)
   The uniformity is routine but must be paid: Y/p>=Y^.6 tends to infinity,
   and these are fixed-relative-length intervals. The first two counts
   also follow directly from theta(bX)-theta(aX)=(b-a+o(1))X and
   log(prime)<=L. The last sum is(1/10+o(1))L by partial summation.
6. Let W_Y(m) be f0 times the sum of log p E(q) over the triples(7)
   with pc+q=m. It is nonnegative by(5), independent of lambda, and
    A_lambda(m)>=W_Y(m)
   by the injection and log(pc)>=log p. The same pointwise lower bound
   holds for each variant named in step1, including the tuplewise one.
   Summing over the central even targets using(5),(8) yields
    sum_m W_Y(m)
      >= f0 * [Y/(20L)]*[L/2]*[Y/(20L)]*[L/20]
       = f0 Y^2/16000.                                   (9)
   This counts actual triples by summing over m; it makes NO assertion
   about an individual prescribed target's prime-pair distribution.

KEEP THE SINGULAR SERIES IN THE PIGEONHOLE STEP.
7. With C2=prod_(ell>2)(1-1/(ell-1)^2)>0, write for even m
    S_2(m)=2C2 sum_(d|m,d odd squarefree)g(d),
    g(d)=prod_(ell|d)1/(ell-2).
   Since the number of positive even m<=2Y divisible by odd d is floor(Y/d),
    sum_(m even,0<m<=2Y)S_2(m)
      <=2C2 Y sum_(d odd squarefree)g(d)/d =2Y.             (10)
   The convergent Euler product cancels EXACTLY, prime by prime:
    (1-1/(ell-1)^2)*(1+1/[ell(ell-2)])=1.
   All terms used in the extension are nonnegative. Thus(9),(10) force
   some central even m with W_Y(m)/(Y S_2(m))>=f0/32000. Because W_Y is
   cutoff-independent, this SAME m proves(2) for every allowed lambda.
   Leaving S_2(m) out of this step would give a weaker and insufficiently
   normalized obstruction; the exact average handles it without assumptions.

WHAT CHANGES NEXT.
8. The per-box O(Y S_2(m)/L) bound from polynomial_joint_majorant.py remains
   useful for narrow bands and error disposal. The accumulation across a
   full exponent range cannot be improved to uniform relative smallness by
   bounding the entire remainder in absolute value: an actual prime-partner,
   semiprime-first-variable component already has the mass proved above.
   Its contribution to the signed remainder is NEGATIVE, but other parts
   can compensate it. The proof does not bound that compensation or the
   total signed value. A sufficiently strong one-sided signed bound could
   still finish the unexceptional route; absolute smallness is not necessary.
   Preserve polynomial cutoffs, the joint affine estimate, TI, balanced
   projection and conditional coverage. Reactivate an absolute argument
   only on a restricted range excluding this mass or with a different
   comparison object; do not rename full absolute summation as cancellation.

Finite guards below check the prime-model identity, surviving actual
coefficient, triple geometry, singular-series normalization and constants.
They do not run a prime-range experiment or provide a numerical PNT onset.
"""
from fractions import Fraction as F
from math import prod

from major_arc_kernel import _factorization, _mobius_phi, sampled_kernel
from unexceptional_vaughan_gate import _positive


def prime_model_constant(samples):
    samples = tuple(samples)
    if len(samples) < 2 or any(type(g) not in (int, F) or g < 0 for g in samples):
        raise ValueError('nonnegative exact kernel samples including index1 required')
    return sum((F(_mobius_phi(r)[0]**2, _mobius_phi(r)[1])*samples[r]
                for r in range(1, len(samples))), F(0))


def prime_model_pair(prime, samples):
    _positive(prime, 'prime')
    if _factorization(prime) != ((prime, 1),) or prime < len(samples):
        raise ValueError('actual prime greater than the finite kernel support required')
    return sampled_kernel(prime, 1, tuple(samples)), prime_model_constant(samples)


def prime_partner_budget(bound, delta, inverse_log_y):
    """Normalize(4)-(5) by L; this verifies assumptions, not an onset."""
    if any(type(v) is not F for v in (bound, delta, inverse_log_y)) or bound < 1:
        raise ValueError('exact parameters and B>=1 required')
    if not 0 < delta <= min(F(1, 4800), 1/(80*bound)):
        raise ValueError('the explicit small-delta condition is required')
    if not 0 < inverse_log_y <= 1/(40*bound):
        raise ValueError('requires L>=40B, with exact positive inverse L')
    model_upper = 5*bound*(inverse_log_y+2*delta)
    return model_upper, F(3, 4)-model_upper


def prime_triple_geometry(y, p, c, q, cutoff):
    for value, name in ((y, 'Y'), (cutoff, 'cutoff')):
        _positive(value, name)
    for prime in (p, c, q):
        if _factorization(prime) != ((prime, 1),):
            raise ValueError('all three entries must be actual primes')
    if not cutoff < p < c < q or not y**3 < p**10 <= y**4:
        raise ValueError('distinct ordered primes in the selected factor scales required')
    n, target = p*c, p*c+q
    if not 7*y < 10*n <= 8*y or not 7*y < 10*q <= 8*y:
        raise ValueError('the positive physical rectangle is required')
    return n, target, F(n, y), F(q, y)


def singular_local_cancellation(prime):
    if _factorization(prime) != ((prime, 1),) or prime <= 2:
        raise ValueError('odd prime required')
    return (1-F(1, (prime-1)**2))*(1+F(1, prime*(prime-2)))


def finite_singular_average(y, primes):
    """Exact finite Euler-product counterpart of the mean bound(10)."""
    _positive(y, 'Y')
    primes = tuple(primes)
    if len(primes) > 12 or len(set(primes)) != len(primes):
        raise ValueError('at most12 distinct odd primes required')
    for prime in primes:
        singular_local_cancellation(prime)
    c2 = prod((1-F(1, (p-1)**2) for p in primes), start=F(1))
    direct = sum((2*c2*prod((F(p-1, p-2) for p in primes if m % p == 0), start=F(1))
                  for m in range(2, 2*y+1, 2)), F(0))
    divisors = [(1, F(1))]
    for p in primes:
        divisors += [(d*p, g/F(p-2)) for d, g in list(divisors)]
    expanded = 2*c2*sum((g*(y//d) for d, g in divisors), F(0))
    return direct, expanded, F(2*y)


def absolute_mass_constants():
    """PNT lower constants, partner error and singular-series average paid."""
    average = F(1, 20)*F(1, 2)*F(1, 20)*F(1, 20)
    return average, average/2

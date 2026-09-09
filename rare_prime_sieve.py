"""Rare-sign prime candidates with rough partners on suppressed classes.

Owner: Kevin's research. Purpose: isolate the necessary rare-prime side of
the unresolved pair correlation and sieve its partners with relative errors.
The finite helpers check residues, local densities and factor multiplicity.
They neither detect an exceptional zero nor provide an asymptotic onset.
Sol checked the deduction and actual files. Five focused tests passed
normally and with Python -O; the tests verify finite algebra only.

Conditional theorem, with the deduction independently checked by Sol:
Let I=(Y/2,Y], m even in[5Y/4,7Y/4], J_m={n:n,m-n in I}. Let chi be
primitive quadratic of conductor D>24 with an ACTUAL real zero beta, and
assume
  D<=Y**(delta/4), 0<t=(1-beta)*log(Y)<=1/log(Y), m in F_D.
Here F_D={B=0,C=-A} is exactly the earlier suppression family, not a set
of counterexamples. Fix sufficiently small delta>0, then a sufficiently
large integer u, both independent of Y,D,m,beta. Set
  E=floor(Y**delta), z=ceil(Y**(delta/u)).
For sufficiently large Y there are at least
  c_delta*Y*t/log(Y)**2                                   (1)
primes p in J_m with chi(p)=+1, gcd(m-p,D)=1, and P^-(m-p)>z.
Every such partner has chi(m-p)=-1 and Omega(m-p)<u/delta, where
Omega counts prime factors WITH MULTIPLICITY. This is a bounded-almost-
prime partner theorem with a rare-sign first prime. It is not a prime
partner theorem, a P_2 bound, an actual zero, or new Goldbach coverage.
The onset is ineffective; no numerical delta,u or threshold is supplied.

Exact character mechanism:
1. C=-A says that the sum of A numbers in{+1,-1} equals -A, so EVERY
   allowed unit pair has chi(a)*chi(m-a)=-1. B=0 gives exactly A/2
   allowed residues of each sign. On F_D all prime divisors>=5 of D
   divide m. Their allowed proportions are1; the 2-part also contributes1
   (an 8-part needs m=0 or4 mod8 for C/A to be -1). Only a 3-part can
   reduce the proportion, by1/2 when 3 does not divide m. Consequently
     A/phi(D) is in{1,1/2}.                              (2)
   Thus every actual prime pair with both entries>D has one sign+ and
   one sign-. In a reflection-invariant interval such as J_m, its ordered
   prime-pair count is exactly twice the number with first prime of sign+.
   There is no prime diagonal in this regime. The word 'rare' acquires
   its analytic meaning from the ACTUAL exceptional-zero hypothesis;
   an arbitrary finite character is not known to have rare positive primes.

Relative weighted sieve proof:
2. Let L=log(Y), and let J_real be the real interval cut out by I and m-I.
   It has length >=Y/4. Use the nonnegative weight log(p) on primes p in
   J_m for which chi(p)=+1 and gcd(m-p,D)=1. Put
     X=A/(2*phi(D))*integral_{J_real}(1-v**(beta-1))dv.
   Uniformly for v in J_real, 1-v**(beta-1)=t*(1+O(t+1/L)); hence
     X=(1+o(1))*A/(2*phi(D))*length(J_real)*t.
   In particular X is comparable to Y*t by (2). Integer endpoint choices
   are retained by the progression formulas, not used as exact integrals.
3. For squarefree d<=E, coprime to Dm, the condition d|(m-p) gives
   exactly A/2 reduced residue classes modulo Dd, by CRT. The exceptional
   character is +1 on every one. Apply the quantitative Linnik estimate
   from the bulk source deduction in relative_type_i.py: Thorner--Zaman
   Theorem2.1 and equation(4.2), https://arxiv.org/html/2108.10878#S2 .
   This replaces the earlier Tao exposition with its acknowledged
   Proposition23 proof gap. On J_real the main term for each class is
     integral_{J_real}(1-v**(beta-1))dv/phi(Dd),
   and the error inside Y/phi(Dd) is
     O(exp(-c*log(Y)/log(Dd)*log(1/e_d)))
                   +O(L**2/(Dd)),
     e_d=(1-beta)*log(Dd)<=5*delta*t/4.
   Since Dd<=Y**(5*delta/4), a sufficiently small fixed delta ensures
   y>=(Dd)**C and c*log(y)/log(Dd)>=8. Thus the first error is O(t**8).
   Subtract the two endpoints. The weighted divisor count has main X/phi(d)
   and error bounded by
     O(Y*A/phi(D)/phi(d)*(t**8+L**2/(Dd)))                (3)
   before removing proper prime powers. No density factor A/phi(D) is
   discarded until its uniform lower bound (2) has been established.
4. If d shares a prime with D, the partner condition makes its count zero.
   If it shares a prime with m but not D, a prime p in this progression
   would have to equal a prime divisor of d<Y/2, impossible on J_m.
   Hence the multiplicative local density is
     g(ell)=1/(ell-1) for primes ell not dividing Dm,
     g(ell)=0 for primes ell dividing Dm.
   This includes g(2)=0. For d=1 the empty product gives g(1)=1.
   Summing (3) over the relevant squarefree d<=E, and using
   sum_{d<=E}1/phi(d)<<L and sum_d1/(d*phi(d))<infinity, gives
     sum |r_d| << Y*A/phi(D)*(t**8*L+L**2/D)
                                      +Y**(1/2+o(1)). (4)
   The final term removes proper prime powers globally: each p**j in J_m,
   j>=2, is counted at most tau(m-p**j)=Y**o(1) times; m-p**j is nonzero.
   Their total logarithmic weight is Y**(1/2+o(1)). The prime counts on
   nonreduced d are already zero, so no prime-power density is imported.
5. For the partner sieve, the dimension-one condition holds with fixed
   uniform constants: for ell>=3, g(ell)<=1/(ell-1), and deleting local
   factors can only decrease the dimension product. Mertens' product and
   the convergent correction product give uniformly
     V(z)=prod_{ell<=z}(1-g(ell)) >>1/log(z).
   Use Ford, Sieve Methods Lecture Notes2023, Theorem3.6(a,b), printed p38:
   https://ford126.web.illinois.edu/sieve2023.pdf
   The lower sieve has squarefree support d<=E, |lambda_d|<=1 and a
   relative main error exp(-s*log(s)+s*log_3(s)+O(s)), with fixed uniform
   constants. Here s=max(100,log(E)/log(z)); choose u sufficiently large
   so this error is <1/2 throughout [u-1,u]. Our integer choices give
   s in that interval eventually, and 2<=z<=sqrt(E).
6. The exceptional quality (or directly t<=1/L) and Siegel bounds give
     t>>_a D**(-a), D>>_H L**H
   for every fixed a,H>0, as in relative_type_i.py. Therefore (4), divided
   by X/log(z), is at most a constant times
     t**7*L**2 + L**3/(D*t) + Y**(-1/2+o(1))*L/t=o(1).
   The first term is at most L**(-5); the other terms follow from Siegel
   and D<=Y**(delta/4). The lower sieve proves weighted mass >>Y*t/log(z).
   Each prime weight is <=log(Y), proving (1). Every counted partner is
   <=Y with all prime factors>z>=Y**(delta/u). Their product proves the
   strict multiplicity bound Omega(m-p)<u/delta, without rounding a root.

Remaining arithmetic gap:
The partner sign -1 does NOT force primality. For example D=31,m=2790,
p=1459 is a sign+ prime, while m-p=1331=11**3 is sign- and has no prime
factor<=10; chi_31(11)=-1. This finite identity asserts no exceptional zero
for D=31. A sign- integer has an odd number of sign- prime factors, counted
with multiplicity. If its total Omega is even, it therefore has at least
one sign+ factor; if Omega is odd it can have none. Even a semiprime can
have sign- by including one factor of each sign. What is missing is
control excluding all such composite partners,
or a positive lower bound for the prime partners inside this candidate pool.
Neither the sign decomposition nor the bounded-almost-prime result supplies it.
"""
from fractions import Fraction
from math import gcd

from exceptional_character_model import character_values, pair_moments
from major_arc_kernel import _mobius_phi


def suppressed_residue_split(conductor: int, target: int, *, two_sign: int = 1
                             ) -> tuple[Fraction, tuple[int, ...], tuple[int, ...]]:
    """Exact allowed-unit proportion, sign+ residues, sign- residues on F_D.

    Requires a primitive quadratic D>24 and an even target in F_D. This is
    finite residue algebra, not a claim that a zero exists or primes are rare.
    """
    if type(conductor) is not int or conductor <= 24:
        raise ValueError("require an integer primitive conductor D>24")
    a, b, c = pair_moments(conductor, target, two_sign=two_sign)
    if b != 0 or c != -a:
        raise ValueError("target must belong to the suppression family F_D")
    chi = character_values(conductor, two_sign=two_sign)
    allowed = [r for r in range(conductor) if chi[r] and chi[(target-r) % conductor]]
    positive = tuple(r for r in allowed if chi[r] == 1)
    negative = tuple(r for r in allowed if chi[r] == -1)
    return Fraction(a, sum(bool(v) for v in chi)), positive, negative


def rare_sieve_density(conductor: int, target: int, divisor: int, *, two_sign: int = 1
                       ) -> Fraction:
    """Exact g(d) relative to X for the rare-prime partner sieve.

    d is positive and squarefree; d=1 has density1. Factors shared with
    D or the target give density0. This coefficient is not an actual count.
    """
    suppressed_residue_split(conductor, target, two_sign=two_sign)
    mu, phi = _mobius_phi(divisor)
    if mu == 0:
        raise ValueError("divisor must be squarefree")
    return Fraction(0) if gcd(divisor, conductor*target) > 1 else Fraction(1, phi)


def rough_factor_limit(upper: int, cutoff: int) -> int:
    """Upper bound on Omega(n) for 1<=n<=upper with every prime factor>cutoff.

    Uses integer multiplication and counts repeated factors. The bound can
    be loose when cutoff+1 is composite; it never identifies n as prime.
    """
    if any(type(v) is not int for v in (upper, cutoff)) or upper < 1 or cutoff < 2:
        raise ValueError("require integers upper>=1 and cutoff>=2")
    factors, product = 0, 1
    while product <= upper//(cutoff+1):
        product *= cutoff+1
        factors += 1
    return factors

"""A positive corrected comparison, with an incompatible old Type I premise.

Owner: Kevin's research. Purpose: retain the exceptional character in a
prime-versus-model comparison and audit its use in composite_bilinear_bridge.
This is not a prime-pair theorem, a zero detection, or a novelty claim.
Sol checked the analytic deductions and actual verifier. Four focused tests
passed normally and with Python -O; they do not establish analytic estimates.

Positive prime-versus-model theorem:
Let N be large and even, I=(N/4,N/2], and let Q be even with
  exp(sqrt(log N))<=Q<=N**rho,
where rho>0 is a sufficiently small fixed constant, rho<1/7. Suppose a
primitive quadratic character chi of conductor D>24 dividing Q has an
exceptional zero beta of level Q and a sufficiently small fixed quality
kappa, in the sense of source Definition7.1. Set
  c_Q=Q/phi(Q), b(t)=c_Q*1_{(t,Q)=1}*(1-chi(t)*t**(beta-1)),
  F(t)=log(t)*1_{t prime}, T=sum_{n in I} F(n)*b(N-n),
  t0=(1-beta)*log N, mu=min(1,t0).
The comparison b is nonnegative but includes composites. It is NOT the
large-subpower-presieve comparison of composite_bilinear_bridge.py.

On the allowed residues Omega={a modQ: (a,Q)=(N-a,Q)=1}, define
  A=|Omega|, B=sum_Omega chi(a), C=sum_Omega chi(a)*chi(N-a),
  K=Q*A/phi(Q)**2.
Then, uniformly under these premises,
  T=K*integral_I [1-(B/A)*(u+v)+(C/A)*u*v] dt
       +O(K*N*t0*exp(-c*log N/log Q)+K),                 (1)
where u=t**(beta-1), v=(N-t)**(beta-1). Consequently
  T >> K*N*mu > 0.                                       (2)
Constants and onset are not numerical. The zero is a hypothesis.

Primary source: Grimmelt--Teravainen, arXiv:2508.16400v2,
Definition7.1, equation(7.2), and Lemma7.4, checked2026-09-08:
https://arxiv.org/html/2508.16400v2#S7.SS2
We use the character-mean lemma directly, not the source's disputed
squarefree-supported majorant or a claim about pointwise Fourier errors.

Proof of(1):
Expand c_Q*1_{(N-a,Q)=1} and its product with chi(N-a) in multiplicative
characters on the units moduloQ. Every coefficient has absolute value<=K.
The principal coefficients are K and K*B/A; the exceptional coefficients
are K*B/A and K*C/A. Reflection interchanges the two linear character sums.
Each character moduloQ induces a DISTINCT primitive character of conductor
dividingQ. All primes in I exceedQ, so their values agree exactly with
the induced characters. Apply the source's sum over primitive characters;
the maximum coefficient K means no phi(Q) or logarithmic multiplicity loss.
On this bulk interval, multiplying the prime-indicator formula by log(t)
via Abel summation cancels its logarithmic normalization. A second Abel
step handles v: its supremum and total variation are bounded absolutely.
The source main densities are1 and -u. Thus the resulting density is
K-K*(B/A)*u-v*(K*B/A-K*(C/A)*u), as displayed. The discrete main densities
can be integrated with O(K) total cost; only the principal and exceptional
characters contribute. Prime powers never enter F.

Proof of the positive margin:
CRT shows that B/A and C/A agree with the moments at conductorD: extra
prime factors and higher prime powers in Q multiply all three moments by
the same positive count. In exceptional_character_model.py let
  P=A-(u+v)B+uvC, S=A+(u+v)B+uvC.
Its proved inequality5P>=3S gives8P>=3(P+S)=6(A+uvC). Therefore
  P/A >= (3/4)*(1-uv) >= (3/8)*mu,
since t(N-t)>=N on I for N>=6 and1-exp(-t0)>=min(1,t0)/2.
The main integral is at least3*K*N*mu/32. Put s=logN/logQ. The exceptional
quality gives t0<=kappa*s. Hence the relative error in(1) is bounded by
a constant times max(1,kappa*s)*exp(-c*s), uniformly for s>=1/rho, and
is absorbed by choosing rho sufficiently small. The source's effective
lower bound1-beta >>D**(-1/2)/log(D)**2 absorbs the O(K) term. Finally
K=2*prod_{p|Q,p>2,p not dividing N}(1-1/(p-1)**2)
       *prod_{p|Q,p>2,p dividing N}p/(p-1) >=1.
This includes the suppressed classes: their model margin is small, positive,
and proportional to mu. No prime-versus-prime positivity follows from T.

Compatibility obstruction, unconditional:
Let0<rho<1 be fixed. More generally take any Q-periodic functions f,g,
with mean1 and0 respectively, |f|,|g|<=M=N**o(1), Q<=N**rho. Let
  b(t)=f(t)-t**(beta-1)*g(t), beta in[1/2,1],
where g=0 is allowed and no actual zero is required. For a prime ell not
dividing NQ, complete periods and Abel summation give
  sum_{ell*k in I} b(N-ell*k)=N/(4*ell)+O(M*Q).
Let L=logN and take primes ell in(2L,4L] not dividing NQ. The prime number
theorem gives total logarithmic mass(2+o(1))*L in that interval, while
prime factors of NQ use at most(1+rho)*L. Thus there are
>>_rho L/logL eligible primes. Their reciprocal-square sum is
>>_rho 1/(L*logL).
Bombieri--Vinogradov, including maxima over reduced residues and endpoints,
with Abel log weighting, gives TOTAL progression error O_A(N/log(N)**A)
when comparing sum Lambda(N-ell*k) to N/(4*(ell-1)). We only select a
subset of the moduli in that theorem. Passing from log-weighted primes
to Lambda costs O(sqrt(N)*log(N)**4) across these logarithmically sized
moduli, also negligible. Thus the signed sum of discrepancies
over these ell has positive main term
  (N/4)*sum_ell 1/(ell*(ell-1)) >>_rho N/(logN*loglogN).
The summed O(MQ) errors are smaller by a power of N, and BV with A=3
is smaller as well. It follows that, for any fixed gamma>0,
  sum_{d<=N**gamma} max_J |sum_{k in J, dk in I}
       (Lambda(N-dk)-b(N-dk))| >>_rho N/(logN*loglogN).    (3)
In particular the earlier Type I premise fails already for its requested
A=2 logarithmic saving. This holds for the corrected comparison above:
f=c_Q*1_unit has mean1, g=f*chi has mean0, and M=c_Q=N**o(1).
The same obstruction holds without a character. Primary BV source:
Ford, Sieve Methods Lecture Notes2023, Theorem3.4, printedp35:
https://ford126.web.illinois.edu/sieve2023.pdf

This closes a positive comparison main term but prevents simply inserting
that comparison into the old Vaughan argument. Equation(3) does not exclude
cancellation among the specific signed Vaughan coefficients, a larger
sieve model, or a different decomposition. Those require further estimates.
The finite helpers below verify only residue normalization and complete
period arithmetic. No test proves(1), its zero premise, BV, or Goldbach.
"""
from fractions import Fraction
from math import gcd

from exceptional_character_model import character_values


def periodic_pair_data(conductor: int, modulus: int, target: int,
                       u: int | Fraction, v: int | Fraction, *, two_sign: int = 1
                       ) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Return exact(K,B/A,C/A,P/A) for a small finite character model.

    Q must be an even multiple of the primitive D>24. u,v are exact formal
    weights in[0,1], not supplied zero estimates. No analytic range is checked.
    """
    if type(conductor) is not int or conductor <= 24:
        raise ValueError("require an exact primitive conductor D>24")
    chi = character_values(conductor, two_sign=two_sign)
    if (type(modulus) is not int or modulus < 2 or modulus % 2
            or modulus % conductor):
        raise ValueError("require an exact even modulus divisible by D")
    if type(target) is not int or target < 6 or target % 2:
        raise ValueError("require an exact even target at least6")
    if any(type(t) not in (int, Fraction) or not 0 <= t <= 1 for t in (u, v)):
        raise ValueError("require exact rational weights in[0,1]")
    units = [a for a in range(modulus) if gcd(a, modulus) == 1]
    allowed = [a for a in units if gcd(target-a, modulus) == 1]
    a_count = len(allowed)
    b_sum = sum(chi[a % conductor] for a in allowed)
    c_sum = sum(chi[a % conductor]*chi[(target-a) % conductor] for a in allowed)
    k = Fraction(modulus*a_count, len(units)**2)
    b_ratio, c_ratio = Fraction(b_sum, a_count), Fraction(c_sum, a_count)
    u, v = Fraction(u), Fraction(v)
    return k, b_ratio, c_ratio, 1-(u+v)*b_ratio+u*v*c_ratio


def periodic_progression_sum(values: list[int | Fraction], target: int,
                             divisor: int, first_index: int, terms: int) -> Fraction:
    """Exactly sum f(target-divisor*k) for a finite consecutive k interval.

    values lists one FULL period, in residue order starting at0. The divisor
    must be coprime to the period; it need not be prime. Signed rational
    entries are allowed. This computes periodic arithmetic, not prime counts.
    """
    if (type(values) is not list or not values
            or any(type(t) not in (int, Fraction) for t in values)):
        raise ValueError("require a nonempty exact rational period")
    if (any(type(t) is not int for t in (target, divisor, first_index, terms))
            or divisor < 1 or terms < 0 or gcd(divisor, len(values)) != 1):
        raise ValueError("require exact indices, nonnegative length, coprime divisor")
    cycles, tail = divmod(terms, len(values))
    result = Fraction(cycles)*sum(values)
    for j in range(tail):
        result += values[(target-divisor*(first_index+j)) % len(values)]
    return result

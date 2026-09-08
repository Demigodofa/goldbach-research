"""Exact residue model for the prime/rough-semiprime comparison.

Owner: Kevin's research. Purpose: check whether a quadratic character bias
can reverse the positive model margin before attempting an analytic transfer.
These functions evaluate FINITE CHARACTER MODELS, not prime counts or L(N).

Let chi be a primitive nonprincipal real character of conductor D, N even,
and Omega={a mod D: (a,D)=(N-a,D)=1}. Write
  A=|Omega|, B=sum_Omega chi(a), C=sum_Omega chi(a)*chi(N-a).
For 0<=u,v<=1, define the nonnegative model pair counts
  P=A-(u+v)*B+u*v*C, S=A+(u+v)*B+u*v*C.
The two linear sums agree by a -> N-a. The signs are motivated by the
exact multiplicative-group identity, for every unit n modulo D:
  sum_{a unit}(1-u*chi(a))*(1-v*chi(n/a))/phi(D)
    = 1+u*v*chi(n).
Orthogonality removes both linear terms, and multiplicativity gives the
last term. This identity does NOT assume actual primes are independent.

Finite comparison lemma: if D>21, P>=3*S/5 for all even N and u,v in [0,1].
Proof: a primitive real conductor has odd squarefree part and 2-part 1,4,
or 8. For even D, all odd residues at the 2-part are allowed because N is
even; its nonprincipal character sum is zero. Hence B=0 and P=S. For odd
D, Chinese remaindering gives local values at an odd prime p dividing D:
  p|N:  A_p=p-1, B_p=0,          C_p=chi_p(-1)*(p-1);
  p does not divide N: A_p=p-2, B_p=-chi_p(N), C_p=-chi_p(-1).
The last identity follows by scaling a=N*t and counting solutions to
y*y=t*(1-t), or by the usual quadratic character sum. Thus if (N,D)>1,
B=0 again. Otherwise A=prod(p-2), |B|=|C|=1. For D>21 this product is
at least 9: either D has a prime >=11, or D is 35 or 105. Consequently
epsilon=|B|/A<=1/9. If B<=0, P>=S. If B>0, the bilinear polynomial
  5*P-3*S=2*(A+u*v*C)-8*(u+v)*B
is nonnegative at the four corners of [0,1]^2: the worst corner is (1,1),
where it is at least 2*A-18*B>=0. Bilinear interpolation proves the claim.
For 0<=rho<=49/100 this implies P-rho*S >= (11/60)*P >= 0.

Powers-of-two corollary: for N=2**j, j>=1, D>24, P>=2*A/3, and therefore
  P-rho*S >= 11*A/90 > 0,  0<=rho<=49/100.
For odd D, use |B|,|C|<=A/9. For even D, B=0; its odd part must contain
a prime p>=5 (otherwise D is 4,8,12,24). Since p does not divide N, its
normalized correlation has modulus 1/(p-2)<=1/3. All other local normalized
correlations have modulus <=1, so |C|<=A/3. Also A>0 for every even N.
The stronger absolute margin here concerns this model only.

Connection and unclosed analytic prerequisites:
Grimmelt--Teravainen, arXiv:2508.16400v2, Section 1.2.5 and Theorem 7.9,
https://arxiv.org/html/2508.16400v2 , treat a possible exceptional character
in a power-saving Fourier approximation. Their stated theorem covers primes
and a specified three-prime weight, not our cubic rough-semiprime indicator.
Transferring the comparison still requires a proved approximation for that
indicator, its correctly normalized kernel and opposite character sign,
convolution error bounds relative to possibly suppressed main terms, and
control of endpoints and sieve remainders. No power-saving exceptional-set
theorem for canonical L, or pointwise theorem for powers of two, follows
from this finite lemma. The bound log(2)<25/36<7/10 motivates rho<=49/100;
it does not certify the omitted analytic errors.
The actual rough-semiprime character mean, its bulk normalization, and a
minor-arc estimate have since been proved in `rough_semiprime_character.py`.
A signed Fourier model with a corrected pointwise majorant is now proved
in `major_arc_kernel.py`. The nonnegative model replacement and additive
convolution transfer remain open.
"""
from fractions import Fraction


def character_values(conductor: int, *, two_sign: int = 1) -> tuple[int, ...]:
    """Construct a primitive real character; two_sign selects chi_8 or chi_-8.

    All odd local components are Legendre characters. The 4-component is
    chi_-4. For a conductor with 8-component, two_sign=1 gives chi_8 and
    two_sign=-1 gives chi_-8. A negative sign is invalid without 8-component.
    Enumerating a conductor is intended for small exact verification only.
    """
    if type(conductor) is not int or conductor < 3:
        raise ValueError("conductor must be an integer >=3")
    if type(two_sign) is not int or two_sign not in (-1, 1):
        raise ValueError("two_sign must be the integer -1 or 1")
    rest, two_power = conductor, 0
    while rest % 2 == 0:
        rest //= 2
        two_power += 1
    if two_power not in (0, 2, 3) or (two_power != 3 and two_sign != 1):
        raise ValueError("primitive quadratic 2-part must be 1,4,8")
    primes = []
    p = 3
    while p * p <= rest:
        if rest % p == 0:
            primes.append(p)
            rest //= p
            if rest % p == 0:
                raise ValueError("odd conductor part must be squarefree")
        p += 2
    if rest > 1:
        primes.append(rest)
    values = []
    for a in range(conductor):
        value = 1
        if two_power:
            if a % 2 == 0:
                value = 0
            elif two_power == 2:
                value = 1 if a % 4 == 1 else -1
            else:
                value = 1 if a % 8 in (1, 7) else -1
                if two_sign == -1 and a % 4 == 3:
                    value = -value
        for p in primes:
            residue = pow(a, (p - 1) // 2, p)
            value *= -1 if residue == p - 1 else residue
        values.append(value)
    return tuple(values)


def pair_moments(conductor: int, target: int, *, two_sign: int = 1) -> tuple[int, int, int]:
    """Return exact A,B,C for the even target's complete residue period."""
    if type(target) is not int or target % 2:
        raise ValueError("target must be an even integer")
    chi = character_values(conductor, two_sign=two_sign)
    allowed = [a for a in range(conductor) if chi[a] and chi[(target-a) % conductor]]
    return (len(allowed), sum(chi[a] for a in allowed),
            sum(chi[a] * chi[(target-a) % conductor] for a in allowed))


def pair_models(conductor: int, target: int, u: int | Fraction, v: int | Fraction,
                *, two_sign: int = 1) -> tuple[Fraction, Fraction]:
    """Evaluate exact P,S; no floating endpoints or prime-count interpretation."""
    if any(type(t) not in (int, Fraction) or not 0 <= t <= 1 for t in (u, v)):
        raise ValueError("u,v must be exact integers or Fractions in [0,1]")
    a, b, c = pair_moments(conductor, target, two_sign=two_sign)
    u, v = Fraction(u), Fraction(v)
    return a - (u+v)*b + u*v*c, a + (u+v)*b + u*v*c

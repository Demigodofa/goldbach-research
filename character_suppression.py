"""Locate the arithmetic family where the signed character margin can vanish.

Owner: Kevin's research. Purpose: isolate the possible small-conductor
suppression before attempting to control the remaining Fourier exceptions.
These exact helpers concern a FINITE CHARACTER MODEL. They neither detect
an exceptional zero nor classify actual Goldbach counterexamples.
Sol also checked the actual verifier and transfer statement. Four finite
tests passed normally and with Python -O, including complete character
periods, both 8-component signs, parity, rational margins, and band edges.

Localization lemma (Sol reviewed the argument, 2026-09-08):
Let D>24 be a primitive quadratic conductor, with either primitive sign
at an 8-component. Write D=q*h, where q is the product of its prime
divisors >=5. Then h is in {1,3,4,8,12,24}, and q>1. Use A,B,C,P,S
from exceptional_character_model.py, with an even target m and u,v in [0,1].
Define F_D={even m: B=0 and C=-A}. Then
  F_D is contained in {m:q divides m};
  outside F_D, P>=2*A/3 and P-(49/100)*S>=11*A/90;
  inside F_D, P=S=A*(1-u*v).
In particular F_D occupies at most 24 residue classes modulo D. Parity
is an additional restriction when D is odd; the verifier incorporates it
by returning even residues modulo lcm(2,D).

Proof:
At an odd prime p|D the normalized C-factor is chi_p(-1) if p|m,
and -chi_p(-1)/(p-2) otherwise. If some p>=5|D misses m, then
|C|<=A/3. If B=0 this gives P>=A-|C|>=2*A/3. If B is nonzero,
D is odd and (m,D)=1: |B|=|C|=1, A>=9, so P>=A-3>=2*A/3.
If instead q|m, then q>1 forces B=0. The remaining local factors are
from 3 and the 2-part, hence C/A is in {-1,0,1}. Outside C=-A this
gives P>=A; inside it P=S=A*(1-u*v). The already proved comparison
P>=3*S/5 gives P-(49/100)*S>=11*P/60, proving the stated margin.

Exact local rule when q|m:
The primes >=5 contribute epsilon_q=product (-1)**((p-1)//2).
The 3-component contributes -1 if 3|m, and +1 otherwise. The 4-component
contributes -1 at m=0 mod4 and +1 at m=2 mod4. For the 8-component,
writing sigma=+1 for chi_8 and -1 for chi_-8, the contribution is sigma
at m=0 mod8, -sigma at m=4 mod8, and 0 at m=2 or6 mod8.
Missing components contribute 1. The product is -1 exactly on F_D.

Transfer to the ACTUAL canonical bound, in the small-conductor case only:
Use Y=2X, R=Y**delta and all hypotheses of prime_pair_transfer.py, with
an exceptional conductor 24<D<=R**(1/4). Its complete Euler-product
pair expansion has error O(YR**(-1/3)). Outside F_D the lemma above
replaces its suppressed margin by an absolute positive margin. The
pointwise error e=t*exp(-c/delta), t=(1-beta)*log Y=O(1/delta), is
absorbed for sufficiently small fixed delta. The existing Parseval bound
  sum_m |Q_+/-|**2 <<_delta Y**3*R**(-2/3)*log(Y)**2
then excludes at most O_delta(YR**(-1/2)) targets at a fixed threshold
c0*Y. Outside both F_D AND that additional Fourier-residual set,
  L(m) >>_delta Y/log(Y)**2,  m in [Y/2,Y],
for sufficiently large Y. Unweighting and removal of the end segments
are exactly the proved steps 5-6 of prime_pair_transfer.py.

Inside F_D the previous mu=min(1,t) margin remains valid, so the number
of targets with L<=0 there is bounded by
  min(O(Y/D+1), O_delta(YR**(-2/3)*log(Y)**2/mu**2)).
The first term follows from at most 24 classes, an absolute constant.
This localizes suppression; it does NOT say all actual exceptions are
in F_D, remove the large-conductor gcd exclusion, or certify a named
uncomputed target. No numerical constants/onset or historical novelty
are asserted. The unstructured Fourier-residual family remains open.
"""
from math import lcm

from major_arc_kernel import _factorization


def suppression_classes(conductor: int, *, two_sign: int = 1
                        ) -> tuple[int, int, tuple[int, ...]]:
    """Return (q, period, residues) for exactly F_D, including even parity.

    D>24 must be a primitive quadratic conductor. The return is a finite
    model classification, not prime flags or a claim of an exceptional zero.
    Only at most 24 cofactor residues are inspected after factoring D.
    """
    if type(conductor) is not int or conductor <= 24:
        raise ValueError("require an integer primitive conductor D>24")
    if type(two_sign) is not int or two_sign not in (-1, 1):
        raise ValueError("two_sign must be integer -1 or 1")
    factors = _factorization(conductor)
    exponent2 = next((e for p, e in factors if p == 2), 0)
    if (exponent2 not in (0, 2, 3)
            or any(e != 1 for p, e in factors if p != 2)
            or (two_sign != 1 and exponent2 != 3)):
        raise ValueError("primitive quadratic 2-part is 1,4,8; odd part is squarefree")
    q = 1
    large_sign = 1
    for p, _ in factors:
        if p >= 5:
            q *= p
            large_sign *= 1 if p % 4 == 1 else -1
    period = lcm(2, conductor)
    residues = []
    for multiple in range(period//q):
        target = q*multiple
        if target % 2:
            continue
        correlation = large_sign
        if conductor % 3 == 0:
            correlation *= -1 if target % 3 == 0 else 1
        if exponent2 == 2:
            correlation *= -1 if target % 4 == 0 else 1
        elif exponent2 == 3:
            correlation *= {0: two_sign, 4: -two_sign}.get(target % 8, 0)
        if correlation == -1:
            residues.append(target)
    return q, period, tuple(residues)


def count_suppression_targets(conductor: int, first: int, last: int,
                              *, two_sign: int = 1) -> int:
    """Count the exact finite model family in an inclusive positive even band."""
    if (type(first) is not int or type(last) is not int or first < 2
            or first % 2 or last % 2 or last < first):
        raise ValueError("require a nonempty positive even band")
    _, period, residues = suppression_classes(conductor, two_sign=two_sign)
    return sum((last-r)//period-(first-1-r)//period for r in residues)

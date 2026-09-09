"""Monotone Euler cutoffs remove the coarse large-conductor gcd exclusion.

Owner: Kevin's research. Purpose: transfer the exact suppression classes to
every active exceptional conductor. This is a proof prerequisite with finite
coefficient verifiers, not a prime sieve or an explicit Goldbach certificate.
Sol reviewed the mathematical argument and actual verifier on 2026-09-08.
Four focused tests passed normally and with Python -O, including the
independent Euler expansion and a negative nonmonotone-cutoff control.

Additional permissible choice: fix the smooth cutoff G from the preceding
Fourier theorems with 0<=G<=1 and G nonincreasing on [0,infinity). It remains
1 on [0,1] and supported in [-2,2]. Such cutoffs exist, and all preceding
results hold for this subclass. Their assertions for arbitrary G are not
being changed. The canonical bound L itself is independent of this choice.

Uniform Euler lemma:
For a positive even m and any positive D, let
  a(r)=mu(r)**2*c_r(m)/phi(r)**2,
  U_D=sum_{(r,D)=1}a(r)*G(log(D*r)/log R)**2,
  S_out=product_{p not dividing D}(1+a(p)).
Then S_out>0 and 0<=U_D<=(5/2)*S_out. No small-D condition is required.

Proof of nonnegativity:
Put f(s)=G(log(s)/log R)**2 for s>=1. For squarefree r, split r=a*b,
where a has prime factors dividing m, and b has prime factors not dividing
m*D; primes dividing D are excluded throughout. The a-coefficient is
positive. For fixed a, the inner b-sum is at least
  f(D*a)*(1-sum_{b>1}|coefficient(b)|)
  = f(D*a)*(2-product_{p not dividing m*D}(1+1/(p-1)**2)).
Here f(Dab)<=f(Da); positive b>1 terms may be discarded in a lower bound.
The negative-prime set omits 2 because m is even. Its product is at most
  (5/4)*exp(sum_{k>=2}1/(4*k*k))
  <=(5/4)*exp(1/4)<5/3.
The sum is bounded by an integral, and exp(x)<1/(1-x) for 0<x<1.
Thus each inner sum is at least f(Da)/3, proving U_D>=0.

Proof of the upper bound:
The absolute Euler sum converges: there are only finitely many primes
dividing the positive m, and all remaining terms are O(1/p**2).
Since 0<=f<=1, divide that absolute sum by S_out. Every positive local
factor cancels. The ratio is at most
  product_{p odd}(1+1/(p-1)**2)/(1-1/(p-1)**2)
  <=(5/3)*exp(sum_{k>=2}2/(4*k*k-1))
  =(5/3)*exp(1/3)<5/2.
Use log(1+x)<=x and
2/(4*k*k-1)=1/(2*k-1)-1/(2*k+1) for the telescoping sum.
This also proves uniformity in m,D and the cutoff.

Large-conductor consequence:
Use the exact periodic coefficients of signed_pair_main_term.py and put
theta=U_D/S_out in [0,5/2]. Apart from the already proved U0-S_2 error,
the pair coefficient normalized by S_2(m) is
  1 +/- theta*(B/A)*(u+v)+theta*(C/A)*u*v.
For rho=49/100, its minus-minus-rho-plus difference is
  (1-rho)*(1+theta*(C/A)*u*v)
       -(1+rho)*theta*(B/A)*(u+v).                         (1)
Outside the exact family F_D of character_suppression.py:
* If B=0, then C/A>=-1/3. Hence (1)>=(1-rho)/6=17/200.
* If B is nonzero, D is odd, (m,D)=1, and |B|=|C|=1.
  Here A=product_{p|D}(p-2)>=sqrt(D/3), since p-2>=sqrt(p)
  for p>=5, and the possible factor at3 is 1. Thus for D>R**(1/4),
  the exceptional terms in (1) are o(1). Explicitly A>=20 suffices
  for (1)>=17/400, using
    (1-rho)-(5/2)*(3+rho)/A >= 59/800 >17/400 at A=20.
The bound on A holds eventually uniformly throughout this large-D range.
The exact periodic error O(R**8) and principal coefficient error
O(YR**(-1/3)) are negligible. This proves a fixed positive signed-model
margin for all R**(1/4)<D<=R**2 outside F_D, with NO gcd-cover exclusion.

Transfer and resulting actual theorem:
Take Y=2X and R=Y**delta, for fixed sufficiently small delta>0, using
the dyadic composition and all hypotheses of prime_pair_transfer.py.
Absorb its pointwise errors with the fixed margin and then its Fourier
pair residual at threshold c0*Y. For every active exceptional conductor
24<D<=R**2, the actual bound satisfies
  L(m)>>_delta Y/log(Y)**2
outside BOTH F_D and a separate O_delta(YR**(-1/2)) Fourier-residual set,
for even m in [Y/2,Y] and sufficiently large Y. For small D this is the
previously checked transfer; the argument above handles large D. With no
active model term, set F_D empty and use the principal margin.

For large D, F_D contains O(Y/D+1)=O(YR**(-1/4)) targets. For small D,
the previous suppressed-margin estimate still leaves at most
O_delta(YR**(-1/3)) possible failures, including its Fourier residuals.
Consequently L(m)>0 for all but O_delta(X**(1-delta/4)) even m in [X,2X].
This replaces the previous delta/8 exceptional-size exponent. It does
not strengthen the old half-main-term lower bound to this exceptional
size. The remaining Fourier errors and suppressed classes can still
contain targets; no numerical exponent/onset, universal Goldbach coverage,
named uncomputed interval, or historical novelty is asserted.

Siegel refinement of the ACTUAL canonical-L theorem:
Sol checked the deduction and actual proof text on 2026-09-08.
For the same sufficiently small fixed delta>0 and EVERY fixed 0<k<2/3,
  #{even m in[X,2X]: L(m)<=0} <<_{delta,k} X**(1-delta*k). (2)
The starting threshold and constants in this refinement are ineffective.
This is an asymptotic conclusion from the existing unconditional analytic
inputs, not an additional assumption that an exceptional zero exists.
The earlier effective zero-distance argument and its delta/4 exponent
remain available separately; no effective onset was supplied for that result.

Additional primary input: Matomaki--Merikoski, Siegel zeros, twin primes,
Goldbach's conjecture, and primes in short intervals, IMRN2023, equation(6):
https://arxiv.org/html/2112.11412v2
Siegel's theorem gives eta <<_epsilon D**epsilon, for every fixed epsilon>0,
when a primitive quadratic character has a real zero
beta=1-1/(eta*log D), eta>=10. Its constants are ineffective.
Only this zero-distance estimate is used here, not the paper's conditional
pointwise Goldbach theorem or its separate target-range hypotheses.

Proof with explicit exponent slack:
Keep Y=2X, R=Y**delta and all dyadic intervals, cutoffs, normalizations,
and error identities from prime_pair_transfer.py. Set
  a=1/3+k/2, tau=1/6-k/4, so 1/3<a<2/3 and 0<tau<1/6.
Split the active exceptional conductor at D=R**a.

For D<=R**a, the exact periodic formulas in signed_pair_main_term.py
already hold for every D<=R**2. Its absolute Euler tail, with Q=R/D,
now gives error per unit length
  O((D/R)**(1/2)*exp(O(sqrt(log Y))))
    =O(R**(-(1-a)/2+o(1))).
This includes the D*(|B|+|C|)/phi(D)**2 multiplier. The principal error
O(R**(-1/3)) and the periodic error O(R**8/Y) are unchanged. Thus the
full character-moment comparison extends beyond the earlier D<=R**(1/4).
If eta>=10, choose epsilon=tau/(2*a) in Siegel's estimate. Then
  t=(1-beta)*log Y >>_{delta,k} R**(-tau/2),
since D**epsilon<=R**(tau/2) and log Y/log D>=1/(a*delta).
If eta<10, directly t>=1/(10*a*delta). In either case
  mu=min(1,t) >>_{delta,k} R**(-tau).
The positive suppressed-model margin therefore survives uniformly, including
targets in F_D: (1-a)/2-tau=1/6, 1/3>tau, and R**8/Y=o(R**(-tau)).
The already checked pointwise errors are proportional to t and are absorbed
by the same sufficiently small fixed delta, before applying Siegel's lower
bound. Their absorption does not require an effective Siegel constant.

Use the unsimplified Fourier residual energy from prime_pair_transfer.py:
  sum_m |Q_+/-|**2 <<_delta Y**3*R**(-2/3)*log(Y)**2.
At threshold c*Y*mu this discards at most
  O_{delta,k}(Y*R**(-2/3+2*tau)*log(Y)**2)
    =O_{delta,k}(Y*R**(-a)*log(Y)**2).
The old omitted endpoints O(YR**(-1/2)) are o(Y*mu/log(Y)**2), so its
unweighting and cubic-composite containment still give actual L(m)>0.

For D>R**a, the monotone-cutoff argument above supplies a fixed margin
outside F_D; it applies since a>1/4. The discarded arithmetic family has
O(Y/D+1)=O(YR**(-a)) targets. At a fixed margin the SAME Fourier energy
discards O_delta(YR**(-2/3)*log(Y)**2), retaining its full exponent instead
of the earlier convenient R**(-1/2) simplification. The absent-model case
uses this latter bound too. Finally a-k=1/3-k/2>0 absorbs the logarithms
and proves(2), with all analytic constants and fixed cutoffs accounted for.

For example k=1/2 gives an exceptional-size exponent delta/2 in place of
delta/4 for the SAME delta. No k=2/3 endpoint, numerical delta or onset,
uniformity as k approaches2/3, half-main-term bound on this smaller set,
or coverage of every even integer is asserted. The Fourier-residual set
can remain nonempty. This strengthens this recursive bound's theorem;
it is not a claim to improve the literature's best Goldbach exceptional set.
"""
from fractions import Fraction
from math import gcd

from major_arc_kernel import _mobius_phi, ramanujan


def cutoff_euler_sum(target: int, conductor: int,
                     weights: tuple[int | Fraction, ...]) -> Fraction:
    """Compute U_D from exact nonincreasing cofactor weights in [0,1].

    weights[r] represents G(log(D*r)/log R)**2; index0 is unused, and
    weights past the last index are zero. Finite samples do not certify
    smoothness, an exceptional character, or actual prime counts.
    """
    if type(target) is not int or target < 2 or target % 2:
        raise ValueError("target must be a positive even integer")
    if type(conductor) is not int or conductor < 1:
        raise ValueError("conductor must be a positive integer")
    if len(weights) < 2 or any(type(w) not in (int, Fraction) for w in weights):
        raise ValueError("weights must contain index1 and exact rational values")
    if (any(not 0 <= w <= 1 for w in weights[1:])
            or any(weights[r] < weights[r+1] for r in range(1, len(weights)-1))):
        raise ValueError("cofactor weights must be nonincreasing in [0,1]")
    result = Fraction(0)
    for r in range(1, len(weights)):
        if gcd(r, conductor) == 1:
            mu, phi = _mobius_phi(r)
            result += Fraction(mu*mu*ramanujan(r, target), phi*phi)*weights[r]
    return result


def normalized_comparison(a: int, b: int, c: int,
                          theta: int | Fraction, u: int | Fraction,
                          v: int | Fraction) -> Fraction:
    """Evaluate (1) exactly; supplied moments are not certified as characters."""
    if (any(type(n) is not int for n in (a, b, c)) or a < 1
            or abs(b) > a or abs(c) > a):
        raise ValueError("require integer moments A>0 and |B|,|C|<=A")
    if any(type(t) not in (int, Fraction) for t in (theta, u, v)):
        raise ValueError("theta,u,v must be exact rationals")
    if not 0 <= theta <= Fraction(5, 2) or not 0 <= u <= 1 or not 0 <= v <= 1:
        raise ValueError("require theta in [0,5/2] and u,v in [0,1]")
    theta, u, v = Fraction(theta), Fraction(u), Fraction(v)
    rho = Fraction(49, 100)
    return ((1-rho)*(1+theta*Fraction(c, a)*u*v)
            -(1+rho)*theta*Fraction(b, a)*(u+v))

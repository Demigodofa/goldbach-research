"""Identify what the formal composite cancellation does, and does not, add.

Owner: Kevin's research. Purpose: test whether the cancellation noticed in
quintic_loss_budget.py supplies a new estimate for the ACTUAL signed loss.
It instead equals a polynomial already present in the accessible divisor
main. The arithmetic discrepancy and complementary divisor sum remain
uncontrolled. No prime-pair positivity or new actual coverage is claimed.
Sol checked the theory and actual files. Five focused exact tests passed
normally and with Python -O.

Exact formal theorem:
Let f be any normalized polynomial of degree d, f(0)=0, f(1)=1. Set
h(x)=f(1-x)-f(x), and fix 0<=theta<1/d. For odd k define
  J_k(x)=sum_{S subset {1,...,k}}(-1)^|S| f(sum_{i not in S}x_i),
  I_k(theta)=1/k! * integral_{sum x_i=1, x_i>=theta}
                      J_k(x)/product x_i dx_1...dx_(k-1).
For k=1 the integral means evaluation at x1=1, giving I_1=1.
Every J_k is divisible by product x_i, and J_k=0 when k>d. Thus all
integrals below are ordinary finite polynomial integrals, including theta0.
With V having the normalized Dickman density exp(-gamma)*rho(v), put
  B_f(theta)=-E[h'(theta*V)]/2.
Then EXACTLY
  sum_{1<=k<=d, k odd} I_k(theta)=B_f(theta).           (1)
In particular B_f(0)=(f'(0)+f'(1))/2=A_f, so the total FORMAL composite
integral is A_f-1. The quintic cancellation at theta0 was forced by A_f=1;
it was not a second, independent estimate for actual composite partners.
No density interpretation for the factor-share measure is assumed.

Source input and exact moments:
Gorodetsky's ViBrANT seminar notes, Section2, printed p2, give
  integral_0^infinity exp(-s*v)*rho(v)dv
    =exp(gamma+integral_0^1 (exp(-s*v)-1)dv/v):
https://people.maths.ox.ac.uk/gorodetsky/vibrant.pdf
Hence M(t)=E exp(tV)=exp(integral_0^1(exp(t*v)-1)dv/v).
Writing mu_n=E V^n, the identity t*M'(t)=M(t)*(exp(t)-1) yields
  mu_0=1, mu_n=(1/n)*sum_{j=0}^{n-1}binom(n,j)*mu_j.
The first five are 1,1,3/2,17/6,19/3. These are exact moments, not
decimal samples of rho or an assertion about actual prime factors.

Proof of(1), by a finite coefficient calculation:
Use the exponential generating parameter t for f(x)=x^j and work only
through degree d. The finite difference of exp(t*x) is
product_i(exp(t*x_i)-1). Define g_theta,t(x)=(exp(t*x)-1)/x for x>=theta
and zero otherwise. The sum of odd convolution powers g^{*k}(1)/k! has
Laplace transform sinh(G), where for real s>|t|,
  G=log(s/(s-t))-J,
  J=integral_0^theta (exp(t*x)-1)*exp(-s*x)dx/x.
Consequently
  sinh(G)=1/2*(s/(s-t)*exp(-J)-(s-t)/s*exp(J)).         (2)
The inverse transforms b_plus,b_minus of exp(+J),exp(-J) are a unit
atom at0 plus convolution series of the compactly supported function
(exp(t*x)-1)/x on[0,theta]. Its coefficient t^j has support[0,j*theta].
Since d*theta<1, every coefficient through degree d of the direct b terms
vanishes at x=1. In the remaining convolutions, integrals ending at1 can
be extended to infinity coefficientwise. Thus the generating expression
at x=1, through degree d, becomes
  t/2*(exp(t)*M(-theta*t)+M(theta*t)).                 (3)
For example the first term uses the Laplace transform of b_minus at s=t,
which is exp(integral_0^theta(exp(-t*x)-1)dx/x)=M(-theta*t).
Expression(3) is precisely -E[h'(theta*V)]/2 for the exponential input,
coefficient by coefficient. Linearity proves(1) for every polynomial.
Only finitely many convolution powers affect each coefficient, so no
infinite formal interchange or distributional prime hypothesis is used.
At theta0, b_plus=b_minus is just the atom at0 and the same calculation
gives t*(exp(t)+1)/2 directly. The strict cutoff condition is material;
beyond it, compactly supported terms can reach x=1 and cannot be dropped.

The quintic example, now with a nonzero cutoff:
For f(s)=s-kappa*s^2*(1-s)^2*(1-2s) and 0<=theta<1/5,
  I_3=-(kappa/12)*(1-3theta)^2*(1+10theta-15theta^2),
  I_5= (kappa/12)*(1-5theta)^4,
  B_f=1-2kappa*theta+18kappa*theta^2
           -(170/3)kappa*theta^3+(190/3)kappa*theta^4. (4)
Thus I_3+I_5=B_f-1 exactly. Taking positive parts destroys this signed
identity; it does not bound the positive loss from quintic_loss_budget.py.

Link to the ACTUAL accessible divisor main, with the errors retained:
In the existing actual-zero regime, write a=1/2-2epsilon and
Z=length(J_real)*S_2(m)*t. The previous Type-I proof gives
  T_low/Z=F_f(a,theta)+O_f(eta_s/theta^2)+o_Y(1),
where eta_s is the fixed fundamental-lemma error and
  F_f=[h(a)*rho(a/theta)-theta*integral_0^(a/theta)
                   h'(theta*v)*rho(v)dv]/(2theta*exp(gamma)).
This is the SAME pool and normalization as cubic_positivity_obstruction.py
and log_weight_barrier.py. The helper below bounds the exact difference
F_f-B_f by a rational factorial tail. It does NOT remove the fixed sieve
error or certify a numerical onset for the actual prime sum.
Indeed, if h'(x)=sum b_j*x^j and m=floor(a/theta)>=max(2,2*deg(h')),
  |F_f-B_f| <= [|h(a)|/theta
                +3*sum_j |b_j|*theta^j*(m+1)^j]/(2*m!). (5)
Use rho(v)<=1/floor(v)! from its delay equation. On successive unit
intervals the bound for v^j*rho(v) has ratio at most2/(m+1)<=2/3:
(1+1/(n+1))^j<=1/(1-j/(n+1))<=2. This proves the geometric tail
factor3, and exp(-gamma)<1 bounds the endpoint term without decimals.
For fixed f,a this tail decreases faster than every power of theta.
Choose u first, then Y; no growing-degree, growing-u or new uniformity.

Precise remaining arithmetic question:
Let C_actual=T_f-P be the EXACT composite contribution, including any
previously negligible classes, and let T_boundary=T_f-T_low. Define
  Delta=C_actual-(B_f(theta)-1)*Z.
There is an exact bookkeeping identity
  P/Z-1 = T_boundary/Z-Delta/Z+(T_low/Z-B_f(theta)).    (6)
The last parenthesis is controlled to a chosen tolerance by the existing
parameter order. Neither T_boundary nor Delta has a sufficient signed
bound. Replacing Delta by0 because of(1) would ASSUME the missing prime
correlation. This pursuit therefore closes the formal-to-Type-I identity
but does not close the arithmetic cancellation or Goldbach gap.
"""
from fractions import Fraction as F
from itertools import product
from math import comb, factorial, prod

from log_weight_barrier import _coefficients, semiprime_kernel


def _inputs(coefficients, theta, max_degree=64):
    values = _coefficients(coefficients)
    while values[-1] == 0:
        values = values[:-1]
    degree = len(values)-1
    if degree > max_degree:
        raise ValueError(f"finite verifier supports degree at most {max_degree}")
    if type(theta) is not F or not 0 <= theta < F(1, degree):
        raise ValueError("require exact Fraction 0<=theta<1/degree")
    return values


def dickman_moments(order: int) -> tuple[F, ...]:
    """Exact normalized Dickman moments through order<=64, not prime moments."""
    if type(order) is not int or not 0 <= order <= 64:
        raise ValueError("require integer moment order in[0,64]")
    moments = [F(1)]
    for n in range(1, order+1):
        moments.append(sum(comb(n, j)*moments[j] for j in range(n))/n)
    return tuple(moments)


def formal_dickman_main(coefficients: tuple, theta: F) -> F:
    """B_f(theta)=-E h'(theta*V)/2; not the full actual prime correlation."""
    values = _inputs(coefficients, theta)
    h = semiprime_kernel(values)  # H=1+h has the same derivative.
    moments = dickman_moments(len(h)-2)
    return -sum(j*h[j]*theta**(j-1)*moments[j-1] for j in range(1, len(h)))/2


def _compositions(total, count):
    if count == 1:
        yield (total,)
        return
    for first in range(1, total-count+2):
        for rest in _compositions(total-first, count-1):
            yield (first,)+rest


def _shifted_simplex_monomial(powers, theta):
    k = len(powers)
    scale = 1-k*theta
    result = F(0)
    for selected in product(*(range(a+1) for a in powers)):
        selected_sum = sum(selected)
        coefficient = prod(comb(a, b)*factorial(b) for a, b in zip(powers, selected))
        result += (coefficient*theta**(sum(powers)-selected_sum)
                   *scale**(selected_sum+k-1)/factorial(selected_sum+k-1))
    return result


def formal_factor_integrals(coefficients: tuple, theta: F) -> tuple[tuple[int, F], ...]:
    """Compute each odd factor integral by finite differences and shifted simplices.

    This route is independent of the Dickman moments. Degree<=12 is a
    computational cap for composition enumeration, not a theorem boundary.
    Coefficients have the existing normalized exact int/Fraction meaning.
    """
    values = _inputs(coefficients, theta, max_degree=12)
    degree = len(values)-1
    results = [(1, F(1))]
    for k in range(3, degree+1, 2):
        value = F(0)
        for j in range(k, degree+1):
            if values[j] == 0:
                continue
            for composition in _compositions(j, k):
                multiplier = F(factorial(j), factorial(k)*prod(factorial(a) for a in composition))
                value += (values[j]*multiplier
                          *_shifted_simplex_monomial(tuple(a-1 for a in composition), theta))
        results.append((k, value))
    return tuple(results)


def accessible_main_enclosure(coefficients: tuple, theta: F, endpoint: F) -> tuple[F, F]:
    """Enclose the explicit Dickman F_f, retaining actual sieve errors separately.

    Requires m=floor(endpoint/theta)>=max(2,2*deg(h')) and m<=10000.
    This returns no interval for the actual prime sum and no numerical onset.
    """
    values = _inputs(coefficients, theta)
    if type(endpoint) is not F or not 0 < endpoint <= F(1, 2) or theta == 0:
        raise ValueError("require exact 0<endpoint<=1/2 and theta>0")
    h = list(semiprime_kernel(values))
    h[0] -= 1
    m = endpoint//theta
    if not max(2, 2*(len(h)-2)) <= m <= 10000:
        raise ValueError("require max(2,2*deg(h'))<=floor(endpoint/theta)<=10000")
    center = formal_dickman_main(values, theta)
    endpoint_value = sum(c*endpoint**j for j, c in enumerate(h))
    tail = sum(abs(j*h[j])*theta**(j-1)*(m+1)**(j-1) for j in range(1, len(h)))
    radius = (abs(endpoint_value)/theta+3*tail)/(2*factorial(m))
    return center-radius, center+radius

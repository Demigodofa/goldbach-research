"""Parseval pays every Mobius covariance dyadic block up to N^(1499/2000).

Owner: Kevin's Goldbach research.  Purpose: prune the dyadic endpoint
reduction before seeking new arithmetic cancellation.  This is an
unconditional absolute estimate for short and medium blocks, not an estimate
for the surviving long blocks or the signed Goldbach correlation.

FIX ONE BLOCK.
Keep the full setup

 H=N^(1/10), B=2N^(9/1000), M=N^(59/100),
 1<=d<=B, M<m<=2M prime, q=dm,                         (1)

and one aligned dyadic block Q=(L,L+Y].  Collapse the exact tail to

 c(n)=1_Q(n)1_((n,q)=1)sum_(a|n,a>N^(3/20))mu(a)log(n/a). (2)

Pointwise, |c(n)|<=tau(n)log N=N^(o(1)), uniformly on n comparable with N,
so

                         sum_n|c(n)|^2<=Y*N^(o(1)).       (3)

For active h the exact algebraic kernel is

 K_h(n)=e_q(-hn)+(m-1)^(-1)e_d(-h*mbar*n).               (4)

Extend (4) to every h modulo q only as a nonnegative Parseval majorant of the
active set; at h divisible by m it need not equal the true high projector.

PARSEVAL AND COLLISIONS.
For the q-transform, each residue contains at most ceil(Y/q) integers of Q.
For the d-transform it contains at most ceil(Y/d).  Parseval and Cauchy in
each residue give

 sum_(h mod q)|sum_n c(n)e_q(-hn)|^2
       <=q*ceil(Y/q)*sum|c(n)|^2,                         (5)

 sum_(h mod q)|(m-1)^(-1)sum_n c(n)e_d(-h*mbar*n)|^2
       <=q/(m-1)^2*ceil(Y/d)*sum|c(n)|^2.                (6)

Since m is a large odd prime, each right coefficient is at most Y+q.
Using |A+C|^2<=2|A|^2+2|C|^2 yields

 sum_(h in B_q)|T_mu(d,m,h;Q)|^2
                    <=4*(Y+q)*Y*N^(o(1)).                (7)

SUM THE EXACT OUTER FAMILY.
Insert mu(d)^2(log m)^2/q.  The q term in (7) contributes one Y per
(d,m), while the Y term contributes Y^2/q.  Standard harmonic and prime-count
upper bounds therefore give

 E_Y <=N^(o(1))*(B*M*Y+Y^2).                             (8)

If Y=N^y, the two exponents are

 family term:    y+9/1000+59/100 = y+599/1000,
 collision term: 2y.                                    (9)

The application benchmark is 1499/1000.  Both terms fit whenever

 y<=1499/2000=.7495.                                     (10)

At the endpoint, the collision term reaches the benchmark while the family
term is only 2697/2000=1.3485, leaving margin 301/2000=.1505.  Thus every
dyadic selector with Y<=N^(1499/2000) is already affordable, uniformly in its
modulus-dependent location, with all coprimality masks and the low kernel
retained.  The O(log^2 N) endpoint-recombination loss is absorbed in o(1).

DISPOSITION.
Only dyadic lengths N^(1499/2000)<Y<=3N/4 remain.  Equation (8) has no H gain;
above the threshold its Y^2 collision term exceeds the target.  A new
arithmetic estimate is required only for these long blocks.  This pruning
does not prove that the long-block energy is large or that polynomial tools
cannot help when paired with additional arithmetic cancellation.
"""

import cmath
from fractions import Fraction as F
from math import gcd, pi


def dyadic_scale_budget():
    """Return the exact exponent threshold and margins in (9)--(10)."""
    b, m = F(9, 1000), F(59, 100)
    target = F(1499, 1000)
    threshold = target / 2
    return {
        "divisor_family": b + m,
        "target": target,
        "paid_length_threshold": threshold,
        "collision_at_threshold": 2 * threshold,
        "family_at_threshold": threshold + b + m,
        "family_margin_at_threshold": target - (threshold + b + m),
        "long_blocks_require_arithmetic_input": True,
        "short_blocks_paid_uniformly_in_location": True,
    }


def finite_parseval_collision_receipt(d, prime_modulus, left, right,
                                       coefficients):
    """Numerically check (5)--(7) for exact-support finite coefficients."""
    if (type(d) is not int or type(prime_modulus) is not int
            or type(left) is not int or type(right) is not int
            or d < 1 or prime_modulus < 3 or left < 0 or left >= right
            or gcd(d, prime_modulus) != 1):
        raise ValueError("require positive coprime d,m and 0<=left<right")
    q, length = d * prime_modulus, right - left
    values = dict(coefficients)
    if any(type(n) is not int or not left < n <= right or gcd(n, q) != 1
           for n in values):
        raise ValueError("coefficients must lie in the block and be q-units")
    inverse_m = 0 if d == 1 else pow(prime_modulus, -1, d)

    additive_energy = low_energy = combined_energy = 0.0
    for h in range(q):
        additive = sum(value * cmath.exp(-2j * pi * h * n / q)
                       for n, value in values.items())
        low = sum(value * cmath.exp(
            -2j * pi * h * inverse_m * n / d if d > 1 else 0j
        ) for n, value in values.items()) / (prime_modulus - 1)
        additive_energy += abs(additive) ** 2
        low_energy += abs(low) ** 2
        combined_energy += abs(additive + low) ** 2
    square_mass = sum(abs(value) ** 2 for value in values.values())
    bound = 4 * (length + q) * square_mass
    return {
        "modulus": q,
        "length": length,
        "square_mass": square_mass,
        "additive_energy": additive_energy,
        "low_energy": low_energy,
        "continued_kernel_energy": combined_energy,
        "parseval_collision_bound": bound,
        "bound_holds": combined_energy <= bound + 1e-9,
    }

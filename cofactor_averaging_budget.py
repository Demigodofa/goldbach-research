"""A failed quantitative test of generic trilinear cofactor averaging.

Owner: Kevin's Goldbach research. Purpose: prevent an unsupported use of a
published Kloosterman bound in the still-open cofactor range. This is an
EXACT ERROR-BUDGET calculation, not a lower bound for a sum or a new prime
correlation estimate. It preserves cofactor averaging as an open approach.

Question tested:
Can Bettin--Chandee's trilinear estimate replace absolute summation over
the remaining M and give a power saving relative to Y*t? The hypothesis
predicts an exponent strictly below1 on EVERY required dyadic box. A box
whose substituted upper estimate exceeds Y falsifies that proposed uniform
deduction, not the possibility that the ACTUAL sum is much smaller.

Primary source: Bettin--Chandee, Trilinear forms with Kloosterman fractions,
Theorem1, equation(1.2), printed p2, arXiv:1502.00769v1:
https://arxiv.org/pdf/1502.00769v1 . Checked2026-09-09.
The source bounds a sum with separate coefficients alpha_r, beta_c, nu_k
and phase e(vartheta*k*inverse(r)/c), subject to gcd(r,c)=1, by their
three L2 norms times
  (1+abs(vartheta)*K/(R*C))^(1/2)
   *[(K*R*C)^(7/20+epsilon)*(R+C)^(1/4)
     +(K*R*C)^(3/8+epsilon)*(K*R+K*C)^(1/8)].           (1)
Both terms in the bracket must be budgeted; one cannot choose the smaller.

Actual affine geometry, from rare_affine_small_cofactor.py:
Let M~B=Y^b, q=a*l with a~A=Y^x<=sqrt(Y/M), and p=c*d with
c~C=Y^y<=sqrt(Y). Then Q=Y/B. Group r=M*a, of size R=B*A, so
  r_exp=b+x, c_exp=y, k_exp=b+x+y-1.                    (2)
The last exponent is the ideal Poisson frequency length K=R*C/Y. The
d1=d2=e=1 sieve-index term already has this budget. Conductor D=Y^o(1),
logarithms and arbitrarily small epsilon losses cannot repair a fixed
positive excess in the exponent; those costs are omitted here. A fixed negative k_exp has no
nonzero frequencies eventually after those losses are chosen small enough.
The test treats the boxes k_exp>=0, including the critical boundary.

After shared-factor removal, gcd(M*a,c)=1 holds. The convolution coefficient
alpha_r has at most tau(r) representations r=M*a, so the generic available
norm budgets are
  ||alpha||2 <= R^(1/2)*Y^o(1), ||beta||2<=C^(1/2)*Y^o(1),
  ||nu||2 <= K^(1/2)*Y^o(1).                            (3)
These are UPPER bounds being substituted, not assertions of norm saturation.
The Poisson prefactor is Q/(A*C)=Y/(R*C), not1 and not1/B. Also
vartheta is the TARGET m~Y, so vartheta*K/(R*C) has exponent0. Inserting
an additional power B into that phase factor would be incorrect.

There is a separate source-application gap: actual smooth weights and
frequency cutoffs couple M,a,c,k and may retain M after r=M*a. Theorem1
does not directly apply to arbitrary such weights. A separable decomposition
would need proof. For this NECESSARY STRENGTH TEST we grant one for free;
failure even under that optimistic assumption is enough to reject the
proposed unchanged plug-in. It is not a bound on the actual coupled sum.

Write r=b+x, s=y, k=r+s-1. Combining(1)-(3) and the prefactor gives
  E1=1-3*(r+s)/20+17*k/20+max(r,s)/4,
  E2=1-(r+s)/8+k+max(r,s)/8.                            (4)
Because k=r+s-1, these equal
  E1=3/20+7*(r+s)/10+max(r,s)/4,
  E2=7*(r+s)/8+max(r,s)/8.
They are increasing in r,s. Hence for each b>=0 their largest values on
0<=x<=(1-b)/2, 0<=y<=1/2, k>=0 occur at the REAL admissible corner
  x=(1-b)/2, y=1/2, r=(1+b)/2, k=b/2,
and are exactly
  E1_max=39/40+19*b/40, E2_max=15/16+b/2.               (5)
At b=1/5 they are107/100 and83/80; at b=13/25 they are611/500
and479/400. Both exceed1 throughout the remaining interval [1/5,13/25].
The first could be below1 only for b<1/19, and the second only for b<1/8.
The sum of the two source terms is therefore not a power-saving certificate
even through the already-completed small-cofactor range.

In the actual-zero large-V regime, t=Y^-o(1), so any fixed positive excess
in(5) matters: logarithmic or any fixed rarity-factor gain is not enough
to repair that power budget. This does NOT claim the true error exceeds Y.
Fixing k, using the source with numerator length1, and then summing the K
frequencies worsens E1 by3*k/20 and leaves E2 unchanged. Swapping r,c by
reciprocity leaves(4) invariant (even granting a free smooth phase adjustment).
Neither is a materially different successful application of(1).

Reassessment:
The generic L2 trilinear plug-in FAILED its concrete test. Do not retry it
with the same norms, phase and box geometry under a new label. Preserve
the exact grouping/prefactor and the restricted affine theorem. A useful
next hypothesis must exploit structure that this generic norm reduction
discards, obtain a stronger estimate at these boxes, or change the prime-
pair mechanism. No impossibility theorem for arithmetic coefficients, other
averaging methods, polynomial tools, or Goldbach follows. No new coverage.

The routines are exact rational bookkeeping for future source comparisons;
their finite tests do not validate a theorem's application to coupled weights.
"""
from dataclasses import dataclass
from fractions import Fraction as F


def _exact(value, name):
    if type(value) not in (int, F):
        raise ValueError(f"{name} must be an exact rational")
    return F(value)


@dataclass(frozen=True)
class TrilinearBudget:
    inverse_variable: F
    denominator: F
    frequency: F
    prefactor: F
    norm_product: F
    phase_factor: F
    first: F
    second: F
    fixed_frequency_first: F


def bc_budget(cofactor_exponent, first_divisor_exponent, second_divisor_exponent):
    """Substitute one admissible current-task box into the optimistic budget."""
    b = _exact(cofactor_exponent, "cofactor_exponent")
    x = _exact(first_divisor_exponent, "first_divisor_exponent")
    y = _exact(second_divisor_exponent, "second_divisor_exponent")
    if not 0 <= b <= F(13, 25):
        raise ValueError("cofactor exponent must be in[0,13/25]")
    if not 0 <= x <= (1-b)/2 or not 0 <= y <= F(1, 2):
        raise ValueError("divisor box exceeds the smooth hyperbola support")
    r, s, k = b+x, y, b+x+y-1
    if k < 0:
        raise ValueError("this box has a negative ideal frequency exponent")
    prefactor = 1-r-s
    norms = (r+s+k)/2
    phase = max(F(0), 1+k-r-s)/2
    first = prefactor+norms+phase+F(7, 20)*(k+r+s)+max(r, s)/4
    second = prefactor+norms+phase+F(3, 8)*(k+r+s)+max(k+r, k+s)/8
    return TrilinearBudget(r, s, k, prefactor, norms, phase, first, second,
                           first+F(3, 20)*k)


def worst_bc_budget(cofactor_exponent):
    """The proved monotone worst corner, not a numerical optimizer."""
    b = _exact(cofactor_exponent, "cofactor_exponent")
    return bc_budget(b, (1-b)/2, F(1, 2))

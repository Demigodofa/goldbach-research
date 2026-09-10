"""Source gate for large-sieve control of the Mobius-band covariance.

Owner: Kevin's Goldbach research.  Purpose: test whether an existing classical
or asymptotic multiplicative large sieve proves equation (10) of
``mobius_band_character_covariance.py``.  It does not; the exponent ranges are
promising, but the sourced forms and the required signed covariance differ.

PRIMARY SOURCE CHECKED 2026-09-10.
J. B. Conrey, H. Iwaniec and K. Soundararajan, *Asymptotic Large Sieve*,
arXiv:1105.1176v1:
https://arxiv.org/pdf/1105.1176v1 .

The displayed classical multiplicative large sieve, equation (1.4), is

 sum_(q<=Q) q/phi(q) sum*_(chi mod q)
   |sum_(n<=X)a_n chi(n)|^2 <= (Q^2+X)sum|a_n|^2.           (1)

The source explicitly notes after its additive dual (1.11) that duality loses
access to special coefficient structure.  Its bilinear consequence (1.9),
for a smooth separated F and coefficient lengths A,B, has cost

 L(A,B)*(Q^2+A)^(1/2)*(Q^2+B)^(1/2)*||alpha||_2||beta||_2. (2)

At Q=M=N^(59/100), Q^2=N^(59/50)>N dominates every factor length in our
product.  Equations (1)--(2) therefore retain the full Q^2 family cost.  More
decisively, they are positive norm inequalities: applying them separately to
W_m and C_m cannot determine the sign of sum W_m(eta)C_m(eta).  They reproduce
the already known full-energy bound, not its H^-1 active-band fraction.

THE ASYMPTOTIC LARGE SIEVE IS CLOSE IN SCALE BUT NOT IN FORM.
The source's Theorem 2.2 gives a diagonal asymptotic for its form SS(A x B)
with arbitrary coefficients when each common sequence has length at most
Q^(1-epsilon).  Theorems 2.3--2.4 extend the common sequence support bound
to Q^(2-delta) for
specific L-function coefficients convolved with a SHORT mollifier of length
at most Q^(1-epsilon), under the stated nonsingularity/cancellation conditions.
The modulus is averaged with a smooth weight over ALL q comparable to Q and
all primitive characters; F is a common smooth two-variable box weight.

Our scales do pass the superficial exponent checks:

 N=Q^(100/59),          100/59=1.6949...<2,
 N^(1/2)=Q^(50/59),      50/59=.8474...<1,
 V=N^(3/20)=Q^(15/59),   15/59=.2542...<1,
 R=M/H=Q^(49/59),        49/59=.8305...<1.                (3)

But equation (10) in the current problem is not SS(A x B).  It contains

 * only prime moduli m in (M,2M], with an additional d-component later;
 * a shrinking, modulus-dependent numerator set I_m of length m/H;
 * two linked character indices through C_m(eta)=sum_chi
       c_(eta*chi)conj(c_chi), multiplied by W_m(eta);
 * the q-dependent normalized Gauss phase inside c_chi;
 * the LONG complementary tail mu_(>V), whereas the source's favorable
   hypothesis uses a short supported mollifier; and
 * hard hyperbolic product endpoints before any smoothing transfer.

None of Theorems 2.2--2.5 states a diagonal asymptotic after imposing these
restrictions.  Positivity does not allow enlarging the signed OFF covariance
from prime to all moduli, and replacing the shrinking numerator set by all
nonzero residues deletes precisely the question being tested.  The source is
therefore not a licensed proof of the H^-1 estimate.

WHAT THE SOURCE CHANGES.
The paper's direct-bilinear strategy is a relevant component: it preserves
special Mobius structure specifically because ordinary duality discards it,
and its Q^(2-delta) reach contains our total length.  A valid adaptation would
need a LOCAL asymptotic large sieve whose test function also depends on h/m,
and which admits the actual prime-modulus weight and Gauss-phased four-transform
covariance.  A first sufficient intermediate theorem would be equation (10)
for smooth separated d=1 boxes and a smooth prime-m weight.  Hard endpoints and
d>1 would still require separate transfers.

FINITE SIGN DIAGNOSTIC, NOT SOURCE EVIDENCE.
For the exact U=1 tail at N=200000, all 171 prime m in the finite block gave
signed OFF/DIAG=-0.041560.  Eight deterministic coefficient shuffles had mean
-0.000202 and standard deviation 0.008892; eight independent random-sign
controls had mean 0.002523 and standard deviation 0.009538.  At N=1200000 a
120-prime sample again gave -0.041708.  This makes simple reinforcement less
plausible and motivates retaining the covariance sign, but the tiny V=6,8,
the few controls and floating FFTs cannot establish persistence or novelty.

DISPOSITION.
The standard/hybrid large sieve as a black box is rejected for this target.
The asymptotic large-sieve architecture remains a promising component, not an
applicable theorem.  The signed prime-modulus local covariance remains OPEN.
"""

from fractions import Fraction as F


def covariance_source_scale_receipt():
    """Exact N- and Q-exponents in (3), plus the source applicability gates."""
    q = F(59, 100)
    product = F(1)
    factor = F(1, 2)
    cutoff = F(3, 20)
    active = q - F(1, 10)
    return {
        "Q_in_N": q,
        "classical_Q_squared_in_N": 2 * q,
        "product_in_Q": product / q,
        "balanced_factor_in_Q": factor / q,
        "mobius_cutoff_in_Q": cutoff / q,
        "active_band_length_in_Q": active / q,
        "product_below_Q_squared_margin_in_N": 2 * q - product,
        "balanced_factor_below_Q_margin_in_N": q - factor,
        "standard_large_sieve_controls_signed_covariance": False,
        "asymptotic_large_sieve_theorem_directly_applies": False,
        "local_prime_modulus_adaptation_proved": False,
    }

"""Retain a common signed polynomial condition on actual band survivors.

Owner: Kevin's Goldbach research. Purpose: keep the arithmetic phase
information in zero detection after the reviewed length filter, and state
exactly what a geometric inversion pays. This is a proof component for
the next paired estimate, not a solution of that estimate or Goldbach.

1. REMOVE ALL TYPE II ZEROS, INCLUDING THE OVERLAPPING ONES.
Keep target N, T=N^(9/10), L=logN, a=16/25, b=19/25, and the
fixed real smooth chi supported in(1,2). All zeros below are ACTUAL
positive-height zeta-zero copies, counted with multiplicity. Retain the
exact detector D_M and contour I_T from zero_detector_band_reduction.py:
 B=2*T^(1/100), Y=sqrtT,
 a_T(n)=sum_(d|n,d<=B)mu(d),
 D_M(s)=sum_(M<n<=2M)a_T(n)*exp(-n/Y)*n^(-s),
 I_T(rho)=(1/(2pi*i))*int_(Re z=1/2-beta)
                  Y^z*Gamma(z)*M_T(rho+z)*zeta(rho+z)dz.       (1)
Allowed M are dyadic, T^(1/100)<=M<=sqrtT*(logT)^2.

Let II be ALL middle-strip zeros a<beta<b with |I_T(rho)|>=1/3.
They may also be Type I. The previously proved restricted count
R_II(s,T)<<T^(2*(1-s))*(logT)^C holds for every s in[a,b]
and counted all such Type II zeros, not just the non-Type-I ones.
Thus its SAME positive layer cake, including the boundary at a, gives
 E_II=sum_(rho in II)|chi(gamma/T)|^2*N^(2beta-2)
                                      <<N^(-6/125)*L^C.       (2)
The corrected NEGATIVE real part of Gamma on this contour remains
essential. The source's printed sign error is not reinstated here.

Let D={beta<=a or beta>=b}, and let G be the middle-strip zeros
detected at ANY good M, where good means
 N^(41/50)<=M^k<=N^(49/50) for some integer1<=k<=100.
Set W=D union II union G, and R=the complement in the full band.
II and G may overlap. NONNEGATIVITY, not a disjointness assertion, gives
 E_W<=E_D+E_II+E_G.                                          (3)
The retained estimates make E_W all-log small. Apply the masked Gram
bound to W, using the arithmetic O(1) norm ONLY for the full unmasked
field Z. The row, column and intersection costs are sqrt(L E_W),
sqrt(L E_W), and L E_W. The exact beta transfer and previously paid
absolute errors therefore give, for every fixed A>0,
 sum_(rho,sigma)chi*chi*J_N(rho,sigma)
 =sum_(rho,sigma in R)chi*chi*J_N(rho,sigma)+O_A(N/L^A).        (4)
The inherited errors N^(9/10)L^12 and N^(-7/10)L^13 are included.
For II alone the union exponent remains122/125; for G,623/625.
No arbitrary masked field is assigned the full arithmetic norm.

2. ONE COMMON BAD-LENGTH POLYNOMIAL, WITH A FIXED DISK CONSTRAINT.
Define, independently of rho,
 H_N(s)=sum_(allowed M which are NOT good)D_M(s).               (5)
This is a single Dirichlet polynomial, not a zero-dependent selection.
The prior integer-power coverage proves that, for sufficiently large N,
all its lengths have logM/logN in the four OPEN gaps
 (49/300,41/250), (49/250,41/200),
 (49/200,41/150), (49/150,41/100).                             (6)
In particular its support has n<=2*N^(41/100). The dyadic blocks
are disjoint as sets of integers even if their endpoints coincide.

The actual smoothed zero equation in Appendix C of the pinned primary
source Maynard--Pratt2206.11729v2, pp36-37, is
 1+sum_(all allowed M)D_M(rho)=I_T(rho)+O(T^(-1/2)),            (7)
uniformly for our beta interval and T<=gamma<=2T. The source and
its proof/correction are recorded in zero_detector_band_reduction.py:
 https://arxiv.org/pdf/2206.11729v2
Checked again2026-09-10. No Hypothesis F or fixed vertical lines enter.
To reconcile strict source dyadic endpoints with our inclusive list:
if M=T^(1/100) exactly, its block ends at B=2*T^(1/100), where
a_T(n)=0 throughout. If M=Y*(logT)^2 exactly, adding its block
changes only the exponentially small smoothed tail. The first nonzero
coefficient is exp(-1/Y)=1+O(T^-1/2), as already paid in(7).

The number q_T of allowed dyadic lengths satisfies
 q_T<=( (49/100)*logT+2*loglogT )/log2+1<logT                 (8)
eventually, since (49/100)/log2<1. The additive1 pays both
endpoints; no integer rounding or finite onset is suppressed.
For rho in R, |I_T(rho)|<1/3 and EVERY good D_M is strictly
below1/(3logT). Hence(7) gives
 |1+H_N(rho)|<=1/3+q_good/(3logT)+O(T^-1/2)
                       <=2/3+o(1)<=3/4                       (9)
for all sufficiently large N, uniformly over these actual zero copies.
The unknown error constant prevents a numerical onset claim.
Consequently every survivor satisfies
 Re H_N(rho)<=-1/4,  1/4<=|H_N(rho)|<=7/4,
 |1/H_N(rho)|<=4.                                            (10)
The common disk centered at -1 contains strictly more information than
the earlier detector magnitude threshold or a least-length assignment.
The Type-I/II dichotomy also implies that every survivor has a detecting
length; (9) itself already guarantees a nonzero common H_N value.

3. A BOUNDED RECIPROCAL IS NOT YET A SHORT ARITHMETIC INVERSION.
For e=1+H_N(rho), |e|<=3/4. For every integer J>=1 the exact
geometric identity is
 1=-H_N(rho)*sum_(j=0)^(J-1)e^j+e^J.                         (11)
Thus -sum_(j=0)^(J-1)e^j approximates 1/H_N(rho) with error
at most4*(3/4)^J. The minus sign is necessary. There is no
assertion that multiplying a zero field by this polynomial preserves
its arithmetic energy or produces cancellation in its reflected pair.

Here is the actual coefficient cost of the remainder in(11). Write
 c_rho=chi(gamma/T)*N^(beta-1)*exp(i*gamma*logN),
 Z_err(x)=sum_(rho in R)c_rho*e_rho^J*x^(beta-1/2+i*gamma).
The crude actual zero count O(TL) and beta<b give
 E_R=sum_(rho in R)|c_rho|^2<<N^(21/50)*L.
The Gram estimate for arbitrary coefficients on these actual copies
then proves, on the fixed central interval with smooth cutoff theta,
 ||theta*Z_err||_2<<(3/4)^J*N^(21/100)*L.                     (12)
To make this displayed bound O(N^-sigma), for a fixed sigma>0,
it suffices that
 J>=((21/100+sigma)*logN+2*loglogN)/log(4/3).                  (13)
This is a SUFFICIENT choice from this crude energy estimate, not a
necessary degree lower bound or proof that smaller J fails.

The explicitly truncated polynomial -H_N*sum_(j<J)(1+H_N)^j
has support no longer than (2*N^(41/100))^J. For the choice(13)
this support majorant is exp(O((logN)^2)). That is only an UPPER
bound on the straightforward expansion, not a proved minimal length.
Possible coefficient cancellations, factorizations, arithmetic resummation
or better residual estimates are not ruled out. The previous fixed-power
moment theorem with k<=100 does not by itself control this changing-degree
expansion, its coefficient constants, or its support majorant.

4. WHAT REMAINS OPEN.
Equation(9) is an actual common arithmetic phase constraint and(4) is
an actual negligible deletion. Neither supplies the sign of J_N or a
bound improving O(N) for the surviving pair sum. In particular the
two linked prime conditions and the full signed Goldbach margin remain
open. The disk and reciprocal can be paired with a new arithmetic
ingredient; the polynomial/phase tools have not been discarded.
No numerical zeros, finite Goldbach experiment, general impossibility
claim or external novelty claim is used. This result is new-to-this-task.
"""
from fractions import Fraction as F


def disk_consequences(radius):
    """Exact geometric budgets; these do not evaluate an actual zero."""
    if type(radius) is not F or not 0 <= radius < 1:
        raise ValueError('exact radius in[0,1) required')
    return {'real_upper': -1+radius, 'modulus_lower': 1-radius,
            'modulus_upper': 1+radius, 'reciprocal_upper': 1/(1-radius)}


def finite_inverse(value, degree):
    """Geometric reciprocal approximant; caller owns its disk hypothesis."""
    if type(degree) is not int or degree < 1:
        raise ValueError('positive integer degree required')
    return -sum((1+value)**j for j in range(degree))


def crude_residual_exponents():
    energy=F(9,10)+2*F(19,25)-2
    return {'energy': energy, 'norm': energy/2}


def union_energy_bound(energies, masks):
    """Finite positive-energy guard, including overlapping copy masks.

    Keys identify separate copies, never merely coincident zero locations.
    Supplied nonnegative values are abstract fixtures, not computed zeros.
    """
    if any(type(v) is not F or v < 0 for v in energies.values()):
        raise ValueError('nonnegative exact copy energies required')
    union=set().union(*masks)
    actual=sum((energies[key] for key in union),F(0))
    majorant=sum((energies[key] for mask in masks for key in mask),F(0))
    return actual,majorant

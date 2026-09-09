"""A count-compatible spectral model with actual finite-period reinforcement.

Owner: Kevin's Goldbach research. Purpose: test whether the single-zero
counting/density inputs used so far suffice for the remaining comparable
linear-height phase. This is an ARTIFICIAL, N-DEPENDENT model. It is not
the zeta-zero set, a Goldbach counterexample, or an all-method barrier.
Preserve the successful phase bounds and the earlier polynomial tools.

1. PRECISE MODEL CONCLUSION AND ITS LIMIT.
Fix c=1/100 and a nonzero real smooth chi supported compactly in(c,2c).
For every sufficiently large N we construct a global positive-height
sequence Gamma_N. Its counting function agrees with the smooth
Riemann-von Mangoldt main M(T) to O(1), uniformly in N and T. Every
mock location is rho=1/2+i*gamma; add conjugate locations if desired.
They are simple and have the usual reflection/conjugation symmetry of
LOCATIONS. Critical-line placement satisfies all the single-zero density
envelopes used here, and local occupancy is O(log(2T)). No Euler product,
prime explicit formula or zeta functional-equation identity is imposed.

Evaluate the SAME analytic finite-period kernel, now at these mock points:
 J_N(rho,sigma)=(e/pi)Gamma(rho)Gamma(sigma)
             *int_0^pi exp(iNt)(1/N+it)^(-rho-sigma)dt.
With ell=log(N/2), the resulting finite weighted sum satisfies
 sum_(gamma,eta in Gamma_N) chi(gamma/N)chi(eta/N)J_N
   =-C_chi N ell^2+O_chi(N(logN)^(3/2)+sqrtN(logN)^2),
 C_chi=(1/pi)int chi(s)^2 ds>0.                                     (1)
In particular its REAL part is at most -c_chi Nlog^2N for large N.
Thus the listed counting, density, symmetry and occupancy conditions
alone cannot give a uniform all-log bound or an O(N) lower bound for
THIS smooth comparable-height band across admissible configurations.

The spectrum depends on N. We do not construct one fixed spectrum with
this behavior for infinitely many N. Nor does a negative weighted band
alone determine the whole unweighted correlation: other regions might
compensate. This is a limitation of the specified inputs and conclusion,
not a failure of Goldbach or a prohibition on combining these tools with
additional arithmetic information. The actual signed margin stays OPEN.

2. A FINER ACTUAL KERNEL EXPANSION, WITH THE ENDPOINT KEPT.
On cN<gamma,eta<2cN with beta=beta'=1/2, put h=gamma+eta,q=h/N.
The stationary main from the preceding modules is
 A=2sqrt(2pi)/sqrt h,
 Theta=gamma log(Ngamma/h)+eta log(Neta/h)-pi/4.
We now prove the UNIFORM expansion
 J_N=A exp(iTheta)
     +N^-1 b(q)exp{i[phi(gamma)+phi(eta)+N*pi]}+O_c(N^-3/2),          (2)
 b(q)=-2e exp(-q/pi)/(pi-q), phi(t)=tlog(t/pi)-t.
The earlier coarse O(N^-1) pairwise remainder is insufficient for (1),
since there are O(N^2 log^2N) pairs. The explicit endpoint in (2) must
also be summed, rather than discarded because it is smaller per pair.

Here is a proof of (2). Write a=1/N and f_q(t)=t-qlogt. Uniform complex
Stirling, with relative error O(N^-1), leaves the integral
 2e exp{i[gamma loggamma-gamma+eta logeta-eta]}
    *int_0^pi B_a(q,t)exp(iN f_q(t))dt,
 B_a=(a+it)^-1 exp[-(q/a)arctan(a/t)]
                    *exp[-i(q/(2a))log(1+a^2/t^2)].                 (3)
This is the exact integrand factorization before the stated Gamma error.
At t=0 use the original integrand, not the singular extracted phase.

The part t<=a^(1/4) is exponentially small in a^-1/4: for t>=a,
arctan(a/t)>=a/(2t), and for t<=a the damping is exp(-c'/a).
Polynomial factors from (a+it)^-1 are absorbed. Insert a smooth lower
cutoff transitioning at this small scale. On its complement, Taylor
expansion and exp(-q/(2t)) absorb every inverse power of t, giving
 B_a=-i t^-1 exp(-q/t)+O_(C^r)(a)                                   (4)
for each fixed r, after extending the cut amplitude by0 at t=0. The
cutoff transition and the corresponding flat limiting amplitude have
exponentially small C^r costs. This does NOT assert that the uncut B_a
itself has bounded derivatives at0.

The phase f_q has one nondegenerate stationary point t=q, with
f_q''(q)=1/q. Since q is in the fixed compact interval[2c,4c], choose
a fixed smooth central cutoff inside(0,pi), equal1 near this whole
stationary range. Its Morse coordinate and all required derivatives are
uniform. In that coordinate write the compact amplitude as
B(0)chi_0(w)+B'(0)w chi_0(w)+w^2 R(w), with chi_0 even and equal1
near0. The odd term integrates to0. The constant gives its Fresnel
main; the cutoff Fresnel tails are O(N^-K) for any fixed K by repeated
nonstationary integration. For the remainder, one integration by parts
turns w^2R into -(R+wR')/(iN); the second-derivative bound for this
smooth compact integral is O(N^-1/2). Thus the central error is
O(N^-3/2). The C^r error in (4) contributes the same order. Restoring
the phase and amplitude gives exactly A exp(iTheta).

Outside the central cutoff, f_q' is uniformly separated from0 wherever
the cut amplitude is supported. Two integrations by parts produce the
upper endpoint B_a(q,pi)exp(iN f_q(pi))/(iN f_q'(pi)), with
O(N^-2) remainder and no lower boundary. Using (4) at pi gives
 b(q)=2e[-i pi^-1 exp(-q/pi)]/[i(1-q/pi)]
     =-2e exp(-q/pi)/(pi-q).
The Gamma error multiplies a total integral O(N^-1/2), so costs
O(N^-3/2). This proves (2), including every finite-period contribution.

3. A QUARTER-SHIFTED LATTICE MAKES THE STATIONARY MAIN NEGATIVE.
Let d=2pi/ell and take full grid points x_k=d(k+1/4). Only positive
points in the support of chi are used. Write
 D(gamma,eta)=gamma log(2gamma/h)+eta log(2eta/h).
Then Theta=h*ell+D-pi/4, and on every grid pair
 exp(i h ell)=exp[2pi i(k+j+1/2)]=-1.                               (5)
Consequently the full-grid stationary sum is the negative of the grid
sum of chi(gamma/N)chi(eta/N)A exp(iD-i*pi/4).

Apply two-dimensional Poisson summation. The physical first derivatives
of D are log(2gamma/h),log(2eta/h), uniformly bounded on the support,
whereas nonzero dual frequencies are integer multiples of ell. After
rescaling gamma=Nx,eta=Ny, integrate the FULL phase in a coordinate
with nonzero dual index. Repeating sufficiently often gives summable
decay in every nonzero index and a negligible total. For two nonzero
indices, integrate in both coordinates; for one, only that coordinate
is needed. Do not treat exp(iD) as a slowly varying amplitude.

The zero-frequency continuous integral has a stationary diagonal. Put
h=gamma+eta and v=gamma-eta; the Jacobian is1/2, and
 D=(h/2)[(1+v/h)log(1+v/h)+(1-v/h)log(1-v/h)],
 D_vv(h,0)=1/h.
Uniform transverse stationary phase gives sqrt(2pi h)exp(i*pi/4),
canceling the -pi/4 in (5). Its product with A and the Jacobian is2pi.
The remaining integral is therefore
 2pi int chi(h/(2N))^2 dh+O(1)=4pi N int chi(s)^2 ds+O(1).            (6)
The error follows from the same next-order Morse bound; the fixed smooth
support makes it uniform in h. This is an ASYMPTOTIC, not an exact
evaluation. Multiplying by the grid density d^-2 and restoring (5),
the full-grid stationary sum is
 -(N ell^2/pi)int chi^2+O_chi(ell^2).                                (7)

4. THE FULL-GRID ENDPOINT IS NONRESONANT; ITS TAIL IS PAID.
In the endpoint term of (2), Poisson aliases have frequencies m*ell.
The only potentially close one is m=1, but
 phi'(gamma)-ell=log(2gamma/(pi N))
is a fixed negative distance from0 on cN<gamma<2cN. Other integer
aliases are separated by growing multiples of ell, for large N. In
scaled coordinates, repeated nonstationary integrations in each
coordinate therefore give a negligible total for the full-grid endpoint
sum. The coupled smooth amplitude b((gamma+eta)/N) has uniformly
bounded derivatives on the fixed box; it introduces no coupled mask.
The prefactor N^-1 and the grid density d^-2 are included in this bound.
Finally the O(N^-3/2) pairwise remainder in (2), summed over the
O(N^2L^2) grid pairs, is O(sqrtN L^2). The ACTUAL full-grid J sum
thus has the same negative leading term as (7).

5. A GLOBAL PER-N COUNT-CONSTRAINED SPECTRUM BY ROUNDING.
The smooth Riemann-von Mangoldt main is
 M(t)=t/(2pi)[log(t/(2pi))-1]+7/8,
 M'(t)=log(t/(2pi))/(2pi).                                         (8)
It is strictly increasing above2pi. Begin with baseline heights
xi_j=M^-1(j), j=1,2,..., taking the inverse on this increasing branch.
Their count is max(0,floor M(t)) above2pi and differs from M(t) by
O(1) everywhere relevant. Put all these mock locations on beta=1/2.

For each xi_j in[cN/2,3cN], round it UP to the first grid point x_k
at or above xi_j; keep every other baseline height unchanged. The
displacement is less than d (zero at equality). Throughout this extended
band and neighboring cells, M'(t)d<1 for sufficiently large N, since
the grid density ell/(2pi) exceeds M'(t) by
 (1/(2pi))log(pi N/t),
a positive fixed quantity on that band. Thus each grid cell contains at
most one baseline point, preventing collisions, including at the boundary.
At any threshold t, only points originally in(t-d,t] can be moved past
it, and at most one is moved. The global count consequently changes by
at most1, so the new Gamma_N satisfies
 #{gamma in Gamma_N:gamma<=t}=M(t)+O(1)                              (9)
with an absolute constant independent of N. Endpoint full/half-count
conventions change this by at most one because these mock points are simple.

Inside the support of chi all new heights are on the grid, and a grid
point x_k is occupied precisely when
floor M(x_k)-floor M(x_(k-1))=1. The increments are0 or1. Telescoping
and (8) show that only O(N) of the O(NL) full-grid points in(cN,2cN]
are omitted: the difference of grid density and M' is uniformly O(1).
Equation (9) also gives local occupancy O(log(2t)), uniformly in N.
All points have beta=1/2, so the density counts above1/2 vanish and
the total-count endpoint has the required bound. Reflection and
conjugation symmetry of locations are immediate. These facts do not
make the spectrum the zeros of zeta or supply its arithmetic identities.

6. THINNING PRESERVES THE NEGATIVE ACTUAL KERNEL SUM.
The stationary discrete operator from discrete_spectral_cancellation.py
applies to arbitrary sequences in this fixed comparable band. Its
stationary T^-1/2 amplitude cancels its sqrtT norm, leaving O(L) times
the two coefficient l2 norms. The full grid has O(NL) nodes, whereas
the omitted set has O(N). With the fixed bounded chi weights, changing
one side therefore costs O(L sqrt(NL)sqrtN)=O(NL^(3/2)). Decompose
the full-full minus kept-kept sum into omitted-full plus kept-omitted
to pay both changes. Carrier phases do not alter these l2 norms.

For the endpoint, the crude uniform pairwise O(N^-1) bound suffices
for the DIFFERENCE: O(N) omitted nodes against O(NL) total nodes cost
O(NL). It would not suffice on the full grid. The uniform remainder
still costs O(sqrtN L^2). Combining with (7) proves (1).

The chosen band lies above the old low-axis and sub-five-sixths cutoffs
for large N, and its two scales are comparable, so the newly paid
strongly unequal tag family does not remove it. The very near-height
strip in this model has absolute size at most O(sqrtN W_N L^2), from
the same local counts and |J|=O(N^-1/2); this is o(N) for the retained
W_N=exp[O(sqrtL)]. Removing that strip therefore also leaves (1).
The original smooth height-sum weight is1. These observations locate
the model in the same troublesome geometry; they do not transfer it
to the actual zero set or determine the full unweighted signed sum.

7. SOURCE AND CLAIM BOUNDARIES.
The count law used for comparison was checked directly in Brent, Platt
and Trudgian, Accurate estimation of sums over zeros of the Riemann
zeta-function, Mathematics of Computation90(2021), printedp2926,
equations(5)-(7): N(T)=M(T)+Q(T), Q(T)<<logT. Their half-weight endpoint
convention is harmless for our O(1) model construction.
https://maths-people.anu.edu.au/brent/pd/rpb276-MC-preprint.pdf
The source's numerical zero results and RH-related remarks are not used.
All kernel, Gamma and discrete-transfer inputs otherwise come from the
reviewed predecessor modules; the2016 explicit-formula correction persists.
The reusable addition is the paid expansion (2), and the restricted
negative finding is the insufficiency statement after (1). No novelty,
actual prime/zero computation, coverage, or new global impossibility claim.
"""
from fractions import Fraction as F


def lattice_carrier_turns(k, j, shift=F(1,4)):
    if any(type(n) is not int for n in (k,j)) or type(shift) is not F:
        raise ValueError('integer indices and rational shift required')
    return k+j+2*shift


def transverse_curvature(height_sum, difference):
    if any(type(t) is not F for t in (height_sum,difference)) or height_sum<=abs(difference):
        raise ValueError('rational positive sum exceeding absolute difference required')
    return height_sum/(height_sum**2-difference**2)


def floor_increment_selection(profile):
    """Exact abstract rounding guard, not a numerical RVM/zero computation."""
    if any(type(t) is not F for t in profile):
        raise ValueError('rational monotone toy profile required')
    if any(not 0<=b-a<1 for a,b in zip(profile,profile[1:])):
        raise ValueError('profile increments must lie in[0,1)')
    floors=[t.numerator//t.denominator for t in profile]
    return [b-a for a,b in zip(floors,floors[1:])]


def thinning_error_powers(removed_n=F(1), removed_log=F(0)):
    if any(type(t) is not F or t<0 for t in (removed_n,removed_log)):
        raise ValueError('nonnegative rational cardinality powers required')
    return {'stationary_N':(removed_n+1)/2,
            'stationary_log':1+(removed_log+1)/2,
            'endpoint_N':removed_n, 'endpoint_log':removed_log+1}


def summed_pair_remainder_power(pair_power):
    if type(pair_power) is not F:
        raise ValueError('rational pairwise N power required')
    return 2+pair_power


def endpoint_alias_argument_upper(x):
    """Use pi>3 to bound 2x/pi; x is the normalized mock height."""
    if type(x) is not F or not F(1,100)<=x<=F(1,50):
        raise ValueError('rational normalized height in[1/100,1/50] required')
    return 2*x/3

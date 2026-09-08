# A subpower presieve eventually defeats the raw union certificate

Owner: Kevin's Goldbach investigation. Purpose: establish a proved scaling
constraint on the first stage, instead of treating a smaller prime cutoff
as a free simplification. Status: deduction from standard sieve theorems,
independently checked by Sol; new-to-this-task, with no worldwide novelty
claim. No Goldbach assumption is used.

## Statement and scope

For even N>=6 use the same square-start events E_r as `cubic_sieve.py`, but
allow an arbitrary first-stage cutoff z. Write A_z for the surviving ordered
odd candidates, M_z=|A_z|, and

    S1_z = sum_{odd prime z<r<=sqrt(N-3)} |E_r intersection A_z|,
    R_z = M_z-S1_z.

R_z is always a lower bound for the ordered Goldbach count. With a cutoff
below the cube root, residual triple and higher intersections can be
nonempty, so R_z+S2 must not automatically be called the exact count.

Let N tend to infinity through powers of2. If z=z(N)>=2 and

    log(z)/log(N) -> 0,

then R_z(N)<0 for all sufficiently large members of this sequence. In fact

    R_z/M_z <= -1+o(1).

The cutoff class includes fixed cutoffs, powers of log(N), and such larger
subpower examples as exp(sqrt(log(N))). It excludes N^(1/3). The conclusion
rules out these shallow first stages for this specific first-order lower
bound. It does not rule out retaining higher intersections, other bounds,
or Goldbach itself. No explicit onset or numerical threshold is claimed.

## Combinatorial part

Let Q_z count members of A_z whose leading argument is prime, and let nu(a)
be the number of residual events containing candidate a. A surviving
composite argument has least prime factor>z, which supplies a residual event.
For N=2^k, two composite arguments cannot have the same odd least factor:
that factor would divide their sum N. Thus, pointwise,

    nu(a) >= 2 - 1_{a prime} - 1_{N-a prime}.

Reflection preserves A_z, so the leading-prime and trailing-prime counts
are both Q_z. Summing proves

    S1_z >= 2M_z-2Q_z,
    R_z <= 2Q_z-M_z.                                      (1)

This does not require semiprimality. Below the cubic cutoff, a composite
argument can meet several residual events, making the raw margin still
smaller. At the cubic cutoff on powers of2, (1) is an equality.

## Sieve inputs and remainder control

The required external tools are the fundamental lemma with weights of
absolute value at most1, and the unweighted, maximum-over-reduced-residues
Bombieri-Vinogradov theorem. Both are stated in [Kevin Ford's Sieve Methods
notes (2023), Theorems3.6 and3.4, PDF pp.38 and35](https://ford126.web.illinois.edu/sieve2023.pdf).
The sieve dimension condition is on PDF p.18. These statements apply here
with fixed dimensions2 and1; the following calculations check the inputs.

Set D=floor(N^(1/4)). The subpower condition ensures z<=sqrt(D) eventually
and s=log(D)/log(z)->infinity. Define products over odd primes only:

    V2(z) = product_{3<=p<=z} (1-2/p),
    V1(z) = product_{3<=p<=z} (1-1/(p-1)),
    V0(z) = product_{3<=p<=z} (1-1/p).

Their local densities satisfy the fixed-dimension hypotheses by Mertens'
product estimates; the factor at2 is set to zero in the density function
(equivalently,2 is not a sieve prime). All odd primes are coprime to N.

For M_z first restrict to odd a with both a,N-a>=z^2. The removed endpoint
regions contain O(z^2) candidates. Inside the central interval each p<=z
excludes exactly the two distinct classes a=0,N modulo p. For squarefree
odd d the intersection count is

    X * 2^omega(d)/d + O(2^omega(d)),  X=N/2+O(z^2).

The remainder sum is small enough. Indeed,

    sum_{d<=D} 2^omega(d)
      = sum_{e<=D} mu(e)^2 floor(D/e)
      <= D(1+log D).

Since V2(z) is bounded below by a positive constant times
1/log(2z)^2, both D log(D) and z^2 are o(N V2(z)). The fundamental lemma
therefore gives, including the endpoint correction,

    M_z = (1+o(1)) (N/2) V2(z).                          (2)

For Q_z the leading argument is prime. Its surviving complement is either
z-rough or is itself a prime<=z. The latter contributes at most pi(z).
Sieve the prime-supported sequence of N-p, for primes p<=N, by odd primes
through z. For every odd squarefree d the relevant reduced class is
p=N modulo d, with main term Li(N)/phi(d). It is reduced because N=2^k.
The maximum in Bombieri-Vinogradov therefore covers this N-dependent class
uniformly. Restricting the modulus sum to d<=N^(1/4) is permitted for large
N, and a fixed sufficiently large logarithmic saving makes its error
o(Li(N)V1(z)). The fundamental lemma gives the upper estimate

    Q_z <= (1+o(1)) Li(N) V1(z) + pi(z).                 (3)

Using the prime sequence through N rather than exactly3..N-3 can include
extra endpoint candidates. This only enlarges the upper bound. The
pi(z) term explicitly restores small prime complements that the ordinary
rough sieve would discard but the square-start presieve preserves.

## Comparison and conclusion

There is an exact product identity

    V2(z)/V1(z) = V0(z).

Also pi(z)=o(N V2(z)) under the subpower hypothesis. From (2) and (3),

    2Q_z/M_z <= (4+o(1))/(log(N)*V0(z)) + o(1).

Mertens' lower bound V0(z) >> 1/log(2z), valid uniformly for z>=2, makes
the right side tend to0. This handles bounded and unbounded z, including
sequences that do not themselves converge to infinity. When z->infinity,
V0(z)~2exp(-gamma)/log(z) gives the more familiar leading ratio

    2Q_z/M_z <= (2exp(gamma)+o(1))*log(z)/log(N).

Substituting in (1) proves R_z<=-(1-o(1))M_z<0 eventually. Higher
intersections can still restore a positive exact Goldbach count; they were
never included in this raw certificate.

## Finite examples and verification

`presieve_scaling.py` reuses the exact event masks while varying the cutoff.
It computes only the raw union lower bound and makes no two-overlap
assumption. `evidence/presieve-cutoff-scaling.json` freezes13 powers of2,
from2^8 through2^20, and three cutoff rules before computation. A separate
least-prime-factor array verifies every first-stage count, every leading
prime count, and the direct ordered Goldbach counts.

| N | Cutoff z | M_z | S1_z | Raw R_z | Actual ordered G |
|---:|---:|---:|---:|---:|---:|
| 32,768 | log2(N)=15 | 1,618 | 1,562 | 56 | 488 |
| 65,536 | log2(N)=16 | 3,240 | 3,524 | -284 | 870 |
| 65,536 | cube root cutoff40 | 1,940 | 1,268 | 672 | 870 |
| 1,048,576 | log2(N)=20 | 40,942 | 54,512 | -13,570 | 8,478 |
| 1,048,576 | cube root cutoff101 | 19,878 | 13,660 | 6,218 | 8,478 |

The negative raw values are failures of the shallow certificate; the exact
positive counts are independently verified. The first displayed negative
logarithmic case is not asserted to be the smallest failure among all even
targets, or an effective onset for the general asymptotic theorem.

Four focused tests compare arbitrary cutoff event membership and bounds
through500, test (1) on powers of2, check monotonicity when more events move
into the presieve, and validate the base/input cases. The low-cutoff example
a=105 at N=128 explicitly meets three distinct residual events3,5,7.

## Review and next consequence

The independent reviewer confirmed the proof and required the reflection
step in (1) and the small-prime-complement exception in (3) to be explicit.
The source lane verified the unweighted BV statement, the weight bound,
the dimension hypotheses, and the exact product ratio.

This shows why shrinking the first stage indefinitely is not a viable way
to make the raw formula close itself. The cubic cutoff remains outside this
negative theorem; the substantive unresolved direction is still a positive
bound controlling the reflected prime/semiprime correlation there.

## Fixed-power extension: current status

Resolved on 2026-09-08: `dhr_margin.py` contains the checked rational
comparison and remainder argument. For N through powers of two it proves
limsup R_z/M_z <= -347/14042 at z=N^(1/6), and <= -1/496 at
z=N^(20/119). Booker-Browning's explicit certified interval for beta_2
closes the numerical premise. No finite onset or Goldbach disproof follows.
The older candidate below records the superseded, more demanding route.

### Superseded candidate from the renewed run

A later bounded source check identified a route that might strengthen the
negative result to z=N^(1/6). This is not yet a proved extension. With
integer-sieve level D_M=N/log^B N and prime-supported BV level
D_Q=sqrt(N)/log^B N, the formal comparison would require

    f_2(6)>2*exp(2*gamma)/9,

where f_2 is the DHR dimension-two lower sieve function; the right side
is approximately0.70494. Exact DHR equations and the relevant numerical
parameters are recorded in Kao, arXiv:1606.03505, section4:
https://arxiv.org/html/1606.03505v1 . The source lane checked them, but its
printed decimal values are not a certified interval calculation.

If rigorous bounds beta_2<4.267, alpha_2>5, F_2(4)>1.836 and F_2(5)>1.20
are supplied, the differential equation and monotonicity would imply

    f_2(6)>=((25-4.267^2)*F_2(4)+11*F_2(5))/36>0.71309.

The remaining prerequisites are certified constant/function enclosures
and a complete treatment of the DHR weighted remainder sums at the proposed
levels. The source check supplied exact candidate equations, not those
missing proofs. Keep this dormant until a bounded attempt can close both;
do not silently replace the proved subpower statement with z=N^(1/6).

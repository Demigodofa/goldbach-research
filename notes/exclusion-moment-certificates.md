# Stacking exact exclusion counts into a survivor proof

Owner/purpose: Kevin's proposed sequence of calculations Z. Status: proved
finite counting inequalities and checked computation. The general method has
established probability/linear-programming precedents; no novelty claim.

## Counts passed between stages

Fix an even target N and the previously proved prime-safe window
`[p+1,q^2-1]`, where q is the prime after p. Restrict candidate a to odd values
such that both a and N-a lie in this window. Write M for the candidate count.

For each odd prime r<=p, the exclusion event B_r is `r|a or r|(N-a)`.
For an individual candidate let X(a) be the number of distinct such events it
meets. Count a prime once even if it divides both summands. Define

    S_j = sum over j-element sets D of |intersection_{r in D} B_r|
        = sum over candidates a of binomial(X(a),j),
    S_0 = M.

CRT combines the forbidden residue classes0 and N modulo each r, merging
them when r|N. For a resulting class b modulo d, its number of representatives
in [L,H] is exactly

    floor((H-b)/d) - floor((L-1-b)/d).

Including the initial odd class modulo2 enforces parity. Disjoint CRT classes
can be added without double counting. A zero intersection has no nonempty
descendant, so the implementation safely prunes it. This uses floor arithmetic
on residue classes rather than selecting a Goldbach witness.

The survivor count Z is the number of candidates with X(a)=0. Every survivor
gives two primes by the prime-safe-window theorem. A positive lower bound
therefore certifies N even if its individual witness was never searched for.
Counts are for ordered pairs; a and N-a are distinct candidates unless equal.

## A bound on how many exclusions can overlap

Let r_1<...<r_m be the odd wheel primes. If a candidate meets k distinct
exclusions, their product divides a(N-a). Hence

    r_1*...*r_k <= a(N-a) <= floor(N^2/4).

This bounds k by a finite K even when the wheel has many more than K primes.
Consequently `Z=sum_{j=0}^K (-1)^j S_j` is exact; all later terms vanish.
The initial implementation uses this conservative product cap. For odd
summands, when N is divisible by4 the product upper bound improves by1.

The reviewer derived a stronger optional cap. Let

    T_k = min over subsets A of {r_1,...,r_k}
          (product(A) + product(complement(A))).

Assign each excluded prime to a summand it divides. The two assigned products
divide a and N-a, so their sum is <=N. Replacing chosen primes by smaller
ones cannot increase the minimum. Thus k exclusions require T_k<=N.
For N=246, the product test permits five primes because15015<=15129,
but the best split is105+143=248>246. The split test therefore permits at
most four exclusions. This is a proved refinement, separate from any measured
performance benefit.

## Polynomial lower bounds can use earlier stages more effectively

Any polynomial Q with Q(0)=1 and Q(k)<=0 for integers1<=k<=K satisfies

    Z >= sum_a Q(X(a)).

Expressing Q in the binomial basis makes its sum a linear combination of the
known S_j. Round a rational lower bound upward because Z is an integer.

The quadratic `(1-x)(1-x/K)` gives, for K>=2,

    Z >= ceil(M-S_1+2*S_2/K).

The cubic `(1-x)(1-x/a)(1-x/(a+1))`, for integer a>=1, is nonpositive at
every positive integer: the only additional positive-sign interval lies
strictly between the adjacent integer roots a and a+1. It gives

    Z >= ceil(M-S_1 + ((4a-2)*S_2-6*S_3)/(a*(a+1))).

For a=2 this is third-degree Bonferroni. Other choices can give a larger
bound. These inequalities were independently derived and checked by the Sol
reviewer; tests also exhaust arbitrary small multiplicity histograms.

**Worked target1000.** In the prime-safe window using p=31,q=37, the odd
candidates are33 through967. CRT counts give

    M=468, S_1=902, S_2=724, S_3=296.

Ordinary third-degree Bonferroni gives -6 and is inconclusive. The a=3 cubic
instead gives

    Z >= ceil(468-902+(5*724-3*296)/6) = 22.

Thus this third overlap stage already proves prime-pair existence. Continuing
through the product cap K=5 yields the exact count48 in this chosen window.
No universal statement about other N follows from this example.

## Initial1,000-target experiment

`evidence/exclusion-stages-1000.json` covers evens6 through2004. All1,000
targets obtained a positive lower bound. Stopping degrees were:

| Highest overlap degree evaluated | Targets settled |
|---:|---:|
| 0 | 2 |
| 1 | 21 |
| 2 | 59 |
| 3 | 737 |
| 5 | 181 |

Thus819 settled by degree3. In405 cases the quadratic or adjusted cubic was
positive while the ordinary odd Bonferroni bounds available at that stage
were not. This excludes seven early exact-closure/base cases from the comparison.
The run used1,754,292 CRT/floor evaluations and took0.547 seconds on the shared
machine; this is descriptive, not a benchmark against a tuned sieve.

All1,000 reported lower/upper bounds were independently checked against prime
pairs counted by a separate sieve. The full CRT intersection sequences through
N=1000 were compared with direct divisibility multiplicities; generic moment
bounds were checked on all histograms with entries0,1,2 and support0 throughK,
for each K<=6. Full representative moment sequences are retained in
`evidence/exclusion-count-examples.json`.

This experiment counts each finite target. It does not yet prove one uniform
formula positive over an unbounded family.

## Strongest real bound from the retained moments

Let n_k>=0 be unknown multiplicity counts for k=0,...,K, constrained by the
known moments `S_j=sum_k binomial(k,j)*n_k` through degree d. Minimizing n_0
is a finite linear program. Its dual maximizes `sum_j c_j*S_j` over
polynomials Q of degree<=d with Q(0)<=1 and Q(k)<=0 for1<=k<=K.

For feasible input moments the objective is bounded above by an actual n_0.
For d<=K the polynomial polyhedron is pointed: a lineality polynomial would
vanish at K+1 distinct nodes and therefore vanish identically. A positive
optimum must have Q(0)=1, since otherwise positive rescaling improves it.
An optimal nonzero vertex has d distinct positive integer roots. Sign changes
force the first root to be1, pair each positive-sign interior gap into adjacent
roots, and require the final root K when d is even. Thus enumerate:

- Odd degree: root1 and disjoint adjacent pairs.
- Even degree: roots1,K and disjoint adjacent pairs strictly between them.
- Also retain the zero lower bound.

This family gives the optimal **real** moment-LP bound. Its upward rounding
need not equal the stronger integer-programming bound. K=0 is exactly M;
d=0<K gives0; d>=K gives exact inclusion-exclusion through K. The input
moments must be feasible exact counts; the polynomial module alone does not
certify their provenance.

Sol independently proved this vertex argument. `moment_polynomials.py` uses
exact rational finite differences to get the binomial coefficients. A separate
test enumerates primal supports and solves rational linear systems; its optima
match the dual-polynomial results on frozen feasible small instances. Generic
sign and histogram tests supply additional checks.

Using this full root family and the split cap on the same1,000 targets gives
stopping counts2,21,60,736,181 at degrees0,1,2,3,4, respectively. All1,000
now settle by degree4. CRT/floor evaluations fall from1,754,292 to1,505,240;
measured time rises from0.547 to0.687 seconds because exact-bound selection
also costs work. These are descriptive shared-machine timings, not a claimed
speedup. All refined lower/upper bounds passed independent prime-pair counts.
See `evidence/exclusion-stages-root-split-1000.json`.

## A concrete proof that three aggregate moments lose needed information

For N=554, exact divisibility counts give the actual histogram below. An
abstract histogram with no survivors has the same M,S_1,S_2,S_3 and cap K=5:

| Exclusion multiplicity k | Actual candidates | Abstract alternative |
|---:|---:|---:|
| 0 | 17 | 0 |
| 1 | 72 | 132 |
| 2 | 88 | 18 |
| 3 | 56 | 76 |
| 4 | 12 | 27 |
| 5 | 8 | 0 |

Both columns yield `[M,S_1,S_2,S_3]=[253,504,408,184]`. Therefore these
aggregates and K alone cannot force a survivor, even with integer counts.
The abstract column does not reproduce the actual modular locations or each
prime's individual exclusion set; it is not a Goldbach counterexample.

The next moment distinguishes them. The actual S_4 is52. The polynomial with
roots1,2,3,5 gives

    Z >= ceil(M-S_1+S_2-S_3+4*S_4/5) = 15.

All181 initial targets needing more than three overlap degrees admit such an
integer zero-survivor alternative for the first three aggregates. The bounded
constructor checks its output moments exactly. This identifies a real loss
of information in the proposed interface, and shows precisely what the fourth
stage recovers. See `evidence/three-moment-information-loss.json`.

## The fixed four-degree rule fails at4412

The next scan tested evens2006 through20000, stopping at its first
inconclusive degree-four bound. It reached4412 after1,204 targets. The chosen
prime-safe window has p=61,q=67 and2,144 odd candidates63 through4349.
Its first moments are

    [M,S_1,S_2,S_3,S_4]=[2144,5204,5490,3314,1198], K=7.

The abstract integer histogram

    [n_0,...,n_7]=[0,861,0,887,348,9,28,11]

has exactly the same five quantities and no survivors. It proves that even
integer moment reasoning using those inputs alone cannot certify this target.
The real window has88 ordered prime pairs, independently counted by trial
division. The fifth moment252 yields a lower bound67; the sixth moment26
yields85; exact closure yields88. This refutes the fixed four-degree
sufficient-condition hypothesis, not Goldbach or adaptive stages.
Receipts: `evidence/fixed-degree-four-falsifier.json` and
`evidence/degree-four-information-loss-4412.json`.

Next test a materially different interface: retain location by partitioning
the candidate-summand window and computing low-degree moments separately.
Global aggregation may hide a locally positive bound. Compare the same total
candidate window and preserve every gap; do not claim a uniform future result
from one rescued example. Candidate-summand windows are distinct from blocks
of target even numbers.

## Prior art

Prékopa's [1988 Boole-Bonferroni and linear-programming paper]
(https://pubsonline.informs.org/doi/10.1287/opre.36.1.145)
uses initial binomial moments to obtain sharp bounds for a union of events.
The complement is the zero-event probability considered here. His [1990
discrete-moment paper](https://doi.org/10.1016/0166-218X(90)90068-N) develops
the finite-support moment/linear-programming connection and dual polynomial
structure. Our investigation adapts this established family to the finite
Goldbach exclusion counts; it has not established a new general sieve bound.

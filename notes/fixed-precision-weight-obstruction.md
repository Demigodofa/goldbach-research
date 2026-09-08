# Fixed integer precision cannot give an eventual universal block certificate

Owner: Kevin's Goldbach investigation; derivation: Rill. Purpose: falsify a
specific proposed universal use of our block formula before investing in
that use. Status: proof independently checked by Sol on 2026-09-08. Visible
provenance: independently synthesized in this run from the local-peak idea,
standard progression counting, and Vaughan's global theorem. Novelty label:
new-to-this-task; no worldwide originality claim or finite threshold.

## Stronger theorem about genuine representation counts

For every fixed m>=2 and H>0, there are infinitely many even N such that
all m counts G(N),G(N+2),...,G(N+2m-2) are positive and

    G(N)>H*sum_{j=1}^{m-1}G(N+2j).

Thus a count can dominate all its finitely many subsequent neighboring
counts by an arbitrarily large prescribed factor. The proof below already
establishes this: omit the integer weights, and choose
s(P)>168*H*sum_{j=1}^{m-1}s(2j). The leading lower bound in (2) and the
neighbor upper bounds in (2),(5) give the displayed ratio. All counts are
genuine prime-pair counts; their simultaneous positivity follows from the
same exceptional-set argument, not an unproved pointwise conjecture.

Consequently, for m>=3, ANY positive weighting rule whose within-block
dynamic range max_j(w_j)/min_j(w_j) is bounded by a fixed constant D
fails the test Z>0 on infinitely many fully represented blocks. The rule
may depend on targets, position, history, or even counts; the range bound
alone is enough. Choose H>2D/(m-2), so the weighted leading value exceeds
2/(m-2) times the sum of the weighted neighbors, and apply the final Z
inequality below. The fixed integer rule is a corollary since 1<=w(n)<=C.

## Statement

Write s(n)=product over odd primes p dividing n of (p-1)/(p-2). Fix an
integer m>=3 and a positive integer C. At each even target use

    w(n)=ceil(C/s(n)),   x_j=w(N+2j) G(N+2j),   0<=j<m,
    Z=(sum_j x_j)^2-(m-1)sum_j x_j^2.

Proposed conclusion: there are infinitely many even N for which every one
of the m consecutive targets is Goldbach-representable, yet Z<0.
In particular, the fixed C=2^32 rule cannot certify all sufficiently large
1,000-target blocks. This says nothing against the sound implication
Z>0 => all counts positive. It refutes completeness of one fixed choice
of weights, not Goldbach or the aggregate-moment interface.

The quantifiers matter: m and C are fixed first; an enormous but fixed
auxiliary prime product is then chosen; only the interval parameter X
tends to infinity. No modulus is permitted to grow with X in this proof.
For m=2 the conclusion is false: Z=2x_0x_1 is always positive when both
counts are positive. For m=1 the test is simply x_0^2>0.

## Input from established mathematics

Let kappa=2*product_{p>2}(1-1/(p-1)^2)>0, so that the full Goldbach
singular series on even n is kappa*s(n). Let

    R(n)=sum_{p+q=n} (log p)(log q),

where p and q are primes, ordered. This is a prime-only logarithmically
weighted count, not a sum including all prime powers. Vaughan's global
mean-square theorem gives, for every fixed A>0,

    sum_{n<=Y} |R(n)-n*kappa*s(n)|^2 <<_A Y^3/(log Y)^A

on the even terms (the source also defines its series for odd terms).
The checked authority is R. C. Vaughan, *The Hardy-Littlewood Method*,
second edition, Chapter 3 section 3.2, printed pp.34-36: definition (3.16),
singular series (3.26), and Theorem 3.7, p.36. A readable scan is
https://djvu.online/file/y04IjoKF754hT . The 1972 article's publisher record
https://doi.org/10.4064/aa-22-1-21-48 confirms bibliographic metadata only;
its PDF was not read in this run. No numerical constant or validity
threshold is extracted from the book theorem.

Apply the theorem at Y=3X. Outside o(X) even n in [X,3X],

    (kappa/2)*s(n)*n <= R(n) <= (3*kappa/2)*s(n)*n.       (1)

Indeed every bad n contributes at least (kappa*X/2)^2 to the error sum,
because s(n)>=1. Any one fixed A>0 then gives o(X) bad n.

Put L=log X. For these good n, uniformly as X tends to infinity,

    (kappa/4)*s(n)*n/L^2 <= G(n) <= 7*kappa*s(n)*n/L^2. (2)

For the lower bound, R(n)<=(log(3X))^2 G(n), and eventually
(log(3X))^2<=2L^2. For the upper bound, pairs with both primes greater
than sqrt(X) have logarithmic weight at least L^2/4, so their count is
at most 4R(n)/L^2. Pairs with one smaller prime number at most 2sqrt(X),
which is eventually at most kappa*s(n)*n/L^2. Combine these with (1).
Thus (2) concerns genuine prime pairs and in particular implies G(n)>0.

## A fixed progression with one very large singular factor

Choose an integer y>2(m-1) and let P be the product of all primes <=y.
For multiples N of P, every prime <=y dividing N+2j, 1<=j<m, divides
2j, and conversely. Therefore

    s(N)>=s(P),
    s(N+2j)=s(2j)*exp(T_j(N)),
    T_j(N)=sum_{p>y, p|N+2j} log((p-1)/(p-2)).           (3)

For an even argument 2 the empty singular-factor product is 1. Multiplicity
of a prime factor never changes s. Let A_X be the consecutive multiples
of P in [X,2X], of cardinality K_X=X/P+O(1).

For p>y, multiplication by P is invertible modulo p, so at most
K_X/p+1 members of A_X have p dividing N+2j. Also
log((p-1)/(p-2))<=1/(p-2)<=3/p. For X large enough every such prime is
at most 3X. Consequently

    average_{N in A_X} sum_{j=1}^{m-1} T_j(N)
      <=3(m-1)sum_{p>y}1/p^2
        +3(m-1)/K_X * sum_{p<=3X}1/p
      <=3(m-1)/(y-1)+O_m(log(3X)/K_X).                (4)

The error tends to zero because P is fixed. Choose y large enough that
3(m-1)/(y-1)<1/4. Markov's inequality then shows that a proportion
at least 3/4-o(1) of A_X has sum_j T_j(N)<=1. For all these N,

    s(N+2j)<=e*s(2j)<3*s(2j),  1<=j<m.               (5)

Finally s(P) tends to infinity as y grows. One elementary reason is
log((p-1)/(p-2))>=1/(p-1)>=1/p and the divergence of sum_p 1/p.
The usual prime harmonic asymptotic is recorded in
https://dlmf.nist.gov/27.11.E8 .
Thus we may choose a single y meeting (4), y>2(m-1), and

    s(P)>112/(m-2) * sum_{j=1}^{m-1}(C+3*s(2j)).       (6)

Only after this choice is made do we let X tend to infinity.

## Simultaneous genuine counts and a failed Z

There are o(X) bad targets for (2). For fixed m the set of N for which
any N+2j is bad also has cardinality o(X). Since P is fixed, this is
o(K_X), regardless of how huge P is. Remove these bad N from the positive
proportion of A_X satisfying (5). A positive proportion remains for all
sufficiently large X; each corresponding entire block has G(N+2j)>0.

For such a block let B=sum_{j=1}^{m-1}x_j. Since w(N)>=1, (2) gives

    x_0 >= (kappa/4)*s(P)*N/L^2.

For every s>0, ceil(C/s)*s<C+s. Since N+2j<=2N for large N, (2) and
(5) give

    B <=14*kappa*N/L^2 * sum_{j=1}^{m-1}(C+3*s(2j)).

Equation (6) therefore implies x_0>2B/(m-2). Cauchy-Schwarz on the
other m-1 entries gives B^2<=(m-1)sum_{j=1}^{m-1}x_j^2. Hence

    Z=-(m-2)x_0^2+2Bx_0+B^2-(m-1)sum_{j=1}^{m-1}x_j^2
      <=x_0*(2B-(m-2)x_0)<0.

Taking disjoint dyadic ranges of sufficiently large X gives infinitely
many such blocks. No individual counterexample at C=2^32 is identified
or claimed. The global almost-all theorem is enough for this existential
falsifier because the modulus is fixed; it would not certify an arbitrary
named 1,000-target block.

In fact the proof retains at least (3/4-o(1))X/P acceptable starts in
each [X,2X], and hence at least X/(2P) eventually. The failure set has
positive lower density, though its P-dependent bound may be extremely
small. The fixed P depends on m and the requested count ratio or weight
range. This stronger density consequence was separately checked by Sol.

## What survives and the repair target

Exact reciprocal weights 1/s(n) do not have this rounding floor. Neither
do adaptive integer scales C chosen to keep s(n)/C small in the block:

    1 <= ceil(C/s(n))*s(n)/C < 1+s(n)/C.

For any prescribed delta>0, C>=max_block s(n)/delta bounds that relative
rounding distortion by delta using target factorization only. This removes
the specific amplification in this proof; it does not prove positive Z
for all actual prime counts. Analytic concentration of those counts is
still required. Existing finite receipts remain valid with their recorded
weights and are not overwritten.

The elementary outlier implication and equality boundary were checked
with exact fractions in 39,050 cases: m=3..7, tail entries 0..4, leading
entry exactly 2B/(m-2) or one larger. Every case satisfied the claimed
nonpositive or negative conclusion. These checks validate arithmetic
implementation only; they are not substitutes for the infinite proof.

## Implemented precision repair and finite comparison

`block_moments.adaptive_weight_bits(first_even,count,d)` selects the
smallest b>=1 for which 2^b>=d*max_block s(n), using exact fractions and
integer comparisons only. Use that b as the common `bits` argument for
`make_certificate`. The normalized rounding factor is in [1,1+1/d).
This is a target-only bound; selecting b does not inspect a Goldbach count.
The common block scale can grow without a predetermined bit limit.

The frozen comparison uses the previously independently checked block
100000..101998 and bit counts 1,2,4,8,32. Their support lower bounds are
978,988,999,1000,1000. With d=10000, the adaptive rule chooses 16 bits and
also certifies 1000. Its maximum singular factor is exactly 6912/1925.
All six receipts replayed and share the count hash independently checked
in `evidence/block-moment-certificates.json`; their exact moments and rules
are retained in `evidence/weight-precision-comparison.json`.

The full suite now has 82 passing tests both normally and under Python -O.
New tests check the least valid precision, exact relative distortion,
invalid inputs, and the outlier boundary. The earlier fixed-bit receipts
are preserved and retain their valid finite conclusions. These experiments
do not exhibit a 32-bit failure or locate the theorem's enormous onset.

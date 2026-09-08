# What the next calculation must retain

Owner/purpose: guide Kevin's stacked-formula investigation away from a hidden
assumption about prime-pair overlap. These are source boundaries and a precise
next experiment, not a new theorem proving Goldbach.

## Relevant limitations in the literature

Tao's [general parity-obstruction discussion]
(https://terrytao.wordpress.com/2014/11/21/a-general-parity-problem-obstruction/)
uses the Goldbach forms m and N-m explicitly. Its broad criterion relies on a
Liouville pseudorandomness principle and is not presented as an unconditional
impossibility theorem for all methods. It explains why certain sieve counts
can leave the parity of the number of prime factors unresolved. It does not
invalidate exact finite modular computation or our prime-safe-window theorem.

Ford and Maynard's [prime-producing sieves, Theorem2.1, pp.2-3]
(https://www.ford126.web.illinois.edu/wwwpapers/prime-producing-sieves.pdf)
give a formal limitation for specified Type I and Type II axioms: in certain
parameter ranges, nonnegative sequences can satisfy those distribution
conditions while vanishing on primes. This limits what follows from those
particular axioms. It is not a theorem that every enhanced sieve, exact
calculation, or Goldbach approach must fail.

## A precise but currently unsupported sufficient correlation estimate

Let Lambda be the von Mangoldt function: Lambda(p^k)=log p for prime p and
k>=1, and zero otherwise. A possible extra input would be constants c>0,N0
such that, for every even N>=N0,

    sum_{N/4 < m <= 3N/4} Lambda(m)*Lambda(N-m) >= c*N.

This is joint information about reflected arguments, not a consequence of
separate prime counts. We have not proved or assumed this estimate. It is
already a strong quantitative version of the needed Goldbach information.

**Prime powers matter.** Mere positivity of this sum does not establish that
both arguments are prime, since Lambda also supports proper prime powers.
For N>=2, the number of proper prime powers <=N is at most

    floor(log_2 N)*sqrt(N).

Indeed each exponent k>=2 contributes at most N^(1/k)<=sqrt(N), and there
are at most floor(log_2 N) relevant exponents. Counting duplicates only makes
this upper bound larger. Terms with at least one proper prime-power argument
therefore contribute at most

    2*floor(log_2 N)*sqrt(N)*(log N)^2 = o(N).

The hypothetical c*N lower bound eventually exceeds this contribution,
forcing a term with both arguments prime. This subtraction is necessary;
the initial source-researcher wording omitted it and Rill corrected it before
acceptance. No numerical cutoff is asserted.

## Next bounded experiment: count exclusion overlaps exactly

For a fixed N and a prime-safe candidate window, first restrict to odd
candidate summands a_i. For each remaining wheel prime r, let B_r be the
indices for which r divides a_i or N-a_i. For a subset D of primes, CRT gives
the exact forbidden residue classes; floor arithmetic counts their intersection
without individually searching prime-pair witnesses.

Let S_j be the sum of all j-fold intersection sizes and S_0 the candidate
count. Bonferroni gives rigorous lower bounds at odd truncation degree and
upper bounds at even degree. Feed the best lower and upper bounds forward;
a positive lower bound settles the target. A later interval analysis can ask
whether one bound holds uniformly across many targets.

Do not assume successive odd truncations improve monotonically. For a point
belonging to ten exclusion sets, degrees1 and3 contribute -9 and-84,
respectively. Retain the maximum lower bound obtained so far. The experiment
will measure whether low-degree overlap information suffices on bounded
examples and how much exact arithmetic was needed. Its failure would reject
that truncation level, not exact inclusion-exclusion or Goldbach.

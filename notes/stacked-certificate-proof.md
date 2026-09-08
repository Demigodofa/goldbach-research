# Three stages of finite coverage

Purpose: turn Kevin's stacking and interval-elimination idea into an exact,
reviewable finite algorithm. This is new-to-this-task, not a new Goldbach bound.

## Stage 1: certified prime inputs

An integer x>1 is composite only if it has a prime divisor at most sqrt(x).
A segment ending at H can therefore be sieved exactly using every prime up to
floor(sqrt(H)), starting each prime's removals at max(p^2,ceil(L/p)*p).
Starting at p^2 preserves p itself. The remaining values greater than1 are prime.
The implementation additionally checks selected input primes by trial division
for representative blocks, or against a separate monolithic sieve in a large
stacking run. It never labels an untested probable prime as a proof.

## Stage 2: a progression of sums from two prime progressions

Let A={a+di:0<=i<m} and B={b+dj:0<=j<n}, with every member prime and
d a positive even integer. Then

    A+B = {a+b+dt : 0<=t<=m+n-2}.

Proof: each sum has t=i+j in this range. Conversely, for every such t choose
`i=min(m-1,t)` and `j=t-i`; these indices lie in the two allowed ranges.
Thus every output is the sum of two primes, without searching for its pair.
This certifies an arithmetic progression of even targets. It certifies a
contiguous interval of evens only when d=2; other steps leave residue gaps.

## Stage 3: union with explicit unresolved positions

For a block of 1,000 even targets, convert each output progression into its
exact membership mask. The union is certified because membership in any one
output is enough. If all 1,000 bits are set, the whole block is certified.
Otherwise preserve the zero positions as unresolved. Overlap does not add
extra coverage, and no gap is filled merely because surrounding values work.

Greedy selection minimizes the number of retained certificates approximately;
it is not claimed optimal. Every chosen certificate is independently checked
for prime inputs, arithmetic endpoints, and output membership. Adjacent complete
block certificates can then be composed after checking parity and endpoints.

## Measured representative blocks

Each row contains exactly1,000 even targets. Times below are certificate
generation only; separate trial-division verification adds additional work.

| First target | Last target | AP-sum certificates | Unique prime inputs checked | Generation seconds |
|---:|---:|---:|---:|---:|
| 1,000,000 | 1,001,998 | 195 | 231 | 0.296 |
| 1,000,000,000 | 1,000,001,998 | 218 | 222 | 0.250 |
| 1,000,000,000,000 | 1,000,000,001,998 | 225 | 200 | 0.250 |

All three blocks were completely certified; all selected input primes passed
exhaustive trial division. The experiment demonstrates certificate composition
and reduction in per-target witness material. It does **not** establish a speed
advantage over a tuned Goldbach sieve or a universal rule covering future blocks.
These values are far inside the already published binary verification bound.

## Full stack and carry-forward measurement

`evidence/stack-1000-blocks.json` records a complete composition of1,000 blocks
of1,000 evens each, from4 through2,000,002. It used193,669 AP certificates,
no unresolved targets, and no palette expansion beyond1,000. Total run time
was558.953 seconds. The receipt retains per-block summaries, while the three
representative full certificate files above retain source-prime proof inputs.
The script can reconstruct the complete run; the aggregate receipt alone does
not contain every underlying certificate.

The large run used ordinary Python, with its original assertion checks active.
The hardened explicit-exception verifier subsequently passed the retained
representative certificates under `python -O`. The large run was not repeated
merely to reconfirm the same finite coverage.

An AP-sum certificate may extend beyond the block where it was selected. Its
full output can be intersected with a later block and those targets removed
from the unresolved mask. Reverify its prime inputs and reconstruct its output
before reuse; never trust a saved certified label or copied coverage count.
If this union fills the later block, new prime generation can be skipped.

`evidence/carryover-comparison.json` compares ten equal adjacent blocks starting
at1,000,000. Carry-forward settled56 of10,000 targets; zero full blocks skipped
fresh generation. Fresh mode took3.858 seconds; carry mode4.189 seconds,
including required carry validation. These descriptive timings provide no
speedup evidence. Both modes left zero unresolved targets. Meaningful corruption
and full-carry tests live in `test_carryover.py`.

## A necessary change between stages: the prime palette must be able to grow

No fixed finite list S of primes can supply a summand for every even integer.
For a direct elementary proof take `N=4*product(S)`. For every p in S,

    N-p = p * (4*product(S\{p})-1),

and the second factor is at least3. Thus every N-p is composite. The same
holds for arbitrarily large suitable multiples of product(S). This needs no
Goldbach assumption or distribution theorem. It refutes a fixed-input palette,
not a changing palette or the certificate-composition rule.

For instance, 510510 is divisible by every prime through17, and exceeds twice
each of them. None of those primes can be one summand of a Goldbach pair for
510510. A later stage must permit larger primes or another supported mechanism.

**Unresolved mathematical interface:** derive a bound or invariant showing that
the evolving prime inputs necessarily generate a complete next-block mask.
Generating and checking the mask is finite computation. Proving it always fills
is the missing universal statement.

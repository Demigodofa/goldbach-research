# Two aggregate moments can certify an entire finite block

Owner: Kevin's Goldbach investigation. Purpose: formulate a collective
calculation Z that accepts aggregate estimates and can compose across
adjacent blocks. This is a new-to-this-task use of Cauchy-Schwarz, not a
new theorem about the distribution of prime pairs.

## Exact certificate

Let G_i be the ordered Goldbach count for each of m targets. Choose strictly
positive weights w_i, and put x_i=w_i G_i. Then x_i>=0, with x_i>0 exactly
when G_i>0. Define two aggregate moments

    S=sum_i x_i,   T=sum_i x_i^2.

If T=0, every entry is zero. Otherwise, if r entries are positive,
Cauchy-Schwarz on their support gives S^2<=rT. Therefore

    r >= ceil(S^2/T),
    number_of_zeros <= m-ceil(S^2/T).

In particular the exact integer test

    Z=S^2-(m-1)T > 0

certifies every target at once. Equality is insufficient: the vector
(0,2,2) gives m=3,S=4,T=8,Z=0. Conversely the positive vector (1,1,100)
fails the test. Thus failure is inconclusive, rather than evidence of an
actual zero count. No optimality over integer-valued inputs is claimed.

For m>=2 and S>0 the same condition is

    CV^2=(mT-S^2)/S^2 < 1/(m-1).

The code uses exact integers for the decision. Decimal CV values in the
experimental receipt are diagnostic only.

The certificate also accepts separately proved bounds S>=L>=0 and T<=U:

    L^2>(m-1)U

is sufficient. Those bounds must have an independent justification. A caller
supplying two unsupported numbers has not proved anything about a block.

## Target-only normalization

Raw Goldbach counts fluctuate strongly with the target's divisibility.
The Hardy-Littlewood prediction includes the factor

    s(N)=product_{odd prime p|N} (p-1)/(p-2).

The ordered-count prediction is G(N)~2*C2*s(N)*N/log(N)^2, with C2 the
twin-prime constant. It is stated as a conjecture in [Bhowmik and Halupczok,
Conditional Bounds on Siegel Zeros, Section3, PDF pp.7-8](https://pro.univ-lille.fr/fileadmin/user_upload/pages_pros/gautami_bhowmik/Publications/CANT2020.pdf).

This motivates, but is not a premise of, the frozen integer weights

    w_N=ceil(2^32 * product_{odd prime p|N} (p-2)/(p-1)).

The product is evaluated exactly over distinct odd prime factors. The
ceiling is always at least1, including when a very large singular factor
would make a fixed-scale floor vanish. These weights depend only on N,
not on its computed G(N). Consequently the certificate remains valid
regardless of whether the conjectural normalization is accurate. We do not
use count-dependent weights such as1/G(N).

## One subdivision can strengthen the bound

Use the same weights when splitting a block into disjoint parts j. Ignore
parts with T_j=0 in the following sum; they have S_j=0. Weighted Cauchy gives

    sum_j S_j^2/T_j >= (sum_j S_j)^2 / sum_j T_j.

After ceiling, the sum of the partwise positive-count lower bounds is at
least the bound from the whole block. In particular, if every part certifies
all its entries, their disjoint union is certified. This is ordinary proof
composition with verified coverage. Finer partitions may cost more work;
at singleton resolution this reduces to separate positivity checks.

## Implementation and frozen experiment

`block_moments.py` implements the exact support bound, the bounded-moment
criterion, the target-only weights, and canonical replay. Its current
producer computes exact finite counts from the packed prime polynomial
before aggregating them. It has not yet replaced those computations with
analytic moment bounds. Externally supplied receipts must pass
`replay_certificate`; all serialized fields are compared with a fresh
computation, including the moment values, weights and count hashes.

The experiment froze three blocks of1,000 even targets and both unit and
singular-factor weights before calculation. All3,000 ordered counts were
independently checked using direct prime-complement tests from a separate
full sieve, including the equal-prime diagonal correction. Exact moments
matched those independent counts, and all receipts replayed.

| First even target | Unit-weight lower bound on positives | Target-weight lower bound | Target-weight CV^2 |
|---:|---:|---:|---:|
| 10,000 | 870 | 998 | 0.00254355 |
| 100,000 | 871 | 1,000 | 0.000275894 |
| 1,000,000 | 870 | 1,000 | 0.0000424810 |

The strict threshold for these blocks is1/999. The first weighted block
did not pass, so a single adaptive subdivision was frozen: two adjacent
parts with500 targets each. Both10,000..10,998 and11,000..11,998 passed,
certifying the entire original block by composition. Their moments were
independently checked and their receipts replayed. No further subdivision
or search was performed. The retained evidence is
`evidence/block-moment-certificates.json`.

Six focused tests include all nonnegative vectors of lengths1..6 with
entries0..3, strict boundary and inconclusive-positive examples, exact
factor weights, verified-moment-bound inputs, direct trial-prime moment
checks, and receipt type/value tampering.

## Where the unbounded difficulty remains

The second moment expands as

    T=sum_N w_N^2 sum_{p+q=N} sum_{p'+q'=N} 1.

It therefore contains information about prime quadruples satisfying
p+q=p'+q'=N, and how representations concentrate within the specified
block. A uniform lower bound for S and upper bound for T sharp enough to
make Z positive have not been proved. The correlation information has
moved into an aggregate quantity; it has not disappeared.

A partial bound such as998 also does not identify which targets are
positive or which two could remain unresolved from those moments alone.
The independent finite counts in this experiment are all positive, but that
fact must not be attributed to an aggregate test that only certified998.
There is no speed claim, no effective infinite-range moment estimate, and
no proof of Goldbach. The useful new interface is an exact block condition
that can consume future rigorously justified moment bounds.

## Later review and precision refinement

The renewed run independently checked the implementation and all eight
retained receipts. No material defect was found. A later theorem proves
that any fixed within-block dynamic range of positive weights fails this
test on infinitely many fully represented blocks; see
`fixed-precision-weight-obstruction.md`. That includes the fixed 32-bit
rule, while leaving every earlier accepted finite certificate valid.

The implemented adaptive bit rule bounds relative rounding distortion by
1/d from target factorization alone. At d=10000 it chooses 16 bits for
100000..101998 and certifies all 1000 targets. Nine focused tests and the
full 82-test suite pass normally and under optimized Python.

A more useful analytic precision target is centered energy about a fixed,
independently specified positive reference a:

    E_a=sum_i(x_i-a)^2 < a^2.

A zero coordinate alone would contribute a^2. Equivalently, completing
the square shows this inequality forces Z>0. The strict normalized RMS
threshold is 1/sqrt(m), or 3.16228% at m=1000. Equality is insufficient,
as (0,a,...,a) shows. By contrast, separate relative bounds on the large
first and second moments around a flat model require symmetric relative
error below about 0.0333482% at m=1000. These are different error models.
Neither threshold supplies its own analytic premise or removes the need
to control prime-pair correlations. The adaptive almost-all proof attempt
is recorded separately in `adaptive-moment-almost-all.md`.

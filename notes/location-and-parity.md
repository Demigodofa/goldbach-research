# What location preserves and truncated overlap counts omit

Owner/purpose: Kevin's staged Goldbach investigation. These are proved finite
information statements with a checked example. They do not prove Goldbach or
an impossibility theorem for prime-specific methods.

## Optimizing before aggregation preserves more information

For a fixed multiplicity cap K and maximum overlap degree d, write

    L(s) = max over feasible polynomials Q of c_Q dot s,

where s is the exact binomial-moment vector and Q is a pointwise lower bound
for the zero-multiplicity indicator on integers 0 through K. Include Q=0.
For disjoint candidate windows, moment vectors add exactly. Hence

    L(sum_i s_i) <= sum_i L(s_i).

The left side chooses one polynomial after combining the data; the right side
may choose a different valid polynomial in each window. Because survivor counts
are integers, summing the rounded local bounds also cannot be worse than the
rounded global bound. A refinement preserves this inequality. Arbitrary
partitions of different sizes need not refine each other.

Each local cap must be valid. Keeping the global cap everywhere makes the
comparison depend only on location. If smaller local caps are independently
proved, they can strengthen the local bounds further. Do not silently use a
smaller cap merely because a window contains fewer candidates.

## N=4412: location rescues a degree-four bound

Keep the original odd candidate sequence 63 through 4349, its 17 odd wheel
primes, cap K=7, and overlap degree 4. Split candidate indices into equal
adjacent parts. These are windows of candidate summands, not blocks of target
even integers.

| Parts | Sum of integer lower bounds | Sum of upper bounds | CRT/floor evaluations in local calculations |
|---:|---:|---:|---:|
| 1 | 0 | 314 | 25,918 |
| 2 | 0 | 314 | 40,148 |
| 4 | 0 | 314 | 58,856 |
| 8 | 4 | 314 | 81,740 |
| 16 | 12 | 314 | 108,336 |

Every count is for ordered pairs. Four survivors guarantee two distinct
unordered prime pairs here; the middle value N/2 is even and cannot be an
odd-prime summand. Independent exact counting finds 88 ordered pairs in the
entire window.

The two-half split cannot help this target: reflection a -> N-a preserves
every exclusion event and exchanges the halves. Their moment vectors are
identical halves of the global vector. With eight parts, the windows
599 through 1133 and 3279 through 3813 each prove at least two survivors;
the other local lower bounds are zero. The actual counts in those two windows
are 13 each, checked independently after the proof calculation.

`evidence/partition-eight-4412.json` retains all eight moment vectors and
their independent checks. They sum exactly to the original global moments.
The comparison routine also calculates a global baseline; that extra work is
not included in the local-evaluation column above. No speed advantage is
claimed. The useful result is that location can strengthen the proof without
increasing its overlap degree.

Local intersections may become empty before the requested degree. All later
intersection sums are then provably zero and can be padded for comparison.
The implementation records this exact closure and rejects unsupported padding.
An initial version incorrectly rejected these valid short local sequences;
the targeted regression for N=1000 split into 100 windows now passes in normal
and optimized Python.

## An exact ambiguity exists at every fixed truncated degree

Fix d>=0 and put m=d+1. In one abstract exclusion system, create one candidate
for each even-cardinality subset of {1,...,m}; in another, use every odd-cardinality
subset. Event E_r contains a candidate exactly when its subset includes r.

Both universes contain 2^d candidates. For every specified set J of j<=d
event names, both have exactly 2^(d-j) candidates in the intersection of
those events: at least one of the m-j remaining membership choices is free,
so half of the completions have either parity. Thus the systems share even
all the individually named intersections through degree d, not just their sums.
Their aggregate moments are

    S_j = binomial(d+1,j) * 2^(d-j),  0<=j<=d.

Yet the even-subset system includes the empty subset and has one survivor;
the odd-subset system has none. Their multiplicity cap is K=d+1. Scaling
both systems by a common positive integer preserves the ambiguity.

This proves that truncated exclusion information does not, in general,
determine survivor existence. It does not establish that prime-divisibility
events can realize the abstract alternatives. Interval location, reflection,
prime-square thresholds, and other arithmetic conditions can supply extra
information. When d>=K, exact inclusion-exclusion already recovers the survivor
count, so the countermodel does not apply. This elementary construction should
not be described as a proof of the full classical sieve parity barrier.

Both general statements were independently reconstructed by the bounded Sol
reviewer. The next route changes the information entering the overlap stages:
first sieve through a growing cube-root threshold, then use the constrained
factorization types of the remaining candidates.

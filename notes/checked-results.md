# Checked results and live hypotheses

Owner/purpose: Kevin's overnight Goldbach investigation. This is the canonical
mathematical notebook; scripts and compact receipts support reproducibility.
All new results here are **new-to-this-task**, not claims of historical novelty.

## 1. A chosen pair has no universal bounded repair radius

Status: **proved using established CRT and Dirichlet's theorem**, independently
reconstructed by the bounded Sol reviewer `finite_radius_review`, then checked
by Rill. This limits one proposal; it does not refute Goldbach or all induction.

For every integer K >= 0, infinitely many unordered odd-prime pairs {P,7}
admit no redistribution `(p+2k,q+2-2k)` with `|k|<=K`, in either orientation.

Proof: Let `T={-K,...,K+1}\{0}`. For each t in T choose a distinct prime
`l_t>2(K+1)`. CRT gives a class a modulo `M=product(l_t)` satisfying
`a=-2t (mod l_t)` for all t. Since `0<|2t|<l_t`, each residue is nonzero;
therefore `gcd(a,M)=1`. Dirichlet's theorem supplies arbitrarily large prime
representatives P. Choose `P-2K>max(l_t)`. Each `P+2t`, t in T, has the proper
divisor l_t and is composite.

For orientation (P,7), k=0 makes the second target 9; every k!=0 makes the
first target composite. For (7,P), k=1 makes the first target 9; otherwise
`t=1-k` belongs to T and makes the second target composite. This exhausts
the permitted k, including K=0. No prime-tuples conjecture or Goldbach
assumption occurs in this argument.

Established dependency: Andrew Sutherland, MIT 18.785, Lecture 18, Theorem
18.1 (2021), [Dirichlet's theorem](https://math.mit.edu/classes/18.785/2021fa/LectureNotes18.pdf).
Reviewer also located [Dirichlet's original 1837 paper](https://www.e-rara.ch/download/pdf/5688045.pdf).

The negated assertion is `exists K, for all chosen prime pairs, exists a repair`.
It does **not** negate `exists K, for all N, some representation has a repair`.
Example: the pair (7,23) for 30 has no |k|<=1 repair; the different pair
(13,17) repairs immediately to (13,19) for 32.

Retained mechanism: adaptive selection among multiple starting pairs, or a
radius that grows with N. Reactivation trigger for bounded chosen-pair repair:
only a materially restricted family with a stated condition excluding the
construction above. Do not retest an unrestricted constant radius.

## 2. Radius conventions and a bijection

For fixed p+q=N with odd primes, every ordered prime representation r+s=N+2
corresponds to exactly one integer `k=(r-p)/2`; conversely each successful k
gives such a representation. This is algebra, not an existence proof.

Initial experiment used cost `|k|`, which depends on orientation. For further
experiments use the symmetric cost `B=max(|k|,|1-k|)`; each coordinate changes
by at most 2B. Allowed k are `1-B,...,B`, and swapping the pair sends k to
`1-k`, preserving B. B=1 means direct +2; B=2 allows also (-2,+4) and
(+4,-2). Keep the initial raw result labeled asymmetric.

## 3. Exact finite observations

`python redistribution.py check` independently compares the sieve with trial
division on 10,001 integers and checks nearest-shift minimization against
exhaustive target enumeration through N=500 in both metrics.

The initial asymmetric scan through N=20,000 checks 1,437,830 starting pairs.
Its largest recorded |k| is 148 at (8467,8539), moving to (8171,8837).
Selecting the best starting pair at each N instead needs at most |k|=2 over
that finite range. See `evidence/scan-20000-asymmetric.json`.

Concrete CRT witnesses for K=1,2,4,8,12,16 are saved in
`evidence/crt-witnesses.json`. The largest chosen pair is
`(7,18304487399189)`. Its larger member was checked by exhaustive trial
division through 4,278,374; every permitted shift has an explicit obstruction.
These finite certificates use orientation (7,q). The general theorem above
separately handles both orientations.

A symmetric-displacement-4 scan found an edge between some representations
of each N and N+2 for every even N=6,...,10,000,000. This is a computational
observation, not a theorem. A universal assertion would also imply infinitely
many twin primes, so it has not reduced the unproved burden. See the exact
quantifier argument in `review-receipts.md`.

## 4. Stacked blocks of 1,000 even integers

Kevin's steering at about 03:34 UTC: let a first formula handle 1,000 at a
time, feed its output to the next, and stack the stages. Implemented stages:

1. An exact prime sieve produces prime/composite data with an explicit bound.
2. A block stage covers 1,000 consecutive evens with verified prime-pair
   witnesses. Candidate small primes each cover a bit mask of positions.
3. The next stage combines disjoint adjacent block certificates, preserving
   exact endpoints and checking no number is omitted.
4. Investigate the missing universal interface condition: why must each next
   block's union of prime-pair masks cover all 1,000 positions?

The finite stages can be fully verified and efficient. An unbounded loop of
finite checks is not an infinite proof. A uniform lower bound, invariant, or
inductive coverage condition would be the mathematical contribution needed.

The completed stack certified all1,000,000 evens from4 to2,000,002, using
193,669 AP-sum certificates across1,000 blocks. Independent prime-input
verification used a monolithic sieve; generation used segmented sieving.
The558.953-second run is a finite composition demonstration, not a new bound.

Carry-forward reuse settled56 of10,000 targets in ten adjacent blocks starting
at1,000,000. No entire realistic sample block skipped new generation, although
a constructed valid certificate tests that full-carry path. Measured cover
times were3.858 seconds fresh and4.189 seconds with carry validation included.

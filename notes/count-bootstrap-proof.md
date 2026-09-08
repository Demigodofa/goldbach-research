# Exact counts can generate the next stage without a fresh prime oracle

Owner: Kevin's Goldbach investigation. Purpose: make the requested output-fed
stages mathematically explicit and executable. This composes formal series
inversion with the elementary least-factor sieve; it is not a new prime
formula claim or a proof of Goldbach positivity.

## Three steps and their input contract

Suppose the actual ordered Goldbach counts G(6),G(8),...,G(B) are available,
where B>=6 is even. The separate count G(4)=1 is not part of this prefix.

1. Invert the count polynomial prefix, as proved in
   `smaller-input-count-recurrence.md`, to recover the prime flags for all
   odd integers 3..B-3. The exact numeric counts are required; success/failure
   flags cannot replace them. The prime 2 is a known base fact.
2. Sieve the new argument interval using only those recovered primes and2.
3. Square the resulting odd-prime polynomial to obtain the new ordered-count
   prefix. Carry-free packed multiplication is one exact implementation.

The input counts must already be proved correct. Formal binary consistency
alone is insufficient: a toy nonprime sequence can also have a square.
Canonical replay begins with G(6)=1 from3+3, rather than accepting an
unverified external prefix as evidence.

## A proved expansion limit

Any unknown odd prime is at least B-1. If an integer x<(B-1)^2 is composite,
its least prime factor is at most sqrt(x)<B-1. Thus that factor is2 or one
of the recovered odd primes <=B-3. Sieving with just this list classifies
every such x exactly.

For even target T, its largest odd argument is T-3. Therefore every count
through the even endpoint

    T_max = (B-1)^2+1

can be generated, because T_max-3=(B-1)^2-2 is below the unsafe square.
This is a sufficient uniform endpoint; a specific prime list might permit
a larger extension, but no such improvement is needed here.

The first possible full expansions are

    6 -> 26 -> 626 -> 390626 -> ... .

Only the prior prefix needed to recover odd primes through
floor(sqrt(T-3)) has to be inverted for a particular next endpoint T.

For B>=626, B+2000 <= (B-1)^2+1. Consequently the pipeline can add exactly
1,000 new even targets on every subsequent stage, indefinitely as a
mathematical algorithm. This does not assert that physically executing all
stages is possible.

## Executed chain and verification

`count_bootstrap.py` starts at the canonical base and implements these three
steps. Production code uses only recovered divisors and2 for local composite
marking; the standard prime sieve is not called. Each stage records its
input-count hash, exact recovered-divisor range, output-count hash and
collective positivity result. Counts are decoded from byte-aligned digits.
An extension explicitly checks that its recomputed earlier prefix agrees
with the input prefix. Compact receipts omit the bulk count list and must
pass `replay_receipt` from the canonical base before external acceptance.

`evidence/count-bootstrap-stages.json` records the executed endpoints
6 -> 26 -> 626 -> 2626 -> 4626 -> 6626. Every one of the3,311 counts through
6626 matched direct ordered pair counts using independent exact trial-prime
flags. The compact receipt also passed a fresh canonical replay.

| Newly generated interval | Number of even targets | Minimum ordered count |
|---|---:|---:|
| 628..2626 | 1,000 | 20 |
| 2628..4626 | 1,000 | 56 |
| 4628..6626 | 1,000 | 100 |

These are finite results. The full mathematical jump from626 to390626 is
proved safe above but is not claimed as an executed measurement here.
Seven focused tests cover independent full counts, early endpoints requiring
no odd divisor inputs, exact safe-boundary rejection, malformed parameters,
full and compact receipt tampering, and a guard against calling the standard
sieve builder. They pass normally and with Python optimization enabled.

## What this does and does not establish

By induction, every finite stage computes actual Goldbach counts. The
endpoints grow without bound, so this defines a complete deterministic
generation procedure starting from the small base. It does not assume that
the later counts are positive: a zero count would still be a correct output.

Consequently the proved induction invariant is exactness of the generated
counts. The missing Goldbach induction invariant is strict positivity of
every newly generated count. A proof of the former is not a proof of the
latter, even though both use the same stages.

The number of stages can be small while work and stored data grow greatly.
No fixed-work, polynomial-in-bit-length, or speed advantage is claimed.
The procedure establishes Kevin's requested dependence on earlier outputs,
not an escape from computing a finite amount of new arithmetic each stage.
The same recovered prime list could also seed an ordinary incremental sieve;
passing through Goldbach counts is a valid reconstruction path rather than
a new source of prime information or a reason for positivity.

# An exact three-stage prime-pair count

Owner/purpose: Kevin's proposal to combine small calculations into a formula.
Status: the identity below is proved for every even N; its positivity for
every N remains unproved. The implementation computes finite instances.
This is a new-to-this-task use of standard sieve and inclusion-exclusion ideas,
not a claim of a new Goldbach theorem.

## The three stages

For even N>=6, consider the ordered odd candidates

    A = {3,5,...,N-3}, H=N-3, z=floor(cuberoot(H)).

For each odd prime r<=sqrt(H), define the composite-detection event

    E_r = {a in A : (r divides a and a>=r^2)
                    or (r divides N-a and N-a>=r^2)}.

The square threshold matters: the prime r itself is never removed, but any
composite is detected by its least prime factor. These are different events
from raw divisibility classes used in the earlier prime-safe-window method.

1. Remove all E_r with r<=z. Retain the actual surviving set A_0, with M=|A_0|.
2. For residual primes z<r<=sqrt(H), calculate
   `S_1=sum_r |E_r intersect A_0|` and
   `S_2=sum_{r<s} |E_r intersect E_s intersect A_0|`.
3. The exact number of ordered prime representations is

       G(N) = M-S_1+S_2.

For N=4, use the separate exact base G(4)=1 from2+2.
Only the first two overlap degrees are needed after the first stage, even
though the number of sieving primes grows with N.

## Why all triple intersections vanish

Any composite argument x<=H that survives stage1 has every prime factor >z.
If it had three prime factors counted with multiplicity, then

    x >= (z+1)^3 > H,

a contradiction. Thus each surviving argument is either prime or a semiprime
pq with p<=q and both factors>z. Its least factor p detects it because
pq>=p^2. If q>p, then pq<q^2, so event E_q does not detect it. A square p^2
still meets only E_p. A prime argument meets no residual event.

Each candidate therefore belongs to at most two distinct residual events,
one contributed by each argument. If both composite arguments have the same
least factor, they contribute a single event, as the union definition requires.
Every triple residual intersection inside A_0 is empty, so inclusion-exclusion
terminates exactly after S_2. The complement contains precisely prime pairs.

This proof handles the small cases where z<2, prime squares, repeated factors,
and the diagonal pair a=N/2. Unequal pairs contribute twice to G; an equal-prime
pair contributes once. The Sol reviewer independently checked the theorem and
these boundaries. The cube-root cutoff is computed with exact integer arithmetic.

## The information passed forward is not only M

Stage2 needs A_0's surviving positions to calculate its intersections. Two sets
of the same size can produce different S_1 and S_2. The implementation retains
A_0 as a bit mask, masks each residual event against it, and counts intersections
exactly. The compact trace M,S_1,S_2 can be independently reconstructed from N
and the prime cutoffs; arbitrary supplied values are not a proof.

The fixed number of stages does not imply fixed work or fixed information.
Stage1 absorbs a growing collection of exclusions. Goldbach still requires

    M(N)-S_1(N)+S_2(N) > 0  for every even N>=6.

The simpler sufficient condition M>S_1 is also not proved universally.

## Measured examples

All results below were independently matched to a separate prime sieve.
These use the complete candidate range, unlike earlier restricted windows.

| N | Cube-root cutoff z | Original odd candidates | M after first stage | S_1 | S_2 | Exact ordered pairs |
|---:|---:|---:|---:|---:|---:|---:|
| 554 | 8 | 275 | 43 | 22 | 0 | 21 |
| 1,000 | 9 | 498 | 98 | 46 | 4 | 56 |
| 4,412 | 16 | 2,204 | 220 | 142 | 12 | 90 |
| 10,000 | 21 | 4,998 | 524 | 304 | 34 | 254 |
| 100,000 | 46 | 49,998 | 3,574 | 2,290 | 336 | 1,620 |
| 1,000,000 | 99 | 499,998 | 25,686 | 18,098 | 3,216 | 10,804 |

For 4,412 the full count is90, while the earlier candidate window63 through4349
contained88. The scopes differ; the new count includes the previously omitted
small-summand representations. For1,000,000 the first stage eliminates474,312
known composite candidate positions. This describes a rigorous elimination,
not a measured speed advantage over a tuned Goldbach implementation.

The block4 through2002 (1,000 evens) matches the independent sieve in every
case. All1,000 also have positive raw union lower bound M-S_1. That finite
observation supplies no unbounded positivity estimate. Receipts are
`evidence/cubic-sieve-1000.json` and `evidence/cubic-sieve-examples.json`.

Six focused tests compare direct trial-prime counts through2000, exercise
cube-root boundaries, independently verify residual multiplicity<=2, preserve
prime arguments, and test a common least factor. They pass in normal and
optimized Python.

## Classical predecessor and remaining work

The cube-root cutoff has a classical precedent: Lagarias, Miller, and Odlyzko's
[Meissel-Lehmer treatment, Section2, PDF pp.7-8]
(https://www-users.cse.umn.edu/~odlyzko/doc/arch/meissel.lehmer.pdf)
decomposes a partial sieve into counts by the number of prime factors. With
the sieve taken through the cube root, terms with three or more prime factors
vanish. Their problem is counting individual primes. The reflected-pair
identity above applies that elementary factorization restriction to two
arguments and uses square-start events to obtain multiplicity at most two.
We do not transfer their computational complexity bounds to this implementation.

The next bounded search completed all8,999 evens from2004 through20,000 with
no nonpositive raw union margin. Combined with the first block, this checks
M-S_1>0 for every even4 through20,000. The smallest relative margin in the
new range occurs at4856: M=250,S_1=168, so the raw lower bound is82;
S_2=24 gives the full count106. This finite search took27.687 seconds and is
retained in `evidence/cubic-union-bound-scan-20000.json`.

The next research task is the missing uniform inequality, not a longer finite
verification record. Derive certified count/error bounds for the first-stage
survivors and residual single exclusions, beginning with a central window
where all small-prime square thresholds are already satisfied. Determine
whether those bounds retain enough margin to prove positivity. Do not replace
this step by an independence assumption or a favorable average density.

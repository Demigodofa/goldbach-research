# Use prime gaps to attack restricted-search rules

Owner: Kevin's Goldbach investigation. Purpose: follow the request to select
disproof candidates mathematically, starting with statements that can be
falsified independently of the full Goldbach conjecture.

## An interval of guaranteed palette misses

Let q<r be consecutive odd primes and let K>0. For every even target N with

    q+K<N<r,

no prime p<=K can appear in a Goldbach representation. Otherwise the prime
complement N-p would satisfy

    q<N-p<r,

contradicting the absence of a prime in that gap. Thus a proved prime gap
certifies an entire interval of failures for the restricted palette.

At the endpoint N=r-1, every addend in any prime pair must be at least

    N-q=r-q-1.

This is a necessary lower bound on the addends, not a claim that the bound
itself is prime or that a pair necessarily exists.

## Explicit checked fixture

The primes492113 and492227 are consecutive, with gap114. The retained
fixture `evidence/prime-gap-palette-stress.json` contains a proper divisor
for each of the56 odd integers between them; every intervening even integer
is composite by2. Both endpoints were independently checked by trial
division, and a full sieve independently confirmed the gap.

For cap K=100 the whole interval492214..492226, seven even targets, is a
guaranteed palette miss. Independent prime-pair searches give:

| Even target | Least prime addend | Complement |
|---:|---:|---:|
| 492214 | 101 | 492113 |
| 492216 | 103 | 492113 |
| 492218 | 151 | 492067 |
| 492220 | 107 | 492113 |
| 492222 | 109 | 492113 |
| 492224 | 157 | 492067 |
| 492226 | 113 | 492113 |

The final target therefore has minimum addend exactly113. It also defeats
the proposed cutoff8*log(N), with natural logarithm. This can be checked
without trusting a rounded logarithm: N<(8/3)^14 and e>8/3, so log(N)<14,
giving8*log(N)<112<113. The receipt retains the exact rational comparison.

The relative packed certifier independently returns all seven cap-100
misses, and its receipt passes fresh replay. These are counterexamples to
the restricted rule; the displayed pairs show that none is a Goldbach
counterexample.

## Every fixed constant times log(N) is insufficient

[Maynard, Large gaps between primes, Theorem1]
(https://annals.math.princeton.edu/2016/183-3/p03) proves an unconditional
prime-gap result stronger than the consequence needed here:

    limsup_(consecutive primes q<r) (r-q)/log(q) = infinity.

For example Bertrand's bound r<2q gives
log(r-1)<=log(q)+log(2), so the unbounded ratio also supplies infinitely
many gaps with

    r-q-1 > C*log(r-1)

for any fixed constant C>0. At N=r-1, the endpoint lemma forces every
possible Goldbach addend above C*log(N).

Therefore a prime palette capped at any fixed C*log(N) cannot be a universal
positive-certificate method. This statement is unconditional and does not
assume that Goldbach holds at the selected targets. If a representation
exists there, it necessarily uses larger primes. No practical threshold for
each C is claimed, and the result does not rule out faster-growing caps.

The independent Sol review confirmed the gap lemma, its whole-interval
version, the finite example, and the logarithmic-cutoff consequence. The
prime-gap theorem supplies an input to this argument; the palette consequence
is the task's direct deduction from that input.

## Research decision

Prime-gap tails are a justified stress family for small-addend stages.
Palette failure and low total Goldbach counts are different properties; a
target can have many representations using larger primes. Do not label a
palette miss a Goldbach candidate without an independent full check.

Proved statements can compose to cover infinitely many inputs; finite
successful computations alone cannot do so. The complementary research
strategy is to state a candidate rule precisely, construct inputs that
stress its premise, and either produce an actual counterexample or identify
the next unproved statement. Exhausting an ever-larger numerical range is
not an infinite proof and is not the default next experiment.

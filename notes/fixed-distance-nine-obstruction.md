# A fixed nearby-prime distance does not bound the required addend

Owner: Kevin's Goldbach investigation. Purpose: test whether a locally short
distance to a prime can supply the missing search-range guarantee. The
construction and deduction are new-to-this-task combinations of classical
results; no claim of worldwide originality is made.

## Statement and exact meaning of distance

For even N>4 define d(N)=N-prevprime(N), where prevprime is the largest prime
strictly below N. Among Goldbach-representable N, let m(N) be the least prime
that can occur as an addend.

For every fixed finite K, there are infinitely many Goldbach-representable
even N satisfying

    d(N)=9,   m(N)>K.

Consequently there is no finite-valued function F of d alone that guarantees
m(N)<=F(d(N)), even when its domain is restricted to representable targets.
The distance d is not the complete gap between two consecutive primes. This
argument fixes the preceding endpoint's distance to N, not the next prime's
location.

If d(N) itself is prime, prevprime(N)+d(N) already provides a representation.
The fixed composite value9 avoids that immediate certificate.

## First component: impose all required composite offsets

Fix K>=3 and let

    H={2,4,6,8} union {9-p: p<=K is an odd prime}.

Every h in H is nonzero and even. In particular9-p cannot be zero because9
is composite. For each distinct h choose a distinct odd prime ell_h that
does not divide h. Impose

    q=1 mod2,   q=-h mod ell_h.

CRT gives one residue a modulo M=2*product ell_h. Its residue is coprime to
M: it is odd, and is nonzero modulo every ell_h. Thus Dirichlet's theorem
supplies infinitely many prime q in that progression.

Choose q>K and large enough that q+h>ell_h for every h. Every q+h is then a
proper composite multiple of its assigned divisor. Put N=q+9. The four odd
integers q+2,q+4,q+6,q+8 are composite; the other integers between q and N
are even and greater than2. Therefore prevprime(N)=q and d(N)=9.

For each odd prime p<=K the complement N-p=q+(9-p) is composite. The p=2
complement is also even and greater than2. Hence no pair at N uses an addend
at most K. This component alone establishes infinitely many palette misses.
It does not, by itself, show that those particular N are representable.

## Second and third components: guarantee infinitely many are representable

The [prime number theorem for arithmetic progressions in NIST DLMF27.11]
(https://dlmf.nist.gov/27.11) states, for a fixed reduced class a mod M,

    pi(X;M,a) ~ X/(phi(M)*log X).

Thus the constructed N=q+9 in [X,2X] number

    A_K(X) ~ X/(phi(M)*log X).

The original [Montgomery-Vaughan exceptional-set paper, Acta Arithmetica27
(1975),353-370](https://doi.org/10.4064/aa-27-1-353-370) gives a fixed positive
delta with E(Y)<<Y^(1-delta), where E counts even Goldbach exceptions. The
statement is also given in [Pintz's primary author account, introduction
equation1.6](https://arxiv.org/pdf/1804.09084). That account was read; the
original publisher's bibliographic record was verified, while its PDF
download returned403 in the root's web tool. No effective numerical
threshold or value of delta is used here.

The needed consequence is just

    E(2X)=o(X/log X),

because log(X)/X^delta tends to zero. For fixed K, the modulus M is fixed,
so E(2X)=o(A_K(X)). For all sufficiently large X the constructed family
contains more members than the total possible Goldbach exceptions. At least
one member in each such disjoint dyadic interval is therefore representable.
In fact the fraction of this constructed family that is exceptional tends
to zero. This proves the statement.

The order of quantifiers is essential: first fix K and M, then let X grow.
This argument does not provide a bound for a palette K(X) or modulus M(X)
that grows with the target. The asymptotic argument also does not identify
which individual members are representable; finite witnesses below do that
separately.

## Explicit finite witnesses

`distance_nine_stress.py` constructs the CRT data, performs an explicitly
bounded exact prime search, and verifies the proper composite divisors and
any supplied Goldbach pair. The progression must be reconstructed exactly
before a supplied witness is accepted. A search limit is inconclusive.

`evidence/distance-nine-crt-witnesses.json` records:

| Blocked cap K | Prime q | Even N=q+9 | Actual minimum addend | Complement prime |
|---:|---:|---:|---:|---:|
| 17 | 4,304,309 | 4,304,318 | 127 | 4,304,191 |
| 29 | 1,420,043,879,999 | 1,420,043,880,008 | 277 | 1,420,043,879,731 |

For K=17 the reduced progression is q=4,304,309 modulo9,699,690; its first
admissible candidate is prime. For K=29 the progression is q=16,120,449,089
modulo200,560,490,130; the eighth tested candidate is the displayed prime.
All claimed prime inputs were checked by exact trial division. The receipt
also includes a proper divisor of the complement for every smaller prime
addend, proving that the displayed addends are actual minima.

Four focused tests exercise the complete offset set and reduced residue,
the explicit smaller witness, bounded-search outcomes, and rejection of
forged patterns, invalid prime inputs, and invalid pairs.

## Review and resulting direction

Independent Sol review confirmed the CRT construction. It first correctly
flagged that CRT plus Dirichlet alone does not guarantee representability.
The root supplied the density comparison, and the review confirmed that
the progression count dominates the exceptional-set bound for fixed K.
The source lane located the original exceptional-set paper and the fixed
progression hypothesis. The representability claim uses all three pieces.

This is a concrete example of proof composition across infinitely many
inputs. It rules out a proposed predictor; it does not establish Goldbach
for every target, or rule out a method using more information than d(N).
The next candidate rule must retain additional arithmetic structure, rather
than treating the nearest-prime distance as a sufficient search bound.

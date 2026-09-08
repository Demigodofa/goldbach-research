# A maximum-gap calculation that removes an entire target interval

Owner/purpose: Kevin's requested calculation Z. This is a finite proved
certificate mechanism, new-to-this-task. It is not a universal Goldbach proof.

## Definitions and interval theorem

Let p be a prime, q the next prime, and W the product of every prime through p.
For each even residue t modulo W define the periodic survivor set

    C_t = {a in Z : gcd(a,W)=gcd(t-a,W)=1}.

Let J be an upper bound for every cyclic gap between consecutive survivors,
over all these even residues. Then every interval of J consecutive integers
contains a survivor, for every even t. Such survivors always exist somewhere:
modulo each odd prime r, at most two residues are forbidden; modulo2 only one
is forbidden. CRT combines an allowed residue at every prime. This proves
periodic nonemptiness, but gives no sufficiently short gap bound by itself.

**Prime-safe window.** Every integer in [L,U]=[p+1,q^2-1] coprime to W is
prime. Otherwise its least prime divisor is at most its square root, strictly
less than q, and therefore is one of the factors of W, a contradiction.

**Interval theorem.** If J<=U-L+1, every even N in

    2L+J-1 <= N <= 2U-J+1

is a sum of two primes. Round the lower endpoint upward and upper endpoint
downward to even integers. Equivalently, the unrounded bounds are

    2p+J+1 <= N <= 2q^2-J-1.

Proof: the candidates a for which both a and N-a lie in [L,U] form the
integer interval

    [max(L,N-U), min(U,N-L)].

Its number of integer positions is at least J precisely throughout the
displayed range (under J<=U-L+1). The gap bound supplies a survivor a there.
Both a and N-a are coprime to W and in the prime-safe window, hence prime.
No Goldbach decomposition for a particular N was used in deriving the interval.

## Exact finite calculation

`paired_wheel.py` represents the units modulo W by a bit set A. Negation
preserves A, so C_t is the bitwise intersection of A with its circular shift
by t. The maximum cyclic gap is one more than the longest zero run. Intersection
doubling finds those runs in two periods. Every even target residue is examined;
there is no random sampling or assumed distribution of primes.

The generic cyclic algorithm matched independent point enumeration on all8,178
nonempty bit sets of widths1 through12. Reflected survivor sets matched direct
gcd enumeration for124 even-residue patterns in wheels2,6,30,210. A separate
sieve confirmed343 target instances in the resulting six intervals. The latter
is an implementation check, not the basis of the interval proof.

| Last wheel prime p | Wheel W | Exact maximum gap J | Certified even targets |
|---:|---:|---:|---|
| 2 | 2 | 2 | 8 through14 |
| 3 | 6 | 6 | 14 through42 |
| 5 | 30 | 18 | 30 through78 |
| 7 | 210 | 30 | 46 through210 |
| 11 | 2,310 | 66 | 90 through270 |
| 13 | 30,030 | 150 | 178 through426 |

Their union is every even from8 through426. Together with4=2+2 and6=3+3,
they cover all evens4 through426. This is a small demonstration of a gap-based
Z, not a new computational verification record or a speed advantage.
The last wheel alone certifies125 consecutive evens. Its15,015 target-residue
patterns concern a modular surrogate, rather than separately searching those
125 targets for prime pairs. The surrogate can cost more than direct checking.

## Primary-source relationship and exact unresolved condition

Ziller and Morack define the paired Jacobsthal function as the worst gap over
all phases of two same-direction progressions. Reflection is encoded by
negating one Goldbach summand. Their proposed bound
`h_2(k)<p_k^2-p_k` for every k>=3 would imply both Goldbach and infinitely many
prime pairs of each fixed even difference. That bound is Conjecture6, not a
proved theorem. See [definitions and Proposition3.2, pp.3-5; Conjecture6, p.8]
(https://arxiv.org/pdf/1706.00317).

Their [computation note, Table1, p.3](https://arxiv.org/pdf/1706.03668) reports
finite values through the21st prime73. Our independently computed first six
values match its2,6,18,30,66,150. We have not independently verified the larger
reported values and do not infer the unbounded conjecture from them.

The interval theorem above exposes a concrete stacking interface. For adjacent
wheel primes p_k,p_(k+1), and even gap bounds J_k,J_(k+1), the certified even
intervals meet or are adjacent provided

    J_k + J_(k+1) + 2*p_(k+1) + 2 <= 2*p_(k+1)^2.

This condition is sufficient for those two interval outputs to compose. It
does not follow merely from CRT nonemptiness. Proving suitable bounds for all
future wheels remains unresolved; computing a few more wheels cannot fill
that logical gap. A target-anchored bound may avoid the stronger all-phase
requirement, but it needs its own noncircular estimate.

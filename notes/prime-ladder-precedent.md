# Published precedent for stacked interval certificates

Purpose: test Kevin's proposed range-elimination mechanism against a proof
method that actually scaled, and identify its exact transfer boundary.
Source triage: bounded Terra lane `prime_ladder_sources`; formulas checked by Rill.

## The transfer

Assume binary Goldbach has been verified for every even E from4 through an
even bound B. For any certified odd prime p, every odd N in

    p+4 <= N <= p+B

is the sum of three primes: N-p is an even integer in the verified range,
so N-p=a+b, hence N=p+a+b. One prime rung therefore certifies an entire
odd interval, without individually checking the targets inside it.

Consecutive rungs p_i<p_(i+1) leave no missing odd target when

    p_(i+1)-p_i <= B-2.

Indeed, the next interval must start at most2 after the preceding interval
ends. A rung gap equal to B would leave exactly one uncovered odd target.

## What the published calculation did

Helfgott and Platt combined a binary range through `4*10^18` with certified
prime ladders to establish the ternary statement up to

    8,875,694,145,621,773,516,800,000,000,000.

They allowed rung gaps from4 through B and separately handled the endpoint
case B+2. Helfgott's later exposition supplies

    4,000,000,000,000,000,002
      = 2,000,000,000,000,001,301
      + 1,999,999,999,999,998,701.

For an odd n choose the greatest rung p<n. If n-p>=4, the bounded rung gap
places it in the verified binary interval. If n-p=2, use the preceding
rung p'; then n-p' lies between6 and B+2. The displayed additional binary
partition handles the only new endpoint. Boundary coverage at the start/end
of the full ladder must also be checked in an actual implementation.

Primary sources:

- H. A. Helfgott and D. J. Platt, *Numerical Verification of the Ternary
  Goldbach Conjecture up to 8.875*10^30* (2013), pp.1,3, Theorem4.1:
  https://arxiv.org/pdf/1305.3062
- H. A. Helfgott, *The ternary Goldbach problem* (2015), pp.37-38, the
  prime-ladder exposition and B+2 endpoint repair:
  https://arxiv.org/pdf/1501.05438
- T. Oliveira e Silva, S. Herzog, S. Pardi, *Empirical Verification of the
  Even Goldbach Conjecture and Computation of Prime Gaps up to 4*10^18*,
  Mathematics of Computation83 (2014), pp.2034,2039,2041; Algorithms1.3-1.4:
  https://www.ams.org/mcom/2014-83-288/S0025-5718-2013-02787-1/S0025-5718-2013-02787-1.pdf

The binary paper's block algorithms sieve a slightly enlarged prime interval,
mark target sums, and send rare unmarked targets to a single-number search.
Its computational segments are efficient exhaustive verification, not a rule
that derives an arbitrary distant binary interval from an earlier one.

## Boundary for the current goal

The ladder transfer really does skip vast ranges using a proved interface.
It adds a third prime and changes parity. It therefore does not establish
binary Goldbach. A binary transfer must preserve exactly two summands while
guaranteeing primality after changing the target; a nearby prime alone does
not guarantee that its reflected partner N-p is prime.

Retained component: explicit interval endpoints, maximum allowed gap, and
separate endpoint repairs. These apply to our AP-sum and block certificates.
Unresolved component: a uniform prime-input or coverage guarantee that keeps
the binary certificate pipeline successful for every future block.

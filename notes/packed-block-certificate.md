# An exact collective Z for a finite block

Owner: Kevin's Goldbach investigation. Purpose: implement the requested
small-stage calculation that certifies1,000 targets together and carries
computed output into the next stage. Retain the proof, executable replay,
and representative receipts. This is new-to-this-task use of classical
polynomial convolution and Kronecker substitution, with no novelty claim.

## Tiny example

Take the known primes3,5,7 and form P(x)=x+x^2+x^3. Then

    P(x)^2 = x^2 + 2x^3 + 3x^4 + 2x^5 + x^6.

Coefficient k counts ordered pairs summing to2(k+1). All five displayed
coefficients are positive, so all five evens6,8,10,12,14 are certified
together. The coefficient3 for10 represents3+7,5+5,7+3.

## Stage one: encode the finite prime inputs

For a computed bound Nmax>=6, generate the odd primes p<=Nmax-3. Let n be
their count. Choose B=2^w so that B/2>n, and form

    P(B) = sum_(odd prime p<=Nmax-3) B^((p-1)/2).

The implementation uses a deterministic sieve for these prime inputs. It
reserves byte-aligned digit width using an upper bound on the number of odd
candidates through a declared finite capacity. It does not claim that future
primes can be predicted from the previous prime list.

## Stage two: one square computes many pair counts

Compute C=P(B)^2. Algebra gives C=sum c_k B^k, where

    c_k = #{ordered encoded prime pairs (p,q): p+q=2(k+1)}.

For each p there is at most one corresponding q, so c_k<=n<B/2. No base-B
carry occurs. Every c_k is an actual digit of the integer C. For targets up
to Nmax, all possible odd summands are within the prime input cutoff, so
these are full ordered Goldbach counts. N=4 is separate as2+2.

For m consecutive even targets starting at N0, put k0=N0/2-1 and extract

    A = (C >> (w*k0)) & (B^m-1).

This extracts their m count digits at once. Here >> and & denote exact
integer shift and bitwise AND.

## Stage three: test all counts for zero together

Put h=B/2 and define

    L = (B^m-1)/(B-1),
    H = h*L,
    Z = ((A | H)-L) & H.

L has digit1 in every position, H has digith, and every extracted count c
is belowh. Thus A|H has digith+c. Subtracting L makes each digit h+c-1
without any borrow between digits. Its h bit is set exactly when c>0.

Therefore

    Z=H  if and only if every target in the block has a prime pair.

The test does not separately inspect each target count or search for its
representation. If it fails, only the zero positions need to be listed.
The input bound c<h is essential and is checked by the mask routine. For
example c=h would invalidate this bit argument; the implementation rejects
such input rather than accepting a purported certificate.

## Stacking the next prime input

If D contains only newly added prime monomials, then

    Pnew=Pold+D,
    Cnew=Cold+2*Pold*D+D^2.

All objects must use the same sufficiently wide base. The implementation
chooses a finite capacity in advance and rejects an extension beyond it.
Extending further requires rebuilding with an adequate width. For efficient
representation of D, its first nonzero-possible exponent is factored into a
digit shift, leaving a shorter polynomial to multiply.

New odd prime inputs begin at least at Nold-1. Their sums with any odd prime
are at least Nold+2, so earlier target counts remain unchanged. The current
prime-discovery implementation uses a fresh sieve on extension; it reuses
the polynomial and its square, not the entire prime-discovery computation.

## Implementation and finite evidence

`packed_goldbach.py` provides build_prime_square, extend_prime_square,
certify_block, positive_digit_mask, and replay_certificate. Replay rebuilds
the finite prime inputs and square and compares the complete receipt,
including parameters, coverage, and the prime-polynomial hash. No assertion
is used as an acceptance gate.
PrimeSquare is internal builder state, not an authenticated external object.
The reviewer confirmed that a manually forged state can make certify_block
emit an apparent success. Therefore successful fresh replay is the acceptance
gate for an externally supplied receipt; a focused forgery test enforces this
boundary. All retained example receipts passed that gate.

`evidence/packed-square-blocks.json` records:

| Targets | Construction | Certified targets | Local construction and Z time |
|---|---|---:|---:|
| 6..2004 | Initial square | 1,000 | 0.000221s |
| 2006..4004 | Update from previous square | 1,000 | 0.000310s |
| 4006..6004 | Second update | 1,000 | 0.000433s |
| 1,000,000..1,001,998 | Separate larger square | 1,000 | 3.181758s |

Every receipt passed fresh replay. These are single-run descriptive times
including input construction/update and the collective check, excluding
fresh replay. They are not a comparative speed benchmark. The first three
blocks compose to all evens6 through6004;4 has its explicit base pair.

Seven focused tests exhaust1,792 small sentinel patterns, compare1,000 exact
coefficients against independent trial-prime pair counts, check incremental
equality against a fresh square, verify preservation of earlier counts,
reject tampered receipts, and exercise the digit and target input contracts.
The mathematical review independently confirmed the index convention,
coefficient bound, no-carry/no-borrow proof, and incremental identity.

## What has and has not been removed

After the exact finite test returns Z=H, that specified block needs no further
Goldbach check: the collective certificate covers every target in it. This
is the requested kind of calculation-based elimination.

The integer square still performs a finite convolution whose input and
arithmetic sizes grow with the computed bound. Bulk arithmetic does not make
that work disappear. Proving that Z=H for all future blocks without carrying
out each computation would still require a new uniform positivity argument.
The certificate does not supply that argument.

The standard packing principle is described in [Harvey, Faster polynomial
multiplication via multipoint Kronecker substitution, introduction]
(https://arxiv.org/pdf/0712.4046): a sufficiently large evaluation base allows
integer multiplication to preserve the polynomial coefficients without
overlap. Our finite Goldbach application uses the elementary single-product
version, not the paper's faster multipoint algorithms or performance claims.

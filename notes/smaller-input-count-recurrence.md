# What previous exact counts can carry into the next stage

Owner: Kevin's Goldbach investigation. Purpose: determine whether the cubic
formula's residual terms can use smaller, previously computed results.
This is a proved algebraic reduction with a checked finite reconstruction
implementation. The full residual-count recurrence has not been implemented.

## Corrected information boundary

An initial review said that ordinary Goldbach totals do not determine the
weighted correlations required below. That is too strong when the entire
exact earlier count sequence is retained. The root identified a formal
square-root inversion, and independent review confirmed the correction.

Let a_k be1 when2k+1 is prime, otherwise0, and let

    P(x)=sum_(k>=1) a_k*x^k,   a_1=1,
    P(x)^2=sum_n c_n*x^n,     c_n=G_odd(2n+2).

For k>=2,

    c_(k+1)=2*a_k + sum_(i=2 to k-1) a_i*a_(k+1-i),
    a_k=(c_(k+1)-sum_(i=2 to k-1) a_i*a_(k+1-i))/2.

Thus full exact ordered counts for all even targets6 through X+3 recover
the prime indicators through any odd X. The known leading coefficient a_1=1
selects the unique formal square root. For example G(8)=2 recovers primality
of5; G(10)=3 together with that result recovers7; G(12)=2 recovers that9 is
composite.

One scalar G(M), or just the success/failure flags of prior certificates,
does not contain this exact coefficient sequence. The full sequence does.
Reconstructing it is an exact computation, not a free information shortcut.

## Residual intersections as smaller prime-input problems

Use H=N-3, z=floor(cuberoot(H)), and the cubic sieve's square-start events
after its small-prime presieve. For residual primes z<r<s<=sqrt(H), put

    H_rs(N)=#{primes u>=r, v>=s: r*u+s*v=N}.

Every surviving composite is semiprime and belongs only to its least-factor
event. Therefore an E_r and E_s intersection must use different arguments.
Reflection gives two distinct orientations, so

    |E_r intersect E_s|=2*H_rs(N),
    S2=2*sum_(r<s) H_rs(N).

The orientations cannot coincide: r*u=s*v would force u=s and v=r, contrary
to v>=s>r. Prime squares are included correctly by the non-strict cofactor
lower bounds. Equivalently H_rs counts primes u in

    r<=u<=(N-s^2)/r,  u congruent N*r^(-1) mod s,

whose quotient (N-r*u)/s is a prime at least s. This displays the residue
information required by a direct computation.

For a common least factor r, the two coordinate arms of one event overlap in

    D_r = 1_(r divides N) * #{ordered primes u,v>=r: u+v=N/r}.

This overlap belongs inside the single-event union, not S2. If M=N/r>=2r,
its count is

    D_r=G_odd(M)-2*#{primes u<r: M-u prime}.

If M<2r it is zero. Let R_z(y) denote survival of the small-prime
square-start sieve and define

    A_r=#{primes u>=r: r*u<=H and R_z(N-r*u)}.

Then the first residual moment is

    S1=sum_r (2*A_r-D_r).

## Size reduction and remaining gap

If residual primes exist, let r0 be the smallest and let X be the largest
odd integer at most H/r0. Every residual cofactor is at most X, and

    X < H^(2/3),   X+3<N.

The exact earlier sequence through X+3 therefore recovers every prime flag
needed for the residual computations. It also covers the relevant smaller
prime divisors. Together with deterministic roughness tests it contains
enough information to compute the residual terms. Cases with no residual
primes simply have no such correction terms.

The full computation still includes the current rough survivor term M and
the expression G(N)=M-S1+S2. Exact earlier counts make these computations
possible; knowing only that the earlier counts are positive does not supply
a positive lower bound for this difference. The reduction therefore gives
smaller inputs for a finite computation, not an induction proving Goldbach.

The corrected route should retain exact count output when reconstruction
or weighted residual correlations are needed. It must not repeat the rejected
claim that an entire exact count prefix loses the prime-indicator information.

## Executable reconstruction and semantic limit

`count_reconstruction.py` implements recover_binary_flags and a formal
convolution-prefix helper. The decoder uses no primality oracle. It rejects
noninteger or negative counts, G(6) other than1, odd recovery numerators,
and recovered values outside{0,1}.

Five tests generate actual ordered counts for the1,000 evens6 through2004
by independent trial primality and recover the prime flags for odds3 through
2001 exactly. They also exercise malformed inputs and show two information
boundaries: distinct exact count prefixes can have the same positivity
booleans; a toy binary sequence marking9 as present can pass the algebra
without being a prime indicator sequence. Thus successful reconstruction
certifies binary square-root consistency. Its primality meaning requires
the premise that the supplied counts really are Goldbach counts.

# Adaptive normalization: an almost-all success theorem

Owner: Kevin's mathematical investigation; derivation: Rill. Purpose: test
whether adaptive precision removes the structural failure proved for fixed
dynamic ranges. Status: proof independently checked by Sol on 2026-09-08.
Novelty: new-to-this-task, not an assertion of historical priority.

## Statement

Fix a block length m>=1 and a positive integer d such that m<(2d+1)^2.
For a block of targets n_j=N+2j, 0<=j<m, set

    s(n)=product_{odd prime p|n}(p-1)/(p-2),
    C=2^b, where b is the smallest integer >=1 with C>=d*max_j s(n_j),
    w_j=ceil(C/s(n_j)),   x_j=w_j G(n_j),
    Z=(sum_j x_j)^2-(m-1)sum_j x_j^2.

Conclusion: for every fixed A>0, all but O_{m,d,A}(X/log^A X)
even block starts N in [X,2X] have Z>0 as X tends to infinity.
The constants and the starting threshold have not been made numerical.
This does not identify every exceptional start or prove their absence.

The rule is implemented by `adaptive_weight_bits`, followed by the existing
finite certificate generator with a common bit count for the whole block.
The theorem concerns a specific adaptive formula. It does not claim that
computing its input moments is faster or that the producer avoids exact G.

## Source input and conversion to unweighted counts

Use the checked prime-only logarithmic mean-square theorem in Vaughan,
*The Hardy-Littlewood Method*, 2nd edition, Theorem 3.7, printed p.36,
https://djvu.online/file/y04IjoKF754hT . See the precise normalization and
source boundary in `fixed-precision-weight-obstruction.md`.

Let kappa=2*product_{p>2}(1-1/(p-1)^2), and let R(n) sum log(p)log(q)
over ordered prime pairs p+q=n. Apply the theorem at 3X, with saving A+2.
Since s(n)>=1, each bad n contributes at least (kappa*X/log X)^2;
dividing the global bound O_A(X^3/log^(A+2) X) by that quantity shows
that all but O_A(X/log^A X) even n in [X,3X] satisfy

    |R(n)-kappa*s(n)*n| <= kappa*s(n)*n/log X.          (1)

For each such n, uniformly across [X,3X],

    G(n)=kappa*s(n)*n/log^2 n * (1+O(loglog X/log X)). (2)

The lower half follows from R(n)<=log^2(n) G(n). For the upper
bound, discard pairs with one prime <=n/log^4 n; there are at most
2n/log^4 n of them. Each remaining pair has logarithmic weight at least
(log n-4loglog n)^2. Hence

    G(n) <= R(n)/(log n-4loglog n)^2 + 2n/log^4 n.

Dividing by kappa*s(n)*n/log^2 n and using s(n)>=1 proves (2).
All denominators are positive once X is sufficiently large. This step
does not include prime powers or use an unproved pointwise Goldbach law.

For fixed m, removing the N for which any N+2j violates (1) removes at
most m times the global bad-target count. Thus (2) holds simultaneously
throughout every remaining block, with the same uniform relative error.

## Rounding and centered error

The common scale C satisfies, exactly,

    1 <= w_j*s(n_j)/C < 1+s(n_j)/C <= 1+1/d.           (3)

Write F(t)=t/log^2 t. Because m is fixed, F(N+2j)/F(N)=1+o(1)
uniformly for 0<=j<m and N in [X,2X]. Combine (2),(3) and rescale by
the common positive number kappa*C*F(N). The normalized values
y_j=x_j/(kappa*C*F(N)) obey

    1-o(1) <= y_j <= 1+1/d+o(1),                      (4)

uniformly over every good block, even though C varies with N.

Choose the fixed reference a=1+1/(2d). Then (4) implies

    E=sum_j(y_j-a)^2 <= m*(1/(2d)+o(1))^2 < a^2,      (5)

eventually, because m<(2d+1)^2. Let S=sum y_j,T=sum y_j^2.
Equation (5) is T-2aS+(m-1)a^2<0. Also

    2aS-(m-1)a^2 <= S^2/(m-1)                       (m>=2),

by completing the square. Hence S^2>(m-1)T. Multiplying back by the
square of kappa*C*F(N) proves Z>0. For m=1, (5) directly implies y_0>0
and Z=x_0^2>0. This proves the assertion with the stated bad-start count.

## What this changes

The fixed-range obstruction does not apply to this rule because the
within-block dynamic range is allowed to grow with the singular factors.
The positive result uses a global theorem to obtain an almost-all statement;
the negative result uses a fixed progression to locate infinitely many
failures of fixed ranges. These statements are compatible. Infinitely
many exceptions can have zero density.

For m=1000 the condition holds even with d=16; the implemented conservative
choice d=10000 leaves much more rounding margin. Neither choice removes
the unproved task of certifying every exceptional block. No universal
positivity, effective all-start bound, or computation-saving claim follows.

## Pursuit result

Status: `changed-under-evidence`. The declaration followed the 17:13:22 UTC
clock check; the completed proof and independent review were in hand by
17:22:33 UTC, within the 30-minute pursuit budget. No new range scan or
external action was needed. The exact reference-box slack at m=1000,d=16
is 89/1024; d=15 gives negative slack and is not covered by this proof.

The result changes the design from fixed-range weights to an adaptive
target-only scale with a proved almost-all guarantee. It leaves the main
goal open: certify the exceptional blocks. The reviewer checked the source
exponent bookkeeping, unweighted conversion, common-scale cancellation,
fixed-shift union, strict centered inequality, and the m=1 case. No material
gap was found. Historical originality remains unconfirmed; see
`local-peak-prior-art-check.md`.

"""Dyadic reduction of arbitrary hard intervals for the Mobius band target.

Owner: Kevin's Goldbach research.  Purpose: remove endpoint choice as a
power-scale issue after the finite sign mechanism failed.  This is an exact
deterministic reduction, not the missing arithmetic estimate on a dyadic block.

DYADIC PARTITION.
Write intervals in the existing convention J=(L,R].  A dyadic block is

 Q=(k*2^j,(k+1)*2^j],       j>=0, k>=0.                  (1)

The standard maximal dyadic partition P(J) consists of disjoint blocks whose
union is J, has at most two blocks of each length, and satisfies

 |P(J)|<=2*ceil(log_2(R+1)).                              (2)

The bound by log R rather than log |J| is harmless here because R<=7N/8.

LINEARITY OF THE ACTUAL COEFFICIENT.
For every q=dm and active h, the exact tail sum T_mu(q,h;J) is linear in the
indicator of J.  Hence

 T_mu(q,h;J)=sum_(Q in P(J))T_mu(q,h;Q).                 (3)

For d=1, the residue vector F_(m,J), its mean, and
delta_(m,J)=F_(m,J)-average(F_(m,J)) are all linear as well:

 delta_(m,J)=sum_(Q in P(J))delta_(m,Q).                 (4)

There is no extra endpoint-dependent mean term.

ENERGY LOSS.
Let K=2*ceil(log_2(N+1)).  Cauchy in the at most K blocks gives exactly

 sum_(h in B_q)|T_mu(q,h;J)|^2
   <=K*sum_(Q in P(J))sum_(h in B_q)|T_mu(q,h;Q)|^2.     (5)

At each dyadic length 2^j there are at most two blocks.  Label them by
s=1,2, inserting the zero block when absent.  After the positive d,m weights
are summed, (5) becomes

 E({J_m})<=K*sum_(j,s) E({Q_(m,j,s)}) .                 (6)

There are at most K selector families (j,s).  Therefore a uniform estimate

 E({Q_(m,j,s)})<=C_epsilon*N^(1499/1000+epsilon)         (7)

uniformly for every j,s occurring at N and every choice of one aligned
length-2^j block per modulus implies

 E({J_m})<=K^2*C_epsilon*N^(1499/1000+epsilon).          (8)

The factor K^2 is a fixed logarithmic loss and is absorbed by N^epsilon after
the usual epsilon adjustment.  Thus arbitrary hard endpoints cause no power
loss and do not disturb the H^(-1) target.

SCOPE.
Equation (7) is still unproved and still permits the block location to depend
on m.  The reduction does not make Conrey--Iwaniec--Soundararajan directly
applicable, smooth a sharp dyadic block, estimate the Mobius correlations, or
handle d>1 by itself.  It only converts the endpoint problem into fixed-length
aligned selector families at logarithmic cost.  Short dyadic boundary blocks
remain present and must be estimated or paid trivially at their actual length.
"""

from math import ceil, log2


def dyadic_partition(left, right):
    """Return the maximal aligned dyadic partition of integer interval (L,R]."""
    if (type(left) is not int or type(right) is not int
            or left < 0 or left >= right):
        raise ValueError("require integers 0<=left<right")
    l, r = left, right
    scale = 1
    from_left, from_right = [], []
    while l < r:
        if l & 1:
            from_left.append((l * scale, (l + 1) * scale))
            l += 1
        if r & 1:
            r -= 1
            from_right.append((r * scale, (r + 1) * scale))
        l //= 2
        r //= 2
        scale *= 2
    return tuple(from_left + list(reversed(from_right)))


def dyadic_partition_receipt(left, right):
    """Expose coverage, alignment, and per-scale multiplicities for tests."""
    blocks = dyadic_partition(left, right)
    multiplicities = {}
    for block_left, block_right in blocks:
        length = block_right - block_left
        multiplicities[length] = multiplicities.get(length, 0) + 1
    return {
        "blocks": blocks,
        "block_count": len(blocks),
        "logarithmic_cap": 2 * ceil(log2(right + 1)),
        "multiplicities": multiplicities,
        "at_most_two_per_scale": all(count <= 2
                                     for count in multiplicities.values()),
    }


def finite_energy_cauchy_receipt(block_vectors):
    """Check (5) for finite complex h-vectors attached to dyadic blocks."""
    vectors = tuple(tuple(vector) for vector in block_vectors)
    if not vectors:
        raise ValueError("at least one block vector required")
    dimension = len(vectors[0])
    if any(len(vector) != dimension for vector in vectors):
        raise ValueError("all block vectors must have the same dimension")
    combined = tuple(sum(vector[index] for vector in vectors)
                     for index in range(dimension))
    left = sum(abs(value) ** 2 for value in combined)
    component_energy = sum(abs(value) ** 2
                           for vector in vectors for value in vector)
    right = len(vectors) * component_energy
    return {
        "block_count": len(vectors),
        "combined_energy": left,
        "cauchy_bound": right,
        "inequality_holds": left <= right + 1e-12,
    }

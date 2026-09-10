"""Exact unique-large-prime switching identity and its sign obstruction.

For product index k near N, the core term has k=n*m, n<N**.41 and a
prime m>N**.59.  Since m>sqrt(k), it is unique.  Switching therefore
identifies the coefficient exactly, but the truncated-Mobius cofactor
weight is signed.  This is a limitation of a direct one-sided sieve plug-in,
not a Goldbach counterexample or an all-method parity theorem.
"""
from major_arc_kernel import _factorization, _mobius_phi


def _positive_integer(value, name):
    if not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def divisors(n):
    _positive_integer(n, "n")
    values = [1]
    for p, exponent in _factorization(n):
        values = [d * p**e for d in values for e in range(exponent + 1)]
    return tuple(sorted(values))


def short_divisor_weight(n, cutoff):
    """a_B(n)=sum_{d|n,d<=B} mu(d), exactly."""
    _positive_integer(n, "n")
    _positive_integer(cutoff, "cutoff")
    return sum(_mobius_phi(d)[0] for d in divisors(n) if d <= cutoff)


def large_prime_log_vector(k, short_cutoff, large_cutoff):
    """Log-prime vector for sum_{m|k, m prime>P} a_B(k/m) Lambda(m)."""
    for value, name in ((k, "k"), (short_cutoff, "short cutoff"),
                        (large_cutoff, "large cutoff")):
        _positive_integer(value, name)
    if large_cutoff * large_cutoff <= k:
        raise ValueError("require P^2>k so the large prime factor is unique")
    out = []
    for p, exponent in _factorization(k):
        if p > large_cutoff:
            # Lambda(m) can also see p^j.  The paid prime-only replacement
            # retains only m=p; proper powers belong to its separate error.
            out.append((p, short_divisor_weight(k // p, short_cutoff)))
    return tuple((p, c) for p, c in out if c)


def prime_atom_log_vector(k, large_cutoff):
    """The desired n=1 atom in the same prime-only large-factor model."""
    _positive_integer(k, "k")
    _positive_integer(large_cutoff, "large cutoff")
    return ((k, 1),) if k > large_cutoff and _factorization(k) == ((k, 1),) else ()


def switched_remainder_vector(k, short_cutoff, large_cutoff):
    """Exact composite-cofactor remainder after removing the prime atom."""
    total = dict(large_prime_log_vector(k, short_cutoff, large_cutoff))
    for p, c in prime_atom_log_vector(k, large_cutoff):
        total[p] = total.get(p, 0) - c
    return tuple((p, c) for p, c in sorted(total.items()) if c)


def negative_cofactor_witness(p, q, cutoff):
    """Verify a_B(pq)=-1 when p,q<=B<pq are distinct primes."""
    for value, name in ((p, "p"), (q, "q"), (cutoff, "cutoff")):
        _positive_integer(value, name)
    if p == q or _factorization(p) != ((p, 1),) or _factorization(q) != ((q, 1),):
        raise ValueError("distinct primes required")
    if not (p <= cutoff and q <= cutoff < p * q):
        raise ValueError("require p,q<=B<pq")
    value = short_divisor_weight(p * q, cutoff)
    return {"cofactor": p * q, "weight": value,
            "one_sided_sieve_usable": value >= 0}

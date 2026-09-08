"""Formal recovery of binary input flags from an exact ordered-count prefix.

If ``a[k-1]`` is the flag attached to odd ``2*k+1``, then the ordered
Goldbach-like prefix is the coefficient prefix of ``(sum a_k x^k)^2``.
This module establishes only that algebraic square-root consistency.  Calling
the recovered flags prime indicators requires independent knowledge that the
input counts were actual ordered Goldbach counts; no primality oracle appears
here.
"""
from __future__ import annotations


def _exact_nonnegative(value: object, name: str) -> int:
    if type(value) is not int or value < 0:
        raise ValueError(f"{name} must be a nonnegative exact integer")
    return value


def recover_binary_flags(ordered_counts: list[int]) -> list[int]:
    """Recover flags for odds 3 through ``2*m+1`` from ``G(6)..G(2*m+4)``.

    ``ordered_counts[k-1]`` is the coefficient of ``x**(k+1)``.  With
    ``a_1=1`` forced by ``G(6)=1``, its new terms are exactly ``2*a_k``:

    ``a_k = (G(2*k+4) - sum_{i=2}^{k-1} a_i*a_{k+1-i}) / 2``.
    """
    if not isinstance(ordered_counts, list) or not ordered_counts:
        raise ValueError("ordered counts must be a nonempty list")
    for index, count in enumerate(ordered_counts):
        _exact_nonnegative(count, f"ordered count {index}")
    if ordered_counts[0] != 1:
        raise ValueError("G(6) must equal 1 to select the binary square root")
    flags = [1]
    for k in range(2, len(ordered_counts) + 1):
        known_cross_terms = sum(flags[i - 1] * flags[k - i]
                                for i in range(2, k))
        numerator = ordered_counts[k - 1] - known_cross_terms
        if numerator % 2:
            raise ValueError(f"count at index {k - 1} gives an odd recovery numerator")
        recovered = numerator // 2
        if recovered not in (0, 1):
            raise ValueError(f"count at index {k - 1} does not recover a binary flag")
        flags.append(recovered)
    return flags


def ordered_count_prefix_from_binary_flags(flags: list[int]) -> list[int]:
    """Return the exact ordered convolution prefix for a supplied binary sequence.

    This is a formal helper, not a primality calculation.  For a flag list of
    length ``m``, its output is the ``m`` coefficients corresponding to even
    targets 6 through ``2*m+4``.
    """
    if not isinstance(flags, list) or not flags:
        raise ValueError("flags must be a nonempty list")
    if any(type(flag) is not int or flag not in (0, 1) for flag in flags):
        raise ValueError("flags must be exact binary integers")
    if flags[0] != 1:
        raise ValueError("the leading flag a_1 must be 1")
    return [sum(flags[i - 1] * flags[k - i] for i in range(1, k + 1))
            for k in range(1, len(flags) + 1)]

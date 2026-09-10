"""Exact row-period cancellation for the signed CRT count error.

For fixed ``m,a,b,s`` in the same-row setup, put ``q=lcm(a,b)``.  Whenever
``gcd(a,b)|s``, the compatible CRT residue for ``y`` changes by ``-m`` modulo
``q`` when the row index ``ell`` increases by one.  Since the project has
prime ``m>max(a,b)``, multiplication by ``m`` permutes the residues modulo
``q``.  Hence, for every starting row,

    sum_(ell=ell0)^(ell0+q-1) E_(a,b,s)(ell) = 0.        (1)

This is an exact cancellation mechanism linking the two divisor conditions:
over a full lcm period every possible CRT endpoint occurs once.

It does not by itself give a useful uniform incomplete-period bound.  After
removing complete copies of the interval modulo ``q``, ``E(ell)`` is the
indicator of one cyclic interval sampled along the rotation ``-m``, minus
its mean.  Its Fourier expansion is

    E(ell)=sum_(1<=k<q) chat(k)e_q(-k*m*ell),            (2)

so a block of ``A`` rows contains geometric factors
``min(A,1/(2||km/q||))``.  A modulus resonant modulo ``q`` can therefore
retain a constant fraction of the trivial ``A`` loss.  Prime-modulus or
divisor-pair averaging is a genuinely new arithmetic requirement; the
period identity alone does not cross the ``B=N^.245`` endpoint.
"""

import math

import numpy as np

from mobius_covariance_endpoint_probe import _prime_flags
from signed_crt_discrepancy_probe import crt_interval_count_error


def same_row_crt_count_error(modulus, ell, left, right, separation):
    """Return the exact pair count, density, error, and compatible residue."""
    if any(type(value) is not int for value in (
            modulus, ell, left, right, separation)):
        raise ValueError("all arguments must be integers")
    if (ell < 0 or not 1 < left < modulus or not 1 < right < modulus
            or abs(separation) >= modulus - 1):
        raise ValueError("invalid same-row CRT ranges")
    common_divisor = math.gcd(left, right)
    length = modulus - 1 - abs(separation)
    if separation % common_divisor:
        return {
            "compatible": False,
            "count": 0,
            "density": 0.0,
            "error": 0.0,
            "residue": None,
        }

    reduced_left = left // common_divisor
    reduced_right = right // common_divisor
    right_residue = (-modulus * ell) % right
    left_residue = (-modulus * ell - separation) % left
    multiplier = (((left_residue - right_residue) // common_divisor)
                  * pow(reduced_right, -1, reduced_left)) % reduced_left
    residue = (right_residue + right * multiplier) % math.lcm(left, right)
    lower = max(1, 1 - separation)
    upper = min(modulus - 1, modulus - 1 - separation)
    count, endpoint_formula, direct_error = crt_interval_count_error(
        lower, upper, residue, math.lcm(left, right))
    if abs(endpoint_formula - direct_error) > 1e-12:
        raise ArithmeticError("endpoint formula mismatch")
    return {
        "compatible": True,
        "count": count,
        "density": length / math.lcm(left, right),
        "error": direct_error,
        "residue": residue,
    }


def complete_row_period_receipt(modulus, ell_first,
                                left, right, separation):
    """Evaluate and certify the exact full-period cancellation (1)."""
    if type(modulus) is not int or modulus < 3:
        raise ValueError("modulus must be an integer at least 3")
    flags = _prime_flags(modulus)
    if not flags[modulus]:
        raise ValueError("modulus must be prime")
    period = math.lcm(left, right)
    values = tuple(same_row_crt_count_error(
        modulus, ell, left, right, separation)["error"]
        for ell in range(ell_first, ell_first + period))
    return {
        "modulus": modulus,
        "ell_first": ell_first,
        "left": left,
        "right": right,
        "separation": separation,
        "period": period,
        "error_sum": float(sum(values)),
        "maximum_partial_sum": float(max(abs(sum(values[:length]))
                                         for length in range(period + 1))),
        "complete_period_cancellation_proved": True,
        "incomplete_period_power_saving_proved": False,
    }


def endpoint_error_fourier_reconstruction(
        modulus, left, right, separation):
    """Check the exact nonzero-frequency reconstruction in (2)."""
    if any(type(value) is not int for value in (
            modulus, left, right, separation)):
        raise ValueError("all arguments must be integers")
    period = math.lcm(left, right)
    if math.gcd(modulus, period) != 1:
        raise ValueError("modulus must be coprime to the lcm period")
    values = np.array([same_row_crt_count_error(
        modulus, ell, left, right, separation)["error"]
        for ell in range(period)], dtype=float)
    coefficients = np.fft.fft(values) / period
    reconstructed = np.fft.ifft(coefficients * period).real
    return {
        "period": period,
        "mean_error": float(coefficients[0].real),
        "maximum_reconstruction_error": float(
            np.max(np.abs(values - reconstructed))),
        "largest_nonzero_fourier_coefficient": float(
            np.max(np.abs(coefficients[1:])) if period > 1 else 0.0),
        "nonzero_frequency_expansion_proved": True,
    }


def worst_incomplete_row_block(modulus, left, right,
                               separation, row_count):
    """Maximize an incomplete sum over all starts in one lcm period."""
    if type(row_count) is not int or row_count < 1:
        raise ValueError("row_count must be a positive integer")
    period = math.lcm(left, right)
    values = tuple(same_row_crt_count_error(
        modulus, ell, left, right, separation)["error"]
        for ell in range(period))
    sums = tuple(sum(values[(start + offset) % period]
                     for offset in range(row_count))
                 for start in range(period))
    worst_index = max(range(period), key=lambda index: abs(sums[index]))
    return {
        "modulus": modulus,
        "left": left,
        "right": right,
        "separation": separation,
        "period": period,
        "row_count": row_count,
        "worst_start": worst_index,
        "worst_signed_sum": float(sums[worst_index]),
        "absolute_sum_over_row_count": float(
            abs(sums[worst_index]) / row_count),
        "incomplete_period_power_saving_proved": False,
    }


if __name__ == "__main__":
    print(complete_row_period_receipt(71, 3, 5, 7, 17))
    print(endpoint_error_fourier_reconstruction(71, 5, 7, 17))
    print(worst_incomplete_row_block(71, 5, 7, 17, 8))

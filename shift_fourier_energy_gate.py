"""Exact Fourier-energy budget for the shift-bandpass proposal.

For one modulus q, periodize the full kernel W(r)=C0(r/H) and write
 S_q=sum_(a mod q) W_q(a-N) A_high(q,a).
With unnormalized finite Fourier transforms,
 S_q=q^-1 sum_h What_q(-h)e(-hN/q) Ahat_q(h).
Poisson localizes What to about q/H frequencies of size O(H), so its
total square mass is qH.  Parseval therefore reproduces the original
residue Cauchy bound; bandpass localization alone gives no H saving.

The precise new input would be a band-energy estimate
 sum_(h~q/H)|Ahat_q(h)|^2 <= H^-1 sum_h|Ahat_q(h)|^2
on average over the actual structured q.  This would give H^-1/2 in
the correlation and close the top exponent conditionally.  No such
prime-discrepancy estimate is proved here.

Hard shift truncations, endpoint masks, or other r-dependent weights
convolve and spread the DFT.  Their leakage must be bounded before the exact
support statement can be used in the arithmetic sum.
"""
from fractions import Fraction as F

Q = F(599, 1000)
H = F(1, 10)


def kernel_frequency_budget(q_exponent=Q, shift_exponent=H):
    if not all(isinstance(x, F) and 0 < x < 1
               for x in (q_exponent, shift_exponent)):
        raise ValueError("exact exponents in (0,1) required")
    if q_exponent <= shift_exponent:
        raise ValueError("require q>H")
    count = q_exponent - shift_exponent
    amplitude = shift_exponent
    return {
        "active_frequency_count": count,
        "coefficient_amplitude": amplitude,
        "kernel_square_energy": count + 2 * amplitude,
        "parseval_expected_energy": q_exponent + shift_exponent,
    }


def required_prime_band_energy_ratio(shift_exponent=H):
    """Power exponent of the needed band/total energy ratio."""
    if not isinstance(shift_exponent, F) or not 0 < shift_exponent < 1:
        raise ValueError("exact shift exponent in (0,1) required")
    return -shift_exponent


def resulting_correlation_gain(shift_exponent=H):
    """Square root of the required energy ratio."""
    return required_prime_band_energy_ratio(shift_exponent) / 2


def generic_large_sieve_improves(q_exponent=Q, frequency_length=None):
    """The generic (length+conductor) term is conductor-dominated here."""
    if frequency_length is None:
        frequency_length = q_exponent - H
    if not all(isinstance(x, F) and 0 <= x <= 1
               for x in (q_exponent, frequency_length)):
        raise ValueError("exact exponents in [0,1] required")
    generic_term = max(frequency_length, q_exponent)
    return generic_term < q_exponent


def energy_gate_receipt():
    budget = kernel_frequency_budget()
    return {
        **budget,
        "kernel_energy_matches_parseval":
            budget["kernel_square_energy"] == budget["parseval_expected_energy"],
        "required_band_energy_ratio": required_prime_band_energy_ratio(),
        "conditional_correlation_gain": resulting_correlation_gain(),
        "generic_large_sieve_improves": generic_large_sieve_improves(),
        "arithmetic_band_energy_proved": False,
        "mask_leakage_paid": False,
    }

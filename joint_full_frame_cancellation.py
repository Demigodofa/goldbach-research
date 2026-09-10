"""Use the joint row-prime rotation to improve the exact full frame.

The exact full-frequency collision Gram contains, for ``q=lcm(a,b)``, the
count of multiples of ``q`` among ``ml+1,...,ml+m-1``.  Split

    C_q(m,l)-m/q
      =[C_q(m,l)-(m-1)/q] - 1/q.                       (1)

The bracketed term is the same mean-zero cyclic interval discrepancy treated
in ``joint_prime_row_crt_bound.py``.  Its row Fourier coefficients and joint
prime-row Cauchy bound therefore give the saving

    delta(q)=N^eps{A^(-1/2)+sqrt(q/(M*A))+q^(-1/2)}.    (2)

The fixed ``-1/q`` bias in (1), the row-log variation, and the exact centering
terms are covered by the non-endpoint part of the earlier full-frame
perturbation.  Abel summation handles the smooth row logs.  Applying
rectangular Schur on scales ``U,W`` and then maximizing ``U,W<=B`` gives

    ||G_joint-P0_joint||_F
      << N^eps{(B^2/M)
          [A^(-1/2)+B/sqrt(M*A)+B^(-1/2)] + B/A}.       (3)

Here ``P0`` is the frozen positive gcd-feature Gram and ``F`` is the summed
block totient frame.  The finite multiples-poset inversion already proves
``P0>=N^-eps F`` on the lower union, so a power-small right side in (3)
transfers coercivity to the aggregate exact full Gram.

At ``H=N^.1,M=N^.59,A=N^.41,B=N^beta``, the signed-count terms in (3) have
exponents

    2*beta-.795,  3*beta-1.09,  1.5*beta-.59,          (4)

and the smooth remainder has exponent ``beta-.41``.  Thus the joint full
frame survives for ``beta<109/300=.36333...``.  The active signed endpoint
from ``joint_prime_row_crt_bound.py`` is stricter at
``beta<49/150=.32666...`` on a row interval whose length is comparable to
``A``.

The aggregate theorem uses one common divisor coefficient vector across the
prime-row sum, as required by the actual Mobius vector.  It is not a
row-by-row lower frame.  In particular, it does not yet transfer the active
bound through every lag: a lag ``Delta`` leaves only ``A-Delta`` base rows,
and aggregate coercivity does not lower-bound each geometric energy
``sqrt(E_ell E_(ell+Delta))`` in the existing lag budget.  The completely
assembled lower union therefore remains at ``beta<.295``.  A weighted
all-lag lower-frame lemma is the next requirement.  None of these statements
proves the final signed prime correlation.
"""

import math

import numpy as np

from divisor_active_full_gram import _full_collision_gram
from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from near_cutoff_geometric_bound import _active_modes


def _multiband_frame_receipt(exact, ideal, frame):
    """Return spectra without assuming the multiband ideal dominates F."""
    scale = np.sqrt(frame)
    normalized_ideal = ideal / (scale[:, None] * scale[None, :])
    normalized_error = (exact - ideal) / (
        scale[:, None] * scale[None, :])
    normalized_exact = exact / (scale[:, None] * scale[None, :])
    ideal_values = np.linalg.eigvalsh(
        (normalized_ideal + normalized_ideal.T) / 2)
    error_values = np.linalg.eigvalsh(
        (normalized_error + normalized_error.T) / 2)
    exact_values = np.linalg.eigvalsh(
        (normalized_exact + normalized_exact.T) / 2)
    return {
        "ideal_over_frame_eigenvalue_min": float(ideal_values[0]),
        "ideal_over_frame_eigenvalue_max": float(ideal_values[-1]),
        "error_over_frame_eigenvalue_min": float(error_values[0]),
        "error_over_frame_eigenvalue_max": float(error_values[-1]),
        "error_over_frame_operator_norm": float(max(
            abs(error_values[0]), abs(error_values[-1]))),
        "proved_exact_over_frame_lower_via_weyl": float(
            ideal_values[0] + error_values[0]),
        "actual_exact_over_frame_eigenvalue_min": float(exact_values[0]),
        "actual_exact_over_frame_eigenvalue_max": float(exact_values[-1]),
        "finite_lower_frame_certificate_survives": bool(
            ideal_values[0] + error_values[0] > 0),
    }


def joint_multiband_full_frame_probe(
        moduli, shift_length, ell_first, row_count,
        divisor_lower, divisor_upper):
    """Measure aggregate exact, ideal, and error spectra on a lower union."""
    if not isinstance(moduli, (tuple, list)) or not moduli:
        raise ValueError("moduli must be a nonempty tuple or list")
    if any(type(value) is not int for value in moduli):
        raise ValueError("every modulus must be an integer")
    if any(type(value) is not int for value in (
            shift_length, ell_first, row_count,
            divisor_lower, divisor_upper)):
        raise ValueError("all other arguments must be integers")
    if (not 2 <= shift_length <= divisor_lower
            or ell_first < 1 or row_count < 1
            or divisor_lower < 2 or divisor_upper <= divisor_lower
            or divisor_upper >= min(moduli)):
        raise ValueError("invalid joint full-frame ranges")
    flags = _prime_flags(max(moduli))
    if any(not flags[modulus] for modulus in moduli):
        raise ValueError("every modulus must be prime")

    mobius = _mobius_values(divisor_upper)
    divisors = tuple(
        value for value in range(divisor_lower + 1, divisor_upper + 1)
        if mobius[value])
    if not divisors:
        raise ValueError("the squarefree divisor range must be nonempty")
    divisor_array = np.array(divisors, dtype=float)
    totients = np.array([_totient(a) for a in divisors], dtype=float)
    gcd_matrix = np.gcd.outer(divisors, divisors).astype(float)
    gcd_kernel = ((gcd_matrix - 1)
                  / np.multiply.outer(divisor_array, divisor_array))
    exact = np.zeros((len(divisors), len(divisors)), dtype=float)
    ideal = np.zeros_like(exact)
    frame = np.zeros(len(divisors), dtype=float)
    for modulus in moduli:
        rho = len(_active_modes(modulus, shift_length)) / (modulus - 1)
        outer_weight = math.log(modulus) ** 2 / modulus * rho
        for ell in range(ell_first, ell_first + row_count):
            logs = np.log(modulus * ell / divisor_array)
            exact += outer_weight * _full_collision_gram(
                modulus, ell, divisors)
            ideal += (outer_weight * modulus ** 2
                      * logs[:, None] * logs[None, :] * gcd_kernel)
            frame += (outer_weight * modulus ** 2 * logs ** 2
                      * totients / divisor_array ** 2)
    return {
        "moduli": tuple(moduli),
        "prime_count": len(moduli),
        "shift_length": shift_length,
        "ell_first": ell_first,
        "row_count": row_count,
        "divisor_range": (divisor_lower, divisor_upper),
        "divisor_count": len(divisors),
        **_multiband_frame_receipt(exact, ideal, frame),
        "joint_full_frame_asymptotic_theorem": False,
        "signed_prime_correlation_proved": False,
    }


def project_joint_full_frame_exponent_budget(divisor_exponent):
    """Return (4), the active endpoint terms, and the combined threshold."""
    if (isinstance(divisor_exponent, bool)
            or not isinstance(divisor_exponent, (int, float))
            or not 0 < divisor_exponent < .5):
        raise ValueError("divisor_exponent must lie in (0,.5)")
    beta = float(divisor_exponent)
    full_terms = (
        2 * beta - .795,
        3 * beta - 1.09,
        1.5 * beta - .59,
        beta - .41,
    )
    active_terms = (
        2 * beta - .695,
        3 * beta - .99,
        1.5 * beta - .49,
    )
    return {
        "divisor_exponent": beta,
        "joint_full_frame_term_exponents": full_terms,
        "joint_full_frame_worst_exponent": max(full_terms),
        "joint_full_frame_power_saving": max(full_terms) < 0,
        "joint_active_endpoint_term_exponents": active_terms,
        "joint_active_endpoint_power_saving": max(active_terms) < 0,
        "joint_aggregate_components_power_saving": (
            max(full_terms) < 0 and max(active_terms) < 0),
        "all_lag_energy_transfer_proved": False,
        "previous_complete_assembly_supported": beta < .295,
        "strict_joint_full_frame_threshold": 109 / 300,
        "strict_fixed_long_lag_component_threshold": 49 / 150,
        "strict_previous_complete_assembly_threshold": .295,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    for beta in (.295, .32, .326, 49 / 150, .35, 109 / 300):
        print(project_joint_full_frame_exponent_budget(beta))
    print(joint_multiband_full_frame_probe(
        (1009, 1013, 1019, 1021, 1031), 5, 9, 8, 8, 64))

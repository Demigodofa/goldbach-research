"""Falsify a weighted all-lag lower-frame transfer.

For one common divisor coefficient vector ``c`` define exact row energies
``E_(m,l)=c*G_(m,l)c`` and diagonal totient-frame energies
``F_(m,l)=c*F_(m,l)c``.  For a lag set ``J`` compare

    Q_J(c) = [sum_m w_m rho_m sum_(Delta in J,l)
                 sqrt(E_(m,l)E_(m,l+Delta))]
             /[sum_m w_m rho_m sum_(Delta in J,l)
                 sqrt(F_(m,l)F_(m,l+Delta))].           (1)

The aggregate lower frame does not formally imply a lower bound for (1).
This probe attacks that gap with the aggregate minimum generalized
eigenvector, every single-row minimum generalized eigenvector, coordinate and
Mobius vectors, and seeded real and complex random coefficients.  The minimum
reported quotient is therefore a finite adversarial measurement, not a
uniform theorem.  Polynomial decay as the divisor union grows is the
falsifier.
"""

import math

import numpy as np

from divisor_active_full_gram import _full_collision_gram
from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from near_cutoff_geometric_bound import _active_modes


def _minimum_generalized_vector(matrix, diagonal):
    inverse_scale = 1 / np.sqrt(diagonal)
    normalized = (inverse_scale[:, None] * matrix
                  * inverse_scale[None, :])
    normalized = (normalized + np.conjugate(normalized.T)) / 2
    values, vectors = np.linalg.eigh(normalized)
    return float(values[0]), inverse_scale * vectors[:, 0]


def _quadratic_energy(matrix, coefficients):
    value = float(np.real(
        np.conjugate(coefficients) @ matrix @ coefficients))
    tolerance = 1e-10 * max(
        1.0, float(np.linalg.norm(matrix))
        * float(np.linalg.norm(coefficients)) ** 2)
    if value < -tolerance:
        raise ArithmeticError("a row Gram produced negative energy")
    return max(0.0, value)


def all_lag_frame_transfer_probe(
        moduli, shift_length, ell_first, row_count,
        divisor_lower, divisor_upper, lag_blocks,
        random_trials=256, random_seed=20260910):
    """Return adversarial finite quotients (1) for several lag blocks."""
    if not isinstance(moduli, (tuple, list)) or not moduli:
        raise ValueError("moduli must be a nonempty tuple or list")
    if any(type(value) is not int for value in moduli):
        raise ValueError("every modulus must be an integer")
    if any(type(value) is not int for value in (
            shift_length, ell_first, row_count,
            divisor_lower, divisor_upper, random_trials, random_seed)):
        raise ValueError("integer parameters must be integers")
    if (not 2 <= shift_length <= divisor_lower
            or ell_first < 1 or row_count < 2
            or divisor_lower < 2 or divisor_upper <= divisor_lower
            or divisor_upper >= min(moduli) or random_trials < 0):
        raise ValueError("invalid all-lag ranges")
    if not isinstance(lag_blocks, (tuple, list)) or not lag_blocks:
        raise ValueError("lag_blocks must be nonempty")
    for block in lag_blocks:
        if (not isinstance(block, (tuple, list)) or len(block) != 2
                or any(type(value) is not int for value in block)
                or not 1 <= block[0] < block[1] <= row_count):
            raise ValueError("each lag block must satisfy 1<=first<stop<=rows")
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
    totients = np.array([_totient(value) for value in divisors], dtype=float)

    row_data = {}
    aggregate_exact = np.zeros((len(divisors), len(divisors)))
    aggregate_frame = np.zeros(len(divisors))
    for modulus in moduli:
        rho = len(_active_modes(modulus, shift_length)) / (modulus - 1)
        weight = math.log(modulus) ** 2 / modulus * rho
        for ell in range(ell_first, ell_first + row_count):
            exact = _full_collision_gram(modulus, ell, divisors)
            logs = np.log(modulus * ell / divisor_array)
            frame = modulus ** 2 * logs ** 2 * totients / divisor_array ** 2
            row_data[(modulus, ell)] = (weight, exact, frame)
            aggregate_exact += weight * exact
            aggregate_frame += weight * frame

    candidates = []
    aggregate_minimum, aggregate_vector = _minimum_generalized_vector(
        aggregate_exact, aggregate_frame)
    candidates.append(("aggregate_minimum", aggregate_vector))
    for modulus in moduli:
        for ell in range(ell_first, ell_first + row_count):
            _, exact, frame = row_data[(modulus, ell)]
            _, vector = _minimum_generalized_vector(exact, frame)
            candidates.append((f"row_minimum_m{modulus}_l{ell}", vector))
    candidates.append((
        "mobius", np.array([mobius[value] for value in divisors], dtype=float)))
    for index in range(len(divisors)):
        coordinate = np.zeros(len(divisors))
        coordinate[index] = 1
        candidates.append((f"coordinate_{divisors[index]}", coordinate))
    generator = np.random.default_rng(random_seed)
    for trial in range(random_trials):
        candidates.append((f"random_real_{trial}", generator.normal(
            size=len(divisors))))
        candidates.append((f"random_complex_{trial}", generator.normal(
            size=len(divisors)) + 1j * generator.normal(size=len(divisors))))

    def lag_quotient(coefficients, lag_first, lag_stop):
        exact_sum = frame_sum = 0.0
        exact_rows = []
        for modulus in moduli:
            energies = {}
            frames = {}
            weight = row_data[(modulus, ell_first)][0]
            for ell in range(ell_first, ell_first + row_count):
                _, exact, frame = row_data[(modulus, ell)]
                energies[ell] = _quadratic_energy(exact, coefficients)
                frames[ell] = float(np.sum(
                    frame * np.abs(coefficients) ** 2))
                exact_rows.append(weight * energies[ell])
            for delta in range(lag_first, lag_stop):
                for ell in range(
                        ell_first, ell_first + row_count - delta):
                    exact_sum += weight * math.sqrt(
                        energies[ell] * energies[ell + delta])
                    frame_sum += weight * math.sqrt(
                        frames[ell] * frames[ell + delta])
        aggregate_exact_energy = sum(exact_rows)
        aggregate_frame_energy = _quadratic_energy(
            np.diag(aggregate_frame), coefficients)
        return (
            exact_sum / frame_sum,
            aggregate_exact_energy / aggregate_frame_energy,
            max(exact_rows) / aggregate_exact_energy,
        )

    blocks = []
    for lag_first, lag_stop in lag_blocks:
        best = None
        for name, coefficients in candidates:
            quotient, aggregate_ratio, concentration = lag_quotient(
                coefficients, lag_first, lag_stop)
            if best is None or quotient < best[0]:
                best = (quotient, name, aggregate_ratio, concentration)
        blocks.append({
            "lag_range": (lag_first, lag_stop - 1),
            "minimum_tested_exact_over_frame_lag_budget": best[0],
            "minimizing_candidate": best[1],
            "candidate_aggregate_exact_over_frame": best[2],
            "candidate_max_weighted_row_energy_fraction": best[3],
        })
    return {
        "moduli": tuple(moduli),
        "prime_count": len(moduli),
        "shift_length": shift_length,
        "row_range": (ell_first, ell_first + row_count - 1),
        "divisor_range": (divisor_lower, divisor_upper),
        "divisor_count": len(divisors),
        "aggregate_exact_over_frame_minimum": aggregate_minimum,
        "candidate_count": len(candidates),
        "lag_blocks": tuple(blocks),
        "weighted_all_lag_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    result = all_lag_frame_transfer_probe(
        (1009, 1013, 1019, 1021, 1031), 5, 9, 32, 8, 64,
        ((1, 2), (1, 8), (8, 16), (16, 32)), random_trials=128)
    for key, value in result.items():
        print(f"{key}: {value}")

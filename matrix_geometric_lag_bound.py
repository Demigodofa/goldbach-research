"""Direct quadratic minorant for the nonlinear all-lag energy.

For positive definite row Grams ``G_u,G_v``, their matrix geometric mean

    G_u # G_v = G_u^(1/2)
        (G_u^(-1/2) G_v G_u^(-1/2))^(1/2) G_u^(1/2)

satisfies

    c*(G_u # G_v)c <= sqrt((c*G_u c)(c*G_v c)).        (1)

This follows from positivity of the block matrix
``[[G_u,G_u#G_v],[G_u#G_v,G_v]]``.  For diagonal frame matrices, scalar
AM-GM gives

    sqrt((c*F_u c)(c*F_v c))
        <= c*((F_u+F_v)/2)c.                           (2)

After summing weighted lag edges, (1)-(2) minorize the exact nonlinear lag
quotient by one generalized eigenvalue.  The matrix inequalities are exact;
the eigenvalues produced here are finite floating-point measurements rather
than asymptotic lower-frame theorems.
"""

import math

import numpy as np

from divisor_active_full_gram import _full_collision_gram
from divisor_full_frame_probe import _totient
from mobius_covariance_endpoint_probe import _prime_flags
from mobius_covariance_lag_probe import _mobius_values
from near_cutoff_geometric_bound import _active_modes


def _symmetric(matrix):
    return (matrix + np.conjugate(matrix.T)) / 2


def _positive_square_root(matrix, require_positive=False):
    matrix = _symmetric(np.asarray(matrix))
    values, vectors = np.linalg.eigh(matrix)
    scale = max(1.0, float(np.max(np.abs(values))))
    tolerance = 1e-11 * scale
    if values[0] < -tolerance:
        raise ArithmeticError("matrix is not positive semidefinite")
    if require_positive and values[0] <= tolerance:
        raise ArithmeticError("matrix is not numerically positive definite")
    values = np.maximum(values, 0.0)
    root = (vectors * np.sqrt(values)) @ np.conjugate(vectors.T)
    return _symmetric(root), values, vectors


def matrix_geometric_mean(left, right):
    """Return the Kubo-Ando geometric mean of two positive matrices."""
    left = _symmetric(np.asarray(left))
    right = _symmetric(np.asarray(right))
    if left.shape != right.shape or left.ndim != 2 \
            or left.shape[0] != left.shape[1]:
        raise ValueError("left and right must be equal-size square matrices")
    left_root, left_values, left_vectors = _positive_square_root(
        left, require_positive=True)
    left_inverse_root = (
        left_vectors * (1 / np.sqrt(left_values)))
    left_inverse_root = (left_inverse_root
                         @ np.conjugate(left_vectors.T))
    middle = _symmetric(left_inverse_root @ right @ left_inverse_root)
    middle_root, _, _ = _positive_square_root(middle)
    return _symmetric(left_root @ middle_root @ left_root)


def _generalized_spectrum(matrix, positive_diagonal):
    scale = np.sqrt(np.asarray(positive_diagonal, dtype=float))
    normalized = matrix / (scale[:, None] * scale[None, :])
    return np.linalg.eigvalsh(_symmetric(normalized))


def matrix_geometric_lag_probe(
        moduli, shift_length, ell_first, row_count,
        divisor_lower, divisor_upper, lag_blocks):
    """Measure the direct matrix-geometric lower operator by lag block."""
    if not isinstance(moduli, (tuple, list)) or not moduli:
        raise ValueError("moduli must be a nonempty tuple or list")
    if any(type(value) is not int for value in moduli):
        raise ValueError("every modulus must be an integer")
    if any(type(value) is not int for value in (
            shift_length, ell_first, row_count,
            divisor_lower, divisor_upper)):
        raise ValueError("range parameters must be integers")
    if (not 2 <= shift_length <= divisor_lower
            or ell_first < 1 or row_count < 2
            or divisor_lower < 2 or divisor_upper <= divisor_lower
            or divisor_upper >= min(moduli)):
        raise ValueError("invalid matrix-geometric lag ranges")
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
    rows = {}
    minimum_input_eigenvalue = math.inf
    for modulus in moduli:
        rho = len(_active_modes(modulus, shift_length)) / (modulus - 1)
        weight = math.log(modulus) ** 2 / modulus * rho
        for ell in range(ell_first, ell_first + row_count):
            exact = _symmetric(_full_collision_gram(
                modulus, ell, divisors))
            minimum_input_eigenvalue = min(
                minimum_input_eigenvalue,
                float(np.linalg.eigvalsh(exact)[0]))
            logs = np.log(modulus * ell / divisor_array)
            frame = modulus ** 2 * logs ** 2 * totients / divisor_array ** 2
            rows[(modulus, ell)] = (weight, exact, frame)

    block_receipts = []
    for lag_first, lag_stop in lag_blocks:
        lower_operator = np.zeros(
            (len(divisors), len(divisors)), dtype=float)
        upper_frame = np.zeros(len(divisors), dtype=float)
        edge_count = 0
        for modulus in moduli:
            weight = rows[(modulus, ell_first)][0]
            for delta in range(lag_first, lag_stop):
                for ell in range(
                        ell_first, ell_first + row_count - delta):
                    _, left_exact, left_frame = rows[(modulus, ell)]
                    _, right_exact, right_frame = rows[
                        (modulus, ell + delta)]
                    lower_operator += weight * matrix_geometric_mean(
                        left_exact, right_exact)
                    upper_frame += weight * (left_frame + right_frame) / 2
                    edge_count += 1
        values = _generalized_spectrum(lower_operator, upper_frame)
        block_receipts.append({
            "lag_range": (lag_first, lag_stop - 1),
            "edge_count": edge_count,
            "matrix_geometric_over_arithmetic_frame_minimum":
                float(values[0]),
            "matrix_geometric_over_arithmetic_frame_maximum":
                float(values[-1]),
            "measured_positive_generalized_eigenvalue": bool(values[0] > 0),
        })
    return {
        "moduli": tuple(moduli),
        "row_range": (ell_first, ell_first + row_count - 1),
        "divisor_range": (divisor_lower, divisor_upper),
        "divisor_count": len(divisors),
        "minimum_input_gram_eigenvalue": minimum_input_eigenvalue,
        "lag_blocks": tuple(block_receipts),
        "matrix_geometric_scalar_minorization_proved": True,
        "asymptotic_all_lag_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(matrix_geometric_lag_probe(
        (1009, 1013), 5, 9, 16, 8, 64,
        ((1, 2), (1, 8), (8, 16))))

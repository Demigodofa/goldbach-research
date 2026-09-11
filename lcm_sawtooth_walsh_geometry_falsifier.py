"""Falsify a coefficient-uniform Walsh/complement comparison.

On the Boolean divisor group for squarefree ``d`` with ``omega(d)=k``, let
``bar(u)=d/u``.  Complement geometry alone cannot prove

    (sum_u |f_u|^2)^2 <= C 2^k |sum_u f_u f_bar(u)|^2.

Indeed, put ``f_1=1``, ``f_d=epsilon``, and all other entries zero.  The left
base is ``(1+epsilon^2)^2`` while the complement convolution squared is
``4 epsilon^2``.  Their ratio divided by ``2^k`` tends to infinity as
``epsilon`` tends to zero.  The paired-support majorant is exactly
``2|epsilon|`` and therefore avoids this artificial mismatch.

This is an abstract resonant-coefficient obstruction.  It does not use or
falsify the project's fixed Mobius-polynomial coefficients.
"""


def walsh_geometry_resonance(prime_factor_count=5, epsilon=1e-6):
    """Return an exact finite witness and the general epsilon formula."""
    if (type(prime_factor_count) is not int or prime_factor_count < 1
            or not isinstance(epsilon, (int, float))
            or not 0 < epsilon < 1):
        raise ValueError("require k>=1 and 0<epsilon<1")
    group_size = 1 << prime_factor_count
    values = [0.0] * group_size
    values[0] = 1.0
    values[-1] = float(epsilon)
    complement_convolution = sum(
        values[mask] * values[(group_size - 1) ^ mask]
        for mask in range(group_size))
    walsh_majorant = sum(value ** 2 for value in values)
    paired_majorant = sum(
        abs(values[mask] * values[(group_size - 1) ^ mask])
        for mask in range(group_size))
    ratio = walsh_majorant ** 2 / complement_convolution ** 2
    return {
        "prime_factor_count": prime_factor_count,
        "boolean_group_size": group_size,
        "epsilon": float(epsilon),
        "walsh_majorant": walsh_majorant,
        "complement_convolution": complement_convolution,
        "paired_support_majorant": paired_majorant,
        "walsh_energy_over_complement_energy": ratio,
        "ratio_after_2_to_omega_cost": ratio / group_size,
        "exact_ratio_formula": "(1+epsilon^2)^2/(4*epsilon^2)",
        "ratio_diverges_as_epsilon_tends_to_zero": True,
        "coefficient_uniform_2_to_omega_bound_falsified": True,
        "fixed_mobius_polynomial_bound_falsified": False,
    }


if __name__ == "__main__":
    for key, value in walsh_geometry_resonance().items():
        print(f"{key}: {value}")

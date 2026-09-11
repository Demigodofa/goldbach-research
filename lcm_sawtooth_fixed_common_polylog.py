"""Polylog residual-collapse bound for every fixed common-part layer.

Fix ``c=d_C`` in the three-way conductor assignment

    d=d_L*d_R*c,
    a=d_L*c*alpha,  b=d_R*c*beta.

The base factors have product ``d*c``.  If ``d*c>B*V``, every occurring
residual pair forces both base factors into ``(V,B]``, so its ``r=1`` base
pair is present.  The same three-state argument as in the no-common layer
then gives

    |A_(d,c,r)| <= 3^omega(r) A_(d,c,1),
    r <= B^2/(d*c),

and hence a ``(1+log(B^2/(d*c)))^6`` collapsed/diagonal bound within this
fixed layer.  Combining different ``c`` layers still requires control of
their signed diagonal interference.

When the stronger condition ``d>B*V`` holds, splitting every common prime
left or right maps ``2^omega(c)`` copies of a fixed-common base pair into
retained no-common base pairs of no smaller log weight.  Therefore

    2^omega(c) A_c <= A_1,
    sum_(c|d) A_c^2 <= (5/4)^omega(d) A_1^2.

This controls separated base energy, not the Mobius-signed combined base.
"""

from lcm_sawtooth_high_d_assignment import _squarefree_prime_factors
from lcm_sawtooth_no_common_polylog import three_state_harmonic_receipt


def fixed_common_layer_polylog_receipt(
        X, divisor_lower, divisor_upper, target_divisor, common_part):
    """Return the conditional fixed-layer theorem bound."""
    if (not isinstance(X, (int, float))
            or any(type(value) is not int for value in (
                divisor_lower, divisor_upper, target_divisor, common_part))):
        raise ValueError("all inputs must be integers")
    if (X <= divisor_upper or divisor_lower < 1
            or divisor_upper <= divisor_lower
            or target_divisor < 1 or common_part < 1
            or target_divisor % common_part):
        raise ValueError("invalid fixed common-layer controls")
    _squarefree_prime_factors(target_divisor)
    residual_limit = max(
        1, divisor_upper ** 2 // (target_divisor * common_part))
    bound = three_state_harmonic_receipt(residual_limit)
    omega_divisor = len(_squarefree_prime_factors(target_divisor))
    omega_common = len(_squarefree_prime_factors(common_part))
    range_condition = (
        X > divisor_upper
        and target_divisor * common_part
        > divisor_lower * divisor_upper)
    base_domination_range_condition = (
        X > divisor_upper
        and target_divisor > divisor_lower * divisor_upper)
    return {
        "X": X,
        "divisor_range": (divisor_lower, divisor_upper),
        "target_divisor": target_divisor,
        "common_part": common_part,
        "omega_divisor": omega_divisor,
        "omega_common_part": omega_common,
        "residual_limit": residual_limit,
        "three_state_harmonic_squared_bound": bound["exact_squared_bound"],
        "log_six_bound": bound["log_six_bound"],
        "fixed_common_layer_range_condition": range_condition,
        "base_domination_range_condition": base_domination_range_condition,
        "fixed_common_layer_polylog_bound_proved_for_reported_range": (
            range_condition),
        "fixed_common_base_to_no_common_factor": 2 ** omega_common,
        "separated_base_l1_to_no_common_factor": (3 / 2) ** omega_divisor,
        "separated_base_l2_to_no_common_factor": (5 / 4) ** omega_divisor,
        "fixed_common_base_domination_proved_for_reported_range": (
            base_domination_range_condition),
        "separated_base_energy_domination_proved_for_reported_range": (
            base_domination_range_condition),
        "common_layer_diagonal_interference_bound_proved": False,
    }


if __name__ == "__main__":
    for common in (1, 2, 6, 30):
        print(fixed_common_layer_polylog_receipt(
            128021 * 5311, 16, 404, 30030, common))

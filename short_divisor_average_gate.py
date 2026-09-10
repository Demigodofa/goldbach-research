"""Can averaging only the short divisor d rescue the Burgess deficit?

Use the most favorable direct benchmark: discard the composite-modulus cost,
work only at the prime component m=N^.59, and take the optimal licensed
Burgess parameter r=2.  Its excess over the direct H=N^.1 bound is .060625.
The whole d-family has length at most N^.009, so square-root cancellation
saves at most .0045 and even complete cancellation saves at most .009.
Neither closes the deficit.  This gates d-averaging alone, not coupled
spectral cancellation involving m, the primes, or the target shifts.
"""
from fractions import Fraction as F

from dual_burgess_gate import H, burgess_dual_exponent

D = F(9, 1000)
M = F(59, 100)


def favorable_burgess_deficit():
    return burgess_dual_exponent(2, M, H) - H


def r_continuous_derivative_numerator(r, q_exponent=M, shift_exponent=H):
    """Positive multiple of d/dr(E_r-H): (-B)r-2C."""
    if not isinstance(r, F) or r < 1:
        raise ValueError("exact r>=1 required")
    return (F(3, 4) * q_exponent - shift_exponent) * r - q_exponent / 2


def divisor_average_budget(divisor_exponent=D):
    if not isinstance(divisor_exponent, F) or not 0 <= divisor_exponent <= 1:
        raise ValueError("exact divisor exponent in [0,1] required")
    deficit = favorable_burgess_deficit()
    square_root = divisor_exponent / 2
    complete = divisor_exponent
    return {
        "optimistic_burgess_deficit": deficit,
        "square_root_d_gain": square_root,
        "residual_after_square_root": deficit - square_root,
        "complete_d_gain": complete,
        "residual_after_complete_d_cancellation": deficit - complete,
        "d_average_alone_closes": complete >= deficit,
    }

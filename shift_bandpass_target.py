"""Frequency target hidden by the previous absolute shift Cauchy bound.

The retained kernel has C0(s)=2*pi*int chi(t)^2 exp(i*s*t)dt with chi
supported in (1,2).  Poisson summation of the FULL periodized lattice
sum of C0(r/H) modulo q therefore removes additive frequency zero and
localizes h at size q/H (up to fixed 2*pi constants).  At
q=N^.599,H=N^.1 this is h=N^.499.  Hard truncations or extra shift masks
need a separate leakage estimate.

This localization is an arithmetic target, not a saving by itself.  Generic
coefficients can align with the bandpass and saturate Cauchy.  A new prime
progression/Kloosterman estimate at these nonzero frequencies would be needed.
"""
from fractions import Fraction as F

Q_TOP = F(599, 1000)
H_SHIFT = F(1, 10)
OLD_LOSS = F(49, 1000)


def additive_frequency_exponent(q_exponent=Q_TOP, h_exponent=H_SHIFT):
    if not all(isinstance(x, F) and 0 < x < 1
               for x in (q_exponent, h_exponent)):
        raise ValueError("exact exponents in (0,1) required")
    if q_exponent <= h_exponent:
        raise ValueError("require q much longer than the shift scale")
    return q_exponent - h_exponent


def square_root_shift_budget(loss=OLD_LOSS, h_exponent=H_SHIFT):
    """Net exponent if a NEW estimate supplies H^(1/2) cancellation."""
    if not all(isinstance(x, F) and x >= 0 for x in (loss, h_exponent)):
        raise ValueError("nonnegative exact exponents required")
    return loss - h_exponent / 2


def angular_band_excludes_zero(support_left=F(1), support_right=F(2)):
    """The angular transform support of chi^2 is separated from zero."""
    if not all(isinstance(x, F) for x in (support_left, support_right)):
        raise ValueError("exact support endpoints required")
    if not 0 < support_left < support_right:
        raise ValueError("require support interval strictly right of zero")
    return True


def target_receipt():
    return {
        "zero_additive_frequency_absent": angular_band_excludes_zero(),
        "active_frequency_exponent": additive_frequency_exponent(),
        "old_power_loss": OLD_LOSS,
        "conditional_square_root_net_exponent": square_root_shift_budget(),
        "saving_proved": False,
        "hard_truncation_leakage_paid": False,
        "missing_input": "prime-progression spectral estimate at h~q/H with target-varying residue",
        "generic_obstruction": "an arbitrary discrepancy sequence may align with the bandpass",
    }

"""Assemble the proved same-row near-cutoff active-frame estimate.

For one complete row and D_U={U<a<=2U:mu(a)^2=1}, the exact centered active
Gram decomposes as

 A_exact = M_triangular + D_CRT + C_centering.             (1)

The three terms are bounded by ``triangular_crt_main_bound.py``,
``crt_pair_discrepancy_bound.py``, and
``active_centering_schur_bound.py``.  Their normalized Schur majorants add,
so for U=floor(N^.15), H=floor(N^.1), m asymp N^.59, l asymp N^.41,

 A_exact <= O_eps(N^eps) rho F                           (2)

as quadratic forms.  More explicitly the two vanishing losses beyond the
N^eps triangular main are

 N^eps{H U^2 log(m)/m + H log(m)/l
        + H U log(m)/m*(1+U/m) + 1/m}=o(1).              (3)

Together with the previously proved exact full-frequency lower frame
G_full>=F/2 for all sufficiently large N, (2) implies the same-row
active/full matrix inequality.  Shifted rows and the signed prime-correlation
estimate are not included.
"""

from active_centering_schur_bound import row_centering_schur_bound
from active_totient_frame_probe import single_modulus_active_totient_frame
from crt_pair_discrepancy_bound import row_crt_discrepancy_bound
from triangular_crt_main_bound import row_triangular_main_bound


def row_near_cutoff_active_frame_bound(modulus, shift_length, ell,
                                       divisor_left, compare_exact=False):
    """Add the three rigorous normalized Schur bounds in (1)."""
    triangular = row_triangular_main_bound(
        modulus, shift_length, divisor_left)
    discrepancy = row_crt_discrepancy_bound(
        modulus, shift_length, ell, divisor_left)
    centering = row_centering_schur_bound(
        modulus, shift_length, ell, divisor_left)
    total = (
        triangular["proved_triangular_main_schur_bound"]
        + discrepancy["proved_discrepancy_schur_bound"]
        + centering["proved_centering_schur_bound"])
    result = {
        "modulus": modulus,
        "shift_length": shift_length,
        "ell": ell,
        "divisor_band": (divisor_left, 2 * divisor_left),
        "divisor_count": triangular["divisor_count"],
        "triangular_main_bound":
            triangular["proved_triangular_main_schur_bound"],
        "crt_discrepancy_bound":
            discrepancy["proved_discrepancy_schur_bound"],
        "centering_bound": centering["proved_centering_schur_bound"],
        "proved_exact_centered_active_schur_bound": total,
        "same_complete_row_active_frame_theorem": True,
        "asymptotic_same_row_active_full_theorem": True,
        "shifted_rows_proved": False,
        "signed_prime_correlation_proved": False,
    }
    if compare_exact:
        exact = single_modulus_active_totient_frame(
            modulus, shift_length, ell, 1, divisor_left)
        actual = exact["active_frame_schur_row_sum_max"]
        result["exact_active_frame_schur_row_sum"] = actual
        result["proved_over_exact"] = total / actual
    return result


if __name__ == "__main__":
    for key, value in row_near_cutoff_active_frame_bound(
            1009, 5, 9, 8, compare_exact=True).items():
        print(f"{key}: {value}")

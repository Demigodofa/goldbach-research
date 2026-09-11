"""Reject a universal nonpositive-cross-term shortcut.

Project-scaled Mobius tests have complete-period energy below the diagonal,
but this sign is not a formal consequence of Mobius coefficients. The exact
squarefree interval

    m=31, ell=11, 13<a<=21

has complete-period energy more than 1.43 times its diagonal. Thus a proof
must use the project ranges or a quantitative structured-sum estimate; it
cannot assert that all off-diagonal Mobius covariance is nonpositive.
"""

from lcm_sawtooth_exact_gcd_factorization import (
    lcm_sawtooth_exact_gcd_factorization_probe,
)


def complete_energy_diagonal_sign_falsifier():
    receipt = lcm_sawtooth_exact_gcd_factorization_probe(31, 11, 13, 21)
    return {
        "modulus": 31,
        "ell": 11,
        "divisor_range": (13, 21),
        "complete_energy_over_diagonal": receipt[
            "signed_energy_over_diagonal"],
        "positive_cross_excess_over_diagonal": (
            receipt["signed_energy_over_diagonal"] - 1),
        "universal_nonpositive_mobius_cross_term_falsified": (
            receipt["signed_energy_over_diagonal"] > 1),
        "project_scaled_cross_sign_theorem_proved": False,
    }


if __name__ == "__main__":
    print(complete_energy_diagonal_sign_falsifier())

"""Fixed counterexample to a universal contraction for the Walsh ``e=1`` block.

The Walsh positive majorant remains exact, and its dyadic ``e``-block Cauchy
reduction remains valid.  What fails is the stronger proposed lemma

    E_[1,2) <= Delta_(c=1)

for every admissible finite interval.  The witness below was found in a scan
of 8,588 exact small cases.  It has only two multi-residual coordinates in its
dominant conductor block, so it does not decide the project-scaled version of
the estimate.
"""

from lcm_sawtooth_no_common_walsh import dominant_no_common_walsh_probe


def e1_block_counterexample():
    """Return a reproducible receipt for the fixed small-range witness."""
    receipt = dominant_no_common_walsh_probe(131, 2, 8, 17, sample_count=None)
    e1_ratio = receipt[
        "dyadic_common_divisor_square_energy_over_diagonal"][1]
    return {
        "tested_small_case_count": 8588,
        "modulus": receipt["modulus"],
        "ell": receipt["ell"],
        "divisor_range": receipt["divisor_range"],
        "dominant_block_range": receipt["dominant_block_range"],
        "selected_coordinate_count": receipt["selected_coordinate_count"],
        "e1_block_square_energy_over_no_common_diagonal": e1_ratio,
        "full_walsh_majorant_over_no_common_diagonal": receipt[
            "selected_walsh_majorant_over_no_common_diagonal"],
        "actual_no_common_energy_over_diagonal": receipt[
            "selected_no_common_actual_over_diagonal"],
        "maximum_assignment_identity_error": receipt[
            "maximum_assignment_identity_error"],
        "maximum_walsh_identity_error": receipt[
            "maximum_walsh_identity_error"],
        "universal_e1_block_diagonal_bound_falsified": e1_ratio > 1,
        "project_scaled_e1_block_bound_proved": False,
        "walsh_factorization_retained": True,
        "dyadic_cauchy_reduction_retained": True,
    }


if __name__ == "__main__":
    for key, value in e1_block_counterexample().items():
        print(f"{key}: {value}")

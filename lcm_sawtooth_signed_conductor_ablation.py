"""Test whether one conductor controls the finite effective-log fit.

For the complete prime block, remove each Fourier conductor from both the
active/full residue forms and the one-frequency arithmetic covariance.  Then
recompute the axial Schur response and its best moment-curve parameter.  This
is a signed-interaction ablation: unlike positive conductor statistics, it
allows the active-minus-half-full matrix and its Schur inverse to determine
the response.

The declared sparse upper-support hypothesis requires some omission to move
the fitted parameter by at least ``.005`` and the largest mover to belong to
the upper half of the conductor support.  A finite pass would identify a
candidate mechanism, not prove uniform control or prime correlation.
"""

from itertools import combinations

from lcm_sawtooth_axial_moment_curve import (
    project_axial_moment_curve_receipt,
)
from lcm_sawtooth_incomplete_frequency import _quadratic_support_data


def classify_conductor_ablation(rows, upper_conductors, threshold=.005):
    """Apply the predeclared magnitude and upper-support falsifiers."""
    rows = tuple(rows)
    upper_conductors = frozenset(upper_conductors)
    if not rows:
        raise ValueError("at least one ablation row is required")
    if threshold <= 0:
        raise ValueError("threshold must be positive")
    largest = max(rows, key=lambda row: abs(row["parameter_shift"]))
    magnitude_passes = abs(largest["parameter_shift"]) >= threshold
    location_passes = largest["excluded_conductor"] in upper_conductors
    return {
        "largest_influence_conductor": largest["excluded_conductor"],
        "largest_absolute_parameter_shift": abs(largest["parameter_shift"]),
        "influence_threshold": threshold,
        "magnitude_falsifier_passes": magnitude_passes,
        "upper_half_location_falsifier_passes": location_passes,
        "sparse_upper_conductor_hypothesis_passes": bool(
            magnitude_passes and location_passes),
    }


def classify_pair_interactions(
        rows, absolute_threshold=.00025, relative_threshold=.25):
    """Apply the declared absolute and relative nonadditivity thresholds."""
    rows = tuple(rows)
    if not rows:
        raise ValueError("at least one pair row is required")
    if absolute_threshold <= 0 or relative_threshold <= 0:
        raise ValueError("interaction thresholds must be positive")
    qualifying = tuple(
        row["conductors"] for row in rows
        if (abs(row["interaction_shift"]) >= absolute_threshold
            and row["relative_interaction"] >= relative_threshold))
    largest = max(rows, key=lambda row: abs(row["interaction_shift"]))
    return {
        "absolute_interaction_threshold": absolute_threshold,
        "relative_interaction_threshold": relative_threshold,
        "qualifying_interaction_pairs": qualifying,
        "largest_interaction_pair": largest["conductors"],
        "largest_absolute_interaction_shift": abs(
            largest["interaction_shift"]),
        "largest_interaction_relative_to_single_magnitudes": largest[
            "relative_interaction"],
        "nonlinear_pair_interaction_hypothesis_passes": bool(qualifying),
    }


def project_signed_conductor_ablation_receipt(scale_modulus):
    """Return the complete leave-one-conductor-out moment-fit receipt."""
    baseline = project_axial_moment_curve_receipt(scale_modulus)
    support = tuple(sorted(
        conductor for conductor, _ in _quadratic_support_data(
            *baseline["divisor_range"])[1]))
    upper_conductors = support[len(support) // 2:]
    baseline_parameter = baseline["best_parameter"]
    if baseline_parameter is None:
        raise ArithmeticError("baseline moment-curve fit selected infinity")
    rows = []
    for conductor in support:
        ablated = project_axial_moment_curve_receipt(
            scale_modulus, (conductor,))
        parameter = ablated["best_parameter"]
        if parameter is None:
            raise ArithmeticError(
                f"ablation of conductor {conductor} selected infinity")
        rows.append({
            "excluded_conductor": conductor,
            "best_parameter": parameter,
            "parameter_shift": parameter - baseline_parameter,
            "projective_moment_curve_distance": ablated[
                "projective_moment_curve_distance"],
        })
    classification = classify_conductor_ablation(
        rows, upper_conductors)
    return {
        "scale_modulus": scale_modulus,
        "divisor_range": baseline["divisor_range"],
        "conductor_support": support,
        "upper_half_conductors": upper_conductors,
        "baseline_best_parameter": baseline_parameter,
        "baseline_projective_moment_curve_distance": baseline[
            "projective_moment_curve_distance"],
        "rows": tuple(rows),
        **classification,
        "finite_leave_one_conductor_out_test_completed": True,
        "uniform_effective_log_mechanism_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


def project_cluster_pair_interaction_receipt(scale_modulus, conductors):
    """Measure pair nonadditivity within a selected conductor cluster."""
    conductors = tuple(sorted(set(conductors)))
    if (len(conductors) < 2
            or any(type(value) is not int or value < 2
                   for value in conductors)):
        raise ValueError("require at least two distinct integer conductors")
    baseline = project_axial_moment_curve_receipt(scale_modulus)
    baseline_parameter = baseline["best_parameter"]
    if baseline_parameter is None:
        raise ArithmeticError("baseline moment-curve fit selected infinity")
    single_shifts = {}
    for conductor in conductors:
        parameter = project_axial_moment_curve_receipt(
            scale_modulus, (conductor,))["best_parameter"]
        if parameter is None:
            raise ArithmeticError(
                f"ablation of conductor {conductor} selected infinity")
        single_shifts[conductor] = parameter - baseline_parameter

    rows = []
    for left, right in combinations(conductors, 2):
        parameter = project_axial_moment_curve_receipt(
            scale_modulus, (left, right))["best_parameter"]
        if parameter is None:
            raise ArithmeticError(
                f"ablation of conductors {left},{right} selected infinity")
        joint_shift = parameter - baseline_parameter
        additive = single_shifts[left] + single_shifts[right]
        interaction = joint_shift - additive
        single_magnitude = (
            abs(single_shifts[left]) + abs(single_shifts[right]))
        if single_magnitude:
            relative = abs(interaction) / single_magnitude
        else:
            relative = float("inf") if interaction else 0.0
        if not additive:
            relation = "no_additive_prediction"
        elif interaction * additive > 0:
            relation = "reinforcement"
        else:
            relation = "cancellation"
        rows.append({
            "conductors": (left, right),
            "joint_best_parameter": parameter,
            "left_single_shift": single_shifts[left],
            "right_single_shift": single_shifts[right],
            "additive_shift_prediction": additive,
            "joint_parameter_shift": joint_shift,
            "interaction_shift": interaction,
            "relative_interaction": relative,
            "interaction_relation_to_additive_prediction": relation,
        })
    classification = classify_pair_interactions(rows)
    return {
        "scale_modulus": scale_modulus,
        "conductors": conductors,
        "baseline_best_parameter": baseline_parameter,
        "single_parameter_shifts": tuple(
            (conductor, single_shifts[conductor])
            for conductor in conductors),
        "rows": tuple(rows),
        **classification,
        "finite_nonlinear_pair_interaction_measured": True,
        "uniform_effective_log_mechanism_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(project_signed_conductor_ablation_receipt(127))

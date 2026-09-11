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

import numpy as np

from lcm_sawtooth_axial_moment_curve import (
    axial_moment_curve_fit_from_difference,
    axial_moment_curve_fit_from_frame,
    project_axial_moment_curve_receipt,
    trace_traceless_difference_from_frame,
)
from lcm_sawtooth_arithmetic_covariance_basis import (
    covariance_inverse_root,
    project_one_frequency_covariance,
)
from lcm_sawtooth_centered_basis_gershgorin import (
    symmetric_square_transform,
)
from lcm_sawtooth_incomplete_frequency import _quadratic_support_data
from lcm_sawtooth_lifted_endpoint_frame import (
    lifted_endpoint_residue_gram_receipt,
    project_prime_block_lifted_endpoint_scan,
)
from lcm_sawtooth_trace_traceless_block_frame import (
    trace_traceless_transform,
)


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


def project_frozen_whitening_interaction_receipt(
        scale_modulus, conductors, retention_threshold=.75):
    """Compare a pair interaction with baseline whitening held fixed."""
    conductors = tuple(sorted(set(conductors)))
    if (len(conductors) != 2
            or any(type(value) is not int or value < 2
                   for value in conductors)):
        raise ValueError("require exactly two distinct integer conductors")
    if not 0 < retention_threshold <= 1:
        raise ValueError("retention threshold must lie in (0,1]")
    recomputed = project_cluster_pair_interaction_receipt(
        scale_modulus, conductors)
    recomputed_row = recomputed["rows"][0]
    recomputed_interaction = recomputed_row["interaction_shift"]
    if not recomputed_interaction:
        raise ArithmeticError("recomputed pair interaction is zero")

    baseline_frame = project_prime_block_lifted_endpoint_scan(scale_modulus)
    covariance, _ = project_one_frequency_covariance(
        scale_modulus, baseline_frame)
    baseline_transform, _ = covariance_inverse_root(covariance)

    def fitted_parameter(excluded=()):
        frame = (baseline_frame if not excluded
                 else project_prime_block_lifted_endpoint_scan(
                     scale_modulus, excluded))
        parameter = axial_moment_curve_fit_from_frame(
            frame, baseline_transform)["best_parameter"]
        if parameter is None:
            raise ArithmeticError(
                f"frozen-whitening ablation {excluded} selected infinity")
        return parameter

    baseline_parameter = fitted_parameter()
    left_parameter = fitted_parameter((conductors[0],))
    right_parameter = fitted_parameter((conductors[1],))
    joint_parameter = fitted_parameter(conductors)
    left_shift = left_parameter - baseline_parameter
    right_shift = right_parameter - baseline_parameter
    joint_shift = joint_parameter - baseline_parameter
    frozen_interaction = joint_shift - left_shift - right_shift
    retained_fraction = abs(frozen_interaction / recomputed_interaction)
    same_sign = frozen_interaction * recomputed_interaction > 0
    passes = same_sign and retained_fraction >= retention_threshold
    return {
        "scale_modulus": scale_modulus,
        "conductors": conductors,
        "retention_threshold": retention_threshold,
        "recomputed_whitening_interaction_shift": recomputed_interaction,
        "frozen_whitening_left_shift": left_shift,
        "frozen_whitening_right_shift": right_shift,
        "frozen_whitening_joint_shift": joint_shift,
        "frozen_whitening_interaction_shift": frozen_interaction,
        "interaction_retained_fraction": retained_fraction,
        "interaction_sign_preserved": same_sign,
        "frozen_whitening_retention_hypothesis_passes": bool(passes),
        "uniform_effective_log_mechanism_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


def project_pair_matrix_interaction_receipt(
        scale_modulus, conductors, dominance_threshold=.75):
    """Split fixed-whitening interaction at Boolean inclusion-exclusion."""
    conductors = tuple(sorted(set(conductors)))
    if (len(conductors) != 2
            or any(type(value) is not int or value < 2
                   for value in conductors)):
        raise ValueError("require exactly two distinct integer conductors")
    if not 0 < dominance_threshold <= 1:
        raise ValueError("dominance threshold must lie in (0,1]")

    exclusions = ((), (conductors[0],), (conductors[1],), conductors)
    frames = {
        excluded: project_prime_block_lifted_endpoint_scan(
            scale_modulus, excluded)
        for excluded in exclusions
    }
    covariance, _ = project_one_frequency_covariance(
        scale_modulus, frames[()])
    baseline_transform, _ = covariance_inverse_root(covariance)
    differences = {
        excluded: trace_traceless_difference_from_frame(
            frame, baseline_transform)
        for excluded, frame in frames.items()
    }
    left = (conductors[0],)
    right = (conductors[1],)
    additive = differences[left] + differences[right] - differences[()]
    cross = differences[conductors] - additive
    fits = {
        excluded: axial_moment_curve_fit_from_difference(
            difference, baseline_transform)["best_parameter"]
        for excluded, difference in differences.items()
    }
    additive_parameter = axial_moment_curve_fit_from_difference(
        additive, baseline_transform)["best_parameter"]
    if additive_parameter is None or any(
            parameter is None for parameter in fits.values()):
        raise ArithmeticError("matrix decomposition selected infinity")

    total_interaction = (
        fits[conductors] - fits[left] - fits[right] + fits[()])
    matrix_cross_output = fits[conductors] - additive_parameter
    downstream_output = (
        additive_parameter - fits[left] - fits[right] + fits[()])
    if not total_interaction:
        raise ArithmeticError("total fixed-whitening interaction is zero")
    cross_fraction = abs(matrix_cross_output / total_interaction)
    cross_same_sign = matrix_cross_output * total_interaction > 0

    additive_traceless = additive[1:, 1:]
    exact_traceless = differences[conductors][1:, 1:]
    cross_traceless = cross[1:, 1:]
    additive_values, additive_vectors = np.linalg.eigh(additive_traceless)
    exact_values, exact_vectors = np.linalg.eigh(exact_traceless)
    additive_weakest = additive_vectors[:, 0]
    exact_weakest = exact_vectors[:, 0]
    cross_norm = float(np.linalg.norm(cross, "fro"))
    single_change_norm = float(
        np.linalg.norm(differences[left] - differences[()], "fro")
        + np.linalg.norm(differences[right] - differences[()], "fro"))
    if not single_change_norm:
        raise ArithmeticError("both single-removal matrix changes are zero")
    positivity_restored = bool(
        additive_values[0] < 0 < exact_values[0])
    dominance_passes = bool(
        cross_same_sign and cross_fraction >= dominance_threshold)
    return {
        "scale_modulus": scale_modulus,
        "conductors": conductors,
        "dominance_threshold": dominance_threshold,
        "total_frozen_whitening_interaction_shift": total_interaction,
        "matrix_cross_output_shift": matrix_cross_output,
        "downstream_nonlinear_output_shift": downstream_output,
        "decomposition_residual": (
            total_interaction - matrix_cross_output - downstream_output),
        "matrix_cross_output_fraction": cross_fraction,
        "matrix_cross_output_sign_preserved": cross_same_sign,
        "matrix_cross_output_dominance_hypothesis_passes": dominance_passes,
        "matrix_cross_frobenius_norm": cross_norm,
        "matrix_cross_relative_to_single_change_norms": (
            cross_norm / single_change_norm),
        "additive_surrogate_traceless_smallest_eigenvalue": float(
            additive_values[0]),
        "exact_joint_traceless_smallest_eigenvalue": float(exact_values[0]),
        "cross_restores_traceless_positive_definiteness": positivity_restored,
        "cross_rayleigh_on_additive_weakest_direction": float(
            additive_weakest @ cross_traceless @ additive_weakest),
        "exact_rayleigh_on_additive_weakest_direction": float(
            additive_weakest @ exact_traceless @ additive_weakest),
        "additive_rayleigh_on_exact_weakest_direction": float(
            exact_weakest @ additive_traceless @ exact_weakest),
        "cross_rayleigh_on_exact_weakest_direction": float(
            exact_weakest @ cross_traceless @ exact_weakest),
        "weakest_direction_absolute_overlap": abs(float(
            additive_weakest @ exact_weakest)),
        "finite_pair_matrix_interaction_decomposed": True,
        "uniform_effective_log_mechanism_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


def project_cluster_matrix_stabilization_receipt(
        scale_modulus, pairs, minimum_restoration_fraction=.75):
    """Test fragile-mode stabilization across selected conductor pairs."""
    pairs = tuple(tuple(sorted(set(pair))) for pair in pairs)
    if (not pairs or any(
            len(pair) != 2
            or any(type(value) is not int or value < 2 for value in pair)
            for pair in pairs)):
        raise ValueError("require at least one pair of distinct conductors")
    if not 0 < minimum_restoration_fraction <= 1:
        raise ValueError("restoration fraction must lie in (0,1]")
    rows = tuple(
        project_pair_matrix_interaction_receipt(scale_modulus, pair)
        for pair in pairs)
    positive_rayleigh_pairs = tuple(
        row["conductors"] for row in rows
        if row["cross_rayleigh_on_additive_weakest_direction"] > 0)
    restoration_pairs = tuple(
        row["conductors"] for row in rows
        if row["cross_restores_traceless_positive_definiteness"])
    restoration_fraction = len(restoration_pairs) / len(rows)
    all_positive = len(positive_rayleigh_pairs) == len(rows)
    passes = bool(
        all_positive
        and restoration_fraction >= minimum_restoration_fraction)
    return {
        "scale_modulus": scale_modulus,
        "pairs": pairs,
        "minimum_restoration_fraction": minimum_restoration_fraction,
        "rows": rows,
        "positive_fragile_direction_rayleigh_pairs": positive_rayleigh_pairs,
        "positive_definiteness_restoration_pairs": restoration_pairs,
        "positive_definiteness_restoration_fraction": restoration_fraction,
        "all_pair_cross_rayleigh_contributions_positive": all_positive,
        "cluster_fragile_mode_stabilization_hypothesis_passes": passes,
        "finite_cluster_matrix_stabilization_measured": True,
        "uniform_pair_matrix_stabilization_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


def project_primewise_pair_rayleigh_receipt(
        scale_modulus, conductors, nonnegative_fraction_threshold=.75,
        maximum_positive_mass_share=.25):
    """Decompose a fixed aggregate fragile-direction contribution by prime."""
    conductors = tuple(sorted(set(conductors)))
    if (len(conductors) != 2
            or any(type(value) is not int or value < 2
                   for value in conductors)):
        raise ValueError("require exactly two distinct integer conductors")
    if not 0 < nonnegative_fraction_threshold <= 1:
        raise ValueError("nonnegative fraction threshold must lie in (0,1]")
    if not 0 < maximum_positive_mass_share <= 1:
        raise ValueError("positive mass share cap must lie in (0,1]")

    exclusions = ((), (conductors[0],), (conductors[1],), conductors)
    frames = {
        excluded: project_prime_block_lifted_endpoint_scan(
            scale_modulus, excluded)
        for excluded in exclusions
    }
    covariance, _ = project_one_frequency_covariance(
        scale_modulus, frames[()])
    baseline_transform, _ = covariance_inverse_root(covariance)
    lifted_transform = symmetric_square_transform(
        baseline_transform) @ trace_traceless_transform()
    differences = {
        excluded: trace_traceless_difference_from_frame(
            frame, baseline_transform)
        for excluded, frame in frames.items()
    }
    left = (conductors[0],)
    right = (conductors[1],)
    additive = differences[left] + differences[right] - differences[()]
    _, additive_vectors = np.linalg.eigh(additive[1:, 1:])
    fragile = additive_vectors[:, 0]
    aggregate_cross = (
        differences[conductors] - differences[left]
        - differences[right] + differences[()])
    aggregate_rayleigh = float(
        fragile @ aggregate_cross[1:, 1:] @ fragile)

    row_count = frames[()]["row_count"]
    ell_freeze = frames[()]["ell_freeze"]
    divisor_lower, divisor_upper = frames[()]["divisor_range"]
    rows = []
    for frame_row in frames[()]["rows"]:
        modulus = frame_row["modulus"]
        prime_differences = {}
        prime_active = {}
        prime_full = {}
        for excluded in exclusions:
            receipt = lifted_endpoint_residue_gram_receipt(
                modulus, row_count, ell_freeze,
                divisor_lower, divisor_upper, excluded)
            active_gram = np.asarray(
                receipt["active_window_residue_energy_gram"])
            full_gram = np.asarray(receipt["full_residue_energy_gram"])
            active = lifted_transform.T @ active_gram @ lifted_transform
            full = lifted_transform.T @ full_gram @ lifted_transform
            prime_active[excluded] = (active + active.T) / 2
            prime_full[excluded] = (full + full.T) / 2
            prime_differences[excluded] = (
                prime_active[excluded] - .5 * prime_full[excluded])
        prime_cross = (
            prime_differences[conductors] - prime_differences[left]
            - prime_differences[right] + prime_differences[()])
        active_cross = (
            prime_active[conductors] - prime_active[left]
            - prime_active[right] + prime_active[()])
        full_cross = (
            prime_full[conductors] - prime_full[left]
            - prime_full[right] + prime_full[()])
        rows.append({
            "modulus": modulus,
            "fragile_direction_cross_rayleigh": float(
                fragile @ prime_cross[1:, 1:] @ fragile),
            "active_window_cross_rayleigh": float(
                fragile @ active_cross[1:, 1:] @ fragile),
            "minus_half_full_cross_rayleigh": float(
                -.5 * fragile @ full_cross[1:, 1:] @ fragile),
        })

    contribution_sum = sum(
        row["fragile_direction_cross_rayleigh"] for row in rows)
    nonnegative_count = sum(
        row["fragile_direction_cross_rayleigh"] >= 0 for row in rows)
    nonnegative_fraction = nonnegative_count / len(rows)
    positive_mass = sum(
        max(0.0, row["fragile_direction_cross_rayleigh"])
        for row in rows)
    negative_mass = -sum(
        min(0.0, row["fragile_direction_cross_rayleigh"])
        for row in rows)
    if not positive_mass:
        raise ArithmeticError("primewise decomposition has no positive mass")
    largest_positive = max(
        rows, key=lambda row: row["fragile_direction_cross_rayleigh"])
    largest_share = (
        largest_positive["fragile_direction_cross_rayleigh"] / positive_mass)
    fraction_passes = (
        nonnegative_fraction >= nonnegative_fraction_threshold)
    concentration_passes = largest_share <= maximum_positive_mass_share

    def component_summary(key):
        values = tuple(row[key] for row in rows)
        component_positive_mass = sum(max(0.0, value) for value in values)
        if not component_positive_mass:
            raise ArithmeticError(f"{key} has no positive mass")
        component_nonnegative_count = sum(value >= 0 for value in values)
        largest_index = max(range(len(rows)), key=lambda index: values[index])
        component_largest_share = (
            values[largest_index] / component_positive_mass)
        component_fraction = component_nonnegative_count / len(rows)
        return {
            "sum": sum(values),
            "positive_mass": component_positive_mass,
            "negative_mass": -sum(min(0.0, value) for value in values),
            "nonnegative_count": component_nonnegative_count,
            "nonnegative_fraction": component_fraction,
            "largest_positive_contributor": rows[largest_index]["modulus"],
            "largest_positive_mass_share": component_largest_share,
            "broad_sign_falsifier_passes": bool(
                component_fraction >= nonnegative_fraction_threshold
                and component_largest_share <= maximum_positive_mass_share),
        }

    active_summary = component_summary("active_window_cross_rayleigh")
    full_subtraction_summary = component_summary(
        "minus_half_full_cross_rayleigh")
    return {
        "scale_modulus": scale_modulus,
        "conductors": conductors,
        "prime_count": len(rows),
        "nonnegative_fraction_threshold": nonnegative_fraction_threshold,
        "maximum_positive_mass_share": maximum_positive_mass_share,
        "rows": tuple(rows),
        "nonnegative_prime_count": nonnegative_count,
        "nonnegative_prime_fraction": nonnegative_fraction,
        "positive_rayleigh_mass": positive_mass,
        "negative_rayleigh_mass": negative_mass,
        "primewise_rayleigh_sum": contribution_sum,
        "aggregate_cross_rayleigh": aggregate_rayleigh,
        "primewise_aggregate_residual": contribution_sum - aggregate_rayleigh,
        "largest_positive_contributor": largest_positive["modulus"],
        "largest_positive_mass_share": largest_share,
        "nonnegative_fraction_falsifier_passes": fraction_passes,
        "positive_mass_concentration_falsifier_passes": concentration_passes,
        "broad_primewise_sign_hypothesis_passes": bool(
            fraction_passes and concentration_passes),
        "active_window_component": active_summary,
        "minus_half_full_component": full_subtraction_summary,
        "active_component_broad_sign_hypothesis_passes": active_summary[
            "broad_sign_falsifier_passes"],
        "full_subtraction_broad_sign_candidate_passes": (
            full_subtraction_summary["broad_sign_falsifier_passes"]),
        "uniform_primewise_cross_rayleigh_sign_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


def project_active_full_pair_rayleigh_split_receipt(
        scale_modulus, conductors, active_fraction_threshold=.75):
    """Split a fragile-direction Boolean contribution into active and full."""
    conductors = tuple(sorted(set(conductors)))
    if (len(conductors) != 2
            or any(type(value) is not int or value < 2
                   for value in conductors)):
        raise ValueError("require exactly two distinct integer conductors")
    if not 0 < active_fraction_threshold <= 1:
        raise ValueError("active fraction threshold must lie in (0,1]")

    exclusions = ((), (conductors[0],), (conductors[1],), conductors)
    frames = {
        excluded: project_prime_block_lifted_endpoint_scan(
            scale_modulus, excluded)
        for excluded in exclusions
    }
    covariance, _ = project_one_frequency_covariance(
        scale_modulus, frames[()])
    baseline_transform, _ = covariance_inverse_root(covariance)
    transform = symmetric_square_transform(
        baseline_transform) @ trace_traceless_transform()

    def transformed(frame, key):
        gram = np.asarray(frame[key])
        result = transform.T @ gram @ transform
        return (result + result.T) / 2

    active = {
        excluded: transformed(
            frame, "aggregate_active_window_residue_energy_gram")
        for excluded, frame in frames.items()
    }
    full = {
        excluded: transformed(
            frame, "aggregate_full_residue_energy_gram")
        for excluded, frame in frames.items()
    }
    difference = {
        excluded: active[excluded] - .5 * full[excluded]
        for excluded in exclusions
    }
    left = (conductors[0],)
    right = (conductors[1],)
    additive = difference[left] + difference[right] - difference[()]
    _, vectors = np.linalg.eigh(additive[1:, 1:])
    fragile = vectors[:, 0]

    def boolean_cross(parts):
        return (
            parts[conductors] - parts[left] - parts[right] + parts[()])

    active_rayleigh = float(
        fragile @ boolean_cross(active)[1:, 1:] @ fragile)
    full_rayleigh = float(
        fragile @ boolean_cross(full)[1:, 1:] @ fragile)
    full_subtraction_rayleigh = -.5 * full_rayleigh
    net_rayleigh = active_rayleigh + full_subtraction_rayleigh
    if net_rayleigh <= 0:
        raise ArithmeticError("net Boolean cross Rayleigh must be positive")
    active_fraction = active_rayleigh / net_rayleigh
    active_passes = bool(
        active_rayleigh > 0
        and active_fraction >= active_fraction_threshold)
    return {
        "scale_modulus": scale_modulus,
        "conductors": conductors,
        "active_fraction_threshold": active_fraction_threshold,
        "active_window_boolean_cross_rayleigh": active_rayleigh,
        "full_residue_boolean_cross_rayleigh": full_rayleigh,
        "minus_half_full_boolean_cross_rayleigh": full_subtraction_rayleigh,
        "net_boolean_cross_rayleigh": net_rayleigh,
        "active_window_fraction_of_net_reinforcement": active_fraction,
        "full_subtraction_fraction_of_net_reinforcement": (
            full_subtraction_rayleigh / net_rayleigh),
        "full_subtraction_reinforces_fragile_direction": bool(
            full_subtraction_rayleigh > 0),
        "active_window_leading_hypothesis_passes": active_passes,
        "finite_active_full_boolean_rayleigh_split_measured": True,
        "uniform_active_window_cross_rayleigh_sign_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


def project_cluster_primewise_component_receipt(
        scale_modulus, pairs, minimum_passing_fraction=.75):
    """Test whether either primewise component is broad across a cluster."""
    pairs = tuple(tuple(sorted(set(pair))) for pair in pairs)
    if (not pairs or any(
            len(pair) != 2
            or any(type(value) is not int or value < 2 for value in pair)
            for pair in pairs)):
        raise ValueError("require at least one pair of distinct conductors")
    if not 0 < minimum_passing_fraction <= 1:
        raise ValueError("passing fraction must lie in (0,1]")
    rows = tuple(
        project_primewise_pair_rayleigh_receipt(scale_modulus, pair)
        for pair in pairs)
    active_broad_pairs = tuple(
        row["conductors"] for row in rows
        if row["active_component_broad_sign_hypothesis_passes"])
    full_subtraction_broad_pairs = tuple(
        row["conductors"] for row in rows
        if row["full_subtraction_broad_sign_candidate_passes"])
    active_fraction = len(active_broad_pairs) / len(rows)
    full_fraction = len(full_subtraction_broad_pairs) / len(rows)
    return {
        "scale_modulus": scale_modulus,
        "pairs": pairs,
        "minimum_passing_fraction": minimum_passing_fraction,
        "rows": rows,
        "active_component_broad_pairs": active_broad_pairs,
        "full_subtraction_broad_pairs": full_subtraction_broad_pairs,
        "active_component_cluster_passing_fraction": active_fraction,
        "full_subtraction_cluster_passing_fraction": full_fraction,
        "active_component_cluster_hypothesis_passes": bool(
            active_fraction >= minimum_passing_fraction),
        "full_subtraction_cluster_hypothesis_passes": bool(
            full_fraction >= minimum_passing_fraction),
        "uniform_primewise_component_sign_proved": False,
        "uniform_active_full_lower_frame_proved": False,
        "signed_prime_correlation_proved": False,
    }


if __name__ == "__main__":
    print(project_signed_conductor_ablation_receipt(127))

"""Walsh factorization of the dominant no-common assignment layer.

For the exact common part ``d_C=1``, write ``d=u*v``, ``a=u*alpha`` and
``b=v*beta``.  After factoring the fixed sign ``mu(d)``, the collapsed layer
has the exact divisor convolution

    T_(d,1) = mu(d)/d sum_e phi(e) sum_(u|d) F_(u,e) F_(d/u,e),

where

    F_(u,e) = sum_(alpha: e|alpha, (alpha,d)=1,
                         V<u*alpha<=B) mu(alpha)L_(u*alpha)/alpha.

On the Boolean divisor group of squarefree ``d``, Walsh inversion writes the
inner convolution as the difference between even- and odd-character spectral
squares.  This preserves the polynomial weights and gives an exact candidate
mechanism for left/right assignment cancellation.
"""

import math

from divisor_full_frame_probe import _totient
from lcm_sawtooth_exact_gcd_factorization import (
    _squarefree_divisors_with_complement_mobius,
    sawtooth_gcd_mobius_transform,
)
from lcm_sawtooth_high_d_assignment import _squarefree_prime_factors
from lcm_sawtooth_no_common_polylog import three_state_harmonic_receipt
from lcm_sawtooth_residual_cube import (
    residual_cube_closed_form,
    truncated_residual_cube,
)
from lcm_sawtooth_structured_divisor_sum import _coefficient_data
from mobius_covariance_endpoint_probe import _prime_flags


def _walsh_transform(values):
    transformed = list(values)
    width = 1
    while width < len(transformed):
        for start in range(0, len(transformed), 2 * width):
            for offset in range(width):
                left = transformed[start + offset]
                right = transformed[start + width + offset]
                transformed[start + offset] = left + right
                transformed[start + width + offset] = left - right
        width *= 2
    return tuple(transformed)


def _divisor_from_mask(primes, mask):
    value = 1
    for index, prime in enumerate(primes):
        if mask & (1 << index):
            value *= prime
    return value


def _target_receipt(
        modulus, ell, divisor_lower, divisor_upper, target_divisor, data=None,
        direct_value=None):
    if data is None:
        data = _coefficient_data(
            modulus, ell, divisor_lower, divisor_upper)
    mobius, divisors, coefficients, _ = data
    primes = _squarefree_prime_factors(target_divisor)
    group_size = 1 << len(primes)
    divisor_by_mask = tuple(
        _divisor_from_mask(primes, mask) for mask in range(group_size))
    mask_by_divisor = {
        divisor: mask for mask, divisor in enumerate(divisor_by_mask)}

    direct = direct_value
    if direct is None:
        direct = 0.0
        for left in divisors:
            for right in divisors:
                q = math.lcm(left, right)
                if (q % target_divisor == 0 and math.gcd(
                        target_divisor, math.gcd(left, right)) == 1):
                    direct += coefficients[left] * coefficients[right] / q

    values_by_e = {}
    X = modulus * ell
    for value in divisors:
        assigned_part = math.gcd(value, target_divisor)
        if assigned_part not in mask_by_divisor:
            continue
        alpha = value // assigned_part
        if math.gcd(alpha, target_divisor) != 1:
            continue
        base_term = int(mobius[alpha]) * math.log(X / value) / alpha
        for common_divisor, _ in (
                _squarefree_divisors_with_complement_mobius(alpha)):
            values_by_e.setdefault(common_divisor, [0.0] * group_size)[
                mask_by_divisor[assigned_part]] += base_term

    even_mass = odd_mass = 0.0
    positive_majorant_by_common_divisor = {}
    paired_majorant_by_common_divisor = {}
    direct_assignment_convolution = 0.0
    walsh_assignment_convolution = 0.0
    paired_absolute_convolution = 0.0
    complement_mismatch_half_square = 0.0
    for common_divisor, values in values_by_e.items():
        weight = _totient(common_divisor)
        convolution = sum(
            values[mask] * values[(group_size - 1) ^ mask]
            for mask in range(group_size))
        paired_absolute = sum(
            abs(values[mask] * values[(group_size - 1) ^ mask])
            for mask in range(group_size))
        direct_assignment_convolution += weight * convolution
        transformed = _walsh_transform(values)
        even = sum(
            value ** 2 for mask, value in enumerate(transformed)
            if mask.bit_count() % 2 == 0) / group_size
        odd = sum(
            value ** 2 for mask, value in enumerate(transformed)
            if mask.bit_count() % 2 == 1) / group_size
        even_mass += weight * even
        odd_mass += weight * odd
        positive_majorant_by_common_divisor[common_divisor] = (
            weight * (even + odd) / target_divisor)
        paired_majorant_by_common_divisor[common_divisor] = (
            weight * paired_absolute / target_divisor)
        paired_absolute_convolution += weight * paired_absolute
        complement_mismatch_half_square += weight * 0.5 * sum(
            (abs(values[mask])
             - abs(values[(group_size - 1) ^ mask])) ** 2
            for mask in range(group_size))
        walsh_assignment_convolution += weight * (even - odd)
    expanded = (
        int(mobius[target_divisor]) / target_divisor
        * direct_assignment_convolution)
    walsh_expanded = (
        int(mobius[target_divisor]) / target_divisor
        * walsh_assignment_convolution)
    total_spectral_mass = even_mass + odd_mass
    positive_majorant = total_spectral_mass / target_divisor
    paired_positive_majorant = paired_absolute_convolution / target_divisor
    complement_magnitude_mismatch = (
        positive_majorant - paired_positive_majorant)
    complement_mismatch_half_square /= target_divisor
    paired_sign_incoherence = paired_positive_majorant - abs(direct)
    majorant_over_absolute_direct = (
        positive_majorant / abs(direct) if direct else float("inf"))
    paired_majorant_over_absolute_direct = (
        paired_positive_majorant / abs(direct) if direct else float("inf"))
    return {
        "target_divisor": target_divisor,
        "target_prime_factor_count": len(primes),
        "direct_no_common_collapsed_sum": direct,
        "assignment_convolution_sum": expanded,
        "walsh_expanded_sum": walsh_expanded,
        "assignment_identity_error": direct - expanded,
        "walsh_identity_error": direct - walsh_expanded,
        "even_walsh_mass": even_mass,
        "odd_walsh_mass": odd_mass,
        "walsh_positive_majorant": positive_majorant,
        "positive_majorant_by_common_divisor": tuple(sorted(
            positive_majorant_by_common_divisor.items())),
        "paired_majorant_by_common_divisor": tuple(sorted(
            paired_majorant_by_common_divisor.items())),
        "paired_support_positive_majorant": paired_positive_majorant,
        "complement_magnitude_mismatch": complement_magnitude_mismatch,
        "complement_mismatch_half_square": (
            complement_mismatch_half_square),
        "complement_mismatch_identity_error": (
            complement_magnitude_mismatch
            - complement_mismatch_half_square),
        "paired_sign_incoherence": paired_sign_incoherence,
        "walsh_loss_decomposition_error": (
            positive_majorant - abs(direct)
            - complement_magnitude_mismatch - paired_sign_incoherence),
        "walsh_majorant_over_absolute_sum": majorant_over_absolute_direct,
        "walsh_majorant_energy_factor": majorant_over_absolute_direct ** 2,
        "paired_majorant_over_absolute_sum": (
            paired_majorant_over_absolute_direct),
        "paired_majorant_energy_factor": (
            paired_majorant_over_absolute_direct ** 2),
        "walsh_parity_relative_imbalance": (
            abs(even_mass - odd_mass) / total_spectral_mass
            if total_spectral_mass else 0.0),
        "no_common_assignment_convolution_proved": True,
        "walsh_parity_square_identity_proved": True,
        "walsh_positive_majorant_proved": True,
        "paired_support_majorant_proved": True,
        "walsh_loss_decomposition_proved": True,
        "walsh_parity_cancellation_bound_proved": False,
    }


def no_common_walsh_probe(
        modulus, ell, divisor_lower, divisor_upper, target_divisor):
    """Verify the assignment convolution and Walsh-square identity at ``d``."""
    if any(type(value) is not int for value in (
            modulus, ell, divisor_lower, divisor_upper, target_divisor)):
        raise ValueError("all inputs must be integers")
    if (ell < 1 or divisor_lower < 1
            or divisor_upper <= divisor_lower or divisor_upper >= modulus
            or target_divisor < 1 or target_divisor > divisor_upper ** 2):
        raise ValueError("invalid no-common Walsh ranges")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")
    data = _coefficient_data(
        modulus, ell, divisor_lower, divisor_upper)
    if not data[1]:
        raise ValueError("the divisor interval has no squarefree values")
    _squarefree_prime_factors(target_divisor)
    return _target_receipt(
        modulus, ell, divisor_lower, divisor_upper, target_divisor, data)


def dominant_no_common_walsh_probe(
        modulus, ell, divisor_lower, divisor_upper, sample_count=8):
    """Test Walsh parity balance on the top no-common dominant conductors."""
    if (sample_count is not None
            and (type(sample_count) is not int or sample_count < 1)):
        raise ValueError("sample_count must be positive or None")
    if not _prime_flags(modulus)[modulus]:
        raise ValueError("modulus must be prime")
    data = _coefficient_data(
        modulus, ell, divisor_lower, divisor_upper)
    mobius, divisors, coefficients, lcm_coefficients = data
    if not divisors:
        raise ValueError("the divisor interval has no squarefree values")

    diagonal_by_divisor = {}
    residual_count_by_divisor = {}
    for q, coefficient in lcm_coefficients.items():
        for divisor, _ in _squarefree_divisors_with_complement_mobius(q):
            if divisor <= divisor_upper:
                continue
            weight = sawtooth_gcd_mobius_transform(modulus, divisor)
            if weight <= 0:
                continue
            diagonal_by_divisor[divisor] = (
                diagonal_by_divisor.get(divisor, 0.0) +
                weight * (coefficient / q) ** 2)
            residual_count_by_divisor[divisor] = (
                residual_count_by_divisor.get(divisor, 0) + 1)
    diagonal_by_block = {}
    for divisor, diagonal in diagonal_by_divisor.items():
        if residual_count_by_divisor[divisor] < 2:
            continue
        block = 1 << (divisor.bit_length() - 1)
        diagonal_by_block[block] = diagonal_by_block.get(block, 0.0) + diagonal
    no_common_sums = {}
    no_common_residual_terms = {}
    for left in divisors:
        for right in divisors:
            q = math.lcm(left, right)
            pair_term = coefficients[left] * coefficients[right] / q
            pair_common = math.gcd(left, right)
            for divisor, _ in _squarefree_divisors_with_complement_mobius(q):
                if (divisor <= divisor_upper
                        or math.gcd(divisor, pair_common) != 1):
                    continue
                no_common_sums[divisor] = (
                    no_common_sums.get(divisor, 0.0) + pair_term)
                residuals = no_common_residual_terms.setdefault(divisor, {})
                residuals[q] = residuals.get(q, 0.0) + pair_term
    entries = []
    for divisor, value in no_common_sums.items():
        if residual_count_by_divisor.get(divisor, 0) < 2:
            continue
        weight = sawtooth_gcd_mobius_transform(modulus, divisor)
        if weight <= 0:
            continue
        energy = weight * value ** 2
        block = 1 << (divisor.bit_length() - 1)
        entries.append((divisor, block, energy))
    if not diagonal_by_block or not entries:
        raise ArithmeticError("no positive no-common dominant support")
    dominant_lower = max(diagonal_by_block, key=diagonal_by_block.get)
    dominant_entries = sorted(
        (entry for entry in entries if entry[1] == dominant_lower),
        key=lambda entry: entry[2], reverse=True)
    selected = (
        dominant_entries if sample_count is None
        else dominant_entries[:sample_count])
    total_selected_energy = sum(entry[2] for entry in selected)
    total_block_energy = sum(entry[2] for entry in dominant_entries)
    selected_diagonal = sum(
        sawtooth_gcd_mobius_transform(modulus, divisor) * sum(
            term ** 2
            for term in no_common_residual_terms[divisor].values())
        for divisor, _, _ in selected)
    residual_mobius_aligned_energy = 0.0
    residual_mobius_signed_energy = 0.0
    complete_cube_energy = 0.0
    boundary_cube_energy = 0.0
    complete_boundary_cross_energy = 0.0
    complete_cube_pair_count = 0
    nonpositive_complete_cube_pair_count = 0
    minimum_complete_cube_relative_margin = 1.0
    truncated_cube_piece_count = 0
    nonpositive_truncated_cube_piece_count = 0
    minimum_truncated_cube_relative_margin = 1.0
    maximum_truncated_cube_reconstruction_error = 0.0
    complete_collapsed_by_divisor = {}
    boundary_collapsed_by_divisor = {}
    complete_residual_diagonal = 0.0
    complete_amplitudes_by_divisor = {}
    maximum_complete_residual = 1
    X = modulus * ell
    for divisor, _, _ in selected:
        weight = sawtooth_gcd_mobius_transform(modulus, divisor)
        divisor_primes = _squarefree_prime_factors(divisor)
        divisor_sign = (-1) ** len(divisor_primes)
        group_size = 1 << len(divisor_primes)
        for q, term in no_common_residual_terms[divisor].items():
            residual = q // divisor
            residual_primes = _squarefree_prime_factors(residual)
            residual_sign = (-1) ** len(residual_primes)
            energy = weight * term ** 2
            aligned_sign = divisor_sign * residual_sign * term
            if aligned_sign >= 0:
                residual_mobius_aligned_energy += energy
                residual_mobius_signed_energy += energy
            else:
                residual_mobius_signed_energy -= energy
            complete_value = 0.0
            reconstructed_value = 0.0
            for mask in range(group_size):
                left_part = _divisor_from_mask(divisor_primes, mask)
                right_part = divisor // left_part
                truncated = truncated_residual_cube(
                    X, left_part, right_part, divisor_lower, divisor_upper,
                    residual_primes)
                truncated_value = truncated["truncated_cube_sum"]
                if truncated["retained_assignment_count"]:
                    truncated_cube_piece_count += 1
                    if truncated_value <= 0:
                        nonpositive_truncated_cube_piece_count += 1
                    minimum_truncated_cube_relative_margin = min(
                        minimum_truncated_cube_relative_margin,
                        truncated_value / truncated["absolute_term_sum"])
                    reconstructed_value += (
                        divisor_sign * residual_sign * truncated_value
                        / (divisor * residual))
                if (not divisor_lower < left_part
                        or not divisor_lower < right_part
                        or left_part * residual > divisor_upper
                        or right_part * residual > divisor_upper):
                    continue
                log_left = math.log(X / left_part)
                log_right = math.log(X / right_part)
                closed = residual_cube_closed_form(
                    log_left, log_right, residual_primes)
                complete_cube_pair_count += 1
                if closed <= 0:
                    nonpositive_complete_cube_pair_count += 1
                minimum_complete_cube_relative_margin = min(
                    minimum_complete_cube_relative_margin,
                    closed / (log_left * log_right))
                complete_value += (
                    divisor_sign * residual_sign * closed
                    / (divisor * residual))
            maximum_truncated_cube_reconstruction_error = max(
                maximum_truncated_cube_reconstruction_error,
                abs(term - reconstructed_value))
            boundary_value = term - complete_value
            complete_cube_energy += weight * complete_value ** 2
            complete_residual_diagonal += weight * complete_value ** 2
            complete_collapsed_by_divisor[divisor] = (
                complete_collapsed_by_divisor.get(divisor, 0.0)
                + complete_value)
            boundary_collapsed_by_divisor[divisor] = (
                boundary_collapsed_by_divisor.get(divisor, 0.0)
                + boundary_value)
            complete_amplitudes_by_divisor.setdefault(divisor, {})[
                residual] = (
                    divisor_sign * residual_sign * divisor * residual
                    * complete_value)
            if complete_value:
                maximum_complete_residual = max(
                    maximum_complete_residual, residual)
            boundary_cube_energy += weight * boundary_value ** 2
            complete_boundary_cross_energy += (
                2 * weight * complete_value * boundary_value)
    complete_collapsed_energy = sum(
        sawtooth_gcd_mobius_transform(modulus, divisor) * value ** 2
        for divisor, value in complete_collapsed_by_divisor.items())
    boundary_collapsed_energy = sum(
        sawtooth_gcd_mobius_transform(modulus, divisor) * value ** 2
        for divisor, value in boundary_collapsed_by_divisor.items())
    collapsed_complete_boundary_cross = sum(
        2 * sawtooth_gcd_mobius_transform(modulus, divisor)
        * complete_collapsed_by_divisor[divisor]
        * boundary_collapsed_by_divisor[divisor]
        for divisor in complete_collapsed_by_divisor)
    complete_amplitude_monotonicity_violations = 0
    for amplitudes in complete_amplitudes_by_divisor.values():
        base = amplitudes.get(1, 0.0)
        complete_amplitude_monotonicity_violations += sum(
            amplitude < -1e-12 or amplitude > base + 1e-12
            for amplitude in amplitudes.values())
    actual_residual_amplitude_positivity_violations = 0
    maximum_actual_amplitude_over_base = 0.0
    maximum_nontrivial_amplitude_over_base = 0.0
    maximum_nontrivial_amplitude_over_tau_base = 0.0
    maximum_actual_amplitude_over_tau_squared_base = 0.0
    for divisor, _, _ in selected:
        divisor_sign = (-1) ** len(_squarefree_prime_factors(divisor))
        terms = no_common_residual_terms[divisor]
        base_term = terms.get(divisor, 0.0)
        base_amplitude = divisor_sign * divisor * base_term
        for q, term in terms.items():
            residual = q // divisor
            residual_primes = _squarefree_prime_factors(residual)
            residual_sign = (-1) ** len(residual_primes)
            amplitude = divisor_sign * residual_sign * q * term
            if amplitude < -1e-12:
                actual_residual_amplitude_positivity_violations += 1
            if base_amplitude > 0:
                maximum_actual_amplitude_over_base = max(
                    maximum_actual_amplitude_over_base,
                    amplitude / base_amplitude)
                if residual > 1:
                    maximum_nontrivial_amplitude_over_base = max(
                        maximum_nontrivial_amplitude_over_base,
                        amplitude / base_amplitude)
                    maximum_nontrivial_amplitude_over_tau_base = max(
                        maximum_nontrivial_amplitude_over_tau_base,
                        amplitude / ((1 << len(residual_primes))
                                     * base_amplitude))
                tau_squared = (1 << len(residual_primes)) ** 2
                maximum_actual_amplitude_over_tau_squared_base = max(
                    maximum_actual_amplitude_over_tau_squared_base,
                    amplitude / (tau_squared * base_amplitude))
    complete_harmonic_bound = (1 + math.log(maximum_complete_residual)) ** 2
    complete_range_condition = (
        X * math.sqrt(min(divisor for divisor, _, _ in selected))
        > divisor_upper ** 2)
    maximum_residual_limit = max(
        divisor_upper ** 2 // divisor for divisor, _, _ in selected)
    three_state_bound = three_state_harmonic_receipt(
        max(1, maximum_residual_limit))
    no_common_polylog_condition = (
        X > divisor_upper
        and min(divisor for divisor, _, _ in selected)
        > divisor_lower * divisor_upper)
    receipts = tuple(_target_receipt(
        modulus, ell, divisor_lower, divisor_upper, divisor, data,
        no_common_sums[divisor])
        for divisor, _, _ in selected)
    selected_majorant_energy = sum(
        energy * receipt["walsh_majorant_energy_factor"]
        for (_, _, energy), receipt in zip(selected, receipts))
    selected_paired_majorant_energy = sum(
        energy * receipt["paired_majorant_energy_factor"]
        for (_, _, energy), receipt in zip(selected, receipts))
    common_divisor_attribution = {}
    dyadic_square_energy = {}
    e1_coordinate_data = []
    for (divisor, _, _), receipt in zip(selected, receipts):
        weight = sawtooth_gcd_mobius_transform(modulus, divisor)
        majorant = receipt["walsh_positive_majorant"]
        components_by_block = {}
        for common_divisor, component in receipt[
                "positive_majorant_by_common_divisor"]:
            common_divisor_attribution[common_divisor] = (
                common_divisor_attribution.get(common_divisor, 0.0)
                + weight * majorant * component)
            block = 1 << (common_divisor.bit_length() - 1)
            components_by_block[block] = (
                components_by_block.get(block, 0.0) + component)
        for block, component in components_by_block.items():
            dyadic_square_energy[block] = (
                dyadic_square_energy.get(block, 0.0)
                + weight * component ** 2)
        coordinate_diagonal = weight * sum(
            term ** 2
            for term in no_common_residual_terms[divisor].values())
        e1_component = dict(receipt[
            "positive_majorant_by_common_divisor"]).get(1, 0.0)
        e1_energy = weight * e1_component ** 2
        e1_coordinate_data.append((
            divisor, coordinate_diagonal, e1_energy,
            e1_energy / coordinate_diagonal))
    attribution_total = sum(common_divisor_attribution.values())
    if abs(attribution_total - selected_majorant_energy) > max(
            1e-9, 1e-9 * selected_majorant_energy):
        raise ArithmeticError("common-divisor attribution failed")
    dyadic_common_divisor_attribution = {}
    for common_divisor, attribution in common_divisor_attribution.items():
        block = 1 << (common_divisor.bit_length() - 1)
        dyadic_common_divisor_attribution[block] = (
            dyadic_common_divisor_attribution.get(block, 0.0) + attribution)
    thresholds = (1, 2, 4, 8, 16, 32, 64)
    cumulative_attribution = {
        threshold: sum(
            attribution for common_divisor, attribution
            in common_divisor_attribution.items()
            if common_divisor <= threshold) / selected_majorant_energy
        for threshold in thresholds}
    dyadic_attribution_fractions = {
        block: attribution / selected_majorant_energy
        for block, attribution in sorted(
            dyadic_common_divisor_attribution.items())}
    effective_dyadic_block_count = 1 / sum(
        fraction ** 2 for fraction in dyadic_attribution_fractions.values())
    dyadic_square_energy_over_diagonal = {
        block: energy / selected_diagonal
        for block, energy in sorted(dyadic_square_energy.items())}
    dyadic_block_count = len(dyadic_square_energy)
    dyadic_cauchy_bound_over_diagonal = dyadic_block_count * sum(
        dyadic_square_energy_over_diagonal.values())
    e1_bad_coordinates = tuple(
        row for row in e1_coordinate_data if row[3] > 1)
    e1_total_energy = dyadic_square_energy.get(1, 0.0)
    e1_by_prime_factor_count = {}
    for divisor, coordinate_diagonal, e1_energy, _ in e1_coordinate_data:
        prime_factor_count = len(_squarefree_prime_factors(divisor))
        group = e1_by_prime_factor_count.setdefault(
            prime_factor_count, [0, 0.0, 0.0])
        group[0] += 1
        group[1] += coordinate_diagonal
        group[2] += e1_energy
    e1_prime_factor_receipt = {
        prime_factor_count: {
            "coordinate_count": group[0],
            "diagonal_fraction": group[1] / selected_diagonal,
            "e1_energy_fraction": (
                group[2] / e1_total_energy if e1_total_energy else 0.0),
            "e1_energy_over_diagonal": group[2] / group[1],
        }
        for prime_factor_count, group in sorted(
            e1_by_prime_factor_count.items())}
    return {
        "modulus": modulus,
        "ell": ell,
        "divisor_range": (divisor_lower, divisor_upper),
        "dominant_block_range": (dominant_lower, 2 * dominant_lower),
        "selected_coordinate_count": len(receipts),
        "selected_no_common_energy_fraction": (
            total_selected_energy / total_block_energy),
        "selected_walsh_majorant_over_actual_energy": (
            selected_majorant_energy / total_selected_energy),
        "selected_no_common_actual_over_diagonal": (
            total_selected_energy / selected_diagonal),
        "residual_mobius_aligned_diagonal_fraction": (
            residual_mobius_aligned_energy / selected_diagonal),
        "residual_mobius_sign_energy_correlation": (
            residual_mobius_signed_energy / selected_diagonal),
        "complete_cube_energy_over_diagonal": (
            complete_cube_energy / selected_diagonal),
        "boundary_cube_energy_over_diagonal": (
            boundary_cube_energy / selected_diagonal),
        "complete_boundary_cross_over_diagonal": (
            complete_boundary_cross_energy / selected_diagonal),
        "complete_boundary_diagonal_reconstruction_error": (
            (complete_cube_energy + boundary_cube_energy
             + complete_boundary_cross_energy) / selected_diagonal - 1),
        "complete_collapsed_over_complete_diagonal": (
            complete_collapsed_energy / complete_residual_diagonal
            if complete_residual_diagonal else 0.0),
        "boundary_collapsed_over_boundary_diagonal": (
            boundary_collapsed_energy / boundary_cube_energy
            if boundary_cube_energy else 0.0),
        "complete_collapsed_energy_over_diagonal": (
            complete_collapsed_energy / selected_diagonal),
        "boundary_collapsed_energy_over_diagonal": (
            boundary_collapsed_energy / selected_diagonal),
        "collapsed_complete_boundary_cross_over_diagonal": (
            collapsed_complete_boundary_cross / selected_diagonal),
        "collapsed_complete_boundary_reconstruction_error": (
            (complete_collapsed_energy + boundary_collapsed_energy
             + collapsed_complete_boundary_cross) / selected_diagonal
            - total_selected_energy / selected_diagonal),
        "complete_log_squared_harmonic_bound": complete_harmonic_bound,
        "maximum_complete_residual": maximum_complete_residual,
        "complete_amplitude_monotonicity_violations": (
            complete_amplitude_monotonicity_violations),
        "actual_residual_amplitude_positivity_violations": (
            actual_residual_amplitude_positivity_violations),
        "maximum_actual_residual_amplitude_over_r1": (
            maximum_actual_amplitude_over_base),
        "maximum_nontrivial_residual_amplitude_over_r1": (
            maximum_nontrivial_amplitude_over_base),
        "maximum_nontrivial_residual_amplitude_over_tau_r1": (
            maximum_nontrivial_amplitude_over_tau_base),
        "maximum_actual_residual_amplitude_over_tau_squared_r1": (
            maximum_actual_amplitude_over_tau_squared_base),
        "complete_cube_log_squared_range_condition": (
            complete_range_condition),
        "maximum_no_common_residual_limit": maximum_residual_limit,
        "no_common_three_state_harmonic_squared_bound": (
            three_state_bound["exact_squared_bound"]),
        "no_common_log_six_bound": three_state_bound["log_six_bound"],
        "no_common_polylog_range_condition": no_common_polylog_condition,
        "complete_cube_pair_count": complete_cube_pair_count,
        "nonpositive_complete_cube_pair_count": (
            nonpositive_complete_cube_pair_count),
        "minimum_complete_cube_relative_margin": (
            minimum_complete_cube_relative_margin),
        "truncated_cube_piece_count": truncated_cube_piece_count,
        "nonpositive_truncated_cube_piece_count": (
            nonpositive_truncated_cube_piece_count),
        "minimum_truncated_cube_relative_margin": (
            minimum_truncated_cube_relative_margin),
        "maximum_truncated_cube_reconstruction_error": (
            maximum_truncated_cube_reconstruction_error),
        "selected_walsh_majorant_over_no_common_diagonal": (
            selected_majorant_energy / selected_diagonal),
        "selected_paired_majorant_over_actual_energy": (
            selected_paired_majorant_energy / total_selected_energy),
        "selected_paired_majorant_over_no_common_diagonal": (
            selected_paired_majorant_energy / selected_diagonal),
        "common_divisor_cumulative_majorant_attribution": (
            cumulative_attribution),
        "dyadic_common_divisor_majorant_attribution": (
            dyadic_attribution_fractions),
        "effective_dyadic_common_divisor_block_count": (
            effective_dyadic_block_count),
        "dyadic_common_divisor_square_energy_over_diagonal": (
            dyadic_square_energy_over_diagonal),
        "dyadic_common_divisor_block_count": dyadic_block_count,
        "dyadic_cauchy_bound_over_no_common_diagonal": (
            dyadic_cauchy_bound_over_diagonal),
        "e1_maximum_coordinate_energy_over_diagonal": max(
            row[3] for row in e1_coordinate_data),
        "e1_bad_coordinate_count": len(e1_bad_coordinates),
        "e1_bad_coordinate_diagonal_fraction": sum(
            row[1] for row in e1_bad_coordinates) / selected_diagonal,
        "e1_bad_coordinate_energy_fraction": (
            sum(row[2] for row in e1_bad_coordinates) / e1_total_energy
            if e1_total_energy else 0.0),
        "e1_by_target_prime_factor_count": e1_prime_factor_receipt,
        "selected_receipts": receipts,
        "maximum_assignment_identity_error": max(
            abs(receipt["assignment_identity_error"]) for receipt in receipts),
        "maximum_walsh_identity_error": max(
            abs(receipt["walsh_identity_error"]) for receipt in receipts),
        "minimum_walsh_parity_relative_imbalance": min(
            receipt["walsh_parity_relative_imbalance"]
            for receipt in receipts),
        "maximum_walsh_parity_relative_imbalance": max(
            receipt["walsh_parity_relative_imbalance"]
            for receipt in receipts),
        "finite_dominant_walsh_measurement": True,
        "common_divisor_majorant_attribution_identity_proved": True,
        "dyadic_common_divisor_cauchy_reduction_proved": True,
        "paired_support_majorant_proved": True,
        "paired_support_subpower_bound_proved": False,
        "omega_stratified_e1_bound_proved": False,
        "residual_mobius_sign_rule_proved": False,
        "complete_residual_cube_identity_proved": True,
        "complete_cube_log_squared_bound_proved_for_reported_range": (
            complete_range_condition),
        "no_common_polylog_bound_proved_for_reported_range": (
            no_common_polylog_condition),
        "boundary_truncated_cube_control_proved": False,
        "walsh_parity_cancellation_bound_proved": False,
    }


if __name__ == "__main__":
    for modulus, ell, lower, upper in (
            (16001, 1252, 11, 190),
            (64007, 3281, 16, 404)):
        print(dominant_no_common_walsh_probe(
            modulus, ell, lower, upper))

"""Exact three-state residual-prime cube identity.

Let ``r`` be squarefree and let ``L_x=log(X/x)``.  For fixed complementary
parts ``u,v``, sum over every pair ``alpha,beta`` of divisors of ``r`` whose
lcm is ``r``.  A prime of ``r`` is assigned left, right, or to both sides;
the both-side state has weight -1 from ``mu(gcd(alpha,beta))``.  Then

    sum mu(gcd(alpha,beta)) L_(u alpha) L_(v beta)
      = L_u L_v - sum_(p|r) log(p)^2.                         (1)

The identity applies when the hard interval retains the entire three-state
cube.  Boundary-truncated cubes require a separate remainder.
"""

import math


def residual_cube_closed_form(log_left, log_right, residual_primes):
    """Return the right side of (1) without enumerating the cube."""
    return (float(log_left) * float(log_right)
            - sum(math.log(prime) ** 2 for prime in residual_primes))


def truncated_residual_cube(
        X, left_part, right_part, lower, upper, residual_primes):
    """Enumerate the hard-range part of the three-state residual cube."""
    if (not all(isinstance(value, (int, float)) for value in
                (X, left_part, right_part, lower, upper))
            or not 0 <= lower < upper < X
            or left_part <= 0 or right_part <= 0):
        raise ValueError("invalid truncated cube ranges")
    primes = tuple(residual_primes)
    if (len(set(primes)) != len(primes)
            or any(type(prime) is not int or prime < 2 for prime in primes)):
        raise ValueError("residual primes must be distinct integers >=2")
    direct = absolute = 0.0
    retained = 0

    def visit(index, alpha, beta, common_parity):
        nonlocal direct, absolute, retained
        if index == len(primes):
            left = left_part * alpha
            right = right_part * beta
            if not (lower < left <= upper and lower < right <= upper):
                return
            term = ((-1) ** common_parity
                    * math.log(X / left) * math.log(X / right))
            direct += term
            absolute += abs(term)
            retained += 1
            return
        prime = primes[index]
        visit(index + 1, alpha * prime, beta, common_parity)
        visit(index + 1, alpha, beta * prime, common_parity)
        visit(index + 1, alpha * prime, beta * prime, common_parity + 1)

    visit(0, 1, 1, 0)
    return {
        "truncated_cube_sum": direct,
        "absolute_term_sum": absolute,
        "retained_assignment_count": retained,
        "truncated_cube_positive": direct > 0,
        "finite_truncated_cube_measurement": True,
        "uniform_truncated_cube_positivity_proved": False,
    }


def residual_cube_identity(log_left, log_right, residual_primes):
    """Enumerate (1) and return its closed form and numerical error."""
    if not isinstance(log_left, (int, float)) or not isinstance(
            log_right, (int, float)):
        raise ValueError("logarithmic endpoints must be real")
    primes = tuple(residual_primes)
    if (len(set(primes)) != len(primes)
            or any(type(prime) is not int or prime < 2 for prime in primes)):
        raise ValueError("residual primes must be distinct integers >=2")

    direct = 0.0

    def visit(index, log_alpha, log_beta, common_parity):
        nonlocal direct
        if index == len(primes):
            direct += ((-1) ** common_parity
                       * (log_left - log_alpha)
                       * (log_right - log_beta))
            return
        logarithm = math.log(primes[index])
        visit(index + 1, log_alpha + logarithm, log_beta, common_parity)
        visit(index + 1, log_alpha, log_beta + logarithm, common_parity)
        visit(index + 1, log_alpha + logarithm,
              log_beta + logarithm, common_parity + 1)

    visit(0, 0.0, 0.0, 0)
    closed = residual_cube_closed_form(log_left, log_right, primes)
    return {
        "residual_primes": primes,
        "three_state_assignment_count": 3 ** len(primes),
        "direct_cube_sum": direct,
        "closed_form": closed,
        "identity_error": direct - closed,
        "closed_form_positive": closed > 0,
        "complete_residual_cube_identity_proved": True,
        "boundary_truncated_cube_control_proved": False,
    }


if __name__ == "__main__":
    for key, value in residual_cube_identity(12.0, 11.0, (2, 3, 5)).items():
        print(f"{key}: {value}")

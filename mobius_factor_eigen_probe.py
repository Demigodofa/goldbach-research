"""Generalized eigentest for the three Mobius-factor covariance components.

Owner: Kevin's Goldbach research.  Purpose: test whether the recombined
all-factor coefficient vector follows a stable low-energy covariance direction
or whether a special OFF eigenmode supplies new cancellation.  This is finite
floating evidence at tiny H,V, not an asymptotic theorem.

Let D be the 3 by 3 principal-energy matrix and O the OFF covariance matrix
from ``mobius_factor_covariance_probe.py``.  For a real component vector c,

    principal(c)=c^T D c,       OFF(c)=c^T O c.            (1)

The generalized eigenvalues of O v=lambda D v are the extremal OFF/principal
ratios available inside this three-dimensional component span.  Normalize the
eigenvectors in the D metric.  The squared D-projections of e=(1,1,1) then add
to one and reconstruct the actual full-tail OFF/principal ratio.

MEASURED RESULTS.

 N       H   cos(e, smallest-D vector)  smallest-D/trace  e^T D e/trace
 32000   2            .986820                 .082079          .268851
 200000  3            .993335                 .067086          .215935
 1200000 4            .995139                 .057514          .184177

Thus equal recombination is stably close to the smallest principal-energy
direction in these tests.  This is consistent with the exact identity

 sum_(a>V,a|n)mu(a)log(n/a)
   =Lambda(n)-sum_(a<=V,a|n)mu(a)log(n/a),                 (2)

which identifies e as the full complementary tail.  Identity (2) names the
arithmetic cancellation but supplies no active-band estimate.

The generalized OFF evidence is not stable enough to define a new special
mode.  At the same scales its eigenvalues and the D-spectral weights of e are

 H=2: (-.08030,-.00491,+.02879), weights (.77370,.15731,.06899)
 H=3: (-.07267,-.01096,+.00781), weights (.58849,.10714,.30438)
 H=4: (-.05754,-.00107,+.00536), weights (.67252,.32736,.00011).

The positive-mode weight moves from 6.9% to 30.4% to .011%; it is not a stable
explanation of the actual negative ratios (-.06091,-.04156,-.03905).  The
near-e direction in D is a useful finite signature of cross-factor Mobius
cancellation, but no power decay or sign theorem follows.  In particular it
does not license discarding any factor range or replacing (2) by a bound.  The
reported Euclidean cosine also depends on the natural unscaled three-component
basis; arbitrary rescaling of the components would change it.  The generalized
eigenvalues, D-metric weights, and reconstructed ratio are the invariant parts
of the eigentest.
"""

import numpy as np

from mobius_factor_covariance_probe import finite_factor_covariance_probe


def factor_eigen_receipt(N=32000):
    """Return the principal and generalized spectral data for one finite N."""
    base = finite_factor_covariance_probe(N)
    principal = np.asarray(base["principal_matrix"], dtype=float)
    off = np.asarray(base["off_matrix"], dtype=float)
    principal = (principal + principal.T) / 2
    off = (off + off.T) / 2

    d_values, d_vectors = np.linalg.eigh(principal)
    if np.any(d_values <= 0):
        raise ArithmeticError("finite principal matrix is not positive definite")
    inverse_sqrt = (d_vectors @ np.diag(1 / np.sqrt(d_values))
                    @ d_vectors.T)
    whitened_off = inverse_sqrt @ off @ inverse_sqrt
    generalized_values, whitened_vectors = np.linalg.eigh(
        (whitened_off + whitened_off.T) / 2)
    generalized_vectors = inverse_sqrt @ whitened_vectors

    actual = np.ones(3)
    actual_principal = float(actual @ principal @ actual)
    projections = generalized_vectors.T @ principal @ actual
    spectral_weights = projections ** 2 / actual_principal
    smallest_vector = d_vectors[:, 0]
    if smallest_vector @ actual < 0:
        smallest_vector = -smallest_vector
    cosine = float((smallest_vector @ actual)
                   / (np.linalg.norm(smallest_vector) * np.linalg.norm(actual)))
    reconstructed = float(generalized_values @ spectral_weights)

    return {
        "N": N,
        "H": base["H"],
        "M": base["M"],
        "V": base["V"],
        "principal_eigenvalue_shares": tuple(float(value / np.trace(principal))
                                                for value in d_values),
        "principal_condition_number": float(d_values[-1] / d_values[0]),
        "smallest_principal_eigenvector": tuple(float(x) for x in smallest_vector),
        "smallest_principal_cosine_with_all_factor": cosine,
        "generalized_off_over_principal_eigenvalues": tuple(
            float(x) for x in generalized_values),
        "all_factor_generalized_spectral_weights": tuple(
            float(x) for x in spectral_weights),
        "spectral_weight_sum": float(np.sum(spectral_weights)),
        "reconstructed_all_factor_off_over_principal": reconstructed,
        "direct_all_factor_off_over_principal": base["total_off_over_diagonal"],
        "all_factor_principal_over_component_trace": float(
            actual_principal / np.trace(principal)),
        "identity_alone_proves_active_band_bound": False,
    }


if __name__ == "__main__":
    for key, value in factor_eigen_receipt().items():
        print(f"{key}: {value}")

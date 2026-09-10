"""Deterministic variance bound for a weighted lag graph.

Let positive vertex weights ``alpha_v``, nonnegative ratios ``r_v``, and
nonnegative edge weights ``beta_uv`` be given.  Put

    mu = sum_v alpha_v r_v / A,
    sigma^2 = sum_v alpha_v (r_v-mu)^2 / A,
    D = max_v degree_beta(v) / alpha_v,
    kappa = D A / W,

where ``A=sum alpha_v`` and ``W=sum beta_uv``.  Then

    sum_uv beta_uv sqrt(r_u r_v) / W >= max(0, mu-kappa sigma).       (1)

Indeed ``sqrt(xy) >= mu-|x-mu|-|y-mu|``.  Summing over edges, using
``degree_beta(v)<=D alpha_v``, and applying weighted Cauchy proves (1).
The factor ``kappa`` records boundary-degree and frame-weight distortion
exactly; no regularity assumption is hidden in the statement.
"""

import math


def weighted_geometric_variance_bound(ratios, vertex_weights, edges):
    """Return the actual edge mean and the rigorous lower bound (1).

    ``edges`` is an iterable of ``(left_index, right_index, edge_weight)``.
    """
    ratios = tuple(float(value) for value in ratios)
    vertex_weights = tuple(float(value) for value in vertex_weights)
    edges = tuple((left, right, float(weight)) for left, right, weight in edges)
    if not ratios or len(ratios) != len(vertex_weights):
        raise ValueError("ratios and vertex weights must have equal positive length")
    if any(value < 0 or not math.isfinite(value) for value in ratios):
        raise ValueError("ratios must be finite and nonnegative")
    if any(value <= 0 or not math.isfinite(value)
           for value in vertex_weights):
        raise ValueError("vertex weights must be finite and positive")
    if not edges:
        raise ValueError("at least one edge is required")

    degrees = [0.0] * len(ratios)
    edge_sum = 0.0
    geometric_sum = 0.0
    for left, right, weight in edges:
        if (type(left) is not int or type(right) is not int
                or not 0 <= left < len(ratios)
                or not 0 <= right < len(ratios) or left == right):
            raise ValueError("edge endpoints must be distinct valid indices")
        if weight < 0 or not math.isfinite(weight):
            raise ValueError("edge weights must be finite and nonnegative")
        degrees[left] += weight
        degrees[right] += weight
        edge_sum += weight
        geometric_sum += weight * math.sqrt(ratios[left] * ratios[right])
    if edge_sum <= 0:
        raise ValueError("total edge weight must be positive")

    vertex_sum = sum(vertex_weights)
    mean = sum(weight * ratio for weight, ratio
               in zip(vertex_weights, ratios)) / vertex_sum
    variance = sum(weight * (ratio - mean) ** 2 for weight, ratio
                   in zip(vertex_weights, ratios)) / vertex_sum
    degree_ratio = max(degree / weight for degree, weight
                       in zip(degrees, vertex_weights))
    degree_factor = degree_ratio * vertex_sum / edge_sum
    raw_bound = mean - degree_factor * math.sqrt(variance)
    actual = geometric_sum / edge_sum
    return {
        "weighted_vertex_mean": mean,
        "weighted_vertex_variance": variance,
        "edge_degree_factor": degree_factor,
        "variance_lower_bound": max(0.0, raw_bound),
        "raw_variance_lower_bound": raw_bound,
        "weighted_edge_geometric_mean": actual,
        "inequality_verified_numerically": actual + 1e-12 >= raw_bound,
    }

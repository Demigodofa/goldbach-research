# q286 Target Vector PCA

Status: selected-target visualization diagnostic only. This is not a proof of
Goldbach.

## Artifact

Generated data:

```text
evidence/q286-target-vector-pca.json
```

Builder:

```text
python tools/build_q286_target_vector_pca.py
```

The script reads `evidence/q286-target-vector-overlay.json`, standardizes
selected target coordinates, and runs SVD/PCA on two finite datasets:

- an alignment/complement dataset over eight selected targets;
- a component-action dataset over the five targets with lower-support
  component coordinates.

## Alignment Dataset

Targets:

```text
10664, 14138, 70526, 1222142, 1323632, 1379072, 1426262, 3305200
```

Features:

```text
first_three
complement
full
certificate_margin
l2_negative_bound_utilization
l2_to_sufficient_ratio
```

The first principal component explains about `0.8908699272236911` of selected
variance.  Its strongest positive loading is `certificate_margin`; its
strongest negative loading is `l2_to_sufficient_ratio`.  Role centers on PC1:

```text
boundary_failure:        -3.9250456603343693
alignment_stress_success: 1.1963389076022708
late_active_success:      1.4203581992873093
```

Interpretation: in this selected fixture, boundary failures separate sharply
from rescued/stress successes along a margin-versus-discrepancy-size axis.

## Component Dataset

Targets:

```text
10664, 14138, 1222142, 1323632, 1379072
```

Features:

```text
first_three
full
visible_lower_package
lower_package_rescue_margin
component_57_centered
component_711_centered
centered_lower_support
```

The first principal component explains about `0.8965052711777547` of selected
variance.  Role centers on PC1:

```text
boundary_failure:   2.7476953891641935
late_active_success: -1.831796926109462
```

Interpretation: in this selected fixture, the boundary/late split is also
visible in the lower-support component coordinates.  The largest boundary
outlier remains `14138`.

## Boundary

This is a tiny selected PCA.  It is useful for choosing axes in a heat/shape
map and for proposing falsifier directions, but it does not establish a
population cluster, a probability model, a pointwise signed prime-correlation
estimate, strict closure, outer assembly, or Goldbach.

The next statistically disciplined step would be to apply the same frozen
feature map to unchanged-selector targets from new windows.  Without that
denominator, PCA separation can reflect selected-fixture design or attention
bias.

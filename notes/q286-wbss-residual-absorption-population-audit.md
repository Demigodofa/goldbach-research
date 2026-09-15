# q286-WBSS Residual Absorption Population Audit

Status: finite population diagnostic. Goldbach is not proved.

Receipt:

```text
tools/build_q286_wbss_residual_absorption_population_audit.py
evidence/q286-wbss-residual-absorption-population-audit.json
```

## Question

The residual absorption threshold audit fit `.126` and `.13` on the `196`
post-discovery rows. This audit asks whether that finite fit was caused by
excluding the `34` discovery rows from the same lower-face dual-edge source.

This is broader than the previous fixture, but it is not a fresh asymptotic
holdout.

## Result

All `230` available lower-face dual-edge rows were replayed:

```text
all dual-edge rows:                         230
discovery rows:                              34
post-discovery rows:                        196
positive pushback rows, all population:      29
positive pushback rows, discovery:            5
top-20 nonnegative rows:                      0
```

The maximum pushback/top20-drag ratio over all `230` rows is still:

```text
0.12566677703853088 at target 365578
```

That row is in the post-discovery bucket. The discovery-row maximum is:

```text
0.1187884461709314 at target 10564
```

Therefore:

```text
theta = 1/8 = 0.125   fails on the full 230-row population
theta = 0.126         passes the full 230-row population
theta = 0.13          passes the full 230-row population
```

## Decision

The decimal fit is not caused merely by excluding the discovery rows. The
one-sided top-20/residual split still survives this broader finite population.
But the constants remain finite-data fits only; the universal residual
absorption bound is open.

## Boundary

This audit proves no residual absorption theorem, no signed projection theorem,
no q286 threshold theorem, no strict-central Goldbach theorem, and no Goldbach
proof. It only extends the finite threshold check from `196` post-discovery
rows to all `230` available lower-face dual-edge rows.

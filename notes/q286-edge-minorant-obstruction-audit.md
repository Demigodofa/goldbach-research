# q286 edge-minorant obstruction audit

Status: finite minorant obstruction and `new-to-this-task`
changed-under-evidence result.  This is not a coefficientwise minorant
theorem, signed prime-correlation estimate, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

Receipt:

```text
tools/build_q286_edge_minorant_obstruction_audit.py
evidence/q286-edge-minorant-obstruction-audit.json
```

## Question

The unnormalized dual-edge audit left three possible exits:

```text
prove the raw signed witness directly,
construct a coefficientwise nonnegative minorant,
or separately prove T_N > 0.
```

This audit tests the strongest easy version of the second route.  For each
dual edge, write:

```text
Full(mu_N)>0
  iff E_mu_N[gap] - required > 0
  iff E_mu_N[gap-required] > 0.
```

If `gap-required` were nonnegative on every reflection orbit, any nonzero
strict-central mass would rescue automatically.

## Result

For the `196` checked post-discovery rows:

```text
pointwise minorant pass count:              0 / 196
support orbits negative count:              196 / 196
minimum pointwise rescue coefficient:       -7.283885499227512..-2.5357299258914665
negative rescue coefficient orbit count:    224..560
positive rescue coefficient orbit count:    348..659
actual mass on negative rescue coefficients:
                                           0.32730051201285604..0.5711006912377132
actual mass on positive rescue coefficients:
                                           0.42889930876228677..0.672699487987144
positive/negative rescue ratio:             1.0191444227555964..3.167398344085266
signed part identity error:                 0.0..8.881784197001252e-16
```

The weakest post-discovery signed-part row is again `94856`:

```text
negative rescue drag:              0.6569258553446623
positive rescue contribution:      0.6695023216384622
positive/negative rescue ratio:    1.0191444227555964
final normalized margin:           0.012576466293799937
```

## Interpretation

The easy coefficientwise minorant route fails for a structural reason.  The
lower-face support has zero edge gap while the required rescue amount is
positive, so the pointwise coefficient `gap-required` is negative on the bad
support itself.  No theorem that merely says "the pair weights are
nonnegative" can close this edge.

The actual rows rescue because their mass distribution favors the positive
part of the pointwise rescue coefficient enough to beat the negative drag.
That is exactly a distributional anti-landing statement:

```text
sum_{gap>required} W_N * (gap-required)
  >
sum_{gap<required} W_N * (required-gap).
```

## Decision

Do not promote the coefficientwise minorant shortcut.  The remaining q286
bridge is one of:

- a signed binary-prime correlation theorem for `gap-required`;
- a sharper cone that forbids actual mass from landing too heavily on the
  negative rescue coefficient set;
- or an independent lower bound for `T_N>0`.

The first two are genuinely distributional.  The third remains risky because
it may simply reintroduce Goldbach-like input as a premise.


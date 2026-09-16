# q286 active-selector L2 bridge-status audit

## Question

Is the q286 active-selector `L2` rarity target genuinely non-circular, and is
it actually confirmed?

## Receipt

```text
tools/build_q286_active_selector_l2_bridge_status_audit.py
evidence/q286-active-selector-l2-bridge-status-audit.json
```

## Answer

The `L2` target is a valid non-circular sufficient theorem shape if it is
proved as a pointwise arithmetic estimate for actual strict-central
binary-prime residue weights:

```text
For N == a mod 286 with T_N=sum_u W_N(u)>0,
if ||W_N - T_N/|A_a|||_2 / T_N <= 0.3 / ||gamma_a||_2,
then first_three(N) >= -0.3.
```

It is non-circular in that form because the premise is about prime-pair
residue weights before applying the active selector; it does not assume
`first_three >= -0.3`.

But it is not confirmed.  No pointwise `L2` discrepancy theorem is proved, and
finite windows do not prove the universal premise.  Also, the premise is
normalized by `T_N`, so it only has content when strict-central prime-pair mass
already exists.  It can control the distribution of existing mass; it cannot
by itself prove that the mass exists.

## Quantified sufficient range

The existing q286 coefficient algebra gives:

```text
L2 sufficient relative-delta range:
  0.0059551615239434134 .. 0.017908306132142508
Linf sufficient relative-delta range:
  0.0012438599030454016 .. 0.002451362294448365
even target residues checked: 143
```

So plain `L2` is not an easy finite bridge.  It asks for sub-percent to
low-percent pointwise control of strict-central binary-prime residue
discrepancy, depending on the target residue.

## Sample stress

The clear sample rows already show why generic `L2` uniformity is too blunt:

```text
target   tail?   L2 budget utilization   signed projection passes?
1222142  yes     2.0973149884967834      no
1240888  no      1.82647385924401        yes
1242118  no      2.9097499848440553      yes
```

Both clear rows fail the generic `L2` budget but pass the signed-projection
threshold.  Their deviations are allowed because they are mostly orthogonal or
favorably aligned relative to the q286 coefficient vector.

## Decision

`HOLD_L2_is_valid_sufficient_non_circular_shape_but_unconfirmed`.

Do not treat `L2` as an accepted bridge.  Use it only as a theorem target, or
replace it with the sharper coefficient-sensitive signed-projection obligation:

```text
<delta_N, c_a> >= -0.3
```

or equivalently the residue-pair correlation form:

```text
sum_{u in A_a}(W_N(u)-T_N/|A_a|)*gamma_a(u) >= -0.3*T_N.
```

## Boundary

Logical bridge-status audit only.  This proves no `L2` discrepancy theorem,
active-selector rarity theorem, strict-central prime-pair existence theorem,
q286 threshold theorem, or Goldbach proof.

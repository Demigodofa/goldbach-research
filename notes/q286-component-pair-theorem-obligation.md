# q286 component-pair theorem obligation

Status: theorem obligation and finite diagnostic; Goldbach not proved.

Date: 2026-09-13.

## Fixed objects

The active lower-support component-pair route works at modulus `10010`.
Let `U` be the `2880` unit residues modulo `10010`.  For an even target `N`,
let

```text
A_N = {r in U : gcd(N-r,10010)=1}.
```

For the checked component-pair targets in this note, `|A_N| = 1485`.
Let `W_N(r)` be the strict-central weighted prime-pair mass with first prime
`p == r mod 10010`:

```text
W_N(r) = sum log(p)log(N-p)
```

over strict-central prime pairs `N/3 < p < 2N/3`.  Let

```text
mu_N = (sum_{r in A_N} W_N(r)) / |A_N|,
d_N(r) = W_N(r) - mu_N  for r in A_N,
d_N(r) = 0              otherwise.
```

The lower-support component receipt decomposes the fixed assembled coefficient
vector by CRT character support.  For the active pair, write the two centered
coefficient vectors on `A_N` as

```text
c_57,N
c_711,N
```

for supports `(5,7)` and `(7,11)`.  Their centered actions are exactly

```text
<c_57,N, d_N> / P(N)
<c_711,N, d_N> / P(N)
```

where `P(N)` is the principal normalization used by the receipts.

## Current theorem target

After finite boundary exceptions, prove that targets in the active subcone

```text
first_two_q286_modes(N)/P(N) < -0.2
first_three_q286_modes(N)/P(N) < -0.3
```

do not have simultaneous sufficiently negative centered action in both active
lower-support channels.  The strongest finite pattern currently checked is
that the late sparse-tail comparison targets have no simultaneous negative
action at all:

```text
<c_57,N,d_N>/P(N) < 0 and <c_711,N,d_N>/P(N) < 0
```

does not occur for `1222142`, `1323632`, or `1379072`.

## Finite selected-target evidence

The selected-target receipt

```text
q286_lower_support_component_pair_tail_window_receipt(
    selected_targets=(1222142,1323632,1379072),
    first_two_threshold=.2,
    tail_threshold=.3)
```

completed in `64.87790719999975s`.  All three selected targets were active
tail-subcone targets and none had simultaneous negative pair action:

```text
target   (5,7) action/P          (7,11) action/P         pair sum/P
1222142 -0.0010834080557930044   0.014826359763802442   0.013742951708009437
1323632  0.06545161702266966     0.022043464205542592   0.08749508122821226
1379072 -0.036824552185769695    0.08354880369092735    0.04672425150515765
```

The boundary comparison target `14138` does have simultaneous negative
component-pair action:

```text
14138   -0.7331790639459977     -0.41936420368103794
```

so any eventual theorem must split away a finite boundary/full-negative layer.

## Coefficient geometry receipt

`q286_lower_support_component_pair_coefficient_geometry_receipt` now makes the
fixed coefficient-vector scan executable.  Focused regression
`test_q286_lower_support_component_pair_coefficient_geometry` passed in
`32.897s`.

Across all `5005` even target residues modulo `10010`, the two active
coefficient vectors are structurally near-orthogonal:

```text
admissible_counts:
  1485, 1620, 1650, 1782, 1800, 1944, 1980,
  2160, 2200, 2376, 2400, 2592, 2640, 2880
cosine range: -0.0381940494499906 .. 0.0419660251672338
absolute cosine maximum: 0.0419660251672338
median cosine: about 0
(5,7) norm/principal_mean range: 46.621944574458 .. 109.5307597246672
(7,11) norm/principal_mean range: 58.599508082320234 .. 118.2876619523048
pair-sum norm/principal_mean range: 87.54836438202342 .. 161.21091245944086
```

This is fixed-coefficient evidence, not a prime-pair theorem.

## Selected-target discrepancy geometry

A direct coefficient/discrepancy geometry probe over
`14138,1222142,1323632,1379072` measured the two coefficient vectors and their
alignment with the actual strict-central prime-pair discrepancy vector.

Common fixed data:

```text
period 10010
unit_count 2880
principal_mean 44002.512499999146
admissible_count 1485
```

Results:

```text
target 14138
weight_l2_rel 0.11251754817108045
(5,7)  coeff_norm/principal_mean 92.9842972930563
       action/P -0.7331790639459977
       cosine with d_N -0.07007775521562869
(7,11) coeff_norm/principal_mean 79.95577232597192
       action/P -0.41936420368103794
       cosine with d_N -0.0466145261936264
pair coefficient cosine 0.004826197080648738

target 1222142
weight_l2_rel 0.016376641721585147
(5,7)  action/P -0.0010834080557930044, cosine -0.0007117056633438867
(7,11) action/P  0.014826359763802442,  cosine  0.011278165563276089
pair coefficient cosine -0.0010921005009287641

target 1323632
weight_l2_rel 0.01572226822549456
(5,7)  action/P 0.06545161702266966,  cosine 0.044770873322439404
(7,11) action/P 0.022043464205542592, cosine 0.017465998749571405
pair coefficient cosine -0.0008340640836047953

target 1379072
weight_l2_rel 0.015831861533604066
(5,7)  action/P -0.036824552185769695, cosine -0.02501473336272637
(7,11) action/P  0.08354880369092735,  cosine  0.06574110996645298
pair coefficient cosine -0.000834064083604795
```

Interpretation: the active coefficient vectors are nearly orthogonal, not
oppositely constrained.  The late targets avoid simultaneous negativity
because the actual prime-pair discrepancy vector has small relative L2 size
and favorable signed alignment, not because the fixed coefficient geometry
itself forbids the bad cone.

## Cone-projection receipt

`q286_lower_support_component_pair_cone_projection_receipt` now projects the
actual strict-central prime-pair discrepancy vector `d_N` onto the
two-dimensional span of the `(5,7)` and `(7,11)` centered coefficient vectors.
Focused regression `test_q286_lower_support_component_pair_cone_projection`
passed in `88.970s`.

Default selected-target output:

```text
tested 4
both_negative (14138,)
maximum span projection fraction: target 14138, 0.08397880199809928
minimum span projection fraction: target 1222142, 0.01129983025146733
```

Rows:

```text
target 14138
  weight_l2_rel 0.11251754817108045
  actions (5,7) -0.7331790639459977, (7,11) -0.41936420368103794
  projection_fraction 0.08397880199809928
  orthogonal_fraction 0.9964675412751607

target 1222142
  weight_l2_rel 0.016376641721585147
  actions (5,7) -0.0010834080557930044, (7,11) 0.014826359763802442
  projection_fraction 0.01129983025146733
  orthogonal_fraction 0.9999361548800446

target 1323632
  weight_l2_rel 0.01572226822549456
  actions (5,7) 0.06545161702266966, (7,11) 0.022043464205542592
  projection_fraction 0.04807076284797583
  orthogonal_fraction 0.9988439326337293

target 1379072
  weight_l2_rel 0.015831861533604066
  actions (5,7) -0.036824552185769695, (7,11) 0.08354880369092735
  projection_fraction 0.0703199163405805
  orthogonal_fraction 0.997524490609556
```

Interpretation: the active obstruction is not the full discrepancy vector.
Almost all measured discrepancy L2 is orthogonal to the two dangerous
component directions.  The theorem target is a very small signed projection:
prevent the actual prime-pair discrepancy vector from entering a narrow
negative cone in the two-dimensional component-pair span after finite boundary
exceptions.

## Finite-vector obstruction

The simultaneous-negativity exclusion cannot be proved from support,
nonnegativity, total mass, and these two centered coefficient vectors alone.
Given any target residue with nonzero centered vectors `c_57` and `c_711`,
choose a centered perturbation `h` with

```text
<c_57,h> < 0
<c_711,h> < 0
```

for example a small negative combination of the two coefficient vectors unless
one vector is a nonpositive multiple of the other.  Since the measured pair
cosines are near zero, such a perturbation is available in the checked
residue classes.  Then `W(r)=mu+epsilon*h(r)` remains nonnegative for
sufficiently small `epsilon`, preserves total admissible mass, but makes both
centered actions negative.

Therefore an eventual proof must use arithmetic information about actual
binary prime-pair weights.  It cannot be a pure convex-geometry or
support-only argument.

## Support-geometry obstruction receipt

`q286_lower_support_component_pair_support_geometry_obstruction_receipt` now
makes the finite-vector obstruction executable.  It scans all `5005` even
target residues modulo `10010`; for each residue it starts from uniform mass
on the admissible classes and applies a small centered perturbation in the
direction `-(c_57+c_711)`.  The perturbation preserves total mass, keeps all
weights nonnegative, and makes both active component actions negative.

Focused regression
`test_q286_lower_support_component_pair_support_geometry_obstruction` passed
in `36.947s`.

Receipt summary:

```text
even_residue_count 5005
obstructed_count 5005
all_obstructed True
```

The least-negative artificial witness still has both actions negative:

```text
target_residue 3424
admissible_count 1485
minimum_weight 0.000402191677018091
maximum_weight 0.00101010101010101
actions:
  (5,7)  -0.07974971574660267
  (7,11) -0.354289196314675
```

Sample active residues:

```text
target 14138, residue 4128:
  (5,7) -0.32518448457077637
  (7,11) -0.24079217206428727

target 1222142, residue 922:
  (5,7) -0.3206698173170558
  (7,11) -0.23907114747538058

target 1323632, residue 2312:
  (5,7) -0.32089141167428276
  (7,11) -0.23909711917141777

target 1379072, residue 7702:
  (5,7) -0.3208914116742828
  (7,11) -0.23909711917141777
```

This closes the pure support/nonnegativity/total-mass/coefficient-geometry
route for the component-pair theorem.  It does not refute arithmetic
cone-avoidance by actual prime-pair weights.

`q286_lower_support_component_pair_reflection_support_geometry_obstruction_receipt`
adds the actual ordered prime-pair reflection symmetry `w(r)=w(N-r)` to the
same finite-vector obstruction.  Focused regression
`test_q286_lower_support_component_pair_reflection_support_obstruction` passed
in `34.893s`.  It still obstructs all `5005` even residues modulo `10010`.

```text
obstructed even target residues: 5005 / 5005
maximum reflection weight error: 0
least-negative reflected witness residue: 9864
least-negative reflected witness actions:
  (5,7)  about -0.033788733675468835
  (7,11) about -0.2559098620858012
sample target 14138 reflected actions:
  (5,7)  about -0.3366393727298987
  (7,11) about -0.11037824420364589
```

Thus pair-swap symmetry does not reopen the support-only route.  The surviving
component-pair theorem must use genuine prime-pair arithmetic beyond support,
nonnegativity, total mass, and reflection symmetry.

## Character-mixture receipt

`q286_lower_support_component_pair_character_mixture_receipt` now expresses the
two active component actions as exact fixed character mixtures modulo `10010`.
Focused regression
`test_q286_lower_support_component_pair_character_mixture` passed in
`68.299s`.

The active cone is much smaller than full residue-class control:

```text
(5,7) active character count: 8
(7,11) active character count: 23
active union character count: 31
(5,7) L1/principal_mean: 5.716280579904891
(7,11) L1/principal_mean: 9.546677026856452
pair-sum L1/principal_mean: 15.262957606760951
pair-sum L2/principal_mean: 3.003987991450646
maximum action reconstruction error: 4.961197005087556e-14
```

The active character labels use only the expected adjacent factor blocks in
the factor order `(5,7,11,13)`:

```text
(5,7) labels:
  (1,1,0,0), (1,3,0,0), (1,5,0,0),
  (2,2,0,0), (2,4,0,0),
  (3,1,0,0), (3,3,0,0), (3,5,0,0)

(7,11) labels:
  (0,1,1,0), (0,1,3,0), (0,1,5,0), (0,1,7,0), (0,1,9,0),
  (0,2,2,0), (0,2,4,0), (0,2,6,0), (0,2,8,0),
  (0,3,1,0), (0,3,3,0), (0,3,5,0), (0,3,7,0), (0,3,9,0),
  (0,4,2,0), (0,4,4,0), (0,4,6,0), (0,4,8,0),
  (0,5,1,0), (0,5,3,0), (0,5,5,0), (0,5,7,0), (0,5,9,0)
```

`q286_lower_support_component_pair_real_channel_receipt` then collapses those
complex characters by conjugation.  Focused regression
`test_q286_lower_support_component_pair_real_channel` passed in `30.401s`.

```text
(5,7) complex rows: 8, real conjugacy channels: 4
(7,11) complex rows: 23, real conjugacy channels: 12
active union complex rows: 31
active union real conjugacy channels: 16
self-conjugate active channels: 1
pair-sum real-channel L1/principal_mean: 15.262957606760951
maximum conjugate coefficient error: below 1e-12
```

The lone self-conjugate active label is `(0,3,5,0)`.  Thus the surviving
component-pair theorem can be stated over `16` real conjugacy channels rather
than `31` unrelated complex character sums.  Each non-self-conjugate channel
has exact contribution formula `2*Re(c*S_chi)`, while the self-conjugate
channel has formula `Re(c*S_chi)`.

`q286_lower_support_component_pair_real_channel_action_receipt` evaluates
those `16` real formulas on selected actual strict-central prime-pair weights.
Focused regression
`test_q286_lower_support_component_pair_real_channel_action` passed in
`73.676s`.

```text
active real channels: 16
maximum reconstruction error: 1.1310397063368782e-15

target 14138:
  real-channel pair sum -1.152543267627036
  direct pair sum       -1.152543267627035
  most negative channel representative (1,1,0,0): -0.2557958141902999
  most positive channel representative (0,2,4,0): 0.03572303158301167

target 1222142:
  real-channel pair sum 0.01374295170801024
  direct pair sum       0.013742951708009191
  most negative channel representative (2,2,0,0): -0.01554557757654789
  most positive channel representative (0,1,9,0): 0.030691736538992695

target 1323632:
  real-channel pair sum 0.08749508122821215
  direct pair sum       0.08749508122821231
  most negative channel representative (0,3,3,0): -0.019336499365645184
  most positive channel representative (1,3,0,0): 0.03208999267160749

target 1379072:
  real-channel pair sum 0.046724251505156425
  direct pair sum       0.046724251505157556
  most negative channel representative (1,5,0,0): -0.018921846854424336
  most positive channel representative (0,3,3,0): 0.030290294154962222
```

This converts the selected-target obstruction/rescue comparison into actual
signed real-channel contributions for the current boundary/comparison set.
It is still finite evidence and does not prove a pointwise real-channel
estimate.

`q286_lower_support_component_pair_real_channel_rescue_margin_receipt` rewrites
the lower-support rescue identity as an exact floor for the centered
real-channel pair sum, after the non-pair lower-support terms and the pair
local means are accounted for.  Focused regression
`test_q286_lower_support_component_pair_real_channel_rescue_margin` passed in
`119.854s`.

```text
target 14138:
  required centered pair sum -0.2756019941861918
  actual centered pair sum   -1.152543267627036
  margin                     -0.8769412734408442

target 1222142:
  required centered pair sum -0.9319733145059023
  actual centered pair sum    0.01374295170801024
  margin                      0.9457162662139125

target 1323632:
  required centered pair sum -0.9367241850081613
  actual centered pair sum    0.08749508122821215
  margin                      1.0242192662363734

target 1379072:
  required centered pair sum -0.8982746156725305
  actual centered pair sum    0.046724251505156425
  margin                      0.944998867177687

late-comparison uniform sufficient floor:
  centered pair sum >= -0.8982746156725305
  minimum actual late centered pair sum 0.01374295170801024 at 1222142
  uniform-floor margin 0.9120175673805407
```

This is the cleanest selected-target sufficient inequality so far: a future
pointwise theorem may target the centered real-channel pair sum against this
floor.  Over the three late comparison targets, the strongest selected
uniform sufficient floor is `-0.8982746156725305`, still leaving observed
margin `0.9120175673805407`.  The receipt proves no eventual floor estimate.

`q286_lower_support_component_pair_real_channel_bound_budget_receipt` converts
that selected floor into sufficient norm budgets for the `16` real channel
representative sums.  Focused regression
`test_q286_lower_support_component_pair_real_channel_bound_budget` passed in
`121.411s`.

```text
real-channel coefficient norms, divided by principal mean:
  L1   15.262957606760978
  L2    4.167538506325983
  Linf  1.7049336541439826

late-comparison uniform floor -0.8982746156725305:
  sufficient normalized Linf channel bound 0.05885324711081062
  sufficient normalized L2 channel bound   0.2155408076755675

all-selected floor -0.2756019941861918:
  sufficient normalized Linf channel bound 0.018056919326311264
  sufficient normalized L2 channel bound   0.06613064132889246

actual maximum normalized representative channel sums:
  14138    0.2659059415120284
  1222142  0.024982703095853185
  1323632  0.025545756019543613
  1379072  0.027155981994015317
```

This does not prove such a pointwise real-channel norm estimate.  It only
quantifies the theorem needed: an eventual normalized `Linf` bound below
about `0.0589` on the active real channels would be strong enough for the
late selected floor, while the boundary target `14138` is far outside that
budget.

`q286_lower_support_component_pair_conditional_norm_closure_receipt` makes
the conditional theorem boundary explicit.  Focused regression
`test_q286_lower_support_component_pair_conditional_norm_closure` passed in
`116.123s`.

It separates the two assumptions needed to turn the selected norm budget into
a rescue theorem:

1. floor stability: the required centered pair floor is at most
   `-0.8982746156725305`;
2. real-channel norm control: every active representative character sum has
   normalized absolute value at most `0.05885324711081062`.

Under those two assumptions, the triangle inequality guarantees centered pair
sum at least `-0.8982746156725305`.  On the selected rows, exactly
`1222142`, `1323632`, and `1379072` satisfy both assumptions and are rescued.
The boundary target `14138` satisfies neither assumption.  Thus the non-
circular proof target has split into two genuine theorems: an eventual
floor-stability theorem for the active lower-support subcone, and an eventual
pointwise norm estimate for the `16` real character channels.

`q286_lower_support_component_pair_floor_stability_decomposition_receipt`
decomposes the floor-stability half into the lower-support package floor and
the fixed non-pair plus pair-local offset.  Focused regression
`test_q286_lower_support_component_pair_floor_stability_decomposition` passed
in `121.972s`.

```text
uniform selected centered-pair floor: -0.8982746156725305
rescued required lower-support package ceiling: -0.6751407665271594
rescued floor-offset floor: 0.2231338491453711

target 14138:
  required lower-support package floor -0.1378737877186007
  floor offset                         0.1377282064675911
  required centered pair floor        -0.2756019941861918

target 1379072:
  required lower-support package floor -0.6751407665271594
  floor offset                         0.2231338491453711
  required centered pair floor        -0.8982746156725305
```

The sufficient term conditions learned from the selected rescued targets are:

```text
required_lower_support_package_to_rescue <= -0.6751407665271594
non_pair_lower_support_actual + component_pair_local_mean >= 0.2231338491453711
```

They hold exactly for the three late selected targets and fail for `14138`.
This is still finite decomposition evidence only; it does not prove those two
term inequalities eventually hold on the active subcone.

Selected-target rows:

```text
target 14138:
  actions (5,7) -0.7331790639459962, (7,11) -0.4193642036810369
  pair_sum -1.152543267627033
  active character L2 relative 0.635690384197428

target 1222142:
  actions (5,7) -0.0010834080557931736, (7,11) 0.014826359763802375
  pair_sum 0.013742951708009201
  active character L2 relative 0.07487477355460123

target 1323632:
  actions (5,7) 0.06545161702266966, (7,11) 0.02204346420554273
  pair_sum 0.0874950812282124
  active character L2 relative 0.09041458261739957

target 1379072:
  actions (5,7) -0.03682455218576963, (7,11) 0.08354880369092721
  pair_sum 0.046724251505157584
  active character L2 relative 0.08819254618298306
```

This sharpens the arithmetic theorem obligation: one need not prove full
pointwise equidistribution modulo `10010`.  A signed cone-avoidance theorem
for the `16` coefficient-bearing real formulas inside the two explicit
adjacent character-label blocks above would target the surviving obstruction
directly.  Such a theorem is still pointwise binary-prime correlation input
and is not supplied by the finite receipts.

## Precise unresolved theorem

A non-circular sufficient theorem is one of the following, after finite
boundary exceptions:

1. A cone-avoidance theorem for actual strict-central prime-pair discrepancy:

```text
not ( <c_57,N,d_N>/P(N) < -eta_57(N)
      and <c_711,N,d_N>/P(N) < -eta_711(N) )
```

on the active `.2`/`.3` subcone, with thresholds strong enough to preserve the
lower-support rescue inequality.  The projection receipt sharpens this as a
two-dimensional cone-avoidance statement for a small projection of `d_N`, not
as a bound for the full residue discrepancy vector.

2. A sharper signed estimate proving that at least one component-pair action
is nonnegative, or that their sum is bounded below:

```text
max(<c_57,N,d_N>, <c_711,N,d_N>) >= 0
```

or

```text
<c_57,N+c_711,N, d_N>/P(N) >= -epsilon_N
```

with `epsilon_N` smaller than the available lower-support margin.

3. A fixed-modulus pointwise binary Goldbach-in-progressions estimate strong
enough to make the whole centered discrepancy small relative to principal:

```text
||d_N||_2 / sum_r W_N(r) = o(1)
```

uniformly on the active residue classes.  This would eventually make every
fixed centered component action `o(P(N))`, but it is a hard pointwise
prime-pair correlation theorem, not a finite diagnostic.

Current judgment: the component-pair lane has identified a precise theorem
obligation.  It has not proved Goldbach.  More threshold receipts are circular
unless they test a new cone-avoidance mechanism, a sharper prime-pair
discrepancy theorem, or a real boundary split.

After the conditional norm-closure receipt, the most precise current target is
the conjunction of:

```text
required_centered_pair_sum_to_rescue(N) <= -0.8982746156725305
max_active_real_channel |S_chi(N)| / total_weight(N)
    <= 0.05885324711081062
```

for all sufficiently late targets in the active `.2`/`.3` lower-support
subcone, plus a finite boundary check.  This is narrower than full residue
equidistribution but still demands a pointwise binary-prime character-sum
estimate not proved in this repository.

The floor-stability half can now be sharpened further as:

```text
required_lower_support_package_to_rescue(N) <= -0.6751407665271594
non_pair_lower_support_actual(N) + component_pair_local_mean(N)
    >= 0.2231338491453711
```

which implies the selected centered-pair floor condition above.

`q286_lower_support_component_pair_floor_identity_receipt` then removes the
remaining bookkeeping slack: the selected centered-pair rescue floor is exactly

```text
required_centered_pair_sum_to_rescue
  = -1 - (
      first_three
      + q286_after_first_three
      + non_pair_lower_support_actual
      + component_pair_local_mean
    ).
```

Focused regression `test_q286_lower_support_component_pair_floor_identity`
passed in `118.879s`, with reconstruction error below `1e-12`.  Therefore the
floor-stability half is equivalent on these rows to the single combined-driver
inequality

```text
first_three + q286_after_first_three
  + non_pair_lower_support_actual + component_pair_local_mean
    >= -0.1017253843274695.
```

For `14138`, the combined driver is `-0.7243980058138082`; for `1379072`, it
is exactly the selected boundary floor `-0.1017253843274695`.  This is still
an identity and selected comparison, not an eventual theorem.

`q286_lower_support_component_pair_combined_driver_channel_closure_receipt`
packages the current clean sufficient theorem.  Focused regression
`test_q286_lower_support_component_pair_combined_driver_channel_closure`
passed in `121.404s`.

On the selected lower-support component-pair lane, the two assumptions are:

```text
combined driver >= -0.1017253843274695
max_active_real_channel |S_chi(N)| / total_weight(N)
    <= 0.05885324711081062
```

Together they force centered-pair rescue.  The selected late comparison
targets `1222142`, `1323632`, and `1379072` satisfy both assumptions and are
rescued.  The boundary target `14138` satisfies neither.  This is now the
cleanest current conditional closure of the q286 component-pair lane; proving
those two assumptions eventually remains open.

`q286_lower_support_component_pair_action_identity_receipt` verifies the
direct recombined identity

```text
full_action / P = 1 + combined_driver + centered_pair_sum.
```

Focused regression `test_q286_lower_support_component_pair_action_identity`
passed in `114.284s`, with reconstruction error below `1e-12`.  This turns
the current q286 component-pair target into the clean positivity statement:

```text
combined_driver >= -0.1017253843274695
centered_pair_sum >= -0.8982746156725305
```

where the second condition follows from active-channel normalized `Linf <=
0.05885324711081062`.  On the selected rows, the identity-positive targets,
the actual-positive targets, and the conditional-closure targets are exactly
`1222142`, `1323632`, and `1379072`.  The boundary `14138` remains negative.

`q286_lower_support_component_pair_closure_margin_profile_receipt` records the
selected margins against the two clean assumptions.  Focused regression
`test_q286_lower_support_component_pair_closure_margin_profile` passed in
`118.798s`.

```text
driver floor: -0.1017253843274695
centered-pair floor: -0.8982746156725305
active-channel Linf bound: 0.05885324711081062

target 14138:
  driver margin  -0.6226726214863387
  channel margin -0.20705269440121776
  full action    -0.8769412734408442

target 1379072:
  driver margin  0.0 (within roundoff)
  channel margin 0.031697265116795305
  full action    0.944998867177687
```

Among the selected late positives, `1379072` is binding on the driver floor,
while `1323632` is closest to the active-channel Linf bound.  Thus the next
useful theorem attempts should treat the driver lower bound and the real-
channel pointwise bound as separate pressure points, not as one generic
positivity margin.

`q286_lower_support_component_pair_channel_pressure_profile_receipt` then
identifies which active real channels create the selected Linf pressure.
Focused regression
`test_q286_lower_support_component_pair_channel_pressure_profile` passed in
`124.495s`.

```text
active-channel Linf bound: 0.05885324711081062

worst overall:
  target 14138
  representative label (1,1,0,0)
  normalized abs sum 0.2659059415120284
  margin to bound -0.20705269440121776
  contribution/principal -0.2557958141902999

worst late positive:
  target 1379072
  representative label (0,3,3,0)
  normalized abs sum 0.027155981994015317
  margin to bound 0.031697265116795305
  contribution/principal 0.030290294154962222
```

This separates two finite channel facts that were previously easy to blur:
`1323632` is closest to the selected channel bound among late positives, but
`1379072` has the largest single active real-channel normalized sum among
those late positives.  The boundary failure is dominated by the `(1,1,0,0)`
channel.  This is finite pressure profiling only; it does not prove the
pointwise real-channel norm estimate.

`q286_lower_support_component_pair_channel_conductor_profile_receipt` records
the actual conductors of those `16` real channels.  Focused regression
`test_q286_lower_support_component_pair_channel_conductor_profile` passed in
`118.119s`.

```text
active real channels: 16
active conductors: 35, 77
channel counts: conductor 35 -> 4; conductor 77 -> 12
uses factor 13: False

worst overall pressure:
  target 14138
  representative label (1,1,0,0)
  conductor 35

worst late-positive pressure:
  target 1379072
  representative label (0,3,3,0)
  conductor 77
```

Thus the active q286 component-pair channel problem is not a full
modulus-`10010` pointwise theorem.  The surviving channel estimate can be
phrased as fixed-conductor twisted binary-Goldbach control on the adjacent
conductors `35=5*7` and `77=7*11`, with the target residue still inherited
from the lcm-period setup.  This is a meaningful narrowing of the theorem
obligation, not a proof of that twisted estimate.

`q286_lower_support_component_pair_fixed_conductor_reduction_receipt` verifies
that reduction directly.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_reduction` passed in
`162.840s`.  For every selected target and every active real channel, it
aggregates the strict-central discrepancy by residue modulo the channel's
own conductor and reconstructs the original period-`10010` character sum.
The regression checks maximum character-sum reduction error below `1e-8` and
residue-character consistency error below `1e-12`.

The pressure witnesses survive this smaller-conductor reconstruction:

```text
target 14138, label (1,1,0,0), conductor 35:
  normalized abs sum 0.2659059415120284

target 1379072, label (0,3,3,0), conductor 77:
  normalized abs sum 0.027155981994015317
```

This makes the next analytic statement sharper: bound the relevant twisted
binary-prime discrepancy after aggregation modulo `35` and `77`.  It does not
remove the need for a pointwise prime-correlation theorem.

`q286_lower_support_component_pair_fixed_conductor_residue_pressure_receipt`
profiles the residue aggregates behind those fixed-conductor character sums.
Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_residue_pressure`
passed in `208.170s`.

The simple residue-level triangle bounds are too crude:

```text
channel bound: 0.05885324711081062

worst residue Linf pressure:
  target 14138, conductor 35
  residue Linf/total 0.05327502632021343
  plain Linf triangle bound 1.2786006316851224
  margin to sufficient per-residue Linf bound -0.05082280769059632
  top residues 1,32 negative and 17 positive

worst residue L1 pressure:
  target 14138, conductor 77
  residue L1/total 0.4624962038193246
  margin to channel bound -0.40364295670851397

late positive 1379072, conductor 77:
  residue Linf/total 0.003645150940944693
  residue L1/total 0.0861163627414237
  plain Linf triangle bound 0.2187090564566816
  actual worst active channel normalized sum 0.027155981994015317
```

Thus a proof cannot merely show that each residue aggregate modulo `35` or
`77` is small at the observed late scale: multiplying by `phi(77)=60` loses
too much.  The surviving theorem must exploit cancellation inside the fixed
conductor character sums, or prove a much sharper residue-discrepancy bound
than the measured late-positive aggregates suggest.  This is a useful
falsifier for a plain residue-Linf proof, not evidence against Goldbach.

`q286_lower_support_component_pair_fixed_conductor_character_cancellation_receipt`
then measures how much cancellation the active character sums actually
preserve relative to those residue envelopes.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_character_cancellation`
passed in `180.890s`.

```text
least-cancelled selected channel:
  target 14138, label (1,1,0,0), conductor 35
  actual normalized sum 0.26590594151202823
  actual / plain Linf triangle 0.20796637739931306
  actual / plain L1 triangle 0.713179126554023
  actual margin to channel bound -0.2070526944012176

worst late-positive actual channel:
  target 1379072, label (0,3,3,0), conductor 77
  actual normalized sum 0.02715598199401531
  actual / plain Linf triangle 0.12416487197179206
  actual / plain L1 triangle 0.3153405593261632
  needed actual / plain Linf triangle to clear bound 0.26909378177701265
  margin to channel bound 0.03169726511679531
```

So the late-positive row is not rescued by tiny residue aggregates; it is
rescued because the relevant character sum is only about `12.4%` of the crude
max-residue triangle envelope.  A plausible theorem target is therefore a
fixed-conductor character-cancellation estimate for the actual binary-prime
residue discrepancy, not a residue occupancy bound alone.

`q286_lower_support_component_pair_fixed_conductor_reflection_orbit_receipt`
tests whether pair-swap reflection becomes useful after the fixed-conductor
reduction.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_reflection_orbit`
passed in `217.106s`.

Reflection-orbit triangle compression is a strong but incomplete explanation:

```text
channel bound: 0.05885324711081062

passing late positives by reflection-orbit bound:
  1222142, 1323632

failing late positives by reflection-orbit bound:
  1379072

worst selected reflection-orbit envelope:
  target 14138
  label (0,1,3,0), conductor 77
  reflection-orbit L1 0.3296060502917276

worst late-positive reflection-orbit envelope:
  target 1379072
  label (0,2,6,0), conductor 77
  reflection-orbit L1 0.06039386426228221
  margin to channel bound -0.0015406171514715863
```

This revives pair-swap symmetry only in a narrower form: after aggregation to
conductors `35` and `77`, pairing residues by `r <-> N-r` explains enough
cancellation for two of the three selected late positives, but not for the
driver-bound target `1379072`.  The remaining channel theorem needs either a
small residual cross-orbit cancellation estimate or a sharper reflection-orbit
bound; plain pair-swap symmetry alone is still not a proof.

`q286_lower_support_component_pair_fixed_conductor_residual_orbit_cancellation_receipt`
then measures the signed cancellation still present after reflection-orbit
compression.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_residual_orbit_cancellation`
passed in the corrected run.

Both positive reflection-envelope failures occur at `1379072`, and both are
rescued by signed cross-orbit cancellation:

```text
failure 1:
  label (0,1,5,0), conductor 77
  actual normalized sum 0.005352592501155273
  reflection-orbit L1 0.05943056357350034
  actual/orbit-L1 ratio 0.09006464316185545
  needed ratio to clear bound 0.9902858659252705

failure 2:
  label (0,2,6,0), conductor 77
  actual normalized sum 0.01746105205795644
  reflection-orbit L1 0.0603938642622822
  actual/orbit-L1 ratio 0.289119636096235
  needed ratio to clear bound 0.9744905021347716
```

Thus the channel-side theorem target has split once more: reflection-orbit
envelopes almost suffice, and the remaining `1379072` failures need only
moderate signed cancellation across those reflection orbits.  This is still
finite selected evidence, not a uniform residual-orbit theorem.

`q286_lower_support_component_pair_fixed_conductor_orbit_polygon_receipt`
turns those two residual failures into exact complex-vector polygons.  Focused
regression `test_q286_lower_support_component_pair_fixed_conductor_orbit_polygon`
passed in `351.969s`.

```text
channel bound: 0.05885324711081062

1379072, label (0,1,5,0), conductor 77:
  edge count 38
  polygon perimeter 0.059430563573500336
  resultant 0.0053525925011552716
  closure ratio 0.09006464316185543
  largest edge 0.0063135866309737085
  largest-edge/perimeter 0.10623467541520827
  margin to channel bound 0.05350065460965535

1379072, label (0,2,6,0), conductor 77:
  edge count 38
  polygon perimeter 0.0603938642622822
  resultant 0.01746105205795644
  closure ratio 0.289119636096235
  largest edge 0.00713099129439525
  largest-edge/perimeter 0.11807476440696593
  margin to channel bound 0.041392195052854186
```

This is the numeric version of the visual idea: each reflection orbit is an
edge in the complex plane.  The residual theorem target is not merely "make
the edges small"; it is to prove that the `38` orbit edges cannot align enough
to make the resultant approach their perimeter on the selected conductor-`77`
driver-bound rows.

`q286_lower_support_component_pair_fixed_conductor_orbit_phase_profile_receipt`
bins those polygon edges by phase.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_orbit_phase_profile`
passed in `283.200s`.

```text
phase bins: 12

1379072, label (0,1,5,0):
  nonzero bins 11
  largest bin mass 0.007878236700811583
  largest bin / perimeter 0.132562039245484
  signed bin L1 0.058765359273537675
  resultant 0.0053525925011552716

1379072, label (0,2,6,0):
  nonzero bins 10
  largest bin mass 0.016182424368813935
  largest bin / perimeter 0.26794815278810286
  signed bin L1 0.06015000330167732
  resultant 0.01746105205795644
```

The harder polygon has a dominant phase bin, but even there the largest bin is
only about `26.8%` of the perimeter.  This suggests a possible proof shape:
control phase-bin mass balance and then control signed cancellation between
phase bins.  It is still a finite selected measurement, not a phase-balance
theorem.

`q286_lower_support_component_pair_fixed_conductor_phase_bin_compression_receipt`
then tests the coarser signed phase-bin envelope against the channel bound.
Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_bin_compression`
passed in `209.826s`.

```text
channel bound: 0.05885324711081062

1379072, label (0,1,5,0):
  signed bin L1 0.058765359273537675
  margin to channel bound 0.000087887837272945
  resultant 0.0053525925011552716
  phase-bin signed bound clears

1379072, label (0,2,6,0):
  signed bin L1 0.06015000330167732
  margin to channel bound -0.001296756190866699
  resultant 0.01746105205795644
  phase-bin signed bound still fails
```

This rules out the strongest easy geometric closure: phase-bin compression
alone does not certify all residual conductor-`77` polygons.  It remains useful
because it clears one of the two residual rows and leaves a single hard row
where inter-bin signed cancellation, not merely orbit-level reflection pairing,
must be proved or replaced.

`q286_lower_support_component_pair_fixed_conductor_phase_antipodal_compression_receipt`
pairs opposite phase bins.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_compression`
passed in `218.344s`.

```text
channel bound: 0.05885324711081062

1379072, label (0,1,5,0):
  antipodal phase-pair L1 0.009229827584054894
  margin to channel bound 0.049623419526755724
  resultant 0.0053525925011552716
  antipodal phase bound clears

1379072, label (0,2,6,0):
  antipodal phase-pair L1 0.03657040255445905
  margin to channel bound 0.022282844556351572
  resultant 0.01746105205795644
  antipodal phase bound clears
```

This revives the geometric route in a narrower form.  The hard row is not
explained by arbitrary phase-bin compression, but it is explained on the
selected fixture by antipodal phase-sector cancellation.  The surviving theorem
target is now explicit: prove that the conductor-`77` residual orbit polygons
have enough opposite-sector pairing, or replace that statement with a sourced
pointwise fixed-conductor binary-prime estimate.

`q286_lower_support_component_pair_fixed_conductor_phase_antipodal_pair_balance_receipt`
profiles the six antipodal phase pairs themselves.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_pair_balance`
passed in `252.478s`.

```text
high ratio threshold: 0.75

1379072, label (0,1,5,0):
  weighted antipodal cancellation ratio 0.15706238672161288
  largest pair abs 0.0031320675991354753
  high-ratio pair count 1

1379072, label (0,2,6,0):
  weighted antipodal cancellation ratio 0.6079867090121881
  largest pair abs 0.015424610859844602
  largest pair cancellation ratio 0.9711661073614952
  high-ratio pair count 2
```

This falsifies a too-strong refinement: not every antipodal phase pair
cancels uniformly.  The hard row still clears because the weighted L1 over all
six antipodal pairs is below the channel bound.  A proof should target that
weighted antipodal-pair sum, not a per-pair cancellation floor.

`q286_lower_support_component_pair_fixed_conductor_phase_antipodal_threshold_envelope_receipt`
separates high-ratio antipodal exceptions from the remaining pair mass.  With
threshold `0.75`, the envelope

```text
sum(high-ratio pair abs) + 0.75 * sum(remaining pair source mass)
```

clears both selected residual polygons.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_threshold_envelope`
passed in `395.264s`.

```text
1379072, label (0,1,5,0):
  high-ratio pair count 1
  thresholded envelope 0.044857036354937124
  margin to channel bound 0.013996210755873498

1379072, label (0,2,6,0):
  high-ratio pair count 2
  thresholded envelope 0.049789406359944485
  margin to channel bound 0.009063840750866137
```

This gives the cleanest current finite theorem shape: prove that the
high-ratio opposite-sector pairs have small total contribution, and prove a
fixed-ratio cancellation bound for the remaining antipodal pair mass.  The
receipt is still selected finite evidence, not a uniform theorem.

`q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_exception_receipt`
then checks whether the high-ratio exceptions are structurally one-sided.
Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_exception`
passed in `210.678s`.

```text
thin side ratio threshold: 0.05

1379072, label (0,1,5,0):
  high-ratio pair count 1
  maximum small/large side ratio 0.0
  high-ratio exception abs sum 0.0031320675991354753

1379072, label (0,2,6,0):
  high-ratio pair count 2
  maximum small/large side ratio 0.046829417626061014
  high-ratio exception abs sum 0.024020095646099474
```

All selected high-ratio exceptions are thin-opposite-side pairs at this
threshold.  This refines the proof target again: bound the mass of one-sided
opposite-sector exceptions, and separately prove fixed-ratio cancellation for
the non-thin antipodal pairs.  This remains finite selected evidence only.

## External source context

Fresh public-source check on 2026-09-13 confirms the route is close to known
binary Goldbach-in-progressions and zeta/L-function territory, but the checked
sources do not supply the pointwise fixed-modulus channel estimate above.

- Bhowmik, Halupczok, Matsumoto, and Suzuki,
  "Goldbach Representations in Arithmetic Progressions and zeros of
  Dirichlet L-functions", arXiv:1704.06103, states average asymptotic results
  under a conjecture on distinct zeros and conversely relates good error terms
  to zero locations:
  https://arxiv.org/abs/1704.06103
- Bhowmik and Halupczok, "Asymptotics of Goldbach Representations",
  arXiv:1809.06920, frames classical Goldbach-representation asymptotics
  against RH and AP variants against zeros of L-functions:
  https://arxiv.org/abs/1809.06920
- Halupczok, "Goldbach's problem with primes in arithmetic progressions and
  in short intervals", arXiv:1212.4406, proves mean-value style binary/ternary
  AP and short-interval estimates, with applications in ternary/almost-prime
  settings:
  https://arxiv.org/abs/1212.4406

These sources support the caution that the missing channel theorem may brush
against RH/GRH-type terrain, but they are not an importable proof of the
selected q286 conditional closure.

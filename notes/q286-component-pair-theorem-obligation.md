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

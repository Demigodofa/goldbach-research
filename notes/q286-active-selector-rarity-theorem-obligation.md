# q286 Active-Selector Rarity Theorem Obligation

Status: theorem-obligation bookkeeping only. This is not a proof of Goldbach.

## Selector

The current q286 active lane is:

```text
first_two_modes_to_principal_ratio < -0.2
first_three_modes_to_principal_ratio < -0.3
```

Therefore a theorem proving

```text
first_three_modes_to_principal_ratio >= -0.3
```

on a target range excludes the active selector on that range before any
fixed-inequality or strict-closure stress is needed.

## Exact Quantity

The fast scanner in `_q286_first_three_tail_fast_scan_receipt` computes the
same first-three singular-mode quantity as the direct mode-only receipt, but
as a fixed linear functional of strict-central prime-pair residue weights
modulo `286`.

For an even target `N`, let:

- `U_286` be the reduced residue classes modulo `286`;
- `A_N` be the admissible unit residues `u` with `(N-u,286)=1`;
- `w_N(u)` be the strict-central weighted prime-pair mass with first prime
  congruent to `u mod 286`;
- `W_N = sum_u w_N(u)`;
- `m_N = W_N / |A_N|`;
- `delta_N(u) = w_N(u) - m_N` on `A_N` and `0` off `A_N`;
- `ell` be the fixed q286 first-three singular-mode linear coefficient vector;
- `P` be the fixed principal mean per unit weight.

Then the measured quantity is:

```text
first_three(N) = Re(sum_u ell(u) delta_N(u)) / (P W_N).
```

The active-selector rarity theorem is therefore a pointwise signed
prime-pair residue discrepancy estimate:

```text
Re(sum_u ell(u) delta_N(u)) >= -0.3 P W_N
```

for all targets outside a finite checked set, or for the specific outer
target family being assembled.

## Quantified Norm Certificate

The existing executable certificate
`q286_first_three_weighted_discrepancy_norm_receipt` converts the same
linear functional into conservative sufficient conditions.  For each target
residue it subtracts the admissible mean from the q286 first-three coefficient
vector and computes:

```text
|Re(sum_u ell(u) delta_N(u))| / (P W_N)
    <= ||ell_centered||_1 * ||delta_N||_infinity / (P W_N)

|Re(sum_u ell(u) delta_N(u))| / (P W_N)
    <= ||ell_centered||_2 * ||delta_N||_2 / (P W_N).
```

Therefore either of the following would be a sufficient, non-circular route
to the active `.3` first-three cutoff on a target range:

```text
||delta_N||_infinity / W_N
    <= 0.3 P / ||ell_centered||_1

||delta_N||_2 / W_N
    <= 0.3 P / ||ell_centered||_2.
```

Direct coefficient evaluation with `theorem_threshold=.3` gives the q286
residue-class ranges:

```text
L_infinity sufficient relative-delta range:
  0.0012438599030454018 .. 0.002451362294448365

L2 sufficient relative-delta range:
  0.005955161523943415 .. 0.017908306132142508
```

The worst class for both sufficient criteria is target residue `0 mod 286`,
with `120` admissible unit residues, centered coefficient `L1`
`10612733.570460552`, centered coefficient `L2`
`2216691.1337206536`, `L_infinity` sufficient relative delta
`0.0012438599030454018`, and `L2` sufficient relative delta
`0.005955161523943415`.

This is useful because it gives a fully quantified theorem obligation.  It is
also a warning: a plain uniform q286 residue-weight discrepancy theorem strong
enough for this route would need sub-percent relative `L2` control in the
worst target residue class.  The finite scout receipts do not prove that
estimate; they only say the checked windows did not produce active-selector
rows.

## Reflection-Support Obstruction

The receipt
`q286_first_three_reflection_support_obstruction_receipt` checks whether the
rarity theorem could follow from only:

- admissible q286 residue support;
- nonnegative weights;
- fixed total mass;
- ordered prime-pair reflection symmetry `w(u)=w(N-u)`.

For each even target residue modulo `286`, it minimizes the centered
first-three coefficient over reflection orbits, then mixes the extremal orbit
with the uniform admissible distribution so every admissible residue still has
strictly positive weight.  With `tail_threshold=.3` and `slack_factor=1.25`,
all `143/143` even target residues have such a positive reflected witness with
constructed first-three ratio below `-0.3`.

Compact evidence:

```text
evidence/q286-first-three-reflection-support-obstruction.json
```

Worst extremal row:

```text
target residue 0 mod 286
extremal orbit: 23, 263
minimum extremal first-three/principal: about -6.796121290546607
```

Least-negative extremal row:

```text
target residue 10 mod 286
extremal orbit: 85, 211
minimum extremal first-three/principal: about -2.5675553132435125
```

This refutes only a support/nonnegativity/total/reflection-only rarity proof.
It does not refute a proof using actual prime-pair distribution, character
cancellation, local congruence constraints beyond reflection, finite boundary
verification, or a sharper pointwise discrepancy theorem.  It sharpens the
remaining obligation: the proof must use arithmetic distribution of binary
prime-pair residues, not merely q286 geometry.

## Reflection-Orbit Cap Diagnostic

After the reflection-support obstruction, the next natural geometric
strengthening is to bound concentration on each reflection orbit.  The receipt
`q286_first_three_reflection_orbit_cap_receipt` computes, for every even
target residue modulo `286`, the largest uniform cap `rho` such that every
reflection-symmetric probability distribution with each orbit mass at most
`rho` would force `first_three >= -0.3`.

Compact evidence:

```text
evidence/q286-first-three-reflection-orbit-cap.json
```

On the exact coefficient geometry, the sufficient caps are small:

```text
minimum sufficient max orbit mass: 0.016823304298596065
maximum sufficient max orbit mass: 0.026762977396728494
```

The one-period prime-pair window starting at `10000` violates this sufficient
cap on every tested target with prime pairs:

```text
tested targets:            5005
cap certified targets:     0
cap violation targets:     5005
maximum actual orbit mass: 0.12026969709166307
worst actual/cap ratio:    about 5.923169478623975
```

This does not show the first-three rarity theorem is false; the cap is only a
sufficient worst-case geometric condition.  It does show that a standalone
uniform reflection-orbit mass cap is far too strong for actual prime weights.
The surviving target is signed cancellation or arithmetic distribution across
orbits, not merely small maximum orbit mass.

## Reflection-Orbit Signed-Cancellation Diagnostic

The receipt
`q286_first_three_reflection_orbit_signed_cancellation_receipt` keeps the same
reflection-orbit decomposition but separates actual orbit-average contribution
by sign.  For each strict-central target, it writes the first-three ratio as:

```text
negative orbit contribution
+ positive orbit contribution
+ zero orbit contribution
```

with reconstruction checked against the direct q286 first-three value.  This
does not add a theorem; it measures the compensation theorem that would be
needed after the orbit-cap route failed.

Compact evidence:

```text
evidence/q286-first-three-reflection-orbit-signed-cancellation.json
```

On the first q286 period starting at `10000`:

```text
tested targets with prime pairs:       5005
first-three tails below -0.3:           972
negative-pressure targets:             5002
rescued negative-pressure targets:     4030
tail negative-pressure targets:         972
rescued negative-pressure fraction:    about 0.8056777289084366
maximum reconstruction error:          about 9.992007221626409e-16
```

The worst target remains `10664`:

```text
first_three/principal:                  about -1.1500880008976309
negative orbit contribution:            about -1.269809632792171
positive orbit contribution:            about 0.1197216318945406
negative orbit mass fraction:           about 0.799310342754281
positive compensation surplus to .3:    about -0.8500880008976304
```

The largest positive-compensation row is `11108`:

```text
first_three/principal:                  about 1.4825249111772503
negative orbit contribution:            about -0.6327193495305856
positive orbit contribution:            about 2.1152442607078363
maximum reflection-orbit mass fraction: about 0.12026969709166307
```

Interpretation: large orbit mass is not itself the enemy.  Almost every target
has negative orbit pressure below the `.3` threshold before compensation; most
are cleared by positive orbit contribution.  The next non-circular target is a
pointwise arithmetic lower bound on positive-orbit compensation relative to
negative-orbit pressure, or an explicit classification of the compensation
deficit rows.  This remains finite diagnostic evidence, not a proof of
eventual first-three rarity or Goldbach.

## Reflection-Orbit Ratio Certificate

The receipt
`q286_first_three_reflection_orbit_ratio_certificate_receipt` turns the signed
decomposition into an explicit sufficient condition.  Let
`B=-negative_orbit_contribution` and
`R=positive_orbit_contribution/B`.  With the fixed constants

```text
B <= 1.25
R >= 0.76
```

one has the algebraic implication

```text
first_three >= -(1 - 0.76)*1.25 = -0.3.
```

The receipt does not prove either inequality.  It only measures where actual
strict-central q286 rows satisfy this fixed certificate.

Compact evidence:

```text
evidence/q286-first-three-reflection-orbit-ratio-certificate.json
```

Single-period window results:

```text
baseline start 10000:
  tails: 972
  certified: 3645
  certified tails: 0
  uncertified clear: 388
  uncertified tails: 972
  pressure failures: 16
  ratio failures: 1356

intermediate start 90080:
  tails: 241
  certified: 4451
  certified tails: 0
  uncertified clear: 313
  uncertified tails: 241
  pressure failures: 0
  ratio failures: 554

late start 1120120:
  tails: 0
  certified: 5005
  certified tails: 0
  uncertified clear: 0
  uncertified tails: 0
  pressure failures: 0
  ratio failures: 0
```

The late minimum-ratio row is `1129472`, with
`R=0.7600375137629325` and first-three/principal about
`-0.2192068192668631`.  The late maximum-pressure row is `1122550`, with
`B=1.049858297023376` and first-three/principal about
`0.08634675899428819`.

Interpretation: this is a real algebraic certificate and a sharper eventual
theorem target: prove an eventual negative-pressure ceiling and an eventual
positive-compensation ratio floor, then finitely check the earlier
uncertified rows.  The early/intermediate windows also show why this is not
already a proof: ratio failures explain the remaining tails, and the constants
are only measured, not proved.

## Pressure-Ratio Cycle Horizon

The receipt
`q286_first_three_reflection_orbit_ratio_cycle_horizon_receipt` applies the
same fixed certificate by q286 cycle.  It is not a new threshold search: the
constants remain `B <= 1.25` and `R >= 0.76`.

Compact evidence:

```text
evidence/q286-first-three-reflection-orbit-ratio-cycle-horizon.json
```

In the early horizon from start `10000`, cycles `0..15`:

```text
tested targets with prime pairs:       80080
tails:                                  5297
certified targets:                     70016
certified tails:                           0
uncertified clear targets:              4767
uncertified tails:                      5297
pressure failures:                        24
ratio failures:                        10059
all-certified cycles:                     []
no-tail cycles:                           []
```

In the late horizon from start `1120120`, cycles `0..7`:

```text
tested targets with prime pairs:       40040
tails:                                     0
certified targets:                     40029
certified tails:                           0
uncertified clear targets:                11
uncertified tails:                         0
pressure failures:                         0
ratio failures:                           11
all-certified cycles:                    [0]
no-tail cycles:             [0,1,2,3,4,5,6,7]
```

The late minimum-ratio clear exception is target `1178192`, with
`R=0.7199213315162449`, `B=0.954498236614443`, and first-three/principal about
`-0.2673345951810655`.  This is an important demotion: the fixed ratio floor
`.76` is a useful sufficient certificate, but it is too strict to certify all
late no-tail rows.  The next theorem target must either prove the fixed
certificate only on a subregion plus classify the clear exceptions, or replace
`.76` with a pressure-dependent compensation curve that still implies the
`-.3` first-three floor.

Kevin's suggested clean rectangle `B <= 1`, `R >= 0.70` has the same algebraic
bound:

```text
first_three >= -(1 - 0.70)*1 = -0.3.
```

Compact evidence:

```text
evidence/q286-first-three-reflection-orbit-b1-r70-certificate.json
```

On the same horizons, this candidate gives:

```text
early cycles 0..15 from start 10000:
  tails:                       5297
  certified targets:          69838
  certified tails:                0
  uncertified clear targets:   4945
  uncertified tails:           5297
  pressure failures:           5370
  ratio failures:              6734

late cycles 0..7 from start 1120120:
  tails:                          0
  certified targets:          39829
  certified tails:                0
  uncertified clear targets:    211
  uncertified tails:              0
  pressure failures:            211
  ratio failures:                 0
```

This is a useful changed condition: lowering the ratio floor to `.70` clears
the late ratio exceptions, but the `B <= 1` pressure ceiling becomes the only
late failure mode.  The late maximum-pressure clear exception is target
`1179464`, with `B=1.0671808195157813`, `R=0.8345837922126714`, and
first-three/principal about `-0.17652900418767442`.  This points away from one
rectangle and toward the curve `R >= 1 - .3/B`, or a two-region theorem:
`B <= 1` with `R >= .70`, plus a separate high-pressure clear-row mechanism.

The three-branch rational staircase makes that curve idea explicit while
keeping complete algebraic quantifiers.  With
`B=-negative_orbit_contribution` and `R=positive_orbit_contribution/B`, each
branch below satisfies `(1-R)B <= .3`, hence certifies
`first_three >= -.3`:

```text
B <= 1,     R >= 7/10
B <= 21/20, R >= 5/7
B <= 5/4,  R >= 19/25
```

Compact evidence:

```text
evidence/q286-first-three-reflection-orbit-staircase-certificate.json
```

On early cycles `0..15` from start `10000`, the staircase certifies `73101`
of `80080` targets and has no certified-tail counterexample, but all `5297`
first-three tails remain outside the staircase; another `1682` clear targets
also remain outside it.  The worst uncertified row is still target `10664`,
with first-three/principal about `-1.1500880008976309`.

On late cycles `0..7` from start `1120120`, where the two flat rectangles had
complementary clear failures, the staircase certifies all `40040` targets and
has zero uncertified rows.  In particular, the prior dual-rectangle
intersection row `1157462` is certified by the middle branch:
`B=1.0267310119901476`, `R=0.7346113305066312`, and exact curve margin about
`0.026800810026198607`.

On the unchanged holdout from start `1200200`, cycles `0..7`, the staircase
tests another `40040` targets and leaves exactly two rows outside the union:
tail target `1222142` and clear target `1242118`.  The tail row has
`B=1.0110386036156538`, `R=0.6957705083951388`, first-three/principal about
`-0.30758776037087937`, and exact-curve margin about
`-0.007504916571675957`.  The clear row has
`B=1.0002438240043041`, `R=0.7136430774230906`, first-three/principal about
`-0.28642674326843226`, and exact-curve margin about
`0.01356994805249534`.  So the holdout refines the theorem target rather than
falsifying the algebra: the unchanged staircase avoids certifying the true
tail but is still slightly too coarse near the exact curve.

Status: `aha-candidate`, finite diagnostic.  The mechanism is now a precise
eventual theorem candidate: prove that all sufficiently late q286 rows lie in
this safe staircase, or replace the staircase by the exact pressure-dependent
curve `R >= 1 - .3/B`, then separately discharge the finite early rows outside
it.  No eventual staircase occupancy theorem, first-three rarity theorem,
signed prime-correlation estimate, or Goldbach proof is established.

A post-hoc refinement of the holdout miss inserts one exact rational branch
between the first two steps:

```text
B <= 101/100, R >= 71/101
```

This is algebraically safe because `(1-71/101)*(101/100)=3/10`.  The refined
four-branch staircase is recorded in:

```text
evidence/q286-first-three-reflection-orbit-refined-staircase.json
```

On the same three horizons it has no certified-tail counterexample.  It leaves
the genuine holdout tail `1222142` outside the certificate, but now certifies
the clear holdout row `1242118` by the added step.  The holdout
`1200200`, cycles `0..7`, therefore changes from two outside rows to exactly
one outside row, the tail `1222142`.  Early cycles `0..15` improve only
slightly, from `1682` to `1669` uncertified clear rows, while all `5297` tails
remain outside.  This is useful theorem shaping but is not independent
validation, because the added step was chosen after seeing the holdout clear
miss.

A direct boundary-pair autopsy is recorded in:

```text
evidence/q286-first-three-boundary-pair-autopsy.json
```

In the holdout from start `1200200`, only three rows lie in the near-threshold
window `-.33 <= first_three <= -.27`: tail `1222142`, clear `1242118`, and
clear `1240888`.  Relative to tail `1222142`, clear row `1242118` improves by
`0.02116101710244711`, split almost evenly between lower negative pressure
(`0.01079477961134967`) and higher positive compensation
(`0.010366237491097219`).  Clear row `1240888` has worse negative pressure by
about `0.0046492825627517664`, but has higher positive compensation by about
`0.03755294143301424`, for net improvement about
`0.03290365887026253`.  Thus the near-boundary rows already show at least two
rescue patterns: balanced pressure/compensation improvement, and compensation
overcoming worse pressure.

The character-coordinate autopsy for this q286 first-three layer has support
`(11,13)` on natural modulus `286`.  A conductor-77 explanation is therefore
not native to this receipt; conductor `77` belongs to the separate
lower-support/component-pair lanes and needs an explicit overlay test before
being claimed relevant here.

The positive-orbit landing profile is recorded in:

```text
evidence/q286-first-three-positive-orbit-landing-profile.json
```

It converts the autopsy into the explicit factorization
`first_three = -B + P`, with
`B = negative_mass * negative_landing_mean_abs` and
`P = positive_mass * positive_landing_mean`.  On the holdout from start
`1200200`, cycles `0..7`, it finds the same three near-boundary rows and
classifies clear `1242118` as a balanced reduced-pressure plus increased
positive-compensation row, while clear `1240888` is a
positive-compensation-over-worse-pressure row.

The useful correction is that "positive compensation" here is primarily a
mass-allocation statement, not a higher positive-landing-mean statement.  For
`1242118`, positive mass fraction rises by about `0.039081854763197754`
relative to tail `1222142`, while its positive landing mean decreases by about
`0.10041285646025777`.  For `1240888`, positive mass fraction rises by about
`0.08474552493215814`, while positive landing mean decreases by about
`0.17154941547522462`.  Thus the next theorem mechanism should classify
mass transfer between negative and positive orbit classes near the exact
curve, not merely search for stronger positive-orbit average coefficients.

The simple positive-mass separator falsifier is recorded in:

```text
evidence/q286-first-three-positive-mass-threshold-falsifier.json
```

It tests the tempting local rule suggested by the holdout:

```text
near-boundary row and positive_orbit_mass_fraction >= .49
    => clear first_three >= -.3.
```

The rule happens to split the three near-boundary rows in the
`1200200` holdout: the two clear rows are above `.49`, and the tail
`1222142` is below.  But it fails immediately on broader windows.  On early
cycles `0..15` from start `10000`, among `2289` near-boundary rows there are
`265` high-positive-mass tails and `896` low-positive-mass clear rows.  On
the next cycles `8..15` from start `90080`, among `677` near-boundary rows
there are `64` high-positive-mass tails and `294` low-positive-mass clear
rows.  Thus positive mass share alone is not a theorem mechanism; any viable
mass-transfer theorem must also use landing means, orbit coefficients, target
residue structure, or another arithmetic constraint.

The mass-matched opposite-outcome decomposition is recorded in:

```text
evidence/q286-first-three-mass-matched-pair-decomposition.json
```

It keeps the same near-boundary window and decomposes each clear-minus-tail
matched pair by the exact midpoint product identities
`B = negative_mass * negative_landing_mean_abs` and
`P = positive_mass * positive_landing_mean`.  Matching prioritizes identical
target residue modulo `286`, then identical reflection-orbit sign masks, then
nearest positive/negative mass fractions.  In early cycles `0..15`, all
`1024` tail pairs are same-residue/sign-mask matches; in cycles `8..15`,
`264/283` are same-residue/sign-mask matches; the late `1120120` window has
no near-boundary tail rows; and the `1200200` holdout has one fallback pair.

This changes the mechanism picture.  Across all `1308` matched pairs, the
positive landing-quality term is positive in `865` pairs and is the largest
absolute term in `769` pairs, with aggregate sum about `40.420704`.  The
positive mass-transfer term is almost sign-balanced (`657` positive,
`651` negative) and aggregate sum about `1.388876`.  The holdout fallback pair
`1222142 -> 1242118` is different: both positive mass transfer and negative
pressure mass control are large and helpful, but they are mostly offset by
worse positive and negative landing-quality terms.  Therefore the next proof
target is a coupled mass/landing arithmetic estimate near the exact curve, not
positive mass share alone and not pressure control alone.

The exact mass/landing theorem obligation is recorded in:

```text
evidence/q286-first-three-mass-landing-obligation.json
```

For actual strict-central binary-prime mass on the q286 first-three
reflection-orbit sign classes, write
`P = m_plus * ell_plus`, `B = m_minus * ell_minus`, and
`first_three = P - B`.  The pointwise first-three rarity theorem at threshold
`tau=.3` is exactly:

```text
m_plus(N) * ell_plus(N) + tau >= m_minus(N) * ell_minus(N).
```

On the holdout sample rows, tail `1222142` has slack about
`-0.00758776037087916`; clear rows `1242118` and `1240888` have slacks about
`0.013573256731567618` and `0.025315898499383316`.  The recorded
mass/landing and threshold-slack reconstruction errors are below `2.3e-16`.
This is theorem-obligation bookkeeping, not a proof: the missing input is a
pointwise arithmetic estimate for actual binary-prime residue weights forcing
that inequality.

The backward orbit-uniformity budget is recorded in:

```text
evidence/q286-first-three-orbit-uniformity-budget.json
```

For each target residue `a`, local uniform reflection-orbit mass gives
`first_three=0`, so
`first_three(N)=<mu_N-u_a,c_a>`.  Therefore either
`||mu_N-u_a||_1 <= tau/||c_a||_infinity` or
`||mu_N-u_a||_2 <= tau/||c_a||_2` is a rigorous sufficient condition for
`first_three(N) >= -tau`.  With `tau=.3`, the q286 even-residue budgets range
from about `0.0093982579157629` to `0.07455426391330403` in L1 and from about
`0.007916843497532824` to `0.03539182086849026` in L2.

The stress rows show why this backward theorem is too blunt as the main proof
route.  Tail `1222142` fails the budget, but clear rows `1242118` and
`1240888` fail it as well.  The clear row `1242118` has L1 budget utilization
about `14.291145699121145` and L2 utilization about
`2.9097499848440553`; `1240888` has L1 utilization about
`6.505901726697682` and L2 utilization about `1.82647385924401`.  Thus a
generic orbit-uniformity theorem would be sufficient but far stronger than
the observed active-scale rescue mechanism requires.  The live target remains
coefficient-sensitive mass/landing control.

## Current Evidence

Finite denominator evidence so far:

- `evidence/q286-tail-selector-grid-12x25.json`: `300` neutral selector
  targets, zero active-tail hits.
- `evidence/q286-first-three-tail-scout-4x12x25.json`: `1200` targets, zero
  first-three hits below `-0.3`.
- `evidence/q286-first-three-tail-scout-8x12x25-late.json`: `2400` later
  targets, zero first-three hits below `-0.3`; worst block minimum
  `-0.1282544626188415` at target `2562584`.
- `evidence/q286-tail-selector-active-residue-holdout-6x5.json`: `30`
  same-residue holdout targets after `1379072`, zero active-tail hits.

Strict closure has still only been stressed on the selected late active rows
`1222142`, `1323632`, and `1379072`. The finite rarity evidence must not be
counted as strict-closure support.

## Falsifier

Any unchanged-selector holdout that finds a target with:

```text
first_three(N) < -0.3
```

falsifies a naive finite rarity extrapolation and must be escalated to the
full active selector. If it also satisfies `first_two < -0.2`, the strict
closure receipt must be run with unchanged constants. A nonpositive strict
closure margin would falsify the current conditional constants.

## Proof Routes

1. Prove the pointwise residue-discrepancy inequality above by analytic means.
   This is a binary prime-pair distribution estimate modulo `286` with a
   signed q286 test vector; it is close to known hard territory around
   Goldbach in arithmetic progressions and L-function zero control.
2. Prove a weaker eventual theorem: after a finite bound `N0`, the
   first-three ratio is above `-0.3`, then check all active-selector targets
   below `N0` by exact receipts.
3. Abandon rarity as the main path if new holdouts produce repeated active
   rows, and instead use those rows to stress the fixed strict-closure
   inequality or identify a new channel-bound obstruction.

## Boundary

This obligation would close only the current q286 active selector. It would
not by itself prove Goldbach. The outer assembly, finite boundary cases,
endpoint/noncentral terms, and signed prime-correlation control remain open.

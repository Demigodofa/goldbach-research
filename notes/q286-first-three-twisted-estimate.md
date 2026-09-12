# q286 first-three twisted estimate target

Status: theorem-shaped target, not proved.

Date: 2026-09-12.

## Context

The strict-central assembled coefficient on `U_10010` has been reduced to a
positive principal contribution plus exact lower-modulus support channels.  In
the dominant `q286 = 2*11*13` support, the centered component is split into a
local lower-modulus prediction, six separable singular modes, and a small
measured tail.

Finite diagnostics show that the first three q286 singular modes are the
active lower-tail core on the first complete residue period:

- On `10000..20008`, all `75` negative full-action targets have negative
  first-three q286 mode sum.
- Removing modes `1`, `2`, and `3` leaves no nonpositive full-action target
  in that period.
- The worst remaining full-action ratio after removing those modes is
  `0.018073313793834367` principal, at `N=14138`.
- Removing only modes `1` and `2` leaves one target, `N=14138`, still negative
  by `0.007038026892741689` principal.

This makes modes `1..3` the present proof target.  The claim is finite
evidence only.

## Exact finite object

For each leading mode `j`, the q286 coefficient is separable:

```text
C_j(r) = sigma_j A_j(r mod 11) B_j(r mod 13)
```

where `A_j` and `B_j` are finite mixtures of nonprincipal multiplicative
characters.  For a strict-central even target `N`, the mode contribution is

```text
T_j(N) =
  sum_{N/3 < p < 2N/3, p and N-p prime}
    log(p) log(N-p) C_j(p mod 286).
```

Equivalently, after expanding `A_j` and `B_j`,

```text
T_j(N) =
  sigma_j sum_{alpha=1..9} sum_{beta=1..11}
    u_{j,alpha} v_{j,beta}
    sum_{N/3 < p < 2N/3}
      Lambda(p) Lambda(N-p)
      chi_11(p)^alpha chi_13(p)^beta,
```

up to the already-explicit endpoint convention replacing prime sums by
strict-central weighted prime-pair sums.

The mode vectors are broad, not single-character:

- Mode `1`: effective side character counts `4.899124389855417` and
  `5.8587969819448205`.
- Mode `2`: effective counts `3.994990282499014` and
  `4.9888048746106834`.
- Mode `3`: effective counts `4.787886564984907` and
  `5.526188486527063`.
- The largest side character-energy fraction among these six sides is only
  `.2588529653280147`.

So a proof cannot estimate one exceptional character and call the mode paid.
It needs a finite but broad small-conductor mixture.

## Sufficient estimate shape

Let

```text
P(N) = positive principal contribution,
R_0(N) = exact non-q286 supports + q286 local + modes 4..6 + q286 tail.
```

The strict-central coefficient action is

```text
P(N) + R_0(N) + T_1(N) + T_2(N) + T_3(N).
```

A direct sufficient theorem is therefore:

```text
T_1(N) + T_2(N) + T_3(N) > -P(N) - R_0(N)
```

for every sufficiently large even `N`, with a finite check below the onset.

A cleaner but stronger route would prove constants `eta, rho > 0` and an
onset `N_0` such that

```text
R_0(N) >= -eta P(N),
T_1(N) + T_2(N) + T_3(N) >= -(1 - eta - rho) P(N)
```

for all even `N >= N_0` in the strict-central unit range.  The finite
diagnostics only motivate this split; they do not prove either inequality.

## Why this is hard

The inner sums are fixed-modulus, one-sided twisted binary-prime correlations:

```text
sum Lambda(p) Lambda(N-p) chi(p).
```

The character is nonprincipal and has small fixed conductor, so the expected
main term is zero after local averaging.  But the required conclusion is a
pointwise lower-tail bound for every even `N`, not merely an averaged
equidistribution statement.  This is exactly the kind of signed prime
correlation estimate that the project has not yet proved.

Chen-type results are a warning sign here.  Replacing one prime by an almost
prime avoids part of the parity obstruction.  Forcing the remaining almost
prime factor to be prime is not usually a small refinement of the same sieve;
it is the missing binary-prime correlation strength.  In this project, the
analogous "final factor" appears as pointwise control of the first-three
q286 twisted correlations.

## Source-boundary check

Current primary/expository source checks support caution rather than direct
import of a theorem.  Halupczok's 2012 paper, "Goldbach's problem with primes
in arithmetic progressions and in short intervals", states mean-value
theorems of Bombieri-Vinogradov type for binary and ternary additive prime
problems in arithmetic progressions and short intervals.  That is adjacent,
but it is not the pointwise lower-tail theorem for our fixed target `N`.

Bhowmik, Halupczok, Matsumoto, and Suzuki's "Goldbach Representations in
Arithmetic Progressions and zeros of Dirichlet L-functions" is also cautionary:
its abstract obtains average asymptotics under a distinct-zero conjecture for
Dirichlet L-functions, and relates good error terms back to zero locations and
possible Siegel zeros.  The Bhowmik-Halupczok survey notes that good average
orders with strong error terms in the arithmetic-progression setting are tied
to GRH-type hypotheses.

Working conclusion: do not cite the literature as already proving our
first-three q286 pointwise lower-tail estimate.  The direct target remains a
new in-repo proof obligation, or a carefully sourced theorem whose hypotheses
match this exact fixed-modulus, strict-central, weighted, pointwise form.

## Next falsifiers

1. Test whether first-three removal leaves a positive margin on more complete
   period cycles, not just the first period.
2. Measure whether the first-three lower tail decays with lifts of the same
   residue class, or whether it has recurring large negative excursions.
3. Compare first-three mode sums to classical fixed-modulus AP discrepancy
   proxies; if the bad targets are selected by ordinary residue imbalance,
   a sourced AP theorem might help.  If not, the proof needs a genuine
   binary-correlation input.
4. Preserve the endpoint/noncentral reconciliation separately; this note only
   concerns the strict-central unit coefficient action.

## AP discrepancy proxy result

`q286_first_three_ap_discrepancy_proxy_receipt` compares the first-three q286
mode sum against two ordinary residue-discrepancy envelopes.  For each target,
it forms the strict-central prime-pair weight in every admissible residue
class modulo `286`, subtracts the uniform admissible mean, and compares the
first-three mode action with:

- a uniform residue-error `L^1` envelope,
- a Cauchy `L^2` envelope,
- the actual alignment with that `L^2` envelope.

On selected hard targets
`10424,10664,14138,30164,40676,85496,88346,11194,15272`, the required
uniform relative residue error to match the actual first-three mode size lies
between about `.130487` and `.528174`.  The largest lower-tail selected case
is `10664`, with first-three ratio `-1.150088`, maximum residue deviation
`2.315106`, required uniform error `.528174`, and L2 alignment `.220032`.

On the complete first period `10000..20008`, the first-three q286 mode sum is
negative at `2525` of `5005` targets.  The worst lower tail is again `10664`,
with first-three/principal ratio `-1.1500880008976306`.  The largest required
uniform relative error over negative first-three targets is
`.5281735902332463`, again at `10664`; over all targets the largest two-sided
value is `.7408970850830631` at `10724`, where the first-three mode is
positive.  The largest L2 alignment over negative first-three targets is only
`.26921675478661156`, at `14892`; the largest two-sided alignment is
`.3784984423382312`, at `17446`.

Status `changed-under-evidence`: a naive AP-discrepancy proof would need a
pointwise uniform residue error well below the actually observed residue
fluctuations at small scale, while the Cauchy L2 envelope is loose by a factor
of at least about `1/.269` on the lower tail.  Ordinary AP discrepancy remains
a useful diagnostic, but a proof still needs coefficient-sensitive binary
correlation structure rather than just a black-box full-residue equidistribution
bound.

## Exact-negative residue drivers

`q286_first_three_full_negative_driver_receipt` restricts the AP-proxy
diagnostic to exact full-action negative targets.  On the first full period
`10000..20008`, there are `75` exact negatives.  Among their top eight
negative residue drivers, residue `133` appears in `60` cases and is empty
relative to the uniform admissible mean in all `60`; residue `153` appears in
`61` cases and is empty in `59`.  Both residues appear in `46` cases, and
both are empty in `44`.

The top eight residue terms carry a moderate but not total amount of the
absolute real contribution: minimum fraction `.44127253691663915`, mean
`.5145044943315689`, maximum `.639566987107544`.

Status `aha-candidate`: the worst strict-central failures often come from
missing high-positive first-three q286 coefficient residues, especially `133`
and `153`, each of which contributes about `-0.3224` principal when empty in
the main hard cases.  This gives a sharper residue-hitting subproblem, but it
does not explain all negatives and cannot replace the broader twisted
correlation estimate.

The same receipt now separates local admissibility from genuine empty
admissible classes.  Among the `75` exact negatives, residue `133` is locally
admissible `68` times, empty in `60`, positive in `8`, and inadmissible in
`7`; residue `153` is admissible `70` times, empty in `59`, positive in `11`,
and inadmissible in `5`.  Both driver residues are admissible in `63` exact
negative targets and both are admissible-empty in `44`.

This refines the residue-hitting subproblem: a proof cannot merely say these
classes are sometimes locally unavailable.  In many exact negative cases they
are locally available but contain no strict-central prime pair at the tested
scale.

## Driver-residue lift occupancy

`q286_driver_residue_lift_occupancy_receipt` follows the exact first-period
negative base targets through period lifts `(0,1,4,9,19,49)` and tests literal
strict-central occupancy in residues `133` and `153`.

Default run: `75` first-period negative bases and `450` lifted targets.  At
lift `0`, all `75` bases are negative; both driver residues are admissible in
`63` cases, both admissible-empty in `44`, at least one driver residue is
positive in `19`, and both are positive in `0`.

At lift `1`, no lifted target is negative; both driver residues are still
admissible in `63` cases, both admissible-empty in only `6`, at least one is
positive in `66`, and both are positive in `38`.  At lift `4`, both-empty
disappears, at least one driver is positive in `74`, and both are positive in
`59`.  At lifts `9,19,49`, at least one driver is positive in all `75`; both
are positive in `61,63,63` respectively.

Status `aha-candidate`: the high-positive driver residues tend to fill quickly
under sampled period lifts of first-cycle bad bases, matching the observed
positivity of the full action at those lifts.  However, lift `1` already has
six positive targets where both driver residues are still admissible-empty, so
driver-residue hitting is not equivalent to positivity.  It is a finite clue,
not a substitute for the first-three twisted correlation estimate.

A consecutive-lift check over lifts `0..10` sharpens the same clue.  It uses
the same `75` first-period negative bases and tests `825` lifted targets.
The full action is negative only at lift `0`:

```text
negative full-action counts:
  0:75, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0
```

First-hit summary:

- every base has positive full action by lift `1`;
- every base has at least one positive driver residue by lift `2`;
- every base is no longer in the "both driver residues admissible-empty"
  condition by lift `2`;
- all possible bases with both driver residues positive attain that by lift
  `3`, but `12` bases do not have both driver residues positive in lifts
  `0..10`.

Per-lift driver occupancy:

```text
both admissible-empty:
  0:44, 1:6, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0
any driver positive:
  0:19, 1:66, 2:73, 3:75, 4:74, 5:75, 6:75, 7:75, 8:75, 9:75, 10:75
both drivers positive:
  0:0, 1:38, 2:56, 3:61, 4:59, 5:59, 6:60, 7:63, 8:63, 9:61, 10:63
```

Status `changed-under-evidence`: the first-cycle failures are not stable under
nearby period lifts, and the driver-empty obstruction disappears by lift `2`.
This strengthens the residue-occupancy hypothesis, but also shows the theorem
cannot be "both drivers are always hit" because `12` bases lack simultaneous
positive occupancy in these lifts.  The next useful finite question is whether
a small, explicitly chosen set of high-positive q286 residues forms a stable
hitting cover for the observed lower tail, or whether the missing coefficient
mass moves too much and forces the full twisted binary-prime estimate.

## High-positive residue cover

`q286_high_positive_residue_cover_receipt` tests that next finite question
directly on the observed first-period negative targets.  It looks inside the
largest negative first-three residue contribution rows and keeps only residues
with positive q286 coefficient, negative weight deficit, and zero literal
strict-central prime-pair weight.  These are the "empty high-positive
coefficient" defects.

For the `75` exact full-action negative targets, with `top_count=24`, the
greedy cover is:

```text
residue 133 covers 60 targets
residue 153 covers the remaining 15 targets
uncovered targets: 0
```

The most frequent empty high-positive coefficient residues in those top rows
begin:

```text
133:60, 153:59, 5:37, 123:36, 163:32, 17:31, 119:31,
71:27, 269:27, 281:26, 167:25, 239:25
```

Status `aha-candidate`: the original pair `133,153` is not just visually
prominent; within the top-24 negative contribution rows it covers every
first-period full-action failure by empty high-positive coefficient defects.
The caveat is equally important: this is an observed finite cover using ranked
local rows, not a proof that those residues must be occupied at large scale.
The analytic target is now sharper: prove enough lower occupancy in this
explicit high-positive residue pair, or prove that the compensating positive
mass must arrive through the broader q286 coefficient mixture.

The same cover survives the first eight complete periods when the negative
targets are first extracted from `q286_first_two_mode_lower_tail_receipt` and
then passed to `q286_high_positive_residue_cover_receipt` as selected targets.
Across `40040` tested targets, there are `89` full-action negatives.  With
`top_count=24`, the high-positive empty-residue greedy cover is still:

```text
residue 133 covers 70 targets
residue 153 covers the remaining 19 targets
uncovered targets: 0
```

Status `strengthened-aha-candidate`: the `133/153` cover is not merely a
first-period accident among the currently observed lower-tail targets.  The
proof gap is now quite specific: a pointwise theorem must either force
occupation of these two high-positive residue channels often enough, or show
that any failure of these channels is compensated by the remaining q286
coefficient mixture.

## Exact local target for residues 133 and 153

The two cover residues are units modulo `286`:

```text
133 == 1 mod 11, 3 mod 13
153 == -1 mod 11, -3 mod 13
```

For an even target `N`, the residue channel `p == r mod 286` is locally
admissible exactly when `N-r` is also a unit modulo `286`.  Since parity is
automatic for even `N` and odd `r`, only the `11` and `13` factors matter.
Thus:

- residue `133` is inadmissible only if `N == 1 mod 11` or `N == 3 mod 13`;
- residue `153` is inadmissible only if `N == -1 mod 11` or `N == -3 mod 13`;
- both residues are admissible in `99` of the `143` residue classes modulo
  `143`;
- at least one residue is admissible in `141` of `143` classes;
- both are inadmissible only for `N == 23 mod 143` and `N == 120 mod 143`.

The exact analytic subproblem is therefore:

```text
For all sufficiently large even N outside the two both-inadmissible classes,
prove enough strict-central prime pairs with p == 133 or 153 mod 286,
or prove an explicit compensating lower bound from the remaining q286
coefficient channels when these two channels are empty or deficient.
```

This is sharper than a generic fixed-modulus AP estimate because the desired
bound is pointwise in `N`, weighted by the strict-central interval, and tied to
the signed coefficient margin needed to overcome the observed lower tail.

## Cover-residue margin

`q286_high_positive_cover_margin_receipt` measures the amount of extra
strict-central log-weight in the cover residue rows that would flip a bad
target's signed action.  It combines the AP-residue row slopes with the full
assembled action ratio.  This asks how strong an occupancy theorem would need
to be, not whether such a theorem has been proved.

On the `89` full-action negative targets from the first eight complete
periods, using cover residues `133,153` and `top_count=24`, the receipt gives:

```text
tested targets: 89
cover-residue margin rows: 152
missing targets: 0
maximum required weight to flip full action: 161.06677938455093
worst full-action target/residue: N=14138, residue 153
maximum target-minimum required weight to flip full action: 161.06677938455
maximum required weight to cancel first-three alone: 927.3759573295491
worst first-three target: N=88346
```

Status `theorem-target-sharpened`: nonempty occupation of `133` or `153` is
not the right sufficient statement by itself.  The proof needs a quantitative
pointwise lower bound for strict-central log-weight in these channels, or an
explicit compensation term.  The worst observed full-action gap is much smaller
than the worst first-three-only gap, which means the remaining coefficient
mixture is already compensating substantially and should be kept in the proof
model rather than discarded.

## Strength audit for the residue-occupancy route

The cleanest possible residue theorem would assert, for every sufficiently
large even `N` in the `141/143` locally supported classes,

```text
sum_{N/3 < p < 2N/3, p == 133 or 153 mod 286}
  log(p) log(N-p) 1_{N-p prime}
  >= required_margin(N).
```

Any positive lower bound in this form already gives a strict-central Goldbach
representation for those classes.  So the pure occupancy route is not a small
technical refinement; it is a restricted binary Goldbach theorem with one prime
forced into one of two fixed residue classes.  The two both-inadmissible
classes would still need compensation or a different residue set.

This reframes the value of the `133/153` discovery.  Its promise is not that
local admissibility alone will prove occupancy.  Its promise is that the
coefficient decomposition may reduce the signed lower-tail problem to a
finite, explicit pair of channels plus a measured compensating remainder.  A
credible proof should therefore keep one of two shapes:

- a genuinely new pointwise binary-prime-in-AP estimate for the cover channels,
  strong enough to beat the measured margin;
- a compensation theorem showing that whenever the cover channels are empty or
  deficient, the remaining q286 coefficient mixture and lower-modulus channels
  supply the missing positive mass.

This is the current curiosity-guided fork.  The next falsifier is to search for
observed targets where the cover residues are admissible-empty but the full
action is still positive, then measure which remaining coefficient rows provide
the compensation.  If the compensator moves chaotically, the route collapses
back to the full signed prime-correlation estimate.  If the compensator is
structured, it may give a second finite channel cover.

## Compensation when the cover pair remains empty

The first compensation falsifier used `q286_driver_residue_lift_occupancy_receipt`
on lifts `0,1,2`.  Among the lifted targets, there are exactly six positive
full-action cases where both cover residues remain admissible-empty:

```text
25036, 25306, 25372, 25582, 26002, 26722
```

Their first-three q286 mode sums are still negative, so the positive full
action comes from compensation outside the cover pair and outside the isolated
first-three deficit.  Looking at the top eight positive first-three residue
contribution rows for these six targets gives the leading recurrence counts:

```text
1:4, 265:4, 263:3, 211:3, 283:3,
177:2, 285:2, 45:2, 239:2, 109:2, 119:2, 199:2, 127:2
```

The top negative rows remain highly structured:

```text
133:6, 153:6, 23:6, 75:4, 159:3, 243:3
```

Status `partial-falsifier`: compensation exists, but it is not yet as clean as
the `133/153` negative cover.  The positive rows have several repeated
residues rather than a single obvious second pair.  This keeps the compensation
route alive, but warns that the next theorem may need a finite positive
portfolio or the full coefficient mixture, not just one additional channel.

`q286_cover_pair_compensation_portfolio_receipt` preserves the same check as a
reusable diagnostic.  With the default six compensation targets and
`top_count=24`, the greedy positive-row portfolio is:

```text
residue 263 covers all 6 targets
uncovered targets: 0
positive contribution ratio sum for residue 263: 0.24395443390945223
```

The strongest recurrence counts among the top positive rows are:

```text
263:6, 1:6, 283:6, 211:5, 265:5, 45:5, 285:5, 239:5,
127:4, 177:4, 179:4, 19:4
```

For these six targets, every first-three mode sum remains negative; the
largest is `-0.45659669277283`.  The full action becomes positive because the
non-first-three part is large: `full_without_first_three/principal` ranges
from `1.1168686400774108` to `1.5840594595083313`.

Status `refined-compensation`: residue `263` is a clean finite positive-row
portfolio marker for the first observed compensation cases, but the decisive
positive mass is still the broader full-without-first-three component.  The
next falsifier is therefore to test whether `263` persists when searching
positive full-action targets with empty `133/153` outside these six lifted
cases, and whether the full-without-first-three lower bound has a structural
explanation.

That next falsifier was run over the whole first period.  Among `5005` targets,
there are `204` positive full-action targets where both `133/153` are
admissible-empty, compared with `44` negative both-empty cases.  Applying the
same top-positive first-three portfolio scan with `top_count=24` to those
`204` positive both-empty targets gives a five-residue greedy cover:

```text
179 covers 135 targets
29 covers 41 additional targets
167 covers 17 additional targets
241 covers 8 additional targets
109 covers the remaining 3 targets
uncovered targets: 0
```

The most frequent positive-row residues in those `204` targets begin:

```text
179:135, 109:124, 243:121, 29:106, 111:104, 89:102,
241:95, 265:93, 127:92, 263:91, 145:86, 3:85
```

Status `single-compensator-falsified`: residue `263` is not the global
first-period compensator for positive both-empty targets.  The compensation
route remains structured, but the observed structure is a finite portfolio
with several moving residues.  A proof that discards the compensating remainder
and tries to replace it with one clean positive channel would lose this
evidence.

This whole-period falsifier is now preserved by
`q286_positive_both_empty_compensation_cover_receipt`.  Its default run
recomputes the `204` positive both-empty targets, the `44` negative both-empty
count, and the five-residue greedy positive portfolio above.

`q286_residue_portfolio_local_admissibility_receipt` checks the finite local
obstructions for these portfolios exactly.  The cover pair `133,153` has local
holes at `N == 23 mod 143` and `N == 120 mod 143`, as above.  The broad
positive portfolio

```text
179, 29, 167, 241, 109
```

has at least one locally admissible channel in all `143` target classes modulo
`143`.  Its residues are:

```text
179 == 3 mod 11, 10 mod 13
29  == 7 mod 11, 3 mod 13
167 == 2 mod 11, 11 mod 13
241 == 10 mod 11, 7 mod 13
109 == 10 mod 11, 5 mod 13
```

Status `local-hole-removed-for-portfolio`: the compensating portfolio does not
need a separate local-exception branch.  The remaining obstacle is entirely
arithmetic occupancy/correlation: local admissibility holds, but strict-central
prime-pair weight still has to be forced or compensated quantitatively.

The five-residue observed portfolio is not locally minimal.  Exact set-cover
over the observed portfolio shows that three residues already suffice to remove
all local holes; examples include:

```text
179,29,167
179,29,241
179,29,109
179,167,241
179,167,109
29,167,241
29,167,109
```

Likewise, among the twelve most frequent first-period positive-row residues,
there are many three-residue locally complete subportfolios.  This separates
two notions that should not be conflated: local admissibility can be covered
with three residues, but the measured top-positive contribution cover over the
`204` positive both-empty targets needed five residues.  The hard part is not
local coverage; it is quantitative, signed prime-pair mass in the right rows.

`q286_positive_both_empty_compensation_min_cover_receipt` now verifies that the
five-residue observed cover is not merely a greedy artifact.  For the `204`
first-period positive both-empty targets and `top_count=24`, there are `118`
candidate positive-row residues.  Exact set-cover search gives:

```text
size 1: checked 118, no cover
size 2: checked 6903, no cover
size 3: checked 266916, no cover
size 4: checked 7673835, no cover
size 5: first covers found after 1203567 checked combinations
```

Example size-five covers include:

```text
179,109,29,241,167
179,109,241,49,167
179,109,241,167,219
179,29,111,89,211
179,29,111,89,123
```

Status `observed-cover-minimal`: with this top-row universe, the measured
compensation cover really needs five residues on the first-period positive
both-empty set.  This strengthens the warning that local coverage and observed
signed contribution coverage are different problems.

The broad compensation receipt now retains coefficient sign and weight
direction.  For the five greedy portfolio residues on the `204` positive
both-empty targets:

```text
179: seen 135, negative-coefficient deficits 135, zero weight 131
29:  seen 106, negative-coefficient deficits 106, zero weight 99
167: seen 83,  positive-coefficient surplus 83,  zero weight 0
241: seen 95,  negative-coefficient deficits 95,  zero weight 92
109: seen 124, negative-coefficient deficits 124, zero weight 122
```

Status `direction-pivot`: most observed compensation is not extra occupation
in favorable positive-coefficient channels.  It is absence or deficit in
negative-coefficient channels, with `167` as the one surplus-positive exception
inside the greedy portfolio.  A proof based only on lower bounds for favorable
residue classes misses this sign direction; the compensation theorem would
need either pointwise upper control/avoidance for negative coefficient rows or
a more global signed cancellation argument.

`q286_positive_both_empty_remainder_compensation_receipt` separates the same
`204` positive both-empty targets into first-three q286 modes and everything
else in the full assembled action.  The result is uniform across the set:

```text
tested targets: 204
first-three negative count: 204
first-three positive count: 0
full-without-first-three positive count: 204
first-three/principal range: -1.0569183143768839 .. -0.24090148941651918
full-without-first-three/principal range: 0.5824447187803936 .. 1.7888048047901408
full-action/principal range: 0.004707257667117509 .. 1.3953476720743383
```

Status `remainder-compensation-is-primary`: the positive both-empty targets are
not rescued by making the isolated first-three q286 modes positive.  They are
rescued by the remaining coefficient mixture.  This makes the next serious
proof object the lower envelope of `full_without_first_three`, especially on
targets where the `133/153` cover pair is empty.

## Full-without-first-three lower envelope

The remainder target was then measured directly over the first eight complete
periods using `q286_first_two_mode_lower_tail_receipt(cycle_count=8,
targets_per_cycle=5005)`.  Across `40040` tested targets:

```text
full-action negative count: 89
first-three negative count: 19970
full-without-first-three nonpositive count: 0
reduced-without-first-three nonpositive count: 0
```

The lower envelope is again the known hard target `N=14138`:

```text
full/principal: -0.8769412734408442
first-three/principal: -0.8950145872346785
full-without-first-three/principal: 0.018073313793834367
reduced-without-first-three/principal: 0.018035201222613817
full-minus-reduced/principal: 0.000038112571220549896
```

The residual `full-minus-reduced` term is small on this scan, ranging from
`-0.033888231610242237` at `N=13826` to `0.0337333396277375` at `N=12298`.

Status `lower-envelope-target`: on this measured domain, the entire problem is
concentrated in the first-three q286 lower tail.  The complement
`full_without_first_three` is positive everywhere tested, but with a very small
minimum margin at `N=14138`.  A proof can therefore try to establish a
positive lower envelope for the complement and then bound the first-three
negative tail relative to it; the caveat is that this is still finite evidence,
not an asymptotic theorem.

`q286_first_three_to_complement_ratio_receipt` turns that into the direct
relative inequality target.  For the same `40040` eight-period targets:

```text
full-action negative count: 89
tail/complement ratio > 1: 89
tail/complement ratio > 0.9: 150
tail/complement ratio > 0.5: 1425
maximum tail/complement ratio: 49.52133280284266 at N=14138
```

The top five ratio targets are:

```text
14138: ratio 49.52133280284266, full/principal -0.8769412734408442
16388: ratio 3.98376882600334, full/principal -0.28928582270738745
10424: ratio 3.112065323290175, full/principal -0.6387603808369553
15026: ratio 2.957502749609025, full/principal -0.5504724490146756
17522: ratio 2.9074726562363096, full/principal -0.22113235970668946
```

Status `relative-tail-obstruction`: in the measured domain, proving a uniform
relative bound `-first_three <= theta * full_without_first_three` with
`theta < 1` would exactly rule out these q286 failures.  The worst target is
not hard because the first-three tail is uniquely enormous; it is hard because
the positive complement is tiny.  This points to a local boundary-layer problem
near `N=14138`, not just a global first-three estimate.

`q286_tail_complement_lift_profile_receipt` tests whether the largest ratio
targets remain bad under arithmetic-period lifts.  With default bases
`14138,16388,10424,15026,17522` and lifts `0..7`, it tests `40` lifted
targets.  The ratio is greater than `1` exactly five times, once for each base,
and always at lift `0`:

```text
14138: ratio>1 lifts (0,), max ratio 49.52133280284266
16388: ratio>1 lifts (0,), max ratio 3.98376882600334
10424: ratio>1 lifts (0,), max ratio 3.112065323290175
15026: ratio>1 lifts (0,), max ratio 2.957502749609025
17522: ratio>1 lifts (0,), max ratio 2.9074726562363096
```

Status `persistent-residue-class-falsified`: the top hard targets do not stay
dangerous under nearby period lifts.  This supports an early-cycle scarcity or
boundary-layer explanation rather than a fixed bad residue class.  Any proof
route based on monotonic/lift growth must still be made rigorous, but the
finite evidence says the worst ratios clear immediately after the first lift.

`q286_boundary_layer_clearance_receipt` combines the lift-profile ratio,
`133/153` occupancy, and ordinary AP pair-weight data for the same five hard
bases at lifts `0` and `1`.  Its default run tests `10` targets:

```text
cleared by lift 1: 5/5 bases
lift-1 complement positive: 5/5 bases
lift-1 any 133/153 driver positive: 3/5 bases
lift-1 both 133/153 admissible-empty: 1/5 bases
```

The complement and mean-weight growth from lift `0` to lift `1` are:

```text
14138: complement +1.3595294862243734, mean weight +34.922817965063224
16388: complement +0.631809974687409,  mean weight +31.344820347033945
10424: complement +0.2295180640871176, mean weight +64.73676062630474
15026: complement +0.8356570560198036, mean weight +56.82784425993418
17522: complement +1.0940601855617555, mean weight +59.00260351147824
```

Status `clearance-mechanism-refined`: lift-one clearance is universal for the
top five ratio bases, but `133/153` filling is not.  The common observed
feature is positive complement growth alongside larger strict-central residue
mean weight.  This moves the plausible proof route toward a boundary-layer
lower bound for the complement, not a driver-only hitting theorem.

A broader lift-profile falsifier used the top twenty ratio bases from the
eight-period scan:

```text
14138, 16388, 10424, 15026, 17522, 14852, 12424, 10294, 17042, 10814,
18364, 17702, 12032, 15470, 10564, 17678, 11902, 11614, 10354, 12118
```

For these bases and lifts `0..7`, `160` lifted targets were tested.  The
ratio `-first_three/full_without_first_three` exceeds `1` exactly `20` times,
once for each base, and always at lift `0`.  No tested base has a later
ratio-over-one lift.

Status `boundary-layer-strengthened`: the first-cycle scarcity pattern is not
limited to the top five hard cases.  The next proof-shaped question is whether
one can prove an explicit lift-growth or large-N lower bound for the
full-without-first-three complement in each residue class after the first
boundary layer.

The same lift-clearance test was then applied to all `89` full-action negative
targets from the eight-period scan, treating each negative target as a base and
testing lifts `0..3`.  This covers `356` lifted targets.  The result is exact
on the measured set:

```text
base count: 89
tested lifted targets: 356
ratio > 1 count: 89
ratio > .9 count: 89
bad bases with ratio > 1 outside lift 0: 0
```

Status `observed-failures-clear-immediately`: every observed eight-period
failure clears by lift `1` in this test.  This is stronger than the top-twenty
check, but still finite.  The proof route suggested by the evidence is an
eventual lower-envelope theorem for the complement after the first arithmetic
period lift of any residue class, plus a finite/boundary verification below
that onset.

## Complement cycle envelope

`q286_complement_cycle_envelope_receipt` summarizes the complement lower
envelope by complete arithmetic-period cycles.  Its default run uses the first
eight cycles, `40040` targets:

```text
total full-action negatives: 89
total full-without-first-three nonpositive: 0
global complement minimum: cycle 0, N=14138, 0.018073313793834367
after-first-cycle complement minimum: cycle 2, N=36254, 0.2104242574698779
```

Per-cycle rows:

```text
cycle 0: full negatives 75, complement nonpositive 0, min complement 0.018073313793834367 at 14138
cycle 1: full negatives 3,  complement nonpositive 0, min complement 0.26287606080608905 at 22766
cycle 2: full negatives 5,  complement nonpositive 0, min complement 0.2104242574698779 at 36254
cycle 3: full negatives 4,  complement nonpositive 0, min complement 0.256264703595679 at 49904
cycle 4: full negatives 0,  complement nonpositive 0, min complement 0.31137108785748546 at 51248
cycle 5: full negatives 0,  complement nonpositive 0, min complement 0.39727017945100246 at 66284
cycle 6: full negatives 0,  complement nonpositive 0, min complement 0.4792269914847067 at 71744
cycle 7: full negatives 2,  complement nonpositive 0, min complement 0.4621616810941522 at 89944
```

Status `cycle-envelope-quantified`: the measured complement boundary layer is
cycle `0`; after that, the observed complement floor is more than ten times
larger.  This suggests a proof strategy with two pieces: a finite/boundary
argument for the initial cycle and an eventual complement lower-envelope
estimate for later cycles.  No monotonic theorem is claimed.

The same receipt was run on the next eight-cycle block, starting at `90080`,
corresponding to global cycles `8..15`.  It tested another `40040` targets:

```text
total full-action negatives: 0
total full-without-first-three nonpositive: 0
block complement minimum: local cycle 6, N=154426, 0.37335759682269043
```

Per-cycle complement minima in this later block:

```text
global cycle 8:  0.3919391850281447 at 92896
global cycle 9:  0.3892844567915921 at 109066
global cycle 10: 0.4200084725782136 at 118726
global cycle 11: 0.4091399535574407 at 122996
global cycle 12: 0.4210309762268075 at 131524
global cycle 13: 0.4244575987164013 at 142052
global cycle 14: 0.37335759682269043 at 154426
global cycle 15: 0.38413360717946904 at 164284
```

Status `later-cycle-envelope-strengthened`: the measured post-boundary floor
does not collapse in cycles `8..15`; it rises above the first block's
after-cycle-0 floor.  This is still finite evidence, but it sharpens the
possible theorem shape: complement positivity may have a small finite onset
followed by a stable lower envelope.

The wider pending scan over global cycles `16..31` completed as a further
falsifier.  It used `q286_complement_cycle_envelope_receipt(start=170160,
cycle_count=16, targets_per_cycle=5005)`, testing `80080` targets:

```text
total full-action negatives: 0
total full-without-first-three nonpositive: 0
block complement minimum: global cycle 19, N=205514, 0.42968514453254214
```

Per-cycle complement minima in this wider block:

```text
global cycle 16: 0.4649897326875926 at 179404
global cycle 17: 0.4664904581773077 at 189764
global cycle 18: 0.4889894819098438 at 199774
global cycle 19: 0.42968514453254214 at 205514
global cycle 20: 0.5427355349523361 at 219724
global cycle 21: 0.5010043408493222 at 225254
global cycle 22: 0.5108243580654256 at 231344
global cycle 23: 0.49031061617966964 at 246464
global cycle 24: 0.4878545916998052 at 254374
global cycle 25: 0.5061461832940138 at 270124
global cycle 26: 0.4463683887804602 at 274966
global cycle 27: 0.504971943945799 at 281674
global cycle 28: 0.4997990373400434 at 292664
global cycle 29: 0.4573748899036469 at 307096
global cycle 30: 0.5343912322442239 at 315624
global cycle 31: 0.5163376893087155 at 326206
```

Status `wider-envelope-strengthened`: the complement floor in cycles `16..31`
stays above the cycles `8..15` floor and far above the cycle-0 boundary
minimum.  The observed post-boundary floor is now monotone by tested block
minimum across blocks `1..7`, `8..15`, and `16..31`, but no monotonic theorem
has been proved.

A coarser later-horizon falsifier sampled global cycles `32..47` with
`targets_per_cycle=501`, starting at `330320`.  It tested `8016` targets:

```text
total full-action negatives: 0
total full-without-first-three nonpositive: 0
sampled block complement minimum: global cycle 43, N=440866, 0.49906371578900943
```

The sampled per-cycle complement minima were:

```text
global cycle 32: 0.6042973622004102 at 330966
global cycle 33: 0.587380111321078 at 340486
global cycle 34: 0.5938253288828608 at 350624
global cycle 35: 0.5981462465001088 at 360786
global cycle 36: 0.5509255816224139 at 370796
global cycle 37: 0.5886469400329274 at 380444
global cycle 38: 0.5819616227738739 at 391306
global cycle 39: 0.6256438335597275 at 401374
global cycle 40: 0.587309690118216 at 411046
global cycle 41: 0.5826448055567107 at 421336
global cycle 42: 0.5751621229298687 at 430576
global cycle 43: 0.49906371578900943 at 440866
global cycle 44: 0.5565874811655189 at 450876
global cycle 45: 0.534662460823786 at 460606
global cycle 46: 0.5709637618961914 at 471106
global cycle 47: 0.5708157549176014 at 480906
```

Status `coarse-later-horizon-strengthened`: no collapse appears in this
sampled later block; the sampled complement floor continues upward.  The word
sampled matters: this is not a complete-cycle check and cannot replace the
full-period envelope receipts.

## Boundary target inventory

The hardest complement target in the measured first block, `N=14138`, is not
scarce in ordinary strict-central Goldbach representations.  Direct inventory
over `N/3 < p < 2N/3` gives:

```text
strict-central interval: 4713..9425
ordered strict-central prime pairs: 75
total log-pair weight: 5862.85778490767
mean over 99 admissible q286 residue classes: 59.22078570613808
weight in residue 133: 0
weight in residue 153: 0
largest residue weights:
  205: 235.39078971716816
  125: 233.7296237950301
  285: 233.72962379503008
  159: 157.03530703722484
  251: 157.03530703722484
```

Status `residue-specific-scarcity`: the boundary obstruction is not lack of
Goldbach pairs in the strict-central interval.  It is signed residue placement:
the cover pair is empty, while the occupied residues do not give enough
positive complement to absorb the first-three q286 tail.  This supports a
residue-distribution proof target rather than a raw pair-count target.

The first-three residue anatomy at `N=14138` makes the sign direction explicit:

```text
first-three/principal: -0.8950145872346784
positive first-three row sum/principal: 0.5383359639042713
negative first-three row sum/principal: -1.4333505511389497
signed/absolute contribution ratio: -0.45393351346984234
top-absolute row fraction: 0.6971100214766663
maximum relative residue deviation: 2.974800180551649
rms relative residue deviation: 0.9941766583984686
```

Largest negative first-three rows:

```text
133: coeff +1404595.8164, weight 0,      contribution -0.3224324185890418
153: coeff +1404595.8164, weight 0,      contribution -0.3224324185890399
23:  coeff -299046.4120,  weight 156.78, contribution -0.1130889762466301
285: coeff -133083.6238,  weight 233.73, contribution -0.09002335832662271
159: coeff -226811.5922,  weight 157.04, contribution -0.08599669218564053
205: coeff -105808.8708,  weight 235.39, contribution -0.07225488414275169
29:  coeff -162737.3264,  weight 155.85, contribution -0.06095547110471638
```

Largest positive first-three rows:

```text
211: coeff -226290.1103, weight 0, contribution 0.051946094893403655
243: coeff -163375.4802, weight 0, contribution 0.03750370790634848
43:  coeff -163375.4802, weight 0, contribution 0.03750370790634512
257: coeff -162737.3264, weight 0, contribution 0.03735721630866466
45:  coeff -133875.9469, weight 0, contribution 0.030731933587607903
237: coeff -118858.7410, weight 0, contribution 0.02728465434219034
```

Status `boundary-anatomy`: the hardest target is a signed residue-placement
imbalance, not a raw absence of pairs.  The leading damage is empty
positive-coefficient cover rows, while leading compensation is mostly empty
negative-coefficient rows.  This reinforces that the missing theorem must be
signed and coefficient-sensitive.

`q286_boundary_component_split_receipt` compares the boundary target `14138`
with its first period lift `24148`:

```text
N=14138
  full/principal: -0.8769412734408442
  reduced model/principal: -0.8769793860120647
  q286 deviation/principal: -0.8666741397111133
  first-three/principal: -0.8950145872346785
  q286 after first three/principal: 0.028340447523565238
  full without first three/principal: 0.018073313793834367
  reduced without first three/principal: 0.018035201222613817
  full minus reduced/principal: 0.000038112571220549896

N=24148
  full/principal: 1.2567753658081395
  reduced model/principal: 1.2400949523363975
  q286 deviation/principal: -0.12126698742344302
  first-three/principal: -0.12082743421006822
  q286 after first three/principal: -0.00043955321337479925
  full without first three/principal: 1.3776028000182077
  reduced without first three/principal: 1.3609223865464657
  full minus reduced/principal: 0.016680413471741984
```

Status `complement-source-refined`: the lift-one clearance is not primarily
q286-after-first-three becoming positive.  At `24148`, q286 after the first
three modes is essentially zero/slightly negative, while the complement is
large.  The compensating lower envelope therefore lives mostly outside the
first-three q286 tail and its immediate q286 residual.

## 2026-09-12: boundary complement support split

`q286_boundary_complement_support_split_receipt` decomposes the boundary
complement `full - first_three_q286` into principal plus lower-modulus CRT
support components.  It compares the hardest measured boundary target
`14138` with its first arithmetic-period lift `24148`.

Measured principal-relative split:

```text
N=14138
  full without first three: 0.018073313793834367
  q286 actual support: -0.862126212281399
  q70 support: -0.6530100068358881
  q154 support: -0.43137904901734725
  smaller supports together: 0.06957399469379079
  non-q286 support sum: -1.0148150611594444
  q286 actual after first three: 0.032888374953279564
  q286 deviation after first three: 0.028340447523565238

N=24148
  full without first three: 1.3776028000182077
  q286 actual support: -0.11671905999372909
  q70 support: 0.35469923238633455
  q154 support: -0.06691780878077785
  smaller supports together: 0.08571300219631225
  non-q286 support sum: 0.373494425801869
  q286 actual after first three: 0.004108374216339139
  q286 deviation after first three: -0.00043955321337479925
```

Reconstruction errors for `full - first_three_q286` are below `7e-16` in the
ratio arithmetic.  Focused regression
`test_q286_boundary_complement_support_split` passed in `153.125s`; bytecode-
disabled `py_compile` also passed.

Status `aha-candidate`: lift-one clearance is not q286 residual positivity.
At `24148`, q286 after the first three modes is essentially zero/slightly
negative, while the complement is large.  The visible driver is the positive
principal channel reinforced by a positive `(5,7)`/mod-70 support and smaller
positive supports.  The boundary target `14138` is tiny because principal is
almost exactly cancelled by negative q70, q154, and non-first-three q286
support.  The next direct estimate should therefore treat q286 first-three as
the main negative tail, but the lower envelope after removing it must use joint
q70/q154/q286 support control, not q286 alone.

## 2026-09-12: first-three-removed support envelope scan

`q286_first_three_removed_support_envelope_receipt` scans the assembled action
after removing only the first three q286 separable modes.  It keeps principal,
q286-after-first-three, q70, q154, and smaller support terms explicit, so the
post-first-three lower-envelope target can be tested without hiding the
support mixture inside one error term.

Four-window sample, matching the earlier reduced-envelope scan
(`cycle_count=4`, `targets_per_cycle=501`, `2004` targets):

```text
minimum complement: 0.17754016683566773 at N=10354, cycle 0
nonpositive complement count: 0
minimum without q70: -0.011932443115723584 at N=10814
nonpositive without q70 count: 1
maximum reconstruction error: 4.440892098500626e-16
cycle minima: 0.17754016683566773, 0.29137600918050843,
  0.41005118614375335, 0.27718627994335954
```

Complete first-period scan (`5005` targets):

```text
minimum complement: 0.018073313793834256 at N=14138
nonpositive complement count: 0
minimum without q70: -0.011932443115723584 at N=10814
nonpositive without q70 count: 1
maximum reconstruction error: 6.661338147750939e-16
```

Selected component rows from the full first period:

```text
N=10814
  complement: 0.17818268929554124
  without q70: -0.011932443115723584
  q70: 0.19011513241126482
  q154: -0.7887852463184296
  q286 after first three: -0.096403079307679
  small supports: -0.1267441174896149

N=14138
  complement: 0.018073313793834256
  without q70: 0.6710833206297226
  q70: -0.6530100068358884
  q154: -0.4313790490173474
  q286 after first three: 0.03288837495327912
  small supports: 0.06957399469379084

N=14732
  complement: 0.06913849299419508
  without q70: 0.9431698876158701
  q70: -0.874031394621675
  q154: 0.010783876363777105
  q286 after first three: -0.0696142958377479
  small supports: 0.002000307089840918
```

Status `changed-under-evidence`: q70 is structurally necessary in the support
envelope, but not because it has a fixed favorable sign.  It rescues `10814`
while hurting `14138` and `14732`.  The theorem target must be a joint signed
lower-envelope inequality for principal plus q70/q154/q286-after-first-three
and smaller supports.  A one-support positivity lemma is now falsified as a
complete explanation.

## 2026-09-12: first-period support Gram after first-three removal

A first-period normalized Gram/correlation check was run on the component
vectors from `q286_first_three_removed_support_envelope_receipt` over all
`5005` targets.  Components were measured in principal-relative units.

Basic statistics:

```text
q286_after_first3 mean  0.010650365091959399 min -0.20627076849182013 max 0.4689649942154356 rms 0.06070748215359575
q70              mean -0.033461102392216995 min -0.874031394621675   max 0.7114998115797481 rms 0.18650862719915784
q154             mean -0.024596827574109935 min -0.7887852463184296  max 0.7711813776303265 rms 0.17751405988614322
small supports   mean -0.002191411746741188 min -0.17485448534823922 max 0.1743775542593439 rms 0.06046506124504247
non_q286         mean -0.060249341713068116 min -1.0148150611594449  max 0.9893238099904496 rms 0.274285742847285
complement       mean  0.9504010233788912   min 0.018073313793834256 max 2.055236408924841 rms 0.9887972490595348
```

Centered correlations, in the order
`q286_after_first3, q70, q154, small, non_q286, complement`:

```text
q286_after_first3  1.000000  0.026703 -0.057913 -0.011828 -0.022409  0.197052
q70                0.026703  1.000000  0.045469 -0.033593  0.707980  0.700122
q154              -0.057913  0.045469  1.000000  0.056056  0.700826  0.674573
small             -0.011828 -0.033593  0.056056  1.000000  0.239610  0.232380
non_q286          -0.022409  0.707980  0.700826  0.239610  1.000000  0.975731
complement         0.197052  0.700122  0.674573  0.232380  0.975731  1.000000
```

Raw cosines with the complement are small for q70/q154/non-q286 because the
complement contains the large constant principal term.  The centered Gram is
the relevant diagnostic for moving cancellation.  In that centered view, q70
and q154 are almost orthogonal to each other (`0.045469`), but each strongly
feeds the moving non-q286 envelope (`0.707980` and `0.700826`), and non-q286
almost completely tracks complement motion (`0.975731`).

Status `changed-under-evidence`: the lower-envelope problem is not explained
by pairwise q70/q154 cancellation; those two supports are nearly orthogonal as
moving centered vectors.  The complement floor comes from a principal constant
plus a broad non-q286 support vector whose motion is mostly the combined q70
and q154 directions.  The theorem target should use a vector/norm envelope for
the combined lower-modulus support action, not scalar sign control of any one
support.

## 2026-09-12: support Gram receipt codified

`q286_first_three_removed_support_gram_receipt` now makes the post-first-three
support Gram diagnostic executable.  It calls
`q286_first_three_removed_support_envelope_receipt`, builds component vectors
for `q286_after_first_three`, `q70`, `q154`, `small_supports`, `non_q286`, and
`complement`, then records component statistics, centered correlations, and raw
cosines.  This replaces the prior scratch Gram calculation with a reusable
receipt and regression.

Full first-period receipt (`cycle_count=1`, `targets_per_cycle=5005`):

```text
tested targets: 5005
minimum complement: 0.018073313793834256 at N=14138
nonpositive complement count: 0
q70/q154 centered correlation: 0.045468960787398205
non_q286/complement centered correlation: 0.9757310575760174
q70 and q154 nearly orthogonal on sample: True
non_q286 tracks complement motion on sample: True
```

Component stats, principal-relative:

```text
q286_after_first_three mean 0.010650365091959399 min -0.20627076849182013 max 0.4689649942154356 rms 0.06070748215359575 centered_rms 0.059765944423535375
q70 mean -0.033461102392216995 min -0.874031394621675 max 0.7114998115797481 rms 0.18650862719915784 centered_rms 0.18348248593915445
q154 mean -0.024596827574109935 min -0.7887852463184296 max 0.7711813776303265 rms 0.17751405988614322 centered_rms 0.1758016994529653
small_supports mean -0.002191411746741188 min -0.17485448534823922 max 0.1743775542593439 rms 0.06046506124504247 centered_rms 0.06042533695332598
non_q286 mean -0.060249341713068116 min -1.0148150611594449 max 0.9893238099904496 rms 0.274285742847285 centered_rms 0.2675867813484607
complement mean 0.9504010233788912 min 0.018073313793834256 max 2.055236408924841 rms 0.9887972490595348 centered_rms 0.2728697390845307
```

Validation: bytecode-disabled `py_compile` passed.  Focused regression
`test_q286_first_three_removed_support_gram` passed in `62.264s`.

Status `changed-under-evidence`: the near-orthogonality and non-q286 tracking
claims are now executable receipt fields.  The next analytic formulation can
refer to the exact vector components and their measured Gram data, while still
keeping the no-overclaim flags: no eventual vector-envelope theorem, no signed
prime-correlation estimate, and no Goldbach proof.

## 2026-09-12: vector-stress receipt falsifies norm-only certificate

`q286_first_three_removed_vector_stress_receipt` now stress-tests whether the
post-first-three support envelope can be certified by component norms alone.
It writes the complement as

```text
1 + q286_after_first_three + q70 + q154 + small_supports
```

in principal-relative units, then records covariance, cross terms, finite box
and Cauchy-style lower bounds, and the pointwise alignment of the component
vector with the all-ones summation direction.

Full first-period run (`5005` targets):

```text
minimum complement: 0.018073313793834145 at N=14138
nonpositive complement count: 0
mean complement: 0.9504010233788913
component box lower bound: -1.043941894780164
rms-only lower bound: -18.352119644096938
finite max-norm lower bound: -0.7399426654787107
maximum centered vector norm: 0.845171844428801 at N=11096
```

Variance decomposition for the four moving support components:

```text
diagonal variance sum: 0.07179524963572285
cross-term total: 0.002662644872337
normalized cross-term total: 0.0370866441142947
support-sum variance: 0.07445789450805985
```

Thus the aggregate cross terms are slightly positive, not substantially
negative.  The measured positivity is not certified by global pairwise
cancellation or by a norm-only inequality.

Worst and near-worst rows:

```text
N=14138
  complement: 0.018073313793834145
  centered vector norm: 0.7449546451454716
  centered support sum: -0.9323277095850572
  sum-direction cosine: -0.6257613907508397
  vector: (0.03288837495327912, -0.6530100068358884,
           -0.4313790490173474, 0.06957399469379084)

N=10814
  complement: 0.17818268929554137
  centered vector norm: 0.812984679177623
  centered support sum: -0.7722183340833499
  sum-direction cosine: -0.47492797457418856
  vector: (-0.096403079307679, 0.19011513241126482,
           -0.7887852463184296, -0.1267441174896149)

N=14732
  complement: 0.06913849299419517
  centered vector norm: 0.8451450743457142
  centered support sum: -0.8812625303846962
  sum-direction cosine: -0.5213676072518928
  vector: (-0.0696142958377479, -0.874031394621675,
           0.010783876363777105, 0.002000307089840918)
```

Validation: bytecode-disabled `py_compile` passed.  Focused regression
`test_q286_first_three_removed_vector_stress` passed in `64.418s`.

Status `changed-under-evidence`: reject a pure norm-only proof of the measured
post-first-three lower envelope.  The next theorem target must control
pointwise alignment of the lower-modulus support vector with the summation
direction, or use arithmetic structure stronger than aggregate Gram/covariance
cancellation.

## 2026-09-12: low-tail inventory for pointwise alignment

A low-tail inventory was computed from
`q286_first_three_removed_vector_stress_receipt(cycle_count=1,
targets_per_cycle=5005)`.  This uses the executable vector-stress receipt and
sorts the first-period targets by the post-first-three complement.

Threshold counts:

```text
complement < 0.02: 1
complement < 0.05: 1
complement < 0.10: 5
complement < 0.15: 7
complement < 0.20: 16
complement < 0.25: 29
complement < 0.30: 50
```

Bottom five component vectors, in the order
`q286_after_first_three, q70, q154, small_supports`:

```text
N=14138 complement 0.018073313793834145 signs +--+
  vector (0.03288837495327912, -0.6530100068358884,
          -0.4313790490173474, 0.06957399469379084)
  centered norm 0.7449546451454716, sum-direction cosine -0.6257613907508397

N=14732 complement 0.06913849299419517 signs --++
  vector (-0.0696142958377479, -0.874031394621675,
          0.010783876363777105, 0.002000307089840918)
  centered norm 0.8451450743457142, sum-direction cosine -0.5213676072518928

N=12578 complement 0.07154179749160794 signs +--+
  vector (0.050498156312654, -0.41458610566581544,
          -0.5783571695768337, 0.013986916421603032)
  centered norm 0.6736144069590293, sum-direction cosine -0.652345924321017

N=12944 complement 0.08894502770264667 signs +---
  vector (0.01618618544956041, -0.2219973488172028,
          -0.6075006647372669, -0.09774314419244402)
  centered norm 0.6200673983334086, sum-direction cosine -0.6946470641672423

N=16388 complement 0.09695316211707872 signs ----
  vector (-0.0074806666605387595, -0.1546306060642018,
          -0.7113359155341294, -0.029599649624051275)
  centered norm 0.6981207412534195, sum-direction cosine -0.6112466016476718
```

Status `aha-candidate`: the post-first-three lower floor is thin but not a
single residue accident.  The bottom cases are mostly simultaneous negative
alignment of q70 and q154, with q286-after-first-three comparatively small and
sometimes positive.  A pointwise theorem could try to prove that such aligned
lower-modulus deficits cannot exceed the principal buffer after the first
three q286 modes are removed.  The measured data does not supply that theorem.

## 2026-09-12: low-tail period lifts clear by lift one

`q286_first_three_removed_low_tail_lift_receipt` follows the bottom
post-first-three complement targets through arithmetic-period lifts.  The
default bases are the first-period bottom five `14138, 14732, 12578, 12944,
16388`; lifts are `0, 1, 4, 9, 19, 49`; threshold is `.3`.

Default run (`30` lifted targets):

```text
global minimum: base 14138, lift 0, target 14138, complement 0.018073313793834145
targets below .3: 5
all tested lifts positive: True
every base clears .3 on tested lifts: True
```

Every base has its minimum at lift `0`, and every base first clears the `.3`
threshold at lift `1`:

```text
base 14138: min 0.018073313793834145 at lift 0; lift 1 complement 1.377602800018208
base 14732: min 0.06913849299419517 at lift 0; lift 1 complement 1.3857462229590352
base 12578: min 0.07154179749160794 at lift 0; lift 1 complement 1.056148898018834
base 12944: min 0.08894502770264667 at lift 0; lift 1 complement 0.6470013535948573
base 16388: min 0.09695316211707872 at lift 0; lift 1 complement 0.7287631368044876
```

Later sampled lifts stay positive but not monotone; e.g. base `12944` has
complements `.6470, .9492, .7679, .5835, .6765` at lifts `1,4,9,19,49`.
Thus the clearing evidence is not monotone decay of component oscillation.

Validation: bytecode-disabled `py_compile` passed.  Focused regression
`test_q286_first_three_removed_low_tail_lift` passed in `68.207s`.

Status `aha-candidate`: the worst first-period pointwise alignments are not
persistent in these same-residue period lifts.  The useful theorem target may
be a finite/onset boundary treatment plus an eventual alignment-clearance
estimate, but the sampled lift profile does not prove either one.

## 2026-09-12: all first-period `.3` low-tail bases clear by lift one

`q286_first_three_removed_low_tail_auto_lift_receipt` now selects every base
in a finite window whose post-first-three complement is below a threshold and
runs the period-lift profile on all selected bases.  It widens the previous
named-bottom-five falsifier to an automatically selected low-tail set.

Default widened experiment with `low_threshold=.3` and lifts `0,1,2,3`:

```text
base window: 10000..20008, 5005 even targets
selected base count below .3: 50
tested lifted targets: 200
base minimum: 0.018073313793834145 at N=14138
global lifted minimum: 0.018073313793834145 at N=14138
unique first-clear lifts: [1]
maximum first-clear lift: 1
below-threshold counts by lift: {0: 50, 1: 0, 2: 0, 3: 0}
all selected lifts positive: True
```

The selected bases begin
`10084, 10112, 10214, 10294, 10354, 10564, 10774, 10814, 11194, 11432`
and end
`16388, 16448, 16638, 16946, 17042, 17074, 17102, 17126, 17522, 18684`.

Status `aha-candidate`: the first-period post-first-three low tail below `.3`
is not persistent under the first three same-residue period lifts.  Every
selected low-tail base clears the `.3` threshold at lift `1`.  This strengthens
the boundary/onset split as a finite phenomenon, but still does not prove an
eventual alignment-clearance theorem or Goldbach.

## 2026-09-12: four-period `.3` low-tail lift recurrence check

A cross-period run of `q286_first_three_removed_low_tail_auto_lift_receipt`
checked complete base periods starting at `10000`, `20010`, `30020`, and
`40030`, selecting all bases with post-first-three complement below `.3` and
testing lifts `0,1`.

```text
start 10000: selected 50, base minimum 0.018073313793834145 at 14138,
  below-threshold counts {0: 50, 1: 0}, max first-clear lift 1
start 20010: selected 4, base minimum 0.26287606080608905 at 22766,
  below-threshold counts {0: 4, 1: 0}, max first-clear lift 1
start 30020: selected 4, base minimum 0.21042425746987792 at 36254,
  below-threshold counts {0: 4, 1: 0}, max first-clear lift 1
start 40030: selected 6, base minimum 0.2562647035956789 at 49904,
  below-threshold counts {0: 6, 1: 0}, max first-clear lift 1
```

All selected bases in all four periods clear the `.3` threshold at lift `1`.
The low-tail population is much larger in the first period (`50`) than in the
next three complete periods (`4,4,6`).  This supports an onset/boundary-layer
interpretation for the post-first-three complement floor while still leaving
the required eventual alignment-clearance theorem open.

Status `aha-candidate`: the same-residue low-tail obstruction has not persisted
in any checked complete period.  The next efficient step should avoid repeated
one-period wrappers and codify a multi-period low-tail scanner if wider ranges
are needed.

## 2026-09-12: multi-period low-tail lift receipt

`q286_first_three_removed_low_tail_multi_period_receipt` now scans multiple
base periods in one support-vector stress receipt, selects every base below a
post-first-three complement threshold, and tests all selected bases through
period lifts in one lift receipt.  This replaces the slow repeated one-period
wrapper used for the first recurrence check.

Four-period run (`cycle_count=4`, `targets_per_cycle=5005`, `low_threshold=.3`,
`lifts=(0,1)`):

```text
base-scan tested targets: 20020
selected low-tail bases: 64
selected counts by cycle: {0: 50, 1: 4, 2: 4, 3: 6}
tested lifted targets: 128
base minimum: 0.018073313793834145 at N=14138
global lifted minimum: 0.018073313793834145 at N=14138
below-threshold counts by lift: {0: 64, 1: 0}
maximum first-clear lift: 1
all selected bases clear threshold: True
all selected lift targets positive: True
```

Cycle minima:

```text
cycle 0: N=14138, complement 0.018073313793834145, selected 50
cycle 1: N=22766, complement 0.26287606080608905, selected 4
cycle 2: N=36254, complement 0.21042425746987792, selected 4
cycle 3: N=49904, complement 0.2562647035956789, selected 6
```

Validation: bytecode-disabled `py_compile` passed.  The first attempt at the
focused regression caught an integration bug (`vector_stress` has no
`cycle_rows` field); the receipt now computes cycle minima directly from
`target_rows`.  Corrected focused regression
`test_q286_first_three_removed_low_tail_multi_period` passed in `122.320s`.

Status `aha-candidate`: the four-period same-residue recurrence check is now
executable and reproduces the low-tail clearance pattern.  All selected `.3`
low-tail bases clear at lift `1` in the checked window.  This still does not
prove the eventual lift-clearance theorem or Goldbach.

## 2026-09-12: eight-period `.3` low-tail recurrence check

`q286_first_three_removed_low_tail_multi_period_receipt` was run over the
first eight complete periods with `targets_per_cycle=5005`, `low_threshold=.3`,
and lifts `0,1`.

```text
base-scan tested targets: 40040
selected low-tail bases: 64
selected counts by cycle: {0: 50, 1: 4, 2: 4, 3: 6, 4: 0, 5: 0, 6: 0, 7: 0}
tested lifted targets: 128
base minimum: 0.018073313793834145 at N=14138
global lifted minimum: 0.018073313793834145 at N=14138
below-threshold counts by lift: {0: 64, 1: 0}
maximum first-clear lift: 1
all selected bases clear threshold: True
all selected lift targets positive: True
```

Cycle minima:

```text
cycle 0: N=14138, complement 0.018073313793834145, selected 50
cycle 1: N=22766, complement 0.26287606080608905, selected 4
cycle 2: N=36254, complement 0.21042425746987792, selected 4
cycle 3: N=49904, complement 0.2562647035956789, selected 6
cycle 4: N=51248, complement 0.31137108785748546, selected 0
cycle 5: N=66284, complement 0.3972701794510025, selected 0
cycle 6: N=71744, complement 0.4792269914847066, selected 0
cycle 7: N=89944, complement 0.46216168109415223, selected 0
```

Status `aha-candidate`: the `.3` post-first-three low tail is confined to the
first four complete periods in the checked eight-period window, and every
selected same-residue base clears at lift `1`.  This strengthens the finite
boundary/onset interpretation.  It does not prove an eventual clearance theorem
or Goldbach.

## 2026-09-12: complement threshold-horizon receipt

`q286_first_three_removed_complement_threshold_horizon_receipt` now summarizes
cycle minima of the post-first-three complement against fixed thresholds.  It
uses `q286_complement_cycle_envelope_receipt` and records threshold rows with
cycles below threshold, last cycle below threshold, and the first cycle at or
above threshold in the checked window.

The focused regression initially caught two schema assumptions: complement
cycle rows do not expose `start`/`end`, and the envelope receipt does not expose
`arithmetic_period`.  The horizon receipt now computes cycle ranges from the
known period `10010` and actual `target_count`.

Eight-period run (`cycle_count=8`, `targets_per_cycle=5005`, thresholds
`.3,.4,.5`):

```text
tested targets: 40040
global minimum: cycle 0, N=14138, 0.018073313793834367
after-first-cycle minimum: cycle 2, N=36254, 0.2104242574698779
total full-action negatives: 89
total complement nonpositive: 0

threshold .3: cycles (0,1,2,3), targets (14138,22766,36254,49904),
  last cycle below 3, first cycle at/above 4
threshold .4: cycles (0,1,2,3,4,5), targets (14138,22766,36254,49904,51248,66284),
  last cycle below 5, first cycle at/above 6
threshold .5: cycles (0,1,2,3,4,5,6,7), targets (14138,22766,36254,49904,51248,66284,71744,89944),
  no checked cycle at/above .5
```

Cycle minima:

```text
0: N=14138, 0.018073313793834367
1: N=22766, 0.26287606080608905
2: N=36254, 0.2104242574698779
3: N=49904, 0.256264703595679
4: N=51248, 0.31137108785748546
5: N=66284, 0.39727017945100246
6: N=71744, 0.4792269914847067
7: N=89944, 0.4621616810941522
```

Validation: bytecode-disabled `py_compile` passed.  Corrected focused
regression
`test_q286_first_three_removed_complement_threshold_horizon` passed in
`63.488s`.

Status `changed-under-evidence`: the executable horizon says `.3` is an early
threshold in the first eight periods, clearing at cycle `4`; `.4` clears at
cycle `6`; `.5` does not clear in the checked window.  This gives a sharper
finite onset target for any eventual complement-floor theorem.

## 2026-09-12: later-block threshold horizon falsifies monotone `.4` clearance

The threshold-horizon receipt was run on the later complete-period block
starting at `90080`, with `cycle_count=8`, `targets_per_cycle=5005`, and
thresholds `.4,.45,.5`.  These local cycle indices correspond to global cycles
`8..15`.

```text
tested targets: 40040
global minimum in this block: local cycle 6, N=154426, 0.37335759682269043
total full-action negatives: 0
total complement nonpositive: 0

threshold .4: local cycles (0,1,6,7), targets (92896,109066,154426,164284),
  last local cycle below 7, first local cycle at/above 2
threshold .45: all local cycles (0..7) below
threshold .5: all local cycles (0..7) below
```

Cycle minima:

```text
local 0/global 8:  N=92896,  0.3919391850281447
local 1/global 9:  N=109066, 0.3892844567915921
local 2/global 10: N=118726, 0.4200084725782136
local 3/global 11: N=122996, 0.4091399535574407
local 4/global 12: N=131524, 0.4210309762268075
local 5/global 13: N=142052, 0.4244575987164013
local 6/global 14: N=154426, 0.37335759682269043
local 7/global 15: N=164284, 0.38413360717946904
```

Status `changed-under-evidence`: preserve `.3` as the robust checked horizon
threshold after global cycle `3`, but reject a monotone or permanent `.4`
clearance inference from the first eight periods.  The later block has no
full-action negatives and no complement nonpositive cases, yet `.4` low-tail
cycle minima recur.  Any eventual complement-floor theorem needs a threshold
small enough to survive recurrence, or a proof that the recurring floor still
stays above the required margin.

## 2026-09-12: first-three tail threshold horizon

`q286_first_three_tail_threshold_horizon_receipt` now measures where the first
three q286 separable modes fall below negative thresholds.  This is the direct
counterpart to the complement threshold horizon: if the complement floor is
only about `.3`, then a separate uniform bound `first_three >= -.3` would be
needed to prove positivity by independent envelopes.

Eight-period run (`cycle_count=8`, `targets_per_cycle=5005`, thresholds
`.3,.5,.75,1.0`):

```text
tested targets: 40040
global minimum first-three: cycle 0, N=10664, -1.1500880008976306
full-action negatives: 89
post-first-three complement nonpositive: 0

threshold .3: 4406 targets, hits in all 8 cycles
threshold .5: 1143 targets, hits in all 8 cycles
threshold .75: 173 targets, hits in 7 cycles (all except cycle 5)
threshold 1.0: 5 targets, hits in cycles 0 and 1
```

Cycle minima and threshold counts:

```text
cycle 0: min N=10664, -1.1500880008976306, counts {.3:972, .5:358, .75:95, 1.0:4}, full negatives 75
cycle 1: min N=29152, -1.0394802094365456, counts {.3:824, .5:240, .75:26, 1.0:1}, full negatives 3
cycle 2: min N=30298, -0.9219319460533107, counts {.3:867, .5:285, .75:35, 1.0:0}, full negatives 5
cycle 3: min N=45184, -0.9252620391138453, counts {.3:426, .5:81, .75:11, 1.0:0}, full negatives 4
cycle 4: min N=52672, -0.7971692976412812, counts {.3:283, .5:37, .75:3, 1.0:0}, full negatives 0
cycle 5: min N=69116, -0.7320730201760477, counts {.3:425, .5:63, .75:0, 1.0:0}, full negatives 0
cycle 6: min N=70526, -0.7650482510196677, counts {.3:330, .5:47, .75:2, 1.0:0}, full negatives 0
cycle 7: min N=88346, -0.796958962112027, counts {.3:279, .5:32, .75:1, 1.0:0}, full negatives 2
```

Validation: bytecode-disabled `py_compile` passed.  Focused regression
`test_q286_first_three_tail_threshold_horizon` passed in `68.352s`.

Status `changed-under-evidence`: reject independent-envelope closure using a
`.3` complement floor plus a separate `first_three >= -.3` theorem.  The
first-three tail exceeds `.3` in every checked cycle and exceeds `.5` in every
checked cycle.  Since the post-first-three complement is always positive, the
remaining theorem must control pointwise co-occurrence: when first-three is
very negative, the complement must be correspondingly large, except for the
finite full-action negative boundary cases still needing treatment.

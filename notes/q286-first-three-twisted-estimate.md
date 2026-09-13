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

## 2026-09-12: first-three/complement co-occurrence receipt

`q286_first_three_complement_cooccurrence_receipt` now measures the actual
pointwise recombination

```text
full action = first_three_q286 + post_first_three_complement
```

and bins targets by negative first-three tail size.  It records rescue counts,
negative full-action counts inside each tail, and centered correlations among
first-three, complement, and recombined full action.

Eight-period run (`cycle_count=8`, `targets_per_cycle=5005`, thresholds
`.3,.5,.75,1.0`):

```text
tested targets: 40040
full-action negatives: 89
minimum full action: N=14138, -0.8769412734408442
minimum first-three: N=10664, -1.1500880008976306
minimum complement: N=14138, 0.018073313793834367
first_three/complement centered correlation: -0.04967965232137842
first_three/full centered correlation: 0.7605574171870063
complement/full centered correlation: 0.6106847343442704
```

Negative-tail bins:

```text
first_three < -.3:
  tail targets 4406, rescued 4320, full negatives 86,
  rescue fraction 0.9804811620517476,
  mean complement 1.021029437934667,
  mean recombined 0.5747406357928522

first_three < -.5:
  tail targets 1143, rescued 1071, full negatives 72,
  rescue fraction 0.937007874015748,
  mean complement 1.0438518320203745,
  mean recombined 0.41343657154653096

first_three < -.75:
  tail targets 173, rescued 137, full negatives 36,
  rescue fraction 0.791907514450867,
  mean complement 1.0381299356023956,
  mean recombined 0.2096477602472142

first_three < -1.0:
  tail targets 5, rescued 3, full negatives 2,
  rescue fraction 0.6,
  mean complement 1.0534609578401883,
  mean recombined -0.004269413900421726
```

Status `changed-under-evidence`: the co-occurrence theorem target is sharper
but harder.  Most large negative first-three tails are rescued by complement,
but the centered first_three/complement correlation is near zero, so there is
no simple linear compensation law.  The exact full negatives are concentrated
inside the negative first-three tail bins: `86/89` full negatives lie below
`-.3`, `72/89` below `-.5`, and `36/89` below `-.75`.  The remaining proof
must distinguish the rescued majority from the finite/structured non-rescued
minority.

## 2026-09-12: non-rescued first-three tail classification

`q286_nonrescued_first_three_tail_classification_receipt` now classifies the
targets where the first-three q286 mode sum is below `-.3` and the recombined
full action is still nonpositive.  It builds on the first-three/complement
co-occurrence receipt, then records cycle counts, residues modulo the q286
arithmetic period, severity bins, the worst non-rescued targets, and selected
same-residue period lifts.

Eight-period run (`cycle_count=8`, `targets_per_cycle=5005`, threshold `.3`,
lift offsets `0,1`):

```text
tested targets: 40040
tail targets: 4406
rescued tail targets: 4320
non-rescued tail targets: 86
rescue fraction: 0.9804811620517476

cycle counts: {0: 72, 1: 3, 2: 5, 3: 4, 4: 0, 5: 0, 6: 0, 7: 2}
severity counts: {'below_.5': 72, 'below_.75': 36, 'below_1.0': 2}
residue count: 86
residues with multiple hits: ()
max hits per residue: 1

worst 10 targets:
  14138, 10424, 15026, 12424, 18364,
  10294, 17702, 12118, 12032, 14852

lift negative counts by offset: {0: 86, 1: 0}
maximum first positive lift: 1
all non-rescued clear by first positive lift: True
```

The worst target remains `14138`, with first-three `-0.8950145872346785`,
complement `0.018073313793834367`, and full action
`-0.8769412734408442`.  Its lift by one period, `24148`, has first-three
`-0.12082743421006822`, complement `1.3776028000182077`, and full action
`1.2567753658081395`.

The other worst targets have the same qualitative pattern: each is negative
at lift `0`, and the full action is positive at lift `1`.  Some remain below
the first-three tail threshold after lift `1` (`15026`, `17702`, and `14852`
among the worst ten), but their complements are then large enough to rescue
the full action.

Validation: bytecode-disabled `py_compile` passed; `git diff --check` passed;
the strengthened bytecode-disabled focused regression
`test_q286_nonrescued_first_three_tail_classification` passed in `153.798s`.
Before that, the initial schema-focused version had passed in `73.696s`, and
a direct one-target probe at `14138` confirmed the known-target assertion set.

Status `aha-candidate`: the non-rescued minority is not explained by repeated
residues in the first eight periods.  The failures are concentrated near the
early cycles and all checked non-rescued targets clear at same-residue lift
`1`.  This supports a boundary/onset-channel theorem target: prove a finite
initial obstruction set plus a period-lift or cycle-threshold clearance
estimate, rather than trying to bound every first-three negative tail
independently.  No eventual theorem, signed prime-correlation estimate, or
Goldbach proof is established.

## 2026-09-12: sampled later-cycle non-rescue falsifier

After the non-rescued classifier suggested an onset/boundary mechanism, a
larger two-block scan over global cycles `16..31` was attempted but interrupted
without evidence because it gave no progress output.  A narrower falsifier then
tested individual later cycles with visible progress using
`q286_first_three_complement_cooccurrence_receipt`.

```text
global cycle 16, start 170160:
  full-action negatives 0
  minimum full action 0.24084360363205248 at N=171058
  first_three < -.3 tail targets 98, non-rescued inside tail 0

global cycle 24, start 250240:
  full-action negatives 0
  minimum full action 0.2360810314099344 at N=255704
  first_three < -.3 tail targets 24, non-rescued inside tail 0

global cycle 32, start 330320:
  full-action negatives 0
  minimum full action 0.38731649100422866 at N=331444
  first_three < -.3 tail targets 11, non-rescued inside tail 0
```

Status `aha-candidate`: sampled later cycles preserve the onset-clearance
hypothesis and show the broad first-three `.3` tail shrinking in these samples.
This does not prove all later cycles clear, and the interrupted broad scan is
not evidence.  The next bounded theorem/falsifier should either scan all
intervening cycles with progress checkpoints or derive a cycle-parameter
lower bound that explains why non-rescued targets vanish after the early
boundary window.

## 2026-09-12: continuous later-cycle clearance through cycle 32

The intervening-cycle falsifier was then run one cycle at a time for global
cycles `17..23` and `25..31`, closing the gaps between the prior sampled
cycles `16`, `24`, and `32`.  Together with the earlier later-block check over
global cycles `8..15`, this gives checked clearance from global cycle `8`
through global cycle `32`: zero full-action negatives and zero non-rescued
`.3` first-three tail targets in every checked cycle after cycle `7`.

Per-cycle results for `17..23`:

```text
cycle 17: min full 0.21536449275070285 at 186206, .3 tail 128
cycle 18: min full 0.17360050532072466 at 194384, .3 tail 71
cycle 19: min full 0.2929123622405331 at 207346, .3 tail 71
cycle 20: min full 0.2588725511282396 at 218324, .3 tail 61
cycle 21: min full 0.39872529505835763 at 226388, .3 tail 33
cycle 22: min full 0.3266126414016192 at 237224, .3 tail 33
cycle 23: min full 0.4015078565586767 at 247444, .3 tail 34
```

Per-cycle results for `25..31`:

```text
cycle 25: min full 0.2838145346629123 at 267406, .3 tail 26
cycle 26: min full 0.3329714387142352 at 272224, .3 tail 35
cycle 27: min full 0.2928208837468891 at 285734, .3 tail 16
cycle 28: min full 0.29640489346594706 at 292664, .3 tail 9
cycle 29: min full 0.4058022481349303 at 308834, .3 tail 11
cycle 30: min full 0.27087324489275805 at 313244, .3 tail 10
cycle 31: min full 0.3328572856429641 at 325156, .3 tail 8
```

Every listed cycle has non-rescued `.3` count `0`.  The smallest later-cycle
minimum in the newly checked individual cycles is cycle `18`, value
`0.17360050532072466`.

Status `changed-under-evidence`: the finite onset-clearance hypothesis has
become sharper: measured non-rescued targets occur only in cycles `0..7`, and
cycles `8..32` are clear.  The next proof target is no longer just "later
samples look good"; it is an eventual cycle-clearance inequality, or a
bounded scan that keeps pushing the first possible recurrence horizon outward
with explicit progress and no hidden batch runs.  Goldbach remains open.

## 2026-09-12: cycles 33 through 40 preserve onset-clearance

A bounded curiosity pursuit tested whether the first possible recurrence after
the continuous `8..32` clearance appears immediately in cycles `33..40`.  The
scan used one-cycle progress output and threshold `.3`.

```text
cycle 33: min full 0.42833183582677603 at 348034, .3 tail 6
cycle 34: min full 0.3251629846307217 at 357344, .3 tail 9
cycle 35: min full 0.4092351836182406 at 360494, .3 tail 10
cycle 36: min full 0.4442751912780733 at 371726, .3 tail 9
cycle 37: min full 0.31158984534443446 at 383486, .3 tail 12
cycle 38: min full 0.3942721291260182 at 397186, .3 tail 4
cycle 39: min full 0.4643236210873841 at 409226, .3 tail 2
cycle 40: min full 0.4194037639449049 at 416996, .3 tail 6
```

Every listed cycle has full-action negative count `0` and non-rescued `.3`
count `0`.  The smallest minimum in this sweep is cycle `37`, value
`0.31158984534443446`.

Status `aha-candidate`: the onset-clearance mechanism survived the first
post-32 recurrence sweep.  The `.3` first-three tail is small but not gone;
therefore the likely theorem is not simply "eventually no `.3` tail", but
"eventually every `.3` tail is complement-rescued" with a separate finite
initial exception table.  This remains finite evidence, not a proof.

## 2026-09-12: non-rescued cycle-horizon receipt

`q286_nonrescued_first_three_tail_cycle_horizon_receipt` now codifies the
cycle-clearance horizon question directly.  For each cycle it records full-
action negatives, `.3` first-three tail count, non-rescued tail count, minimum
full action, minimum recombined value inside the tail, and the first suffix of
the checked horizon where all non-rescued tail counts vanish.

The focused regression locks the known transition boundary:

```text
start 80070, cycle_count 2, targets_per_cycle 5005, threshold .3
local cycle 0 / global cycle 7: non-rescued tail count 2
local cycle 1 / global cycle 8: non-rescued tail count 0
cycles_with_nonrescued_tail_targets: (0,)
suffix_clear_start_cycle: 1
suffix_clear_global_cycle: 8
```

Validation: bytecode-disabled `py_compile` passed; focused regression
`test_q286_nonrescued_first_three_tail_cycle_horizon` passed in `202.762s`.

Status `changed-under-evidence`: the manually measured onset-clearance lane is
now reproducible as a task-owned receipt.  This does not prove eventual
clearance, but it turns future horizon extensions and falsifiers into one
standard API instead of ad hoc one-cycle scripts.

## 2026-09-12: cycles 41 through 48 preserve receipt-driven clearance

The new cycle-horizon receipt was then used for the next recurrence band,
global cycles `41..48`, one cycle at a time.  Every checked cycle again has
full-action negative count `0` and non-rescued `.3` first-three tail count
`0`.

```text
cycle 41: min full 0.4011370672130772 at 425186, .3 tail 5
cycle 42: min full 0.3632776359552527 at 438458, .3 tail 7
cycle 43: min full 0.37175458031519565 at 440866, .3 tail 1
cycle 44: min full 0.3415555323766872 at 458576, .3 tail 5
cycle 45: min full 0.41925661871917613 at 461936, .3 tail 5
cycle 46: min full 0.3722882842435854 at 474886, .3 tail 8
cycle 47: min full 0.3560917899268151 at 480614, .3 tail 12
cycle 48: min full 0.3753970321225119 at 492056, .3 tail 8
```

The smallest minimum in this band is cycle `44`, value
`0.3415555323766872`.  The `.3` tail still recurs, so the candidate remains
eventual complement rescue of tail targets, not eventual disappearance of the
tail.

Status `aha-candidate`: the checked continuous clearance horizon now reaches
global cycle `48`.  This strengthens the boundary/onset hypothesis but is
still finite evidence only.

## 2026-09-12: preserve rescued tail target lists

`q286_first_three_complement_cooccurrence_receipt` now stores the actual
`tail_targets` and `rescued_tail_targets` for each negative first-three
threshold, not just their counts.  The cycle-horizon receipt carries those
tuples through each cycle row as well.  This is a data-contract improvement
for the next proof/falsifier step: inspect the rescued targets and their
components directly, rather than treating complement rescue as an aggregate
count.

Validation: bytecode-disabled `py_compile` passed; focused regression
`test_q286_first_three_complement_cooccurrence` passed in `79.293s`; focused
regression `test_q286_nonrescued_first_three_tail_cycle_horizon` passed in
`223.811s`.

Status `changed-under-evidence`: future mechanism searches can use exact
tail/rescue target lists from the receipt.  No mathematical theorem is added
by this data-shape change.

## 2026-09-12: cycle 43 single-tail microscope

The new target-list receipt was applied to global cycle `43`, where the `.3`
tail count is `1`.  The unique tail target is `448346`, and it is rescued:

```text
cycle 43 range: 440430..450438
tail_targets: (448346,)
rescued_tail_targets: (448346,)
nonrescued: ()
cycle minimum full action: 440866, value 0.37175458031519565
minimum tail recombination: 448346, value 0.6674962581507213
```

A selected-target component check gives:

```text
target 448346
first_three: -0.3106946886916736
complement: 0.9781909468423949
full: 0.6674962581507213
mode1: -0.07325200159068547
mode2: -0.22838146439652587
mode3-through-6: -0.015412775568364774
full_without_first_two: 0.9691297241379326
full_without_first_three: 0.9781909468423949
```

Status `aha-candidate`: at least this late single-tail case is not a delicate
near-zero rescue.  It barely enters the `.3` first-three tail and has a large
post-first-three complement buffer.  A plausible proof target is now a
two-zone statement: finite/boundary non-rescued exceptions, plus an eventual
tail regime where the first-three deficit is shallow or the complement buffer
is uniformly large.

## 2026-09-12: first-three tail rescue-profile receipt

`q286_first_three_tail_rescue_profile_receipt` now makes the complement-rescue
mechanism inspectable.  For a finite cycle window it stores exact tail targets,
rescued/non-rescued target splits, per-tail deficit, complement, recombined
margin, complement-over-threshold, complement-over-deficit, and cycle/global
extrema.

The focused regression uses the cycle `43` microscope:

```text
start 440430, cycle_count 1, targets_per_cycle 5005, threshold .3
tail_targets: (448346,)
rescued_tail_targets: (448346,)
nonrescued_tail_targets: ()
first_three: -0.3106946886916736
complement: 0.9781909468423949
rescue_margin: 0.6674962581507213
```

Validation: bytecode-disabled `py_compile` passed; focused regression
`test_q286_first_three_tail_rescue_profile` passed in `254.052s`.

Status `changed-under-evidence`: complement rescue is now a first-class
measured object in the code.  The next falsifier can profile entire later
bands and ask whether rescued tails are uniformly shallow, uniformly buffered,
or split between the two.  No eventual theorem is proved.

## 2026-09-12: cycle 41 through 48 rescue-profile band

The rescue-profile receipt was applied one cycle at a time to global cycles
`41..48` with threshold `.3`.  A first eight-cycle batched profile attempt was
interrupted without evidence because it produced no progress output; the
recorded results below come from progress-visible one-cycle receipt calls.

```text
cycle 41: tail 5, nonrescued 0,
  deepest deficit 0.39427060083228704 at 425588,
  min complement 0.781798032050101 at 422558,
  min margin 0.4707764146934693 at 422558
cycle 42: tail 7, nonrescued 0,
  deepest deficit 0.46290305391350506 at 438458,
  min complement 0.8204259011595246 at 439258,
  min margin 0.3632776359552527 at 438458
cycle 43: tail 1, nonrescued 0,
  deepest deficit 0.3106946886916736 at 448346,
  min complement 0.9781909468423949 at 448346,
  min margin 0.6674962581507213 at 448346
cycle 44: tail 5, nonrescued 0,
  deepest deficit 0.3692776238508373 at 457886,
  min complement 0.8724528784004306 at 450716,
  min margin 0.5405019857795196 at 452126
cycle 45: tail 5, nonrescued 0,
  deepest deficit 0.35636261412344544 at 467066,
  min complement 0.8521273377762162 at 467066,
  min margin 0.4957647236527708 at 467066
cycle 46: tail 8, nonrescued 0,
  deepest deficit 0.37843343883082914 at 475046,
  min complement 0.6972694262235392 at 474886,
  min margin 0.3722882842435854 at 474886
cycle 47: tail 12, nonrescued 0,
  deepest deficit 0.3944561276678578 at 487304,
  min complement 0.6963418713847755 at 480614,
  min margin 0.3560917899268151 at 480614
cycle 48: tail 8, nonrescued 0,
  deepest deficit 0.3595148345647118 at 495086,
  min complement 0.6776643969822953 at 492056,
  min margin 0.3753970321225119 at 492056
```

Across this band, deepest measured deficit is `0.46290305391350506`, minimum
measured complement is `0.6776643969822953`, and minimum measured rescue
margin is `0.3560917899268151`.

Status `aha-candidate`: in cycles `41..48`, rescue is not merely shallow-tail
avoidance; there is also a substantial complement floor on the tail set.  The
next theorem target can be stated more concretely as an eventual tail-set
complement lower bound, with finite boundary exceptions.  This remains finite
evidence.

## 2026-09-12: cycle 8 through 15 transition rescue profile

The first all-rescued block after the non-rescued boundary exceptions was then
profiled one cycle at a time.  Every `.3` first-three tail target in global
cycles `8..15` is rescued, but the rescue margins show this is still a
transition zone, not yet the same comfortable lower-buffer regime seen in
cycles `41..48`.

```text
cycle 8: tail 241, nonrescued 0,
  deepest deficit 0.7148225634431425 at 91502,
  min complement 0.43158471467708337 at 90236,
  min margin 0.012576466293799509 at 94856
cycle 9: tail 171, nonrescued 0,
  deepest deficit 0.5926699645046699 at 109796,
  min complement 0.5806226642468715 at 109178,
  min margin 0.07726048593671965 at 109178
cycle 10: tail 140, nonrescued 0,
  deepest deficit 0.6411932627360791 at 114992,
  min complement 0.5727079396588117 at 118376,
  min margin 0.1550114122052504 at 110522
cycle 11: tail 127, nonrescued 0,
  deepest deficit 0.5997410872772851 at 121006,
  min complement 0.547769243338859 at 125294,
  min margin 0.1605535322957213 at 125504
cycle 12: tail 56, nonrescued 0,
  deepest deficit 0.6723169131273059 at 130436,
  min complement 0.6592212264718553 at 134252,
  min margin 0.26395705277117026 at 130436
cycle 13: tail 50, nonrescued 0,
  deepest deficit 0.4632755258077992 at 146038,
  min complement 0.6883035728573399 at 143984,
  min margin 0.28109028136702996 at 142456
cycle 14: tail 46, nonrescued 0,
  deepest deficit 0.5026436484490796 at 153848,
  min complement 0.5180359445835337 at 156304,
  min margin 0.1966652332290977 at 151766
cycle 15: tail 60, nonrescued 0,
  deepest deficit 0.509781424812556 at 160648,
  min complement 0.7025730485646823 at 163652,
  min margin 0.27790002360283217 at 168748
```

Across this block, deepest measured deficit is `0.7148225634431425`, minimum
tail-set complement is `0.43158471467708337`, and minimum rescue margin is
only `0.012576466293799509`.

Status `changed-under-evidence`: cycle `8` through `15` refines the two-zone
picture into at least three zones: finite non-rescued boundary cycles `0..7`,
rescued-but-delicate transition cycles beginning at `8`, and later
large-buffer cycles such as `41..48`.  An eventual complement-floor theorem
may still be viable, but it cannot honestly start at cycle `8` with the later
band's comfortable constants.

## 2026-09-12: cycle 16 through 23 transition-to-buffer profile

The next block was profiled to locate where the rescued-but-delicate transition
begins to resemble the later large-buffer regime.

```text
cycle 16: tail 98, nonrescued 0,
  deepest deficit 0.5527135941604301 at 175318,
  min complement 0.5760177247529142 at 171298,
  min margin 0.24084360363205248 at 171058
cycle 17: tail 128, nonrescued 0,
  deepest deficit 0.6743272141983545 at 189598,
  min complement 0.5889821568177451 at 186206,
  min margin 0.21536449275070285 at 186206
cycle 18: tail 71, nonrescued 0,
  deepest deficit 0.48287099311618276 at 193888,
  min complement 0.4989495025198246 at 194384,
  min margin 0.17360050532072466 at 194384
cycle 19: tail 71, nonrescued 0,
  deepest deficit 0.48201659617143827 at 201298,
  min complement 0.6780178733043838 at 204884,
  min margin 0.2929123622405331 at 207346
cycle 20: tail 61, nonrescued 0,
  deepest deficit 0.43884496135661705 at 210788,
  min complement 0.5988837526199124 at 218324,
  min margin 0.2588725511282396 at 218324
cycle 21: tail 33, nonrescued 0,
  deepest deficit 0.39066098536104277 at 223738,
  min complement 0.743572200067494 at 226388,
  min margin 0.39872529505835763 at 226388
cycle 22: tail 33, nonrescued 0,
  deepest deficit 0.4409537634451392 at 230378,
  min complement 0.6410327223101169 at 237224,
  min margin 0.3266126414016192 at 237224
cycle 23: tail 34, nonrescued 0,
  deepest deficit 0.39781870621255433 at 249178,
  min complement 0.8442681247456885 at 248294,
  min margin 0.49510376866205685 at 248294
```

Across cycles `16..23`, deepest measured deficit is `0.6743272141983545`,
minimum complement is `0.4989495025198246`, and minimum rescue margin is
`0.17360050532072466`.  Cycles `16..20` still have transition-size margins;
cycles `21..23` move closer to the later large-buffer pattern.

Status `changed-under-evidence`: the measured transition zone extends at least
through cycle `20`.  A plausible next falsifier is to profile cycles `24..40`
and ask whether all cycles from `21` onward maintain a stable complement floor,
or whether additional dips force a longer transition exception range.

## 2026-09-12: cycle 24 through 32 rescue-profile block

Cycles `24..32` were profiled to test whether the stable complement floor might
begin around cycle `21`.  Every `.3` tail target is rescued, but the band still
contains dips below the later `41..48` floor.

```text
cycle 24: tail 24, nonrescued 0,
  deepest deficit 0.44657825143023566 at 253948,
  min complement 0.5500849164245104 at 255704,
  min margin 0.2360810314099344 at 255704
cycle 25: tail 26, nonrescued 0,
  deepest deficit 0.4471460665759927 at 263818,
  min complement 0.6007609171755264 at 267406,
  min margin 0.2838145346629123 at 267406
cycle 26: tail 35, nonrescued 0,
  deepest deficit 0.44374046537763967 at 276908,
  min complement 0.6873831502570427 at 273554,
  min margin 0.37781577724659793 at 273554
cycle 27: tail 16, nonrescued 0,
  deepest deficit 0.42167301271086116 at 283978,
  min complement 0.7284779611458865 at 283984,
  min margin 0.3701615804113509 at 281794
cycle 28: tail 9, nonrescued 0,
  deepest deficit 0.42049668248053657 at 297698,
  min complement 0.8633215437422637 at 290614,
  min margin 0.5214200073841513 at 290614
cycle 29: tail 11, nonrescued 0,
  deepest deficit 0.3502973592209339 at 302068,
  min complement 0.8013120275242169 at 304718,
  min margin 0.4672757791717939 at 304718
cycle 30: tail 10, nonrescued 0,
  deepest deficit 0.38848590069555405 at 313244,
  min complement 0.60662043049502 at 316604,
  min margin 0.27087324489275805 at 313244
cycle 31: tail 8, nonrescued 0,
  deepest deficit 0.40441112104182764 at 321326,
  min complement 0.8175201849094438 at 320906,
  min margin 0.46258734180359734 at 321326
cycle 32: tail 11, nonrescued 0,
  deepest deficit 0.38706490670172006 at 337738,
  min complement 0.7752913928884343 at 339788,
  min margin 0.4107035662278525 at 339788
```

Across cycles `24..32`, deepest measured deficit is `0.4471460665759927`,
minimum complement is `0.5500849164245104`, and minimum rescue margin is
`0.2360810314099344`.

Status `changed-under-evidence`: a stable later-band floor does not begin at
cycle `21` with the `41..48` constants; cycles `24`, `25`, and `30` still dip.
The transition exception range may extend at least through cycle `30`, though
all checked tails remain rescued.

## 2026-09-12: cycle 33 through 40 rescue-profile gap

Cycles `33..40` were profiled to close the gap before the already-profiled
`41..48` band.

```text
cycle 33: tail 6, nonrescued 0,
  deepest deficit 0.34321738931316387 at 346106,
  min complement 0.7375394421707127 at 348034,
  min margin 0.42833183582677603 at 348034
cycle 34: tail 9, nonrescued 0,
  deepest deficit 0.4015357008802212 at 357838,
  min complement 0.9944590534863758 at 359558,
  min margin 0.6629863461200328 at 359558
cycle 35: tail 10, nonrescued 0,
  deepest deficit 0.36500539908474905 at 360638,
  min complement 0.8178747303615322 at 367298,
  min margin 0.5093338345489309 at 367298
cycle 36: tail 9, nonrescued 0,
  deepest deficit 0.4258451609398066 at 372332,
  min complement 0.7885951080158726 at 371726,
  min margin 0.4442751912780733 at 371726
cycle 37: tail 12, nonrescued 0,
  deepest deficit 0.37765470838997645 at 380642,
  min complement 0.6393542776650206 at 383486,
  min margin 0.31158984534443446 at 383486
cycle 38: tail 4, nonrescued 0,
  deepest deficit 0.32710356439231264 at 399898,
  min complement 0.7963661886207664 at 395102,
  min margin 0.4794316683488638 at 395102
cycle 39: tail 2, nonrescued 0,
  deepest deficit 0.3094987184808311 at 405872,
  min complement 1.0919527773516675 at 405872,
  min margin 0.7824540588708364 at 405872
cycle 40: tail 6, nonrescued 0,
  deepest deficit 0.3846501792659953 at 414986,
  min complement 0.7579188931125779 at 416242,
  min margin 0.43699838873029884 at 416242
```

Across cycles `33..40`, deepest measured deficit is `0.4258451609398066`,
minimum complement is `0.6393542776650206`, and minimum rescue margin is
`0.31158984534443446`.

Status `aha-candidate`: cycles `33..40` look like a large-buffer regime with
a weaker floor than the `41..48` band because of cycle `37`.  A plausible
finite profile now has boundary `0..7`, delicate transition `8..20`, middle
transition/buffer `21..32`, and a stronger buffer from at least cycle `33` in
the checked data.  This is still finite evidence.

## 2026-09-12: cycle 49 through 56 fresh buffer falsifier

To test whether the apparent stronger buffer from cycle `33` onward survives a
fresh later band, cycles `49..56` were profiled one cycle at a time.

```text
cycle 49: tail 6, nonrescued 0,
  deepest deficit 0.44255568348284197 at 509672,
  min complement 0.8368015445516385 at 508348,
  min margin 0.46078186902488183 at 510152
cycle 50: tail 3, nonrescued 0,
  deepest deficit 0.37035214736551525 at 514562,
  min complement 0.7538824783148609 at 518162,
  min margin 0.44122501338695486 at 518162
cycle 51: tail 3, nonrescued 0,
  deepest deficit 0.35747665699173076 at 524102,
  min complement 0.8989632198575439 at 523972,
  min margin 0.572761029891046 at 523972
cycle 52: tail 5, nonrescued 0,
  deepest deficit 0.3888756497982782 at 532628,
  min complement 0.8480642340892312 at 534052,
  min margin 0.5433755019084853 at 534052
cycle 53: tail 8, nonrescued 0,
  deepest deficit 0.3465642209092222 at 548666,
  min complement 0.6899144617707726 at 548666,
  min margin 0.3433502408615505 at 548666
cycle 54: tail 5, nonrescued 0,
  deepest deficit 0.3401085703527049 at 553372,
  min complement 0.8113292463070148 at 560468,
  min margin 0.49576421351691824 at 560468
cycle 55: tail 8, nonrescued 0,
  deepest deficit 0.36650590504909997 at 564082,
  min complement 0.814965663059211 at 564082,
  min margin 0.44845975801011106 at 564082
cycle 56: tail 4, nonrescued 0,
  deepest deficit 0.35420070413168947 at 573304,
  min complement 0.8825192218246329 at 576218,
  min margin 0.5503239726047701 at 576218
```

Across cycles `49..56`, deepest measured deficit is `0.44255568348284197`,
minimum complement is `0.6899144617707726`, and minimum rescue margin is
`0.3433502408615505`.

Status `aha-candidate`: this fresh band does not break the checked stronger
buffer pattern from cycle `33` onward.  The limiting point is cycle `53`, but
it remains above the cycle `37` minimum margin and above the `41..48` minimum
complement.  Still finite evidence only.

## 2026-09-12: tail rescue floor-candidate receipt

`q286_first_three_tail_rescue_floor_candidate_receipt` now turns the checked
large-buffer pattern into an explicit finite falsifier.  The candidate tests:

```text
first_three tail threshold: .3
complement floor: .63
rescue margin floor: .3
optional first-three deficit ceiling: .47
```

The focused regression anchors the limiting checked cycle `37`, where the
candidate still passes:

```text
global cycle 37, start 380370
tail targets: 12
nonrescued tail targets: 0
minimum complement: 0.6393542776650206
minimum rescue margin: 0.31158984534443446
maximum first-three deficit: 0.37765470838997645
complement violations: ()
margin violations: ()
deficit violations: ()
```

Validation: bytecode-disabled `py_compile` passed; focused regression
`test_q286_first_three_tail_rescue_floor_candidate` passed in `195.123s`.

Status `changed-under-evidence`: the post-cycle-33 buffer hypothesis is now an
executable candidate with named constants and violation lists.  It remains a
finite falsifier, not an eventual theorem.

## 2026-09-12: cycles 57 through 64 floor-candidate falsifier

The explicit floor candidate was tested on a fresh later band, global cycles
`57..64`, using complement floor `.63`, rescue margin floor `.3`, and deficit
ceiling `.47`.

```text
cycle 57: tail 3, nonrescued 0, passed True,
  min complement 0.8190553940491911,
  min margin 0.5060636152562996,
  max deficit 0.3548674811303196
cycle 58: tail 1, nonrescued 0, passed True,
  min complement 0.8358976413272554,
  min margin 0.4482571418757897,
  max deficit 0.3876404994514657
cycle 59: tail 1, nonrescued 0, passed True,
  min complement 0.9710569609849097,
  min margin 0.6559217285324122,
  max deficit 0.3151352324524975
cycle 60: tail 4, nonrescued 0, passed True,
  min complement 0.9567430686502207,
  min margin 0.6258862787672124,
  max deficit 0.35470238126589504
cycle 61: tail 0, nonrescued 0, passed True
cycle 62: tail 2, nonrescued 0, passed True,
  min complement 0.8108005830373728,
  min margin 0.510165699170394,
  max deficit 0.3322965476929664
cycle 63: tail 2, nonrescued 0, passed True,
  min complement 1.1103018790146253,
  min margin 0.779117628373549,
  max deficit 0.33872363964153773
cycle 64: tail 1, nonrescued 0, passed True,
  min complement 1.0477337101487416,
  min margin 0.6333079595885993,
  max deficit 0.4144257505601422
```

No complement-floor, margin-floor, or deficit-ceiling violations occurred.
The limiting nonempty cycle in this band is cycle `58` for rescue margin and
cycle `64` for deficit, both still safely inside the finite candidate.

Status `aha-candidate`: the named `.63/.3/.47` floor candidate survived a
fresh later-band falsifier.  This strengthens the cycle-33-onward buffer
hypothesis but remains finite evidence.

## 2026-09-12: cycles 97 through 104 far-band floor-candidate probe

The explicit floor candidate was also tested on a much later band, global
cycles `97..104`, using the same constants:

```text
first_three tail threshold: .3
complement floor: .63
rescue margin floor: .3
optional first-three deficit ceiling: .47
```

Every checked cycle passed, but all passes were vacuous for the floor
inequalities because no `.3` first-three tail targets appeared:

```text
cycle 97: tail 0, nonrescued 0, passed True
cycle 98: tail 0, nonrescued 0, passed True
cycle 99: tail 0, nonrescued 0, passed True
cycle 100: tail 0, nonrescued 0, passed True
cycle 101: tail 0, nonrescued 0, passed True
cycle 102: tail 0, nonrescued 0, passed True
cycle 103: tail 0, nonrescued 0, passed True
cycle 104: tail 0, nonrescued 0, passed True
```

Status `changed-under-evidence`: this is stronger evidence for later-band
absence of the `.3` first-three tail in the sampled far window, but it does
not add a nonempty stress test for the `.63/.3/.47` rescue floors.  The next
mathematical target remains an analytic reason for tail disappearance or
tail rescue beyond the finite windows.

## 2026-09-13: cycles 65 through 96 sparse recurrence and rescue

The mode-only horizon receipt completed the missing cycles in the gap between
the nonempty `57..64` floor-candidate block and the vacuous `97..104` far
band.  Across global cycles `65..96`, the `.3` first-three tail is sparse but
does recur.  Exactly nine checked cycles have one tail hit:

```text
cycle 72: tail 1, min first_three -0.3215492897967754 at 733126
cycle 73: tail 1, min first_three -0.3183278779198759 at 741976
cycle 76: tail 1, min first_three -0.31105367215090923 at 775426
cycle 77: tail 1, min first_three -0.3351606547038982 at 782336
cycle 79: tail 1, min first_three -0.32984168711159817 at 805682
cycle 80: tail 1, min first_three -0.30973201334501105 at 818528
cycle 81: tail 1, min first_three -0.3267869890169187 at 828418
cycle 83: tail 1, min first_three -0.32567901877988487 at 846632
cycle 94: tail 1, min first_three -0.34548559053695327 at 955832
```

The remaining checked cycles in `65..96` have zero `.3` tail hits.  The
largest near misses were cycle `65` at `-0.297132521004334`, cycle `82` at
`-0.297626634216987`, and cycle `86` at `-0.2972215111537993`.

Every sparse recurrence cycle was then stress-tested with the existing
`.63/.3/.47` floor candidate.  All nine passed; all had zero non-rescued tail
targets and no complement, rescue-margin, or deficit violations:

```text
cycle 72: tail 1, nonrescued 0, passed True,
  min complement 1.0285334831447543,
  min margin 0.706984193347979,
  max deficit 0.3215492897967754
cycle 73: tail 1, nonrescued 0, passed True,
  min complement 1.1172241778551262,
  min margin 0.7988962999352504,
  max deficit 0.3183278779198758
cycle 76: tail 1, nonrescued 0, passed True,
  min complement 1.3662358768256575,
  min margin 1.0551822046747483,
  max deficit 0.31105367215090923
cycle 77: tail 1, nonrescued 0, passed True,
  min complement 0.9955200042901746,
  min margin 0.6603593495862764,
  max deficit 0.3351606547038982
cycle 79: tail 1, nonrescued 0, passed True,
  min complement 0.9842009544848696,
  min margin 0.6543592673732714,
  max deficit 0.32984168711159817
cycle 80: tail 1, nonrescued 0, passed True,
  min complement 0.9952438997675463,
  min margin 0.6855118864225354,
  max deficit 0.30973201334501105
cycle 81: tail 1, nonrescued 0, passed True,
  min complement 1.0101301471453275,
  min margin 0.6833431581284087,
  max deficit 0.3267869890169187
cycle 83: tail 1, nonrescued 0, passed True,
  min complement 0.9592810149486167,
  min margin 0.6336019961687318,
  max deficit 0.3256790187798849
cycle 94: tail 1, nonrescued 0, passed True,
  min complement 1.017679414218682,
  min margin 0.6721938236817288,
  max deficit 0.3454855905369533
```

Validation: no-bytecode `py_compile` passed, and focused regression
`test_q286_first_three_tail_mode_only_horizon` passed in `148.520s` before
the scans.

Status `changed-under-evidence`: the far-band tail-disappearance reading is
falsified by sparse recurrences in cycles `65..96`.  The stronger surviving
hypothesis is tail-set rescue: after the finite boundary and transition
regimes, rare `.3` first-three tail hits appear, but the checked hits have
large complement buffers and pass the existing floor candidate.  This is
finite evidence only, not an eventual theorem or a Goldbach proof.

## 2026-09-13: cycles 105 through 136 sparse recurrence falsifier

The next complete 32-cycle block after the vacuous `97..104` window was
scanned with the mode-only horizon receipt.  The `.3` first-three tail is even
sparser in this block: exactly three cycles have one tail hit.

```text
cycle 121: tail 1, min first_three -0.30758776037088004 at 1222142
cycle 131: tail 1, min first_three -0.31527029112934163 at 1323632
cycle 136: tail 1, min first_three -0.3394138842129011 at 1379072
```

All other global cycles in `105..136` were tail-free at threshold `.3`.

The three recurrence cycles were stress-tested with the same `.63/.3/.47`
floor candidate.  All three passed with zero non-rescued tail targets and no
violations:

```text
cycle 121: tail 1, nonrescued 0, passed True,
  min complement 1.2533040265847926,
  min margin 0.9457162662139126,
  max deficit 0.3075877603708801
cycle 131: tail 1, nonrescued 0, passed True,
  min complement 1.339489557365715,
  min margin 1.0242192662363734,
  max deficit 0.31527029112934163
cycle 136: tail 1, nonrescued 0, passed True,
  min complement 1.284412751390588,
  min margin 0.944998867177687,
  max deficit 0.3394138842129011
```

Status `aha-candidate`: this fresh later block strengthens the selected-tail
rescue hypothesis.  Sparse tail recurrences persist, so disappearance remains
false, but all checked late recurrences so far have large complement buffers.
The theorem target is now explicitly a selected-tail complement lower bound
or an explanation of why late tail spikes are forced into high-complement
positions.  Finite evidence only.

## 2026-09-13: accelerated mode-only scanner and cycles 137 through 168

The brute-force mode-only scanner was too slow for repeated far-horizon work:
four 8-cycle workers for cycles `137..168` were stopped after they had each
accumulated more than 1300 CPU seconds without returning a receipt.  That was
productive CPU use, but not a good research loop.

Added `q286_first_three_tail_mode_only_fast_horizon_receipt`, which precomputes
the q286 first-three singular-mode linear functional and uses NumPy residue
accumulation for strict-central prime-pair weights.  The new receipt was
validated against the original slow mode-only horizon receipt on a five-target
focused regression:

```text
test_q286_first_three_tail_mode_only_fast_horizon ... ok
Ran 1 test in 86.198s
```

A one-cycle benchmark for global cycle `137` took about `53.115s`.  Four
accelerated 8-cycle workers then scanned global cycles `137..168`; every cycle
was tail-free at threshold `.3`.

```text
cycles 137..144: no .3 tail hits; block minimum cycle 142,
  target 1435228, first_three -0.27272709731535705
cycles 145..152: no .3 tail hits; block minimum cycle 149,
  target 1505642, first_three -0.25332323305534654
cycles 153..160: no .3 tail hits; block minimum cycle 158,
  target 1595576, first_three -0.22021297112953594
cycles 161..168: no .3 tail hits; block minimum cycle 162,
  target 1636472, first_three -0.24997112424637502
```

Status `engineering-plus-evidence`: the selected-tail rescue hypothesis is not
stress-tested by this block because there are no selected tail targets, but the
absence result is now much cheaper to extend.  This remains finite evidence
only; it is not a Goldbach proof or an eventual tail theorem.

## 2026-09-13: cycles 169 through 200 remain tail-free

The accelerated mode-only scanner was then applied to the next full 32-cycle
block, global cycles `169..200`.  Every cycle was tail-free at threshold `.3`;
there were no selected targets requiring complement rescue-floor checks.

```text
cycles 169..176: no .3 tail hits; block minimum cycle 170,
  target 1714286, first_three -0.2244238458552083
cycles 177..184: no .3 tail hits; block minimum cycle 180,
  target 1817576, first_three -0.24578791073619177
cycles 185..192: no .3 tail hits; block minimum cycle 187,
  target 1890178, first_three -0.23662242439894973
cycles 193..200: no .3 tail hits; block minimum cycle 197,
  target 1991786, first_three -0.19098821755917464
```

Status `finite-tail-absence-evidence`: after sparse recurrences through cycle
`136`, the checked window `137..200` has no `.3` first-three tail hits.  This
does not prove eventual disappearance; it does make the next falsifier cheaper:
continue fast tail scans and apply the expensive rescue-floor receipt only to
nonempty selected-tail cycles.

## 2026-09-13: cycles 201 through 232 remain tail-free

The accelerated scanner was extended through global cycle `232`.  Every cycle
in `201..232` was tail-free at threshold `.3`; again no complement rescue-floor
check was needed.

```text
cycles 201..208: no .3 tail hits; block minimum cycle 206,
  target 2080934, first_three -0.1941773413191678
cycles 209..216: no .3 tail hits; block minimum cycle 216,
  target 2180908, first_three -0.20154505507379825
cycles 217..224: no .3 tail hits; block minimum cycle 217,
  target 2191822, first_three -0.20736210641526237
cycles 225..232: no .3 tail hits; block minimum cycle 231,
  target 2326222, first_three -0.20693553807121948
```

Status `finite-tail-absence-evidence`: checked cycles `137..232` are now
tail-free at threshold `.3`, but this still does not prove eventual
disappearance.  The current falsifier remains any later fast-scan cycle with a
`.3` first-three tail hit, followed by a rescue-floor failure.

## 2026-09-13: cycles 233 through 264 remain tail-free

The accelerated scanner was extended through global cycle `264`.  Every cycle
in `233..264` was tail-free at threshold `.3`; no complement rescue-floor
check was needed.

```text
cycles 233..240: no .3 tail hits; block minimum cycle 235,
  target 2366548, first_three -0.18648556964961702
cycles 241..248: no .3 tail hits; block minimum cycle 245,
  target 2466634, first_three -0.18814240147876807
cycles 249..256: no .3 tail hits; block minimum cycle 250,
  target 2516512, first_three -0.1956485325659766
cycles 257..264: no .3 tail hits; block minimum cycle 257,
  target 2584486, first_three -0.18282739060588282
```

Status `finite-tail-absence-evidence`: checked cycles `137..264` are now
tail-free at threshold `.3`.  This strengthens the post-136 finite horizon but
still does not prove eventual disappearance or Goldbach.

## 2026-09-13: cycles 265 through 296 remain tail-free

The accelerated scanner was extended through global cycle `296`.  Every cycle
in `265..296` was tail-free at threshold `.3`; no complement rescue-floor
check was needed.

```text
cycles 265..272: no .3 tail hits; block minimum cycle 266,
  target 2672932, first_three -0.19902872242009065
cycles 273..280: no .3 tail hits; block minimum cycle 273,
  target 2751106, first_three -0.1771080171549704
cycles 281..288: no .3 tail hits; block minimum cycle 288,
  target 2900782, first_three -0.16965353530921884
cycles 289..296: no .3 tail hits; block minimum cycle 292,
  target 2935984, first_three -0.19368388953654794
```

Status `finite-tail-absence-evidence`: checked cycles `137..296` are now
tail-free at threshold `.3`.  The deepest value in the last 160 checked cycles
is still above `-.3`, but this is finite evidence only.

## 2026-09-13: fast scanner late-tail regression

The fast scanner now has a focused equivalence regression on the known late
tail target `1222142` from global cycle `121`.  The direct one-target probe
matched the slow mode-only scanner to within about `6.2e-16`, and the committed
test passed:

```text
test_q286_first_three_tail_mode_only_fast_late_tail_hit ... ok
Ran 1 test in 60.506s
```

Status `validation`: the optimized scanner is checked on both an initial
five-target window and a late nonempty `.3` tail target.  This validates the
finite scanner implementation, not an eventual theorem.

## 2026-09-13: sparse tail hit residue profile

Added `q286_first_three_tail_hit_residue_profile_receipt`, a finite diagnostic
over the validated fast scanner.  It classifies first-three tail hits by target
residue modulo `286`, target residue modulo the full arithmetic period
`10010`, target offset inside the period, and cycle residues modulo `11` and
`13`.  Focused regression
`test_q286_first_three_tail_hit_residue_profile` passed in `28.527s`.

Applying the receipt to the sparse-hit bands gives:

```text
cycles 65..96: 9 tail hits
  residues mod 286: {20: 2, 72: 1, 80: 1, 92: 1, 108: 1,
    126: 1, 162: 1, 282: 1}
  repeated mod 286 residues: (20,)
  residues mod 10010: {1236: 1, 1556: 1, 2396: 1, 4656: 1,
    4882: 2, 5792: 1, 7598: 1, 7718: 1}
  repeated mod 10010 residues: (4882,)

cycles 105..136: 3 tail hits
  residues mod 286: {24: 1, 64: 1, 266: 1}
  repeated mod 286 residues: ()
  residues mod 10010: {922: 1, 2312: 1, 7702: 1}
  repeated mod 10010 residues: ()
```

Status `falsifier`: the sparse late first-three tail is not explained by a
single q286 residue channel or a single full-period residue in the checked
nonempty bands.  The next proof-facing target should not be a one-residue
exception theorem; it should either explain isolated signed-prime oscillation
events across several residues or prove selected-tail complement rescue.

## 2026-09-13: cycles 297 through 328 remain tail-free

The accelerated scanner was extended through global cycle `328`.  Every cycle
in `297..328` was tail-free at threshold `.3`; no complement rescue-floor
check was needed.

```text
cycles 297..304: no .3 tail hits; block minimum cycle 297,
  target 2986282, first_three -0.1868226923569528
cycles 305..312: no .3 tail hits; block minimum cycle 305,
  target 3069904, first_three -0.15929169145794012
cycles 313..320: no .3 tail hits; block minimum cycle 315,
  target 3170596, first_three -0.1684585498216937
cycles 321..328: no .3 tail hits; block minimum cycle 328,
  target 3299602, first_three -0.19260805167808093
```

Status `finite-tail-absence-evidence`: checked cycles `137..328` are now
tail-free at threshold `.3`.  This remains finite evidence only, not an
eventual first-three tail theorem.

## 2026-09-13: post-136 near-tail threshold profile

The fast scanner was rerun on cycles `137..264` with thresholds `.2`, `.25`,
`.275`, and `.3` to test whether the `.3` disappearance is a sharp threshold
artifact or part of broader damping.  Results:

```text
cycles 137..168:
  .2 tail count 57, last cycle 167
  .25 tail count 4, last cycle 149
  .275 tail count 0
  .3 tail count 0
  minimum first_three -0.27272709731535705 at cycle 142

cycles 169..200:
  .2 tail count 17, last cycle 191
  .25 tail count 0
  .275 tail count 0
  .3 tail count 0
  minimum first_three -0.24578791073619177 at cycle 180

cycles 201..232:
  .2 tail count 3, last cycle 231
  .25 tail count 0
  .275 tail count 0
  .3 tail count 0
  minimum first_three -0.20736210641526237 at cycle 217

cycles 233..264:
  .2 tail count 0
  .25 tail count 0
  .275 tail count 0
  .3 tail count 0
  minimum first_three -0.1956485325659766 at cycle 250
```

Status `finite-damping-evidence`: checked data now shows a stronger staged
finite pattern after cycle `136`: no `.275` tail from `137..264`, no `.25` tail
after cycle `149` through `264`, and no `.2` tail after cycle `231` through
`264`.  This suggests a proof-facing envelope target, but it is still finite
evidence only and does not prove eventual disappearance.

## 2026-09-13: threshold-ladder receipt

Added `q286_first_three_tail_threshold_ladder_receipt`, a reusable finite
diagnostic for the near-tail damping question.  It wraps the validated fast
mode-only scanner and summarizes tail counts across nested thresholds by
whole window and by configurable cycle blocks.  Focused regression
`test_q286_first_three_tail_threshold_ladder` passed in `29.667s` on known
late tail target `1222142`, where `.2` and `.3` tails are present but `.4`
is cleared.

A redundant attempt to rerun the ladder receipt over cycles `265..328` was
stopped after it remained CPU-bound for too long.  No result from that
interrupted probe is recorded.  The earlier committed per-cycle minima already
show that cycles `265..328` stay above `-.2`, but future confirmations should
use narrower blocks or an optimized summary-only path.

Status `tooling`: near-tail threshold ladders are now reproducible, but the
receipt is still a finite diagnostic.  It proves no eventual envelope and no
Goldbach theorem.

## 2026-09-13: threshold-ladder summary path

The accelerated first-three tail scanner now has a private summary mode used
by `q286_first_three_tail_threshold_ladder_receipt`.  Public calls to
`q286_first_three_tail_mode_only_fast_horizon_receipt` still retain per-target
rows for equivalence checks and residue profiling; the threshold ladder uses
the same scan but returns an empty `rows` payload with
`target_rows_included=False`.

Validation:

```text
python -B -m py_compile lcm_sawtooth_goldbach_transfer.py test_lcm_sawtooth_goldbach_transfer.py
test_q286_first_three_tail_mode_only_fast_horizon ... ok
test_q286_first_three_tail_hit_residue_profile ... ok
test_q286_first_three_tail_threshold_ladder ... ok
Ran 3 tests in 82.235s
```

Status `tooling`: this removes avoidable row retention from long ladder
probes and preserves rowful diagnostics where they are semantically required.
It is not new finite evidence and proves no eventual q286 tail bound.

## 2026-09-13: cycles 265 through 328 threshold ladder

Using the summary-mode threshold-ladder receipt, cycles `265..328` were
confirmed clear at thresholds `.2`, `.25`, `.275`, and `.3`.  The run was
split into four 16-cycle probes to avoid repeating the interrupted monolithic
64-cycle attempt.  Each probe tested `80080` targets and returned
`target_rows_included=False`.

```text
265..272: counts {.2: 0, .25: 0, .275: 0, .3: 0},
  minimum cycle 266, target 2672932, first_three -0.19902872242009065
273..280: counts {.2: 0, .25: 0, .275: 0, .3: 0},
  minimum cycle 273, target 2751106, first_three -0.1771080171549704
281..288: counts {.2: 0, .25: 0, .275: 0, .3: 0},
  minimum cycle 288, target 2900782, first_three -0.16965353530921884
289..296: counts {.2: 0, .25: 0, .275: 0, .3: 0},
  minimum cycle 292, target 2935984, first_three -0.19368388953654794
297..304: counts {.2: 0, .25: 0, .275: 0, .3: 0},
  minimum cycle 297, target 2986282, first_three -0.1868226923569528
305..312: counts {.2: 0, .25: 0, .275: 0, .3: 0},
  minimum cycle 305, target 3069904, first_three -0.15929169145794012
313..320: counts {.2: 0, .25: 0, .275: 0, .3: 0},
  minimum cycle 315, target 3170596, first_three -0.1684585498216937
321..328: counts {.2: 0, .25: 0, .275: 0, .3: 0},
  minimum cycle 328, target 3299602, first_three -0.19260805167808093
```

Status `finite-damping-evidence`: checked cycles now show no `.2` tail from
cycle `233` through `328`, no `.25` tail after cycle `149` through `328`, and
no `.275` or `.3` tail from cycle `137` through `328`.  This is finite
evidence only, not an eventual q286 tail theorem.

## 2026-09-13: prime-sliced fast scanner

The accelerated first-three scanner now slices the precomputed prime table for
strict-central candidate primes instead of constructing each full central
integer interval and then masking nonprimes.  This keeps the measured receipt
semantics unchanged while reducing avoidable per-target array work.

Validation:

```text
python -B -m py_compile lcm_sawtooth_goldbach_transfer.py test_lcm_sawtooth_goldbach_transfer.py
test_q286_first_three_tail_mode_only_fast_horizon ... ok
test_q286_first_three_tail_mode_only_fast_late_tail_hit ... ok
test_q286_first_three_tail_hit_residue_profile ... ok
test_q286_first_three_tail_threshold_ladder ... ok
Ran 4 tests in 85.710s
```

A direct summary-mode one-cycle probe at global cycle `329` tested `5005`
targets in `32.48320049999893s`, returned `target_rows_included=False`, and
was clear at thresholds `.2`, `.25`, `.275`, and `.3`.  Its minimum was target
`3304702`, first-three ratio `-0.1451192809169075`.

Status `engineering-plus-finite-evidence`: this is an equivalent scanner
optimization plus one additional checked clear cycle.  It proves no eventual
tail theorem.

## 2026-09-13: crude max-discrepancy bound falsifier

The q286 first-three linear form gives a clean but too-strong sufficient
condition.  For each target residue, center the first-three coefficient vector
over the locally admissible q286 classes.  If every admissible class has
strict-central log-pair weight within `epsilon * total_weight` of its
admissible mean, then

```text
first_three/principal >=
  -epsilon * centered_coefficient_l1(target mod 286) / principal_mean.
```

For threshold `.2`, the worst target residue would require
`epsilon <= 0.0008292399353636012`; for threshold `.3`, it would require
`epsilon <= 0.0012438599030454018`.  These constants are exact consequences
of the q286 first-three coefficient vector used by the scanner.

A cycle-329 one-cycle probe shows this max-error route is much too blunt:

```text
worst max relative class deviation:
  target 3309688, residue 96
  max_relative_delta 0.004732557895915037
  sufficient epsilon for .2 0.0009242116815595694
  ratio to sufficient epsilon 5.120642803312157
  actual first_three/principal 0.06420907247979844
  crude absolute bound 1.0241285606624315

worst crude-bound margin:
  target 3310440, residue 276
  actual first_three/principal -0.018485733850377103
  max_relative_delta 0.0009614480069711092
  sufficient epsilon for .2 0.0015875174271220405
  crude absolute bound 0.12112597827843535
```

Status `falsifier`: a proof that relies only on a uniform maximum residue
deviation would demand far more equidistribution than the checked harmless
targets exhibit.  The viable theorem target should retain coefficient signs,
weighted norms, or cancellation across q286 residue classes.

## 2026-09-13: weighted discrepancy norm receipt

Added `q286_first_three_weighted_discrepancy_norm_receipt`, which makes the
coefficient-side obstruction reusable.  For each target it computes the
actual first-three signed dot product, the relative `L_infinity` and `L2`
deviations of admissible residue weights from their mean, the corresponding
Cauchy bounds against the centered q286 coefficient vector, and how much of
those bounds is actually used by the negative part.

Validation:

```text
python -B -m py_compile lcm_sawtooth_goldbach_transfer.py test_lcm_sawtooth_goldbach_transfer.py
test_q286_first_three_weighted_discrepancy_norm ... ok
test_q286_first_three_tail_mode_only_fast_horizon ... ok
test_q286_first_three_tail_mode_only_fast_late_tail_hit ... ok
test_q286_first_three_tail_hit_residue_profile ... ok
test_q286_first_three_tail_threshold_ladder ... ok
Ran 5 tests in 84.240s
```

Applying the receipt to global cycle `329` with threshold `.2`:

```text
tested targets: 5005
tail targets below -.2: 0
L_infinity Cauchy-certified clear: 88
L2 Cauchy-certified clear: 182
L_infinity sufficient epsilon range: 0.0008292399353636012..0.0016342415296322433
L2 sufficient epsilon range: 0.0039701076826289435..0.011938870754761672

minimum actual first_three:
  target 3304702, first_three -0.14511928091690746
  L_infinity bound 0.46491537546015893
  L2 bound 0.5323076329663895
  L2 negative utilization 0.27262295696982886

maximum L2 sufficient-ratio:
  target 3305012, first_three 0.09669909148902203
  L2 ratio 3.023923187218037

maximum negative-bound utilization:
  target 3305200, first_three -0.14018011556710205
  L_infinity negative utilization 0.3122496337068043
  L2 negative utilization 0.37431718152903626
```

Status `falsifier-plus-target`: plain `L2` Cauchy is still too weak to explain
the checked `.2` clearance: it certifies only `182/5005` targets in cycle
`329`.  However, the worst negative target uses only about `37.5%` of its
available `L2` bound.  The next theorem target is therefore an alignment or
signed-cancellation estimate for the q286 coefficient vector, not just an
unweighted `L2` discrepancy bound.

## 2026-09-13: cycle-329 alignment profile

The weighted-norm receipt now records `l2_alignment_cosine`, cumulative counts
for negative `L2`-bound utilization, cumulative counts for `L2` sufficient-
ratio exceedance, and the ten strongest negative-alignment rows.  Focused
regression `test_q286_first_three_weighted_discrepancy_norm` passed after
these fields were added.

Applying it to global cycle `329` at threshold `.2`:

```text
tested targets: 5005
tail targets below -.2: 0
negative first-three targets: 2346
L_infinity Cauchy-certified clear: 88
L2 Cauchy-certified clear: 182
L2 sufficient-ratio exceedance counts: {1.0: 4823, 2.0: 1673, 3.0: 1}
negative L2-utilization counts:
  >= .125: 430
  >= .25: 26
  >= .375: 0
  >= .5: 0
  >= .75: 0

strongest negative alignment:
  target 3305200, first_three -0.14018011556710205,
  l2_alignment_cosine -0.37431718152903626,
  l2_to_sufficient_ratio 1.8724777072012133
```

Status `hypothesis-target`: in this checked cycle, a universal negative
alignment ceiling just below `.375` would close the `.2` tail even though
plain `L2` size fails.  This is still finite evidence only.  The next falsifier
is to test whether the `.375` alignment ceiling persists across the checked
post-232 damping window and the earlier sparse-tail window.

## 2026-09-13: selected bad-target alignment check

Added `q286_selected_first_three_alignment_receipt`, a finite diagnostic for
testing an explicit selected target set against a candidate negative-alignment
ceiling.  It wraps the weighted-discrepancy receipt target-by-target and
records tail targets, negative targets, alignment-ceiling violations, the
maximum negative-alignment row, and the maximum `L2` sufficient-ratio row.

Validation:

```text
python -B -m py_compile lcm_sawtooth_goldbach_transfer.py test_lcm_sawtooth_goldbach_transfer.py
test_q286_first_three_weighted_discrepancy_norm ... ok
test_q286_selected_first_three_alignment ... ok
Ran 2 tests in 28.192s
```

Default selected set:

```text
targets:
  10424, 10664, 10814, 14138, 14732, 58736, 88346, 125504,
  448346, 1222142, 3304702, 3305200
tail_count below -.2: 9
negative_count: 11
alignment_ceiling: .375
violation_count: 0
tail_targets:
  10424, 10664, 10814, 14138, 58736, 88346, 125504, 448346, 1222142
maximum negative alignment:
  target 3305200, first_three -0.14018011556710205,
  l2_negative_bound_utilization 0.37431718152903626
maximum L2 sufficient-ratio:
  target 10664, first_three -1.1500880008976309,
  l2_to_sufficient_ratio 26.134535399601887,
  l2_negative_bound_utilization 0.2200322261927699
```

Status `survived-selected-falsifier`: the `.375` negative-alignment ceiling
survives this selected bad-target set, including the first-period worst
first-three tail, the boundary full-negative target, the older `448346` tail,
and the late `1222142` tail.  It remains a finite hypothesis, not a theorem.
The next test is a windowed scan over earlier sparse-tail cycles.

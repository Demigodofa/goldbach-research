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

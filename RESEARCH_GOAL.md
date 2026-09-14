# Rill's chosen mathematical research goal

Owner: Kevin; lead: Rill (`agent.rill`). Purpose: preserve the self-chosen
goal and its evidence rules across continuation, instead of reviving an
expired deadline after a session boundary.

## Latest continuation evidence, 2026-09-13

The q286 first-three route now has a window-level alignment/complement
certificate.  `q286_first_three_tail_alignment_complement_window_receipt`
finds first-three lower-tail hits in a finite window, then checks whether the
measured complement beats the candidate alignment loss `.4*l2_bound`.

Validation: `py_compile` passed, and focused regression
`test_q286_first_three_tail_alignment_complement_window` passed in `79.721s`.

On global cycles `105..136`, at tail threshold `.3`, theorem threshold `.2`,
and alignment ceiling `.4`, the receipt tested `160160` targets, found exactly
three tail hits `1222142,1323632,1379072`, certified all three by complement,
found no failed certificates, and found no actual full-action negatives.  The
worst certificate margin was at `1222142`:

```text
first_three -0.3075877603708801
complement 1.2533040265847926
.4*l2_bound 0.3580390674135778
margin 0.8952649591712147
full 0.9457162662139126
```

The precise unresolved theorem candidate is now:

1. Prove a signed q286 first-three alignment estimate
   `first_three(N) >= -0.4*l2_bound(N)`.
2. Prove a conditioned complement lower envelope
   `full_without_first_three(N) > 0.4*l2_bound(N)` on the first-three lower
   tail, after excluding and finitely checking the boundary/full-negative
   layer.

This is a coefficient-matched binary-prime residue discrepancy problem plus a
complement lower-envelope problem.  It is not solved by a generic max-residue
discrepancy bound, and it is not merely local admissibility.  If this
collapses to an equally hard pointwise prime-pair occupancy theorem in fixed
residue channels, that should be recorded as the impasse rather than promoted
as proof progress.

Status `theorem-shaping-finite-evidence`: the measured sparse late-tail band
fits the complement-vs-alignment route, while the boundary target `14138`
remains an explicit failure of the same sufficient condition.  Goldbach, the
eventual alignment theorem, the eventual complement theorem, and the signed
prime-correlation estimate remain open.

The precise obligation and an obstruction are now recorded in
`notes/q286-complement-alignment-theorem-obligation.md`.  The obstruction is
finite-dimensional but decisive for proof strategy: for any target residue
with nonzero centered q286 first-three coefficient vector, arbitrary
nonnegative admissible weights with the same support and total mass can be
chosen with alignment cosine exactly `-1`.  Therefore a `.4` alignment ceiling
cannot follow from support, nonnegativity, total mass, or Cauchy geometry
alone.  It must use arithmetic information about actual binary prime-pair
residue weights, or else be identified as hard as a pointwise restricted
Goldbach-in-progressions theorem.

That note also records the exact conditional closure now available.  A
pointwise fixed-modulus strict-central equidistribution theorem
`W_N(r)=M_N/|U_q(N)|+o(M_N)` would make all centered coefficient actions
`o(P(N))` and hence give eventual strict-central positivity after a finite
remainder.  This is rigorous as a conditional theorem but is not a proof,
because the hypothesis is already a hard binary Goldbach-in-progressions
statement.  Quantitatively, the q286 first-three L2 route has
`K_a <= 50.37646733742071`; later stress targets are compatible with
L2-relative discrepancies of about `0.021..0.030`, while the boundary target
`14138` would require about `0.000362`.

The sharper target is the q286 character mixture, not full residue
equidistribution.  The first-three term uses `99` nonprincipal character
products `chi_11(p)^alpha chi_13(p)^beta`, with
`sum |a| / principal_mean = 32.308079615836355` and
`||a||_2 / principal_mean = 4.5987212546879235`.  Thus a pointwise triangle
bound with `max |S_{alpha,beta}(N)| <= epsilon M_N` would force a `.2`
principal first-three bound for `epsilon < 0.006190401979261144`; a pointwise
L2 bound on the character-error vector would be substantially sharper.  This
remains an unproved twisted binary-prime correlation theorem.

`q286_first_three_character_mixture_norm_receipt` now measures the exact
99-character vector on selected targets.  Validation passed with focused test
`test_q286_first_three_character_mixture_norm` in `49.460s`.  On selected
stress targets `14138,70526,1222142,1379072,1426262,3305200`, all six
first-three values are negative, but no target is certified by the raw
triangle or plain character-vector L2 bound at `.2` principal.  The vector-L2
negative-bound utilizations are approximately
`.186,.386,.355,.393,.416,.406`, and reconstruction error is below `1.3e-16`.
The next theorem target is therefore coefficient-specific anti-alignment or
internal structure inside the 99-character vector, not a raw norm estimate
alone.

`q286_first_three_character_mode_coordinate_receipt` now measures the
rank-three singular coordinates themselves.  Validation passed with focused
test `test_q286_first_three_character_mode_coordinate` in `50.160s`.  On the
same selected stress targets, the three singular-mode contributions are almost
all same-sign negative; signed/absolute mode ratios are `-1` except
`1222142`, which is `-0.9919670741891364`, and mode 3 is small.  This
falsifies an internal rank-three cancellation explanation.  The next theorem
target is simultaneous negative alignment of q286 singular modes 1 and 2.

`q286_first_two_mode_sign_window_receipt` now measures the mode-1/mode-2 sign
quadrants over finite windows.  Validation passed with focused test
`test_q286_first_two_mode_sign_window` in `51.487s`.  On cycle `0`, sign counts
were `++:1283`, `+-:1132`, `-+:1403`, `--:1187`; `972` targets were below the
`.3` first-three threshold, and `698` of those were both-negative.  Thus the
both-negative quadrant is a strong tail selector but too common to exclude as
a theorem.  The next target is magnitude/subcone control inside that quadrant
or complement co-occurrence there.

`q286_first_two_mode_subcone_magnitude_window_receipt` now refines that
quadrant by thresholds on the sum of singular modes `1` and `2`.  Validation
passed with focused test
`test_q286_first_two_mode_subcone_magnitude_window` in `51.269s`.  On cycle
`0`, first-two below `-.2` found `1401` targets and `971/972` lower-tail
targets; first-two below `-.4` found `608` targets, all lower-tail, but still
did not cover all tails.  This is finite subcone structure, not a theorem.
The next target is persistence in later sparse-tail windows and complement
co-occurrence on that subcone.

`q286_first_two_mode_subcone_complement_window_receipt` now attaches
post-first-three complement rescue to the first-two magnitude subcone.
Validation passed with focused test
`test_q286_first_two_mode_subcone_complement_window` in `108.791s`.  A compact
selected probe on late sparse-tail targets `1222142,1323632,1379072` found all
three below `-.2` in first-two sum, none below `-.4`, and all strongly
rescued by complement with full-action ratios about `.946,1.024,.945`.
This makes `.4` a severe cycle-0 selector rather than a late-tail theorem
candidate.  More threshold receipts would be circular unless tied to a new
mechanism; the next target is the exact theorem behind either `.2` subcone
alignment control, conditioned complement lower bounds, or a proof that this
reduces to fixed-modulus binary Goldbach in progressions.

The non-circular theorem package is now explicit in
`notes/q286-complement-alignment-theorem-obligation.md`.  The remaining
options are: prove eventual extinction of the `.2` first-two subcone, prove
conditioned complement rescue on
`L_12/P < -.2` and `F_3/P < -.3`, or prove that either statement requires a
pointwise fixed-modulus binary-prime-in-progressions theorem.  Further
threshold receipts are demoted unless they test a new mechanism with a
falsifier.  Goldbach and the required pointwise signed prime-correlation
theorem remain open.

A support-decomposition mechanism probe now compares boundary/full-negative
targets `10664,14138,24148` with late sparse-tail subcone targets
`1222142,1323632,1379072` using
`q286_first_three_removed_support_envelope_receipt`.  The late targets all
remain complement-rescued after removing q70 (`without_q70` at least
`1.1759`), with q70, q154, and small-support terms positive.  The boundary
layer differs: `14138` has tiny complement because q70 and q154 are strongly
negative, while `10664` has positive complement but a larger first-three
deficit.  This moves the next proof target from q70-only rescue to positivity
of the lower-support package on the late `.2` subcone, or a reduction showing
that package positivity is again a fixed-modulus binary-prime correlation
theorem.

`q286_subcone_lower_support_package_receipt` now makes that mechanism
executable.  Focused test `test_q286_subcone_lower_support_package` passed in
`59.804s`.  On default selected targets, subcone targets are
`10664,14138,1222142,1323632,1379072`; the nonrescued subcone targets are the
finite boundary examples `10664,14138`, while late targets
`1222142,1323632,1379072` are all rescued, all lower-package-positive, and all
remain rescued after removing q70.  The next theorem target is now exact:
eventual lower-support-package positivity on the late `.2` subcone, or a
reduction showing that positivity is a hard fixed-modulus binary-prime
correlation theorem.

The receipt now records the exact rescue inequality.  With
`G/P = F_3/P + 1 + Q_tail/P + H/P`, where `H` is the non-q286 lower-support
package, rescue is equivalent to `H/P > -1 - Q_tail/P - F_3/P`.  The finite
late examples have positive `H/P`; the boundary failures `10664,14138` miss
this floor.  Thus the current theorem is no longer a vague complement floor:
it is a conditioned lower bound for `H/P` on the late `.2` subcone, after
finite boundary exceptions.

`q286_lower_support_package_support_only_obstruction_receipt` now records the
proof-strategy obstruction: actual witness targets `10664,14138` lie in the
same `.2`/`.3` subcone but fail the lower-support rescue inequality, while
late comparison targets `1222142,1323632,1379072` succeed.  Therefore
the weak projected implication from support, nonnegativity, and total mass is
insufficient.  This does not refute every geometric proof; a viable geometric
route would need additional constraints such as residue moments, symmetry,
target-conditioned adjacency, signed coefficient cones, or other actual
residue-weight structure.  The missing theorem must use such arithmetic
information about the pointwise prime-pair residue weights, or be recorded as
a fixed-modulus binary-prime correlation input.

`q286_lower_support_package_local_discrepancy_receipt` now measures the next
narrowed theorem target.  It decomposes `H/P` into a local admissible mean
plus a centered fixed-modulus residue-weight discrepancy.  Validation:
`py_compile` passed, and focused regression
`test_q286_lower_support_package_local_discrepancy` passed in `90.058s`.

On default selected targets, all five subcone targets are raw-L2-insufficient.
For late targets `1222142,1323632,1379072`, the local admissible mean already
clears the required lower-support floor by about `0.899..0.930` principal, but
plain Cauchy/L2 would require relative discrepancy about `0.0072..0.0075`,
while actual measured relative discrepancy is about `0.0157..0.0164`.
Boundary target `10664` has negative local margin; `14138` has a positive
local margin but a large negative centered action.

Current theorem obligation: prove coefficient-sensitive signed residue-weight
control for the lower-support package on the eventual late `.2`/`.3` subcone,
or record that this is a pointwise fixed-modulus binary Goldbach-in-
progressions theorem.  The weak support/nonnegative/mass implication and a
plain L2 discrepancy theorem are both insufficient at the measured scale.

`q286_lower_support_package_component_local_discrepancy_receipt` now splits
that local discrepancy by CRT support component.  Validation passed with
focused regression
`test_q286_lower_support_package_component_local_discrepancy` in `79.731s`;
component reconstruction error was at most `5.551115123125783e-17`.

The component split shows that boundary failures are not diffuse: `10664` and
`14138` are dominated by simultaneous negative centered action in `(5,7)` and
`(7,11)`, with `14138` having centered actions about `-0.733` and `-0.419`.
Late selected subcone targets have positive local means, and at least one of
the same two channels turns positive enough: `1222142` is led by positive
`(7,11)`, `1323632` by positive `(5,7)`, and `1379072` by positive `(7,11)`
despite mildly negative `(5,7)`.

The next theorem target is now narrower than package positivity: after finite
boundary exceptions, prove that the `.2` first-two / `.3` first-three subcone
cannot have simultaneous strongly negative centered action in both `(5,7)` and
`(7,11)` lower-support channels, or record that as a fixed-modulus pointwise
binary-prime correlation theorem.

`q286_lower_support_component_pair_tail_window_receipt` now makes that target
executable on finite windows: it finds `.2` first-two / `.3` first-three
tail-subcone targets, then measures centered actions for the active component
pair `(5,7)` and `(7,11)`.  Focused regression
`test_q286_lower_support_component_pair_tail_window` passed in `186.487s`.
On witness `1222142`, there is no simultaneous negative pair action:
`(7,11)` is positive while `(5,7)` is only mildly negative.  This supports the
current theorem target but remains finite evidence only.  Broad scans should
wait for coefficient/component caching because the current receipt chains
several heavy decompositions.

The receipt now has a selected-target path for explicit candidates, reducing
the focused regression to `81.792s`.  The current q286 closure map is recorded
both as prose in `notes/q286-closed-lanes-map.md` and as typed graph data in
`notes/q286-closed-lanes-map.graph.json`.

The fixed lower-support component decomposition is now cached in
`_q286_lower_support_component_data`.  The component-local focused regression
calls the receipt twice and verifies a cache hit; it passed in `134.987s`.
This is a real fixed-setup optimization, but it does not yet cache the
target-specific prime-pair or lower-support package work.

## Latest continuation evidence, 2026-09-12

The q286 first-three twisted-correlation route now has a sharper finite
residue-occupancy diagnostic.  The driver residues `133` and `153` were tracked
through consecutive period lifts `0..10` for the `75` first-period targets
where the full assembled strict-central action is negative.  Across `825`
lifted targets, full-action negativity occurs only at lift `0`; every base is
positive by lift `1`.

The first-hit summary is:

- maximum first positive full-action lift: `1`, with no missing bases;
- maximum first lift with at least one positive driver residue: `2`, with no
  missing bases;
- maximum first lift escaping the both-driver-admissible-empty condition: `2`,
  with no missing bases;
- maximum first lift with both driver residues positive: `3`, but `12` bases
  do not have both residues positive in lifts `0..10`.

This changes the next action.  The driver-empty obstruction is real at the
first-cycle bad targets, but it is not persistent under nearby period lifts and
is not equivalent to positivity.  The next bounded finite test should ask
whether a small explicit set of high-positive q286 residues gives a stable
hitting cover for the lower tail, before attempting to formulate the full
pointwise fixed-modulus twisted binary-prime correlation estimate.

That finite test now has a positive result.  The diagnostic
`q286_high_positive_residue_cover_receipt` keeps empty positive-coefficient
residues from the largest negative first-three q286 contribution rows.  For
all `75` exact first-period full-action negative targets, with `top_count=24`,
the greedy cover has only two residues: `133` covers `60` targets and `153`
covers the remaining `15`; uncovered targets: `0`.

This makes the `133/153` mechanism a sharper theorem target, but it remains
finite evidence.  The next proof obligation is an explicit lower-occupancy or
compensation estimate for this residue pair inside the strict-central
binary-prime problem, not a claim that the cover itself proves Goldbach.

An eight-cycle falsifier check strengthened this rather than breaking it:
among `40040` tested targets, the lower-tail receipt found `89` full-action
negatives, and the selected-target high-positive cover again used only residues
`133` and `153`.  Residue `133` covered `70`; residue `153` covered the
remaining `19`; uncovered targets: `0`.

The next action should therefore move from broad discovery to theorem-shaping:
derive the exact congruence/local-admissibility conditions for residues `133`
and `153`, then identify what known or in-repo binary-prime-in-AP estimate
would be sufficient to force enough strict-central occupancy or compensation.

The exact local conditions are now derived.  Residue `133` is `1 mod 11` and
`3 mod 13`; residue `153` is `-1 mod 11` and `-3 mod 13`.  For even `N`, both
channels are admissible in `99/143` classes modulo `143`, at least one is
admissible in `141/143`, and both are inadmissible only at `N == 23 mod 143`
and `N == 120 mod 143`.  The next proof step is therefore not local
admissibility but pointwise strict-central prime-pair occupancy or
coefficient-mixture compensation.

The quantitative margin is now measured.  For the same `89` eight-cycle
negative targets, `q286_high_positive_cover_margin_receipt` finds no missing
cover-residue rows among `133,153`.  The worst extra strict-central log-weight
needed in one cover channel to flip the full assembled action is
`161.06677938455093`, with the same value as the worst target-wise minimum.
By contrast, cancelling the first-three mode alone can require
`927.3759573295491`, so a proof should retain the compensating remainder
instead of trying to dominate the entire first-three lower tail directly.

Hardness audit: a pointwise theorem giving positive strict-central occupancy
in the `133/153` channels for every sufficiently large locally admissible
target would already prove a restricted binary Goldbach theorem for `141/143`
target classes.  Therefore the residue route is not automatically easier than
Goldbach.  Its plausible value is coefficient-specific compensation: when the
cover channels are empty or deficient, a structured remainder may force enough
positive mass.  The next finite falsifier is to inspect positive full-action
targets with admissible-empty `133/153` channels and test whether their
compensation rows form another stable finite pattern.

That compensation falsifier has an initial answer.  In lifts `0,1,2` of the
first-period negative bases, exactly six positive full-action targets still
have both `133/153` admissible-empty:
`25036,25306,25372,25582,26002,26722`.  Their first-three mode sums remain
negative.  The top positive compensating residue rows are recurrent but not a
single clean pair: `1` and `265` appear in `4/6`, while `263`, `211`, and
`283` appear in `3/6`.  This suggests a finite positive portfolio may be needed
if the compensation route is to avoid the full signed-correlation estimate.

The portfolio check is now codified as
`q286_cover_pair_compensation_portfolio_receipt`.  On the same six targets,
with `top_count=24`, residue `263` alone covers all six in the greedy
positive-row portfolio.  However, every first-three mode sum remains negative;
the full-without-first-three component ranges from `1.1168686400774108` to
`1.5840594595083313` principal.  This points the next proof attempt toward a
structured lower bound for the compensating remainder, not merely another
positive first-three residue.

The `263` single-compensator hypothesis is now falsified at first-period
scale.  Among all `5005` first-period targets, `204` are positive even though
both `133/153` are admissible-empty.  Their top-positive first-three rows are
covered by a five-residue greedy portfolio:
`179,29,167,241,109`, with cover counts `135,41,17,8,3` and no uncovered
targets.  The compensation route remains structured, but it is now a finite
portfolio problem rather than a one-channel theorem.

This broader compensation portfolio is now executable through
`q286_positive_both_empty_compensation_cover_receipt`, whose default run
recomputes the same `204` positive both-empty targets, `44` negative both-empty
targets, and five-residue cover.

The local obstruction for that five-residue positive portfolio is now exactly
audited.  `q286_residue_portfolio_local_admissibility_receipt` confirms that
`179,29,167,241,109` has at least one locally admissible channel in every
target class modulo `143`.  Thus the compensating-portfolio route is blocked
by quantitative prime-pair occupancy/correlation, not by local congruence
holes.

Exact local set-cover over the observed positive portfolio shows three
residues already suffice for local completeness, for example `179,29,167` or
`179,29,241`.  Since the measured positive-row cover over the `204` positive
both-empty targets needed five residues, the missing theorem is not about
local availability; it is about quantitative signed contribution in the
occupied rows.

The observed five-residue compensation cover is now verified minimal in its
top-row universe.  `q286_positive_both_empty_compensation_min_cover_receipt`
checks `118` candidate residues across the `204` first-period positive
both-empty targets and finds no size `1`, `2`, `3`, or `4` cover.  Size `5`
covers exist.  This strengthens the separation between easy local coverage and
hard quantitative signed contribution coverage.

The broad compensation portfolio now has sign-direction evidence.  Four of the
five greedy residues, `179,29,241,109`, help only as negative-coefficient
deficits, usually zero-weight rows; only `167` helps as positive-coefficient
surplus.  This pivots the theorem target away from simple favorable-residue
lower bounds and toward either upper/avoidance control for negative
coefficient channels or a global signed-cancellation estimate.

The remainder split is now measured.  On the `204` positive both-empty targets,
all `204` have negative first-three q286 mode sums and all `204` have positive
full-without-first-three remainder.  The first-three range is
`-1.0569183143768839..-0.24090148941651918`, while
full-without-first-three ranges `0.5824447187803936..1.7888048047901408`.
Thus the next proof object is the lower envelope of the compensating remainder,
not positivity of the first-three subsystem.

That lower-envelope target now has an eight-period measurement.  Over `40040`
targets, `q286_first_two_mode_lower_tail_receipt` reports `89` full-action
negatives and `19970` negative first-three q286 sums, but zero nonpositive
full-without-first-three and zero nonpositive reduced-without-first-three
values.  The minimum complement margin is at `N=14138`, where
`full_without_first_three/principal = 0.018073313793834367`.  The current
proof target is therefore a positive lower envelope for the complement plus a
relative bound for the first-three lower tail.

The relative-tail obstruction is now measured by
`q286_first_three_to_complement_ratio_receipt`.  Across the same `40040`
targets, exactly the `89` full-action negatives have
`-first_three/full_without_first_three > 1`; `150` targets exceed `.9` and
`1425` exceed `.5`.  The maximum ratio is `49.52133280284266` at `N=14138`.
The next proof attempt should explain the tiny complement margin at `14138`
and then seek a relative tail bound, not merely an absolute first-three bound.

The hard-ratio bases were tested under period lifts.  For
`14138,16388,10424,15026,17522` and lifts `0..7`, ratio `>1` occurs exactly at
lift `0` for each base and nowhere else.  This falsifies the hypothesis that
the bad behavior is a persistent residue class; it looks like early-cycle
scarcity or a boundary layer that clears under lifting.

The lift-one clearance mechanism is now refined.  For those five hard bases,
`q286_boundary_layer_clearance_receipt` shows all five clear by lift `1` and
all five have positive complement at lift `1`, but only three have any
`133/153` driver occupancy and one remains both-driver admissible-empty.
Therefore the common mechanism is complement growth, not driver-pair filling.
The next proof target is a boundary-layer lower bound for the complement.

The boundary-layer hypothesis now has a top-twenty lift check.  For the top
twenty ratio bases and lifts `0..7`, ratio `>1` occurs exactly once per base
and always at lift `0`.  No tested later lift stays dangerous.  The route now
asks for a proof of complement lower growth after the first boundary layer,
rather than a persistent residue-class obstruction.

The lift-clearance check now covers all `89` eight-period negative targets as
bases.  For lifts `0..3`, ratio `>1` occurs exactly `89` times and always at
lift `0`; no base remains dangerous at lifts `1`, `2`, or `3`.  This makes the
next theorem target an eventual complement lower envelope after the first
arithmetic-period lift, with the initial boundary layer treated separately.

The complement cycle envelope is now quantified.  Over eight complete cycles,
`q286_complement_cycle_envelope_receipt` reports no nonpositive complement
values.  The global complement minimum is the cycle-0 boundary target
`N=14138` with value `0.018073313793834367`; after the first cycle, the
minimum is `0.2104242574698779` at `N=36254`.  This supports splitting the
route into an initial boundary check plus a later-cycle complement lower-bound
theorem.

A later eight-cycle block, global cycles `8..15`, was tested with
`start=90080`.  It has zero full-action negatives, zero complement nonpositive
cases, and minimum complement `0.37335759682269043` at `N=154426`.  This
strengthens the finite case for a small-onset complement lower envelope, while
still leaving the asymptotic theorem open.

The previously pending wider scan over global cycles `16..31` has completed.
It tested `80080` targets and found zero full-action negatives and zero
complement nonpositive cases.  The block complement minimum is
`0.42968514453254214` at `N=205514`.  The finite evidence now suggests a
post-boundary complement floor that strengthens across later tested blocks,
but the required asymptotic lower-envelope theorem remains open.

A coarser sampled later-horizon scan over global cycles `32..47` tested `8016`
targets and again found zero full-action negatives and zero complement
nonpositive cases.  The sampled block complement minimum was
`0.49906371578900943` at `N=440866`.  This supports, but does not prove, an
eventual positive complement lower envelope.

The boundary target `N=14138` was inventoried directly.  It has `75` ordered
strict-central prime pairs and total log-pair weight `5862.85778490767`, so it
is not a raw pair-count scarcity.  The cover residues `133` and `153` have
zero weight, making the obstruction residue-specific signed placement.

The signed anatomy of `N=14138` confirms that interpretation.  The leading
negative rows are empty positive-coefficient residues `133` and `153`, each
contributing about `-0.3224324` principal.  The leading positive rows are
mostly empty negative-coefficient residues such as `211,243,43,257`.  The
missing theorem must therefore control signed residue placement, not only total
strict-central pair count.

The boundary component split now shows the lift-one clearance is broader than
q286 residual compensation.  At `14138`, q286 after first three is positive
`0.028340447523565238` and the full complement is only
`0.018073313793834367`; at lift-one target `24148`, q286 after first three is
slightly negative while full-without-first-three is `1.3776028000182077`.
The next proof target should identify the non-first-three, mostly non-q286
source of the complement lower envelope.

## Current authorization and objective

On 2026-09-08 Kevin removed the six-hour limit and asked what goal Rill
would choose. Rill chose: develop a new proof method for prime-pair coverage,
with Goldbach as the ultimate target. Seek rigorously certified families of
even integers and a composition theorem covering every sufficiently large
even integer. A finite independently checked remainder would then finish
Goldbach. No such universal coverage theorem has been established.

The research is open-ended, with no current wall-clock deadline. The first
observable milestone is a mathematically correct, independently checked
theorem with a bounded literature comparison. Call a result new-to-this-task
until its external novelty has actually been assessed. Historical recognition
is not a measurable promised outcome; prize money and realized earnings remain
zero. No spending, publication, contacts, or foreground input is authorized.

Kevin subsequently authorized Rill to adjust the goal as ideas develop, and
explicitly paused notes/manuscript preparation to concentrate on mathematics.
Do not resume publication packaging without fresh steering. Keep only the
minimal execution state and useful mathematical tests needed to continue.

Each hypothesis has a mechanism, prediction, falsifier, and bounded next
test. Stop or revise individual routes when their evidence warrants it.
An active goal flag, a saved plan, and a queued message are not evidence of
continuous execution. Preserve any execution gaps honestly. Do not mark the
overall goal achieved on the basis of finite verification or a partial theorem.

## First chosen question under the discretionary grant

Question: can an adaptive, target-only normalization make the aggregate
prime-pair certificate work for almost all blocks, while retaining a precise
description of what is still missing for every block?

Residues: exact Goldbach count prefixes recover prime locations
(`notes/count-bootstrap-proof.md`); truncated moments can lose enough
information to permit zero-survivor countermodels
(`notes/exclusion-moment-certificates.md`); the newly derived local-peak
theorem forces every fixed dynamic range of weights to fail on infinitely
many represented blocks (`notes/fixed-precision-weight-obstruction.md`).
These are connections from successive parts of this investigation. They
are not claimed as inspiration from an unrelated earlier project. Mark the
selection as potentially influenced by the current task (`recent-capture-risk`).

First action: derive an almost-all success theorem for the adaptive precision
rule from the checked global weighted mean-square theorem, explicitly handling
unweighted counts, rounding, fixed block length, and exceptional starts.
Initial pursuit budget: 30 minutes of mathematical reasoning/source checking,
at most one bounded reviewer follow-up, no new model installation, spending,
publication, or other external operations. This bounds the experiment, not
the overall research authorization. No compute-heavy range extension is needed.
Abandon or sleep this formulation if it requires an unproved pointwise
distribution assertion or fails the reviewer check; preserve the exact gap.
Do not disguise an almost-all statement as coverage of every named block.

The first question returned `changed-under-evidence`: the adaptive
almost-all theorem was proved and independently checked within its budget.
See `notes/adaptive-moment-almost-all.md`. The local-peak theorem and its
fixed-range obstruction are also checked. A bounded literature comparison
found older uses of the underlying mechanism; external novelty remains
unconfirmed. The next mathematical gap is control of the exceptional blocks,
with effective bounds or an amplification/composition argument that cannot
leave a hidden exceptional family behind.

Current mathematical state, 2026-09-08: the canonical parity-preserving
bootstrap is implemented at local commit 14c6b6c. Starting only from L(6)=1,
it generated the contiguous bound prefix through 20,000 and certified the
separate frozen 1,000-even block 1,002,000..1,003,998; the intervening gap
was not evaluated. The next analytic pursuit also returned
`changed-under-evidence`: an independently checked argument proves
L(N)>=M(N)/2 for all but O_a(X/log(X)^a) even N in [X,2X], for every fixed
a>0 and sufficiently large X. M is the full Goldbach singular-series main
term. The threshold is not numerical, and the exceptional set may be
nonempty. The mathematical argument and source prerequisites are retained
beside the implementation in `parity_bound_bootstrap.py`. No new manuscript
or historical-priority investigation was undertaken. The open target is
coverage of the exceptional family; parity propagation itself does not stall
when a lower bound fails to certify a target.

The next finite refinement reuses earlier numerical lower bounds as well as
their parities. For each residual q dividing N, it clips J(N/q)-2e_q at
the exact same-factor diagonal. The resulting recursive J satisfies
L<=J<=R<=G and the same parity, with no exact-count input. On the same frozen
block it strengthened 280 bounds, with maximum gain 582, but added no new
certifications. `evidence/parity-factor-refinement.json` records this run.
The proved total gain is at most N/(z+1)=O(N^(2/3)) and vanishes on powers
of two. This limits the correction's size; it does not prove that actual
exceptions exist or cannot be repaired. Cross-factor composite-pair control
remains the missing arithmetic step.

The shared-prime reduction now includes composites with different least
factors that share a larger prime. `shared_prime_correction.py` reduces every
such distinct pair to a unique prime divisor ell of N and smaller cofactor
target N/ell. Its lower-bound mode uses earlier numerical bounds; its exact
mode uses earlier parity-recovered prime flags and inspects at most two
smaller targets. Adding the exact correction to canonical L leaves precisely
the ordered coprime composite-pair loss below G. It replaces the same-factor
gain rather than being added on top of it. At N=234 it raises 28 to the exact
count30 by recovering 91+143 and its reflection. The remaining problem is
control of the coprime composite-pair contribution; no universal positivity
or historical-priority claim follows.

A bounded symmetry hypothesis was falsified: re-pairing a fixed four-prime
quartet cannot always transfer its coprime loss to a smaller target. Its
three targets U=ab+cd, V=ac+bd, W=ad+bc satisfy U>V>W, leaving W with no
smaller re-pairing. The smallest cubic-valid example has factors7,11,13,17
and targets262,278,298; all have cutoff6. At262 the actual counts are
L=15, shared correction0, G=17, so this is no Goldbach counterexample.
The algebra and minimality were independently checked, and a regression in
`test_shared_prime_correction.py` retains the falsifier. Finite witness reuse
remains valid; a useful descent must go beyond a fixed quartet's pairings.
This does not test a descent restricted to yet-unknown failed targets.

The quantitative exceptional-set pursuit produced a finite character-model
comparison, retained in `exceptional_character_model.py`. For a primitive real
character of conductor D>21, its prime-sign pair model P and the opposite-sign
semiprime model S satisfy P>=3S/5, uniformly in both bias weights in [0,1].
For powers of two and D>24, P>=2A/3, where A is the number of admissible
residue pairs. Consequently P-rho*S>=11A/90 for rho<=49/100 on that family.
The sign change itself follows from an exact multiplicative character
convolution. Sol independently checked the algebra, all conductor cases, and
the necessary small-conductor exclusions. These are model statements, not
prime-count estimates or coverage of previously uncomputed powers of two.
The bounded pursuit returned `changed-under-evidence`: a possible exceptional
character does not destroy this model margin. A power-saving exceptional-set
theorem for canonical L remains unproved. The relevant Grimmelt--Teravainen
Theorem 7.9 (arXiv:2508.16400v2) does not state the required approximation for
our rough-semiprime weight. The remaining step is to prove that approximation
and its convolution errors, with the correct opposite character sign and
errors relative to any suppressed main term. Historical priority was not
investigated, in accordance with Kevin's latest steering.

The next bounded pursuit closed two analytic prerequisites for the actual
rough-semiprime weight, retained in `rough_semiprime_character.py`. Applying
the source's prime-character estimate twice proves the uniform semiprime
character mean with the positive exceptional term. It includes prime squares,
arbitrary interval endpoints, and the inverse-kernel normalization on the
central half of the range. The argument is valid through power-sized moduli;
its character-mean accuracy at a fixed power is a small constant, not itself
a power saving. An elementary bilinear argument separately proves the
minor-arc Fourier bound Y*R^(-1/3), including the normalized weight. Parseval
then bounds the number of targets with minor contribution larger than
Y/log(Y)^3 by O(Y*R^(-1/2)). These proofs were independently checked by Sol.
This is a power saving for that error component only. The pursuit returned
`changed-under-evidence`; a full major-arc model with controlled errors and
the final convolution comparison remain unproved. No numerical onset or
additional Goldbach coverage follows from these prerequisites alone.

The major-arc pursuit uncovered and repaired a source-definition mismatch.
The literal squarefree-supported H_R of arXiv:2508.16400v2 vanishes at25,
while its Lemma4.11 kernel is at least2 there when R=2,r=1. The exact
identity Lambda_R,r(n)=Lambda_R,r(rad(n)) supplies the corrected majorant
H_R(rad(n)), with an implied constant depending on the smooth cutoff.
This local repair was independently checked; it is not a refutation of the
source's main theorem. No unproved mean estimate for the repair was imported.
The corrected majorant now supports a complete signed Heath--Brown Fourier
model for our normalized rough-semiprime weight. Its Fourier remainder is
O(Y*R^(-1/3)); the separate pointwise error is bounded by H_R(rad(n)) times
the checked character-mean accuracy. The proof handles endpoint strips and
takes the exceptional-zero alternative at level R^4. If its conductor is
larger than R^2, its model term is omitted but the exceptional error case is
retained. Sol checked the proof; `major_arc_kernel.py` and its focused tests
retain the result and source counterexample. The pursuit returned
`changed-under-evidence`. Replacement by a nonnegative rough-number model
and usable correlation bounds for the corrected majorant remain unproved.
The overall Goldbach coverage goal remains active.

The corrected-majorant pursuit closed its mean, second moment, and additive
correlation bounds. `radical_majorant_correlation.py` applies Henriot's New
Theorem 5 from the 2014 erratum, including its corrected zero-exponent
condition. For d=log(R)/log(Y), the central pair bound is
sum H_R(rad(n))*H_R(rad(m-n)) << Y*S_2(m)/d^2, uniformly in central even m.
The erratum's exact local factors give this square loss; the initially
considered sixth-power loss was unnecessary. The proof also bounds the
signed Fourier model's error pairings by e*(1+e)*Y*S_2(m)/d^2, where e is
the previously checked character-mean error. Its remaining Fourier pair
residual is at most Y/log(Y)^3 outside O(Y*R^(-1/2)) targets. Sol checked
the source application, norm bounds, convolution algebra, and exceptional
count. Four exact local-density tests passed normally and with Python -O.
The pursuit returned `changed-under-evidence`; no numerical onset, new
Goldbach coverage, or historical-priority claim follows. The remaining gap
is evaluation/comparison of the signed pair main terms with enough positive
margin, including control relative to any exceptionally suppressed term.
The overall Goldbach goal remains active; no wake was queued.

After Kevin flagged an interruption, the exact thread rollout and Git
history were checked. The last completed reviewed checkpoint is aca72fc;
the earlier bootstrap, almost-all theorem, and analytic prerequisites are
intact. The next root-derived candidate is in `signed_pair_main_term.py`.
It evaluates the signed pair main terms, derives a linear suppressed margin
for small exceptional conductors, and bounds an explicit large-conductor
gcd family by O(Y*R^(-1/8)). Six exact-arithmetic tests pass normally and
with Python -O, including active composite conductors and divisor-cover
overlaps. These are finite-algebra checks, not an analytic review.
The existing moment_bound_review handle initially reported pending_init
across repeated observations. It subsequently initialized and checked the
actual files, returning PASS for the coefficient identities, uniform tails,
linear suppressed margin, and large-conductor divisor bound. The result is
now promoted on that completed review, not on the earlier queued request.
No replacement reviewer or wake continuation was queued. Actual-prime
Fourier transfer and conversion to canonical L remain open. The next bounded
mathematical job is the prime-side Fourier transfer and the pair residual
relative to the now checked suppressed margin. The overall goal stays active;
the old native 9am wording remains superseded.

The prime-side transfer and dyadic composition are now proved and checked
by Sol in `prime_pair_transfer.py`. They give a power-saving exceptional
set for the ACTUAL canonical bound: for every sufficiently small fixed
delta>0, L(N)>0 for all but O_delta(X^(1-delta/8)) even N in [X,2X], for
sufficiently large X. The proof reuses the same R, character alternative,
and kernels on disjoint dyadic intervals, controls the pair residual
relative to the linear suppressed margin, and converts the weighted
comparison back to integer counts. Each canonical composite is already
a semiprime inside a single fixed larger semiprime set; the removed end
segments contain too few positions to erase the margin. Four finite tests
passed normally and with Python -O, including cross-interval pairs and
the direction of the weight conversion. The pursuit returned
`changed-under-evidence`. This improves the exceptional-set size for L>0;
it does not give the earlier half-main-term lower bound outside that smaller
set, eliminate all exceptional targets, supply a numerical exponent/onset,
or certify an uncomputed named interval. The next mathematical gap is
coverage or further arithmetic restriction of the remaining exception
family. No historical-priority search or wake queue was used. Overall
Goldbach coverage remains unresolved and the goal stays active.

The next bounded pursuit localized the small-conductor suppression.
For primitive quadratic D>24 let q be the product of p>=5 dividing D.
The finite model can have a vanishing margin only on F_D={B=0,C=-A},
an explicitly computed family contained in q|N and occupying at most24
residue classes modulo D. Outside it the model has a fixed positive margin;
inside it P=S=A*(1-u*v). Sol checked the lemma and its analytic transfer.
For the small-conductor case D<=R^(1/4), the actual canonical bound obeys
L(N)>>_delta Y/log(Y)^2 outside BOTH F_D and a separate
O_delta(Y*R^(-1/2)) Fourier-residual set. Inside F_D the previous suppressed
error count can also be capped by the exact arithmetic family's size.
`character_suppression.py` preserves the proof and exact residue/count
verifier; four focused tests passed normally and with Python -O.
The pursuit returned `changed-under-evidence`: it localizes one source
of suppression, while unstructured Fourier exceptions and the separate
large-conductor case remain. No universal coverage, named uncomputed target,
numerical onset, or historical-priority claim follows. No wake was queued;
the overall Goldbach goal remains active.

The monotone-cutoff pursuit removed the coarse large-conductor gcd cover.
Choose the already allowed smooth G additionally nonincreasing on its
positive argument, with 0<=G<=1. `monotone_euler_cutoff.py` proves
0<=U_D<=(5/2)*S_out uniformly, using positive/negative prime-factor
separation and elementary Euler-product bounds. This transfers the exact
family F_D to ALL active exceptional conductors: outside F_D and a separate
O_delta(Y*R^(-1/2)) Fourier-residual set, L(N)>>_delta Y/log(Y)^2.
The resulting total exceptional-size bound for L>0 is now
O_delta(X^(1-delta/4)); the earlier half-main-term guarantee is unchanged.
Sol checked the proof. Four focused tests passed normally and with Python
-O; an initial test normalization omitted a directly enumerated character
sign B=-1, and was corrected without changing the negative-cutoff witness.
The pursuit returned `changed-under-evidence`. The remaining gap is control
of the Fourier residual and the exact suppressed classes, not the discarded
coarse gcd cover. No numerical onset, universal coverage, publication work,
historical-priority search, or wake queue was introduced. Overall goal active.

The next pursuit tested the Fourier-only gap rather than increasing a range.
`reflection_fourier_gap.py` proves a new concentration statement for the
existing artificial reflection model: its centered Fourier supremum is
O(sqrt(H*log H)) with high probability. After prime-density scaling and
forcing a truthful prefix through B, the error is
O(sqrt(H)*log(H)^(3/2)+B*log H), yet the center remains missing while
every other central even sum is represented. The same retained-core event
allows every prescribed prefix simultaneously. This fixed-wheel baseline
permits prefix exceptions for primes dividing the wheel; it does not impose
full primality, a growing sieve, or the actual prime/semiprime dependency.
Sol checked the proof, including the whole-circle grid argument and matching.
Four tiny Fourier/moment tests passed normally and with Python -O; the old
frozen model run was not repeated. The pursuit returned
`changed-under-evidence`: norm/energy estimates of this quality alone cannot
force an isolated hole to spread or prove universal coverage. The actual
almost-all theorems remain intact. The next mathematical gap is direct
arithmetic control of the combined actual prime/composite pair residual,
including its behavior on the suppressed classes. No Goldbach counterexample,
historical-priority claim, publication work, or wake queue. Overall goal active.

The actual-survivor pursuit retained an exact signed identity and rejected
its first plug-in estimate. With A=P+C and Liouville lambda,
P-C=-lambda*A, including prime squares, and L=[(P-C)*A]+d_C=2[P*A]-[A*A]+d_C.
`factored_linear_barrier.py` tests the standard one-dimensional lower
linear sieve in this identity. Even granting the optimistic leading upper
bound [A*A]<=((1+log(u-1))^2+o(1))*K, its best limiting coefficient for
2<=u<=3 is -(1-log(u-1))^2< -121/1296. At u=3 it is -(1-log2)^2.
The source only applies at theta<1; theta=1 is a coefficient limit, not a
new distribution theorem. This is a failure of that specific certificate,
not an upper bound on actual L or an impossibility result for all sieves.
Sol checked the identity, normalization, and conditional boundary. Four
focused tests passed normally and with Python -O, with exact rational
logarithm enclosures and selected actual prime-square/diagonal controls.
The pursuit returned `changed-under-evidence`: keep the factorization for
coupled correlation or switching work; do not repeat the direct plug-in
without new arithmetic input. Actual Goldbach coverage remains unresolved.
No range extension, historical-priority search, publication work, or wake queue.

The next bounded pursuit connected the exact suppressed classes to an
existing pointwise theorem. `exceptional_pointwise_bridge.py` applies
Matomaki--Merikoski, IMRN2023, Theorem1.4: its leading coefficient is
exactly 1+C_D(N)/A_D(N), vanishes precisely on our F_D, and is at least2/3
elsewhere. For each fixed alpha in (0,1), assuming a primitive quadratic
zero beta=1-1/(eta*log D), D>24 and eta sufficiently large, EVERY even N
outside F_D in max(D^10,N0)..D^(eta^(1-alpha)) has actual
G(N)>=S_2(N)*N/(4*log(N)^2). No additional Fourier-residual exception is
needed in this conditional branch. Prime-power removal and the two
independent size thresholds are checked; no numerical onset is supplied.
Every power of two in that range is included. F_D is empty exactly for
the allowed conductors D=1 or5 mod12, giving whole conditional intervals.
Sol checked the deduction and implementation; four focused tests passed
normally and with Python -O. The pursuit returned `changed-under-evidence`:
this source-backed conditional branch bypasses a Fourier residual for G,
but neither proves the zero assumption nor improves canonical L on its
exceptions. The suppressed classes, absent/insufficient-zero case, and
out-of-range targets remain open. The source supplies the analytic theorem;
no historical novelty, unconditional coverage, publication work, or wake queue.
Overall Goldbach coverage remains unresolved and the goal stays active.

The next bounded pursuit checked whether that conditional branch can stack.
Landau--Page, in Michel's primary lecture source printed p21, implies that
distinct sufficiently strong primitive real zeros satisfy
log(D2)/log(D1)>c*eta1, for a fixed c below its positive absolute constant.
Consequently the next interval starts after the square of the previous
upper endpoint when 10*c*eta1^alpha>=2. A family above one sufficiently
large fixed strength threshold cannot cover all large evens by these
intervals alone, even if every suppressed residue family is empty.
`exceptional_pointwise_bridge.py` retains the proof and exact rational
separation check. Sol reviewed both; seven focused tests passed normally
and with Python -O. The review clarified that v=o(eta) suffices for the
geometric gap, while making the source error envelope tend to zero needs
the stronger v*log(eta)^6/eta=o(1). The pursuit returned
`changed-under-evidence`: individual conditional intervals remain usable,
but this strong-zero family cannot supply the desired global stacking.
These are certificate gaps, not Goldbach failures; weaker zeros and other
analytic regimes are not excluded. No numerical Landau--Page constant,
actual zero, historical novelty, publication work, or wake queue was added.
The overall goal remains active; other arithmetic coverage is still needed.

The next coupled-correlation pursuit tested a precise finite prerequisite.
`coupled_product_model.py` forces the second residue weight to be the exact
multiplicative convolution of the first with itself. For a half-support
whose prime-pair correlation at0 vanishes, the product-pair mean is at
least1/2 when the cyclic group order is divisible by4. When its order is
2 mod4, that mean is zero exactly at the two parity cosets; a quantitative
lower bound controls distance to these cosets. In prime residue fields,
these are the odd quadratic-residue/nonresidue cases. Thus product coupling
and bounded density alone still permit a negative signed comparison.
The m4 and m6 sharp examples, 510 exhaustive tiny subsets, and independent
finite-field product checks passed normally and with Python -O. Sol reviewed
the proof and implementation. The pursuit returned `changed-under-evidence`:
quadratic-character behavior is special, and a general product-coupling
argument requires more arithmetic input. This artificial model does not
impose actual integer factor windows, unique semiprime counting, a truthful
prime prefix, or the source prime-distribution estimates. It neither refutes
canonical L nor gives Goldbach counterexamples or new actual coverage.
No historical-priority search, publication work, or wake queue. Overall goal
active; actual coupled estimates remain the missing step.

The next pursuit proved a robust positive inverse statement in that model.
For any two possibly different cyclic densities f1,f2 in[0,2] with mean1,
the product distribution g=f1*f2 has reflected pair mean at least1/2
when4 divides the group order. Otherwise, a pair mean <=E0<1/2 forces
both factors within L1 distance 1-sqrt(1-E0)<=E0 of their respective odd
quadratic coset densities; neither a binary nor a missing-prime-sum premise
is needed. The inverse distance bound is sharp. If a bounded observed
weight w approximates g in L1 by epsilon, the same conclusion holds with
E0=pair_mean(w)+4*epsilon. `coupled_product_model.py` retains the proof and
general rational verifier. Sol checked both; eight tests passed normally
and with Python -O, including asymmetric/non-skew inputs and explicit
cap/error-budget falsifiers. The pursuit returned `changed-under-evidence`:
the quadratic structure test survives approximation, but applying it to
actual primes requires proving the density cap and a sufficiently small
product-distribution error at a relevant scale. Those arithmetic inputs
remain unproved; no new actual Goldbach coverage, historical-priority
search, publication work, or wake queue. Overall goal remains active.

The next pursuit checked the scale needed to apply that product model.
For prime ell>=7 and two unit-group densities in[0,2] with mean1, their
normalized multiplicative convolution g has additive pair mean at every
nonzero target at least (ell-4-sqrt(ell))/(ell-1)>0. The proof uses the
standard Jacobi-sum identities and the factor Fourier mass bound. However,
at the sufficient no-alias scale ell>2H, uniform atoms on earlier cofactor
primes<=H/(z+1) have mean L1 distance at least2z/(z+1)>=4/3 from EVERY
mean1 density capped at2. Thus the direct single-modulus application fails
its density premise before integer product windows need consideration.
`product_resolution.py` retains both deductions and exact rational checks.
Sol checked the mathematics and implementation; five focused tests passed
normally and with Python -O. The pursuit returned `changed-under-evidence`:
nonzero residue coverage is positive in the model, but that alone cannot
identify one exact integer sum. The sufficient no-alias modulus is not
claimed necessary; joint moduli, proved smoothing transfers, and certified
alias exclusion remain separate questions. No new actual Goldbach coverage,
historical-priority search, publication work, or wake queue. Overall goal
active; the arithmetic transfer to individual targets remains unresolved.

The next bounded pursuit checked multiple-modulus assembly and returned
`changed-under-evidence`. `joint_residue_model.py` gives an exact family
D=3Q where every proper-divisor joint projection is uniform and its pair
mean positive, yet the full product-pair mean is zero. Under those exact
projection and cap2 premises, a small full mean forces both factors close
to the full quadratic-character cosets; local projections erase that mode.
The construction uses nonunit targets and is not a coprime-target no-go.
For squarefree D with least prime p0>=7, ANY global cap2 mean1 factors
have positive product-pair mean at every unit target, bounded below by
theta*(p0-4-sqrt(p0))/(p0-2), theta=prod(p-2)/phi(D). This complementary
theorem needs no proper-projection uniformity. However, at the sufficient
no-alias scale D>2H, cubic-prefix prime atoms have distance from EVERY
global mean1 cap2 density greater than2*(1-2^(1/4)*H^(-1/12)), tending to2.
The elementary phi(D)>=D^(3/4) bound makes this valid even with many prime
moduli. Thus this direct atomic implementation still fails its required
global input; smaller marginal density bounds do not supply it. Sol checked
the deductions and implementation; seven focused tests passed normally
and with Python -O, including exact radical bounds, sharp inverse cases,
nonuniform composite marginals, and a lower-conductor premise falsifier.
The first test run caught and corrected floating division in test-side
coefficient arithmetic; the mathematical statement needed no correction.
The pursuit closed within30 minutes. No new actual Goldbach coverage,
historical-priority search, publication work, or wake queue. Overall goal
active; arithmetic control of joint dependence or another rigorously
justified transfer is still needed for individual unresolved targets.

The next arithmetic pursuit returned `changed-under-evidence` for the
unweighted cubic switching proposal. `switched_cubic_barrier.py` retains
the exact identity G=T-U, T=[P*A], U=[P*C], and separates distinct-factor
and prime-square contributions. This route needs no upper grant for M.
Using the primary switching formulas with the required distribution and
natural-mass hypotheses explicitly granted, the lower term has coefficient
B(theta1)<2log2 for every fixed theta1<1. The switched upper subtraction
has coefficient2*integral d alpha/[alpha*(1-alpha)*theta2(alpha)]>=2log2
on1/3..1/2 when theta2<=1. Thus this particular lower certificate cannot
give a positive leading term. At the formal two-level1 limit its coefficient
is exactly0; the source does not assert that endpoint or determine the
lower-order sign. Sol confirmed the normalization and emphasized charging
cutoff/factor-dividing-N exceptions O(N/z), separately from O(z) and
O(sqrt(N)) terms. The verifier preserves these finite terms. Four focused
tests passed normally and with Python -O; Sol reviewed the implementation.
The distribution grants remain grants, including after sequence removals;
position-error bounds do not prove weighted remainder estimates. No actual
negative G or L, no exclusion of other weights or coupled switching, and
no new Goldbach coverage follows. The pursuit closed within30 minutes;
no historical-priority search, publication work, or wake queue. Overall
goal active; a stronger joint arithmetic estimate is still needed.

The weighted cubic follow-up also returned `changed-under-evidence`.
For every fixed Lipschitz profile 0<=w<=1 supported in[1/3,b], b<=1/2,
the source-form additive distinct-prime-divisor weights have certificate
coefficient B_w-C_w<=B0(theta1)-2log2<0 for fixed theta1<1 under the same
explicit distribution/mass grants. At the formal two-level1 limit the
entire weight functional cancels exactly. This excludes positive leading
certificates only for this stated family and these sieve estimates; weights
can improve a weaker certificate at lower switched levels while it remains
negative. The inequality is uniform in profiles; analytic o(K) is only
claimed for each fixed Lipschitz profile with its granted remainders.
`switched_cubic_barrier.py` retains the deduction, rational piecewise-linear
integral enclosures, and the exact finite weighted certificate J_W<=G.
Its losses count small prime terms and negative composite weights; a prime
square's divisor counts once. Sol checked the deduction and actual verifier;
eight combined focused tests passed normally and with Python -O. This
pursuit closed within30 minutes. No new actual Goldbach coverage, numerical onset,
historical-priority search, publication work, or wake queue. Overall goal
active; these separate weighted estimates do not close the pointwise gap.

The next pursuit strengthened the ACTUAL canonical-L exceptional-set theorem.
Keeping the same sufficiently small fixed delta>0, every fixed 0<k<2/3
now gives #{even m in[X,2X]: L(m)<=0}=O_{delta,k}(X^(1-delta*k)).
For example k=1/2 replaces delta/4 by delta/2 for the same delta.
The additional established input is Siegel's ineffective zero-distance
bound, stated in Matomaki--Merikoski equation(6). The deduction is in
`monotone_euler_cutoff.py`: enlarge the full-Euler comparison range to
D<=R^a, a=1/3+k/2, retain the suppressed margin mu>>R^(-tau),
tau=1/6-k/4, and use the unsimplified Fourier energy. Both the small-D
Fourier residual and large-D arithmetic family cost O(YR^(-a)*log(Y)^2),
which is smaller than O(YR^(-k)) for each fixed k. This is unconditional
asymptotically but has ineffective constants and onset. It neither assumes
an actual exceptional zero exists nor uses the separate conditional
pointwise Goldbach theorem. No k=2/3 endpoint, numerical delta/onset,
half-main-term strengthening, or empty exceptional set is proved. Sol
checked the analytic deduction and actual proof text. The bounded pursuit
closed within30 minutes. No executable implementation changed;
syntax checks and four exact rational exponent controls also passed.
No new prime-range scan, historical-priority search, publication work,
or wake queue. Overall goal active; individual exceptional targets remain
the unresolved step.

The next finite pursuit implemented the existing square-root support
identity with the parity bootstrap in `support_exact_batch.py`. A fixed
z=708 for the SAME1000 evens1002000..1003998 leaves2042 composites, all
above half the last target, so G=[A*A]-2[A*C] is exact throughout the band.
Only canonical earlier bounds through2830 are needed, classifying odd
prime inputs through1415, instead of the prior20000-prefix cubic run.
Binary reflected-intersection counts replace wide packed multiplication;
the production route uses neither exact-count input nor a high prime square.
A,C still encode full primality information through earlier-factor arithmetic.
Every one of the1000 counts matched an independent ordinary-sieve/packed
prime-square control. Minimum ordered G is7925 at1002002 (M8399,AC237);
there were no zero targets. Complete production time was0.1106447s,
including0.0027641s input generation; independent full-square validation
was2.1423617s. The same-block ordinary-sieve/bitset reference was faster
at0.0559214s, so no superiority over that baseline is claimed. Four focused
tests passed normally and with Python -O, including complete small exact
counts, exhaustive small binary correlations, negative parity inputs,
diagonals, strict support boundaries and unsafe ranges. Sol checked the
mechanism, implementation and evidence. The pursuit closed within30 minutes.
`evidence/support-exact-batch.json` retains the exact counts for
future same-block comparisons. The gap between2830 and1002000 was not
computed; these separated outputs are not a contiguous count prefix.
No new support theorem, universal positivity, historical-priority search,
publication work, or wake queue. Overall research active; this improves
the finite checker, while the universal exceptional-target gap remains.

The next pursuit specified a composite-supported joint arithmetic target in
`composite_bilinear_bridge.py`. For N=2x and I=(x/2,x], compare Lambda(N-n)
with normalized roughness through exp(sqrt(log x)). Established BV and the
fundamental lemma give the stated averaged Type I estimate and the correct
singular-series prime-versus-rough main term, with uniform local factors,
nonreduced progressions, short-interval remainders and prime powers charged.
An explicitly UNPROVED Type II estimate for all divisor-bounded coefficients
in the stated factor range would then imply positive actual Goldbach counts
for every sufficiently large even N. A direct Vaughan decomposition reduces
the sufficient missing estimate further to one fixed-coefficient composite
correlation J_N=o(x); its definition and signs are retained in the verifier.
This is a precise reformulation of the remaining pointwise correlation, not
evidence that it is easier or has been proved. Sol checked the deduction and
actual files. Four focused exact-rational tests passed normally and with
Python -O, verifying the decomposition, prime-power retention, local residue
normalization and input boundaries; they do not prove an analytic estimate.
The pursuit returned `changed-under-evidence` within30 minutes. No new
Goldbach coverage, numerical onset, historical-priority search, publication
work or wake queue. Overall goal remains active; J_N=o(x) is unresolved.

The next pursuit audited that uncorrected J_N target and returned
`changed-under-evidence`. If primitive quadratic conductors D tend to
infinity with actual real-zero strengths eta tending to infinity, choose
N as the least multiple of2D at least D^12. The localized proof of
Matomaki--Merikoski, Sections2 and7, gives the same interval's pair mass
(b_D(N)/4+o(1))*S_2(N)*N. The source's varying smoothing family and its
transition-strip error are accounted for explicitly. Since b_D=1+chi(-1),
our existing TI/MAIN/Vaughan relation forces
J_N/(S_2(N)*N)=chi(-1)/4+o(1). Thus the universal uncorrected cancellation
target would also exclude every such hypothetical strong-zero sequence,
including characters with an empty suppression family. No actual zero or
failure of Goldbach is asserted. The deduction, exact residue witness and
six focused tests are in `composite_bilinear_bridge.py` and its test file;
tests passed normally and with Python -O, and Sol checked both mathematics
and actual files. The pursuit closed within30 minutes. The sufficient
implication remains valid, but the next pointwise approach must retain the
character contribution and bound the remaining error against a proved
positive margin. The corrected leading term alone still gives no positivity
on the suppression family. No new coverage, numerical onset, priority search,
publication work or wake queue. Overall research remains active.

The next pursuit returned `changed-under-evidence` with two linked results
in `periodic_character_comparison.py`. For a sufficiently small fixed rho,
an even modulus Q with exp(sqrt(logN))<=Q<=N^rho, and an actual exceptional
character D>24 dividing Q, the nonnegative comparison
b(t)=(Q/phiQ)*1_(t,Q)=1*(1-chi(t)*t^(beta-1)) has prime-versus-model mass
>>K*N*min(1,(1-beta)logN) on N/4<n<=N/2. Here K=Q*A/phiQ^2 and A is
the allowed residue count. Direct character expansion and Gallagher's
averaged estimate preserve the positive margin even in suppressed classes.
This is not a prime-versus-prime lower bound; the comparison includes composites.
However, ANY bounded mean-one Q-periodic model, also allowing a bounded
mean-zero periodic character correction times t^(beta-1), has Type I error
>>N/(logN*loglogN) when Q<=N^rho, rho<1, and amplitudes are N^o(1).
Primes near logN outside the factors of NQ give an exact density defect;
PNT counts enough such primes and summed BV controls actual progressions.
Thus the old Type I premise fails already at its A=2 saving for this model.
The earlier much larger primorial comparison is outside this obstruction.
Sol checked both deductions and the actual helpers/tests; four focused
tests passed normally and with Python -O. The pursuit closed within30 minutes.
No new coverage, actual zero detection, numerical onset, priority search,
publication work or wake queue. A useful next approach must retain the
character margin while repairing the arithmetic-distribution compatibility,
or control the specific signed decomposition without that absolute Type I
premise. Overall research remains active.

The next pursuit tested weighted pooling of the small wheel models and
returned `changed-under-evidence`. `wheel_mixture_obstruction.py` proves
that ANY finite mixture of normalized unit wheels Q_i<=N^sigma, sigma<1,
with real coefficients summing to1 and total variation<=C0*(logN)^B,
still has absolute Type I error >>N/((logN)^(B+1)*loglogN). There is no
bound on the component count or their combined least common multiple.
The statement also allows a common primitive character correction, with
one necessary prime-conductor exclusion handled explicitly. Weighted prime
coverage and a nonnegative test align the signed defects; negative mixture
coefficients are not treated as positive. Convex and bounded-variation
signed mixtures fail already at the A=2 saving. Positive model margins
are preserved only for nonnegative mixtures under the earlier common
actual-zero premises. Sol checked the proof and actual helpers; four focused
tests passed normally and with Python -O, including joint-period counts,
negative coefficients, repeated prime powers and the character exclusion.
The pursuit closed within30 minutes. Thus arbitrarily many easy models
of this stated kind do not repair the distribution mismatch. Specific
signed Vaughan cancellation, different residue weights or larger individual
models remain distinct possibilities. No new actual coverage, zero detection,
numerical onset, priority search, publication work or wake queue. Overall
research remains active; the exact earlier-output parity mechanism is intact.

The next pursuit returned `changed-under-evidence` with a constructive
two-scale signed comparison in `ramanujan_type_i.py`. Let S=Y^delta and
R=S^12, with sufficiently small fixed delta. For the common exceptional
alternative at level R^4, the unexceptional branch and the branch with an
actual primitive exceptional conductor 24<D<=S^(1/4) now have both:
an absolute Type I error O_A(Y/log(Y)^A) for every fixed A, and a pointwise
positive prime-versus-coarse-model mass >>Y*S_2(m)*mu throughout the stated
central band. Here mu=1 without an exceptional zero and
mu=min(1,(1-beta)log(Y)) otherwise. The Ramanujan progression means reproduce
the full reduced-residue density; the exceptional resonances are sparse
enough for the absolute estimate by ineffective Siegel bounds. Separating
the two scales bounds the fine Fourier residual against the coarse model
and preserves its linear character margin. The model is signed and includes
composites. The Type I error is not proved small relative to arbitrarily
suppressed mu, and neither a Type II bound nor actual prime-pair positivity
follows. Other exceptional-conductor regimes are outside this result.
Sol checked the theory and actual files, correcting one displayed scale
dependence to 1-beta<=kappa/(48*delta*log(Y)). Six focused tests passed
normally and with Python -O: complete progression periods, nonreduced and
prime-power moduli, whole-Dq character resonance, all four mixed-kernel
correlations, unequal cutoffs and input boundaries. These finite tests
verify algebra, not analytic estimates. The pursuit closed within30 minutes.
No new Goldbach coverage, numerical onset, zero detection, priority search,
publication work or wake queue. Overall research remains active; this repairs
two comparison prerequisites while retaining the precise transfer gap.

The next pursuit closed the character-relative Type I gap in the SAME
two-scale conductor regime. `relative_type_i.py` proves the stronger error
O_A(Y*mu/log(Y)^A) for every fixed A, with one sufficiently small fixed
delta chosen independently of A and an ineffective onset. Moderate mu uses
the earlier absolute estimate with a larger saving. For smaller mu,
quantitative Linnik estimates retain the zero-repulsion log(1/e) gain;
lifting small-conductor characters to lcm(D,r) removes the exceptional main
term without a totient loss. The Drappeau--Fiorilli high-conductor mean
estimate controls the complementary characters. Siegel bounds make the
model tails, periods, resonances and proper prime powers harmless relative
to mu. Sol checked the source use, proof and actual files. Four focused
exact tests passed normally and with Python -O, including a complex quartic
character control and the boundary where the exceptional projection survives.
The pursuit returned `changed-under-evidence` within30 minutes. Thus the
positive comparison mass and distribution error now share the required
scale in these branches. Type II and the specific signed prime-weighted
residual remain unproved; other exceptional-conductor regimes are still
outside this theorem. No new actual Goldbach coverage, numerical onset,
zero detection, priority search, publication work or wake queue. Overall
research remains active.

The next pursuit proved a conditional rare-sign candidate-pool theorem in
`rare_prime_sieve.py`. On the exact suppression classes F_D, allowed unit
pairs always have opposite character signs, and A/phi(D) is1 or1/2. Under
the stronger actual-zero condition 0<t=(1-beta)log(Y)<=1/log(Y), with
D<=Y^(delta/4), every central suppressed target has >>_delta Y*t/log(Y)^2
primes of sign+ whose reflected partners are coprime to D and have no prime
factor at most ceil(Y^(delta/u)), for sufficiently small fixed delta and
large fixed integer u. Quantitative Linnik progression errors, normalized
CRT counts and Ford's fundamental lemma keep the entire sieve remainder
small relative to the rare-prime population. Integer rounding and prime
powers are charged. The partners have fewer than u/delta prime factors
WITH MULTIPLICITY; they are not proved prime or P_2. Sol checked the theory
and actual files. Five exact tests passed normally and with Python -O.
A finite guard, D31,m2790,p1459,m-p=11^3, shows why the sign and roughness
conditions alone do not force primality; it asserts no exceptional zero.
For sign- composites, even total factor multiplicity requires a sign+
factor, whereas odd multiplicity can use only sign- factors. The remaining
question is control of composite partners within the proved candidate pool.
The pursuit returned `changed-under-evidence` within30 minutes. No actual
zero, numerical onset, new Goldbach coverage, priority search, publication
work or wake queue. Overall research remains active.

The rare-factor pruning pursuit in `rare_factor_pruning.py` keeps the SAME
conditional rare-prime pool and its conductor/zero hypotheses. With
w=floor(sqrt(E)), candidates whose partner has a sign+ prime factor
z<q<=w occupy only an o(1) fraction of that pool. An upper sieve on q|m-p
uses each all-squarefree remainder index qd at most once. Matomaki--Merikoski
Lemma2.2 bounds the reciprocal rare-prime sum by
O_(delta,u)(eta^(-2/u)+t+1/z)=o(1), preserving >>Y*t/log(Y)^2 candidates.
This is not an O(t) relative-loss claim. Even-factor composites with a
sign+ factor>w and odd-factor composites made entirely of sign- primes
remain uncontrolled. Sol checked the theory and actual files; five focused
exact tests passed normally and with Python -O. The pursuit returned
`changed-under-evidence` within30 minutes. No actual zero, numerical onset,
prime-partner theorem, new Goldbach coverage, priority search, publication
work or wake queue. Overall research remains active.

The next pursuit returned `changed-under-evidence`: the large-factor
cofactor switch still leaves an uncontrolled two-prime correlation, but
`character_partner_weight.py` gives a precise weighted reduction using the
standard W=chi*log. On a negative-sign squarefree partner, W is zero unless
there is exactly one negative prime r; then W=2^omega_+*log(r). On the SAME
pruned pool, its weighted sum T equals the positive-first actual prime-pair
mass P plus a nonnegative large-positive-factor squarefree term and a
nonnegative repeated-factor term. The latter is at most
Y^(1-delta/u+o(1))=o_A(Y*t/log(Y)^A) for every fixed A under the existing
hypotheses. This removes pure negative-sign odd composites from the weighted
equation, without claiming that they leave the candidate pool. A positive
lower bound for T AND control of the large-factor term remain unproved;
the known candidate count does not imply positivity of this new weight.
Sol checked theory and actual files; five symbolic algebra tests passed
normally and with Python -O. The pursuit closed within30 minutes. No new
Goldbach coverage, actual zero, numerical onset, priority search, publication
work or wake queue. Overall research remains active.

The next pursuit closed the h>=2 part of that squarefree composite error.
`multi_rare_partner.py` proves E_2plus<<_(delta,u)Y*S_2(m)*t^2=o(Y*t),
with ALL prior hypotheses unchanged. The existing cutoff w gives an
O(t) reciprocal sum of positive-sign primes above w. Henriot's corrected
New Theorem5 bounds the two affine prime conditions uniformly after fixing
the product M of positive factors, including primes dividing its leading
coefficient. The squarefree Euler tail of degree at least2 is O(t^2).
Consequently T=P+E_1+E_rem, with E_rem>=0 and E_rem=o(Y*t). The remaining
E_1 consists exactly of semiprime partners r*q, with r a negative-sign
prime and q a positive-sign prime>w, weighted by 2*log(p)*log(r).
This does not establish positivity of T or make E_1 negligible. Sol checked
the proof and actual files; five focused exact tests passed normally and
with Python -O. The finite cofactor control used target17,918 inside the
already certified prefix, adding no new coverage. The pursuit returned
`changed-under-evidence` within30 minutes. No actual zero, numerical onset,
priority search, publication work or wake queue. Overall research remains active.

The rare-sign distribution pursuit in `rare_twisted_bv.py` returned
`changed-under-evidence` within30 minutes. In the SAME actual-zero regime,
with delta sufficiently small for this fixed saving, it proves a relative
twisted Bombieri--Vinogradov error O(Y*t/log(Y)^6) through
Q=floor(Y^(9/20)/D^3). A three-way conductor split combines quantitative
Linnik, the aggregate corrected Gallagher estimate, and the induced-character
mean bound; transformed-principal resonance is explicitly charged. Using
the same injective sieve-remainder accounting raises the removable positive
factor cutoff to w*=floor(sqrt(floor(Q/3))). Its semiprime contribution is
O(Y*S_2(m)*t^2+Y*t/log(Y)^5)=o(Y*t). Consequently the SAME weighted total
now satisfies T=P+E_1(q>w*)+o(Y*t), with nonnegative discarded error.
Both positivity of T and control of the remaining large-q semiprimes remain
unproved. Sol checked theory and actual files; five focused exact tests
passed normally and with Python -O. No actual zero, numerical onset, new
Goldbach coverage, priority search, publication work or wake queue.
Overall research remains active.

The next pursuit tested a cofactor switch, then changed the partner weight
in `cubic_character_minorant.py`. Put U=chi*log^3 and
K(n)=10W(n)-9U(n)/log(n)^2. The finite-difference identity
U=(1*chi)*(mu*log^3)>=0 proves K<=10W; K equals log(n) on negative-sign
primes. For a mixed-sign squarefree semiprime n=rq, with r negative and
q positive, its exact numerator is
log(n)^2*K(n)=log(r)*(2log(r)-log(q))*(log(r)+7log(q)).
Thus every q>r^2 contribution is negative and may be dropped in an upper
bound for the NEW signed total T_K. Prior negligible-error estimates transfer
with a factor10, yielding T_K<=P+E_mid+o(Y*t), where the remaining positive
semiprimes satisfy w*<q<r^2, hence r>n^(1/3). This does not lower-bound T_K
by the old nonnegative total T. Showing T_K exceeds E_mid and the error is
still open. Sol checked theory and actual files; five exact tests passed
normally and with Python -O, including an independent nonnegative convolution,
negative weights and the one-sided partition at existing-prefix targets.
The pursuit returned `changed-under-evidence` within30 minutes. No actual
zero, numerical onset, new Goldbach coverage, priority search, publication
work or wake queue. Overall research remains active.

The higher-logarithm pursuit returned a checked obstruction in
`log_weight_barrier.py`. For any prime-normalized kernel f, its mixed-sign
semiprime multiplier is H(a)=1+f(1-a)-f(a), so H(a)+H(1-a)=2. Its integral
over every symmetric share interval is fixed, and its positive-part integral
cannot be smaller. The cubic kernel's uniform-share positive mass is10/9,
versus1 for W; this is a formal comparison, not actual prime density.
Moreover finite nonnegative subtractions of higher chi*log^j weights cannot
decrease the q<=r semiprime contribution. Higher degree alone therefore
does not remove the remaining range by this pointwise route. Arbitrary
polynomial coefficients also have an explicit derivative-norm cost near
balanced factors. Sol checked theory and actual files; five focused exact
tests passed normally and with Python -O. The prior cubic identity remains
valid; signed-total positivity and the actual composite correlation stay open.

The same pursuit found Tao's acknowledged Proposition23 proof gap in the
previous quantitative Linnik exposition. The required estimate was rederived
from Thorner--Zaman Theorem2.1 and equation(4.2), using height q^2, an
integer-zero-count cutoff, and endpoint subtraction to cancel low-zero
constants. `relative_type_i.py` owns the checked replacement deduction;
the rare-prime sieve and twisted distribution proof now point to it. This
preserves the required t-power errors and normalized L^2/D error after a
sufficiently small fixed delta choice. Sol checked the repair; no executable
change or repeated old experiment was needed. The pursuit closed within30
minutes, with no actual zero, numerical onset, new Goldbach coverage,
priority search, publication work or wake queue. Overall research remains active.

The next pursuit combined relative distribution with the tunable cubic
weight in `balanced_semiprime_budget.py`. For each fixed0<epsilon<=1/100,
choose delta sufficiently small DEPENDING on epsilon and kappa=1/epsilon.
In the same actual-zero regime and on the original pruned pool at those
parameters, the new signed total satisfies
P>=T_kappa-C*epsilon*Y*S_2(m)*t-o_epsilon(Y*t), with C absolute.
The relative distribution proof extends to Q=Y^(1/2-epsilon)/D^3;
injective sieve support handles positive factors through Y^(1/2-2epsilon),
without requiring q<=sqrt(level). The cubic weight makes larger factors
nonpositive beyond Y^(1/2+2epsilon). Its positive multiplier is at most3
on the remaining band, whose actual reciprocal rare-prime mass is
2epsilon*t+o(t/loglog(Y)). An auxiliary fixed cutoff Y^(1/10) in Henriot's
corrected theorem makes the two-prime upper-bound constant absolute.
Thus the positive composite loss is an arbitrarily small FIXED fraction
of the prime-pair scale. This is not a little-o bound for one fixed epsilon,
a same-delta or growing-kappa theorem, or a positive lower bound for T_kappa.
That signed-total lower bound remains the required gap. Sol checked theory
and actual files; four focused exact tests passed normally and with Python
-O. The pursuit returned `changed-under-evidence` within30 minutes. No
actual zero, numerical onset, new Goldbach coverage, priority search,
publication work or wake queue. Overall research remains active.

The positivity pursuit found a checked obstruction in
`cubic_positivity_obstruction.py`. Pairing complementary divisors gives the
exact cubic hyperbola kernel h(x)=(1-2x)*(1+kappa*x*(1-x)). Let T_low
retain only divisors d<=Y^(1/2-2epsilon) in the SAME T_kappa. At fixed
epsilon and sufficiently small delta, then sufficiently large fixed u,
the actual-zero hypotheses imply T_low<=-(kappa/32)*Y*S_2(m)*t.
The signed sieve expansion uses unique rough/smooth factorization of its
remainder indices. Actual character rarity reduces its divisor MAIN to
a Mobius simplex limit, the Dickman function. Its exact first three
moments give the normalized coefficient (2-kappa)/2 as theta=delta/u
decreases. Choosing u first makes the fixed sieve error sufficiently
small; Y then grows. No growing-u or growing-kappa theorem is asserted.
This is a negative estimate ONLY for T_low, not the full signed total.
Its complementary divisor range must supply a substantial positive term
for this weight to prove positivity; treating that range as negligible
would make the route fail. The earlier composite-error inequality remains
valid. Sol checked theory and actual files; five exact tests passed
normally and with Python -O, including rational Dickman tail enclosures,
both boundary signs, and complete finite divisor/support controls. The
pursuit returned `changed-under-evidence` within30 minutes. No new actual
Goldbach coverage, zero, numerical onset, priority search, publication
work or wake queue. Overall research remains active.

The next weight-redesign pursuit returned a broader checked tradeoff in
`log_weight_barrier.py`. A fixed polynomial f has accessible endpoint-main
coefficient A_f=(f'(0)+f'(1))/2, with the precise order: choose u large
for a requested tolerance, then Y sufficiently large. For the safe
nonnegative logarithmic-subtraction family, put B=sum(j-2)c_j. Then
A_f=1-B/2 and H_f(a)>=(1-a)*(2-B*a*(2a-1)) for1/2<a<1.
Making H_f(a)<=0 requires B>=2/(a*(2a-1))>2, so the accessible main
turns negative. Cubic and quartic penalties attain this bound; higher
degree cannot improve suppression per main-term cost within this family.
A separate formal derivative argument shows that positive A_f and any
semiprime sign deletion force positive all-negative triple weight somewhere
in the open logarithmic-share simplex. It asserts no actual triple count.
The explicit alternative f(s)=s-100s^2(1-s)^2(1-2s) has A_f=1 and
H_f(3/4)=-193/64, but triple weight7263/15625 at shares(9/10,1/25,3/50).
This preserves a candidate component while exposing the new composite
error that prevents reuse of the old pointwise bound. Neither changing
degree nor changing signs alone has closed the prime correlation gap.
Sol checked theory and actual files; nine exact tests passed normally
and with Python -O, including sharp costs and an independent eight-divisor
triple expansion. The pursuit closed within30 minutes, with no new actual
coverage, zero, numerical onset, priority search, publication work or wake
queue. Overall research remains active.

The next pursuit controlled part of the alternative's new error in
`quintic_partner_weight.py`. For ANY fixed polynomial, its rough-partner
weight is bounded by C_f,theta*log(Y), so repeated factors, two or more
positive-sign factors, and positive factors w<q<=Y^(1/2-2epsilon) can
be discarded absolutely with o(Y*t) cost using the existing estimates.
For the alternative quintic, seven or more negative factors give zero;
five give the strictly positive normalized weight240*kappa*2^h*product x_i.
The surviving signed reduction is exactly prime pairs plus two-, three-,
four-, five- and six-factor partners and o(Y*t). Even classes have one
positive-sign factor above the enlarged cutoff; odd classes have none.
Positive pure triples force a prime larger than n^(18/25), leaving a
two-prime cofactor below Y^(7/25). An auxiliary sieve then gives the actual
bound S_3^+<<kappa*Y*S_2(m)*t with an absolute constant. Its remainder
indices are NOT injective: at most binom(omega(index),2) choices cost
O(log(Y)^2), still absorbed by the relative distribution budget. This is
only a main-scale bound, not a small fraction or a positivity theorem.
Positive balanced five-factor weights expose an additional surviving loss.
Sol checked theory and actual files; five exact tests passed normally
and with Python -O. The pursuit returned `changed-under-evidence` within30
minutes. No new actual coverage, zero, numerical onset, priority search,
publication work or wake queue. Overall research remains active.

The next pursuit closes the remaining MAIN-SCALE error bounds for that
quintic in `quintic_loss_budget.py`. In the same actual-zero regime,
all surviving positive composite weights total at most
C*(1+kappa)*Y*S_2(m)*t+o(Y*t), with C absolute, independent of theta.
For five negative factors, use their two smallest factors as cofactor and
adapt the auxiliary sieve cutoff to the second smallest. For the even
factor classes, switch the actual prime variable to the single large
positive-sign factor; repaired bulk Linnik then uses modulus D*e at scale
Y/M, without requiring distribution at modulus M. Its summed errors are
O_kappa(Y*(t^28*log(Y)^2+log(Y)^3/D)+Y^(19/25+o(1)))=o(Y*t).
An explicitly FORMAL logarithmic-share measure gives signed pure-triple
and pure-five integrals -kappa/12 and +kappa/12. This exact cancellation
does not assert an actual prime-factor distribution or signed correlation.
The composite bound is still not a small specified fraction, and the
positive lower bound for the full signed total remains unproved.
Five exact tests passed normally and with Python -O, covering adaptive
index multiplicity, complete switched CRT counts, range slack, weighted
factor shapes and independent iterated polynomial integration.
Sol checked theory and actual files. The pursuit returned
`changed-under-evidence` within30 minutes.
No new actual coverage, zero, numerical onset, priority search,
publication work or wake queue. Overall research remains active.

The signed-cancellation pursuit found a general conservation identity in
`formal_weight_conservation.py`. For every normalized polynomial f of
degree d and0<=theta<1/d, the sum of FORMAL odd all-negative factor
integrals equals B_f(theta)=-E[h'(theta*V)]/2, h=f(1-x)-f(x), with V
the normalized Dickman variable. At theta0 this is A_f, so the formal
composite total is A_f-1. At nonzero theta the quintic gives exactly
1-2kappa*theta+18kappa*theta^2-(170/3)kappa*theta^3
+(190/3)kappa*theta^4. A convolution generating function proves the
identity for every degree; independent exact simplex and moment algorithms
check it through degree10. A rational factorial enclosure connects B_f
to the already proved accessible-divisor main, retaining its fixed sieve
error separately. Thus the formal cancellation supplies no second estimate
for actual composite correlations. The exact remaining identity is
P/Z-1=T_boundary/Z-Delta/Z+(T_low/Z-B_f), where
Delta=(T_f-P)-(B_f-1)Z and Z=length(J_real)*S_2(m)*t.
The signed quantity T_boundary-Delta still lacks the estimate needed for
positivity. Five focused exact tests passed normally and with Python -O.
Sol checked theory and actual files. The pursuit returned
`changed-under-evidence` within30 minutes.
No new actual coverage, zero, numerical onset, priority search,
publication work or wake queue. Overall research remains active.

On 2026-09-09 Kevin resumed the clean main checkpoint cf48198, with latest
mathematics6f9a77b, and reaffirmed open-ended curiosity, 30-minute hypothesis
ceilings, independent correctness review, and no manual wake queues. He
clarified that seeking a new arithmetic ingredient must preserve the useful
polynomial identities and bounds: the earlier limitations concern specific
approaches, not every future use of those tools. The operative question is
what mechanism could make the linked prime conditions cancel or reinforce
each other, and what would demonstrate it. This is a resumed execution, not
evidence of research running between the saved checkpoint and this session.

The first resumed pursuit returns `changed-under-evidence` in
`buchstab_endpoint_bridge.py`. Exact least-prime Buchstab subtraction up to
R=floor(Y^(1/2-2epsilon)) leaves actual prime partners and only distinct
mixed-sign semiprimes. The earlier corrected Henriot bound and actual
rare-prime reciprocal estimate bound this endpoint loss by
C*epsilon*Z+o(Y*t), with C absolute and Z=length(J_real)*S_2(m)*t.
There is no additional rarity factor. The initial rough-pool mass is
L*X*V(z)+O(eta_u*L*X*V(z))+o(Y*t), retaining the fixed sieve error.
The remaining unproved target is a stated one-sided bound on the exact
prime-times-rough sum U_A(z,R). Its condition P^-(k)>=q couples the two
variables; it is not automatically a separated-coefficient Type II sum.
This range adds smaller factors while excluding the balanced endpoint,
so it is not claimed to be a subset or a proved easier version of the
old Vaughan target. No cancellation estimate has been obtained.
Ford--Maynard's bounded-sequence sieve motivated the test but is not
imported: its positivity/comparison and boundedness hypotheses are missing
for the signed rare-scale model. The exact Buchstab identity also accepts
polynomial kernel weights, but their initial full total cannot be replaced
by T_low or its formal main. Sol independently checked theory and actual
files; five exact tests passed normally and with Python -O, including
prime powers, strict cutoffs, actual finite reflected-prime/sign support
and the existing1459+11^3 example. The pursuit closed within30 minutes.
The next useful action must test an arithmetic estimate for U, possibly
using preserved polynomial components, not iterate this counting identity.
No new actual coverage, zero, numerical onset, priority search, publication
work, push, foreground operation, or wake queue. Overall research active.

The next pursuit tests whether lambda_chi=1*chi can supply a SECOND rarity
factor for two linked positive-character primes. The direct multiplicative
upper bound retains the empty-cofactor atom1 and supplies none. A restricted
coefficient-one route succeeds in `rare_shifted_divisor_bound.py`: with an
ACTUAL zero beta=1-1/(eta*log D), X=D^V, V>=log^3 eta and t=V/eta<=1/log X,
the weighted sum over X<p<=2X, p,p+h prime, chi(p)=chi(p+h)=+1 satisfies
Q++<<S_2(h)*X*t^2*log^8 eta=o(S_2(h)*X*t), uniformly for even0<h<=X/2.
This is a deduction from Matomaki--Merikoski Proposition2.3, equation(15)
and Lemma2.4, https://arxiv.org/html/2112.11412v2 . It is an actual
conditional upper estimate, with no assumption of independent prime signs.
Subtracting the lemma's y=X and y=X^2 evaluations bounds each rough harmonic
character partial sum by O(E/U), E=O(t*U^4)+O(eta^-20), U=K*log eta.
The smooth hyperbola identity produces two such factors after ALL main
terms are recombined before absolute values. Complete residue sums restore
the conductor-prime local factors. The proof budgets every dyadic error.
Growing U is justified directly by the source, in this NEW restricted regime;
it does not alter the earlier fixed-u conclusions or parameter order.

The original transfer to q,p=m-M*q, chi(M)=-1, M<=Y^(13/25), remains OPEN.
The source only gives coefficient-one relations. Substitution n=M*q kills
lambda_chi(n) exactly; a divisor divisibility restriction or an enlarged
modulus requires a new uniform theorem. Cowan's twisted-divisor Theorem1.1
does not cover the zero shifts in its divisor parameters and the principal
product chi^2; Tao--Teravainen supplies no stated variable-M transfer either.
Neither the rare/common Goldbach pair nor the Buchstab one-sided target is
estimated here. Preserve the polynomial identities and bounds for future
combinations with this or another arithmetic ingredient. Five finite tests
check exact hyperbola recombination, log-form cancellation, conductor factors,
and the failed multiplier substitution; they are not tests of an actual zero
or an infinite prime estimate. Overall research remains active.
Sol reviewer `/root/sieve_review` independently passed both the theory and
actual files. The five focused tests passed normally in0.088s and under
Python -O in0.093s. Reassessment: `changed-under-evidence` within30 minutes;
retain the coefficient-one component, leave the variable-M transfer open.
No new actual coverage, zero, numerical onset, publication, push, foreground
work, installs or manual wake queue. The saved Qwen-unavailable exception
remains unchanged; this was active execution, with no intervening idle work
claimed.

The affine-extension pursuit in `rare_affine_small_cofactor.py` proves
negligibility for a part of the ACTUAL cofactor range, while the full range
remains open. Retain the new actual-zero/large-V assumptions Y=D^V,
V>=log^3 eta, t=V/eta<=1/log Y. For fixed0<theta<1/5, sum the positive-prime
pair-log mass for q and p=m-M*q over all original-Y^theta-rough integers
2<=M<=Y^(1/5) with gcd(M,Dm)=1. The total is o_theta(Y*t), uniformly over
even m in[Y,2Y] with q in(Y/(2M),Y/M] and p in(Y/2,Y]. Squarefreeness
and a five-factor cap are unnecessary. The actual even quintic classes are
a subset, and the fixed-polynomial bound |K_f(n)|<<_(f,theta)log Y transfers
this to their FULL ABSOLUTE contribution in that cofactor range.

This adapts the proof of Matomaki--Merikoski Proposition2.3; it is not an
invocation of its coefficient-one statement for a different equation.
Directly making p's large divisor implicit leaves Poisson modulus D*d2*c;
M enters as an invertible inverse-phase factor. The derivative scales
1/(Y/M) and M/Y agree. The two rough harmonic character cancellations
survive, after every orientation main is recombined before absolute values.
Corrected Henriot New Theorem5 bounds the affine divisor-weighted sieve
tails; its norm and function-class conditions are included. Shared primes
dividing m are removed on the original rough support without applying
Henriot at an unjustified tiny divided scale. Conductor and M-coprimality
local factors are separately restored. With sum_M1/M=O_theta(1), the main
is O_theta(S_2(m)*Y*t^2*log^8 eta). The summed oscillatory error is
D^2*Y^(44/45+o(1)); the M-coprimality error is Y^(1-theta+o(1)), and
the remaining errors are O_theta(S_2(m)*Y*eta^-20). These are all o(Y*t)
in the stated regime. The exact density verifier retains the1/a Jacobian.

The full M<=Y^(13/25) extension FAILS the available error-budget test.
Ignoring small conductor/sieve/log losses, direct absolute Weil bounds
sum to Y^(3/4+alpha), and the reversed-orientation budget to
Y^(3/4+3alpha/4), for M<=Y^alpha. The latter is Y^(57/50) at alpha13/25.
These are METHOD upper bounds, not lower bounds or universal obstructions.
The reversed complete theorem is not promoted. A new estimate, plausibly
averaging across cofactors before absolute values, is needed for the larger
range. All-negative odd composite classes and the positive lower bound
for the signed total also remain open. Preserve all polynomial components,
the coefficient-one theorem and the new partial affine theorem together.
Sol reviewer `/root/sieve_review` passed both the theory and actual files,
including the affine source adaptation, corrected sieve-tail conditions,
all M/theta factors and the final o(Y*t) conclusion. Four exact tests passed
normally and under Python -O, both in0.011s. The pursuit returned
`changed-under-evidence` within30 minutes: a small-cofactor arithmetic loss
is now negligible, while full-range absolute summation failed its budget.
Next concrete test: can averaging the remaining cofactors BEFORE absolute
values preserve the two character cancellations and gain the missing power?
No new actual coverage, zero, numerical onset, publication, push, foreground
work, installs or manual wake queue. No process is left running at this
checkpoint. The overall Goldbach research goal remains active.

The next cofactor-averaging pursuit returns a SOURCE-BUDGET FAILURE in
`cofactor_averaging_budget.py`. Test: does Bettin--Chandee Theorem1,
equation(1.2), https://arxiv.org/pdf/1502.00769v1 , give a power saving
after grouping r=M*a in the actual inverse phase? For M~Y^b, small
q-divisor a~Y^x and p-divisor c~Y^y, set r_exp=b+x, s=y and
k_exp=b+x+y-1>=0. The Poisson prefactor is Y/(R*C), and the numerator
parameter is the target m~Y. The generic L2 norms contribute
(r_exp+s+k_exp)/2; the phase ratio m*K/(R*C) has exponent0.
Even granting a COST-FREE separation of the actual coupled weights, the
two source terms give worst-box exponents
`39/40+19*b/40` and `15/16+b/2`, attained at x=(1-b)/2,y=1/2.
At b=1/5 these are107/100 and83/80; at b=13/25 they are611/500 and479/400.
Both exceed1 throughout the remaining interval. The theorem returns their
SUM, not their minimum. Fixed-frequency application followed by summation
worsens its first term and leaves the second unchanged; reciprocity does
not change the exponents. The required separable decomposition has not
been proved either, but granting it for free already fails the strength test.

This is a calculation of substituted UPPER bounds, not evidence that the
actual oscillatory error is large. It rules out only the unchanged generic-
norm plug-in as a sufficient proof. No new prime estimate or coverage is
claimed. Preserve cofactor averaging, the exact grouping/normalization, the
polynomial tools and all previous arithmetic components. A materially new
next test should retain the separate M and a structure after beta-sieving
and test whether that gives stronger averaged cancellation; merely citing
the same generic trilinear estimate under new notation is not a new route.
Sol reviewer `/root/sieve_review` independently checked the source scaling,
monotonicity and thresholds, then the actual files: PASS. Four exact tests
passed normally in0.020s and under Python -O in0.036s. They test bookkeeping,
not the coupled-sum source hypotheses or any analytic prime estimate. The
pursuit returned `changed-under-evidence` within30 minutes. The previous
actual affine result remains the latest arithmetic estimate; this pursuit
adds a verified failed-source application, with its useful setup preserved.
No new coverage, zero, effective onset, publication, push, foreground work,
installs or manual wake queue. Qwen remains unavailable without a retry.
No research process is left running at this checkpoint. Overall goal active.

The separate-factor pursuit proves a RESTRICTED EXPONENTIAL-KERNEL bound
in `separate_factor_prime_kernel.py`. Keeping M,a separate, their exact
double Fourier transform at prime modulus p is p*Kl_3(t*h*l;p) off the
axes,1 on each single nonzero axis, and1-p at the origin, when p does not
divide t. The t=0 case is separately the product of Ramanujan sums.
Pointwise complete-sum bounds alone reach Y. Retaining the original
frequency k and grouping w=k*l AFTER completion instead permits a bilinear
application of Kowalski--Michel--Sawin Theorem1.1, equation(1.2):
https://arxiv.org/pdf/1511.01636v5 . This is a different, successful
source-strength test from the failed generic r=M*a reduction.

The proved model has P=Y^(1/2), M~B=Y^b, a~A=Y^((1-b)/2), k<=K=Y^(b/2),
1/5<=b<=12/25, smooth SEPARATE M,a weights and arbitrary bounded k weights
for each PRIME modulus p in[P,2P]. With the actual Poisson prefactor
Y/(B*A*p), the sum is O_epsilon(Y^(127/128+epsilon)), uniformly m in[Y,2Y].
Dual lengths U=p/B,V=p/A satisfy U*V*K~p; the grouped coefficient at w=k*l
is divisor-bounded. The source gives saving p^-1/64. Schwartz truncation
preserves its hypotheses after small epsilon losses. Axes and p|m moduli
cost O(B*A+A+B), at most Y^(37/50), and are treated without the unit formula.

This is an analytic cancellation theorem in the stated model, NOT a new
original-affine prime-pair estimate. The actual modulus d2*c is generally
composite; rough/sieve/character coefficients and coupled Poisson weights
have not been transferred. KMS section1.5.2 does not supply the needed
composite version. Neither all hyperbola boxes nor the remaining b range
are covered here. The latest ORIGINAL-AFFINE result remains2b8cf98.
Preserve the polynomial identities, bounds and all previous components.
Next concrete question: can a composite-modulus third-divisor/Kloosterman
distribution estimate support these factors with the actual small sieve
indices and conductor while retaining a power saving? Source hypotheses
and losses, including any roughness relaxation, must be checked explicitly.
Four exact cyclotomic/budget tests passed normally in0.062s and under -O
in0.075s; they guard identities and bookkeeping, not the analytic source.
Sol reviewer `/root/sieve_review` independently checked the source, theory
and actual files: PASS, including all modes and the source's prime boundary.
The pursuit returned `changed-under-evidence` within30 minutes: keeping
factors separate now has a proved cancellation component worth transferring.
The overall research goal remains active; no new coverage or signed
prime-correlation estimate, publication, push, installs or manual wake queue.
Qwen remains unavailable without a retry. No process is left running at
this checkpoint, and no work between inactive turns is claimed.

The next transfer pursuit proves `decorated_prime_kernel.py`: the kernel
now permits c=s*p with p prime near P=Y^(1/2), s<=S, arbitrary bounded
joint residue weights modulo J<=J0, and frequencies k<=H*K. The underlying
B=Y^b,A=Y^((1-b)/2),K=Y^(b/2),1/5<=b<=12/25 geometry is retained. The
TOTAL modulus grows with s; the frequency inflation H is explicit. For
S,J0,H<=Y^(1/4096), the proved bound is
  Y^(127/128+epsilon)*S^4*J0^4*H
    +H*B*A*log(2S)+S*H*J0*(A+B) <<Y^(4073/4096+epsilon).
CRT at period cJ splits off prime p even if gcd(s,J)>1. The prime Kl3
argument is m*k*h*l*inverse(s^3*J^2), with any stated unit multiplier.
The small transform has magnitude at most(sJ)^2. Splitting the two dual
residue classes costs(sJ)^2 more; its k dependence is absorbed as a bounded
k coefficient. No third residue split is needed. Axes and p|m modes are
below Y^(3/4). Uniform smooth coupling of M,a is allowed via a convergent
Fourier decomposition, with k-dependent coefficients handled explicitly.

A second retained component is the NONNEGATIVE relaxation of original M
to z-rough M: its reciprocal mass is O(U), and the existing zero mode keeps
both character harmonics, giving at most one extra factor U~log eta and
still o(Y*t). No chi(M) factor appears. Prime-divisor coprimality costs
are O(U/z). This is a statement about the zero-mode expression, not a
replacement of the entire arithmetic sum. A beta sieve introduces a new
index e0; its longer dual range cancels the apparent1/e0 gain. Index counts,
periods, frequency inflation and tails must be paid before any prime result.

The source search did not justify a general-composite plug-in. Topacogullari
1506.02608v1 Thm1.3/section4 treats the right additive orientation but is
untwisted; Drappeau--Topacogullari2019 Lemma4.5 allows characters but has
|h|<=X^(1/4) and an ordinary-divisor second factor. Do not combine their
separate features into an unstated theorem. Their methods remain candidates.
The CRT theorem covers SMALL prime multiples, not balanced composite cores.
All original sieve costs, other boxes/ranges and the signed correlation
remain OPEN; latest original-affine estimate remains2b8cf98. Polynomial
components remain preserved. Next test: a general-composite factor estimate
or a costed spectral adaptation meeting the actual character/shift conditions.
Sol reviewer `/root/sieve_review` passed theory and actual files, after
correcting a divisor-sum notation to DISTINCT PRIME divisors. Five new exact
CRT/budget tests passed normally in0.022s and under -O in0.026s. No old
experiment was rerun. The pursuit returned `changed-under-evidence`
within30 minutes. No new coverage, zero, effective onset, publication, push,
foreground work, installs or manual wake queue. Qwen remains unavailable;
no process is left running at this checkpoint. Overall research goal active.

The next bounded pursuit proves `hyperbola_prime_kernel.py`: changing the
completed-frequency grouping, with a linear-completion estimate in the
small-divisor region, covers EVERY box of the smooth decorated prime-core
model. The parameters are B=Y^b,A=Y^x,P=Y^y,K=B*A*P/Y, with
  1/5<=b<=13/25, 0<=x<=(1-b)/2, 0<=y<=1/2.
The preceding modulus c=s*p, p prime near P, joint periodic weights and
S,J0,H<=Y^(1/4096) remain. The final bound is unchanged:
  Y^(127/128+epsilon)*S^4*J0^4*H
    +H*B*A*log(2S)+S*H*J0*(A+B) <<Y^(4073/4096+epsilon).
Nonempty boxes force p large enough for CRT and k<p. For y<=49/100,
pointwise complete-sum bounds suffice. For y>=49/100 and x>=1/16,
keep the completed divisor frequency l separate and group w=k*|h|.
KMS's bulk exponent becomes(103*y+12)/64<=127/128. For x<1/16,
the exact Fourier transform of Kl3, extended at zero by1/p, is a
classical Kl2 sum at nonzero frequencies and zero at frequency0.
Linear completion on l=r+T*j uses j-scale p/A<=p, even when the
l-scale exceeds p. Every prime-axis mode and the thin dual-length
strip below1 are included. Smooth coefficients remain essential.

This closes the box-range gap in the MODEL, including b through13/25.
It does not close the general-composite core, original coefficient/sieve
transfer, or signed prime-correlation gaps. The latest original-affine
estimate remains2b8cf98. Polynomial components remain preserved.
Next concrete test: can factorization or completion give a power saving
for a general composite core in the critical modulus boxes, after
explicitly retaining nonunit modes and the actual coefficient costs?
Do not import an unstated composite-modulus KMS theorem.
Five NEW exact Fourier/progression/budget tests passed normally in0.222s
and under -O in0.226s. Sol `/root/sieve_review` independently passed the
linear lemma, full theory and actual files, with no correction required.
The pursuit returned `changed-under-evidence` within30 minutes. No old
experiment was rerun. No new prime coverage, zero, effective onset,
publication, push, foreground work, installs or manual wake queue.
Qwen remains unavailable without a retry. No process is left running
at this checkpoint; the overall research goal remains active.

The next composite-modulus pursuit proves `composite_linear_kernel.py`:
for ALL integers q near C=Y^y, including prime powers, the same smooth
box model with arbitrary joint periods J_q<=J0 and k<=H*B*A*C/Y satisfies
  sum_q |E_q| <<Y^epsilon*H*(J0^2*min(A,B)*C^(3/2)+J0*B*A).
No coprimality between J_q and q, or between m*k and q, is required.
The normalized complete transform in one frequency is an ordinary
Kloosterman sum. Periodic lifting costs J^2; the nonzero-frequency gcd
factor is absorbed by a divisor average. The h=0 mode uses a separate
restricted Ramanujan decomposition and the modulus average of gcd(q,m*k).
All its costs are included, including shared period factors and prime powers.
The sole analytic input is the ordinary composite Weil bound, checked in
Topacogullari1506.02608v1 section2 p4; no shifted-divisor or composite KMS
theorem is imported.

This saves a power when min(b,x)+3*y/2<=127/128, giving
Y^(4067/4096+epsilon) with J0,H<=Y^(1/4096). It FAILS the required power
budget at b=x=1/3,y=1/2, where the bound is Y^(13/12+epsilon) before
decorations. That is a failure of this upper bound, not evidence that the
true error is large. Preserve the composite unbalanced component, the
prime-core theorem and all polynomial tools. The next method must save
more than1/12 at this box and pay period/frequency costs.
One concrete UNTESTED route is additive autocorrelation of multiplicative
Kl3 dilates plus CRT. Check prime diagonal cases, coefficient nonunits and
prime powers before claiming any composite bilinear consequence. KMS
Remark1.2 points to FKM arXiv1211.6043 Theorem1.17; that exact theorem has
not yet been read here and is only a primary locator.

Six NEW exact composite-transform, restricted-Ramanujan, gcd-average and
budget tests passed normally in0.774s and under -O in0.769s. Sol
`/root/sieve_review` independently passed the transforms, full theory and
actual files, with no correction required. The pursuit returned
`changed-under-evidence` within30 minutes: useful general-composite
coverage is preserved alongside a quantified critical failure.
The full original arithmetic/sieve transfer and signed correlation remain
OPEN; latest original-affine estimate remains2b8cf98. No old experiment,
new prime coverage, zero, effective onset, publication, push, foreground
work, installation or manual wake queue. Qwen remains unavailable without
a retry. No process is left running at this checkpoint; overall goal active.

The next pursuit proves `squarefree_correlation_kernel.py`. FKM
arXiv1211.6043v3 Theorem1.17, Proposition3.1 and sections3/6 have now been
read. The proof uses only the PRIME bounded-exceptional-pair theorem.
CRT and a congruence count give the derived squarefree bilinear bound
  |sum alpha_a beta_n K_q(c*a*n)|
    <<q^epsilon*M*N*(q^-1/4+M^-1/2+q^(1/4)*N^-1/2),
for bounded coefficients, ANY integer multiplier c and no coefficient
coprimality restriction. K_q(0)=1/q for squarefree q is explicit.
No composite KMS/FKM theorem is imported. Knowing the exact prime
exceptional pairs is unnecessary: fixing one coefficient variable fixes
the other variable AND the additive frequency modulo each selected divisor.

The exact local F_p expansion retains every nonunit mode. Its four
degenerate prime assignments have normalized rescaled mass g/D^2;
their costs in all three bilinear terms are at most1. A transient briefing
overstatement was corrected: the short-variable factor can be D^-1/2,
not uniformly D^-3/4. The saved proof uses the valid <=1 statement, and
a regression fixture preserves that boundary. Shared period factors and
both axes, including their subtracted overlap, are explicitly paid for.

At the SAME formerly failing balanced box B=A=Y^(1/3),C=Y^(1/2),K=Y^(1/6),
the smooth model over ALL SQUAREFREE q near C now satisfies
  sum_q |E_q| <<Y^(23/24+epsilon)*H*J0^8+Y^epsilon*H*J0*B*A
               <<Y^(11803/12288+epsilon).
This includes small prime factors and balanced semiprime cores. Prime
powers, further box coverage and original arithmetic/sieve transfer remain
OPEN, as does the signed prime-correlation estimate. Latest original-affine
bound remains2b8cf98. All preceding polynomial and kernel tools are preserved.

Next UNTESTED question: can prime-power stationary phase prove
  |F_q(h,l;t)| <<q^(1+epsilon)*gcd(q,h,l,t),
including unequal valuations, p=2,3, and zero parameters? Even exponents
suggest a count of cubic stationary points; odd exponents also need the
quadratic Gauss sum. If valid, Fourier expansion of a period-J weight at
qJ should cost J^4, and the nonzero-frequency divisor average should give
O(Y^epsilon*H*J0^4*C) per modulus. Then test a squarefull-part split:
small squarefull part u<=Y^(1/128) costs at most u^(13/4) in the proved
squarefree CRT estimate, while the large-part moduli number is
O(C*Y^(-1/256)). Expected total exponent4085/4096 is UNPROVED until all
these steps are checked. This route could remove prime powers by density
without assuming a prime-power correlation theorem.

Seven NEW exact CRT, conjugation, degeneration, exceptional-class and
budget tests passed normally in0.191s and under -O in0.190s. Sol
`/root/sieve_review` independently passed source/theory and actual files.
The pursuit returned `changed-under-evidence` within30 minutes. No old
experiment was rerun; no new prime coverage, zero, effective onset,
publication, push, foreground work, installation or manual wake queue.
Qwen remains unavailable without a retry. No process is left running at
this checkpoint; the overall research goal remains active.

The next pursuit proves `all_moduli_balanced_kernel.py`. The proposed
prime-power pointwise bound holds for every q,h,l,t:
  |F_q(h,l;t)|<=6^omega(q)*q*gcd(q,h,l,t).
The proof removes the common valuation, handles its all-zero case
separately, counts cubic stationary points at even exponents, and pays
the quadratic Gauss sums at odd exponents. The bad primes2,3 and unequal
valuations are included. Only the previously checked PRIME Kl3 bound is
imported; no prime-power correlation theorem is assumed.

An exact double Fourier lift pays J^4 for arbitrary joint period J,
including gcd(q,J)>1. The nonzero-frequency gcd average gives
O(Y^epsilon*H*J0^4*C) per modulus. Split the FULL squarefull part u(q)
at Z=Y^(1/128). Moduli with u>Z number O(C*Z^-1/2); for u<=Z, the saved
squarefree correlation estimate absorbs the small part at cost Z^(13/4).
Both axes and their overlap retain the earlier general-modulus bounds.
At B=A=Y^(1/3),C=Y^(1/2),K=Y^(1/6), the smooth model over ALL integers
q near C therefore satisfies
  sum_q |E_q|<<Y^epsilon*H*(J0^8*Y^(23/24)*Z^(13/4)
                              +J0^4*Y*Z^-1/2+J0*Y^(2/3))
              <<Y^(4085/4096+epsilon),
for J0,H<=Y^(1/4096). This closes the squarefree restriction at this box.
It does not close a prime-power correlation theorem, other box geometries,
original arithmetic/sieve transfer, or the signed prime correlation.
Latest original-affine estimate remains2b8cf98; polynomial tools remain.

Six NEW exact stationary, valuation, Gauss, periodic-lift, squarefull and
budget tests passed normally and under -O, each in0.299s. Sol
`/root/sieve_review` independently passed the prime-power proof, global
transfer and actual files, with no correction required. This pursuit began
08:34 UTC and returned `changed-under-evidence` within30 minutes.
Next concrete question: at B=A=Y^(1/4),C=Y^(1/2),K=1, both current
composite budgets reach Y before decorations. What additional cancellation
mechanism can beat that boundary, with its coefficients and moduli paid for?
This is an upper-bound budget obstruction, not evidence of a large true sum.
No old experiment was rerun; no new prime coverage, zero, effective onset,
publication, push, foreground work, installation or manual wake queue.
Qwen remains unavailable without retry. No research process is left running
at this checkpoint. Overall goal active; no claim of execution during pauses.

The next pursuit proves `reciprocal_energy_kernel.py`, using an elementary
modulus-average mechanism at the remaining symmetric boundary. In a fourth
moment, the reciprocal relation has integer numerator
  D=(a1+a2)*a3*a4-(a3+a4)*a1*a2.
For D!=0, a modulus contributes only if q divides m*k*D, giving a divisor
bound even when m*k is not a unit. For D=0, fixing a1,a2 and reducing
u/v=1/a1+1/a2 gives (u*a3-v)*(u*a4-v)=v^2. This counts ALL rational
relations, including non-diagonal ones, in O(A^(2+epsilon)). Thus
  sum_(q near C) E_(q,mk)(A)<<Y^epsilon*(A^4+C*A^2).
No prime-only additive-energy theorem or composite extension is imported.

Holder in the spatial variable and then q, including repeated inverse
residues when B>q, gives
  R(B,A,C)=C^(3/4)*B^(3/4)*(B+C)^(1/4)*(A^4+C*A^2)^(1/4).
The full smooth model satisfies
  sum_q |E_q|<<Y^epsilon*H*J0^2*min(R(B,A,C),R(A,B,C)).
This covers ALL integer moduli and arbitrary bounded separated spatial
weights. Joint period J costs J^2. The k count cancels the kernel prefactor;
no spatial Poisson decomposition or separate axis estimate is needed.
At B=A=Y^(1/4),C=Y^(1/2),K=1, the bound is Y^(15/16+epsilon)*H*J0^2,
hence3843/4096 after caps. Throughout valid boxes with b,x<=9/32,y<=1/2,
monotonicity gives127/128 before caps and4067/4096 after caps.

The common nonzero m*k across q is essential; arbitrary t_q=q destroys
the divisor argument. Arbitrary coupled arithmetic weights remain outside
the separated-weight assertion. At b=1/2,x=1/4,y=1/2, the new energy
budget is9/8 and the previous linear budget is1. Preserve these failures
alongside the useful region; they are not lower bounds on the true sum.
Next concrete question: after completing the long M variable at this box,
can a modulus-averaged correlation of the resulting ordinary Kloosterman
sums save a power with both a and k near Y^(1/4)? This is UNTESTED.
All original sieve/weight transfer and the signed prime correlation remain
OPEN; latest original-affine result remains2b8cf98. Polynomial tools remain.

Five NEW exact rational-relation, weighted fourth-moment, divisor-average,
multiplicity and budget tests passed normally in0.112s and under -O in0.110s.
Sol `/root/sieve_review` independently passed the critical proof, general
family and actual files with no correction needed. This pursuit began
08:50 UTC and returned `changed-under-evidence` within30 minutes. No old
experiment was rerun; no new prime coverage, zero, effective onset,
originality, publication, push, foreground work, installation or wake queue.
Qwen remains unavailable without retry. No research process is left running
at this checkpoint; the overall goal remains active, with pauses reported.

The next pursuit changes direction under the source evidence. The ordinary
Kl2 bilinear interval theorems checked here do not accept the inverse-a
support after M-Poisson. Freezing a instead leaves h too short to improve
the existing Weil budget. Preserve these source-applicability failures;
they do not refute the source theorems or every use of completion.

`two_prime_kl3_kernel.py` instead derives a rank-three bilinear theorem for
q=p1*p2 with distinct primes and p_min>=q^(2/5). For arbitrary complex
coefficients supported <=X, sqrt(q)<=X<=q^(1/2+1/128), and ANY integer c,
the norm factor is q^(11/64+epsilon)*X^(5/8), hence q^(31/64) at X=sqrt(q).
The source's literal zero extension is used during amplification, then
the natural K_p(0)=1/p extension is recovered with a paid nonunit error.
KMS prime eight-factor correlations, all-twist diagonal subtraction, and
rank-three CRT with frequency twist h*(q/p)^2 supply the arithmetic gain.
Small auxiliary shifts synchronize the two local diagonals as one integer
multiset equality. Generic, bad and diagonal tuples are all costed.
This derives a two-prime Kl3 statement; MQW's Kl2 theorem is not imported
as a Kl3 theorem, and no prime-square correlation assertion is made.

For the same smooth MODEL at B=Y^(1/2),A=Y^(1/4),C=Y^(1/2),K=Y^(1/4),
the specified two-prime moduli satisfy
  sum_q |E_q|<<Y^(127/128+epsilon)*J0^5*H^2+Y^(3/4+epsilon)*H*J0,
hence exponent4071/4096 after caps. Nonunit m*k, joint periods, both
integer axes and the zero-extension correction are included. General
factorizations, prime powers in this box, full box coverage and the actual
arithmetic/sieve transfer remain OPEN. Latest original-affine remains
2b8cf98. The formal cancellation still does not estimate the signed
prime correlation. Preserve the polynomial identities and earlier bounds.

This pursuit began09:01:55 UTC, with a09:32 UTC ceiling. Five NEW exact
tests passed normally in0.233s and under -O in0.335s. Verifier-only
corrections fixed late-bound histogram generators, float division, and a
vanishing test fixture. Sol `/root/sieve_review` passed the theory,
varying-length argument and actual files, with no material correction.
This pursuit returns `changed-under-evidence` within its30-minute ceiling.
Next concrete question: can CRT counting of bad primes replace the
small-shift condition at every prime, giving a saved bound for general
squarefree moduli in this unbalanced box? Test the complete bad-set and
nonunit-difference costs before asserting any extension. No original
prime coverage, effective onset, zero, novelty or outside action is claimed.
No old experiment was rerun. Qwen remains unavailable without retry;
no model install, publication, push, foreground action or manual wake queue.
No research process is left running at this checkpoint. The overall goal
remains active, with no claim of execution during pauses.

The next pursuit proves `squarefree_unbalanced_kernel.py`: the unbalanced
MODEL box B=Y^(1/2),A=Y^(1/4),C=Y^(1/2),K=Y^(1/4) is now covered for
ALL squarefree q. FKM1405.2293v2 Corollary3.4 supplies the prime four-factor
bound with an explicit rank3 normality check. Divisor shifts preserve one
modulus factor and expose this correlation on the other. A weighted signed
congruence graph bounds every nonunit difference; they are not discarded.

An integer factorization dichotomy combines that route with the retained
prime/two-prime amplification. It gives norm factor X*q^(-1/256+epsilon)
for arbitrary coefficients supported <=X, sqrt(q)<=X<=q^(1/2+1/256),
for the natural K_q extension and ANY integer multiplier. A disjoint
gcd(c,q), gcd(m,q0), gcd(n,q1) partition pays the nonunit cases explicitly.
Fixing h before the l,k bilinear estimate needs only one period-residue
split: the small-transform cost is T^3. All joint periods, nonunit modes,
integer axes and their overlap remain included. The full MODEL satisfies
  sum_q |E_q|<<Y^(1-1/4096+epsilon),
with raw exponent1-511/1048576. The source hypotheses and the original
arithmetic/sieve-transfer boundary remain explicit in the proof module.

The exact exponent test corrected an overcount in the draft: the period
decoration total is6+1/256, not7+1/256. The correction strengthens the
bound. Eight NEW finite algebra/budget tests passed normally in0.124s and
under -O in0.135s. Sol `/root/sieve_review` passed the theory, actual files,
divisor-shift endpoints, corrected arithmetic and the following splice.

The existing squarefull-part split does NOT finish the same box at the
full period/frequency caps. Even after using the small-squarefull density,
its head/tail exponents are
  1-511/1048576+(3/2+1/256)*z, 1+5/4096-z/2.
Their optimal maximum is467315/466944>1 at z=199/233472, within the
proved support ranges. This is a failure of these upper bounds only.
Do not repeat the same splice. Next concrete question: can a prime-square
four-factor correlation, derived from the retained stationary-phase
formula, save a power outside explicit exceptional congruences? Check
the critical equations and exact finite sums before any general claim.

Preserve KMS Proposition4.29's fixed integral bad hypersurface as another
promising component; its full alternative CRT/amplification route was
not proved or needed here. Prime powers in this box, full box coverage,
original sieve transfer and the signed prime correlation remain OPEN.
Latest original-affine remains2b8cf98; all polynomial tools survive.
This pursuit began09:26:06 UTC and returns `changed-under-evidence` before
its09:56 UTC ceiling. No old experiment, install, publication, push,
foreground action or manual wake queue. Qwen remains unavailable without
retry. No research process is left running at this checkpoint. The overall
goal remains active, with no claim of execution during pauses.

The next pursuit, **90488ef**, saves the SAME unbalanced MODEL box for
EVERY integer modulus, in `all_moduli_unbalanced_kernel.py`. The repeated
prime factors stay in the factor r preserved by divisor shifts; only its
coprime complement s needs to be squarefree. This uses the existing
all-prime-power pointwise bound and avoids the failed residue-split cost.
For full squarefull part U(q)<=q^(2/5), the corrected classification gives
r in[q^(1/32),q^(69/160)] or a small factor with one/two large simple
primes left. Independent review caught the missing transition cases in
the proposed narrower2/5 upper limit. The wider range still saves1/256.

All integer multipliers and prime-power zero patterns are included by the
exact recursion G_e=K_(p^e)(hlt)+p*1_(p|h,l,t)*G_(e-1), ending at the
retained prime identity. Its terms pay volume massD^-1 and fixed-h norm
massD^-1/2, up to divisor factors. The exact period lift costs J^4;
arbitrary-position second intervals and periods sharing q are paid.
Using U(q)<=q^(39/100) as the good-modulus cutoff gives
 Y^(1-1/512+epsilon)*J0^(7/2)*H^(3/2).
The remaining O(C^(161/200)) moduli use squarefull density and the
retained pointwise bound. Axes and overlap remain included. At the full
H,J0 caps the good exponent is1-3/4096 and the theorem is1-1/4096.
The preceding squarefull-residue budget remains a valid failed route.

A separate retained component proves the prime-square four-factor bound
<=108p for p>=5 and p not dividing a(u-v), uniformly in the Fourier
twist. It comes from the exact unit-cube-root formula for K_(p^2), a
tangent stationary equation and a degree<=12 polynomial with nonzero
constant on each of at most9 branches. Explicit p=113 witnesses show
both exceptional families can exceed108p. This component is promising
but not needed by the all-integer MODEL proof.

Nine NEW exact tests passed normally in0.195s and under -O in0.151s.
Sol `/root/sieve_review` passed the derivation, corrected classification,
actual files, interval transfer, recursion, exponent costs and fixtures.
This pursuit began09:51:06 UTC and returns `changed-under-evidence`
before its10:21 UTC ceiling. No old experiment or outside action occurred.
Qwen remains unavailable without retry; no manual wake was queued.
Next question: does the exact envelope of combined reviewed model bounds
cover the canonical hyperbola-box domain, or which explicit box remains?
Pay all period/frequency caps and source support conditions in that test.
Full box coverage, original sieve transfer and signed prime correlation
remain OPEN; latest original-affine stays2b8cf98, formal conservation
6f9a77b stays distinct from the signed gap, and polynomial tools survive.
No research process is left running at this checkpoint. The overall goal
remains active, without claiming work during execution gaps.


The next pursuit, **220920c**, closes the smooth MODEL box geometry:
`full_model_box_kernel.py` proves sum_q|E_q|<<Y^(1-1/4096+epsilon)
for ALL integer moduli throughout 1/5<=b<=13/25,
0<=x<=(1-b)/2,0<=y<=1/2, with the stated full period/frequency caps,
nonunit modes, integer axes and overlap. This is not sieve transfer.

Swapping the balanced grouping gives a broad regional theorem with
bare exponent<=63/64 and a paid squarefull cutoff Z=Y^(1/256). The
residual strip requires two new transfers: rectangular divisor shifts
with an arbitrary coupled periodic local factor, and exact grouping of
the completed h,k variables after fixing kappa modulo J. The local
factor remains periodic mod rJ even when q and J share primes. The
prime/two-prime core amplification also retains unequal interval lengths.
The total period cost is J^5; no coupled weight is separated for free.

The grouped recursion L2 mass is merely bounded, not D^-1/2. Small
divisors use the nonnegative modulus powers of the rectangular bounds;
large divisors use their volume1/D. Complementary simple-prime nonunit
partitions pay1/Ds and preserve the local period. The critical residual
exponents at full caps are1-(19/8)/4096,1-(81/16)/4096 and1-2/4096,
all below the uniform claim. Earlier failed combinations and the
prime-square component remain available with their original boundaries.

Eight NEW exact checks passed normally in0.148s and under -O in0.134s.
Sol `/root/sieve_review` passed the theory and actual proof/code/tests.
The checks cover shared periods/nonunit kappa, grouped mass=1 witnesses,
rectangular moment normalization, exact supports/costs and domain cuts.
This pursuit began10:15:59 UTC and returns `changed-under-evidence`
before its10:45:59 ceiling. No old experiment or outside action occurred;
Qwen remains unavailable without retry and no manual wake was queued.

The next test concerns actual arithmetic: can a positive upper-sieve
majorant of a weaker fixed-power cofactor roughness condition preserve
harmonic density while fitting all original sieve-index, period and
frequency costs within the saving? The actual family allows an arbitrary
rough subset, so direct treatment as a smooth/short-period weight is
invalid. Test positivity, density, M's coprimality/discriminant cases
and amplitude regularity explicitly before transferring the theorem.
Original sieve transfer and signed prime correlation remain OPEN;
latest original-affine remains2b8cf98 and formal conservation6f9a77b
still leaves its signed difference unestimated. Polynomial tools survive.
No research process is left running at this checkpoint. The overall goal
remains active, without claiming work during execution gaps.

## 2026-09-09: positive cofactor sieve transfers the full affine range

Started10:43:21 UTC; reassessed before11:13:21, `changed-under-evidence`.
Resumed clean main53eeab1 and model mathematics220920c. New reviewed
mathematics **4e106b6**, `rough_cofactor_sieve_bridge.py`, extends the
ACTUAL rare/rare affine bound to every original rough subset M<=Y^(13/25),
with gcd(M,Dm)=1, in the SAME actual-zero large-V regime. Its bound is
 S_2(m)Yt^2(log eta)^9+Y^(1-rho/2+o(1))+S_2(m)Y eta^-19=o_theta(Yt),
rho=2^-20. It does not supply the missing signed prime estimate.

The concrete test passed: upper-beta positivity plus a NEW weighted mean
sum_(M~B)sigma(M)F_C(M)<<B/log z+R sqrt B yields O(U) harmonic mass.
Small prime factors admitted by sigma are paid by F_C(M), not silently
excluded. Corrected Henriot tails retain exact gcd(M,m)=1 and primitive
forms. The zero mode keeps sigma and has two harmonic cancellations.
Actual nonzero modes have q0=d2*c, conductor D, physical M,a, bounded
periodic character factors and uniformly smooth Fourier amplitudes.
Rescaling Ystar=YR^2 pays Hstar<=DR^4,J<=DR^5 and five indices R^5.
The target-gcd tail costs Y^(1-rho+epsilon), including its zero counterpart.

Independent review required native (M,q0)=1 in every truncated Mobius term;
it is now explicit, along with (M,D)=1. Exact CRT signs agree in both
phases. The inherited Y^(1-theta+o(1)) term is absorbed into Y eta^-20 for
each fixed theta; no theta>=rho/2 condition is assumed.
Primary source correction: MM2112.11412v2 equation(22) must use PLUS its
upper-beta remainder. Exact witness1/3=8/35+11/105; relative-O lemma valid.

Nine new exact guards passed normally0.024s and under -O0.017s. Sol
`/root/sieve_review` reviewed theory and actual proof/code/tests, PASS.
No repeated prime scan, outside action, publication, or manual wake queue.
Qwen remains unavailable without retry. Only coherent local commits.

Next question: does the new bound cover every previously surviving even
one-rare-factor composite under the original pruning and fixed polynomial
weights? Test exact cofactor/character coverage and parameter compatibility;
preserve any missing boundary or class instead of assuming it away.
Formal conservation6f9a77b remains a known-main-term identity, with its
signed difference OPEN. Polynomial tools survive and the goal stays active.
No research process is left running; execution gaps remain gaps.

## 2026-09-09: eliminate all polynomial rare-factor losses

Started11:12:52 UTC, reassessed before11:42:52, changed-under-evidence.
Resumed clean main ddfa2aa, actual affine mathematics4e106b6. New reviewed
mathematics **e5c955d**, rare_class_elimination.py, proves for EVERY fixed
normalized polynomial of degree d, in the ADDED actual-zero large-V regime,
 T_f=P+sum_(3<=k<=d, k odd) C_(k,f)^all-negative+o_(f,theta)(Yt).
Every positive-factor composite class is negligible in FULL ABSOLUTE
weight. The quintic now leaves only pure triples and five-factor partners.
The original W=chi*log has T_W=P+E with 0<=E=o_theta(Yt); normalized
quadratics coincide with W exactly on negative-character units.

The old pruning only used the fixed rough divisor bound. Remaining unique
positive q>floor(Y^a) gives q>Y^a exactly, M=n/q<Y^(1-a)<=Y^(13/25),
chi(M)=-1, (M,Dm)=1 and the exact bridge intervals. Q-dependent restrictions
are dominated by the full nonnegative B_M. Never use the false reciprocal
floor inequality. V>=log^3 eta stays an additional assumption; the original
fixed delta,u and B_good are unchanged.

The Buchstab terminal error E_R is also o(Yt), removing its previous
C*epsilon*Z charge. The remaining one-sided prime-times-rough estimate is
 U_A<=LXV(z_old)-(c+C0*eta_u/theta)*Z,
with the original fixed sieve error and >=q least-factor condition intact.
This estimate and a positive lower bound for FULL T_W remain OPEN.
The exact n=957,R=26 fixture has truncated W=log(33/29)>0 and full W=0,
so nonnegativity of W cannot make its signed truncation a lower bound.

Seven new guards passed normally0.023s and under -O0.021s. Sol reviewed
actual proof/code/tests, PASS after an eta_u notation correction. Finite
S2,S4,S6 character fixtures verify support, not an exceptional zero or
prime coverage. No old experiment, outside action, publication or wake queue.

Next UNTESTED question: compare lambda_chi(p)*W(m-p) with one-variable
rare-prime lambda_chi mass. Its zero mode may pair A_z(p) with the weighted
log moment B_z(m-p); MM Lemma2.4 might calibrate B_z without discarding
A_z. The decisive tests are exact local normalization and relative Yt
errors in prime-to-divisor replacement and sieve tails. Existing errors
of order Yt times logarithmic factors would not suffice for a lower bound.
Keep original fixed-theta and growing-U cutoffs distinct. No new signed
estimate is claimed, and formal conservation6f9a77b remains only its
proved identity. All polynomial components survive. Goal active; no
process remains running and no work is claimed during execution gaps.

## 2026-09-09: actual divisor correlation and the cutoff comparison

Started11:34:38 UTC, reassessed11:58 UTC, changed-under-evidence.
Resumed clean main e436401, mathematics e5c955d. New reviewed mathematics
**2b72af7**, rare_divisor_calibration.py, proves in the SAME ADDED actual-zero
large-V regime, for central suppressed targets and fixed smooth g,
 S_z=G_z Q_z+o(Yt)=S_2(m)t I_g+o(Yt),
with U=K log eta, z=Y^(1/U). This is an actual nonnegative divisor sum.
Q_z=(A/phi(D))t I_g+o(Yt/G_z) is calibrated by one-variable rare primes.
Exact G_z=Sigma_(2,z)phi(D)/A, with the tail1+O(U/z). The four conductor
orientations produce A_z B_z, MM Lemma2.4 gives B_z=2C_z(1+O(E)),
A_z=O(E/U), and the replacement costs S_2 Y E^2=o(Yt). The outside1/2,
Abel factor2, atom1, and absolute signed-integral error are all retained.

Dynamic Q_z composite mass is relatively small by its unique largest
positive prime. This is NOT a dynamic S_z prime-replacement theorem.
Separately, ORIGINAL fixed theta permits first-variable replacement via
an upper prime sieve at modulus Dd, never MDd. Explicit FULL/B_good
pruning control and e5c955d then give S_theta=P_g+o(Yt), with factors
strictly>z_old and equality endpoints paid. Growing-U divisor costs2^U
and fixed-theta sieve errors prevent silently composing the two results.
The difference S_z-S_theta and a positive prime-pair lower bound remain OPEN.

Seven new finite algebra guards passed normal0.008s and -O0.007s. Sol
/root/sieve_review checked theory, actual files, strict endpoints and pool
composition, PASS. No finite test is an exceptional-zero or asymptotic proof.
MM equation22 PLUS correction, corrected Henriot, and Thorner--Zaman bulk
source remain in force. No old experiment, outside action or wake queue.

Next UNPROVED test: expose a prime r in[z,z_old] in S_z-S_theta. Positive
r produces affine lambda/W forms with SMALL coefficient r and one harmonic
cancellation; its reciprocal prime mass may supply a second rarity factor.
Negative r on nonzero squarefree W support produces lambda/lambda and two
harmonic cancellations. Test the DIRECT small-cofactor Poisson proof for
both placements and sum all errors: Q>=Y^(1-theta), r prime, theta<1/5,
prospective nonzero cost Y^(7/9+theta+o(1)). Preserve any failing term.
This comparison could avoid the unproved very-short-interval W estimate;
it has not yet been established. Use a new <=30-minute hypothesis clock.
Kevin reiterated freedom to incorporate other mathematical approaches.
No historical priority, prize entitlement, cash or universal coverage claim.
Overall goal active. No research process remains running at the checkpoint;
execution gaps remain gaps, and all polynomial components stay available.

## 2026-09-09: cutoff bridge and conditional coverage of an entire band

Started11:59:43 UTC, reassessed12:14 UTC, changed-under-evidence.
Resumed clean main1e71488, mathematics2b72af7. New reviewed mathematics
**9b6e7b4**, prime_cutoff_bridge.py, proves S_z-S_theta=o_theta(Yt), hence
 P_g=S_2(m)t I_g+o_theta(Yt)
for suppressed targets in the SAME actual-zero restricted large-V regime.
The explicit cutoff error is S_2Yt^2U^8log(2U)+Y^(7/9+theta+o(1))
+S_2Y eta^-20. This is an ACTUAL prime-pair asymptotic, distinct from
formal conservation6f9a77b. Its proof retains the original fixed parameters.

An intermediate prime r in[z,z_old] yields three nonnegative union cases.
Positive r on either side produces an affine lambda/W sum; one harmonic
cancellation and the positive-prime reciprocal mass O(t) supply two rarity
factors. Negative r on nonzero W support produces lambda/lambda and two
harmonic cancellations, with reciprocal loss O(log U). Since r is small,
Q=Y/r>>Y^(4/5); the direct Poisson proof handles both W placements at
modulus Dd2c. Native(r,d2c)=1 remains until the zero mode. The prior
cofactor theorem's stronger roughness hypothesis is replaced by an explicit
prime-coefficient adaptation, not assumed away. Dynamic removals retain
Y/z exp(O(U))L^C, rather than an unjustified fixed-power slogan.

The source main multiplier1+C/A equals zero precisely on F_D and is >=2/3
otherwise. Its CRT proof explicitly includes a vanishing8-part. MM
Theorem1.4 therefore covers the nonsuppressed classes with relative o(1)
error; proper prime powers cost O(sqrt(m)log^3m). That theorem has NO
upper-V restriction. Combining the two cases proves a prime representation
for EVERY even m in[5Y/4,7Y/4], conditional on the stated ACTUAL zero and
eligible parameter regime. The nonsuppressed pair need not lie in(Y/2,Y].
No eligible zero, numerical interval, effective onset, unconditional coverage
or historical novelty has been established. Other zero regimes and the
unexceptional branch remain outside this theorem; overall Goldbach is OPEN.

Nine new exact tests passed normal0.021s and -O0.021s. Sol checked theory,
actual proof/code/tests and coverage corollary, PASS. Source corrections and
runtime limits persist; no scan, publication, contact, spend or wake queue.

Next UNTESTED question: derive the exact Mobius-weighted Type II remainder
in the unexceptional ramanujan_type_i.py comparison, using Vaughan's
identity, and test whether the existing all-moduli reciprocal kernel can
handle its actual large-factor weights. The model only promises smooth
spatial factors and bounded joint periodic weights; arbitrary Mobius or
divisor coefficients may fall outside it. Cost every norm/frequency loss
before claiming a transfer, or preserve the specific remaining correlation.
Do not rerun completed smooth-model cases or discard polynomial tools.
This lane needs a new <=30-minute hypothesis and independent review.
Goal active; no research process remains running at the checkpoint.

## 2026-09-09: unexceptional Vaughan remainder and coefficient-transfer boundary

Started12:16:10 UTC, reassessed12:29 UTC, changed-under-evidence. Resumed
clean maince40960; conditional coverage9b6e7b4 remains valid. New reviewed
mathematics **a771937**, unexceptional_vaughan_gate.py, isolates
 T=sum_(ab in J,a>V0,b>U0)mu(a)B_U0(b)E(m-ab),
with B_U0=Lambda_>U0*1 and the original unexceptional E=Lambda-M_S.
Both Type I terms and proper prime powers are paid. CROSS+T gives actual
prime-pair mass, but T has NO proved sufficient lower bound.

Generic completion does not transfer the existing model: its sharp
worst-case sqrt(N) coefficient cost exceeds the saved Y^(1/4096), even
if one grants uniform additive-modulation bounds the theorem does not state.
This says nothing about a lower bound for actual Mobius/divisor Fourier
norms. Vaughan's free1 must stay; a finite n=30 guard catches its omission.
Cauchy isolates signed prime/model covariance with exact intersection masks.
Its diagonal is already negligible by a fixed power; only a sufficiently
small one-sided upper bound on the weighted off-diagonal is needed.

Nine finite guards passed normal0.008s and -O0.008s. Sol reviewed theory,
actual proof/code/tests and diagonal delta, PASS. No old scan or outside action.
Next test: keep the free divisor variable explicit in the multilinear
Vaughan terms and attempt a LEGAL Poisson/dispersion transfer, accounting
for every short-variable region including k=1. Full arithmetic Type II,
not its smooth/periodic replacement, is the target. Use a new <=30-minute
clock; preserve any remaining correlation. No unexceptional coverage is
claimed. Goal stays active; no process remains running at this checkpoint.

## 2026-09-09: actual balanced divisor convolution with free variables

Started12:30:54 UTC, reassessed12:45:47 UTC, changed-under-evidence.
Resumed clean main5842cd2. Reviewed mathematics **a968833**, in
free_divisor_correlation.py, retains the exact grouping
 h_r=sum_(ad=r,a>W,d>W)mu(a)Lambda(d), |h_r|<=log r,
 T=sum_(rk in J)h_r E(m-rk).
The tiny floor strip r<=Y^gamma is Type I; larger r with k=1 persists.
Merely keeping that k does not license the saved smooth-model input.

A changed grouping gives a POSITIVE component: after expanding Vaughan
on both sides, for coefficient scales Y^gamma<=R,S<=Y^(51/100), fixed
smooth F and actual separate coefficients bounded by log(2Y),
 sum_(Mk+Nl=m)alpha_M beta_N F(Mk/Y,Nl/Y)
  =Y I_F(m/Y)sum_(gcd(M,N)|m)alpha_M beta_N gcd(M,N)/(MN)
    +O_(F,epsilon)(Y^(1983/2000+epsilon)).
This applies to the arithmetic h_M,h_N themselves. Poisson acts only on
the free k variable; a fixed-box Mellin expansion separates the smooth
coupled factor while preserving the outside arithmetic coefficient norms.
Bettin--Chandee Theorem1 then applies directly. Both source terms, gcd
conditions and divisors of m, negative frequencies, unit reduced variables,
small-frequency padding and the Schwartz tail are explicitly included.
The two worst exponents are1983/2000 and153/160, a17/2000 margin.

This is a restricted ACTUAL coefficient convolution, beyond the prior
smooth/periodic model input. Its SIGNED gcd main is still explicit. No
positive prime main, bound on all larger factors or mixed terms, or full
unexceptional T=o(Y) follows. Conditional coverage9b6e7b4 and previous
polynomial/model components remain unchanged. In particular, the failed
old cofactor grouping and generic Fourier-completion budgets are preserved
as method-specific limits, not broad impossibility assertions.

Eight exact guards passed normal0.003s and -O0.002s. Sol reviewed theory
and the actual proof/code/tests, PASS. No scan, publishing or other outside
action occurred. Next bounded question: compare the signed gcd main with
the small-modulus Ramanujan projection of the same coefficients. The test
must pay the q>Y^delta tail and check whether an actual term of T cancels;
an exact main-term rewrite alone will not close the remaining estimate.
Keep all large-product and mixed remainders explicit, and start a fresh
<=30-minute clock. Goal active; no process remains running at checkpoint.

## 2026-09-09: balanced self-correlation removed by an actual Type I transfer

Started12:47:52 UTC, reassessed12:58:25 UTC, changed-under-evidence.
Resumed clean main7eff067. Reviewed mathematics **476e0c3**, in
balanced_projection_transfer.py, composesa968833 with the earlier TI input.
For B(n)=sum_(r|n,Y^gamma<r<=Y^.51)h_r, its exact Ramanujan coefficients
H_B(q)=sum_(q|r)h_r/r satisfy |H_B(q)|<<L^2/q. Set Q=floor(S^2),
P_Q=sum_(q<=Q)H_B(q)c_q and Z=B-P_Q. The signed gcd main has exact
coefficient sum sum_q c_q(m)H_B(q)^2; its tail is <<L^4tau(m)/Q.
Matching BB, BP, PB and PP mains and paying all interval errors gives
 |C_F(Z,Z)|<<Y^(1983/2000+epsilon)+YL^4tau(m)/Q
               +Y^.51 L^3Q^2+L^4Q^4
           <<Y^(1-2delta+epsilon)
for fixed smooth F. This is an ACTUAL self-correlation bound.

The initial idea that P_Q might equal Gamma_S is unnecessary and is not
asserted. Its coefficients differ from the prime model. Crucially P_Q
itself has exact divisor coefficients p_d<<L^3 supported on d<=Q<=Y^gamma,
so the existing TI estimate bounds C_F(P_Q,E) by every fixed logarithmic
saving with E unchanged. For A=VaughanII, H=A-B and R=E-Z,
 T_F=C_F(A,E)=C_F(Z,R)+C_F(H,E)+C_F(Z,Z)+C_F(P_Q,E).
Thus only the first two correlations remain after the proved small terms
are removed. R retains all mixed terms and P_Q-Gamma_S. No Cauchy or sign
claim is inferred from a small additive self-correlation. The TI error
remains logarithmic, separate from the power-saving self-correlation.

For n=pq, distinct primes p,q>W, only h_n=-log n is nonzero among h_r
with r|n; for n=p^2, h_n=-log p. When n is comparable to Y these k=1
terms remain entirely in H. No unexceptional prime lower bound, new
coverage or sharp-cutoff upgrade follows. Earlier conditional coverage,
polynomial identities and analytic components remain intact.

Eight guards passed normal0.009s and -O0.010s. Sol theory/actual-file
review PASS. No previous experiment, scan or outside action was repeated.
Next test: verify a multi-factor prime identity from a primary source and
ask whether it supplies new long free variables in the remaining H.
Use the complete factor-size domain, including all-short-free-variable
terms, as the falsifier; retain actual Mobius/log coefficients and cost
every reciprocal-estimate norm. A formal decomposition alone is not the
missing estimate. Start a fresh <=30-minute clock with independent review.
Goal active; no process remains running at this checkpoint.

## 2026-09-09: multi-factor identity boundary and divisor-weighted Type I

Started13:01:48 UTC, reassessed13:16:56 UTC, changed-under-evidence.
Resumed clean main29b35c9. Reviewed mathematics **b7134e1**, in
multifactor_identity_gate.py, adds the actual unexceptional estimate
 sum_(d<=Y^gamma)tau_s(d)L^b Delta_d <<_(A,s,b)Y/L^A
for FIXED divisor order s and log power b. The proof combines
Delta_d<<YL tau(d)/d+S^4 with tau_s^2 tau_2<=tau_(2s^2) and Cauchy;
the input TI saving2(A+b)+2s^2+1 pays the whole coefficient moment.
This preserves a useful extension for actual grouped arithmetic weights.

The Heath-Brown identity was verified from Tao's2013 subset-sum post and
proved with its exact residual mu_>z^{*K}*1^{*(K-1)}*log. The residual
vanishes below2(z+1)^K, but at K2,z2,n18 equals+log2. A raw top-order
term can have all Mobius variables of scaleY^(1/K) and all free variables
bounded: Y=3p^K, n=2p^K, log variable2 gives the nonzero tuple -log2.
Thus the identity plus TERMWISE application of existing TI/free-variable
BC bounds does not cover every factor box. Grouping Mobius factors into
balanced products retains arithmetic weights; it does not create a free
variable. The optimistic r=s=1 source budgets9/5 and15/8 also fail.

The raw witness cancels in the FULL identity at that composite n. It is
not a lower bound for actual H, a Goldbach counterexample, or a barrier
to cross-term cancellation. Some squarefree smooth inputs already have
original Vaughan A=0. Source MPZ distribution estimates are not our
pointwise correlation input, and no excluded or blocked old route was reused.

Useful restricted components remain: genuine free factors of scale
>=Y^(1-gamma+eta) are controlled by divisor-weighted TI; paired terms
with one original free1 per side and complementary products in the saved
[Y^gamma,Y^.51] range admit the BC proof with fixed divisor-moment norms.
The reviewer corrected a coefficient description: leaving log free removes
the grouped coefficient's L, but its safe divisor order remains2j-1;
the free log variation is paid separately. All parameters remain fixed.

Eight guards passed normal0.006s and -O0.005s. Sol theory/actual-file
review PASS after that correction. No coverage, scan or outside action.
Next test: combine specific HB terms before absolute estimates, derive the
short-free coefficient, and check whether its cancellation gives a bound
against the unchanged E. A reconstruction of Lambda or a prime/roughness
support restriction alone is insufficient. Preserve the exact unresolved
signed correlation if no new estimate results; do not discard the useful
divisor-weighted TI or earlier polynomial/model components. Use a fresh
<=30-minute clock and independent review. Goal active; no research process
remains running at this checkpoint.

## 2026-09-09: actual prime-slot pruning and combined short HB coefficient

Started13:18:59 UTC, reassessed13:37:41 UTC, changed-under-evidence.
Resumed clean maina4a7944. Reviewed mathematics **3fcea6e**, in
short_free_cancellation.py, removes INTERNAL proper prime powers from
A=mu_>W*Lambda_>W*1. For A_p with Lambda_>W restricted to actual primes,
 sum_(n<=Y)|A-A_p|(n)<<Y W^(-1/2)L^3,
 |C_F(A-A_p,E)|<<Y^(1-gamma/4+2delta+o(1))=o(Y).
The positive tuple proof survives support restrictions. For
S_W(c)=sum_(a|c,a<=W)mu(a), the exact remaining prime/cofactor formula is
 T_F=-sum_(p>W prime,c>W)log(p)S_W(c)
                  F(pc/Y,(m-pc)/Y)E(m-pc)+o(Y).
The sum is over distinct prime divisors, not multiplicities. S_W is signed;
rough distinct semiprimes have A_p=-log n, squares p^2 have-log p.
Both linked prime conditions remain and their signed correlation is OPEN.

For the combined all-short HB sector, z=floor(Y^(1/K)), T=floor(Y^eta),
0<eta<1/[K(K-1)], only j=K survives at n~Y eventually. At Y=3p^K,
n=2p^K, 2<=T<p, its ENTIRE coefficient is-log2, though full Lambda=0.
Thus the previous single-tuple witness does not cancel within this sector.
The exact factorization [delta-(delta-mu_<=z*1_<=T)^K]*Lambda_T uses the
truncated logarithmic derivative, not Lambda. Its inverse expansion has
finite fixed depth J<1/eta, with paid divisor orders2J+1 and2J+2.
This preserves a useful algebraic component but supplies no C(S_short,E).

The actual A_p vanishes on final W-smooth numbers. For HB in the INTERNAL
Lambda(d) slot and K>=5, short d is z-smooth with z<W; only the FULL
restored Lambda(d), d>W, restricts to proper powers and is negligible.
Raw HB short terms may be nonzero at composites and need compensation.
Final n=adk need not be smooth. No such removal is proved for HB in E.
No coverage or bound on the full remaining correlation follows; earlier
balanced projection, divisor-weighted TI, polynomial and conditional
coverage results all remain valid.

Eight exact guards passed normal0.006s and -O0.008s. Sol theory and
actual-file review PASS, no correction. No scan or outside action.
Next test: derive an exact smoothed-cutoff Vaughan identity, including
compensation, and determine whether its actual cofactor second moment
improves the prime-correlation budget after Cauchy. A smaller coefficient
norm is not prime covariance; retain that distinction. The narrow search
found no completed equivalent pursuit. Fresh <=30-minute clock required.
Goal active; no research process remains running at this checkpoint.

## 2026-09-09: exact cutoff freedom and a failed optimal-norm budget

Started13:39:04 UTC, reassessed13:51:50 UTC, changed-under-evidence.
Resumed clean main45afe67. Reviewed mathematics **02e1627**, in
optimized_cofactor_cutoff.py, proves the exact generalized Vaughan identity
for any bounded real lambda supported d<=V with lambda1=1. If U,V,UV are
within Y^gamma, its compensating terms are controlled by existing TI;
the actual remainder changes by O_A(Y/L^A). Internal proper-power pruning
persists, but arbitrary lambda can introduce small cofactors c>=2.

The exact cofactor norm is C Q(lambda)+O(||lambda||1^2), with the endpoint
error<=V^2. The classical Selberg minimum Q=1/G(V), G(V) asymp logV,
has a bounded admissible optimizer. This known theorem was checked in
Steve Lester's2015 notes, proof printedpp5-7, and independently derived.
For balanced C~sqrtY and V=W, the best bounded norm is asymp C/logV.
It remains signed: V3 gives S(2)=1/5 and S(6)=-2/5. One must not square
S to create a positive sieve weight while retaining the original identity.

An actual E second-moment bound O(YL) follows from Chebyshev, Ramanujan
orthogonality and the paid S^8 period error. Separate pairwise Cauchy then
gives only O(YsqrtL) for one balanced box, even at the optimal norm.
This is a failed upper-bound calculation, not an actual lower bound or a
no-go theorem for polynomial weights. The exact cutoff freedom and optimal
weights are preserved. Revisit only with a stronger JOINT moment or signed
covariance estimate, not another shape in the same norm-only family.
Keeping the prime sum intact gives the sufficient balanced energy target
H<<Y^2/(C L^5); its diagonal is O(Y L^3), while the weighted off-diagonal
remains OPEN. No new coverage or full remainder estimate follows.

Eight exact tests passed normal0.018s and -O0.020s. Sol theory/actual-file
review PASS without correction. Next question: can the fixed polynomial
cutoff (1-log d/log V)_+^k, k>=9, be dominated by the corrected radical
majorant H_V/logV, then paired with H_S(m-pc) using corrected Henriot to
prove an actual per-box O(Y S_2(m)/logY) bound? Check primitive forms,
coefficient-size and interval conditions, p|m, prime powers and summing
all boxes. This is proposed, not proved. Reuse the existing corrected
source; do not retry blocked fetches. Fresh <=30-minute clock required.
Goal active; no research process remains running at this checkpoint.

## 2026-09-09: polynomial weights obtain an actual joint arithmetic bound

Started13:54:01 UTC, reassessed14:09:07 UTC, progress. Resumed clean
main35cc1e4. Reviewed mathematics **c19cb24**, polynomial_joint_majorant.py,
uses lambda(d)=mu(d)(1-log d/logV)_+^k, fixedk>=9. The full cutoff change
is licensed by existing TI. Mellin inversion gives |S_lambda|<<H_V/logV,
using the corrected radical majorant. The actual E is dominated by H_S;
H_S(ell^j)>=(511/1152)min(logell,logS) also handles prime powers directly.

For p prime not dividing m, corrected Henriot on c and m-pc has primitive
forms, normO(Y), discriminantm^2 and uniform hypotheses for fixed cofactor
exponents1/4<c0<=c1<1-gamma/2. Its special leading-prime factor is
K_p=1+a/p, rho1, with sieve ratio at most2. The corrected zero-valuation
and common-root conventions remain essential. The result is
 sum_c H_V(c)H_S(m-pc)<<C S_2(m)/(dV dS),
which supplies the actual joint bound missing from separate Cauchy.
Chebyshev then gives each prime/cofactor box a positive tuple majorant
O(Y S_2(m)/logY). Globally p|m costsY^(1-gamma/2+2delta+o(1)); the
previous internal-power error is paid once too. This bound accepts any
bounded tuple mask, but the full TI cutoff transfer keeps its smooth F.
It does not equate restricted old hard-cutoff boxes with the new boxes.

OnlyO(1) cofactor boxes fit a prime box under pc~Y. A union of N boxes
costsO(N Y S2(m)/logY), so o(logY) boxes are negligible RELATIVE to YS2.
A fixed polylogarithmic band near sqrtY is controlled; an exponent band
of widthh costsO((h+1/logY)Y S2), uniformly in a fixed domain. The full
positive-width range still hasTheta(logY) boxes and only a main-scale
bound. No signed full-remainder estimate or new prime-pair coverage.

Eight guards pass normal0.004s/-O0.003s. Sol theory/actual-file PASS after
one endpoint correction: J_p lies in a closed enclosure, covered by two
comparable half-open intervals. The initial guard also caught a float
created by an integer max branch; Fraction endpoints now have type tests.
No blocked fetch, previous experiment, or outside action was repeated.

Next question: can a full absolute bound even be o(Y S2(m))? Every
normalized cutoff has S_lambda(c)=1 on prime c>V. Test a lower bound from
actual prime triples pc+q=m averaged over central even m, paying the
fixed-small-delta condition for E(q)>0 and the singular-series average.
This is a proposed falsifier of absolute summation, not of signed methods
or the preserved polynomial/affine component. Fresh <=30-minute clock.
Goal active; no research process remains running at this checkpoint.

## 2026-09-09: actual absolute remainder mass survives every normalized cutoff

Started14:11:13 UTC, reassessed14:21:20 UTC, changed-under-evidence.
Resumed clean main65bf94b. Reviewed mathematics **dc7baa6**, in
absolute_remainder_obstruction.py, proves a full absolute-sum obstruction.
The explicit setup adds delta<=1/(80B), B=max(1,||G||infty), to the
existing delta cap, and fixes nonnegative smooth F>=f0>0 on[.7,.8]^2.
For every sufficiently large Y, SOME central even m in(1.4Y,1.6Y] has
regrouped absolute mass at least(f0/32000)Y S_2(m), SIMULTANEOUSLY for
all normalized bounded cutoffs supported<=V=W. This holds for full
R_lambda, its prime restriction, original hard A, and tuplewise triangle.

For actual prime q~Y, Gamma_S(q) is a constant B_S<=logY/4 eventually,
so E(q)>=logY/2. At a distinct-prime semiprime pc with both factors>W,
the actual coefficient is-log(pc) for every cutoff. Selectp in(Y^.3,Y^.4]
and pc,q in(.7Y,.8Y]. PNT in fixed-relative intervals and partial summation
give f0Y²/16000 total mass over m=pc+q. The triple-to(m,n) map is injective;
p is the unique lower prime factor. No fixed-target prime independence
or actual exceptional zero is assumed. PNT primarycheck: Tao Notes2,
Corollary39/Exercise40(2014), not the excluded Notes7 proposition.

A positive divisor expansion gives the exact mean bound
sum_(m even<=2Y)S_2(m)<=2Y, using the local Euler cancellation
(1-1/(ell-1)^2)(1+1/[ell(ell-2)])=1. The same cutoff-independent
nonnegative mass supplies the same pigeonholed target for every cutoff,
even target-dependent choices. The onset remains nonnumerical.

This rules out uniform relative smallness of the FULL ABSOLUTE remainder,
even after grouping at each n. It makes no lower bound on the absolute
value of the SIGNED total. Other parts may cancel the selected negative
component; Goldbach and the full signed estimate remain open. The joint
polynomial/affine box bound is still useful for narrow ranges. All other
polynomial, TI, projection, source-correction and conditional-coverage
components remain preserved. Repeating full absolute summation with a
new normalized cutoff cannot evade the proved obstruction.

Six exact guards passed normal0.003s/-O0.003s. Sol theory/actual-file PASS,
no correction. A single explicit prime triple tests geometry/coefficient
normalization only; no range scan or numerical asymptotic claim.
Next test: match an actual beyond-half prime-AP theorem to the signed
moduli p*d, retained prime/Mobius/polynomial weights, and moving residue
m~Y. Check uniformity, factor geometry, noncoprime cases and the model
comparison error before importing any distribution conclusion. This is
unproved; a label such as MPZ or well-factorable is insufficient. Fresh
<=30-minute clock required. Goal active; no research process remains running
at this checkpoint.

## 2026-09-09: actual signed component gains a beyond-half distribution input

Started14:24:20 UTC, reassessed14:38:06 UTC, progress. Resumed clean
main6d0a20b; reviewed mathematics **06acf3b**, factored_prime_ap_transfer.py.
Maynard III arXiv:2006.08250v1 Thm1.2 printedp3 has sufficient uniformity
for the actual moving target m. Its absolute discrepancy over factored
moduli allows retained prime and bounded Mobius/polynomial coefficients.

Fixed source sigma1/2000, exponents(.3935,.025,.082), and actual cap
exponents(.3934,.0249,.0819) give a real restricted levelY^.5002. The
strict power slack makes the SAME source parameters valid at all endpoints
in[Y/2,Y]. Select pairs(p,d) with p>U=V=floorY^(gamma/2), d<=V, and
d=h*a*b where p*h,a,b obey those caps. Each modulus has a unique prime
factor>V; one canonical ordered triple avoids multiplicity and allows
composite p*h. This generalization retains h>1. Modulus-only bounded masks
are allowed, including pd>sqrtY. Arbitrary k-dependent masks are not.

The selected ACTUAL signed sum against the unchanged E=Lambda-Gamma_S
is O_A(Y/log(Y)^A) for every fixedA. Common-weight Abel costs two logs;
ordinary strong PNT, checked in Tao2014Notes2 Cor39/Ex40, pays the change
from pi to real density. The elementary Gamma comparison extends to
D=Y^.5002 with YL S^-1/2 exp(O(sqrtL))+D S4 and endpoint costs, all
power-small at modeldelta<=1/4800. Nonreduced Gamma is retained in these
errors; only its FULL mean is0. Nonreduced prime partners are impossible
eventually, and proper powers costY^(.5+o(1)) by divisor counting. The
c=1 compensation vanishes in this component because p<Y/2; d1,k>1 stays.

The direct Maynard II triply-well-factorable import fails both its fixed-a
uniformity gate and an exact support test: balanced factorization forces
coefficients with prime factor>Q^(1/3) to0, but our p>Y^(gamma/2)>Y^(5/24)
exceeds even the maximal allowed cube-root levelY^(1/5). Level padding
does not help. This preserves the polynomial tools for other combinations.

Seven finite guards pass normal0.003s/-O0.003s; Sol theory/actual-file PASS.
PNT normalization and truncated nonreduced Gamma were explicitly checked.
Oxford accepted-PDF403 preserved; readable arxivv1 supplied primary text.
No scan, installation, foreground action or manual wake was performed.

This is an actual partial estimate, not full beyond-half TI, new coverage,
or a percentage of Goldbach solved. Next test: do two-prime moduli with
factor exponents near(.30,.20) leave positive logarithmic coefficient mass
outside EVERY permitted source factor geometry? Check all parameter
inequalities, then identify the exact signed estimate needed there. A
coefficient-mass lower bound would not itself bound the actual correlation.
Do not repeat the cap calculation without a new discriminator. Fresh
<=30-minute clock required. Goal active; no research process remains running
at this reviewed checkpoint.

## 2026-09-09: every admissible factor choice leaves an actual weighted family

Started14:39:59 UTC, reassessed14:52:29 UTC, changed-under-evidence.
Resumed clean main10321f3. Mathematics **6a7c8ac** extends the existing
factored_prime_ap_transfer.py with the source-universal exclusion and an
exact next variance target; the prior good-modulus result stays valid.

All Maynard III Theorem1.2 choices have Q2<x^.05,Q3<x^.1,Q1<x^.4.
Thus rough moduli with least prime factor>x^.1 and size>x^.4 cannot fit.
Primes p in(Y^.3,Y^.30002] and d in(Y^.2001,Y^.20012] supply excluded
moduli inside(Y^.5001,Y^.50014], below the prior numerical capY^.5002.
This excludes every admissible factor choice and endpointx in[Y/2,Y],
not merely one cap selection. Other distribution theorems remain eligible.

For fixednu=gamma/2 and polynomial degreek>=9, coefficients
A_pd=logp(1-logd/logV)^k are positive and
sum A_pd/phi(pd)=c logY+o(logY), c=(.00002)*integral_.2001^.20012
(1-b/nu)^k db/b>0. StrongPNT proves this actual density-weight statement.
The same leading constant survives uniformly after removing(pd,m)>1.
The Gamma progression calculation then gives an ACTUAL MODEL main
c I_F(m/Y)YlogY+o(YlogY). Constants may be tiny; onset is not numerical.
These facts do not estimate the difference with the actual prime partner.
Neither all cutoffs nor growing degrees are excluded by the mass statement.

The exact open centered sum is T_family=P_family-G_family. Its proper
prime-power part is paid. With R=Y^.50014 and B_r the unchanged E sum
in the progression m modulo r, H=sum_family|B_r|^2 has sufficient target
H=o(Y^(74993/50000)). Indeed the ACTUAL coefficient norm is asymptotic
to(a1/b1)(1-b1/nu)^(2k)R and exact Cauchy applies. The variance diagonal
is O(YlogY), since at most3 family moduli divide any n<=Y; the possible
positive prime-divisor counts are(1,1),(1,2),(1,3),(2,1). This uses the
existing actual E second moment, not a new assumption about prime pairs.
An upper bound on the real off-diagonal is still missing; its linked
partners satisfy q1-q2=r(j2-j1) with a common two-prime modulus r.

Thirteen finite guards pass normal0.003s/-O0.003s; Sol theory/actual-file
PASS, including the intact variance extension, no material correction.
No new source fetch, range scan, install, foreground work or wake queue.
Next test: completion/dispersion for this exact off-diagonal, comparing
the needed exponent to retained composite Kloosterman estimates while
paying actual-prime coefficient transfer. A smooth MODEL saving alone
does not license the result. Do not repeat cap optimization or the already
paid norm/diagonal. Fresh <=30-minute clock; the overall goal remains active.
No research process remains running at this reviewed checkpoint.

## 2026-09-09: strong generic error controls still permit coherent resonance

Started14:54:20 UTC, reassessed15:12:23 UTC, changed-under-evidence.
Resumed clean maind87403b. Reviewed mathematics **bd7d1e4**, in
resonant_semiprime_error.py, constructs an ARTIFICIAL errorE_* which
passes the proposed generic controls but defeats the family correlation.
This is a transfer-input countermodel, not Lambda-Gamma or a Goldbach claim.

For the same two-prime rectangle and m0=3Y/2, define
E_*(q)=1_I(q)sum_(p,d)c_pd(m0-q)/(pd). Exact factorization is
f(N)=(s(N)-C_P)(t(N)-C_D), where s,t count prime divisors in the two
intervals and C_P,C_D are their reciprocal sums. PNT makes eachC<=.001.
Thus |E_*|<=4, sum|E_*|^2<=16Y, but E_* is>1/2 on every selected
progression q=m0-rj in the physical interval. The primitive full-pd
denominator removes all proper-divisor mean resonances.

For gamma49/100, the interval-maximum Type I sum is O(Y^.99014/logY^2),
uniformly in shifts. This includes h sharing a prime with pd: each exact
zero-mean component has endpoint error<2. The general permitted gamma
range for this proof is5/12<gamma<1-s1, not everygamma<1/2. Farey spacing
and interval-kernel packing prove Fourier supremumO(Y^.50018 logY).
The same E_* nevertheless has H_*>>Y^(2-s0)/logY^2, exceeding the
old sufficient variance scale, and its actual-polynomial family sum is
>>YlogY. These are rigorous artificial-sequence claims, not measured prime
asymptotics. No actual prime support, CROSS or equalityE=Lambda-Gamma.

The next actual variance formulation uses w=A_r/r, M=sumw~cL,
e_r=rB_r/Y, K=sumw|e_r|^2. Exact Cauchy gives|T/Y|^2<=M K, so
K=o(1/L) is sufficient. Its ACTUAL diagonal is O((Rmax/Y)L^2), negligible.
The weighted real off-diagonal stays open; E_* givesK_*>>L. Review
corrected an ordering claim: this condition and the old unweighted one
are nonordered alternatives, with different endpoint/logarithmic costs.

Six guards pass normal0.007s/-O0.009s; independent Sol theory/actual-file
PASS. No source refetch, prime-range experiment, install, foreground work
or manual wake. Next test: restore the COMPLETE signed cutoff identity
against this resonance and check cancellation between divisor sectors,
using the actual-first-prime support and paying cutoff compensation.
The result for artificialE_* would not estimate the actual signed prime
correlation. Preserve prior identities, actual partial estimates and gaps.
Fresh <=30-minute clock; goal active. No process remains running here.

## 2026-09-09: complete layers cancel, so isolated rectangle control is optional

Started15:14:58 UTC, reassessed15:33:15 UTC, changed-under-evidence.
Resumed verified clean maina650b77. Reviewed mathematics **cb04788** extends
resonant_semiprime_error.py sections8-11. A useful routing correction came
from reapplying the saved cutoff freedom02e1627; no new distribution theorem.

For any subset J of nontrivial d<=V, w_d=-lambda_d, the exact full layer
sum_(d in J,b>U,db|n)w_d Lambda(b) equals a log-weighted d-divisor sum
minus a low-b divisor sum at moduli db<=UV. The latter coefficients are
bounded by log(db). Existing TI and the saved internal-power pruning prove
the complete PRIME layer is O_A(Y/L^A) against actual E=Lambda-Gamma_S.
The same holds for the diagnostic E_*. No c=1 appears because d>=2.
Further prime/cofactor masks do not retain this full identity automatically.

Consequently the old D-band, summed over p>U outside P, equals the negative
of its P-rectangle correlation plus a negligible error, for ACTUAL E too.
It is unnecessary to force the isolated rectangle variance small just to
remove this complete layer. Preserve those sufficient variance conditions,
their generic countermodel and the actual factored-modulus estimate, but
retire that variance as a required next gate. Zeroing all d>1 leaves
lambda=delta_1 and exact remainder -sum_(p|n,p>U,n!=p)logp. This retains
the same missing prime compensation; it is not a Goldbach proof.

The diagnostic cancellation is explicit: selected prime bases have no
powers in the physical window, so its actual-first-Lambda pairing is
C0 I_FY+O_A(Y/L^A), C0=log(a1/a0)log(b1/b0)>0. Complete compensation
and pruning give the same full R_lambda,p pairing for every bounded
normalized cutoff. Meanwhile the isolated polynomial rectangle equals
(1-C0)c I_F YlogY+O_A(Y/L^A); its same-D complementary prime range is
the negative at that precision. The full remaining sectors also carry
C0 I_FY. The exact extra-prime product vanishes only under2(a0+b0)>1;
counting error exponent .80016 and reciprocal errors are power-small.
Keep I_F>0, guaranteed by F>=f0>0 on the saved rectangle. These E_*
statements do not estimate actual prime pairs or refute a one-sided bound.

Ten finite guards pass normal0.019s/-O0.016s; Sol theory and actual-file
PASS, no correction beyond the explicit positive-integral requirement.
No source fetch, repeated range experiment, install, foreground input,
publishing/push, or manual wake queue. All source/runtime corrections stay.

Next concrete test: derive the precise one-sided prime-factor inequality
over m-q (q prime, m fixed) required after an asymmetric U=Y^gamma,
lambda=delta_1 reduction. Check for a tautological restatement first; then
test proposed arithmetic input for the needed sign/constant and uniform
m~Y, rejecting averages over m or results only for shift1. This next test
is unperformed. Fresh <=30-minute clock; overall research goal active.
No research process remains running at this reviewed checkpoint.

## 2026-09-09: the largest-factor route needs a prime-scale endpoint deficit

Started15:34:56 UTC, reassessed15:52:58 UTC, changed-under-evidence.
Resumed verified clean main4adb690. Reviewed mathematics **cb01376**,
prime_factor_endpoint_gate.py, answers the fixed-target factor question.

The asymmetric legal cutoff lambda=delta_1, U=floor(Y^gamma), makes the
complete B_U(n)=sum_(p|n,p>U)logp moment TI-small against actual E after
paid power pruning. With C_U its composite restriction, define exact
A_C=sum C_U(n)Lambda(m-n)F and M_B=sum B_U(n)Gamma_S(m-n)F. Then actual
weighted Goldbach mass G_F=M_B-A_C+O_A(Y/L^A). The missing one-sided
input is A_C<=M_B-kappa Y S_2(m). This is not supplied by the identity.
Existing Gamma comparison gives M_B=Y I_F(L-K_U(m))+Y J_F+small, with
K_U=sum_(h<=U,(h,m)=1)Lambda(h)/phi(h). Its coarse leading expansion is
(1-gamma)I_F YL+O(YloglogY), too imprecise at the desired deficit scale.

The actual odd-variable endpoint is exact: n in(Y/2,Y] is prime iff
P+(n)>Y/3. Any fixed-power threshold Y^theta, theta<1, admits composites
3p with Y=4p eventually. No fixed-target 3p+q lower bound is claimed.
Moreover, the classical parity sequence a_n=1+Liouville(n) has no prime
support and satisfies every local-density, congruence and level1 hypothesis
of Bharadwaj--Rodgers Theorem7. Strong all-log Liouville sums follow from
Tao2014Notes2Ex41 and the square-convolution identity. The source theorem
therefore gives full fixed-dimensional Poisson--Dirichlet factor limits
even though the prime event has probability0. Its local densities are not
those of the actual prime partner. The distinction between all fixed c<1
and the moving endpoint is essential: c=1 has discrepancy at least x/logx.

This is a source-checked application and input limitation, not new prime
coverage or a rejection of polynomial tools. Li arxiv2508.18285v1's reported
fixed-shift factor threshold does not supply the needed endpoint/uniformity;
no estimate from its numerical sieve is used. Preserve all source corrections.
Seven guards pass normal0.008s/-O0.006s; Sol actual-file PASS after explicitly
recording all condition(B) clauses. The first sign fixture had H(10)=0;
H(9)=-1 supplies the corrected nonvacuous guard. No mathematical correction.

Next test: recover the cubic-rough prime/semiprime Liouville split from
factored_linear_barrier.py and write the exact signed sum against a PRIME
partner q, n=m-q. Check whether an arithmetic correlation theorem supplies
a useful negative margin with these unaveraged moving-target quantifiers.
Do not repeat the failed one-dimensional sieve plug-in. Fresh <=30 minutes.
Overall goal active; no research process remains running at this checkpoint.

## 2026-09-09: the rough Liouville bias exists; its prime-partner transfer is open

Started15:56:23 UTC, reassessed16:09:06 UTC, changed-under-evidence.
Resumed verified clean main6dee23f. Reviewed mathematics **ed0d334**, in
rough_liouville_transfer_gate.py, completed the signed-parity source test.
Strict cubic roughness leaves primes and semiprimes including squares.
With the actual prime partner and nonnegative log/F weight, A=C+G and
Q=C-G exactly. Q<=-kappa Y S2(m) would suffice for G>=kappa Y S2(m);
this stronger-than-necessary estimate remains OPEN.

The saved PNT and semiprime integral do prove a useful free-variable bias:
sum R(n)ell(n)logn g(n/Y)=(log2-1)Y integral g+O_g(Y/logY), fixed C1 g
compact in(.5,1). Thus uncentered uniform o(Y) Fourier cancellation after
inserting R is false at frequency0. This does not exclude a centered model.
Exact inclusion-exclusion has positive outer coefficients and inner ell:
R(n)ell(n)=sum_(d|n,d|P(z))ell(n/d). For fixed gamma<1 its d<=Y^gamma
layer is all-log small by the saved Liouville summatory bound and Abel;
the long-d layer carries the free negative mean. It is not rough support,
and neither layer estimate has been transferred to q prime in dk+q=m.

Source-fit conclusion: Lichtman2009.08969v2 averages multiplicative shifts;
its typical-factor cancellation set is disjoint from cubic roughness,
and Theorem6.2 leaves the bad-set contribution. Mangerel2404.12117 treats
full unweighted convolution; its2412.17199v1 GRH followup gives unmasked
sign patterns, with quantitative frequency for prime targets. Neither
supplies our fixed-even-target masks. Krishnamoorthy2608.13266v1 Thm2
is only an averaged binary exceptional-set estimate; no other claim used.
No new prime coverage, historical novelty, or missing signed estimate.

Sol theory/actual-file PASS without material correction. Sixguards pass
normal0.008s/-O0.007s. Preserve all polynomial components and source/runtime
corrections. The OUP IMRN request later returned Internal Error; its earlier
full-text receipt and arxiv route are retained. No installs, spending,
contacts, publication/push, foreground work, or manual continuation queue.

Next concrete test: check Ford--Maynard(b.1)/(b.2) against the existing
nonnegative comparison in composite_bilinear_bridge.py, then identify
which Type II factor region could give a positive lower bound. Do not
repeat its old Vaughan sufficient-condition proof or confuse arbitrary
coefficient Type II with the saved restricted factored-modulus input.
Retain the exceptional-character obstruction to uncorrected asymptotics.
This application test is unperformed. Fresh <=30-minute clock on resumption.
Overall goal active; no research process remains running at this checkpoint.

## 2026-09-09: actual critical composite mass replaces pointwise boundedness

Started16:11:58 UTC, reassessed16:36:57 UTC, changed-under-evidence.
Resumed verified clean main8a3f971. Reviewed mathematics **a301a46**, in
prime_producing_comparison_gate.py and critical_factor_mass.py.
The saved nonnegative comparison satisfies source(b.1)/(b.2), growth and
fixed-divisor-weighted Type I below1/2. Its convex factor-pattern law uses
a last-prime BV/fundamental-lemma transfer with sum1/M=O(1) error payment.
It is not an actual prime-partner Type II estimate.

A positive new component: with P_e=(1/2-e,e,1/3-2e), the critical rough
composite region lies in O(e)-wide semiprime bands near halves or thirds,
and a triprime band near thirds. A two-affine-form upper sieve proves
its actual Lambda(2x-n) mass <=C e S2(2x)x/logx+o(x/logx), C absolute.
Given the additional full tau-bounded Type II estimate for
(x/2)^e<d<=x^(1/3-e), Ford--Maynard's decomposition yields prime mass
>=(1-C'e+o(1))B_P, hence positivity for sufficiently small fixed e after
proper-power removal. The actual signed estimate is OPEN. The proof does
not invoke the failed pointwise divisor bound; its model(b.2) input is
separately available but unnecessary for this particular projection.
No new unconditional Goldbach coverage or numerical onset is established.

The bounded source variant fails for actual w at x=p prime, and no common
positive scalar repairs both of Eq4.1's requirements. The printed p17
counterexample needs zero off support and pointwise K_x(t), since its
constant K leaves a positive x/log^2x secondary term. A corrected restricted
construction is proved; no unrestricted theorem is imported from it.
Source PDF >= comparisons in Thm2.2(A1) and Lemma7.18 are retained.
Eight guards pass normal0.007s/-O0.006s; independent Sol theory and actual
files PASS. Prior source/runtime limits and polynomial tools are preserved.

Next bounded question: extract an actual bilinear coefficient family from
the g(empty)=1 decomposition before the generic supremum, and test whether
its retained Mobius/log structure gives a usable existing arithmetic input.
Reject a mere renaming of the open prime correlation or completed TI work.
This is unperformed; fresh <=30-minute clock next pursuit. Overall goal
active, no manual wake queue, and no process claimed running after closeout.

## 2026-09-09: actual localization to rough squarefree Mobius coefficients

Started16:39:03 UTC, reassessed17:01:31 UTC, changed-under-evidence.
Resumed verified clean maind2379cb; reviewed mathematics **3def1c4**, in
specialized_sieve_coefficients.py. The source coefficient audit found
H(n)=sum_(d|rad u,d<=n^gamma)mu(d), whereu is the entire n^nu-smooth
part ofn. Nonzero nonrough terms require rad u>n^gamma andv=n/u is1
oroneprime. The pure smooth case and a moving nonseparable cutoff remain.
Complementing divisors gives a short t<n^(1/6+3e) in the prime branch,
but its sign is initiallymu(rad u), notmu(u). A rank-two fixture rejects
only a single separated product, not more general decompositions.

An ACTUAL arithmetic improvement followed. A small-prime sieve at level
x^(e/4), multiplied byH, has LCM moduli<=x^(1/2-3e/4), so saved Type I
controls it. Its approximation error is paid by the nonnegative upper/
lower gap and the tau^3 moment. This removes n with a prime factor<=y
from the smooth error, with all-log error. On remaining y-roughn, repeated
factors cost at mostxlog^2x/y. The error can therefore be restricted to
squarefree n, and ordinarymu(u) now replacesmu(rad u) legitimately.
The exact remaining term is S_e=-M_e+all-log, whereM_e=sum mu(r)w_(trv),
r>n^gamma, mu^2(tr)=1, primes oftr in(y,n^nu), andv1orprime>=n^nu.
Keep t1 and every mask. Prime mass=B_P-R_nu(w)+M_e(w)+all-log, stillOPEN.

Actual power pruning also reduces the source root-lift decomposition to
HB4's8 primitive factors per prime slot, with error exponent<=64/75
apart from fixed logarithms. No new free-variable length is obtained.
The saved classical parity model gives S_e(ell)=(1-log2+O(e)+o(1))B0,
showing why this surviving sector cannot be silently dropped. This is an
application/calibration, not another claim about the actual prime partner.
The earlier critical-mass bound and conditional positivity remain valid;
no new Goldbach coverage or quantitative onset was established.

Independent Sol theory and actual-file PASS, including the new sieve
localization. Sixguards pass normal0.015s/-O0.013s; an initial expected
list was corrected to the existing tuple API. Source/runtime corrections,
polynomial tools and exceptions remain preserved. No external actions.

Next bounded test: a quantitative multiplicative-sign criterion on the
newly rough squarefree mu(r) support, with auxiliary primes>y. Derive the
actual masked dilation covariance and its full required error budget;
check for an available arithmetic saving before expanding the method.
Reject mere recovery of a previously open covariance. Unperformed; fresh
<=30-minute clock. Overall goal active; no process claimed beyond closeout.

## 2026-09-09: exact prime-dilation gate and actual coprime localization

Started17:03:39 UTC, reassessed17:21:42 UTC, changed-under-evidence.
Resumed verified clean mainab82775; reviewed mathematics **16fa2d0**,
in rough_mobius_dilation.py. Generic Katai mean-divisor reconstruction
only gives XL/sqrt(logL), too large at X/L precision. Fixed-prime
qualitative hypotheses cannot supply a uniform rate for our moving rough
support. This failure does not exclude other multiplicative-sign methods.

A classical exact Ramare identity avoids that particular loss: the full
prime set(y,x^nu] represents each squarefree r exactly with weight
1/(1+omega(r/p)). Its dyadic Cauchy energy has signed off-diagonalO and
diagonalD<<L^2X/logP. All masks are retained. Summing all rows and prime
blocks pays the diagonal withO(xL^3/sqrt(y)). DefineE=sum O^+/P; then
 |M_e(w)| <<_A x/L^A + sqrt(xL^3 E).
ThusE<<x/L^(2A+3) suffices forM<<x/L^A. This actual covariance input is
OPEN, andR_nu(w) still remains in prime mass=B_P-R_nu+M+all-log.

An ACTUAL additional saving removesgcd(n,2x)>1 fromM at absolute cost
O(xL^3/(ylogy)): at mosttau(n) cofactor representations and
tau(ell*m)<=2tau(m), summed overell|2x withell>y, pay the deletion.
No primality of the reflected partner is assumed. This excludes obvious
common-factor rows before requesting uniform covariance. The remaining
linked arguments areN-cps,N-cqs, relationq*q1-p*q2=(q-p)N.

Green arxiv1604.04481v4,p6 supplies the known identity; p5 already
discusses the analogous shifted-Mobius linked-prime obstacle. General
source parameter restrictions are not waived. Tao's2011 Katai exposition
and BSZ Theorem2 establish the generic-bound/limit-order comparison.
Oxford source403, arxiv succeeded; no unchanged retry. Sol theory and
actual-file PASS. Five finite guards pass0.012s normal and-O. Initial
home-cwd patch placement was repaired by moving only the two new files
into the repo; no overwrite or mathematical change. Reviewer wording
clarified von Mangoldt arguments versus primes. No new coverage, onset,
novelty claim, external actions or discarded polynomial tools.

Next concrete hypothesis, unperformed: raise n's roughness cutoff to a
fixed powerx^kappa while paying at mostdelta*x/L actual localization error,
using joint prime/cofactor majorants rather than the crude L*tau bound.
If valid, the long Mobius cofactor has boundedly many prime factors.
First derive the full kappa,e,delta and logarithmic budget; reject it if
the approximation error cannot reach prime precision. Do not substitute
formal main-term matching for that bound. Fresh <=30-minute pursuit;
overall goal stays active, no process claimed after closeout or manual wake.

## 2026-09-09: actual fixed-power localization for a full polynomial sieve

Started17:29:50 UTC, reassessed17:47:33 UTC, changed-under-evidence.
Resumed verified clean main3df33dc; reviewed mathematics **3882437**,
polynomial_rough_localization.py. The existing hard-H localization proof
does not pay a fixed-power cutoff at prime precision; its bounded sieve
ratio leaves logarithmic losses. A single small-prime layer may still fit
near-half Type I, so this is not a universal boundary-layer obstruction.

The successful alternative is the preserved full polynomial
T_k(n)=sum_(d|n)mu(d)(1-logd/logV)_+^k, V=x^gamma,gamma<1/2,k>=9.
An ACTUAL joint bound proves small-prime loss
O_(gamma,k)((kappa+1/L)S_2(N)x/L)+all-log, fixed0<kappa<=1/20,
with leading constant independent ofkappa. This is relative precision
againstB_P, not a uniformdelta*x/L assertion without the singular series.
Exact p-power extraction retains the Mellin factor logp/L; corrected
Henriot handles m,N-p^j m uniformly whenp^j<=x^.1. Comparisonb is paid
separately through its rough Euler product, whose logy cancelsc_y.
The extra third kernel moment is finite and sumlogp/(p^j)=O(kappa L+1).
Higherpowers costx^(39/40)L; common target factors costall-log.

The polynomial has prime value1 and its whole w-pairing isTI-small.
Therefore prime mass=B_P-C_(k,kappa)(w)+O((kappa+1/L)S_2(N)x/L)+all-log,
whereC sumsT_k(n)w_n over squarefree target-coprime composites with
P-n>x^kappa. Squareful removal costsxL^2/x^kappa; its onset depends on
fixedkappa. The retained factors number strictly less than1/kappa.
This is a NEW exact coefficient/remainder, not oldH/M/R with a mask added.
It introduces necessary composite terms that the hard coefficient killed.
The signedC is stillOPEN; no new Goldbach coverage or numerical onset.

Sol theory and actual-file PASS, fiveguards normal0.001s/-O0.002s.
No mathematical correction. The hard-H single-layer diagnosis was scoped
correctly before promotion. All earlier source corrections and polynomial
tools remain. Original Henriot definitions were rechecked; the corrected
erratum remains authority and its blocked route was not retried. No
publication, external action, install, old experiment rerun or manual wake.

Next unperformed test: derive the polynomial Mellin bound directly rather
than through the fixed power10 majorant. Split at logV/logp while keeping
the saturated local factor. Test the concrete predictions ofO(kappa)
loss for degree4 andO(kappa log(1/kappa)) for degree3, with both actual
and comparison terms, uniform constants and all summation costs paid.
Do not promote a divergent integral or logx loss. Fresh <=30-minute
pursuit; the overall goal remains active, no process claimed after closeout.

## 2026-09-09: direct Mellin localization for cubic and quartic sieves

Started17:50:01 UTC, reassessed18:00:02 UTC, progress.
Resumed verified clean maindbe552e; reviewed mathematics **85e7d44**,
extending polynomial_rough_localization.py. The direct polynomial Mellin
formula and saturated small-prime factor reduce the joint arithmetic
cost toJ_k(beta)=int_1^infty min(1,beta*t)t^(1-k)dt. Uniform corrected
Henriot/Mertens costs t^2 for t>=1; both actuala and comparisonb retain
their required partner prefactors and moments. k>=4 givesJ<<beta,
while k3 givesbeta*(1+log(1/beta)). The k2 positive majorant diverges;
that does not make the exact coefficient integral divergent or disprove
other quadratic approaches.

Complete Chebyshev/Stieltjes summation, including the lower prime atom,
gives relative lossO_(gamma,k)(kappa) for k>=4 and
O_gamma(kappa*(2+log(gamma/kappa))) for k3, fixed
0<kappa<=min(1/20,gamma/2). A separate logL/L error is unnecessary.
The earlier exact NEW polynomial residual identity, common-factor/
prime-power deletions and fixed-kappa squarefree removal all persist.
The same direct calculation without a small factor proves
sum|T_k|(a+b)<<_(gamma,k)S_2(N)x/L+all-log for k>=3. That main-scale
bound has no certified positive margin. Cubic weights remain signed;
C_(k,kappa) and Goldbach coverage remain OPEN.

Sol theory/actual-file PASS, nineguards normal0.013s/-O0.014s.
The added independent rational Riemann checks enclose the claimed J
integrals; other guards preserve the degree2 limitation and cubic signs.
No material correction. The initial review's lower-end error was removed
by the justified cumulative upper bound, not by dropping its atom.
Prior source/runtime corrections and unavailable Qwen exception remain.
No outside action, old experiment rerun, foreground input or wake queue.

Next preliminary hypothesis, unverified: use the MOVING cubic cutoff
sqrt(n). Derive actual Type I at sqrt(x)/log^B x with all b/comparison
errors, then pay the remaining near-cutoff divisors by cubic vanishing.
The predicted tail x*(loglogx)^4/log^2x is small at prime scale. Only
after this transfer, test exact squarefree divisor complementation:
odd factor counts>=5 may vanish and the triprime weight may reduce to
24*product(logp/logn). Check moving-cutoff localization separately;
sqrt(x) and sqrt(n) must not be conflated. No endpoint result is yet
promoted. Fresh <=30-minute test, overall goal active; no process claimed
after closeout or manual continuation queue.

## 2026-09-09: moving cubic endpoint with actual errors paid

Started18:03:24 UTC, reassessed18:15:16 UTC, progress.
Resumed verified clean mainbd4a46b; reviewed mathematics **c0f70ca**,
critical_cubic_sieve.py. ACTUAL Type I now reaches sqrt(x)/log^B x
for this comparison, using the source logarithmic BV range and paying
all b floor/density errors. Moving polynomial coefficients permit Abel;
the cubic near-cutoff tail is O(x*(loglogx)^4/log^2x)=o(x/logx).
This controls the full U_3(n)=sum_(d|n)mu(d)(1-2logd/logn)_+^3 pairing.
It does not supply arbitrary square-root Type I or endpoint all-log error.

The moving small-prime deletion also holds with relative loss
O(kappa*log(e/kappa)), fixed0<kappa<=1/20, by dominating its Euler
factors with a FIXED multiplicative function before corrected Henriot.
Common target factors, high powers and rough squares are paid as before.
On retained squarefree n, exact complementation at sqrt(n) kills odd
factor counts>=5, and U_3(pqr)=24*product(logp/logn). Even classes retain
their signs; prime value is1. Fixed sqrt(x) and nonsquarefree inputs do
not admit that same cancellation. The actual prime identity is
prime mass=B_P-E_kappa(w)-24T_kappa(w)
 +O(kappa log(e/kappa) S_2(N)x/logx)+o_kappa(x/logx),
where E contains even factor counts and T contains ordered triprimes
weighted by product(logp/logn), with all roughness/coprimality masks.
The signed E+24T remains OPEN. No new coverage or effective onset.

Independent Sol theory/actual-file PASS; six focused guards passed
normal0.106s/-O0.108s. No material correction. Prior source/runtime
corrections, unavailable Qwen exception and polynomial tools persist.
No old experiment rerun, install, outside action or manual wake queue.

Next unperformed question: can the retained three-factor product create
a usable extra average in a dispersion estimate with PRIME coefficients?
Derive the exact off-diagonal forms and full cost first; compare the saved
rough-Mobius dilation and free-divisor input boundaries before fetching
new sources. Seek a signed saving on a specified nonempty factor region
at fixed N. Retire the route if it only restates the earlier covariance,
needs free coefficients, drops masks or substitutes target averaging.
Fresh <=30-minute pursuit; overall goal active, no process claimed after
this reviewed checkpoint.

## 2026-09-09: triprime extra-average test does not change the covariance

Started18:18:01 UTC, reassessed by18:25:26 UTC, changed-under-evidence.
Resumed clean maine1e3779; reviewed mathematics **98dc8b7**, extending
critical_cubic_sieve.py. Grouping the two smaller primes into s leaves
unique semiprime rows. Cauchy's actual diagonal costs at most
O_kappa(x^(5/6)log^(3/2)x) over all boxes, but the remaining covariance
t(N-sr)-r(N-st)=(t-r)N is the saved dilation shape with all prime/log
coefficients and masks. No automatic additional free variable appears.
The mechanism is retired; possible future matching trilinear estimates
are not ruled out. Sol theory/actual PASS, nine guards normal0.139s/-O0.142s.
Review corrected the inference that full-square nonnegativity alone
licenses deleting restrictions inside signed rows. No new coverage.

## 2026-09-09: individual target transfer to a finite spectral pair kernel

Started18:23:12 UTC, reassessed18:37:13 UTC, progress.
Reviewed mathematics **02448f6**, pointwise_zero_pair_gate.py. The failed
averaged route exposed a source correction: Languasco2016 arXiv1606.00860
Theorem2.2/Lemma5.1/Section6 supersedes the O(sqrtN) normalized Cesaro
error still present in arXiv1206.0251 and the2015publishedPDF. It isO(N),
and the exponential-sum error needs a constant1. Initial reviewer reliance
on the older publication was retracted after the author's correction.
Unit differences of the corrected averaged formula have unpaid error.

A different route uses the corrected formula on one Fourier period.
The actual coefficient identity R(N)=I_N[S^2] and L2 bounds
||S||2<<sqrt(NlogN), ||S-(1/z-Z)||2<<log^2N pay a pointwise error
O(sqrtN log^(5/2)N+log^4N). The finite-period pair kernel is essential.
After removing the single-zero part usingV=(e^z-1)^-1, one obtains
R(N)=2psi(N-1)-N+B_(N,T)+O(sqrtN log^(5/2)N+log^4N), without RH.
All zeros, both height signs and multiplicities, are retained. A proved
uniform Gamma/zero-count tail licenses T=C_A NlogN, but supplies no
practical complete-zero computation. PNT gives2psi(N-1)-N=N+oN.
The signed condition B_(N,T)>=-(1-delta)N would yield genuineprimepairs
after O(sqrtNlog^2N) proper-power deletion; it remains OPEN. Ordinary
pair-correlation inputs do not automatically estimate this complex kernel.
The inspected stronger1996GMC corollary still permitsX^epsilon exceptions.

Independent Sol theory/actual-file PASS; six exact guards passed
normal0.023s/-O0.034s. No actual zeros or new prime ranges computed, no
coverage/onset/novelty claim, no outside action or manual wake queue.
The previous goal turn was progress and the overall goal remains active.

Next concrete hypothesis, unperformed: opposite-height-sign zero pairs
may be all-log small by one-sided Gamma damping plus the classical zeta
zero-free region and the proved total L2 norm. Bound each suppressed
half-period norm first, including small t and all log costs, then estimate
the actual cross term. Preserve the remaining same-sign pair kernel with
its signed lower-bound gap. Reject any silent RH assumption or substitution
of a positive norm for the target square. Fresh <=30-minute pursuit;
no process claimed after this checkpoint. Polynomial tools remain available.

## 2026-09-09: damped zero interactions deleted without RH

Started18:39:29 UTC, reassessed18:49:04 UTC, progress. Resumed clean
mainc2934bb; reviewed mathematics **cca6455**, one_sided_zero_reduction.py.
The previous goal turn was progress: it paid the actual pointwise spectral
transfer and corrected the explicit-formula authority before promotion.

The new arithmetic input is the classical zeta zero-free region, using
Mossinghoff-Trudgian-Yang arXiv2212.06867v1 Theorem1.3 and compact low-height
extension; no numerical constant or onset supplied. On t>=0 the Gamma
factor of a negative-height zero is exponentially damped. A uniform radial
L2 split at beta3/4, followed by Minkowski and zero counting, gives
||Z_minus||2 << sqrtN exp(-c0 sqrt(logN)). No RH assumption. With the saved
full norm O(sqrt(NlogN)), the actual discarded 2PQ+Q^2 contribution costs
O_A(N/log^A N), for each fixed A. The exact conjugation factor is e/pi.
The suppressed norm is uniform for arbitrary finite truncations; the total
cross estimate is proved first for full sums, then passed only through the
licensed T=C NlogN tail. Fixed T=16pi NlogN suffices asymptotically here.

The retained C_(N,T)=e/pi Re integral_0^pi e^(iNt)Z_(+,T)^2 dt is the
ordered positive-height pair SQUARE, including its diagonal, not a positive
norm. Thus R(N)=2psi(N-1)-N+C_(N,T)+O_A(N/log^A N). A fixed lower margin
C>=-(1-delta)N for all sufficiently large evenN is still UNPROVED. No
new coverage, practical zero computation, numerical onset or novelty claim.
Independent Sol theory/actual-file PASS; five finite sign/algebra/budget
guards normal0.002s/-O0.001s. Polynomial tools and all source corrections
remain available. No outside action, manual wake queue, or process claimed
after this reviewed checkpoint. Overall research goal remains active.

Next unperformed question: can stationary-phase geometry of the retained
positive-height kernel yield a proved aggregate saving on a specified
nonempty region? First derive the exact phase, then pay amplitudes, endpoints
and the zero summation with N fixed. A stationary-point identity alone is
diagnosis, not cancellation. Do not replace the finite kernel or assume RH.
Fresh <=30-minute pursuit, with the actual signed lower bound still open.

## 2026-09-09: actual nonstationary endpoint obstruction and interior saving

Started18:50:54 UTC, reassessed19:01:15 UTC, changed-under-evidence.
Resumed verified clean main3c1e7da; reviewed mathematics **c901fc3**,
spectral_endpoint_obstruction.py. The previous goal turn was progress:
cca6455 paid opposite-height-sign interactions without RH.

For positive-height pairs set b=beta+beta', h=gamma+eta. The phase is
Nt-h log|a+it|-b arg(a+it), with stationary equation u^2-hu+1-b=0,
u=Nt. Test both zero heights in (8piN,9piN]. Any tiny stationary point
lies in [0,1/N], whose integral is exponentially small. The rest has
|phase'| comparable to N/t; two integrations by parts give a uniform
nonzero endpoint term plus O(N^-2) after factoring Gamma damping.
Thus |J_(rho,sigma)|>=c/N*gamma^(beta-1/2)*eta^(beta'-1/2).
Functional-equation reflection beta ->1-beta at fixed positive height
preserves multiplicities and pairs weights x,1/x. Their sum is at least2.
Riemann-von Mangoldt gives (1/2)NlogN+O(N) zeros in the band, proving
ACTUAL ordered termwise absolute mass >>Nlog^2N WITHOUT RH. The small
endpoint-damping constant is fixed; it cannot provide an asymptotic saving.

The proposed absolute deletion of the whole band is retired. This does
not bound its real signed sum, rule out cancellation, or prove a negative
Goldbach coefficient. A useful component survives: for a FIXED smooth
cutoff chi vanishing nearpi, four integrations and the full all-strip
Gamma/zero-count cost give sum|J^chi|<<_chi N^-1log^2N on the SAME band.
The contribution is therefore localized to any fixed endpoint neighborhood.
No uniform shrinking cutoff or whole-tail estimate is asserted.

Independent Sol theory/actual-file and narrow corollary-delta PASS. Six
exact guards normal0.002s/-O0.003s. A finite toy Simpson check agreed with
the endpoint expansion, with refinement differences explicitly not certified
error bounds; no actual zeros or prime ranges computed. No new coverage,
numerical onset, novelty claim, outside action or manual wake queue.
Polynomial components and all corrected authorities persist. Overall goal
active; no research process claimed after this reviewed checkpoint.

Next unperformed question: derive a smooth height-projection kernel at the
endpoint and test whether the exact parity identity for S(a+i*pi), together
with a one-prime PNT input, controls the projected real contribution before
taking absolute values. The unprojected endpoint alone is insufficient.
Keep Gamma phases, all real parts, the finite period and fixed N. Reject
any hidden zero-correlation assumption or mere restatement of the signed
gap. Fresh <=30-minute hypothesis; no Goldbach lower margin is proved.

## 2026-09-09: prime parity gives signed cancellation on a smooth zero-pair region

Started19:03:10 UTC, reassessed19:14:13 UTC, progress. Resumed verified
clean maind104b80; reviewed mathematics **793b135**,
smooth_endpoint_cancellation.py. The previous goal turn was progress:
the endpoint obstruction changed the next test from termwise estimates
to summation before taking real parts.

At z_*=1/N+i*pi, the absolute zero mass is O(N^(3/2)logN). A truncated
radial Fourier projection and the corrected arbitrary-a explicit formula
give, for fixed smooth w supported in (0,infinity),
sum_rho Gamma(rho)z_*^-rho w(gamma/N)
 =sum_n Lambda(n)e^(-n/N)w(pi*n/N)+O_w(sqrtNlogN).
Chebyshev moments pay the radial linearization. Prime parity leaves only
a bounded powers-of-two correction on this support; no PNT asymptotic,
RH or prime/zero-pair correlation assumption is required. The2016 error
correction still controls over the arbitrary-a formula printed in2012/2015.

A smooth tensor expansion, AFTER the single-zero estimate, gives the
two-zero arithmetic main with error O(N^(3/2)logN+Nlog^2N). That main
is real for real weights. The leading endpoint multiplier is -i/(N*d),
d=1-(gamma+eta)/(piN), so its real main vanishes exactly. Three integrations
retain two endpoint terms; the beta-linear secondary term uses one crude
O(N^(3/2)logN) factor and one projected O(N) factor. Every remainder is paid.
Consequently, for each FIXED REAL G in C_c^infinity((8pi,9pi)^2),
Re sum_(rho,sigma)G(gamma/N,eta/N)J_N(rho,sigma)
 =O_G(sqrtNlogN+log^2N).
This is an ACTUAL signed estimate at fixed N on a specified nonempty region.
For nonnegative smooth G positive on a smaller rectangle the previous
argument still gives >>Nlog^2N absolute mass, so summing signs matters.

The hard band, growing or shrinking smooth weights, full tail and the
Goldbach lower margin are not covered by this fixed-G theorem. No new
prime-pair coverage, effective onset, actual zero computation or worldwide
novelty is asserted. Sol theory/actual-file PASS; six exact guards passed
normal0.001s/-O0.001s. Polynomial components and all source corrections
persist. Overall goal active; no outside action, manual wake queue, or
process claimed after this reviewed checkpoint.

Next unperformed question: extend to smooth positive-height pairs with
gamma+eta>(pi+delta)N for fixed delta>0 through T=C NlogN. Explicitly
pay one height approaching0, support growing like logN, all seminorms,
and the height tail. Only polynomial-log losses may be absorbed into
the power saving; fixed-G constants cannot be silently treated as uniform.
No shrinking delta or stationary-region estimate is assumed. Fresh
<=30-minute hypothesis, with the full signed Goldbach margin still open.

## 2026-09-09: the full smooth nonstationary spectral tail is controlled

Started19:16:56 UTC, reassessed19:27:08 UTC, progress. Resumed verified
clean mainf2db6b6; reviewed mathematics **4c69475**,
nonstationary_spectral_reduction.py. Previous goal turn was progress:
fixed-box signed cancellation supplied a concrete extension mechanism.

For fixed delta>0 and fixed smooth Psi, zero belowpi+delta and one above
pi+2delta, the ACTUAL full positive-height pair sum weighted by
Psi((gamma+eta)/N) has real part O_delta(sqrtNlog^40N). The extension
pays support[-S,S] with projection error S Q12 sqrtNlogN, the O(logN)
powers-of-two correction at the axis, and negative-height endpoint terms.
At B=16pi logN the tensor coefficients cost B^32; all remaining support,
seminorm, beta and integration-by-parts costs are explicit polynomial logs.
The sharp absolute tail N^-11/2 log^(5/2)N at T=16piNlogN, multiplied
by full absolute majorant N^(5/2)logN, also pays coupled bounded weights.

Thus the remaining C_low is FINITE, supported on positive
gamma+eta<=(pi+2delta)N, with weight1-Psi. The complete transfer is
R(N)=2psi(N-1)-N+C_low+O_A,delta(N/log^A N), each fixed A. The author
caught and corrected an initial square-root-error claim for this combined
formula before promotion: the earlier opposite-sign error remains
N sqrt(logN)exp(-c sqrt(logN)), so it cannot be absorbed into sqrtNlog^40N.
The new tail alone has the stronger bound. A finite guard preserves this
distinction, and independent actual-file review confirmed the correction.

Sol theory/actual-file PASS; seven guards normal0.002s/-O0.004s. No RH,
target averaging, hard/shrinking cutoff, practical zero certificate, new
prime-pair coverage, numerical onset or worldwide novelty claim. The
surviving signed lower margin stays OPEN. Polynomial tools and all source
corrections persist. Overall goal active; no process claimed after the
reviewed checkpoint, no outside action or manual wake queue.

Next unperformed question: pay the identical-zero contribution in the
surviving stationary sum using a uniform diagonal-kernel bound and a
source-checked classical zero-density theorem. Include small heights,
the finite-period endpoint transition and multiplicity-squared counts.
Seek an all-log bound without RH or an assumption of simple zeros; any
success would still leave the distinct-zero correlation. Fresh <=30 minutes.

## 2026-09-09: identical-zero spectral pairs are absolutely negligible

Started19:29:02 UTC, reassessed19:41:46 UTC, progress. Resumed verified
clean mainccf6291; reviewed mathematics **6abc250**,
spectral_diagonal_bound.py. Previous goal turn was progress: the uniform
nonstationary reduction supplied a finite stationary-region target.

For fixed K,A>0, the actual sum over distinct complex zero locations
0<gamma<=KN of m(rho)^2 |J_N(rho,rho)| is O_(A,K)(N/log^A N).
The uniform kernel bound N^(2beta-1)/sqrt(1+gamma) includes a stationary
point meeting the finite endpoint. It follows from an elementary phase
split giving O(h^(1/2-b)) for EVERY terminal rescaled interval. Actual
bounded-height zeros form a finite set; no numerical zero fact is assumed.

Multiplicity-squared is paid through m(rho)<<log(gamma+3), then the
multiplicity-counted classical density theorem. Low heights are paid first
using the classical zero-free region and H0=exp(alpha sqrt(logN)), with
alpha=min(1,sqrt c). The high-height layer-cake bound uses the uniform
Ingham exponent3(1-sigma)/(2-sigma) with log^5T. Source-checked
arXiv2507.15184v2 Corollary1 and Table1 give a stronger uniform logarithmic
factor, so this weaker input is justified. v2 is a refinement, not a
claimed correction of v1. Three explicit rational exponent ranges pay
all bands, giving N log^8N exp(-c1 sqrt(logN)), hence the stated saving.

This deletes every identical-location pair under the retained bounded
smooth multiplier. Different real parts at the same height remain distinct
and OPEN, with product multiplicities. No RH, simple zeros, square-root
error for the full R formula, signed margin, coverage or numerical onset.
Sol theory/actual-file PASS; six guards passed normal0.007s/-O0.008s.
All polynomial tools and source corrections persist. Overall goal active;
no outside action, manual wake queue, or process claimed after checkpoint.

Next unperformed question: remove an entire near-height strip
|gamma-eta|<=log^B N for fixed B, testing the largest growth allowed by
the density saving. Derive the unequal-zero kernel, retain the cost of
unbalanced small heights, use local zero counts and a symmetric arithmetic
mean inequality. No RH or pair-correlation input is licensed. Fresh
<=30-minute hypothesis; separated-height signed interactions would remain.

## 2026-09-09: a growing near-height zero-pair strip is negligible

Started19:42:53 UTC, reassessed19:48:19 UTC, progress. Resumed verified
clean main95d3e9d; reviewed mathematics **9f47ce4**,
spectral_near_height_bound.py. Previous pursuit was progress: the
identical-zero phase proof depended only on the sums of heights and real
parts, giving a concrete unequal-zero extension.

For all actual positive zeros, |J_N(rho,sigma)| is bounded by
N^(beta+beta'-1)/sqrt(1+min(gamma,eta)). This follows from the uniform
partial-integral bound and Gamma ratio; very unequal heights are paid.
On |gamma-eta|<=W, the denominator comparison costs sqrt(W+1), the
multiplicity-counted local Riemann-von Mangoldt count costs (W+1)logN,
and AM-GM reduces the two real-part weights to the single moment F_K.
The earlier density calculation bounds F_K DIRECTLY by
Nlog^8N exp[-(alpha/10)sqrt(logN)], alpha=min(1,sqrt c). One cannot
instead infer that bound by reversing diagonal<=F_K.

Therefore, for fixed K,A>0, the ENTIRE strip of pairs 0<gamma,eta<=KN,
|gamma-eta|<=exp[(alpha/30)sqrt(logN)], has absolute mass
O_(A,K)(N/log^A N). The explicit intermediate bound is
Nlog^9N exp[-(alpha/20)sqrt(logN)]. All product multiplicities are
counted, including distinct real parts at the same height. Every fixed
log^B N is eventually covered; a width N^epsilon is not. No numerical
constant/onset or zero list is supplied.

With K=pi+2delta the pointwise formula now retains only C_sep with
positive gamma+eta<=(pi+2delta)N, |gamma-eta| above that strip, and the
original bounded smooth weight1-Psi. The formula for R still has its
inherited O_A(N/log^A N) error, not a square-root error. The required
signed lower margin remains OPEN. Sol theory/actual-file PASS; five exact
guards passed normal0.002s/-O0.002s. No RH, simple zeros, new prime/zero
computation, coverage, onset, novelty, outside action or manual wake queue.
All polynomial tools and corrected sources persist; overall goal active.
No research process is claimed after this reviewed checkpoint.

Next unperformed question: remove the low-height axes where
min(gamma,eta)<=exp[(alpha/30)sqrt(logN)], preserving the stronger
unequal-height Gamma ratio. Split the larger height at
exp[(alpha/4)sqrt(logN)]; test zero-free counting below and dyadic ratio
bounds above. A comparable-height replacement would miss the relevant
cost. Fresh <=30 minutes; success would still leave the signed interaction
between separated, growing positive heights, with no Goldbach margin.

## 2026-09-09: low-height axes are paid nearly through square root

Started19:49:53 UTC, reassessed19:58:16 UTC, progress. Resumed verified
clean mainef67439; reviewed mathematics **b2554fd**,
spectral_low_axis_bound.py. Previous goal turn was progress: the reviewed
near-height bound supplied a concrete unequal-height question.

The correct Gamma/phase box majorant for gamma~G<=H~eta is
N^(b+d-1)G^(b-1/2)H^(-b). The author caught an extra H^-1/2 in the
preliminary crude idea before promotion; the missing power is guarded.
Two multiplicity-counted Ingham density estimates, with the beta<1/2
baseline handled by total zero counting, reduce each box to a real-part
exponent affine in h=logH/logX. At h=g it is bounded by
1-(1-2g)(u+v)-g/4; at h=1 by1/2+g. The smaller band's zero-free
restriction pays the low-height limit, including the compact first band.

For every fixed K, uniformly1<=V<=sqrtN, the actual absolute mass of
pairs gamma,eta<=KN with min(gamma,eta)<=V is at most
C_K log^14N [N exp(-c1 sqrtlogN)+sqrtN V]. Consequently the SINGLE
V_N=sqrtN exp[-(loglogN)^2] removes the axes with all-log error and
eventually includes every fixed N^theta,theta<1/2. A fixed logarithmic
divisor gives only its displayed finite rate; V=sqrtN supplies no saving
in this bound. No RH, numerical zero-free constant or onset is supplied.

The retained finite C_core has both heights>V_N, their difference>W_N,
the original height-sum cap and smooth weight, and product multiplicities.
Overlap with the previously removed near-height strip is paid by the
absolute bound on their union. The R error remains O_A(N/log^A N), with
the inherited opposite-sign cost. Its signed lower margin is still OPEN.
Sol theory/actual-file PASS; five guards normal0.051s/-O0.046s. No new
prime/zero computation, coverage, novelty, outside action or manual wake.
Polynomial tools and corrected authorities persist; overall goal active.
No research process is claimed after the reviewed checkpoint.

Next unperformed question: delete pairs whose BOTH heights are below
N^(13/20), using the full paid density-box exponent. Derive the actual
cutoff boundary of that density estimate and preserve its limitations.
Fresh <=30 minutes; the remaining larger-height signed correlation and
Goldbach margin would still require new control.

## 2026-09-09: both-low heights are paid through the Ingham envelope range

Started19:59:18 UTC, reassessed20:05:23 UTC, progress. Resumed verified
clean main1e8c05b; reviewed mathematics **0fed151**,
spectral_height_envelope.py. Previous pursuit was progress: the uniform
axis theorem supplied a paid density-box exponent with explicit costs.

For fixed0<kappa<(52+16sqrt3)/121=0.658783577860..., the ACTUAL
absolute pair sum over gamma,eta<=N^kappa is O_(A,kappa)(N/log^A N)
for every fixed A. The exponent is nondecreasing in the smaller scale g,
so set g=h without dropping the smaller-band zero-free cap. At13/20,
the rational density majorant D(u)<=20u/13+49/200 gives the explicit
gap E<=1-(1-20h/13)(u+v)-h/100. The completed-square certificate,
compact first band, small-height zero-free split and product counts are paid.

Maximizing the uncapped exponent yields M(h)=1-h/2 up to1/3,
3+(11/2)h-4sqrt(3h) up to3/4, and3h/2 thereafter. The relevant
root M=1 is kappa_* above; the other polynomial root is outside its
branch. A tangent density majorant proves the full fixed-kappa range,
with no uniform constants as kappa approaches kappa_*. This is the
CURRENT upper-envelope limit, not an actual zero-mass lower bound or
an impossibility theorem for other density/cancellation inputs.

The concrete retained C_high uses kappa=13/20 and now satisfies
gamma,eta>V_N, |gamma-eta|>W_N, max(gamma,eta)>N^(13/20), and the
original height-sum cap and smooth weight, with every product multiplicity.
The combined R error remains O_A(N/log^A N); its signed lower margin
is OPEN. Sol theory/actual-file PASS; five guards normal0.005s/-O0.005s.
No RH, prime/zero computation, coverage, onset, novelty, outside action
or manual wake. All sources and polynomial tools persist; overall goal
active. No research process claimed after this reviewed checkpoint.

Next unreviewed hypothesis: actual zeros with heights in(T,2T],
T=N^(2/3), have pair-kernel absolute mass >>T^(3/2)log^2T=Nlog^2N
INSIDE the remaining stationary region. Prove a uniform finite-period
stationary-phase main and relative error, then use functional reflection
in beta and multiplicity-counted Riemann-von Mangoldt. Check that the
already paid near-height strip can be deleted without losing the lower
bound. This would establish a real need for signed cancellation in the
retained core, not failure of Goldbach or an impossibility of cancellation.
Fresh <=30 minutes; the actual lower-bound claim is not yet reviewed.

## 2026-09-09: the surviving interior really requires signed cancellation

Started20:06:48 UTC, reassessed20:16:00 UTC, progress. Resumed verified
clean mainb780bbc; reviewed mathematics **fb3da0f**,
stationary_spectral_core.py. Previous goal turn was progress: the reviewed
height envelope distinguished its own limit from an actual-mass question.

A uniform finite-period stationary-phase main is proved with normalized
error O(h^-b), for h=gamma+eta,b=beta+beta' in(0,2),piN>=4h.
Compact Morse/Fresnel analysis and the paid nonstationary complement give
sqrt(2pi)e^-1 h^(1/2-b)exp(i[h-hlogh-b*pi/2+pi/4]). Restoring both
complex Gamma phases and N^(rho+sigma-1) gives positive amplitude
A=2sqrt(2pi)h^-1/2(Ngamma/h)^(beta-1/2)(Neta/h)^(beta'-1/2)
and phase Theta=gamma log(Ngamma/h)+eta log(Neta/h)-pi/4, with relative
error O(T^-1/2) on gamma,eta in(T,2T],T=N^(2/3).

At each fixed ordinate pair, functional reflection in beta pairs x and1/x
with multiplicities. Riemann-von Mangoldt yields absolute kernel mass
>>T^(3/2)log^2T=Nlog^2N, without RH. This band lies inside the actual
retained1-Psi support, above the axis and both-low cutoffs; deleting the
all-log near-height strip preserves the lower bound. This is an actual
obstruction to termwise absolute deletion of that region, not a lower
bound for its signed sum or an impossibility of cancellation.

The total leading amplitude is independently bounded by N^(46/45)log^12N
using the rational density majorant D(u)<=3u/2+4/15. Thus the summed
relative error is O(N^(31/45)log^12N)=o(N), and the signed band truly
equals sum A cosTheta plus that paid error. The cosine sum remains OPEN;
the full pointwise R formula retains its inherited all-log error.
Sol theory/actual-file PASS; five guards normal0.004s/-O0.004s. No actual
zero/prime computation, RH, coverage/onset/novelty, outside action or
manual wake queue. Polynomial tools and source corrections persist;
overall goal active. No process claimed after the reviewed checkpoint.

Next unreviewed question: prove or refute a discrete bilinear L2 estimate
for this entropy phase, using a continuous TT* bound, fixed-frequency
projections and local zero counts, with every sampling/tail cost explicit.
The candidate matrix norm is sqrtT logT; the smooth beta-dependent
amplitude requires its own separable expansion. Even if that works,
the resulting energy sum N^(2beta-1) is not paid by the current Ingham
estimate alone at T=N^(2/3). Source-check a stronger near-one density
bound and Vinogradov-Korobov zero-free region before any use; a recalled
Huxley exponent is only an unverified locator in REFRESH_HANDOFF.md.
Fresh <=30-minute test; no discrete signed estimate is yet proved.

## 2026-09-09: actual signed cancellation in the two-thirds height band

Started20:17:49 UTC, reassessed20:35 UTC, progress. Resumed verified
clean maincda45e8; reviewed mathematics **feb00a9** in
discrete_spectral_cancellation.py. Previous goal turn was progress:
an actual absolute obstruction and controlled complex stationary phase.

For T=N^(2/3), the COMPLEX sum of J_N over both heights in(T,2T]
is O_A(N/log^A N) for every fixed A. This survives subtraction of the
already paid near-height strip. The same band has actual termwise
absolute mass >>Nlog^2N, so this proves cancellation rather than merely
restating a formal identity. The remaining C_high and Goldbach margin
are still OPEN; this result licenses only the specified band.

Remove the separable logN carrier, prove continuous TT* norm sqrtT,
then transfer through fixed Fourier projections with both tails paid.
Schwartz-kernel Schur bounds use copy-counted local occupancy logT,
including repeated zeros and arbitrarily close ordinates. Smooth Fourier
expansion in the two beta parameters preserves coefficient l2 weights.
The stationary factor cancels sqrtT, leaving logT sum N^(2beta-1).

Source-check: Yashiro1310.0765v2 printedp2 eqs(1.1),(1.2) records
Ingham log^5 and Huxley log^44 losses; their respective sigma ranges
give the uniform weaker bound U^[(12/5)(1-sigma)]log^50U. The exact
log-power versions matter; a fixed U^epsilon loss does not suffice.
Mossinghoff-Trudgian-Yang2212.06867v1 printedp2 Theorem1.1 gives the
Vinogradov-Korobov gap delta>>L^-2/3(logL)^-1/3. Layer cake then pays
the energy at N^(2/3)L+N L^51 exp[-c L^(1/3)/(logL)^(1/3)].
Adding the prior complex error N^(31/45)L^12 proves the actual result.
Separate sharp row/column masks are allowed, arbitrary coupled masks
are not; the near strip is handled by its separate absolute estimate.

Sol theory/actual-file PASS; six guards normal0.016s/-O0.016s. No RH,
target average, zero/prime computation, coverage, practical onset,
novelty claim, external action or manual wake. Polynomial components
and all source corrections persist. Overall goal active. No process
is claimed to continue after a stopped checkpoint.

Next unreviewed question: extend the same mechanism uniformly to unequal
height boxes G<=H<=N^(5/6-epsilon) above the already deleted low axis.
Scaling gamma=Gx,eta=Hy,r=G/H and removing gamma log r suggests a
phase with parameter G and mixed derivative-1/(y+r*x), uniformly
nondegenerate at r=0. Candidate physical norm sqrtH cancels the
stationary H^-1/2, leaving sqrt(E_G(NG/H)E_H(N)) times local counts.
Pay projection tails, beta amplitude, both energy gaps, actual stationary
error and dyadic summation, or record the specific obstruction. Fresh
<=30-minute test; no other band or full signed bound yet promoted.

## 2026-09-09: signed cancellation throughout every fixed sub-five-sixths square

Started20:35:13 UTC, reassessed20:43:53 UTC, progress. Resumed verified
clean mainf0af320; reviewed mathematics **2f03381**,
unequal_spectral_cancellation.py. The previous pursuit was progress:
actual signed cancellation in a band where absolute mass is large.

For every FIXED kappa<5/6, the COMPLEX sum over0<gamma,eta<=N^kappa
is O_(A,kappa)(N/log^A N). Unequal-scale TT* has norm sqrtH uniformly
as G/H tends to0 after both separable phase carriers are removed.
Fixed Fourier projections pay both tails and all coincident-copy costs.
The beta amplitude factors into a uniformly smooth part and two different
energy bases: E_G(NG/H), E_H(N). Each has a density gap at least
2-(12/5)kappa>0, while both relative baselines equal H/N. The source-
checked Ingham/Huxley log-power estimate and VK cap therefore pay all
boxes at N^kappa L^4+N L^54 exp[-c_kappa L^(1/3)/(logL)^(1/3)].

The actual complex stationary replacement is also paid. After low-axis
deletion G>=V_N/2>=N^(9/20)>=sqrtH, so both Gamma and normalized
integral errors are O(H^-1/2). The direct positive amplitude has the
old Ingham layer-cake exponent E; increasing g to h and using
D_u<=6u/5+2/5 gives E-h/2<=1-h/5-(1-6h/5)(u+v)<=91/100.
Its exact slack is(1-2u)(2-3u)/(5(1+u)). Total complex error is
O(N^(91/100)L^14); no reverse kernel inequality or numerical evidence.

The concrete actual C_high now retains max(gamma,eta)>N^(4/5), both
heights>V_N, difference>W_N, and the original smooth height-sum cap,
with all product multiplicities. The full square has weight1-Psi=1;
already absolute-small axes and near strips are subtracted afterward.
Thus no coupled mask was slipped into the operator theorem. The signed
Goldbach lower margin remains OPEN, and the full R error is still all-log.
No uniform kappa=5/6 claim, full square-root error, RH, target average,
coverage, practical onset, novelty, outside action or manual wake follows.

Sol theory/actual-file PASS; six guards normal0.019s/-O0.012s. The first
guard run caught a new-wrapper argument mismatch: density_box_exponent
takes u,v, not beta,beta'. It was corrected before PASS without changing
the proof or old files. Polynomial components and all source corrections
persist. Overall goal active; no process claimed after a stopped checkpoint.

Next unreviewed question: can the factor sqrt(G/H) itself absorb energy
growth for strongly unequal boxes reaching gamma,eta<=N/10? The actual
piecewise classical density exponent appears to satisfy D_*(u)<=2u+1/10.
For Z>=Y this suggests E_Y(Z)<<Z Y^(1/10)L^51 and leading box size
N G^(11/20)H^(-9/20)L^52. Test the union of complete dyadic tag boxes
G<=H^(9/11-epsilon), fixed epsilon>0, paying the actual stationary and
Gamma errors and all summation costs. Do not claim a curved coupled-mask
bound, endpoint transition, or linear-height deletion before review.
The fixed N/10 ceiling preserves the uniform finite-period stationary
condition. Fresh <=30-minute test; overall correlation still unresolved.
## 2026-09-09: ratio cancellation pays selected rectangles at linear heights

Started20:46:03 UTC, reassessed20:52:56 UTC, progress. Resumed verified
clean main2f4c161; reviewed mathematics **da07ce0**,
linear_height_ratio_cancellation.py. Previous goal turn was progress:
actual signed cancellation in every fixed sub-five-sixths rectangle.

For fixed1/2<theta<9/11, the union of complete dyadic rectangles
G<=H^theta with individually masked V_N<gamma,eta<=N/10 has complex
sum bounded by N^[1-(9/20)delta_theta]L^54+N^(91/100)L^14,
delta_theta=(9-11theta)/20>0. The actual piecewise Ingham/Huxley
exponent satisfies D_*(u)<=2u+1/10 by two exact rational factorizations.
Layer cake gives E_Y(Z)<<Z Y^(1/10)L^51 for Z>=Y. The phase bound
then costs N G^(11/20)H^(-9/20)L^52; the ratio pays the energy growth.

At linear heights the Gamma error G^-1 is not automatically absorbed
by the normalized integral error H^-1/2. Both are explicitly paid:
the direct old Ingham amplitude exponent E gives E-h/2 and E-g,
affine in h, each bounded by91/100 at h=g and h=1. The N/10 ceiling
keeps piN>=4(gamma+eta), so this is an actual finite-period bound.

The concrete deletion uses theta=4/5 and the current core. Since
2G<H/2 eventually, gamma<eta and their gap exceeds W_N. Therefore
max>N^(4/5) is precisely a separate column mask eta>N^(4/5), forcing
H>N^(4/5)/2. The total main improves to N^(124/125)L^54, with the
same N^(91/100)L^14 actual error. The original1-Psi is exactly1 on
this region. Delete this exact dyadic union and its disjoint transpose
from the previous C_high; no curved mask is passed to the matrix bound.
All other restrictions, multiplicities and the inherited all-log R error
remain. The full signed lower margin remains OPEN.

Sol theory/actual-file PASS; seven guards normal0.013s/-O0.017s. No
actual prime/zero computation, RH, coverage, onset, novelty, outside
action or manual wake. Sources, polynomial components and runtime
limits persist. Overall goal active; no process claimed after stopping.

Next unreviewed question: do the presently used counts/densities permit
reinforcement at comparable linear heights in a MOCK critical-line
spectrum? Candidate: a quarter-shifted lattice of spacing2pi/log(N/2)
in a fixed band gamma~cN<N/10, with fixed smooth separate masks.
The carrier becomes negative on pairs and the entropy phase has a
stationary diagonal, suggesting a main of order-Nlog^2N. Thinning to
the smooth RVM counting main appears to discard only O(N) points,
whose stationary contribution should be smaller by sqrtlogN through
the existing matrix bound. Prove or refute this, with an actual count
construction and finite-period endpoint/stationary errors paid. The
coarse relative N^-1/2 error is insufficient on this full model band.
No actual-zeta, Goldbach counterexample, model theorem or all-method
barrier is claimed. Fresh <=30-minute test of sufficiency of these
counting inputs; preserve all promising components and source boundaries.
## 2026-09-09: the counting constraints permit comparable-height reinforcement

Started20:55:30 UTC, reassessed21:07:44 UTC, progress. Resumed verified
clean main89e7edd; reviewed mathematics **6fb7829**,
spectral_count_resonance_model.py. Previous goal turn was progress:
strongly unequal dyadic rectangles were paid through a linear ceiling.

A global BUT N-DEPENDENT mock critical-line spectrum agrees with the
smooth RVM main to O(1), has the retained density envelopes and local
occupancy, yet its smooth weighted ACTUAL finite-period sum is
 -(Nlog^2(N/2)/pi)int chi^2+O(Nlog^(3/2)N+sqrtN log^2N).
Here chi is any fixed nonzero real smooth function supported in
(1/100,1/50). This is a uniform-input countermodel for that weighted
band only. It does not describe actual zeta zeros, produce one fixed
spectrum across N, determine the full unweighted sum or refute Goldbach.

The quarter-shift lattice gives a negative carrier and stationary
transverse Fresnel main. Poisson zero frequency is asymptotic to
4piN int chi^2, not exactly equal. InverseM(j) baseline heights rounded
upward to the lattice inside an extended band change counts by at most
one and omit only O(N) grid nodes. The existing discrete operator then
pays Nlog^(3/2)N for thinning. Symmetry of locations does not supply
the prime explicit formula, Euler product or zeta functional equation.

Crucially, the ACTUAL kernel is handled: for beta=beta'=1/2 in this
linear band it equals A exp(iTheta) plus the explicit upper endpoint
N^-1 b(q)exp(i[phi(gamma)+phi(eta)+Npi]) and O(N^-3/2), with
b(q)=-2e exp(-q/pi)/(pi-q), phi(t)=tlog(t/pi)-t. The proof uses an
exponentially paid lower cutoff, a next-order Morse remainder and two
noncentral integrations. The endpoint's lattice aliases are nonstationary;
thinning costs NL and the summed pairwise remainder costs sqrtN L^2.
The old coarse remainder would be main-sized and was not substituted.
The model's near-height strip is absolutely all-log and can be removed.

Fresh RVM source check: Brent-Platt-Trudgian, MathComp2021 printedp2926
eqs(5)-(7), https://maths-people.anu.edu.au/brent/pd/rpb276-MC-preprint.pdf .
Half-weight endpoints are absorbed by O(1); no numerical zero results used.
Sol theory/actual-file PASS; seven guards normal0.002s/-O0.002s. All
source corrections, phase tools and polynomial components persist.
Actual full signed margin OPEN; overall goal active. No outside action,
manual wake queue, novelty or claim of a process continuing after stopping.

Next unreviewed test: can the ACTUAL prime explicit formula bound
sum chi(gamma/N)*(N/2)^(rho-1/2) by O_chi(sqrtN log^2N), for fixed
nonnegative chi in this band, without RH or target averaging? The mock
quarter-grid gives an imaginary moment of order NlogN. A smoothed
Guinand/Weil route might exclude that alignment, but the exact source,
off-critical complex argument and analytic test-function conditions must
be checked first. Candidate Fourier truncation must pay replacement,
pole and Gamma terms; a rapidly weighted short prime window should
remain. This single moment is not the missing bilinear estimate. Fresh
<=30 minutes; no arithmetic moment or correlation theorem yet promoted.

## 2026-09-09: the actual arithmetic moment excludes mock alignment

Started21:09:52 UTC, reassessed21:22:23 UTC, progress. Resumed verified
clean main55f2bbf; reviewed mathematics **3bee966**,
arithmetic_zero_moment.py. Previous goal turn was progress: a global
N-dependent count-compatible model reinforced the actual finite kernel.

For fixed real chi smooth compactly supported in(1/100,1/50), the
ACTUAL moment S_N(x)=sum_(gamma>0)chi(gamma/N)*x^(rho-1/2) is
O_chi(sqrtN logN), uniformly for all real N/3<=x<=2N/3. Actual beta
and copies are preserved. No RH, target averaging or PNT asymptotic.
At x=N/2 the mock moment is i*(NlogN/(2pi))*int chi+O(N) for
nonnegative nonzero chi. The arithmetic identity therefore excludes
that alignment; counting constraints alone permitted it. This does
not delete any new region of the coupled sum or prove its lower margin.

Guinand's exact angular formula was checked in Garrett2021 Theorem0.1
printedp1 and CCM1309.1526v1 Lemma5 printedpp6-7, especially the
unconditional proof remark. The test is evaluated at gamma-i(beta-1/2).
Complex H extends by analytic real/imaginary decomposition. An entire
Fourier cutoff V=N^(1/8) pays the complex displacement and all-zero
Schwartz tail by sqrtN L+N^(3/2)L V^-16. The exact prime window has
uniform integer sampling, including nonintegral x; rapid weights avoid
a V loss. Poles cost sqrtN; the Gamma integral costs O(1) after real
cutoff replacement and integration by parts, with derivative checked
through NIST DLMF5.15.1. All errors are explicit in the proof module.

Sol theory/actual-file PASS; seven guards normal0.007s/-O0.007s. The
actual CCM locator is v1 Lemma5 and its proof remark, not recalled
Lemma8 or unavailable v2. Anubis denied the SBM mirror; no retry or
use. No interpolation theorem from2005.02996v3 is invoked. All earlier
source corrections, density and polynomial tools persist. No actual
prime/zero computation, novelty, new coverage, outside action or manual
wake. Overall goal active; no process claimed after a stopped checkpoint.

Next unreviewed question: prove or refute the energy upper bound
int_(1/3)^(2/3)|S_N(aN)|^2 da <<_chi NlogN. Candidate mechanism:
use the retained Ingham inequality D(u)-u<=1/2 to sharpen the
off-critical first-moment replacement, localizing smoothly near the
chi support and separately paying distant zero tails. Near-zero pole
tests may be made small using all the vanishing derivatives of chi at0.
Then a Schwartz sampling L2 estimate with the elementary prime-square
weight sum may prove the energy bound. Every remaining approximation
must be smaller than that energy; do not square the present crude
sqrtN logN error and pretend it is sufficient. No prime correlation
may be silently inserted. Falsifier: an unpaid larger replacement or
a coupled prime term required for the upper estimate. This is a new
arithmetic tool test, not automatic bilinear cancellation. Fresh <=30
minutes; the sufficient Goldbach signed lower margin remains OPEN.

## 2026-09-09: actual arithmetic energy saves a logarithm

Started21:24:53 UTC, reassessed21:31:02 UTC, progress. Resumed verified
clean maina4ff5ac; reviewed mathematics **15b36b9**,
arithmetic_zero_energy.py. Previous goal turn was progress: the actual
arithmetic moment excluded the count-compatible model's alignment.
For the retained fixed chi, int_(1/3)^(2/3)|S_N(aN)|^2 da<<NlogN.
This averages the frequency a at fixed target N; in x=aN measure the
bound is N^2logN. Actual beta, multiplicities and prime powers remain.

The same finite prime window now satisfies S_N(x)=-P_N(x)+O(log^6N)
uniformly. The localized first Taylor term is paid by Ingham's retained
first-moment envelope W_N<<Nlog^6N; its global second-order/cutoff
error is N^-1/2logN. Vanishing chi,chi' at0 improves poles to N^-3/2.
The Gamma O(1) remains. Two Schur bounds for the rapidly decreasing
prime kernel give N^-1 times the squared coefficient norm, which
Chebyshev bounds by O(logN). The improved comparison error contributes
only log^12N to energy. No two-prime estimate, RH or PNT asymptotic.
Sol theory/actual-file PASS; six guards normal0.004s/-O0.004s. No new
source theorem or actual zero/prime computation. Source corrections,
polynomial tools and runtime limits persist; no outside action/manual
wake or process claim after stopping. The full signed margin stays OPEN.

Next unreviewed test: use the exact beta-integral candidate for
2N^(rho+sigma-1)Gamma(rho)Gamma(sigma)/Gamma(rho+sigma) to pair
S_N(aN) with S_N((1-a)N), preserving all real parts. Source-check the
identity, pay endpoint localization in a and the fixed-interval energy
extension, and compare to the ACTUAL finite-period J. Its negative
half-line and upper tail must be paid; fixed endpoint projection and
the new first moment may suffice. Prediction: O_chi(NlogN) for the
smooth comparable linear-height band, still not all-log or a sufficient
Goldbach margin. Falsifier: an unpaid tail or invalid coupled transfer.
Fresh <=30-minute pursuit, not yet performed. Overall goal remains active.

## 2026-09-09: arithmetic energy transfers to the actual coupled band

Started21:32:16 UTC, reassessed21:39:50 UTC, progress. Resumed verified
clean main0073b6b; reviewed mathematics **55401fd**,
arithmetic_beta_transfer.py. This is the second bounded pursuit within
the same live goal turn, following the reviewed arithmetic energy.
For fixed real chi smooth in(1/100,1/50), the ACTUAL COMPLEX sum
sum chi(gamma/N)chi(eta/N)J_N(rho,sigma) is O_chi(NlogN). All beta,
multiplicities and diagonal terms remain; no RH or target averaging.
This excludes the model's Nlog^2N reinforcement in the actual coupled
band, but remains too large for an all-log deletion or the signed margin.

NIST DLMF5.12.1 supplies the source-checked beta integral with positive
complex real parts. The exact quotient has factor2 and becomes
2 int S_N(aN)S_N((1-a)N)/sqrt(a(1-a)) da. Endpoint localization costs
N^-1log^13N after three integrations, zero-free/reflection and the
first moment. Extending the energy to fixed[1/4,3/4] with explicit
constants pays the central integral. Gaussian-regularized inversion and
improper convergence connect the quotient to the FULL line, not directly
to J. The negative half-line is exponentially small; the positive tail
is O(N)+O(log^12N), by fixed endpoint projection and the sharpened
first moment. Its leading +i endpoint is subtracted to recover J.

Sol theory/actual-file PASS; five guards normal0.001s/-O0.001s. No
actual prime/zero computation, new coverage, novelty or outside action.
All earlier corrections and polynomial tools persist. Full margin OPEN;
overall goal active. No manual wake or post-stop execution claim.

Next unreviewed test: derive the actual real-band prime-pair expression
with o(N) error and investigate its sign. For k=n+m-N, a=n/N, the
candidate coefficient is W_a(k)=(1/pi)int chi(av)chi((1-a)v)e^-ikv dv.
Check all constants, variable-a errors, tails and prime powers; the
improved moment replacement and energy suggest a sqrtN log^7N error.
For real parts, test the saved parity projection's cancellation of the
leading imaginary endpoint. Then test whether nonnegative chi can make
Re W_a(k)>=0 for every even k, or whether Poisson summation forces
negative coefficients because the v support misses pi times integers.
This is a concrete test of a positivity mechanism, not a promised lower
bound or an obstruction to every use of these tools. Fresh <=30 minutes.

## 2026-09-09: actual prime-offset transfer refutes simple coefficient positivity

Started21:41:24 UTC, reassessed21:50:22 UTC, changed-under-evidence.
Resumed verified clean main530acc2; reviewed mathematics **3421a80**,
arithmetic_prime_offset.py. Previous goal turn was progress: energy and
its transfer controlled the actual coupled smooth band. The REAL band
now equals the ordered odd-prime sum of logp logq Re W_[p/(p+q)](p+q-N),
with O_chi(sqrtN log^7N) error and
W_a(k)=(1/pi)int chi(av)chi((1-a)v)e^-ikv dv. Every period, cutoff,
ratio-replacement and prime-power error is paid. The symmetric ratio
p/(p+q) replaces the initial p/N with O(log^2N) cost. The prime-offset
sum is absolutely convergent and stays signed; no correlation estimate
is supplied by declaring its formal main equal to its actual value.

At a=1/2, period-pi Fourier inversion gives sum_j W_[1/2](2j)=0,
while W_[1/2](0)>0. Thus some even coefficient is negative for every
nonzero real chi, including nonnegative chi. With chi supported in
(7c/5,8c/5), c1/100, offset100 is explicitly negative because the
cosine phase lies in(2.8,3.2). This refutes coefficientwise positivity
only; no negative actual total, counterexample or all-method barrier.
The transform, polynomial components and all signed estimates remain.
Sol theory/actual-file PASS; five guards normal0.000s/-O0.000s as reported.
No actual prime/zero computation, new coverage, outside action or manual
wake. Overall goal active; the full signed lower margin remains OPEN.

Next direction uses a different quantitative input. Fresh primary source
checked during reassessment: Guth--Maynard arXiv2405.20552v2 (7Apr2026),
Theorem1.2/eq(1.4), printedp2. Its uniform exponent30(1-sigma)/13+o(1)
suggests extending the prior actual full rectangle to fixed kappa<13/15,
concretely17/20. Test the new bound only for u=1-sigma>=1/10 with fixed
epsilon, retaining the old log-power Huxley estimate and VK zero-free
region near1. A T^epsilon loss cannot be silently absorbed there.
Candidate gap at17/20 is1/26; epsilon1/442 suggests a far-range saving
1/520. Uniformize on a finite sigma grid if needed, pay both unequal
energies and actual approximation errors, and check the new core mask.
The speculative error envelope max(91/100,kappa) also needs review.
No new height deletion from the source check alone. Fresh <=30 minutes.

## 2026-09-09: Guth--Maynard input enlarges the actual cancelled square

Started21:52:54 UTC, reassessed21:59:54 UTC, progress. Resumed verified
clean main60ba300; reviewed mathematics **6942c66**,
guth_maynard_spectral_cancellation.py. Previous goal turn made progress:
the actual prime-offset formula refuted one positivity mechanism.
The ACTUAL complex sum with both heights<=N^kappa is all-log small for
every fixed kappa<13/15. GM2405.20552v2 Theorem1.2/eq1.4 is used only
away from real part1, with fixed epsilon paid; a finite sigma grid
provides uniformity. Huxley log-power/VK retain the near-one saving.
At17/20 the far gap is1/26, epsilon1/442 and power saving1/520.
Both unequal energy bases and baselines are included. The actual error
stays N^.91L^14 by changing the majorant branch above h=5/6.

The concrete retained core now has max(gamma,eta)>N17/20. Its axes,
near strip, original sum cap and weights remain. Reconstruct before
the old rectangle deletion to pay overlap correctly. The preserved
theta4/5 tag family uses the separate larger-column mask eta>N17/20,
with total N^(1983/2000)L^54+N^.91L^14. Full signed margin OPEN.
Sol theory/actual-file PASS; seven guards normal0.013s/-O0.014s. No
actual prime/zero computation, target average, RH, novelty or coverage.
All source corrections and polynomial tools remain; overall goal active.

Next unreviewed test: combine the exact GM exponent15u/(8-5u) on
[1/5,3/10] with Huxley below and Ingham above. The proposed majorant
D(u)<=2u+6/65 would enlarge the linear-height ratio family to fixed
theta<59/71, after charging epsilon>0. Concrete candidatetheta53/64,
epsilon1/1170 yields density excess109/1170 and decay1/1280. Pay
both actual errors, the linear N/10 ceiling and the current individual
eta>N17/20 mask before deleting anything. Fresh <=30-minute pursuit.

## 2026-09-09: density shape enlarges the actual unequal-height deletion

Started22:00:55 UTC, reassessed22:10:26 UTC, progress. Resumed verified
clean main6741752; reviewed mathematics **0172597**,
guth_maynard_ratio_cancellation.py. The selected Huxley/GM/Ingham
envelope satisfies D(u)<=2u+6/65; the fixed positive GM epsilon is
paid by ratio decay. For fixed theta<59/71 choose epsilon such that
Delta=[1-a-(1+a)theta]/2>0, a6/65+epsilon. Concrete theta53/64 and
epsilon1/1170 give Delta1/1280. The selected actual complex rectangles
extend to separate individual heights N/2: the smaller height=o(N)
pays the finite-period stationary condition. Both relative errors
H^-1/2 and G^-1 remain separate and total N^.91L^14. The current
eta>N17/20 mask gives N^(25583/25600)L^54+N^.91L^14. This union and
transpose contain the previous theta4/5,N/10 deletion; no curved mask.
Sol theory/actual-file PASS; seven guards normal0.005s/-O0.006s.
Full signed margin OPEN; overall goal active. All polynomial tools,
source corrections and runtime restrictions persist. No outside action.

Next unreviewed test: use the exact Laplace representation to write
J_N=e/(2pi) int_0^infinity exp(-x/N)K_pi(N-x)B_x dx,
B_x=2x^(rho+sigma-1)Gamma(rho)Gamma(sigma)/Gamma(rho+sigma).
Test whether the unequal-height operator bound survives integration
with only logarithmic cost, through individual heights KN and the
original smooth transition weight. Pay x near0, bases below1, the
far tail and Gamma approximation; no hidden coupled masks. This is
a candidate endpoint mechanism, not yet a deletion. Fresh <=30 minutes.

## 2026-09-09: exact convolution carries the ratio family through the transition

Started22:16:52 UTC, reassessed22:23:42 UTC, progress. Resumed verified
clean main9d0edd8; reviewed mathematics **b816865**,
finite_period_ratio_convolution.py. Previous native goal turn was progress:
actual prime-offset identity and positivity falsifier. This pursuit proves
the exact identity J_N=e/(2pi) int exp(-x/N)K_pi(N-x)B_x dx, using
checked NIST DLMF5.9.1, positive real parts and absolute finite-list
Fubini. The beta quotient retains the unequal phase without a finite-
time stationary error. Its integrated main costs an extra logarithm.
Small x, below-one bases, the exponential tail and the Gamma remainder
are all paid. Fixed Q=(K+2)N handles individual heights KN, K>1.

With the ORIGINAL smooth weight1-Psi, selected theta53/64 tags and
separate eta>N17/20 mask, the actual complex contribution is
O(N^(25583/25600)L^55+N^.91L^15). The whole endpoint transition is
included for this unequal family; its transpose is disjoint. Rebuild
before the former N/2 union to avoid a coupled-mask argument. Comparable
large heights and the full signed lower margin remain OPEN. Sol theory
and actual-file PASS; seven guards normal0.108s/-O0.098s. The ordinary
Gamma quadrature fixture only diagnoses normalization/orientation.
No actual zero computation, RH, target average, coverage or outside action.
All source corrections, polynomial tools and runtime limits persist.
Overall goal active; no manual wake or claim of post-stop execution.

Next unreviewed question: at the surviving comparable scale T=N9/10,
can prime support improve the actual moment energy from NlogN to N?
For fixed smooth chi in(1,2), the candidate uses the explicit formula
and a weighted Schur bound on prime windows of width N/T=N1/10.
Source-check an applicable short-interval upper sieve; pay prime powers,
beta displacement, entire-cutoff tails and uniformity. If the energy
passes, test the beta and actual finite-period transfer for an O(N)
complex band bound. This would remain a main-scale upper bound, not an
all-log deletion or signed lower margin. Fresh <=30-minute pursuit.

## 2026-09-09: prime support pays an actual comparable band at main scale

Started22:25:14 UTC, reassessed22:36:11 UTC, progress. Resumed verified
clean mainc6421fc; reviewed mathematics **ba1747b**,
short_prime_window_energy.py. Previous native goal turn made progress
through the endpoint-transition deletion. At fixed T=N9/10, chi real
smooth in(1,2), the actual moment is O(sqrtN), central da-energy O(N),
and actual COMPLEX comparable J_N band O(N). No small constant or
all-log deletion follows; the signed lower margin stays OPEN.

Yamada2312.16090v1 Theorem2 printedp3 eq13 supplies the interval
upper bound. Full Lambda shell masses include explicitly paid proper
powers. The effective H=N1/10 window, Schwartz shell sum and weighted
Schur bounds pay the energy. Guinand displacement N1/10L^6, beta
endpoint N^-7/10L^13, and actual kernel error N9/10L^12 are paid.
Sol theory/actual-file PASS; six guards normal0.020s/-O0.019s. No
actual zero computation, RH, target average, new coverage or outside
action. Original MV institutional copy403; Yamada primary route worked.
All polynomial tools, earlier source corrections and runtime limits stay.

Fresh next-decision source check: GM2405.20552v2 Corollary1.4 printedp3
requires interval length X^(2/15+eps), so it supplies no X1/10 asymptotic.
Next unreviewed question tests a different mechanism: can a positive
artificial additive chirp have strong centered global Fourier cancellation
yet order-N reinforcement under the exact paired prime-window operator?
Candidate f_N(a)=lambda_N a+(a-1/2)^3 has complementary phase sum
lambda_N; choose Tlambda_N an odd multiple of pi and lambda_N->3.
Test the local approximation, discretization and global O(N7/10) Fourier
costs before drawing any conclusion. Model coefficients are not primes
or zeros. This targets a specific transfer from the newly proved bounds;
it must not repeat the older semiprime-modulus model or imply a global
Goldbach obstruction. Fresh <=30 minutes; overall goal active.

## 2026-09-09: complementary phase gives model reinforcement despite Fourier saving

Started22:38:16 UTC, reassessed22:43:56 UTC, changed-under-evidence.
Resumed verified clean main6cf340d; reviewed mathematics **1689968**,
complementary_window_chirp.py. The exact current window operator on
positive ARTIFICIAL coefficients b_N(n)=1+(1/2)cos[T f_N(n/N)],
f_N(a)=lambda_N a+(a-1/2)^3, T=N9/10, has the pointwise expansion
(1/4)sqrt(aN)chi(a f'_N(a))exp[iT f_N(a)]+O(N2/5).
Choose lambda_N->3 with Tlambda_N an odd multiple of pi. Its exact
complementary phase identity gives the paired functional -cN+O(N9/10),
c>0. The model obeys the stated interval/energy mass inequalities AND
has centered smooth global linear Fourier sums O(N7/10). The proof
pays discretization, local linearization, Fourier inversion, all Poisson
aliases and the phase-lattice error. Sol theory/actual-file PASS; six
guards normal0.002s/-O0.002s. It is an N-dependent dense coefficient
model, not Lambda, prime support, Type I, zeta zeros or a counterexample
to Goldbach. The older semiprime-modulus model was checked; this is a
specific complementary additive-phase mechanism in the current operator.

Next unreviewed test returns to ACTUAL primes: source-check an applicable
cubic prime-exponential-sum theorem and test whether
sum psi(n/N)Lambda(n)exp[-iT f_N(n/N)] has a fixed power saving.
Its leading coefficient has size T/(2piN^3), with a reciprocal rational
approximant of denominator q~N21/10. Verify approximation tolerance,
uniform lower coefficients, smoothing, prime powers and actual saving.
The model has an order-N coefficient against its own phase; excluding
that alignment would add a nonlinear arithmetic constraint. It would
not bound arbitrary phase superpositions or the full signed correlation.
Fresh <=30 minutes; overall goal active, full lower margin OPEN. All
polynomial tools, source corrections and runtime restrictions persist.

## 2026-09-09: actual primes exclude the exhibited coherent cubic phase

Started22:46:05 UTC, reassessed22:56:14 UTC, progress. Resumed verified
clean main6eabd32; reviewed mathematics **293fb8b**,
cubic_prime_chirp_exclusion.py. The previous goal turn made progress
through the actual comparable-band bound and a complementary-phase
model. For T=N9/10 and f_N(a)=lambda_N*a+(a-1/2)^3, actual
sum psi(n/N)Lambda(n)exp[-iT f_N(n/N)]=O_psi(N63/64), uniformly
in arbitrary lower coefficients. Le--Spencer II Theorem5 printedp9,
m=1,b=0, supplies the known general-polynomial prime bound; Lemma5
printedp8 and definitions on printedp3/p6 were checked in the author PDF.
The actual reduced approximation has q~N21/10; bracket N^-1/2,
outer power1/16 and epsilon1/64 give the displayed exponent.
Comparable-prefix smoothing and O(sqrtN log^2N) proper powers are paid.

The earlier model instead has (N/4)int psi+O(N7/10) against its own
phase. This excludes THAT global coherent cubic coefficient for primes.
It does not improve the actual paired O(N) band, delete it, supply a
small constant or prove the full signed lower margin. It is a new-to-
this-task application of known mathematics; external novelty is not
claimed. Sol theory/actual-file PASS; six guards normal0.001s/-O0.001s.
Original Harman PDF request returned abstract HTML; Citeseer timed out;
author-hosted Le--Spencer II source worked. No actual prime/zero run,
outside action or post-stop execution claim. Polynomial components,
source corrections and runtime limitations remain preserved.

Next unreviewed test: does order-N reflected-window reinforcement force
a large bounded cubic-phase coefficient? Try the explicit complementary
quintic f_N(a)=lambda_N*a+(a-1/2)^5 as a falsifier, retaining the odd-pi
phase sum. Test the same -cN+O(N9/10) paired functional, but uniformly
O(N41/50) centered correlations against all cubic phases with any fixed
coefficient bound. Pay fifth-derivative oscillation and Poisson aliases;
no inference to actual primes or a general polynomial barrier. This
tests the missing inverse implication before promoting the arithmetic
exclusion to a paired estimate. Fresh <=30 minutes; overall goal active.

## 2026-09-09: a single analytic phase defeats the proposed polynomial inverse step

Started22:57:58 UTC, reassessed23:04:46 UTC, changed-under-evidence.
Resumed verified clean mainf3ba9a7; reviewed mathematics **a6edeb7**,
analytic_complementary_phase.py. Previous goal turn made progress with
the actual cubic-prime exclusion. The quintic test suggested a single
stronger falsifier: f_N(a)=lambda_N*a+sin(a-1/2)-(a-1/2), with
T=N9/10 and Tlambda_N odd*pi near3T. Its positive dense model has
the exact paired functional -cN+O(N9/10), c>0, but centered polynomial
probe correlations O(N^(1-9/(10*(D+2)))) for every FIXED degree D.
The constant and linear coefficients are arbitrary; nonlinear ones
have a fixed bound. The same model works for each fixed D, with
degree-dependent constants and onset. The proof pays local window
errors, complementary normalization, a sine/cosine derivative partition,
elementary high-derivative induction and every Poisson alias.

The proposed inverse implication fails using only those shared probe
and marginal bounds. Actual cubic-prime exclusion and polynomial tools
remain valid. The model has no prime support, Type I or explicit formula;
unbounded nonlinear coefficients, growing degrees and localized probes
are not covered. No actual paired estimate or signed Goldbach margin
has been added. Sol theory/actual-file PASS; seven guards normal0.005s
and -O0.003s. No external source search, prime/zero run or outside action.
All source corrections/runtime limits persist; overall goal active.

Next unreviewed arithmetic test: apply the existing exact Vaughan identity
to actual Lambda against this sine phase, with fixed smooth psi supported
in(1/2,3/4). Try U=V=N1/5 and an applicable discrete second-derivative
sum estimate. Candidate Type I cost is N17/20 times logs. In Type II,
orient M>=K, MK~N, and use the nonzero derivative (u^2 f''(u))' on
the support to test N[K^-1/2+T1/4 M^-1/2+T^-1/4] times logs.
The candidate worst power39/40 would permit N79/80 after logs, but
all masks, arithmetic coefficients, diagonal and variation costs need
proof and review. This tests actual multiplicative structure against the
model; it does not assume a bound for the full linked-prime covariance.
Fresh <=30 minutes. No repeat of higher-degree countermodels is needed.

## 2026-09-09: actual multiplicative curvature excludes fixed analytic alignments

Started23:06:52 UTC, reassessed23:15:26 UTC, progress. Resumed verified
clean maind3aad7a; reviewed mathematics **bad0caf**,
analytic_prime_curvature.py. Previous goal turn made progress by
falsifying the polynomial inverse step. The ACTUAL sine-phase Lambda
sum with fixed smooth support in(1/2,3/4) is O(N39/40 log^3N),
hence O(N79/80), uniformly in affine slope. Exact Vaughan U=V=N1/5
keeps the free convolution1 and actual bounded divisor coefficient.
Type I costs N17/20 L+N11/20 L^2. Type II retains the full product
intersection and diagonal, with the curvature of a dilation difference
giving N[K^-1/2+T1/4 M^-1/2+T^-1/4]. Restoring coefficients and
boxes gives the stated bound. The known discrete source is Robert,
Section3.1 Theorem1 printedp5 eq6, read from the actual author PDF
through web. A separate urllib hash request failed certificate checking;
no bypass or unchanged retry, and no claimed local hash.

The proof yields a reusable criterion with BOTH |f''| and |(u^2f'')'|
bounded away from0. A fixed analytic complementary nonaffine phase h
cannot make either identically zero. Remove its finitely many compact-
support degeneracy points with fixed-delta neighborhoods, pay their
absolute Lambda mass by the checked interval upper bound and powers,
and take limsup N before delta->0. This gives ACTUAL o(N) correlation
for every FIXED real-analytic nonaffine h with h(u)+h(1-u)=0,
uniform in an arbitrary affine slope. No uniform rate over the nonlinear
phase family or deleted neighborhoods is claimed. The sine model's own
coefficient remains (N/4)int psi+O(N1/10), so it fails this arithmetic test.

Sol theory/actual-file PASS; seven guards normal0.002s/-O0.004s.
No actual prime/zero computation, external action or post-stop execution
claim. These are applications of classical arithmetic methods, not an
external novelty claim. The actual paired O(N) band and full signed
Goldbach margin remain OPEN; all earlier tools/corrections are preserved.

Next unreviewed test: uniform cancellation for N-dependent C^3 phases
with |f'|, |f'+u f''| bounded below and first three derivatives bounded
above on a fixed positive support. Try Vaughan U=V=N1/22 and bounded
factor shifts R~N1/22. Both the Type I phase derivative T*d/N and
the Type II difference derivative T*h/N are o(1) in these ranges.
Prove a discrete derivative estimate retaining variation, then test
the Cauchy bound N^2/R+N^2*K*logR/(T*R), with the shifted masks
and actual coefficients kept. Candidate worst exponent43/44 before
logs; no claim yet. This would handle affine and controlled varying
nonlinear phases; the full paired problem still needs further structure.
Fresh <=30 minutes; overall research goal active.

## 2026-09-09: actual cancellation for uniformly controlled varying phases

Started23:17:32 UTC, reassessed23:24:22 UTC, progress. Resumed verified
clean main3e0cb0d; reviewed mathematics **5886079**,
varying_prime_phase.py. Previous native turn made progress through
fixed analytic phase cancellation. Actual Lambda sums with T=N9/10
are O(N43/44 L^3), hence O(N49/50), for N-dependent C3 phases
with |f'|, |f'+u f''| bounded below and derivatives1..3 bounded above
on a fixed positive support. N-dependent C1 amplitudes with uniformly
bounded sup+TV are permitted. Bounded nonzero affine phases are
included, but unrestricted affine slopes are not licensed by this criterion.

An elementary discrete telescoping lemma pays nonmonotone derivative
variation. Exact Vaughan U=V=N1/22 pays the full Type I layer in
N1/10 L^2. Bounded shorter-factor shifts R~N1/22, after Cauchy,
give N^2/R+N^2*K*logR/(T*R), K<=O(sqrtN). Actual coefficients,
shift weights, diagonal and product intersections stay. Robert's finite
shift inequality, Section3.3 Lemma1 printedp8, was checked via web;
the finite proof also retains the conjugation lost in text extraction.
Sol theory/actual-file PASS; seven guards normal0.001s/-O0.001s.
No actual prime/zero computation or outside action; overall goal active.

## 2026-09-09: exact-window projection and a conditional signed-band bridge

Started23:24:22 UTC, reassessed23:30:15 UTC, progress. Reviewed
mathematics **276d174**, window_phase_projection.py, using5886079.
The exact adjoint variable v=Tlog(u/a) gives normalized coefficient
sqrt(u)/N and Fourier sample chi(u f'(u)). All buffered-domain,
local Taylor, Schwartz tail and summed Chebyshev errors are paid.
Actual normalized arithmetic-window projections are O(N^-1/44 L^3);
the zero projections add the retained N^-2/5 L^6 displacement error.

If the actual reflected zero window has an admissible phase expansion
with COMMON bounds, coefficient l1 mass A_N and L2 residual R_N,
the actual weighted T=N9/10 finite-period band is bounded by
N[(N^-1/44 L^3+N^-2/5 L^6)A_N+R_N]+N^.9L^12+N^-.7L^13.
The two last errors reuse the corrected actual beta/finite-period transfer.
Fixed A_N=O(N^kappa), kappa<1/44, and power-small R_N would
conditionally pay this one band all-log. No such expansion exists in
the current evidence. The unconditional O(N) band and full signed
Goldbach margin remain unchanged. Sol theory/actual-file PASS; six
guards normal0.001s/-O0.000s. All earlier corrections/tools persist.

Next unreviewed test checks the exact natural reflected-zero expansion:
phase -(eta/T)log(1-a), amplitude2zeta*a^-1/2*(1-a)^(beta-1),
coefficient chi(eta/T)N^(beta-1)exp(i*eta*logN). Verify uniform
admissibility, then test the predicted actual coefficient-mass bounds
N2/5 logN << A_N << N1/2 L^6 using existing zero counting,
reflection and density, including multiplicities. This would falsify
the DIRECT natural expansion's l1 budget, not the signed band or
every possible recombination. No zero-range experiment is needed.
Fresh <=30 minutes; overall goal active and the full gap remains OPEN.

## 2026-09-09: actual real-part localization of the sublinear comparable band

Started23:34:35 UTC, reassessed23:44:33 UTC, progress. Resumed verified
clean mainbe62912; reviewed mathematics **043cfe0**, in
zero_packet_realpart_localization.py. The previous native goal turn
made progress through the exact-window projection and conditional bridge.
The natural reflected-zero expansion really satisfies the common phase
bounds, but its ACTUAL l1 cost is between N2/5 L and N1/2 L6 by
counting/reflection and retained Ingham. This falsifies only that direct
expansion's sufficient cost test, not the signed band or other expansions.

The alternative square-sum argument advances the ACTUAL band. Uniform
two-IBP Gram decay plus O(L) copy occupancy bounds a masked field by
sqrt(L E_D), E_D=sum_D |chi|^2 N^(2beta-2). Use the O(1) arithmetic
energy only for the full other factor; the masked intersection costs
L E_D. For D={beta<=16/25 or beta>=19/25}, Ingham gives low exponent
-9/1700. GM on beta[.76,.8] gives -3/850, and a fixed401-point grid
with source epsilon1/10000 pays9/25000, retaining <-1/400. The original
Huxley log-power bound gives -u/14 near1, where VK supplies the all-log
saving without a fixed source epsilon. Thus E_D is all-log small.

Inclusion-exclusion and the already ABSOLUTE beta/finite-period errors
give the COMPLEX bound O_A(N/log^A N) for the actual weighted T=N9/10
band with either real part in D. The remaining band has both real parts
in(.64,.76) and stays O(N); its o(N) bound and the full signed Goldbach
margin remain OPEN. No such off-line zeros are asserted to exist.
Sol theory/actual-file PASS; eight guards normal0.013s/-O0.013s.
Classic density, GM and VK sources were freshly accessible. Fresh
Brent--Platt--Trudgian web open returned Internal Error; reuse the
previously checked counting law, no fresh access or unchanged retry claim.
No numerical zero run, outside action or post-stop execution claim.

Next unreviewed question: do the current uniformly controlled C3 phase
projection bounds suffice for paired cancellation? Test a dense positive
ARTIFICIAL coefficient model with complementary phase
 f_N(a)=lambda_N*a+K^-1*sin(K*(a-1/2)), K=N1/10,
where T*lambda_N is an odd multiple of pi nearest3T. Its first derivative
stays bounded, but higher derivatives grow, outside the proved common
phase class. Prediction: the exact window retains a negative main of
size N, while projections against every phase with fixed common C3
bounds are small. Partition the rapid sine periods into second/third
derivative regions; predicted normalized integral cost (K/T)1/3, with
Euler discretization O(T/N). Pay exact-window Taylor cost K/T, and
prove a positive lower bound for the paired amplitude using a fixed
nonnegative nonzero chi. Failure of either uniform projection or actual
window calculation falsifies this model test. It would limit this inverse
implication, not actual primes or all uses of the retained tools.
Fresh <=30 minutes; no claim yet and overall research goal remains active.

## 2026-09-09: controlled C3 projections alone do not control the pair

Started23:47:00 UTC, reassessed23:52:05 UTC, changed-under-evidence.
Resumed clean main96db12d. Previous goal turn made progress through
actual real-part localization. Reviewed mathematics **e368c38**, in
rapid_complementary_phase.py, proves the proposed ARTIFICIAL rapid
complementary model works: positive b_N in[.5,1.5], phase
lambda_N*a+K^-1 sin(K*(a-.5)), K=N1/10, gives EXACT window pair
-cN+O(N9/10), with fixed c>0 by periodic averaging. Its centered
coefficient probes are O(N9/10) uniformly over bounded C3 phases
and bounded C1 amplitude variation. The normalized FULL window
projections, with |g'|>=c, are O(N^-1/10), beating the existing
actual-prime projection exponent while the paired main persists.

The O(K) second/third derivative cells, the dominant Euler O(T)
cost, local window Taylor K/T, and periodic N/K error are retained.
The precise inference from these marginal phase tests to paired
cancellation fails. This does not change any actual-prime theorem:
the model's higher derivatives grow, and prime support, Type I
identities, real-part localization and the zeta spectrum are absent.
Sol theory/actual-file PASS; seven guards normal0.001s/-O0.000s.
No model experiment claimed to be actual primes or actual zeros.
The full signed margin and overall goal remain OPEN.

Next concrete question: can ACTUAL zero-detecting structure remove
the nondetected columns of the remaining(.64,.76) band, leaving a
precise shared Dirichlet-polynomial condition on every surviving zero?
Primary locators checked: Guth--Maynard2405.20552v2 Section13.1,
printedpp48-49, https://arxiv.org/pdf/2405.20552v2 ; and
Maynard--Pratt, https://arxiv.org/pdf/2206.11729 , Definition22 and
Lemmas23-24 printedp16, Appendix C pp36-37. Confirm the latter PDF
version and audit the Appendix C proof before importing its uniform
bound. The paper's later Hypothesis F/finitely-many-lines conclusions
are NOT authorized assumptions and must not be imported.

The source detector uses dyadic lengths M between T1/100 and
T1/2(logT)^2, coefficients (sum_(d|n,d<=2T1/100)mu(d))*exp(-n/sqrtT),
and |D_M(rho)|>=1/(3logT). Every zero is Type I or Type II, possibly
both. Lemma24 states the Type II count above sigma is
O(T^(2(1-sigma)) log^C T). Define the complement of the Type I
condition to obtain a disjoint split; do not presume the original
types are disjoint. If verified uniformly on[.64,.76], layer cake
predicts its coefficient energy O(N^-6/125 log^(C+1)N), since
(.9)*2u-2u=-u/5 and u>=6/25. The existing full/masked Gram
argument would then delete those actual columns with a power saving.
This is a falsifiable source-and-transfer test, not yet a proved result.
Keep these zero-detection Type I/II names distinct from Vaughan sums.
Fresh <=30 minutes; no further artificial phase family is needed now.

## 2026-09-09/10: actual zero-detector reduction of the remaining band

Started2026-09-09 23:53:45 UTC, reassessed2026-09-10 00:02:48 UTC,
progress. Resumed verified clean mainc2248a5. Previous native turn
made progress by falsifying the common-C3 inverse implication.
Reviewed mathematics **0b1a7ba**, zero_detector_band_reduction.py.
The ACTUAL smooth T=N9/10 band reduces with all-log error to zeros
whose real parts are in(.64,.76) and which satisfy a specified classical
Dirichlet-polynomial detector at some allowed dyadic length. The
remaining paired sum is still O(N); its o(N) bound and full signed
Goldbach margin remain OPEN.

Primary source pinned and checked: Maynard--Pratt2206.11729v2,
29May2023,39pages, SHA256
e6407c953c4ddcbf9daa2fa941d1a84bf9db90f19a96e50ee8796bf9aea5947a.
Definition17/equations15-16p14, Definition22/Lemmas23-24p16, and
AppendixCpp36-38. These detector lemmas are unconditional; the later
Hypothesis F is not imported. The original types can overlap; define
the nondetected complement explicitly. The source p6 convention is
M<n<=2M. Its mollified fourth moment is a log-power bound, not a
T^epsilon estimate. The middle-strip Type II count is uniform and
copies are paid by local Riemann-von Mangoldt occupancy.

Preserve a NEW SOURCE CORRECTION: rendered pp37-38 print
Gamma(beta-.5+iu), inconsistent with their contour Re z=.5-beta.
Use the actual Gamma(-delta+iu), delta=beta-.5 in[.14,.26], and
Gamma(z)=Gamma(1+z)/z. Euler's integral bounds it uniformly; Stirling
pays the tail. This repairs the needed restricted count without copying
the incorrect argument. Temporary raster crops were removed afterward.

For nondetected middle-strip U, layer cake including the lower boundary
gives E_U<<N^-6/125 log^C N. The existing Gram estimate and FULL
unmasked arithmetic energy give actual row/column union
O(N122/125 log^C N+N^.9L12+N^-.7L13). Combine the exterior set D
with U BEFORE the Gram bound to obtain the final all-log reduction.
Least detecting length partitions survivors into O(L) disjoint lists and
O(L^2) Cartesian pair lists, with no claimed estimate for that remainder.
Sol theory/actual-file PASS; seven guards normal0.003s/-O0.002s.
No actual prime/zero computation or post-stop execution claim.

Next concrete test: can elementary mean-square estimates delete any
surviving zero detected at a length M with an integer power satisfying
 N^(41/50)<=M^k<=N^(49/50), 1<=k<=100?
For D_M^k, coefficients are bounded by tau_(2k), with support
M^k<n<=(2M)^k. Prediction: mean value plus actual O(L) local zero
occupancy and real-part partial summation give a uniform detector count
<<(T+M^k)*(M^k)^(1-2sigma)*log^C N, with C fixed for k<=100.
Keep the threshold (3logT)^(-k), all coefficient moments and copy costs.
With beta in[.64,.76], the two normalized-energy exponents are at most
-4/625 and -6/625 respectively on this power-length interval. A
positive layer cake and the full/masked Gram argument would give a
power-saving ACTUAL deletion, including a sum over O(L) lengths.
This is not yet reviewed or proved. No numerical zero run is needed.

Concrete proof test: use an interval Sobolev bound to pass zero samples
to mean squares of the polynomial and its derivative, retaining the
O(L) overlap factor. Treat varying beta by the fundamental theorem
of calculus in beta and Cauchy before mean-square integration. Prove
the divisor second-moment bound, and verify the precise primary
Dirichlet-polynomial mean-value input. If the source/normalization or
threshold losses defeat the exponent, record that failure. Otherwise
determine the remaining length intervals exactly; do not presume all
detector lengths admit a suitable integer power. Fresh <=30 minutes.

## 2026-09-10: actual detector length filter and four integer-power gaps

Started00:04:41 UTC, reassessed00:11:25 UTC, progress. Resumed verified
clean main50b7604. Previous native turn made progress through the
actual zero-detector reduction. Reviewed mathematics **8911d43**,
detector_power_length_filter.py, deletes every middle-strip zero
detected at ANY allowed M with N41/50<=M^k<=N49/50,1<=k<=100.
Powered coefficients obey tau_(2k); the matrix-margin proof gives
tau_r^2<=tau_(r^2), and harmonic products pay their second moments.
An elementary mean-square proof with its extra logarithm retained,
unit-interval Sobolev and actual copy occupancy, and integration in
beta pay all sampling and real-part variation costs. The powered
threshold contributes2k to the log exponent, not an unchanged threshold.

The two normalized energy exponents are <=-4/625 and <=-6/625.
Summing all lengths/powers gives energy O(N^-4/625 log^40220 N),
with no numerical-onset claim. Full-unmasked arithmetic energy plus
the restricted Gram bound yields actual union N623/625 times logs;
intersection621/625 and inherited errors are smaller. Combine masks
before applying Gram. Surviving zeros have EVERY detecting length in
one of four OPEN exponent gaps:
(49/300,41/250), (49/250,41/200), (49/200,41/150), (49/150,41/100).
The integer-power coverage is exact; a fractional power is not allowed.
The detector's upper range N9/20 log^2T is retained before taking N large.

Primary mean-value locator checked: Tao254A Notes6,13Feb2015,
Exercise2(ii),eq3; the needed weaker estimate is also fully proved in
the module. This uses no unrelated zero-detector statements on that page.
Sol theory/actual-file PASS; seven guards normal0.050s/-O0.048s.
No numerical zero computation or post-stop execution claim. The signed
sum over surviving detector pairs, full Goldbach margin and goal stay OPEN.

Next concrete question: can the ACTUAL signed zero-detector equation
be retained, instead of only the magnitude threshold? Remove ALL
middle-strip Type II zeros, including ones also Type I: the already
proved restricted Type II count should give the same N^-6/125 energy.
After combining that mask with exterior/good-length masks, every
survivor would have |I(rho)|<1/3 for the exact contour detector I,
and every good-length D_M would be below1/(3logT). The source identity
1+sum_all D_M(rho)=I(rho)+O(T^-1/2), with fewer than logT lengths,
then predicts Re sum_bad_lengths D_M(rho)<=-1/3+o(1), hence<=-1/4
eventually. Test all constants, masks, dyadic endpoints and the actual
source Gamma correction. This would give a common signed polynomial
condition, but is NOT itself the missing signed Goldbach estimate.

A related bounded test may use mixed products D_M^r D_H^s to exclude
simultaneous detections whose product length falls in the same paid
window. Do not assume this forces one gap per zero: the algebraic
length exponents51/250=.204 and51/125=.408 lie in different gaps,
but all nonnegative integer combinations are multiples of.204, missing
[.82,.98] (4*.204=.816,5*.204=1.02). This is a candidate length-
arithmetic limitation, not actual zero evidence or a reviewed theorem.
Prioritize retaining the signed detector equation. Fresh <=30 minutes.

## 2026-09-10: a common signed detector disk for actual survivors

Started00:13:23 UTC, reassessed00:22:12 UTC, progress. Resumed verified
clean main4dadb63. Reviewed mathematics **ec39d86**, signed_zero_detector.py.
The preceding native turn made progress by isolating four detector-length
gaps. This pursuit removes ALL middle-strip Type II zeros, including ones
also Type I. The already proved restricted count gives the same energy
N^-6/125 times logs. Combine exterior/Type-II/good-length masks before
Gram, using the inequality for overlapping nonnegative energies. Retain
the unmasked arithmetic energy only for the full opposite factor.

There is now ONE common polynomial H_N, the sum of all allowed bad-length
detectors, such that EVERY surviving actual zero copy satisfies
|1+H_N(rho)|<=3/4. The source smoothed zero identity, inclusive dyadic
endpoints and fewer-than-logT block count give the disk uniformly for
sufficiently large N. Thus Re H_N<=-1/4 and 1/4<=|H_N|<=7/4,
with |1/H_N|<=4. Its support is <=2N41/100. The corrected negative
Gamma argument remains in force; no source Hypothesis F is imported.

The finite inverse identity has the necessary minus sign:
1=-H_N sum_(j<J)(1+H_N)^j+(1+H_N)^J. The actual residual zero
field has norm O((3/4)^J N21/100 L), paying its crude coefficient
energy N21/50 L and the Gram logarithm. A degree of order logN is
SUFFICIENT for power-small error by this bound. Its straightforward
support majorant is exp(O((logN)^2)), outside the existing fixed-power
estimate. Neither statement is a minimal-degree/length obstruction;
different cancellations, resummations or improved energies may help.

Independent Sol theory and actual-file PASS; seven guards normal0.002s
and -O0.002s. Primary source Appendix C of Maynard--Pratt2206.11729v2
was reread; no new numerical zero run or repeat finite Goldbach experiment.
The disk is signed arithmetic information, not the sign of the paired
kernel. The surviving smooth band remains O(N); the full signed margin,
universal coverage and overall research goal stay OPEN. No post-stop
execution claim, push, publication or manual continuation queue.

Next concrete question: does multiplication by this ACTUAL common H_N
produce a useful prime-product window with a controlled error? Writing
H_N(s)=sum h_N(n)n^-s, the finite zero sum gives the exact dilation
identity H_N acting on S_T(x)=sum h_N(n)n^-1/2 S_T(x/n). The hoped
prime-side expression has coefficient (h_N*Lambda)(k), with the SAME
window Fourier kernel at T log(k/x). This must be derived with actual
zero real parts, source Gamma terms and all summed error costs retained.
Here n can reach2N41/100, so T=N9/10 exceeds x/n; the previous
central-window bound cannot simply be applied at the dilated scales.

Prediction to test, not a theorem: the transfer error can remain smaller
than the N-scale paired target when summed with these specific h_N.
Then compare (h_N*Lambda) with the exact full coefficient identity
(a_T*Lambda)=mu_<=B*log, keeping the bad-length and smoothing masks.
The concrete falsifier is an unpaid main-scale transfer cost or a claim
that drops the residual restriction. A successful identity alone would
still leave its signed prime-pair estimate to prove. Fresh <=30 minutes;
retain useful polynomial and disk components if the proposed use fails.

## 2026-09-10: full detector field to prime products, with the mask gap retained

Started00:23:34 UTC, reassessed00:36:45 UTC, progress with a precise
remaining limitation. Resumed verified clean main85252c3. The previous
native turn made progress through the signed common detector disk.
Reviewed mathematics **5bd0b48**, detector_prime_product_transfer.py,
proves the full-field transfer for ANY coefficients |b(n)|<=A tau(n)
supported on n<=2N41/100, uniformly also for N-dependent A:
S_B(x)=-P_(b*Lambda)(x)+O(A N41/200 L7), x in[N/4,3N/4].
The exact dilation factor is n^-1/2. Its smaller arguments reach
N59/100/8, where T can exceed the prime-window center. The Ingham
tangent D(u)<=1-(4/3)(.5-u), with exact nonnegative difference
(1-2u)^2/[3(1+u)], gives W_T(y)<<T L6 uniformly. The localized
complex shift, global Taylor/Fourier tails, poles and Gamma integral
are all paid before summation. No short-interval prime bound below
length one is assumed.

The exact majorant |b*Lambda|<=A(tau log)/2, including prime powers,
and tau^2<=tau4 give coefficient square sum O(A^2 L5). Schur on
the PRODUCT index k~N has row N/T and column1/T, proving full-field
energy O(A^2 N L5). For the actual detector, exp(-n/sqrtT) can be
removed in this full normalized L2 norm with error N^-1/25 L5/2;
the separate normalized transfer error is N^-67/200 L7. This is not
a pointwise replacement at each survivor zero. The bad dyadic mask
survives, and the unrestricted identity a_T*Lambda=mu_<=B*log leaves
an explicit residual convolution. Conditional prime and semiprime
coefficient examples and exact prime-log fixtures guard that boundary.

The hoped transfer of the SURVIVING pair still needs H-weighted energy
for the removed zeros. Their old unweighted small energy is insufficient
for this step. Crude coefficient amplification gives positive attempted
upper exponents361/1250 for G and309/1250 for Type II, not actual
lower bounds. The reviewer proposed an aggregate H^2 fourth-moment
repair; the lead caught that it substituted the maximal product length
.82 for shorter terms under a negative coefficient exponent. Reviewer
explicitly RETRACTED it. A component at m=.35 has squared length .7,
giving normalized time exponent7/125>0. Preserve this correction; no
masked-energy improvement from that shortcut is promoted.

Independent Sol theory and actual-file PASS after that adjudication.
Seven new guards normal0.059s/-O0.045s. Ingham's source display in
Yashiro1310.0765v2,p2,(1.1) was freshly read; the earlier unconditional
Guinand conventions and source corrections remain. No actual numerical
zero run, new Goldbach range, publication, push or manual wake queue.
No new weighted finite-period J transfer is asserted: those errors
would need fresh bounds with the new weights. The survivor pair estimate,
full signed margin, universal coverage and overall goal stay OPEN.

Next concrete question: can mixed moments pay PART of the H-weighted
good-detector mask while retaining the actual dyadic product scale?
For X_M={middle-strip zeros detected at a good M}, and a bad multiplier
length H, test integers r,s>=1,r+s<=100 with
P=M^r H^s in[N41/50,N49/50]. The polynomial D_M^r D_H^s has
coefficients bounded by tau_(2(r+s)) on(P,2^(r+s)P]. The same
variable-beta mean-square proof predicts normalized moment N^-4/625
times fixed logs. The M threshold bounds the 2s moment of D_H on
X_M; Holder with the existing E_(X_M)<<N^-4/625 times logs should
then bound its weighted second moment with a saving. Pay threshold
power r, Holder weights, copy/length sums and all boundary terms.

Determine which actual pairs (logM/logN,logH/logN) satisfy this
integer-product criterion. Do not infer universal coverage: (.45,.35)
has its smallest mixed sum .80 and every higher one exceeds .98.
The concrete test is a reviewed sufficient weighted-mask deletion and
an exact uncovered-pair record, not another aggregate-upper-support
substitution. If the masks or costs defeat it, retain the counterbudget.
This test is UNREVIEWED and receives a fresh <=30 minutes.

## 2026-09-10: compatible weighted detector masks paid at actual product lengths

Started00:38:54 UTC, reassessed00:49:13 UTC, progress. Resumed verified
clean main94e5784. The preceding native turn made progress through the
full prime-product transfer and identified its survivor-mask limitation.
Reviewed mathematics **5b7dd4e**, mixed_detector_weighted_mask.py.
For a good detecting length M and bad multiplier length H, a mixed
product D_M^r D_H^s with actual P=M^r H^s in[N41/50,N49/50]
and r,s>=1,r+s<=100 has normalized moment N^-4/625 times logs.
The same variable-beta proof and positive layer cake apply to its
actual support(P,2^(r+s)P]; no maximal-support substitution is made.
The M threshold costs2r log powers, and Holder in the positive copy
measure with E_(X_M) preserves the N^-4/625 second-moment saving.

Coverage uses ANY compatible good detector for EACH bad multiplier H.
For fixed H, assign a copy to its least compatible good detecting M;
the assignment is disjoint only in M, while the H overlap is paid by
Cauchy. The aggregate C_cov has coefficient energy N^-4/625 L40230.
It is a one-coordinate weight on rho, so Gram and the full opposite
arithmetic norm give the central paired exponent623/625. NEW weighted
finite-period errors are explicitly paid: Cauchy over O(TL) copies
bounds its l1 norm by N^(9/20-2/625), while the improved full l1 norm
is N2/5 times logs. J-minus-beta costs exponent2367/2500; the beta
endpoint costs-2133/2500, with the actual small-real-part denominators.
Thus the covered one-coordinate ACTUAL J sum is all-log small.
No full H-weighted G deletion or nonindicator union identity is claimed.

The compatibility set is an exact finite union of strips
.82<=r*m+s*h<=.98. For m in[.44,.45], only r=1,s<=3 can work:
the first bad gap is wholly covered with s=3, the second with s=2,
the third iff h<=(.98-m)/2, and the fourth iff h>=.82-m.
Product-window equality is included. The remaining pieces are open.
The closed rectangle m in[.44,.45],h in[.34,.36] is uncovered by
this criterion; a different good detector on the SAME zero may still
pay a multiplier. This is a length-arithmetic limitation, not an
actual-zero population claim or a barrier to every weighted moment.

Independent Sol theory/actual-file PASS. Eight guards normal0.359s,
-O0.400s. The weighted kernel proof was checked against the existing
uniform stationary expansion and actual beta endpoint proof; no new
external theorem was imported. Prior source corrections and the rejected
aggregate H^2 shortcut persist. No new numerical-zero or finite-Goldbach
experiment, publication, push, or manual wake queue. Overall goal,
surviving signed correlation and universal coverage remain OPEN.

Next concrete question: can we pay the ENTIRE H_N-weighted mask of
zeros detected at ANY M with m in[.44,.45], by trading its stronger
M-specific energy against a higher H moment outside the fixed window?
This is a different sufficient estimate, not a retry of the failed
integer-strip membership. Candidate derivation, not yet promoted:
partition beta in[16/25,19/25] into360 bins of width1/3000. At lower
bin edge sigma, write u=1-sigma. D_M^2 has length N^(2m)<=T and
predicts bin energy exponent eM=.9-2m+(4m-2)u, plus2/3000 for
the maximum N^(2beta-2) weight in the bin. Its detector threshold
and logs must remain explicit.

For a fourth-gap multiplier with h<=.38, H^3 has length N^(3h)>T;
its sixth moment pays the POSITIVE possible exponent2u(3h-1), not
a fictitious saving. Holder with exponents2/3 and1/3 predicts
 .6-(4/3)m+u[(8/3)m+2h-2] <=-1/375.
The beta-bin loss2/3000 leaves at least1/500 saving. Combined with
the already paid h>=.82-m (which is <=.38), this could cover the
ENTIRE fourth gap. For the third gap, H^4 and Holder3/4,1/4 give
 .675-1.5m+u(3m+2h-2) <=-17/1000,
before the same bin loss, covering its entire range as well. Gaps1/2
are already covered by the present mixed criterion.

Concrete test: prove these bin moments and every threshold, count,
Holder, union, complex-coefficient and J-kernel transfer cost, then
check whether some good detecting M in[.44,.45] suffices even if
other detected lengths occur. The predicted final coefficient energy
is N^-1/500 times fixed logs. If the binning or moment supports defeat
the gain, preserve the precise failure. This new hypothesis receives
a fresh <=30-minute test and independent correctness review; no claim
yet that the uncovered rectangle or a complete weighted mask is paid.

## 2026-09-10: all middle and low detector-weighted masks paid

Started00:50:45 UTC, reassessed01:07:16 UTC, progress beyond the initial
high-M test. Resumed verified clean main5908ff7. Previous native turn
made progress through compatible mixed weighted masks. Reviewed math
**b42ab25**, weighted_detector_mask_bridge.py, now pays the FULL H_N
weight on every removed middle-strip zero and every low-exterior zero.
The high-exterior H-weighted field is the sole unpaid component of this
particular survivor-to-prime-product bridge; the signed paired estimate
is still a separate unresolved step.

The initial hypothesis did pass: good detector m in[.44,.45] plus
pure multiplier powers6,5,4,3,2 across the four bad gaps gives energy
N^-1/500 L50 after360 beta bins of width1/3000. The support switch
is explicit: powers>=3 have length exponent>.98, while the upper
fourth-gap square is below.82. Longer-than-N moments pay their positive
cost. That valid component is retained, but the actual source Type II
count permits a stronger synthesis.

For ALL middle Type II zeros, including overlap with G, their bin energy
exponent is-u/5+2Delta. Holder with those same pure multiplier moments
has worst unbinned exponent-6/625; the bin loss1/1500 leaves
-67/7500, weakened to-1/125. Logs remain fixed and all bad lengths
are summed. Then take X=G minus II. Every GOOD M has a pre-threshold
full-middle moment of D_M^k with energy N^-4/625, for its licensed k.
Holder on X against E_X<=E_G preserves that saving, WITHOUT assuming
that X is detected at this particular M. Sum good polynomials into A_N.
The saved source equation H_N=-A_N-1+I_T+small has |I_T|<1/3 on X,
so it pays H_N after charging the constant term by E_X. Consequently
the ENTIRE middle removed set G union II has H-weighted energy
N^-4/625 times logs. This uses actual estimates with the identity;
it does not mistake the identity alone for a correlation bound.

For the low exterior beta<=16/25, use powers4,4,3,2 on the four
bad gaps. Their actual product exponents lie in[49/75,41/50].
The variable-beta mean-square proof extends to[0,16/25]; positive
layer cake keeps the N^-2 baseline. Its worst normalized moment is
-11/3750. Holder with the stronger saved low-set energy, followed by
the two bad-length logs, gives E_(D_low,H)<=N^-11/3750 L72.
Union weighted energy is bounded by the sum, including middle overlaps.

Gram gives normalized covered-field norm N^-11/7500 times logs.
The opposite field alone uses arithmetic energy O(1). Newly weighted
J-minus-beta and endpoint bounds give exponents3557/3750 and
-3193/3750, below the central7489/7500. The exact cutoff central
L2 field relation is now
 Z_(H,R)=-P_(h*Lambda)/sqrtN-Z_(H,D_high)+O_L2(N^-11/7500 L^C).
The full-field transfer error N^-59/200 L7 is smaller. No small bound
for Z_(H,D_high), inverse operator, full pair sign or universal coverage
is inferred. The surviving disk and all polynomial components persist.

Independent Sol theory and actual-file PASS for the consolidated proof,
including the Type II synthesis, low-real-part extension and exact field
decomposition. Eight guards normal0.031s/-O0.032s. No new external
theorem, numerical-zero campaign or finite Goldbach range was imported.
All earlier source corrections, runtime limits, the aggregate H^2
retraction, no-push/publication and no-manual-wake boundaries remain.
The overall research goal stays OPEN; no post-stop execution is claimed.

Next concrete question: can the remaining H-weighted HIGH exterior
beta>=19/25 be paid by actual density bounds, moment interpolation
and the signed detector equation? First test the critical candidate
corner beta=5/6, u=1/6 and bad multiplier exponent h=2/5. The
retained Huxley count has exponent3u/(2-3u)=1/3 in T, giving
normalized coefficient energy exponent-1/30 at T=N9/10.
The H^2 moment (p=.8<T exponent.9) gives+1/30, and H^3
(p=1.2) gives+1/15. Holder respectively with weights1/2,1/2
and2/3,1/3 gives ZERO in both cases. Do not call that a saving
or infer that actual zeros occupy the corner.

Concrete test and falsifier: verify the strongest applicable primary
zero-density input at that real part, then determine whether a uniform
strict saving survives the real-part and dyadic-length neighborhoods.
If the existing ingredients reach only zero, preserve the exact scope
of that method limitation and seek an additional arithmetic input; do
not repeat the same integer-moment search under a new name. Source
2507.15184v2 Corollary1/Table1 is an existing locator for comparison,
not unverified authority for a stronger exponent. If extending the
source Type II count above19/25, recheck its uniform Gamma bound,
copy count and beta range before using it. Near beta=1 a fixed bin
width or fixed source epsilon can overwhelm the zero-free saving;
retain the known log-power/Vinogradov--Korobov boundary. This next
high-exterior hypothesis is UNREVIEWED and gets a fresh <=30 minutes.

### 2026-09-10: high weighted exterior paid; survivor transfer closed

Pursuit01:08:59--01:22:55UTC, reassessment: progress. Research commit
45f87c0, high_detector_weighted_bridge.py. The old Huxley zero-saving
corner was not a barrier: a stronger KNOWN Ivic density estimate gives
base energy-19/300 at beta5/6, hence square/cube Holder-3/200,-1/50.
Primary research source TTY2501.16779v1 Table2 p33 and its authors'
maintained ExpDB Corollary11.31 were checked. No novelty/priority claim.

On[4/5,7/8), pure bad powers6,5,4,3 plus that epsilon-loss density,
750 fixed bins and fixed epsilon1/10000 give weighted energy
N^-1/200 L153. On beta>=7/8 use classical Huxley LOG powers with
relative u bins(.99v,v]; exponent-47v/650 plus v/50 becomes
-17v/325<-v/20. VK and O(loglogN) bins give all-log decay.
No fixed epsilon is used near1.

On[19/25,4/5), the source Type II proof extends with corrected
negative Gamma argument, uniform delta in[.26,.3], existing mollified
fourth moment and copy count. Pure moments now switch at h=.39;
the old .38 switch would leave a positive cost. Four hundred fixed
bins preserve N^-1/400. On non-II copies, GM plus EVERY good
polynomial's full moment gives the same saving: licensedk>=2, p<.9
uses convexity with worst-11/3500, and p>=.9 is easier. The bin
and source loss29/100000 is paid. The signed equation H=-A-1+I+small
then controls H, including the constant term. No detection predicate
or arbitrary masked arithmetic norm is assumed.

Thus the entire high H-weighted energy is at most fixed logs times
N^-1/400+exp(-c(logN)^(1/3)/(loglogN)^(1/3)). Together with the
previous middle/low bounds, ALL removed H-weighted zeros are paid.
The exact central norm relation is now
 theta*Z_(H,R)=-theta*P_(h*Lambda)/sqrtN+O_L2,A(logN^-A).
The bad mask and smoothing remain in h. The new one-coordinate
actual J contribution of removed copies is all-log small; its
weighted J-minus-beta and beta endpoint errors are separately paid.

Independent Sol theory and actual-file PASS, no material correction.
Eight new guards normal0.101s/-O0.083s. No old experiment repeated,
numerical zero campaign, push, manuscript, publication or manual wake.
Earlier source corrections, runtime limits and polynomial components
remain. The overall goal stays ACTIVE and mathematically OPEN; no
post-stop execution is claimed.

Next concrete test: does the survivor disk Re H<=-1/4 yield a
coercive inequality for the actual Gram synthesis or reflected pair?
First test the proposed inference in the exact finite Gram form,
including off-diagonal packet overlap. If disk information alone
fails, identify the precise missing term with the actual common H
and prime-product transfer, then test it against retained moments.
Falsifier: an unpaid commutator/inverse/correlation term, or a finite
countermodel to the disk-only implication; such a model is not an
actual-zero counterexample or an all-method impossibility. Do not
promote pointwise bounded reciprocals into an operator bound. Fresh
<=30min; this next hypothesis is UNREVIEWED.

### 2026-09-10: disk coercivity falsified; actual short-shift overlap isolated

Pursuit01:24:30--01:39:27UTC, reassessment: changed under evidence.
Research commit8173dbe, detector_gram_coercivity.py. The exact Gram
form is Re(c*GDc), not a coefficientwise negative sum. An artificial
two-packet witness withr=19/20 and multipliers-1+-i/2 has norm7/20
and POSITIVE mixed form1/8 despite both values lying inside the
survivor disk. Another coefficient choice has bounded pointwise
reciprocals but a synthesized inverse quotient diverging asr tends1.

The strengthened model uses a COMMON real bounded-coefficient
Dirichlet polynomial in one actual allowed bad-length block.
With beta=.7, alpha=atan(.5), t=pi+alpha, m=2alpha/t~.2572076,
delta=t/logN, averaged mean value selects gamma0 with a well-conditioned
two-real-component interpolation. Its coefficients have |b|<=1 and
produce values-1-i/2,-1+i/2+o1. Actual-shaped c coefficients have
ratioe^it(1+o1); normalized norm tends2-4/sqrt5, mixed form tends
sqrt5-2>0. These are ARTIFICIAL frequencies and designed coefficients,
not actual zeros, actual Mobius coefficients or all survivor predicates.
The raw scaleN^-3/5 explicitly does not disprove an ACTUAL estimate
with additive all-log error. The homogeneous disk-only step fails;
special arithmetic coercivity remains open. The exact commutator
retains sum h(n)(n^-sigma-n^-rho); its available derivative upper
budget losesN369/2500 and supplies no small relative norm.

The actual mixed conjugated overlap C_R transfers with all-log error
to (1/N)Re int theta² P_h conj(P_Lambda). Its exact coefficient
kernel K_N(k,l) has sizeT^-1(1+|k-l|/(N/T))^-B. The prefactor
isT²/(4pi²N). For |k-l|>N^.1logN, the Schur norm is
(N/T²)L^(1-B); the coefficient norms addL³, so the tail isL^(4-B).
Prime and square diagonal coefficients vanish; higher powers are
N^-23/30L², using the actual small-prime Mobius cancellation and
the bounded prime-power exponent whenever p>B=2N^.009.

All proper powers are also paid separately. Divisor Cauchy gives
sum|h*Lambda_pp(k)|²/k<=N^-59/200 L11, using tau³<=tau8.
The normalized window norm isN^-59/400 L^(11/2). Opposite proper
powers costN^-1/4 L4 in the mixed overlap. Hence, with all-log error,
C_R equals the exact nonzero-shift sum with h(n), K_N(nm,nm+r),
and TWO PRIME conditions m andnm+r, for0<|r|<=N^.1logN.
The bad cofactor mask, damping, complex kernel and target N persist.
No sign, decay or small constant is proved for that remaining sum.
Its conjugation differs from the original reflected Goldbach pairing.

Independent Sol theory and actual-file PASS, including the final
proper-power strengthening. Nine guards normal/-O0.001s. No old
zero/Goldbach experiment, manuscript, push or manual wake. All prior
source corrections, components and runtime limits remain. The overall
goal is ACTIVE/OPEN; no execution after this checkpoint is claimed.

Next test: expand the specific truncated-Mobius coefficient BEFORE
Cauchy in the ACTUAL short-shift sum, and determine whether averaging
the nonzero r gives a signed saving beyond the current O(L^(5/2))
overlap bound. Keep both prime conditions, all masks and the complex
kernel. Success requires an actual estimate, not formal cancellation
of a predicted main term. Falsifier: an explicit residual or loss
which still consumes the shift-average gain; preserve useful factors
without calling this an all-method barrier. Do not repeat the completed
Gram models, diagonal or proper-power work. Fresh <=30min, UNREVIEWED.

### 2026-09-10: completed short-divisor field suppressed; complement retained

Pursuit01:41:02--02:04:10UTC, reassessment: changed under evidence.
Research commitde84c06, short_divisor_overlap.py. For every possibly
N-dependent |b_d|<=1,d<=B=2N^.009, let
v_b(k)=sum_(d|k,d<=B)b_d log(k/d). With the same T=N^.9,V=N^.125,
Hwin=N/T and cutoffs, the actual central field satisfies
 sup_x |P_vb(x)|/sqrtN
 <<_(M,K) L^2(T^-M+V^-K)+L(B/Hwin)^M=O_A(N^-A)
after choosing fixed M,K for each A. The completed complex overlap
with P_Lambda is therefore also O_A(N^-A).

The initial proof used BV in moduli d<=B, fixed-shift weighted
variation L/(NT), then Poisson on reduced residue classes. It pays
the actual prime discrepancy O(L^(1-D)), freezing BL/T, cutoff
BLV^-K and opposite proper powers N^-1/4 L4. The primary Ford
Sieve Methods2023 Theorem3.4 printedp35 states pi-minus-li; log-Abel
costs an extra logarithm. This is a valid alternative all-log proof.

During audit a stronger elementary proof emerged: the COMPLETED
field is already small without prime distribution. For
f_d,x(u)=log(u/d)u^-1/2 F(Tlog(u/x)), its Mth derivative integral
is O_M(LN^-1/2 Hwin^(1-M)). Nonzero progression Poisson modes sum
to L(B/Hwin)^M after normalization. The zero mode uses the exact
u=x exp(y/T) substitution and Taylor ONLY on the compact cutoff.
All full hatChi moments vanish because chi is supported away0;
cutoff moment tails cost V^-K and the Taylor remainder T^-M.
Summing 1/d costs another L. Thus BV is unnecessary for this saving,
which supplies NO new two-prime correlation ingredient. The result
is stronger than a formal identity but still concerns completion.

For actual a_B=mu_<=B*1, a_B*Lambda=mu_<=B*log uses ALL Lambda
prime powers on the left. Set r_B=a_B-delta_1-h. Exactly,
 C_h+C_r=-E_Lambda+O_A(N^-A), E_Lambda>=0 and O(1).
The complementary cofactor lengths, damping corrections and long
cofactors beyond the original detector list remain in C_r. No sign
for C_h follows; no positive lower bound for E_Lambda is asserted.
The survivor's conjugated overlap connection still has its inherited
all-log error and remains different from reflected Goldbach pairing.

Independent Sol theory/actual-file PASS including the stronger
elementary proof. Nine guards normal0.007s/-O0.006s. An initial
review concern about the L5 coefficient norm was retracted: the
fixed annulus has 1/k=O(1/N), so the tau4 mean costs only L3,
plus L2 from the coefficient. No old experiments, manuscript,
publication, push or manual wake. The overall goal remains ACTIVE
and OPEN; no execution after this checkpoint is claimed.

Next bounded test: restrict the complementary cofactor to n>=N^.6.
Then the product window forces m<=2N^.4 and the expanded moduli
q=dm are below4N^.409, within BV. Keep all Lambda(m), endpoints,
and the complex kernel. Test whether the modulus multiplicity can
be paid by sum_(m|q)Lambda(m)=logq and whether the reduced-residue
Poisson main can be bounded when q>=Hwin, where it no longer
vanishes automatically. Success is an actual saving for this
complementary range with every error paid. Falsifier: an unpaid
resonance, main term or modulus loss. The original bad range
n<=2N^.41 is not brought inside BV's level by this observation.
Fresh <=30min; this proposed estimate is UNREVIEWED.

### 2026-09-10: first-power polynomial norm route fails

Pursuit02:25:27--02:45:30UTC, reassessment: changed under evidence.
Commit151e7c9 records that for b=a_B restricted to N^.41<=n<N^.46,
the retained first-power T-term exponent at beta=19/25 is
21/50-(13/25)h>0 throughout the strip (517/2500 down to113/625).
The second-power detector moment is saving and licensed, but it controls
D_M^2 on detected zeros, not the first-power arithmetic coefficient.
The detector threshold does not provide a lower bound on the nondetected
complement, and Holder cannot identify the missing field. Transfer and
proper-power errors at support .46 remain small. Independent review PASS;
five guards normal/-O passed. This limits one route and preserves the
successful k=2 machinery and paid tail.

Next bounded question: decompose n<N^.41 bilinearly with a genuinely
short factor, preserving both reflected prime conditions and endpoints.
Type I requires progression Poisson; Type II requires a sourced bilinear
mean-square. Any positive exponent or unpaid endpoint is a falsifier.
Fresh <=30min; UNREVIEWED.

### 2026-09-10: large cofactors paid in the actual reflected band

Pursuit02:06:50--02:23:12UTC, reassessment: progress. Research
commit9470731, large_cofactor_overlap.py. The actual cofactor tail
n>=N^.51 has an all-log-small complex overlap, both conjugated and
NONCONJUGATED reflected. This improves the proposed .6 cutoff.
Every fixed eta>.509 works, with no claim at the boundary or of an
effective onset. The bad cofactor ranges remain below the cutoff.

Expanding a_B gives moduli q=dm<=4N^.499. Their error multiplicity
is bounded by sum_(m|q)Lambda(m)=logq. All left prime powers remain;
the opposite proper-power replacement costs N^-1/4 L4. Fixed-shift
variation is1/(NT); the actual hard cofactor boundary contributes
one paid jump. Ford Sieve Methods2023 Theorem3.4 was freshly checked;
its prime-count statement costs an extra log under log-Abel. BV pays
the actual discrepancy O(L^(1-D)), not just a predicted mean.

Reduced-residue Poisson main terms need NOT vanish at large moduli.
Divisor inversion splits their lattices: small spacing is annihilated
by the missing Fourier frequencies; the remaining direct lattice
sums are O(1). Hence the residue main is O(tau(q)). Elementary
totient and harmonic divisor bounds give total main N^-1/10 L9,
freezing N^-9/10 L5 and Fourier cutoff N^-2 L5.

The reflected form was proved separately: l=N-k+r, c=k/(N-k),
leading correlation D_c(s)=int hatChi(y)hatChi(s-cy)dy and transform
(2pi)^2 chi(-c*xi)chi(-xi). BV residues are N+r modq. Shifted Poisson
lattices retain their target-dependent phases, with the same tau(q)
bound. This is not an inference from the conjugated estimate.
Using the established FULL-field Guinand/beta/finite-period bridge
and only THEN splitting the arithmetic coefficient gives
 sum_(actual rho,sigma)chi(gamma/T)chi(gamma'/T)J_N(rho,sigma)/N
       =-R_h-R_(r_<)+O_A(L^-A),
 r_<=a_B*1_(n<N^.51)-delta_1-h.
All zero copies in that full T=N^.9 band remain. No new masked-zero
norm, weighted J replacement or positive reflected energy is assumed.

Independent Sol theory and actual-file PASS. Review corrected the
inherited central formula's rate to S_T=-P+O(N^.1 L6), giving
normalized cross N^-2/5 L6 and square N^-4/5 L12; these suffice.
Eleven guards normal0.010s/-O0.014s. No old experiment, numerical
campaign, manuscript, publication, push or manual wake. All earlier
source corrections, polynomial components and runtime limits persist.
The core belowN^.51, its signed combination with h, other heights
and Goldbach coverage remain OPEN. Overall goal ACTIVE; no execution
after this checkpoint is claimed.

Next question: can the prime companion's conductor factorization
extend the paid range to N^.46<=n<N^.51? First pay left proper
powers using the bounded cofactor support. Then m is prime and m>B;
a conductor dividing dm either divides d or contains m. Derive the
exact character decomposition, preserving induced coprimality masks,
cofactor endpoints and reflected target phases. Test low conductors
against the bandpass cancellation and large conductors against a
fresh primary mean-square/large-sieve source. The tentative shift
average suggests a q<N^.55 threshold, but that is only a heuristic
until all weights and losses are paid. Success requires an actual
saving on this named range. An unpaid small-conductor, endpoint,
character multiplicity or Cauchy loss falsifies the proposed step.
Fresh <=30min; this next hypothesis is UNREVIEWED.

### 2026-09-10: prime-companion conductor gap lowers the cutoff to N^.46

Pursuit02:25:27--02:44:21UTC, reassessment: progress. Research
commitbda7f22, prime_companion_dispersion.py. Both actual conjugated
and nonconjugated reflected overlaps for N^.46<=n<N^.51 are
all-log small. Together with the previous tail result, this pays
every n>=N^.46. The bad range below2N^.41 and the signed core remain.

Both prime powers are paid BEFORE the conductor step. The left
cofactor support N^.51 gives energy N^-49/200 L11 and norm
N^-49/400 L^(11/2); the opposite error stays N^-1/4 L4.
For prime m>B and q=dm, low conductors divide d; all others contain
m. The exact low projection is 1_(m does not divide a)A_d(a)/(m-1),
with a=r or N+r. BV on only d<=B gives error L^(2-D), including
the harmonic companion sum. Its mean is the full reduced-residue
mean, whose resonant tau(q) bound was already paid.

Harcos's primitive large sieve Theorem2 p1 was checked directly.
Binary intervals handle max endpoints BEFORE residue orthogonality.
Central primes p>q make induced lifts exact; their total weight is
at most L2/phi(f). Dyadic conductors and tree levels give maximal
all-residue high variance (NQ+N^2/M)L8. Periodized r weights avoid
a repeated-residue loss. The normalized high bound is
L6*(N^-1/1000+N^-91/2000). No cancellation in mu(d) is assumed.

The actual normalized full T=N^.9 band is now
 sum chi*chi*J_N/N=-R_h-R_(r_core)+O_A(L^-A),
 r_core=a_B*1_(n<N^.46)-delta_1-h.
The full-field bridge and its corrected errors are inherited with
their original scope. No weighted J, masked-zero or positive reflected
energy inference is made. Other heights and Goldbach coverage remain open.

The proof is uniform in literal cofactor endpoints. Stieltjes
superposition pays tail profiles with bounded |f(U)|+Var(f), U>=N^.46.
Review explicitly required the amplitude as well as variation.
Consequently auxiliary a_B(n)exp(-n/N^.47) has both overlaps small:
the below-cutoff difference is N^-.01 tau(n), and the remaining
profile has bounded amplitude and variation. The original N^.45
detector and zero masks are not automatically changed by this result.

Independent Sol theory, actual-file and profile-extension PASS.
Eleven guards normal0.017s/-O0.011s. No old experiment, manuscript,
publication, push or manual wake. All source corrections, runtime
limits and useful polynomial components remain. Goal ACTIVE/OPEN;
no execution after this checkpoint is claimed.

Next concrete test brings those polynomial components back into the
arithmetic reduction: can b=a_B*1_(N^.41<=n<N^.46) have
||theta*P_(b*Lambda)/sqrtN||_2=O_A(L^-A)? Try fourth moments
on compact beta strips and sixth moments near1, paired with the
retained actual zero-density bounds. Verify each density source's
range and epsilon/log distinction; near1 needs relative bins and
the zero-free region, not fixed epsilon. Pay full-field transfer at
upper cofactor scale N^.46 rather than citing the old N^.41 error
unchanged. Success removes this adjacent band by an actual norm
bound. An unpaid exponent, endpoint or transfer loss falsifies the
proposed step. Fresh <=30min, UNREVIEWED; no arbitrary zero mask.

### 2026-09-10: first-power polynomial norm route fails

Pursuit02:25:27--02:45:30UTC changed under evidence; commit151e7c9.
The first-power T-term exponent for b=a_B on N^.41..N^.46 is
21/50-(13/25)h>0 at beta=19/25. The k=2 moment is saving but
controls D_M^2 on detected zeros, not the first-power arithmetic field.
The threshold gives no lower-bound bridge on the nondetected complement.
Independent review PASS; five guards normal/-O passed. Preserve k=2
and the paid N^.46 tail.

Next bounded question: decompose n<N^.41 with the exact retained Vaughan
identity, preserving its free convolution factor, both reflected prime
conditions and hard endpoints. Test Type-I Poisson and a sourced Type-II
bilinear mean-square. Any positive exponent or unpaid endpoint falsifies
the route. Fresh <=30min; UNREVIEWED.

### 2026-09-10: balanced Vaughan core test

The new bounded test `core_vaughan_type_i.py` asks whether the exact balanced Vaughan decomposition can close the remaining n<N^.41 core. It shows Type-II is structurally absent because U*V=N^.499>N^.41. Type-I still fails the available progression route: d<=N^.2495 and a reflected companion m<N^.59 produce modulus dm up to N^.8395, beyond BV level N^.5; fixing d leaves a linked two-prime condition. Exact identity guards and direct checks pass, with pytest unavailable. Preserve this as a limitation of the balanced Type-I route, not an all-method impossibility. Next question: find an arithmetic estimate for that linked Type-I correlation or a deliberately unbalanced decomposition that creates a genuinely usable Type-II range, while retaining endpoints and both prime conditions.

### 2026-09-10: active-band Vaughan Type I terms are affordable

The full-minus-low kernel and a coprimality-twisted exact Vaughan identity,
with `U=V=N^(3/40)`, reduce the new active-band arithmetic question to its
Type II term. Complete unit-residue periods cancel for every active frequency.
Hard-endpoint progression discrepancies have size `O(1)` for constant weight
and `O(log N)` for logarithmic weight; Parseval is taken before Cauchy.
Including every `d<=N^.009` and prime `m~N^.59`, the two Type I energy
exponents are `1.348` and `1.498`, below the absolute `H^-1` benchmark
`1.499`; prime powers sit at that benchmark. This is an absolute-budget
result, not the stronger relative energy conjecture. Independent review PASS
and five exact guards pass normal and optimized. The remaining equation is
the `N^(1.499+o(1))` band-energy bound for the exact
`mu_>V*Lambda_>U*1` term. Its diagonal is target-sized; signed off-diagonal
congruences and the final endpoint/kernel transfer remain open.

The reduction sharpens further with `U=1`, `V=N^(3/20)`. The grouped term is
then identically zero and the exact remainder is simply `mu_>V*log`. Its one
Type I complement still has exponent `1.498`. At `N=200000`, `H=3`, all 171
prime moduli in the finite block and `d=1,2`, its measured band/all energy
ratio was `.104735`, versus `1/(pi H)=.106103`; this found no resonance but
has only finite cutoff `V=6`. The live analytic target is cancellation of the
Mobius-weighted off-diagonal character covariance, not a generic `B_U` form.

### 2026-09-10: character diagonal has the H^-1 gain; covariance is open

On a separated `d=1` product box, Gauss expansion gives the exact band energy
`m/(m-1)^2 sum_eta W_m(eta)C_m(eta)`. Here `W_m` is the character sum over
the active h interval and `C_m` is the multiplicative autocorrelation of the
actual Gauss-phased product `A(chi)B(chi)`. The principal eta term is exactly
an `H^-1` fraction of full character energy. Thus the diagonal has the wanted
gain, and the sole model-box obstruction is signed nonprincipal covariance:
positive alignment reinforces, while cancellation proves the target.
Individual L2 bounds do not control that alignment. Three exact finite-field
guards pass normal and optimized; independent review PASS. The product mask,
hard endpoints, d-component, and covariance estimate remain open.

Review correction for the balanced Vaughan test: its Type-II support calculation is a hypothetical Lambda(n_core) diagnostic, not an identity applied to the actual a_B(n_core)*Lambda(m) residual. Also m>=N^.59 in the reflected product; .8395 is only the top-block q=dm configuration, while smaller core blocks permit larger m. The code and handoff now preserve this narrower scope. The actual signed core remains open.

### 2026-09-10: companion Vaughan scale test reviewed

For the actual residual a_B(n_core)*Lambda(m), Vaughan applied to the long companion m~N^.59 yields a linear triple-convolution scale x=n*a in [.41,.6595], with free factor b in [.3405,.59] and x*b~N. The balanced Type-II factors begin at .2495, giving n*a,n*b at least .6595. This is only scale bookkeeping and proves no correlation estimate. Independent review corrected the earlier double-counting. Next question remains a sourced estimate for this linked bilinear form, with all free factors and endpoints retained.

### 2026-09-10: actual companion Vaughan has no Type II term

The scale picture above is only hypothetical composite support. In the paid prime-only replacement used by the actual residual, m is prime. Its exact Vaughan expansion has only the trivial-divisor linear term log m; the low, subtracted and Type-II terms vanish. Six exact guards pass normally and optimized, and independent review PASS. The proposed dispersion pursuit therefore returned `changed-under-evidence`: it dissolved before Cauchy because there is no actual companion factorization to disperse. Preserve the composite ranges as a warning, not an estimate. Next test the equivalent unique-large-prime-factor formulation using a Buchstab or Chen-style switching identity; success requires a one-sided signed estimate, while an upper-bound-only parity remainder falsifies that route.

### 2026-09-10: unique-large-prime switching exposes a signed remainder

The unique factor m>N^.59 gives an exact switch: the current coefficient at k is a_B(k/m)log(m), and n=1 is precisely the desired prime atom. But the composite remainder is not a nonnegative sieve sequence. For distinct p,q<=B with B<pq, a_B(pq)=-1, within the actual core range. Hence a direct one-sided Buchstab/Chen plug-in is invalid. Five exact guards pass normally and optimized; independent review PASS after a bad finite cutoff fixture was corrected. This is a limitation of the direct nonnegative-weight route only. Status `changed-under-evidence`. Next test the complementary large-divisor identity for a_B(n), looking for usable forced factor structure rather than discarding the signed polynomial component.

### 2026-09-10: Maynard 3/5 theorem misses the actual structure

The top-core modulus q=dm has exponent at most .599, just inside Maynard's triply well-factorable 3/5 theorem numerically. Exact source checking rejects the application: the theorem fixes a residue a, whereas N+r varies with target and shift; and the q-support is incompatible with Definition 2 itself. Under the required balanced triple factorization, every factor is at most Q^(1/3), but q contains the prime m~N^.59>Q^(1/3), so a triply well-factorable convolution must vanish on the actual support. Endpoint weights also vary with q/m/r. Three guards and independent source review PASS. Status `changed-under-evidence`. Preserve the .001 exponent proximity as a clue for adapting underlying methods, not as a licensed theorem.

### 2026-09-10: complementary short-divisor boundary tested

For n>1, the exact identity a_B(n)=-sum_(d|n,d>B)mu(d) has a canonical unique-largest-prime partition d=pe with coefficient mu(e). It preserves the signed remainder and moves q=dm strictly above exponent infimum .599, with moduli potentially approaching N. The previous conductor-gap dispersion calculation loses N^.049 at alpha=.41. Four finite exhaustive guards pass normally and optimized; independent review PASS after correcting .599 from an attained/crossing claim to an infimum. Status `changed-under-evidence`. The direct factorability route is abandoned, but the exact boundary expansion is retained. Next test whether keeping its signs and the shift average before Cauchy can recover the explicit .049 loss through a bilinear or spectral estimate.

### 2026-09-10: an additive bandpass target matches the missing exponent

For the full periodized shift lattice, the actual C0 kernel has no zero additive frequency because its transform is supported away from zero. Modulo q it selects |h|~q/H, hence exponent .499 at the top q=.599 block. A genuinely new H^(1/2) arithmetic cancellation would turn the old .049 loss into -.001. Kernel oscillation alone does not prove this; arbitrary discrepancies saturate Cauchy, and truncation/mask leakage remains unpaid. Four guards and independent review PASS. Status `aha-candidate`, new-to-this-task. The next test is the exact additive-character expansion and whether the nonzero-frequency restriction improves the NQ variance term with every actual phase and endpoint retained.

### 2026-09-10: exact Fourier energy gate

The q/H active modes have amplitude H, so their kernel square mass is qH. Parseval shows this is exactly the old residue-space Cauchy budget; localization alone gives no saving. The required new theorem is now precise: active-band prime-discrepancy energy at most H^-1 of total energy, producing H^-1/2 in the correlation. The generic large sieve remains q-dominated because q/H<q. Four guards and independent review PASS. Masks and endpoints can spread the DFT and need separate leakage bounds. Status `changed-under-evidence`; preserve the arithmetic band-energy target, but do not claim the conditional N^-.001 gain. Next test the Gauss-transform/Burgess route with every normalization factor retained.

### 2026-09-10: direct Burgess dual estimate fails the budget

After the H/sqrt(q) transform factor and L=q/H dual length are retained, the Burgess exponent is E_r=h-q/2+(q-h)(1-1/r)+q(r+1)/(4r^2). At q=.599,h=.1 every licensed r>=2 is worse than the direct .1 bound; r=2 gives .1623125. A cost-free replacement q by the prime component m=.59 still gives .160625. Exact guards and independent review PASS. The refined cited result covers r>2, classical Burgess supplies r=2, and r=1 is only a formal endpoint comparison. Status `changed-under-evidence`. This rejects the direct single-character plug-in, not bilinear CRT/induced-character averaging. Next quantify whether d-averaging can possibly pay the remaining deficit.

### 2026-09-10: d-averaging budget is insufficient

At the favorable prime component m=N^.59, r=2 is the best licensed Burgess parameter and misses the direct shift bound by .060625. Square-root cancellation over d<=N^.009 saves only .0045, and even complete d-cancellation leaves a positive .051625 exponent. Four guards and independent review PASS. Status `changed-under-evidence`. This closes only d-averaging as the sole repair; the surviving route must exploit the long m-family, prime coefficients, or a joint spectral estimate. Next derive and source-check that joint m,h form with the target phase retained.

### 2026-09-10: joint high-character Gauss form derived

For q=dm, the high-character shift transform is exactly q^-1 sum_h What(h)e(-hN/q) times a CRT product of d- and m-Gauss sums. High conductor means the prime-m component is nonprincipal. Since active |h| has exponent .499 below m exponent .59, its Gauss factor is always nonzero with magnitude sqrt(m). Four exhaustive guards and independent review PASS. No spectral saving follows: the d component, prime character sums, target phase and mask leakage remain. Status `changed-under-evidence`. Next source-gate a bilinear Kloosterman/spectral theorem against these exact ranges and coefficients.

### 2026-09-10: full high-character collapse redirects the source target

Summing all d-characters and all nonprincipal m-characters before Cauchy
gives the exact normalized projector
`1_(p=a mod dm)-(m-1)^-1*1_(p=a mod d)`. The prime Gauss identity is
`sum_(chi_m nonprincipal)chi_m(p)G_m(conj(chi_m),c)
 =(m-1)e_m(cp)+1` for c nonzero modulo prime m. This is full minus low in
additive Fourier coordinates, not a newly produced Kloosterman phase or a
prime-correlation estimate. Five exact guards and the preceding four CRT
guards pass normally and optimized; independent review PASS. Status
`changed-under-evidence`. The remaining concrete target is an H^-1
active-band energy estimate for the resulting ordinary additive prime sums,
jointly over m and h, with endpoints, masks, the low subtraction and target
phase retained. A full-size diagonal or frequency near-collision falsifies
that route.

### 2026-09-10: a literal energy conjecture and its resonant boundary

For the top block H=floor(N^.1), B=floor(2N^.009), M=floor(N^.59), q=dm,
the new candidate uses the exact high projector, prime weights log(p), target
phase, long m-dependent prime intervals, and Parseval weight
`mu(d)^2*(log m)^2/q`. With signed h, the corrected angular band is
`q/(2*pi*H)<|h|<q/(pi*H)`. The proposed bound is
`E_band <= C*(log N)^20/H*E_all`. It is only a candidate input: an unproved
transfer must still pay shift-dependent endpoints, kernel weights and mask
leakage.

The uniform prime-density Ramanujan mains cancel exactly between the full and
low terms, even when (h,d)>1. But a coefficient-uniform extension is false:
for d=1, coefficients c_p=e_m(h0*p) on all nonzero residues place exactly
`(m-2)/(m-1)` of total energy in the resonant active mode. Thus a generic
coefficient large sieve cannot prove the candidate; the fixed centered prime
weights must be used. Six new guards and the preceding nine identity/CRT
guards pass normally and optimized. Independent review PASS after correcting
the initially wrong q/H..2q/H band. Status `changed-under-evidence`. Next test
the exact frequency-pair diagonal for the fixed prime-log coefficients and
large-prime moduli, preserving long endpoints and q^-1 weights.

### 2026-09-10: frequency spacing alone is overcrowded

Already for d=1, the exact rational subband m/(6H)<h<m/(4H) lies inside the
correct angular band and contains `M^2/(H log M)=N^(1.08+o(1))` distinct
fractions h/m. There are only O(N/H)=N^.9 cells of width 1/(100N), so one
cell has `>>M^2/(N log M)=N^(.18+o(1))` members. Its length-N exponentials
are nearly parallel. The Gram operator pays this cluster multiplicity; under
the actual q^-1=m^-1 weight, cluster and single-frequency scales are
c*R*N/M and N/M, so the relative loss remains R. The .18 crowding exceeds
the desired .10 gain.

At N=120000,H=3,M=990 an exact finite check found 5414 distinct frequencies
and a width-1/N cluster of 10. Four guards pass normally and optimized;
independent review PASS. Status `changed-under-evidence`. This rejects only a
generic spacing/minimum-gap large-sieve proof, not the fixed centered
prime-log inequality. Next test a sourced Vaughan/Heath--Brown expansion in
the p-variable against the dense m,h cluster, retaining the full-minus-low
correction and long endpoints.

### 2026-09-10: pointwise prime estimates cannot pay band energy

Maynard--Pandey--Radziwill arXiv:2608.14777v1 Theorem1.1 bounds a prime
exponential sum by `X^(o(1))*(X/D^.5+X^(19/24))`. For the exact reduced
h/m with m=X^.59, every allowed q<=X^.5 approximation is distinct and rational
separation forces D>=X/m=X^.41. The resulting pointwise exponent is
159/200=.795. Prime powers cost X^(.5+o(1)) and the d=1 low correction X^.41.

Summing its square over X^1.08 active frequencies with weight X^-.59 gives
X^2.08, while the required H^-1 band budget is X^1.49. The miss is X^.59.
Classical Vaughan .8 misses by X^.60. Algebraically any pointwise exponent
s must satisfy s<=1/2 to reach the energy target. Helfgott
arXiv:1501.05438 equations (3.6)--(3.9) confirms that a global Lambda sum can
be decomposed into Type I/II pieces without pretending an individual prime
factors. Five guards pass normally and optimized; independent source review
PASS. Status `changed-under-evidence`. Preserve the .795 component; the next
test must average explicit Vaughan pieces over m,h before absolute values.

### 2026-09-10: covariance source gate and resonant falsifier

The classical multiplicative large sieve has a `Q^2` family cost and loses the
sign of the new `W_m C_m` covariance. Conrey--Iwaniec--Soundararajan's
asymptotic large sieve reaches superficially compatible support exponents, but
its theorems do not include this prime-modulus, shrinking-numerator,
Gauss-phased two-character covariance or the long complementary Mobius tail.
The architecture is retained as a clue; direct applicability is rejected.
Independent source review PASS; the source guard passes normally and optimized.

The actual conjecture is now written without suppressed data in
`resonant_covariance_falsifier.py` (1)--(6): for every epsilon>0, its exact
`mu_>N^(3/20)*log` band energy, including all `d<=2N^.009`, prime
`N^.59<m<=2N^.59`, strict centered angular modes, coprimality masks, hard
intervals, and weight `mu(d)^2(log m)^2/(dm)`, should be
`O_epsilon(N^(1499/1000+epsilon))`.

A fully coefficient-uniform version is exactly false. On one complete prime
residue box, `alpha_a=e_m(h0*a)`, `beta_1=1` puts
`((m-2)^2+R-1)/((m-2)(m-1))` of all energy in the active band and makes
`OFF/E_all=(m-3)(m-1-R)/((m-2)(m-1))`. This tends to one, not `H^-1`. The
finite exact receipt `m=1009,H=5` gives band ratio `63382/63441` and positive
OFF ratio `59354/63441`. This falsifies generic coefficient arguments only;
the fixed shared Mobius--log coefficients remain open. Two guards pass normally
and optimized; independent review PASS. Status `changed-under-evidence`.

Next test the actual prime-modulus sum before absolute values: expand its Gauss
phases and character shifts to see whether it becomes a diagonal plus a signed
Kloosterman/Ramanujan-type remainder. A retained full-energy positive diagonal
is the falsifier. Polynomial identities remain available as components;
overall Goldbach signed correlation remains OPEN.

### 2026-09-10: mean-zero additive form of the actual covariance

For d=1 and every literal hard interval, the tail collapses to the fixed
coefficient `r_V(n)=sum_(a|n,a>V)mu(a)log(n/a)`. If `F_m(x)` is its nonzero
residue sum and `delta_m=F_m-average(F_m)`, the centered projector kills the
average exactly. The open covariance is therefore

`OFF_m=sum_(h in I_m)|delta_hat_m(h)|^2
       -R_m*m/(m-1)sum_x|delta_m(x)|^2`.

No Kloosterman phase or positive full-energy diagonal appears. OFF is precisely
the excess of the actual discrepancy's active Fourier energy above its uniform
share. The raw kernel diagonal has trace zero and pointwise size `O(H^-1)`;
all possible excess is off-diagonal in the mean-zero residue correlations.

A reproducible finite lag decomposition at `N=200000` confirms the previous
`OFF/DIAG=-.041560`, but shows much larger cancellation among raw pieces:
W off-diagonal `-1.90631e10`, centering `+1.90245e10`, first lobe
`+5.59840e10`, second lobe `-7.34683e10`. This only rejects dropping those
pieces at that tested scale. Six new guards and independent review PASS after
scope correction. Status `progress`; the spectral estimate remains OPEN.

Next test endpoint robustness of the apparent negative covariance by scanning
admissible hard windows and allowing each prime modulus its most reinforcing
choice. Uniform sign failure redirects the target to magnitude rather than
negativity; growth of OFF/DIAG is the falsifier. Polynomial and asymptotic
large-sieve components remain available; the Goldbach signed gap stays OPEN.

### 2026-09-10: endpoint freedom defeats a uniform sign mechanism

All 276 admissible N/32-grid windows common to every modulus had negative
aggregate covariance at `N=32000,200000,1200000`. The theorem allows J_m to
depend on m, however. Choosing the most positive grid interval independently
gives `OFF/DIAG=.138274,.116086,.059999` at `H=2,3,4`, with respectively
62/68, 157/171 and 374/444 positive modulus choices. This numerically rejects
uniform aggregate nonpositivity as the mechanism.

It does not reject the needed magnitude estimate: each positive aggregate is
a small fraction of DIAG, individual ratios remain moderate, and the cutoffs
`V=4,6,8` are far from asymptotic. The reproducible probe keeps every fixed
arithmetic coefficient and mask. One guard passes normally/optimized;
independent review reproduced H=2 and H=3. Status `changed-under-evidence`.

Next test a deterministic dyadic reduction for arbitrary J_m. Mean removal is
linear, so the hoped-for cost is only `O(log^2 N)` by block decomposition and
Cauchy. A power-sized modulus-dependent multiplicity or surviving mean term is
the falsifier. Passing this gate would isolate fixed dyadic Mobius bilinear
blocks for a new arithmetic estimate. The signed Goldbach gap remains OPEN.

### 2026-09-10: dyadic endpoint reduction costs only logarithms

Every hard interval splits into at most two aligned dyadic blocks per scale
and at most `K=2ceil(log_2(N+1))` blocks total. Tail formation and d=1 mean
removal are exactly linear. Cauchy contributes one K; the scale/slot selector
families contribute another. Hence a block-selector estimate uniform over all
scales and modulus-dependent locations implies the arbitrary-interval theorem
with only `K^2`, absorbed in epsilon. Four exhaustive guards and independent
review PASS. Status `progress`.

This does not estimate a block or make its location modulus-independent.
Next compute the full Parseval collision budget for common block length Y and
discard every scale already below exponent 1.499. The remaining long-block
threshold will define the next arithmetic input. The signed Goldbach estimate
and d>1 transfer remain OPEN.

### 2026-09-10: Parseval prunes dyadic lengths through N^.7495

For one selected block of length Y, full-frequency Parseval with exact q- and
d-residue collision counts bounds the continued full-minus-low kernel by
`4(Y+q)Y*N^o(1)`. Inserting `mu(d)^2(log m)^2/q` and summing the complete
family gives `E_Y<<N^o(1)(Y^2+BMY)`. Thus lengths `Y=N^y` have exponents
`2y` and `y+.599`; both fit the `1.499` benchmark exactly when
`y<=1499/2000=.7495`. Three guards and independent review PASS. Status
`progress`.

Only longer blocks need new cancellation. Next split `mu_>V*log` by factor
exponent alpha into the below/above-m regimes separated at `.41` and `.59`,
and compute their individual averaged-energy budgets before applying another
large-sieve or bilinear theorem. The signed prime correlation remains OPEN.

### 2026-09-10: the best factor-by-factor Cauchy still retains Y^2

On a surviving block `Y=N^y`, split the Mobius factor at `N^alpha` and choose
the shorter of it and its `N^(1-alpha)` cofactor as the outer variable
`Z=N^s`. Since `s<=.5<y`, each fixed outer value leaves `O(Y/Z)` inner values.
Parseval plus Cauchy gives `Y^2+ZqY` per modulus and
`N^o(1)(Y^2+ZBMY)` after the exact outer family. Its exponent is
`max(2y,y+s+.599)`. The `2y` term exceeds 1.499 for every `y>.7495`, in the
lower, balanced and upper factor regimes alike.

Four guards and independent review PASS after correcting the initially
omitted `+1` for a generic long outer factor; the final proof always chooses
`Z<Y`. Status `changed-under-evidence`. The factor components remain available,
but their signs or joint m,h average must precede Cauchy. Next test a direct
signed adaptation on the balanced `.41<alpha<.59` box, where both factor
supports are below m. The Goldbach signed estimate remains OPEN.

### 2026-09-10: balanced factor covariance matrix

The exact d=1 central tail was split at the literal finite boundaries
`V<a<=floor(N^.41)`, `floor(N^.41)<a<M`, and `a>=M`, where
`M=floor(N^.59)`. The reproducible 3 by 3 covariance probe gives balanced
component `OFF/DIAG=+.006337` at `N=200000,H=3,V=6` and `+.002394` at
`N=1200000,H=4,V=8`, so this component shows no finite resonant concentration.
It cannot be separated from the full tail: component principal diagonals total
`4.63` and `5.43` times the recombined diagonal, and cross OFF changes sign.
The result is finite evidence at tiny V, not an asymptotic estimate or a license
to discard polynomial/factor components. The recombination guard passes normal
and optimized; independent review reproduced both scales and PASSed. Status
`progress`. Next source-gate an exact balanced `(a,b,h)` trilinear estimate;
any full-norm or family term above the `N^1.499` budget falsifies that route.

### 2026-09-10: balanced finite-field trilinear source gate

The d=1 balanced block has an exact dual `(a,b,h)` representation with the
hard product interval inside an arbitrary pair weight. Petridis--Shparlinski
Theorem 1.3 therefore applies legally, but after optimal endpoint localization
its bound is at least `N^.405625` worse than the existing Parseval dual norm.
Even an optimistic use of its separable Theorem 1.1 is at least `N^.265`
worse. The refined `47/52` theorem of Macourt--Petridis--Shkredov--Shparlinski
remains more than `N^.4` worse wherever its two-small-support condition holds.
All use coefficient sup norms and discard the decisive `l2` normalization of
the active-frequency dual vector.

Wright's 2026 nearly-balanced convolution theorem requires the chosen factor
length to exceed the modulus by a fixed power; both current balanced factors
are strictly shorter than `N^.59`, so its range fails. The low-projector rank
term itself is paid with dual exponent `y-.345<=.655`, below `.7495`.
Four exact guards and independent primary-source review PASS. Status
`changed-under-evidence`: these black-box source routes are rejected, while
the exact pair-weight encoding, factors and rank payment are preserved. Next
test prime-exponent rebalancing against every inherited budget and a sourced
beyond-one-half convolution range. The signed Goldbach estimate remains OPEN.

### 2026-09-10: companion-exponent rebalancing gate

With companion exponent `mu`, the exact active-band benchmark is `.909+mu`,
the retained U=1 Type-I exponent is `.318+2mu`, and the margin is `.591-mu`.
Lowering `.59` keeps that component valid. It does not reach the checked
distribution sources in the still-open range: cofactors below `N^.46` force
`mu>.54`, while Wright Theorem 2.2's two modulus inequalities permit some
factor exponent only when `mu<17/33=.51515...`. Balanced factors directly
violate its required factor-longer-than-modulus inequality. Classical BV with
`d<=N^.009` requires the strict condition `mu<.491`.

The Wright/BV ranges are contained in companion ranges already paid by the
actual tail estimates. Six guards pass normal/optimized; independent review
held the first draft for strict BV and longer-factor boundary corrections and
then PASSed them. Status `changed-under-evidence`. This rejects source-range
rebalancing, not the factors or the signed covariance. Next test whether the
full factor vector occupies a stable low-energy covariance eigendirection and
whether any such relation contains information beyond the known convolution
identity. The Goldbach correlation remains OPEN.

### 2026-09-10: factor eigentest reduces to the complementary identity

For the measured three-component principal matrix D and OFF matrix O, the
generalized eigentest `O v=lambda D v` exactly reconstructs the all-factor
ratio from the D-spectral weights of `e=(1,1,1)`. At
`N=32000,200000,1200000`, e has natural-coordinate cosine
`.986820,.993335,.995139` with the smallest-D vector, matching the geometry
expected from `mu_>V*log=Lambda-mu_<=V*log`. That cosine is coordinate-scale
dependent and is only a finite clue.

There is no stable generalized OFF mode: the positive-mode weight of e is
`6.899%,30.438%,.011%` across the three scales, although its direct
OFF/principal ratio remains modestly negative. One guard passes normal and
optimized; independent review reproduced the data and PASSed the exact linear
algebra and convolution sign. Status `changed-under-evidence`. The identity
geometry and factor components remain useful, but no new sign, saving, or
power law was found.

Next test whether the actual Goldbach transfer produces a structured interval
family J_m, allowing the signed m-average to be used before the stronger
arbitrary-selector supremum. Free endpoints or persistence of the known
dense frequency-cluster loss falsifies that route. The fixed Mobius-band
inequality and signed prime correlation remain OPEN.

### 2026-09-10: exact endpoint alignment survives the physical transfer

For a physical cofactor block `A<n<=2A`, expanding `d|n` and setting `n=d*l`,
`q=dm` gives the common progression-index interval
`floor(A/d)+1<=l<=floor(2A/d)`. The conjugated and reflected partner primes are
exactly `q*l+r` and `N-q*l+r`. Their interval endpoints are therefore affine
and residue-aligned modulo q, rather than arbitrary independent selectors in
m. The strong arbitrary-`J_m` inequality remains sufficient if proved, but it
is not forced by the original endpoint geometry.

A finite d=1 test retains the exact Mobius tail, active angular band and outer
prime weights. Every admissible dyadic affine location at N=32000 and N=200000
has negative aggregate covariance for both orientations and `r=-H,0,H`; the
ranges are `-.289474..-.009879` and `-.163491..-.000267`. The default
N=1200000 block gives `-.1569` and `-.1775`. These results reject the earlier
arbitrary-selector positive resonance on this actual-shaped family, but the
near-zero margin and omitted full Schwartz-weighted r-sum give no sign or
power theorem. Two guards normal/optimized and independent direct review PASS.

Curiosity status `aha-candidate`, new-to-this-task. Next derive the full
aligned `(d,m,l,r,h)` form before endpoint maximization and test whether its
r-transform eliminates the long-block collision or dense-frequency loss.
The fixed band inequality and signed prime correlation remain OPEN.

### 2026-09-10: endpoint alignment does not itself remove the collision

On either physical progression `p=q*l+r` or `p=N-q*l+r`, both terms of the
full-minus-low additive kernel are independent of l. This invalidates treating
the aligned object as a generic collection of unrelated length-N frequencies,
but exact Parseval followed by Cauchy across K progression indices still costs
`q*K*sum|c|^2`. Since `Y=qK` and the coefficient square mass is `Y*N^o(1)`,
the old `Y^2` collision survives. It exceeds `N^1.499` for every
`y>.7495`.

Two exact guards normal/optimized and independent review PASS. Status
`changed-under-evidence`: preserve the aligned common-index formulation, but
reject phase collapse alone as the missing H gain. Next expand the actual
progression covariance before Cauchy, separate its paid diagonal, and test the
signed l1!=l2 correlations averaged over prime m. The fixed band inequality
and signed Goldbach correlation remain OPEN.

### 2026-09-10: same-row cancellation and cross-row reinforcement

The aligned d=1 covariance now has an exact finite row decomposition. Its true
point diagonal is negligible at all tested scales. Same-row, distinct-residue
correlations are large and negative, while different-l correlations are almost
equally large and positive. For example at `N=1200000,A=39`, normalized pieces
are `-1.05e-8,-4.886587,+4.729663`, leaving total `-.156924`; at the weak
`N=200000,A=30` block, `-3.729491+3.726097` leaves `-.003395`.

Independent review verified the exact indexing, kernel, centering and
recombination and reproduced a direct two-row case; one guard passes normal
and optimized. Status `changed-under-evidence`. Componentwise off-diagonal
cancellation is false in these measurements, so the signed recombination must
remain intact. Next decompose the reinforcing cross-row term by l-lag and test
whether it is local or oscillatory before the prime-m sum. The fixed band
inequality and signed Goldbach correlation remain OPEN.

### 2026-09-10: positive aligned covariance is not lag-local

The exact d=1 aligned covariance was decomposed by progression-index lag
`Delta=l2-l1`.  Every lag recombines to the previous same-row, cross-row and
total values.  Across `N=32000`, `200000` and `1200000`, between `.21012` and
`.40049` of all positive cross-row mass lies in the last half of the available
lags, with positive mass reaching `Delta=A-2`.  This is finite evidence only,
but it rejects truncating the reinforcing term to a bounded local-lag model at
the tested scales.

Since the underlying integer difference is `q*Delta+(s-r)`, the missing input
would have to control a prime-weighted family of growing shifts while retaining
the signed same-row/cross-row recombination.  One guard passes normally and
optimized.  Independent review checked the exact lag identity, indexing,
centering and normalization and matched a direct Q-matrix sum to rounding.
Status `changed-under-evidence`.
Next test one dyadic lag block and demand an `H^-1` saving from the actual
Mobius--log coefficients; principal-size positive resonance across growing
blocks is the falsifier.  The exact band inequality remains OPEN.

### 2026-09-10: dyadic lag cancellation survives a quantified gate

For each dyadic lag block, define `C_j` as the exact prime-weighted signed
cross-row covariance and `P_j` as `rho_m=|I_m|/(m-1)` times its row-energy
Cauchy baseline.  The concrete sublemma
`max(C_j,0)<=C_epsilon*N^epsilon*P_j` is coefficient-uniformly false under
identical resonant rows, which give ratio about `1/rho_m`, but it remains
plausible for the fixed Mobius--log array.

At `(N,A)=(32000,9),(200000,19),(200000,30),(1200000,39)`, the maximum
positive ratios are `.56517,.33922,.34099,.30564`; no tested dyadic block
exceeds one H^-1 Cauchy budget.  The main block signs agree across all sampled
prime moduli, so prime-m averaging is not producing the observed cancellation.
The gain occurs inside complete dyadic sums over lags.  This is finite evidence
at H=2,3,4, not a uniform estimate.

Three guards normal/optimized and independent review PASS.  Status `progress`.
Next derive the exact l-Fourier representation and locate the joint active-h,
positive-dyadic-multiplier region.  Tensor resonance is the falsifier.  The
same-row and d>1 obligations and the signed Goldbach gap remain OPEN.

### 2026-09-10: exact active-band reduction after l-Fourier diagonalization

Zero-padding the aligned row sequence to any `L>=2A-1` gives the exact identity
`C_j(m)=L^-1 sum_k W_j(k)G_m(k)`, where `W_j` is the dyadic cosine multiplier
and `G_m` is active h-band energy minus its uniform `rho_m` share.  This locates
the possible tensor resonance without claiming spectral equidistribution.

Splitting `C_j=D_j+O_j` into active and outside h modes is sharper.  The
outside coefficient is `-rho_m`, so pairwise Cauchy proves
`max(O_j,0)<=P_j`.  Only the positive signed active-band autocorrelation needs
a new bound: `max(D_j,0)<<N^epsilon P_j`.  Its largest measured ratios are
`.00296848,.01150376,.01022114,.00278596` in the four saved configurations;
nearly all positive total covariance is supplied by the already-paid outside
term.  H=2--4 gives no asymptotic theorem.

Arbitrary-array identities at three padding factors, actual-data guards and
independent review PASS.  Status `aha-candidate`, new-to-this-task.  Next split
`D_j` by dyadic Mobius-divisor ranges and test its factor diagonal before any
absolute values.  A principal-size positive diagonal falsifies that route.
The same-row, d>1 and full signed Goldbach estimates remain OPEN.

### 2026-09-10: factor-diagonal sign fails, near-cutoff band survives

The active dyadic remainder `D_j` was expanded exactly over dyadic Mobius
divisor ranges.  Its factor diagonal changes sign: the lag-1 diagonal/P_j is
`-.07934` at N=32000, `+.07665` at N=200000,A=19, `+.07676` at A=30, and
`+.02874` at N=1200000.  Cross-band terms nearly reverse those values, leaving
the previously measured totals `.00297,.01150,.01022,.00279`.

No positive diagonal is principal-size in these finite runs; the largest sum
of positive band diagonals is `.08415*P_j`.  At N=200000 the near-cutoff band
`V<a<=2V` dominates several signs, making its exact residue progression the
next target.  Independent review and two normal/optimized guards PASS.  A
redundant full matrix run was stopped; even the linear-cost exact N=1200000
case takes about four minutes, so N=200000 is the routine ceiling.  Status
`changed-under-evidence`.

Next test whether geometric cancellation in the near-cutoff progressions,
quantified by `||h*a/m||`, survives the h and prime-m averages.  Resonant
positive density is the falsifier.  Polynomial/log weights remain usable by
partial summation.  The same-row, d>1 and signed Goldbach gaps remain OPEN.

### 2026-09-10: deterministic geometric saving for each near-cutoff divisor

For every `m>a>=H>=2` with `(a,m)=1`, the exact active band satisfies

`sum_h min(ceil(m/a),m/(2|ha|_m))^2 <=96m^2/(aH)`.

Abel summation and the centered term give the rigorous weighted consequence
`sum_h|Phi_(a,m,l)(h)|^2<=800mu(a)^2 log(N)^2m^2/(aH)`.  Thus each individual
near-cutoff divisor progression has the desired geometric cancellation.  The
actual finite prime/divisor averages are only `1.04,2.01,1.89` times the
square-root scale and below `.009` of the pointwise-trivial scale.

Three guards and independent review PASS.  Status `progress`, new-to-this-task.
The unresolved loss is coherent summation across `V<a<=2V`; plain Cauchy loses
that band cardinality.  Next test cross-divisor Gram quasi-orthogonality with
the fixed mu(a) vector.  Growth proportional to V is the falsifier.  The
l-lag, same-row, d>1 and signed Goldbach estimates remain OPEN.

### 2026-09-10: finite cross-divisor Gram quasi-orthogonality

The exact active-band Gram matrix of the near-cutoff divisor progressions was
measured over all prime companions and aligned rows.  For divisor-band sizes
`3,8,15,29`, the fixed Mobius Rayleigh ratios are
`1.000006--1.08804`, while the largest diagonal-normalized arbitrary-coefficient
eigenvalues are `1.00020,1.00101,1.70449,1.57175` in the N=200000 campaign.
The N=32000 three-divisor values are `1.000609,1.140689`.

No measured ratio follows the raw divisor count.  This is useful finite support
for quasi-orthogonality, not an asymptotic theorem, and it currently controls
same-row active energy rather than signed l-lags.  Two guards and independent
review PASS.  Status `progress`.

Next compare the active Gram to rho times the exact full-frequency collision
Gram on the divisor-progression subspace.  A generalized eigenvalue growing
like H or band size falsifies the route.  The l-lag, same-row, d>1 and signed
Goldbach gaps remain OPEN.

### 2026-09-10: restricted active/full matrix inequality survives finite stress

The full-frequency divisor Gram now has an exact Parseval formula through
common multiples of `lcm(a,a')`.  Comparing the active Gram with `rho_m` times
this full Gram gives fixed-Mobius quotients `.489--1.019` and worst generalized
eigenvalues `1.155--1.865` across the saved N=32000/200000 bands of size
3,8,15,29.  Denominator condition numbers are below 3.38.

The exact proposed inequality, including the definitions of `H,M,V,A,U,D_U`,
the active band `I_m`, every prime/row/frequency range, both `rho_m` factors,
the `(log m)^2/m` weight, arbitrary coefficients `c_a`, and the centered
progression `u_(a,m,l)(h)`, is recorded in `divisor_active_full_gram.py` and
`REFRESH_HANDOFF.md`.  Its generalized eigenvector is the finite worst-case
resonant coefficient choice; the Mobius receipt uses `c_a=mu(a)`.

Single-prime stress tests at H=5,10,14,20 and up to 39 divisors give largest
eigenvalues `.042,2.042,2.724,2.653`, with fixed-Mobius quotients
`.009,1.060,1.176,1.410`.  This rejects H-sized and divisor-count-sized
resonance in the tested range, but proves no uniform estimate or trend.

Three guards and independent review PASS.  Status `aha-candidate`,
new-to-this-task.  Next test an explicit Schur/Gershgorin bound for the
normalized active off-diagonal kernel after prime averaging, then transfer it
to shifted row pairs.  Growth like H is the falsifier.  The same-row, d>1 and
signed Goldbach gaps remain OPEN.

### 2026-09-10: pure Gershgorin fails at H=20

Diagonal normalization gives a concrete proof attempt: Schur bounds the
active numerator by its maximum absolute row sum, while Gershgorin bounds the
full denominator below by one minus its maximum absolute off-diagonal row
sum.  It survives all five saved prime-averaged bands with certificates
`1.750--4.058`.

The stronger single-prime stress at `(m,H,U,row_count)=(100003,20,64,4)`
falsifies that denominator step: its off-diagonal row sum is `1.07859`, so the
Gershgorin lower bound is `-.07859`.  This does not falsify the active/full
matrix inequality.  The exact normalized denominator eigenvalue is `.57739`,
the active Schur row sum is `1.95360`, their valid ratio is `3.38353`, and the
actual generalized eigenvalue is `2.65303`.

The surviving question is now sharper: prove or falsify a uniform lower frame
bound for the exact full common-multiple Gram, retaining spectral cancellation
that Gershgorin discards.  The active row-sum upper bound is separately
promising.  Shifted rows, d>1, and the signed Goldbach estimate remain OPEN.
Independent review PASSed the derivation, computation, and scope.

### 2026-09-10: exact gcd feature frame found inside the full denominator

Freezing `log(n/a)` at the left row endpoint gives ideal kernel
`m^2 log(ml/a)log(ml/a')*(gcd(a,a')-1)/(aa')`.  The totient identity expands
this as a positive feature Gram.  On one dyadic band, the `d=a` feature is
unique to coordinate `a`, proving the exact row-wise Loewner lower bound
`P0>=diag(m^2 log(ml/a)^2 phi(a)/a^2)`.

The exact-minus-ideal perturbation is also small in every finite stress.  Its
frame-normalized minimum eigenvalue is positive `.00190--.00888`, its norm is
below `.0305`, and the exact/frame minimum is above `1.002`.  These are finite
certificates; the positivity itself is not claimed uniformly.

Independent review PASS.  Status `aha-candidate`, new-to-this-task.  Next
prove or falsify a normalized Schur perturbation estimate in the near-cutoff
band `U=V`: count discrepancies appear to cost `U^2/m` and log variation
`U/A`, which decay under the selected exponents.  Shifted rows, d>1, and the
signed Goldbach estimate remain OPEN.

### 2026-09-10: near-cutoff full denominator now has a theorem

The exact endpoint and logarithmic perturbation of the positive gcd frame can
be bounded entrywise.  If `F_aa=m^2 log(ml/a)^2 phi(a)/a^2`, an explicit Schur
sum `eta` proves row by row that the exact full-frequency Gram satisfies
`G>=(1-eta)F`.

For `U=V=N^.15`, the proved estimate is
`eta <<_eps U^(2+eps)/m+U^(1+eps)/l
 <<_eps N^(-.29+eps)+N^(-.26+eps)=o(1)`.
Thus `G>=F/2` for every complete near-cutoff row at sufficiently large N,
without using prime averaging.  Exact finite constants over all saved rows
are `.58623,.85083,.89862` at N=32000,200000,1200000.

Independent review PASSed every inequality, asymptotic exponent, receipt, and
test.  This closes the same-row full-frequency denominator lower frame only.
The next obstruction is the active cross-divisor numerator normalized by this
frame; shifted rows, d>1, and signed Goldbach cancellation remain OPEN.

### 2026-09-10: active numerator passes the proven-frame finite gate

The exact active Gram normalized by the totient frame has largest
eigenvalues `1.765,4.211,2.815,4.220,3.348` across the five saved aggregate
bands; absolute Schur bounds are `1.766,4.211,2.817,4.225,4.113`.  Larger-H
single-prime stresses through H=20 and 39 divisors have eigenvalue at most
`6.196` and Schur bound at most `6.252`.

No tested coefficient resonance grows like the divisor count.  Wider bands
do contain individual off-diagonal-heavy rows, so uniform near-diagonality is
not inferred.  Independent review PASSed the exact weights, normalization,
receipts, and scope.  This remains finite evidence.  Next decompose active
off-diagonal entries into equality collisions, unequal differences, and
centering to locate the observed cancellation.  Shifted rows, d>1, and the
signed estimate remain OPEN.

### 2026-09-10: located the near-cutoff active cancellation

The exact active off-diagonal Gram splits into equality collisions,
unequal-integer Dirichlet-kernel terms, and centering.  In the four
single-prime stresses, equality and unequal row sums are `1.5--3.5` each but
their total is only `.007--.071`; their matrix cosines are below `-.99949`.
The prime-averaged N=32000 near-cutoff cosine is `-.999993` and separate
bounds lose a factor `499`.  Centering is around `.001`.

The N=200000 `(48,96]` aggregate is a useful counterexample to universality:
its equality/unequal cosine is only `-.047`, although total off-diagonal mass
is still `1.094`.  Independent review PASSed all formulas, receipts, and
scope.  Next prove the equality component directly through its normalized
gcd kernel; the unequal-difference kernel is then the remaining same-row
piece.  Shifted rows, d>1, and signed Goldbach remain OPEN.

### 2026-09-10: equality-collision component is now proved

The equal-integer part of the active Gram has an explicit frame-normalized
Schur majorant.  Combining `C_lcm<=m/lcm(a,b)+2` with the dyadic gcd row sum
`sum_b gcd(a,b)<=U tau(a)+a` proves

`Eeq <= O_eps(N^eps(1+U^2/m))*rho*F`.

At `U=N^.15,m=N^.59`, the boundary term is
`N^(-.29+eps)`.  The nondecaying divisor contribution is retained as
`N^eps`.  Independent review PASSed every formula, exponent, receipt, and
test.  Equality collisions are no longer the same-row obstruction.  The
unequal-difference active Dirichlet kernel remains OPEN, as do shifted rows,
d>1, and signed Goldbach cancellation.

### 2026-09-10: local-lobe explanation is falsified

An exact cyclic-distance decomposition of the unequal Dirichlet kernel shows
that `d<=H` reinforces equality and `H<d<=2H` gives the main sign reversal,
but the residual after `2H` is still `.506` and `.211` in two tested rows.
Alternating dyadic tails reduce it to `.00524` and `.00817`.

Independent review PASSed the Fourier sign, pair enumeration, bins,
normalization, receipts, and tests.  Cancellation confined to `d<=2H` is
directly contradicted for this tested family.  The preserved route is to keep
the complete Dirichlet kernel and use summation by parts against the CRT pair-
count function.  The unequal-kernel theorem, shifted rows, d>1, and signed
Goldbach remain OPEN.


### 2026-09-10: triangular CRT main isolates the true residual

The frozen signed-difference density has an exact sampled Fejer formula after
writing `m-1=gJ+s`.  Across five single-prime stresses its frame-normalized
Frobenius size is `.00216` down to `.000059` of equality.  The exact raw
residual is `.00524--.03241`, and the exact-minus-main discrepancy carries
essentially all of it.

Independent review PASSed the CRT model, Fejer identity, optimized geometric
formula, weights, receipts, and tests.  This is finite evidence only.  Next
attempt a full bound: apply the one-divisor geometric lemma to the sampled
gcd kernel and the discrete Dirichlet `L1` bound to endpoint/log discrepancy.
The predicted count-error loss is `H U^2 log(m)/m=N^(-.19+o(1))`.  Same-row
active control, shifted rows, d>1, and signed Goldbach remain OPEN.

### 2026-09-10: triangular CRT main is now proved

The sampled triangular kernel is a residue-class Gram.  Splitting
`g=gcd(a,b)` at `H`, the one-divisor geometric lemma handles `g>=H`, while a
no-wrap reciprocal-square tail handles `g<H`.  After rho-frame normalization
and the dyadic gcd row sum this proves

`M_CRT <= O_eps(N^eps(1+H^2/m))*rho F`.

The extra term is `N^(-.39+eps)`.  Independent review PASSed every bound,
normalization, exponent, receipt, and test; standalone APIs were tightened to
reject composite moduli.  The triangular main is closed.  Endpoint/log CRT
discrepancy and centering remain OPEN, along with shifted rows, d>1, and the
signed Goldbach estimate.

## 2026-09-10: CRT pair discrepancy satisfies the active frame bound

Let `S={m*l+1,...,m*l+m-1}`, `R=m-1`, `g=gcd(a,b)`,
`q=lcm(a,b)`, and `L_a=log(m*l/a)`.  If `C_(a,b)(r)` is the exact
log-weighted number of pairs in `S` with difference `r`, divisible by `a`
and `b` respectively, its triangular model is

`C0_(a,b)(r)=1_(g|r)(R-|r|)L_aL_b/q`, `|r|<R`.

CRT and endpoint log variation give the exact uniform error

`|C_(a,b)(r)-C0_(a,b)(r)|
 <=1_(g|r){L_aL_b+(m/q+1)[(L_a+L_b)/l+1/l^2]}`.

For the two-interval active set, the discrete Dirichlet kernel satisfies
`sum_(s mod m)|K_I(s)|<=4m(1+log m)`.  Since each residue has at most two
signed representatives with `|r|<R`, the exact normalized entry majorant for
the raw exact-minus-triangular matrix `D` is

`|D_(a,b)|/[rho*m^2*L_a*L_b*sqrt(phi(a)phi(b))/(ab)]
 <=8(1-rho)m(1+log m)
 {L_aL_b+(m/q+1)[(L_a+L_b)/l+1/l^2]}
 /[rho*m^2*L_a*L_b*sqrt(phi(a)phi(b))/(ab)]`.

Schur and the dyadic gcd/divisor sums therefore prove

`||D||_(rho F)
 <<_eps N^eps{H U^2 log(m)/m+H log(m)/l}`.

At the project exponents `H=N^.1`, `U=N^.15`, `m=N^.59`, `l=N^.41`, the
two terms are `N^(-.19+eps)` and `N^(-.31+eps)`.  Thus the raw CRT
pair-count discrepancy is `o(1)` against the totient frame.  Exact finite
Schur certificates are `66.01,44.75,44.80` over all saved near-cutoff rows at
N=`32000,200000,1200000`; their looseness is harmless to the asymptotic
statement.

Independent review PASSed the signed ranges, CRT count, log error, two-
interval kernel constant, signed-representative factor, frame normalization,
Schur step, exponents, receipts, and normal/optimized tests.  This closes the
raw exact-minus-triangular discrepancy.  The centering correction remains
OPEN, as do shifted rows, `d>1`, and the signed Goldbach correlation.

## 2026-09-10: exact resonant coefficients do not break the active frame scale

`resonant_coefficient_falsifier.py` attacks the active/totient-frame
inequality with the strongest possible complex coefficient vector for each
finite matrix.  If `A` is the exact active Gram and `F` the diagonal totient
frame, it diagonalizes `F^(-1/2) A F^(-1/2)`.  With top unit eigenvector `d`,
the project coefficient convention is `c_a=conj(d_a)/sqrt(F_a)`, so
`sum_a F_a|c_a|^2=1` and its quotient is the exact finite maximum over every
complex `c`.

Two more structured attacks were added.  A single-mode lock uses
`c_a proportional to conj(u_a(h))/F_a`; an equal-frame-magnitude coordinate
ascent chooses every phase adversarially while forcing
`|sqrt(F_a)c_a|=|D_U|^(-1/2)`.  These test both a sharp Fourier peak and
coherent cross-divisor phase alignment.

New single-prime cases `(m,H,l_first,row_count,U)`
`(100003,30,32,2,96)`, `(100003,40,32,1,128)`,
`(100003,50,32,1,160)`, `(100003,80,32,1,256)`, and
`(100003,120,32,1,384)` have exact optimal quotients
`5.83271,5.68998,6.57528,6.37258,8.32580`.  The last case has 236 squarefree
divisors; its ratios to `H` and the divisor count are `.06938` and `.03528`.
Its single-mode, flat-phase, and fixed-Mobius quotients are respectively
`7.90929,4.59297,2.18449`.  The optimal whitened coordinate at `a=390` has
amplitude `.95128`, hence carries `.905` of the coefficient norm.

Thus a constant-one inequality is exactly falsified, but the new campaign
finds no `H`-sized or divisor-count-sized resonance.  The worst vector is
mostly a one-divisor Fourier resonance rather than a coherent divisor-band
amplification.  This is finite evidence only and does not exclude slower
growth or prove the `N^epsilon` estimate.

Independent review PASSed the complex conjugation convention, whitening,
coefficient reconstruction, single-mode maximizer, flat-phase coordinate
updates, deterministic starts, all receipts, and normal/optimized tests.  The
next proof obligation is still the centering correction; shifted rows, `d>1`,
and the signed Goldbach correlation remain OPEN.

## 2026-09-10: same-row near-cutoff active/full inequality is proved

For one complete row write the raw progression transform as `r_a(h)`, its
weight sum as `S_a`, and the centered transform as
`u_a(h)=r_a(h)+S_a/(m-1)`.  If `Q_a=sum_(h in I)r_a(h)`, the centering
matrix is exactly

`C_(a,b)=(1-rho){S_a*conj(Q_b)/(m-1)+S_b*Q_a/(m-1)
                 +|I|S_aS_b/(m-1)^2}`.

The progression contains at most `m/a+1` terms, all on distinct residues
modulo the prime `m`.  With `L_a=log(ml/a)` and `W_a=L_a+1/l`,

`S_a<=(m/a+1)W_a`,
`|Q_a|<=4m(1+log m)W_a`.

After division by the geometric mean of the rho-weighted totient frames and
Schur summation, `active_centering_schur_bound.py` proves

`||C||_(rho F)
 <<_eps N^eps{H U log(m)/m*(1+U/m)+1/m}`.

At `H=N^.1,U=N^.15,m=N^.59` its leading exponent is `-.34+eps`, so the
centering correction is `o(1)`.  The uniform explicit certificates over all
saved near-cutoff rows are `4.76675,2.45576,2.34078` at
N=`32000,200000,1200000`; direct exact centering norms are orders of magnitude
smaller.  The deliberately off-exponent H=120,U=384 stress has a loose bound
`231.90` against exact `.01113`; it does not contradict the project-exponent
theorem.

`near_cutoff_active_frame_theorem.py` now assembles the compatible identity

`A_exact_centered=M_triangular+D_CRT+C_centering`.

The triangular term is `O_eps(N^eps(1+H^2/m))`; the CRT discrepancy is
`O_eps(N^eps[H U^2 log(m)/m+H log(m)/l])`; and the centering bound is above.
Therefore every same complete near-cutoff row satisfies

`A_exact_centered <= O_eps(N^eps) rho F`.

The previously proved full-frequency lower frame gives `G_full>=F/2` for all
sufficiently large N.  Hence

`A_exact_centered <= O_eps(N^eps) rho G_full`,

which proves the exact active/full matrix inequality for the same-row
near-cutoff divisor band.  Positive `(log m)^2/m` weights allow direct
summation over every project prime and row.

Independent review PASSed the centering identity, counts, distinct-residue
argument, kernel bound, normalization, asymptotic exponent, exact comparisons,
and the integration of all three matrices.  Fifteen linked tests pass in
normal and optimized modes with warnings treated as errors.  This is a real
same-row closure.  It does not control shifted row pairs, `d>1`, or the
remaining signed Goldbach prime-correlation estimate.  The next concrete
question is whether the same CRT/Dirichlet representation extends to a fixed
nonzero row shift without losing a factor equal to the number of rows.

## 2026-09-10: shifted triangular CRT main has no lag loss

For rows `m*l+x` and `m*(l+Delta)+y`, put `s=x-y` and
`g=gcd(a,b)`.  The two divisor conditions are CRT-compatible exactly when

`s == m*Delta (mod g)`.

Thus the shifted triangular kernel is

`T_(g,t)(h)=sum_(|s|<m-1,s==t mod g)(m-1-|s|)e_m(-hs)`,
`t=m*Delta mod g`.

If `A_r(h)=sum_(1<=x<m,x==r mod g)e_m(-hx)`, exact pair counting gives

`T_(g,t)(h)=sum_(r mod g)A_r(h)conj(A_(r-t)(h))`.

Cauchy and permutation of the residue classes prove pointwise

`|T_(g,t)(h)|<=sum_r|A_r(h)|^2=T_(g,0)(h)`.

Therefore the complete shifted active sum is dominated by the previously
proved zero-shift sampled Fejer kernel.  Every shifted triangular-density
block has the same frame-normalized Schur bound
`O_eps(N^eps(1+H^2/m))`, uniformly in the row separation `Delta`, with no
lag-count factor.

`shifted_triangular_crt_main_bound.py` verifies the exact cross-correlation
identity, pointwise domination, and inherited active bound.  Four tests pass
normally and optimized.  Independent review PASSed the CRT orientation,
feature identity, Cauchy step, logarithm/frame cancellation, and scope.  This
closes the triangular main for each shifted row pair only.  Summing lags still
needs explicit bookkeeping; shifted CRT discrepancy and centering remain
OPEN, as do `d>1` and the signed Goldbach correlation.

## 2026-09-10: every shifted near-cutoff row pair satisfies the active frame bound

For complete rows `l_L,l_R`, signed within-row separation `s=x-y`, and
`g=gcd(a,b)`, CRT compatibility is

`g | s-m(l_R-l_L)`.

With `L_a=log(m l_L/a)` and `L'_b=log(m l_R/b)`, the exact shifted
pair-count/log discrepancy at each compatible separation is bounded by

`L_a L'_b+(m/lcm(a,b)+1)
 [L'_b/l_L+L_a/l_R+1/(l_L l_R)]`.

The signed-residue multiplicity remains at most two, so the discrete
Dirichlet L1 proof gives the same discrepancy scale as in one row.  The
cross-row centering identity also retains the same bounds with the two
row-specific logs.  Combining those terms with the shifted triangular main,
and normalizing the left and right coordinates by their respective totient
frames, rectangular Schur proves

`||F_L^(-1/2) A_(L,R) F_R^(-1/2)||
 <<_eps N^eps`

for every pair `A<=l_L,l_R<2A` in the near-cutoff band.  The vanishing losses
are still

`N^eps[H U^2 log(m)/m+H log(m)/A
       +H U log(m)/m*(1+U/m)+1/m]`.

`shifted_active_frame_bound.py` implements the exact entry majorants and
compares them with the full cross-row active matrix.  For row separations
`3,7,16,28`, the exact normalized operator norms are
`.04454,2.68364,3.38796,6.16660`; there is no measured lag-count or divisor-
count amplification.  The explicit proof constants are deliberately loose.

Independent review PASSed the asymmetric log errors, CRT condition, signed
multiplicity, centering, two-frame normalization, rectangular Schur step,
SVD comparisons, asymptotic uniformity, and normal/optimized tests.  Combined
with `G_l>=F_l/2`, this gives a pairwise active/full estimate with at most a
factor two.  Summing all pairs in a dyadic lag block remains separate
bookkeeping; cross-factor-band terms, `d>1`, and the signed Goldbach
correlation remain OPEN.

## 2026-09-10: near-cutoff dyadic lag sums lose no row-count factor

For one prime and one squarefree near-cutoff divisor band, let `E_l` be the
exact full-frequency energy in row `l` and

`B_(l,r)=(1-rho)sum_(h in I)Phi_l(h)conj(Phi_r(h))`.

The shifted-pair theorem gives

`|B_(l,r)|<=eta*rho*sqrt(F_l F_r)`.

If the full row frames satisfy `G_l>=kappa F_l`, then

`|B_(l,r)|<=(eta*rho/kappa)sqrt(E_l E_r)`.

For any dyadic lag set `J`, define

`D_J=2 Re sum_(Delta in J,l)B_(l,l+Delta)`,
`P_J=2 rho sum_(Delta in J,l)sqrt(E_l E_(l+Delta))`.

Termwise summation over exactly the same pairs proves

`|D_J|<=(eta/kappa)P_J`.

Thus neither the number of rows nor the number of lags is lost.  At the
project exponents `eta<<_eps N^eps` and eventually `kappa>=1/2`.  Positive
prime weights can sum the same inequality, and the logarithmic number of
dyadic lag blocks is absorbed by `N^eps`.

`near_cutoff_dyadic_lag_bound.py` retains the exact pair enumeration and full
energies.  Small finite receipts have deliberately huge theorem constants but
exact signed ratios between `-.263` and `+.031`.  Independent review PASSed
the factor of rho, lower-frame transfer, factor two, pair ranges, conjugation,
and normal/optimized tests.

This closes the dyadic active-lag bookkeeping for one near-cutoff divisor
band.  It does not combine distinct divisor bands, compare `P_J` with any
other global denominator, handle `d>1`, or prove the signed Goldbach
correlation.  Next test the rectangular active operator between two different
dyadic divisor bands; growth like the square root of their scale ratio is the
falsifier for naive band summation.

## 2026-09-10: rectangular Schur controls cross-bands below N^.245

`cross_divisor_band_probe.py` tests the exact active operator between
squarefree bands `(U,2U]` and `(W,2W]`, with separate rho-weighted totient
frames.  The exact worst complex-coefficient singular values stay between
`2.066` and `4.032` as `W/U` grows from `2` to `16` in the new
m=`10007,30011,100003` cases.  Their ratios to `sqrt(W/U)` fall at the larger
scale ratios; fixed-Mobius quotients are `.0023--.1517`.  This finite evidence
rejects observed square-root scale growth but is not a theorem by itself.

`cross_divisor_band_bound.py` supplies the theorem.  Assume
`H<=U<=W`, both complete-row indices are comparable to `A`, and the project
central ranges make the frozen logs comparable to `log N`.  The triangular
gcd majorant has row sum
`O_eps(N^eps sqrt(W/U))` and column sum
`O_eps(N^eps sqrt(U/W))`; rectangular Schur cancels the scale ratio.  The
remaining normalized operator losses are

`O_eps(N^eps[H U W log(m)/m+H log(m)/A
              +H W log(m)/m+1/m])`.

Thus, for `H=N^.1`, `m=N^.59`, and `A=N^.41`, every pair of divisor bands
with

`H<=U,W<=N^(.245-delta)`

is controlled for each fixed `delta>0`.  The endpoint exponent is strict:
`.1+2(.245)-.59=0`, so `N^.245` itself is not claimed.

Independent review PASSed the exact cross matrix, two frames, SVD and Mobius
quotients, transposition test, truncated column gcd sum, rectangular Schur,
all asymptotic losses, strict exponent, corrected range statement, and six
normal/optimized tests.

This extends the active-frame theorem from the near-cutoff band to every pair
of lower bands below `N^(.245-delta)`.  It does not yet assemble those bands
against the exact full energy: cross-band terms in that denominator can
cancel, so a multi-band lower frame or another coercive comparison remains
OPEN.  Larger factors, `d>1`, and the signed Goldbach correlation also remain
OPEN.  Next test the exact full Gram of the union of lower bands against the
block totient frame; a minimum generalized eigenvalue tending to zero is the
falsifier.

## 2026-09-10: lower divisor bands assemble through a subpower full frame

`multiband_full_frame_probe.py` tests the exact full-frequency Gram `G`, the
frozen positive gcd-feature Gram `P0`, and block totient frame `F` on every
squarefree divisor in `(V,B]`.  As the scale ratio `B/V` grows from `2` to
`64`, the measured ideal minimum eigenvalue falls from `1` to `.099` at
m=1009 and `.092` at m=10007.  The exact minima remain positive (`.0165` and
`.0416` in the widest finite cases).  Thus a constant lower frame is not
supported, but no polynomial collapse is observed.

The mechanism is finite Mobius inversion over multiples.  Put

`x_a=c_a log(ml/a)/a`,
`y_d=sum_(a in D,d|a)x_a`, `D={V<a<=B:mu(a)^2=1}`.

Then

`P0=sum_(d>1)phi(d)|y_d|^2`,
`F=sum_(a in D)phi(a)|x_a|^2`, and
`x_a=sum_(k<=B/a)mu(k)y_(ak)`.

Harmonic-weighted Cauchy proves exactly

`F<=H_(floor(B/(V+1))) C_D P0`,

where

`C_D=max_(1<d<=B) phi(d)^(-1)
 sum_(a in D,a|d,mu(d/a)^2=1)phi(a)d/a`.

Since `C_D<=max_(d<=B)(d/phi(d))tau(d)=N^o(1)`, this yields
`P0>=N^-eps F`.  The exact-minus-frozen union perturbation satisfies

`||G-P0||_F <<_eps N^eps(B^2/m+B/l)`.

For `B<=N^(.245-delta)`, this is power-small relative to the subpower ideal
coercivity, so the exact full Gram obeys `G>=N^-eps F` after epsilon
renaming.

There are only `O(log N)` dyadic bands.  The reviewed cross-band active
operator bounds assemble by Cauchy with one logarithmic factor, which is
absorbed into `N^eps`; the multiband lower frame then transfers the result to
exact full energy.  Consequently the same-row, shifted-row, and dyadic-lag
active/full controls now hold for the complete lower divisor union

`N^.15<a<=N^(.245-delta)`

for each fixed `delta>0`.

Independent review PASSed the multiples-poset inversion, harmonic inequality,
feature coefficient, subpower estimate, union perturbation, epsilon renaming,
eigenvalue probes, six normal/optimized tests, and the band-assembly argument.
Finite explicit perturbation constants are too loose to certify the larger
small-N unions, so no finite positivity is inferred from them; the directly
computed exact eigenvalues are separate evidence.

The remaining divisor range begins at the sharp boundary of this elementary
route.  Its CRT count-error term is `H B^2/m`, which becomes order one at
`B=N^.245`; absolute endpoint errors cannot cross it.  Next isolate the
signed sawtooth in the CRT count discrepancy and test whether averaging it
over divisor pairs or prime moduli gains a power.  Larger factors, `d>1`, and
the final signed Goldbach prime-correlation estimate remain OPEN.

## 2026-09-10 continuation: the missing arithmetic ingredient is now explicit

The CRT endpoint loss has been rewritten as an exact signed
fractional-part difference.  Every fixed compatible divisor pair and
separation has zero total error over a complete `lcm(a,b)` row period.
Finite worst-coefficient tests show substantial cancellation over consecutive
rows and over the joint prime-row average.  They do not supply a theorem.

The full-period identity cannot finish the endpoint by itself.  A checked
example with prime `m=71 == 1 mod lcm(5,7)` retains more than half of the
trivial scale on a suitable eight-row block.  The new bounded hypothesis is
therefore a joint bilinear one: after retaining the endpoint Fourier
coefficients and the complete active kernel, the sum over prime moduli
`M<m<=2M` and rows `A<=ell<2A` should gain a power over the absolute CRT
count bound for `q=lcm(a,b)<=B^2`.  Test it first at and above
`B=N^.245`; falsify it with the exact generalized eigenvector.  Reassess
within 30 minutes.  Polynomial/logarithmic weights, the triangular main,
the centering estimates, and the lower full frame remain available tools.

This is a new-to-this-task mechanism statement, not a signed
prime-correlation estimate or a Goldbach proof.  Independent review PASSed
the exact identity and finite probe after correcting the Fourier helper's
coprimality guard.  Publication of this repository was explicitly authorized
on 2026-09-10; manuscript preparation, outside contacts, spending, and
foreground work remain excluded.

## 2026-09-10 continuation: lower-band control reaches .295-delta

The joint prime-row hypothesis passed.  Exact row-rotation orthogonality plus
Cauchy over the prime subset proves a signed endpoint saving

`N^eps{A^(-1/2)+sqrt(q/(MA))+q^(-1/2)}`.

After bandwise rectangular Schur, the endpoint component is power-small for
all divisor scales `B<N^(49/150)`.  Combining it with the previously checked
components advances the complete lower union from `.245-delta` to
`.295-delta`.  Independent review PASSed after two scope corrections recorded
in `REFRESH_HANDOFF.md`.

The active endpoint is no longer the immediate barrier.  The exact full Gram
was compared to its frozen positive gcd feature with an absolute perturbation
`N^eps(B^2/M+B/A)`, which becomes order one at `B=N^.295`.  The next bounded
question is whether that signed exact-minus-frozen perturbation cancels after
the joint prime-row sum.  Test the minimum generalized eigenvalue for unions
crossing `.295`, and derive the exact signed perturbation before proposing a
uniform bound.  A polynomially collapsing minimum eigenvalue is the falsifier.
Reassess within 30 minutes.  The signed prime-correlation estimate remains
open and must not be inferred from this divisor-frame extension.

## 2026-09-10 continuation: aggregate frame gain does not yet transfer to all lags

The signed joint rotation also improves the aggregate exact full-frame error:
it is power-small through `B<N^(109/300)`.  Finite generalized eigenvalues
show the expected row-average improvement.  This result passed independent
review after narrowing an invalid integration claim.

The complete active/full and dyadic-lag result remains at `.295-delta`.
For a lag `Delta`, only `A-Delta` base rows remain, and aggregate coercivity
does not imply the termwise geometric-energy lower bounds in the current lag
budget.  The next bounded hypothesis is a weighted all-lag lower-frame
inequality for a common divisor coefficient vector.  Test whether aggregate
full energy can coexist with polynomial collapse of the sum of lag-pair
geometric means; such a coefficient vector falsifies the transfer.  Reassess
within 30 minutes.  Do not report the separate `49/150` active endpoint and
`109/300` aggregate-frame thresholds as an assembled range.

## 2026-09-10 continuation: first all-lag falsifier did not collapse

A finite weighted all-lag probe tested aggregate and rowwise minimum
generalized eigenvectors, coordinates, Mobius coefficients, and seeded real
and complex random vectors.  Across lower unions ending at `64,128,256`, the
minimum lag quotient stayed essentially equal to the aggregate full-frame
minimum; no separate lag-energy collapse was measured.  Independent review
PASSed the probe and its deliberately finite scope.

This does not prove the weighted transfer.  The next 30-minute hypothesis is
that direct nonlinear minimization of the lag quotient, seeded by coherent
combinations of row-minimum modes, still cannot beat the aggregate minimum by
a polynomial factor.  A reproducible ratio that decays materially faster
with divisor-range growth falsifies it.  Keep the complete assembled exponent
at `.295` until a uniform all-lag lower bound is actually proved.

## 2026-09-10 continuation: nonlinear lag minimization changes direction

Projected complex-gradient descent and coherent combinations of row-minimum
modes did not materially lower the finite all-lag quotient.  The only new
minimum was `.16688794` versus `.16690301` before refinement on the wider
tested union.  Independent review verified the optimizer and preserved its
nonexhaustive scope.

The next 30-minute hypothesis is that a uniform second-moment bound for
normalized row-energy deviations can replace the unavailable termwise lower
frame.  Mechanism: small variance makes low-energy rows sparse, and a dyadic
lag graph loses only the edges incident to that sparse set.  Prediction: the
worst resonant vectors have bounded or decreasing variance relative to their
mean as primes and rows are added.  Falsifier: healthy aggregate energy paired
with order-one or polynomially growing normalized variance.  No assembled
exponent beyond `.295` is claimed.

## 2026-09-10 continuation: finite variance falsifier remains favorable

The exact frame-weighted row-ratio variance was added to the nonlinear
all-lag probe.  On the current `8<a<=64` and `8<a<=128` worst vectors, the
relative variances were `2.78e-4` and `6.61e-4`; no tested frame mass lay below
half the mean.  Independent review reproduced the measurements and verified
that the weighted mean is exactly the candidate aggregate quotient.

This is finite evidence, not the needed uniform second-moment theorem.  The
next bounded task is to prove the deterministic weighted lag-graph lemma that
states precisely how a row-ratio variance controls the loss of geometric-mean
edges, including boundary degrees and varying frame energies.  Only after that
lemma is checked should the arithmetic variance estimate be attempted.  The
all-lag transfer, any assembled exponent beyond `.295`, and the signed prime
correlation remain open.

## 2026-09-10 continuation: deterministic graph step closes

For arbitrary weighted lag graphs, a proved inequality now bounds the edge
average of `sqrt(r_u r_v)` below by the vertex mean minus an explicit
boundary-degree factor times the weighted standard deviation.  Substituting
the exact Goldbach frame weights makes its left side precisely the all-lag
quotient.  Independent review verified the proof, implementation, and nine
normal/optimized tests.

The finite certificates retain most of the aggregate lower frame even on the
long boundary-heavy lag block.  This does not prove uniform small variance.
The next bounded experiment maximizes relative row-ratio variance across the
full adversarial coefficient family; checking only the lag minimizer is too
narrow.  Order-one or divisor-range-growing variance is the falsifier.  If it
does not occur, formulate the exact arithmetic second-moment operator bound.
The assembled exponent remains `.295`, and the signed prime correlation is
open.

## 2026-09-10 continuation: uniform variance is too strong

A fixed two-prime, 16-row sweep found the maximum sampled relative row-ratio
variance rising from `.00031` at divisor cutoff 32 to `.11907` at 256 and
`.16231` at 320.  Independent review reproduced the results.  The high
variance vectors retained lag quotients `.34424` and `.38914`, while the
actual tested lag minima were `.13732` and `.13220`; the two threats did not
coincide.

The deterministic variance-to-graph lemma remains proved, but requiring tiny
variance for every coefficient vector is abandoned.  Preserve the possible
low-energy-cone version.  The next 30-minute hypothesis is that the scalar
geometric means can be minorized directly by matrix geometric means, turning
the whole lag numerator into one positive quadratic operator whose generalized
eigenvalue can be tested against the arithmetic-mean frame denominator.  A
zero or rapidly collapsing eigenvalue falsifies that route.  No assembled
range beyond `.295` is claimed.

## 2026-09-10 continuation: direct matrix-geometric lag certificate

The nonlinear lag numerator has an exact quadratic minorant: sum the
Kubo--Ando geometric means of each pair of exact row Grams.  Scalar AM--GM
simultaneously turns the frame denominator into a quadratic upper bound.  The
resulting minimum generalized eigenvalue is a valid lower certificate for all
coefficient vectors in each finite instance.  Independent review verified
the inequality directions and implementation.

For the fixed two-prime, 16-row experiment, the long-lag certificate stays
positive from divisor cutoff 32 through 320, decreasing from `.38324` to
`.12531`.  This is much stronger than sampled optimization but remains finite
floating-point evidence.  The next bounded test must scale modulus, row range,
and divisor cutoff together at the project exponents.  The target theorem is
subpower coercivity of the summed matrix-geometric operator through
`beta<49/150`; polynomial eigenvalue decay falsifies it.  The assembled range
remains `.295`, and the signed prime correlation is open.

## 2026-09-10 continuation: ideal all-lag frame closes

At project-like simultaneous scaling, exact matrix-geometric lag certificates
remain between `.334` and `.153` from `M=251` through `16001`.  Direct
exact-versus-frozen-ideal lag comparisons approach ratio one: `1.0038` at
`M=1009` and `1.00037` at `M=16001`.  Independent review reproduced the
receipts and kept them finite in scope.

The frozen ideal lag frame is now a theorem.  Rowwise multiband inversion,
monotonicity of the matrix geometric mean, and the uniform central-row log
comparison prove its summed operator is `N^-epsilon` coercive on every
nonempty dyadic lag block, without a boundary loss.  The next concrete
question is whether the exact summed matrix-geometric operator differs from
the frozen ideal by `o(N^-epsilon)` through `beta<49/150`.  A polynomially
negative normalized eigenvalue of that difference, or a project-scaled exact
certificate falling polynomially below the ideal one, falsifies the transfer.
No assembled range beyond `.295` is claimed; the signed prime correlation is
still open.

## 2026-09-10 continuation: direct exact-to-ideal falsifier is favorable

The full normalized spectrum of the exact-minus-ideal matrix-geometric lag
operator was measured under project scaling.  From `M=1009` to `16001`, its
negative edge shrank from `-.00463` to `-.000743`, while its norm shrank from
`.04296` to `.00502`.  Weyl retained `.15201` of an ideal minimum `.15275` at
the largest test.  Independent review verified the spectrum and inequality
direction.

This rules out a hidden bad eigendirection in the tested cases only.  The next
30-minute proof hypothesis is that the nonlinear exact-to-ideal perturbation
obeys a power-small joint prime-row estimate comparable to the already-proved
aggregate full-Gram perturbation.  Test the Fréchet/variational structure of
the matrix geometric mean before claiming that cancellation transfers through
it; a dependence on an unavailable rowwise condition number falsifies that
proof route.  The complete range remains `.295`, and the signed prime
correlation is open.

## 2026-09-10 continuation: nonlinear curvature is a real term

A stable central linearization split the exact matrix-geometric perturbation
into its first variation and nonlinear remainder.  The remainder is negative
as joint concavity predicts, and its negative norm is comparable to the
harmful total perturbation from `M=1009` through `8009`.  Independent review
verified the calculation.

Therefore first-order prime-row cancellation alone is insufficient.  The
curvature route would need a new quantitative lower-conditioning estimate.
The next bounded hypothesis is stronger and cleaner: the exact individual-row
full Grams may themselves satisfy the subpower multiband lower frame through
the active endpoint range, despite failure of the earlier absolute
perturbation proof.  First measure the minimum rowwise generalized eigenvalue
under project scaling and attack its exact centered-divisibility factorization.
Polynomial rowwise collapse is the falsifier.  The assembled exponent remains
`.295`, and the signed prime correlation is open.

## 2026-09-10 continuation: exact Mobius lcm identity, truncated L1 obstruction

Every tested exact single-row Gram at project scaling retained 98%--99% of
the ideal multiband minimum through `M=16001`.  A rowwise theorem specialized
to the actual Mobius vector would be enough for the scalar lag denominator.
Independent review verified both statements and their limits.

For the actual Mobius-log coefficients, the complete squarefree divisor cube
over a fixed lcm collapses exactly to
`mu(q)[log(X)^2-sum_(p|q)log(p)^2]`.  The actual truncated interval destroys
most of that cancellation: over `B=32` through `2048`, more than 90% and
eventually 99.8% of grouped L1 mass comes from incomplete `q>B`, and the total
remains on the finite `B^2` scale.

The identity is retained, but the L1 proof route is rejected.  The next
30-minute hypothesis is that the signed high-lcm coefficients cancel against
the exact CRT count discrepancies across `q` for the actual Mobius vector.
Measure the rowwise signed-to-absolute ratio at project scaling before seeking
a bilinear estimate.  A ratio bounded away from zero across scales falsifies
this route.  The assembled exponent remains `.295`; the signed prime
correlation remains open.

## 2026-09-10 continuation: signed lcm cancellation survives truncation

Although grouped L1 mass remains on the `B^2` scale, its actual correlation
with the strict CRT count error cancels increasingly under project scaling.
From `M=1009` to `16001`, the worst rowwise signed/absolute ratio falls from
`.1680` to `.0377`, its median from `.0290` to `.00949`, and the worst frozen
count perturbation/frame ratio from `.0203` to `.00434`.  Independent review
verified the exact count, normalization, receipts, and repaired empty-range
guard.

This is finite evidence for a signed-q mechanism, not a theorem.  The next
30-minute question uses the exact factorization `a=gr,b=gs`, which turns the
coefficient into `mu(r)mu(s)` and the sawtooth modulus into `grs`.  Compare
this structured trilinear cancellation with randomized signs; if Mobius is no
better than the random baseline or a resonant sign family keeps a constant
ratio, do not attribute the effect to the complete-cube identity.  The
assembled exponent remains `.295`, and the signed prime correlation is open.


## 2026-09-10 continuation: reciprocal sawtooth, not the fixed bias

The incomplete high-lcm cancellation was compared with 256 seeded independent
Rademacher signs on the squarefree divisors. Depending on the project-scaled
row, between `.0820` and `.7148` of random trials had a signed/absolute ratio
at most the Mobius ratio. Mobius therefore has no consistent finite advantage
over this random-sign baseline. Independent review verified the construction
after correcting the even-sample median. This rejects a uniquely complete-cube
explanation, not every deterministic use of Mobius structure.

The exact change of variables `a=gr,b=gs`, with `g=gcd(a,b)`, is now executable
and independently checked. It is a bijection from ordered squarefree pairs to
pairwise-coprime squarefree triples satisfying `V<gr,gs<=B`, and it turns the
coefficient sign into `mu(r)mu(s)` with modulus `grs`. This preserves a real
bilinear arithmetic ingredient after the random-sign comparison.

A separate decomposition tests whether the good frozen count error was only
created by the deterministic `-1/q` correction. It was not: from `M=1009`
through `16001`, maximum cyclic-sawtooth/frame ratios decreased from `.01934`
to `.00438`, while the reciprocal-bias maximum decreased from `.001006` to
`.0000408`. The cyclic component closely tracks the full frozen error at every
tested scale. Independent review verified the fractional-part identity, sign,
normalization, and full row sweeps. These are finite measurements and prove no
asymptotic cancellation.

The next <=30-minute question is whether a Fourier expansion of
`{X/(grs)}-{(X+m-1)/(grs)}` exposes a bilinear reciprocal-phase estimate in
`r,s` that survives the pairwise-coprime constraints and hard ranges
`V<gr,gs<=B`. Any candidate must be compared with the exact sum and rejected
if a dyadic/frequency block retains constant normalized size or endpoint loss
exceeds the frame. The assembled exponent remains `.295`; the signed prime
correlation and Goldbach remain open.


## 2026-09-10 continuation: a fixed-Mobius variance route emerges

The reciprocal trilinear mass is genuinely two-variable in the finite tests:
with `min(r,s)>=ceil(sqrt(B))`, the long-bilinear region carries between 67%
and 89% of cyclic tuple-level L1 mass over all sampled project rows. This is
before equal-lcm grouping and proves no cancellation, but it rules out axis
concentration as the finite explanation.

More significantly, the complete exact fixed-Mobius row ratio was measured,
including varying logarithms and the centering term omitted by the frozen CRT
probe. With the exact active-frame vertex weights, eight evenly spaced primes
in `[M,2M]`, all project rows, and `beta=.32`, the scaled variances
`M*Var(R)` were

`.06154,.03191,.05334,.03748,.03398,.02714,.02283`

for `M=251,503,1009,2003,4001,8009,16001`. The signed CRT collision term
accounts for most of the variance; the log/centering residual is smaller.
Applying the already-proved weighted graph lemma to the long lag block gives
finite lower certificates `.98490,.82294,.64772` at
`M=1009,4001,16001`, compared with actual quotients
`1.01307,.83486,.65264`. Independent review verified the full scalar formula,
its matrix match, weights, edge set, receipts, and tests.

This revives the earlier variance tool only for the fixed Mobius coefficients;
the failed uniform-all-coefficients variance hypothesis remains rejected. A
sufficient new arithmetic target is a frame-weighted lower mean together with

`sum alpha_(m,l)(R_(m,l)-Rbar)^2
 <= M^(-1+epsilon) sum alpha_(m,l)`

uniformly through `beta<49/150`. The observed `1/M` scale is finite evidence,
not a theorem, and only eight sampled primes were used at each scale. The next
bounded task is an exact Fourier/row-rotation expansion of this second moment,
retaining the `mu(r)mu(s)` structure. Standard large-sieve `Q^2` loss is the
first falsifier. The assembled exponent remains `.295`; the signed prime
correlation and Goldbach remain open.


## 2026-09-10 continuation: diagonal energy closed, cross-modulus covariance open

The cyclic-sawtooth diagonal now has a rigorous bound. With
`K_q=sum_(lcm(a,b)=q)mu(a)mu(b)L_aL_b` and complete row-period variance
`v_(m,q)=theta(1-theta)`, `theta=((m-1) mod q)/q`, commit `331fc5d` proves

`sum_q K_q^2 v_(m,q)
 <= m R_max sum_(a,b) L_a^2L_b^2/lcm(a,b)`,

`R_max<=max_q 3^omega(q)`, together with the exact conversion

`sum_(a,b) L_a^2L_b^2/lcm(a,b)
 = sum_(d<=B) phi(d)[sum_(d|a)L_a^2/a]^2`.

Independent review verified every step and the executable checks. This gives
the correct subpower diagonal scale after the existing frame lower estimate.
It does not bound cross-`q` covariance over an incomplete row interval or the
prime sample.

Finite data show the actual collision mean square at 48%-82% of the diagonal,
while most diagonal mass in the largest sampled row lies between `sqrt(N)`
and `m`. Thus the cross terms reduce the answer in the samples, but the usual
additive large-sieve `Q^2` loss is too costly in the dominant range. An
unweighted `B^2/sqrt(V)` conjecture was also discarded because isolated
prime-pair lcms obstruct it asymptotically; the sawtooth variance factor is
the ingredient that makes the proved diagonal bound possible.

The next concrete target is a specialized cross-modulus Bessel estimate for
the actual Mobius lcm coefficients: cross covariance at most `N^epsilon`
times diagonal through `B<=N^(49/150-delta)`. It is falsified if a resonant
dyadic pair of `q` blocks has a covariance/diagonal ratio growing by any fixed
positive power. The fixed-Mobius all-row second moment, signed prime
correlation, and Goldbach remain open; the assembled exponent is still
`.295-delta`.


## 2026-09-10 continuation: shared factors are the cross-term mechanism

The complete-period cross covariance is now exact. If
`s_q=(m-1) mod q`, `g=gcd(q,r)`, and `n_t(q)` counts the final `s_q` residues
in class `t mod g`, then

`Cov_m(q,r)
 = [g sum_(t mod g)n_t(q)n_t(r)-s_q s_r]/(qr)`

and

`|Cov_m(q,r)| <= gcd(q,r)^2/(4qr)`.

Consequently coprime lcm moduli have zero complete-period covariance. The
linked conditions can cancel or reinforce only through shared prime factors;
the sign is the alignment of their terminal residue-class errors. Independent
review verified the CRT formula, bound, frozen-coefficient energy split,
optimized implementation, and tests.

For the actual frozen Mobius coefficient vector, sampled complete-period
total/diagonal ratios decreased from `.5638` to `.3277` across four small
`(m,B)` choices, so the shared-factor off-diagonal was negative there. This
does not establish its sign or asymptotic size.

The incomplete row interval and row-varying logs remain outside the lemma.
The next concrete test isolates their boundary covariance and averages it over
the project primes. Any fixed positive-power growth relative to the proved
diagonal rejects the route. The fixed-Mobius second moment, signed prime
correlation, and Goldbach remain open; complete assembly stays
`.295-delta`.


## 2026-09-10 continuation: the incomplete boundary stays small in the next test

The remaining finite effects now have an exact decomposition. Each grouped
lcm coefficient is a quadratic `K_q(L)=A_qL^2+B_qL+C_q` in
`L=log(m*l)`. After freezing it at the midpoint row, the boundary excess is

`B_m=A^(-1)sum_(A<=l<2A)|sum_q K_q d_(m,q)(l)|^2
     -sum_(q,r)K_qK_r Cov_m(q,r)`.

The verifier also computes the exact signed difference after restoring the
row-varying quadratic coefficients. Independent review confirmed the
polynomial identity, both energy differences, project scaling, prime sampler,
normalization, and tests.

Over eight evenly spaced primes, the maximum `|B_m|/D_m`, with
`D_m=sum_q K_q^2v_(m,q)`, decreased from `.12105` at `M=1009` to
`.03037` at `M=4001`. The maximum varying-log difference/diagonal decreased
from `.01964` to `.005770`; every frozen incomplete total/diagonal ratio was
below `.672`. These measurements support a subpower boundary but prove no
asymptotic estimate.

Exact dense cross-covariance evaluation is quadratic in the number of lcm
values. The `M=8009` eight-prime sweep exceeded the useful interactive
runtime, and no result from it is retained. The next target is a sparse
divisor/GCD-sum factorization proving both the complete-period kernel and the
absolute prime-averaged boundary are at most `N^epsilon` times the diagonal.
A normalized operator norm growing as `N^c` for fixed `c>0` falsifies the
route. The signed prime correlation and Goldbach remain open; complete
assembly remains `.295-delta`.


## 2026-09-10 continuation: sparse absolute covariance has no finite power loss

The absolute complete-period covariance now has the exact sparse factorization

`(1/4)sum_(q,r)|K_qK_r|gcd(q,r)^2/(qr)
 = (1/4)sum_d J_2(d)[sum_(d|q)|K_q|/q]^2`.

It follows from the proved pair covariance bound and dominates the full signed
complete-period quadratic form. The divisor form removes the dense `q,r`
runtime bottleneck; original lcm coefficient construction is still quadratic
in the divisor count.

Across eight project primes at each of seven scales from `M=251` through
`16001`, the median majorant/actual-diagonal ratio stayed between `2.897` and
`3.560`, and every maximum stayed between `3.385` and `3.632`. The sign-free
majorant therefore shows no finite positive-power growth. Independent review
verified the identity, domination, scale sweep, implementation, and tests.

The missing proof is a weighted GCD-operator estimate relative to
`sum_q |K_q|^2v_(m,q)`, not merely an unweighted GCD-sum theorem. Very small
`v_(m,q)` may permit resonant vectors. The next falsifier computes that
generalized eigenvalue and compares its extremizer with the actual Mobius
coefficient direction. Polynomial eigenvalue growth closes the absolute route
but leaves signed cancellation available. The incomplete boundary, signed
prime correlation, and Goldbach remain open; complete assembly remains
`.295-delta`.


## 2026-09-10 continuation: resonant coefficients do not match Mobius

The coarse gcd majorant cannot be promoted to a uniform weighted theorem.
Whenever an lcm support coordinate satisfies `q|(m-1)`, its true variance and
all true covariances are zero, but the coarse majorant retains diagonal
weight `1/4`. This is an exact counterexample to the proposed uniform coarse
operator comparison.

The correct test deletes those null coordinates and diagonalizes

`R_(q,r)=|Cov_m(q,r)|/sqrt(v_(m,q)v_(m,r))`.

Its largest eigenvalues at six scales through `M=8009` were
`2.479,3.064,3.063,3.323,4.639,4.372`, with no observed power growth. The
actual Mobius absolute Rayleigh ratios stayed in `[1.842,2.332]`, and its
signed ratios decreased overall from `.727` to `.471`. At the largest two
scales the squared overlap between the absolute Mobius vector and the worst
resonant vector was only `.0272,.0336`. Independent review verified the exact
falsifier, operator normalization, computations, and tests.

The sparse majorant remains a valid actual-vector bound and the exact operator
remains a possible subpower object. The next task seeks a shared-factor
frequency factorization of the exact normalized kernel and tests its Schur or
spectral growth. The incomplete boundary, signed prime correlation, and
Goldbach remain open; complete assembly remains `.295-delta`.


## 2026-09-10 continuation: complete-period covariance becomes positive squares

The cross-modulus mechanism now has a one-variable exact form. For
`g=gcd(q,r)` and `s_g=(m-1) mod g`,

`Cov_m(q,r)=s_g(g-s_g)/(qr)=g^2v_(m,g)/(qr)`.

The covariance kernel is nonnegative; coefficient signs alone decide whether
cross terms cancel or reinforce. Its divisor Mobius transform is the positive
primitive Fourier energy

`H_m(d)=sum_((k,d)=1)|sum_(0<=x<m-1)e_d(kx)|^2`.

Hence

`sum_(q,r)x_qx_rCov_m(q,r)
 =sum_d H_m(d)[sum_(d|q)x_q/q]^2`

is an exact positive sum-of-squares factorization. Independent review verified
the residue identity, Parseval/conductor grouping, inversion, code, and tests.

For the actual Mobius coefficients, median signed energy/diagonal decreased
from `.734` to `.472` over seven scales through `M=16001`; the corresponding
termwise-absolute ratio only rose from `1.867` to `2.339`. The ratio between
them rose from `2.54` to `4.97`, exposing increasing cancellation inside the
structured sums `S_d=sum_(d|q)K_q/q`.

The next target is an exact original-divisor expansion and dyadic energy test
for `S_d`. A fixed-power dyadic concentration falsifies the factorized route.
The incomplete boundary, signed prime correlation, and Goldbach remain open;
complete assembly remains `.295-delta`.


## 2026-09-10 continuation: dominant primitive energy has a short residual lcm

The structured coordinate in the positive factorization now has the exact
original-divisor expansion

`S_d=sum_(k|d)mu(k) sum_e phi(e)
 [sum_(a in D,e|a,(a,k)=1)mu(a)log(X/a)/a]^2`.

This follows from inclusion-exclusion for `d|lcm(a,b)` and the gcd/totient
identity. Independent review verified the formula, implementation, dyadic
partition, edge guards, and tests.

At seven central scales through `M=16001`, the energy fraction from `d<=B`
fell to `.0218`; roughly 98% is on `d>B`. The largest block tracks `d` near
the prime scale and consistently carries about 28%-38% of the energy. This
rules out a small-conductor proof but creates a complementary opportunity:
for `d=d_Ld_Rd_C` assigned across the two divisors, the remaining modulus is
at most `B^2/d`, which is only `N^.05` near the dominant `d=N^.59` scale.

The next target is to verify and bound that three-way assignment expansion.
The incomplete boundary, signed prime correlation, and Goldbach remain open;
complete assembly remains `.295-delta`.


## 2026-09-10 continuation: exact short-residual Bessel reduction

The proposed three-way assignment has now been verified exactly. For
`d=d_Ld_Rd_C`, with primes assigned to left-only, right-only, or common,

`a=d_Ld_C alpha`, `b=d_Rd_C beta`,
`lcm(a,b)=d lcm(alpha,beta)`,

and the remaining lcm satisfies
`lcm(alpha,beta)<=B^2/(d d_C)<=B^2/d`. Substitution gives an exact signed
formula for `S_d` with the original hard ranges and the correct Mobius sign
`mu(d_Ld_R)mu(alpha)mu(beta)`.

Writing the supported lcm as `q=dr` gives the exact target

`sum_d H_m(d)[sum_r K_(dr)/(dr)]^2
 <= N^epsilon sum_d H_m(d)sum_r K_(dr)^2/(d^2r^2)`.

At `M=16001`, singleton residual coordinates contribute `.5974` of the full
numerator and equal their diagonal exactly. The multi-residual quotient is
`.26675`; conductors whose maximum residual is at most `64` account for
`.9369` of the full complete energy. These are finite measurements.
Independent review verified the exact identities, support diagnostics,
implementation, and stated theorem boundary.

Universal nonpositive Mobius cross terms cannot prove the inequality: the
exact case `m=31, ell=11, 13<a<=21` has total/diagonal `1.4358389461`.
The next bounded test is the multi-residual quotient on dyadic conductor
blocks at project scales. Fixed-power growth rejects the route; stable
subpower behavior identifies the precise signed residual sum requiring a
theorem. The incomplete boundary, signed prime correlation, and Goldbach
remain open; complete assembly remains `.295-delta`.


## 2026-09-10 continuation: cancellation persists inside conductor blocks

The multi-residual quotient has now been localized exactly to dyadic
conductor blocks. Across eight project primes per scale, the median global
high-`d` quotient decreases from `.49399` at `M=251` to `.25668` at
`M=16001`. The block containing the largest share of the high-`d` diagonal
has median quotient only `.172`-`.225` across all seven scales and carries
median diagonal fraction `.31287` at the largest scale.

At the two largest sampled scales, every high-`d` dyadic block has quotient
below one: maxima `.95327` at `M=8009` and `.87258` at `M=16001`. Smaller
scales do have blocks above one, so this is finite evidence for strengthening
local cancellation, not a pointwise sign rule or an asymptotic bound.
Independent review verified the partitions, measurements, code, and tests.

The next target splits the three-way assignment by common-prime content and
left/right imbalance to identify which arithmetic feature predicts the
signed residual cancellation. A feature class with fixed-power quotient
growth or no signed/absolute separation falsifies that proposed mechanism.
The incomplete boundary, signed prime correlation, and Goldbach remain open;
complete assembly remains `.295-delta`.


## 2026-09-10 continuation: isolate alternating common-part cancellation

The dominant residual blocks now have an exact two-class decomposition by
whether `d_C=gcd(d,gcd(a,b))` equals one. At `M=16001`, the median separate
and common class quotients are `.35337` and `.89806`, so common-prime terms do
not cancel more strongly in isolation. Their collapsed correlation is
`-.88213`, however, and cross-class interference reduces the within-class
quotient `.41975` to the actual `.17292`.

The sign source is explicit:
`mu(a)mu(b)=mu(d)mu(d_C)mu(alpha)mu(beta)`. Removing only `mu(d_C)` raises the
dominant-block median quotient to `.51663`, `2.986` times the actual value;
the increase occurs for all eight largest-scale samples. This is finite
causal evidence for alternating common-part ownership, not an asymptotic
bound. Independent review verified the identities, intervention, data, code,
and tests.

The next target is a weighted almost-orthogonality estimate for the exact
common-part divisor transform
`S_d=mu(d)d^(-1)sum_(c|d)mu(c)A_(d,c)`. A power-growing layer Gram eigenvalue
or actual-vector alignment falsifies this route. The incomplete boundary,
signed prime correlation, and Goldbach remain open; complete assembly remains
`.295-delta`.


## 2026-09-10 continuation: reduce to a six-layer generalized operator

Factoring the common-part sign exactly gives
`y_(d,r)=sum_(c|d)mu(c)A_c(d,r)`. On each dominant high-conductor block, the
collapsed and residual-diagonal norms of arbitrary common-layer combinations
form two positive semidefinite Gram matrices.

At `M=16001`, across eight primes, their largest generalized eigenvalue is
only `1.01972`-`1.03045`. The actual Mobius layer quotient is
`.16676`-`.17980`, and its squared diagonal-metric overlap with the worst
mode is `.000810`-`.004075`. Only six common-part layers are active. The
largest eigenvalue over all 56 saved project samples is `1.10393`.

Independent review verified the exact layer factorization, generalized
operator, numerical rank treatment, Rayleigh quotient, overlap, code, and
tests. These finite matrices do not prove a uniform estimate. The next target
is the analytic Loewner inequality `G_col<=N^epsilon G_diag`; a growing
eigenvalue, rank failure, or increasing actual extremizer alignment rejects
this reduced route. The incomplete boundary, signed prime correlation, and
Goldbach remain open; complete assembly remains `.295-delta`.


## 2026-09-10 continuation: absolute common layers remain constant-scale

Replacing each aggregated `A_c(d,r)` by its absolute value raises the
largest-scale median common-layer eigenvalue from `1.02474` to `2.17966`.
This shows that layer-entry signs provide about a factor-two improvement,
while the observed support geometry alone still avoids the available
`N^.05` Cauchy loss.

New eight-prime sweeps at `M=32003` and `64007` give signed worst-eigenvalue
medians `1.02898,1.03814`, absolute medians `2.23308,2.27972`, and actual
Mobius quotients `.16088,.16916`. The active layer count stays six and the
actual worst-mode overlap falls to `.000155` at the largest scale.
Independent review verified the construction, data, code, and tests. These
remain finite measurements.

The next target tests a Schur bound arising from the nested supports
`r<=B^2/(dc)` by measuring individual layer quotients and normalized
cross-layer row sums. Growth comparable to the raw residual count falsifies
that support-geometric route. The incomplete boundary, signed prime
correlation, and Goldbach remain open; complete assembly remains
`.295-delta`.


## 2026-09-10 continuation: prove the singleton common-layer tail

For a dominant conductor block `d>=D`, common part `c=d_C`, and residual
`r=lcm(alpha,beta)`, the hard ranges prove
`r<=B^2/(dc)<=B^2/(Dc)`. Therefore every layer with
`c>B^2/(2D)` has `r=1` and equals its own diagonal exactly.

At `M=64007`, this leaves only `c=1,2,3` interactive; `c=5,6,7` are the
proved singleton tail. The `c=1` layer alone carries median `.89995` of the
separated diagonal. Its signed quotient is `.33394`, versus `1.89497` after
removing aggregated residual signs.

A simple layer-diagonal Schur/coercivity argument gives the valid but loose
median upper bound `7.64511`, while the true generalized eigenvalue is
`1.03814`. Independent review verified the exact tail theorem, numerical
receipts, code, and tests.

The next target is an exact convolution formula for the dominant `c=1`
layer over assignments `d_Ld_R=d`, with the established polynomial and
gcd/totient tools retained. The incomplete boundary, signed prime
correlation, and Goldbach remain open; complete assembly remains
`.295-delta`.


## 2026-09-10 continuation: Walsh-factor the dominant no-common layer

The `c=1` layer now has the exact assignment convolution

`T_(d,1)=mu(d)d^(-1)sum_e phi(e)sum_(u|d)F_(u,e)F_(d/u,e)`.

Walsh inversion on the Boolean divisor group writes the inner convolution as
even-character spectral squares minus odd-character squares. Discarding that
parity sign gives the proved positive majorant

`|T_(d,1)|<=d^(-1)sum_e phi(e)sum_(u|d)F_(u,e)^2`.

On the complete dominant blocks at `M=16001,32003,64007`, this majorant's
energy is `2.30319,2.73485,2.91017` times the exact `c=1` diagonal. The
actual signed ratios are `.35677,.32652,.33426`. Thus a tool built entirely
from the retained polynomial and divisibility sums has replaced the signed
left/right convolution at a finite constant-looking cost.

Independent review verified the assignment formula, Walsh identity,
majorant, full-block measurements, code, and tests. The next target is a
subpower bound for the square of this positive `e,u` sum against the `c=1`
residual diagonal. The incomplete boundary, signed prime correlation, and
Goldbach remain open; complete assembly remains `.295-delta`.


## 2026-09-10 continuation: reduce the Walsh majorant dyadically in `e`

Writing the exact positive Walsh majorant as `M_d=sum_e m_(d,e)` and grouping
`e` dyadically gives the rigorous pointwise Cauchy reduction

`M_d^2 <= J sum_j M_(d,j)^2`, with `J<=1+floor(log_2 B)`.

At `M=16001,32003,64007`, the resulting sums of block-square energies divided
by the exact `c=1` diagonal are `.91159,1.02198,1.05333`; the full Cauchy
bounds are `7.29270,9.19778,9.48001`. Small `e` dominates: `e<=64` carries
between `.906` and `.940` of the exact majorant-energy attribution.

The strongest possible first-block lemma is false without project scaling.
An exact 8,588-case scan found `(m,ell,V,B)=(131,2,8,17)`, where the dominant
block has two coordinates and the `e=1` block-square/diagonal ratio is
`32.9683041217`. This blocks unchanged attempts to prove the universal
constant-one inequality. It does not contradict the exact Walsh identity,
the positive majorant, the dyadic reduction, or the narrower project-scaled
possibility; central project rows have measured the `e=1` ratio below one.

The next target is a scaled per-block estimate that uses the hard relation
among `m,ell,V,B,D`, allowing a subpower factor. A fixed-power increase or a
sparse resonance persisting along that family rejects it. The incomplete
boundary, signed prime correlation, and Goldbach remain open; complete
assembly remains `.295-delta`.


## 2026-09-10 continuation: retain only complementary assignments

The exact `u<->d/u` link gives the proved refinement

`|T_(d,1)|<=P_d<=M_d`,

where

`P_d=d^(-1)sum_e phi(e)sum_(u|d)|F_(u,e)F_(d/u,e)|`

and `M_d` is the Walsh-square majorant. `P_d` removes all assignment mass whose
complement cannot meet the second linked condition.

At `M=16001,32003,64007,128021`, the full central dominant-block energy of
`P_d` numerically equals the actual signed `c=1` energy, with ratios to the
residual diagonal `.35677,.32652,.33426,.33174`; the Walsh ratios rise through
`3.35289`. Universal paired-sign coherence is false in small ranges, so this
equality remains project-scale evidence rather than a theorem.

The `M=128021` run also raises the `e=1` ratio to `1.01024`, falsifying its
constant-one project conjecture. The surviving candidate is the stratified
estimate `E_(1,k)<=C 2^k Delta_(1,k)` for `k=omega(d)`. Every measured class
ratio divided by `2^k` is below `.082` in the eight-prime samples through
`M=64007`, and the new `k=4,5` values are `.0783,.0592`. Because
`2^omega(d)=d^o(1)`, proving this would give the needed subpower loss.

The next target is an analytic comparison using the complement involution and
the central divisor window, with a project-scaled resonant family as the
falsifier. The incomplete boundary, signed prime correlation, and Goldbach
remain open; complete assembly remains `.295-delta`.


## 2026-09-10 continuation: prove a polylog bound for the dominant `c=1` layer

The Boolean Walsh norm cannot be controlled for arbitrary coefficients even
after paying `2^omega(d)`: the exact resonance `F_1=1,F_d=epsilon` makes the
normalized ratio tend to infinity. The fixed hard-range coefficients instead
admit a direct base-pair argument.

For every squarefree `d>B*V`, any occurring no-common pair
`a=u alpha,b=(d/u)beta` forces both `u` and `d/u` into `(V,B]`. The `r=1`
base pair is therefore present. A residual `r` has at most `3^omega(r)`
left/right/both assignments and its logarithmic products are no larger than
the base product. Hence

`|A_(d,r)|<=3^omega(r)A_(d,1)`.

Together with `r<=B^2/d`, this proves

`|sum_r K_(d,r)|^2
 <=(1+log(B^2/d))^6 sum_r |K_(d,r)|^2`.

This is a genuine polylogarithmic, hence `N^epsilon`, theorem for every
reported conductor satisfying `d>B*V`; it closes the dominant `c=1` residual
collapse analytically. It does not control interference among common layers
or the other conductor ranges.

The complete residual cube also has the exact value
`L_uL_(d/u)-sum_(p|r)log(p)^2`, and its residual sum reduces to coprime
reciprocal Mobius sums plus a two-log correction. These identities remain
available for sharper constants and boundary analysis, but the polylog proof
needs only the three-state count and the hard base support.

Independent review verified every range implication, factor, residual limit,
harmonic exponent, implementation, and focused normal/optimized tests. The
next target is extending the base-pair domination through the interacting
`c>1` common layers and comparing their separated diagonal with the actual
combined residual diagonal. The incomplete boundary, signed prime
correlation, and Goldbach remain open; complete assembly remains
`.295-delta`.

### 2026-09-10 continuation: fixed common layers are individually polylogarithmic

For every squarefree conductor `d`, fixed `c|d`, and retained decomposition
`a=d_L*c*alpha`, `b=d_R*c*beta` with `d=d_L*d_R*c`, `a,b in (V,B]`, `X>B`,
and `d*c>B*V`, the corresponding base pair is also retained. Therefore

`|A_(d,c,r)|<=3^omega(r)A_(d,c,1)`, `r<=B^2/(d*c)`,

and the collapsed-to-diagonal quotient inside that fixed common layer is at
most `(1+log(B^2/(d*c)))^6`. Independent review returned PASS. The theorem
does not control cancellation when distinct `c` layers occupy the same
residual coordinate.

The tested bridge was the high-conductor pointwise base inequality

`sum_c A_(d,c,1)^2 <= 4^omega(d)
 |sum_c mu(c)A_(d,c,1)|^2`, `d>B*V`.

It is REFUTED inside its stated range. At `M=16001`, `V=11`, `B=190`, and
`d=2310>B*V`, the inequality fails by factor `4.53569094`. At `M=128021`,
`d=15015`, it fails by factor `21.24873`; the raw ratio is `21758.70168`.
Both witnesses lie below the selected dominant dyadic block, which explains
why the first narrow sweep missed them.

A weaker theorem survives: splitting every prime of `c` left or right injects
`2^omega(c)` copies of each fixed-common base assignment into no-common base
assignments with no smaller log weight. Thus

`2^omega(c)A_(d,c,1)<=A_(d,1,1)` and
`sum_c A_(d,c,1)^2<=(5/4)^omega(d)A_(d,1,1)^2`.

This controls separated base energy but cannot stop the actual Mobius-signed
base sum from approaching zero. The next approach must average that
cancellation over conductors or absorb it before diagonalization. The
residual lift, signed prime correlation, and Goldbach remain open.

### 2026-09-11 continuation: close the complete-period `d>B*V` component

The common-layer coercivity gap can be bypassed. Let `P_(d,c,r)` be the
termwise-positive majorant of the signed fixed-cell coefficient. The common
cells partition the `R_q` ordered pairs of lcm `q=d*r`, so cellwise Cauchy and
the exact positive-weight identity

`sum_(d|q)H_m(d)=F_m(q)=q^2v_(m,q)`

prove

`sum_(d>B*V)H_m(d)sum_(r,c)P_(d,c,r)^2/(d*r)^2
 <=sum_q R_qv_(m,q)
       sum_(lcm(a,b)=q)L_a^2L_b^2`.

The right side is the established diagonal Cauchy envelope. For `d>B*V`,
the fixed-common log-six theorem applies to every `c|d`; Cauchy over common
parts costs at most `2^omega(d)`, and `r<B/V`. Hence the actual
complete-period high-conductor energy is bounded by the same diagonal
envelope times

`max_(d<=B^2)2^omega(d)(1+log ceil(B/V))^6=N^o(1)`.

Independent review returned PASS. This closes the complete-period `d>B*V`
component through the existing frame bound without lower-bounding the signed
combined common layer. The transition range `B<d<=B*V`, incomplete-row
covariance, signed prime correlation, and Goldbach remain open. The next
question splits the transition range at `d*c>B*V` and isolates the remaining
small-common-part core.

### 2026-09-11 continuation: close every complete-period conductor

The transition analysis first isolated the only base-support failure: under
`B>V^2` and `B<d<=B*V`, an assignment can have exactly one conductor base at
most `V`, but cannot have two. This one-sided component is order one in the
sampled transition energy, so no asymptotic smallness is claimed.

A global weighted-Cauchy argument makes base support unnecessary. The exact
rectangle identity

`sum_(alpha<=A,beta<=C)1/lcm(alpha,beta)
 =sum_e phi(e)/e^2 H_floor(A/e)H_floor(C/e)
 <=H_A H_C H_min(A,C)`

costs at most `H_B^3` per three-way assignment. Combining this with
`H_m(d)<=m*d` and `sum_(d|q)3^omega(d)=4^omega(q)` proves

`sum_d H_m(d)|S_d|^2
 <=m H_B^3 max_(q<=B^2)4^omega(q)
   sum_(a,b)L_a^2L_b^2/lcm(a,b)`.

Every extra factor is subpower, and the last quantity is the established
totient-frame pair mass. Independent review returned PASS. Thus all
complete-period conductors are controlled; the transition split remains a
useful structural diagnostic but is no longer a gap in that component.

The unresolved target is the incomplete prime-row covariance. The next
bounded hypothesis is that its boundary correction admits a factorization
whose operator norm is subpower after the actual arithmetic row spacing is
used. No signed prime-correlation estimate or Goldbach proof is claimed.

### 2026-09-11 continuation: isolate the exact incomplete-frequency operator

For frozen coefficients, the incomplete row has the exact reduced-frequency
form

`sum_q K_q d_(m,q)(l)=sum_(d>1)S_d Z_d(l)`,

with `S_d=sum_(d|q)K_q/q` and
`Z_d=sum_((k,d)=1)G_(m,d,k)e(k*m*l/d)`. Complete Parseval gives the already
controlled energy `sum_d H_m(d)S_d^2`; every incomplete boundary term is an
interaction between distinct reduced Farey frequencies.

The sharp incomplete/complete ratios for arbitrary conductor vectors reach
`9.777` by `M=16001`, while the actual Mobius vectors stay between `.660`
and `1.032` on the seven central tests and have tiny overlap with the worst
resonance. A near-Farey-pair explanation failed on the first exact test: pairs
within `1/A` contributed only `.0805` of complete energy, versus `.2302` from
the remaining boundary pairs.

The surviving mechanism uses the polynomial weights rather than discarding
them. Since every `S_d(log X)` is quadratic, frozen coefficient vectors lie
in one rank-three arithmetic span. Its sharp ratios remain between `1.064`
and `1.419` on the same scale range. Independent review returned PASS on the
identity, operator normalization, resonant-vector test, and structured-span
calculation.

The next bounded target is a subpower bound for this explicit rank-three
family over every project row, followed by prime averaging and Abel transfer
for the varying logarithms. The arbitrary-vector contraction route is
rejected; an arbitrary-vector subpower theorem is neither proved nor
falsified. The signed prime-correlation estimate and Goldbach remain open.

### 2026-09-11 continuation: absorb the varying logs exactly

The actual curve `(t^2,t,1)` is much less resonant than arbitrary vectors in
the quadratic span. More significantly, allowing `t=log(m*l)` to vary with
the row still gives one explicit `3 x 3` generalized eigenvalue problem. For

`P_(d,l)(lambda)=sum_(j=0)^2 lambda_j
 (log(m*l))^(2-j)S_d^(j)`, seek

`A^(-1)sum_l |sum_d P_(d,l)(lambda)Z_d(l)|^2
 <=N^epsilon A^(-1)sum_l sum_d H_m(d)|P_(d,l)(lambda)|^2`

uniformly over `lambda in R^3` and the project ranges. The actual weights are
`lambda=(1,1,1)`. Independent review returned PASS on this exact reduction.

The sharp varying-family maxima over every prime in `[M,2M]` are
`1.665,1.733,1.604` at `M=251,503,1009`; actual-weight maxima are
`1.502,1.594,1.361`. The central `M=16001` values are `1.139` and `1.036`.
No asymptotic inference is made. A power-growing full-block generalized
eigenvalue is the concrete falsifier. The signed prime-correlation estimate
and Goldbach remain open.

### 2026-09-11 continuation: the resonance moves with the prime

The actual outer sum uses one common polynomial family, so the worst
coefficient vector cannot depend freely on `m`. Exact full-prime-block Gram
aggregation confirms that this matters. At `M=251,503,1009`, per-prime sharp
ratios as large as `1.665,1.733,1.604` fall to aggregate ratios
`1.0419,1.0195,1.0324`. Four positive weight choices, including the two
`rho_m` active-frequency weights, change these values only within the ranges
`1.0411--1.0440`, `1.0193--1.0195`, and `1.0307--1.0338`. Independent review
returned PASS; these are finite weighted results only.

The geometric numerator turns every boundary entry into four terms of the
form `e(m*l*theta)` with rational `theta`, summed jointly over prime `m` and
row `l`. This is the concrete candidate mechanism: prime multiplication moves
the resonant Farey clusters while the polynomial coefficient directions stay
common. The next proof target is a subpower weighted prime-row bilinear bound
for the resulting three aggregate matrix entries. A power-growing aggregate
generalized eigenvalue falsifies it. The signed prime-correlation estimate and
Goldbach remain open.

The complete prime-block falsifier now also passes at `M=2003`: among 249
primes the per-prime sharp maximum is `1.480723`, while prime aggregation
gives sharp ratio `1.016111` and actual ratio `.980678`. All four positive
weightings keep the sharp ratio below `1.01703`. The cached shared polynomial
support and these values passed independent review. This remains finite
evidence; the rational-phase bilinear estimate is still the next theorem
target.

### 2026-09-11 continuation: reject the maximum-Q joint bound

The actual conductor support contains primitive frequency pairs whose reduced
difference denominator is of order `B^4`. Four retained primes above `B/2`
give coprime conductors `d,e asymp B^2`, with nonzero structured quadratic
coefficients `2/d,2/e`, and the difference `1/d-1/e` has denominator `d*e`.

Therefore inserting the worst difference modulus into the existing joint
prime-row factor costs

`sqrt(B^4/(M*A))=N^(2*beta-1/2)`.

This route stops strictly at `beta=1/4` and loses `N^.14` at `beta=.32`.
The exact witness and exponent budget passed independent review. This does
not reject weighted or signed averaging over difference moduli. That narrower
arithmetic distribution is now the next falsifiable question; the aggregate
matrix measurements remain promising finite evidence only.

### 2026-09-11 continuation: positive conductor sparsity fails finitely

With `E_d=H_m(d)|S_d|^2`, the ordered product-energy fraction on conductor
pairs with `lcm(d,e)>MA` rises from `.10838` at `M=251` to `.51043` at
`M=16001` for the actual vector; each of the three polynomial basis vectors
is at least as concentrated there. Independent review returned PASS. Because
the reduced frequency-difference denominator only divides `lcm(d,e)`, this
rules out conductor-pair sparsity alone, not frequency-level reduction or
signed cancellation. The next bounded test measures the actual reduced-
denominator distribution before choosing between those mechanisms.

### 2026-09-11 continuation: positive reduced-Q sparsity fails finitely

Weighting every primitive `k/d` by its exact energy
`|S_d|^2|G_(m,d,k)|^2` and reducing `k/d-h/e`, the fraction with `Q>MA` is
`.0973180,.1421667,.2089,.34115` at `M=251,503,1009,4001`. The first two are
exact enumerations; the latter two are deterministic weighted samples with
standard errors below `.00091`. Independent review returned PASS. Reduction
lowers the corresponding conductor-lcm fractions but leaves an increasing,
order-one finite mass. This rejects only positive denominator sparsity on the
tested scales. The next bounded experiment bins the actual signed incomplete-
row pair sum by `Q` and compares every bin with its absolute envelope.

### 2026-09-11 continuation: locate strong within-prime signed cancellation

The exact frozen-log decomposition answers that experiment at three primes.
For `m=251,373,499`, the `Q>mA` signed contributions are only
`-.02642,.00403,.02433` times complete energy, although their termwise-
absolute envelopes are `4.584,3.563,2.921`. The resulting net/envelope ratios
are all below `.0084`, and direct row averaging reconstructs every bin.
Independent review returned PASS. This is finite within-prime cancellation;
it neither proves a bound nor separates conductor signs from rational-phase
oscillation. The next bounded test replaces `S_d` by `|S_d|` to distinguish
those two mechanisms before attempting the outer prime average.

### 2026-09-11 continuation: phase geometry survives sign removal

Replacing `S_d` by `|S_d|` preserves every magnitude and absolute envelope,
yet the high-`Q` net/envelope ratios remain below `.0100` at all three tested
primes. Independent review returned PASS. With the actual magnitudes fixed,
the rational phases and interval kernel are therefore sufficient for this
finite high-`Q` cancellation. The whole boundary changes materially, so the
conductor signs still matter elsewhere. The next bounded test separates
cancellation within each exact `Q` from cancellation across different `Q`.

### 2026-09-11 continuation: exact-Q packet target

That separation finds substantial cancellation at both layers. For the actual
weights at `m=251,373,499`, summing within each exact `Q>mA` leaves
`.0687,.0716,.1100` of the pairwise envelope; summing the resulting `Q`
packets leaves another `.0839,.0158,.0757`. Independent review returned PASS.
The intermediate sums `sum_Q|C_Q|` are only `.315,.255,.321` times complete
energy, so cross-`Q` cancellation would not be needed if this persists
uniformly. The new concrete target is
`sum_(Q>mA)|C_Q| <= N^epsilon sum_d H_m(d)|S_d|^2`; a power-growing quotient
falsifies it. Derive the exact reduced-residue convolution for `C_Q` and test
the next project scale before attempting prime aggregation.

At the next project fixture `m=503`, the reviewed exact packet quotient is
`.595735`, up from `.255--.321` in the smaller common-`B` fixtures but still
below the falsification threshold `1`. Within-`Q` cancellation leaves `.06457`
of the pair envelope and across-`Q` cancellation leaves `.09126` of that
residual. This is one finite result, not evidence of boundedness. Next locate
whether the increase is concentrated in a few exact `Q` packets.

The increase is broad in the finite data. At `m=503`, 181 high-`Q` packets
have effective count `71.04`; the largest carries only `.0482`, the top 20
carry `.4091`, and 108 are needed for 90% of `sum_Q|C_Q|`. Independent review
returned PASS. Short exceptional-packet removal is therefore not the measured
mechanism. Next test the exact `Q`-weighted Cauchy majorant and, if it remains
comparable, target a weighted square-sum bound for the whole packet family.

The reviewed weighted Cauchy bound remains within a factor `1.79` of the exact
packet sum, but reaches `1.06524` times complete energy at `m=503`. It therefore
provides no constant-below-one closure. The route survives only as the explicit
square-sum obligation `sum Q|C_Q|^2`, whose required `N^epsilon` estimate is
open.

### 2026-09-11 curiosity continuation: centered residue spectrum

The exact identity `C_Q=sum_(r,Q)=1 D_Q(r)K_A(r/Q)` was verified on the five
largest `m=251` packets. The constant-residue projection reduces to a short
Ramanujan-sum average but contributes below `.0035` of every packet; centered
residue L2 fractions exceed `.9998`. Uniform rank-one CRT factorization also
fails on this family, though a few prime splits are anisotropic. Independent
review PASSed the corrected verifier. Block unchanged constant-mean and
uniform-rank-one retries; preserve the exact residue identity and split
anisotropy.

The final curiosity status is `new-to-this-task` `aha-candidate`. The transform
test gives the exact compression `C_Q=A^-1 sum_(active ell)T_Q(ell)` and full-
period Parseval. Active/full L2 ratios lie in `[.8798,1.4669]` for the five
leading `m=251` and ten leading `m=503` packets, with independent review PASS.
This finite prediction survived its next-scale falsifier. The candidate route
is a window-equidistribution bound for `T_Q`, followed by a global bound for
`sum_Q Q sum_r|D_Q(r)|^2`. Neither estimate is proved.

### 2026-09-11 continuation: row means require aggregate cancellation

Across all 44 high-`Q` packets at `m=251`, active-window/full-period weighted
L2 is `.99503`, but Jensen leaves `5829.26 E^2` against the actual weighted
packet square `117.80 E^2`. The missing row-mean factor is `.020208`, close to
`1/A`; its `A`-scaled aggregate is `.92959`. Individual selected `m=503`
packets instead cost as much as `20.42`, and their biased top-ten aggregate is
`6.3319`. Independent review PASSed the receipts and corrected the scope:
these finite values reject constant-one/small-constant per-packet cancellation,
not an unspecified `O(1)` or `N^epsilon` bound. The live target is now an
aggregate large-sieve inequality over rows and exact `Q`; all-packet `m=503`
remains unmeasured.

### 2026-09-11 curiosity continuation: broad row-lag cancellation

The all-packet selection test changes the evidence materially. For
`m=251,373,499` in the common `(A,L,B)=(46,46,20)` regime and the project
fixture `(m,A,L,B)=(503,75,75,29)`, the exact quotients

`A sum_Q Q|C_Q|^2 / sum_Q Q mean_(ell in I)|T_Q(ell)|^2`

are `.929586,.872182,3.075815,1.203135`. In particular, the full 181-packet
`m=503` value is far below the biased top-ten value `6.33188`. Independent
review reproduced the full residue-energy receipts and returned PASS. This is
finite support for aggregate square-root-scale row cancellation, not a
constant-one, uniform `O(1)`, or `N^epsilon` theorem.

A concrete curiosity hypothesis asked whether the `m=499` excess came from a
few short row lags. With `v_ell=(sqrt(Q)T_Q(ell))_Q`, the exact identity

`||sum_ell v_ell||^2/sum_ell||v_ell||^2=1+sum_(h=1)^(A-1)rho_h`

was implemented and checked to errors below `1.4e-14`. Before measurement,
"few" meant at least 60% of absolute lag mass in the five largest lags and
"short" meant at least 60% in the first five. Both predictions fail at every
saved full fixture: largest-five shares `.378,.415,.428,.337`; first-five
shares `.159,.293,.292,.250`. The sparse/short-lag explanation is
`directly-contradicted`, while the exact lag decomposition is preserved as a
component. The live mechanism must control a broad signed row Gram sum across
exact denominators, plausibly through a coefficient-sensitive large sieve or
operator estimate. Its concrete target is the aggregate inequality displayed
in `REFRESH_HANDOFF.md`; a power-growing all-packet quotient falsifies it.
The signed prime-correlation estimate and Goldbach remain OPEN.

### 2026-09-11 curiosity continuation: recurring exceptional row directions

Against 16,384 deterministic sign probes of each actual row Gram matrix, the
constant direction is ordinary at m=251,373 and the project m=503 fixture,
but the m=499 quotient 3.07581 exceeds every probe. A fixed-geometry
neighbor scan falsifies the idea that this is isolated: m=509 gives
2.62084, at empirical percentile .99951, while eight other neighboring
primes lie in .902--1.624. These probes preserve the measured Gram matrix
and diagnose exceptional alignment; they do not model arithmetic independence
or prove a bound.

The exceptions localize sharply by exact denominator: five packets carry
.9262 and .9858 of positive excess at m=499,509. The leaders are
Q=62985 and 67830. A new exact conductor-pair split shows coherent
reinforcement among (221,285),(195,323),(247,255) for the former
(.9820 coherence, .5339 largest share). For the latter, coherence is
.9855 but (210,323) carries .9538; hence a universal multi-channel
mechanism is rejected. Preserve exact-Q localization and the channel
decomposition. Next falsify a small-near-resonant-frequency explanation inside
the exceptional (210,323) channel before attempting a cyclic Ramanujan
correlation estimate. The signed Goldbach correlation remains OPEN.

### 2026-09-11 curiosity continuation: an explicit endpoint resonance

Inside the dominant (m,Q)=(509,67830) packet, only .04340 of ordered
primitive-frequency pairs satisfy min(r,Q-r)<=Q/A, yet they supply .98810
of the signed (210,323) channel. Endpoint modes k,h in {+1,-1} alone supply
.98414. The exact rotated fractions satisfy

121/210 - 186/323 = 23/67830,

equivalently 4*210*323-509*(210+323)=23. Their phase separation across
A=46 rows is therefore tiny. The material m=499 channels also pass the
predeclared 60% endpoint test: (221,285) gives .62765 with residual 554,
and (195,323) gives .95169 with residual 887. Their full near-main-lobe
signed fractions are .96401 and 1.10365.

This identifies a new-to-this-task finite mechanism: endpoint-amplified
geometric coefficients reinforce when their modulus-rotated conductor
fractions obey a small integer residual. The exact-Q, conductor-channel,
near-resonance, and endpoint components are preserved. What remains unproved
is the arithmetic statement needed for Goldbach: that all such resonances,
with their actual coefficients and outer prime signs, have a sufficiently
small aggregate. Next test a coefficient-weighted endpoint score on the fixed
prime scan; score/rank failure falsifies endpoint sufficiency.

### 2026-09-11 continuation: endpoint score isolates spikes, not baseline

Define the normalized coefficient-weighted endpoint score by exact-Q grouping:

R_end =
A sum_Q Q|C_Q(k,h in {+1,-1}, min(r,Q-r)<=Q/A)|^2
/ sum_Q Q mean_I|T_Q|^2.

On the ten-prime fixed-geometry scan, its two leaders are (509,499), exactly
the set of the two full-quotient leaders (499,509). Their endpoint scores are
2.04118 and 1.73924. This supports endpoint resonance as an exceptional-spike
detector. It does not reconstruct all ordinary values: Pearson correlation is
.8210, Spearman rank correlation is .6000, and m=457 has score .15717
against full quotient 1.49983. Strong endpoint sufficiency or rank equivalence
is directly contradicted; preserve the score for the exceptional lane and
retain non-endpoint modes for the baseline.

For coprime d,e the near endpoint condition is exactly

|m(sigma*e-tau*d)-n*d*e| <= d*e/A.

Together with
|G_(m,d,+/-1)|=|sin(pi*(m-1)/d)|/sin(pi/d), this identifies the next
proof component: an energy-normalized weighted count or large-sieve estimate
for these short linear residuals over conductors and outer primes. No such
uniform estimate is yet proved; the signed Goldbach correlation remains OPEN.

### 2026-09-11 continuation: weighted endpoint incidences stay near 1/A

Complete project prime-block counts at M=251,503,1009,2003 give
A-scaled endpoint near-pair densities

1.96011,2.17108,2.05762,2.02055.

After weighting by |c_i c_j|, the values are
2.43539,2.82140,2.48488,2.42314. With the proof-relevant
Q|c_i c_j|^2 weight they are
2.89246,3.61695,2.81935,2.88377. All pass the predeclared aggregate
threshold 4. Individual primes can exceed 4, so only prime-block averaging is
supported. This strengthens the earlier joint-prime rotation evidence with a
specific count for the newly isolated endpoint spikes; it does not repeat or
replace the existing full operator scans.

Writing d=g d', e=g e', endpoint reduction gives exactly

Q=lcm(d,e)/gcd(g,sigma e'-tau d').

Maximum measured near-packet ordered multiplicities 12,12,24,24 reject only
literal invariance or a cap of 12, not an unspecified uniform O(1) bound. The
endpoint proof obligation is now a weighted O(N^epsilon/A) prime-block
incidence estimate, a representation bound from this formula, and a comparison
of the resulting total endpoint pair-square envelope with the active-window
denominator under the correct prime weights. Incidence plus multiplicity alone
controls the near packet sum only relative to that envelope. Non-endpoint
modes, the full signed prime-row estimate, and Goldbach remain OPEN.

### 2026-09-11 continuation: assembled endpoint bound stays finite

The missing envelope normalization was measured on the ten-prime fixed
geometry: the total high-Q endpoint pair-square envelope divided by the
active-window denominator lies in [.23300,.30345]. At the larger project
m=503 fixture it is .23214. Combining actual near terms by exact Q and
applying the exact multiplicity-weighted Cauchy bound gives normalized values
in [.25907,5.15290] on the ten-prime family and 1.27488 at project m=503.
The resonant m=499,509 bounds are 3.25768,3.53222.

This finite test passes the stated finite assembled-Cauchy threshold 10 and
confirms that weighted incidence, packet multiplicity, and envelope
normalization can coexist without a large measured loss. It does not prove the
envelope comparison uniformly or with the required complete-prime-block
weights. The next analytic target is to compare the endpoint pair-square
envelope with complete conductor energy and then transfer full-period energy
to the active row window while preserving the Q restriction and 1/A incidence
gain. Any power loss in B rejects that formulation. Non-endpoint modes, signed
prime correlation, and Goldbach stay OPEN.

### 2026-09-11 continuation: arbitrary conductor energy cannot close endpoints

The endpoint/conductor comparison splits into one surviving lemma and one
sharp obstruction. For `n=m-1` and squarefree `d`, the distinct endpoint
frequency energy satisfies

`E_end(d)<=min(1,2*pi^2*n*2^omega(d)/phi(d))*H_m(d)`.

This follows by counting primitive frequencies up to `d/(2n)`, where every
geometric sum has magnitude at least `2n/pi`. It is a reusable subpower
endpoint-dilution tool.

It does not absorb the difference-denominator weight. For coprime supported
conductors `d,e>=2n`, `(m,de)=1`, `de>mA`, normalize an otherwise zero
coefficient vector by `S_d=H_m(d)^(-1/2)` and
`S_e=H_m(e)^(-1/2)`. Its conductor energy is 2, while its eight ordered
cross-endpoint pairs all have `Q=de` and force

`endpoint pair-square envelope / conductor energy^2
 >=32n^2/pi^4`.

The exact certificate `(m,A,d,e)=(101,10,221,437)` gives `19452.67` against
the rigorous lower bound `3285.11`. Independent proof/code review PASSed,
including exhaustive squarefree and conductor-pair checks. Therefore a
generic arbitrary-conductor-vector, conductor-energy-only subpower comparison
is directly contradicted. The actual three-coordinate polynomial family,
prime aggregation, endpoint incidence, and endpoint-dilution lemma remain
active; no polynomial tool is discarded.

The next bounded test lifts the three polynomial coordinates to the six
symmetric-square monomials. In that space the endpoint envelope and the full
exact-Q residue energy become two explicit positive semidefinite quadratic
forms. Test their complete-prime-block generalized eigenvalue and nullspace.
Growth or a numerator-positive denominator-null direction rejects this lifted
sufficient route, not necessarily the rank-one actual polynomial family.
Passing finite blocks would leave a concrete six-coordinate
bilinear prime-row theorem, not a proof of it. The signed prime-correlation
estimate and Goldbach remain OPEN.

### 2026-09-11 continuation: lifted full-period endpoint frame passes finitely

The three polynomial coordinates were lifted exactly to the six symmetric
monomials. Exact grouping by `(Q,r)` produces PSD forms `N_m,D_m` with

`y^T N_m y = sum_(endpoint pairs,Q>mA) Q|c_i c_j|^2`,

`y^T D_m y = sum_(Q>mA) Q sum_(r,Q)=1 |D_Q(r;y)|^2`.

The actual polynomial selector is `y=(1,...,1)` after embedding the log powers
in the conductor basis. Independent scalar grouping reconstructs both forms.
After summing matrices over every prime before taking one generalized
direction, the complete unweighted blocks give lifted/actual ratios
`.296974/.273013` at `M=127` and `.263441/.256514` at `M=251`. Both
denominator matrices have rank 6, with no numerator-positive null direction.
The maximum individual lifted ratios are `.393341` and `.336431`.

Independent review PASSed the algebra, exact residue grouping, PSD and
generalized-eigenvalue logic, diagonal equilibration, reconstruction, and
aggregation. It reproduced the full `M=127` block and one `M=251` prime. The
captured full `M=251` run took `257.4` seconds. These are finite full-period,
unweighted measurements, not a uniform or prime-weighted theorem.

The six-dimensional space is only a sufficient relaxation of the rank-one
polynomial lifts. The next bounded hypothesis compares the same endpoint form
with the active-window residue-energy Gram. An active-denominator null
direction or power-growing generalized ratio rejects the lifted sufficient
route. A finite pass would isolate the six bilinear entries requiring a
weighted prime-row estimate. The signed prime-correlation estimate and
Goldbach remain OPEN.
### 2026-09-11 continuation: active-window lifted frame passes finitely

For the actual rows `A<=ell<2A`, the exact six-vector residue coefficients now
give the PSD form

`D_active(y)=sum_(Q>mA)Q*A^(-1)sum_ell|T_Q(ell;y)|^2`.

The complete unweighted `M=127` block has lifted/actual endpoint-to-active
ratios `.331216/.287160` and actual active/full energy `.950735`. At `M=251`
the corresponding values are `.259769/.252997` and `1.013903`. Both active
denominator forms have rank 6 with no numerator-positive null direction; the
maximum individual lifted ratios are `.480153` and `.361873`.

Independent review reproduced the full smaller block and the `m=251`
one-prime active values, checked the inverse-FFT sign and `Q/A` normalization,
and verified the aggregate matrix order. A separate scalar test at
`lambda=(2,-1,3)` reconstructs the active quadratic form. The captured exact
larger block took `399.3` seconds.

This supports only a finite unweighted sufficient relaxation. It proves no
constant-one window law, uniform bound, outer-weighted block estimate,
rank-one polynomial theorem, or signed prime correlation. The next bounded
test repeats matrix-first aggregation with the four existing positive outer
weights. Strong weight sensitivity or growth rejects that route; stable finite
ratios would leave a six-coordinate weighted prime-row estimate as the next
analytic obligation. Goldbach remains OPEN.

### 2026-09-11 continuation: four outer weights are stable on two blocks

The lifted endpoint and active-window matrices were aggregated before the
generalized quotient with the existing weights `1`, `log(m)^2/m`,
`rho_m log(m)^2/m`, and `rho_m*m*log(m)^2`. The relaxed ratios are respectively

`M=127: .331216, .330626, .330721, .334205`,

`M=251: .259769, .258553, .258602, .263471`.

All weighted denominators have rank 6 and no numerator-positive null
direction. Actual-selector ratios vary only from `.284545` to `.292816` at the
smaller block and `.251971` to `.254539` at the larger. Thus neither strong
weight sensitivity nor scale growth appears in this finite test.

Independent review reproduced the complete `M=127` weighted block, checked the
`rho_m` and matrix-first conventions, and audited the captured larger-block
loop. Review PASSed; numerical conclusions are limited to the displayed
precision.

This is `changed-under-evidence`, not a theorem: the arbitrary-vector
conductor-energy route remains directly contradicted, but the structured
polynomial coordinates, rank-one subfamily, positive weights, prime averaging,
and active-row Gram remain available together. The next target is a uniform
matrix-first weighted six-coordinate endpoint/active inequality. Its proof,
the sharper rank-one alternative, and the signed prime correlation all remain
OPEN. Goldbach remains OPEN.

### 2026-09-11 continuation: outer weights reduce to one unweighted PSD bound

For arbitrary positive semidefinite pairs `N_m,D_m`, positivity proves

`sum w_m N_m <= C*kappa_w sum w_m D_m`,

whenever `sum N_m<=C sum D_m`, with
`kappa_w=max_m(w_m)/min_m(w_m)`. For the four project weights, exact counting
of the strict active-frequency interval gives `kappa_rho<8` on every dyadic
block `M>=17`; logarithmic monotonicity yields uniform distortion bounds
`1,2,16,25`.

Independent review PASSed the matrix proof, active-mode formula, uniform
constants, shared implementation, and exact `M=127,251` receipts. Normal and
optimized focused tests pass. Status `aha-candidate`, novelty
`new-to-this-task`: the four outer-weighted lifted estimates are now reduced
to one unweighted Loewner estimate at fixed cost.

That unweighted endpoint/active inequality remains OPEN. No rank-one or signed
prime-correlation theorem follows. The next bounded test asks whether the
unweighted six-coordinate comparison holds uniformly for each prime rather
than only after block aggregation; growth of the individual generalized
quotient falsifies that stronger route while preserving the block-average and
polynomial components. Goldbach remains OPEN.

### 2026-09-11 continuation: finite six-coordinate active/full lower frame

The new exact diagnostic tests

`D_active,m >= c D_full,m`

on the six lifted coordinates. A nullspace-coupling error in the first minimum
implementation was caught by independent review and corrected with the Schur
complement before promotion. Rank-zero full forms are vacuous; singular
nonzero forms minimize globally over their nullspaces.

The aggregate spectra are `[.876880,1.146289]` at `M=127` and
`[1.000055,1.024474]` at `M=251`. Minimum nonvacuous individual lower values
are `.520814` at `m=151` and `.736692` at `m=269`; the tiny `M=95` support
gives `.631274`. Thus the concrete finite candidate `c=1/2` survives all
tested nonvacuous primes. Independent corrected review returned PASS.

This is finite `changed-under-evidence`, not a uniform theorem. It differs from
the earlier divisor-progression active/rho-full result and does not prove the
rank-one polynomial comparison or signed prime correlation. A separate
`m=503` endpoint/active computation passed at `.289096`, but the complete
73-prime block was stopped after one row because its serial runtime would
exceed the 30-minute budget. The next test examines whether the worst
six-coordinate lower-frame direction is close to a rank-one polynomial lift.
Goldbach remains OPEN.

### 2026-09-11 continuation: rank-one sharpening fails at the worst prime

For `m=151`, the corrected relaxed active/full minimum is `.5208139494943`.
The associated symmetric matrix has relative projective signed-rank-one
Frobenius distance `.145708107581`. Direct deterministic optimization on
`y=lambda lambda^T` finds an explicit quotient `.521176346342`, only `.0696%`
above the rigorous relaxed lower bound. The actual selector `(1,1,1)` gives
`.859110744`.

Independent review verified the Schur minimizer, coordinate map, analytic
gradient, explicit candidate quotient, and numerical scope. Review PASSed.
Status `abandoned` applies only to the hypothesis that imposing rank one gives
material extra lower-frame margin at this fixture. It does not reject the
rank-one polynomial family or polynomial weights. The numerical search is an
upper-bound witness, not proof of its global minimum.

The six-coordinate lower-frame theorem therefore remains the cleaner
sufficient target. Its uniform proof, the signed prime correlation, and
Goldbach remain OPEN.

### 2026-09-11 continuation: aggregate Gershgorin certifies one half finitely

After diagonal equilibration and exact eigenspace whitening of the aggregate
`D_full`, the transformed active form `W` has Gershgorin lower bounds
`.745431302419` at `M=127` and `.989533649267` at `M=251`. The exact generalized
minima are `.876880294682` and `1.000054641629`, respectively. Thus absolute
off-diagonal row sums already certify `D_active>=D_full/2` on both finite
aggregate blocks.

Independent review PASSed the congruences, orientation, Gershgorin implication,
guards, smaller receipt, and captured larger loop. This is
`changed-under-evidence`: unlike the earlier failed diagonally normalized
divisor-progression Gershgorin route, exact whitening of this six-coordinate
aggregate produces strong finite row margins.

The uniform entrywise estimates are OPEN. The next proof target is
`W_ii-sum_(j!=i)|W_ij|>=1/2` for all six rows at project scale. This finite
certificate does not prove the lower-frame theorem, signed prime correlation,
or Goldbach.

### 2026-09-11 continuation: raw coordinate Gershgorin is falsified

For `C_ii=D_full(ii)^(-1/2)`, the direct scaled difference
`C(D_active-D_full/2)C` at `M=127` has diagonal range
`[.455089,.469415]`, absolute row-radius range `[2.284714,2.312280]`, and
minimum Gershgorin edge `-1.846212097816`. The difference is nevertheless PSD,
so this is cancellation lost by the certificate rather than failure of the
lower-frame inequality.

Independent review reproduced the values and returned PASS. Status
`abandoned` applies only to diagonal scaling plus raw-coordinate Gershgorin.
Exact whitening, the half-frame candidate, rank-one/polynomial components, and
the signed problem remain active. The next test seeks an explicit centered
polynomial basis whose symmetric square approximates full-Gram whitening.
Goldbach remains OPEN.

### 2026-09-11 continuation: fixed dyadic-centered basis is falsified

Use `z=(L-mu)/s`, where
`mu=log(sqrt(2)*M*ell_freeze)` and `s=log(2)/2`, to map coefficients of
`a2*z^2+a1*z+a0` into the original `(L^2,L,1)` degree basis. Applying the
exact symmetric square of this fixed three-coordinate transform to the
aggregate active/full forms at `M=127` gives minimum diagonal-scaled
Gershgorin edge `-1.866444004344` for `D_active-D_full/2`. The raw-basis edge
was `-1.846212097816`, and the invariant generalized minimum is still
`.876880294682`.

The declared negative-edge falsifier fired, so the larger block was not run.
Status `abandoned` applies only to this exact midpoint/half-log-two transform
combined with raw-coordinate Gershgorin. The polynomial identities, other
basis changes, full-Gram whitening, half-frame candidate, and possible new
arithmetic ingredients remain active. The signed prime correlation and
Goldbach remain OPEN.

### 2026-09-11 continuation: arithmetic covariance recovers part of the cancellation

For every supported primitive frequency, let `b` be its three degree-labelled
coordinate vector and `G` its geometric coefficient. The unsummed positive
matrix

`C=sum |G|^2 b b^T`

is a natural one-frequency conductor-energy covariance. At `M=127`, whiten
this three-dimensional `C`, take the exact symmetric square of that transform,
and apply diagonal-scaled scalar Gershgorin to `D_active-D_full/2`. The minimum
edge improves from the raw basis value `-1.846212097816` to
`-.676462318151`, but remains negative. The six individual edges are all
negative, so the declared scalar-certificate falsifier fires.

The same transform reduces the condition number of the diagonally
equilibrated full Gram from about `5.51e11` to `5.71e3`, an improvement by
more than seven orders of magnitude. It is therefore a useful preconditioner
even though its scalar absolute row sums remain too large.

Pursuit status `changed-under-evidence`: the exact conjunction of
one-frequency covariance whitening, symmetric-square lift, and scalar
Gershgorin is blocked at this fixture, while the large improvement supports
the conductor covariance as a useful component for a block or sign-sensitive
argument. No uniform comparison between this covariance and the full Gram is
proved. Polynomial identities and bounds remain active. The signed prime
correlation and Goldbach remain OPEN.

### 2026-09-11 continuation: trace/traceless block norm is too coarse

After the one-frequency arithmetic whitening, use the canonical decomposition
`Sym^2(R^3)=span(I)+Sym^2_0(R^3)` and test the diagonally scaled difference
`D_active-D_full/2` by a `1+5` two-block Gershgorin bound. At `M=127`, the
trace block value is `.471397947622`, the traceless block minimum is
`.013920013451`, and the cross-block operator norm is `.572958667340`.
Consequently the two block edges are `-.101560719718` and
`-.559038653889`; the declared negative-edge falsifier fires.

The full scaled difference still has smallest eigenvalue `.000153909342`,
and eliminating the traceless block exactly gives positive trace Schur
complement `.000385168986`. Thus the lower-frame matrix survives through a
nearly saturated trace/traceless interaction that the separate block minima
and one cross norm discard.

Pursuit status `changed-under-evidence`. Block only this arithmetic basis,
canonical `1+5` split, and coarse two-block norm certificate. Preserve the
trace/traceless decomposition and Schur interaction for an arithmetic estimate
that retains their alignment. No uniform frame or signed prime-correlation
estimate follows, and Goldbach remains OPEN.

### 2026-09-11 continuation: the Schur response is nearly axial

In the arithmetic-whitened trace/traceless split, write the unscaled candidate
difference as `H=[[a,b],[b^T,C_0]]`. Map the eliminating response
`v=-C_0^(-1)b^T` back to a traceless symmetric `3 by 3` tensor. The orbit
`alpha*(u*u^T-I/3)` is characterized projectively by eigenvalue pattern
`2:-1:-1`; its Frobenius distance is rotation invariant.

At `M=127`, the response eigenvalues are
`(-.565862,-.541268,1.107130)` and the axial distance is `.0128247`. The
independently larger complete block `M=251` gives
`(-.578949,-.525283,1.104231)` and distance `.0280486`. The latter scan took
`371.8` seconds on the stable difference-first route. Both pass the declared
10-percent falsifier by a wide margin.

The cross row `b` itself is a covector; directly treating its monomial
coefficients as a primal symmetric tensor misses the Frobenius-dual
off-diagonal factors. That comparison was removed. The stated invariant
applies only after `C_0^(-1)` produces the primal Schur response.

Status `aha-candidate`, novelty `new-to-this-task`: the Schur response is an
almost single-axis quadrupole on two finite blocks. The next concrete question
is whether the non-axial residual
can be bounded uniformly relative to the positive trace Schur margin. No
uniform axial theorem, margin-preserving replacement, active/full lower frame,
signed prime correlation, or Goldbach theorem follows yet.

### 2026-09-11 continuation: axial error stays below the Schur margin finitely

Let `v_ax` be the best Frobenius axial approximation to the exact response
`v=-C_0^(-1)b^T`. Completing the square gives the exact finite identity

`Schur margin = q(v_ax)-(v_ax-v)^T C_0 (v_ax-v)`.

At `M=127`, the margin is `.005795730854` and the nonaxial energy error is
`.005427450063`, ratio `.9364565`; the error is `.4835929` of the axial trial
value. At `M=251`, the margin is `.3004649470`, error `.1723708946`, ratio
`.5736805`; the error is `.3645406` of the axial trial value. Both pass the
predeclared error-below-margin test, though the smaller fixture is close.

The stable computation forms `D_active-D_full/2` before the arithmetic
congruence. Subtracting separately transformed forms perturbs the tiny smaller
margin, so that order is superseded. Pursuit status `changed-under-evidence`:
the axial pattern now supplies two explicit analytic obligations—lower-bound
`q(v_ax)` and upper-bound the nonaxial `C_0`-energy. Neither uniform bound is
proved. The active/full lower frame, signed prime correlation, and Goldbach
remain OPEN.

### 2026-09-11 continuation: axiality is one determinant inequality

For every nonzero real symmetric traceless `3 by 3` tensor `K`, define

`J(K)=3*sqrt(6)*|det K|/||K||_F^3`.

Diagonalization and the traceless eigenvalue-circle parametrization prove

`distance_projective(K, axial orbit)=sin(acos(J(K))/3)`.

The proof uses
`lambda_j=sqrt(2/3)r cos(theta+2*pi*j/3)`, so
`3*sqrt(6)det(K)/r^3=cos(3 theta)`; projective axial rays occur every
`pi/3`. This is an exact elementary identity, not a finite fit.

For the stable Schur responses, `J=.9992599265` at `M=127` and
`J=.9964609101` at `M=251`. The earlier distance threshold `.1` is exactly
equivalent to `J>=cos(3 asin(.1))=.9551879396`. Status `aha-candidate`,
novelty `new-to-this-task`: a five-coordinate spectral-looking condition is
now one scalar determinant/norm inequality. A uniform lower bound for this
specific arithmetic response invariant, the axial/nonaxial energy estimates,
the lower frame, signed prime correlation, and Goldbach remain OPEN.

### 2026-09-11 continuation: the axial axis lies on a scaled-log moment curve

The first interpretation test is negative: at `M=127`, the selected axial
axis in arithmetic-whitened parameter space is `60.9127` degrees from the
actual selector `lambda=(1,1,1)`. Status `abandoned` applies only to identifying
the weak frame direction with the actual selector.

After mapping the axis back to original degree parameters, a stronger pattern
appears. Its best projective fits to `(t^2,t,1)` are

`M=127: t=.2795716513, distance=4.16667e-5`,

`M=251: t=.2809004167, distance=5.55179e-5`.

Both pass the predeclared one-percent falsifier by more than two orders of
magnitude. Since `K_q(L)=A_q L^2+B_q L+C_q`, the selector `(t^2,t,1)` exactly
evaluates the same conductor polynomial at `tL`. The fitted `t` values also
lie inside the divisor-log exponent support `.15--.32` when `L` is the global
`log(m*ell)` scale.

Status `aha-candidate`, novelty `new-to-this-task`. The next concrete question
is whether `t` equals or is controlled by an explicit weighted statistic of
`log d/log(m*ell)` from the one-frequency conductor covariance. No formula,
uniform moment-curve alignment, lower frame, signed prime correlation, or
Goldbach theorem is proved.

### 2026-09-11 continuation: centroid fails; upper-conductor proximity is coarse

The first explicit formula for the fitted scaled-log parameter is falsified.
Using positive weights `A_d^2|G|^2`, the means of the normalized conductor
quadratic vertices `-B_d/(2A_d L)` are

`M=127: .2402747204` and `M=251: .2458970461`,

missing the fitted `.2795716513,.2809004167` by `.03930,.03500`. Both exceed
the predeclared `.01` error threshold. Block only this exact positive centroid;
the moment-curve observation and polynomial components remain active.

The vertex of the largest conductor with nonzero quadratic coefficient gives
`.2779236924` for `d=143` and `.2858488160` for `d=323`, with errors
`.001648,.004948`. Thus the largest-conductor vertex lies within the coarse
one-percent scale of `t` on both blocks, but does not equal it and drifts
across it.

Pursuit status `changed-under-evidence`. Preserve the finite upper-support
proximity as a candidate observation and reject the simple centroid as a
formula. The fitted parameters were supplied to this comparison, not derived
by it. A dominance mechanism, uniform effective-log formula, lower frame,
signed prime correlation, and Goldbach remain OPEN.

The next non-averaged positive statistic also fails. The conductors with the
largest total `A_d^2|G|^2` weights are `d=91` at `M=127` and `d=30` at
`M=251`; their midpoint vertices `.2526121254,.2532200077` miss the fitted
parameters by `.02696,.02768`. The `.01` falsifier therefore rejects the
largest-positive-weight conductor formula as well. This further narrows the
surviving observation to finite proximity with the upper conductor boundary,
without a positive-weight dominance explanation.

### 2026-09-12 continuation: the old mod-130 source is a fiber average of F_130

The source-assembly bridge now has one exact finite component. The actual
direct full-period lag-130 source `F_130` on `U_10010` does not descend
pointwise to `U_130`, but its centered fiber sums do. For every `r in U_130`,
with

`S_130(r)=sum_(a in U_10010, a=r mod 130)F_130(a)`,

the previously used globally centered recombined quotient-77 source satisfies

`G_0(r)=-(S_130(r)-mean_s S_130(s))`.

Each fiber has `60` lifts, so the equivalent fiber-average form is
`G_0=-60` times the centered average of `F_130` over the fibers. The reviewed
finite reconstruction error is about `2.5e-14`; the best coefficient is `-1`
up to roundoff. The lag-110 fiber source is a negative control, with
correlation about `.03145` to `G_0` and direct negative reconstruction error
greater than `.9`.

Independent review returned PASS for the sign, factor `60`, centering,
source provenance, lag-110 negative control, and scope. The focused test
passes normally and under `-O`; the full
`test_lcm_sawtooth_goldbach_transfer` module now has four tests and passes in
`146.863s`. This is an `aha-candidate`, novelty `new-to-this-task`.

This result connects the older mod-130 Halupczok transfer to the new direct
U10010 source theorem as a fiber-averaged shadow. It still does not prove
pointwise descent, original outer assembly identification, the formal
`T_boundary-Delta` signed estimate, or Goldbach. The next question is whether
the original count-four outer assembly uses this lag-130 fiber-shadow channel
with fixed coefficients, or whether it also contains moving coefficients,
lag 110, omitted source families, endpoints, or a scale-dependent boundary
remainder.

### 2026-09-12 continuation: the centered fixture channel uses that shadow

The source-table bridge now extends to the tested linked-prime outer channel.
On fixture targets `1000` and `1002`, the quotient-77 recombined centered
source correlation from `linked_prime_centering_receipt` equals the strict
central prime sum weighted by the lag-130 fiber shadow

`G_shadow(r)=-(S_130(r)-mean_s S_130(s))`.

The principal constant channel remains separate, and constant plus centered
shadow reconstructs the quotient-77 direct channel. The quotient-91 channel,
corresponding to lag `110`, cancels on these fixtures.

Independent review returned PASS. The strict central intervals are
`(333,667)` and `(334,668)`, with `18` and `24` linked-prime terms and no
nonunit or inadmissible terms. Faraday independently checked the
lag-to-quotient correspondence, sign and centering, weighted correlations
approximately `-224301.665678` and `430678.315436`, quotient-77 reconstruction
to `5.38e-13`, quotient-91 cancellation at relative scale `1.97e-16`, and the
open-scope flags.

Status `changed-under-evidence`: the tested centered quotient-77 outer channel
is the lag-130 fiber shadow. This still does not identify the full outer
assembly, endpoints, all target residues, the formal `T_boundary-Delta`
signed estimate, a pointwise estimate, or Goldbach. The next bounded question
is whether this constant-plus-fiber-shadow decomposition extends beyond the
fixture targets to every target class required by the original assembly, or
whether nonfixture/end boundary terms introduce moving coefficients.

### 2026-09-12 continuation: all 65 even classes pass the centered sample

The centered channel bridge now has a finite representative test in every
even target class modulo `130`. The default receipt selects `65` targets
spanning `10000..10128`, each with a strict-central prime pair, and compares
the quotient-77 recombined centered channel with the lag-130 fiber-shadow
prime sum.

The maximum natural-scale bridge error is `4.941748661419397e-13`. The
signed/final-scale diagnostic is `1.22718066202769e-10`, below the separate
`1e-9` diagnostic tolerance; this scale is retained because signed
cancellation can make the final value smaller than the termwise identity
scale. Quotient-91 cancels at relative scale `5.160774356541489e-16`, and no
nonunit or inadmissible terms occur.

Independent review returned PASS, including the 65 residue selection,
strict-central ordered-pair convention, lag-to-quotient mapping,
natural-versus-signed scale distinction, quotient-91 cancellation, and scope
flags. Status `changed-under-evidence`: the centered quotient-77 bridge is
not just a fixture accident. It remains finite sample evidence only; a
symbolic all-target proof, endpoint/noncentral terms, full outer assembly,
formal `T_boundary-Delta`, pointwise control, and Goldbach remain open.

### 2026-09-12 continuation: symbolic centered bridge for N>=40

The centered bridge is now a coefficient identity rather than a finite target
sample. Recombining all four quotient-77 divisor rows and centering the
resulting `U_130` vector gives the negative lag-130 fiber shadow with relative
error `2.520761115387016e-14`. The quotient-91 recombined source cancels at
relative sectorwise `L^2` scale `2.446659437662094e-16`.

For every even `N>=40`, strict central prime pairs have both primes greater
than `13`, so they are units modulo `130`. Thus, with the existing ordered
strict-central convention, the quotient-77 centered unit correlation equals
the central Goldbach sum weighted by

`G_shadow(r)=-(S_130(r)-mean_s S_130(s))`.

Independent review returned PASS for the four-row recombination, centering,
sign and 60-lift factor, quotient-91 cancellation, the `N>=40` threshold,
ordered interval convention, and open-scope flags. Status `aha-candidate`,
novelty `new-to-this-task`. Endpoint/noncentral terms, the principal constant
channel, full outer assembly, formal `T_boundary-Delta`, pointwise signed
control, and Goldbach remain open.

## 2026-09-12: principal plus centered quotient-77 channel

The strict-central quotient-77 direct channel has now been split into its
principal and centered parts as a coefficient-vector identity.  In
`symbolic_principal_plus_centered_channel_receipt`, the recombined quotient-77
source on `U_130` equals a constant vector plus the negative lag-130 fiber
shadow already identified in the symbolic centered bridge.

The measured principal constant is approximately
`-196.43749999997192 + 1.29e-12i`, with rational witness
`c0=-3143/16`.  Because this witness is recovered from floating source tables,
its check uses a separate `1e-10` numerical tolerance; the actual source-vector
reconstruction remains at relative error `2.520761115387016e-14`, below the
`1e-12` identity tolerance.

Consequently, for every even `N>=40`, the strict-central quotient-77 direct
unit channel has the form

`c0*W_unit(N) + sum_(N/3<p<2N/3, p,N-p prime)
   log(p)log(N-p) G_shadow(p mod 130)`,

using the existing ordered strict-central convention and
`G_shadow(r)=-(S_130(r)-mean_s S_130(s))`.  The `N>=40` threshold is unchanged:
strict central prime pairs then have both primes greater than `13`, so no
nonunit modulo-130 correction enters this channel.

Independent review returned PASS. Faraday checked that all four quotient-77
rows are recombined, that the row vector is target-independent by construction,
that the fiber-shadow sign is correct, that the rational witness is within the
separate numerical tolerance, that the ordered strict-central formula applies,
and that the open-scope flags remain false.

Focused normal and optimized tests pass.  This is progress on the bookkeeping
bridge, not on the missing signed prime-correlation estimate.  Endpoint and
noncentral terms, the full outer assembly, the formal `T_boundary-Delta` error,
pointwise signed control, and Goldbach remain open.

Next concrete question: in the original outer assembly, are the remaining
endpoint/noncentral contributions expressible as explicit boundary channels
with controlled sign or cancellation, or do they introduce a moving coefficient
that is exactly where the signed estimate still lives?  A useful next test is
to recover the full assembly term-by-term and compare it against the reviewed
principal-plus-shadow strict-central channel, with any residual classified by
support, coefficient source, and dependence on `N`.

## 2026-09-12: q286 discrepancy is a two-sided fiber imbalance

`q286_residue_discrepancy_profile_receipt` expands the q286 lower-modulus
deviation as
`sum_r (W_N(r)-mean_s W_N(s))*C_q286(r)` over admissible unit residues modulo
`286`.  This is the first residue-fiber view of the dominant obstruction:
the local q286 prediction can be positive while the actual contribution is
negative because the strict-central prime-pair weights are unevenly
distributed across signed q286 fibers.  The measured profile is two-sided:
negative q286 coefficient fibers are overweighted in aggregate, while some
large positive coefficient fibers are underweighted and can produce the
largest individual negative deviation terms.

This is not yet a signed estimate.  It identifies the target estimate:
control the dot product between prime-pair residue imbalance modulo `286` and
the q286 coefficient vector, then fold in the secondary q70 and q154 supports.

Measured on `N=10424,14138,88346`, the q286 deviation reconstruction error is
`3.7884157269915995e-30`, and the weight/coefficient real correlation is
negative on all three targets.  The three correlations are
`-0.19146520713929577`, `-0.1727458822172166`, and
`-0.30904476926988145`.  Negative coefficient fibers are overweighted by
factors `1.2533749052918906`, `1.106127240484188`, and
`1.0999171345323129`, while positive coefficient fibers are underweighted by
ratios `0.8552143398332065`, `0.9366660016465346`, and
`0.9403720326178112`.

The strongest individual negative terms are not exclusively overweighted
negative fibers.  Large positive fibers `133` and `153` recur at the top when
they are underweighted, so the eventual theorem must bound the full signed
imbalance vector, not merely count prime pairs in negative coefficient
classes.

As an L2/Cauchy target, the observed q286 residue-weight L2 deviations relative
to total prime-pair weight are `0.10117134973122574`, `0.0999185136738501`, and
`0.050092570911679776`.  The corresponding one-principal-unit sufficiency
thresholds are about `0.02`.  These bad targets therefore violate a crude
q286-only Cauchy threshold, but the actual signed deviation uses only about
`17%` to `31%` of the Cauchy envelope.  Next estimate route: prove either
stronger residue-weight L2 equidistribution or a signed angle bound between
the imbalance vector and `C_q286`.

## 2026-09-12: q286 character imbalance is narrower than residue support

The q286 deviation also has an exact character-coordinate form.  The coefficient
reconstructs from characters modulo `286` with relative error
`2.3684586932433417e-15`, and the bad-target deviations reconstruct with
maximum relative error `1.938291320163869e-15`.

The useful surprise is that only `59` character coefficients are active above
tolerance, not all `99` possible labels that are nontrivial at both primes
`11` and `13`.  Every active label still has both-prime support.  The leading
coefficient labels are stable coefficient features, but the leading negative
target-contribution labels vary with `N`, so the immediate route is not a
single-character obstruction.  The target estimate is a finite family of
twisted strict-central Goldbach sums modulo `286`, with a 59-character
coefficient support.

## 2026-09-12: q286 character matrix is effectively low-rank

The q286 character coefficient matrix over nontrivial labels modulo `11` and
`13` has shape `9 x 11`, with `59` active entries.  It has full numerical row
rank `9`, so no exact low-rank proof has been found.  But the singular spectrum
is highly concentrated: the first two singular modes carry
`0.9760410444893589` of coefficient energy, and the first four carry
`0.9970750809967631`.

This changes the next estimate experiment.  Instead of treating q286 only as
59 unrelated twisted sums, test whether the leading separable singular modes
have a stronger signed prime-pair estimate, while the small singular tail is
paid by a crude large-sieve or L2 bound.

## 2026-09-12: leading q286 singular modes explain sampled bad deviations

The singular compression survives the first target-side falsifier.  On the
three bad targets `10424,14138,88346`, the first two singular modes explain
about `90.16%`, `100.37%`, and `98.71%` of the signed q286 deviation.  The
first four modes explain `100.68%`, `98.63%`, and `101.62%`, so their signed
residual is at most about `1.62%` of the actual q286 deviation in the sample.

But the first-four tail is not proved harmless by Cauchy: the tail Cauchy
envelope remains up to `0.3016306796889374` of the actual deviation.  Thus a
valid proof route cannot simply discard the tail from coefficient energy.  It
must either prove a better tail/imbalance angle bound or keep enough modes that
the remaining Cauchy envelope is below the positive margin.

## 2026-09-12: singular modes pass lower-tail stress but not all targets

A broader stress set shows the leading q286 singular modes are a lower-tail
tool, not a uniform approximation theorem.  On negative q286-deviation targets
in the set `10424,10664,10814,14138,14732,58736,88346,125504`, the first four
modes leave at most about `0.055453596612858175` signed residual fraction.

The stress falsifier is `N=14732`: q286 is positive and small there, and the
first-four residual is about `0.21904521472590485` of the small q286 deviation,
with a crude Cauchy tail envelope about `6.743841172259878` times the actual
deviation.  Therefore singular compression should be used for negative
excursion control or margin-relative estimates, not as a pointwise equality
shortcut.

## 2026-09-12: q286 singular-mode cycle scan added

`q286_singular_mode_cycle_scan_receipt` is now the bounded scanner for the
singular-mode lower-tail hypothesis.  It tests consecutive even targets across
period cycles and reports negative q286 lower-tail counts, worst negative
first-four/six residuals, significant-negative residuals, worst all-target
residuals, and residual size relative to the principal margin separately.

Use it to decide whether the leading-mode estimate should be promoted into a
formal proof attempt.  It remains sampled evidence only; it is not a signed
prime-correlation theorem.

The first `4` cycles sampled at `251` consecutive even targets each give
`1004` total targets.  q286 is negative at `529`, but only `120` are below
`-0.4` of the principal.  The all-negative relative approximation claim fails:
near-zero q286 deviations such as `N=20494` make the first-four residual
`19.725975817977446` times the tiny q286 deviation.  Measured against the
principal margin, however, the worst first-four residual is only
`0.06654914350747668` of principal.

For significant negative q286 deviations, the first-four singular modes remain
useful in this sample: the worst residual/deviation fraction is
`0.09165079440299802` at `N=30202`.  Next proof-shaped target: formulate a
principal-margin inequality, not a relative-to-q286-deviation approximation.

The complete first even-residue period `10000..20008` changes the compression
target from four modes to six.  Among `5005` targets, q286 has `2475` negative
deviations and `594` significant negatives below `-0.4` principal.  First-four
significant-negative control fails at `N=14680`, with residual/deviation
`0.17156063983875328`, although the first-four residual stays below
`0.09572218559054874` of principal.

Using six singular modes improves the first-period sample: worst significant
six-mode residual/deviation is `0.07205086151962896`, and the worst six-mode
principal-relative residual is `0.033888231610242146`.  Next target: estimate
the six leading separable q286 modes directly and prove a principal-margin
tail bound for the remaining three singular modes.

## 2026-09-12: dominant support matrix scanner added

`dominant_support_character_matrix_structure_receipt` now applies the
character-matrix/SVD diagnostic to `(11,13)`/`286`, `(7,11)`/`154`, and
`(5,7)`/`70`.  The next question is whether the secondary q154 and q70
supports have similarly small separable-mode skeletons, so the full centered
error can be attacked as a short list of product-character modes plus tails.

Measured answer: yes, coefficient-side compression is present in all three
dominant supports.  Top-two singular energy is `0.9760410444893589` for q286,
`0.906627345943789` for q154, and `0.9915109122214548` for q70.  The supports
still have full row rank (`9`, `5`, and `3` respectively), so this is not an
exact algebraic collapse.  It is a leading-mode/tail analytic strategy.

## 2026-09-12: dominant support tail scanner added

The next decomposition target is implemented in
`dominant_support_singular_tail_scan_receipt`: exact lower-modulus local
predictions plus leading singular modes for the three dominant supports,
defaulting to six q286 modes, all five q154 modes, and all three q70 modes.  It measures
the remaining combined tail relative to the principal contribution.

If the combined tail stays small in principal units while the leading modes
explain the negative excursions, the analytic proof target becomes a finite
list of separable twisted Goldbach estimates plus an explicit tail inequality.

The first `501` targets show why the default pays q154 and q70 exactly.  The
`6+4+2` budget has worst tail/principal `0.1013264220803796`, just beyond the
initial `0.1` diagnostic mark.  The `6+5+3` budget has worst tail/principal
`0.026483963220719955`, leaving only the q286 singular tail.  This is a
cleaner proof target: six q286 separable modes plus exact secondary dominant
supports plus a small q286 tail.

On the full first period, the default `6+5+3` scan tests all `5005` even
targets from `10000` through `20008`.  The combined dominant supports are
negative at `2789` targets, but the worst remaining tail after the modeled
local-plus-singular decomposition is only `0.03388823161024216` of principal.
The most negative modeled dominant-support ratio is `-1.9465533807058557` at
`N=14138`.

This means the next proof-shaped work should not spend effort compressing q154
or q70 further.  Keep them exact and focus on estimating the six q286 leading
modes and the q286 three-mode tail relative to the principal margin.

## 2026-09-12: q286 singular mode contribution scanner added

`q286_leading_singular_mode_contribution_receipt` now decomposes the six q286
leading modes into individual rank-one contributions.  Use it to decide
whether the analytic problem has one dominant separable twist or a genuinely
multi-mode signed family.  It keeps the output in principal-relative units so
future bounds can be compared directly with the positivity margin.

Measured answer: the obstruction is multi-mode.  On
`N=10424,14138,14680,88346`, modes `1`, `2`, and `3` are negative on every
target, and there is no single common negative mode.  Mode `1` is largest at
`10424`, `14138`, and `88346`, while mode `2` is largest at `14680`.

Six-mode sums nearly reproduce q286 on these targets: residual/principal is
about `-0.00873`, `0.000038`, `0.01110`, and `0.00927`.  Next proof-shaped
target: estimate a small multi-mode family, especially common negative modes
`1..3`, rather than betting on one separable character twist.

## 2026-09-12: q286 leading mode period-profile scanner added

`q286_leading_mode_cycle_profile_receipt` now profiles modes `1..6` over
consecutive target ranges.  It records whether modes `1..3` remain negative on
significant q286 lower-tail targets across a broader scan, or whether the
common-negative observation was a small-target artifact.

Measured answer: common-negative mode control is a small-target artifact.  In
the full first period `10000..20008`, no leading mode is negative on every
significant q286 lower-tail target.  Modes `1` and `2` are still negative on
most significant lower tails (`562/594` and `493/594`), while modes `3..6`
are more target-dependent.

Next target: formulate a target-dependent signed envelope for the six q286
modes, likely using principal-relative mode-size bounds and cancellation among
positive/negative modes, rather than a fixed-sign theorem for modes `1..3`.

## 2026-09-12: q286 separable mode coefficient scanner added

`q286_separable_mode_coefficient_receipt` exposes each leading q286 singular
mode as a product coefficient `s_j*A_j(p mod 11)*B_j(p mod 13)`.  This is the
right language for a direct analytic attack: estimate a small family of
separable twisted Goldbach sums rather than an opaque residue table.  It is
still only coefficient-side structure until a signed prime-pair estimate is
proved.

Measured factorization error is `2.8885744504287083e-16`.  All six modes have
mixed residue signs, but not all are balanced.  Mode `1` has sign counts
`60/60` and extrema `+/-851577.2681`; mode `2` has sign counts `84/36` and
extrema `-172835.1666`/`552774.7022`; mode `4` reverses the skew with `36/84`.
Next target: separate balanced-twist cancellation from sign-skewed local bias
inside the six q286 modes.

## 2026-09-12: q286 separable mode local-bias scanner added

`q286_separable_mode_local_bias_receipt` now separates each leading q286 mode
into deterministic local prediction and prime-residue deviation.  This is the
next needed distinction before an analytic estimate: if local bias dominates,
the problem is algebraic/admissibility; if deviation dominates, the problem is
genuine signed prime-pair distribution in the separable twist.

Measured answer: the local means are essentially zero over the first period.
Local admissibility creates oscillatory terms, not a persistent bad local main.
For significant q286 lower tails, modes `1` and `2` are mainly dangerous
through prime-residue deviation, not through local bias: their deviation is
negative on `562/594` and `493/594` significant targets, while their local
terms are negative on `244/594` and `115/594`.

Next target: estimate separable prime-residue deviations directly, while
carrying local oscillatory terms as explicit bounded margin costs.

## 2026-09-12: q286 leading-mode lift-decay scanner added

`q286_leading_mode_lift_decay_receipt` now checks fixed bad residue classes
across later period lifts.  It tracks whether first-two, first-three, and
six-mode q286 contributions shrink in principal-relative units as `N` grows.
Use it to decide whether a threshold-plus-finite-check route is plausible for
the leading separable modes.

Measured answer: the first tested lifts support finite-scale amplification but
not monotone decay.  For bases `10424,12118,14138,14680`, the zero-lift
first-three absolute ratios are `0.9411943888163556`,
`1.0401885969034605`, `0.8950145872346784`, and `0.4282674888747748`; each has
a later sampled lift below `0.076`.  However, across all sampled lifted values,
the maximum first-three ratio is still `0.6777494578790298` and the maximum
six-mode ratio is `0.6782174958798006`.

The six-mode residual remains small in the lift sample, at most
`0.016680413471741894` of principal.  Next target: prove a nonmonotone
principal-relative envelope for leading q286 modes, or find a source theorem
that gives decay after excluding a finite initial range.

## 2026-09-12: significant q286 lift-envelope scanner added

`q286_significant_lift_envelope_receipt` now stress-tests the lift-decay route
across significant first-period q286 lower-tail base targets.  It first
selects bases below the configured principal-relative threshold, then measures
their lifted first-three, six-mode, residual, and full q286 ratios.

Use this to falsify or support threshold-plus-finite-check: persistent large
lifted ratios mean the route needs a stronger analytic input; uniformly small
lifted ratios would motivate a formal envelope theorem plus finite range.

Measured answer on all `594` significant first-period bases: every base has a
sampled positive lift with smaller first-three absolute mode ratio than at lift
zero, but no uniform small lifted envelope follows.  The maximum lifted
first-three ratio is `1.3478240385516096`, maximum lifted six-mode ratio is
`1.378316975940504`, and maximum lifted q286 ratio is `1.3963940029628314`.
The six-mode residual remains small, at most `0.024761483446069824`.

The key falsifier is base `11322`, whose lift `1` turns into a large positive
excursion: q286 `1.3964`, first-three `1.3478`, six-mode `1.3783`.  Therefore
threshold-plus-finite-check cannot rely on simple sampled lift smallness.  The
analytic target is a nonmonotone two-sided principal-relative envelope for the
leading modes.

## 2026-09-12: q286 leading-mode period-envelope scanner added

`q286_leading_mode_period_envelope_receipt` now scans q286 deviation,
first-three leading modes, six leading modes, and six-mode residual by period
cycle in principal-relative units.  Use it to test whether a two-sided
envelope remains bounded or decays across cycles after simple lift-smallness
failed.

Four-cycle sampled result (`2004` targets): the residual stays small, worst
`0.026483963220719737` of principal, but the leading modes themselves can be
large.  Worst q286 magnitude is `1.7498864766477102` and worst six-mode
magnitude is `1.7410021829174136`, both at `N=20414`.

Thus the current analytic target is not to bound the six leading modes by a
small absolute constant.  The target is lower-envelope control after combining
positive principal, exact q154/q70, local terms, six q286 leading modes, and
the small q286 tail.

## 2026-09-12: reduced full lower-envelope scanner added

`reduced_full_lower_envelope_receipt` now measures the actual full assembled
action against the current reduced model: principal, every non-q286 support
exact, q286 local prediction, six q286 singular modes, and q286 tail.  This is
the right finite diagnostic before a formal estimate, because it restores the
small supports rather than leaving the model at the dominant-support layer.

## 2026-09-12: count-four residual has live holdout sectors

The first post-principal-split residual test falsifies an overly small next
hypothesis.  The reviewed quotient-77 principal-plus-shadow channel and the
quotient-91 linked-slice cancellation do not exhaust the count-four source
model.  `count_four_outer_holdout_sector_receipt` connects the new
strict-central bridge to the older six-quotient projected-Fourier/count-four
table and classifies the missing part.

The linked-prime slice uses quotients `(77, 91)`, with lags `(130, 110)`.
The full two-prime count-four table also has live holdout quotients
`(35, 55, 65, 143)`, with lags `(286, 182, 154, 70)`.  Their projected
Fourier cancellation quotients are respectively
`.010906884721340548`, `.024560020667301303`, `.0005487547365190931`, and
`.006101857449924944`; their count-four recombination quotients are
`.16118908808873234`, `.3024507788824479`, `.014327564985042195`, and
`.09820822341044044`.  All are positive in the frozen source table.

Independent review returned PASS.  Faraday checked the imports, noncircularity,
period-10010 quotient-to-lag map, reuse of
`two_prime_projected_fourier_holdout_receipt`, exact fixture values, and the
scope flags.  Focused normal and optimized tests pass.

Status `changed-under-evidence`: the residual is not just endpoint/noncentral
bookkeeping inside the already reviewed q77/q91 linked-prime slice.  At the
count-four source-table level, four additional quotient sectors remain live
and need their own bridge or estimate.  This does not identify the full outer
assembly, prove those holdouts' final contribution, estimate the formal signed
error, prove a pointwise signed prime-correlation bound, or prove Goldbach.
The q77 principal-plus-shadow channel remains a useful component; only the
hypothesis that it leaves merely q77/q91 endpoint cleanup is blocked.

Next concrete question: can one holdout sector, starting with quotient `65`
(lag `154`, the smallest projected cancellation quotient), be converted into a
strict-central prime-pair channel with fixed coefficients the way q77 was, or
does its common modulus/support force a moving coefficient or nonunit boundary?
A useful test is to build the q65 analogue of the direct source/fiber-shadow
comparison and then check whether its strict-central unit threshold and target
residue admissibility give a symbolic coefficient identity or a precise
falsifier.

## 2026-09-12: q65 holdout has a nonzero fiber-shadow candidate

The first holdout-sector probe preserves the q77 lesson without assuming the
same bridge.  For quotient `65`, lag `154`, the full-period direct source on
`U_10010` does not descend pointwise to `U_154`, but it has a large nonzero
centered fiber-shadow candidate after summing the `48` lifts over each of the
`60` unit residues modulo `154`.

The reviewed measurements are: centered fiber `L^2` norm
`86071.18524618556`, centered/total fiber `L^2` ratio
`.9948879642115595`, maximum within-fiber deviation
`28401.117801547734`, and fiber mean approximately
`-1127.8833333333703 - 3.04e-13i`.  The nonzero within-fiber deviation is the
explicit witness that pointwise descent fails.  Since `154=2*7*11`, every even
`N>=34` has strict-central prime pairs above `11`, hence units modulo `154`.

Independent review returned PASS.  Faraday checked the quotient-lag-common
map `10010/gcd(154,10010)=65`, `phi(154)=60`, uniform fiber size `phi(65)=48`,
the numerical fixtures, the pointwise-descent failure, the `N>=34` threshold,
the sign-convention wording, and the false open-scope flags.  Focused normal
and optimized tests pass.

Status `changed-under-evidence`: q65 is a real holdout component with a
q77-like fiber-aggregation object available.  This is not yet a q65
linked-prime or outer-row bridge, not a full outer assembly identification,
not a formal signed-error estimate, not a pointwise signed prime-correlation
bound, and not Goldbach.  The negative centered-fiber sign is only a candidate
convention inherited from q77 until a q65 row bridge fixes the sign.

Next concrete question: construct the q65 analogue of the q77 coefficient-row
comparison.  Does any count-four sector row or character-projection row equal
this q65 fiber shadow, up to centering/sign/constant, on strict-central unit
prime pairs?  Falsifier: no fixed recombined source vector over `U_154`, a
sign/scale mismatch that cannot be explained by centering, or a required
coefficient depending on the target residue `N mod 154`.

## 2026-09-12: q65 active linked-prime row bridge is falsified

The q65 holdout fiber shadow survives as a component, but the first attempted
q77-style row bridge fails.  For quotient `65` / lag `154` / common modulus
`154`, the linked-prime character machinery selects active divisors
`(1, 5, 13, 65)`.  Recombining those active additive source rows over `U_154`
gives an essentially zero centered source vector, not the q65 fiber shadow.

The reviewed measurements are: recombined active source `L^2` norm
`2.0414796274281065e-11`, below the separate floating cancellation tolerance
`1e-10`; q65 fiber-shadow `L^2` norm `86071.18524618556`; same-sign and
opposite-sign shadow match errors both `1.0`; best scalar projection onto the
fiber shadow has magnitude about `2.75e-17`; and the active source vector has
exactly zero spread across targets `1000` and `1002`.  Thus target dependence
is not the failure mode at the source-vector layer.  The failure mode is that
these active rows cancel before reaching the nonzero fiber-shadow object.

Independent review returned PASS.  Faraday checked the imports and absence of
accidental earlier-function changes, the quotient/lag/common map, active
divisors, `U_154` ordering guard, cancellation tolerance, numerical
interpretation, target-spread calculation, and open-scope flags.  Focused
normal and optimized tests pass; compile, diff check, and the broader q65
component/holdout-sector validation pass.

Status `changed-under-evidence`: block only the exact q65 analogue
"active linked-prime divisor rows reproduce the q65 fiber shadow up to
centering/sign/constant."  Preserve the nonzero q65 fiber shadow and the live
q65 count-four sector as useful components.  A different count-four sector row,
projection, or arithmetic estimate is not ruled out.  No full outer assembly,
formal signed-error estimate, pointwise signed prime-correlation bound, or
Goldbach theorem follows.

Next concrete question: inspect the count-four sector decomposition itself for
q65, rather than the linked-prime active rows.  Which sector(s) produce the
lag-154 projected Fourier mass, and does any sector-level additive source over
`U_154` align with the q65 fiber shadow?  Falsifier: all sector-level source
vectors either cancel, live on a different quotient/common-modulus object, or
require target-dependent coefficients.

## 2026-09-12: q65 projected spatial bridge recovers the fiber shadow

The q65 active linked-prime row bridge failed, but that failure identified the
wrong layer rather than killing the q65 component.  The projected-Fourier
spatial source for quotient `65` / lag `154` does recover the q65 fiber shadow.
Compute the signed projected value for each spatial frequency coprime to
`154`, using the same transform formula as `_projected_fourier_total`; then
group the `3900=65*phi(154)` spatial frequencies by residue modulo `154` and
center over `U_154`.  The grouped centered spatial vector equals the negative
of the q65 fiber-shadow vector.

The reviewed measurements are: projected signed total `-67673.0`, absolute
mass about `123321031.2302159`, cancellation quotient
`.0005487547365190931`, grouped centered spatial `L^2` norm
`86071.18524618639`, fiber-shadow `L^2` norm `86071.18524618556`, opposite-sign
relative error about `1.26e-14`, and best scalar approximately
`-1.0000000000000098 - 1.06e-16i`.

Independent review returned PASS.  Faraday checked that the spatial loop
matches `_projected_fourier_total` term-for-term, that grouping by spatial
frequency modulo `154` is correct, that the projected-spatial construction and
direct-source fiber construction are independent, and that the numerical
fixtures/tolerances and open-scope flags are correct.  Focused normal and
optimized tests pass; compile, diff check, and the combined q65/holdout test
set pass.

Status `aha-candidate`, novelty `new-to-this-task`: the q65 holdout sector has
a source identity parallel to q77, but in the projected-Fourier spatial layer
rather than in the active linked-prime row layer.  The active linked-prime row
bridge remains falsified; the projected spatial bridge is a source identity,
not yet a target prime-pair bridge.  No full outer assembly, formal signed
error, pointwise signed prime-correlation estimate, or Goldbach theorem
follows.

Next concrete question: transfer this projected-spatial q65 source identity to
a strict-central prime-pair correlation.  Does grouping spatial frequencies by
`p mod 154` give a fixed weighted Goldbach sum for every even `N>=34`, or is
there an additional transform/duality step before spatial coefficients become
prime-residue coefficients?  Falsifier: a direct target computation disagrees
with the grouped-spatial coefficient vector beyond numerical tolerance, or the
coefficient depends on `N mod 154`.

### 2026-09-12 continuation: q65 needs the Fourier-dual coefficient

The tempting q65 shortcut is now falsified: the grouped spatial vector cannot
be used directly as the prime-residue coefficient by matching residue labels.
The grouped centered spatial vector over `U_154` has `L^2` norm
`86071.18524618639`, while its finite Fourier-dual prime-residue coefficient
has `L^2` norm `751779.5321027868`.  The best scalar fit still has relative
error `.9511342058094504`.

The useful component is the dual route.  On fixture targets `1000` and `1002`,
the Fourier-dual coefficient's strict-central prime-pair sum matches the
spatial-frequency reconstruction with maximum relative error
`1.5578275920406705e-14`, and no nonunit central prime pairs occur.  The
naive target sums differ materially from the dual sums on both fixtures.

Status `changed-under-evidence`: same-index spatial-to-prime transfer is
blocked; Fourier-dual target transfer is live but only fixture-checked.  A
symbolic all-target q65 bridge, full outer assembly, formal signed error,
pointwise signed control, and Goldbach remain open.

### 2026-09-12 continuation: q65 Fourier-dual transfer is symbolic

The q65 dual route now has a symbolic coefficient receipt.  The fixed
strict-central coefficient is the finite additive Fourier dual of the grouped
projected-spatial source over `U_154`, not the same-index spatial vector.  It
is independent of the target residue.  Because strict-central prime pairs for
even `N>=34` have both primes greater than `11`, no nonunit correction enters
this q65 unit channel.

Thus the q65 projected-spatial target action has the fixed form

`sum_(N/3<p<2N/3, p,N-p prime)
   log(p)log(N-p) C_q65(p mod 154)`.

Status `aha-candidate`, novelty `new-to-this-task`: q65 is now a fixed
strict-central coefficient channel in the Fourier-dual basis.  This still
does not prove a signed estimate, identify the full outer assembly, control
the remaining holdout sectors, estimate `T_boundary-Delta`, or prove Goldbach.

### 2026-09-12 continuation: q55 is principal, not centered

The next holdout sector behaves differently.  For q55 / lag `182`, the grouped
projected-spatial values over `U_182` are constant up to floating noise rather
than carrying a nonzero centered shadow.  The constant grouped spatial value is
`-50617.0`; because the unit Ramanujan value for modulus `182` is `-1`, the
induced strict-central prime-residue coefficient is the constant `50617.0`.

The fixture target reconstruction passes within `1e-9` and no nonunit
strict-central prime pairs occur for the tested targets.  Since `182=2*7*13`,
the symbolic unit threshold is `N>=40`.

Status `changed-under-evidence`: q55 is preserved as a fixed principal
strict-central channel, not a q65-like centered channel.  The remaining live
holdouts are q35 and q143; signed control and Goldbach remain open.

### 2026-09-12 continuation: live holdouts are fixed coefficient channels

The q65 target-transfer wording has been corrected: the dual receipt transfers
the centered component, while the full projected-spatial channel is principal
mean plus centered Fourier dual.  A new full-channel receipt now checks q35,
q65, and q143 on fixture targets, with no nonunit central prime pairs and
target reconstruction error below `1e-9`.

The full channel data are:

`q35`: common modulus `286`, principal coefficient `-21442.808333333334`,
centered dual `L^2` norm `2232674.8772659665`.

`q65`: common modulus `154`, principal coefficient `1127.8833333333334`,
centered dual `L^2` norm `751779.5321027868`.

`q143`: common modulus `70`, principal coefficient `13896.875`, centered dual
`L^2` norm `443487.86788549845`.

Together with q55's principal-only channel, the live count-four holdouts have
fixed strict-central coefficient descriptions at the source/channel level.
Status `aha-candidate`, novelty `new-to-this-task`: the residual source
bookkeeping is now a finite explicit coefficient family.  The missing step is
signed prime-correlation control for that family, plus any remaining endpoint
or noncentral terms in the original outer assembly.  Goldbach remains open.

### 2026-09-12 continuation: assembled fixed family on U_10010

The q77 channel and the four live holdout channels have now been lifted to
`U_10010` and assembled as one fixed strict-central prime-residue coefficient
family.  The aggregate principal mean is `44002.512499999146 + 3.18e-10i`,
matching the expected principal sum `44002.5125`.  The lifted centered norms
are `339622.7115252295` for q77, `10937828.421665356` for q35,
approximately zero for q55, `5208481.3827695325` for q65, and
`4858166.184415171` for q143.

The aggregate centered norm is `13056020.079597872`, while the sum of centered
component norms is `21344098.70037529`, giving cancellation ratio
`.6116922650553668`.  This is useful compression but not a signed estimate.

Status `aha-candidate`, novelty `new-to-this-task`: the residual channel
bookkeeping is now one explicit finite coefficient vector on `U_10010`.  The
next analytic problem is to decompose or bound the corresponding signed
strict-central prime-residue correlation.  Endpoint/noncentral reconciliation
and Goldbach remain open.

### 2026-09-12 continuation: character spectrum is broad

The assembled centered coefficient was decomposed into the full character
basis on `U_10010`.  Reconstruction error is `2.86792335453186e-15`, and
Parseval matches at character energy `59187382055.160706`.  The top `12`
characters carry only `.2525547318628327` of the energy, the participation
ratio is `66.02126503332039`, and `110` characters clear the nontrivial
threshold.  The largest individual character carries only about `2.38%`.

Status `changed-under-evidence`: the small dominant-character shortcut is
blocked.  The explicit finite coefficient family remains useful, but the
signed estimate likely needs conductor-support grouping, CRT tensor structure,
or a broad weighted large-sieve argument.  Goldbach remains open.

### 2026-09-12 continuation: pairwise sector cancellation is tiny

Kevin asked whether the `.6116922650553668` aggregate norm ratio represented
true cancellation.  The pairwise normalized Gram says no.  The centered
self-energy total is `170481491158026.06`; the total cross term is
`-21830839163.179787`, only `-.00012805401345852797` of self-energy.  The most
negative normalized off-diagonal real Gram entry is `-.0010025610827496898`,
while the largest positive entry is `.015594243759942`.

Status `changed-under-evidence`: net negative cross term exists, but it is too
small to explain a proof-scale saving.  The `.612` ratio was mostly a
triangle-norm comparison, not substantial cross-channel cancellation.  The
next target remains structural decomposition or direct signed
prime-correlation control.

### 2026-09-12 continuation: q77 action and local mains checked directly

`q77_original_strict_central_action_receipt` now compares the original
quotient-77 linked-prime strict-central row action with the q77 component of
the assembled coefficient.  The residue map is `p mod 10010 -> p mod 130`,
with quotient factor `77`, unit-fiber size `60`, and no ordered-pair factor
`1/2`.  The coefficient-vector error is `2.558560547443785e-14`, the assembled
action error is `1.0853470557705165e-13`, and the comparison to the original
direct-unit action is `9.405451349754832e-13`.

The assembled coefficient's local main was then inspected across all `5005`
even residues modulo `10010`.  Every local main is positive.  The minimum is
at residue `4124`, value `39463390.92458851 + 1.0388056078764754e-06i`; the
maximum is at residue `7140`, value `133823614.44192465 + 8.225108938743084e-07i`.
The mean real local main is `72921965.97002855`, so the minimum-to-mean ratio
is `.5411728880267469`.

Status `changed-under-evidence`: q77 factor/map bookkeeping is now tied back
to the original strict-central action, and the assembled coefficient has no
local-main sign obstruction.  The remaining target is a pointwise signed
prime-correlation estimate against this positive main, plus endpoint and
noncentral reconciliation.  Goldbach remains open.

### 2026-09-12 continuation: direct assembled prime sums have small-cycle negatives

`combined_coefficient_prime_correlation_diagnostic_receipt` directly computes
the assembled coefficient on actual ordered strict-central prime pairs and
normalizes by `N * local_main(N mod 10010)/(3*phi(10010))`, with no
singular-series factor inserted.  On the first complete even-residue cycle
`10000 <= N <= 20008`, it covers all `5005` residue classes and finds `75`
negative weighted sums.  The worst real sum is at `N=14138`, value
`-226233724.4857778 + 8.264519577794347e-06i`; the worst normalized
multiplier is at `N=10424`, value `-2.470255524753131`.

The twelve worst normalized residues were checked at period lifts
`1,2,5,10,20,50`.  Each was negative in the first cycle and positive at the
sampled higher lifts, so the finite diagnostic does not falsify an eventual
asymptotic estimate, but it does prove that positive local mains alone are not
enough.

Status `changed-under-evidence`: the signed prime-correlation estimate is now
the active bottleneck in a concrete form.  A successful route must either give
an explicit threshold with finite verification below it, or prove a direct
uniform pointwise bound for the normalized moving error against the weakest
positive local-main margin.  Endpoint/noncentral reconciliation and Goldbach
remain open.

### 2026-09-12 continuation: holdout original-action audits

`holdout_original_projected_action_audit_receipt` independently recomputes the
original projected count-four spatial actions for q35, q55, q65, and q143, and
compares them to the assembled component coefficient actions.  The audit
passes with maximum action relative error `2.3027261888604984e-13`.

Per sector: q35 has coefficient-vector/action errors
`4.673050255673673e-14` and `2.3027261888604984e-13`; q55 has
`2.3717099635538043e-13` and `3.0598780471187056e-14`; q65 has
`1.8920317816138494e-15` and `5.3211501061131093e-14`; q143 has
`6.710683956519706e-15` and `1.5392616872595559e-13`.

Status `verified-bookkeeping`: all five assembled sectors now have direct
source/action audits in the strict-central fixture layer.  This strengthens
the coefficient bridge but does not close endpoint/noncentral terms or the
pointwise signed prime-correlation estimate.

### 2026-09-12 continuation: first-cycle negatives clear sampled lifts

The default `combined_coefficient_negative_residue_lift_receipt` tested every
one of the `75` first-cycle negative residue classes at additional period lifts
`(0, 1, 4, 9, 19, 49)`.  None stayed negative at any tested positive lift.
The weakest lifted normalized multiplier is `0.3807824713878283` at target
`20674`.

Status `aha-candidate`: sampled evidence now favors a threshold-plus-finite
check route over a persistent negative-residue obstruction.  The required
mathematical step remains a uniform pointwise lower bound, or an explicit
threshold theorem plus finite verification below it.

### 2026-09-12 continuation: period-cycle envelope has later finite recurrence

`combined_coefficient_period_cycle_envelope_receipt` scanned the first `12`
complete even-residue cycles from `10000` through `130118`.  Negative direct
assembled prime-correlation counts by cycle are
`75, 3, 5, 4, 0, 0, 0, 2, 0, 0, 0, 0`.  The global worst remains
`N=10424`, normalized multiplier `-2.470255524753131`.  The later recurrence
is in cycle `7`, where targets `85496` and `88346` are negative and the worst
normalized multiplier is `-0.42157916666493706`.

Testing the two cycle-7 negative residues at additional period lifts
`(0, 1, 4, 9, 19, 49)` found no persistent lifted negatives; the weakest
lifted normalized multiplier is `1.735447134625385` at `278536`.

Status `changed-under-evidence`: there is no monotone threshold at `50040`,
but sampled negative recurrences still clear at higher residue lifts.  Continue
with a farther threshold search or a residue-wise lower-envelope argument.

### 2026-09-12 continuation: full residue uniformity margin is unrealistic here

`combined_coefficient_uniform_residue_margin_receipt` computes a sufficient
condition for positivity from full residue-class uniformity modulo `10010`.
The minimum sufficient relative-discrepancy margin is
`0.20799157662677328` at residue `6866`; the maximum is
`0.5502078345733764`; the mean is `0.30832888056671387`.

On `10000 <= N <= 20008`, zero of `5005` targets satisfy that strong
condition.  The worst discrepancy-to-margin ratio is `118.38461370559743` at
`N=10366`.  This does not disprove positivity; it shows that a proof via full
mod-`10010` residue equidistribution is much too expensive at the current
finite scales.

Status `changed-under-evidence`: use CRT/conductor support or lower-dimensional
structure before asking for full unit-residue uniformity.  The direct
pointwise estimate remains open.

### 2026-09-12 continuation: support components descend to lower moduli

`combined_coefficient_support_descent_receipt` reconstructs the assembled
centered coefficient by CRT character-support components and verifies actual
descent to lower natural moduli.  Reconstruction error is
`2.8141365849948198e-15`; maximum support-descent relative error is
`5.591563085286316e-18`.

The nonzero lower moduli are `10, 14, 22, 26, 70, 130, 154, 286`.  Most energy
lives on three two-prime supports: `(11,13)`/modulus `286` carries
`.70082890257693`, `(7,11)`/modulus `154` carries `.15893232135172436`, and
`(5,7)`/modulus `70` carries `.13627165529397434`.

Status `aha-candidate`: the coefficient is broad across individual
characters, but it is not full-dimensional in CRT support.  Replace the
unrealistic full mod-`10010` uniformity route with lower-modulus component
estimates, primarily for moduli `286`, `154`, and `70`.

### 2026-09-12 continuation: bad targets decompose by support

`combined_coefficient_support_contribution_receipt` decomposes bad direct
targets by CRT support components.  For targets `10424`, `14138`, and `88346`,
support reconstruction error is at most `8.53529361294973e-15`.

The largest negative support at all three targets is `(11,13)`/modulus `286`.
The negative sums come from the positive principal component being overwhelmed
by the dominant two-prime supports `(11,13)`/`286`, `(5,7)`/`70`, and
`(7,11)`/`154`.

Status `aha-candidate`: focus the direct estimate on the modulus-`286`
component and its joint behavior with moduli `70` and `154`.  The small
single-support corrections are secondary.

### 2026-09-12 continuation: centered-error lower-tail target

`combined_coefficient_centered_error_envelope_receipt` writes the direct
assembled strict-central prime-pair sum as
`principal_mean * W_unit(N) + centered_error(N)`, with principal mean
`44002.512499999146 + 3.18e-10i`.  Positivity is therefore reduced to the
explicit lower-tail condition
`centered_error(N).real / principal(N).real > -1`.

Across the first `12` complete even-residue cycles, the global worst ratio is
`-1.876941273440844` at `N=14138`.  Negative-or-zero counts by cycle remain
`75, 3, 5, 4, 0, 0, 0, 2, 0, 0, 0, 0`.  Even positive cycles can be close to
the threshold: cycle `4` has minimum `-0.9975041993462069` at `N=58736`.

Status `changed-under-evidence`: the explicit pointwise task is now a lower
tail bound for the centered lower-modulus support correlations against the
positive principal contribution.  Local-main positivity and average behavior
remain insufficient.

### 2026-09-12 continuation: support-cycle lower-tail drivers

`combined_coefficient_support_cycle_envelope_receipt` measures support
components as ratios to the positive principal contribution across full
period cycles.  Over the first `12` cycles, the global centered minimum is
still `N=14138`, centered/principal ratio `-1.8769412734408446`, and the
dominant negative support at that target is `(11,13)`/modulus `286`.

Global support minima: `(11,13)`/`286` reaches `-1.0602630156038382` at
`N=10664`; `(5,7)`/`70` reaches `-0.8740313946216749` at `N=14732`;
`(7,11)`/`154` reaches `-0.7887852463184297` at `N=10814`.  All smaller
single/support terms bottom above `-0.108` in the scan.

Status `changed-under-evidence`: prioritize the modulus-`286` lower-tail
estimate and its reinforcement with moduli `70` and `154`; do not spend the
next analytic attempt on the tiny single-support terms.

### 2026-09-12 continuation: q286 bad targets are discrepancy-driven

`combined_coefficient_lower_modulus_deviation_receipt` compares actual
support contributions to lower-modulus local predictions on bad targets
`10424`, `14138`, and `88346`.  For the dominant `(11,13)`/`286` support, the
local prediction is positive on all three targets, but the actual contribution
is negative.  The q286 deviation-to-principal ratios are `-0.970542065173128`,
`-0.8666741397111133`, and `-0.7731555354500473`.

The q286 prime residues are still sparse but improving across those targets:
`57/99`, `59/99`, and `95/99` admissible residues receive prime-pair weight;
maximum residue weight to mean drops from `4.36663181730314` to
`2.1264906126189658`.

Status `changed-under-evidence`: q286 is not failing because its local main
has the wrong sign.  It is a genuine lower-modulus prime-residue discrepancy
problem.  q70 and q154 can add secondary local-sign bias, but q286 is the main
first target.

### 2026-09-12 continuation: reduced full lower-envelope model

`reduced_full_lower_envelope_receipt` puts the current decomposition back
against the full assembled coefficient action.  It keeps every non-q286
support exact, splits q286 into local prediction plus six leading singular
modes plus q286 tail, and measures the full action, reduced model, small
support contribution, and q286 tail in principal-relative units.

On the first `501` even targets from `10000`, the full action and reduced
model have the same `16` negative targets.  The worst target is `N=10424`,
with full-action/principal ratio `-0.6387603808369553` and reduced-model ratio
`-0.6300258931770139`.  The maximum q286 tail ratio is
`0.02648396322072016` at `N=10042`; reconstruction error is about
`1.73e-13`.

On the complete first even-residue period `10000..20008`, the exact full
action has `75` negative targets while the reduced model has `77`.  The worst
target agrees: `N=14138`, with full-action/principal ratio
`-0.8769412734408442` and reduced-model ratio `-0.8769793860120647`.  The
maximum q286 tail ratio is `0.033888231610242195` at `N=13826`, and the
maximum reconstruction error is about `8.82e-13`.

Status `aha-candidate`: the proof-shaped finite target has narrowed to
principal plus exact non-q286 support channels plus q286 local and six
separable q286 modes, with a measured q286 tail below `0.034` principal on
the first full residue period.  The reduced model is not sign-identical to the
full action, and no asymptotic bound, endpoint/noncentral reconciliation, or
Goldbach proof follows.

### 2026-09-12 continuation: reduced lower-envelope cycle scan

`reduced_full_lower_envelope_cycle_scan_receipt` repeats the reduced/full
comparison over consecutive `10010`-period windows.  Default scan: four
windows of `501` even targets each, covering `10000..11000`, `20010..21010`,
`30020..31020`, and `40030..41030`.  The reduced model and exact full action
agree in sign on all `2004` sampled targets, and every full negative is
captured by the reduced model.  Total negative counts are `19` for both.

Cycle summaries: cycle `0` has `16` negatives and minimum full-action ratio
`-0.6387603808369553` at `N=10424`; cycle `1` has no negatives and minimum
`0.05648283359949622` at `N=20908`; cycle `2` has `2` negatives and minimum
`-0.057467693572052184` at `N=30164`; cycle `3` has `1` negative and minimum
`-0.04529074309387505` at `N=40676`.  The worst q286 tail remains cycle `0`,
`0.02648396322072016` principal at `N=10042`, with maximum reconstruction
error about `1.73e-13`.

Status `aha-candidate`: the reduced model is a good finite lower-envelope
proxy in this four-window sample.  The next direct estimate should target the
six separable q286 prime-residue mode sums inside this reduced model, allowing
exact q70/q154 support reinforcement and a small explicit q286-tail allowance.
This is still finite evidence, not an eventual threshold theorem.

### 2026-09-12 continuation: reduced-envelope mode signatures

The q286 six-mode decomposition was inspected on the main bad targets
`10424`, `14138`, the later reduced/full negatives `30164`, `40676`, and the
two full-period reduced-model-only negatives `11194`, `15272`.

The first-cycle worst targets remain mode-1 dominated.  The later shallow
negatives are still mostly a modes-1/2 phenomenon but not a fixed-sign
theorem.  At `30164`, mode `2` is slightly larger than mode `1`; at `40676`,
mode `1` leads but modes `1` and `2` together carry almost all negative mass.
The reduced-model-only boundary target `11194` has positive mode `1` but
large negative mode `2`, while `15272` is tail-rescued by a positive q286
residual of `0.018953225776954182` principal.

Status `changed-under-evidence`: do not try to prove a one-mode or fixed-sign
lemma.  The direct estimate must control a target-dependent signed envelope
for at least the first two q286 separable modes, with modes `3..6` and the
small tail paid in the margin.

### 2026-09-12 continuation: first-two q286 modes isolate sampled negatives

`q286_first_two_mode_lower_tail_receipt` measures whether the first two
separable q286 singular modes alone account for the reduced lower-tail
obstruction.  Default scan: four `501`-target windows covering the same ranges
as the reduced-envelope cycle scanner.  All `19` negative full-action targets
have negative first-two q286 mode sum.  The first-two negative contribution is
at least `1.36990224676328` times the full negative deficit on those targets.
Removing modes `1` and `2` leaves a positive lower envelope on the sampled set:
the worst full action without those modes is `0.09048725420345835` principal at
`N=10354`; the worst reduced action without those modes is
`0.08579199551280053` there.  The most negative first-two mode sum is
`-1.1124437977839818` principal at `N=10664`.

Status `aha-candidate`: in this sample, the actual negative assembled
strict-central channel is entirely created by the first two q286 separable
modes; all exact non-q286 supports, q286 local term, modes `3..6`, and tail
leave a positive margin once modes `1` and `2` are removed.  This strongly
focuses the next analytic target, but it is still finite sampled evidence.
It does not prove an eventual lower envelope, endpoint/noncentral terms, the
signed prime-correlation estimate, or Goldbach.

Full first-period scan: on all `5005` targets in `10000..20008`, all `75`
negative full-action targets have negative first-two and first-three q286 mode
sums.  Removing modes `1` and `2` leaves only one nonpositive target,
`N=14138`, with remaining full-action ratio `-0.007038026892741689`.
Removing modes `1`, `2`, and `3` leaves no nonpositive target; the worst
remaining full-action ratio is `0.018073313793834367`, again at `N=14138`.
The minimum first-two capture on negative targets is `0.9919743463947972`;
the minimum first-three capture is `1.02060949158308`.

Status update `aha-candidate`: the first full residue period says modes
`1..3`, not just `1..2`, are the finite lower-tail core.  A prospective proof
can try to bound the combined first-three q286 separable mode sum from below,
then pay q286 local, modes `4..6`, exact non-q286 supports, and the q286 tail
as a residual positive-margin problem.  This remains a finite diagnostic.

### 2026-09-12 continuation: leading q286 modes are broad character mixtures

`q286_leading_mode_character_shape_receipt` checks whether the first three
q286 singular modes are sparse enough in multiplicative-character space that a
single-character estimate might suffice.  They are not sparse on either side.
For modes `1`, `2`, and `3`, the mod-`11` effective character counts are
`4.899124389855417`, `3.994990282499014`, and `4.787886564984907`; the
mod-`13` effective counts are `5.8587969819448205`, `4.9888048746106834`, and
`5.526188486527063`.  The largest side energy fraction across all six sides is
only `.2588529653280147`.

Status `changed-under-evidence`: reject a sparse single-character shortcut.
The first-three lower-tail estimate must handle a broad but finite mixture of
small-conductor twisted Goldbach sums modulo `11` and `13`.

The theorem-shaped target is written in
`notes/q286-first-three-twisted-estimate.md`.  It formulates the first-three
mode contribution as a finite mixture of fixed-modulus one-sided twisted
binary-prime correlations and records why this is the signed prime-correlation
step rather than a solved bookkeeping issue.  The next falsifier is to test
first-three removal on more complete period cycles and same-residue lifts.

Two complete-period falsifier: `q286_first_two_mode_lower_tail_receipt` with
`cycle_count=2, targets_per_cycle=5005` tests `10010` targets in
`10000..30018`.  The exact full action has `78` negative targets.  All `78`
have negative first-two and first-three q286 mode sums.  Removing modes `1`
and `2` leaves only one nonpositive target, still `14138`; removing modes
`1..3` leaves zero nonpositive targets.  The worst first-three-removed margin
is unchanged from cycle `0`: `0.018073313793834367` principal at `14138`.
Cycle `1` has only `3` negatives, all captured by first-three modes, with
minimum first-three capture `28.192546577633923` times the full deficit.

Status `aha-candidate`: the first-three lower-tail core survives the next
complete period.  The evidence still remains finite; the next risk is not
cycle `1`, but later recurrence or a missing endpoint/noncentral term.

Four complete-period falsifier: with `cycle_count=4, targets_per_cycle=5005`,
the scan tests `20020` targets in `10000..50038`.  The exact full action has
`87` negative targets.  All `87` have negative first-two and first-three q286
mode sums.  Removing modes `1` and `2` again leaves only `N=14138`
nonpositive; removing modes `1..3` leaves zero nonpositive targets.  The
worst first-three-removed margin is still `0.018073313793834367` principal at
`14138`.  Negative counts by complete period are `75,3,5,4`; minimum
first-three capture ratios on negative targets are
`1.02060949158308, 28.192546577633923, 3.47131599019328,
3.480217094913758`.

Status update `aha-candidate`: the first-three q286 lower-tail core survives
the first four complete periods, including later recurrence cycles.  This
strengthens the direct target but remains finite evidence only.

Eight complete-period recurrence falsifier: with
`cycle_count=8, targets_per_cycle=5005`, the scan tests `40040` targets in
`10000..90148`, including the previously observed cycle-7 recurrence.  The
exact full action has `89` negative targets.  All `89` have negative
first-two and first-three q286 mode sums.  Removing modes `1` and `2` again
leaves only `N=14138` nonpositive; removing modes `1..3` leaves zero
nonpositive targets.  The worst first-three-removed margin is still
`0.018073313793834367` principal at `14138`.  Negative counts by complete
period are `75,3,5,4,0,0,0,2`; cycle `7` has two negatives and minimum
first-three capture `6.157687584867484`.

Status update `aha-candidate`: the first-three q286 lower-tail core survives
the known later recurrence cycle.  This strengthens the finite threshold
route, but it is not an asymptotic theorem.

`reduced_full_lower_envelope_receipt` and
`q286_first_two_mode_lower_tail_receipt` now also accept explicit
`selected_targets`, so sparse same-residue lift checks do not require scanning
the full interval between them.

Selected lift falsifier: bases `10424,14138,85496,88346,10664` were tested at
lifts `(0,1,4,9,19,49)`, for `30` selected targets.  The exact full action is
negative at five selected targets: `10424`, `10664`, `14138`, `85496`, and
`88346`.  All five have negative first-two and first-three q286 mode sums.
Removing modes `1..3` leaves no nonpositive selected target.  The weak finite
margin remains the original `N=14138` case, not a later lift.

Status `aha-candidate`: same-residue lifts of the sampled hard bases do not
falsify the first-three core.  This still does not prove an eventual threshold
or the signed estimate.

Lift-ratio detail: the first-three q286 mode sum does not monotonically decay
on the selected lifts; it remains a large two-sided oscillatory term.  For
base `10424`, first-three ratios over lifts `(0,1,4,9,19,49)` are
`-0.941194, 0.168907, 0.677749, -0.367466, -0.261887, -0.023974`; for
`14138`, `-0.895015, -0.120827, -0.015748, 0.010948, -0.057286, 0.178011`;
for `85496`, `-0.725207, 0.066675, 0.048974, 0.024041, -0.105822,
-0.062692`; for `88346`, `-0.796959, 0.183091, 0.507478, -0.062886,
-0.195348, 0.093594`; and for `10664`, `-1.150088, -0.306513, -0.148512,
-0.140603, -0.295436, 0.06831`.

Status `changed-under-evidence`: reject monotone decay of the first-three
modes as a proof route.  Preserve the stronger useful pattern that the
residual action after removing these modes stays positive on the selected
lifts.

### 2026-09-12 continuation: q286 first-three AP-discrepancy proxy

`q286_first_three_ap_discrepancy_proxy_receipt` compares the first-three q286
mode action with ordinary residue-discrepancy envelopes modulo `286`: a
uniform `L^1` envelope, a Cauchy `L^2` envelope, and actual L2 alignment.

On the complete first period `10000..20008`, the first-three q286 mode sum is
negative at `2525/5005` targets.  The worst lower tail is `10664`, with
first-three/principal ratio `-1.1500880008976306`.  The largest required
uniform relative error over negative first-three targets is
`.5281735902332463`, again at `10664`; over all targets the largest two-sided
value is `.7408970850830631` at `10724`, where the first-three mode is
positive.  The largest L2 alignment over negative first-three targets is only
`.26921675478661156`, at `14892`.

Status `changed-under-evidence`: ordinary AP discrepancy is not a sufficient
black-box explanation.  The Cauchy L2 envelope is loose on the lower tail, and
a proof needs coefficient-sensitive binary correlation structure, not just
full residue-class equidistribution.

`q286_first_three_full_negative_driver_receipt` then restricts the AP-proxy
diagnostic to exact full-action negative targets.  On the first full period
there are `75` exact negatives.  Among their top eight negative residue
drivers, residue `133` appears in `60` cases and is empty in all `60`; residue
`153` appears in `61` cases and is empty in `59`.  Both residues appear in
`46` cases, and both are empty in `44`.  The top eight residue terms carry
absolute real contribution fraction between `.44127253691663915` and
`.639566987107544`, with mean `.5145044943315689`.

Status `aha-candidate`: missing high-positive first-three q286 coefficient
residues, especially `133` and `153`, often drive the exact lower-tail
failures.  This gives a sharper residue-hitting subproblem, but it does not
explain all negatives and cannot replace the broader twisted-correlation
estimate.

The enhanced receipt separates local admissibility from genuine empty
admissible classes.  Among the `75` exact negatives, residue `133` is
admissible `68` times, empty in `60`, positive in `8`, and inadmissible in
`7`; residue `153` is admissible `70` times, empty in `59`, positive in `11`,
and inadmissible in `5`.  Both residues are admissible in `63` exact negative
targets and both are admissible-empty in `44`.

Status update `aha-candidate`: the sharper subproblem is not just local
admissibility; many lower-tail failures have locally available high-positive
residue classes with no strict-central prime pair at the tested scale.

`q286_driver_residue_lift_occupancy_receipt` follows the exact first-period
negative base targets through period lifts `(0,1,4,9,19,49)`.  Default run:
`75` bases and `450` lifted targets.  At lift `0`, all `75` bases are
negative; both driver residues are admissible in `63` cases, both
admissible-empty in `44`, at least one driver is positive in `19`, and both
are positive in `0`.  At lift `1`, no lifted target is negative, and both
driver residues are admissible-empty in only `6`.  At lift `4`, both-empty
disappears.

Status `aha-candidate`: sampled lifts support a finite threshold route where
high-positive driver residues fill quickly.  But driver-residue hitting is not
equivalent to positivity, because lift `1` has six positive targets with both
driver residues still admissible-empty.

### 2026-09-12 continuation: boundary complement support split

`q286_boundary_complement_support_split_receipt` splits `full -
first_three_q286` into principal and lower-modulus support components at the
boundary target `14138` and its lift `24148`.  The split reconstructs the
complement with error below `7e-16` in principal-relative arithmetic.

At `14138`, the complement is tiny, `0.018073313793834367`, because principal
`1.0` is almost cancelled by q70 `-0.6530100068358881`, q154
`-0.43137904901734725`, and non-q286 support sum `-1.0148150611594444`, while
q286 actual after first three contributes only `0.032888374953279564`.
At `24148`, q286 after first three is not the rescue mechanism: q286 deviation
after first three is `-0.00043955321337479925`, but q70 is positive
`0.35469923238633455` and the full complement is `1.3776028000182077`.

Validation: bytecode-disabled `py_compile` passed; focused regression
`test_q286_boundary_complement_support_split` passed in `153.125s`.

Status `aha-candidate`: the complement lower envelope is a joint lower-modulus
support problem, not a q286-only residual problem.  The next direct theorem
attempt should keep q70/q154/q286 support terms explicit after separating the
first-three q286 tail.

### 2026-09-12 continuation: first-three-removed support envelope scan

The post-first-three complement is now scanned by lower-modulus support.
`q286_first_three_removed_support_envelope_receipt` keeps principal, q70,
q154, q286-after-first-three, and smaller support terms explicit.

The four-window sample (`2004` targets) and complete first-period scan (`5005`
targets) both have zero nonpositive complement values after removing the first
three q286 modes.  The first-period minimum is still the boundary target
`14138`, with complement `0.018073313793834256`.

A one-support simplification was falsified: removing q70 gives a negative
value at `10814`, `-0.011932443115723584`, because q70 contributes a positive
`0.19011513241126482` there.  But q70 is strongly negative at other near-floor
targets, including `14138` (`-0.6530100068358884`) and `14732`
(`-0.874031394621675`).

Status `changed-under-evidence`: the lower-envelope theorem must be joint and
signed.  q70 is required in the support mixture, but no single lower-modulus
support has a fixed rescue sign.

### 2026-09-12 continuation: support Gram after first-three removal

A first-period normalized Gram/correlation check over all `5005` targets shows
that, after removing q286 modes `1..3`, q70 and q154 are nearly orthogonal as
centered moving vectors (`0.045469`).  They are not irrelevant: each strongly
feeds the non-q286 support sum (`0.707980` and `0.700826`), and that non-q286
sum almost completely tracks centered complement motion (`0.975731`).

Status `changed-under-evidence`: pursue a vector/norm lower-envelope estimate
for principal plus combined lower-modulus supports.  Do not collapse the next
step into a fixed-sign q70, q154, or q286 lemma.

### 2026-09-12 continuation: support Gram receipt codified

The post-first-three support Gram diagnostic is now executable as
`q286_first_three_removed_support_gram_receipt`.  Its full first-period run
confirms q70/q154 centered correlation `0.045468960787398205` and
non_q286/complement centered correlation `0.9757310575760174`, with zero
nonpositive complement targets and minimum complement
`0.018073313793834256` at `14138`.

Status `changed-under-evidence`: the immediate target is a vector/norm lower
envelope for the explicit support components, not an informal Gram observation
or a one-support sign claim.

### 2026-09-12 continuation: vector-stress receipt falsifies norm-only certificate

`q286_first_three_removed_vector_stress_receipt` now measures whether the
post-first-three complement follows from a norm-only support-vector envelope.
On the complete first period, the observed minimum complement is positive
`0.018073313793834145` at `14138`, but all tested norm-only lower bounds are
negative: box `-1.043941894780164`, rms-only `-18.352119644096938`, and
finite max-norm `-0.7399426654787107`.

The aggregate cross-term total is slightly positive, not substantially
negative: normalized cross-term total `0.0370866441142947`.  Thus the support
Gram helps diagnose geometry, but it does not itself prove cancellation.  The
remaining lower-envelope estimate must control pointwise arithmetic alignment
of q286-after-first-three, q70, q154, and smaller supports.

Status `changed-under-evidence`: reject the norm-only route; attack the
pointwise signed support-vector alignment directly.

### 2026-09-12 continuation: low-tail inventory for pointwise alignment

Sorting the first-period targets by post-first-three complement gives a thin
floor: `1` target below `0.05`, `5` below `0.10`, `16` below `0.20`, and `50`
below `0.30`.  The bottom five are `14138`, `14732`, `12578`, `12944`, and
`16388`.

Status `aha-candidate`: low-tail cases are mostly joint q70/q154 negative
alignment with smaller q286-after-first-three influence.  Try a pointwise
joint-deficit estimate rather than a norm-only or one-support sign route.

### 2026-09-12 continuation: low-tail period lifts clear by lift one

`q286_first_three_removed_low_tail_lift_receipt` tests the first-period bottom
five post-first-three complement bases through lifts `0,1,4,9,19,49`.  All
`30` lifted targets are positive.  The only values below `.3` are the five
lift-0 bases, and every base first clears `.3` at lift `1`.

Status `aha-candidate`: the measured low-tail alignment is not persistent
under these same-residue period lifts.  Next theorem shape: separate finite
onset/boundary treatment from an eventual pointwise alignment-clearance
estimate.

### 2026-09-12 continuation: all first-period `.3` low-tail bases clear by lift one

`q286_first_three_removed_low_tail_auto_lift_receipt` selects every first-
period base with post-first-three complement below `.3`.  It found `50` bases.
Across lifts `0,1,2,3`, all `200` lifted targets are positive; all `50` below-
threshold values are at lift `0`; every selected base first clears `.3` at
lift `1`.

Status `aha-candidate`: the low-tail alignment looks like a first-period/onset
phenomenon across the whole `.3` low-tail set, not just the bottom five.

### 2026-09-12 continuation: four-period `.3` low-tail lift recurrence check

Complete periods starting `10000`, `20010`, `30020`, and `40030` were scanned
for post-first-three complement below `.3`; selected base counts were
`50,4,4,6`.  In all four periods, all selected bases cleared the `.3`
threshold at lift `1`.

Status `aha-candidate`: the checked same-residue low-tail obstruction does not
persist through lift `1`; wider scans should use a dedicated multi-period
scanner rather than repeated one-period wrappers.

### 2026-09-12 continuation: multi-period low-tail lift receipt

`q286_first_three_removed_low_tail_multi_period_receipt` now codifies the
four-period `.3` low-tail recurrence check.  It scanned `20020` base targets,
selected `64` low-tail bases with per-cycle counts `{0: 50, 1: 4, 2: 4, 3: 6}`,
and found below-threshold counts `{0: 64, 1: 0}` over lifts `0,1`.  Every
selected base cleared at lift `1`.

Status `aha-candidate`: recurrence evidence is now reusable and executable;
no eventual theorem is proved.

### 2026-09-12 continuation: eight-period `.3` low-tail recurrence check

`q286_first_three_removed_low_tail_multi_period_receipt` scanned the first
eight complete periods (`40040` targets), selected `64` bases below `.3`, and
found selected counts `{0: 50, 1: 4, 2: 4, 3: 6, 4: 0, 5: 0, 6: 0, 7: 0}`.
All selected bases cleared `.3` at lift `1`; below-threshold counts by lift
were `{0: 64, 1: 0}`.

Status `aha-candidate`: the measured `.3` low tail is now confined to the
first four periods of the checked eight-period window and clears immediately
under same-residue lift.  No eventual theorem is proved.

### 2026-09-12 continuation: complement threshold-horizon receipt

`q286_first_three_removed_complement_threshold_horizon_receipt` now gives an
executable threshold horizon for post-first-three complement minima.  On the
first eight complete periods, `.3` is below threshold only in cycles `0..3`
and first clears at cycle `4`; `.4` first clears at cycle `6`; `.5` does not
clear in the checked window.  The global minimum remains `14138` at
`0.018073313793834367`, with zero complement nonpositive targets.

Status `changed-under-evidence`: use this as the finite onset threshold target
for any eventual complement-floor theorem; no asymptotic theorem is proved.

### 2026-09-12 continuation: later-block threshold horizon falsifies monotone `.4` clearance

A later threshold-horizon run over global cycles `8..15` found zero full-action
negatives and zero complement nonpositive cases, with minimum
`0.37335759682269043` at `154426`.  Threshold `.3` remains clear, but `.4`
reappears below threshold in global cycles `8,9,14,15`; `.45` and `.5` are
below in all checked cycles of this block.

Status `changed-under-evidence`: `.3` is the currently robust checked horizon;
`.4` monotone/permanent clearance is falsified by recurrence.

### 2026-09-12 continuation: first-three tail threshold horizon

`q286_first_three_tail_threshold_horizon_receipt` now checks the negative
first-three q286 tail against thresholds.  Over the first eight complete
periods, first-three is below `-.3` at `4406` targets and below `-.5` at
`1143` targets, with hits in every cycle.  The global minimum is
`-1.1500880008976306` at `10664`.

Status `changed-under-evidence`: the `.3` complement floor cannot be paired
with an independent uniform `first_three >= -.3` theorem.  The next target is a
pointwise co-occurrence estimate: large negative first-three tail must force or
coincide with large enough complement, apart from finite boundary exceptions.

### 2026-09-12 continuation: first-three/complement co-occurrence receipt

`q286_first_three_complement_cooccurrence_receipt` now bins targets by negative
first-three q286 tail and measures complement rescue.  Over eight complete
periods, first_three `< -.3` has `4406` targets with `4320` rescued and `86`
full negatives; `< -.5` has `1143` with `1071` rescued and `72` full
negatives; `< -.75` has `173` with `137` rescued and `36` full negatives; `<
-1.0` has `5` with `3` rescued and `2` full negatives.  Centered
first_three/complement correlation is `-0.04967965232137842`.

Status `changed-under-evidence`: the next target is not independent envelopes
or a linear compensation law.  It is classification/control of the non-rescued
minority inside large negative first-three tail bins.

### 2026-09-12 continuation: non-rescued first-three tail classification

`q286_nonrescued_first_three_tail_classification_receipt` now separates the
non-rescued minority where `first_three < -.3` and full action is nonpositive.
In the first eight complete periods, the `.3` first-three tail has `4406`
targets, with `4320` rescued and `86` non-rescued.  The non-rescued cycle
counts are `{0: 72, 1: 3, 2: 5, 3: 4, 4: 0, 5: 0, 6: 0, 7: 2}`; severity
counts are `72` below `-.5`, `36` below `-.75`, and `2` below `-1.0`.

The `86` non-rescued targets occupy `86` distinct residues modulo the q286
period, so repeated residue persistence is not the finite explanation.  Same-
residue lifts at offsets `0,1` give negative counts `{0: 86, 1: 0}`; all
checked non-rescued targets clear by first positive lift `1`.

Status `aha-candidate`: the promising theorem shape is now boundary/onset
clearance for the non-rescued minority plus a complement-rescue estimate for
the broad first-three tail.  This preserves the earlier Goldbach objective but
does not prove Goldbach, RH, or any prize-level result.

### 2026-09-12 continuation: sampled later-cycle non-rescue falsifier

Individual later-cycle falsifiers at global cycles `16`, `24`, and `32` found
zero full-action negatives and zero non-rescued `.3` first-three tail targets.
The respective minimum full-action ratios were `0.24084360363205248`,
`0.2360810314099344`, and `0.38731649100422866`; `.3` tail counts were `98`,
`24`, and `11`.

Status `aha-candidate`: this supports but does not prove the boundary/onset
clearance route.  Intervening-cycle scans or an analytic cycle-parameter lower
bound remain required.

### 2026-09-12 continuation: continuous later-cycle clearance through cycle 32

Intervening cycles `17..23` and `25..31` were checked one at a time.  Each had
zero full-action negatives and zero non-rescued `.3` first-three tail targets.
Together with prior checks for cycles `8..16`, `24`, and `32`, this gives
continuous measured clearance for global cycles `8..32`.  The smallest newly
checked minimum is cycle `18`, value `0.17360050532072466` at `N=194384`.

Status `changed-under-evidence`: the current onset-clearance target is now
specific: explain why non-rescued targets appear in cycles `0..7` but vanish
in the checked cycle range `8..32`, or find the first recurrence with a
progress-visible scan.  This is finite evidence only.

### 2026-09-12 continuation: cycles 33 through 40 preserve onset-clearance

Cycles `33..40` were checked one at a time.  Each had zero full-action
negatives and zero non-rescued `.3` first-three tail targets.  The `.3` tail
still appears, with counts `6,9,10,9,12,4,2,6`, so the sharper target is
eventual complement rescue of the remaining `.3` tail rather than eventual
absence of that tail.

Status `aha-candidate`: onset-clearance survived the first post-32 recurrence
sweep; finite evidence only.

### 2026-09-12 continuation: non-rescued cycle-horizon receipt

`q286_nonrescued_first_three_tail_cycle_horizon_receipt` now codifies the
onset-clearance horizon.  The focused regression checks the transition
boundary from global cycle `7` (`2` non-rescued `.3` tail targets) to global
cycle `8` (`0`), with the checked clear suffix starting at global cycle `8`.
Validation: bytecode-disabled `py_compile` passed and the focused regression
passed in `202.762s`.

Status `changed-under-evidence`: horizon extension and recurrence falsifiers
now have a reusable receipt rather than ad hoc scripts.  Eventual clearance and
Goldbach remain open.

### 2026-09-12 continuation: receipt-driven clearance through cycle 48

The new cycle-horizon receipt checked global cycles `41..48`; each has zero
full-action negatives and zero non-rescued `.3` first-three tail targets.  The
`.3` tail persists with counts `5,7,1,5,5,8,12,8`, and the smallest full-action
minimum in the band is `0.3415555323766872` at `N=458576`.

Status `aha-candidate`: continuous measured clearance now reaches global
cycle `48`; finite evidence only.

### 2026-09-12 continuation: preserve rescued tail target lists

The co-occurrence and cycle-horizon receipts now carry actual `.3` tail target
lists and rescued target lists, not just counts.  Validation: bytecode-disabled
`py_compile` passed, co-occurrence focused regression passed in `79.293s`, and
cycle-horizon focused regression passed in `223.811s`.

Status `changed-under-evidence`: the next mechanism search can inspect exact
rescued targets from the receipt data shape.  No theorem is proved by this
change.

### 2026-09-12 continuation: cycle 43 single-tail microscope

Global cycle `43` has one `.3` first-three tail target, `448346`, and it is
rescued with first_three `-0.3106946886916736`, complement
`0.9781909468423949`, and full margin `0.6674962581507213`.  The cycle full
minimum is elsewhere (`440866`, value `0.37175458031519565`).

Status `aha-candidate`: this supports a two-zone target: finite/boundary
non-rescued exceptions plus an eventual regime where tail deficits are shallow
or complement buffers are uniformly large.

### 2026-09-12 continuation: first-three tail rescue-profile receipt

`q286_first_three_tail_rescue_profile_receipt` now records exact tail targets,
rescued/non-rescued splits, per-tail deficit, complement, recombined margin,
and rescue-buffer extrema.  The focused regression anchors the cycle `43`
single-tail case (`448346`) and passed in `254.052s` after bytecode-disabled
`py_compile`.

Status `changed-under-evidence`: complement rescue can now be profiled across
later bands to test whether tails are shallow, strongly buffered, or split
between those regimes.  No theorem is proved.

### 2026-09-12 continuation: cycle 41 through 48 rescue-profile band

The rescue-profile receipt was run one cycle at a time over global cycles
`41..48`.  Every `.3` tail target is rescued.  Across the band, deepest
first-three deficit is `0.46290305391350506`, minimum tail-set complement is
`0.6776643969822953`, and minimum rescue margin is `0.3560917899268151`.

Status `aha-candidate`: this supports a sharper eventual target: prove a
tail-set complement lower bound after the finite boundary regime.  Finite
evidence only.

### 2026-09-12 continuation: cycle 8 through 15 transition rescue profile

The first all-rescued block after the boundary was profiled.  Cycles `8..15`
all have zero non-rescued `.3` tail targets, but cycle `8` has a small rescue
margin: deepest deficit `0.7148225634431425`, minimum tail-set complement
`0.43158471467708337`, and minimum rescue margin `0.012576466293799509`.

Status `changed-under-evidence`: the measured picture is now three-zone:
finite non-rescued boundary cycles, rescued-but-delicate transition cycles,
and later large-buffer cycles.  Later-band complement-floor constants cannot
be assumed from cycle `8`.

### 2026-09-12 continuation: cycle 16 through 23 transition-to-buffer profile

Cycles `16..23` were profiled.  Every `.3` tail target is rescued.  Deepest
deficit is `0.6743272141983545`, minimum tail-set complement is
`0.4989495025198246`, and minimum rescue margin is `0.17360050532072466`.
Cycles `16..20` remain transition-like; cycles `21..23` are closer to the
later large-buffer profile.

Status `changed-under-evidence`: test cycles `24..40` next to determine
whether a stable complement floor begins near cycle `21` or if the transition
exception range extends farther.

### 2026-09-12 continuation: cycle 24 through 32 rescue-profile block

Cycles `24..32` were profiled.  Every `.3` tail target is rescued.  Deepest
deficit is `0.4471460665759927`, minimum tail-set complement is
`0.5500849164245104`, and minimum rescue margin is `0.2360810314099344`.
Cycles `24`, `25`, and `30` dip below the later `41..48` complement floor.

Status `changed-under-evidence`: the stable later-band floor does not begin at
cycle `21` with the later constants; transition exceptions may extend through
cycle `30`.

### 2026-09-12 continuation: cycle 33 through 40 rescue-profile gap

Cycles `33..40` were profiled.  Every `.3` tail target is rescued.  Deepest
deficit is `0.4258451609398066`, minimum tail-set complement is
`0.6393542776650206`, and minimum rescue margin is `0.31158984534443446`.
Cycle `37` is the limiting dip.

Status `aha-candidate`: finite data now suggests four zones: boundary `0..7`,
delicate transition `8..20`, middle transition/buffer `21..32`, and stronger
buffer from at least cycle `33`.  No eventual theorem is proved.

### 2026-09-12 continuation: cycle 49 through 56 fresh buffer falsifier

Cycles `49..56` were profiled as a fresh later-band falsifier.  Every `.3`
tail target is rescued.  Deepest deficit is `0.44255568348284197`, minimum
tail-set complement is `0.6899144617707726`, and minimum rescue margin is
`0.3433502408615505`.

Status `aha-candidate`: the fresh band does not break the checked stronger
buffer pattern from cycle `33` onward; finite evidence only.

### 2026-09-12 continuation: tail rescue floor-candidate receipt

`q286_first_three_tail_rescue_floor_candidate_receipt` now tests the
post-cycle-33 buffer candidate explicitly: first-three threshold `.3`,
complement floor `.63`, rescue margin floor `.3`, and optional deficit ceiling
`.47`.  Focused regression on global cycle `37` passes with no violations;
minimum complement `0.6393542776650206`, minimum rescue margin
`0.31158984534443446`, and maximum deficit `0.37765470838997645`.

Status `changed-under-evidence`: the candidate is now executable and
falsifiable, but remains finite evidence only.

### 2026-09-12 continuation: cycles 57 through 64 floor-candidate falsifier

The explicit `.63/.3/.47` floor candidate was tested on fresh cycles `57..64`.
Every cycle passed; cycle `61` had no `.3` tail targets.  No complement,
margin, or deficit violations occurred.  The limiting nonempty values are
margin `0.4482571418757897` at cycle `58` and deficit `0.4144257505601422` at
cycle `64`.

Status `aha-candidate`: the named post-cycle-33 floor candidate survived a
fresh later-band falsifier; finite evidence only.

### 2026-09-12 continuation: far-band floor-candidate probe

The `.63/.3/.47` floor candidate was tested on global cycles `97..104`.  Each
cycle passed, with zero nonrescued targets and zero `.3` first-three tail
targets in every checked cycle.

Status `changed-under-evidence`: this extends finite far-band evidence for
tail absence, but it does not prove an eventual theorem and does not provide a
new nonempty stress test of the floor constants.  The next proof target is an
analytic explanation for disappearance or rescue of the tail beyond the
measured windows.

### 2026-09-13 continuation: sparse late recurrences all rescued

The missing mode-only cycles in the `65..96` gap were completed.  The `.3`
first-three tail does not permanently disappear after cycle `64`; it recurs
sparsely at global cycles `72`, `73`, `76`, `77`, `79`, `80`, `81`, `83`, and
`94`, with one tail target in each cycle.  All other cycles in `65..96` are
tail-free at threshold `.3`.

The recurrence cycles were then checked with the `.63/.3/.47` floor candidate.
All nine passed, with zero non-rescued tail targets and zero floor violations.
The weakest rescue margin among these sparse recurrences is
`0.6336019961687318` at cycle `83`; the deepest first-three deficit is
`0.3454855905369533` at cycle `94`.

Status `changed-under-evidence`: the live target is no longer tail
disappearance.  It is a selected-tail rescue theorem: rare late first-three
tail hits must be paired with enough complement buffer.  This remains finite
evidence only; Goldbach and the needed pointwise signed correlation theorem
remain open.

### 2026-09-13 continuation: cycles 105 through 136 preserve selected-tail rescue

The next 32-cycle block was checked with the mode-only horizon receipt.
Cycles `105..136` have only three `.3` first-three tail hits: global cycles
`121`, `131`, and `136`, one hit each.  All three passed the `.63/.3/.47`
floor candidate with zero non-rescued targets and no violations.  The weakest
margin among the three is `0.944998867177687` at cycle `136`; the deepest
deficit is also cycle `136`, `0.3394138842129011`.

Status `aha-candidate`: the selected-tail rescue target survived a fresh later
block.  The live proof obligation is a complement lower bound conditioned on
the first-three tail set, not tail disappearance.  Still finite evidence only.

### 2026-09-13 continuation: fast scanner and cycles 137 through 168

The original mode-only horizon scanner was too slow for repeated late-cycle
extension.  Four brute-force 8-cycle workers for cycles `137..168` were
stopped after accumulating more than 1300 CPU seconds each without returning
receipts.  A new accelerated scanner,
`q286_first_three_tail_mode_only_fast_horizon_receipt`, now precomputes the
q286 first-three singular-mode linear functional and uses NumPy residue
accumulation.

Validation: `py_compile` passed, and focused equivalence regression
`test_q286_first_three_tail_mode_only_fast_horizon` passed against the slow
mode-only receipt on a five-target window in `86.198s`.

Using the fast receipt, global cycles `137..168` are all tail-free at
threshold `.3`.  The lowest first-three values by 8-cycle block are:
cycle `142`, `-0.27272709731535705`; cycle `149`,
`-0.25332323305534654`; cycle `158`, `-0.22021297112953594`; and cycle `162`,
`-0.24997112424637502`.

Status `engineering-plus-evidence`: this improves the scanner and extends
finite tail-absence evidence, but it does not prove tail disappearance,
selected-tail rescue, Goldbach, RH, or any pointwise signed-correlation
estimate.

### 2026-09-13 continuation: cycles 169 through 200 remain tail-free

The accelerated mode-only scanner was applied to global cycles `169..200`.
All 32 cycles are tail-free at threshold `.3`, so no complement rescue-floor
check was required.  Block minima were: cycle `170`,
`-0.2244238458552083`; cycle `180`, `-0.24578791073619177`; cycle `187`,
`-0.23662242439894973`; and cycle `197`, `-0.19098821755917464`.

Status `finite-tail-absence-evidence`: checked cycles `137..200` are now
tail-free after the sparse selected-tail recurrences through cycle `136`.
This remains finite evidence only and does not prove eventual disappearance.

### 2026-09-13 continuation: cycles 201 through 232 remain tail-free

The fast mode-only scanner was extended through global cycle `232`.  Cycles
`201..232` are all tail-free at threshold `.3`; no rescue-floor check was
required.  Block minima were: cycle `206`, `-0.1941773413191678`; cycle `216`,
`-0.20154505507379825`; cycle `217`, `-0.20736210641526237`; and cycle `231`,
`-0.20693553807121948`.

Status `finite-tail-absence-evidence`: cycles `137..232` are checked
tail-free after the sparse recurrences through cycle `136`.  This remains a
finite diagnostic, not an eventual theorem.

### 2026-09-13 continuation: cycles 233 through 264 remain tail-free

The fast mode-only scanner was extended through global cycle `264`.  Cycles
`233..264` are all tail-free at threshold `.3`; no rescue-floor check was
required.  Block minima were: cycle `235`, `-0.18648556964961702`; cycle `245`,
`-0.18814240147876807`; cycle `250`, `-0.1956485325659766`; and cycle `257`,
`-0.18282739060588282`.

Status `finite-tail-absence-evidence`: cycles `137..264` are checked
tail-free after the sparse recurrences through cycle `136`.  This remains a
finite diagnostic, not an eventual theorem.

### 2026-09-13 continuation: cycles 265 through 296 remain tail-free

The fast mode-only scanner was extended through global cycle `296`.  Cycles
`265..296` are all tail-free at threshold `.3`; no rescue-floor check was
required.  Block minima were: cycle `266`, `-0.19902872242009065`; cycle `273`,
`-0.1771080171549704`; cycle `288`, `-0.16965353530921884`; and cycle `292`,
`-0.19368388953654794`.

Status `finite-tail-absence-evidence`: cycles `137..296` are checked
tail-free after the sparse recurrences through cycle `136`.  This remains a
finite diagnostic, not an eventual theorem.

### 2026-09-13 continuation: fast scanner late-tail regression

Added and passed
`test_q286_first_three_tail_mode_only_fast_late_tail_hit`, which compares the
fast scanner against the slow mode-only scanner on the known late `.3` tail
target `1222142` from global cycle `121`.  The focused test passed in
`60.506s`.

Status `validation`: the fast scanner is now checked on a late nonempty tail
case as well as the initial tiny window.  This supports the finite horizon
receipts but does not prove an eventual theorem.

### 2026-09-13 continuation: sparse tail hit residue profile

Added `q286_first_three_tail_hit_residue_profile_receipt`, with focused
regression `test_q286_first_three_tail_hit_residue_profile` passing in
`28.527s`.  The receipt profiles first-three tail hits by residues modulo
`286` and `10010`, offsets, and cycle residues.

Measured sparse-hit bands:

- Cycles `65..96`: nine hits; only `20 mod 286` repeats, and only
  `4882 mod 10010` repeats.
- Cycles `105..136`: three hits; no repeated residue modulo `286` or `10010`.

Status `falsifier`: the checked sparse late tail is not a single-residue or
single-period-residue channel.  The proof target remains broader signed
oscillation control or selected-tail complement rescue.

### 2026-09-13 continuation: cycles 297 through 328 remain tail-free

The fast mode-only scanner was extended through global cycle `328`.  Cycles
`297..328` are all tail-free at threshold `.3`; no rescue-floor check was
required.  Block minima were: cycle `297`, `-0.1868226923569528`; cycle `305`,
`-0.15929169145794012`; cycle `315`, `-0.1684585498216937`; and cycle `328`,
`-0.19260805167808093`.

Status `finite-tail-absence-evidence`: cycles `137..328` are checked
tail-free after the sparse recurrences through cycle `136`.  This remains a
finite diagnostic, not an eventual theorem.

### 2026-09-13 continuation: post-136 near-tail threshold profile

The fast scanner was rerun on cycles `137..264` with thresholds `.2`, `.25`,
`.275`, and `.3`.  The `.3` disappearance is not isolated:

- `137..168`: `.2` count `57`, `.25` count `4`, `.275`/`.3` count `0`;
  minimum `-0.27272709731535705`.
- `169..200`: `.2` count `17`, `.25`/`.275`/`.3` count `0`; minimum
  `-0.24578791073619177`.
- `201..232`: `.2` count `3`, `.25`/`.275`/`.3` count `0`; minimum
  `-0.20736210641526237`.
- `233..264`: all four threshold counts `0`; minimum
  `-0.1956485325659766`.

Status `finite-damping-evidence`: checked cycles show no `.275` tail from
`137..264`, no `.25` tail after cycle `149` through `264`, and no `.2` tail
after cycle `231` through `264`.  This remains finite evidence only.

### 2026-09-13 continuation: threshold-ladder receipt

Added `q286_first_three_tail_threshold_ladder_receipt`, with focused regression
`test_q286_first_three_tail_threshold_ladder` passing in `29.667s`.  The
receipt turns the near-tail threshold profile into a reusable finite diagnostic
over nested thresholds and configurable cycle blocks.

A redundant ladder probe over cycles `265..328` was interrupted after it stayed
CPU-bound too long; no result from that probe is recorded.  Existing committed
per-cycle minima already imply those cycles stay above `-.2`, but a future
confirmation should use narrower blocks or optimize the summary path.

Status `tooling`: the staged damping question is now executable as a receipt,
not just prose.  Still no eventual theorem.

### 2026-09-13 continuation: threshold-ladder summary path

The threshold-ladder receipt now uses a summary mode of the validated fast
scanner and does not retain per-target rows.  Public fast-horizon calls remain
rowful for equivalence checks and downstream residue diagnostics.

Validation: `py_compile` passed, and the focused bundle
`test_q286_first_three_tail_mode_only_fast_horizon`,
`test_q286_first_three_tail_hit_residue_profile`, and
`test_q286_first_three_tail_threshold_ladder` passed in `82.235s`.

Status `engineering`: this makes larger near-tail ladder probes cheaper and
safer to run, but it is not new theorem evidence and proves no eventual q286
tail bound.

### 2026-09-13 continuation: cycles 265 through 328 threshold ladder

The summary-mode threshold ladder was run in four 16-cycle probes covering
cycles `265..328`.  Every 8-cycle block had zero targets below `-.2`, `-.25`,
`-.275`, and `-.3`; each probe confirmed `target_rows_included=False`.

Block minima:

- `265..272`: cycle `266`, target `2672932`, first-three
  `-0.19902872242009065`.
- `273..280`: cycle `273`, target `2751106`, first-three
  `-0.1771080171549704`.
- `281..288`: cycle `288`, target `2900782`, first-three
  `-0.16965353530921884`.
- `289..296`: cycle `292`, target `2935984`, first-three
  `-0.19368388953654794`.
- `297..304`: cycle `297`, target `2986282`, first-three
  `-0.1868226923569528`.
- `305..312`: cycle `305`, target `3069904`, first-three
  `-0.15929169145794012`.
- `313..320`: cycle `315`, target `3170596`, first-three
  `-0.1684585498216937`.
- `321..328`: cycle `328`, target `3299602`, first-three
  `-0.19260805167808093`.

Status `finite-damping-evidence`: the checked damping window is now extended
to cycle `328` at the `.2` threshold, but this is still finite evidence and
not an eventual first-three tail theorem.

### 2026-09-13 continuation: prime-sliced fast scanner

The fast first-three scanner now slices the precomputed prime table for
strict-central candidate primes and tests prime partners, rather than building
a dense central integer interval for every target.  The receipt semantics are
unchanged.

Validation: `py_compile` passed, and the focused bundle
`test_q286_first_three_tail_mode_only_fast_horizon`,
`test_q286_first_three_tail_mode_only_fast_late_tail_hit`,
`test_q286_first_three_tail_hit_residue_profile`, and
`test_q286_first_three_tail_threshold_ladder` passed in `85.710s`.

One direct summary-mode probe at global cycle `329` tested `5005` targets in
`32.48320049999893s` and found zero targets below `-.2`, `-.25`, `-.275`, or
`-.3`.  Its minimum was target `3304702`, first-three
`-0.1451192809169075`.

Status `engineering-plus-finite-evidence`: the checked `.2` tail-free window
now reaches cycle `329`, but this is still finite evidence and not an eventual
first-three tail theorem.

### 2026-09-13 continuation: crude max-discrepancy bound falsifier

A theorem that bounds only the maximum residue-class deviation from the
admissible mean is now identified as too blunt for the q286 first-three route.
The centered coefficient L1 bound would require relative max deviation at most
`0.0008292399353636012` in the worst target residue to force the `.2` lower
tail away.

At cycle `329`, target `3309688` has max relative deviation
`0.004732557895915037`, which is `5.120642803312157` times that target's `.2`
sufficient epsilon, but its actual first-three value is positive
`0.06420907247979844`.  Thus large pointwise residue deviations can be
harmless when aligned with favorable q286 coefficients.

Status `falsifier`: the next proof route should not seek a plain
supremum-norm equidistribution theorem.  It should seek a signed weighted norm
or cancellation estimate matched to the q286 first-three coefficient vector.

### 2026-09-13 continuation: weighted discrepancy norm receipt

The route now has an executable weighted-norm diagnostic:
`q286_first_three_weighted_discrepancy_norm_receipt`.  It computes the actual
first-three signed dot product, `L_infinity` and `L2` residue-weight deviations
from the admissible mean, Cauchy bounds from the centered q286 coefficient
vector, and negative-bound utilization.

Validation: `py_compile` passed, and the focused bundle
`test_q286_first_three_weighted_discrepancy_norm`,
`test_q286_first_three_tail_mode_only_fast_horizon`,
`test_q286_first_three_tail_mode_only_fast_late_tail_hit`,
`test_q286_first_three_tail_hit_residue_profile`, and
`test_q286_first_three_tail_threshold_ladder` passed in `84.240s`.

On global cycle `329`, threshold `.2`, all `5005` targets are actually clear,
but `L_infinity` Cauchy certifies only `88` and plain `L2` Cauchy certifies
only `182`.  The worst actual negative value is target `3304702`,
`-0.14511928091690746`; the maximum negative `L2`-bound utilization is only
`0.37431718152903626` at target `3305200`.

Status `falsifier-plus-target`: the proof target has narrowed from generic
residue equidistribution to an alignment or signed-cancellation estimate for
the q286 coefficient vector.

### 2026-09-13 continuation: cycle-329 alignment profile

The weighted discrepancy receipt now records the signed `L2` alignment angle
between the centered q286 coefficient vector and the centered residue-weight
discrepancy.  On cycle `329`, threshold `.2`, there are `2346` negative
first-three targets but none has negative `L2`-bound utilization at or above
`.375`; only `26` exceed `.25`.

The strongest negative alignment is target `3305200`, with first-three
`-0.14018011556710205` and `l2_alignment_cosine`
`-0.37431718152903626`.  The minimum first-three target `3304702` has
first-three `-0.14511928091690746` but weaker negative alignment
`-0.27262295696982886`.

Status `hypothesis-target`: a negative-alignment ceiling near `.375` would
explain cycle `329` where plain `L2` Cauchy does not.  This must now be tested
against earlier sparse-tail and near-tail windows before becoming a serious
lemma candidate.

### 2026-09-13 continuation: selected bad-target alignment check

The alignment ceiling now has a selected-target falsifier receipt:
`q286_selected_first_three_alignment_receipt`.  It checks explicit bad and
near-bad targets against a candidate negative-alignment ceiling.

Validation: `py_compile` passed, and focused tests
`test_q286_first_three_weighted_discrepancy_norm` and
`test_q286_selected_first_three_alignment` passed in `28.192s`.

On the default selected set
`10424,10664,10814,14138,14732,58736,88346,125504,448346,1222142,3304702,3305200`,
there are `9` targets below `-.2`, `11` negative first-three targets, and
zero violations of the `.375` negative-alignment ceiling.  The worst
negative-alignment row is still `3305200` with utilization
`0.37431718152903626`; the largest discrepancy-size row is `10664`, with
`l2_to_sufficient_ratio 26.134535399601887` but utilization only
`0.2200322261927699`.

Status `survived-selected-falsifier`: the ceiling survived known bad selected
targets, but remains finite evidence.  The next obligation is a windowed scan
over earlier sparse-tail cycles.

### 2026-09-13 continuation: sparse-tail alignment window falsifier

The `.375` alignment ceiling is now falsified by a sparse-tail window scan.
`q286_first_three_tail_alignment_window_receipt` finds q286 first-three tail
targets with the fast scanner, then checks weighted alignment only on those
tail hits.

Validation: `py_compile` passed, and focused tests
`test_q286_selected_first_three_alignment` and
`test_q286_first_three_tail_alignment_window` passed in `27.157s`.

On global cycles `105..136`, tail threshold `.3`, the receipt found tail
targets `1222142`, `1323632`, and `1379072`.  At alignment ceiling `.375`,
`1323632` and `1379072` violate.  The maximum utilization is
`0.38387259544434144` at `1379072`.  Rechecking the same window at ceiling
`.4` gives zero violations.

Status `falsifier`: the proof target cannot be a `.375` ceiling.  The
surviving measured target is a looser `.4` negative-alignment ceiling, which
must next be tested on cycles `65..96` and any later recurrence.

### 2026-09-13 continuation: cycles 65 through 96 alignment window

The `.4` negative-alignment ceiling was tested on the earlier sparse-tail
recurrence band, global cycles `65..96`.  The receipt found nine `.3` tail
targets:

`733126,741976,775426,782336,805682,818528,828418,846632,955832`.

There were zero `.4` alignment violations.  The maximum utilization was
`0.35911925295935604` at target `782336`, whose first-three ratio is
`-0.33516065470389805`.

Status `survived-window-falsifier`: `.4` survives the checked sparse-tail
bands `65..96` and `105..136`; `.375` remains false.  This is finite evidence,
not a theorem.

### 2026-09-13 continuation: selected alignment shared-sieve path

The selected-target alignment receipt now computes selected rows with one
shared prime/log table rather than rebuilding target-by-target.  Focused tests
`test_q286_selected_first_three_alignment` and
`test_q286_first_three_tail_alignment_window` passed in `28.112s`.

The default selected set at ceiling `.4` still has zero violations, maximum
negative utilization `0.37431718152903626` at `3305200`, and maximum raw L2
sufficient-ratio `26.134535399601887` at `10664`.

Status `engineering`: this makes broader selected falsifier checks cheaper;
it does not change the finite mathematical evidence or prove a theorem.

### 2026-09-13 continuation: cycle-0 dense-tail alignment check

The `.4` negative-alignment ceiling was tested on global cycle `0`, where
there are `972` targets below the `.3` first-three tail threshold.  There were
zero `.4` alignment violations.  The maximum negative utilization was
`0.2692173284796089` at target `14892`, whose first-three ratio is
`-0.8671841914960792`.

Status `survived-dense-tail-falsifier`: `.4` survives cycle `0` as well as the
two checked sparse-tail recurrence bands.  This is finite evidence only; a
proof would still need a signed alignment estimate plus a discrepancy-size
estimate.

### 2026-09-13 continuation: eight-period tail alignment check

The `.4` negative-alignment ceiling was tested against all `.3` first-three
tail targets in the original eight-period q286 horizon.  Among `40040` tested
targets there are `4406` tail targets, spread across all eight cycles, and
zero `.4` alignment violations.

The maximum negative utilization is `0.3724338138420597` at target `70526`,
whose first-three ratio is `-0.7650482510196679`.  The maximum raw L2
sufficient-ratio remains the early target `10898`, with ratio
`35.552799422567006` but utilization only `0.11954563697711441`.

Status `survived-eight-period-falsifier`: `.4` survives the full checked
eight-period tail set.  This is still finite evidence and proves no eventual
estimate or Goldbach theorem.

### 2026-09-13 continuation: post-136 near-tail alignment checks

The `.4` negative-alignment ceiling was tested on the post-136 `.2` near-tail
windows.  It has zero violations in cycles `137..168`, `169..200`, and
`201..232`.

The maxima were:

- `137..168`: target `1426262`, utilization `0.3833219530783246`.
- `169..200`: target `1762964`, utilization `0.37640635712461384`.
- `201..232`: target `2326222`, utilization `0.34127687470555046`.

Status `survived-near-tail-falsifier`: `.4` survives the checked `.2`
near-tail windows as well as the `.3` tail windows.  This is finite evidence
only and not an eventual theorem.

### 2026-09-13 continuation: alignment/complement certificate split

The route now has a selected-target complement certificate:
`q286_selected_alignment_complement_certificate_receipt`.  It checks whether
the measured complement beats `.4 * l2_bound`, which would certify positivity
under a future `.4` alignment theorem.

Validation: `py_compile` passed, and
`test_q286_selected_alignment_complement_certificate` passed in `85.218s`.

On selected targets `14138,70526,1379072,1426262,3305200`, the certificate
passes all except `14138`.  The failed target is also the actual full-negative
boundary target:

`complement 0.018073313793834367`, `.4*l2_bound 1.9956301199132718`, margin
`-1.9775568061194373`.

Status `route-split`: a future proof should treat early boundary/full-negative
cases separately, then seek an eventual complement-vs-alignment bound for the
later regime.

### 2026-09-13 continuation: direct lower-support component rows

The lower-support component-pair receipt now has a direct component-row helper,
`_q286_lower_support_component_rows_for_targets`, which reuses the cached fixed
q286 lower-support component data and computes only the target-specific
strict-central residue weights.  This lets
`q286_lower_support_component_pair_tail_window_receipt` measure the active
`(5,7)` / `(7,11)` component pair without calling the full
component-local/package receipt for selected targets.

Validation:

```text
python -B -m py_compile lcm_sawtooth_goldbach_transfer.py test_lcm_sawtooth_goldbach_transfer.py
test_q286_lower_support_component_pair_tail_window ... ok
Ran 1 test in 96.695s
test_q286_lower_support_package_component_local_discrepancy ... ok
Ran 1 test in 167.910s
```

A compact unselected-window smoke probe at `start=1222142`,
`cycle_count=1`, `targets_per_cycle=1` also exercised the repaired window
join and returned the same active target:

```text
tested 1
tails (1222142,)
both_negative ()
period 10010
first_two -0.3088331795605278
first_three -0.3075877603708794
full 0.9457162662139126
pair {(5, 7): -0.001083408055793006, (7, 11): 0.014826359763802506}
source_subcone True
source_lower_tail False
```

Status `engineering-validation`: this preserves the component-pair theorem
target while removing one unnecessary package/decomposition layer from the
selected-target path and fixing provenance for the window path.  It is not new
proof evidence.  Broad scans still require further optimization of the
lower-tail computation and target-specific prime-pair/residue-weight work, or
a direct proof attempt for the signed pointwise arithmetic estimate.

### 2026-09-13 continuation: lighter component-pair window selector

The component-pair window receipt now uses
`q286_first_two_mode_lower_tail_receipt` directly in both selected-target and
window modes.  This removes the intermediate
`q286_first_two_mode_subcone_complement_window_receipt` dependency from
`q286_lower_support_component_pair_tail_window_receipt`; the receipt now
sources first-two, first-three, full-action, and provenance rows from the
lower-tail receipt.

Validation:

```text
python -B -m py_compile lcm_sawtooth_goldbach_transfer.py test_lcm_sawtooth_goldbach_transfer.py
test_q286_lower_support_component_pair_tail_window ... ok
Ran 1 test in 96.155s
```

The focused test now asserts that the component-pair receipt has no
`source_subcone_complement_window_receipt` and does have
`source_lower_tail_receipt`.  A compact unselected window probe at
`1222142` passed in `102.02481009999974s`:

```text
tested 1
tails (1222142,)
both_negative ()
period 10010
source_subcone_receipt False
source_lower_tail_receipt True
first_two -0.30883317956052847
first_three -0.3075877603708801
full 0.9457162662139126
pair {(5, 7): -0.001083408055793006, (7, 11): 0.014826359763802506}
source_subcone False
source_lower_tail True
```

Status `engineering-validation`: the active component-pair theorem target is
unchanged.  The remaining broad-scan bottleneck is now isolated to the
lower-tail computation and target-specific strict-central residue weights, not
the removed subcone-complement wrapper.  Goldbach and the signed pointwise
estimate remain open.

### 2026-09-13 continuation: integrated q286 mode rows

`reduced_full_lower_envelope_receipt` now stores the individual q286 singular
mode contributions it already computes while forming the reduced model.
`q286_first_two_mode_lower_tail_receipt` reuses those stored mode rows instead
of running a separate `q286_leading_singular_mode_contribution_receipt` pass
over the same targets.

Validation:

```text
python -B -m py_compile lcm_sawtooth_goldbach_transfer.py test_lcm_sawtooth_goldbach_transfer.py
test_reduced_full_lower_envelope ... ok
test_q286_first_two_mode_lower_tail ... ok
Ran 2 tests in 65.408s
test_q286_lower_support_component_pair_tail_window ... ok
Ran 1 test in 67.676s
```

The reduced-envelope regression now asserts that the stored six mode ratios
plus the stored residual reconstruct the q286 deviation ratio.  The
component-pair focused regression improved from about `100.618s` to `67.676s`
on the same selected target.

The compact unselected window probe at `1222142` improved from about
`102.025s` to `66.23108959999809s` with unchanged measured values:

```text
tested 1
tails (1222142,)
both_negative ()
period 10010
source_subcone_receipt False
source_lower_tail_receipt True
first_two -0.30883317956052847
first_three -0.3075877603708801
full 0.9457162662139126
pair {(5, 7): -0.001083408055793006, (7, 11): 0.014826359763802506}
source_subcone False
source_lower_tail True
```

Status `engineering-validation`: this removes a duplicate q286
singular-mode target sweep from the component-pair route.  The remaining
broad-scan cost is the target-specific strict-central prime-pair/residue-weight
work in the reduced-envelope and lower-support component rows.  No eventual
q286 theorem, signed prime-correlation estimate, RH statement, or Goldbach
proof is established.

### 2026-09-13 continuation: sparse residue-weight reuse

The lower-tail route now has an opt-in sparse residue-weight payload.  When
`include_residue_weights=True`, `reduced_full_lower_envelope_receipt` records
the strict-central prime-pair log-weight by residue modulo `10010`, and
`q286_first_two_mode_lower_tail_receipt` carries that row forward.  The
component-pair receipt opts into this payload and passes it to
`_q286_lower_support_component_rows_for_targets`, avoiding a second
strict-central prime-pair sweep for the lower-support component rows.

Default reduced-envelope and lower-tail receipts remain compact; the new
payload is only included when explicitly requested.

Validation:

```text
python -B -m py_compile lcm_sawtooth_goldbach_transfer.py test_lcm_sawtooth_goldbach_transfer.py
test_q286_lower_support_component_pair_tail_window ... ok
Ran 1 test in 63.162s
test_reduced_full_lower_envelope ... ok
test_q286_first_two_mode_lower_tail ... ok
Ran 2 tests in 66.328s
```

The compact unselected component-pair probe at `1222142` passed in
`68.88616069999989s`; it confirmed `weights_included True`, `1337` sparse
residue-weight rows, no simultaneous negative pair action, and unchanged
measured first-two/first-three/full-action values up to floating-point
roundoff:

```text
tested 1
tails (1222142,)
both_negative ()
period 10010
source_subcone_receipt False
source_lower_tail_receipt True
weights_included True
first_two -0.30883317956052847
first_three -0.3075877603708801
full 0.9457162662139126
pair {(5, 7): -0.0010834080557930044, (7, 11): 0.014826359763802442}
weight_row_count 1337
```

Status `engineering-validation`: this removes a duplicate target-specific
strict-central sweep from the component-pair receipt.  Broad scans are still
finite diagnostics, and the theorem target remains the signed pointwise
arithmetic estimate preventing simultaneous strong negative `(5,7)` and
`(7,11)` lower-support centered action on the active subcone.  Goldbach
remains open.

### 2026-09-13 continuation: three-target component-pair finite probe

The selected-target component-pair receipt was run over all three known late
sparse-tail comparison targets:

```text
q286_lower_support_component_pair_tail_window_receipt(
    selected_targets=(1222142,1323632,1379072),
    first_two_threshold=.2,
    tail_threshold=.3)
```

It completed in `64.87790719999975s`.  All three selected targets were in the
`.2` first-two / `.3` first-three subcone, sparse lower-tail residue weights
were reused, and no target had simultaneous negative centered action in both
active lower-support channels:

```text
tested 3
tails (1222142, 1323632, 1379072)
both_negative ()
weights_included True
1222142 pair_sum 0.013742951708009437
  (5,7) -0.0010834080557930044
  (7,11) 0.014826359763802442
1323632 pair_sum 0.08749508122821226
  (5,7) 0.06545161702266966
  (7,11) 0.022043464205542592
1379072 pair_sum 0.04672425150515765
  (5,7) -0.036824552185769695
  (7,11) 0.08354880369092735
```

Status `finite-diagnostic`: this strengthens the finite comparison set for the
active component-pair theorem target but does not prove the eventual exclusion,
a signed prime-correlation estimate, RH, or Goldbach.  The remaining
non-circular path is still to prove, or reduce precisely, the fixed-modulus
pointwise statement preventing simultaneous strong negative `(5,7)` and
`(7,11)` centered action on the active subcone after finite boundary
exceptions.

### 2026-09-13 continuation: component-pair theorem obligation sharpened

The exact component-pair obstruction is now recorded in
`notes/q286-component-pair-theorem-obligation.md`.  The active centered
actions are inner products between the actual strict-central prime-pair
residue discrepancy vector `d_N` modulo `10010` and two centered fixed
coefficient vectors `c_57,N` and `c_711,N`.

New executable receipt
`q286_lower_support_component_pair_coefficient_geometry_receipt` scans all
`5005` even target residues modulo `10010`.  Focused regression
`test_q286_lower_support_component_pair_coefficient_geometry` passed in
`32.897s`.  Across all even residues, the pair coefficient cosine remains in
`-0.0381940494499906 .. 0.0419660251672338`, so the two coefficient vectors
are structurally near-orthogonal rather than oppositely constrained.

A direct selected-target discrepancy probe on
`14138,1222142,1323632,1379072` found boundary target `14138` has much larger
relative residue-weight discrepancy (`0.11251754817108045`) and simultaneous
negative component actions, while the late sparse-tail targets have relative
discrepancy around `.0157..0164` and avoid the both-negative cone.

Status `theorem-obligation`: this is useful because it rules out a pure
coefficient-geometry proof of the component-pair exclusion.  Nonnegativity,
support, and total mass alone permit small centered perturbations making both
actions negative.  The remaining theorem must use actual binary prime-pair
arithmetic: either a cone-avoidance theorem for the prime-pair discrepancy
vector on the active `.2`/`.3` subcone, a signed lower bound for the pair sum,
or a fixed-modulus pointwise Goldbach-in-progressions estimate strong enough
to make all fixed centered component actions `o(P(N))`.  Goldbach remains
open.

### 2026-09-13 continuation: component-pair cone projection

New receipt `q286_lower_support_component_pair_cone_projection_receipt`
projects the actual strict-central prime-pair discrepancy vector onto the
two-dimensional span of the `(5,7)` and `(7,11)` centered coefficient vectors.
Focused regression `test_q286_lower_support_component_pair_cone_projection`
passed in `88.970s`.

Default selected-target output confirms that the finite boundary target
`14138` is the only both-negative case among
`14138,1222142,1323632,1379072`:

```text
both_negative (14138,)
14138 projection_fraction 0.08397880199809928
1222142 projection_fraction 0.01129983025146733
1323632 projection_fraction 0.04807076284797583
1379072 projection_fraction 0.0703199163405805
```

Status `theorem-sharpening`: almost all measured discrepancy L2 is orthogonal
to the dangerous two-component span, even at the boundary witness.  The
non-circular theorem target is now narrower than global equidistribution:
prove signed cone avoidance for the small projection of the actual prime-pair
discrepancy vector onto the `(5,7)/(7,11)` span after finite boundary
exceptions.  This is still a pointwise binary-prime correlation problem, not a
Goldbach proof.

### 2026-09-13 continuation: component-pair support-geometry obstruction

New receipt
`q286_lower_support_component_pair_support_geometry_obstruction_receipt`
makes the finite-vector obstruction explicit.  For every even target residue
modulo `10010`, it constructs nonnegative admissible weights with the same
total mass and both `(5,7)` and `(7,11)` centered component actions negative.
Focused regression
`test_q286_lower_support_component_pair_support_geometry_obstruction` passed
in `36.947s`.

Receipt summary:

```text
even_residue_count 5005
obstructed_count 5005
all_obstructed True
least-negative maximum component action:
  target_residue 3424
  max action -0.07974971574660267
```

Status `lane-closed`: this closes a possible pure
support/nonnegativity/total-mass/coefficient-geometry proof of the
component-pair exclusion.  The surviving route must use actual prime-pair
arithmetic: a signed cone-avoidance theorem for the tiny projection measured
above, or a precise reduction to fixed-modulus pointwise binary Goldbach in
progressions.  Goldbach remains open.

### 2026-09-13 continuation: component-pair character-mixture theorem target

New receipt `q286_lower_support_component_pair_character_mixture_receipt`
expresses the active `(5,7)` and `(7,11)` component actions as exact character
mixtures modulo `10010`.  Focused regression
`test_q286_lower_support_component_pair_character_mixture` passed in `68.299s`.

The active arithmetic target is smaller than full residue-class
equidistribution:

```text
(5,7) active character count 8
(7,11) active character count 23
active union character count 31
pair-sum L1/principal_mean 15.262957606760951
pair-sum L2/principal_mean 3.003987991450646
maximum action reconstruction error 4.961197005087556e-14
```

The focused regression now freezes the exact active labels.  In factor order
`(5,7,11,13)`, the `(5,7)` component uses `(a,b,0,0)` labels and the
`(7,11)` component uses `(0,b,c,0)` labels.

Follow-up receipt `q286_lower_support_component_pair_real_channel_receipt`
collapses the active complex labels by conjugation.  Focused regression
`test_q286_lower_support_component_pair_real_channel` passed in `30.401s`:
`8 -> 4` real channels for `(5,7)`, `23 -> 12` for `(7,11)`, and `31 -> 16`
for the active union, with the lone self-conjugate active label `(0,3,5,0)`.
The receipt now exposes coefficient-bearing real formulas: `2*Re(c*S_chi)`
for conjugate pairs and `Re(c*S_chi)` for the self-conjugate channel; the
pair-sum real-channel L1/principal_mean remains `15.262957606760951`.

Status `theorem-sharpening`: after closing support geometry, the surviving
non-circular target is signed cone avoidance for `16` coefficient-bearing real
conjugacy formulas inside these two explicit adjacent character-label blocks,
not arbitrary residue occupancy.  This is narrower than full fixed-modulus
Goldbach-in-progressions but remains a pointwise binary-prime correlation
theorem.  Goldbach remains open.

New receipt `q286_lower_support_component_pair_real_channel_action_receipt`
evaluates those `16` formulas on selected actual strict-central prime-pair
weights.  Focused regression
`test_q286_lower_support_component_pair_real_channel_action` passed in
`73.676s`.  It reconstructs the selected pair sums with maximum error
`1.1310397063368782e-15`: `14138` has real-channel pair sum
`-1.152543267627036`, while the late comparison targets `1222142`,
`1323632`, and `1379072` have positive sums `0.01374295170801024`,
`0.08749508122821215`, and `0.046724251505156425`.
This is exact finite decomposition evidence, not a pointwise theorem.

New receipt
`q286_lower_support_component_pair_real_channel_rescue_margin_receipt`
rewrites the selected lower-support rescue condition as a centered
real-channel pair-sum floor.  Focused regression
`test_q286_lower_support_component_pair_real_channel_rescue_margin` passed in
`119.854s`.  `14138` misses its floor by `-0.8769412734408442`; late targets
`1222142`, `1323632`, and `1379072` clear by `0.9457162662139125`,
`1.0242192662363734`, and `0.944998867177687`.  Over the late comparison set,
the uniform selected sufficient floor is centered pair sum
`>= -0.8982746156725305`, leaving observed margin `0.9120175673805407`.
This is a selected finite floor identity, not an eventual real-channel
estimate.

New receipt
`q286_lower_support_component_pair_real_channel_bound_budget_receipt`
translates that selected late floor into sufficient normalized channel-norm
thresholds.  Focused regression
`test_q286_lower_support_component_pair_real_channel_bound_budget` passed in
`121.411s`.  The active real-channel coefficient norms divided by principal
mean are `L1=15.262957606760978`, `L2=4.167538506325983`, and
`Linf=1.7049336541439826`.  Therefore the late selected floor would follow
from normalized real-channel representative sums bounded by
`0.05885324711081062` in `Linf`, or `0.2155408076755675` in `L2`.  This is a
sufficient-bound budget only; it does not prove the required pointwise
real-channel estimate.

New receipt
`q286_lower_support_component_pair_conditional_norm_closure_receipt`
separates the selected conditional theorem into two assumptions.  Focused
regression
`test_q286_lower_support_component_pair_conditional_norm_closure` passed in
`116.123s`.  The two assumptions are:
`required_centered_pair_sum_to_rescue <= -0.8982746156725305` and active
real-channel normalized `Linf <= 0.05885324711081062`.  On the selected rows,
exactly `1222142`, `1323632`, and `1379072` satisfy both assumptions and are
rescued; `14138` satisfies neither.  This is a conditional implication
check, not a proof of floor stability, pointwise channel control, or
Goldbach.

New receipt
`q286_lower_support_component_pair_floor_stability_decomposition_receipt`
decomposes the floor-stability half.  Focused regression
`test_q286_lower_support_component_pair_floor_stability_decomposition` passed
in `121.972s`.  The selected sufficient term conditions are:
`required_lower_support_package_to_rescue <= -0.6751407665271594` and
`non_pair_lower_support_actual + component_pair_local_mean >=
0.2231338491453711`.  The three late comparison targets satisfy both
conditions; `14138` satisfies neither.  This is still finite decomposition
evidence, not an eventual floor-stability theorem.

New receipt `q286_lower_support_component_pair_floor_identity_receipt`
collapses that bookkeeping into an exact identity.  Focused regression
`test_q286_lower_support_component_pair_floor_identity` passed in `118.879s`.
The selected floor-stability half is equivalent to:
`first_three + q286_after_first_three + non_pair_lower_support_actual +
component_pair_local_mean >= -0.1017253843274695`.  `14138` has combined
driver `-0.7243980058138082`, while `1379072` sits on the selected floor.
This is an exact selected identity, not an eventual lower-bound theorem.

New receipt
`q286_lower_support_component_pair_combined_driver_channel_closure_receipt`
packages the clean conditional closure.  Focused regression
`test_q286_lower_support_component_pair_combined_driver_channel_closure`
passed in `121.404s`.  The two assumptions are combined driver
`>= -0.1017253843274695` and active real-channel normalized
`Linf <= 0.05885324711081062`.  Together they force selected centered-pair
rescue.  The three late comparison targets satisfy both; `14138` satisfies
neither.  Proving these assumptions eventually remains open.

New receipt `q286_lower_support_component_pair_action_identity_receipt`
verifies the direct identity
`full_action/P = 1 + combined_driver + centered_pair_sum`.  Focused
regression `test_q286_lower_support_component_pair_action_identity` passed in
`114.284s`, with reconstruction error below `1e-12`.  On the selected rows,
the identity-positive, actual-positive, and conditional-closure targets are
exactly `1222142`, `1323632`, and `1379072`; `14138` remains negative.

New receipt
`q286_lower_support_component_pair_closure_margin_profile_receipt` records
selected margins against the clean assumptions and now reports the strict
conditional closure scalar `driver_margin + L * channel_margin`, where
`L = 15.262957606760978` is the active real-channel L1/principal mean.
Focused regression
`test_q286_lower_support_component_pair_closure_margin_profile` passed in
`139.808s`.  Boundary target `14138` has strict closure margin
`-3.782909118497761`, while late positives have positive margins:
`1222142` has `0.5506633762515991`, `1323632` has
`0.546820393849208`, and `1379072` has `0.48379401372791037`.  This turns
the two-assumption closure into one executable slack diagnostic; proving it
positive on the whole active lane remains open.

New receipt
`q286_lower_support_component_pair_channel_pressure_profile_receipt` identifies
the real-channel labels responsible for selected Linf pressure.  Focused
regression
`test_q286_lower_support_component_pair_channel_pressure_profile` passed in
`124.495s`.  The boundary target `14138` is worst overall at label
`(1,1,0,0)` with normalized sum `0.2659059415120284`, missing the channel
bound by `-0.20705269440121776`.  Among late positives, `1379072` has the
largest single-channel pressure at `(0,3,3,0)`, normalized sum
`0.027155981994015317`, while still clearing the selected bound by
`0.031697265116795305`.  This is finite pressure profiling only, not a
pointwise channel theorem.

New receipt
`q286_lower_support_component_pair_channel_conductor_profile_receipt` then
records the conductors of the active real channels.  Focused regression
`test_q286_lower_support_component_pair_channel_conductor_profile` passed in
`118.119s`.  All `16` channels have conductor `35` or `77` (`4` and `12`
channels respectively), and none uses the factor `13`.  The boundary pressure
label `(1,1,0,0)` has conductor `35`; the worst late-positive pressure label
`(0,3,3,0)` has conductor `77`.  This narrows the pointwise channel estimate
to fixed-conductor twisted binary-Goldbach control on adjacent conductors,
not a full modulus-`10010` theorem.

New receipt
`q286_lower_support_component_pair_fixed_conductor_reduction_receipt`
reconstructs each selected active period-`10010` channel sum from
strict-central discrepancy aggregated modulo its own conductor.  Focused
regression
`test_q286_lower_support_component_pair_fixed_conductor_reduction` passed in
`162.840s`, with character reduction error below `1e-8` and residue-character
consistency error below `1e-12`.  The boundary pressure label `(1,1,0,0)`
reconstructs at conductor `35` with normalized sum `0.2659059415120284`; the
worst late-positive pressure label `(0,3,3,0)` reconstructs at conductor `77`
with normalized sum `0.027155981994015317`.  The unresolved theorem is now a
fixed-conductor twisted binary-prime discrepancy estimate on those adjacent
conductors, not merely a formal lcm-period identity.

New receipt
`q286_lower_support_component_pair_fixed_conductor_residue_pressure_receipt`
profiles the residue aggregates behind the fixed-conductor sums.  Focused
regression
`test_q286_lower_support_component_pair_fixed_conductor_residue_pressure`
passed in `208.170s`.  The simple residue triangle route is too crude:
boundary `14138` has worst residue Linf pressure at conductor `35`,
`0.05327502632021343`, giving plain Linf triangle bound
`1.2786006316851224`; the worst residue L1 row is `14138` at conductor `77`,
`0.4624962038193246`.  Even late-positive `1379072` at conductor `77` has
plain Linf triangle bound `0.2187090564566816`, above the needed channel
bound `0.05885324711081062`, although its actual active channel normalized
sum is only `0.027155981994015317`.  Therefore the fixed-conductor theorem
must use cancellation inside the character sums, not just max residue
aggregate control.

New receipt
`q286_lower_support_component_pair_fixed_conductor_character_cancellation_receipt`
measures the cancellation ratio between actual active character sums and the
plain residue envelopes.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_character_cancellation`
passed in `180.890s`.  The least-cancelled selected channel is still boundary
`14138`, label `(1,1,0,0)`, conductor `35`, with actual/linf-triangle ratio
`0.20796637739931306` and actual/l1-triangle ratio `0.713179126554023`.
The worst late-positive actual channel is `1379072`, label `(0,3,3,0)`,
conductor `77`, with actual normalized sum `0.02715598199401531`,
actual/linf-triangle ratio `0.12416487197179206`, and actual/l1-triangle
ratio `0.3153405593261632`.  This clears the channel bound even though the
plain residue triangle bound fails, so the viable channel theorem must retain
fixed-conductor character cancellation.

New receipt
`q286_lower_support_component_pair_fixed_conductor_reflection_orbit_receipt`
tests pair-swap reflection after fixed-conductor aggregation.  Focused
regression
`test_q286_lower_support_component_pair_fixed_conductor_reflection_orbit`
passed in `217.106s`.  Reflection-orbit triangle compression clears selected
late positives `1222142` and `1323632`, but not `1379072`.  The worst
late-positive reflection envelope is `1379072`, label `(0,2,6,0)`, conductor
`77`, with reflection-orbit L1 `0.06039386426228221`, missing the channel
bound by `-0.0015406171514715863`.  The worst selected envelope remains the
boundary row `14138`, label `(0,1,3,0)`, conductor `77`, with orbit L1
`0.3296060502917276`.  This makes the live channel-side theorem smaller
again: prove residual cross-orbit cancellation, or sharpen the reflection-
orbit bound, for conductor `77` near the driver-bound row.

New receipt
`q286_lower_support_component_pair_fixed_conductor_residual_orbit_cancellation_receipt`
measures the signed cancellation remaining after reflection-orbit compression.
The corrected focused regression records two positive reflection-envelope
failures, both at `1379072` and conductor `77`: label `(0,1,5,0)` has actual
sum `0.005352592501155273` versus orbit L1 `0.05943056357350034`, while label
`(0,2,6,0)` has actual sum `0.01746105205795644` versus orbit L1
`0.0603938642622822`.  Both clear the channel bound by signed cross-orbit
cancellation.  This is the current narrowest channel-side target: prove or
replace a residual signed orbit-cancellation estimate for the conductor-`77`
driver-bound row.

New receipt
`q286_lower_support_component_pair_fixed_conductor_orbit_polygon_receipt`
expresses the two residual conductor-`77` failures as exact complex-vector
polygons.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_orbit_polygon` passed
in `351.969s`.  Both residual rows at `1379072` have `38` reflection-orbit
edges.  Label `(0,1,5,0)` has perimeter `0.059430563573500336` but resultant
only `0.0053525925011552716`, closure ratio `0.09006464316185543`.  Label
`(0,2,6,0)` has perimeter `0.0603938642622822`, resultant
`0.01746105205795644`, closure ratio `0.289119636096235`.  This converts the
visual/geometric hunch into a falsifiable theorem target: bound alignment of
the conductor-`77` orbit-polygon edges on the active driver-bound rows.

New receipt
`q286_lower_support_component_pair_fixed_conductor_orbit_phase_profile_receipt`
measures phase-bin balance for those two polygon rows.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_orbit_phase_profile`
passed in `283.200s`.  With `12` phase bins, label `(0,1,5,0)` occupies
`11` bins and has largest-bin fraction `0.132562039245484`; label `(0,2,6,0)`
occupies `10` bins and has largest-bin fraction `0.26794815278810286`.
This preserves the visual/geometric route as a concrete theorem target:
phase-bin mass balance plus signed cancellation between bins.

`q286_lower_support_component_pair_fixed_conductor_phase_bin_compression_receipt`
tests whether the signed phase-bin envelope alone clears those residual
polygons.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_bin_compression`
passed in `209.826s`.  The signed phase-bin bound clears label `(0,1,5,0)`:
signed-bin L1 `0.058765359273537675` versus channel bound
`0.05885324711081062`, margin `0.000087887837272945`.  It still misses the
harder label `(0,2,6,0)`: signed-bin L1 `0.06015000330167732`, margin
`-0.001296756190866699`.  Thus coarse phase-bin compression is not a proof
engine by itself; the remaining narrow theorem target is inter-bin signed
cancellation or a sharper phase-balance estimate for the single hard
conductor-`77` row.

`q286_lower_support_component_pair_fixed_conductor_phase_antipodal_compression_receipt`
pairs opposite phase bins in the same residual polygons.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_compression`
passed in `218.344s`.  Antipodal pairing clears both residual rows:
label `(0,1,5,0)` has antipodal-pair L1 `0.009229827584054894`, margin
`0.049623419526755724`; the hard label `(0,2,6,0)` has antipodal-pair L1
`0.03657040255445905`, margin `0.022282844556351572`.  The live visual
theorem target is therefore not arbitrary phase-bin compression but antipodal
phase-sector cancellation for the conductor-`77` residual orbit polygons.

`q286_lower_support_component_pair_fixed_conductor_phase_antipodal_pair_balance_receipt`
then checks whether each opposite-sector pair cancels uniformly.  Focused
regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_pair_balance`
passed in `252.478s`.  This falsifies the uniform per-pair version: the hard
label `(0,2,6,0)` has weighted antipodal cancellation ratio
`0.6079867090121881`, largest pair abs `0.015424610859844602`, largest pair
cancellation ratio `0.9711661073614952`, and `2` high-ratio pairs at threshold
`0.75`.  The theorem target is therefore the weighted six-pair antipodal L1
bound, not a claim that every opposite-sector pair individually cancels well.

`q286_lower_support_component_pair_fixed_conductor_phase_antipodal_threshold_envelope_receipt`
splits that weighted bound into explicit high-ratio exceptions plus a
thresholded envelope for the remaining pair mass.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_threshold_envelope`
passed in `395.264s`.  With threshold `0.75`, the envelope
`sum(high-ratio pair abs) + 0.75 * sum(remaining pair source mass)` clears both
residual rows.  The hard label `(0,2,6,0)` has thresholded envelope
`0.049789406359944485`, margin `0.009063840750866137`; label `(0,1,5,0)` has
thresholded envelope `0.044857036354937124`, margin
`0.013996210755873498`.  This is the current sharpest proof-shaped
decomposition of the residual conductor-`77` visual route.

`q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_exception_receipt`
checks the high-ratio exceptions in that envelope.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_exception`
passed in `210.678s`.  With thin-side ratio threshold `0.05`, all selected
high-ratio exceptions are one-sided: label `(0,1,5,0)` has maximum
small/large side ratio `0.0` and high-ratio exception abs sum
`0.0031320675991354753`; hard label `(0,2,6,0)` has maximum small/large side
ratio `0.046829417626061014` and high-ratio exception abs sum
`0.024020095646099474`.  The high-ratio part of the theorem target is now
thin opposite-sector mass control.

`q286_lower_support_component_pair_fixed_conductor_phase_antipodal_exception_budget_receipt`
states the explicit thin-exception budget after the non-thin pair envelope.
Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_exception_budget`
passed in `391.565s`.  With
`allowed exception abs = channel_bound - 0.75 * low-ratio pair mass`, label
`(0,1,5,0)` may spend `0.01712827835500897` on high-ratio thin exceptions,
spends `0.0031320675991354753`, and has margin
`0.013996210755873494`.  The hard label `(0,2,6,0)` may spend
`0.033083936396965614`, spends `0.024020095646099474`, and has margin
`0.00906384075086614`.  The current sharpest visual theorem target is now a
two-part inequality: non-thin antipodal pairs satisfy the fixed-ratio bound,
and thin opposite-sector exceptions stay below the displayed absolute budget.

`q286_lower_support_component_pair_fixed_conductor_phase_antipodal_nonthin_ratio_receipt`
checks the non-thin side of that inequality directly.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_nonthin_ratio`
passed in `210.885s`.  With thin-side threshold `0.05` and ratio bound `0.75`,
label `(0,1,5,0)` has `5` non-thin pairs, non-thin mass
`0.05563329167440221`, non-thin abs `0.006097759984919418`, and maximum
non-thin ratio `0.2161610623897297`.  The hard label `(0,2,6,0)` has `3`
non-thin pairs, non-thin mass `0.03435908095179335`, non-thin abs
`0.012550306908359576`, and maximum non-thin ratio `0.6626326478324716`,
leaving margin `0.08736735216752844` to the `0.75` bound.

`q286_lower_support_component_pair_fixed_conductor_phase_antipodal_sector_geometry_receipt`
then replaces the measured non-thin ratio with a sector-geometry envelope.  In
`12` phase bins, opposite sectors are separated by at least `5*pi/6`, so the
sector cosine bound is `-0.8660254037844387`.  Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_sector_geometry`
passed in `240.891s`.  Label `(0,1,5,0)` has maximum sector-envelope ratio
`0.3325400441705825`, margin `0.4174599558294175` to the `0.75` bound.  The
hard label `(0,2,6,0)` has maximum sector-envelope ratio
`0.6862033816719031`, margin `0.06379661832809691`.  Thus, on the selected
fixture, the non-thin half of the two-part inequality is explained by
phase-sector separation plus side-balance.

`q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_budget_receipt`
then turns the selected thin-exception budget into a large-side mass budget.
Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_budget`
passed in `614.609s`.  Since selected high-ratio exceptions have small side at
most `0.05` times the large side, `(1.05) * large-side mass` clears the allowed
exception budget for both residual rows.  Label `(0,1,5,0)` has large-side
mass `0.0031320675991354753`, envelope `0.0032886709790922493`, and margin
`0.01383960737591672`.  The hard label `(0,2,6,0)` has large-side mass
`0.02490542589058863`, envelope `0.026150697185118062`, and margin
`0.006933239211847552`.  This reduces the selected thin-exception side to
large-side mass control; it is not a uniform theorem or a Goldbach proof.

`q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_support_receipt`
then profiles the support of the selected thin large-side mass.  Focused
regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_support`
passed in `403.837s`.  Across selected high-ratio thin exceptions, large-side
mass occurs only in phase bins `4,5,7`: label `(0,1,5,0)` has exception pair
`(1,7)` with large side in bin `7`, while the hard label `(0,2,6,0)` has
exception pairs `(4,10)` and `(5,11)` with large sides in bins `4,5`.  Thus a
single-orientation large-side proof is finitely falsified; the remaining
support-shaped target is explicit thin exception bin-pair mass control.

`q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_edge_support_receipt`
then profiles the reflection-orbit edges inside those large-side bins.
Focused regression
`test_q286_lower_support_component_pair_fixed_conductor_phase_antipodal_thin_large_side_edge_support`
passed in `415.057s`.  The selected thin large-side bins are not single-edge:
edge counts are `3`, `5`, and `2`; the hard `(4,10)` bin has five edges and
largest-edge ratio `0.4406627296301651`.  Leading orbits are `(3,76)`,
`(26,53)`, and `(6,73)` for bin pairs `(1,7)`, `(4,10)`, and `(5,11)`.
Thus the one-edge shortcut is finitely falsified; the surviving target is
small explicit reflection-orbit mass/cancellation control.

`q286_lower_support_component_pair_fixed_inequality_stress_receipt` now freezes
that route as one finite quantified inequality with unchanged constants:
`(1 + thin_side_ratio_threshold) * thin_large_side_mass <= channel_bound -
ratio_bound * low_ratio_pair_mass`, with `phase_bin_count = 12`,
`ratio_bound = 0.75`, and `thin_side_ratio_threshold = 0.05`.  The focused
regression `test_q286_lower_support_component_pair_fixed_inequality_stress`
now checks both buckets and passed in `282.271s`: the active pair
`((5,7),(7,11))` evaluates two residual polygon rows with no counterexample
and worst margin `0.006933239211847554`, while `((5,),(7,))` is correctly
classified as `not_applicable_no_residual_polygons`.

The full anti-cherry-pick component-pair census is now recorded in
`evidence/q286-fixed-inequality-21pair-census.json`.  On the predeclared target
fixture `14138,1222142,1323632,1379072`, all `21` unordered lower-support
component pairs completed with zero errors.  Only one pair was applicable:
`((5,7),(7,11))`, and it passed with two residual polygon rows, zero failures,
and worst margin `0.006933239211847554`; the other `20` pairs were
`not_applicable_no_residual_polygons`.  Therefore the census gives no
counterexample to the fixed inequality, but it is not broad reinforcement:
the inequality is active only on the already-identified residual-polygon lane.

`q286_lower_support_component_pair_fixed_inequality_target_census_receipt`
now audits the target denominator for that same fixed inequality.  It declares
the target source, selects all targets satisfying
`first_two < -0.2` and `first_three < -0.3`, then classifies each stressed
target as passed, failed, not-applicable, or error.  The focused regression
`test_q286_lower_support_component_pair_fixed_inequality_target_census` passed
in `278.805s` on the known active target and marks caller-supplied targets as
non-neutral.  The compact selector-driven probe in
`evidence/q286-fixed-inequality-target-window-census.json` scanned
`1379072,1379074,1379076,1379078,1379080`, selected exactly `1379072`, and
found one passing evaluated target with two residual polygon rows, zero
failures, and zero errors.  This reduces target cherry-picking ambiguity only
inside a tiny local active window; it is not a broad sample, a uniform theorem,
or evidence that Goldbach is proved.

`q286_lower_support_component_pair_tail_selector_grid_receipt` now separates
broad target-denominator scanning from the expensive fixed-inequality stress
stack.  The focused regression
`test_q286_lower_support_component_pair_tail_selector_grid` passed in
`35.441s`.  The selector-only grid in
`evidence/q286-tail-selector-grid-6x25.json` scanned `150` predeclared targets
across starts `1000000,1010010,1020020,1030030,1040040,1050050` and found
zero targets satisfying the active `first_two < -0.2` and `first_three < -0.3`
predicate.  This is denominator evidence only: no fixed-inequality stress rows
were generated, so it is not support for the inequality.

The active-residue holdout in
`evidence/q286-tail-selector-active-residue-holdout-6x5.json` then scanned
the six same-residue q286-period shifts immediately after the known
`1379072` hit: starts `1389082,1399092,1409102,1419112,1429122,1439132`, five
targets each.  It found zero active tail targets across `30` scanned targets.
This suggests the known active row is not trivially periodic in the next six
same-residue windows, but no fixed-inequality rows were stressed and no
theorem is proved.

`q286_active_lane_strict_closure_margin_census_receipt` now applies the fixed
strict closure scalar to targets selected by a predeclared active-lane window,
while keeping the closure constants calibrated from
`14138,1222142,1323632,1379072`.  Focused regression
`test_q286_active_lane_strict_closure_margin_census` passed in `259.586s`.
The evidence file
`evidence/q286-active-lane-strict-closure-margin-census-1379072-window.json`
records the compact active window `1379072,1379074,1379076,1379078,1379080`:
one selected tail target, `1379072`, with calibrated strict closure margin
`0.48379401372791037`.  This is finite selected-window evidence only; the
universal active-lane strict-margin theorem remains open.

Public-source check on 2026-09-13: the closest visible literature remains
Goldbach representations in arithmetic progressions and their relation to
zeros of Dirichlet L-functions/RH-type statements, not a ready-made pointwise
fixed-modulus theorem for this `16`-channel target.  See
`notes/q286-component-pair-theorem-obligation.md` for the current source
context and links to arXiv:1704.06103, arXiv:1809.06920, and arXiv:1212.4406.

Additional closure: `q286_lower_support_component_pair_reflection_support_geometry_obstruction_receipt`
enforces the ordered prime-pair symmetry `w(r)=w(N-r)` on the artificial
support obstruction.  Focused regression
`test_q286_lower_support_component_pair_reflection_support_obstruction` passed
in `34.893s`.  All `5005` even residues modulo `10010` remain obstructed, with
maximum reflection weight error `0`.  Therefore pair-swap symmetry alone does
not prove the component-pair exclusion; the missing theorem must use sharper
prime-pair arithmetic.

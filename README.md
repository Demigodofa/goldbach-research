# Goldbach redistribution research

Owner: Kevin; research and integration: Rill (`agent.rill`).
Purpose: investigate a sequence of small proved statements that could help explain
prime-pair coverage of even integers. This is a research record, not a claimed
proof of Goldbach. Retain checked proofs, source references,
reproducible experiments, counterexamples, and precise remaining questions.

## Active goal

Kevin withdrew the six-hour cutoff on 2026-09-08 and invited Rill to choose
the goal. The chosen direction is a new proof method for prime-pair coverage,
with Goldbach as the ultimate target: prove whole families of even numbers
have prime pairs, then seek a proof that the families cover every sufficiently
large even number. The current controlling contract is `RESEARCH_GOAL.md`.
The research has no current wall-clock deadline. Individual hypotheses still
receive bounded tests and explicit decisions, so an unproductive approach
does not consume an unlimited run. Preserve checked results and precise gaps.
The first milestone is an independently checked theorem with a bounded
prior-art assessment; worldwide novelty and a complete Goldbach proof are
not established. Any eventual external submission requires Kevin's approval.
Kevin authorized publication of this repository on public GitHub on 2026-09-10.
No spending or contacting others. Use background execution only. Do not change
unrelated projects or user files.

Original start: 2026-09-08 03:22:30 UTC; original deadline: 09:00 Eastern.
Execution audit after resumption: the sustained run through09:00 was not
fulfilled. Project activity is recorded through03:07 Eastern and resumes
around12:46 Eastern. The root acknowledged the misleading implication of
continued overnight work. See `notes/execution-gap-2026-09-08.md`; an active
goal flag must not be treated as evidence that execution continued. The
native goal text retains that earlier deadline because its available update
interface changes terminal status only; Kevin's latest instruction and the
current contract control scope. See `notes/six-hour-renewal-2026-09-08.md`.

## Current mathematical checkpoint (2026-09-10)

The assembled divisor-frame argument still reaches
`N^.15<a<=N^(.295-delta)` for every fixed `delta>0`. Later exact
factorizations isolate the dominant unresolved high-conductor error into
squarefree conductor, common-part, and residual coordinates.

For every fixed common part `c|d` with `d*c>B*V`, the residual collapse is now
proved polylogarithmic:

    |sum_r K_(d,c,r)|^2
      <= (1+log(B^2/(d*c)))^6 sum_r |K_(d,c,r)|^2.

The proof uses a retained `r=1` base pair, at most `3^omega(r)` residual
assignments, and a `tau_3` harmonic bound. Under the stronger condition
`d>B*V` (and `X>B`), a second theorem gives `2^omega(c)A_c<=A_1` and
therefore controls the separated base energy by `(5/4)^omega(d)A_1^2`.
Independent review passed both arguments.

The fixed-layer theorem now combines with a global pair-mass argument. The
positive common cells partition the ordered pairs of each lcm `q`; cellwise
Cauchy followed by `sum_(d|q)H_m(d)=q^2v_(m,q)` returns their entire
`d>B*V` contribution to the already-proved diagonal Cauchy envelope. Hence
the complete-period high-conductor component is controlled, up to a subpower
factor, by the existing frame estimate without lower-bounding a signed common
layer.

The actual common layers carry Mobius signs. Exact project-scaled witnesses
show their combined base can nearly vanish, refuting a proposed pointwise
`4^omega(d)` comparison. For `d>B*V`, the new pair-mass argument bypasses
that pointwise obstruction. The transition conductors and incomplete-row
covariance still require control. The signed prime-correlation estimate and
Goldbach remain open. Read the final
sections of `REFRESH_HANDOFF.md` and `RESEARCH_GOAL.md` for exact quantifiers,
witnesses, validation, and the next question.

## Starting facts

Goldbach asks whether every even N >= 4 is the sum of two primes.
Given N = p + q, a redistribution to N + 2 has the form

    (p, q) -> (p + 2k, q + 2 - 2k), k an integer.

For odd primes both target primes must also be odd (apart from the base 4).
Adding 2 to just one member is insufficient: 38 has only (7,31) and (19,19),
and every direct extension contains 9,33, or21. Yet 40 has (3,37), (11,29),
and (17,23). This is a counterexample to a proposed transition rule, not to
Goldbach. The separate base transition 4 -> 6 also cannot use an even shift.

## Evidence rules

- Mark claims proved, externally established, computationally checked,
  conjectured, or refuted. Numerical ranges never imply universal proofs.
- Every new hypothesis states its quantifiers, mechanism, prediction,
  falsifier, and the smallest relevant test.
- Distinguish repairing every chosen pair from existence of some repairable
  pair. These have different quantifiers.
- Preserve useful components of refuted proposals. Call novelty only
  new-to-this-task unless a bounded prior-art search justifies more.
- Critical mathematical claims receive a fresh bounded review.

## Initial research lanes

Rill owns code, experiments, integration, and this notebook. A bounded theory
reviewer may assess the existence of a universal fixed redistribution radius.
Reviewer is read-only and returns exact statements and proofs to Rill; it must
not spawn another reviewer or run a second open-ended investigation. Use public
primary mathematical sources. No GUI or signed-in accounts are needed.
First review checkpoint: a finite-window theorem or a precise reason the proposed
proof fails. Model routing receipt: conserve, at most two spawned lanes;
Sol retained for mathematical verification, Terra/high for ordinary research.

The finite-radius theorem review is complete. The same read-only Sol lane now
reviews the interval-count and AP-sum certificate proofs and code. A second,
read-only Terra/high lane `prime_ladder_sources` locates the exact Helfgott/Platt
prime-ladder coverage transfer and the binary Goldbach computation precedent.
Root alone edits files. Both return bounded reports, not further agents; their
review checkpoints are 10 and 15 minutes respectively. Public sources only,
no browser/account ownership or GUI input, no spending or publication.

## Startup exceptions

The `py` launcher is absent; Python 3.11 is available as `python`.
The compiled startup receipt had no Goldbach capability route. Use the direct
bounded Academy capsule and the task's exact mathematical sources instead.
The local Qwen default runtime manifest is absent at
`C:\Users\benja\tools\qwen-cmd-assistant\runtime.json`; strict runtime validation
therefore cannot pass. Record the exception and do not install a multi-gigabyte
runtime merely for this mathematical task. No local-Qwen contribution is claimed.

## Research record and navigation

The current next action is maintained at the end of `REFRESH_HANDOFF.md` and
`RESEARCH_GOAL.md`. The historical record begins with a fixed-radius question,
which has a checked negative theorem; the adaptive
displacement-4 observation has been identified as a stronger conjecture.
The active direction follows Kevin's later steering: stacked1,000-number
blocks and calculation-based elimination of certified spans.

- `notes/checked-results.md`: starting results and research questions.
- `notes/interval-certificate-proof.md`: a genuine small interval proof.
- `notes/stacked-certificate-proof.md`: the three finite stages and limits.
- `notes/prime-ladder-precedent.md`: published successful stacking and its
  ternary-versus-binary boundary.
- `notes/review-receipts.md`: independent review and verifier corrections.
- `notes/paired-wheel-intervals.md`: gap-based Z and its stacking inequality.
- `notes/exclusion-moment-certificates.md`: staged CRT counts, sharper
  polynomial bounds, and exact information-loss examples.
- `notes/location-and-parity.md`: partition improvement and general truncated
  intersection countermodels.
- `notes/cubic-three-stage-identity.md`: a proved fixed-stage exact count,
  with the remaining uniform positivity requirement stated separately.
- `notes/central-crt-error-budget.md`: proved elementary count/error bounds
  and a measured explanation of why their worst-case errors do not finish it.
- `notes/exceptional-set-scope.md`: why selected almost-all and interval
  hitting theorems do not identify a whole block as certified.
- `notes/packed-block-certificate.md`: a proved integer-square and simultaneous
  nonzero-digit Z, with finite reuse into successive1,000-target blocks.
- `notes/relative-block-convolution.md`: the same exact collective check
  using a short relative polynomial near distant targets.
- `notes/disproof-directed-prime-gaps.md`: proved counterexamples to every
  fixed logarithmic palette, with a checked finite stress interval.
- `notes/smaller-input-count-recurrence.md`: corrected exact-count inversion
  and the smaller prime inputs required by residual correlations.
- `notes/fixed-distance-nine-obstruction.md`: an infinite representable
  stress family with fixed nearby-prime distance and unbounded minimum addend.
- `notes/count-bootstrap-proof.md`: a proved output-fed count pipeline,
  implemented from the canonical base through three new1,000-target stages.
- `notes/cubic-margin-structure.md`: the exact prime/semiprime meaning of
  the raw margin and the missing reflected-correlation bound.
- `notes/subpower-presieve-obstruction.md`: why subpower first-stage cutoffs
  eventually fail the raw-union certificate on powers of2.
- `notes/two-moment-block-certificate.md`: an exact weighted two-moment
  collective certificate, its finite successes, and its correlation gap.
- `notes/fixed-precision-weight-obstruction.md`: proved local count peaks
  and the failure of every fixed dynamic range of block weights.
- `notes/adaptive-moment-almost-all.md`: a checked almost-all guarantee
  for adaptive target-only weights, with exceptional starts left explicit.
- `notes/local-peak-prior-art-check.md`: bounded comparison and the
  unconfirmed external novelty of these deductions.
- `evidence/block-*.json`: representative complete block certificates.

The1,000-block composition run completed: all1,000,000 even targets from4
through2,000,002 were certified. The retained representative blocks also pass
the hardened verifier under optimized Python. Carrying AP certificates into
the next block settled56 of10,000 sample targets before fresh generation;
that sample was slightly slower overall, so no speed advantage is claimed.

The exact paired-wheel computation through prime13 gives maximum gaps
2,6,18,30,66,150, matching the published first six values. A prime-safe-window
theorem converts these into overlapping certified target intervals covering
8 through426 (4 and6 have explicit base pairs). Sol reviews the interval
theorem; the carry and primary-source lanes are complete.

The next phase implemented target-specific CRT exclusion counts. All1,000
evens6 through2004 receive a positive count lower bound by degree4 using
the complete real moment-LP polynomial family and a split-product cap.
For181 targets, exact integer countermodels show that the first three aggregate
moments alone cannot force a survivor. Their actual fourth moments resolve
the ambiguity. These countermodels do not preserve modular geometry and are
not Goldbach counterexamples. Twenty-four tests pass normally and under
optimized Python; both1,000-target receipts match independent prime counts.

The fixed degree4 rule then failed at4412: its first four overlap moments
also admit an explicit integer zero-survivor countermodel. The actual window
has88 prime pairs; degree5 proves at least67. This refutes the fixed-degree
interface while preserving the moment machinery.

Keeping eight disjoint candidate windows rescues4412 at the same degree4,
with a total lower bound4 ordered survivors. It costs more arithmetic. The
proved partition inequality explains why retaining location can strengthen
the bounds; an abstract parity construction shows why fixed truncated event
data alone cannot generally decide survivor existence.

A subsequent cube-root presieve yields a stronger structural reduction: every
remaining composite argument is semiprime and meets exactly one residual
square-start event. Hence every candidate meets at most two residual events,
and `G(N)=M-S1+S2` is an exact ordered Goldbach-count identity for every even
N>=6, with G(4)=1 separate. This is a proved counting identity, not a proof
that its value is always positive. The first stage must retain survivor
locations, and its prime inputs grow with N. Full counts through2002 and
representative targets through1,000,000 match independent prime sieves.
Thirty-five tests pass normally and under optimized Python.

The bounded raw-margin search completed2004 through20,000 with no failure.
Together with the first block, `M-S1>0` is checked for all evens4 through20,000;
this is a finite observation only. Its receipt is
`evidence/cubic-union-bound-scan-20000.json`. No shell job remains running.

The central-window CRT bounds are now proved and implemented. At N=1,000,000,
the first-stage estimate is25,030.946 versus an exact25,166, but the elementary
absolute error allowance is188,286,357,653. This bound cannot establish a
positive first-stage count. The diagnostic does not show large actual errors;
it exposes the loss from summing their worst-case absolute values. A check of
specific standard lower-sieve parameters also gives no automatic replacement.
The prime number theorem additionally proves that this same crude allowance
eventually exceeds N for every target, so the unchanged bound cannot be an
eventual certificate. The complete39-test suite passes normally and under
optimized Python; independent code review found no material issue.

Selected exceptional-set and interval-hitting theorems were also checked:
they bound unnamed exceptions or guarantee one member, and do not certify
every target in a named block.

The collective certificate is now proved and implemented: encode the
odd-prime polynomial in carry-free digits, square it, then use a borrow-free
sentinel subtraction to test all1,000 counts together. Three successive
blocks6..6004 reuse prior square output and all pass; a separate block
1,000,000..1,001,998 also passes. Every receipt replays exactly. This is a
finite batch mechanism, not an unbounded positivity proof.

The relative product is also complete. With167 odd palette primes and a
2,993-integer nearby segment, it certifies1,000-target blocks beginning at
one million, one billion, and one trillion. Prime inputs and every restricted
coefficient were independently checked, and all receipts replay. The complete
53-test suite passes normally and under optimized Python.

Kevin's latest steering prioritizes attempts to disprove proposed rules and
mathematically select difficult cases. The prime-gap obstruction is now
proved: every fixed C*log(N) small-prime cap fails infinitely often. The
checked gap492113..492227 defeats cap100 on all seven evens492214..492226,
and every one has an independently verified larger-prime pair. This defeats
the narrower palette rules, not Goldbach.

The count-prefix reconstruction is now implemented: exact counts for all
1,000 evens6..2004 recover the prime flags3..2001. Its five tests also prove
the semantic limit: algebraically consistent binary inputs are not themselves
primality evidence, and positivity booleans discard needed information.

A stronger stress theorem is now proved. For every fixed K, infinitely many
Goldbach-representable targets have preceding-prime distance exactly9 but
minimum addend>K. CRT supplies a reduced prime progression, fixed-modulus
PNT counts it, and the Goldbach exceptional-set bound is too small to cover
it. K and the modulus must stay fixed before the asymptotic limit. Explicit
targets4,304,318 and1,420,043,880,008 have minimum addends127 and277 respectively,
despite distance9 in each case. Their receipts include exact prime checks
and proper divisors for all smaller candidate complements.

A frozen adversarial comparison tested whether large minimum addends select
weak normalized cubic margins `(M-S1)/M`. Stress targets492218,492224,4304318
were each compared with four controls at offsets +/-210 and +/-420, keeping
the residue modulo210. Their ascending ranks were3,2,5 out of5; only one was
below its control median. Thus this small descriptive comparison does not
support using the minimum addend alone to select weak raw margins. All15
exact counts matched an independent monolithic prime sieve. The receipt is
`evidence/raw-margin-adversarial-comparison.json`; this is not a statistical
significance or universal-selector claim. The complete62-test suite passes
normally and under optimized Python, and independent Sol review found no
material issue in the count reconstruction or fixed-distance construction.

The output-fed count pipeline is now proved and implemented. Exact counts
through even B recover primes through B-3 and suffice to generate counts
through the safe next endpoint (B-1)^2+1. The executed chain6->26->626->2626
->4626->6626 contains three new1,000-target blocks, whose minimum ordered
counts are20,56,100. All3,311 counts through6626 match independent trial-prime
pair counts, and the compact receipt replays from canonical G(6)=1. The
complete69-test suite passes normally and under optimized Python. This proves
correct count generation, including any possible future zero, not positivity.

The cubic raw margin has a precise class interpretation: R=M-S1 equals the
number of prime-prime candidates minus semiprime-semiprime candidates having
distinct least factors. Moving residual events into the presieve adds the
covered pair intersections; beyond sqrt(N/2) it makes the raw formula exact
but leaves positivity equivalent to Goldbach. The same-factor correction is
unconditionally O(N^(2/3)). Buchstab's one-variable rough-number theorem
motivates a heuristic positive margin but does not control the reflected
pair correlation. A finite labelled-set countermodel demonstrates why its
favourable marginal prime fraction alone cannot prove the desired claim.

A scaling obstruction now narrows the choice of first-stage cutoff. For
N tending to infinity through powers of2 and any z>=2 with log(z)/log(N)->0,
the raw bound R_z eventually becomes negative. The proof combines the
combinatorial inequality R_z<=2Q_z-M_z with dimension-two and prime-supported
dimension-one sieve estimates; the latter uses Bombieri-Vinogradov. It does
not assume Goldbach. The cubic cutoff z=N^(1/3) is outside this obstruction.
A frozen13-target comparison independently verifies the finite effect:
N65536 at cutoff16 has raw-284 and actual ordered count870, while its cubic
cutoff40 gives raw672. At N1048576 the logarithmic and cubic raw bounds are
-13570 and6218, with actual count8478. The full73-test suite passes normally
and under optimized Python. No negative raw bound is a Goldbach disproof.

Before execution stopped, the weighted two-moment experiment was completed.
For m nonnegative weighted counts, S=sum(x),T=sum(x^2), the exact test
S^2>(m-1)T certifies allm positive. Weights depend only on each target's
distinct odd prime factors. It certifies the1,000-target blocks beginning
at100000 and1000000; the block beginning10000 certifies after one split into
two500-target halves. All3,000 counts and both split moments were checked
independently and the receipts replayed. Current production still computes
the individual counts before aggregating them; no analytic moment bounds
or unbounded positivity theorem were established. The full79-test suite
passed normally and under optimization after the12:46 Eastern resumption.

Next formulate a falsifiable surviving rule that uses more arithmetic
information, and choose adversarial inputs against it. Fixed palettes,
fixed-constant logarithmic palettes, and bounds depending only on distance
to the preceding prime have been ruled out as universal guarantees. The
exact cubic count identity survives; its uniform positive lower bound is
still unproved. No Goldbach counterexample has been found. No shell job is
running. The earlier full residual recurrence is no longer the preferred
computational task: the simpler count bootstrap now implements dependence
on earlier count output. The remaining research task is a uniform positive
inequality that uses arithmetic correlation, rather than another exact
count rewrite or an unsupported independence assumption.
The confirmed deadline **2026-09-08 13:00 UTC** has passed. The intended
research direction above is preserved as an unresolved question, not a
claim that work continued through the deadline or authorization for a new
indefinite run. A later instruction superseded both limits: the goal is now
open-ended and coherent checkpoints are pushed to the public repository.

## Current analytic frontier (2026-09-11)

The old deadline is superseded; the open-ended research goal remains active.
The complete-period lcm-sawtooth energy is now rigorously bounded for every
primitive conductor by

`m H_B^3 max_(q<=B^2)4^omega(q)
 sum_(a,b)L_a^2L_b^2/lcm(a,b)`.

This follows from a weighted-Cauchy argument and an exact reciprocal-lcm
harmonic identity. Independent review checked the normalization and returned
PASS. The transition-conductor decomposition is retained because it isolates
one-sided base failures, but the global bound bypasses them for complete
periods.

The remaining analytic gap is the incomplete prime-row boundary covariance,
followed by the signed prime-correlation estimate. Goldbach remains open.

The incomplete boundary now has an exact primitive-frequency operator. Its
worst arbitrary conductor vectors are strongly resonant, but the actual
Mobius vector and the full three-dimensional quadratic-log coefficient span
remain near the complete-period scale in tests through `M=16001`. This is a
reviewed finite reduction and a concrete next hypothesis, not an asymptotic
boundary estimate.

Row-varying logarithms are now included exactly in the same reduction. The
resulting `3 x 3` generalized eigenvalue remains below `1.74` in whole-prime
block scans through `M=1009` and is `1.139` at the central `M=16001` row.
Proving a uniform subpower bound for this explicit matrix is the current
complete-period transfer problem.

Across every prime in the project blocks `M=251,503,1009`, aggregating before
choosing the worst quadratic-log direction reduces the sharp ratios to
`1.042,1.019,1.032`. Four natural positive outer weights give the same finite
picture. This identifies joint prime-row phase rotation as the current
candidate mechanism; its asymptotic bilinear estimate is still open.

The complete `M=2003` prime block also passes the same falsifier: its weighted
aggregate sharp ratios are at most `1.01703`. This 249-prime computation is
reviewed finite evidence only.

A direct frequency-pair application of the existing joint bound has now been
ruled out beyond `beta=1/4`: supported frequency differences can have reduced
denominator of order `B^4`, producing a power loss at `beta=.32`. Any proof of
the observed aggregate cancellation must retain coefficient-weighted or
signed difference-modulus structure.

A reviewed positive-energy diagnostic now rules out the simplest sparse-pair
escape on the tested scales: the actual conductor product-energy fraction with
`lcm(d,e)>MA` grows from `.108` at `M=251` to `.510` at `M=16001`. This is not
yet a reduced-frequency or signed estimate; the next test resolves the actual
denominator of `k/d-h/e` under the primitive-frequency energy distribution.

That reduced-frequency test now also rejects positive sparsity finitely. The
reviewed `Q>MA` mass rises from `.0973` at `M=251` to `.3411` at `M=4001`;
the first two scales were enumerated exactly and the larger two were sampled
with recorded errors. The next test asks where the actual signed pair
contributions cancel, both by `Q` range and after prime aggregation.

An exact signed-bin calculation now finds strong within-prime cancellation:
at `m=251,373,499`, the `Q>mA` net is below `.0084` of its termwise-absolute
envelope despite envelopes between `2.92` and `4.58` times complete energy.
This reviewed result is finite and uses frozen logs. The next sign-removal
test distinguishes Mobius conductor signs from rational-phase oscillation.

The sign-removal falsifier leaves the high-`Q` net/envelope ratio below one
percent at all three primes while materially changing the whole boundary.
Rational phase geometry is therefore sufficient for the measured high-`Q`
cancellation with the actual magnitudes fixed; conductor signs remain relevant
elsewhere. The next exact decomposition separates within-`Q` from across-`Q`
cancellation.

The exact-`Q` split leaves only `6.9%--11.0%` of the high-`Q` pair envelope
after summing within each denominator, and the resulting packet absolute sum
is `0.255--0.321` times complete energy. This suggests the concrete packet
target `sum_(Q>mA)|C_Q| <= N^epsilon E_complete`; it is reviewed finite
evidence, not yet a uniform Ramanujan/Parseval bound.

At the next project fixture `m=503`, that packet quotient is `.595735`: still
below one, but nearly twice the earlier range. The exact result passed review
and keeps the route alive while weakening any constant-small interpretation.

The increase is distributed: at `m=503` the largest exact-`Q` packet carries
under 5% of the packet sum, 108 of 181 packets are needed for 90%, and the
effective count is 71. The next route tests a `1/Q`-weighted Cauchy square-sum
rather than trying to discard a short exceptional set.

That exact Cauchy majorant is within factor `1.79` of the packet sum but equals
`1.06524` complete energies at `m=503`. It isolates
`sum_(Q>mA)Q|C_Q|^2` as a plausible square-sum target without proving the
needed `N^epsilon` bound.

A bounded curiosity probe rewrites each packet as
`C_Q=sum_(r,Q)=1D_Q(r)K_A(r/Q)`. On the five leading `m=251` packets, the
constant-residue Ramanujan projection contributes under `.35%`, and no uniform
rank-one CRT factorization appears. The centered residue spectrum is the live
component; its active-window versus full-period L2 concentration is the next
falsifier.

That additive-spectrum falsifier now passes on the five leading `m=251` and
ten leading `m=503` packets: every active/full L2 ratio lies between `.880`
and `1.467`. The exact packet/Parseval compression is a reviewed
`new-to-this-task` aha candidate, while the uniform window and global residue-
energy bounds remain open.

The all-packet `m=251` residue calculation shows why the spectral window alone
is insufficient: active-window L2 is `.995` of full-period L2, but averaging
across rows supplies a further `.0202`, approximately `1/A`. The `A`-scaled
aggregate is `.930`; selected `m=503` packets are much less uniform, with a
biased top-ten aggregate `6.33`. The next target is an aggregate row-by-`Q`
large-sieve bound, not constant-one cancellation for every packet.

That selection issue is now resolved. All 181 `m=503` packets give an
`A`-scaled aggregate quotient `1.203`, while the other complete saved families
give `.872,.930,3.076`. These are finite order-one measurements, not a uniform
bound. An exact row-lag expansion then falsifies the idea that a few short
lags explain the result: the five largest lags carry only 34%--43% of absolute
lag mass, and the first five only 16%--29%. The surviving target is a broad,
coefficient-sensitive row-by-exact-`Q` large-sieve/operator estimate. The
signed prime correlation and Goldbach remain open.

A deterministic row-Gram sign-probe test now finds that m=499 is genuinely
exceptional relative to its own measured Gram matrix, and a fixed-geometry
scan finds a second exception at m=509. In both cases five exact denominators
carry over 92% of positive row-scale excess. The leading m=499 packet is
coherent reinforcement of several complementary conductor pairs; the leading
m=509 packet is instead 95% dominated by (210,323). This rejects one
universal internal explanation while localizing the next arithmetic question
to primitive-frequency structure inside a named conductor pair.

That internal test finds an explicit mechanism. At m=509, the rotated
endpoint modes 121/210 and 186/323 differ by only 23/67830; four conjugate
terms account for about 68% of the dominant channel envelope and endpoint
modes supply 98.4% of its signed value. The two material m=499 channels have
analogous main-lobe endpoint residuals 554 and 887. This explains the measured
exceptional packets through endpoint-amplified near frequencies, while the
uniform count, coefficient-weighted aggregate, outer prime correlation, and
Goldbach remain open.

The normalized endpoint score was then checked on ten fixed-geometry primes.
It identifies m=499 and 509 as the two exceptional cases, with raw Pearson
correlation .821 to the full row quotient, but only .600 rank correlation.
Endpoint resonance therefore detects the measured spikes without explaining
the full baseline. For coprime conductors its surviving condition is the
explicit linear inequality
|m(sigma e-tau d)-n d e|<=d e/A, with the actual geometric and structured
weights retained. Controlling that weighted count over conductors and primes
is now a named proof obligation.

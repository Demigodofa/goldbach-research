# Goldbach redistribution research

Owner: Kevin; research and integration: Rill (`agent.rill`).
Purpose: investigate a sequence of small proved statements that could help explain
prime-pair coverage of even integers. This is a local research deliverable, not a
claimed proof or a publication. Retain checked proofs, source references,
reproducible experiments, counterexamples, and precise remaining questions.

## Active goal

Start: 2026-09-08 03:22:30 UTC.
Deadline confirmed by Kevin: **2026-09-08 09:00 America/New_York (EDT)**,
equivalently **2026-09-08 13:00 UTC**.
Work until that deadline, then deliver a compact, verified research report.
A complete Goldbach proof is an aspiration, not the required stopping condition.
No spending, public repository creation, publishing, or contacting others.
Use background execution only. Do not change unrelated projects or user files.

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

## Current next action

The fixed-radius question has a checked negative theorem; the adaptive
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

Next formulate a falsifiable surviving rule that uses more arithmetic
information, and choose adversarial inputs against it. Fixed palettes,
fixed-constant logarithmic palettes, and bounds depending only on distance
to the preceding prime have been ruled out as universal guarantees. The
exact cubic count identity survives; its uniform positive lower bound is
still unproved. No Goldbach counterexample has been found. No shell job is
running. The full residual recurrence remains a possible computational task,
but it must not be confused with positivity induction.
The confirmed deadline remains **2026-09-08 13:00 UTC**. No remote publication
is authorized or configured; this repository is local.

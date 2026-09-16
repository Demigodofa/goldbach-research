# Bounded mathematical and verifier reviews

Owner: Rill. Purpose: preserve the reasoning and validation that support claimed
results, including corrections that change future execution. No raw model
reasoning is retained. Model agreement is not a proof by itself.

## Full residual periodic envelope and interval gap, 2026-09-16

A separate fresh-context read-only Sol review
(`01a0ac6a-401a-7d81-8414-e89168828373`) returned PASS with no material
findings for `notes/residual-periodic-envelope-and-window-gap.md`, its
small exact helper and tests. This was a supplied-derivation review, not
blind discovery. The reviewer checked the primary Goldston-Yildirim PDF,
including the explicit unsmoothed estimate in Lemma 2.1 (2.13), rather
than differentiating an error term.

The accepted theorem bounds the ABSOLUTE Ramanujan-conductor envelope of
the actual frozen long residual by
`L^3 exp(-c sqrt(log R))+tau(N)L^4/sqrt R`, uniformly in the target at
fixed `0<theta<1/2`. Low-conductor mains cancel inside each coefficient;
the high-conductor gcd tail retains divisors on both sides of the split.
This gives `Delta_0=E_D+O_(theta,J)(N/log(N)^J)`, where `E_D` is the
full weighted long-long CRT interval discrepancy. The incomplete reflected
operator, including same-conductor endpoint and cross-conductor terms,
remains uncontrolled at the required pointwise scale.

Eight new exact tests pass; the lead's affected four-module suite passes
40 tests normally and under optimized Python, and the combined regression
suite passes 75 tests. The reviewer independently ran 45 new/affected
tests in both modes. These are not a repository-wide test run and do not
prove the external theorem or asymptotics. The helper is deliberately
fixture-scale, not a scalable large-target evaluator.

The exact `c_15`, `N=34` sign-transfer falsifier has periodic mean `1`,
strict central sum `-3`, and discrepancy `-43/3`. It is not the actual
Goldbach residual or a counterexample to Goldbach. A bounded local Qwen
check reproduced the value vector and these totals, but incorrectly wrote
`34 mod 15 = 14`. Rill rejected that intermediate statement; a linked
correction confirmed remainder `4`. Rill checked `c_15(4)=mu(15)=1`
directly, not from the helper's vague qualification. Both calls used exact
file input, returned untruncated answers and confirmed native tools disabled
with zero tool calls. No helper output serves as proof authority.

This checkpoint controls a real component of the full divisor expansion;
it does not estimate the remaining interval error or establish an effective
starting point, q286/Q46189 transfer, or Goldbach. The full prove-or-disprove
goal stays active. Do not promote complete-period control into window control.

## Finite cutoff mixture obstruction, 2026-09-16

A separate fresh-context read-only Sol reviewer
(`01a0ac59-7eed-7e81-8878-6849969107e0`) checked
`notes/finite-cutoff-mixture-obstruction.md`, the helper extension, tests,
and the primary Goldston-Yildirim PDF. This was review of a supplied
derivation, not blind discovery. The consolidated verdict was conditional
PASS with three narrow qualifications, all applied by Rill: rescaling a
nonzero coefficient sum is covered only if normalized weights stay bounded;
absorb the `o(H)` error in the final positive margin; and say rank at most
one, including the zero case. No defect was found in the substantive proof.
The reviewer then checked those exact corrections and confirmed final PASS;
that confirmation did not rerun tests or broaden the review.

The accepted scope is a fixed finite set `0<theta_i<1/2` with uniformly
bounded real weights. The reviewer confirmed the rectangular common-divisor
uniformity and tails, the Selberg-coordinate cross-covariance argument,
completion of squares and unique norm minimizer, and the failure of plain
norm Cauchy already on `N=2^m`. The primary inputs are Lemma 2.1 (printed
p.16) and the unshifted Theorem 5.1(5.3) (printed p.31), not a forbidden
large-shift application. This is not a no-go for genuinely signed,
nonlinear, growing-family or other changed methods.

Eight new exact-algebra tests and a 67-test combined regression run pass.
The lead's 32-test new/parent suite also passes under optimized Python;
the reviewer independently ran the 19-test new/immediate-parent suite in
both modes. The fixtures validate algebra, support and boundaries, not the
external theorems or asymptotic estimates. A helper's incorrect suffix
telescoping is preserved as an explicit regression.

The local Qwen advisory got the proposed minimizer and bilinear expansion
but supplied incorrect intermediate telescoping and baseline factorization.
Rill rejected those explanations and sent a linked correction. That follow-up
returned only a runtime tool-work receipt, not a usable corrected derivation;
it was not accepted as mathematical evidence. The checked proof and exact
tests, not either advisory, establish the algebra. Future arithmetic-only
helper corrections should use the exact-file route that disables native
tools; saying "no tools needed" alone did not produce the required answer.
No local helper output was promoted to this proof or shared knowledge.

The useful negative result blocks unchanged finite cutoff coefficient scans.
The full prove-or-disprove goal remains active; its one-sided residual bound,
effective starting point and q286/Q46189 transfer gaps remain OPEN.

## Cutoff-normalized complementary remainder, 2026-09-16

A separate read-only Sol review (`01a0ac44-b822-7c63-9584-9463e00f38b9`)
gave a consolidated PASS to the proof and primary-source applications in
`notes/cutoff-normalized-complementary-remainder.md`. This was a fresh
review context supplied the derivation, not blind independent discovery.
It directly checked Goldston-Yildirim Lemma 2.1's logarithmic uniformity
condition, its `j=0,1` specializations, both common-divisor tails, the Euler
collapse, and the moving-residue use of Bombieri-Vinogradov at the two
strict endpoints. No correction to the displayed deductions was required.

The accepted result is a proved reduction: in the new cutoff-scale
normalization, `C(A,A)=H+O_(theta,J)(N/log(N)^J)` and
`C(A,Lambda)=H+O_(theta,J)(N/log(N)^J)`, so
`Delta_0=C(D,D)+O_(theta,J)(N/log(N)^J)`. Fixed `0<theta<1/2` is essential;
no uniformity over a changing theta or numerical starting point is claimed.
The published pair theorem's small-shift restriction is NOT bypassed by
citation; the written common-divisor argument supplies the required extension.
The original scale-`N` decomposition is not separately reclassified.

Eleven new tests pass normally and under `python -O`; the lead's combined
suite passes 59 tests. The reviewer also ran the 24-test new/parent suite
in both modes and found no implementation issue. These verify exact finite
algebra, not the analytical inputs or asymptotic conclusion.

A local Qwen response incorrectly rejected the Euler identity by retaining
non-squarefree powers of two and misvaluing the factor at two. Rill rejected
that objection by exact calculation, sent a linked correction, and checked
the corrected response. The explicit `N=8` rational fixture preserves the
zero Mobius-square weights. Neither response serves as proof authority.

The one-sided bound for `C(D,D)` remains OPEN. This is a useful change in
the remaining obligation, not a Goldbach proof, an external novelty claim,
or permission to resume constant scans. The primary source is linked with
equation/page locators in the mathematical note.

## Complementary-divisor mapping and sign check, 2026-09-16

A separate read-only Sol review (`01a0ac33-64b3-78e3-bd5c-e1ec0de0cea8`)
checked `notes/q286-q46189-complementary-divisor-mapping.md`, its original
source-module links, `complementary_divisor_correlation.py`, and its tests.
This was a fresh context given the proposed derivation, not blind discovery.
The reviewer confirmed the full frozen Mobius identity for `n>1`, the
complementary CRT residue and compatibility condition, the sharp inclusive
endpoint-error bound, `|E_B|<=B^2 log(N)^2`, the prime-power correction,
the exact `Delta_0` mapping, and the stated conditional epsilon gate.

Four clarifications were incorporated: retain the uncontrolled main
adjustment alongside the mixed/long terms; state the source's inclusive
prime-modulus interval; define the ordered prime-only mass explicitly;
and distinguish the source's selected `Q>mA` endpoint subsystem and
six-dimensional matrix relaxation from realizable arithmetic squares.
Failure of the relaxation is not impossibility for the Mobius family.

The divisor-switching follow-through is also exact on its stated domains.
The reviewer checked that the squarefree outer sign disappears from the
diagonal square but survives in the complementary product, without any
independence assertion. The `n=12`, `D=(2,7]` example falsifies extension
of that factorization to all integers: its middle-band sum is `-log 2`,
not zero. Nonsquarefree composites cannot be discarded as prime powers.

Thirteen focused tests pass, also under `python -O`; the combined run with
the prior local-density, cap-homogeneity, raw-sum, and original lcm source
regressions passes 48 tests. One test directly compares original source
code to the block-square formula. Two initial fixture bugs were corrected:
unintended float division in a rational expected value, and using `N=100`
when a nonzero proper-power example was required (`N=50`, `25+25`, is used).
The analytical proofs are the written derivations, not these finite tests.
A bounded local Qwen check returned a truncated opening only and contributes
no review authority or mathematical evidence.

Disposition: no constant scan or status-only audit. The short-short binary
counting error and prime-power term have universal `o(N)` bounds at the
named cutoff. The signed main adjustment plus mixed/long-divisor estimate
remains OPEN; no Q46189 transfer, strict-central theorem, or Goldbach proof
has been obtained. Kevin's route freedom is preserved: choose a question
for mathematical value, not because a previous handoff prescribed it.

## Independent local density and the missing mass direction, 2026-09-16

A separate read-only Sol review (`01a0ac24-41e4-7bf2-b6b4-8b6b09414af1`)
checked the supplied proof in
`notes/q286-independent-local-density-and-mass-direction.md`, the exact
fixtures in `periodic_pair_local_density.py`, and their ten passing tests.
This was a fresh reviewer context given the draft, not a blind independent
discovery. It confirmed the CRT normalization, uniform pushforward to all
four q286 moduli, centering kernel, and adverse-gap comparison.

The reviewer caught a substantive domain omission: the limiting singular
series claim requires positive even `N`; `N=0` is valid only for the finite
CRT fixtures. It also requested a distinction between orthogonal centering
in uniform residue coordinates and oblique centering in unequal orbit
coordinates, and a local definition of `A_raw_-`. Rill incorporated these
corrections and retained the prior exact decomposition as valid. The older
audit is clarified, not algebraically refuted.

The proof consists of CRT lift counting, a convergent telescoping-product
comparison, and direct linear algebra. The tests check implementation; model
agreement is not the proof. No prime-pair asymptotic, major/minor arc bound,
rigorous interval certificate for the floating q286 coefficients, or Goldbach
proof follows. A q286/Q46189 combination still needs an actual arithmetic
mapping that controls the missing total-mass error or the full signed error.

## Finite-radius theorem

Sol `finite_radius_review` independently reconstructed a CRT/Dirichlet family
showing that no constant radius repairs every chosen prime pair, even allowing
either orientation. Rill checked the nonzero residues, coprimality, proper
divisors, endpoints, and swapped-coordinate case. Accepted with its exact
quantifiers; no claim about every representation of a constructed N.

## The apparently stronger displacement-4 invariant

The exact scan through N=10,000,000 found a successful edge between some
representations of N and N+2 with each summand moving at most4.
Sol verified that a universal version would imply both Goldbach and infinitely
many twin primes. The four allowed k are -1,0,1,2; every edge contains a twin
pair. If only finitely many twin members existed, choosing a sufficiently
large even multiple of all of them would make every complementary N-p
composite. Hence they could not supply a summand for every large even N.
This is a strengthening in content, not an established simpler subproblem.
Do not call it logically strictly stronger without a separation theorem.

Modulo3, when all four primes exceed3:

| N mod3 | (p,q) mod3 | allowed k mod3 | allowed k for displacement4 |
|---:|---|---|---|
| 0 | (1,2) | 0 | 0 |
| 0 | (2,1) | 1 | 1 |
| 1 | (2,2) | 0 or1 | 0 or1 |
| 2 | (1,1) | 2 | -1 or2 |

These are necessary conditions, never sufficient primality conditions.
Any coordinate equal to3 must be handled explicitly. In particular p=3
always permits k=1, and q=3 always permits k=0. Do not apply the table to
those cases or to a target coordinate equal to3.

## Interval-count and AP-sum certificates

Sol checked the interval-hole lemma and AP-sum theorem and their inclusive
endpoints. Rill also tested 15,876 arbitrary small set pairs for the hole
lemma, and 3,267 generic AP sum cases independently of prime examples.

For the1,000 evens starting1,000,000,000, the reviewer confirmed the proof
structure:218 AP-sum certificates cover the full mask;222 unique prime inputs
are checked by exact trial division; the AP theorem constructs every output
witness without per-output search. This is a finite certificate only.

The reviewer found that Python `assert` was used in `verify_block`, allowing
`python -O` to remove all certification checks. The earlier ordinary-Python
runs retained their checks, but the verifier was not safe in optimized mode.
Rill replaced these checks with explicit ValueError paths, added integer/parity
validation and fresh-coverage checks, and added six corruption/composition
tests. The same tests passed under ordinary Python and `python -O`.
The serialized hole-certificate verifier now recomputes prime counts and all
derived metadata. The single-target N=4 base case and composition gap handling
are also covered. Tests are in `test_certificates.py`.

## Carry-forward certificates

Sol independently checked the carry invariant: validate every source prime/AP,
recompute its intersection with the later target block, and replay carried plus
fresh coverage during verification and composition. No coverage defect was
found. A monkeypatched palette/generator that raises was never reached in the
synthetic full-carry case. The stack wrapper still has one-time setup, and
mandatory source verification remains real work.

The reviewer found two ancillary evidence issues: carry counts and path labels
were not verified, and shallow copies aliased nested source AP dictionaries.
Terra reconstructed AP proof dictionaries and added explicit checks for all
present carry counts, provenance order, mode, and the logically skipped path.
Historic files without carry metadata remain supported. Twelve corruption,
composition, and aliasing tests passed under normal and optimized Python.
Rill inspected the revised verifier and tests. A saved skip flag can prove only
that the carried/base proof already suffices; it cannot certify historical CPU
execution or benchmark timing. The recorded comparison remains descriptive.

## Paired-wheel interval theorem

Sol independently checked the prime-safe window, reflection, all-phase
quantifier, cyclic gap convention, and rounded endpoints. No defect found.
All six exact-gap rows satisfy the window hypothesis; all five joins satisfy
`J_k+J_(k+1)+2*p_(k+1)+2<=2*p_(k+1)^2`. Rill's implementation checks agree
with independent cyclic enumeration, gcd construction, and finite Goldbach
consequences. The review explicitly preserves the conditional status of
`interval_from_gap`; only exhaustive `analyze_wheel` supplies its finite bound.
No per-target witness is an input to the interval derivation.

## Staged exclusion moments and information loss

Sol checked the product and split-product multiplicity caps, exact termination
at the cap, quadratic bound, adjacent-root cubic coefficients, and the real
moment-LP vertex proof. The normalized root families span the optimal real
polynomial bound for feasible moments; their ceiling is not asserted to solve
the integer moment optimization. Independent rational primal LP enumeration
matches the implemented dual values on small frozen fixtures.

The same reviewer checked the N=554 actual/abstract histograms, equality of
their first three moments, the support cap, and the fourth-degree lower bound15.
The accepted conclusion is specifically that these aggregate inputs alone
cannot force a survivor. The abstract model does not preserve prime identities,
individual intersection counts, or modular geometry. All181 recorded ambiguous
targets have explicitly verified nonnegative integer alternative histograms.

Rill independently compared all lower/upper bounds in both1,000-target runs
with exact prime-pair counts from a separate sieve. The CRT moment sequence
through N=1000 also matches direct divisor-membership counting. Twenty-four
tests pass under ordinary and optimized Python after integration, covering the
earlier block verifiers as well as the new moment and ambiguity methods.

## Location partitions and cubic reduction

Sol independently proved the partition optimization inequality, including
integer rounding and cap compatibility. It also checked the parity-split
abstract systems: they share all individually named intersections through a
fixed degree while differing in survivor existence. These results concern
the retained information, not an impossibility theorem for arithmetic methods.

Terra implemented exact candidate clips and partitions. Rill found a valid
early-empty-intersection case rejected by the first version; Terra corrected
it by padding only mathematically proved zero moments and added a targeted
regression. The eight N=4412 local vectors add to the original global vector,
and each local lower/upper bound contains independently counted prime pairs.

Sol then independently checked the cubic presieve identity: small-prime
composite removal preserves primes; remaining composites have two prime
factors; square-start residual events detect exactly the least factor; each
candidate therefore meets at most two residual events. The ordered identity
M-S1+S2 is exact for every even N>=6, with a separate4 case. It does not
establish a positive value for every N.

Rill inspected the implementation and matched all1,000 complete counts from4
through2002 plus six representative targets through1,000,000 against separate
prime sieves. Thirty-five tests pass under ordinary and optimized Python after
integration. Exact integer cube-root boundary tests avoid a floating-cutoff
error. Full-count scope is distinguished from earlier restricted windows.

## 2026-09-08 renewed run: adaptive block moments

The read-only Sol lane `moment_bound_review` checked the existing block
moment implementation and all eight retained receipts, then the exact
singular-factor refactor and minimal adaptive bit rule. No material defect
was found. Root's full 82-test suite passed both normally and under -O;
the six new precision-comparison receipts replayed and their count hashes
matched the independently checked prior block.

The reviewer independently checked the local count-ratio theorem, the
fixed-progression tail average, simultaneous positive counts via Vaughan's
exceptional set, constants, fixed-modulus quantifiers, and the bounded
dynamic-range obstruction. It confirmed the positive lower density
consequence and the m=2 exception for the block test.

One bounded follow-up checked the adaptive almost-all theorem, including
the A+2 source saving, conversion from prime-only logarithmic weights to
unweighted counts, the common adaptive scale, fixed shifts, centered
energy, strict condition m<(2d+1)^2, and m=1. The proof passed. Root adopted
the wording clarification that the lower half of the asymptotic follows
immediately, while the full asymptotic also needs the endpoint-split upper
bound. The remaining exceptional starts are not certified by this theorem.

The Terra source lane corrected an initial terminology error: Vaughan's
R_1 counts prime-only logarithmic pairs, not all von-Mangoldt prime-power
terms. Root verified the actual book scan, equations (3.16),(3.26) and
Theorem3.7 p.36. The original1972 article was metadata-only; neither lane
claims to have read that PDF. Prior-art comparison found related older
mechanisms and did not establish historical originality of our deductions.

# Riemann crossover inventory

Owner: Kevin; lead: Rill. Purpose: select reusable research assets for Kevin's
RH attempt without rebuilding existing tools or importing Goldbach-specific
claims as RH evidence. Retrieval: current REFRESH_HANDOFF and RESEARCH_GOAL.
Source checkpoint: `0891530` (positive Jordan boundary, pushed).

This is an initial source-inspected inventory, not a claim to have rereviewed
every proof or executed every historical tool. No RH theorem is claimed.

## What the questions mean

Chen's Goldbach theorem gives a prime plus a number with at most two prime
factors for every sufficiently large even integer. It is a proved additive
approximation to Goldbach, not an earlier stage of RH. RH concerns the real
parts of all nontrivial zeros of zeta. The recent exceptional-zero work
concerns quadratic Dirichlet L-functions, not solely the Riemann zeta
function; do not confuse RH with generalized RH. Primary reference routes:
[Tao's Chen lecture](https://terrytao.wordpress.com/2015/01/29/254a-supplement-5-the-linear-sieve-and-chens-theorem-optional/),
[Bombieri's RH description](https://www.claymath.org/wp-content/uploads/2022/05/riemann.pdf).

## Visual and navigation assets

- `tools/build_q286_residual_support_order_raw_bound_phase_space.py` and
  `tools/build_q286_active_lane_strict_closure_phase_space_html.py`: existing
  self-contained HTML with projected 3D points, rotation/zoom, point and table
  selection, and underlying row details. Actual HTML files are present in
  `evidence/`. Reuse interaction patterns with an RH adapter, not the data or
  axis semantics. These are embedded Canvas-2D projection implementations,
  not a generic Three.js package. The raw-bound renderer actually uses
  log(pair count) vertically; it assumes positive counts. Its annotations,
  coloring, thresholds and normalization are Goldbach-specific. Do not
  transplant that assumption to a diagnostic that must display zero/failure.
  Source was inspected; browser rendering was NOT retested in this audit.
- `tools/build_q286_evidence_glow_map.py`,
  `tools/build_q286_target_vector_overlay.py`,
  `tools/build_q286_target_vector_pca.py`, and
  `tools/build_q286_visual_summary_svg.py`: existing glow, vector/PCA and
  static visual pipeline. JSON and SVG outputs are present. The design
  separates evidence from attention and retains boundary labels. HOWEVER,
  `add_hit` simply adds caller-supplied weights and records layers. It does
  not prove source independence or automatically deduplicate shared evidence.
  RH reuse requires explicit provenance/dependency handling. Glow is neither
  a probability of truth nor a proof score. PCA geometry is sample/scaling
  dependent, not a theorem about the underlying arithmetic.
- `tools/build_goldbach_semantic_route_graph.py` and
  `evidence/goldbach-semantic-route-graph.json`: typed nodes and relations for
  obligations, hypotheses, falsifiers and unresolved steps; multiple views
  and cycle/return signals. Reuse the schema, while keeping human notes linear.
  Its hard-coded sources and historical "current" labels do NOT track the
  latest frontier automatically. An RH graph would need new authoritative
  nodes, not renamed Goldbach ones.
- `tools/build_goldbach_route_pattern_atlas.py` and
  `notes/q286-closed-lanes-map.graph.json`: routes through past attempts and
  scoped failures. Useful for avoiding duplicate experiments. Historical
  "dead" branches mean a named proposal failed under specified assumptions,
  not that every stronger version or the conjecture is impossible.

No new graph is justified until it answers a named question better than the
existing table or formula. No saved-camera persistence, animation feature,
current browser behavior or exhaustive graph coverage is certified here.

## Mathematical and computational assets

- `mobius_lag_spectral_probe.py`: `dyadic_spectral_decomposition` accepts an
  arbitrary complex array and retains signed quadrant contributions in a
  zero-padded linear-autocorrelation identity. The generic array transform is
  reusable; its Goldbach arithmetic producer and asymptotic gate are not RH
  inputs. Padding tests check that circular wraparound is not mistaken for
  an arithmetic correlation.
- `weighted_lag_graph_lemma.py`: a genuinely domain-independent weighted
  graph variance inequality, with degree/weight distortion charged explicitly.
  Reusable if an RH construction supplies its hypotheses. It does not create
  a zeta operator, an arithmetic sign estimate or a positivity bridge for free.
- `arithmetic_zero_moment.py`, `arithmetic_zero_energy.py`: saved prime/zero
  transforms and a mean-square estimate retaining actual real parts and
  multiplicities. These are closer to RH than residue-colored q286 plots.
  Their parameter regimes, smoothing, measure and error terms must be read
  before reuse. The displayed energy averages over a frequency parameter,
  not target integers; it does not imply that individual zeros lie on a line.
- `zero_detector_band_reduction.py`, `signed_zero_detector.py`: saved
  Dirichlet-polynomial detectors and signed constraints on surviving zeros.
  Candidate starting material for an RH question, NOT exclusion of every
  off-critical zero. Existing bounds and length gaps remain scoped as written.
- `spectral_endpoint_obstruction.py`, `spectral_count_resonance_model.py`:
  valuable stress tests for spectral proposals. The latter is explicitly an
  artificial N-dependent spectrum; it preserves named counting data but not
  the Euler product or prime explicit formula. It is not a zeta counterexample
  and not a single global spectrum with an infinite-target conclusion.
- `notes/positive-jordan-deformation-boundary.md`: reusable exact Mobius/Jordan
  identities and an averaging estimate. Its deletion example already shows
  why leading real asymptotics cannot license boundary differentiation.
  A possible density factorization through `1/zeta(w)^2` is a locator for a
  transfer question, not a proved RH bridge here. Analytic continuation and
  exclusion of poles must not be conflated.
- Existing exact arithmetic helpers, focused identity tests, source-linked
  notes and metadata import can preserve reproducibility and failed ideas.
  Floating plots and passing fixtures do not certify infinite estimates.

The older arithmetic/spectral module descriptions above were inspected as
locators. Their full analytical proof chains were NOT independently rereviewed
in this inventory. Keep the source modules authoritative, not this summary.

## Creativity with an actual test

Quantum physics is a legitimate source of mechanisms. The Hilbert--Polya
program seeks a self-adjoint operator with the required exact zeta spectral
correspondence; Berry--Keating develop quantum-chaotic/prime-orbit analogies.
This is established prior art, not a new idea of ours. See
[Berry--Keating, sections 1-2](https://michaelberryphysics.wordpress.com/wp-content/uploads/2013/06/berry307.pdf).
Real eigenvalues or matching mean spacings alone do not establish that
correspondence. A proof would need a valid operator/domain and an exact
identification accounting for ALL nontrivial zeros, including multiplicities,
without assuming they are already on the critical line.

The most useful first discrimination question suggested by the old tools is:
does a proposed prime-side transform preserve sensitivity to an off-critical
real part, or did centering, taking absolute values, or fitting a spectrum
erase the very information RH asks about?

- Mechanism: retain the full zero exponent, not only its height. For
  `rho=beta+i*gamma` and `u=log(x)`, the exact factor is
  `x^(rho-1/2)=exp((beta-1/2)*u)*exp(i*gamma*u)`.
- Changed prediction: a candidate that truly preserves this field must retain
  the different scale dependence of beta=1/2 and beta!=1/2. Conjugate and
  reflected copies must be included where the formula requires them.
- Falsifier: a representation that gives identical output after moving a
  symmetry-compatible test quartet off the line has lost information. This
  falsifies its proposed discriminating use, not RH. Such a mock quartet is
  not evidence that zeta has those zeros.
- Required analytical bridge: a finite diagnostic is insufficient. Any RH
  conclusion must additionally prove a target-independent estimate or exact
  spectral identity excluding every beta>1/2, with the full zero sum,
  cancellation, tails and all heights accounted for. No such estimate is
  supplied by this inventory. Choose the exact transform and state its bound
  BEFORE a future computation; do not infer a bound from a visualization.

This is a screening question, not a claimed new proof strategy. Do not build
a quartet simulator automatically: first check whether the exact formula
already settles the proposed information-loss question on paper.

## Reverse-engineering published results

Kevin suggests working backward from published consequences of RH. Keep the
logical directions explicit: RH implies X does not let a proof of X establish
RH. A disproof of X would refute RH, provided the implication and its other
hypotheses hold. A proved equivalence RH iff X is a genuine alternative
target; a conditional proof of X using RH cannot then be reused to prove RH.
There is no established percentage of a proof completed by counting related
papers, equivalent criteria, or conditional consequences.

Two primary-source criteria worth comparing against existing tools:

- [Lagarias](https://arxiv.org/abs/math/0008177): an all-integer inequality
  involving divisor sums and harmonic numbers is equivalent to RH. Exact
  divisor tools fit the finite arithmetic, but finite checks do not supply
  the required universal inequality.
- [Baez-Duarte](https://arxiv.org/abs/math/0205003): in L2(0,infinity), RH is
  equivalent to the indicator of (0,1) being in the closed linear span of
  `x -> fractional_part(1/(n*x))`, for positive integers n. This is an
  established logical bridge for a SPECIFIC approximation problem, unlike
  an arbitrary useful-looking L2 bound. Our Mobius, kernel and exact-accounting
  tools make it a candidate for inspection, not a result. The approximation
  rate stated in that paper assumes RH; importing it as unconditional would
  be circular. The defining approximation target does not assume RH.

[Goldston--Suriajaya, 2025](https://arxiv.org/abs/2511.20059) is a concrete
published example of asking what removing RH from a known argument would
yield. Its stated two-thirds conclusion is not proved unconditionally there.
It is a source locator for a dependency audit, not evidence of a new theorem
in this repository. An asymptotic proportion of zeros on the line, even one,
does not by itself exclude an exceptional set of density zero. RH requires
every nontrivial zero to lie on the line.

Before selecting one of these alternatives, identify exactly where RH is
used in the source proof and which independent estimate could replace it.
Do not create new coefficient scans merely because an equivalent criterion
is computationally accessible. No full source-proof audit has yet been done.

## Validation and continuation

Confirmed presence of both linked-view HTML files, glow/PCA JSON, static SVG,
semantic graph and pattern atlas. Inspected the render selection path, graph
schema, glow accumulator and selected mathematical module definitions.

Actual command, 19 tests passed:

```text
py -3 -m unittest test_weighted_lag_graph_lemma test_mobius_lag_spectral_probe test_goldbach_semantic_route_graph test_goldbach_route_pattern_atlas
```

These check selected generic helpers and stored graph contracts. They do not
prove graph freshness, renderer correctness, RH relevance of every historical
result, or RH itself. No historical evidence was regenerated or relabeled.
No new visualization, RH numerical scan or autonomous continuation was made.

Next research should select ONE arithmetic question using these assets and
its exact assumptions, rather than finish a dashboard merely because it is
available. Goldbach remains open at the preserved checkpoint. NO QWEN.

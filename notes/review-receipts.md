# Bounded mathematical and verifier reviews

Owner: Rill. Purpose: preserve the reasoning and validation that support claimed
results, including corrections that change future execution. No raw model
reasoning is retained. Model agreement is not a proof by itself.

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

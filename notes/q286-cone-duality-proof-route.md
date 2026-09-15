# q286 cone-duality proof route

Status: theorem-shaping note.  This is not a cone theorem, signed
prime-correlation theorem, threshold theorem, or Goldbach proof.

## Why this replaces more audits

The recent q286 scans have made the finite picture sharper, but they have not
defined a mathematical class that can be proved.  The useful pivot is to stop
asking for more rows and instead define the fixed finite-dimensional operator
whose bad region must be excluded.

The current evidence says:

- the checked post-discovery first-three-tail rows are rescued;
- the rescue is near-sharp, with worst checked drag-to-margin ratio
  `0.9696841556062236`;
- discovery rows contain real drag-overturn counterexamples;
- support, nonnegativity, total mass, pair reflection, simple label
  dictionaries, and small fixed channel subsets are all too weak.

So the next proof route is not another filter.  It is a cone separation
problem with an arithmetic cone strong enough to describe actual
strict-central prime-pair residue measures.

## Operator space

Let `M=10010` be the assembled strict-central arithmetic period used by
`combined_fixed_strict_central_coefficient_receipt`.  Let

```text
U = (Z/MZ)^*
```

and, for an even target residue `a = N mod M`,

```text
A_a = {r in U : a-r is also in U}.
```

For an even target `N`, define the strict-central weighted binary-prime
measure on `A_a` by

```text
W_N(r) = sum log(p) log(N-p)
```

over primes `p` with

```text
N/3 < p < 2N/3
p == r mod M.
```

Let `T_N=sum_r W_N(r)`.  When `T_N>0`, normalize:

```text
mu_N(r) = W_N(r) / T_N.
```

Then `mu_N` lies in the target-conditioned simplex:

```text
mu_N(r) >= 0
sum_{r in A_a} mu_N(r) = 1
mu_N(r) = 0 outside A_a.
```

Ordered pair symmetry adds

```text
mu_N(r) = mu_N(a-r).
```

This support/reflection simplex is not enough.  Earlier finite-vector
obstruction receipts construct synthetic measures in this simplex that enter
the bad q286 region.  Any proof must add arithmetic information about actual
binary-prime residue distribution.

## Fixed functionals

The verifier constructs fixed coefficient maps on `U` from the assembled
coefficient vector, decomposes them by character support, and handles the
native q286 support `(11,13)` by pushing through the `C10 x C12` character
table and its frozen singular-mode matrices.

For each residue class `a`, this gives affine functionals of `mu`:

```text
F3_a(mu) = first three q286 singular modes / principal
C_a(mu)  = full action / principal - F3_a(mu)
A_a(mu)  = F3_a(mu) + C_a(mu)
```

Equivalently, after subtracting the uniform measure on `A_a`, these are fixed
linear actions on the centered discrepancy vector.  The complement functional
must be defined on the full `M=10010` residue space, not only on the 17
outside q286 channels, because it includes non-q286 support terms as well as
the q286 local, higher-mode, and residual terms.

The current finite suffix target is:

```text
F3_a(mu_N) < -0.3       implies
S_a(mu_N) = 1 + F3_a(mu_N) > 0
D_a(mu_N) = max(0, 1 - C_a(mu_N)) < S_a(mu_N).
```

The failure region is therefore the affine cone slice:

```text
F3_a(mu) < -0.3
S_a(mu) > 0
D_a(mu) >= S_a(mu).
```

For linear programming, replace the max by the equivalent linear bad branch:

```text
C_a(mu) <= 1
1 - C_a(mu) >= 1 + F3_a(mu)
```

or simply:

```text
C_a(mu) <= -F3_a(mu).
```

Together with `F3_a(mu)<-0.3`, this is the exact non-rescue condition.

## Candidate theorem

Candidate, not proved:

For every sufficiently large even `N` whose strict-central q286 row is in the
tail region `F3_a(mu_N)<-0.3`, the actual normalized prime-pair measure
`mu_N` belongs to an arithmetic cone `K_a` for which

```text
K_a intersect {F3_a < -0.3, C_a <= -F3_a} = empty.
```

Equivalently, there is a dual certificate: a nonnegative combination of the
defining inequalities of `K_a` plus the tail/failure inequalities produces an
impossible inequality such as `0 < -eta`.

This is the Farkas/LP-duality form of the proof.  It would turn the current
finite q286 rescue envelope into a checkable certificate rather than another
empirical scan.

## What can define `K_a`

The cone constraints must be fixed before testing and must come from
arithmetic, not from fitted row outcomes.  Plausible ingredients are:

- explicit binary Goldbach-in-progressions bounds for the residue classes of
  `M` or its factors;
- fixed-character estimates for the finite support families used by the
  verifier;
- positive semidefinite covariance or moment inequalities for the
  strict-central prime-pair residue measure;
- coefficient-sensitive mass/landing inequalities on q286 reflection-orbit
  sign classes;
- sourced zero-free-region or GRH-conditional bounds, clearly labeled by
  hypothesis.

The following are already too weak as standalone `K_a` definitions:

- local admissible support only;
- nonnegative mass plus total mass;
- ordered pair reflection symmetry;
- a uniform reflection-orbit mass cap;
- static label-only dictionaries on the 17 outside channels;
- a fixed small subset of residual-drag channels.

## Minimal executable test

Before any fresh scan, build a deterministic LP feasibility verifier for each
target residue `a mod M`:

```text
variables: mu(r), r in A_a
constraints: candidate K_a constraints
bad branch: F3_a(mu) <= -0.3 and C_a(mu) <= -F3_a(mu)
output: infeasible certificate or synthetic bad measure
```

If the LP returns a synthetic bad measure, that cone is insufficient and the
counterexample should be preserved as a theorem-form failure.  If the LP is
infeasible with rational or interval-certified dual multipliers, that becomes
a real candidate proof certificate, subject to independent mathematical
review and a separate finite boundary check.

## Prediction

Unlike another audit, this route predicts a reusable implication:

```text
mu in K_a and F3_a(mu)<-0.3  =>  C_a(mu)>-F3_a(mu).
```

The implication should hold for every admissible measure in the cone, not just
for scanned rows.  If it depends on the measured block index or on selecting
rows that already pass the ratio envelope, it is not a theorem mechanism.

## Falsifier

The route is falsified for a proposed cone `K_a` if the LP finds a feasible
synthetic measure satisfying all cone constraints and the non-rescue branch.
The existing reflection-support obstruction already supplies this falsifier
for the weakest cone, so the next cone must include genuine arithmetic
distribution input.

If every source-backed cone strong enough to separate the bad branch reduces
to a pointwise signed binary-prime correlation estimate, that is not a
failure.  It is the correct theorem boundary: the q286 hole is then a
localized form of the hard signed prime-correlation problem.

## Decision

This is the current strategic pivot:

1. Define `K_a`.
2. Ask LP duality for a certificate or a synthetic bad measure.
3. Only after a cone survives that theorem-form test should new target rows be
   scanned as heldout evidence.

Novelty label: `new-to-this-task`.


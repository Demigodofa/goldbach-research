# q286 lift-project dictionary audit

Status: finite dictionary audit and partial falsifier.  This is not a proof of
Goldbach, a rank-`1` theorem, or a residual-drag theorem.

## Purpose

This receipt tests the smallest executable form of the AI unit-distance
method-transfer idea:

```text
Can a simple lifted dictionary on the q286 outside-channel label lattice
explain the frozen Octave rank-1 outside direction and tighten the current
residual-drag hole without target-specific fitting?
```

The generated evidence is:

```text
evidence/q286-lift-project-dictionary-audit.json
```

The builder is:

```text
tools/build_q286_lift_project_dictionary_audit.py
```

## Frozen Fixture

The audit reuses the existing full-window q286 denominator:

- six near-boundary windows;
- `716` total checked targets;
- stress row `1222142` as the lone deficit;
- `715` clear rows;
- the same `17` outside real channels after removing the volatile
  pair/complement channels.

It scores predeclared channel-label dictionaries against the frozen Octave
rank-`1` outside direction and the known rank-`1` high residual-drag rows.

## Candidate Family

The tested dictionaries are deliberately simple:

- all-ones outside-channel sum baseline;
- low-degree label-lattice polynomial subspaces;
- separate low-frequency character phases on the `C10` and `C12` label
  factors;
- coupled sum/difference phase features;
- a combined low-frequency lift;
- parity and edge/boundary features.

Each nontrivial subspace is projected onto the frozen rank-`1` right singular
vector once, then replayed across all full-window rows.  No candidate receives
row-specific fitting.

## Result

No candidate passed the local hole-tightening gate:

```text
cosine with frozen rank-1 direction >= 0.9
all reconstructed outside deltas positive
no 0.75 residual-drag cap failures
at least 70 percent recall of the rank-1 high-drag set at k=10
```

The best real candidate is `full_low_frequency_lift`:

```text
rank1 cosine:        0.8324697828558575
explained fraction:  0.6930059393680785
cap failures:        0
nonpositive deltas:  0
high-drag overlap:   6 of 10
max drag ratio:      0.7019514025426515
mean delta/full:     0.852702998...
max delta/full:      3.3551576...
```

The all-ones dictionary is only a tautological baseline: summing all `17`
outside channels exactly recovers the exact outside delta, so it has no
residual drag but also no explanatory grip on the rank-`1` direction and no
high-drag overlap.

## Claude Order-Weight Candidate

Kevin pasted a Claude proposal after the first audit.  The proposal had two
parts:

1. the outside labels are even-parity character labels, `a+b = 0 mod 2`;
2. the rank-`1` magnitude might follow the order-weight formula
   `gcd(a,10)/10 * gcd(b,12)/12`.

The parity observation is real but not separating in the actual q286
pipeline:

```text
outside labels even parity:  17/17
volatile labels even parity: 8/8
parity separates outside from volatile: false
```

The order-weight vector fails as a rank-`1` explanation:

```text
rank1 cosine:                 0.304375...
Spearman(rank1, order):      -0.0947775...
Pearson(rank1, order):       -0.1694603...
high-drag overlap at k=10:    0/10
max rank1-loading tie range:  0.5786474...
mean dictionary/full ratio:   0.4978193...
```

It has no `0.75` cap failures and no nonpositive reconstructed deltas, but
that is mostly because it conservatively under-reconstructs the outside delta.
This is not a residual-drag explanation.

The primitive-root-`2` realpart negative control also fails the positivity
screen, with `5` nonpositive reconstructed deltas and `5` cap failures.

## Interpretation

Grok returned a useful sequential-adversarial no-go intuition: simple
non-post-hoc arithmetic dictionaries on only these `17` labels should not be
expected to explain the rank-`1` direction.  Claude returned a more concrete
candidate.  The local audit supports the cautious version of Grok's criticism
and falsifies Claude's specific order-weight vector as a rank-`1` explanation.
The tested simple family does not explain the rank-`1` shadow well enough to
promote it.

The stronger no-go claim is not proved.  The low-frequency lift is not random:
it preserves positivity, has no `0.75` cap failures, and identifies `6` of the
`10` high-drag rows.  That is a partial signal, not a theorem engine.

## Next Decision

Retire the simple label-only dictionary family as the immediate explanation
for q286 rank-`1`.  Preserve two surviving components:

- low-frequency label-lattice structure is a useful feature family;
- the next test should be held-out and row-dependent, not another static
  label-only replay.

The next stronger lane should test a richer arithmetic lift with target
residue or splitting data included up front.  If that richer lift also fails,
the rank-`1` direction should be treated as a finite SVD compression shadow,
and the proof route should move back to row-dependent residual balance or a
larger signed cone.

## Boundary

This audit tightens the q286 method-transfer lane by closing the simplest
label-only version and preserving one partial low-frequency signal.  It does
not prove any uniform estimate, any held-out theorem, any pointwise
Goldbach-in-progressions theorem, or Goldbach.

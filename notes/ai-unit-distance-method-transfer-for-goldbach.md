# AI unit-distance method transfer for Goldbach

Status: source-backed strategy note and aha-candidate, not a theorem and not
proof of Goldbach.

## Source trigger

Kevin pointed to Tim Lee's 2026 Understanding AI discussion of OpenAI's
unit-distance counterexample:

```text
https://www.understandingai.org/p/openais-milestone-math-breakthrough
```

Primary OpenAI/source materials:

```text
https://openai.com/index/model-disproves-discrete-geometry-conjecture/
https://cdn.openai.com/pdf/74c24085-19b0-4534-9c90-465b8e29ad73/unit-distance-remarks.pdf
https://arxiv.org/abs/2605.20579
```

The transferable lesson is methodological.  The unit-distance result did not
close a hard problem by squeezing the original planar picture harder.  It
changed representation: a high-dimensional algebraic construction was
projected back to the plane, with the imported algebraic structure doing the
work.

Goldbach is a different problem.  The OpenAI result was a construction that
disproved a geometry conjecture.  Goldbach, if true, asks for a universal
positivity theorem for every even integer above the checked boundary.  A
construction-only counterexample style is therefore not the direct analogue,
and this should not be treated as a universal proof engine.

The realistic use is local hole-tightening: use a representation shift where
one specific obstruction is already glowing, then require the lifted view to
explain that obstruction better than the current coordinates do.  The analogue
worth testing is:

```text
find a lifted representation in which prime-pair mass has a forced positive
structure, then prove that projection back to ordinary even targets cannot
erase all of that positivity.
```

## Mechanism

Current q286 work has a repeated finite shadow:

- a frozen Octave rank-1 outside direction stays positive on full-window
  clear-minus-stress rows;
- the residual-drag cap survives the same full denominator;
- the simplest fixed small-channel certificate is falsified.

That combination says the search may be in the wrong coordinates.  The rank-1
direction should be treated as a shadow of a possible hidden lifted basis, not
as a theorem object by itself.

Candidate lifted domains to test, without promotion:

- Dirichlet/ray-class character lifts over fixed modulus families;
- algebraic-number-field or CM-style lifts where splitting behavior partitions
  prime-pair channels;
- higher-rank torus/nilsequence lifts that turn row-dependent cancellation
  into structured frequency cancellation;
- additive-combinatorial transference lifts where dense model positivity is
  proved before pushing through a pseudorandom majorant.

## Prediction

If this method transfer is useful, one lifted dictionary should reproduce the
current q286 rank-1 outside direction with predeclared coefficients or a
small-dimensional invariant subspace.  It should also predict, before fitting
to them, which rows become high residual-drag rows such as `1242118`,
`1222048`, `1220056`, and `1200254`.

The first win condition is not a proof.  It is a non-post-hoc dictionary that
explains the existing finite shadow better than SVD alone and creates a
concrete theorem statement with known inputs.

## Falsifier

Retire this lane if every tested lifted dictionary either:

- reconstructs the q286 rank-1 direction only after target-specific fitting;
- fails to predict the held-out high residual-drag rows;
- collapses to the already-refuted fixed small-channel certificate; or
- restates an unproved pointwise Goldbach-in-progressions theorem without
  simplifying its inputs.

## Smallest next test

Build a lift-and-project dictionary audit:

1. Freeze the existing full-window q286 denominator and stress row `1222142`.
2. Predeclare a small set of candidate lifted dictionaries before seeing new
   holdout rows.
3. Project each dictionary onto the 17 outside channels used in the
   rank-1/residual-drag audits.
4. Score whether each dictionary explains the frozen rank-1 direction,
   predicts high residual-drag rows, and gives a signed inequality candidate.
5. Record failures as falsifiers, not as hidden tuning steps.

Useful first artifact name:

```text
tools/build_q286_lift_project_dictionary_audit.py
evidence/q286-lift-project-dictionary-audit.json
```

First local holes to target:

- the arithmetic meaning of the frozen q286 rank-`1` outside direction;
- the near-sharp `0.75` residual-drag cap;
- row-dependent residual balance after the fixed small-channel certificate
  failed;
- whether high residual-drag rows are predicted by a lifted dictionary before
  fitting.

## Boundary

This note does not import OpenAI's theorem into Goldbach.  It preserves a
source-backed search tactic for selected holes: change the representation,
prove the projection loss, and keep every candidate falsifiable.

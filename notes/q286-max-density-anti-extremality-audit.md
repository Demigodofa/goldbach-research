# q286 maximum-density anti-extremality audit

Status: finite cone falsifier.  This is not a maximum-density theorem, signed
prime-correlation estimate, q286 threshold theorem, strict-central Goldbach
theorem, or Goldbach proof.

Receipt:

```text
tools/build_q286_max_density_anti_extremality_audit.py
evidence/q286-max-density-anti-extremality-audit.json
```

## Question

The convex-envelope obstruction showed that support/reflection/coefficient
geometry admits synthetic tail failures.  The next candidate was:

```text
maybe actual prime-pair measures avoid the bad lower face because
no reflection orbit can carry too much mass.
```

For each tested residue, solve:

```text
minimize lambda
subject to mu >= 0, sum mu = 1,
           F3(mu) <= -0.3,
           Full(mu) <= 0,
           mu(orbit) <= lambda*u_a(orbit).
```

If actual rows had maximum orbit-density multiple below this minimum bad
`lambda`, a max-density theorem would exclude the bad branch.

## Result

It fails as a proof cone.

```text
target rows checked:                  230
target residues checked:              204
actual certificate pass count:        0
post-discovery certificate pass count: 0 / 196
```

The LP bad branch can be reached with only a mild density tilt:

```text
minimum bad max-density multiple:
  min   1.0357032987728947
  mean  1.0925776941656318
  max   1.2007521303394815
```

Actual rows are much more concentrated than that:

```text
actual max orbit-density multiple:
  min   3.3411693332118935
  mean  7.07269630587032
  max   25.29622421615252
```

The actual/bad-threshold ratio is never below `2.9576969247757057` and reaches
`23.16563808841412`.

## Interpretation

This kills the simple maximum-atom/maximum-orbit-mass explanation.  It is not
true that the bad branch requires a wildly concentrated measure.  The LP can
construct bad measures that are close to uniform in the maximum-density sense.

That matters because it changes the theorem target.  A sieve-style upper
bound on individual residue-pair cells, even if strong, is unlikely to be the
right bridge by itself.  The actual rows are allowed to be concentrated, but
their concentration lands in a favorable signed pattern.

So the next cone has to be more structured:

```text
not:  every orbit mass is small
but:  mass cannot tilt toward the negative Full lower face
      without also forcing compensating positive landing
```

Candidate replacements:

- a signed-moment cone using the actual `F3` and `Full` coefficient directions;
- a top-k signed landing constraint, separating heavy favorable and adverse
  orbits;
- an entropy or transport inequality relative to the lower-envelope optimizer,
  not relative to uniform;
- a sourced binary prime-pair AP estimate for the exact signed functional.

## Decision

Max-density anti-extremality is demoted as a standalone proof route.  The
anti-extremality problem survives, but it must be coefficient-sensitive or
lower-face-relative.


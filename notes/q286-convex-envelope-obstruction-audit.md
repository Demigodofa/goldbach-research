# q286 convex-envelope obstruction audit

Status: finite coefficient-envelope diagnostic.  This is not an
anti-extremality theorem, signed prime-correlation estimate, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof.

Receipt:

```text
tools/build_q286_convex_envelope_obstruction_audit.py
evidence/q286-convex-envelope-obstruction-audit.json
```

## Question

The landing-cone route asks whether the q286 coefficient geometry itself
forces rescue, or whether actual strict-central prime-pair measures avoid a
bad part of the coefficient hull for a deeper arithmetic reason.

For each target residue, push the reflection simplex through the two
coefficient functionals:

```text
F3(mu)    = first-three action
Full(mu)  = full q286 action
```

At an observed value `F3(mu)=t`, solve the LP lower-envelope problem:

```text
min Full(mu)
subject to mu >= 0, sum mu = 1, reflection orbits fixed, F3(mu)=t.
```

This uses pre-existing tight rows from the nonprincipal-drag envelope receipt.
It does not scan new targets and does not select by a new pass/fail outcome.

## Result

The audit tested `230` tight source rows over `204` target residues.

Every tested residue admits a synthetic coefficient-only tail failure:

```text
synthetic tail-failure residues: 204 / 204
```

The coefficient-only tail halfspace has strongly negative possible full
action:

```text
minimum full on tail halfspace:
  min   -10.089065110068542
  mean   -6.8251449689048656
  max    -4.709304090441504
```

Actual rows sit far above the coefficient-only lower envelope:

```text
actual surplus above lower envelope:
  min    3.0041922291206915
  mean   5.476563203477463
  max    8.746810155749943
```

For the post-discovery rows only:

```text
post-discovery rows:                         196
post-discovery surplus above lower envelope:
  min    3.1310310375615944
  mean   5.496203298315322
  max    7.8631684141402225

post-discovery position between envelopes:
  min    0.3422581800099013
  mean   0.5004481478426532
  max    0.626814811541939
```

The tightest actual row by this metric is still an early discovery failure:
`14138`, with actual full action `-0.8769412734408436` but still
`3.0041922291206915` above the coefficient-only lower envelope.  The tightest
post-discovery row is `548126`, with actual full action
`0.5953011116701278` and surplus `3.1310310375615944`.

## Interpretation

This cleanly separates two ideas:

1. Coefficient geometry alone does not close the q286 hole.  The bad branch is
   present inside the reflection simplex for every tested residue.
2. Actual prime-pair measures are not behaving like lower-envelope extremal
   measures.  They land in the interior of the coefficient hull, well above
   the worst possible `Full` value at the same `F3`.

So the next theorem is not:

```text
support + reflection + q286 coefficients force Full > 0.
```

That is false in this LP model.

The next theorem should instead be an anti-extremality statement:

```text
Actual W_N cannot concentrate on the lower convex face of the
(F3, Full) coefficient hull strongly enough to make Full <= 0
after the finite boundary split.
```

## New mathematical problem

Define the q286 Convex-Envelope Anti-Extremality Problem:

For each even residue `a mod 10010`, let `H_a` be the convex hull of the orbit
coefficient pairs

```text
(gamma_F3_a(orbit), gamma_full_a(orbit)).
```

Let `L_a(t)` be the lower envelope

```text
L_a(t) = min Full(mu) subject to F3(mu)=t.
```

Find explicit `N0(a)` and `eta_a(N)>0` such that the actual strict-central
prime-pair measure satisfies

```text
Full(mu_N) >= L_a(F3(mu_N)) + eta_a(N)
```

and the right side is positive on the q286 tail lane after the finite boundary
split.

This is a coefficient-matched transport/correlation theorem.  It is narrower
than Goldbach itself, but still needs genuine arithmetic input about binary
prime-pair landing.  A sourced binary Goldbach-in-progressions estimate,
signed character-moment inequality, or transport entropy bound could serve as
the missing input if it controls this exact envelope gap.


# q286 lower-face support signature audit

Status: finite support-signature diagnostic and `new-to-this-task`
aha-candidate.  This is not a support-signature theorem, signed
prime-correlation estimate, q286 threshold theorem, strict-central Goldbach
theorem, or Goldbach proof.

Receipt:

```text
tools/build_q286_lower_face_support_signature_audit.py
evidence/q286-lower-face-support-signature-audit.json
```

## Question

The lower-face overlap audit found that actual prime-pair measures almost
avoid the coefficient-only lower-face optimizer.  The next question is whether
that bad support can be named before looking at future rows:

```text
Is B_a(F3(mu_N)) a fixed residue/arithmetic support dictionary,
or is the stable object the moving lower face itself?
```

This is the heat-map step-back version of the q286 pivot: look at the bad
face, not another chosen list of outside channels.

## Result

The audit reuses the `230` rows from
`evidence/q286-lower-face-overlap-audit.json`, including `196`
post-discovery rows.

For the post-discovery rows:

```text
lower-face support size:                    2 on 196 / 196 rows
complement-closed supports:                 196 / 196 rows
all-negative-Full supports:                 152 / 196 rows
positive-F3 compensator present:            192 / 196 rows
negative-Full lower mass fraction:          0.932438665145394..1.0
mean negative-Full lower mass fraction:     0.9928125264077061
actual mass on extracted support:           0.0..0.012172473138011076
unique support signatures modulo 286:       126
top support signature share modulo 286:     0.07142857142857142
```

## Interpretation

The lower-face support has a stable coefficient geometry but not a simple
fixed residue signature.  Every checked post-discovery bad optimizer is a
two-orbit pair-reflection face.  Almost all of the optimizer mass lies on
negative-Full orbits, and the actual prime-pair measure places almost no mass
there.  However, the residue signatures modulo `286` are dispersed: the most
common support pattern covers only `14` of `196` post-discovery rows.

This demotes another local dictionary route.  A theorem that says "avoid these
specific residues" is not the right object.  The better object is:

```text
Avoid the LP-defined negative-Full lower face selected by the target residue
and observed F3 value.
```

## Candidate theorem refinement

For each even target residue `a mod 10010` and observed value
`t=F3(mu_N)`, let `lambda_a(t)` be a lower-face optimizer and
`B_a(t)` its two-orbit support.  The measured candidate is:

```text
mu_N(B_a(F3(mu_N))) <= beta_a(N)
```

with `beta_a(N)` small enough that signed transport away from `lambda_a`
satisfies:

```text
transport_positive(mu_N-lambda_a)
  > transport_negative(mu_N-lambda_a) + rho_a(N).
```

The receipt suggests that any proof must be coefficient-face-relative, not a
static label or residue-class theorem.  It still requires pointwise signed
binary-prime correlation input.

## Falsifier

Freeze this description before testing new q286 windows.  The candidate is
falsified if a predeclared later row has:

- lower-face support size different from `2`;
- less than `0.9` lower-face mass on negative-Full support;
- actual mass on lower-face support no longer small; or
- a dominant fixed residue signature emerges on held-out rows, showing that
  this audit missed a simpler arithmetic selector.


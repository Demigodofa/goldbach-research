# q286 lower-face overlap audit

Status: finite face-relative diagnostic and theorem candidate.  This is not a
lower-face overlap theorem, signed prime-correlation estimate, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof.

Receipt:

```text
tools/build_q286_lower_face_overlap_audit.py
evidence/q286-lower-face-overlap-audit.json
```

## Question

The maximum-density cone failed because actual rows are naturally
concentrated.  The next question is face-relative:

```text
At the same observed F3 value, does actual prime-pair mass sit on the
coefficient-only lower face, or does it move away from that bad optimizer?
```

For each pre-existing tight row, solve:

```text
min Full(lambda)
subject to lambda >= 0, sum lambda = 1, F3(lambda)=F3(mu_N).
```

Then compare actual `mu_N` to the lower-face optimizer `lambda`.

## Result

The audit checked `230` pre-existing tight rows, including `196`
post-discovery rows.

For post-discovery rows:

```text
actual mass on lower-face support:
  min   0.0
  mean  0.00298102069845743
  max   0.012172473138011076

total variation from lower-face optimizer:
  min   0.9878275268619889
  mean  0.9970189793015426
  max   1.0000000000000002

surplus above lower face:
  min   3.131031037561594
  mean  5.496203298315322
  max   7.8631684141402225

positive/negative signed transport ratio:
  min   3.273467296185124
  mean  6.754054098893982
  max   9.410452590913094
```

The tightest post-discovery row is `548126`:

```text
actual full:                         0.5953011116701273
lower-face full:                    -2.5357299258914665
surplus above lower face:            3.131031037561594
actual mass on lower-face support:   0.0
total variation from lower face:     1.0
positive/negative transport ratio:   5.477628478253741
```

## Interpretation

This is the first anti-extremality candidate that survives the local
falsifier.  The bad lower-face measures are not ruled out by coefficient
geometry, and they are not ruled out by a max-density cap, but actual
post-discovery prime-pair measures land almost disjointly from the lower-face
optimizer support.

The theorem target can now be stated without hunting for another row filter:

```text
Actual strict-central W_N has small overlap with the lower-face optimizer
support B_a(F3(mu_N)), and the signed transport away from that face has
positive/negative ratio > 1.
```

This is still a signed binary-prime correlation theorem.  It is useful because
it names the bad object explicitly: the lower-envelope optimizer, not a vague
negative channel set or a generic uniformity ball.

## Candidate theorem

For each even residue `a mod 10010`, define the lower-face optimizer set
`B_a(t)` from the LP

```text
L_a(t)=min Full(lambda),  F3(lambda)=t.
```

Find explicit `N0(a)` and margins `beta_a(N), rho_a(N)` such that for every
even `N>=N0(a)` in the q286 tail lane:

```text
mu_N(B_a(F3(mu_N))) <= beta_a(N)
```

and

```text
transport_positive(mu_N-lambda_a) >
transport_negative(mu_N-lambda_a) + rho_a(N).
```

Together with `Full(lambda_a)=L_a(F3(mu_N))`, this would imply

```text
Full(mu_N) > 0
```

after the finite boundary split if the surplus beats `-L_a(F3(mu_N))`.

## Falsifier

The candidate is falsified if a predeclared later q286 tail row has high mass
on `B_a(F3(mu_N))`, small total variation from the lower-face optimizer, or
positive/negative transport ratio `<=1` while still lying in the post-boundary
class.


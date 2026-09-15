# q286 proof-definition pivot

Status: theorem-shaping note.  This is not a threshold theorem, signed
correlation theorem, pointwise character-sum theorem, or Goldbach proof.

## Why this pivot is needed

The q286 receipts have reached the point where additional finite audits are
mostly measuring the same obstruction at higher resolution.  The next progress
bar is not more rows; it is a mathematical definition that lets a theorem say
what class of rows is being controlled and what operator is being bounded.

In particular, `post-discovery` is currently a computation-schedule phrase,
not a mathematical class.  It must be replaced by either:

- an explicit threshold statement, such as all relevant even `N >= N0`;
- a non-post-hoc arithmetic selector, such as a residue/correlation/cone
  condition stated before looking at outcomes; or
- a proof that no such local selector exists and that the remaining obligation
  is inherently a signed prime-correlation theorem.

Until one of those exists, more scans can strengthen finite evidence but cannot
close the proof.

## Current q286 objects

Fix `q=286=2*11*13`.  For each even target `N`, the current verifier forms a
strict-central prime-pair residue distribution and projects its q286 deviation
onto frozen singular-mode matrices.  Let `P(N)>0` denote the principal
contribution used for normalization.

Define the normalized first-three mode pressure:

```text
F3(N) = mode_1(N)/P(N) + mode_2(N)/P(N) + mode_3(N)/P(N).
```

The current first-three-tail predicate is:

```text
F3(N) < -0.3.
```

Define the complement ratio:

```text
C(N) = full_action(N)/P(N) - F3(N).
```

The full normalized action is therefore:

```text
A(N) = F3(N) + C(N).
```

The principal-only surplus after the first three modes is:

```text
S(N) = 1 + F3(N).
```

The nonprincipal drag against that surplus is:

```text
D(N) = max(0, 1 - C(N)).
```

When `C(N) <= 1`, full positivity is exactly:

```text
S(N) > D(N).
```

When `C(N) > 1`, the complement supplies a positive bonus and `D(N)=0`, so
`S(N)>0` is already enough.

Thus the finite checked suffix can be restated as a ratio-envelope target:

```text
D(N) / S(N) < 1
```

on first-three-tail rows with `S(N)>0`.

## Candidate theorem statement

Candidate, not proved:

For all even `N` in a yet-to-be-defined q286 suffix class `Q286*`, if
`F3(N)<-0.3`, then:

```text
S(N)>0
and
D(N)/S(N) <= 1 - eta(N)
```

for some positive margin `eta(N)`.

The checked finite data show this shape on blocks `1..11`, with worst observed
post-discovery ratio `0.9696841556062236` at target `94856`.  The margin is
therefore near-sharp; an eventual proof cannot use a loose average estimate.

## What is missing

The missing definition is `Q286*`.

A useful definition must be fixed before looking at new outcomes and must
predict the difficult rows differently from a generic finite scan.  Acceptable
forms include:

- an explicit analytic threshold `N>=N0` with a proof;
- an arithmetic residue/correlation condition that excludes the discovery
  drag-overturn rows while retaining the checked suffix rows;
- a convex-cone statement on admissible prime-pair residue measures whose
  inequalities imply `S>D`; or
- a Fourier/operator estimate bounding the nonprincipal part relative to the
  principal-only surplus.

Unacceptable forms:

- `rows after block 0`, unless backed by a theorem explaining why that block
  boundary matters;
- `rows that pass D/S<1`, which is tautological;
- a fitted finite classifier without a frozen arithmetic mechanism;
- another broad scan with no new definition or falsifier.

## Pivot rule

Do not run another q286 block scan merely to extend the table.  The next q286
work should be one of:

1. Define a non-post-hoc candidate for `Q286*` and test it on already stored
   rows before any fresh scan.
2. Prove or source-bound an operator inequality that implies `D/S<1`.
3. Show that every plausible local definition collapses to a signed
   prime-correlation estimate, and preserve the route as an explicit theorem
   obligation rather than another audit lane.

## Current finite evidence

The latest receipts supporting this definition layer are:

```text
evidence/q286-principal-rescue-obstruction-audit.json
evidence/q286-nonprincipal-drag-envelope-audit.json
```

They prove only checked finite statements.  They do not prove Goldbach.

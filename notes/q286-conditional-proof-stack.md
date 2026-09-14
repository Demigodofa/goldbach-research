# q286 Conditional Proof Stack

Status: conditional theorem bookkeeping only.  This is not a proof of
Goldbach.

Date: 2026-09-14.
Source checkpoint: `86b4af821ccec2bbdb2edb8ab96ddf66c84e34cf`.

## Purpose

The q286 work now has several useful but separate records:

- finite denominator scans for when the active tail appears;
- an active-selector rarity obligation for the q286 first-three term;
- an alignment/complement theorem obligation for first-three tail targets;
- a component-pair conditional closure for the active lower-support lane;
- boundary witnesses showing that support, nonnegativity, and total mass are
  not enough.

This note states the strongest current theorem stack in one place, with the
exact proof gaps preserved.  It is meant to prevent finite receipts from being
mistaken for a universal theorem.

## Fixed Quantities

For each strict-central even target `N`, the q286 lane uses:

- `F3(N)`: the normalized first-three q286 singular-mode contribution.
- `C3(N)`: the normalized complement
  `full_without_first_three_to_principal_ratio`.
- `B2(N)`: the implemented q286 first-three `L2` Cauchy envelope
  `||c_a||_2 ||d_N||_2 / P(N)`.
- `L12(N)`: the normalized sum of the first two q286 singular-mode
  coordinates.
- `M_active(N)`: the calibrated strict closure margin from
  `q286_active_lane_strict_closure_margin_census_receipt`,

```text
M_active(N) = D(N) - d0 + L * (B - max_channel(N)).
```

The current constants for that active closure are:

```text
d0 = -0.1017253843274695
L  = 15.262957606760951
B  = 0.05885324711081062
```

The current active selector is:

```text
L12(N) < -0.2
F3(N) < -0.3
```

## Conditional Theorem A: Rarity Route

Let `N0` be an explicit finite boundary.  Suppose that for every
strict-central target `N >= N0` in the outer assembly:

```text
F3(N) >= -0.3,
C3(N) > 0.3.
```

Then `F3(N) + C3(N) > 0` for all such targets, so the q286 first-three split
does not obstruct strict-central positivity after the finite boundary check.

Current status: unproved.  The first inequality is exactly the
active-selector rarity obligation.  The quantified norm certificate shows a
plain sufficient `L2` discrepancy theorem would need relative control at
least as strong as `0.005955161523943415` in the worst q286 residue class.
The second inequality is a complement lower-envelope theorem, also unproved
as a universal statement.

## Conditional Theorem B: Alignment/Complement Route

Let `N0` be an explicit finite boundary.  Suppose that for every target
`N >= N0` in the first-three lower-tail set `F3(N) < -0.3`:

```text
F3(N) >= -0.4 * B2(N),
C3(N) >  0.4 * B2(N).
```

Then `F3(N) + C3(N) > 0` on the first-three lower tail.  Targets outside the
tail still require their own complement floor, for example `C3(N) > -F3(N)`.

Current status: unproved.  The finite window `105..136` satisfies the measured
certificate on its three `.3` tail rows, and cycles `233..264` have no `.2`
or `.3` tail rows.  These are finite evidence only.  The boundary target
`14138` is an explicit failure of this sufficient condition and must be in a
finite boundary layer or handled by a different argument.

## Conditional Theorem C: Active-Lane Strict Closure

Let `N0` be an explicit finite boundary.  Suppose that every target
`N >= N0` satisfying the active selector also satisfies:

```text
M_active(N) > 0.
```

Then the calibrated component-pair identity gives positive recombined action
on the active lower-support lane.  Equivalently, one may prove the separated
sufficient conditions:

```text
D(N) >= d0 + eta_D,
max_channel(N) <= B - eta_B,
eta_D + L * eta_B > 0.
```

Current status: unproved.  The selected late active rows
`1222142`, `1323632`, and `1379072` have positive strict margins, but the
strict closure margin has not been stressed on a broad active population
because broad denominator scans have not produced active rows.

## Boundary And Outer Assembly Still Required

Any q286 conditional theorem above still needs:

- an explicit finite boundary set and exact verification for all targets below
  the stated onset;
- endpoint and noncentral terms;
- the full outer assembly connecting this strict-central q286 positivity to
  actual Goldbach coverage;
- independent mathematical review of any promoted pointwise prime-correlation
  estimate.

Therefore the current strongest honest statement is:

```text
If the named q286 pointwise residue-correlation hypotheses and finite
boundary checks are proved, then this q286 strict-central obstruction lane
closes.
```

It is not:

```text
Goldbach is proved.
```

## Falsifiers

- Any unchanged-selector target with `F3(N) < -0.3` and nonpositive
  `M_active(N)` falsifies the current active-lane strict closure constants.
- Any sufficiently late target with `F3(N) < -0.3` and
  `C3(N) <= 0.4 * B2(N)` falsifies the current alignment/complement theorem
  candidate outside the boundary layer.
- Any proof that the required q286 pointwise inequalities imply pointwise
  Goldbach in fixed residue classes should be recorded as a hard theorem
  equivalence/impasse, not as a solved proof.

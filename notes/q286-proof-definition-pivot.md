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
evidence/q286-convex-envelope-obstruction-audit.json
evidence/q286-max-density-anti-extremality-audit.json
evidence/q286-lower-face-overlap-audit.json
```

They prove only checked finite statements.  They do not prove Goldbach.

## Convex-envelope refinement

`tools/build_q286_convex_envelope_obstruction_audit.py` generated
`evidence/q286-convex-envelope-obstruction-audit.json`.

This refines the cone-duality target without scanning new targets.  For each
tested residue, the reflection simplex is pushed into the `(F3, Full)` plane
and LP computes the coefficient-only lower envelope at observed `F3` values.

Result: every one of the `204` tested residues admits a synthetic tail failure
inside the coefficient hull, and actual post-discovery rows sit at least
`3.1310310375615944` above the lower envelope.

Therefore `Q286*` cannot be defined by support, reflection, and q286
coefficient geometry alone.  A viable definition must add arithmetic
anti-extremality: actual strict-central prime-pair measures avoid the lower
convex face of the coefficient hull.

## Max-density demotion

`tools/build_q286_max_density_anti_extremality_audit.py` generated
`evidence/q286-max-density-anti-extremality-audit.json`.

This tests the first simple anti-extremality cone:

```text
mu(orbit) <= lambda*u_a(orbit).
```

Result: every actual row fails the sufficient max-density certificate.  The
minimum bad max-density multiple is only `1.0357032987728947..1.2007521303394815`,
while actual rows have maximum orbit-density multiple
`3.3411693332118935..25.29622421615252`.

Thus the lower-face avoidance is not explained by small atoms.  The next
definition must control signed landing relative to the coefficient face, not
only absolute concentration relative to uniform.

## Lower-face overlap candidate

`tools/build_q286_lower_face_overlap_audit.py` generated
`evidence/q286-lower-face-overlap-audit.json`.

This tests the face-relative replacement for max-density.  At each actual
row's observed `F3`, solve the coefficient-only lower-envelope optimizer
`lambda_a`, then compare actual `mu_N` to that optimizer.

Post-discovery rows have at most `0.012172473138011076` actual mass on the
lower-face optimizer support, total variation from the optimizer at least
`0.9878275268619889`, and positive/negative transport ratio at least
`3.273467296185124`.

This preserves a real candidate for `Q286*`: not small absolute
concentration, but small overlap with the bad lower face and positive signed
transport away from it.

## Lower-face support signature refinement

`tools/build_q286_lower_face_support_signature_audit.py` generated
`evidence/q286-lower-face-support-signature-audit.json`.

This checks whether the bad lower-face support is itself a simple residue
dictionary.  Result: no fixed residue selector is visible at this scale.  The
`196` post-discovery rows all have two complement-closed lower-face support
orbits, and the negative-Full lower-mass fraction is at least
`0.932438665145394`, but there are `126` distinct support signatures modulo
`286`; the most common one covers only `14` rows.

Thus the current `Q286*` definition should not be "avoid this fixed residue
set."  It should be face-relative: for the target residue `a` and observed
`t=F3(mu_N)`, actual prime-pair mass must avoid the LP-defined bad support
`B_a(t)` and carry positive signed transport away from the corresponding
optimizer.

## Dual-edge rescue refinement

`tools/build_q286_lower_face_dual_edge_audit.py` generated
`evidence/q286-lower-face-dual-edge-audit.json`.

For each checked row, the two-orbit lower-face optimizer defines an affine
lower edge

```text
ell_a,t(x) = slope_a,t * F3(x) + intercept_a,t
```

and an orbit gap

```text
g_a,t(x)=Full(x)-ell_a,t(x).
```

The finite audit verifies `g_a,t>=0` on every coefficient orbit to floating
precision.  On post-discovery rows, the exact theorem-shaped rescue ratio

```text
E_mu_N[g_a,t] / max(0,-ell_a,t(t))
```

ranges from `1.0021652272515458` to `1.3070973629998075`.  Thus the next
definition is a near-sharp dual-edge gap theorem, not a looser channel,
residue, max-density, or L1-uniformity theorem.

## Unnormalized edge-witness refinement

`tools/build_q286_unnormalized_dual_edge_witness_audit.py` generated
`evidence/q286-unnormalized-dual-edge-witness-audit.json`.

Multiplying the dual-edge identity by the strict-central pair mass `T_N`
gives:

```text
raw_edge_gap - raw_required_edge_gap = T_N * Full(mu_N).
```

On post-discovery rows, the raw margin after rescue is
`490.7620118705381..361940.33348482125`, with identity error at most
`2.3283064365386963e-10`.  This gives the right theorem language:

```text
prove raw_full_signed_witness > 0 directly.
```

It does not close the normalization gap, because the receipt is computed on
rows where strict-central pair mass was already observed.

## Edge-minorant obstruction

`tools/build_q286_edge_minorant_obstruction_audit.py` generated
`evidence/q286-edge-minorant-obstruction-audit.json`.

This tests the easy coefficientwise minorant route.  For the dual edge, write
the rescue margin as:

```text
E_mu_N[gap-required].
```

If `gap-required` were nonnegative on every reflection orbit, ordinary
nonnegative pair mass would be enough.  It is not: on post-discovery rows the
pointwise minorant pass count is `0/196`, and the lower-face support itself
carries negative pointwise rescue coefficients on `196/196` rows.

Actual rows rescue by distributional landing.  Their positive/negative rescue
ratio is `1.0191444227555964..3.167398344085266`.  Therefore the next
definition must control signed landing against the negative rescue coefficient
set; it cannot be only a coefficientwise nonnegative minorant.

## Anti-landing mass-balance refinement

`tools/build_q286_anti_landing_mass_balance_audit.py` generated
`evidence/q286-anti-landing-mass-balance-audit.json`.

This tests whether signed landing can be weakened to a simple mass-majority
condition.  It cannot.  On the `196` post-discovery rows, actual pair mass
lands more on positive rescue coefficients in `178` rows, but `18` rows
rescue despite having more mass on negative rescue coefficients.

All `196` rows satisfy the sharper coefficient-weighted inequality:

```text
average_positive_rescue_coefficient / average_negative_rescue_coefficient
  >
mass_negative / mass_positive.
```

The checked coefficient-lift surplus range is
`0.01681775158832699..1.568503471168754`.  Thus `Q286*` cannot be defined by
unweighted support mass alone; it must include signed landing quality,
prime-pair correlation, or an equivalent fixed-modulus binary-prime theorem.

## Source-backed stop/go rule

`notes/q286-source-backed-theorem-pivot.md` turns this into a stop/go rule.
The next proof-relevant object is the raw weighted binary-prime sign sum
`B_Phi(N)`.  A finite q286 audit now counts as progress only if it changes a
predeclared implication toward:

```text
B_Phi(N) > 0
```

for all sufficiently large covered even `N`, plus finite verification below
the threshold.  Otherwise the q286 lane should be treated as finite structure
and put to sleep as a Goldbach proof engine.

## q286-WBSS main-term sign

`tools/build_q286_wbss_main_term_sign_audit.py` generated
`evidence/q286-wbss-main-term-sign-audit.json`.

This confirms that the current proof target is not doomed by sign of the
local-uniform main term.  On the checked `196` post-discovery rows, both the
frozen full q286 coefficient and the target-dependent edge beta coefficient
have positive local-uniform means.  The tightest sufficient L1 budgets are
about `0.020711496156757627` for the full coefficient and
`0.026797640365636533` for edge beta.

Therefore a valid `Q286*` definition could be a source-backed pointwise
binary-prime orbit-distribution class:

```text
||mu_N-u_a||_1 < mean_u(Phi_a)/||Phi_a-mean_u(Phi_a)||_infty.
```

No such theorem is currently proved here.

## L1 uniformity demotion

`tools/build_q286_wbss_l1_budget_obstruction_audit.py` generated
`evidence/q286-wbss-l1-budget-obstruction-audit.json`.

The displayed L1 condition is only a sufficient condition and is too strong
for the observed q286 rows.  Actual L1 distances are
`0.5533526980785324..1.574410774410774`, and no checked post-discovery row is
inside the full or edge-beta sufficient L1 budget.

So a future `Q286*` definition should not demand ordinary total-L1 closeness
to local uniform.  It must be signed/coefficient-sensitive or unnormalized.

## Coefficient-aligned replacement

`tools/build_q286_wbss_signed_discrepancy_problem.py` generated
`evidence/q286-wbss-signed-discrepancy-problem.json`.

The replacement problem is exact:

```text
lambda_phi(N) = -<mu_N-u_a, phi_a-m_a> / m_a < 1.
```

This is equivalent to positive signed expectation because the checked local
means are positive.  It is still useful because it names the one signed
projection that must be controlled; all orthogonal distributional mess can be
ignored for this bridge.  The finite post-discovery rows all pass the scalar
threshold, while none pass the old L1 budget.

Next work should seek a real theorem for `lambda_phi(N)<=1-eta(N)`, or move
directly to the unnormalized signed witness `B_Phi(N)>0`.  A scan that only
adds more passing lambda rows without proposing a source-backed bound should
be treated as low-value.

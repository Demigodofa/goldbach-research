# q286 proof fixture stack

Status: proof-navigation artifact.  Goldbach is not proved.

The current q286 route should be handled like a physical fixture, not like a
free-space fabrication.  The exact algebraic identities are the bolted frame
points.  The unresolved analytic estimates are tacks.  A condensed theorem
should only be welded out after every tack is proved against the actual q286
frame.

## Bolted anchors

- `evidence/q286-first-three-mass-landing-obligation.json`:
  `first_three = P-B = m_plus*ell_plus - m_minus*ell_minus`.
- `evidence/q286-first-three-signed-projection-obligation.json`:
  with `delta_N=mu_N-u_a`, `first_three(N)=<delta_N,c_a>`.
- `evidence/q286-first-three-residue-pair-correlation-obligation.json`:
  the signed-projection tack is exactly the fixed-modulus residue-pair
  discrepancy inequality against centered coefficients `gamma_a(u)`.
- `evidence/q286-residue-pair-external-theorem-comparison.json`:
  average, almost-all, distribution, and upper-bound AP-Goldbach results do
  not supply the pointwise q286 obligation as stated; full fixed-modulus AP
  asymptotics would imply it but are Goldbach-strength for strict-central AP
  existence.
- `evidence/q286-residue-pair-character-mode-narrowing.json`:
  near-boundary samples are almost perfectly same-sign negative in the
  rank-three q286 first-three character-mode ledger, so internal mode
  cancellation is not the observed rescue mechanism there.
- `evidence/q286-first-three-singular-mode-residue-obligation.json`:
  each singular coordinate is now an exact centered residue-discrepancy
  projection; modes `1` and `2` are same-sign negative on the three
  near-boundary samples, and their sum falls below `-.3` only on tail
  `1222142`.
- `evidence/q286-first-three-dominant-mode-reflection-support-obstruction.json`:
  support, nonnegativity, total mass, and ordered-pair reflection symmetry
  alone do not force the dominant `mode_1+mode_2` sum above `-.3`; every even
  q286 residue has a positive reflected synthetic witness below the floor.
- `evidence/q286-first-three-dominant-mode-character-sum-obligation.json`:
  the surviving dominant `mode_1+mode_2` residual is now an exact q286
  character-sum obligation with `50` active complex products collapsing to
  `25` real conjugacy channels.
- `evidence/q286-first-three-dominant-mode-channel-norm-budget.json`:
  independent `Linf`/`L2` smallness of the `25` real channels is sufficient
  but too blunt on the current near-boundary samples; clear rows fail the
  budgets while passing by signed structure.
- `evidence/q286-first-three-dominant-mode-signed-channel-profile.json`:
  the signed structure is now split exactly into positive offset and negative
  pressure; active samples suggest two theorem branches, pressure below `.3`
  or enough positive offset above pressure.
- `evidence/q286-first-three-dominant-mode-signed-channel-branch-sample.json`:
  deterministic near-boundary mass-matched samples show that the clear rows
  mostly use the positive-offset branch under pressure, while five sampled
  rows remain true finite deficits.  This demotes a pressure-ceiling-only
  explanation for the selected rows.
- `evidence/q286-first-three-dominant-mode-channel-swing-pairs.json`:
  selected deficit-to-clear pairs have recurrent helpful channels `(2,6)` and
  `(3,1)`, but the helpful swing is portfolio-level: reaching `80%` of
  positive delta takes `5` to `9` helpful channels across the checked pairs.
  This demotes a one- or two-channel offset lemma.
- `evidence/q286-first-three-dominant-mode-helpful-portfolio.json`:
  freezing the helpful labels into fixed portfolios separates the selected
  clear rows from selected deficits, but the universal two-channel portfolio
  captures as little as `0.0534` of a positive swing delta and the recurrent
  portfolio still leaves a nonportfolio residual.
- `evidence/q286-first-three-dominant-mode-portfolio-residual-obligation.json`:
  bolting on the `11`-channel recurrent portfolio and subtracting it from the
  selected dominant rows gives the exact rowwise obligation
  `portfolio_sum >= -0.3 - nonportfolio_residual_sum`; the remaining theorem
  is a portfolio lower bound against this residual requirement, or a residual
  theorem that keeps the requirement in range.
- `evidence/q286-first-three-dominant-mode-residual-channel-profile.json`:
  the `14` residual channels left after subtracting the recurrent portfolio do
  not contain an individual channel separator on the selected fixture, and the
  residual delta is negative in every selected deficit-to-clear pair.  This
  demotes a small residual-channel classifier and leaves the recurrent
  portfolio as the object that must overcome adverse residual requirements.
- `evidence/q286-first-three-dominant-mode-portfolio-ablation.json`:
  leave-one-out and prefix ablations of the fixed recurrent portfolio show
  that a four-channel prefix keeps every selected clear row passing but also
  over-rescues every selected deficit, while the full selected classification
  first reappears at all `11` recurrent channels.  This separates the
  lower-bound theorem target from exact deficit/clear classification.
- `evidence/q286-first-three-dominant-mode-prefix-tail-classification.json`:
  the four-channel clear prefix and seven-channel classification tail satisfy
  `full_portfolio = prefix + tail`, with exact tail obligation
  `tail_sum >= -prefix_slack`; the prefix over-rescues all selected deficits
  and the tail restores them while preserving all selected clears.
- `evidence/q286-first-three-dominant-mode-tail-ablation.json`:
  the seven-channel classification tail is not compressed by tested
  leave-one-out or prefix ablations; every tail channel is essential for the
  selected tail classification, and the first successful tail prefix is the
  full seven-channel tail.
- `evidence/q286-first-three-dominant-mode-residual-staircase.json`:
  the selected prefix/tail order has an exact cumulative ledger.  The
  four-channel prefix is the first stage clearing all selected clear rows but
  still over-rescues all five selected deficits; the first stage matching the
  selected dominant-floor classification is the full eleven-channel portfolio.
  The tail is signed rather than monotone-positive, so the missing theorem is
  cumulative portfolio control or a replacement deficit-exclusion theorem.
- `evidence/q286-first-three-dominant-mode-staircase-geometry-obstruction.json`:
  weak support/nonnegativity/total/reflection geometry does not force the
  staircase.  At the full stage every selected pass can be made to fail
  synthetically, every selected deficit can be over-rescued synthetically, and
  no selected classification is geometry-forced.
- `evidence/q286-first-three-dominant-mode-staircase-arithmetic-gap.json`:
  actual strict-central prime-pair rows sit inside those weak-geometry
  intervals, but the intervals are far too wide.  Full-stage pass positions
  are about `0.2166..0.3528`, deficit positions about `0.2887..0.4044`, while
  actual one-sided margins are only about `0.008833..0.099229`.
- `evidence/q286-first-three-dominant-mode-staircase-orbit-mass-gap.json`:
  the weak synthetic obstruction breaks rows by concentrating on extremal
  reflected orbits, but actual prime-pair mass is not concentrated there on
  the selected fixture.  Full-stage breaker-orbit mass ranges from `0` to
  about `0.0246193103`, while top actual orbit mass ranges from about
  `0.0256818041` to `0.0831971135`; the breaker orbit is never the top
  actual mass orbit.
- `evidence/q286-first-three-dominant-mode-staircase-hinge-decomposition.json`:
  each selected staircase row is exactly decomposed into above-floor positive
  hinge minus below-floor negative hinge, with maximum identity error about
  `3.33e-16`.  Full-stage supporting and opposing masses both stay near
  one-half, and the selected rows split between mass-driven and landing-driven
  classifications.
- `evidence/q286-first-three-dominant-mode-staircase-hinge-threshold.json`:
  the hinge balance is equivalently the support-mass threshold
  `supporting_mass >= opposing_landing/(supporting_landing+opposing_landing)`.
  Full-stage surplus ranges from about `0.0028592222` to `0.0330812983`,
  with tightest row `1222142`.  The support side is still inherited from the
  finite classification, so this is an obligation form, not a theorem.
- `evidence/q286-first-three-dominant-mode-staircase-above-floor-threshold.json`:
  the post-hoc support side is replaced by the arithmetically defined
  above-floor orbit set.  At the full stage, the above-floor signed surplus is
  positive on selected passes and negative on selected deficits, with tightest
  absolute surplus about `0.0028592222`.  The empty stage has ten sign errors,
  so the formulation is a full-stage target, not an all-prefix theorem.
- `evidence/q286-first-three-orbit-uniformity-budget.json`:
  generic orbit uniformity is a valid sufficient theorem but too blunt, since
  clear rows `1242118` and `1240888` fail the sufficient budgets.
- `evidence/q286-first-three-mass-matched-pair-decomposition.json`:
  mass/landing pair evidence keeps the surviving mechanism coefficient
  sensitive.

## Tacked unresolved joints

1. Prove the q286 first-three signed-projection anti-alignment theorem:
   `<delta_N,c_a> >= -0.3`, or the equivalent cosine floor, for all
   sufficiently large targets in the lane.
2. Prove the conditioned complement or lower-support rescue needed after the
   first-three lane is controlled.
3. Prove or cite the required pointwise binary-prime residue-correlation
   theorem:
   `sum_{u in A_a}(W_N(u)-T_N/|A_a|)*gamma_a(u) >= -tau*T_N`.
   The current residual ledger shows the largest local deficits are not
   anonymous noise; residues such as `133` and `153` dominate the sample
   tail/near-clear rows.
4. Prove a lower bound for the combined dominant singular-mode projection
   `mode_1(N)+mode_2(N)`, or classify the arithmetic conditions that stop
   simultaneous strong negativity in those two coordinates.  The
   support/reflection-only version of this tack is now obstructed, so the
   surviving proof must use actual prime-pair arithmetic or a stronger
   residue-weight constraint.  The current exact arithmetic formulation is
   pointwise signed control of `25` real q286 binary-prime character channels;
   plain independent channel `Linf`/`L2` control is sufficient but already too
   blunt on the active samples.  The sharper split is negative-channel
   pressure versus positive-channel offset, and the wider branch sample points
   toward offset forcing under pressure rather than a pressure ceiling alone.
   The swing-pair decomposition further sharpens this to a helpful-channel
   portfolio estimate, not a tiny-channel lemma.  The fixed-portfolio
   diagnostic preserves the recurrent portfolio as a finite candidate while
   keeping the nonportfolio residual explicit.  The portfolio/residual
   obligation now rewrites that residual explicitly as the rowwise required
   portfolio floor.  The residual-channel profile demotes a one-channel
   residual classifier: no residual channel separates the selected outcomes,
   and residual deltas move against the clear side on all selected pairs.
   The portfolio ablation then splits the surviving target into a possible
   smaller clear-side lower-bound package and a separate classification or
   exclusion problem for over-rescued deficits.  The prefix/tail receipt makes
   that split exact: prove prefix lower bounds and tail/exclusion control.
   The tail-ablation receipt further says the selected tail control is a
   seven-channel package on current evidence, not a one-channel or proper
   prefix correction.  The residual-staircase receipt then shows the signed
   cumulative load path: the prefix clears all selected clears while
   over-rescuing all selected deficits, intermediate tail channels can knock a
   clear row below the floor, and only the full eleven-channel portfolio
   matches the selected classification.  The staircase-geometry obstruction
   closes the weak-geometry proof shortcut under that load path: actual
   prime-pair arithmetic or stronger residue-weight structure is required.
   The arithmetic-gap receipt quantifies this requirement as pointwise
   placement inside a broad weak cone: lower bounds for selected pass rows and
   upper bounds/exclusion or complement rescue for selected deficits.  The
   orbit-mass gap receipt then isolates one concrete subclaim: actual
   prime-pair mass must be bounded away from the reflected breaker orbits, or
   the signed aggregate must be controlled in a way that neutralizes those
   orbits.  The hinge-decomposition receipt shows that the selected fixture is
   a mixed mass-and-landing balance, not a one-dimensional mass cap or landing
   floor.
5. Prove the dangerous reflected-orbit mass-control tack for the dominant
   staircase, or replace it with an equally explicit signed aggregate theorem.
6. Prove the row-dependent hinge-balance theorem for actual q286 reflection
   orbits, or replace it with an equally explicit signed aggregate theorem.
7. Prove or replace the hinge-threshold surplus theorem
   `supporting_mass - opposing_landing/(supporting_landing+opposing_landing)
   > 0`, including a non-circular arithmetic definition of the intended
   support side.
8. Prove the non-post-hoc full-stage above-floor threshold sign theorem:
   the sign of
   `above_mass - below_landing/(above_landing+below_landing)` matches the
   required q286 dominant staircase side.  Do not promote this to an
   all-prefix theorem unless the empty-stage and other prefix failures are
   separately handled.
9. Finish the finite boundary, endpoint, noncentral, and outer-assembly work.

## Condensation rule

Do not condense this into a Goldbach proof until all tacked joints are proved.
When they are, the route can be shortened to a conditional theorem stack:
signed projection controls q286 first-three; complement/lower support rescues
the remaining strict-central action; finite and endpoint assembly close the
global statement.

Current next non-circular action: prove a lower bound for the recurrent
helpful-channel portfolio or its clear-side four-channel prefix against the
rowwise residual requirement, then prove tail classification or a separate
exclusion/complement mechanism for prefix-overrescued deficits, or reduce the
same claim to a fixed-modulus strict-central binary Goldbach/AP theorem.
Current finite evidence says the dominant projection is a prefix/tail
portfolio arithmetic problem, not a geometry-only, tiny-channel, or one-piece
classifier problem; the tested tail itself is also not visibly compressible
and not monotone-positive under the frozen channel order.  Weak reflected
geometry also does not force the frozen staircase classifications.  The
current quantitative target is actual arithmetic placement inside the broad
weak-geometry interval, not shrinking that interval by geometry alone.  The
newest sharpened subtarget is actual mass control on the dangerous reflected
breaker orbits used by the synthetic weak-geometry witnesses, now refined by
the mixed hinge-balance decomposition and its tiny positive threshold surplus.
The current non-post-hoc version is the full-stage above-floor signed surplus;
prefix-stage failures must remain visible.

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
   portfolio floor.
5. Finish the finite boundary, endpoint, noncentral, and outer-assembly work.

## Condensation rule

Do not condense this into a Goldbach proof until all tacked joints are proved.
When they are, the route can be shortened to a conditional theorem stack:
signed projection controls q286 first-three; complement/lower support rescues
the remaining strict-central action; finite and endpoint assembly close the
global statement.

Current next non-circular action: prove a lower bound for the recurrent
helpful-channel portfolio against the rowwise residual requirement, prove a
residual-channel theorem that keeps that requirement in range, or reduce the
same claim to a fixed-modulus strict-central binary Goldbach/AP theorem.
Current finite evidence says the dominant projection is a portfolio/residual
arithmetic problem, not a geometry-only or tiny-channel problem.

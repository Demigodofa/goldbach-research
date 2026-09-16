# q286-WBSS negative-region mass threshold audit

## Question

After the pointwise positive floor fails, what negative-region mass or
signed-shape control would still make the single q286 weight positive?

## Receipt

```text
tools/build_q286_wbss_negative_region_mass_threshold_audit.py
evidence/q286-wbss-negative-region-mass-threshold-audit.json
```

## Result

The crude sign-only route is too strong.  If all positive mass were allowed to
sit at the smallest positive coefficient and all negative mass at the most
negative coefficient, the admissible negative-mass fraction would need to be
tiny:

```text
robust sign-mass threshold: 0.0007147368046632611..0.0033012537800608146
local-uniform negative fraction: 0.296969696969697..0.47205387205387206
local-uniform rows passing robust threshold: 0 / 5005
```

So a theorem saying only "few prime pairs land in the negative region" would
need an unrealistically severe bound.

The meaningful target is signed shape or correlation.  If the within-sign
conditional averages are no worse than their local-uniform averages, then the
negative-mass cutoff is much larger:

```text
shape mass threshold: 0.48729403831397616..0.6355852930606508
local-uniform margin to shape threshold: 0.10534041937277128..0.27126236049137376
local-uniform rows passing shape threshold: 5005 / 5005
```

This explains why the local-uniform major term remains positive even though
every target has negative admissible residues.

## Raw Theorem Boundary

The theorem must ultimately be raw and strict:

```text
sum_{u:phi(u)>0} P_N(u)phi(u)
  > sum_{u:phi(u)<0} P_N(u)(-phi(u)).
```

Here `P_N(u)` is raw strict-central log-pair mass with left prime residue `u`.
Normalized statements about fractions of mass in the negative region are useful
diagnostics, but by themselves they are conditional on `T_N>0`.  They do not
prove strict-central support unless embedded in a raw strict positivity proof.

## Decision

`TARGET_signed_negative_region_correlation_obligation`.

The pointwise floor failure does not force q286 to sleep.  It does sleep the
support-only and robust sign-mass-only shortcuts.  The surviving target is a
universal pointwise signed-shape/correlation theorem, a raw adverse-drag
theorem, or a direct major/minor arc estimate proving the positive weighted
mass exceeds the adverse weighted mass for every sufficiently large covered
`N`.

This proves no signed negative-region distribution theorem, raw adverse-drag
theorem, positive-mass theorem, q286 threshold theorem, strict-central
Goldbach theorem, or Goldbach proof.

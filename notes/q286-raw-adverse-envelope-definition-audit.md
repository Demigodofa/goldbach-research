# q286 raw adverse-envelope definition audit

## Question

Can the q286 adverse-envelope route be stated as a genuinely raw, non-circular theorem target, and exactly where do T_N or mu_N dependencies remain?

## Receipt

```text
tools/build_q286_raw_adverse_envelope_definition_audit.py
evidence/q286-raw-adverse-envelope-definition-audit.json
```

## Result

```text
finite calibration rows:                  348
max checked raw adverse ratio:             0.23148438379145228
min checked raw adverse gate gap:          286929.1729900494
all checked raw gate gaps positive:        True
finite evidence is acceptance condition:  false
raw adverse-envelope theorem proved:      false
```

The strict statement `A_raw_-(N)<L_raw(N)` is non-circular in form:
if strict-central support is empty, both sides are zero and the strict
inequality fails.  A proof of the strict inequality would therefore
create support.

But the proof must be stated directly in raw sums.  `U_d=T_N*E_d` is
only safe as shorthand after `U_d` is also defined without `mu_N`.
Likewise `L_raw=T_N*M(a)` is a raw-form local main, but it cannot be
made positive by assuming `T_N>0` unless the route is explicitly a
two-theorem bridge.

## Decision

The q286 adverse-envelope route survives as a non-circular strict theorem shape only when it is stated directly in raw unnormalized sums.  The definitions L_raw=T_N*M(a) and U_d=T_N*E_d are dangerous if E_d is first introduced through mu_N: that is a mass-positive shorthand, not the theorem.  The next useful object is a raw-sum expansion ledger for U_d and W_phi, or else an explicit two-theorem bridge with a separate positive-mass theorem.

This is a definition-boundary audit only.  It proves no positive-mass
theorem, raw adverse-envelope theorem, raw weighted witness theorem,
strict-central Goldbach theorem, or Goldbach proof.

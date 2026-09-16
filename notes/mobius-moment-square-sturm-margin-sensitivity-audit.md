# Mobius moment-square Sturm margin sensitivity audit

## Question

The Sturm certificate uses the recorded source curve coefficients and proves
`P_M(t) - 427/1000` has no real roots on the checked scales.  Does that tight
margin still survive if the polynomial is rebuilt from the serialized
coefficient-provenance receipt?

## Receipt

```text
tools/build_mobius_moment_square_sturm_margin_sensitivity_audit.py
evidence/mobius-moment-square-sturm-margin-sensitivity-audit.json
```

## Result

```text
status: FALSIFY_tight_margin_from_serialized_provenance_coefficients
tight margin:                         427/1000
tight source curve margin passes:     true
tight provenance margin passes:       false
tight failing provenance scales:      167
robust margin:                        21/50
robust source curve margin passes:    true
robust provenance margin passes:      true
```

At margin `427/1000`, the source curve coefficients remain root-free, but the
serialized coefficient-provenance reconstruction has `2` real roots at
`M=167`.

At margin `21/50`, both the source curve coefficients and the serialized
coefficient-provenance coefficients are root-free on every checked scale.

## Decision

This falsifies a tempting bridge: do not use rounded serialized provenance
coefficients to carry the tight `0.427` Sturm margin.  The tight margin belongs
only to the source curve coefficient receipt unless exact coefficient
derivations are available.

For cross-artifact finite work, `0.42` is the robust checked margin.  For a
universal theorem, the target is sharper:

```text
derive exact coefficient formulas, then prove the Sturm/sign certificate
directly; otherwise use a margin robust to the available coefficient error.
```

This is finite serialization-sensitivity evidence only.  No robust-margin
universal theorem, tight-margin serialized-provenance theorem,
coefficient-family theorem, universal Sturm-certificate theorem, half-frame
curve-positivity theorem, uniform active/full lower-frame theorem, Mobius
covariance theorem, signed prime-correlation estimate, q286 theorem,
strict-central Goldbach theorem, or Goldbach proof is established.

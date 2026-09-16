# Mobius moment-square Sturm margin-window audit

## Question

The robust Sturm chamber audit showed that margin `21/50` survives both the
source-curve coefficients and the independently serialized coefficient-
provenance reconstruction, while the tighter `427/1000` margin fails for the
provenance serialization at `M=167`.  How wide is that window?

## Receipt

```text
tools/build_mobius_moment_square_sturm_margin_window_audit.py
evidence/mobius-moment-square-sturm-margin-window-audit.json
```

## Method

Each recorded decimal coefficient is rationalized as `Rational(str(x))`.  For
each checked scale, the audit computes the stationary-point minimum of the
degree-8 polynomial and then brackets that critical value at denominator
`10^6` with exact Sturm root counts.  This audits the serialized polynomial
families.  It is not an exact symbolic active/full Gram theorem.

## Result

```text
status: MEASURE_serialized_sturm_margin_window
tight margin:                         427/1000
robust margin:                        21/50
controlling scale:                    M=167

source serialized critical margin:     0.4270105091865797085
source slack above 427/1000:           0.0000105091865797085

provenance serialized critical margin: 0.4269818990580671773
provenance slack above 427/1000:      -0.0000181009419328227
provenance slack above 21/50:          0.0069818990580671773
```

The `M=167` provenance margin is bracketed by Sturm counts:

```text
426981/1000000  -> 0 real roots after shift
213491/500000   -> 2 real roots after shift
```

## Decision

The robust `21/50` certificate has real serialized-coefficient room, but the
tight `427/1000` certificate is too close to the coefficient serialization
noise to be used as a theorem target unless exact coefficients are derived and
carried symbolically.

The theorem-shaped target is now more precise:

```text
prove a universal, pointwise, unnormalized lower bound
P_M(t) >= 21/50
```

for the actual coefficient family, or prove a Sturm variation-count theorem at
that margin from exact coefficient formulas.  This remains a finite serialized
margin-window diagnostic only.  No critical-margin theorem, robust-margin
universal theorem, coefficient-family theorem, universal Sturm certificate,
moment-square positivity theorem, uniform active/full lower-frame theorem,
Mobius covariance theorem, signed prime-correlation theorem, q286 theorem, or
Goldbach proof is established.

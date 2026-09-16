# Mobius moment-square robust Sturm chamber audit

## Question

After the margin-sensitivity audit, the tight `427/1000` margin is unsafe for
rounded provenance coefficients, while `21/50` survives both coefficient
sources.  At that robust margin, is there a stable Sturm certificate shape that
a theorem should preserve?

## Receipt

```text
tools/build_mobius_moment_square_robust_sturm_chamber_audit.py
evidence/mobius-moment-square-robust-sturm-chamber-audit.json
```

## Result

```text
status: TARGET_robust_sturm_variation_chamber
robust margin:                         21/50
source/provenance sign words match:    true
source variation certificates pass:    true
provenance variation certificates pass:true
distinct checked sign-word pairs:      4
```

At margin `21/50`, the source curve coefficients and serialized
coefficient-provenance coefficients agree on the Sturm sign words for each
checked scale.  The sign words are not globally identical across all checked
scales:

```text
M=127  +infty: +++--+--+  -infty: +-++---++
M=149  +infty: ++--+---+  -infty: +--+++-++
M=167  +infty: ++--++--+  -infty: +--++--++
M=191  +infty: ++---+--+  -infty: +--+---++
M=211  +infty: ++---+--+  -infty: +--+---++
M=227  +infty: ++---+--+  -infty: +--+---++
```

But each checked scale has

```text
V(-infty) = 4
V(+infty) = 4
```

and therefore zero real roots by Sturm variation counting.

## Decision

The robust theorem target should be variation-count preservation, not one
fixed Sturm sign word.  A candidate universal route is:

```text
derive exact coefficient formulas and prove that, at margin 21/50,
the Sturm sequence keeps equal variation counts at -infty and +infty.
```

This is finite Sturm-chamber diagnostic evidence only.  No robust Sturm
variation-chamber theorem, robust-margin universal theorem, coefficient-family
theorem, universal Sturm-certificate theorem, half-frame curve-positivity
theorem, uniform active/full lower-frame theorem, Mobius covariance theorem,
signed prime-correlation estimate, q286 theorem, strict-central Goldbach
theorem, or Goldbach proof is established.

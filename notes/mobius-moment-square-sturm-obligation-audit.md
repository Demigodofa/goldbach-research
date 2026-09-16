# Mobius moment-square Sturm obligation audit

## Question

The margin-window audit says the robust margin `21/50` has usable room, while
the tight `427/1000` margin is too close to serialized coefficient noise.  If
the robust route is to become theorem-shaped, what exact sign obligations does
the Sturm proof need?

## Receipt

```text
tools/build_mobius_moment_square_sturm_obligation_audit.py
evidence/mobius-moment-square-sturm-obligation-audit.json
```

## Method

For each checked scale and both serialized coefficient families, rationalize
the recorded decimal coefficients with `Rational(str(x))`, form
`P(t)-21/50`, compute SymPy's canonical Sturm sequence, and record the
leading-coefficient sign of every Sturm polynomial.  Those signs determine the
sign words at `+infinity` and `-infinity`; equal variation counts imply no real
roots.

This is a finite diagnostic of the serialized Sturm obligations.  It is not an
exact symbolic active/full Gram theorem.

## Result

```text
status: EXTRACT_robust_sturm_sign_obligations
robust margin:                              21/50
checked leading-coefficient obligations:    108
zero leading-coefficient obligations:       0
source/provenance sign words match:         true
source variation certificates pass:         true
provenance variation certificates pass:     true
distinct checked sign-word pairs:           4
```

The weakest checked nondegeneracy is the final degree-0 Sturm constant at
`M=167` in the coefficient-provenance serialization:

```text
coefficient family: coefficient_provenance_serialized
sequence index:     8
degree:             0
sign:               +
absolute value:     about 8.004e-19
```

## Decision

The robust certificate is not a single fixed sign word.  The checked scales
occupy four sign-word chambers, but in every chamber the variation counts at
the two infinities agree.

The theorem target becomes:

```text
derive exact coefficient formulas for the actual family and prove that the
canonical Sturm sequence for P_M(t)-21/50 keeps the required nonzero leading
coefficient signs, or at least equal variation counts, for every sufficiently
large admissible M.
```

The finite audit confirms that the current serialized data is not sitting on a
zero-leading-coefficient degeneracy, but it also shows where the proof is most
delicate: the terminal Sturm constant near `M=167`.  No Sturm-obligation
theorem, robust Sturm chamber theorem, robust-margin universal theorem,
coefficient-family theorem, universal Sturm certificate, moment-square
positivity theorem, uniform active/full lower-frame theorem, Mobius covariance
theorem, signed prime-correlation theorem, q286 theorem, or Goldbach proof is
established.

# q286-WBSS Marginal Cone Gap Audit

Status: finite LP cone falsifier and theorem-boundary evidence only.
Goldbach is not proved.

Receipt:

```text
tools/build_q286_wbss_marginal_cone_gap_audit.py
evidence/q286-wbss-marginal-cone-gap-audit.json
```

## Question

After the q286-WBSS signed-discrepancy problem was extracted, the live question
became whether this is a real narrowing or just a renamed copy of the same
Goldbach-strength hole.

This audit tests a concrete version of that concern:

Can lower-modulus AP-style marginal information force the signed expectation
`<mu_N,phi_a> > 0`, or can a synthetic reflected nonnegative measure keep the
same lower projections while making the signed expectation nonpositive?

## Method

Stress rows were selected before this LP from the prior signed-discrepancy
receipt: the union of the top `12` post-discovery rows by `lambda_phi` and the
top `6` by L1 worst-case load for each of the full and edge-beta coefficient
families.  This produced `24` targets.

For each row and coefficient family, the LP minimizes the signed expectation
over reflected nonnegative orbit measures with the same actual projections to
the following modulus families:

```text
support_reflection_only:                 []
prime_factor_marginals:                  [5, 7, 11, 13]
q286_joint_marginal:                     [286]
dominant_coefficient_support_marginals:  [70, 154, 286]
all_coefficient_support_marginals:       [10, 14, 22, 26, 70, 130, 154, 286]
```

A nonpositive LP optimum is a synthetic bad measure and falsifies that cone as
a proof bridge.

## Result

For both full and edge-beta coefficients:

```text
support/reflection only:          24/24 bad measures feasible
prime-factor marginals:           24/24 bad measures feasible
q286 joint marginal:              24/24 bad measures feasible
dominant support marginals:        3/24 bad measures feasible
all coefficient-support marginals: 0/24 bad measures feasible
```

The dominant-support cone nearly closes the hole, but it fails on three stress
rows:

```text
90644, 94856, 109178
```

The tightest row `94856` remains bad-feasible under the dominant supports,
with minimum signed expectation about `-0.047366411447256`.

The all-support cone forces positivity, but that is expected: these moduli are
exactly the lower supports to which the full coefficient descends.  It fixes
the coefficient expectation without proving why actual primes must satisfy a
usable theorem for those projections.

## Decision

This is not merely renaming, but it also does not close the hole.

What it kills:

- prime-factor AP marginals;
- q286-only marginals;
- support/reflection geometry;
- the idea that the top three natural supports `[70,154,286]` are sufficient
  without tail control.

What survives:

- a coefficient-support projection theorem for
  `[10,14,22,26,70,130,154,286]`;
- or a sharper theorem proving the three dominant supports plus an explicit
  signed tail lower bound.

## Tail-support follow-up

`tools/build_q286_wbss_tail_support_minimal_cone_audit.py` generated
`evidence/q286-wbss-tail-support-minimal-cone-audit.json`.

That follow-up shows the explicit signed tail lower bound can be narrowed, on
the same stress LP, to the single tail modulus `130`.  The four-modulus family
`[70,130,154,286]` forces positivity on all `24` stress rows for both full and
edge beta, with coefficient span residual below `1.3e-14`.

Thus the strongest current non-renaming projection target is not the full
all-support cone but this smaller four-modulus cone.  It still needs a real
binary-prime projection theorem before it becomes proof progress.

## Gap

The remaining implication is still arithmetic and external to the LP:

```text
actual strict-central binary-prime measures satisfy enough signed lower-modulus
projection control to keep <mu_N,phi_a> positive.
```

Without that source-backed binary-prime projection theorem, the all-support
cone is just a finite-dimensional restatement of the signed expectation.

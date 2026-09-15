# q286-WBSS Tail Support Minimal Cone Audit

Status: finite LP cone audit and coefficient-compression evidence only.
Goldbach is not proved.

Receipt:

```text
tools/build_q286_wbss_tail_support_minimal_cone_audit.py
evidence/q286-wbss-tail-support-minimal-cone-audit.json
```

## Question

The marginal-cone gap audit found that dominant coefficient-support marginals
`[70,154,286]` force positivity on `21/24` stress-selected rows, but fail on:

```text
90644, 94856, 109178
```

The question here is whether that crack requires all tail supports
`[10,14,22,26,130]`, or whether a smaller named tail projection closes it.

## Result

The smallest tail subset that forces positive signed expectation for both full
and edge-beta coefficient families on all `24` stress-selected rows is:

```text
[130]
```

Thus the finite LP closes with the four-modulus projection family:

```text
[70,130,154,286]
```

The maximum coefficient-projection span residual over the checked rows is at
floating precision:

```text
full coefficient:      1.2625229801710029e-14
edge beta coefficient: 7.69251740102256e-15
```

By tail-subset size:

```text
size 0: 0 closing subsets; best still has 3 bad rows
size 1: 1 closing subset;  [130]
size 2: 4 closing subsets; all include 130
size 3: 6 closing subsets; all include 130
size 4: 4 closing subsets; all include 130
size 5: 1 closing subset;  all tails
```

## Decision

This is a real narrowing relative to the previous answer.  The all-support
projection family is not needed on the stress gate.  The coefficient-complete
span appears already at:

```text
70, 130, 154, 286
```

So the next theorem-shaped problem is:

```text
prove strict-central binary-prime projection control for moduli
70, 130, 154, and 286 strong enough to preserve the positive q286-WBSS
expectation.
```

## Boundary

This still does not prove the required arithmetic estimate.  The LP says that
these four projections would be sufficient on the checked stress rows; it does
not prove actual primes obey an eventual projection theorem.  Goldbach remains
open.

The useful change is that the candidate bridge is no longer "all coefficient
supports" and no longer ordinary AP marginals.  It is a smaller four-modulus
projection problem.

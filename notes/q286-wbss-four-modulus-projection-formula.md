# q286-WBSS Four-Modulus Projection Formula

Status: finite formula extraction only. Goldbach is not proved.

Receipt:

```text
tools/build_q286_wbss_four_modulus_projection_formula.py
evidence/q286-wbss-four-modulus-projection-formula.json
```

## Question

The four-modulus span identity showed that the full q286-WBSS unit coefficient
descends to total mass plus projections modulo:

```text
70, 130, 154, 286
```

This receipt asks whether that algebraic compression can be written as an
explicit theorem-facing binary-prime projection formula, with a concrete error
budget for any future source-backed distribution estimate.

## Result

The normalized unit coefficient is reconstructed by:

```text
f(u) = alpha_0
     + sum_{d in {70,130,154,286}} sum_s alpha_{d,s} 1_{u == s mod d}
```

The LSQR reconstruction over all `2880` units modulo `10010` has relative
L2 residual:

```text
8.752538645134008e-16
```

and maximum absolute residual:

```text
2.1316282072803006e-14
```

For every even target residue modulo `10010`, averaging over the locally
admissible unit residues gives a positive local-uniform main term. The worst
row is target residue `4124`, with local-uniform main term:

```text
0.6039353780830684
```

The total nonconstant coefficient L1 norm is:

```text
372.962002076135
```

So the blunt sufficient projection-error budget is:

```text
0.0016192946592982506
```

Meaning: if every nonconstant projected residue probability error across the
four moduli were bounded in absolute value by that epsilon, the signed
expectation would stay positive for every even residue. This is only a
sufficient worst-case budget; the previous L1 audit already showed that blunt
absolute-error uniformity is usually far too pessimistic.

## Decision

This is a useful narrowing of the q286-WBSS proof obligation. The coefficient
side is now an explicit four-modulus projection formula rather than a
black-box unit vector on all `10010` residues.

The hole is still open. The next theorem has to prove one of:

```text
strict-central binary-prime projection control modulo 70, 130, 154, and 286
strong enough to beat the recorded coefficient budget;
```

or:

```text
a signed/correlation estimate for the same formula that avoids the pessimistic
absolute-error L1 budget.
```

No binary-prime projection theorem, signed discrepancy theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof is established.

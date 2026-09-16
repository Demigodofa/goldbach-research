# Mobius rank-aware lower-frame obligation

## Question

After the axial Schur-response shortcut failed, what is the exact theorem
shape left for the Mobius active/full lower-frame route?

The previous checkpoint showed that full-positive-definite whitening is too
strong and that axial compression is not a standalone certificate.  The
remaining statement has to compare the active and full quadratic forms on the
positive range of the full form, while treating full-null directions
separately.

## Receipt

```text
mobius_rank_aware_lower_frame.py
tools/build_mobius_rank_aware_lower_frame_obligation.py
evidence/mobius-rank-aware-lower-frame-obligation.json
```

## Rank-Aware Decomposition

For positive-semidefinite forms `A` and `F`, the target is not ordinary
full-Gram whitening when `F` is singular.  The finite quotient calculation is:

```text
1. diagonal-equilibrate F where its diagonal is positive;
2. split the space into positive eigenspace(F) plus nullspace(F);
3. measure the raw positive-range minimum;
4. Schur-minimize over harmless full-null coordinates;
5. check that active-null coupling is zero up to tolerance;
6. compare the resulting quotient minimum with 1/2.
```

This makes the theorem obligation explicit:

```text
eventual support activation of the full Gram
harmlessness/control of full-null directions
positive-range Schur-minimized quotient lower bound >= 1/2
```

## Checked Diagnostic

```text
M=83   rank=0  nullity=6  pre-support/vacuous
M=101  rank=0  nullity=6  pre-support/vacuous
M=127  rank=6  nullity=0  quotient_min=0.8768802946823542
M=149  rank=6  nullity=0  quotient_min=0.9344345921816697
M=167  rank=5  nullity=1  quotient_min=0.8511480691308368
M=191  rank=6  nullity=0  quotient_min=0.9726898127803637
```

The rank-deficient nonvacuous scale is `M=167`.  Its quotient minimum remains
above `1/2`, so it is not a lower-frame falsifier.  But the stricter numerical
certificate flags a null-coupling term about `3.45e-08`, so `M=167` becomes the
exact scale requiring proof-level nullspace/coupling control.  It is also a
falsifier of the stronger full-positive-definite whitening formulation.

## Decision

The active target is now:

```text
TARGET_rank_aware_positive_range_lower_frame_plus_support_activation
```

The next mathematical proof must supply support activation, full-null
harmlessness, and a positive-range quotient lower bound.  This checkpoint is
finite diagnostic evidence only.  No uniform active/full lower-frame theorem,
Mobius covariance theorem, signed prime-correlation estimate, q286 theorem,
strict-central Goldbach theorem, or Goldbach proof is established.

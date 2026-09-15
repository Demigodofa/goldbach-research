# q286 principal-rescue obstruction audit

Status: finite obstruction audit.  This is not a threshold theorem, signed
correlation theorem, pointwise character-sum theorem, or Goldbach proof.

Receipt:

```text
tools/build_q286_principal_rescue_obstruction_audit.py
evidence/q286-principal-rescue-obstruction-audit.json
```

## Question

The later-tail decomposition showed principal baseline alone keeps the later
`73` tail rows positive.  This receipt asks whether the checked q286 failures
are caused by `first_three < -1`, by nonprincipal drag overturning a positive
principal-only margin, or by both.

## Mechanism

Rerun the validated prime-indexed row verifier over checked blocks `0..11`.
For every first-three-tail row compute:

```text
principal_only_margin = 1 + first_three_modes_to_principal_ratio
nonprincipal_correction = complement_to_principal_ratio - 1
full = principal_only_margin + nonprincipal_correction
```

Then classify every tail row as principal-only positive, first-three below
`-1`, nonprincipal-rescued, or nonprincipal-drag-overturned.

## Result

The receipt scanned `480480` targets across checked blocks `0..11` and stored
all `6150` first-three-tail rows.  Source-count validation matched the prior
margin schedule and later full-block receipts.

The discovery block still contains all `86` full-nonpositive tail rows.  Only
`5` tail rows have `first_three < -1`, while `84` of the `86`
full-nonpositive rows have positive principal-only margin and are broken by
nonprincipal drag.  Therefore the discovery-block obstruction is not explained
by `first_three < -1` alone.

Post-discovery blocks `1..11` contain `1744` tail rows, with `0`
full-nonpositive rows and `0` first-three-below-`-1` rows.  The minimum
post-discovery principal-only margin is `0.28517743655685746`; the minimum
later-block principal-only margin is `0.5574443165171574`.  Maximum full
rebuild error is `2.220446049250313e-16`.

Decision: the checked post-discovery/later hole continues to close in this
finite schedule, but the proof shape is now two-part: prove post-discovery
`first_three > -1` and separately bound nonprincipal drag below the remaining
principal-only surplus.  This receipt falsifies the stronger claim that all
checked failures are caused only by `first_three < -1`.

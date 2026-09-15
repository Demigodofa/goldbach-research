# q286 nonprincipal-drag envelope audit

Status: finite checked-block diagnostic.  This is not a threshold theorem,
signed correlation theorem, pointwise character-sum theorem, or Goldbach
proof.

Receipt:

```text
tools/build_q286_nonprincipal_drag_envelope_audit.py
evidence/q286-nonprincipal-drag-envelope-audit.json
```

## Question

The principal-rescue obstruction audit showed that post-discovery q286 tail
rows stay positive, but that many discovery failures are principal-positive
rows overturned by nonprincipal drag.  This receipt asks whether the checked
post-discovery suffix satisfies the sharper finite envelope:

```text
nonprincipal_drag < principal_only_margin
```

where:

```text
principal_only_margin = 1 + first_three_modes_to_principal_ratio
nonprincipal_drag = max(0, 1 - complement_to_principal_ratio)
```

## Falsifier

Any post-discovery first-three-tail row with
`nonprincipal_drag / principal_only_margin >= 1` falsifies the checked suffix
envelope.

## Result

The receipt scanned the same `480480` targets and validated against the
principal-rescue obstruction audit: all checked source counts match.

Post-discovery blocks `1..11` contain `1744` first-three-tail rows and `0`
drag-overturn rows.  The maximum checked post-discovery ratio is
`0.9696841556062236`, leaving a gap below `1` of only
`0.030315844393776437`.  The tightest row is target `94856`, with
principal-only margin `0.4148479630137373`, nonprincipal drag
`0.40227149671993767`, and final drag-surplus margin
`0.012576466293799604`.

Later blocks `6..11` are much safer: the maximum drag-to-margin ratio is
`0.47454631067294206`.

Discovery block `0` contains `84` drag-overturn rows, matching the previous
obstruction audit's principal-positive full failures.  The worst ratio is
`27.66930751295942` at target `14996`, where the principal-only margin is only
`0.007630578562948465` and nonprincipal drag is `0.21113282476001705`.

Decision: the checked suffix theorem target can be sharpened to
`first_three > -1` plus `nonprincipal_drag / principal_only_margin < 1`, but
the early post-discovery margin is near-sharp.  A loose mean or absolute drag
bound will not close the proof; the needed estimate must control worst-case
signed drag relative to the available principal-only surplus.

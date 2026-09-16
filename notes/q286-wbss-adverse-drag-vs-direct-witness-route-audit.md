# q286-WBSS adverse-drag versus direct-witness route audit

## Question

The current q286-WBSS acceptance target is universal, pointwise, and
unnormalized:

```text
adverse_drag(N) < local_main(N)
```

This is sufficient for the direct signed witness `B_Phi(N)>0`, but it is
stricter because it discards all helpful projected terms.  Does this route
still look like a theorem target that earns its keep, or is it probably too
strong compared with proving the direct signed witness?

## Receipt

```text
tools/build_q286_wbss_adverse_drag_vs_direct_witness_route_audit.py
evidence/q286-wbss-adverse-drag-vs-direct-witness-route-audit.json
```

## Logical Status

The implication is one-way:

```text
A_-(N) < M(N)
  => M(N) + sum_d E_d(N) >= M(N) - A_-(N) > 0.
```

So adverse-drag positivity proves the q286-WBSS signed witness for that
target.  The converse is false as algebra: direct positivity can be saved by
helpful projected terms, while adverse-drag deliberately refuses to count
them.

## Finite Route Cost

On the current `348`-row calibration set:

```text
direct witness positive rows:                 348 / 348
adverse-only witness positive rows:            348 / 348
rows needing positive help for positivity:       0 / 348

adverse-only witness range:
  0.5992601478393073 .. 1.090868544326864

adverse-only fraction of direct witness:
  0.7368071926156354 .. 1.0000000000000004
  mean 0.9335996319912551

positive-help fraction of direct witness:
  -3.642342207889426e-16 .. 0.2631928073843646
  mean 0.06640036800874495
```

The largest route cost occurs at target `1098236`: the adverse-only witness is
about `73.68%` of the direct witness, so helpful projected terms account for
about `26.32%` of direct positivity there.

## Decision

`HOLD_adverse_drag_is_valid_stricter_route_not_theorem`.

The adverse-drag route earns its keep as a lead sufficient target in the
checked calibration set: no checked row requires positive projected help merely
to stay positive.  But it is not equivalent to the direct witness, and proving
it may be harder than proving `B_Phi(N)>0` with signed cancellation.

Next theorem work should prefer adverse-drag only if it can be tied to
source-backed one-sided binary-prime projection control.  Otherwise, the
direct signed witness remains the cleaner theorem object.

## Boundary

Finite route-comparison audit only.  This proves no pointwise adverse-drag
theorem, direct signed-witness theorem, fixed-modulus binary-prime correlation
theorem, q286 threshold theorem, strict-central Goldbach theorem, or Goldbach
proof.

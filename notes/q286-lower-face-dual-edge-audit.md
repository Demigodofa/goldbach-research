# q286 lower-face dual-edge audit

Status: finite dual-edge diagnostic and `new-to-this-task` aha-candidate.
This is not a dual-edge theorem, signed prime-correlation estimate, q286
threshold theorem, strict-central Goldbach theorem, or Goldbach proof.

Receipt:

```text
tools/build_q286_lower_face_dual_edge_audit.py
evidence/q286-lower-face-dual-edge-audit.json
```

## Question

The lower-face support audit showed that the bad support is not a fixed
residue dictionary.  The next step is to remove the remaining LP opacity:

```text
Can each bad optimizer be restated as an affine lower edge in the
(F3, Full) coefficient plane?
```

If yes, the complement rescue inequality becomes a single edge-gap statement.

## Result

For the `196` checked post-discovery rows:

```text
edge formula error:                 0.0..8.881784197001252e-16
minimum gap over all coefficient orbits:
                                    -5.329070518200751e-15..4.440892098500626e-16
actual edge gap:                    3.131031037561594..7.8631684141402225
required edge gap for positivity:   2.5357299258914665..7.283885499227512
edge-gap rescue ratio:              1.0021652272515458..1.3070973629998075
edge-gap margin after rescue:       0.01257646629380016..1.0551822046747485
dual slope:                         0.45308219617844336..1.2458803473056286
```

The tightest checked post-discovery row is `94856`:

```text
actual Full:                        0.012576466293799767
lower edge value at actual F3:      -5.808381676713722
actual edge gap:                    5.820958143007522
required edge gap for positivity:   5.808381676713722
edge-gap rescue ratio:              1.0021652272515458
```

## Interpretation

The lower-face bridge now has a clean dual form.  For the affine edge

```text
ell_a,t(x) = slope_a,t * F3(x) + intercept_a,t
```

define the nonnegative orbit gap

```text
g_a,t(x) = Full(x) - ell_a,t(x).
```

The LP certificate says `g_a,t(x) >= 0` for every reflection orbit, with zero
on the lower-face support.  For the actual measure:

```text
Full(mu_N) = ell_a,t(F3(mu_N)) + E_mu_N[g_a,t].
```

So the exact complement rescue inequality is:

```text
E_mu_N[g_a,t] > -ell_a,t(F3(mu_N)).
```

The checked rows all satisfy this, but the weakest row is close:
the ratio is only `1.0021652272515458`.  This explains why the loop feels like
it is tightening without closing: the right theorem is now very narrow, and a
loose AP or uniformity estimate will almost certainly be too weak.

## Candidate theorem refinement

For every even `N` in a proved q286 tail class, with
`a=N mod 10010` and `t=F3(mu_N)`, prove:

```text
sum_orbits mu_N(orbit) * g_a,t(orbit)
  >= (1 + eta_a(N)) * max(0, -ell_a,t(t)).
```

with `eta_a(N)>0`.  In unnormalized form:

```text
sum_orbits W_N(orbit) * g_a,t(orbit)
  > -T_N * ell_a,t(t).
```

This is still downstream of `T_N` unless paired with an independent lower
bound or restated as a direct positive signed prime-pair sum.  The audit
therefore sharpens the bridge gap; it does not close it.

## Falsifier

Freeze the edge-gap formula before testing fresh windows.  The candidate is
falsified if a held-out post-boundary row has:

- invalid lower-edge gaps beyond numerical tolerance;
- edge-gap rescue ratio `<= 1`;
- a much smaller positive non-support gap that makes the edge unstable under
  exact arithmetic; or
- an actual mass distribution concentrated on the zero-gap lower face.


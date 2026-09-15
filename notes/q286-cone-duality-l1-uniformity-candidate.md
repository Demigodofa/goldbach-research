# q286 cone-duality L1-uniformity candidate

Status: finite cone-definition and LP diagnostic.  This is not an
AP-uniformity theorem, signed prime-correlation theorem, q286 threshold
theorem, or Goldbach proof.

## Candidate

The first executable cone from `notes/q286-cone-duality-proof-route.md` is:

```text
K_a(rho) =
  nonnegative probability measures on admissible units modulo 10010,
  symmetric under r -> a-r,
  with L1 distance <= rho from the local uniform admissible measure.
```

For each selected target residue `a`, the LP minimizes that L1 distance while
forcing the bad branch:

```text
F3(mu) <= -0.3
full_action(mu) <= 0.
```

Because `full_action = F3 + C`, the second inequality is the linear form of
failed complement rescue on a first-three tail.

## Evidence

Executable receipt:

```text
tools/build_q286_cone_duality_l1_uniformity_candidate.py
evidence/q286-cone-duality-l1-uniformity-candidate.json
```

The script reconstructs `F3` and `full_action` as fixed affine functionals on
the normalized strict-central residue measure modulo `10010`, then solves the
nearest-bad LP on seven selected target residues:

```text
14138, 14996, 94856, 1222142, 1240888, 1242118, 1379072
```

Reconstruction against the existing optimized row verifier is at floating
precision:

```text
maximum reconstruction error: 5.273559366969494e-16
```

All seven selected residues admit a synthetic reflected admissible bad measure.
The nearest-bad L1 distances from uniform are:

```text
minimum: 0.05724560696825869
mean:    0.09720394355055242
maximum: 0.11764562474360012
```

Equivalently, the total-variation radii are about:

```text
0.028622803484129346 .. 0.05882281237180006
```

The actual selected rows are much farther from uniform:

```text
actual L1 minimum: 0.47982423933735313
actual L1 mean:    1.0412615462552854
actual L1 maximum: 1.8989898989898988
```

No actual selected target passes the L1-uniformity certificate.  The clear
near-boundary rows are representative:

```text
1222142 actual L1 / nearest-bad L1: 4.3100534420996075
1240888 actual L1 / nearest-bad L1: 4.343379940177118
1242118 actual L1 / nearest-bad L1: 6.693235458821063
1379072 actual L1 / nearest-bad L1: 4.6865021954109425
```

## Decision

The L1-uniformity cone is a valid sufficient theorem shape:

```text
||mu_N - uniform||_1 < minimum_bad_l1(a)
  => the q286 bad branch is impossible for residue a.
```

But it is too strong to be the main proof mechanism for the observed q286
rows.  Actual clear rows fail the sufficient L1 budgets by factors of roughly
`4.3` to `6.7`, yet still clear by signed complement structure.  The route
therefore pivots again inside cone-duality: keep LP/Farkas as the certificate
language, but replace the blunt L1 ball with a coefficient-sensitive arithmetic
cone.

## Next candidate

The next cone should use one of:

- signed character moment bounds for the finite support families;
- q286 mass/landing inequalities on reflection-orbit sign classes;
- binary Goldbach-in-progressions bounds only if they control the specific
  signed functionals, not merely raw residue counts;
- a PSD/covariance constraint tied to the actual strict-central prime-pair
  measure.

Do not retry a larger L1-uniformity scan unless an external AP theorem supplies
a concrete bound in this radius range.


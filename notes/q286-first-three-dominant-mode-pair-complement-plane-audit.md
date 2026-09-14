# q286 Dominant-Mode Pair/Complement Plane Audit

Status: finite pair/complement plane diagnostic only.  This records a narrow
local locator around the q286 stress row; it is not a stable selector theorem,
adverse-pair theorem, pointwise character-sum estimate, or Goldbach proof.

## Mechanism

The adverse-pair sign shortcut failed because the named stress pair
`(1,7),(4,4)` also has positive sum on nearby clear rows.  This receipt keeps
the same top-`20` near-boundary ledger but treats each row as a point in the
two-coordinate plane:

```text
(1,7),(4,4) pair sum     versus     six-channel repair-complement sum
```

It checks scalar neighborhoods centered at the stress row `1222142`,
stress-centered pair/complement rectangles, and the natural rectangle spanned
by the two tightest rows, `1222142` and clear row `1242118`.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_pair_complement_plane_audit.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-pair-complement-plane-audit.json`
- Source:
  `evidence/q286-first-three-dominant-mode-adverse-pair-near-boundary-falsifier.json`

## Results

The top-`20` closest near-boundary rows still contain one dominant-floor
deficit, `1222142`, and nineteen clears.  In the coupled plane, square boxes
centered on `1222142` with pair/complement epsilons `.005`, `.01`, and `.02`
select only the finite stress deficit on the checked set.

The first checked square false positive appears at `.03` by `.03`:

```text
1222142   deficit
1242118   clear
1222048   clear
1242136   clear
```

The natural rectangle spanned by the two tightest rows already contains both
`1222142` and the closest clear, `1242118`, even with zero padding:

```text
1222142   deficit   pair 0.0216228924   complement -0.0870297837
1242118   clear     pair 0.0287525311   complement -0.1086215180
```

The complement coordinate is the strongest single local scalar in this
top-`20` finite check: a complement-sum neighborhood around `1222142` remains
isolated through epsilon `.02`, then admits four clear rows at `.03`.

## Interpretation

The loop is tightening locally.  Pair-plus-complement geometry sees the stress
row better than pair sign alone, but the theorem has not fallen out of the
plane.  A proof route would still need an arithmetic reason why the allowed
pair/complement band is legitimate uniformly, or a stronger signed aggregate
estimate from actual binary-prime residue weights.

# q286 dominant-mode character-sum obligation

Status: theorem-obligation refinement.  Goldbach is not proved.

The dominant `mode_1 + mode_2` residual survived the support/reflection
obstruction.  This note rewrites that residual as an exact fixed-modulus
character-sum problem.

For q286 strict-central binary-prime residue weights, let `S_chi(N)` be the
centered weighted character sum of the actual prime-pair residue distribution
against a product character `chi` modulo `286`.  The dominant two-mode
projection has the form:

```text
mode_1(N) + mode_2(N) = Re sum_chi c_chi S_chi(N) / P_N.
```

Complex conjugacy reduces the active channels to real formulas of the form:

```text
2*Re(c*S_chi)
```

There are no self-conjugate active channels in the dominant two-mode sum.

## Channel Count

Receipt:
`evidence/q286-first-three-dominant-mode-character-sum-obligation.json`

The dominant two-mode sum uses:

- `50` active complex q286 character products,
- `25` real conjugacy channels,
- `0` active self-conjugate channels.

The dominant real-channel `L1` coefficient size is about
`32.215594107770805` relative to the principal mean.  This is narrower than
the full `99`-character product space, but it is not a tiny single-character
proof route.

The companion norm-budget note
`q286-first-three-dominant-mode-channel-norm-budget.md` shows that plain
independent `Linf`/`L2` smallness of these channels is sufficient but too
blunt on the current near-boundary samples.  The surviving theorem should use
signed channel structure, not only channel size.

The next signed-structure layer is recorded in
`q286-first-three-dominant-mode-signed-channel-profile.md`, which splits the
dominant channel sum into positive offset and negative pressure.

## Sample Reconstruction

The receipt reconstructs the prior residue-obligation dominant-mode ratios on
the near-boundary samples:

| target | dominant character sum/P | slack to `-.3` | top negative real channel |
| --- | ---: | ---: | --- |
| `1222142` | `-0.3088331795605278` | `-0.008833179560527815` | `(5,5)` |
| `1242118` | `-0.2834710865332539` | `0.016528913466746065` | `(5,1)` |
| `1240888` | `-0.27281342661908214` | `0.027186573380917844` | `(1,7)` |

The maximum complex-character identity error is `0` on the checked rows, and
the maximum real-channel identity error is below `1e-9` in the focused
regression.

## Remaining Theorem

After this split, the dominant-mode lower bound is no longer a generic
geometric statement.  It asks for pointwise arithmetic control of these `25`
real channels, or for a theorem showing that complement/lower-support terms
rescue the rows when the dominant channel sum is too negative.

This is still not a proof of the q286 first-three theorem, and not a proof of
Goldbach.  It states the next analytic object: fixed-modulus signed
binary-prime character sums for the actual strict-central prime-pair weights.

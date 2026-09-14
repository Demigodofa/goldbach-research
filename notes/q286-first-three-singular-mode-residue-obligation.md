# q286 first-three singular-mode residue obligation

Status: theorem-obligation refinement.  Goldbach is not proved.

This note is the next residual layer below the q286 residue-pair correlation
obligation.  The residue-pair identity already bolts the first-three signed
projection to actual strict-central binary-prime residue weights.  This split
keeps the same frame and asks what remains after the first-three coefficient is
expanded into its first three singular character modes.

For target residue `a=N mod 286`, admissible residue set
`A_a={u in U_286 : a-u in U_286}`, strict-central binary-prime residue weights
`W_N(u)`, total weight `T_N=sum_u W_N(u)`, and centered mode coefficient
`gamma_{a,j}(u)`, the exact mode identity is:

```text
mode_j(N) =
sum_{u in A_a} (W_N(u)-T_N/|A_a|) * gamma_{a,j}(u) / T_N.
```

The executable receipt verifies this identity against the prior q286
character-mode coordinate receipt.  The largest mode identity and recombined
identity errors are below `1e-9` in the focused regression.

## Sample facts

Receipt: `evidence/q286-first-three-singular-mode-residue-obligation.json`

On samples `1222142`, `1242118`, and `1240888`, modes `1` and `2` are
same-sign negative on all three rows.  Their combined pressure is:

| target | full first-three/P | mode 1+2/P | slack to `-.3` |
| --- | ---: | ---: | ---: |
| `1222142` | `-0.3075877603708801` | `-0.3088331795605278` | `-0.008833179560527815` |
| `1242118` | `-0.2864267432684323` | `-0.2834710865332539` | `0.016528913466746065` |
| `1240888` | `-0.27468410150061706` | `-0.27281342661908214` | `0.027186573380917844` |

Thus the dominant two-mode residual already separates the tail row from the
two near-clear rows in this holdout sample.  The third mode is small at this
scale and shifts rows slightly, but it is not the observed rescue mechanism.

## Residual theorem

The sharper remaining q286 first-three theorem can now be stated as a
two-mode residue-discrepancy problem:

```text
mode_1(N)+mode_2(N) >= -0.3 - allowed_remaining_terms(N)
```

where the allowed remaining terms must be supplied by the third singular mode,
the complement/lower-support lanes, or an external fixed-modulus
binary-prime-in-progressions estimate.

Equivalently, prove a pointwise lower bound for the combined centered
residue-discrepancy projection:

```text
sum_{j in {1,2}} sum_{u in A_a}
  (W_N(u)-T_N/|A_a|) * gamma_{a,j}(u) / T_N
```

or classify the finite/residue conditions under which simultaneous strong
negativity in these two singular coordinates is impossible for actual
prime-pair weights.

The support/reflection-only version of this theorem is already obstructed.
`notes/q286-first-three-dominant-mode-reflection-support-obstruction.md`
constructs positive nonnegative reflected synthetic support weights with
`mode_1+mode_2 < -0.3` for every even target residue modulo `286`.  Therefore
any successful proof of the dominant two-mode lower bound must use actual
prime-pair arithmetic or a stronger residue-weight constraint than support,
total mass, nonnegativity, and ordered-pair reflection symmetry.

The exact arithmetic form is now recorded in
`notes/q286-first-three-dominant-mode-character-sum-obligation.md`: the
dominant two-mode projection uses `50` active complex q286 character products,
or `25` real conjugacy channels after pairing complex conjugates.  This is the
current analytic target beneath the residue-discrepancy identity.

## Boundary

This is not a proof of the q286 first-three theorem.  It proves only exact
finite algebraic identities and a better statement of the missing arithmetic
input.  A future proof still needs pointwise signed prime-correlation control,
conditioned complement/lower-support rescue, endpoint and noncentral terms,
finite boundary work, and the full outer Goldbach assembly.

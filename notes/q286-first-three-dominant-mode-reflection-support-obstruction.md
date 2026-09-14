# q286 dominant-mode reflection-support obstruction

Status: finite-vector obstruction.  Goldbach is not proved.

This closes one tempting shortcut under the singular-mode residual.  After the
q286 first-three coefficient is split into singular modes, the immediate
residual theorem asks for control of the dominant `mode_1 + mode_2` projection.
This note checks whether that bound could follow from only:

- admissible q286 support,
- nonnegative weights,
- total mass normalization, and
- ordered prime-pair reflection symmetry `w(u)=w(N-u)`.

It cannot.

## Result

Receipt:
`evidence/q286-first-three-dominant-mode-reflection-support-obstruction.json`

For every even target residue modulo `286`, the executable receipt minimizes
the centered `mode_1 + mode_2` coefficient over reflection orbits and then
mixes the worst orbit with the local uniform admissible distribution to keep a
strictly positive reflected synthetic weight vector.

All `143` even target residues have positive reflected synthetic witnesses
with:

```text
mode_1(N) + mode_2(N) < -0.3.
```

The worst extremal reflected orbit occurs at target residue `46`, with
dominant-mode ratio about `-6.79376971010447`.  The least-negative extremal
row is still target residue `276`, with dominant-mode ratio about
`-2.5799705631335383`.

Thus support, nonnegativity, total mass, and pair-reflection symmetry alone do
not prove the dominant two-mode lower bound.

## What Remains

The next non-circular theorem must use at least one ingredient absent from the
synthetic obstruction:

- actual binary prime-pair distribution,
- a stronger residue-weight structural constraint,
- a pointwise fixed-modulus character-sum estimate,
- complement/lower-support rescue, or
- a finite-boundary plus asymptotic assembly strong enough to replace the
  dominant-mode bound.

This result does not refute arithmetic q286 rarity and does not refute every
possible geometric proof.  It refutes only the support/nonnegativity/total/
reflection-only dominant-mode claim.

# q286-WBSS K286 two-mode reflection/parity audit

## Question

Does ordered-pair reflection remove a universal part of the exact `K_286`
two-mode singular burden?

## Mechanism

For each even target residue `a mod 286`, strict-central ordered prime pairs
have the reflection map

```text
r -> a-r mod 286.
```

For a residue coefficient `phi`, center it on the admissible units for `a`:

```text
gamma_a(r) = phi(r) - mean_admissible(phi).
```

Then split

```text
gamma_even(r) = (gamma_a(r) + gamma_a(a-r)) / 2
gamma_odd(r)  = (gamma_a(r) - gamma_a(a-r)) / 2
```

The odd part is algebraically invisible to any reflection-symmetric residue
mass.  This is real structure, but it is only an algebraic coefficient
identity; it is not a binary-prime distribution theorem.

## Receipt

```text
tools/build_q286_wbss_k286_two_mode_reflection_parity_audit.py
evidence/q286-wbss-k286-two-mode-reflection-parity-audit.json
```

## Result

For the combined scaled first two singular modes
`sigma_1*u_1*vh_1 + sigma_2*u_2*vh_2`:

```text
target residues checked:          143
even energy fraction minimum:     0.399466343237569
even energy fraction mean:        0.50010368361382
even energy fraction maximum:     1.0
odd energy fraction maximum:      0.600533656762431
worst even target residue:        0 mod 286
best odd target residue:          110 mod 286
max reconstruction error:         3.552713678800501e-15
max odd pair-sum error:           0.0
max even pair-difference error:   0.0
```

Mode-specific summaries:

```text
mode 1 even energy fraction: min 0.22442739917640642,
                             mean 0.4999397483825339,
                             max 0.9999999999999999
mode 1 odd energy fraction:  max 0.7755726008235937

mode 2 even energy fraction: min 0.31661956590224133,
                             mean 0.4999108618662231,
                             max 1.0
mode 2 odd energy fraction:  max 0.6833804340977587
```

## Decision

`AUDIT_k286_two_mode_reflection_parity_not_proof`.

The reflection-odd null identity is useful structure.  It can reduce the
effective coefficient burden for many nonzero target residues and may help a
target-residue-specific analytic estimate.

It does not solve the universal pointwise target.  Target residue `0 mod 286`
keeps essentially the entire combined two-mode coefficient in the
reflection-even subspace.  Therefore reflection alone cannot prove the desired
universal estimate.

The next acceptable route is a genuinely pointwise, unnormalized analytic
estimate, such as a theorem proving

```text
adverse_drag_raw(N) < local_main_raw(N)
```

for every sufficiently large covered even `N`, or an equivalent
binary-prime moment theorem with a non-circular bridge.

No zero-mass check is promoted to a logical bridge.  No non-circular `L2`
target is confirmed.  No binary-prime moment theorem, raw adverse-drag bound,
q286 threshold theorem, strict-central Goldbach theorem, or Goldbach proof is
established.

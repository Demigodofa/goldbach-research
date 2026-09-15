# q286-WBSS Mod-286 Fourier Interaction Audit

Status: finite Fourier interaction diagnostic. Goldbach is not proved.

Receipt:

```text
tools/build_q286_wbss_mod286_fourier_interaction_audit.py
evidence/q286-wbss-mod286-fourier-interaction-audit.json
```

## Question

The mod-286 interaction audit showed that the recurring negative signed drag
is not a one-factor modulo `11` or modulo `13` marginal. This audit asks the
next theorem-facing question: after primitive-root coordinates identify
`(Z/11Z)^* x (Z/13Z)^*` with `C10 x C12`, is the interaction carried by a tiny
set of multiplicative character modes?

## Result

The coefficient side confirms a pure two-factor interaction, but not a tiny
one:

```text
residue count:                         120
nonzero conjugacy groups:              25
zero Fourier-axis energy share:        3.243981252694915e-33
top 1 conjugacy group energy share:    0.06226340943530814
top 8 conjugacy groups energy share:   0.41552805891437444
top 10 conjugacy groups energy share:  0.5079835773727566
top 20 conjugacy groups energy share:  0.8702131544344734
top 25 conjugacy groups energy share:  1.0000000000000002
```

Replaying the same `196` post-discovery actual projection-error rows gives a
mixed outcome:

```text
top 8 groups negative contribution count:       189 / 196
top 8 contribution range:                       -0.4417578167298069..0.05669988379087601
top 10 groups negative contribution count:      196 / 196
top 10 contribution / total ratio range:        0.009071759166255295..1.0393932987832106
top 20 groups negative contribution count:      196 / 196
top 20 contribution / total ratio range:        0.5030209754400546..1.1437286994687021
```

So the first sign-stable truncation uses `10` conjugacy groups, but it is too
weak to be a standalone explanation: on the weakest row it carries only about
`0.9%` of the full interaction drag. The first tested truncation carrying at
least half the drag on every row uses `20` conjugacy groups.

## Decision

Demote the tiny-character shortcut. The useful surviving object is a
band-limited signed interaction inequality plus a residual bound:

```text
top 20 conjugacy groups supply a sign-stable main drag,
and the remaining five conjugacy groups must be bounded as residual drag.
```

This is sharper than "control all mod-286 cells" and broader than "one or two
characters explain the drag." It names a realistic intermediate theorem
target, but that target is still an unproved fixed-modulus binary-prime
correlation statement.

## Boundary

This audit proves no multiplicative-character theorem, no signed projection
theorem, no q286 threshold theorem, no strict-central Goldbach theorem, and no
Goldbach proof. It only classifies the finite Fourier structure of the
already isolated mod-286 interaction.

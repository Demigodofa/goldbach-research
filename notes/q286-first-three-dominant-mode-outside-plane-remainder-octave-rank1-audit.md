# q286 outside-plane remainder Octave rank-1 audit

Date: 2026-09-14

Status: finite Octave rank-`1` outside-remainder audit only.  This is not a
rank-`1` theorem, residual-bound theorem, signed projection theorem, or
Goldbach proof.

The previous separator receipt showed that stress row `1222142` is the unique
minimum outside-pair/complement remainder row on the predeclared `72`-row
denominator.  This receipt asks whether the `71` clear-minus-stress outside
channel vectors have a low-dimensional Octave handle.

The evidence is:

```text
tools/build_q286_first_three_dominant_mode_outside_plane_remainder_octave_rank1_audit.py
evidence/q286-first-three-dominant-mode-outside-plane-remainder-octave-rank1-audit.json
```

The builder recomputes the exact q286 signed channel profiles for the `72`
holdout rows, removes the eight volatile pair/complement channels, subtracts
the stress row from each clear row on the remaining `17` outside channels, and
uses Octave `11.3.0` to SVD the resulting `71 by 17` matrix.

Octave rank `1` is already all-positive on the reconstructed outside-delta row
sums.  The first singular mode carries about `0.7471393937` of the matrix
energy.  Its minimum reconstructed outside delta is about `0.1016883950` at
clear row `1240160`.

The exact outside-remainder minimum is still different: clear row `1242118`
has exact outside delta about `0.0398241886`.  Rank `1` therefore gives a
finite compression handle, not an exact ordering theorem.  The rank-`1`
reconstruction overshoots the exact outside delta on `36` of the `71` clear
rows, and the residual row-sum ranges from about `-0.1146136245` to
`0.1032801744`.

So the loop tightened again, but into a two-part theorem obligation:

```text
positive rank-1 outside direction
- bounded residual row-sum drag
```

The next useful proof target is to identify the arithmetic meaning of the
rank-`1` outside direction and prove that the remaining outside-channel
residual cannot undo the positive rank-`1` margin under the relevant
pair/complement placement conditions.

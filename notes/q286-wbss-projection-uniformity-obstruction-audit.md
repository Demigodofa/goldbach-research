# q286-WBSS Projection-Uniformity Obstruction Audit

Status: finite obstruction to one proof bridge. Goldbach is not proved.

Receipt:

```text
tools/build_q286_wbss_projection_uniformity_obstruction_audit.py
evidence/q286-wbss-projection-uniformity-obstruction-audit.json
```

## Question

The four-modulus projection formula gave a blunt sufficient condition:

```text
max projected residue probability error modulo 70, 130, 154, and 286
  <= 0.0016192946592982506
```

would force positivity of the q286-WBSS signed expectation for every even
target residue. This audit asks whether the actual checked successful
strict-central rows are even close to satisfying that projected
L-infinity-uniformity condition.

## Result

On the `196` post-discovery q286-WBSS rows:

```text
actual signed expectations positive:          196 / 196
rows inside blunt projection-error budget:      0 / 196
maximum projected cell error range:             0.0054355245292371495..0.03166078595284763
mean maximum projected cell error:              0.011916198098095038
error-to-budget ratio range:                    3.356723557399196..19.552207975890227
projection formula replay max abs error:        4.440892098500626e-16
```

The worst row is target `93932`, where the largest projected cell error is
`0.03166078595284763`, about `19.55` times the sufficient budget.

## Decision

Demote the blunt four-modulus projected L-infinity uniformity bridge. The
actual successful rows are too far from projected local uniform for a proof
based on a common absolute cell-error budget to explain the phenomenon.

This does **not** falsify the four-modulus formula. The formula still
reconstructs the signed witness at floating precision and remains useful
because it names the exact projected quantities. The next theorem must be
coefficient-sensitive:

```text
control the signed weighted projection error for the four-modulus formula,
or prove the raw q286-WBSS signed witness B_Phi(N)>0 directly.
```

## Boundary

This audit proves no binary-prime projection theorem, no signed discrepancy
theorem, no q286 threshold theorem, no strict-central Goldbach theorem, and no
Goldbach proof. It only blocks one too-strong uniform projection route.

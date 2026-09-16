# Mobius moment-square degree-5 Q46189 50A..60A distance profile audit

## Question

Inside the `50A..60A` signed-balance witness, does the replacement
advantage live at exact circular distances, or does it require short
aggregate distance blocks?

## Receipt

```text
tools/build_mobius_moment_square_degree5_q46189_50a60a_distance_profile_audit.py
evidence/mobius-moment-square-degree5-q46189-50a60a-distance-profile-audit.json
```

## Result

```text
distance range:                         [2151, 2580]
exact distances checked:                430
pointwise positive gaps:                83
pointwise nonpositive gaps:             347
Q 50A..60A total / diag:                -0.08597078804878477
componentwise min-replacement envelope: -0.5389671631863593
componentwise envelope gap:             -0.4529963751375745
micro-slices separating by both:        56A_to_57A, 57A_to_58A
minimal separating micro-slices:        56A_to_57A, 57A_to_58A
2A witness:                             56A_to_58A [2409, 2494]
2A Q positive share:                    0.26392574746028347
2A min replacement positive share:      0.3055515148922263
2A positive-share gap:                  0.04162576743194285
2A Q total / diag:                      -0.057125505502661246
2A min replacement total / diag:        -0.023310151551005336
2A total gap:                           0.03381535395165591
```

## Decision

The exact-distance sharpening is too strict.  Only `83` of `430`
distances have a positive pointwise min-replacement gap, and the
disconnected exact-distance envelope is worse than the adverse
`Q=46189` total.

The useful local structure is a short aggregate block.  The
`56A..58A` block separates by both positive share and total pressure,
while `56A..57A` and `57A..58A` are the minimal one-`A` separating
micro-slices.  This narrows the next theorem-shaped target to
short-block signed balance, not pointwise exact-distance dominance.

This is finite selected-family diagnostic evidence only.  It proves
no exact-distance pointwise theorem, short-block positive-share
theorem, short-block pressure theorem, replacement residue-gap bound
theorem, coordinate-00 residue-gap sign theorem, strict-central
Goldbach theorem, or Goldbach proof.

# q286-WBSS active-character collapse audit

## Question

After closing the named source-fit routes, should the raw active-character
target remain the active q286 proof engine?

## Receipt

```text
tools/build_q286_wbss_active_character_collapse_audit.py
evidence/q286-wbss-active-character-collapse-audit.json
```

## Result

```text
status: SLEEP_active_character_route_until_independent_raw_theorem_or_new_engine
active complex characters: 122
active real channels: 64
aggregate character L2: 5.525106448699807
normalized L2 cap when mass-positive: 0.10930746469603118
direct raw pointwise source bridges found: 0
```

The raw active-character target is logically clean only when stated as a strict
unnormalized theorem.  But that theorem is itself support-creating:

```text
W_phi(N)>0
```

is a sum over strict-central prime-pair terms, so proving it for a covered
target implies a strict-central Goldbach representation for that target.

Likewise the raw aggregate `L2` theorem shape

```text
C2 * sqrt(sum |D_raw_{d,chi}(N)|^2) < T_N*M(a)
```

is non-circular as a theorem shape, because it fails at zero support.  But no
universal pointwise raw active-character moment theorem is present.

## Route Classification

```text
direct W_phi(N)>0: valid raw target, but Goldbach-strength
raw aggregate L2 < T_N*M(a): non-circular shape, theorem missing
P0-scaled signed major arc: possible raw theorem, unproved
normalized character distribution after T_N>0: conditional decoration
```

## Decision

`SLEEP_active_character_route_until_independent_raw_theorem_or_new_engine`.

The active-character package remains useful structure, but it is not the active
proof engine after the source-fit closure.  A direct `W_phi(N)>0` or raw
aggregate `L2` theorem would be non-circular, but proving it would itself be a
pointwise strict-central binary-prime theorem.  The next evidence-bearing
Goldbach move should therefore switch proof engines or introduce a genuinely
new raw signed-weight theorem.  More finite q286 evidence is not an acceptance
condition.

This is a logical dependency HOLD only.  No active-character moment theorem,
signed-weight major/minor arc estimate, raw weighted witness theorem,
positive-mass theorem, q286 threshold theorem, strict-central Goldbach theorem,
or Goldbach proof is established.

# Goldbach bridge semantic route graph

## Question

Can the active Goldbach route be represented as a semantic dependency graph
while keeping the human-facing notes linear?

## Receipt

```text
tools/build_goldbach_semantic_route_graph.py
evidence/goldbach-semantic-route-graph.json
```

## Result

Yes.  The graph is a derived navigation artifact with current nodes for:

```text
current bridge acceptance gate
raw adverse-drag theorem target
pointwise adverse-drag theorem target
q286 aggregate L2 HOLD
metric-soft source-admissible window finite audit
broad checked-scale phase-translation finite falsifier
finite evidence is not acceptance
Goldbach target
four proof obligations
```

The key machine-facing edges are:

```text
broad translated dominance --falsified by--> M=149,p=163,start=1
broad translated dominance --narrows to--> source-admissible window target
source-admissible window --not acceptance for--> Goldbach
L2 bridge --blocks route--> pointwise adverse-drag as confirmed bridge
raw adverse-drag --raw form of--> pointwise adverse-drag
pointwise adverse-drag --requires--> four proof obligations
finite evidence rule --blocks closeout of--> Goldbach
```

The receipt also stores several projection views so the same evidence can be
read in different useful orders:

```text
branch_map
by_theorem_attempt
by_result_state
by_evidence_weight
churn_or_low_return_flags
thin_or_frontier_flags
```

The `branch_map` uses Goldbach as the nexus, the bridge gate as the trunk,
live branches for raw adverse-drag and source-window work, a held branch for
aggregate `L2`, and dead ends for broad all-translation dominance and finite
evidence as acceptance.  It is deliberately not a pure tree: the graph also
stores `cycle_or_return_signals` for routes that loop back to a gate or HOLD
under unchanged conditions.

The first churn flags are normalized aggregate `L2` finite scans and broad
all-translated active-window dominance.  The first thin/frontier flags are the
source-window implication theorem and the universal pointwise raw adverse-drag
bound.

## Boundary

The semantic graph is not mathematical authority.  It is rebuilt from current
receipts and exists to keep dependencies visible.  The authoritative record is
still the owning commit, evidence receipts, tests, notes, and cited
mathematics.

## Decision

Use the graph as the machine-facing active-route map:

```text
raw pointwise adverse-drag is live and unproved
L2 is held
broad translated dominance is finitely falsified
source-window evidence is useful but needs an implication theorem
finite evidence is not acceptance
Goldbach remains open
```

This proves no semantic graph theorem, aggregate `L2` theorem, source-window
theorem, raw adverse-drag theorem, q286 threshold theorem, strict-central
Goldbach theorem, or Goldbach proof.

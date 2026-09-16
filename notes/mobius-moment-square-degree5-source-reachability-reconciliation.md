# Mobius moment-square degree-5 source reachability reconciliation

## Question

After the start-`1` puncture was proved unreachable from the original
checked-scale source mapping, what remains of the source-window lane?

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_reachability_reconciliation.py
evidence/mobius-moment-square-degree5-source-reachability-reconciliation.json
```

## Result

```text
broad translated quantifier falsified:       true
broad failure count:                         1
reachable source failure count:              0
unreachable translated failure count:         1
unclassified failure count:                   0
all source starts pass:                    true
source start failure count:                   0
minimum source-start ratio:   0.5563677490893767
minimum source-start slack:   0.056367749089376695
```

The only broad translated failure is still:

```text
M=149, p=163, component (00,12), active row start 1
```

but the reachability audit classifies it as:

```text
UNREACHABLE from the original source mapping
```

The canonical source start at that scale is `32`, and all six checked canonical
source starts pass.

## Decision

The broad all-translated-start theorem remains finitely falsified.  The
source-window lane survives as a narrower theorem target: prove canonical
source-start control, or define a non-post-hoc arithmetic admissibility map
that explains which translated starts are reachable.

Endpoint-swap and reduced-denominator analysis of start `1` is reservoir
evidence unless a separate arithmetic mapping makes start `1` source-
admissible.

This is finite reconciliation only.  It proves no source-window theorem,
source-admissible-window theorem, endpoint-swap theorem, strict-central
Goldbach theorem, or Goldbach proof.

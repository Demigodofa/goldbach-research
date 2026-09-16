# Goldbach adverse-alignment unification audit

## Question

Can q286 and Q46189 be combined as versions of the same bad-mass-cannot-coherently-align principle?

## Receipt

```text
tools/build_goldbach_adverse_alignment_unification_audit.py
evidence/goldbach-adverse-alignment-unification-audit.json
```

## Answer

Yes as a shared theorem schema and research language; not yet as a proved theorem or a merged numeric formula.

## Shared Schema

Given a decomposition into channels C_N, define A_D(N)=sum_{c in C_N} max(0,-E_c(N)).  A sufficient bridge has the shape A_D(N) < B_D(N), where B_D(N) is a raw or local structural budget independent of already assuming the desired prime-pair support.

A counterexample-shaped obstruction would need harmful mass to align across all available channels strongly enough to beat the structural budget.  A proof would show that such coherent adverse alignment is impossible in the covered class.

## q286 Instantiation

Channels: `['70', '130', '154', '286']`.

Adverse object: `A_raw_-(N)=sum_d max(0,-U_d(N))`.

Strong finite theorem shape: raw sufficient inequality is non-circular in form, and the finite component envelope survives the checked horizon.

## Q46189 Instantiation

Useful diagnostic/falsifier language, but not theorem-ready after simple sign, curvature, and matrix-margin features failed or stayed weak.

Best input feature: `missing_count` with Pearson `0.32654799306706145`.

Best matrix feature: `tension_sum` with Pearson `-0.2169202637521853`.

## Decision

q286 and Q46189 can be combined as a shared adverse-alignment schema: harmful signed mass should not coherently align across all available channels strongly enough to beat the relevant budget.  This is currently a useful research language, not a theorem.  q286 is the stronger proof-shaped instantiation; Q46189 supplies diagnostics and failed shortcut baselines.

This is a unifying research language only.  It proves no adverse-
alignment theorem, universal raw pointwise theorem, strict-central
Goldbach theorem, or Goldbach proof.

# q286-WBSS four-modulus adverse-drag horizon audit

## Question

The aggregate lambda horizon preserved positivity and `lambda_phi < 1` on
`232` fresh lifted rows.  Is that success dependent on delicate signed
cancellation among the four projected moduli, or does a stronger one-sided
finite certificate survive after discarding every helpful positive projected
term?

## Mechanism

Replay the `232`-row lambda horizon and decompose each row into the four
projected errors for moduli `70`, `130`, `154`, and `286`.  For each row,
compute

```text
adverse_drag = sum(max(0, -E_d))
adverse_only_expectation = local_main - adverse_drag.
```

This is stronger than the signed aggregate witness because it throws away all
positive projected help.

## Receipt

```text
tools/build_q286_wbss_four_modulus_adverse_drag_horizon_audit.py
evidence/q286-wbss-four-modulus-adverse-drag-horizon-audit.json
```

## Result

```text
horizon targets:                         232
target range:                1036248..1115822
actual positive rows:                    232 / 232
adverse-only positive rows:              232 / 232
adverse-only nonpositive rows:             0 / 232
projected subset checks:                3480
projected subset failures:                 0
maximum adverse-drag ratio: 0.18121406011311528
largest adverse-drag target:          1059514
minimum adverse-only expectation: 0.6096203823025632
tightest adverse-only target:          1059514
```

Every single-modulus removal remains positive on all rows.  Every
single-modulus-only expectation `local_main + E_d` also remains positive on
all rows.  More strongly, every nonempty projected subset has positive
`local_main + subset_error` on all `232` rows, for `232 * 15 = 3480` subset
checks.

At the tightest row `1059514`,

```text
local_main:             0.7445418302942308
adverse_drag_ratio:     0.18121406011311528
adverse_only_expectation: 0.6096203823025632
E70:  -0.006421818246366151
E130: -0.00019421834725166684
E154: -0.02689463141005005
E286: -0.10141077998799973
```

## Decision

The successful aggregate lambda horizon has a stronger finite one-sided
certificate: local main beats total adverse projected drag even after all
helpful positive projected terms are discarded.  This demotes explanations
that require delicate signed cancellation or one essential projected modulus.

This is still finite horizon evidence only.  It proves no one-sided signed
concentration theorem, no fixed-modulus equidistribution theorem, no q286
threshold theorem, no strict-central Goldbach theorem, and no Goldbach proof.
The live theorem target is a source-backed bound on one-sided adverse
four-modulus drag relative to local main.

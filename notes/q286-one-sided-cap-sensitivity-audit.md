# q286 one-sided cap sensitivity audit

## Question

For the one-sided q286 route, which uniform per-modulus adverse caps fit the checked component envelope, and which would be sufficient theorem targets if proved universally?

## Receipt

```text
tools/build_q286_one_sided_cap_sensitivity_audit.py
evidence/q286-one-sided-cap-sensitivity-audit.json
```

## Result

```text
component horizon rows:                  232
A_70 observed supremum:                  0.11808088288936758
A_130 observed supremum:                 0.00932108976691037
A_154 observed supremum:                 0.08239931832908774
A_286 observed supremum:                 0.12228599640255161
observed supremum sum:                   0.3320872873879173
minimum local main:                      0.717245423802844
observed max component adverse:          0.12228599640255161
strict equal-cap ceiling min(M)/4:       0.179311355950711
finite cap window nonempty:              True
finite cap window width:                 0.05702535954815938
```

For these caps, smaller is stricter because the cap is an upper bound.
So `.125` is stricter than `.126`, and both are stricter than `.13`.

## Cap Table

```text
cap      observed fit   equal-cap sufficient if universal   margin
0.12     False          True                                 0.23724542380284397
0.122    False          True                                 0.22924542380284396
0.125    True           True                                 0.21724542380284395
0.126    True           True                                 0.21324542380284395
0.13     True           True                                 0.19724542380284393
0.15     True           True                                 0.11724542380284397
0.175    True           True                                 0.017245423802843995
0.18     True           False                                -0.0027545761971560223
```

## Decision

The one-sided per-modulus cap route has a nonempty finite window. The largest observed component adverse supremum is about 0.12228599640255161, while the strict equal-cap ceiling from the minimum checked local main is about 0.179311355950711. Thus .125, .126, and .13 are not too strict for this finite horizon and would be sufficient equal caps if proved universally.  They are still finite-fit candidates only; the universal theorem remains open.

This is finite cap-sensitivity evidence only.  It proves no per-modulus
supremum theorem, one-sided signed concentration theorem, raw adverse-
envelope theorem, strict-central Goldbach theorem, or Goldbach proof.

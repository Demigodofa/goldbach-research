# q286-WBSS K286 zero-residue component-phase audit

## Question

The directional-slack audit showed that aggregate active-character `L2` can
exceed the sufficient zero-lane cap while actual adverse drag remains small.
Where does that nonalignment live?

This audit asks two narrower questions on the `18` cap-violating zero-lane
rows:

1. Which modulus dominates the Cauchy `L2` threat?
2. Which modulus actually realizes the largest adverse component?

It also checks the multiplicative-character phase reconstruction

```text
signed_error_d(row) = sum_chi c_hat_d(chi) * moment_hat_d(row, chi)
```

so that any later phase picture is tied to exact arithmetic.

## Receipt

```text
tools/build_q286_wbss_k286_zero_residue_component_phase_audit.py
evidence/q286-wbss-k286-zero-residue-component-phase-audit.json
```

## Result

```text
L2-cap-violating zero-lane rows:        18
dominant Cauchy-threat modulus:         286 on 18 / 18 rows
dominant actual-adverse modulus counts: 154 -> 6
                                      : 286 -> 5
                                      : 70  -> 4
                                      : 130 -> 3

violating-row aggregate Cauchy threat mean:       1.1189916481072606
violating-row aggregate raw adverse mean:         0.06125731999751208
violating-row aggregate directional efficiency:   0.05468085899942172

modulus 286 Cauchy threat mean:                   0.7672836478772077
modulus 286 actual adverse mean:                  0.029285134674525884
modulus 286 directional efficiency mean:          0.03794725356022015
modulus 286 phase cancellation ratio mean:        0.15132464895023304
modulus 286 adverse/rescue split:                 8 adverse, 10 rescue

largest aggregate threat target:                  1171456
largest aggregate threat residue:                 286 mod 10010
largest aggregate threat ratio:                   1.354153874306624
largest aggregate actual adverse ratio:           0.024989313695990587
largest aggregate directional efficiency:         0.018453821364123796
```

The per-modulus phase reconstruction errors are at floating-point noise level;
for modulus `286`, the maximum reconstruction error is below `5e-17`.

## Decision

`DIAGNOSTIC_zero_residue_component_phase_nonalignment`.

The finite obstruction is sharper now.  Modulus `286` carries the Cauchy norm
threat on every aggregate-`L2` violating zero-lane row, but actual adverse drag
is distributed across moduli.  Even within modulus `286`, the component is a
rescue more often than an adverse term on these rows.

The next theorem-shaped target is a `K_286` phase-oscillation or
coefficient-direction nonalignment estimate, not another aggregate `L2`
estimate.  A universal proof would still need a pointwise, unnormalized
analytical estimate showing raw adverse drag below local main for every
sufficiently large `N`.

No component theorem, phase-mode theorem, coefficient-direction nonalignment
theorem, universal pointwise raw bound, q286 threshold theorem, strict-central
Goldbach theorem, or Goldbach proof is established.

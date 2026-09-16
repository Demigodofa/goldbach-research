# Post-q286 Mobius frontier reconciliation

## Question

The post-q286 proof-engine triage selected the Mobius incomplete prime-row
covariance route and named the incomplete-row boundary operator as the next
test.  But the repository already contains an older boundary-operator chain.
What is the current Mobius frontier after reconciling that existing work?

## Receipt

```text
tools/build_post_q286_mobius_frontier_reconciliation.py
evidence/post-q286-mobius-frontier-reconciliation.json
```

## Result

```text
status: TARGET_mobius_six_coordinate_active_full_lower_frame
```

The boundary-operator derivation is already present.  The exact primitive
frequency/operator reduction in `lcm_sawtooth_incomplete_frequency.py` proves
the conductor packet identity on the checked fixture and restricts the actual
Mobius/log vectors to a rank-three quadratic-log family.  The unproved task is
not to rederive that operator; it is to prove a uniform arithmetic bound for
the resulting structured family.

Small checked fixture:

```text
actual row-varying energy ratio:          1.3185678242920014
sharp row-varying quadratic-span ratio:   1.4913014000886855
```

## Current Frontier

The active Mobius theorem target is now the six-coordinate active/full
lower-frame problem for the incomplete-row boundary.  On the checked
`M=127` aggregate block:

```text
whitened Gershgorin lower-frame bound:     0.7454313024194685
exact smallest generalized eigenvalue:     0.8768802946823543
one-half lower frame certified:            true
```

The axial Schur-response pattern remains a candidate compression:

```text
Schur margin:                              0.005795730853614067
nonaxial energy error:                     0.005427450063227847
nonaxial error / Schur margin:             0.9364565402210543
determinant axial distance:                0.0128246653667984
moment-curve parameter:                    0.2795716513419446
moment-curve projective distance:          4.166667001461609e-05
actual selector angle:                     60.912673267452014 degrees
```

## Decision

Do not use the post-q286 wording as if the boundary operator still needs to be
derived.  The live route is:

```text
six-coordinate active/full lower-frame theorem
plus axial Schur-response determinant/norm and effective-log bounds
```

Smallest next tests:

```text
prove/falsify uniform entrywise estimates for the whitened aggregate matrix
derive/falsify an explicit effective-log formula for the axial moment parameter
prove/falsify determinant/norm lower bounds and nonaxial-energy upper bounds
```

Keep these in sleep/reservoir unless a changed condition appears:

```text
post-q286 wording that says the boundary operator still needs derivation
arbitrary-conductor-vector subpower route
raw-coordinate Gershgorin
fixed dyadic-centered raw-coordinate basis
simple positive centroid formula for the effective-log parameter
```

No uniform active/full lower frame, Mobius covariance theorem, signed
prime-correlation estimate, q286 theorem, strict-central Goldbach theorem, or
Goldbach proof is established.

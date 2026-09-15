# q286-WBSS Mod-286 Interaction Audit

Status: finite interaction diagnostic. Goldbach is not proved.

Receipt:

```text
tools/build_q286_wbss_mod286_interaction_audit.py
evidence/q286-wbss-mod286-interaction-audit.json
```

## Question

The projected-uniformity obstruction localized the recurring signed drag to
the modulo `286` projection. Since `286 = 2*11*13`, this audit asks whether
that drag is explained by simpler one-dimensional modulo `11` or modulo `13`
marginal bias, or by the genuine two-factor interaction on the unit grid
modulo `11 x 13`.

## Result

The mod-286 coefficient is almost entirely an interaction object in this
finite fixture:

```text
residue count:                         120
total centered coefficient SS:         2571.08639647042
mod 11 variance share:                 0.0000226223194893031
mod 13 variance share:                 0.0000907492767647826
additive variance share:               0.000113371596254086
interaction variance share:            0.999886628403746
max decomposition residual:            0
max absolute interaction coefficient:  31.9157419871399
```

Replaying the actual `196` post-discovery rows gives the same answer on the
measure side:

```text
total mod-286 signed error range:       -0.7066366026664204..-0.27555447095822444
interaction component range:            -0.70682602570542..-0.2760993456913682
interaction / total ratio range:        0.9901149848469164..1.0113712816733669
additive marginal component range:      -0.003264936681970069..0.0032405528357605058
mod 11 marginal component range:        -0.0016410202438457175..0.0024058340896744115
mod 13 marginal component range:        -0.0028522972005577494..0.003103157122204108
```

All `196/196` total mod-286 signed errors are negative. All `196/196`
interaction components are also negative. The one-factor marginal components
are small and mixed-sign.

## Decision

Demote the simple one-dimensional AP marginal route for explaining the
mod-286 drag. The useful created object is now sharper:

```text
prove a signed mod-11-by-mod-13 covariance bound for the mod-286 projection,
or bypass the projection route and prove the raw q286-WBSS signed witness
B_Phi(N)>0 directly.
```

This is a genuine narrowing of the finite obstruction: the drag is not merely
"mod 286 is nonuniform"; it is concentrated in the `11 x 13` interaction
component after the one-factor pieces are removed.

## Boundary

This audit proves no interaction theorem, no signed projection theorem, no
q286 threshold theorem, no strict-central Goldbach theorem, and no Goldbach
proof. It only identifies the finite interaction structure that a future
source-backed theorem would need to control.

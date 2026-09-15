# q286-WBSS Mod-286 Residual Group Profile Audit

Status: finite residual-group diagnostic. Goldbach is not proved.

Receipt:

```text
tools/build_q286_wbss_mod286_residual_group_profile_audit.py
evidence/q286-wbss-mod286-residual-group-profile-audit.json
```

## Question

The top-20 bandlimited audit left a one-sided residual theorem target: the
remaining five Fourier conjugacy groups may push upward, but that pushback must
stay below the top-20 negative main drag. This audit asks whether the five
residual groups have a smaller fixed explanation: one culprit group, or a
proper fixed residual subpackage.

## Result

The five residual conjugacy groups, indexed after removing the top `20`, are:

```text
0: representative (k mod 10, ell mod 12) = (1, 1)
1: representative (k mod 10, ell mod 12) = (1, 9)
2: representative (k mod 10, ell mod 12) = (4, 10)
3: representative (k mod 10, ell mod 12) = (4, 2)
4: representative (k mod 10, ell mod 12) = (3, 9)
```

On the `24` rows where the total residual pushes upward, the largest positive
group rotates:

```text
argmax counts by residual group:        0:8, 1:6, 2:2, 3:2, 4:6
group positive-on-upward rows:          11, 19, 13, 13, 17
positive-part sum range:                0.015665110382707383..0.1085525933209394
negative-part sum range:                0.005855819164302735..0.06915095691026972
```

Best fixed subset profiles on those same `24` upward rows:

```text
best size-1 subset:  [1],       touches 19 / 24, signed-positive 19 / 24
best size-2 subset:  [1,4],     touches 23 / 24, signed-positive 20 / 24
best size-3 subset:  [0,1,4],   touches 24 / 24, signed-positive 17 / 24
best size-4 subset:  [0,1,2,4], touches 24 / 24, signed-positive 20 / 24
all five groups:     [0..4],    touches 24 / 24, signed-positive 24 / 24
```

Some proper triples and quadruples have at least one positive member on every
upward-pushback row, but their signed subtotal still fails on some rows. The
actual upward residual is a cancellation balance across all five residual
groups, not a fixed one-group or proper-subset event.

## Decision

Demote the fixed proper residual-subset shortcut. The surviving theorem target
must control the signed aggregate of all five residual groups:

```text
positive_residual_pushback(N)
  = max(0, sum_{g in residual five} R_g(N))
  <= theta * top20_drag(N)
```

for a fixed `theta < 1`, or replace the top-20/residual split with a different
aggregate q286-WBSS signed witness. The prior `theta=0.13` finite target
remains alive; this audit says not to try proving it by isolating one culprit
residual character group.

## Boundary

This audit proves no residual theorem, no signed projection theorem, no q286
threshold theorem, no strict-central Goldbach theorem, and no Goldbach proof.
It only blocks the smaller fixed residual-subset explanation on the current
finite fixture while preserving the five-group one-sided absorption target.

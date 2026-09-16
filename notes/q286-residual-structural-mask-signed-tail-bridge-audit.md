# q286 residual structural-mask signed-tail bridge audit

## Question

The all-row adverse-tail stress audit rejected the unqualified adverse-envelope
version of the structural-mask route.  What survives if the omitted tail is
kept as a signed packet sum instead of being replaced by disconnected adverse
suprema?

## Mechanism

For each structural mask, decompose each frozen row as

```text
full_action = aligned_only_full_action + mask_signed_action + tail_signed_action
```

and compute the positive-row budget

```text
full_action / abs(tail_signed_action)
```

when the omitted tail is nonzero.  This is not a proof.  It measures the
relative signed-tail accuracy a future pointwise theorem would need if the
aligned and retained-mask pieces were handled exactly.

## Receipt

```text
tools/build_q286_residual_structural_mask_signed_tail_bridge_audit.py
evidence/q286-residual-structural-mask-signed-tail-bridge-audit.json
```

## Result

```text
positive rows:                                      5
two-subcube all-row adverse-tail margin:  -0.3385081689657937
two-subcube signed-tail budget:            0.07569390912763455
two-subcube tight target:                              94856
two-subcube tight signed tail:            -0.16211735719392256
two-subcube tight tail abs:                 0.16614898660595553

support-size <=2 all-row adverse-tail margin:
                                             -0.18722458212180332
support-size <=2 signed-tail budget:          0.24152101169573884
support-size <=2 tight target:                            94856

full 15-packet signed budget:                 0.055452588891044076
```

The support-size `<= 2` structural mask has the loosest finite signed-tail
budget on the tight row.  The two-subcube mask still improves materially over
the full 15-packet signed budget, but is more fragile than the support-size
mask under this tail-relative measurement.

## Zero-Mass And L2 Boundary

The prior q286-WBSS observed L2 audit confirmed no zero strict-central pair
mass on its `348` checked rows:

```text
zero pair rows:                 0
zero actual mass rows:          0
nonunit actual mass rows:       0
nonunit uniform mass rows:      0
row-local L2 cap failures:    120
```

That removes a normalization-defect explanation for the finite L2 failures.
It does not confirm a non-circular analytic bridge.  The aggregate L2 formula
remains coefficient arithmetic plus finite diagnostics until an external
pointwise twisted binary-prime moment estimate is proved.

## Decision

`HOLD_signed_tail_bridge_requires_external_pointwise_theorem`.

The next proof object should not be an unqualified adverse-envelope theorem.
It should be a universal, pointwise, unnormalized signed packet/tail estimate
for a mathematically named class, strong enough to imply

```text
AdverseDrag(N) < LocalMain(N)
```

or the corresponding signed lower bound, for every sufficiently large eligible
even `N`.  The support-size `<= 2` mask is now the cleaner finite theorem
target than the two-subcube mask if a signed-tail theorem is pursued.

No signed-tail theorem, non-circular aggregate L2 bridge, structural-mask
theorem, q286 threshold theorem, strict-central Goldbach theorem, or Goldbach
proof is established.

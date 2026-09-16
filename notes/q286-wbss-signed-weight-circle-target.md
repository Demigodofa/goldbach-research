# q286-WBSS signed-weight circle-method target

## Question

What exact circle-method theorem would have to replace the missing signed-region
source bridge, and when does it collapse to ordinary strict-central Goldbach
support?

## Receipt

```text
tools/build_q286_wbss_signed_weight_circle_target.py
evidence/q286-wbss-signed-weight-circle-target.json
```

## Raw Target

Let

```text
I_N={n: N/3<n<2N/3}
P(n)=log(n) if n is prime, otherwise 0
Phi_a(n)=phi_a(n mod 10010), where a=N mod 10010.
```

The exact target is the raw signed weighted convolution

```text
W_phi(N)=sum_{n in I_N} P(n)P(N-n)Phi_a(n)>0
```

for every sufficiently large covered even `N`, plus an explicit finite
remainder.

Equivalently,

```text
W_phi(N)=W_+(N)-W_-(N),
```

where `W_+` sums the positive `Phi_a` residues and `W_-` sums `-Phi_a` on the
negative residues.  The signed-region target is

```text
sum_{u:phi(u)>0} P_N(u)phi(u)
  > sum_{u:phi(u)<0} P_N(u)(-phi(u)).
```

The circle-method form is

```text
W_phi(N)=int_0^1 Q_{a,N}(alpha)P_N(alpha)e(-alpha N)dalpha
```

with

```text
Q_{a,N}(alpha)=sum_{n in I_N}P(n)Phi_a(n)e(alpha n)
P_N(alpha)=sum_{n in I_N}P(n)e(alpha n).
```

## Non-Circularity

If `T_N=0`, then there are no strict-central prime pairs, so

```text
W_phi(N)=W_+(N)=W_-(N)=0.
```

Thus the strict target `W_phi(N)>0` becomes `0>0`, which is false.  A proof of
the raw strict target would create strict-central support.  A normalized
landing theorem cannot do that unless support is created inside the same raw
argument.

## Collapse Classifier

The route survives if the argument proves `W_phi(N)>0`, `W_+(N)>W_-(N)`, or an
equivalent raw adverse-drag inequality directly for every sufficiently large
covered `N`.

The route collapses if the proof first assumes or separately proves `T_N>0`,
then uses q286 only as conditional distribution control.

Invalid substitutes:

```text
finite q286 windows
local-uniform shape margin without pointwise prime-pair control
almost-all or averaged AP Goldbach statements
marginal AP prime counts
normalizing by T_N before raw support exists
```

## Decision

`TARGET_bespoke_signed_weight_circle_method_or_collapse`.

No major/minor arc estimate is proved.  The next evidence-bearing step is a
symbolic major-arc local-factor decomposition for `Phi_a`, or a sleep decision
if that decomposition only becomes positive after importing `T_N>0`.

This proves no major/minor arc estimate, signed negative-region distribution
theorem, raw adverse-drag theorem, positive-mass theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof.

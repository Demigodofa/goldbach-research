# q286-WBSS raw character expansion target

## Question

After the source-theorem fit audit, can the q286 route state the exact raw
character-expanded theorem target instead of asking vaguely for a binary-prime
estimate?

## Receipt

```text
tools/build_q286_wbss_raw_character_expansion_target.py
evidence/q286-wbss-raw-character-expansion-target.json
```

## Raw Expansion

Define the strict-central log-pair mass

```text
T_N = sum_{N/3<p<2N/3, p and N-p prime} log(p)log(N-p).
```

For `d in {70,130,154,286}`, define

```text
Delta_raw_{d,s}(N)
  = Pi_raw_{N,d}(s) - T_N * U_{a,d}(s),
```

where `Pi_raw_{N,d}(s)` is the raw strict-central log-pair mass with left prime
`p == s mod d`, `U_{a,d}` is the local-uniform projected mass, and
`a=N mod 10010`.

For each active multiplicative character,

```text
D_raw_{d,chi}(N) = sum_s chi(s) Delta_raw_{d,s}(N).
```

Using the same finite character coefficients as the multiplicative-character
payment audit,

```text
E_raw_d(N) = sum_chi c_hat_{d,chi} D_raw_{d,chi}(N).
```

The raw q286-WBSS witness is

```text
W_phi(N) = T_N*M(a) + sum_d E_raw_d(N).
```

The strict raw adverse-gap form is

```text
G_raw(N) = T_N*M(a) - sum_d max(0, -E_raw_d(N)).
```

## Sufficient Raw Theorem Shapes

Aggregate `L2` payment:

```text
C2 * sqrt(sum_{d,chi}|D_raw_{d,chi}(N)|^2) < T_N*M(a)
```

with

```text
C2 = 5.525106448699807.
```

When `T_N>0`, this is the normalized cap

```text
sqrt(sum |D_{d,chi}(N)|^2) < 0.10930746469603118.
```

But the raw strict form is the important bridge: if `T_N=0`, every raw
character moment is zero and both sides are zero, so the strict inequality
fails.  A proof of the strict raw inequality would therefore create
strict-central support.

Aggregate `L1` payment:

```text
sum_{d,chi}|c_hat_{d,chi}|*theta_raw_{d,chi}(N) < T_N*M(a),
|D_raw_{d,chi}(N)| <= theta_raw_{d,chi}(N).
```

Direct signed sum:

```text
W_phi(N)>0.
```

## Coefficient Package

```text
active complex characters:       122
active real channels:             64
total character L1:        49.153988812629684
uniform normalized L1 cap:  0.012286599575574883
aggregate character L2:     5.525106448699807
normalized L2 cap:          0.10930746469603118
```

Finite diagnostics from the observed L2 audit remain only diagnostics:

```text
checked rows:                       348
row-local L2 cap violations:        120
global-minimum L2 cap violations:   301
```

They falsify premature claims that the normalized L2 cap already holds on the
checked scale.  They do not refute a future sufficiently-large theorem with an
explicit threshold.

## Collapse Or Sleep Test

If a proposed circle-method proof first needs an independent pointwise lower
bound

```text
T_N >= P(N) > 0
```

for every covered `N`, and the character estimates only work after that mass is
known, then the route has collapsed to ordinary strict-central binary Goldbach
plus decoration.

The route survives only if the raw character inequality itself is proved
strictly, or if the positive-mass input is separately sourced and honestly
labeled Goldbach-strength.

## Decision

`TARGET_raw_character_expanded_q286_WBSS_theorem`.

The exact raw character-expanded target is now defined.  No theorem proving it
is currently present.  The next proof attempt must attack the raw twisted
binary-prime moments directly or put the q286 lane to sleep if it requires
pointwise `T_N>0` first.

This proves no raw character-moment theorem, strict raw-gap theorem,
positive-mass theorem, q286 threshold theorem, strict-central Goldbach theorem,
or Goldbach proof.

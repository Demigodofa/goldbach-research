# q286 raw-sum expansion ledger

## Question

Can U_d(N), W_phi(N), and the q286 adverse envelope be written as direct raw sums with no mu_N notation, while preserving the zero-mass and L2 bridge boundaries?

## Receipt

```text
tools/build_q286_raw_sum_expansion_ledger.py
evidence/q286-raw-sum-expansion-ledger.json
```

## Raw Ledger

The theorem-ready q286 route can be written without `mu_N`:

```text
T_N = sum_{N/3<p<2N/3, p and N-p prime} log(p)log(N-p)
Pi_raw_{N,d}(s) = sum over the same pairs with p == s mod d
U_d(N) = sum_s alpha_{d,s}(Pi_raw_{N,d}(s)-T_N U_{a,d}(s))
L_raw(N) = T_N M(a)
A_raw_-(N) = sum_d max(0,-U_d(N))
W_phi(N) = L_raw(N)+sum_d U_d(N)
```

Equivalently, the character expansion uses

```text
D_raw_{d,chi}(N)=C_{d,chi}(N)-U_{a,d,chi} C_0(N)
U_d(N)=E_raw_d(N)=sum_chi c_hat_{d,chi}D_raw_{d,chi}(N).
```

The direct witness is the unnormalized signed log-pair sum
`W_phi(N)=sum log(p)log(N-p) phi_a(p mod 10010)` over strict-central
prime pairs.

## Zero-Mass Boundary

If no strict-central pair exists, then every raw sum above vanishes.
Thus the strict targets `A_raw_-(N)<L_raw(N)`, the aggregate raw L2
target, and `W_phi(N)>0` all fail at zero support.  A proof of one
of those strict raw statements would therefore create support.

## L2 Status

The L2 target is non-circular as a strict raw shape, but it is not
confirmed as a logical bridge.  The existing zero-mass check is an
arithmetic sanity check, not a pointwise theorem.

## Finite Calibration

```text
rows:                              348
max raw adverse ratio:             0.23148438379145228
min raw adverse gate gap:          286929.1729900494
all checked raw gaps positive:     True
finite evidence is acceptance:     false
```

## q286 / Q46189 Bridge Read

q286 and Q46189 remain compatible as adverse-alignment language: bad
mass must not coherently align across all available channels.  They
are not yet a merged theorem.  Q46189 would need a residual bridge:
harmful source-block mass expressed as raw q286-style adverse mass
plus a universally bounded residual.

Best Q46189 input feature remains `missing_count`
with Pearson `0.32654799306706145`.
Best genuine matrix feature remains `tension_sum`
with Pearson `-0.2169202637521853`.

## Decision

The q286 raw objects can now be stated as a direct raw-sum ledger with no mu_N notation in the theorem-ready statements.  This confirms the arithmetic decomposition and the zero-support non-circularity of the strict raw targets, but it does not prove the universal pointwise estimate.  The L2 target remains a raw candidate only, not a confirmed logical bridge.  Q46189 combines with q286 as adverse-alignment language, not as a theorem input until a residual bridge is proved.

This proves no L2 bridge, q286/Q46189 combined theorem, raw adverse-
envelope theorem, raw witness theorem, strict-central Goldbach theorem,
or Goldbach proof.

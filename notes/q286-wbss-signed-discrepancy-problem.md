# q286-WBSS Signed Discrepancy Problem

Status: finite problem-definition receipt and theorem-shaping evidence only.
Goldbach is not proved.

Receipt:

```text
tools/build_q286_wbss_signed_discrepancy_problem.py
evidence/q286-wbss-signed-discrepancy-problem.json
```

## Question

The q286-WBSS main-term audit found a positive local-uniform mean, but the
L1-budget audit showed that ordinary total-L1 uniformity is far too strong for
the actual strict-central binary-prime measures.  The next question is:

Can the failed L1 bridge be replaced by the exact signed projection that can
erase the positive local mean?

## Definition

For each admissible target residue `a`, let:

- `u_a` be the local uniform orbit measure;
- `mu_N` be the normalized strict-central binary-prime orbit measure;
- `phi_a` be one frozen q286-WBSS coefficient function;
- `m_a=<u_a,phi_a>`.

For the checked q286-WBSS rows, `m_a>0`.  Define:

```text
lambda_phi(N) = -<mu_N-u_a, phi_a-m_a> / m_a.
```

Then:

```text
<mu_N,phi_a> > 0  iff  lambda_phi(N) < 1.
```

So the theorem problem is now:

```text
Prove lambda_phi(N) <= 1 - eta(N)
```

for an explicit positive margin `eta(N)` on every sufficiently large covered
even target, then verify the finite remainder.

Equivalently, prove the unnormalized signed binary-prime correlation estimate
`B_Phi(N)>0` directly.

## Result

On the `196` post-discovery rows:

```text
full coefficient:
  lambda range:              0.1928435193007601..0.9823120581948911
  positivity margin ratio:   0.01768794180510891..0.80715648069924
  L1 worst-case load range:  10.615378246364296..58.85757007200199
  signed threshold passes:   196/196
  L1 budget passes:          0/196

edge beta coefficient:
  lambda range:              -0.35573114438883136..0.9511600258401234
  positivity margin ratio:   0.04883997415987662..1.3557311443888314
  L1 worst-case load range:  3.3936673457437085..55.73635115717084
  signed threshold passes:   196/196
  L1 budget passes:          0/196
```

The tightest signed row is again target `94856`.

## Decision

This turns the previous answer into a sharper problem.  The actual measures
are very far from local uniform, but they are not anti-correlated with the
q286-WBSS coefficient direction strongly enough to destroy positivity.  The
proof target is therefore a coefficient-aligned signed discrepancy theorem,
not total-uniformity, parity, a static dictionary, or an unweighted mass cone.

## Gap

The scalar inequality is exact, so it is not by itself a proof.  The missing
step is a source-backed estimate for:

```text
<mu_N-u_a, phi_a-m_a>
```

or for the corresponding raw weighted binary-prime sign sum.  Without that
estimate, the signed discrepancy problem is only a precise restatement of the
positivity bridge.

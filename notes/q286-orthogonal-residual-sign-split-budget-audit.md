# q286 orthogonal-residual sign-split budget audit

Status: finite theorem-budget audit.  This is not an orthogonal residual
lower-tail theorem, signed binary-prime correlation theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof.

## Question

After plain projection uniformity and generic norm control were demoted, does
the orthogonal-residual decomposition give a materially looser source theorem?

The decomposition is:

```text
full(N) = aligned(N) + <mu_N, h_a>
```

Split the residual coefficient:

```text
<mu_N,h_a> = P_h(N) - D_h(N)
```

and test:

```text
aligned(N) + P_h(N) > D_h(N).
```

## Receipt

```text
tools/build_q286_orthogonal_residual_sign_split_budget_audit.py
evidence/q286-orthogonal-residual-sign-split-budget-audit.json
```

## Result

On the seven frozen signed-pair operator targets:

```text
actual full-positive rows:                       5 / 7
actual full-nonpositive rows:                    2 / 7
rows needing sub-1% symmetric residual control:  1
rows needing sub-5% symmetric residual control:  1
maximum reconstruction error:       4.440892098500626e-16
```

The tight row is again target `94856`:

```text
aligned-only full action:       0.1140460717392141
positive residual contribution: 0.6184971760641977
negative residual drag:         0.7199667815096121
actual full action:             0.012576466293799767
aligned+positive / negative:    1.017468120219977
symmetric residual budget:      0.009396193466872777
```

The budget formula differs from the raw sign split because the aligned term is
held exact:

```text
eps < full_actual / (P_h + D_h).
```

For comparison, the raw full-coefficient sign split had tight symmetric
budget:

```text
0.007201983503733535
```

## Decision

The orthogonal-residual sign split is a better-shaped theorem object than raw
full-coefficient landing, but it is still near-sharp.  Treating the aligned
component as exact relaxes the tight row from `0.007201983503733535` to
`0.009396193466872777`, but that remains sub-percent source control.

So this is not an escape hatch.  The live proof object is a coefficient-specific
signed lower-tail estimate for:

```text
<nu_N,h_a>
```

not broad AP counts, lower-dimensional projection uniformity, global norm
control, or raw residual sign landing.

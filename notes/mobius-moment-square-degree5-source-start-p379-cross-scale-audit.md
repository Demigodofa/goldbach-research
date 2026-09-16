# Mobius moment-square degree-5 source-start p=379 cross-scale audit

## Question

The full fresh-scale sweeps for `M=229` and `M=251` both had their weakest
row at prime `p=379`, component `(00,12)`.  Is `p=379` a repeatable
source-start stress point across nearby scales, or was that a two-scale
coincidence?

## Mechanism

Fix `p=379` and vary `M` across nearby scales for which `p` lies in the
checked prime interval:

```text
M <= 379 <= 2M
```

The audited scales are:

```text
191, 211, 227, 229, 251, 293, 331, 353, 379
```

For each scale, use the original source-start construction:

```text
row_count = int((M**(1/.59))**.41)
ell_freeze = row_count + row_count//2
canonical source start = row_count
```

Then compute the three degree-5 component rows and the degree-5 total row,
testing:

```text
full < 0 and active/full > 1/2
```

## Receipt

```text
tools/build_mobius_moment_square_degree5_source_start_p379_cross_scale_audit.py
evidence/mobius-moment-square-degree5-source-start-p379-cross-scale-audit.json
```

## Result

```text
fixed prime:                       379
scales:                            9
component rows:                    27
degree-5 total rows:               9
dominance rows:                    36
all rows pass signed dominance:    true
minimum slack above one half:      0.40189096624031384
weakest row:                       M=229, p=379, (00,12)
weakest active/full ratio:         0.9018909662403138
maximum slack above one half:      0.49786098870080275
```

Weakest rows by scale:

```text
M=191  original checked   (00,12)  ratio 0.9522968110742764  slack 0.45229681107427644
M=211  original checked   (00,12)  ratio 0.9281670155961498  slack 0.4281670155961498
M=227  original checked   (00,12)  ratio 0.9522114597586332  slack 0.4522114597586332
M=229  fresh full sweep   (00,12)  ratio 0.9018909662403138  slack 0.40189096624031384
M=251  fresh full sweep   (00,12)  ratio 0.934353336374303   slack 0.43435333637430296
M=293  fresh unswept      (00,12)  ratio 0.9715916000491919  slack 0.4715916000491919
M=331  fresh unswept      (00,12)  ratio 0.975572904946616   slack 0.47557290494661597
M=353  fresh unswept      (01,02)  ratio 0.997583046646055   slack 0.497583046646055
M=379  fresh unswept      (01,02)  ratio 0.9785537211809753  slack 0.4785537211809753
```

## Decision

The `p=379` cross-scale stress audit survives with all rows positive.  It
does support treating `p=379` as a concrete attention point near the lower
fresh source-start scales: the weakest component is `(00,12)` from `M=191`
through `M=331`, and the global weakest remains `M=229`, `p=379`.

It also limits the story.  At `M=353` and `M=379`, the weakest component
switches to `(01,02)`, and the slack is substantially larger.  So `p=379` is
finite stress evidence, not a universal stress theorem or a magic-prime rule.

The next evidence-bearing move is to decide whether the `M=293` full sweep
also survives and whether its weakest row is near the `p=379` channel.

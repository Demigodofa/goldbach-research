# q286-WBSS Bauer-Wang source-fit audit

## Question

The raw pointwise source scout left Bauer-Wang 2013 as a relevant source to
inspect.  Does it provide the exact raw pointwise theorem needed to reactivate
the q286 signed-weight proof engine?

## Receipt

```text
tools/build_q286_wbss_bauer_wang_source_fit_audit.py
evidence/q286-wbss-bauer-wang-source-fit-audit.json
```

## Source Boundary

This audit uses the PLDML/ICM metadata and abstract-level theorem shape for
Bauer-Wang, DOI `10.4064/aa159-3-2`.  It is not a full-paper theorem
extraction.

## Result

```text
status: SOURCE_FIT_Bauer_Wang_not_q286_raw_pointwise_bridge
fit to q286 raw pointwise trigger: insufficient
reactivates q286 signed-weight lane: false
external pointwise bridge found: false
```

The available source metadata describes an almost-all theorem over prime
moduli, residue classes, and eligible targets.  That is useful AP-Goldbach
context, but it is not the same as a no-exception raw lower bound for the exact
signed q286 weighted convolution.

## Mismatch

The q286 bridge requires:

```text
target quantifier: every sufficiently large covered even N
modulus: exact fixed q286 finite-modulus package
weight: exact signed q286 left-prime coefficient
scale: raw unnormalized log-prime pair sum
interval: strict central range N/3 < p < 2N/3
finite remainder: explicit N0 plus finite verification below N0
```

Bauer-Wang, as available at the metadata/abstract level, has almost-all target
quantifiers and AP-positive representation structure.  The direct q286 wake-up
therefore fails on the quantifier and object mismatch.

## Decision

`SOURCE_FIT_Bauer_Wang_not_q286_raw_pointwise_bridge`.

Bauer-Wang closes as a direct q286 wake-up source.  Future use would require a
new derivation that supplies the missing every-`N`, exact-q286, signed-weighted,
strict-central, raw-scale, finite-remainder bridge explicitly.

The next evidence-bearing move is no longer another named AP-Goldbach source
fit for q286.  Either derive the raw active-character theorem target from
scratch, or switch to a different proof engine whose first obligation is not
already Goldbach-strength pointwise positivity.

This is source-fit HOLD only.  No Bauer-Wang theorem is promoted to a q286
bridge, no raw weighted witness theorem, no positive-mass theorem, no q286
threshold theorem, no strict-central Goldbach theorem, and no Goldbach proof is
established.

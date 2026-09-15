# q286 Selected-Stress Subclass Channel Decomposition

Status: finite channel-decomposition audit only.  This is not a selected-stress
theorem, signed prime-correlation theorem, pointwise character-sum theorem, or
Goldbach proof.

Receipt:

```text
tools/build_q286_selected_stress_subclass_channel_decomposition.py
evidence/q286-selected-stress-subclass-channel-decomposition.json
```

## Question

Kevin asked whether `(3,1)` may be a stress-classifier lemma, especially after
the large negative selected reference `13822`.  The previous audit showed that
selected stress splits into two finite subclasses:

```text
volatile_overturn:    13822, 164598, 1222142
stable_core_deficit:  24424, 55864
```

This receipt decomposes fresh-unseen selected-reference margins across all 17
outside channels after subtracting the full target-reference local q286 vector.
It also reports seed-residue and nonseed fresh-unseen scopes separately so the
special zero-local seed discussion is not mixed into the broader fresh-window
holdout.

## Result

Scalar `(3,1)` survives as a finite selected-stress classifier coordinate:

```text
stable_core_deficit:  0 failures / 1212, min 0.010958653794
volatile_overturn:   0 failures / 1818, min 0.003510955559
```

Removing `(3,1)` from Kevin's four-channel watchlist makes both subclasses
fail:

```text
stable_core_deficit:  62 failures, min -0.018376824958
volatile_overturn:    5 failures, min -0.008154792326
```

So `(3,1)` is load-bearing for the checked watchlist.  It is not the whole
story: stable-core-deficit has four passing singleton channels, with `(4,6)`
giving the largest singleton minimum, while volatile-overturn has two passing
singletons, `(3,1)` and `(3,11)`.

## Seed And Nonseed Scope

The 12 zero-local seed targets belong to the earlier same-window population.
The later fresh-unseen windows used here contain:

```text
prior seed residues 38/64: 5 targets, all residue 64
residue 38:                0 targets
residue 64:                5 targets
nonseed fresh-unseen:      601 targets
```

On the 601 nonseed targets, scalar `(3,1)` is the only passing singleton and
Kevin's watchlist without `(3,1)` fails:

```text
scalar (3,1):                       0 failures / 3005, min  0.003510955559
watchlist:                          0 failures / 3005, min  0.002034556533
watchlist without (3,1):           67 failures,        min -0.018376824958
frozen full 17 LP:                606 failures,        min -0.143214427823
```

The fresh-unseen prior-seed-residue scope is too small and contains no residue
38 rows, so it must not be treated as the 12-row zero-local seed audit.

## Interpretation

The best finite statement is:

> `(3,1)` is a passing and load-bearing scalar coordinate for the selected
> q286 stress-reference fixture, including both stable-core-deficit and
> volatile-overturn subclasses, on the checked fresh-unseen windows.

The theorem route is still open.  A proof must explain the signed
empirical/correlation-side gap that keeps `(3,1)` positive after local
subtraction, and it must keep the selected-reference fixture separate from the
already-falsified broad `full_nonpositive` stress class.

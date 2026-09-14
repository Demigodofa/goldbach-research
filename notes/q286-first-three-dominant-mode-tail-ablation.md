# q286 dominant-mode tail ablation

Status: finite tail-ablation diagnostic.  Goldbach is not proved.

This note tests whether the seven-channel classification tail from the
prefix/tail split can be compressed on the selected q286 fixture.

Receipt:
`evidence/q286-first-three-dominant-mode-tail-ablation.json`

## Mechanism Tested

The prefix/tail split left:

```text
prefix = (2,6), (3,1), (4,8), (4,2)
tail   = (3,11), (5,5), (4,4), (1,3), (5,3), (2,4), (4,6)
```

The prefix keeps every selected clear row passing but over-rescues every
selected deficit.  The tail restores the selected deficit classification while
preserving clears.  This receipt asks whether a proper subtail can do the same
job.

## Measured Shape

Leave-one-out ablation:

- removing any one of the `7` tail channels loses the selected tail
  classification;
- every tail channel is essential for restoring all selected over-rescued
  failures;
- channels `(5,5)` and `(5,3)` are also essential for preserving all selected
  clear rows under leave-one-out.

The first tail prefix that restores all selected failures and preserves all
selected clears is the full seven-channel tail:

```text
(3,11), (5,5), (4,4), (1,3), (5,3), (2,4), (4,6)
```

The full-tail slack summaries are:

```text
failure tail slack: minimum -0.0992285758, maximum -0.0088331796
clear tail slack:   minimum +0.0095640903, maximum +0.0584289263
```

Thus the selected fixture has a positive margin gap, but it is not carried by
a single tail channel or a proper prefix tail.

## Consequence

The classification-tail theorem is not visibly compressible by the tested
prefix or leave-one-out routes.  The live q286 theorem target is therefore:

```text
prove the four-channel prefix lower bound for rows that should clear,
and prove the full seven-channel tail classification package,
or replace the tail package by a separate deficit exclusion,
complement/lower-support, or fixed-modulus prime-pair theorem.
```

This is finite selected-fixture evidence only.  It is not a uniform theorem
and not a proof of Goldbach.

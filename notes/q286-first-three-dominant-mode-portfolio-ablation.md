# q286 dominant-mode recurrent portfolio ablation

Status: finite ablation diagnostic.  Goldbach is not proved.

This note tests whether the fixed recurrent helpful-channel portfolio can be
compressed after the residual-channel profile demoted a small residual rescue.

Receipt:
`evidence/q286-first-three-dominant-mode-portfolio-ablation.json`

## Mechanism Tested

The previous split fixed the `11` recurrent helpful channels and left a
`14`-channel residual.  This ablation asks two different questions:

```text
1. Can a smaller prefix still keep every selected clear row above the floor?
2. Can a smaller prefix reproduce the full selected pass/fail classification?
```

Those are different theorem targets.  The first is a lower-bound target.  The
second is a classification target.

## Measured Shape

On the selected ten-row fixture, the full `11`-channel portfolio has passing
targets

```text
13556, 40420, 129706, 1242118, 1240888
```

and failing targets

```text
24424, 13822, 55864, 164598, 1222142
```

Leave-one-out results:

- removing any one channel changes the selected pass/fail classification;
- removing one of `5` channels also makes at least one selected clear row fail.

The channels essential for keeping all selected clears passing are:

```text
(2,6), (3,1), (4,8), (5,5), (5,3)
```

The channels essential for reproducing the full selected classification are
all `11` recurrent channels:

```text
(2,6), (3,1), (4,8), (4,2), (3,11), (5,5),
(4,4), (1,3), (5,3), (2,4), (4,6)
```

The first prefix that keeps every selected clear row passing has only `4`
channels:

```text
(2,6), (3,1), (4,8), (4,2)
```

but it over-rescues every selected failing row as well.  Its pass set is all
ten selected targets.  The first prefix reproducing the full selected
classification is therefore the full `11`-channel portfolio.

## Consequence

This splits the next theorem target cleanly:

```text
lower-bound theorem:
  a smaller positive portfolio package may be enough to keep clear-side rows
  above the residual requirement;

classification theorem:
  reproducing the selected deficit/clear split is not compressed by the
  tested prefix or leave-one-out ablations.
```

So the likely theorem route is not "find a tiny exact classifier."  It is
closer to:

```text
prove a recurrent-portfolio lower bound on rows that actually need rescue,
then handle over-rescued finite/deficit rows by a separate exclusion,
boundary, or complement/lower-support mechanism.
```

This is finite theorem-shaping evidence only.

# q286 Dominant-Mode Stable-Core Rectangle Falsifier

Status: finite derivative falsifier only.  This is not a stable-core theorem,
volatile-rim theorem, one-parameter budget theorem, pointwise character-sum
estimate, or Goldbach proof.

## Mechanism

The stable-core named holdout kept the coupled stable-core / volatile-rim
budget alive on the six named clear rows.  This derivative diagnostic checks
whether that coupled budget can be simplified to one independent allowance
`A`:

```text
stable-core margin >= A
volatile drag       <= A
```

Such an allowance would make a row-independent rectangle budget sufficient:
stable surplus would always cover the volatile drag.

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_stable_core_rectangle_falsifier.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-stable-core-rectangle-falsifier.json`
- Source evidence:
  `evidence/q286-first-three-dominant-mode-stable-core-named-holdout.json`
- Reference tail:
  `1222142`

## Result

No one-parameter rectangle allowance exists on the named fixture:

```text
minimum stable-core margin: 0.0309910090793198  at target 1242118
maximum volatile drag:     0.0795878214771284  at target 1240888
obstruction gap:           0.0485968123978086
```

The obstruction is exactly:

```text
max volatile drag > min stable-core margin
```

The coupled rowwise budget still passes all six named clear rows.  Target
`1240888` has a larger volatile drag than `1242118`, but it also has a much
larger stable-core margin.  Therefore the surviving route is not an
independent uniform surplus floor plus an independent uniform rim cap with
the same allowance.

## Interpretation

This closes a tempting simplification.  A proof must control volatile drag as
a function of the row's available stable-core margin, split pressure
subregions, use a richer arithmetic partition, or replace this route with a
lower-support/complement rescue.  The diagnostic is finite and derivative; it
does not prove the coupled inequality outside the named fixture.

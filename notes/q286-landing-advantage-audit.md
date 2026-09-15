# q286 landing advantage audit

Status: finite landing-advantage diagnostic.  This is not a signed
prime-correlation theorem, q286 threshold theorem, strict-central Goldbach
theorem, or proof of Goldbach.

## Question

The coefficientwise minorant audit showed that arbitrary nonnegative residue
mass is too broad: every even admissible support has negative coefficient
cells.  The surviving theorem must therefore say something about where the
actual strict-central prime-pair mass lands.

This audit measures the landing inequality

```text
sum_r W_N(r)c_+(r) > sum_r W_N(r)c_-(r)
```

for the full q286 coefficient and for the partial coefficient
`P+D = P+E_286+E_154+E_70`.  It also measures the support-tail drag condition

```text
tail_negative_drag < partial_margin + tail_positive_mass.
```

## Fixture

`tools/build_q286_landing_advantage_audit.py` generated
`evidence/q286-landing-advantage-audit.json`.

The fixture combines:

```text
known extremals:            113 targets
checked positive suffix:    90080..250238   (80080 even targets)
fresh arithmetic cycle:     250240..260248  (5005 even targets)
```

The landing reconstruction was validated against the prior direct 10-row
support-action decomposition:

```text
maximum partial delta:  8.326672684688674e-16
maximum tail delta:     1.6167622796103842e-15
maximum full delta:     1.1102230246251565e-15
```

## Result

Across all `85198` targets:

```text
partial positive count:       85125
full positive count:          85109
tail sign-change count:       16
negative-tail kill count:     16
positive-tail rescue count:   0
```

All `16` sign changes are the known early negative-tail kills.  The later
windows have none.

Known extremals:

```text
partial positive/negative landing ratio min:  0.5083126470752375
full positive/negative landing ratio min:     0.5259440169653298
tail-control margin min:                      -5141.381971899495
```

Checked positive suffix:

```text
partial positive/negative landing ratio min:  1.0808406831195534
full positive/negative landing ratio min:     1.0097513835500775
tail-control margin min:                      490.7620118705163
```

Fresh next arithmetic cycle:

```text
partial positive/negative landing ratio min:  1.239985148023538
full positive/negative landing ratio min:     1.1701947485425508
tail-control margin min:                      24462.756459696568
```

## Interpretation

This is the first finite audit stated directly in the surviving language:
actual prime-pair mass must land on positive coefficient cells with enough
weighted advantage to beat negative-cell drag.  The later windows support that
shape; the known extremals record the boundary failures.

The theorem target is now:

```text
For actual W_N, not arbitrary nonnegative W:
positive landing contribution > negative landing drag
```

for the full coefficient, plus the tail sub-inequality

```text
tail_negative_drag < partial_margin + tail_positive_mass.
```

This is still a signed binary-prime distribution theorem.  It is not supplied
by the q286 coefficient geometry alone.

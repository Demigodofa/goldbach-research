# q286 support-tail stability window audit

Status: finite support-tail stability diagnostic.  This is not a signed
tail-control theorem, q286 threshold theorem, strict-central Goldbach theorem,
or proof of Goldbach.

## Question

The signed support-tail control definition isolates

```text
A_N/P_N = 1 + d_N + r_N,
```

where `d_N` is the dominant support action from `286`, `154`, and `70`, and
`r_N` is the support tail from `14`, `26`, `130`, `10`, and `22`.

The known-extremals audit showed `16` early negative-tail kills.  This audit
asks whether that failure mode recurs after the last observed raw q286 failure.

## Fixture

`tools/build_q286_support_tail_stability_window_audit.py` generated
`evidence/q286-support-tail-stability-window-audit.json`.

The predeclared windows are:

```text
checked positive suffix:      90080..250238   (80080 even targets)
fresh next arithmetic cycle:  250240..260248  (5005 even targets)
```

The optimized support split was validated against the prior direct 10-row
support-action decomposition:

```text
validation targets:          10
maximum dominant delta:      6.661338147750939e-16
maximum tail delta:          2.220446049250313e-16
maximum full delta:          1.5543122344752192e-15
```

## Result

Across all `85085` tested targets:

```text
full-action nonpositive count:                 0
principal+dominant nonpositive count:          0
tail sign-change count:                        0
negative-tail kill count:                      0
positive-tail rescue count:                    0
maximum reconstruction error:                  4.440892098500626e-16
```

The checked positive suffix has minimum values:

```text
principal+dominant ratio:  0.11074647386141123
support-tail ratio:       -0.1682566032688563
full-action ratio:         0.012576466293799578
```

The fresh next arithmetic cycle has minimum values:

```text
principal+dominant ratio:  0.3385537853460162
support-tail ratio:       -0.15556187569707194
full-action ratio:         0.23608103140993492
```

The tail still erodes many positive partial margins (`37537` in the checked
suffix and `2389` in the fresh cycle), but it does not erase any margin in
these later windows.

## Interpretation

This supports a finite tail-stability candidate after the last observed raw
failure: negative-tail kills appear in the early known-extremal fixture but do
not recur in the checked later suffix or in the next fresh arithmetic cycle.

The result does not prove a threshold theorem.  It only justifies the next
theorem shape:

```text
boundary/early:  finite verification or special signed-tail control;
later:           prove 1+d_N stays positive and r_N cannot erase it.
```

The next falsifier is straightforward: freeze a larger later holdout before
scanning.  Any recurrent negative-tail kill in a predeclared later window
refutes the clean tail-stable threshold story.

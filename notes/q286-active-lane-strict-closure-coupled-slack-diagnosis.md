# q286 active-lane strict-closure coupled-slack diagnosis

## Question

The post-discovery stress audit falsified the selected-late strict-closure
endpoint as a universal active-lane certificate.  What exactly failed: the
driver floor, the channel bound, or only the coupled slack?

## Receipt

```text
tools/build_q286_active_lane_strict_closure_coupled_slack_diagnosis.py
evidence/q286-active-lane-strict-closure-coupled-slack-diagnosis.json
```

## Result

On the `11` post-discovery stress rows:

```text
driver floor condition met:       0 / 11
channel Linf condition met:       8 / 11
coupled strict slack positive:    5 / 11
channel pass but coupled fail:    3 / 11
first channel-bound pass target:  383486
first coupled-slack pass target:  594112
```

The driver floor fails on every stress row, including the five rows where the
combined strict margin is positive.  The pass/fail transition is explained by
whether the channel surplus pays the driver deficit:

```text
target  block  payment ratio  strict margin
94856   1     -0.5237785392  -1.1917268782
194384  2     -0.7285169833  -0.8293645486
255704  3     -0.3135037394  -0.6774660244
383486  4      0.3815528057  -0.2897194486
480614  5      0.2617464200  -0.3757038900
548666  6      0.7219634560  -0.1399657777
594112  7      1.0360157107   0.0145335221
658598  8      1.8768083810   0.2378587945
805682  9      3.1674374837   0.3183458979
846632  10     3.4767626680   0.3628943482
955832  11     1.9118441197   0.1327432031
```

## Decision

The selected-late route should not try to prove the frozen driver floor as an
independent theorem.  That condition is already falsified on the stress set.
The surviving theorem-shaped target is coupled:

```text
driver_margin(N) + L * channel_margin(N) > 0
```

or, better, a direct unnormalized pointwise signed estimate.  This lines up
with the q286-WBSS lesson that fixed separate component suprema are the wrong
object; the proof pressure belongs on aggregate adverse drag below local main
or an equivalent coupled signed-correlation inequality.

## Boundary

Finite coupled-slack diagnosis only.  No universal active-lane theorem,
pointwise adverse-drag theorem, q286 threshold theorem, strict-central
Goldbach theorem, or Goldbach proof is established.

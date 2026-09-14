# q286 Dominant-Mode Pressure/Offset Scalar Falsifier

Status: finite named-row scalar-separator falsifier only.  This is not a
scalar offset theorem, scalar ratio theorem, coupled pressure/offset curve
theorem, pointwise character-sum estimate, or Goldbach proof.

## Mechanism

After the negative-pressure bulk-share diagnostic demoted tiny top-k pressure
control, the next tempting simplification was to certify the positive rescue
side by one scalar:

- a uniform positive-offset floor `P >= c`; or
- a uniform positive/negative pressure ratio floor `R = P/B >= c`.

Here `B` is the dominant-mode negative real-channel pressure and `P` is the
dominant-mode positive real-channel offset.  The exact floor condition remains:

```text
P >= B - 0.3
```

or, for `B > 0`,

```text
R >= 1 - 0.3/B.
```

## Receipt

- Builder:
  `tools/build_q286_first_three_dominant_mode_pressure_offset_scalar_falsifier.py`
- Evidence:
  `evidence/q286-first-three-dominant-mode-pressure-offset-scalar-falsifier.json`
- Source receipt:
  `q286_first_three_dominant_mode_signed_channel_profile_receipt`
- Named rows:
  `1222142`, `1242118`, `1240888`, `1243018`, `1243130`, `1244072`,
  `1244094`

## Falsifiers

The named fixture has `4` positive-offset floor counterexamples.  The most
important one is the high-pressure clear row `1242118`:

```text
tail 1222142:
  B = 0.37196700245556
  P = 0.06313382289502988
  R = 0.16972963321544268
  exact curve margin = -0.02374721279634337
  slack = -0.00883317956053016

clear 1242118:
  B = 0.34343932670896016
  P = 0.05996824017570475
  R = 0.17461087159224334
  exact curve margin = 0.048127608521523896
  slack = 0.01652891346674458
```

The failing row has more positive offset than this clear row.  Therefore a
uniform offset floor strong enough to certify `1242118` would also certify
the tail `1222142`.

There is also `1` global ratio-floor counterexample: tail `1222142` has ratio
`0.16972963321544268`, while clear pressure-branch row `1240888` has ratio
`0.047855301498350294`.  Therefore one global ratio floor cannot be used as a
clear-row separator across the named fixture.

The exact pressure/offset curve has no named-row mismatch.  That is algebraic,
not a theorem: it restates the floor condition.

## Interpretation

This finite diagnostic demotes scalar positive-offset floors and global scalar
ratio floors as theorem mechanisms on the named rows.  It also shows why the
pressure-only branch remains strict: pressure above `0.3` is not failure by
itself, because `1242118` has `B > 0.3` and still clears.

The surviving scalar theorem target is coupled pressure/offset control:

```text
P >= B - 0.3
```

or an arithmetic estimate that implies this curve.  Any future simpler scalar
candidate needs a changed condition, such as a pressure subregion, target
class, lower-support rescue, or another independently defined partition.

# q286 dominant-mode residual channel profile

Status: finite residual-channel diagnostic.  Goldbach is not proved.

This note looks inside the nonportfolio residual left after the recurrent
helpful-channel portfolio is bolted onto the selected q286 dominant rows.

Receipt:
`evidence/q286-first-three-dominant-mode-residual-channel-profile.json`

## Mechanism Tested

After the recurrent helpful portfolio is fixed, the complementary `14` real
channels might have formed a smaller repeated obstruction or a clean
clear-versus-deficit classifier.  This receipt tests that possibility on the
same selected six deficit-to-clear pairs.

The active split is:

```text
25 real dominant channels
= 11 recurrent helpful portfolio channels
+ 14 residual channels.
```

For each target, the residual is also split as

```text
residual_sum = residual_positive_offset - residual_negative_pressure.
```

## Measured Shape

The maximum residual signed-balance identity error is about `1.11e-16`.

Across the selected rows:

- residual negative pressure ranges from about `0.1624889491` to
  `0.7784656902`;
- residual positive offset ranges from about `0.0100232636` to
  `0.6006073306`;
- no individual residual channel separates selected clear rows from selected
  deficit rows.

The harshest residual pressure and harshest residual sum both occur at
target `13556`, which is a passing row:

```text
target 13556:
  residual_sum               = -0.48297017290081456
  residual_negative_pressure = 0.7784656901830459
  residual_positive_offset   = 0.2954955172822313
```

The largest residual positive offset occurs at target `13822`, which is a
failing row:

```text
target 13822:
  residual_sum               = -0.011309233322353403
  residual_negative_pressure = 0.6119165638867794
  residual_positive_offset   = 0.600607330564426
```

The largest residual channels by absolute selected contribution are:

```text
channel  abs selected contribution   clear_mean - failure_mean
(3,3)    0.5306198588               -0.0489646032
(3,5)    0.5153820340               +0.0205485975
(2,10)   0.4755914409               +0.0354752208
(1,11)   0.4608517328               -0.0263793265
(1,7)    0.4556145099               -0.0234599135
(5,1)    0.4454415094               -0.0550704186
```

For every selected deficit-to-clear pair, the residual delta is negative:

```text
(24424,13556):     -0.5407412596
(13822,40420):     -0.2510131904
(55864,40420):     -0.1938102546
(164598,129706):   -0.1426643073
(1222142,1242118): -0.1084846894
(1222142,1240888): -0.0743618794
```

Thus the residual does not supply the observed rescue on these pairs.  It
pushes against the clear side, and the recurrent portfolio must overcome it.

## Consequence

This falsifies a tempting small residual-channel classifier on the selected
fixture.  The next theorem target is not:

```text
prove one residual channel, or a trivially signed residual tail, separates
clear rows from deficits.
```

The sharper target remains:

```text
prove a recurrent-portfolio lower bound strong enough to overcome the
rowwise residual requirement,
```

or prove a genuine residual-channel theorem from fixed-modulus prime-pair
arithmetic.  In particular, target `13556` is the warning row: any proof must
allow a large adverse residual on a row that still clears because the
portfolio is sufficiently positive.

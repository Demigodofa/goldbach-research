# q286 zero-local channel margin audit

Status: finite LP-weighted channel-margin audit over the `12` zero-local
target integers.  This is not a proof of a distributed cone theorem, a
binary-prime correlation theorem, a signed projection theorem, or Goldbach.

## Source

The source decomposition is:

```text
evidence/q286-zero-local-target-channel-decomposition.json
```

The generated audit is:

```text
evidence/q286-zero-local-channel-margin-audit.json
```

The builder is:

```text
tools/build_q286_zero_local_channel_margin_audit.py
```

## Metric

For each target/channel entry, the weighted contribution is:

```text
lp_effective_weight * after_local_delta
```

The local vector has already been subtracted in the source decomposition.  A
fixed subset passes if the sum of selected weighted channel contributions is
positive for every target in the scope.

## All 12 targets

Total positive weighted margin: `1.971706133290348`.
Total negative weighted margin: `-0.09699556098007175`.
Total net LP margin: `1.8747105723102762`.

No single channel removal makes any of the `12` targets fail.  The smallest
fixed subset size is `1`; there are `12` one-channel subsets that keep all
`12` targets positive.

| channel | + | - | min | avg | max | +margin % | removal fail |
|---|---:|---:|---:|---:|---:|---:|---|
| (1,9) | 1 | 11 | -0.003583122 | -0.001407944 | 0.000187484 | 0.01 | no |
| (1,11) | 12 | 0 | 0.006299060 | 0.008199249 | 0.009525721 | 4.99 | no |
| (2,2) | 12 | 0 | 0.001481198 | 0.007050753 | 0.015298769 | 4.29 | no |
| (2,6) | 12 | 0 | 0.003590203 | 0.006079790 | 0.008489638 | 3.70 | no |
| (2,8) | 0 | 12 | -0.006386118 | -0.004702067 | -0.001537749 | 0.00 | no |
| (2,10) | 3 | 9 | -0.002607122 | -0.000801420 | 0.001400111 | 0.12 | no |
| (3,1) | 12 | 0 | 0.019293871 | 0.031510309 | 0.042904405 | 19.18 | no |
| (3,5) | 0 | 12 | -0.001240178 | -0.000902299 | -0.000246310 | 0.00 | no |
| (3,7) | 12 | 0 | 0.006841372 | 0.017182800 | 0.024242434 | 10.46 | no |
| (3,9) | 12 | 0 | 0.002804654 | 0.003463241 | 0.004049939 | 2.11 | no |
| (3,11) | 12 | 0 | 0.009853824 | 0.020351738 | 0.038450679 | 12.39 | no |
| (4,2) | 12 | 0 | 0.006502854 | 0.009241366 | 0.011958835 | 5.62 | no |
| (4,6) | 12 | 0 | 0.003690667 | 0.009766402 | 0.018115692 | 5.94 | no |
| (4,8) | 12 | 0 | 0.005356824 | 0.010445239 | 0.011921646 | 6.36 | no |
| (5,1) | 12 | 0 | 0.000788942 | 0.005614282 | 0.011573732 | 3.42 | no |
| (5,3) | 10 | 2 | -0.000400418 | 0.000909872 | 0.002929668 | 0.59 | no |
| (5,5) | 12 | 0 | 0.023851031 | 0.034224570 | 0.041746548 | 20.83 | no |

Best one-channel subsets by minimum target margin:

```text
(5,5):  min 0.023851031, avg 0.034224570, total 0.410694843
(3,1):  min 0.019293871, avg 0.031510309, total 0.378123706
(3,11): min 0.009853824, avg 0.020351738, total 0.244220858
(3,7):  min 0.006841372, avg 0.017182800, total 0.206193599
(4,2):  min 0.006502854, avg 0.009241366, total 0.110896388
```

## Residue 38

Total positive weighted margin: `0.9610117791496418`.
Total negative weighted margin: `-0.048069089180579554`.
Total net LP margin: `0.9129426899690621`.

No single channel removal makes any residue-`38` target fail.  The smallest
fixed subset size is `1`; there are `13` one-channel subsets that keep all
six residue-`38` targets positive.

| channel | + | - | min | avg | max | +margin % | removal fail |
|---|---:|---:|---:|---:|---:|---:|---|
| (1,9) | 1 | 5 | -0.003583122 | -0.001580349 | 0.000187484 | 0.02 | no |
| (1,11) | 6 | 0 | 0.006299060 | 0.007836699 | 0.009456427 | 4.89 | no |
| (2,2) | 6 | 0 | 0.001481198 | 0.006985024 | 0.015298769 | 4.36 | no |
| (2,6) | 6 | 0 | 0.004192268 | 0.006306233 | 0.008489638 | 3.94 | no |
| (2,8) | 0 | 6 | -0.006156375 | -0.004723128 | -0.001537749 | 0.00 | no |
| (2,10) | 2 | 4 | -0.002607122 | -0.000696265 | 0.001400111 | 0.15 | no |
| (3,1) | 6 | 0 | 0.027858045 | 0.032467137 | 0.042904405 | 20.27 | no |
| (3,5) | 0 | 6 | -0.001156333 | -0.000745974 | -0.000246310 | 0.00 | no |
| (3,7) | 6 | 0 | 0.006841372 | 0.017070200 | 0.024242434 | 10.66 | no |
| (3,9) | 6 | 0 | 0.002804654 | 0.003477021 | 0.003984896 | 2.17 | no |
| (3,11) | 6 | 0 | 0.009853824 | 0.016618109 | 0.024500867 | 10.38 | no |
| (4,2) | 6 | 0 | 0.006635736 | 0.009257696 | 0.011958835 | 5.78 | no |
| (4,6) | 6 | 0 | 0.003690667 | 0.009015976 | 0.014056260 | 5.63 | no |
| (4,8) | 6 | 0 | 0.005356824 | 0.010159174 | 0.011921646 | 6.34 | no |
| (5,1) | 6 | 0 | 0.003409910 | 0.007366238 | 0.011573732 | 4.60 | no |
| (5,3) | 6 | 0 | 0.000279761 | 0.001295968 | 0.002929668 | 0.81 | no |
| (5,5) | 6 | 0 | 0.023851031 | 0.032047355 | 0.037845832 | 20.01 | no |

Best one-channel subsets by minimum target margin:

```text
(3,1):  min 0.027858045, avg 0.032467137, total 0.194802825
(5,5):  min 0.023851031, avg 0.032047355, total 0.192284133
(3,11): min 0.009853824, avg 0.016618109, total 0.099708654
(3,7):  min 0.006841372, avg 0.017070200, total 0.102421200
(4,2):  min 0.006635736, avg 0.009257696, total 0.055546178
```

## Residue 64

Total positive weighted margin: `1.0106943541407063`.
Total negative weighted margin: `-0.0489264717994922`.
Total net LP margin: `0.961767882341214`.

No single channel removal makes any residue-`64` target fail.  The smallest
fixed subset size is `1`; there are `12` one-channel subsets that keep all
six residue-`64` targets positive.

| channel | + | - | min | avg | max | +margin % | removal fail |
|---|---:|---:|---:|---:|---:|---:|---|
| (1,9) | 0 | 6 | -0.002173141 | -0.001235539 | -0.000160135 | 0.00 | no |
| (1,11) | 6 | 0 | 0.007385718 | 0.008561799 | 0.009525721 | 5.08 | no |
| (2,2) | 6 | 0 | 0.002668235 | 0.007116483 | 0.010405369 | 4.22 | no |
| (2,6) | 6 | 0 | 0.003590203 | 0.005853347 | 0.007458610 | 3.47 | no |
| (2,8) | 0 | 6 | -0.006386118 | -0.004681007 | -0.003302671 | 0.00 | no |
| (2,10) | 1 | 5 | -0.002114686 | -0.000906575 | 0.000894661 | 0.09 | no |
| (3,1) | 6 | 0 | 0.019293871 | 0.030553480 | 0.037806958 | 18.14 | no |
| (3,5) | 0 | 6 | -0.001240178 | -0.001058624 | -0.000739660 | 0.00 | no |
| (3,7) | 6 | 0 | 0.012479149 | 0.017295400 | 0.024067177 | 10.27 | no |
| (3,9) | 6 | 0 | 0.002840072 | 0.003449460 | 0.004049939 | 2.05 | no |
| (3,11) | 6 | 0 | 0.018111764 | 0.024085367 | 0.038450679 | 14.30 | no |
| (4,2) | 6 | 0 | 0.006502854 | 0.009225035 | 0.010719125 | 5.48 | no |
| (4,6) | 6 | 0 | 0.004729648 | 0.010516829 | 0.018115692 | 6.24 | no |
| (4,8) | 6 | 0 | 0.009142485 | 0.010731304 | 0.011914390 | 6.37 | no |
| (5,1) | 6 | 0 | 0.000788942 | 0.003862327 | 0.006018830 | 2.29 | no |
| (5,3) | 4 | 2 | -0.000400418 | 0.000523775 | 0.001979602 | 0.38 | no |
| (5,5) | 6 | 0 | 0.029123128 | 0.036401785 | 0.041746548 | 21.61 | no |

Best one-channel subsets by minimum target margin:

```text
(5,5):  min 0.029123128, avg 0.036401785, total 0.218410711
(3,1):  min 0.019293871, avg 0.030553480, total 0.183320881
(3,11): min 0.018111764, avg 0.024085367, total 0.144512205
(3,7):  min 0.012479149, avg 0.017295400, total 0.103772399
(4,8):  min 0.009142485, avg 0.010731304, total 0.064387826
```

## Interpretation

The zero-local rows still require a non-local/correlation bridge because the
local contribution has already been subtracted and is numerical zero.  However,
the smallest-subset test does not support the stronger statement that the LP
positivity requires a distributed fixed channel subset: `(5,5)` alone keeps
all `12` targets positive, and several other single channels do too.

This narrows the theorem target.  The next bridge should not be phrased as
"no small subset can explain the LP margin" for these `12` rows.  A more
accurate target is to explain why several channels have stable positive
LP-weighted sign across both zero-local residues, while the local singular
layer is zero and the raw AP marginal/pigeonhole route is too weak.

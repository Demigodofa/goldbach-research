# q286 dominant-mode portfolio/residual obligation

Status: finite exact decomposition.  Goldbach is not proved.

This note records the "bolt it on and ask what is left" version of the q286
dominant-mode route.  The recurrent helpful-channel portfolio from the swing
pair autopsy is fixed in place, then the remaining real channels are measured
as an explicit residual.

Receipt:
`evidence/q286-first-three-dominant-mode-portfolio-residual-obligation.json`

## Exact Split

For each selected row, the receipt records the identity

```text
dominant_sum = recurrent_portfolio_sum + nonportfolio_residual_sum
```

and rewrites the `-.3` dominant floor as the equivalent rowwise obligation

```text
recurrent_portfolio_sum >= -0.3 - nonportfolio_residual_sum.
```

The recurrent portfolio has `11` real channels:

```text
(2,6), (3,1), (4,8), (4,2), (3,11), (5,5),
(4,4), (1,3), (5,3), (2,4), (4,6)
```

The residual has the remaining `14` real channels.  On the selected ten-row
fixture, the maximum row identity error is `0`, and the maximum floor-identity
error is about `2.78e-17`.

## What Is Left

The exact row split is:

```text
target   portfolio        residual         required_portfolio   slack
24424   -0.3712297594    +0.0577710867    -0.3577710867       -0.0134586727
13556   +0.1925342632    -0.4829701729    +0.1829701729       +0.0095640903
13822   -0.3254351127    -0.0113092333    -0.2886907667       -0.0367443460
40420   +0.0112608272    -0.2623224237    -0.0376775763       +0.0489384035
55864   -0.3307164067    -0.0685121691    -0.2314878309       -0.0992285758
164598  -0.1072363369    -0.2119154555    -0.0880845445       -0.0191517925
129706  +0.1130086892    -0.3545797629    +0.0545797629       +0.0584289263
1222142 -0.1969321863    -0.1119009932    -0.1880990068       -0.0088331796
1242118 -0.0630854039    -0.2203856826    -0.0796143174       +0.0165289135
1240888 -0.0865505541    -0.1862628726    -0.1137371274       +0.0271865734
```

Here `slack = portfolio_sum - required_portfolio`, so the slack is exactly the
dominant-floor slack.  The sampled failing targets are:

```text
24424, 13822, 55864, 164598, 1222142
```

The sampled passing targets are:

```text
13556, 40420, 129706, 1242118, 1240888
```

The worst miss is target `55864`, where the recurrent portfolio falls short
by about `0.0992285758`.  The tightest clear is target `13556`, where the
residual is most negative and forces the largest required portfolio value,
about `0.1829701729`; the actual recurrent portfolio clears it by only about
`0.0095640903`.

## Consequence

The next theorem target is now sharper:

```text
prove a lower bound for the recurrent helpful portfolio against the rowwise
residual requirement -0.3 - nonportfolio_residual_sum,
```

or prove a residual-channel theorem that keeps the required portfolio inside a
range already forced by arithmetic structure.

This does not prove the recurrent portfolio theorem, does not prove a residual
bound, and does not prove Goldbach.  It only replaces a vague
positive-offset-under-pressure picture with an exact portfolio/residual
obligation on the selected q286 fixture.

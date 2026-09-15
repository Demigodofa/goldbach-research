# q286-WBSS known-theorem adequacy audit

## Question

The q286-WBSS coefficient-discrepancy HOLD names an exact analytic payment
request.  Do the standard source-backed theorem shapes currently on the table
pay it?

## Active budget

The active sufficient target remains:

```text
max(0, -E_d(N)) <= B_d(N) for each d
sum_d max(0, B_d(N)) < local_main(N)
```

or the stronger per-residue condition:

```text
|Delta_{d,s}(N)| <= eta_d(N)
sum_d L1_d * eta_d(N) < local_main(N)
```

with the current exact budget:

```text
minimum local main: 0.6039353780830684
total L1:           372.962002076135
equal eta cap:        0.0016192946592982506
```

## Source adequacy

The checked public-source theorem shapes do not pay this budget:

```text
BMOR explicit AP prime counts:
  one-dimensional prime counts in p mod q; no binary partner correlation.

Bhowmik-Halupczok-Matsumoto-Suzuki:
  average Goldbach-in-progressions information; not every target N.

Salmensuu:
  almost-all moduli/residue/target coverage; not every sufficiently large N.

Lichtman:
  level-of-distribution and upper-bound improvements; not a positive
  pointwise one-sided lower discrepancy estimate.
```

Primary/public locators:

```text
https://arxiv.org/abs/1802.00085
https://arxiv.org/abs/1704.06103
https://arxiv.org/abs/2106.00778
https://arxiv.org/abs/2309.08522
```

## Decision

Status:

```text
HOLD_external_known_theorems_do_not_pay_budget
```

The current source-backed theorem shapes do not supply the q286-WBSS
pointwise adverse-drag estimate.  Full pointwise fixed-modulus AP asymptotics
would imply the needed budget, but that is already a binary
Goldbach-in-progressions-strength input rather than a small local q286 lemma.

## Next non-finite route

Candidate: signed-character budget instead of full AP uniformity.

Mechanism: decompose the four q286-WBSS coefficient projections into
Dirichlet-character or finite Fourier modes and attempt to bound only the
adverse signed combination, not every residue-pair channel separately.

Prediction: if the coefficient family is spectrally concentrated or has
cancellations invisible to per-residue L1, the one-sided signed estimate may
be narrower than full pointwise AP Goldbach.

Falsifier: if the adverse WBSS coefficient family spreads substantial weight
across many nonprincipal character channels, each requiring an individual
pointwise binary-prime asymptotic, this route collapses back to the known
Goldbach-strength input.

Smallest test: build a character-mode burden audit for the four WBSS projected
coefficient families and measure whether the adverse budget is concentrated
in few modes or spread across many hard channels.

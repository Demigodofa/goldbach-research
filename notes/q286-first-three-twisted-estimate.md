# q286 first-three twisted estimate target

Status: theorem-shaped target, not proved.

Date: 2026-09-12.

## Context

The strict-central assembled coefficient on `U_10010` has been reduced to a
positive principal contribution plus exact lower-modulus support channels.  In
the dominant `q286 = 2*11*13` support, the centered component is split into a
local lower-modulus prediction, six separable singular modes, and a small
measured tail.

Finite diagnostics show that the first three q286 singular modes are the
active lower-tail core on the first complete residue period:

- On `10000..20008`, all `75` negative full-action targets have negative
  first-three q286 mode sum.
- Removing modes `1`, `2`, and `3` leaves no nonpositive full-action target
  in that period.
- The worst remaining full-action ratio after removing those modes is
  `0.018073313793834367` principal, at `N=14138`.
- Removing only modes `1` and `2` leaves one target, `N=14138`, still negative
  by `0.007038026892741689` principal.

This makes modes `1..3` the present proof target.  The claim is finite
evidence only.

## Exact finite object

For each leading mode `j`, the q286 coefficient is separable:

```text
C_j(r) = sigma_j A_j(r mod 11) B_j(r mod 13)
```

where `A_j` and `B_j` are finite mixtures of nonprincipal multiplicative
characters.  For a strict-central even target `N`, the mode contribution is

```text
T_j(N) =
  sum_{N/3 < p < 2N/3, p and N-p prime}
    log(p) log(N-p) C_j(p mod 286).
```

Equivalently, after expanding `A_j` and `B_j`,

```text
T_j(N) =
  sigma_j sum_{alpha=1..9} sum_{beta=1..11}
    u_{j,alpha} v_{j,beta}
    sum_{N/3 < p < 2N/3}
      Lambda(p) Lambda(N-p)
      chi_11(p)^alpha chi_13(p)^beta,
```

up to the already-explicit endpoint convention replacing prime sums by
strict-central weighted prime-pair sums.

The mode vectors are broad, not single-character:

- Mode `1`: effective side character counts `4.899124389855417` and
  `5.8587969819448205`.
- Mode `2`: effective counts `3.994990282499014` and
  `4.9888048746106834`.
- Mode `3`: effective counts `4.787886564984907` and
  `5.526188486527063`.
- The largest side character-energy fraction among these six sides is only
  `.2588529653280147`.

So a proof cannot estimate one exceptional character and call the mode paid.
It needs a finite but broad small-conductor mixture.

## Sufficient estimate shape

Let

```text
P(N) = positive principal contribution,
R_0(N) = exact non-q286 supports + q286 local + modes 4..6 + q286 tail.
```

The strict-central coefficient action is

```text
P(N) + R_0(N) + T_1(N) + T_2(N) + T_3(N).
```

A direct sufficient theorem is therefore:

```text
T_1(N) + T_2(N) + T_3(N) > -P(N) - R_0(N)
```

for every sufficiently large even `N`, with a finite check below the onset.

A cleaner but stronger route would prove constants `eta, rho > 0` and an
onset `N_0` such that

```text
R_0(N) >= -eta P(N),
T_1(N) + T_2(N) + T_3(N) >= -(1 - eta - rho) P(N)
```

for all even `N >= N_0` in the strict-central unit range.  The finite
diagnostics only motivate this split; they do not prove either inequality.

## Why this is hard

The inner sums are fixed-modulus, one-sided twisted binary-prime correlations:

```text
sum Lambda(p) Lambda(N-p) chi(p).
```

The character is nonprincipal and has small fixed conductor, so the expected
main term is zero after local averaging.  But the required conclusion is a
pointwise lower-tail bound for every even `N`, not merely an averaged
equidistribution statement.  This is exactly the kind of signed prime
correlation estimate that the project has not yet proved.

Chen-type results are a warning sign here.  Replacing one prime by an almost
prime avoids part of the parity obstruction.  Forcing the remaining almost
prime factor to be prime is not usually a small refinement of the same sieve;
it is the missing binary-prime correlation strength.  In this project, the
analogous "final factor" appears as pointwise control of the first-three
q286 twisted correlations.

## Source-boundary check

Current primary/expository source checks support caution rather than direct
import of a theorem.  Halupczok's 2012 paper, "Goldbach's problem with primes
in arithmetic progressions and in short intervals", states mean-value
theorems of Bombieri-Vinogradov type for binary and ternary additive prime
problems in arithmetic progressions and short intervals.  That is adjacent,
but it is not the pointwise lower-tail theorem for our fixed target `N`.

Bhowmik, Halupczok, Matsumoto, and Suzuki's "Goldbach Representations in
Arithmetic Progressions and zeros of Dirichlet L-functions" is also cautionary:
its abstract obtains average asymptotics under a distinct-zero conjecture for
Dirichlet L-functions, and relates good error terms back to zero locations and
possible Siegel zeros.  The Bhowmik-Halupczok survey notes that good average
orders with strong error terms in the arithmetic-progression setting are tied
to GRH-type hypotheses.

Working conclusion: do not cite the literature as already proving our
first-three q286 pointwise lower-tail estimate.  The direct target remains a
new in-repo proof obligation, or a carefully sourced theorem whose hypotheses
match this exact fixed-modulus, strict-central, weighted, pointwise form.

## Next falsifiers

1. Test whether first-three removal leaves a positive margin on more complete
   period cycles, not just the first period.
2. Measure whether the first-three lower tail decays with lifts of the same
   residue class, or whether it has recurring large negative excursions.
3. Compare first-three mode sums to classical fixed-modulus AP discrepancy
   proxies; if the bad targets are selected by ordinary residue imbalance,
   a sourced AP theorem might help.  If not, the proof needs a genuine
   binary-correlation input.
4. Preserve the endpoint/noncentral reconciliation separately; this note only
   concerns the strict-central unit coefficient action.

## AP discrepancy proxy result

`q286_first_three_ap_discrepancy_proxy_receipt` compares the first-three q286
mode sum against two ordinary residue-discrepancy envelopes.  For each target,
it forms the strict-central prime-pair weight in every admissible residue
class modulo `286`, subtracts the uniform admissible mean, and compares the
first-three mode action with:

- a uniform residue-error `L^1` envelope,
- a Cauchy `L^2` envelope,
- the actual alignment with that `L^2` envelope.

On selected hard targets
`10424,10664,14138,30164,40676,85496,88346,11194,15272`, the required
uniform relative residue error to match the actual first-three mode size lies
between about `.130487` and `.528174`.  The largest lower-tail selected case
is `10664`, with first-three ratio `-1.150088`, maximum residue deviation
`2.315106`, required uniform error `.528174`, and L2 alignment `.220032`.

On the complete first period `10000..20008`, the first-three q286 mode sum is
negative at `2525` of `5005` targets.  The worst lower tail is again `10664`,
with first-three/principal ratio `-1.1500880008976306`.  The largest required
uniform relative error over negative first-three targets is
`.5281735902332463`, again at `10664`; over all targets the largest two-sided
value is `.7408970850830631` at `10724`, where the first-three mode is
positive.  The largest L2 alignment over negative first-three targets is only
`.26921675478661156`, at `14892`; the largest two-sided alignment is
`.3784984423382312`, at `17446`.

Status `changed-under-evidence`: a naive AP-discrepancy proof would need a
pointwise uniform residue error well below the actually observed residue
fluctuations at small scale, while the Cauchy L2 envelope is loose by a factor
of at least about `1/.269` on the lower tail.  Ordinary AP discrepancy remains
a useful diagnostic, but a proof still needs coefficient-sensitive binary
correlation structure rather than just a black-box full-residue equidistribution
bound.

## Exact-negative residue drivers

`q286_first_three_full_negative_driver_receipt` restricts the AP-proxy
diagnostic to exact full-action negative targets.  On the first full period
`10000..20008`, there are `75` exact negatives.  Among their top eight
negative residue drivers, residue `133` appears in `60` cases and is empty
relative to the uniform admissible mean in all `60`; residue `153` appears in
`61` cases and is empty in `59`.  Both residues appear in `46` cases, and
both are empty in `44`.

The top eight residue terms carry a moderate but not total amount of the
absolute real contribution: minimum fraction `.44127253691663915`, mean
`.5145044943315689`, maximum `.639566987107544`.

Status `aha-candidate`: the worst strict-central failures often come from
missing high-positive first-three q286 coefficient residues, especially `133`
and `153`, each of which contributes about `-0.3224` principal when empty in
the main hard cases.  This gives a sharper residue-hitting subproblem, but it
does not explain all negatives and cannot replace the broader twisted
correlation estimate.

The same receipt now separates local admissibility from genuine empty
admissible classes.  Among the `75` exact negatives, residue `133` is locally
admissible `68` times, empty in `60`, positive in `8`, and inadmissible in
`7`; residue `153` is admissible `70` times, empty in `59`, positive in `11`,
and inadmissible in `5`.  Both driver residues are admissible in `63` exact
negative targets and both are admissible-empty in `44`.

This refines the residue-hitting subproblem: a proof cannot merely say these
classes are sometimes locally unavailable.  In many exact negative cases they
are locally available but contain no strict-central prime pair at the tested
scale.

# q286 complement-versus-alignment theorem obligation

Status: theorem obligation and finite-vector obstruction; Goldbach not proved.

Date: 2026-09-13.

## Fixed objects

The implemented q286 first-three functional has modulus `286` and `120` unit
residues.  For an even target residue `a = N mod 286`, let

```text
A_a = {r in U_286 : a-r is also in U_286}.
```

The admissible counts are `99`, `108`, `110`, or `120`, depending on `a`.
Let `W_N(r)` be the strict-central weighted prime-pair mass with
`p == r mod 286`:

```text
W_N(r) = sum log(p)log(N-p)
```

over strict-central prime pairs `N/3 < p < 2N/3`.  Let

```text
mu_N = (sum_{r in A_a} W_N(r)) / |A_a|,
d_N(r) = W_N(r) - mu_N  for r in A_a,
d_N(r) = 0              otherwise.
```

The first-three q286 contribution is exactly the finite inner product

```text
F_3(N) = <c_a, d_N>,
```

where `c_a` is the real q286 first-three coefficient vector centered on the
same admissible set.  In principal-normalized form, the implemented L2 bound is

```text
B_2(N) = ||c_a||_2 ||d_N||_2 / P(N).
```

The measured singular values defining the uncentered first-three q286
functional are approximately

```text
158279.09383760378
124234.1882436279
21476.920434701242
```

Across target residues, the centered admissible coefficient norms measured from
the implementation are:

```text
||c_a||_2 range: 737130.2261974699 .. 2216691.1337206536
||c_a||_1 range: 5385068.449447754 .. 10612733.570460552
```

## Sufficient theorem candidate

After excluding and finitely checking the boundary/full-negative layer, a
direct sufficient theorem is:

```text
F_3(N) / P(N) >= -0.4 * B_2(N)
full_without_first_three(N) / P(N) > 0.4 * B_2(N)
```

at least for every target in the first-three lower-tail set.  Together these
give positive recombined strict-central action on that set.  The non-tail set
still needs its own quantified complement statement, but it is not the active
failure mode in the current diagnostics.

## Finite-vector obstruction

The alignment inequality cannot be proved from finite-vector geometry,
admissible support, nonnegativity, and total mass alone.

Fix any target residue `a` with nonzero centered coefficient vector `c_a`.
For any total mass `M > 0`, set the uniform admissible mass
`mu = M / |A_a|`.  For sufficiently small `epsilon > 0`, define

```text
d(r) = -epsilon * c_a(r)  for r in A_a,
W(r) = mu + d(r).
```

Because `c_a` is centered on `A_a`, the new weights still have total mass
`M`; because `epsilon` can be chosen small, all `W(r)` are nonnegative.  But

```text
<c_a, d> = -epsilon ||c_a||_2^2
||c_a||_2 ||d||_2 = epsilon ||c_a||_2^2,
```

so the alignment cosine is exactly `-1`.  Therefore every ceiling
`theta < 1`, including `.4`, is false for arbitrary admissible nonnegative
weights.  A proof of the measured `.4` behavior must use arithmetic facts
about actual binary prime-pair weights, not only residue support or Cauchy
geometry.

## What must be proved or identified

The first missing theorem is a coefficient-matched binary-prime residue
discrepancy estimate:

```text
<c_a, d_N> >= -0.4 ||c_a||_2 ||d_N||_2
```

for all sufficiently large relevant even `N`, or for all such `N` in the
first-three lower-tail regime.

The second missing theorem is a complement lower-envelope estimate:

```text
full_without_first_three(N) / P(N)
    > 0.4 ||c_a||_2 ||d_N||_2 / P(N).
```

This complement statement is not equivalent to a local admissibility theorem.
It must use the actual remaining strict-central coefficient action.  If the
only available route to either statement is pointwise prime-pair occupancy in
specific residue channels strong enough to imply restricted binary Goldbach
classes, then this lane has reached a hard theorem-equivalence obstruction
rather than a proof.

## Conditional theorem from pointwise fixed-modulus equidistribution

There is a clean conditional closure, but its hypothesis is essentially the
kind of pointwise binary-prime-in-progressions theorem that is not presently
available.

Let `q` be a fixed modulus carrying the complete strict-central assembled
coefficient, for example `q=10010`, and let `U_q(N)` be the admissible unit
residue classes for the first prime in `N=p+(N-p)`.  Suppose that for every
admissible residue `r` one has a pointwise strict-central asymptotic

```text
W_N(r) = M_N / |U_q(N)| + o(M_N)
```

uniformly in `r`, where `W_N(r)` is the log-weighted strict-central prime-pair
mass in that residue and `M_N=sum_r W_N(r)`.  Since every centered coefficient
vector on the fixed finite residue set has bounded norm, every centered
coefficient action is then `o(P(N))`, while the principal action is `P(N)`.
Therefore the full assembled strict-central action is

```text
P(N) + o(P(N)) > 0
```

for all sufficiently large even `N` satisfying the local admissibility
conditions.  A finite check below the onset would then close this strict-
central coefficient problem.

This is rigorous as a conditional theorem, but it does not solve Goldbach
because the hypothesis already asserts pointwise positive prime-pair mass in
every admissible residue class at a fixed modulus.  It is stronger than the
coefficient-matched anti-alignment estimate and is in the same hardness family
as binary Goldbach in arithmetic progressions.

For the q286 first-three subproblem, a weaker conditional form is enough.  If

```text
||d_N||_2 / M_N <= delta_N
```

and `K_a = ||c_a||_2 / principal_mean`, then

```text
|F_3(N)| / P(N) <= K_a delta_N.
```

Thus the complement beats the whole first-three L2 envelope whenever

```text
delta_N < (full_without_first_three(N) / P(N)) / K_a.
```

The measured implementation has `K_a <= 50.37646733742071` across target
residues.  On selected stress targets the required L2-relative discrepancy
thresholds are:

```text
target 14138:   0.0003619625968602846
target 70526:   0.03014917441354616
target 1222142: 0.025165692383669395
target 1379072: 0.025798469567275696
target 1426262: 0.023571470732776444
target 3305200: 0.021132268379254724
```

Interpretation: the boundary target `14138` cannot be handled by a realistic
coarse discrepancy theorem because its complement is tiny.  Later stress
targets have thresholds around two to three percent, so a true pointwise
fixed-modulus equidistribution theorem with relative L2 error tending to zero
would eventually dominate them.  The missing ingredient is proving such a
pointwise theorem, not another support-only finite-vector inequality.

## Weaker character-mixture target

Full residue-by-residue equidistribution is stronger than necessary.  The
q286 first-three term is a fixed mixture of only the `9*11 = 99`
nonprincipal character products

```text
chi_11(p)^alpha chi_13(p)^beta,
alpha=1..9, beta=1..11.
```

Let

```text
S_{alpha,beta}(N)
  = sum_{N/3<p<2N/3} Lambda(p)Lambda(N-p)
      chi_11(p)^alpha chi_13(p)^beta.
```

The first-three term has the form

```text
F_3(N) = sum_{alpha,beta} a_{alpha,beta} S_{alpha,beta}(N),
```

with coefficients obtained by truncating the q286 character matrix to its
first three singular modes.  The measured coefficient norms are:

```text
number of character products: 99
sum |a_{alpha,beta}|: 1421636.6771468068
Frobenius norm of a: 202355.2894934171
max |a_{alpha,beta}|: 35926.096497151906
principal_mean: 44002.512499999146
sum |a| / principal_mean: 32.308079615836355
||a||_2 / principal_mean: 4.5987212546879235
```

Therefore a pointwise bound

```text
max_{alpha,beta} |S_{alpha,beta}(N)| <= epsilon M_N
```

would give

```text
|F_3(N)| / P(N) <= 32.308079615836355 * epsilon.
```

In particular, the blunt triangle route would force the first-three term below
`.2` principal once `epsilon < 0.006190401979261144`.  A sharper vector theorem

```text
(sum_{alpha,beta} |S_{alpha,beta}(N)/M_N|^2)^(1/2) <= epsilon_2
```

would give

```text
|F_3(N)| / P(N) <= 4.5987212546879235 * epsilon_2.
```

This is a better theorem target than full residue-class equidistribution:
control the finite signed q286 character mixture directly.  It is still a
pointwise twisted binary-prime correlation theorem, so existing average
Bombieri-Vinogradov style results do not supply it.

## Character-mixture norm receipt

Added `q286_first_three_character_mixture_norm_receipt` to expose the exact
finite character vector for selected targets.  It measures:

- the normalized maximum character imbalance,
- the normalized character-vector L2 imbalance,
- the triangle and vector-L2 character bounds on the first-three term,
- reconstruction error between the residue-side and character-side first-three
  actions.

Validation:

```text
python -B -m py_compile lcm_sawtooth_goldbach_transfer.py test_lcm_sawtooth_goldbach_transfer.py
test_q286_first_three_character_mixture_norm ... ok
Ran 1 test in 49.460s
```

Selected stress targets:

```text
tested 6
coeff_l1/principal_mean 32.308079615836355
coeff_l2/principal_mean 4.598721254687924
negative targets: 14138, 70526, 1222142, 1379072, 1426262, 3305200
triangle-certified targets at .2 principal: none
vector-L2-certified targets at .2 principal: none
maximum reconstruction error: 1.2825000297334084e-16

target 14138:
  first_three -0.8950145872346784
  character_linf_relative 0.2194671982889227
  character_l2_relative 1.0443145675921686
  triangle bound 7.090563715383058
  vector-L2 bound 4.802511598566334
  vector-L2 utilization 0.18636385750778028

target 70526:
  first_three -0.7650482510196676
  character_linf_relative 0.09054141464341225
  character_l2_relative 0.43103036793996347
  triangle bound 2.9252192328298148
  vector-L2 bound 1.9821885144614664
  vector-L2 utilization 0.38596139844323574

target 1222142:
  first_three -0.3075877603708801
  character_l2_relative 0.18844394482113214
  vector-L2 bound 0.8666011743661788
  vector-L2 utilization 0.35493577607467003

target 1379072:
  first_three -0.3394138842129011
  character_l2_relative 0.1880313707312656
  vector-L2 bound 0.864703861129976
  vector-L2 utilization 0.3925203754373925

target 1426262:
  first_three -0.253372013706637
  character_l2_relative 0.13241221074115736
  vector-L2 bound 0.6089268479155769
  vector-L2 utilization 0.41609598028721684

target 3305200:
  first_three -0.14018011556710222
  character_l2_relative 0.07505019406826197
  vector-L2 bound 0.34513492263016987
  vector-L2 utilization 0.40616033433774695
```

Status `falsifier-plus-target`: neither the triangle character bound nor the
plain character-vector L2 bound certifies the selected stress targets at `.2`
principal.  The receipt nevertheless gives the exact theorem-facing vector and
shows the later stress targets are far less extreme than the boundary target.
The next proof step should seek coefficient-specific anti-alignment or sharper
structure inside the 99-character vector, not just a norm bound.

## Bounded source check

Searched current public sources on 2026-09-13 for binary Goldbach in
arithmetic progressions, pointwise estimates, and GRH/RH connections.  The
closest located primary sources do not supply the needed theorem.

- Bhowmik, Halupczok, Matsumoto, and Suzuki, "Goldbach Representations in
  Arithmetic Progressions and zeros of Dirichlet L-functions",
  https://arxiv.org/abs/1704.06103.  The paper states that almost-all
  congruence-conditioned binary Goldbach results are known, but "the complete
  solution of these binary Goldbach problems is out of sight"; it studies
  average orders and relations with zeros of Dirichlet L-functions.  Its
  introduction also records that good average error terms are tied to RH/GRH
  style zero information.  This is adjacent but average, not pointwise in the
  fixed target `N`.
- Halupczok, "Goldbach's problem with primes in arithmetic progressions and in
  short intervals", https://arxiv.org/abs/1212.4406.  The abstract describes
  Bombieri-Vinogradov style mean value theorems for binary and ternary
  additive prime problems in APs and short intervals.  Mean value estimates do
  not imply the pointwise q286 anti-alignment ceiling required here.
- Bhowmik and Halupczok, "Asymptotics of Goldbach Representations",
  https://arxiv.org/abs/1809.06920.  The abstract frames classical Goldbach
  asymptotics in relation to RH, and says AP-restricted variants have
  comparable but weaker relations with zeros of L-functions.  This supports
  caution: the present route may touch RH/GRH-type territory if strengthened
  into sharp averaged asymptotics, but the current pointwise coefficient
  theorem is not obtained from that literature.

Working conclusion: no located source currently gives the exact fixed-modulus,
strict-central, log-weighted, coefficient-matched pointwise theorem needed for
the `.4` alignment route.  Future literature checks should search for exactly
"pointwise binary Goldbach in fixed residue classes with power-saving error"
or a theorem that bounds finite signed character mixtures
`sum Lambda(p)Lambda(N-p) chi(p)` uniformly in every even `N`.

## Current finite evidence

The window receipt
`q286_first_three_tail_alignment_complement_window_receipt` checks this
sufficient condition on finite windows.  On global cycles `105..136`, with
tail threshold `.3` and alignment ceiling `.4`, it found three tail targets
`1222142, 1323632, 1379072`; all three were certified by the measured
complement, and none was an actual full-action negative.

The same sufficient condition fails at boundary target `14138`, where the
complement is only `0.018073313793834367` principal and the target is actually
full-negative in the assembled strict-central action.  Thus any theorem route
must split the boundary layer from the eventual estimate.

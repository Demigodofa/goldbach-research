# q286 residue-pair correlation obligation

Status: theorem-obligation artifact. Goldbach is not proved.

This note is the literal "bolt it on, subtract it, what is left?" version of
the q286 first-three signed-projection joint.

For `M=286`, let `U=(Z/MZ)^*`. For an even target residue `a`, define

```text
A_a = {u in U : a-u in U}.
```

Let `gamma_a(u)` be the q286 first-three coefficient centered on `A_a` and
divided by the principal mean. For an even target `N == a mod 286`, let
`W_N(u)` be the strict-central weighted binary-prime mass with first prime
residue `u`, and let `T_N=sum_u W_N(u)`.

The exact missing theorem behind the signed-projection joint is:

```text
sum_{u in A_a} (W_N(u) - T_N/|A_a|) * gamma_a(u) >= -tau * T_N
```

for all sufficiently large even `N` in the q286 lane, with `tau=.3`.

Equivalently, after normalizing by `T_N`, the residual is just the signed
dot product of the prime-pair residue discrepancy against the fixed q286
coefficient vector. This is the precise residue-correlation theorem backing
the current route.

## Evidence

- Receipt: `q286_first_three_residue_pair_correlation_obligation_receipt`
- Builder:
  `tools/build_q286_first_three_residue_pair_correlation_obligation.py`
- JSON evidence:
  `evidence/q286-first-three-residue-pair-correlation-obligation.json`
- Focused regression:
  `test_q286_first_three_residue_pair_correlation_obligation`

The receipt checks all `143` even target residues modulo `286`; the centered
coefficient sum on every admissible set is zero up to about
`2.31e-14`. The finite sample rows agree with the prior signed-projection
receipt to below `5.6e-17`.

## Residual Ledger

For the tail row `N=1222142`, `N mod 286 = 64`:

- signed projection: about `-0.30758776037087937`
- threshold slack at `tau=.3`: about `-0.007587760370879382`
- largest negative residual hits:
  - residue `133`: about `-0.1537411437490966`
  - residue `153`: about `-0.0803298129041402`
  - residue `23`: about `-0.018864432015842852`
- largest positive residual hits:
  - residue `45`: about `0.008642767093924007`
  - residue `179`: about `0.008020222905569176`
  - residue `3`: about `0.005890498295809695`

For clear row `N=1242118`, `N mod 286 = 20`:

- signed projection: about `-0.28642674326843226`
- threshold slack at `tau=.3`: about `0.013573256731567729`
- largest negative residual hits:
  - residue `153`: about `-0.18777746964652278`
  - residue `133`: about `-0.08454822836650394`
  - residue `263`: about `-0.02162291131120957`
- largest positive residual hits:
  - residue `45`: about `0.012061150604095868`
  - residue `127`: about `0.008669237274622233`
  - residue `179`: about `0.006194684381534304`

For clear row `N=1240888`, `N mod 286 = 220`:

- signed projection: about `-0.27468410150061684`
- threshold slack at `tau=.3`: about `0.02531589849938315`
- largest negative residual hits:
  - residue `153`: about `-0.12630791446582174`
  - residue `133`: about `-0.07138211262175792`
  - residue `263`: about `-0.015757500282928247`
- largest positive residual hits:
  - residue `67`: about `0.009491068242367449`
  - residue `241`: about `0.004214010069498238`
  - residue `141`: about `0.003717415641602436`

Interpretation: this does not look like featureless random spray. The same
large coefficient residues, especially `133` and `153`, recur in the local
ledger. The theorem still needed is not "find a few lucky hits"; it is a
one-sided arithmetic correlation statement saying the weighted residue
discrepancy cannot stay too anti-aligned with `gamma_a`.

## Conditional route

A fixed-modulus strict-central binary-prime AP theorem giving

```text
W_N(u) = T_N/|A_a| + o(T_N)
```

uniformly in `u` for every even residue `a` would imply the q286 first-three
signed-projection bound for every fixed `tau>0`, eventually, whenever
`T_N>0`.

If the theorem is instead stated with a positive Hardy-Littlewood-type main
term rather than normalized by `T_N`, it is Goldbach-strength for the central
window. This note identifies that exact backing theorem; it does not prove or
cite it.

## Boundary

This closes only the ambiguity of what arithmetic input is missing behind the
signed-projection tack. It does not close the signed-projection theorem,
strict-central prime-pair existence, complement/lower-support rescue,
endpoint/noncentral terms, outer assembly, or Goldbach.

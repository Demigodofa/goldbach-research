# q286-WBSS main-term sign audit

Status: finite coefficient diagnostic.  This is not a binary distribution
theorem, signed prime-correlation theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

## Question

The q286 theorem pivot extracted `q286-WBSS`, the weighted binary-prime
sign-sum problem:

```text
B_Phi(N) =
  sum_{r in A_a} Phi_a(r)
    sum_{N/3 < p < 2N/3, p == r mod M, N-p prime}
      log(p)log(N-p).
```

The first orientation check is whether the signed coefficient `Phi_a` has a
positive local-uniform main term over admissible residue-pair orbits.  If the
uniform mean were zero or negative, the q286 witness would not be a normal
main-term proof target; it would require a persistent nonlocal bias.

## Result

`tools/build_q286_wbss_main_term_sign_audit.py` generated
`evidence/q286-wbss-main-term-sign-audit.json`.

For the frozen full q286 signed coefficient on the `196` post-discovery rows:

```text
positive uniform mean count:       196 / 196
uniform mean range:                0.6176511908339223..1.30728332102425
centered Linf range:               15.726925134846791..38.31239944523117
sufficient L1 budget range:        0.020711496156757627..0.06441548422792709
tightest L1 row:                   target 279994
```

For the target-dependent edge coefficient
`beta = gap-required` on the `196` post-discovery rows:

```text
positive uniform mean count:       196 / 196
uniform mean range:                0.17657405569313075..1.0628616001581876
centered Linf range:               3.6184471793783115..14.076074177061635
sufficient L1 budget range:        0.026797640365636533..0.18715353351948102
tightest L1 row:                   target 98216
```

The all-row beta check has one negative-uniform-mean discovery row, so this
does not define a universal row class by itself.  The post-discovery q286 tail
does have favorable local-uniform orientation.

## Meaning

The q286 witness is not blocked by a bad main term.  Under a hypothetical
binary-prime distribution theorem strong enough to keep the actual normalized
orbit measure `mu_N` near the local-uniform admissible measure `u_a`, positivity
would follow from:

```text
||mu_N-u_a||_1
  <
mean_u(Phi_a) / ||Phi_a-mean_u(Phi_a)||_infty.
```

The hard part is proving that kind of binary-prime distribution estimate
pointwise for every target `N`.  Bennett-Martin-O'Bryant-Rechnitzer supplies
source-backed one-dimensional AP prime-count inputs, but previous q286 work
already showed that AP marginals and pigeonhole do not force the binary
convolution or the signed q286 functional.  Tao's parity-obstruction
discussion is also a warning that sieve-linear discrepancy inputs are unlikely
to solve the binary problem without controlling functions like
`Lambda(n)Lambda(N-n)` or using a genuinely different method.

## New theorem target

Prove one of the following:

```text
||mu_N-u_a||_1 < 0.020711496156757627
```

for the frozen full q286 coefficient on every sufficiently large covered
post-discovery-type target, or the sharper coefficient-specific signed
inequality:

```text
B_Phi(N) > 0.
```

The L1 number is a finite worst-case budget from the checked rows, not a
proved universal threshold.  It is useful because it translates the q286
geometry into a concrete analytic demand: a pointwise binary-prime orbit
distribution theorem at roughly a few-percent scale.

## Decision

Continue the q286 lane only through this main-term-plus-error route, a direct
signed binary-prime correlation theorem, or a source-backed fixed-modulus
binary Goldbach-in-progressions theorem.  More row scans without such a
predeclared implication are not proof progress.

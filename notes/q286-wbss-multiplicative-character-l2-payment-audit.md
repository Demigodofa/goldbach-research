# q286-WBSS multiplicative character L2-payment audit

## Question

The character-payment audit used an equal `L_infinity` cap on every active
multiplicative-character moment.  Does the full active character package give
a better theorem target if the missing analytic estimate is an aggregate
`L2` character-moment bound?

## Mechanism

For each projected modulus `d`, the active character expansion gives

```text
E_d(N) = <c_hat_d, D_d(N)>.
```

Therefore

```text
|E_d(N)| <= ||c_hat_d||_2 ||D_d(N)||_2
```

and a second Cauchy step gives

```text
AdverseDrag(N)
  <= sqrt(sum_d ||c_hat_d||_2^2) * sqrt(sum_d ||D_d(N)||_2^2).
```

So an aggregate active-character `L2` theorem paying

```text
sqrt(sum_d ||D_d(N)||_2^2) < LocalMain(N) / sqrt(sum_d ||c_hat_d||_2^2)
```

would imply `AdverseDrag(N) < LocalMain(N)`.

## Result

```text
aggregate coefficient L2 square:       30.52680126946419
aggregate coefficient L2:               5.525106448699807
minimum local main:                     0.6039353780830684
aggregate character-moment L2 cap:      0.10930746469603118
character L_infinity cap:               0.012286599575574883
residue L_infinity cap:                 0.0016192946592982506
relaxation vs character L_infinity:     8.89647815277782
relaxation vs residue L_infinity:      67.50313420004822
```

Per modulus:

```text
modulus   ||c_hat_d||_2   cap if paid alone
70        2.0499520132192397   0.29460951972951294
130       0.18221772146455884  3.3143613762096855
154       2.205804783828344    0.2737936659267245
286       4.628792495952571    0.1304736340225126
```

## Decision

The aggregate active-character `L2` theorem shape is materially sharper than
the equal character-moment cap.  It moves the required pointwise moment bound
from about `0.0122866` to about `0.109307`, an `8.90x` relaxation, and is
about `67.5x` looser than the original equal per-residue cap.

This is the best current theorem-facing formulation of the character route,
but it is still a missing universal analytic estimate.  The route now needs a
pointwise aggregate fixed-modulus twisted binary-prime moment theorem strong
enough to prove

```text
AdverseDrag(N) < LocalMain(N)
```

for every sufficiently large eligible even `N`, followed by finite
initial-range verification.  This receipt proves no aggregate character
moment theorem, pointwise adverse-drag theorem, q286 threshold theorem,
strict-central Goldbach theorem, or Goldbach proof.

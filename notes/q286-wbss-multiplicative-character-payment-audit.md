# q286-WBSS multiplicative character-payment audit

## Question

The residual schedule showed that coefficient-energy truncation cannot close
the q286-WBSS pointwise target.  If the full active multiplicative-character
package is retained, what universal pointwise character-moment estimate would
actually pay the local main?

## Mechanism

For each projected modulus `d`, write the centered coefficient vector in
multiplicative-character coordinates:

```text
c_d(s) = sum_chi c_hat_{d,chi} chi(s)
```

and write the projected error as

```text
E_d(N) = sum_chi c_hat_{d,chi} D_{d,chi}(N)
D_{d,chi}(N) = sum_s chi(s) Delta_{d,s}(N)
```

in the same unnormalized residue-mass scale.  Therefore the sufficient
full-package payment condition is

```text
sum_{d,chi} |c_hat_{d,chi}| * theta_{d,chi}(N) < LocalMain(N).
```

In the equal-cap stress form, if every active character moment satisfies
`|D_{d,chi}(N)| <= theta(N)`, then

```text
AdverseDrag(N) <= total_character_L1 * theta(N).
```

## Result

```text
active nonzero character coefficients:          122
active real conjugacy channels:                  64
self-conjugate active channels:                   6
total character L1:              49.153988812629684
minimum local main:               0.6039353780830684
equal active character-moment cap: 0.012286599575574883
residue equal cap:                0.0016192946592982506
cap relaxation factor:             7.58762434311955
```

Per modulus:

```text
modulus   active chars   real channels   character L1
70        11             6               6.032956699609752
130       23             13              0.818791486578005
154       29             15              9.734847733726912
286       59             30              32.56739289271501
```

## Decision

The full active multiplicative-character package is a better analytic target
than per-residue L1 control: the equal active character-moment cap is about
`7.59` times looser than the equal residue cap.  But this is still a theorem
obligation, not evidence that the theorem is true.

The route now needs a universal, pointwise, unnormalized fixed-modulus twisted
binary-prime estimate strong enough to prove

```text
AdverseDrag(N) < LocalMain(N)
```

for every sufficiently large eligible even `N`, followed by finite
initial-range verification.  This receipt proves no character-moment estimate,
residual character theorem, pointwise adverse-drag theorem, q286 threshold
theorem, strict-central Goldbach theorem, or Goldbach proof.

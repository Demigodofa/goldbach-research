# q286 dominant-mode helpful-channel portfolio

Status: finite fixed-portfolio diagnostic.  Goldbach is not proved.

This note tests whether the helpful channels found in the swing-pair autopsy
form a fixed portfolio on the selected branch rows.

Receipt:
`evidence/q286-first-three-dominant-mode-helpful-portfolio.json`

## Mechanism Tested

The swing-pair receipt found recurrent helpful channel deltas.  This receipt
turns those labels into fixed portfolios and measures their contribution on
the selected target rows:

- universal helpful portfolio: channels helpful in every selected pair;
- recurrent helpful portfolio: channels helpful in at least `4` of the `6`
  selected pairs.

The selected rows are the same ten rows used by the signed branch sample.

## Measured Shape

The row reconstruction error is `0`; the swing reconstruction error is below
`8.2e-15`.

Universal portfolio:

```text
(2,6), (3,1)
```

On the selected rows, this two-channel portfolio separates clear rows from
deficit rows by portfolio contribution:

- deficit portfolio range: about `[-0.1091989843768742, -0.025763340316837968]`;
- clear portfolio range: about `[-0.006651837884822224, 0.29176678826178515]`.

But this is not enough to make the two-channel route a theorem target by
itself.  On pair `(164598,129706)`, the universal portfolio captures only
about `0.053365192147409486` of the positive channel delta.

Recurrent portfolio:

```text
(2,6), (3,1), (4,8), (4,2), (3,11), (5,5),
(4,4), (1,3), (5,3), (2,4), (4,6)
```

This `11`-channel portfolio also separates clear rows from deficit rows in the
selected sample:

- deficit portfolio range: about `[-0.37122975942218756, -0.10723633690587824]`;
- clear portfolio range: about `[-0.08655055405574329, 0.19253426324647357]`.

Its weakest positive-delta capture is again pair `(164598,129706)`, where it
captures about `0.4917301271872004` of the positive channel delta.

## Consequence

The fixed portfolio is a genuine finite candidate: on the selected rows, its
value separates clears from deficits.  But the two-channel version is too weak
as a swing explanation, and even the recurrent portfolio does not eliminate
the nonportfolio residual.  The next theorem target is therefore:

```text
prove a portfolio-level lower bound for the recurrent helpful channel package
under high negative pressure,
```

or prove that this package estimate is already a fixed-modulus binary-prime
character-sum theorem in disguise.

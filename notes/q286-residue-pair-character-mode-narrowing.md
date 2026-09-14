# q286 residue-pair character-mode narrowing

Status: finite theorem-shaping evidence. Goldbach is not proved.

This note follows the external-theorem comparison.  The question was whether
the q286 one-sided residue-pair projection against `gamma_a` is visibly
narrower than full fixed-modulus AP Goldbach.

Existing machinery already expresses the q286 first-three channel in the
character domain:

- the natural first-three support is `(11,13)` on modulus `286`;
- the underlying character-product space has `99` entries;
- the active first-three approximation is rank three, with singular values
  about `158279.09383760378`, `124234.1882436279`, and
  `21476.920434701242`.

The new evidence file
`evidence/q286-residue-pair-character-mode-narrowing.json` applies the
existing character-mixture and singular-coordinate receipts to the current
near-boundary samples `1222142`, `1242118`, and `1240888`.

## Observed Mode Ledger

For tail `1222142`:

- first-three/principal: about `-0.3075877603708801`
- mode 1 contribution: about `-0.22694130852262354`
- mode 2 contribution: about `-0.08189187103790489`
- mode 3 contribution: about `+0.001245419189648385`
- signed/absolute mode ratio: about `-0.9919670741891364`

For clear row `1242118`:

- first-three/principal: about `-0.2864267432684323`
- mode 1 contribution: about `-0.20879991719144114`
- mode 2 contribution: about `-0.07467116934181281`
- mode 3 contribution: about `-0.002955656735178345`
- signed/absolute mode ratio: about `-1.0000000000000002`

For clear row `1240888`:

- first-three/principal: about `-0.27468410150061706`
- mode 1 contribution: about `-0.18692252513915686`
- mode 2 contribution: about `-0.08589090147992547`
- mode 3 contribution: about `-0.0018706748815347056`
- signed/absolute mode ratio: about `-1.0000000000000002`

## Interpretation

The tested near-boundary rows are not being rescued by cancellation among the
rank-three q286 character modes.  The first two singular modes dominate and
are same-sign negative in all three rows; the third mode is tiny.

This narrows the route but also adds pressure.  A proof cannot merely say
"the character mixture cancels internally" at these rows.  It needs one of:

1. A pointwise lower bound for the first two q286 singular character
   coordinates.
2. A structural reason that the first two coordinates cannot both remain too
   negative beyond a finite boundary.
3. A separate complement/lower-support rescue theorem that absorbs this
   first-three negativity.
4. A full fixed-modulus AP/Goldbach-strength input.

## Boundary

This is finite evidence only. It does not prove a pointwise character-sum
estimate, a fixed-modulus binary AP theorem, the q286 signed-projection
theorem, or Goldbach.

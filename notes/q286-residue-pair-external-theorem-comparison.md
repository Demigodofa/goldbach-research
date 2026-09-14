# q286 residue-pair external theorem comparison

Status: source-backed theorem-strength comparison. Goldbach is not proved.

This note classifies the outside arithmetic input needed by
`notes/q286-residue-pair-correlation-obligation.md`.

## q286 obligation

The current q286 signed-projection tack is equivalent to the following
one-sided fixed-modulus residue-pair discrepancy statement. For `M=286`,
`U=(Z/MZ)^*`, `A_a={u in U : a-u in U}`, centered first-three coefficient
`gamma_a(u)`, strict-central weighted binary-prime residue weights `W_N(u)`,
and `T_N=sum_u W_N(u)`, prove for every sufficiently large even
`N == a mod 286`:

```text
sum_{u in A_a}(W_N(u)-T_N/|A_a|)*gamma_a(u) >= -tau*T_N
```

with `tau=.3`.

This is weaker than a full per-residue asymptotic, because it asks only for a
single weighted one-sided projection.  It is stronger than the currently
recorded finite receipts, because it is pointwise and eventual.

## What known-style results would supply it

A fixed-modulus strict-central binary-prime AP theorem of the form

```text
W_N(u) = T_N/|A_a| + o(T_N)
```

uniformly in `u in A_a`, for every even residue `a`, would imply the q286
inequality for every fixed `tau>0` and all sufficiently large `N` with
`T_N>0`.

A stronger Hardy-Littlewood-style statement giving a positive main term for
each residue-pair channel would also imply `T_N>0`; that kind of theorem is
Goldbach-strength for the strict-central AP problem, not a small local lemma.

## Literature boundary checked

The comparison here uses public arXiv source pages as locators, not as proof
imports:

- Bhowmik, Halupczok, Matsumoto, Suzuki,
  "Goldbach Representations in Arithmetic Progressions and zeros of Dirichlet
  L-functions", arXiv:1704.06103. The introduction says AP binary Goldbach
  variants are known in almost-all forms, that complete binary solutions are
  out of sight, and that their paper studies average orders and relations to
  zeros of Dirichlet `L`-functions. It gives summatory asymptotics such as
  `S(x;q,a,b)=x^2/(2 phi(q)^2)+O(x^{1+B_q})`, and discusses GRH/DZC-style
  implications. This is valuable context but it is not a pointwise
  per-target q286 inequality.
- Salmensuu, "The Goldbach conjecture with summands in arithmetic
  progressions", arXiv:2106.00778. The abstract states almost-all results
  over moduli/residue classes/natural numbers. Almost-all coverage does not
  imply the q286 every-large-`N` bound.
- Lichtman, "Primes in arithmetic progressions to large moduli, and Goldbach
  beyond the square-root barrier", arXiv:2309.08522. The abstract records
  improved levels of distribution and applications to upper bounds for
  Goldbach representations. Distribution and upper-bound improvements do not
  supply the needed one-sided pointwise lower discrepancy inequality.

## Conclusion

No checked source here supplies the q286 residue-pair obligation as stated.
The exact current position is:

1. The q286 tack is not vague anymore; it is a fixed-modulus weighted
   residue-pair discrepancy inequality.
2. Full uniform fixed-modulus AP asymptotics would imply it.
3. Average, almost-all, level-of-distribution, and upper-bound results do not
   imply it as stated.
4. A positive pointwise AP asymptotic would be Goldbach-strength for the
   strict-central AP problem.
5. The potentially narrower opportunity is to prove only the specific
   one-sided projection against `gamma_a`, not all residue channels
   separately.

Next non-circular action: attack that one-sided projection directly, preferably
by decomposing `gamma_a` into Dirichlet-character modes and asking whether the
needed lower bound is a smaller signed zero-sum estimate than full AP
Goldbach. If that decomposition still requires pointwise binary-prime
asymptotics in every character channel, record the q286 route as explicitly
conditional on a Goldbach-strength external theorem.

## Sources

- https://arxiv.org/abs/1704.06103
- https://arxiv.org/abs/2106.00778
- https://arxiv.org/abs/2309.08522

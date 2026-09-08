# What the cubic safety margin actually measures

Owner: Kevin's Goldbach investigation. Purpose: choose tests against the
surviving raw-margin rule and prevent count rearrangements or marginal-density
estimates from being mistaken for a positivity proof. The identities below
were independently reviewed by Sol. They are new-to-this-task observations,
not a claim of worldwide novelty.

## Exact classes

Use the complete ordered candidate range and square-start presieve of
`cubic-three-stage-identity.md`, with z=floor(cuberoot(N-3)). Each surviving
argument is prime or semiprime. Define ordered counts:

- PP: both arguments prime;
- PS: exactly one argument semiprime;
- SSsame: both semiprime, with the same least prime factor;
- SSdiff: both semiprime, with distinct least prime factors.

The residual event multiplicity is respectively 0,1,1,2. Consequently

    M = PP + PS + SSsame + SSdiff,
    S1 = PS + SSsame + 2*SSdiff,
    S2 = SSdiff,
    R = M-S1 = PP-SSdiff.

Thus the proposed sufficient condition R>0 asks for strictly more prime-prime
candidates than distinct-factor semiprime-semiprime candidates. A large
minimum prime addend does not directly control either count. The frozen
three-family comparison in `evidence/raw-margin-adversarial-comparison.json`
did not support using that minimum alone to select unusually small R/M.

## Moving exclusions into the first stage

At fixed N, move one residual event E_r into the presieve. Then

    R_new-R = sum_{s != r} |E_r intersection E_s intersection A0| >= 0.

Represent each multiplicity-two candidate by an edge between its two least
factors. This is a multigraph of ordered candidates. Moving a subset T of
events improves R by the number of edges having at least one endpoint in T:

    R_T = PP - number_of_edges_with_both_endpoints_outside_T.

An edge with both endpoints in T counts once. Summing independent vertex
improvements without subtracting their shared edges would overstate the gain.
Nonempty events need not improve the margin: at N=12, E_3 is nonempty but
has no residual intersection, so moving it leaves R=2 unchanged.

Every edge rs satisfies r^2+s^2<=N. Hence moving all residual r with
r^2<=N/2 covers every edge. The resulting two-stage expression is exactly
R_T=PP=G(N), with no explicit pairwise term. This is a valid alternative
count formula; its positivity is precisely the original Goldbach question.
The enlarged first stage still performs growing arithmetic work.

These transformations help only if they enable an independently stronger
bound or cheaper calculation. Computing the exact covered edges merely
reallocates already-known parts of S2 and is not a new positivity argument.

## The common-factor correction has a uniform absolute bound

If both arguments have the same residual least factor r, then r divides N.
There are at most two such distinct odd prime divisors r>z. Indeed, three
would have product at least (z+1)^3>N-3>=N/2 for N>=6. An odd divisor of an
even N is at most N/2, a contradiction.

For each r, at most N/(2r) odd multiples of r lie strictly between 0 and N.
Thus, without any Goldbach assumption,

    SSsame <= sum_{r|N, r>z, r odd prime} N/(2r)
           <= N/(z+1) = O(N^(2/3)).

In particular this is o(N/log(N)^2). Calling it negligible relative to the
actual M would additionally require a suitable lower bound for M, which
has not been supplied. The bound alone says nothing about PP-SSdiff.

## A density heuristic, explicitly separated from a theorem

For fixed u>1, Buchstab's theorem gives
Phi(x,x^(1/u)) ~ u*omega(u)*x/log(x), where Phi counts integers with no
prime factor <=x^(1/u). Its defining equations give
u*omega(u)=1+log(u-1) for 2<=u<=3. Thus the one-variable fraction of primes
among x^(1/3)-rough numbers tends to alpha=1/(1+log(2)). See Kai Fan,
[Numerically explicit estimates for the distribution of rough numbers,
Journal of Number Theory260 (2024), introduction, pp.121-122](https://stvfan.github.io/files/papers/Numerically%20explicit%20estimates%20for%20the%20distribution%20of%20rough%20numbers.pdf).

If prime/semiprime types at reflected positions behaved independently inside
the rough-pair set, the predicted proportions would be alpha^2 for PP and
(1-alpha)^2 for SS, suggesting

    R/M ~ alpha^2-(1-alpha)^2
        = (1-log(2))/(1+log(2)), approximately 0.1812.

This reflected independence is an additional unproved hypothesis. The
one-variable theorem does not imply it or a positive lower bound for R.
The actual square-start presieve also preserves small primes, so identifying
its pair counts with this model needs its own boundary/error analysis.

A finite abstract countermodel makes the logical gap explicit. Take ten
positions 0..9, reflected by j -> 9-j. Let the rough-labelled set be
Rset={0,1,2,3,4,5}, with prime-labelled subset Pset={0,1,2,3}. Two thirds of
the rough-labelled positions are prime-labelled, yet the only rough/rough
positions are 4 and5, and neither is prime-labelled. There is no Pset/Pset
pair. These are arbitrary labels, not actual primes or a Goldbach disproof;
they refute the inference from a favourable marginal fraction alone.

## Resulting research boundary

The exact sufficient condition remains PP>SSdiff. The density calculation
motivates it but does not prove it. A useful future bound must control the
reflected arithmetic correlation or exploit specific factor structure that
the abstract countermodel does not preserve. No larger numerical scan or
unchanged marginal estimate is promoted as a substitute for that step.

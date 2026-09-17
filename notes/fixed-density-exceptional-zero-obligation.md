# A fixed density margin has an exceptional-zero obligation

Owner: Goldbach research. Parent: `94b6cb8cb7b450c9be154bd1c53cec0ad50e8423`.
Purpose: decide whether our fixed positive-fraction residual target carries
an additional arithmetic burden beyond mere prime-pair nonvanishing.
Novelty: `new-to-this-task` source corollary and transfer, not a new source
theorem or a worldwide originality claim.

## Question declared before computation

Could the ACTUAL cutoff residual approach its full adverse baseline under
a specified exceptional-zero hypothesis, despite the positive composite
sector? If so, a fixed margin is not a neutral reformulation of Goldbach.

Mechanism: lift an exact suppressed residue to the source's range; dominate
central prime-only mass by the nonnegative full Mangoldt pair sum; divide
by the actual singular main. The older exact character calculation, rather
than just the newest sector result, motivates this change of direction.
Changed prediction: sufficiently strong zeros in suppressible conductors
force actual relative density collapse and residual/H tending to -1.
Required analytical bound, with an absolute implied constant, is

```text
0 <= T_N/H(N) << f(eta,D),
f(eta,D) = exp(-sqrt(10 log eta)) + exp(-sqrt(10 log D))
                                      + 11(log eta)^6/eta,       (Goal)
```

at a constructed even N in [D^10,2D^10). Falsifiers: the lifted class does
not kill the SOURCE coefficient; the source range is wrong; the error
cannot be normalized uniformly; or the central/full-pair comparison loses
its inequality. Budget: one corollary, exact target tests, separate review;
no zero search or constant scan. Sleep the claim if any source hypothesis
or normalization cannot be paid. Curiosity, inventive synthesis and
hypothesis preservation checked; no Qwen.

## Definitions and source input

Keep the strict central interval I_N=(N/3,2N/3) intersect Z. Write

```text
T_N = sum_(n in I_N, n and N-n prime) log(n)log(N-n),
H(N) = S_2(N)N/3,
D_R(n) = Lambda(n)-sum_(d|n,d<=R)mu(d)log(R/d),
R=floor(N^theta),                    fixed 0<theta<1/2.
```

All sums are ordered. For conductor D>24 and its specified primitive
quadratic character chi, let F_D be the exact suppressed EVEN classes from
`character_suppression.py`. This includes the choice of character at the
8-part. It is not an actual counterexample set.

Primary input, checked 2026-09-16: Matomaki--Merikoski,
[Theorem 1.4](https://arxiv.org/html/2112.11412v2),
also [published in IMRN 2023](https://academic.oup.com/imrn/article/2023/23/20337/7111993).
For an actual real zero beta=1-1/(eta log D), eta>=10, N>=D^10,
V=log N/log D, fix the source constants C=1 and epsilon=1/10:

```text
W(N) := sum_(n=1)^(N-1) Lambda(n)Lambda(N-n)
      = S_2(N)N b_D(N) + O((N/phi(N))N e),
e = exp(-sqrt(V log eta)) + exp(-sqrt(log N))
                                           + V(log eta)^6/eta,
b_D(N) = 1 + chi(-1) 1_(phi(2^r)|N) (-1)^(N/phi(2^r))
                        product_(odd p|D, p not dividing N)(-1/(p-2)).
```

Here D=2^r D_odd. The implied constant is uniform in D, eta and N.
The accepted CRT calculation in `exceptional_pointwise_bridge.py` proves
b_D(N)=0 exactly on F_D. In particular F_D is empty exactly for the allowed
odd conductors D=1 or 5 modulo 12. This last classification is reused, not
a new theorem of this note.

## Target construction and the conditional estimate

Assume F_D is nonempty. Set M=lcm(2,D), choose any residue r in F_D, and put

```text
N = D^10 + ((r-D^10) mod M),                              (1)
```

where the remainder lies in [0,M). Then N is even, lies in F_D, and

```text
D^10 <= N < D^10+M <= D^10+2D < 2D^10.
```

Thus 10<=V<10+log(2)/log(D)<11, including for odd D. The helper chooses
the first such target among the at-most-24 classes; it does not scan prime
pairs. At (1) the source main is zero, and W(N)>=0 gives

```text
0 <= T_N <= W(N) <= K (N/phi(N))N f(eta,D),               (2)
```

for one source constant K. No proper-power subtraction is necessary for
this UPPER bound: all omitted full-sum terms are nonnegative.

For even N, the Euler products give the uniform normalization

```text
S_2(N)/(N/phi(N))
 = C_2 product_(p|N,p>2) (p-1)^2/(p(p-2)) >= C_2 >= 1/2. (3)
```

For the last elementary bound, the sum of 1/(p-1)^2 over odd primes is at
most (1/4)sum_(k>=1)1/k^2<1/2, and finite products of (1-x) are at least
1-sum x; pass to the limit. Dividing (2) by H proves (Goal), with 6K as a
possible implied constant. Every term of f tends to zero as D and eta tend
to infinity independently. There is no constraint connecting their rates
needed for this implication.

## Two precise consequences

**Conditional actual-arithmetic collapse.** Suppose a sequence of primitive
quadratic characters with nonempty F_(D_j) has real zeros of strengths
eta_j, with D_j->infinity and eta_j->infinity. Then the even targets (1)
tend to infinity and

```text
T_(N_j)/H(N_j) -> 0,
C_(N_j)(D_R,D_R)/H(N_j) -> -1.                           (4)
```

The second line uses the accepted cutoff identity
C(D_R,D_R)=T_N-H+O_(theta,J)(N/log(N)^J), including its paid proper-power
correction. Since H>=N/3, the normalized error tends to zero. It uses
ACTUAL Lambda and ACTUAL cutoff coefficients, not a thinned countermodel.
No such sequence of zeros is asserted to exist.

**A necessary zero exclusion for a fixed margin.** Suppose for some fixed
theta, epsilon>0 and onset N_0 one had

```text
C_N(D_R,D_R) >= -(1-epsilon)H(N)  for all even N>=N_0.     (5)
```

The same identity implies T_N/H(N)>=epsilon/2 eventually. Choose eta_0
so that the two eta-dependent terms in 6K f are <epsilon/4 for all
eta>=eta_0, and choose D_0 so that its D-dependent term is <epsilon/4 and
D^10 exceeds that eventual onset for all D>=D_0. Equations (2)-(3) then
contradict (5) for ANY zero with D>=D_0, eta>=eta_0 and F_D nonempty.
Consequently (5) implies, for these characters and sufficiently large D,

```text
no real zero beta >= 1-c/log D,       c=1/eta_0>0.         (6)
```

Enlarge eta_0 to at least 10. Strict choices in the error budgets exclude
the equality case too. Constants and onset are not evaluated here.
No zero exclusion follows by this argument for F_D empty. No converse
to (6), general zero-free theorem, or new unconditional density bound is
claimed.

The restriction is NOT simply odd characters: even characters can have
F_D nonempty at nonmultiples of D. For example, D=33 has chi(-1)=+1 and
b_D(22)=0, while b_D(0)=2. For D=40 with the positive 8-part, b_D(20)=0
and b_D(0)=2. The exact target lift preserves these residues. These are
character examples, not claimed exceptional conductors.

## Decision and boundaries

Pursuit status: `changed-under-evidence`. A fixed positive-fraction residual
gate is now tied to a specific additional zero-exclusion obligation, with
an explicit conditional sequence reaching its adverse baseline. This is
more than repeating that finite evidence cannot prove an infinite bound.
It changes route selection: the fixed-epsilon gate remains a sufficient
research target, but must not silently become the full prove-or-disprove
objective. A successful existence argument could instead allow a positive
margin tending to zero, provided its errors and proper powers are actually
controlled at that smaller scale. No such argument is supplied here.

This does NOT prove that the fixed-margin bound is false: the requisite
zeros may not exist. It does not prove T_N=0 at any target. Relative collapse
T_N/H(N)->0 does not even imply T_N/N->0 when S_2(N) grows, and must not be
substituted into the second-moment thinning criterion. Central nonvanishing
is itself stronger than unrestricted Goldbach. The earlier conditional
off-F_D coverage and separate eligible-regime coverage remain unchanged.

The composite-sector positivity is compatible with (4); the mixed sector
has already spent it. No sector is counted twice. The unit/Vaughan route,
unproved intersection of signed unit/squarefree masks, q286 missing mass,
Q46189 transfer gap, absolute-remainder and finite-cutoff L2 obstructions,
and both thinning boundaries are preserved. The full pointwise favorable
gate, effective onset, finite remainder, and Goldbach proof/disproof remain
open. The tests check exact class lifting and scope, not zeros or asymptotics.

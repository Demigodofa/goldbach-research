# Signed localization to squarefree pairs and the complementary Mobius sign

Owner: Goldbach research. Parent: `e1272528f2ed1fc1013a359645c4557635033b52`.
Purpose: resolve the nonsquarefree remainder obligation for the actual
cutoff residual's complementary-divisor switch, not assume that remainder
is a prime-power error. Novelty: `new-to-this-task` only.

## Question declared before computation

The older `q286-q46189-complementary-divisor-mapping.md` exposed an outer
Mobius sign on squarefree arguments, but correctly retained a nonsquarefree
caveat. Does the ACTUAL signed residual correlation localize to pairs of
squarefree arguments with a negligible error?

Fix `0<theta<1/2`, `R=floor(N^theta)`, `I_N=(N/3,2N/3) intersect Z`,
and even N. Let `L=1+log N`, `A_R(n)=sum_(d|n,d<=R)mu(d)log(R/d)`,
`D_R=Lambda-A_R`, and `C(f,g)=sum_(n in I_N)f(n)g(N-n)`.
The required analytical bound is

```text
C(D_R,D_R)-C(mu^2 D_R,mu^2 D_R)
  = sum_(n in I_N, n or N-n nonsquarefree)D_R(n)D_R(N-n)
  = O_(theta,J)(N/log(N)^J)       for every fixed J>0.          (Goal)
```

Mechanism: square-divisor inclusion-exclusion, exact forced-prime cutoff
identities, and a cutoff-independent excluded-prime density. Square-divisor
multiplicities carry the summable weight `1/lcm(d^2,e^2)`. Large square
divisors are a sparse tail. The mixed prime/cutoff terms require BV as well.

Changed prediction: the squarefree complementary sign formula becomes a
valid representation of Delta_0 up to a proved negligible aggregate error.
Falsifiers: a nonzero local main in a nontrivial square block, a nonuniform
source use, an unpaid overlap or multiplicity, or a main-scale tail.
Budget: one analytical deduction or falsifier, exact identity fixtures,
and a separate mathematical/source review. No target or constant scans.

Creative tools checked: curiosity, inventive synthesis, hypothesis
preservation. The older squarefree caveat, rather than merely the newest
Type I route, motivates this question. No Qwen is used.

## Inputs and scope

Use Goldston and Yildirim,
[Higher correlations of divisor sums related to primes I](https://math.colgate.edu/~integers/d5/d5.pdf),
Lemma 2.1 (2.11)-(2.12), printed p.16, for j=0,1 with fixed bounds on
`log k/log Y`; the Euler identity (2.25), printed p.18; and ordinary BV
(1.30), printed p.8. These primary inputs were checked 2026-09-16.
No restricted-shift theorem is applied at N. The common-divisor argument
below extends the excluded-prime calculation in
`nonunit-residual-localization.md` to excluded P that need NOT divide N.

We also reuse the accepted parent reduction
`Delta_0=C(D_R,D_R)+O_J(N/L^J)`, where
`Delta_0=T_N-H`, `H=S_2(N)N/3`, and T_N is ordered PRIME-only central mass.
All exponents below are fixed. Constants may depend on theta,J and declared
auxiliary exponents, not on N or the growing divisor indices.

This does not assert small ABSOLUTE nonsquarefree mass, pointwise vanishing,
or simultaneous coprime-and-squarefree localization. Separate signed
exceptional-set estimates do not automatically control their intersection.

## Squarefree projection and the large-square tail

Set

```text
gamma = min(theta,1/2-theta)/8,    G=floor(N^gamma).
```

Thus `2gamma<theta`, `theta+2gamma<1/2`, and `2theta+2gamma<1`.
The exact projector, with squarefree d,e on Mobius support, is

```text
mu(n)^2 mu(N-n)^2 = sum_(d^2|n,e^2|N-n) mu(d)mu(e).          (1)
```

The difference in (Goal) is the NEGATIVE of the expansion over
`(d,e)!=(1,1)`. This retains the overlap when both arguments are
nonsquarefree; doubling a one-sided indicator would overcount it.

For any fixed eta>0, products of a fixed number of divisor functions at
integers <=N are `O_eta(N^eta)`, while `|D_R(n)|<<tau(n)L`. Consequently

```text
sum_(d>G,e>=1) sum_(n in I_N,d^2|n,e^2|N-n)
                  |D_R(n)D_R(N-n)| <<_eta N^(1+eta)L^2/G.    (2)
```

Indeed, absorb the e-divisor count and the residual factors into
`N^eta L^2`, then use `sum_(d>G)floor(N/d^2)<=N sum_(d>G)1/d^2<<N/G`.
The e>G tail is symmetric. This proof does not sum a spurious endpoint
`+1` over every pair up to sqrt N. Choose eta<gamma. It remains to control
the signed blocks `d,e<=G`, `(d,e)!=(1,1)`.

## Exact forced-prime identities on a square block

The constraints `d^2|n`, `e^2|N-n` are compatible exactly when
`gcd(d,e)^2|N`. Otherwise the block is empty. For a compatible block put

```text
P=lcm(d,e),  w=P^2,
u=lcm(d,gcd(e,N)),   v=lcm(e,gcd(d,N)).
```

These are squarefree except w. There is one base residue modulo w.
Within that residue, `gcd(n,P)=u`, `gcd(N-n,P)=v`, including cases where
N has repeated prime factors. A prime dividing both d,e requires its
SQUARE to divide N, not just its first power.

Write `F_S^(P)(x)=sum_(a|x,a<=S,(a,P)=1)mu(a)log(S/a)` for real S>=1,
and zero if S<1. Splitting a squarefree divisor into its P-supported and
P-coprime parts gives exactly, on this progression,

```text
A_R(n)   = sum_(h|u) mu(h) F_(R/h)^(P)(n),
A_R(N-n) = sum_(k|v) mu(k) F_(R/k)^(P)(N-n).                (3)
```

The arguments n,N-n need not be squarefree for (3). The logarithmic
cutoffs R/h and R/k remain real, not rounded. Here `P<=G^2`, so all
cutoffs in (3) are at least `R/G^2`, a fixed positive power of N.

## The excluded-prime density with P not necessarily dividing N

For `R/P<=S,T<=R`, define

```text
K_P(S,T;N)=sum_(a<=S,b<=T,(ab,P)=1,(a,b)|N)
             mu(a)mu(b)log(S/a)log(T/b)/lcm(a,b).
```

Since a,b are coprime to P, their compatible reflected CRT congruences
are independent of the base residue modulo w. Thus

```text
sum_(n in I_N,d^2|n,e^2|N-n)F_S^(P)(n)F_T^(P)(N-n)
  = N/(3w) K_P(S,T;N)+O(S*T).                             (4)
```

The strict-central endpoints are retained. Each compatible CRT count
differs from length divided by period by at most one, and
`sum_(a<=S)|mu(a)|log(S/a)<=S` pays all endpoint errors.

Put `c=gcd(a,b)`, so `c|N` and `(c,P)=1`, and
`W=sqrt(min(S,T))>=sqrt(R)/G`. For `c<=W`, the exact block is

```text
mu(c)^2/c * sum_(b<=T/c,(b,cP)=1)mu(b)/b log(T/(cb))
            * sum_(a<=S/c,(a,bcP)=1)mu(a)/a log(S/(ca)).
```

The inner j=0 GY estimate applies: `bcP<=R*P<=R*G^2` and
`S/c>=sqrt(min(S,T))>=sqrt(R)/G`. Their logarithmic ratio is bounded
in terms of theta,gamma. It gives main `bcP/phi(bcP)` and an exponential
error. Harmonic summation of that error costs at most L^3.

The outer j=1 estimate then leaves the main

```text
(P/phi(P)) sum_(c|N,c<=W,(c,P)=1)mu(c)^2 S_2(cP)/phi(c).
```

Its error is at most `O(L^4 exp(-c_theta sqrt(log N)))`, since
`P/phi(P)<<L^2` and `sum_(c<=W)1/phi(c)<<L^2` on squarefree c.
Both source applications have fixed uniformity ratios, not merely a
separate fixed-P asymptotic.

The discarded original tail c>W is `O(tau(N)L^4/W)`. Extending the main
over all c|N costs at most `O(tau(P)tau(N)^3 L^4/W)`, using
`S_2(cP)<=2tau(c)tau(P)` and `1/phi(c)<=tau(c)/c`.
Finally GY (2.25), or its finite Euler product, gives

```text
sum_(c|N,(c,P)=1)mu(c)^2 S_2(cP)/phi(c)=S_2(NP).
```

Thus uniformly in the required indices and cutoff choices,

```text
K_P(S,T;N) = (P/phi(P))S_2(NP)+O(E_P),
E_P << L^4 exp(-c_theta sqrt(log N))
       +tau(P)tau(N)^3 L^4 G/sqrt(R).                       (5)
```

In particular the main is independent of BOTH cutoffs. The claim is not
that this main vanishes: the alternating cutoff sums will cancel it.

## Cancellation survives the full small-block sum

From (3)-(5), each compatible A,A block has main

```text
N/(3w) * (P/phi(P))S_2(NP)
                  * (sum_(h|u)mu(h)) (sum_(k|v)mu(k)).       (6)
```

This is zero whenever `(d,e)!=(1,1)`: d>1 forces u>1 and e>1 forces v>1.
The block error is bounded by

```text
O((N/P^2)tau(P)^2 E_P + R^2 L^2).
```

For any fixed integer B>=0, the EXACT multiplicity identity is

```text
sum_(d,e squarefree) tau(lcm(d,e))^B/lcm(d,e)^2
  = product_p (1+3*2^B/p^2) < infinity.                    (7)
```

At a prime there are three nonempty membership choices: d only, e only,
or both. This justifies convergence without a growing divisor-count loss
against the exponential error. Discarding compatibility only increases
this positive majorant. Hence the total absolute size of the signed A,A
blocks outside (1,1), for d,e<=G, is at most

```text
O(N L^4 exp(-c_theta sqrt(log N))
  +N tau(N)^3 L^4 G/sqrt(R) + R^2 G^2 L^2).                (8)
```

Each term is `O_(theta,J)(N/L^J)` for every fixed J. This bounds absolute
BLOCK totals after cancellation, not absolute individual products.

## Mixed terms and prime powers

Expand `D_R(n)D_R(N-n)=A_R(n)A_R(N-n)-Lambda(n)A_R(N-n)
-A_R(n)Lambda(N-n)+Lambda(n)Lambda(N-n)` within the same blocks.

In a Lambda,A block with d>1, n must be a proper prime power. Summing all
such incidences costs `O_eta(N^(1/2+eta)L^3)`, using the actual counts
`d^2|n`, `e^2|N-n` and divisor bounds. There is no extra G^2 factor.
The same argument handles Lambda,Lambda whenever `(d,e)!=(1,1)`.

It remains to sum Lambda,A blocks with d=1,e>1. If `(e,N)>1`, a prime
n in the block would divide N, hence be N/2, while `e^2|N-n=n` is
impossible. For `(e,N)=1`, expand A_R(m), m=N-n. Terms with `(h,N)>1`
in that expansion have the same prime impossibility; all these nonreduced
terms are bounded by the proper-power incidence estimate just stated.

For `(e,N)=(h,N)=1`, let `q=lcm(e^2,h)`. The progression `n=N mod q`
is reduced and has main `N/(3phi(q))`. Here `q<=G^2 R` is below a fixed
power less than 1/2. The summed BV errors have multiplicity at most
tau(q)^2, since each e and h divides q, and coefficient at most L.
The weighted BV deduction in `unconditional-residual-type-i-transfer.md`
therefore applies to Lambda: Cauchy and a trivial divisor-moment bound
pay any fixed tau(q) power using a stronger source logarithmic saving.
Only the two central endpoints are needed here. Thus these errors are
`O_J(N/L^J)`; no claim beyond the BV range is used.

For each such e, the exact density main is

```text
N/3 * sum_(h<=R,(h,N)=1)mu(h)log(R/h)/phi(lcm(e^2,h))
 = N/(3phi(e^2)) sum_(k|e)mu(k)
       sum_(a<=R/k,(a,eN)=1)mu(a)/phi(a)log(R/(ka)).         (9)
```

In the split `h=k*a`, `k|e`, `(a,eN)=1`, the forced square means
`phi(lcm(e^2,h))=phi(e^2)phi(a)`, independent of k. GY j=1 has uniform
main S_2(eN) because `R/k>=R/G` and `eN<=NG`, again a fixed logarithmic
ratio. The main cancels by `sum_(k|e)mu(k)=0`. Source errors sum with
`sum_(e squarefree)tau(e)/phi(e^2)<=sum tau(e)^2/e^2<infinity`.
Thus (9) contributes only `O(N exp(-c_theta sqrt(log N)))` in aggregate.
Reflection supplies the A,Lambda bound with all strict masks retained.

Combining (2), (8), (9), the BV errors and the proper-power errors proves
(Goal) for every fixed theta and J in the stated ranges.

## Exact complementary switch on the retained support

For squarefree n>1, the frozen identity
`Lambda(n)=sum_(d|n)mu(d)log(R/d)` and the substitution k=n/d give

```text
D_R(n) = -mu(n) W_R(n),
W_R(n) = sum_(k|n,R*k<n)mu(k)log(n/(R*k)).                  (10)
```

The cutoff is the REAL, argument-dependent n/R. Equality contributes
log(1)=0; it must not become a nonzero endpoint term or a frozen common
cutoff. On nonsquarefree n, (10) is generally false: at n=12,R=3 the
actual D_R is -log 2, while multiplication by mu(12) gives zero.
Nor is W_R always positive: W_3(30)=-log 2.

The new analytical localization, not this identity alone, now licenses

```text
S_sf(N) = sum_(n in I_N, n and N-n squarefree)
             mu(n)mu(N-n) W_R(n)W_R(N-n),
Delta_0(N) = S_sf(N)+O_(theta,J)(N/log(N)^J).                (11)
```

The full nonsquarefree set was not treated as a prime-power set. Its
composite cutoff mass was removed by the signed proof above. This result
concerns the actual cutoff-normalized D_R and does not retroactively
remove the exact nonsquarefree caveat from every older middle-band sum.

The open sufficient estimate remains a pointwise lower bound
`S_sf(N)>=-(1-epsilon)H(N)` for some fixed epsilon>0 and all sufficiently
large even N. No independence of the outer signs and W_R, no favorable
sign, no effective threshold, finite-remainder closure or Goldbach
proof/disproof follows. Q46189 still has no proved transfer to this
complementary product. The previous unit/Vaughan route remains intact;
combining its mask with the squarefree mask would require an additional
intersection argument, not subtraction of two separately signed errors.

Pursuit: `changed-under-evidence`. The nonsquarefree residual obligation
in this particular representation is discharged; the signed squarefree
correlation is not. Preserve q286 missing mass, the absolute remainder
obstruction, finite-cutoff L2 obstruction and both thinning boundaries.
Exact helpers and tests are in `squarefree_residual_localization.py` and
`test_squarefree_residual_localization.py`; they check algebraic identities
and boundaries, not the analytical error rate.

## Validation

Separate fresh-context Sol supplied-proof/source review returned scoped
PASS with no material findings; see `notes/review-receipts.md`. The lead
ran 11 focused tests, 134 combined and 99 optimized affected/adjacent
tests successfully. The reviewer independently ran the 11 focused tests
and 22 parent tests in both modes, compilation, and exact projector,
CRT and Euler probes. No analytical or code correction was required.
The proof above, not the number of fixtures, establishes the asymptotic
claim within its stated scope.

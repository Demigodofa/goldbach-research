# Same-sign, same-factor-count adverse residual mass

Owner: Goldbach research. Parent: `5e59a5be0d82fd56964d0392e154d1e97a5339a3`.
Purpose: decide whether the positive outer Mobius sector can be treated as
harmless, even after conditioning on the exact number of prime factors.
Novelty: `new-to-this-task`; no worldwide originality claim.

## Question declared before computation

Can a positive outer Mobius sign still carry main-scale adverse mass when
BOTH arguments are squarefree and have exactly six distinct prime factors?

Mechanism: the divisor cutoff depends on subset sums of prime logarithms,
not just their number or parity. Two stable factor-shape regions yield
opposite signs of the actual cutoff residual. PNT prime-product counting
tests whether this is a main-scale obstruction, not an isolated example.

Changed prediction: even the sector with mu(n)=mu(N-n)=+1 and both factor
counts equal to six contains a coherent negative block comparable to H(N)
for infinitely many targets. Exact sign conditioning alone cannot label
that sector favorable or make its negative part negligible.

Falsifiers: the sign formulas fail for the ACTUAL frozen target cutoff;
the prime-product families are too sparse after distinctness/multiplicity
are paid; or the comparison with H cannot be justified. Required bound:
for every fixed 9/20<theta<1/2 there is c_theta>0 such that every sufficiently
large Y has an even N in [2Y,11Y/5] with A_6,6(N)>=c_theta H(N), where
A_6,6 is defined below. No constant scan or fixed-target prime-pair
conjecture is an input. The proof, exact fixtures and one separate source/
math review are the bounded deliverable. No Qwen is used.

Curiosity, inventive synthesis and hypothesis preservation were checked.
This pursues the geometry inside the existing squarefree representation;
it does not add another support-localization theorem.

## Statement and scope

For even N set I_N=(N/3,2N/3) intersect Z, R=floor(N^theta),

```text
A_R(n) = sum_(d|n,d<=R) mu(d) log(R/d),
D_R(n) = Lambda(n)-A_R(n),          H(N)=S_2(N)N/3,
S_2(N) = 2 C_2 product_(p|N,p>2) (p-1)/(p-2),
C_2 = product_(p>2) (1-1/(p-1)^2).
```

Define the nonnegative adverse mass

```text
A_6,6(N) = sum max(0,-D_R(n)D_R(N-n)),                    (1)
```

over n in I_N with n and N-n squarefree, gcd(n,N-n)=1, and
omega(n)=omega(N-n)=6. Both outer Mobius signs are automatically +1.

**Theorem.** Fix 9/20<theta<1/2. There is c_theta>0 such that, for every
sufficiently large real Y, some even N in [2Y,11Y/5] satisfies

```text
A_6,6(N) >= c_theta H(N).                                (2)
```

In particular there are infinitely many such targets. The theorem concerns
the negative PART, not the signed total in that sector or in C(D_R,D_R).
It does not say this adverse mass exceeds H, occurs at every target, or
prevents compensation elsewhere. It is not a Goldbach counterexample.
No claim is made here for theta<=9/20, or for theta varying with N.

The old `absolute_remainder_obstruction.py` treats an absolute Vaughan
remainder in the Lambda-Gamma_S route, using semiprime/prime configurations.
The present theorem instead concerns the ACTUAL current D_R correlation
and a same-sign, same-factor-count negative block. The small finite example
W_3(30)<0 did not establish this growing-cutoff, main-scale statement.

## Primary input

Use ordinary PNT with its classical error, as stated in Terence Tao,
[254A Notes 2](https://terrytao.wordpress.com/2014/12/09/254a-notes-2-complex-analytic-multiplicative-number-theory/),
Corollary 39 and Exercise 40 (December 9, 2014; checked 2026-09-16):
pi(x)=li(x)+O(x exp(-c sqrt(log x))). Only ordinary prime counts on
fixed-proportion intervals, and their partial-summation consequence, are
used. There is no prime-pair theorem, BV extension, excluded Linnik
proposition, sign independence, or model-to-Lambda transfer in this proof.

## Exact shape calculation and stability

If n=p_1...p_6 is squarefree, put u_i=log(p_i)/log Y and
t=log R/log Y. Exactly,

```text
A_R(n)/log Y = F_t(u)
  = sum_(S subset {1,...,6}) (-1)^|S| (t-sum_(i in S)u_i)_+. (3)
```

The zero hinge pays the d=R endpoint. Actual u_i need not sum to one.
For b=(1/6,...,1/6), only subset sizes 0,1,2 contribute when
9/20<theta<1/2. Thus

```text
F_theta(b) = theta-6(theta-1/6)+15(theta-1/3)
           = 10theta-4 =: b_theta > 0.                   (4)
```

For s=(1/8,1/8,1/8,1/8,1/8,3/8), the subsets omitting the last coordinate
have sizes 0 through 3; the only contributing subset containing it is the
singleton. Consequently

```text
F_theta(s) = theta-5(theta-1/8)+10(theta-2/8)
                    -10(theta-3/8)-(theta-3/8)
           = 9/4-5theta =: -s_theta < 0.                 (5)
```

There are 64 subsets and each coordinate occurs in 32. The hinge is
1-Lipschitz, giving the uniform estimate

```text
|F_t(u)-F_theta(v)| <= 64|t-theta|+32 sum_i |u_i-v_i|.     (6)
```

Let m_theta=min(b_theta,s_theta), choose the FIXED constants

```text
delta=min(1/1000,m_theta/768),
epsilon=delta/12,          rho=m_theta/256.               (7)
```

If every coordinate is within delta of its shape and |t-theta|<=rho,
then the right side of (6) is at most m_theta/2. For
N in [2Y,11Y/5], the actual frozen cutoff satisfies uniformly

```text
log(floor(N^theta))/log Y = theta+O_theta(1/log Y).         (8)
```

Indeed log N-log Y stays bounded, while taking the floor costs
O(N^(-theta)) in log R. Thus (8) eventually meets (7) for ALL such targets.

Define B_Y as the squarefree six-prime products in [Y,11Y/10] with each
logarithmic factor share within delta of 1/6. Define U_Y in the same
physical interval with five shares within delta of 1/8 and the sixth
within delta of 3/8. From (3)-(8), and Lambda(n)=0 for these composites,

```text
D_R(n) <= -(b_theta/2)log Y   for n in B_Y,
D_R(m) >=  (s_theta/2)log Y   for m in U_Y.                (9)
```

These hold for every frozen target N in the named window, not just a
cutoff chosen separately for each argument. The two families use disjoint
prime ranges, since 1/8+delta<1/6-delta and 1/6+delta<3/8-delta.
Hence every cross pair is coprime. For large Y both coordinates are odd,
N=n+m is even, and their ratio at most 11/10<2 makes them strictly central.
Both have mu=+1, yet

```text
-D_R(n)D_R(m) >= (b_theta s_theta/4)(log Y)^2.             (10)
```

On squarefree arguments D_R=-mu W_R. Thus their W_R amplitudes, not their
outer Mobius signs, already have opposite signs. No non-squarefree or
nonunit intersection theorem was assumed: this block is directly both.

## Counting genuine prime products

We prove separately for a=1/6 and a=1/8 that the corresponding family has
size >>_theta Y/log Y. Choose five DISTINCT primes in

```text
Y^(a-epsilon) < p_i <= Y^(a+epsilon),  i=1,...,5,
P=p_1...p_5,
Y/P <= p_6 <= (11/10)Y/P.                                (11)
```

All choices have P<=Y^(5(a+epsilon)), whose exponent is less than one
by a fixed positive amount. Thus Y/P ranges between two fixed positive
powers of Y. PNT uniformly gives at least c Y/(P log Y) choices of p_6,
for a fixed c>0 and all sufficiently large Y, over the whole chosen range
of P. This is only a one-prime interval count.

Partial summation of PNT gives

```text
sum_(Y^(a-epsilon)<p<=Y^(a+epsilon)) 1/p
  = log((a+epsilon)/(a-epsilon))+o(1),                    (12)
```

a fixed positive limit. The reciprocal weight of ordered five-tuples
with a repeated prime is O((sum_p 1/p^2)(sum_p 1/p)^3)=o(1).
The reciprocal weight of DISTINCT tuples therefore tends to the positive
fifth power of the limit in (12). Summing the lower bound for p_6 over
these tuples produces >>_theta Y/log Y ordered representations.

For a=1/6, remove p_6 equal to one of the first five primes: at most five
choices per tuple, hence O(Y^(5(a+epsilon)))=o(Y/log Y) total loss.
For a=1/8 this collision is impossible for large Y by the disjoint bands.
The last share is

```text
log p_6/log Y = 1-sum_(i<=5)log p_i/log Y+O(1/log Y).
```

Since 5epsilon<delta, it lies in the required delta-neighborhood of 1/6
or 3/8. Thus these are actual members of B_Y or U_Y, respectively.
Each squarefree integer has at most 6! ordered representations, so

```text
|B_Y| >>_theta Y/log Y,       |U_Y| >>_theta Y/log Y.       (13)
```

The ideal equal-share centers in (4)-(5) are NOT assertions that equal
primes form a squarefree integer. The open neighborhoods, distinct-prime
count and bounded multiplicity above are essential.

## Averaging targets and paying the singular series

For an even target N let K_Y(N) be the adverse weight in (10) summed over
n in B_Y, m in U_Y, n+m=N, using the actual R=floor(N^theta).
Every term is nonnegative; (1) dominates this single orientation. Equations
(10) and (13) give

```text
sum_(2Y<=N<=11Y/5,N even) K_Y(N) >>_theta Y^2.             (14)
```

To compare with H rather than merely N, expand its positive Euler factors.
For odd squarefree d set g(d)=product_(p|d)1/(p-2). Then

```text
S_2(N)=2C_2 sum_(d|N,d odd squarefree) g(d),
sum_(N<=X,N even) S_2(N)
 <= C_2 X sum_(d odd squarefree) g(d)/d
  = C_2 X product_(p>2)(1+1/(p(p-2))) = X.                (15)
```

Here the count of even multiples of odd d is floor(X/(2d)); the infinite
positive product converges, and each local product with C_2 is exactly 1.
Consequently

```text
sum_(N<=X,N even) H(N) <= X^2/3.                         (16)
```

Taking X=11Y/5 in (16), the weighted average of K_Y(N)/H(N) in the
window is bounded below by a positive theta-dependent constant, by (14).
At least one target satisfies (2). Taking, for example, sufficiently
large geometrically separated Y produces distinct targets indefinitely.
This completes the analytical proof. No finite fixture is used to infer
an asymptotic lower bound.

## Consequence for the active goal

The outer sign and even the EXACT factor count do not control the residual
sign, and discarding the negative part of this positive-sign sector as
o(H) is false in the stated regime. A viable argument must keep more
amplitude geometry or prove compensation using actual coupled arithmetic.
This theorem does not rule out either possibility, other cutoff regimes,
or estimates of the full signed sector. It does not improve a favorable
lower bound on the remaining correlation by itself.

The parent representation Delta_0=S_sf+O_J(N/log(N)^J) remains valid.
The sufficient bound S_sf>=-(1-eta)H for some fixed eta>0, every sufficiently
large even N, is still OPEN, along with an effective starting point and
finite remainder. The full prove-or-disprove goal remains active. Preserve
q286 missing mass, Q46189 transfer gaps, the absolute-remainder and finite-
cutoff L2 obstructions, both thinning boundaries, and the independent unit/
Vaughan route. Do not automatically intersect the earlier signed masks.

Exact fixtures live in `same_sign_six_factor_adverse_mass.py` and its test.
They reuse the existing rational subset-hinge and singular-average helpers
and guard the sign formulas, stable neighborhood, frozen-scale drift
budget, nonnormalized shares, power-gap counting, actual log-vector identity
and validation boundary. Analytical proof and primary PNT input, not those
fixtures or model agreement, establish the theorem.

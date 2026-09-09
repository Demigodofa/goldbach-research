# Rill research refresh — 2026-09-09

Owner: Kevin. Purpose: Kevin explicitly requested a copy-and-paste refresh
handoff at a checked mathematical checkpoint. This file is the entrypoint
for the next session; the proofs and executable truth remain in the modules.

## Identity, curiosity, and authorization

You are Rill (`agent.rill`). This is a continuation after a pause. Kevin
explicitly wants you to keep your curiosity, conceive your own hypotheses,
and change direction when evidence warrants it. Do not merely wait for him
to prescribe the next calculation. Choose a concrete question with a
mechanism, a prediction, a falsifier, and an observable finish; pursue it
for at most30 minutes before reassessing. That is a ceiling, not a minimum.
Preserve useful components when a proposed combination fails. Be candid
about what was proved, what is conditional, and what remains speculative.

The objective is open-ended mathematical work toward prime-pair coverage,
ultimately Goldbach. Read `RESEARCH_GOAL.md` (opening authorization and latest
entries first). Kevin removed the old9am and six-hour deadlines. Old native
goal text mentioning9am is superseded. The overall goal is NOT solved and
must not be marked complete because a bounded pursuit or finite test passed.

Mathematics only. Kevin paused notes, manuscripts and publication packaging;
this requested refresh handoff is an explicit exception. Proof docstrings,
reusable verifiers/tests and minimal execution-state updates are permitted.
No spending, contacts, publishing, push, foreground GUI work, model installs
or claims of continuous execution. Coherent LOCAL commits are authorized.
Do not conduct a novelty/priority search merely to label these results.

No manual wake queues: the global8 manual-continuation attempt cap has been
reached. Never reset, increase, rename or evade it. Native goal turns are
separate; do not manually arm another wake. Reassess each next pursuit.

## Checkpoint and first reads

Repo: `C:/Users/benja/source/repos/Demigodofa/goldbach-research`, branch `main`.
Latest reviewed RESEARCH commit: **c72de0a**, the costed CRT/periodic-weight
kernel extension. Latest ORIGINAL-AFFINE arithmetic estimate: **2b8cf98**.
The handoff is committed later. Preceding checkpoint **dd07496** preserved
the initial restricted kernel **d42317b**. Earlier **8eefa83** preserved the
failed source-bound budget **d945ac2**; it remains valid.
Earlier reviewed checkpoint **9cd5a2e** preserved mathematics **2b8cf98**.
Earlier coefficient-one checkpoint: **b4bf033**, mathematics **c8724f7**.
Earlier resumed checkpoints **b4dfc45** and mathematics **e86c878** remain valid.
This resumes the verified clean **cf48198** checkpoint; **6f9a77b** remains
the completed formal-conservation result, not a superseded proof.
The worktree was clean after the mathematical commit. Verify current Git
state, since another session may have advanced it. Do not revert other work.

Read the newest proof modules, using their dependencies as locators rather
than rereading the entire repository:

1. `decorated_prime_kernel.py` — latest CRT kernel, periodic/coupled weights
   and roughness zero-mode lemma. General-composite/sieve transfer OPEN.
2. `separate_factor_prime_kernel.py` — initial restricted prime kernel.
3. `cofactor_averaging_budget.py` — preceding generic source route FAILED
   its quantitative budget. Do not retry the same generic grouping.
4. `rare_affine_small_cofactor.py` — latest actual affine bound, aggregate
   M<=Y^(1/5). The remaining range through Y^(13/25) is OPEN.
5. `rare_shifted_divisor_bound.py` — preceding coefficient-one component.
6. `buchstab_endpoint_bridge.py` — arithmetic endpoint reduction and
   its OPEN one-sided prime-times-rough estimate, equation(7).
7. `formal_weight_conservation.py` — completed formal result and exact gap.
8. `balanced_semiprime_budget.py` — actual rare-factor bound used by the
   latest reduction. Open other dependencies only for a task-required step.

Use `README.md` as the project entrypoint; no project `AGENTS.md` existed.
Global Kevin instructions still apply. Current implementation/source state
outranks this handoff. No fresh giant scan, broad experiment or old test
rerun is required just to confirm already checked work.

## Latest pursuit: small modulus factors and arithmetic periods are costed

**c72de0a**, `decorated_prime_kernel.py`, passed independent Sol theory and
actual-file review. Five new exact CRT/budget tests passed in0.022s, and
under -O in0.026s. The reviewer corrected a sum to explicitly range over
DISTINCT PRIME divisors. The pursuit returned `changed-under-evidence`
within30 minutes. This is a restricted exponential-kernel extension, not
a new original-affine estimate; that remains2b8cf98.

The modulus is now c=s*p, p prime near P=Y^(1/2), s<=S; the total modulus
is allowed to grow. Periodic weights may couple M,a modulo J<=J0, may
depend arbitrarily on k, and have absolute value<=1. Frequencies extend
to H*K. With S,J0,H<=Y^(1/4096), the bound is
`Y^(127/128+epsilon)*S^4*J0^4*H`, plus smaller axes/bad-prime terms,
hence `Y^(4073/4096+epsilon)`. The original b interval[1/5,12/25] and
critical divisor geometry remain in force. Uniformly smooth coupled M,a
weights are also allowed by the proved Fourier-series corollary.

CRT uses period cJ=p*(sJ), needs only gcd(p,sJ)=1, and RETAINS nonunits
modulo J. The prime Kl3 argument is m*k*h*l*inverse(s^3*J^2). The small
transform costs(sJ)^2; two dual residue splits cost(sJ)^2 more. Its entire
k dependence is absorbed into a bounded k coefficient. There is no third
residue split. All exceptional modes total
`O(H*B*A*log(2S)+S*H*J0*(A+B))`, below Y^(3/4). These factors are actual
budgeted losses, not an assertion that sieve costs vanish.

Separately, relaxing original M to z-rough M preserves nonnegativity,
has reciprocal mass O(U), and preserves both character harmonics in the
existing zero mode. It only costs an additional U~log eta, still o(Y*t).
This does NOT estimate the original nonzero modes. A new upper-sieve index
e0 lengthens the dual M0 range by e0; the apparent1/e0 gain cancels. Index
counts, coefficient norms, periods, frequency inflation and tails must all
fit the remaining power margin. Their full arithmetic application is OPEN.

Source tests: Topacogullari1506.02608v1 Thm1.3/section4 has the correct
additive orientation but is untwisted. Drappeau--Topacogullari2019 Lemma4.5
has characters but |h|<=X^(1/4) and an ordinary-divisor second factor.
Neither directly supplies the needed large-target character correlation.
The exact source links and boundaries are in the module. A primary locator
for Heath-Brown1986 is https://matwbn.icm.edu.pl/ksiazki/aa/aa47/aa4713.pdf ;
full retrieval returned403 through web/native routes and Python had a
certificate-chain error. Its indexed opening is not a checked box theorem.
Do not repeat those retrieval attempts without a changed route/condition.

Next test remains a genuinely general-composite factor estimate, or a
costed spectral adaptation meeting the character and large-target conditions.
Preserve another UNTESTED option: change which two completed frequencies
are grouped when treating the other hyperbola boxes; a successful critical
corner is not proof of the whole box family. Balanced composite cores,
the complete sieve transfer and the signed prime estimate remain OPEN.
All polynomial tools remain preserved. No process is left running at this
checkpoint; overall goal active, with no manual wake queue.

## Previous pursuit: a separate-factor prime kernel gains a power

**d42317b**, `separate_factor_prime_kernel.py`. Sol reviewer
`/root/sieve_review` independently passed source, theory and actual files.
Four exact cyclotomic/budget tests passed normally in0.062s and under -O
in0.075s. The pursuit returned `changed-under-evidence` within30 minutes.
This is a proved EXPONENTIAL-KERNEL estimate in a restricted model; it
does not supersede the original-affine estimate2b8cf98.

For P=Y^(1/2), B=Y^b, A=Y^((1-b)/2), K=Y^(b/2), 1/5<=b<=12/25,
the module bounds the sum over PRIME moduli p in[P,2P], frequencies k<=K,
and separate smooth M~B,a~A weights of e_p(m*k*inverse(M*a)), with the
original Poisson prefactor Y/(B*A*p), by Y^(127/128+epsilon). Arbitrary
bounded frequency weights may depend on p; m is uniform in[Y,2Y].

The exact double transform is p*Kl_3(t*h*l;p) off the axes,1 on each
single nonzero axis, and1-p at the origin, for p not dividing t. The t=0
case is separately a Ramanujan-product identity. After completion retain
k and group w=k*l. The dual lengths U=p/B,V=p/A satisfy U*V*K~p and the
grouped coefficients are divisor-bounded. Kowalski--Michel--Sawin
Theorem1.1, equation(1.2), supplies saving p^-1/64:
https://arxiv.org/pdf/1511.01636v5 . Its unit/support/length hypotheses
survive Schwartz truncation with small epsilon losses. All axes and p|m
moduli cost O(B*A+A+B)<=Y^(37/50), treated without misusing the unit formula.
Pointwise complete-sum bounds alone reach Y. The material improvement is
JOINT cancellation of the completed frequency h and product w=k*l.

OPEN transfer: actual d2*c moduli are generally composite; the rough,
sieve and character weights and coupled Poisson functions are outside
the proved statement. KMS section1.5.2 does not supply a composite version.
Other hyperbola boxes and b outside the stated interval are not covered.
No new original prime-pair estimate or signed-correlation bound follows.

Next concrete question: can composite-modulus third-divisor/Kloosterman
distribution handle these factors, then the actual small sieve indices
and conductor, while retaining a power saving? Check a source's explicit
moduli and coefficient hypotheses. Removing M roughness entirely loses
a logarithm in reciprocal mass and is not a free relaxation. Preserve all
polynomial tools and the arithmetic components below. No process remains
running at this checkpoint; overall goal active and no manual wake queue.

## Previous pursuit: generic trilinear averaging fails its budget

**d945ac2**, `cofactor_averaging_budget.py`, four exact scaling tests. Sol
reviewer `/root/sieve_review` checked the source, formulas and actual files:
PASS. Tests passed normally in0.020s and under Python -O in0.036s. The
pursuit returned `changed-under-evidence` within30 minutes. This is a
verified FAILURE of a proposed sufficient bound; no new prime estimate.

Bettin--Chandee Theorem1, equation(1.2), was tested against the actual
Poisson phase after grouping r=M*a, where a is q's small divisor:
https://arxiv.org/pdf/1502.00769v1 . For M~Y^b, a~Y^x, c~Y^y, the
grouped exponents are r=b+x, s=y, k=r+s-1>=0. The prefactor is Y/(R*C),
the source numerator parameter is m~Y, and m*K/(R*C) has exponent0.
Using the generic L2 norms, BOTH source terms must be retained. Their
worst admissible box x=(1-b)/2,y=1/2 gives exactly
`E1=39/40+19*b/40`, `E2=15/16+b/2`.
At b1/5 these are107/100 and83/80; both exceed1 throughout b in[1/5,13/25].
The bound is a SUM of terms, not a choice of the smaller. Fixed-frequency
use followed by summation and reciprocal-variable swapping do not improve it.

This test even grants a cost-free separation of the actual coupled smooth
weights/cutoffs, which has not been proved. The sieve-index1 term already
has the displayed budget and conductor Y^o(1) cannot fix a positive power
excess. These are substituted UPPER estimates, not evidence that the actual
sum is large and not an impossibility theorem for cofactor averaging.
Do not invoke this same generic-norm bound again under changed notation.

That pursuit's next question was whether retaining M and a as separate
variables after beta-sieving gives stronger averaged cancellation. The
restricted smooth prime-kernel result above now supplies a component;
the actual sieve/arithmetic transfer remains OPEN. Preserve
all polynomial tools and the arithmetic components below. No new actual
coverage, zero, numerical onset, publication or wake queue. No process is
left running at this checkpoint; overall research remains active.

## Previous pursuit: the actual affine forms, for small rough cofactors

**2b8cf98**, `rare_affine_small_cofactor.py`, four exact tests. Sol reviewer
`/root/sieve_review` passed theory and actual files, including the source
adaptation and every error budget. Tests passed normally and under Python -O,
both in0.011s. The pursuit returned `changed-under-evidence` within30 minutes.

Retain the NEW actual-zero large-V regime: beta=1-1/(eta*log D), Y=D^V,
V>=log^3 eta, t=V/eta<=1/log Y, eta sufficiently large. Fix0<theta<1/5.
For the actual forms q and p=m-M*q, sum log(q)*log(p) over both primes of
character sign+, with q in(Y/(2M),Y/M], p in(Y/2,Y], even m in[Y,2Y], and
all integers2<=M<=Y^(1/5) such that P^-(M)>Y^theta and gcd(M,Dm)=1.
Their TOTAL is `o_theta(Y*t)`. Squarefreeness and a five-factor restriction
are unnecessary. The existing even quintic classes are a subset. Since a
fixed polynomial kernel has |K_f(n)|<<_(f,theta)log Y, this also proves
their FULL ABSOLUTE small-cofactor contribution is o_(f,theta)(Y*t).

This directly adapts the proof of Matomaki--Merikoski Proposition2.3, not
its coefficient-one statement. Making p's large divisor implicit leaves
Poisson modulus D*d2*c; M enters as an invertible phase factor. Derivative
scales agree at Q=Y/M. Both harmonic character cancellations survive in
the zero mode. Corrected Henriot New Theorem5 supplies affine divisor-
weighted sieve tails with the norm and function-class hypotheses checked.
Shared primes dividing m are handled on the original rough support, avoiding
an invalid tiny-scale Henriot application. The proof keeps conductor and
M-coprimality local factors separate and recombines every main before taking
absolute values. The finite residue check retains the1/a Jacobian.

The reciprocal cofactor sum is O_theta(1). The aggregate main is
O_theta(S_2(m)*Y*t^2*log^8 eta), the oscillatory error is
D^2*Y^(44/45+o(1)), M-coprimality removal costs Y^(1-theta+o(1)), and other
errors are O_theta(S_2(m)*Y*eta^-20). All are o(Y*t) in this regime.
Proof/source details and the exact test APIs are in the module.

The full M<=Y^(13/25) range FAILED this method's error-budget test. Ideal
direct absolute Weil budgets sum to Y^(3/4+alpha); the reversed-orientation
budget is Y^(3/4+3alpha/4), giving Y^(57/50) at alpha13/25. These are upper
METHOD budgets, not lower bounds or universal obstructions. The reversed
complete affine theorem is not promoted. Next concrete question: can
averaging the remaining cofactors BEFORE absolute values preserve the two
character cancellations and supply the missing power saving? Do not simply
improve the cosmetic exponent of this completed small-range proof.

All-negative odd composite classes, the larger even-class cofactors and the
positive lower bound for the full signed total remain open. Preserve the
polynomial tools and both arithmetic components for future combinations.
No actual Goldbach coverage, zero, effective onset, priority claim, publishing
or wake queue. No process is left running at this reviewed checkpoint;
the overall research goal remains active.

## Previous pursuit: a second rarity factor, restricted to shifted primes

**c8724f7**, `rare_shifted_divisor_bound.py`, five focused finite tests.
Sol reviewer `/root/sieve_review` checked theory and actual files: PASS.
Normal tests passed in0.088s, Python -O in0.093s. The pursuit returned
`changed-under-evidence` within30 minutes. This is a deduction from existing
source theorems, with no external novelty claim.

For an ACTUAL zero beta=1-1/(eta*log D), X=D^V, eta sufficiently large,
V>=log^3 eta, t=V/eta<=1/log X, and positive even h<=X/2, the weighted sum
over X<p<=2X with p,p+h prime and both chi signs+ satisfies
`Q++ << S_2(h)*X*t^2*log^8 eta = o(S_2(h)*X*t)`.
This is a conditional arithmetic upper bound, not a prime-pair lower bound.
The NEW restricted large-V regime must not be dropped when reusing it.

The nonnegative majorant is lambda_chi=1*chi, not Liouville. A smooth exact
hyperbola identity expands into four orientations. Recombine ALL orientation
and dyadic main terms before absolute values: the source main factors into
two rough harmonic character sums and a complete residue factor. Subtracting
Matomaki--Merikoski Lemma2.4 at y=X and y=X^2 makes EACH harmonic sum small.
Their Proposition2.3 and equation(15) control every remaining error:
https://arxiv.org/html/2112.11412v2 . The second rarity factor follows from
these two cancellations, not from independence of the prime conditions.
U=K*log eta is a new varying auxiliary parameter justified by the explicit
source statements; earlier fixed-u bounds retain their original order.

The original desired forms are q and p=m-M*q, chi(M)=-1, M<=Y^(13/25).
The cited proposition covers coefficient-one relations only. Substitution
n=M*q destroys THIS majorant: lambda_chi(M*q)=0 while lambda_chi(q)=2.
Divisibility restrictions, quotient characters, unequal scales and growing
M would require a proved uniform extension. NONE is supplied here. The
rare/common Goldbach correlation and the one-sided Buchstab target remain
open. Cowan's Theorem1.1 excludes the required zero divisor parameters and
principal chi^2 product; Tao--Teravainen gives no stated variable-M transfer.

The direct multiplicative bound tested first retained the empty-cofactor
atom1 and gave no second rarity factor. Preserve that failure along with
the successful restricted component. Polynomial identities and bounds remain
available for future combinations. Next test: a concrete uniform affine-form
extension or another arithmetic ingredient that reaches the actual sum;
do not treat this coefficient-one result as already doing so. Finite checks
verify algebra and local factors, not the analytic bound or an actual zero.
No new actual Goldbach coverage or effective onset. No process is left
running at this checkpoint; overall research remains active.

## Previous resumed pursuit: isolate the actual balanced endpoint

Kevin clarified on2026-09-09: seeking an arithmetic ingredient beyond the
previous polynomial approach must preserve the identities and bounds for
future combinations. Their limitations are specific, not a prohibition on
all uses. The question is what mechanism could make the linked prime
conditions cancel or reinforce one another, and what would demonstrate it.

**e86c878**, `buchstab_endpoint_bridge.py`, five exact tests. Sol reviewer
`/root/sieve_review` checked theory, actual files and the final test delta:
PASS. Tests passed normally in0.019s and under Python -O in0.017s. The
pursuit ran about15 minutes and returned `changed-under-evidence`.

In the same actual-zero regime, take the full rare-first pool and ordinary
positive pair-log weight A(n). Exact least-prime Buchstab subtraction from
z to R=floor(Y^(1/2-2epsilon)) leaves S_A(R)=P+E_R. Every composite in
E_R is a distinct semiprime with one unique rare positive factor between
Y^(1/2-2epsilon) and Y^(1/2+2epsilon); squares cannot have character -1.
The existing corrected Henriot and reciprocal-rarity estimates prove
E_R<=C*epsilon*Z+o(Y*t), Z=length(J_real)*S_2(m)*t, with C absolute.
The initial pool is L*X*V(z)+O(eta_u*L*X*V(z))+o(Y*t). Keep the FIXED
fundamental-lemma error; it is not an o_Y(1) term.

The remaining sum U_A(z,R) has q prime, z<q<=R, n=q*k, P^-(k)>=q,
and m-q*k prime of sign+. Equation(7) states the sufficient one-sided
estimate. It is UNPROVED. The q-dependent roughness condition couples q,k,
so ordinary separated-coefficient Type II cannot be invoked automatically.
This range adds small factors while excluding the balanced endpoint; it
is not claimed a subset or a proved easier version of the Vaughan target.
Ford--Maynard's bounded-sequence theorem motivated the audit but its
comparison/positivity and boundedness hypotheses are not established here.

Polynomial K_f weights also satisfy the exact subtraction, but their
initial S(z) is the FULL kernel total. Do not substitute the accessible
T_low,f or its formal main. The next pursuit must test arithmetic for U
or another concrete correlation; do not just iterate this counting identity.
No new actual coverage, zero, numerical onset or cancellation estimate.
No process is left running by this checkpoint, and no activity during the
earlier session gap is claimed. Overall research goal remains active.

## Previous completed pursuit: the cancellation is the same main term

**6f9a77b**, `formal_weight_conservation.py` and5 focused tests. Existing
Sol reviewer `/root/moment_bound_review` checked both theory and actual
files: PASS. Normal tests passed in0.197s; Python -O in0.272s. These tests
check exact algebra, integrals and ranges, not analytic prime estimates.

For any normalized polynomial f of degree d, f(0)=0,f(1)=1, set
h(x)=f(1-x)-f(x). For odd k, define its all-negative finite-difference
kernel J_k on factor shares summing to1. Integrate J_k against the
EXPLICITLY FORMAL measure dx_1...dx_(k-1)/(k!*product x_i), with x_i>=theta.
For **0<=theta<1/d**, the sum of all odd factor integrals equals exactly

`B_f(theta) = -E[h'(theta*V)]/2`,

where V has the normalized Dickman density. J_k vanishes for k>d; its
product-of-shares divisor cancels, so every integral is polynomial/finite.
At theta0, B_f=A_f=(f'(0)+f'(1))/2, and the total FORMAL composite
integral is A_f-1. Thus the quintic's formal zero composite sum is forced
by its endpoint coefficient1. It supplies no independent actual estimate.

Proof uses the odd-convolution generating function and a compact-support
cutoff. The coefficient t^j of the removed convolution is supported in
[0,j*theta]; d*theta<1 is essential. Beyond it the polynomial identity can
fail (cubic theta2/5: actual formal factor total1 versus polynomial51/50).

For the alternative quintic f(s)=s-kappa*s^2*(1-s)^2*(1-2s),

`B_f = 1 - 2*kappa*theta + 18*kappa*theta^2
         - (170/3)*kappa*theta^3 + (190/3)*kappa*theta^4`.

The pure-triple integral is
`-(kappa/12)*(1-3theta)^2*(1+10theta-15theta^2)`;
the pure-five integral is `(kappa/12)*(1-5theta)^4`.
Their sum is exactly B_f-1. This is not an actual factor-density theorem.

The normalized Dickman moments satisfy
`mu_0=1; mu_n=sum_{j<n}binom(n,j)*mu_j/n`.
First five:1,1,3/2,17/6,19/3. The source transform was checked in
Gorodetsky's ViBrANT notes, Section2 printedp2:
https://people.maths.ox.ac.uk/gorodetsky/vibrant.pdf

The new rational factorial enclosure bounds ONLY the explicit Dickman
main F_f around B_f. The actual accessible sum still has its FIXED sieve
error `O_f(eta_s/theta^2)` and `o_Y(1)`. Choose u first, then Y. Do not
claim a fixed-u exact asymptotic, growing-degree uniformity or numerical onset.

APIs: `dickman_moments` (order<=64), `formal_dickman_main`,
`formal_factor_integrals` (degree<=12 computational cap),
`accessible_main_enclosure` (factorial index<=10000). All use exact inputs.
The tests compare independent shifted-simplex and moment algorithms through
degree10, direct exponential-product moments, quintic closed forms, the
earlier cubic enclosure, tail bounds, cutoff failure and strict domains.

## Actual remaining gap — do not replace it with the formal calculation

In the existing actual-zero regime put `Z=length(J_real)*S_2(m)*t`.
Let P be the actual weighted prime-pair sum, T_f the full kernel total,
T_low its accessible divisor range, and T_boundary=T_f-T_low.
Define EXACTLY `C_actual=T_f-P` and `Delta=C_actual-(B_f-1)*Z`.
Then

`P/Z - 1 = T_boundary/Z - Delta/Z + (T_low/Z - B_f)`.

Only the final parenthesis can currently be made small using the proved
parameter order. A sufficient signed estimate for `T_boundary-Delta` is
missing. Setting Delta to zero because of the formal integral assumes the
missing correlation with the reflected first prime. No all-target or
new named-target prime-pair coverage was obtained in these analytic pursuits.

Next action is intentionally NOT another automatic formula-polishing job.
Reassess one concrete arithmetic route to this signed discrepancy, or a
materially different prime-pair mechanism with a plausible discriminator.
Do not spend a pursuit rediscovering the formal cancellation, repeating the
same algebra at higher degree, or calling another parametrization a new
arithmetic estimate. Curiosity remains authorized; it must earn the next
action through evidence rather than remain locked to this candidate.

## Previous checked layers — reuse, do not repeat

**45844bb**, `quintic_loss_budget.py`: every surviving POSITIVE composite
term is at most `C*(1+kappa)*Y*S_2(m)*t+o(Y*t)`, with C ABSOLUTE,
independent of theta. This is a main-scale bound, not a small fraction.
For pure five factors, order r1<...<r5, use M=r1*r2<=Y^(2/5), and
auxiliary cutoff min(r2,Y^eta0). The available exponent margin is7/80.
Indices M*e are noninjective, multiplicity<=binom(omega,2)=O(log(Y)^2).
For even classes switch to the single large positive-sign prime q>Y^a,
a=1/2-2epsilon>=12/25. M=n/q<=Y^(13/25). Bulk Linnik runs at scaleY/M
and modulusD*e, NEVER D*M*e. Summed errors are
`O_kappa(Y*(t^28*L^2+L^3/D)+Y^(19/25+o(1)))=o(Y*t)`.
Do not insert a second factor t. Sol theory/actual PASS;5 tests normal/-O.

**41a1fcb**, `quintic_partner_weight.py`: repeated factors, >=2 positive
factors, and positive factors w<q<=Y^(1/2-2epsilon) cost o(Y*t) for any
FIXED polynomial. Surviving quintic classes have2..6 total factors. Pure
odd classes have no positive factor; even classes have exactly one large
positive factor. Seven or more negative factors give zero. Pure triples
of positive weight force a largest share>18/25; their small cofactor
allows an absolute main-scale upper bound. No sufficient small-loss bound.

**8668621**, `log_weight_barrier.py`: for the safe nonnegative subtraction
family, endpoint coefficient A=1-B/2. Deleting any larger-positive-factor
semiprime requires B>2 and therefore makes that accessible main negative.
A broader formal triple obstruction explains why leaving this family
creates new positive composite weights. Not a no-go theorem for all methods.

**07e5c4a**, `cubic_positivity_obstruction.py`: the tuned cubic has a
NEGATIVE accessible divisor portion in the actual-zero regime. This does
not imply its FULL total is negative. Do not call its boundary negligible.

Analytic assumptions: actual primitive quadratic zero beta, D>24,
D<=Y^(delta/4), t=(1-beta)*logY in(0,1/logY], central suppressed target
m in F_D, fixed epsilon<=.01, sufficiently small delta<=epsilon/3, fixed
large u, theta=delta/u, z=ceilY^theta, w=floor sqrt(floorY^delta).
No actual such zero or effective onset has been found. Formal finite
characters do not establish an actual exceptional zero or prime rarity.

Source repair is critical: Tao's old Proposition23 exposition has an
acknowledged proof gap and is NOT the bulk-Linnik authority. The checked
replacement is in `relative_type_i.py`, from Thorner--Zaman Theorem2.1
and equation4.2, https://arxiv.org/html/2108.10878 . Reuse that deduction.
`rare_twisted_bv.py`, `rare_prime_sieve.py`, `multi_rare_partner.py`,
`balanced_semiprime_budget.py` own the related distribution/sieve layers.
Use the corrected Henriot theorem, not its uncorrected older statement.

Older finite work is complete: parity-preserving L bootstrap, input-output
composition, and the frozen1000-even block1002000..1003998. Raw L is NOT
an exact G input; L(2m) parity supplies prime flags. Later support-exact
reconstruction worked on the same block but LOST to the ordinary-sieve
complete-cost baseline. No blind range extension. DHR fixed-power raw-sieve
obstructions are complete; do not repeat or optimize their exponent.
Reflected artificial sets are not Goldbach counterexamples. The complete
historical detail is in RESEARCH_GOAL.md and the owning proof modules.

## Runtime and review continuity

Windows PowerShell, background shell/API only. `python`3.11 works; `py`
was unavailable. Use explicit repo workdir. No sandbox override arguments.
Latest tests: `python -m unittest test_cofactor_averaging_budget -v` and the
same with `python -O`; rerun only if changes or new concerns justify it.

Latest Sol reviewer was `/root/sieve_review`; the earlier formal reviewer
was `/root/moment_bound_review`. Inspect whether a handle is available
before reuse in a refreshed thread. One bounded theory
review and one actual-file review sufficed for each pursuit. Do not spawn
duplicative reviewers or delegate a new hypothesis merely to appear busy.
Follow the live budget route before new agents; prior receipt was conserve.
Local Qwen manifest was unavailable: explicit exception, no model install
or unchanged-route retry. Goldbach-specific startup routing was unavailable;
use owning repo sources, do not repair unrelated agent tooling.

Deletion of ignored `local/dhr-python` was rejected by policy. Leave it;
do not retry, delegate, rename or repackage that deletion.

Local Git author identity was unset. If still needed, use the previous
commit's author through per-command `git -c user.name=... -c user.email=...`.
Stage only owned paths and run `git diff --cached --check` before commit;
plain diff does not inspect untracked new files. No push. Preserve clean
checkpoints and honest terminal evidence. The latest pursuit finished at a
natural reviewed checkpoint; no research process is claimed still running.

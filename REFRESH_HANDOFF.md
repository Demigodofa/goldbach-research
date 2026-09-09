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
Latest reviewed RESEARCH commit: **02e1627**, exact cutoff freedom in the
ACTUAL Vaughan remainder, a classical optimal cofactor norm, and its
failed separate-moment budget O(Y sqrt(log Y)) on a balanced box.
Previous **3fcea6e** removes the internal proper prime powers with an
o(Y) error and retains the exact prime/cofactor correlation, still OPEN.
Combined short HB terms do not cancel internally.
Previous **b7134e1** proves fixed divisor-weighted Type I and the precise
scope of the Heath-Brown route; these remain useful components.
Latest ACTUAL CORRELATION TRANSFER remains **476e0c3**, removing
the balanced self-correlation from the smoothed unexceptional remainder:
T_F=C_F(Z,E-Z)+C_F(A-B,E)+o(Y). Both surviving correlations remain OPEN.
Previous **a968833** supplied the restricted arithmetic convolution with
error O(Y^(1983/2000+epsilon)); its signed gcd main is now projected and
cancelled only in the precise self-correlation sense of476e0c3.
Previous **a771937** isolated the exact Vaughan remainder, failed generic
coefficient transfer, and negligible covariance diagonal.
Latest COVERAGE remains **9b6e7b4**, prime cutoff bridge
S_z-S_theta=o(Yt), positive-first prime asymptotic P_g=S_2(m)t I_g+o(Yt),
and CONDITIONAL coverage of every even target in the eligible central band.
The ACTUAL-zero and restricted large-V hypotheses remain essential.
Previous **2b72af7** proved the two different-cutoff components separately.
Previous mathematics **e5c955d** eliminated polynomial positive-factor losses.
Latest ORIGINAL-AFFINE remains **4e106b6**, the positive
cofactor sieve transfer through M<=Y^(13/25). Both use the ADDED actual-zero
large-V regime. The handoff is committed later.
Previous checkpoint **45afe67** preserved3fcea6e.
Previous checkpoint **a4a7944** preservedb7134e1.
Previous checkpoint **29b35c9** preserved476e0c3.
Previous checkpoint **7eff067** preserveda968833.
Previous checkpoint **5842cd2** preserveda771937.
Previous checkpoint **ce40960** preserved9b6e7b4.
Previous checkpoint **1e71488** preserved2b72af7.
Previous checkpoint **e436401** preserved e5c955d.
Previous checkpoint **ddfa2aa** preserved4e106b6.
Previous checkpoint **53eeab1** preserved the full smooth MODEL
hyperbola-box theorem **220920c** for ALL integer moduli.
Preceding checkpoint **83dce5e** preserved the all-integer unbalanced
MODEL saving and prime-square component **90488ef**.
Preceding checkpoint **912ec87** preserved the ALL-squarefree saving
**2c8d197** and its failed squarefull-residue budget.
Earlier checkpoint **228c342** preserved
the two-large-prime Kl3 saving **eb4e380**. Earlier **5477e87** preserved
the reciprocal-energy saving **af8f893**. Earlier **ab8dab9** preserved
the all-integer-modulus balanced saving **6852af6**. Earlier **831bbb2** preserved
the squarefree correlation estimate **7d36ce8**. Earlier **a58428e** preserved
the general-composite linear estimate **c2a5ac5** and its balanced failure.
Earlier checkpoint **d82553e** preserved
the full smooth prime-core theorem **1ab2d03**. Earlier **3b66378** preserved
the costed CRT extension **c72de0a**. Earlier **dd07496** preserved
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

For the next unexceptional lane first read `optimized_cofactor_cutoff.py`,
then `short_free_cancellation.py`,
then `multifactor_identity_gate.py`,
then `balanced_projection_transfer.py`,
then `free_divisor_correlation.py` for its analytic input, and use
`unexceptional_vaughan_gate.py` for the full remaining arithmetic sum.
Preserve `prime_cutoff_bridge.py`, its conditional coverage and exact
remaining scope. Then `rare_divisor_calibration.py`, the two cutoffs now
connected by that bridge, and `rare_class_elimination.py`, the coverage consequences
and still-missing signed lower bound. Then read
`rough_cofactor_sieve_bridge.py`, the actual affine transfer,
positive weighted density lemma and exact source-sign correction.
Then read `full_model_box_kernel.py`, the full-domain MODEL proof,
grouped-period transfer, rectangular bounds and exact budget API.
Then `all_moduli_unbalanced_kernel.py` supplies the all-integer
unbalanced saving, degeneracy recursion and prime-square component.
Then use `squarefree_unbalanced_kernel.py` for its divisor-shift and
prime/core dependencies and the retained failed squarefull-residue budget.
Earlier dependencies, as needed:

1. `two_prime_kl3_kernel.py` — retained two-large-prime correlation mechanism
   used in the latest factorization dichotomy.
2. `reciprocal_energy_kernel.py` — elementary modulus-average
   fourth-moment estimate, symmetric-box saving and remaining unbalanced gap.
3. `all_moduli_balanced_kernel.py` — balanced MODEL saving for all
   integer moduli; prime-power stationary phase and squarefull-part split.
4. `squarefree_correlation_kernel.py` — balanced squarefree-model
   saving; all nonunit modes and short-period costs are included.
5. `composite_linear_kernel.py` — general-composite unbalanced
   estimate, nonunit/period costs and balanced13/12 failure.
6. `hyperbola_prime_kernel.py` — full prime-core MODEL box coverage via changed
   grouping and linear completion. Composite/arithmetic transfer OPEN.
7. `decorated_prime_kernel.py` — CRT kernel, periodic/coupled weights
   and roughness zero-mode lemma. Its box range has now been extended.
8. `separate_factor_prime_kernel.py` — initial restricted prime kernel.
9. `cofactor_averaging_budget.py` — preceding generic source route FAILED
   its quantitative budget. Do not retry the same generic grouping.
10. `rare_affine_small_cofactor.py` — retained original affine definition
   and M<=Y^(1/5) component, now extended by4e106b6 through Y^(13/25).
11. `rare_shifted_divisor_bound.py` — preceding coefficient-one component.
12. `buchstab_endpoint_bridge.py` — arithmetic endpoint reduction and
   its OPEN one-sided prime-times-rough estimate, equation(7).
13. `formal_weight_conservation.py` — completed formal result and exact gap.
14. `balanced_semiprime_budget.py` — actual rare-factor bound used by the
   latest reduction. Open other dependencies only for a task-required step.

Use `README.md` as the project entrypoint; no project `AGENTS.md` existed.
Global Kevin instructions still apply. Current implementation/source state
outranks this handoff. No fresh giant scan, broad experiment or old test
rerun is required just to confirm already checked work.

## Latest pursuit: exact cutoff freedom and the optimal cofactor norm budget

**02e1627**, optimized_cofactor_cutoff.py, permits any real lambda supported
on d<=V, lambda1=1, |lambda_d|<=1. For R_lambda=(mu-lambda)*Lambda_>U*1,
 Lambda=Lambda_<=U+lambda*log-lambda*Lambda_<=U*1+R_lambda.
If U,V,UV<=Y^gamma, the compensating correlations with E are TI-small,
uniformly in lambda. With U=V=W the internal-power pruning still applies.
The exact remaining prime coefficient is
 -sum_(pc=n,p>U prime,c>=2)log p S_lambda(c), S_lambda(c)=sum_(d|c)lambda_d.
General lambda can introduce SMALL cofactors; do not inherit c>W.

The classical Selberg form Q=sum lambda_d lambda_e/[d,e] diagonalizes as
sum_r phi(r)(sum_(r|d)lambda_d/d)^2. Its exact minimum is1/G(V), where
G(V)=sum_(r<=V)mu(r)^2/phi(r) asymp log(2V). The optimizer is
lambda_d=mu(d)d/phi(d)*G_d(V/d)/G(V), and |lambda_d|<=1. This is a known
classical result, checked in Steve Lester's2015 notes, proof printedpp5-7;
the reciprocal normalization is independently derived in the module.
Its cofactor interval norm is C Q+O(||lambda||1^2), with error<=V^2.
For C~sqrt Y and V=W, the best bounded norm is therefore asymp C/log V.
At V3 the optimizer(1,-4/5,-3/5) gives S(2)=1/5 and S(6)=-2/5.

The actual E has second moment O(Y logY), by Chebyshev, Ramanujan
orthogonality, and the paid S^8 incomplete-period error. Pairwise Cauchy
then gives only |T_box|<<Y sqrt(logY) with the optimal weights. This is
a failed upper-bound budget, NOT a lower bound for the real correlation.
Norm-only retuning within this family cannot improve its order. Retain
the identities and optimizer; reactivate with a stronger JOINT moment or
signed covariance estimate. No broad exclusion of polynomial weights.

Keeping the prime sum intact yields |T_box|^2<=M(C) H, with
H=sum_(c~C)|sum_(p~P prime>U)log p F E(m-pc)|^2. On balanced boxes,
H<<Y^2/(C L^5) is sufficient; diagonal H_diag<<Y L^3 is small. The
weighted off-diagonal remains unproved. No coverage or full T estimate.

Started13:39:04 UTC, reassessed13:51:50 UTC, changed-under-evidence.
Eight guards passed normal0.018s and -O0.020s. Sol theory/actual-file
review PASS, no correction. Next concrete test: a fixed degree>=9
polynomial cutoff may obey |S_lambda(c)|<<H_V(c)/log V via Mellin
factorization. Can the corrected Henriot theorem, with primitive forms
c and m-pc, then give an ACTUAL per-box bound O(Y S_2(m)/logY)?
Check coefficient norm/interval hypotheses, p|m, all prime powers, and
the number of boxes. This would be new joint arithmetic input to the
cutoff method, not another marginal norm optimization. The proposed
bound is NOT yet proved. Use radical_majorant_correlation.py and its
already corrected source rather than retrying the blocked erratum URL.
Fresh <=30-minute clock required. Goal active; no process is left running
at this checkpoint.

## Preceding pursuit: actual internal prime-power pruning and combined HB scope

**3fcea6e**, short_free_cancellation.py, proves for the original
A=mu_>W*Lambda_>W*1, W=floor(Y^(gamma/2)), gamma in(5/12,1/2), that
A_p=mu_>W*(log(p)1_(p prime,p>W))*1 satisfies
 sum_(n<=Y)|A-A_p|(n) << Y W^(-1/2)L^3,
 |C_F(A-A_p,E)| << Y^(1-gamma/4+2delta+o(1))=o(Y).
This removes INTERNAL proper prime powers, distinct from the previously
handled outer ones. The proof is a positive tuple majorant, also valid
on any selected support subset. The unchanged E has |E|<<L+S^2.

Let S_W(c)=sum_(a|c,a<=W)mu(a). The remaining coefficient is EXACTLY
 A_p(n)=-sum_(pc=n,p>W prime,c>W)log(p)S_W(c).
The prime-divisor sum counts each prime once, not once per exponent.
Primes contribute0; rough distinct semiprimes pq contribute-log(pq);
p^2 contributes-log p. S_W is signed. Thus
 T_F=-sum_(p>W prime,c>W)log(p)S_W(c)
                  F(pc/Y,(m-pc)/Y)E(m-pc)+o(Y).
This exposes the actual linked prime/cofactor correlation. It does NOT
estimate it or produce a new prime lower bound or coverage.

The all-short HB sum is also derived exactly. With fixed K>=2,
z=floor(Y^(1/K)), T=floor(Y^eta), 0<eta<1/[K(K-1)], every j<K term
vanishes on n~Y eventually. At Y=3p^K, n=2p^K, 2<=T<p, the ENTIRE
short sector equals-log2, while full Lambda(n)=0. Its cancellation is
outside that sector, not across its j terms. The factorization
 S_short=[delta_1-(delta_1-mu_<=z*1_<=T)^{*K}]*Lambda_T
uses Lambda_T=(1_<=T)^(-1)*(1_<=T log), not Lambda. At T2,n4 it is
-log2. The inverse has fixed depth J<1/eta on n<=Y, with divisor bounds
(J+1)tau_(2J+1) and(J+1)L tau_(2J+2) for the inverse and Lambda_T.
These preserve norms but supply no estimate against E.

Support qualifications: A_p is zero on final W-smooth n. If HB is put
in the INTERNAL Lambda(d) slot and K>=5, short d is z-smooth with z<W.
Only the FULL restored Lambda(d), d>W, then restricts to proper powers
and is pruned by the actual estimate. Raw short HB terms can be nonzero
at composites and MUST retain their compensation. Final n=adk need not
be smooth. No short-sector removal is proved for HB in the PARTNER E.

Started13:18:59 UTC, reassessed13:37:41 UTC, changed-under-evidence.
Eight guards passed normal0.006s and -O0.008s. Sol theory/actual-file
review PASS with no correction. No scan or outside action. The next
question, now tested in02e1627 above, was whether a smoothed Mobius cutoff
could reduce the actual cofactor norm
enough to improve the remaining correlation budget? First derive an
EXACT generalized Vaughan identity including compensation, then pay the
cofactor second moment and Cauchy costs. A smaller norm alone cannot
stand in for prime covariance. No matching completed pursuit was found
in the narrow repository search. Preserve polynomial and other reviewed
tools; start a fresh <=30-minute clock. Goal active; no research process
is left running at this checkpoint.

## Preceding pursuit: fixed divisor-weighted TI and multi-factor route boundary

**b7134e1**, multifactor_identity_gate.py, proves for fixed s,b,A that
 sum_(d<=Y^gamma)tau_s(d)L^b Delta_d <<_(s,b,A) Y/L^A,
where Delta_d is the original unexceptional absolute TI discrepancy.
Its proof uses Delta_d<<YL tau(d)/d+S^4, then the elementary divisor
moment tau_s^2 tau_2<=tau_(2s^2) and weighted Cauchy. The needed input
TI log saving is2(A+b)+2s^2+1. This pays actual grouped divisor weights;
their maximum Y^epsilon is NOT absorbed into a logarithmic saving.

The verified Heath-Brown identity has exact residual
 Lambda-HB_(K,z)=mu_>z^{*K}*1^{*(K-1)}*log,
which vanishes for n<2(z+1)^K. At K2,z2,n18 it equals+log2 and
HB=-log2. The primary identity source is Tao's2013 combinatorial subset-
sum post, equations24-25 and the following display. Its MPZ distribution
theorems are not imported as pointwise Goldbach estimates; no old blocked
Heath-Brown1986 route or excluded Notes7 argument was retried.

For j=K, Y=3p^K, all K Mobius variables p, all free1 variables1,
and logarithmic variable2 give a real localized term -log2 at n=2p^K.
Every genuinely free variable is bounded; the grouped arithmetic product
index has exponent1. It misses TI and the free-variable BC range. Grouping
Mobius factors near sqrt(Y) does not make either product a smooth variable.
Even the optimistic r=s=1 BC budgets are9/5 and15/8. This rejects only
TERMWISE treatment by the current estimates. The FULL identity cancels at
this composite n; the witness is not an actual-H lower bound or no-go.
Squarefree smooth composites may have original Vaughan A=0 already.

Positive components persist. A genuine 1/log factor longer than
Y^(1-gamma+eta) is handled by the new divisor-weighted TI lemma. Paired
terms with one untouched free1 per side and complementary products in
[Y^gamma,Y^.51] admit the BC proof with fixed divisor-moment L2 costs.
The grouped coefficient alpha_j=mu_<=z^{*j}*1^{*(j-2)}*log is retained.
All K/divisor orders stay fixed. When log is the free factor the grouped
divisor order remains2j-1; only its grouped coefficient's L disappears,
and the free logarithm's variation is paid separately (review correction).

Started13:01:48 UTC, reassessed13:16:56 UTC, changed-under-evidence.
Eight new guards passed normal0.006s and -O0.005s. Sol theory and actual
file review PASS after the recorded wording correction. No new coverage,
scan, publication or other outside action. Both correlations from476e0c3
remain open; all polynomial/model tools and conditional coverage persist.
The next question, now tested in3fcea6e above, was whether combining
specific Heath-Brown terms BEFORE
taking absolute values remove the all-short-free region while preserving
an estimate against the unchanged E? Derive the combined coefficient and
test its actual support and norm costs. A reconstruction of Lambda or an
untreated prime/roughness indicator is not a cancellation bound. Either
prove a licensed estimate or retain the precise remaining signed weight.
Start a fresh <=30-minute clock and independent review. Goal active; no
research process is left running at this checkpoint.

## Preceding pursuit: balanced self-correlation removed from the actual remainder

**476e0c3**, balanced_projection_transfer.py, sets
 B(n)=sum_(r|n,Y^gamma<r<=Y^.51)h_r,
 H_B(q)=sum_(q|r,Y^gamma<r<=Y^.51)h_r/r,
 Q=floor(S^2), P_Q(n)=sum_(q<=Q)H_B(q)c_q(n), Z=B-P_Q.
The exact gcd main becomes sum_q c_q(m)H_B(q)^2. Its tail above Q is
<<L^4 tau(m)/Q, including nontrivial gcds and nonsquarefree moduli.
BP, PB and PP have matching truncated mains, with all period errors paid.
Usinga968833 gives an ACTUAL fixed-smooth bound
 |C_F(Z,Z)|<<Y^(1983/2000+epsilon)+YL^4tau(m)/Q
               +Y^.51 L^3Q^2+L^4Q^4
           <<Y^(1-2delta+epsilon).
This signed additive self-correlation is not assumed positive.

P_Q is NOT Gamma_S: its coefficients depend on B. Instead its exact
divisor representation has support d<=Q<=Y^gamma and coefficients
p_d=d sum_(q<=Q,d|q)H_B(q)mu(q/d)<<L^3. The existing TI input therefore
proves C_F(P_Q,E)=O_A(Y/log(Y)^A), with E=Lambda-Gamma_S unchanged.
Writing A=VaughanII, H=A-B and R=E-Z yields
 T_F=C_F(Z,R)+C_F(H,E)+C_F(Z,Z)+C_F(P_Q,E).
The last two terms are small by the ACTUAL estimates just given. The first
two remain unestimated; R explicitly retains the P_Q-Gamma_S mismatch.
Keep the arbitrary-logarithm TI saving separate from the power-saving ZZ.
The result requires fixed smooth F; a sharp-cutoff upgrade is not asserted.

The short-free-variable gap is concrete. For n=pq, distinct primes p,q>W,
the only nonzero h_r with r|n is h_n=-log n; for n=p^2 it is -log p.
At n comparable to Y these k=1 terms lie wholly in H. No new prime-pair
coverage follows. Polynomial tools, conditional coverage9b6e7b4, source
corrections and previous model boundaries are preserved.

Started12:47:52 UTC, reassessed12:58:25 UTC, changed-under-evidence.
Eight guards passed normal0.009s and -O0.010s. Sol theory and actual-file
review PASS. No previous experiment, new prime scan or outside action.
The next question, now tested inb7134e1 above, was whether a multi-factor
prime identity, such as the
Heath-Brown identity, expose additional genuinely long free variables in
H that Vaughan's grouping loses? First verify the exact identity from a
primary source, then test its full factor-size domain, including terms
with every free variable short. A successful grouping must preserve all
actual Mobius/log coefficients and pass the existing reciprocal budget;
otherwise retain the explicit uncovered box. A relabelled short variable
or a formal identity alone does not supply cancellation. Give this a fresh
<=30-minute clock and independent review. Goal active; no research process
is left running at this checkpoint.

## Preceding pursuit: an actual balanced convolution with two free variables

**a968833**, free_divisor_correlation.py, keeps
 h_r=sum_(ad=r,a>W,d>W)mu(a)Lambda(d), |h_r|<=log r,
 T=sum_(rk in J)h_r E(m-rk).
Only the floor strip W^2<r<=Y^gamma is already Type I. The full remainder
includes k=1; the old smooth-model input still cannot absorb unchanged
Mobius/prime coefficients just because this k is called free.

For fixed smooth F, separate actual coefficients alpha_M,beta_N bounded
by log(2Y), and dyadic scales Y^gamma<=R,S<=Y^(51/100), the new theorem is
 sum_(Mk+Nl=m)alpha_M beta_N F(Mk/Y,Nl/Y)
  =Y I_F(m/Y)sum_(gcd(M,N)|m)alpha_M beta_N gcd(M,N)/(MN)
    +O_(F,epsilon)(Y^(1983/2000+epsilon)).
It applies to h_M,h_N in the Type-II-by-Type-II term. This is an ACTUAL
arithmetic-coefficient estimate, not a substitution into the old smooth
MODEL. The fixed smooth physical-variable cutoff is part of the theorem.

For g=gcd(M,N)|m, M=gu,N=gv,X=Y/g, Poisson in k gives prefactor
X/(uv), phase e_v(h*(m/g)*inverse(u)), and H0=uv/X. Fixed-box Mellin
separation leaves the actual coefficients outside completion. Bettin--
Chandee Theorem1 permits these separate sequences directly. BOTH source
terms, all three L2 norms, the gcd sums, H0<1 padding, and Schwartz tails
are paid. With R=Y^r,S=Y^s,g=Y^d, the two complete error exponents are
 E1=3/20+7(r+s)/10+max(r,s)/4-9d/5,
 E2=7(r+s)/8+max(r,s)/8-15d/8.
Their worst values are1983/2000 and153/160. The signed gcd zero mode
is NOT identified with a positive prime/model main. Larger M or N, mixed
Vaughan/model terms and short-free-variable regions remain uncontrolled.
The old cofactor geometry's107/100 failure and generic completion loss
remain valid; no new unexceptional prime-pair coverage follows.

Started12:30:54 UTC, reassessed12:45:47 UTC, changed-under-evidence.
Eight new guards passed normal0.003s and -O0.002s. Sol theory and actual
proof/code/test review PASS. No old scan, outside action, or priority claim.
The next question, now tested in476e0c3 above, was whether the signed gcd
main could be matched to the same small-
modulus Ramanujan projection used in the unexceptional comparison?
Concrete test: derive the exact coefficient identity, cost the moduli
q>Y^delta tail, then check whether the resulting term actually cancels an
existing term of T. A formal rewrite alone is insufficient; preserve any
large-product/mixed remainder. This is the next bounded hypothesis, not
a completed cancellation estimate. Give it a fresh <=30-minute clock.
Conditional coverage9b6e7b4, polynomial identities and model bounds stay
available. Goal active; no research process is left running at checkpoint.

## Preceding pursuit: exact unexceptional remainder and failed generic transfer

**a771937**, unexceptional_vaughan_gate.py, derives the exact remaining sum
 T=sum_(ab in J,a>V0,b>U0) mu(a) B_U0(b) E(m-ab),
 B_U0(b)=sum_(d|b,d>U0)Lambda(d), E=Lambda-M_S on I,
 U0=V0=floor(Y^(gamma/2)), gamma=1/2-eps.
Type I terms and prime-power replacements are paid; CROSS+T gives the
actual prime-pair mass. A sufficiently small one-sided lower bound on T
would suffice. Absolute T=o(Y) is a stronger sufficient target, still OPEN.
Keep Vaughan's free convolution1: B_U0 is neither Lambda nor log.
Tao Notes3 Lemma18(32) is the identity source; this does not revive the
excluded Notes7 Linnik proof. Its corrected *1 and divisor bounds persist.

Generic Fourier completion has only l1<=sqrt(N), sharp for quadratic
chirps. Even granting unproved phase-uniform model bounds, its generic
cost defeats the saved1/4096 once length exponent exceeds1/2048. Actual
factor spans exceed5/24. Period-N encoding also violates the model cap.
This is a failed TRANSFER BUDGET, not a lower bound on actual arithmetic
Fourier norms or a no-go theorem for Mobius/divisor cancellation.
Cauchy gives K(b1,b2)=sum_a E(m-ab1)conj(E(m-ab2)), with all masks.
The covariance diagonal is already <<Y^(1+4delta+epsilon), negligible
against the sufficient energy target A B^2/log^6Y. Only a one-sided upper
bound on the weighted OFF-DIAGONAL is needed. Its linked forms satisfy
 b2*p1-b1*p2=(b2-b1)*m.

Started12:16:10 UTC, reassessed12:29 UTC, changed-under-evidence. Nine
new guards passed normal0.008s and -O0.008s; Sol theory/actual-files/delta
review PASS. No unexceptional prime estimate, old scan or outside action.
The next question, now tested in a968833 above, was to retain the free1 instead
of hiding it in B_U0, and test whether a legal Poisson/dispersion step can
use it while keeping Mobius and prime coefficients outside completion.
Derive the exact multilinear terms and cost the SHORT free-variable cases,
including k=1; do not assume a free variable is long or periodic. Observable
test: control the actual Type II sum with all regions paid, or identify the
specific surviving weighted correlation. Give it a fresh <=30-minute clock.
Conditional coverage9b6e7b4 and all polynomial/model tools stay available.
Goal active; no research process remains running at this checkpoint.

## Preceding pursuit: cutoff bridge gives conditional prime-pair coverage

**9b6e7b4**, `prime_cutoff_bridge.py`, proves in the SAME ACTUAL-zero
large-V regime and original fixed parameter choices
 0<=S_z-S_theta
   << S_2(m)Yt^2 U^8 log(2U)+Y^(7/9+theta+o(1))+S_2(m)Y eta^-20
   =o_theta(Yt),
with U=K log eta and theta=delta/u<1/5. It composes2b72af7 into
 P_g=S_2(m)t I_g+o_theta(Yt)
on suppressed targets. This is an ACTUAL weighted prime-pair estimate,
not the earlier formal conservation identity. A smooth minorant I_g>>Y
proves conditional positivity, with ineffective onset and no numerical example.

Mechanism: remove squareful/shared terms with explicit Y/z exp(O(U))L^2.
Any remaining cutoff-difference term has a prime r in[z,z_old]. Positive r
in x or n gives respectively lambda(x)=2lambda(x/r) or W(n)=2W(n/r);
negative r on nonzero W support is unique and W(rM)=lambda(M)log r.
These are three nonnegative union cases, not a disjoint partition. Keep
the reduced variable Q=Y/r as coefficient-r first form, Q>>Y^(4/5).
The DIRECT Poisson proof has modulus Dd2c, with native(r,d2c)=1 retained
until zero mode. Prime r>=z replaces the old cofactor roughness hypothesis
by a proved local-factor bound1+O_A(1/r); it is not a theorem substitution.
Zero-mode coprimality removals sum to Y L^C/z. Both W placements preserve
the normalized smooth derivatives; nonzero modes sum with a fixed margin.

Conductor means are A,0,0,-chi(r)A. Positive r gives one A_z cancellation
and one B_z moment, then its reciprocal prime mass O(t) gives the second
rarity factor. Negative r gives two A_z cancellations and costs only
sum1/r=O(log U). This avoids the failed dynamic pointwise W estimate.

An elementary residue gap completes ALL residue classes in the band:
MM Theorem1.4's multiplier is kappa=1+C/A in {0} union[2/3,2]. The zero
case is exactly F_D; an8-part may instead give C/A=0, so retain that case.
For nonzero kappa, the existing source theorem has relative error o(1),
and proper prime powers cost O(sqrt(m)log^3m). It only requires m>=D^10,
with NO upper-V condition. Thus every even m in[5Y/4,7Y/4] has a prime
representation under the same eligible zero and scale hypotheses. The
nonsuppressed pair is not asserted to lie in(Y/2,Y]. This is CONDITIONAL
coverage, not an actual eligible zero, effective onset, universal Goldbach
or historical-priority claim. The unexceptional and other zero regimes remain.

Started11:59:43 UTC, reassessed12:14 UTC, changed-under-evidence. Nine NEW
finite guards passed normal0.021s and -O0.021s. Sol reviewed theory, actual
files and the all-residue corollary, PASS. The source8-part zero and
prime-power logarithm qualifications are explicitly preserved. No old
prime scan or test campaign, outside action, publication or wake queue.

Next concrete question, UNTESTED: can the retained all-moduli reciprocal
kernel control the ACTUAL Mobius-weighted Type II remainder in the
UNEXCEPTIONAL branch of ramanujan_type_i.py? Start with the exact Vaughan
identity and identify the large-factor weights before any Poisson step.
Test whether they genuinely satisfy full_model_box_kernel.py's smooth /
bounded-periodic input conditions or a proved arbitrary-coefficient
extension; do not silently replace Mobius or divisor coefficients by
periodic weights. Observable test: derive the exact bilinear remainder,
cost its frequency/coefficient norms and either prove a saving on Y or
retain the specific unproved correlation. This is a new arithmetic lane,
not a repeat of the completed smooth-model boxes or formal polynomial work.
Give it a fresh <=30-minute clock and independent review. All polynomial,
character and model components survive; the overall research goal is active.
No research process remains running at this checkpoint. Execution gaps are gaps.

## Preceding pursuit: actual divisor correlation calibrated to rare-prime mass

**2b72af7**, `rare_divisor_calibration.py`, retains the ADDED actual-zero
V>=log^3 eta regime, t=V/eta<=1/logY, central suppressed targets and fixed
nonnegative smooth support. With U=K log eta, z=Y^(1/U), it proves
 Q_z=(A/phi(D))t I_g+o(Yt/G_z),
 S_z=G_z Q_z+o(Yt)=S_2(m)t I_g+o(Yt).
Q_z is the one-variable log(x)lambda(x) mass with partner UNIT mask only;
S_z also requires BOTH variables rough and weights lambda(x)W(m-x)/2.
This is an ACTUAL divisor-correlation asymptotic, not a formal density.
It implies only P_g<=S_z until the composite difference is controlled.

The four orientation means A/D,0,0,-A/D combine to A_z(y)B_z(m-y).
MM Lemma2.4 gives B_z=2C_z(1+O(E)), A_z=O(E/U), E=tU^4+eta^-B.
Retain the outside1/2, the Abel factor2, and the small-divisor atom1.
Replacing B_z costs S_2 Y E^2=o(Yt), using the integral of |A_z|.
Exact G_z=V2_D C_z/V1_D=Sigma_(2,z) phi(D)/A; tail1+O(U/z).
One-variable beta-sieve tails are relative-small; dynamic Q_z composite
mass is O(Yt^2U^2) plus smaller terms by the unique largest positive prime.
Never replace this Q-only bound with an unsupported two-variable bound.

Separately, at ORIGINAL fixed theta, a prime sieve with modulus Dd,
not MDd, proves first-variable replacement. Paying FULL/B_good pruning
explicitly then gives S_theta=P_g+o(Yt). Its factors are strictly>z_old.
The equality endpoint costs Y^(1-theta+o(1)). Growing-U pointwise W costs
can be2^U; fixed-theta sieve errors do not prove the dynamic asymptotic.
The two theorems therefore do not yet compose into a prime lower bound.

Next concrete hypothesis, UNPROVED: bound S_z-S_theta by exposing a prime
r in[z,z_old], with z_old=ceil(Y^theta), theta<1/5. Squareful/shared terms
are already small. Positive r dividing x gives lambda(x)=2lambda(x/r);
positive r dividing negative n gives W(n)=2W(n/r). Their affine lambda/W
forms have Q=Y/r>=Y^(1-theta), coefficient r prime and small. Test the
direct small-cofactor Poisson adaptation, one A_z and one B_z, with
per-r upper bound S_2(Y/r)t U^4 and positive-prime reciprocal mass O(t).
Negative r can only occur on the W side; on squarefree nonzero support,
W(rM)=lambda(M)log r. Test the two-A_z lambda/lambda bound and sum1/r
with O(log U) loss. All three are positive majorizations; summing nonzero
modes should cost Y^(7/9+theta+o(1)). Verify every zero-mode removal and
r|m exception, rather than substituting into the older theorem's hypotheses.
Prediction: cutoff difference o(Yt); falsifier: a surviving Yt-scale error
or a coefficient/character hypothesis outside the cited direct proof.
This is a NEW test, not a proved transfer. Give it a fresh <=30-minute clock.

Started11:34:38 UTC, reassessed11:58 UTC, changed-under-evidence. Seven NEW
finite guards passed normally0.008s and under -O0.007s; Sol reviewed the
theory and actual files, including FULL/B_good and strict endpoints, PASS.
No scans repeated. Polynomial tools and formal conservation6f9a77b survive.
Kevin reiterated freedom to incorporate other mathematical approaches;
historical recognition and prizes remain unverified, with no external action
authorized. Goal active; no process remains running at this checkpoint.

## Preceding pursuit: all polynomial rare-factor composite errors are negligible

**e5c955d**, `rare_class_elimination.py`, composes the original pruning
with4e106b6 for ANY fixed normalized polynomial f of degree d:
 T_f=P+sum_(3<=k<=d, k odd) C_(k,f)^all-negative+o_(f,theta)(Yt).
The ENTIRE absolute contribution of partners containing a positive-sign
prime is negligible. For the quintic this removes S2,S4,S6 and leaves
only the signed pure triple and positive pure five-factor classes.
For the ORIGINAL W=chi*log, and every normalized quadratic, it proves
 T_W=P+E, 0<=E=o_theta(Yt).
This closes W's composite error. Its FULL weighted mass has no proved
positive lower bound; the size of B_good and the accessible main do not
provide one. At chi mod31,n=3*11*29=957,R=floor(n^(12/25))=26,
the truncated W sum is log(33/29)>0 while full W(n)=0. This is an exact
signed-truncation guard, not an actual-zero or asymptotic counterexample.

In the Buchstab endpoint reduction, both terminal factors exceed R and
map to B_M with M the negative prime. Hence E_R=o(Yt), improving the
old C*epsilon*Z loss. The sufficient one-sided estimate is now
 U_A<=LXV(z_old)-(c+C0*eta_u/theta)*Z;
it remains OPEN. The >=q least-factor condition and repeated factors
in U_A remain intact. Formal conservation6f9a77b is unchanged.

Coverage guards: q>floor(Y^a) implies q>Y^a DIRECTLY. Do not use the
false inequality Y/floor(Y^a)<Y^(1-a). Cofactor/character restrictions,
original z_old=ceil(Y^theta), strict interval endpoints and central
suppressed targets are all retained. Pruning can depend on q for each M;
dominate by the full nonnegative B_M, not an invented M-only selection.
V>=log^3 eta is explicitly additional, compatible with fixed delta,u,
and does not follow from the original regime or imply zero existence.

Seven NEW checks passed normally0.023s and under -O0.021s; Sol
`/root/sieve_review` passed theory, actual proof/code/tests and the eta_u
notation correction. Three finite character fixtures cover S2,S4,S6;
they assert no exceptional zero. Started11:12:52 UTC; this pursuit returns
`changed-under-evidence` before11:42:52. No old experiment was rerun.

Next concrete question, UNTESTED: can the correlation lambda_chi(p)*W(m-p)
be calibrated against a ONE-variable rare-prime lambda_chi mass? On F_D,
its zero orientations suggest A_z(p)*B_z(m-p), where
 B_z(y)=sum_(d rough)chi(d)/d*H(d^2/y)*log(y/d^2).
MM Lemma2.4's logarithmic moment may control B_z, while a one-variable
comparison could retain the same unknown A_z. Test exact local constants
and, especially, prime-to-divisor replacement and sieve errors relative
to Yt. An O(Yt*log^C eta) remainder is a failure of the proposed lower
bound. Fixed original theta and the internal growing U must not be mixed.
No positive lower bound from this idea has been proved. MM primary
Lemma2.4/Proposition2.3 was re-opened, not a novelty search.
No process is left running or manual wake queued. The overall goal stays
active; Qwen remains unavailable without retry or installation.

## Previous pursuit: the model transfers to actual affine rare/rare pairs

**4e106b6**, `rough_cofactor_sieve_bridge.py`, proves, under the SAME
actual-zero large-V hypotheses and for ANY original-Y^theta-rough subset
with gcd(M,Dm)=1 and M<=Y^(13/25),
 sum_M B_M <<_theta S_2(m)Yt^2(log eta)^9
                 +Y^(1-rho/2+o(1))+S_2(m)Y eta^-19=o_theta(Yt),
where rho=2^-20. This is an ACTUAL affine upper bound, not just a model.
It does not estimate the signed prime correlation or prove coverage.

The cofactor upper-beta sum sigma>=1_rough>=0 permits arbitrary subsets.
It can admit nonrough M, so retain F_C(M)=prod_(p|M)(1+C/p). The new
weighted mean is sum_(M~B)sigma(M)F_C(M)<<B/log z+R sqrt B, giving
harmonic mass O(U) for B>=Y^(1/5), U=K0 log eta,R=Y^rho,z=Y^(1/U).
This pays the coefficient-dependent Henriot tails and zero density.
Recombine all four character orientations BEFORE absolute values. The
two harmonic cancellations remain, at the explicit extra U cost.

Keep exact (M,Dm)=1 during the Henriot tail estimates. Before truncating
its Mobius expansion in the nonzero modes, insert native (M,q0)=1 and
retain (M,D)=1; otherwise inverse(M) can be undefined in individual terms.
Use physical M,a, q0=d2*c, conductor D, and a normalized bounded D-periodic
character sum. Smooth derivatives are uniform by Fourier integration by
parts. Ystar=YR^2 pays q0<=sqrt Ystar, Hstar<=DR^4,J<=DR^5 and five
sieve/gcd indices costing R^5. The omitted target-gcd tail costs
Y^(1-rho+epsilon), with reciprocal zero-mode weights and no hidden R^3.
No chi(M) factor or enlarged conductor D*M is introduced.

NEW SOURCE CORRECTION: MM2112.11412v2 equation(22) has the wrong sign.
For its upper weights, sum lambda_d*g(d)=Euler product PLUS sum V_r.
R=100,beta=2,z=10,g(d)=1/d gives 1/3=8/35+11/105. Its relative O
lemma survives; retain this exact witness and never copy the minus sign.
The saved CRT convention uses negative signs in BOTH additive phases.

Nine NEW finite guards passed normally in0.024s and with -O in0.017s;
Sol `/root/sieve_review` passed the derivation, actual proof and tests,
including the phase-sign and fixed-theta error-absorption clarifications.
This pursuit began10:43:21 UTC and returns `changed-under-evidence`
before11:13:21. Qwen remains unavailable; no old experiment was rerun.

The THEN-next concrete test was: does this bound cover the ENTIRE previously surviving
even one-rare-factor composite class under its original pruning, fixed
polynomial weights and parameter order? Match its exact cofactor and
character conditions to B_M; any uncovered boundary or class is the
falsifier. Preserve that residual explicitly. Do not infer a signed lower
bound from the already completed formal conservation identity6f9a77b.
All polynomial components remain available. No process is left running
at this checkpoint, no manual wake was queued, and the overall goal stays
active without claiming work during pauses.

## Previous pursuit: the full smooth MODEL box domain is covered

**220920c**, `full_model_box_kernel.py`, proves
 sum_q |E_q| <<Y^(1-1/4096+epsilon)
for EVERY integer modulus and the ENTIRE canonical domain
 1/5<=b<=13/25, 0<=x<=(1-b)/2, 0<=y<=1/2,
with the same smooth MODEL, arbitrary joint periods including gcd(q,J)>1,
all nonunit modes, H,J0<=Y^(1/4096), and all axes/overlap paid.
This closes the model's box geometry; it does NOT transfer sieve weights.

The exact domain partition uses the retained pointwise, linear and energy
bounds. Swapping the balanced grouping covers max(b,x) in[9/32,15/32]:
its bare exponent is<=63/64, and Z=Y^(1/256) pays the old squarefull split.
Both head/tail reach at most1-3/4096. The remainder has b>15/32,
31/128<x<17/64 and49/100<y<=1/2, handled by a new grouping mechanism.

After the exact period lift and prime-power recursion, fix kappa modJ
and group w=eta*kappa, where h=Hdiv*eta,k=Kdiv*kappa. The retained local
kernel is an ACTUALLY coupled function periodic mod rJ in both w,l.
The complement is squarefree and coprime to J. Divisor shifts preserve
this periodic kernel, so unequal interval lengths can be kept. The
prime/two-prime core has rectangular norm R^(11/64)*(MN)^(5/16), with
its shift/support conditions checked. The total period charge is J^5.

Important normalization: grouping gives only bounded recursion L2 mass,
not D^-1/2. Small D use the nonnegative modulus powers in the displayed
bounds; large D retain volume1/D. Complementary simple-prime zero modes
have factor1/Ds; their masks preserve the rJ period. Exact norm=1
fixtures prevent silently reusing the stronger fixed-h mass bound.
At full caps the decisive residual exponents are
 1-(19/8)/4096 (divisor shifts), 1-(81/16)/4096 (core),
 1-2/4096 (large degeneracy divisors).
All are below the uniform claim1-1/4096. The old budget failures and
prime-square correlation remain valid components, with their own scopes.

Eight NEW checks passed normally in0.148s and under -O in0.134s.
Sol `/root/sieve_review` passed the independent derivation, actual proof,
implementation and tests. This pursuit began10:15:59 UTC and returned
`changed-under-evidence` before its10:45:59 ceiling. No old experiment,
outside action or manual wake queue occurred. Qwen remains unavailable.

The THEN-next concrete question was: can a POSITIVE upper-sieve weight replace the
original arbitrary rough-cofactor subset while preserving its harmonic
density and keeping every period/frequency/index cost inside the saving?
`rare_affine_small_cofactor.py` defines that actual family and its affine
Poisson step. A weaker fixed-power roughness cutoff is a candidate, not
a proved transfer. Test majorant positivity, density, coefficient M's
coprimality/discriminant cases, smooth amplitudes and all three original
sieve indices. Do not simply call an arbitrary rough indicator smooth.
At that checkpoint original sieve transfer and signed correlation were OPEN;
the then-latest original-affine was2b8cf98 and formal conservation6f9a77b still
does not estimate its signed difference. All polynomial tools survive.
No research process is left running at this checkpoint; the overall goal
remains active, with no claim of execution during pauses.

## Previous pursuit: repeated factors stay inside the preserved shift factor

**90488ef**, `all_moduli_unbalanced_kernel.py`, proves the SAME unbalanced
MODEL box B=Y^(1/2),A=Y^(1/4),C=Y^(1/2),K=Y^(1/4) for EVERY integer q.
The mechanism is cheaper than the preceding failed residue split: only
the complementary factor s in q=r*s needs to be squarefree. The preserved
r factor may contain arbitrary prime powers, since its role is bounded
periodicity. The retained pointwise theorem provides that bound.

Let U(q) be the FULL squarefull part. For U(q)<=q^(2/5), a corrected
factorization dichotomy gives either a divisor r in[q^(1/32),q^(69/160)]
containing U(q), with squarefree complement, or a small factor leaving
one/two large simple primes. The earlier proposed upper divisor limit
2/5 was too narrow when attaching U(q); independent review caught this.
The widened window still saves1/256. Natural K handles every integer
multiplier for U(q)<=q^(51/128), with all nonunit masks paid.

For all prime powers, the EXACT normalized recursion is
 G_e(h,l,t)=K_(p^e)(hlt)+p*1_(p|h,l,t)*G_(e-1)(h/p,l/p,t/p).
It ends at the retained prime zero-pattern formula. Every reduction D
has volume mass<=D^-1 and fixed-h bilinear norm mass<=D^-1/2, up to
divisor factors. The exact joint-period Fourier lift costs J^4 and
produces arbitrary-position second intervals, permitted by the proof.
D|q and D|h'=(h+qa)/J imply D|h; the nonzero Schwartz divisor savings
therefore survive periods sharing q. No expensive squarefull residue
split is needed. For U(q)<=q^(39/100), the off-axis total is
 Y^(1-1/512+epsilon)*J0^(7/2)*H^(3/2).
The remaining moduli number O(C^(161/200)) by squarefull density and
use the existing pointwise bound. Integer axes and overlap remain paid.
At H,J0<=Y^(1/4096), the good exponent is1-3/4096 and the full MODEL
claim is1-1/4096. The old failed budget remains valid for its own method.

Separately, for p>=5, K_(p^2)(z) is exactly the sum of e_(p^2)(3w) over
unit cube roots w^3=z. Its four-factor correlation is <=108p whenever
p does not divide a(u-v), uniformly in the Fourier twist. Tangent
stationarity reduces to a degree<=12 polynomial with nonzero constant,
at most12 stationary bases for each of at most9 root branches. Both
exceptional families are necessary: p=113 gives explicit correlations
p(p-2) and p(p-1), each exceeding108p. Keep this as a separate promising
component; the all-integer MODEL proof does not require it.

Nine NEW exact checks passed normally in0.195s and under -O in0.151s.
Sol `/root/sieve_review` passed the theory, corrected classification,
actual files, arbitrary-interval transfer, recursion, costs and fixtures.
This pursuit began09:51:06 UTC and returned `changed-under-evidence`
before its10:21 UTC ceiling. Qwen remains unavailable without retry.
No old experiment, outside action or manual wake queue occurred.

Next concrete question: do the combined reviewed model bounds cover the
full canonical hyperbola-box domain, or is there a specific surviving
box? Test the exact exponent envelope with all periods, frequency caps
and source support ranges, before proposing another analytic ingredient.
Full box coverage, original sieve transfer and signed prime correlation
remain OPEN. Latest original-affine stays2b8cf98; the formal identity
6f9a77b and all polynomial tools remain available. No research process
is left running at this checkpoint. The overall goal remains active;
do not claim execution during pauses.

## Previous pursuit: the unbalanced saving covers all squarefree moduli

**2c8d197**, `squarefree_unbalanced_kernel.py`, proves the same unbalanced
MODEL box B=Y^(1/2),A=Y^(1/4),C=Y^(1/2),K=Y^(1/4) for ALL squarefree q.
The previous two-prime theorem remains a component. The new mechanism
uses FKM1405.2293v2 Corollary3.4 with four affine maps and the explicit
rank3 sign-involution normality check. Divisor shifts preserve one factor
of q and expose a four-factor correlation on the complementary factor.
The signed-congruence graph bounds all nonunit differences with arbitrary
coefficient norms; no small-prime residue class is discarded.

If a divisor lies in[q^(1/32),q^(2/5)], this gives a saving. Otherwise a
small cofactor <q^(1/32) leaves one or two large primes, handled by the
reviewed wider-length amplification and one coefficient residue split.
The natural K_q theorem has norm factor X*q^(-1/256+epsilon), for
sqrt(q)<=X<=q^(1/2+1/256), ALL squarefree q and ANY integer multiplier.
Its ordered gcd(c,q), gcd(m,q0), gcd(n,q1) partition is exact and retains
separated coefficient masks. Zero extension is used where required.

For the actual model, fix h before the l,k bilinear bound. Only l needs
a residue split, so the small-transform cost is T^3, not the previous
conservative T^4. Joint periods sharing q, nonunit modes, both integer
axes and overlap are included. The result is
  sum_q |E_q|<<Y^(1-1/4096+epsilon),
with raw exponent1-511/1048576. An exact test corrected the draft's
decoration count from7+1/256 to6+1/256; this strengthens the result.
Eight NEW tests passed normally in0.124s and under -O in0.135s. Sol
`/root/sieve_review` passed the theory, actual files, divisor-shift
endpoints, corrected arithmetic, and the following failed extension.

The existing full-squarefull-part split FAILS its budget here, even using
the small-u density. With Z=Y^z the head/tail upper exponents are
  1-511/1048576+(3/2+1/256)*z, 1+5/4096-z/2.
Their optimal maximum is467315/466944>1 at z=199/233472. This lies in
the allowed support range, so that is not the failure. Keep this as an
upper-budget failure, not a lower bound or a ban on prime-power methods.
Do not repeat that exact splice at the same caps. Next concrete question:
can a prime-square four-factor correlation, derived from the retained
stationary-phase formula, save a power outside explicit exceptional
congruences? Check its critical equations and exact finite sums first.

The reviewer also located KMS Proposition4.29's fixed hypersurface over
Z[1/ell], confirmed in the primary source. Preserve it for a future direct
bad-locus CRT route; that full alternative transfer is not proved here.
Prime powers in this box, full box coverage, original sieve transfer and
the signed prime correlation remain OPEN. Latest original-affine stays
2b8cf98. All polynomial identities and earlier bounds remain available.
This pursuit began09:26:06 UTC and returned `changed-under-evidence`
before its09:56 UTC ceiling. No old experiment or outside action occurred.
Qwen remains unavailable without retry. No research process is left running
at this checkpoint; the overall goal remains active and pauses are explicit.

## Previous pursuit: two large prime factors at the unbalanced box

**eb4e380**, `two_prime_kl3_kernel.py`, derives, for distinct-prime q=p1*p2 with
p_min>=q^(2/5), the bilinear norm factor q^(11/64+epsilon)*X^(5/8),
sqrt(q)<=X<=q^(1/2+1/128). At X=sqrt(q), this is q^(31/64), saving
q^(1/64). KMS prime eight-factor correlations and scalar amplification
are combined with CRT. This is a derived Kl3 theorem; neither KMS's
prime bilinear theorem nor MQW's Kl2 theorem is claimed for composite Kl3.

Critical source correction: KMS uses literal ZERO extension, so the proof
uses Z_q(z)=1_(z,q)=1*K_q(z), then recovers the repository's K_p(0)=1/p
extension by a nonunit error <=3*X/p_min times the coefficient norms.
KMS Theorem4.11 supplies ALL completed twists; averaged subtraction
cancels the diagonal p^2 main term even when the two source twists agree.
Removing only s1=s2 modq would be wrong: gcd(s1-s2,q)=1 is imposed
prime by prime. The rank-three CRT frequency twist is h*(q/p)^2.

Small auxiliary shifts A0=q^(1/8), B0=X*q^(-1/8) satisfy 2*B0<p_min.
Thus both modular diagonals are the same integer multiset condition,
count O(B0^2). The union of the two bad hypersurfaces counts O(B0^3).
Diagonal, bad and generic terms give total O(X^4*q). Nonunit differences
are isolated before Holder and bounded by residue-class multiplicities.

At B=Y^(1/2),A=Y^(1/4),C=Y^(1/2),K=Y^(1/4), the SAME smooth MODEL
over this specified modulus class satisfies
  sum_q |E_q|<<Y^(127/128+epsilon)*J0^5*H^2+Y^(3/4+epsilon)*H*J0,
hence4071/4096 after caps. Joint periods, nonunit m*k, nonzero-frequency
extension corrections, both integer axes and overlap are paid. This
answers the preceding question for these two-prime moduli only. General
factorizations, prime powers in this box, full box coverage and original
arithmetic/sieve transfer remain OPEN; original-affine remains2b8cf98.

The first attempted route FAILED source applicability: after M-Poisson,
the ordinary Kloosterman sum S(h,r_q*m*k/a;q) leaves inverse-a support,
which is not the additive interval required by the checked Blomer--Pascadi
2607.24311v1 or Pascadi GAFA theorems. Freezing a leaves h too short for
their bounds to improve the Weil budget. Keep these useful sources and
the exact failure; no universal limitation of completion is asserted.

Five NEW exact tests passed normally in0.233s and under -O in0.335s.
Sol `/root/sieve_review` passed the theory, varying-X argument and actual
files, with no material correction. Three verifier-only corrections
fixed generator binding, float division and a vanishing complex fixture.
The pursuit began09:01:55 UTC and returns `changed-under-evidence` before
its09:32 UTC ceiling. No research process is left running at this checkpoint;
the overall goal remains active, with no claim of execution during pauses.
No old experiment was rerun or outside action taken. Next concrete
question: can CRT counting of bad primes replace the all-primes-small-shift
condition and save general squarefree moduli at this unbalanced box?
Test all bad-set/nonunit costs before promoting an extension.

## Previous pursuit: reciprocal energy saves the symmetric boundary

**af8f893**, `reciprocal_energy_kernel.py`, passed independent Sol review
of the critical proof, general family and actual files. Five NEW tests passed
normally in0.112s and under -O in0.110s. No correction was needed. The
pursuit began08:50 UTC and returned `changed-under-evidence` within30 minutes.

The new arithmetic mechanism averages a fourth-moment majorant over q.
For the reciprocal relation numerator
`D=(a1+a2)*a3*a4-(a3+a4)*a1*a2`, a nonzero D contributes only through
divisors of the common nonzero m*k*D. The D=0 rational relations are counted
by `(u*a3-v)*(u*a4-v)=v^2`, giving O(A^(2+epsilon)). This includes
non-diagonal relations such as1/3+1/6=1/4+1/4. Consequently
`sum_(q near C) E_(q,mk)(A) <<Y^epsilon*(A^4+C*A^2)`.
This is elementary and covers all integer moduli; no prime-only energy
theorem or unsupported composite extension is imported.

Holder and the inverse-residue multiplicity when B>q give
`R(B,A,C)=C^(3/4)*B^(3/4)*(B+C)^(1/4)*(A^4+C*A^2)^(1/4)`.
The full smooth model satisfies
`sum_q |E_q| <<Y^epsilon*H*J0^2*min(R(B,A,C),R(A,B,C))`.
The period Fourier series pays J^2 even with shared factors. The k count
cancels the kernel prefactor. Arbitrary bounded separated spatial weights
are allowed, and every mode is included without a Poisson-axis split.
At B=A=Y^(1/4),C=Y^(1/2),K=1 the exponent is15/16 before decorations
and3843/4096 after caps. More generally, valid boxes with b,x<=9/32 and
y<=1/2 have exponent127/128 before caps and4067/4096 after caps.

The common nonzero m*k across q is essential. Arbitrary t_q=q would make
every phase1 and invalidate the divisor step. Arbitrary coupled arithmetic
weights remain outside the separated-weight statement. The uniform smooth
coupled-weight corollary retains its already proved derivative hypotheses.

Next concrete UNTESTED question: at b=1/2,x=1/4,y=1/2, can completing
the long M variable and then averaging correlations of the resulting
ordinary Kloosterman sums over moduli save a power, with a,k nearY^(1/4)?
At this box the current energy budget is9/8 and the earlier linear budget
is1 before decorations. Neither budget is a lower bound on the true sum.
Do not extrapolate the newly proved symmetric region to all box geometries.

Full box coverage, original sieve/weight transfer, and the signed prime
correlation remain OPEN. Latest original-affine result is still2b8cf98.
All polynomial and previous kernel components are preserved. No old test
or experiment was rerun; no new prime coverage, actual zero, effective onset,
originality, publication, push, foreground work or installation is claimed.
Qwen remains unavailable without retry. No research process is left running
and no manual wake queue is armed; the overall goal remains active.

## Previous pursuit: the balanced saving covers all integer moduli

The symmetric boundary question pending below is now answered by the latest
pursuit above. Other geometries and the original arithmetic transfer remain.

**6852af6**, `all_moduli_balanced_kernel.py`, passed independent Sol review
of the prime-power proof, global transfer and actual files. Six NEW exact
tests passed normally and under -O, each in0.299s. No correction was needed.
The pursuit began08:34 UTC and returned `changed-under-evidence` within
30 minutes. No old experiment was rerun.

The pointwise bound `|F_q(h,l;t)|<=6^omega(q)*q*gcd(q,h,l,t)` is now PROVED
for every integer modulus and all parameters. Common valuation removal
keeps its all-zero case separate. Even exponents count cubic stationary
points; odd exponents include the quadratic Gauss sum. Mixed valuations,
zero parameters and bad primes2,3 are explicit. The previously checked
PRIME Kl3 bound is the only source input to this new local argument.
No prime-power correlation theorem is imported or proved.

The exact double period lift costs J^4, even when gcd(q,J)>1. A divisor
average gives O(Y^epsilon*H*J0^4*C) per modulus off the two integer axes.
For the FULL squarefull part u(q), split at Z=Y^(1/128). Small u costs
Z^(13/4) in the saved squarefree CRT estimate; large u occurs in
O(C*Z^-1/2) moduli. Both axes and their overlap retain the already proved
general-modulus bounds. At B=A=Y^(1/3),C=Y^(1/2),K=Y^(1/6), all integer
q near C satisfy
`sum_q |E_q| <<Y^epsilon*H*(J0^8*Y^(23/24)*Z^(13/4)+J0^4*Y*Z^-1/2+J0*Y^(2/3))`,
hence exponent4085/4096 with J0,H<=Y^(1/4096). This removes the previous
squarefree restriction at that MODEL box, including arbitrary joint short
periods and nonunit m*k. The finite tests guard exact algebra and budgets;
they do not replace the analytic proof or its checked source input.

Next concrete UNTESTED question: which remaining box geometries resist the
combined model estimates, and what mechanism beats their critical boundary?
At B=A=Y^(1/4),C=Y^(1/2),K=1, both the ordinary composite linear estimate
and the current squarefree bilinear estimate reach Y before decorations.
A proposed regrouping or new correlation input must demonstrate a strict
saving there with all modulus, coefficient and period costs included.
Do not mistake a budget obstruction for a lower bound on the true sum.

Other box geometries, the original sieve/weight transfer, and the actual
signed prime-correlation estimate remain OPEN. Latest original-affine
estimate is still2b8cf98. Polynomial identities and bounds remain useful
components. No new prime coverage, actual zero, effective onset, originality,
publication, push, foreground work or installation is claimed. Qwen remains
unavailable without a retry. No research process is left running and no
manual wake queue is armed. The overall research goal remains active.

## Previous pursuit: squarefree correlations beat the balanced budget

The following prime-power question was pending at this historical checkpoint;
the latest pursuit above now settles its pointwise and balanced-model parts.

**7d36ce8**, `squarefree_correlation_kernel.py`, passed independent Sol
source/theory and actual-file review. Seven NEW exact tests passed normally
in0.191s and under -O in0.190s. The pursuit returned `changed-under-evidence`
within30 minutes. A transient briefing overstatement was corrected: one
partition factor can be D^-1/2, not D^-3/4. The saved proof uses <=1,
and a regression fixture retains this boundary.

FKM arXiv1211.6043v3 Theorem1.17, Proposition3.1 and sections3/6 have
NOW been read. Only the PRIME bounded-exceptional-pair result is used.
CRT fixes two residue classes for each exceptional choice, yielding a
derived squarefree bilinear estimate with factors
`q^-1/4+M^-1/2+q^(1/4)*N^-1/2`. Bounded coefficients and the multiplier
may be nonunits: exact gcd partitions pay their costs. The normalized
inverse-product definition, including K_q(0)=1/q, is explicit. No
composite KMS/FKM theorem or prime-power correlation theorem is imported.

An exact local F_p expansion handles every nonunit frequency pattern.
Its four degenerate prime assignments have rescaled mass g/D^2 and
bounded costs in all three bilinear terms. After shared-period splitting,
both integer axes AND their subtracted overlap are included. At the SAME
balanced box B=A=Y^(1/3),C=Y^(1/2),K=Y^(1/6), all SQUAREFREE q near C
now satisfy `sum_q |E_q| <<Y^(23/24+epsilon)*H*J0^8+Y^epsilon*H*J0*B*A`,
hence exponent11803/12288 for J0,H<=Y^(1/4096). This includes small
prime factors and balanced semiprime cores. The previous13/12 bound
remains valid, but this additional mechanism beats it on squarefree q.

Next UNTESTED question: prove or refute the pointwise prime-power bound
`|F_q(h,l;t)| <<q^(1+epsilon)*gcd(q,h,l,t)`, retaining unequal valuations,
zero parameters and p=2,3. Even exponents suggest cubic stationary-point
counting; odd exponents require a quadratic Gauss sum as well. If it holds,
test its period-qJ transfer (conservative J^4 cost), then split off the
squarefull part u of q at u=Y^(1/128). The small part should cost at most
u^(13/4) in the saved squarefree CRT bound. Large squarefull parts occur
in O(C*Y^(-1/256)) moduli; an averaged pointwise bound of H*J0^4*C per
modulus would make that tail small. The anticipated exponent4085/4096
is UNPROVED until every one of these steps is checked. Do not treat this
next hypothesis as an established prime-power extension.

Prime powers, further box coverage, original sieve/weight transfer and
the signed prime correlation remain OPEN. Latest original-affine result
is still2b8cf98. All polynomial components remain tools. No old experiment
was rerun; Qwen remains unavailable. No process is left running and no
manual wake queue is armed. Overall goal active; no publication, push,
foreground work or installations.

## Previous pursuit: composite completion works but the balanced budget fails

**c2a5ac5**, `composite_linear_kernel.py`, passed independent Sol review
of the transforms, full theory and actual files, with no correction.
Six NEW exact tests passed normally in0.774s and under -O in0.769s.
The pursuit returned `changed-under-evidence` within30 minutes. Both the
useful component and the critical failure are retained.

For ALL integer moduli q near C=Y^y, including prime powers, the same
smooth box model with arbitrary joint period J_q<=J0 and k<=H*B*A*C/Y
satisfies `sum_q |E_q| <<Y^epsilon*H*(J0^2*min(A,B)*C^(3/2)+J0*B*A)`.
Neither gcd(J_q,q)=1 nor gcd(m*k,q)=1 is required. One complete Fourier
transform gives an ordinary Kloosterman sum; periodic lifting costs J^2.
A divisor average absorbs the nonzero-frequency gcd loss. The h=0 mode
uses a separate restricted Ramanujan decomposition and the modulus average
of gcd(q,m*k). All modes and normalization factors are included.
Only the ordinary composite Weil bound from Topacogullari1506.02608v1,
section2 p4, is used; no composite KMS or shifted-divisor theorem is imported.

The bound saves a power when `min(b,x)+3*y/2<=127/128`, with final exponent
4067/4096 for J0,H<=Y^(1/4096). At the critical balanced box b=x=1/3,
y=1/2, it instead gives13/12 BEFORE decorations. That is a failure of
THIS upper-bound budget, not a lower bound on the true error or a no-go
theorem. A next step must save more than1/12 there and pay coefficient costs.
The prime-core theorem and all polynomial tools remain preserved.

Next UNTESTED hypothesis: bound additive autocorrelations of multiplicative
Kl3 dilates, then test a composite bilinear estimate by CRT. Explicitly
handle prime diagonal cases, nonunit coefficients and prime powers. KMS
Remark1.2 cites Fouvry--Kowalski--Michel, Algebraic trace functions over the
primes, arXiv1211.6043, Theorem1.17. That exact theorem has NOT yet been
read here; this is only a primary locator, not a composite consequence.
Do not repeat the completed linear-completion test or call its identity
the missing bilinear estimate. Critical composite boxes, original sieve
transfer and the signed prime correlation remain OPEN; latest original
affine estimate remains2b8cf98. No old experiment was rerun. Qwen remains
unavailable; no process is left running and no manual wake queue is armed.
Overall goal active. No publication, push, foreground work or installations.

## Previous pursuit: every smooth prime-core hyperbola box is covered

**1ab2d03**, `hyperbola_prime_kernel.py`, passed independent Sol review
of the linear lemma, full theory and actual files, with no correction.
Five NEW exact tests passed normally in0.222s and under -O in0.226s.
They guard the Fourier zero convention, progression transforms and exact
boundary budgets; the proof owns continuous analytic uniformity.
The pursuit returned `changed-under-evidence` within30 minutes.

The theorem now allows B=Y^b,A=Y^x,P=Y^y,K=B*A*P/Y throughout
`1/5<=b<=13/25, 0<=x<=(1-b)/2, 0<=y<=1/2`. Keep c=s*p with p prime
near P, bounded joint periodic weights, and S,J0,H<=Y^(1/4096). The bound
remains `Y^(127/128+epsilon)*S^4*J0^4*H` plus the same smaller exceptional
terms, hence `Y^(4073/4096+epsilon)`. Nonempty boxes force p>sJ and k<p.

For y<=49/100, pointwise complete-sum bounds suffice. In the remaining
strip, x>=1/16 is handled by keeping l separate and grouping w=k*|h|;
the bulk exponent is(103*y+12)/64<=127/128. For x<1/16, the exact finite
Fourier transform of normalized Kl3, extended by1/p at zero, is an
ordinary Kl2 sum at nonzero frequencies and zero at frequency0. Smooth
linear completion on l=r+T*j has j-scale p/A<=p, even if the l-scale
exceeds p. All prime-axis modes, bad p|m and the thin dual-length strip
below1 are counted. Arbitrary bounded linear coefficients are NOT allowed.

This closes the full box-range gap in the smooth decorated MODEL. The
latest ORIGINAL-AFFINE estimate remains2b8cf98. General composite cores,
the costed original sieve/weight transfer and the signed prime-correlation
estimate remain OPEN. Polynomial identities and bounds remain tools.
Next concrete test: can factorization or completion give a power saving
for general composite cores in the critical modulus boxes, retaining
nonunit modes and the actual coefficient costs? Do not assume a composite
KMS theorem. No old experiment was rerun; Qwen remains unavailable.
No process is left running at this checkpoint. Overall goal active; no
manual wake queue, publication, push, foreground work or installations.

## Previous pursuit: small modulus factors and arithmetic periods are costed

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
The previously untested frequency-regrouping option has now been completed
by1ab2d03 above for the whole MODEL box family. Balanced composite cores,
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
Latest tests: `python -m unittest test_optimized_cofactor_cutoff.py` and the
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

The web PDF screenshot tool returned a string without an image payload
in this pursuit, with some fetch timeouts. A supported changed route used
urllib plus the already installed PyMuPDF, then view_image, to inspect
the KMS conjugation bars. Use `python -X utf8` when printing extracted
source text; the default cp1252 stdout failed on mathematical Unicode.
The one temporary source PNG was removed after inspection. No installs.

Local Git author identity was unset. If still needed, use the previous
commit's author through per-command `git -c user.name=... -c user.email=...`.
Stage only owned paths and run `git diff --cached --check` before commit;
plain diff does not inspect untracked new files. No push. Preserve clean
checkpoints and honest terminal evidence. The latest pursuit finished at a
natural reviewed checkpoint; no research process is claimed still running.

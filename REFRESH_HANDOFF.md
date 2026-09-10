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
Latest reviewed RESEARCH commit: **151e7c9**, adjacent_polynomial_norm.py.
Pursuit2026-09-10 02:25:27--02:45:30UTC: changed under evidence.
The proposed polynomial norm closure for N^.41<=n<N^.46 is falsified.
At beta=19/25 the first-power T exponent is
21/50-(13/25)h, positive from517/2500 at h=.41 to113/625 at h=.46.
The k=2 exponent is negative and licensed, but it controls D_M^2,
not D_M or the first-power arithmetic field. The detector threshold
only applies on selected detected zeros; no lower bound bridges the
fourth moment to the full arithmetic coefficient. Guinand transfer
and proper-power payment remain small at support .46 but do not repair
this. Independent Sol review PASS after correcting one prose exponent;
five guards normal/-O passed. This is a route limitation, not an
all-method barrier; retain the k=2 component and paid .46 tail.

Next concrete question: can the core n<N^.41 be decomposed bilinearly
with a genuinely short factor? Test a Vaughan-style Type I/II split
preserving both reflected prime conditions and hard endpoints. Type I
needs progression Poisson; Type II needs a sourced bilinear mean-square.
Any positive exponent or unpaid endpoint falsifies that route. Fresh
<=30min, UNREVIEWED.

Previous **bda7f22**, prime_companion_dispersion.py.
Pursuit2026-09-10 02:25:27--02:44:21UTC: progress.
The ACTUAL conjugated and reflected cofactor tail is now paid down
to n>=N^.46, improving the previous N^.51 cutoff. For the intermediate
band, BOTH proper-power replacements are separately paid before using
characters; the left norm is N^-49/400 L^(11/2). With m prime>B,
q=dm has conductors dividing d or containing m. The exact low
projection is 1_(m does not divide a)*A_d(a)/(m-1); its mask stays.
BV on d<=B pays O(L^(2-D)). Primitive large sieve plus induced-lift
weights and binary endpoint decomposition gives high variance
(NQ+N^2/M)L8. The periodized shift weights give a high contribution
L6*(N^-1/1000+N^-91/2000). This is an ACTUAL two-prime estimate.

The full T=N^.9 reflected band still equals -R_h-R_(r_core)+all-log,
but now r_core=a_B*1_(n<N^.46)-delta_1-h. The signed core is OPEN.
The bounds are uniform in literal tail endpoints and extend to a
profile f with |f(U)|+Var(f) bounded, U>=N^.46. Variation alone
is insufficient. This also pays the auxiliary a_B exp(-n/N^.47)
overlap, with a below-cutoff norm error N^-.01 L^(5/2). This does
not replace the original N^.45 detector damping or license a zero mask.
Independent Sol theory/actual-file/profile PASS; eleven guards
normal0.017s/-O0.011s. Harcos primitive large sieve Theorem2 p1
was checked directly; the endpoint maximum stays INSIDE the residue sum.

Next concrete question: do retained polynomial moments and zero
density bounds give an all-log SMALL NORM for the actual coefficient
b(n)=a_B(n)*1_(N^.41<=n<N^.46), convolved with Lambda? Test
squares (fourth moments) on compact beta strips and cubes near1,
including every zero copy and actual real part. Verify source ranges,
epsilon losses and relative near1 bins; no fixed epsilon near1.
The zero-to-prime transfer must be paid at the NEW upper cofactor
scale N^.46. Success pays this adjacent cofactor band in both forms;
an unpaid exponent, endpoint or transfer loss is the falsifier.
Fresh <=30min, UNREVIEWED. No arbitrary masked-field bound is assumed.

### 2026-09-10: first-power polynomial norm route falsified

Pursuit02:25:27--02:45:30UTC changed under evidence; commit151e7c9.
The adjacent first-power T-term exponent at beta=19/25 is
21/50-(13/25)h, positive from517/2500 to113/625 for h=.41..46.
The saving k=2 detector moment controls D_M^2 on detected zeros,
not D_M or the full arithmetic field. The threshold gives no lower
bound on the nondetected complement. Transfer and proper-power errors
remain small but do not bridge these objects. Independent review PASS;
five guards normal/-O passed. This preserves the k=2 component and
paid .46 tail; it is not an all-method barrier.

Next question: can n<N^.41 be decomposed by the retained exact Vaughan
identity into Type-I progression pieces and a Type-II bilinear piece,
keeping its free convolution factor, both reflected prime conditions
and hard endpoints? Any positive exponent or dropped endpoint falsifies
that route. Fresh <=30min, UNREVIEWED.

Previous **9470731**, large_cofactor_overlap.py.
Pursuit2026-09-10 02:06:50--02:23:12UTC: progress.
The complementary range n>=N^.51 now has an ACTUAL all-log-small
overlap, both CONJUGATED and NONCONJUGATED REFLECTED. More generally
any fixed eta>.509 works; equality is not licensed. Expanding the
small divisor gives q=dm<=4N^.499. BV discrepancies are paid with
sum_(m|q)Lambda(m)=logq, including prime powers and hard endpoints.
Resonant reduced-residue lattice sums are bounded by tau(q), not
assumed zero. The main costs N^-1/10 L9; freezing N^-9/10 L5,
cutoff N^-2 L5, opposite proper powers N^-1/4 L4. Only the BV
error is all-log rather than a fixed power. ALL left powers remain.

The reflected calculation uses l=N-k+r, c=k/(N-k), and
D_c(s)=int hatChi(y)hatChi(s-cy)dy, with Fourier transform
(2pi)^2 chi(-c*xi)chi(-xi). Residues are N+r modq, and Poisson
retains exp(-2pi*i*ell*N/e). The actual FULL band at T=N^.9 is
 sum chi*chi*J_N/N = -R_h-R_(r_<)+O_A(L^-A),
r_<=a_B*1_(n<N^.51)-delta_1-h. This uses the previously paid
full-field bridge BEFORE the arithmetic split, not a new weighted
J or masked-zero inference. Corrected inherited central Guinand
cross error is N^-2/5 L6, square N^-4/5 L12. The smaller residual
and its signed combination with h remain OPEN, as do other heights
and universal Goldbach coverage. No positive reflected energy claim.
Independent Sol theory/actual-file PASS after that error-rate fix;
eleven guards normal0.010s/-O0.014s.

That pursuit's next question, now answered inbda7f22, was whether the PRIME companion creates a useful
gap between small and large character conductors in q=d*m? Test
the remaining range N^.46<=n<N^.51. First pay left proper powers
using the actual upper cofactor support; then m is prime, exceeds
B, and a conductor dividing dm either divides d or contains m.
Derive the exact character decomposition with all induced coprimality
masks, hard endpoints and reflected target phases. Test whether
low conductors can be paid by the window cancellation and the large
ones by a sourced mean-square/large-sieve estimate. A heuristic
shift-average threshold would allow q<N^.55, suggesting .46 as a
concrete target, but this has NOT been proved. Falsifier: an unpaid
small-conductor, endpoint, character multiplicity or Cauchy loss.
The reviewed exact conductor argument and its scope are recorded above.

Previous **de84c06**, short_divisor_overlap.py.
Pursuit2026-09-10 01:41:02--02:04:10UTC: changed under evidence.
For arbitrary |b_d|<=1,d<=B=2N^.009, the COMPLETED coefficient
v_b(k)=sum_(d|k,d<=B)b_d log(k/d) has a central window field satisfying
 sup_x |P_vb(x)|/sqrtN <<_(M,K)
 L^2(T^-M+V^-K)+L(B/(N/T))^M.
Thus it is O_A(N^-A) for every fixed A. This is an ACTUAL estimate,
but elementary: progression Poisson, vanishing Fourier moments and
the gap B<<N/T suffice. It needs no prime distribution or Mobius
cancellation. The initially derived BV proof remains valid as an
alternative all-log estimate, with its weighted variation and source
losses paid. Do not describe BV as the ingredient causing this saving.

For a_B=mu_<=B*1, KEEP ALL prime powers in a_B*Lambda=v_mu.
With r_B=a_B-delta_1-h, the exact complex conjugated balance is
 C_h+C_r=-E_Lambda+O_A(N^-A), E_Lambda>=0 and O(1).
No positive lower bound for E_Lambda is claimed. The complement r_B
includes cofactor lengths up to the product scale, not merely the
original short good-polynomial sum. C_r remains unpaid, with only
O(L^(5/2)) direct overlap budget. The survivor connection retains
its previous all-log transfer error. No sign for C_h or the original
NONCONJUGATED reflected Goldbach pairing has been established.
Independent Sol theory/actual-file PASS including the elementary
strengthening; nine guards normal0.007s/-O0.006s.

That pursuit's next question, now answered in9470731, was whether BV could control the complementary cofactor
range n>=N^(3/5) in its actual conjugated overlap? Product k~N then
forces m<=2N^(2/5), so expanding a_B gives moduli q=d*m below
4N^.409. Keep ALL Lambda(m), the actual cofactor endpoints, and
the complex shift kernel. Test the exact reduced-residue Poisson
main even when q is comparable to or larger than N/T; do not assert
that every lattice is annihilated. Charge multiplicities in the
modulus sum (the candidate identity is sum_(m|q)Lambda(m)=logq),
weight variation, Fourier tails and opposite prime powers. Success
requires an actual saving for this restricted complementary range;
an unpaid resonance/main term or modulus loss is the falsifier.
The reviewed strengthening is recorded above. It does not
claim that the bad range n<=2N^.41 falls within BV's modulus level.

Previous **8173dbe**, in detector_gram_coercivity.py:
the proposed DISK-ONLY homogeneous coercivity/inverse inference is false.
Exact artificial Gram G=[[1,r],[r,1]], r=19/20, multipliers-1+-i/2
and c=(1,-1+i/2) give norm7/20 but POSITIVE mixed overlap1/8.
An inverse quotient also diverges as r approaches1. A stronger model
uses ONE real |b(n)|<=1 polynomial on an allowed bad block, exponent
m=2atan(.5)/(pi+atan(.5))~.2572, and actual-shaped N-phase coefficients.
Its mixed overlap stays positive after normalization. These are NOT
actual zeros or the true truncated-Mobius coefficients. The model's
unnormalized scale N^-3/5 does not falsify actual inequalities with
additive all-log errors. Polynomial tools and special arithmetic
coercivity remain possible; no all-method barrier is proved.

For the ACTUAL detector, the mixed CONJUGATED overlap now has an
explicit short-shift arithmetic form with h(n), the complex window
kernel K_N(nm,nm+r), and TWO GENUINE prime conditions m,nm+r.
Only0<|r|<=N^(1/10)*logN is retained; all-log errors pay the rest.
The kernel is T^-1 Schwartz at difference scaleN/T. Its tail Schur
bound cancels the T^2/N prefactor; coefficient logs costL^3.
Original diagonal prime/square terms vanish, and higher powers cost
N^-23/30 L2. All proper powers can then be removed: h*Lambda_pp
has normalized window norm N^-59/400 L^(11/2), from tau^3<=tau8;
the opposite proper-power overlap costs N^-1/4 L4. All masks persist.
This is a reduction of the overlap obstruction, NOT a signed saving
or the original nonconjugated reflected Goldbach pairing.

Independent Sol theory/actual-file PASS; nine guards normal/-O0.001s.
Pursuit2026-09-10 01:24:30--01:39:27UTC: changed under evidence.
That pursuit's next question, now tested in de84c06, was whether the NONZERO SHIFT AVERAGE in this exact
actual sum give a saving when the specific a_T(n)=sum_(d|n,d<=B)mu(d)
is expanded BEFORE Cauchy? Keep both prime conditions and the complex
kernel. Test whether the extra r-average supplies a genuine signed
estimate, compared with the current O(L^(5/2)) overlap bound, or
whether a definite residual still consumes the gain. A formal main-term
identity or removal of prime conditions is not success. Do not redo
the completed Gram models, diagonal or prime-power estimates. Fresh
<=30min; the completed estimate and explicit residual are recorded above.

Previous **45f87c0**, in high_detector_weighted_bridge.py:
the remaining H-weighted HIGH exterior is now paid. Consequently ALL
previously removed zeros have all-log-small H-weighted energy, and the
actual central survivor field satisfies
 theta*Z_(H,R)=-theta*P_(h*Lambda)/sqrtN+O_L2,A(logN^-A)
for every fixed A. The bad cofactor mask and smoothing stay in h.
This closes the weighted deletion error in this transfer, NOT the
inverse problem, signed prime correlation, or Goldbach coverage.

The old zero-saving corner beta=5/6,h=2/5 is repaired by the known
Ivic density bound A(sigma)<=3/(2sigma), verified in TTY2501.16779v1
Table2 p33 and the author-maintained ExpDB Corollary11.31. Its base
energy exponent is-19/300, so square/cube Holder gives-3/200,-1/50
before epsilon, instead of the old Huxley ZERO. No actual zero there
is asserted. Use this epsilon-loss source ONLY on compact[4/5,7/8):
750 fixed bins, epsilon1/10000, all losses paid, energy N^-1/200 L153.
For beta>=7/8 use retained LOG-POWER Huxley and relative u bins
(.99v,v], v=(1/8)*.99^j. The worst exponent after weight loss is
-17v/325<-v/20. VK and O(loglogN) bins give stretched-exponential
decay in logN. Never replace that step with fixed epsilon/bins.

The lower high strip[19/25,4/5) is paid at N^-1/400 times logs.
The corrected source Gamma recurrence extends uniformly to delta
in[.26,.3], licensing the restricted Type II count. Its bad powers
6,5,4,3/2 now switch at h=.39; the OLD .38 switch fails here.
For non-Type-II zeros, GM plus each full good-polynomial moment
gives a weighted saving; k>=2 and convexity pay even p=.82.
The exact signed detector equation then pays H_N, including its
constant term. It requires no new detection predicate on this strip.

The actual newly weighted one-coordinate J contribution is all-log
small, including J-minus-beta and endpoint errors. Independent Sol
theory/actual-file PASS; eight guards normal0.101s/-O0.083s.
Pursuit started2026-09-10 01:08:59UTC, reassessed01:22:55UTC: progress.

The next question at that checkpoint was whether Re H_N<=-1/4 supports
a coercive inequality for the actual packet synthesis or reflected
pairing? First test the exact finite Gram form: negative multiplier
values on individual copies need not imply a negative operator when
the packets overlap. If the disk alone fails, preserve that precise
limitation and express the missing term using the actual common
Dirichlet polynomial and its prime-product transfer. Test whether the
checked moments pay that term; do not silently assume a bounded
inverse, rename the original correlation as a proof, or infer a
barrier for all polynomial tools. This test is now completed in8173dbe.

Previous **b42ab25**, in weighted_detector_mask_bridge.py:
the FULL H_N-weighted removed middle strip and LOW exterior are now
paid. All middle Type II copies have weighted energy N^-1/125 times
logs, using pure moments at their actual lengths and360 fixed beta bins.
For G minus II, full-good polynomial moments plus the saved exact signed
zero equation control H_N, giving weighted energy N^-4/625 times logs.
This covers EVERY good-detected middle zero, not only the high-M slice.
Low exterior beta<=16/25 has weighted energy N^-11/3750 L72:
powers4,4,3,2 of the four bad gaps fit the broader low-beta moment
range, with the beta=0 layer-cake baseline explicitly retained.
Union weighted energy is N^-11/3750 times logs. Its one-coordinate
ACTUAL J sum has central exponent7489/7500, finite-period3557/3750,
and beta-endpoint-3193/3750. All new complex-weight errors are paid.
The exact central L2 survivor bridge is now
Z_(H,R)=-P_(h*Lambda)/sqrtN-Z_(H,beta>=19/25)+small.
At that checkpoint ONLY the H-weighted HIGH exterior remained unpaid;
45f87c0 above now pays it. The signed prime correlation remains open.
The completed test examined the high exterior against actual applicable
density and pure/mixed moments. Test the critical corner beta=5/6,
bad length exponent h=2/5 FIRST: retained Huxley gives base energy
exponent-1/30, whereas H^2 and H^3 moments give+1/30 and+1/15,
so the natural Holder combinations reach ZERO, not a saving. Verify
the strongest applicable primary density input before treating this
as a method limitation. No actual zero at that corner is asserted.
This test is completed above; do not repeat the old corner experiment.
Previous **5b7dd4e**, in mixed_detector_weighted_mask.py:
mixed products D_M^r D_H^s, at their ACTUAL length M^r H^s in
[N41/50,N49/50], pay the H-weighted energy on good-M detected zeros.
The threshold costs2r logs; weighted Holder preserves N^-4/625.
For EACH bad multiplier H, use ANY compatible good detecting M of
the zero, assigning to the least compatible one to avoid duplication.
The covered coefficient C_cov has energy N^-4/625 L40230.
Its one-coordinate ACTUAL finite-period paired sum is all-log small:
central exponent623/625, newly paid J-minus-beta2367/2500, and
beta endpoint-2133/2500. No old unweighted error is silently reused.
For m=logM/logN in[.44,.45], gaps1/2 are fully compatible; gap3
requires h<= (.98-m)/2 and gap4 h>=.82-m. The rectangle
m in[.44,.45],h in[.34,.36] is outside this specific criterion,
not a general impossibility or evidence about actual zeros.
The proposed higher-moment test is completed above and superseded
by the stronger entire-middle-strip result. Its reviewed high-M
component remains in the new module for possible later reuse.
Previous **5bd0b48**, in detector_prime_product_transfer.py:
the FULL actual H-weighted zero field has a prime-product window with
coefficient h*Lambda and uniform error O(N41/200 L7). The exact
dilation n^-1/2 S_T(x/n) is retained down to x/n~N59/100, even
when T>x/n. An Ingham tangent gives W_T(y)<<T L6 on that range.
The full normalized field has L2 norm O(L5/2), from the exact
majorant tau*Lambda=(tau log)/2 and Schur on the PRODUCT index.
Removing exp(-n/sqrtT) costs O(N^-1/25 L5/2) in that full norm;
the bad-length mask remains. The unrestricted identity
a_T*Lambda=mu_<=B*log cannot replace this restricted convolution.
The survivor disk does NOT yet transfer: H can amplify removed zeros,
and their H-weighted energy remains uncontrolled. A proposed aggregate
H^2 fourth-moment shortcut was RETRACTED in review: upper support .82
cannot replace shorter product scales in the weighted coefficient norm.
A component at m=.35 has squared length .7 and POSITIVE energy
budget7/125, not the saving falsely obtained by substituting .82.
No weighted finite-period J transfer or new paired saving is claimed.
The proposed mixed-moment criterion is completed above. Its uncovered
length pieces remain for that criterion; other weighted-moment choices
have not been excluded. The Type II and exterior weighted masks remain.
Previous **ec39d86**, in signed_zero_detector.py:
delete ALL middle-strip Type II zeros, including ones also Type I,
and combine exterior/Type-II/good-length masks BEFORE Gram. Their
overlap costs only the sum of nonnegative coefficient energies.
Every ACTUAL survivor now satisfies |1+H_N(rho)|<=3/4 for ONE
common polynomial H_N=sum of all bad-length D_M. In particular
Re H_N<=-1/4 and |1/H_N|<=4. Its support is <=2N41/100.
The source smoothed identity, inclusive dyadic endpoints and count
are paid uniformly. This is NOT a sign estimate for the paired kernel.
The direct geometric inverse has actual residual norm
O((3/4)^J N21/100 L) by the crude copy energy and Gram bound.
J of order logN is SUFFICIENT to make that bound power-small;
the straightforward support majorant is exp(O((logN)^2)). Neither
is a necessary degree/length lower bound. Existing fixed-power
moments do not control this changing-degree expansion. Preserve the
disk and reciprocal for use with another arithmetic ingredient.
The proposed full-field prime-product transfer and error test is now
completed above. Its survivor-mask bridge remains OPEN; do not repeat
the transfer or replace the restricted convolution by the full identity.
Previous **8911d43**, in detector_power_length_filter.py:
remove every ACTUAL middle-strip zero detected at ANY allowed length
M with N41/50<=M^k<=N49/50 for some integer1<=k<=100. Its energy
is O(N^-4/625 log^C N), giving an actual paired-union bound
N623/625 times logs plus the paid errors. Powered coefficients,
thresholds, changing beta, copies and dyadic sums are all paid.
Surviving detector length exponents logM/logN lie only in four OPEN
gaps: (49/300,41/250), (49/250,41/200), (49/200,41/150),
(49/150,41/100). Every detecting length must lie there, not just
the least one. The signed paired sum over those survivors is OPEN.
Previous **0b1a7ba**, in zero_detector_band_reduction.py:
the ACTUAL smooth T=N9/10 band now reduces, with all-log error, to
zeros with BOTH beta in(.64,.76) AND a classical zero detector
|D_M(rho)|>=1/(3logT), at some allowed dyadic length M. Nondetected
middle-strip columns have coefficient energy N^-6/125 times logs,
so their ACTUAL paired union costs N122/125 times logs plus the
paid finite-period errors. Least detecting length gives disjoint lists;
no saving for the remaining detected-pair sum is yet proved.
Primary Maynard--Pratt2206.11729v2 Definition22/Lemmas23-24 and
Appendix C are unconditional here; DO NOT import Hypothesis F.
Source correction: printed pp37-38 use Gamma(beta-.5+iu) after
a contour with real part .5-beta. The actual negative argument is
retained and bounded by Gamma recurrence on the fixed beta interval.
The rendered PDF confirmed the discrepancy; bound and uniformity
are repaired in the module. Copies and overlapping source types paid.
Previous **e368c38**, in rapid_complementary_phase.py:
an N-dependent dense positive ARTIFICIAL model with phase
lambda_N*a+N^-1/10*sin(N1/10*(a-1/2)) has exact paired value
-cN+O(N9/10), c>0, while its normalized exact-window projections
against EVERY phase in the common bounded C3 class, with |g'|>=c,
are O(N^-1/10). This includes the prior controlled prime-phase class.
All O(K) derivative cells, Euler cost, exact-window errors and periodic
averaging are paid. Thus the marginal controlled-phase tests alone
cannot imply paired cancellation. This model lacks prime support,
Type I identities and actual zeta-zero structure. Its growing higher
derivatives are outside the existing prime theorem; no contradiction
or new actual band bound. Turn next to actual zero-detecting structure.
Previous **043cfe0**, in zero_packet_realpart_localization.py:
within the ACTUAL smooth T=N9/10 band, the contribution from pairs
where EITHER real part is <=16/25 or >=19/25 is O_A(N/log^A N)
for every fixed A. Only BOTH real parts in(.64,.76) remain for this
band, still O(N). A Gram bound pays masked energies by L times the
coefficient square sum; actual prime energy is used only for the full
factor. Ingham, GM with its fixed epsilon/grid charged, and Huxley/VK
pay the deleted regions. Multiplicities, intersection subtraction and
actual finite-period errors remain. This does not delete the full core.
The natural exact phase expansion is admissible but its raw l1 cost
lies between N2/5 L and N1/2 L6, too large for the prior sufficient
budget. This failure does not rule out regrouping or other uses of
the phase/polynomial tools. The full signed Goldbach margin is OPEN.
Previous **276d174**, in window_phase_projection.py:
the exact normalized ACTUAL prime window has O(N^-1/44 log^3N)
projection against controlled varying phases; the actual zero moment
has the same bound plus its paid N^-2/5 log^6N displacement error.
A conditional decomposition of the reflected zero window, with common
phase/amplitude bounds, coefficient mass A_N and L2 residual R_N,
would bound the ACTUAL weighted T=N9/10 band by
N[(N^-1/44 L^3+N^-2/5 L^6)A_N+R_N]+N^.9L^12+N^-.7L^13.
No such small-cost decomposition is established; the unconditional
band remains O(N) and the signed Goldbach margin is still OPEN.
Previous **5886079**, in varying_prime_phase.py:
ACTUAL Lambda sums are O(N43/44 L^3), hence O(N49/50), uniformly
for N-dependent C3 phases with |f'| and |f'+u f''| bounded below,
derivatives1..3 bounded above, and C1 amplitudes of bounded sup+TV
on a fixed support. Short factor shifts retain actual Vaughan weights
and full product masks. Bounded nonzero affine slopes are included;
unrestricted slopes are not included in this particular criterion.
Previous **bad0caf**, in analytic_prime_curvature.py:
ACTUAL Lambda correlation with the sine phase is O(N39/40 log^3N),
hence O(N79/80), on any fixed smooth support in(1/2,3/4), uniformly
in its affine slope. Vaughan's actual coefficients and all Type II
product masks are retained. The reusable criterion requires BOTH
|f''| and |(u^2 f'')'| bounded above/below on a fixed support interval.
It also proves o(N) for ANY FIXED nonaffine real-analytic complementary
phase h(u)+h(1-u)=0, with arbitrary affine slope. The latter is a
qualitative fixed-phase statement, not uniform over changing h.
No improved paired-band bound or signed Goldbach margin follows.
Previous **a6edeb7**, in analytic_complementary_phase.py:
one dense positive ARTIFICIAL sine-phase model has exact paired main
-cN+O(N9/10), yet centered correlations with EVERY FIXED-DEGREE
polynomial probe are O(N^(1-9/(10*(D+2)))). Constant/linear probe
coefficients are arbitrary; nonlinear coefficients have a fixed bound.
The same model works for each fixed D; no growing-degree uniformity.
Thus the proposed inverse step from those probe bounds to paired
cancellation fails. Prime support, Type I and actual correlations stay open.
Previous **293fb8b**, in cubic_prime_chirp_exclusion.py:
the ACTUAL Lambda coefficient against the model's global cubic phase is
O_psi(N63/64), uniformly in all lower polynomial coefficients. The model
instead has (N/4)int psi+O(N7/10). Checked Le--Spencer II Theorem5,
m=1,b=0, applies Harman's known general-polynomial bound; nearest
reciprocal q~N21/10, smoothing and proper powers are paid. This excludes
one coherent global cubic mechanism. It does not improve the actual
paired-window O(N) bound or provide the signed Goldbach lower margin.
Previous **1689968**, in complementary_window_chirp.py:
an N-dependent dense POSITIVE ARTIFICIAL coefficient model reinforces
the exact central paired window as -cN+O(N9/10), c>0, despite all
listed interval/energy bounds and centered smooth linear Fourier sums
O(N7/10). Complementary cubic phases add to an odd multiple of pi.
This is not Lambda, actual zero data, prime support or a Goldbach
counterexample. It limits one proposed transfer from marginal bounds.
Previous **ba1747b**, in short_prime_window_energy.py:
at T=N9/10, fixed real smooth chi in(1,2), the ACTUAL moment is
uniformly O(sqrtN) for x in[N/4,3N/4], its da-energy is O(N), and
the ACTUAL COMPLEX chi-weighted comparable J_N band is O(N).
Prime support, proper powers, beta displacement, beta endpoints and
the actual finite-period remainder are all paid. No small constant,
all-log deletion or sufficient signed lower margin follows.
Previous **b816865**, in finite_period_ratio_convolution.py:
the ACTUAL weighted complex unequal-tag family is all-log small through
the FULL endpoint transition, with individual heights KN for fixed K.
Exact Gamma-Laplace convolution pays every integration range and retains
the original smooth weight1-Psi. Concrete theta53/64, epsilon1/1170
and the current eta>N17/20 mask give
N^(25583/25600)L^55+N^.91L^15. No stationary ceiling remains for THIS
selected family. Comparable high heights and the signed margin stay OPEN.
Previous **0172597**, in guth_maynard_ratio_cancellation.py:
the ACTUAL COMPLEX selected unequal-tag sum is all-log small through
individual heights N/2, for fixed theta<59/71 with its source epsilon
paid. Concrete theta53/64, epsilon1/1170 give decay1/1280; on the
current separate eta>N17/20 core the total costs
N^(25583/25600)L^54+N^.91L^14. Both actual errors and the N/2 ceiling
are licensed by tag asymmetry. The full signed lower margin stays OPEN.
Previous **6942c66**, in guth_maynard_spectral_cancellation.py:
the ACTUAL COMPLEX sum with BOTH heights<=N^kappa is all-log small for
EVERY fixed kappa<13/15. A fixed-epsilon Guth--Maynard bound is used
only away from real part1, with log-power Huxley/VK retained near1.
The actual stationary error stays N^(91/100)log^14N. Concrete cutoff
is now17/20: the core has max height>N^(17/20), with prior axes/strip
and original cap. The previous theta4/5 tag deletion remains with the
new separate column mask. The full signed lower margin remains OPEN.
Previous **3421a80**, in arithmetic_prime_offset.py:
the REAL actual smooth band equals the ordered odd-prime sum
sum logp logq Re W_[p/(p+q)](p+q-N)+O_chi(sqrtN log^7N), where
W_a(k)=(1/pi)int chi(av)chi((1-a)v)exp(-ikv)dv. The transfer pays
all finite-period, localization, ratio-change and prime-power errors.
Even nonnegative chi cannot give nonnegative coefficients on every even
offset: at a=1/2 their total is0 but the offset0 coefficient is positive.
A narrow permitted chi gives Re W_[1/2](100)<0. This refutes ONE
positivity mechanism, not an actual negative total or an all-method claim.
The signed prime correlation and full Goldbach lower margin remain OPEN.
Previous **55401fd**, in arithmetic_beta_transfer.py:
the ACTUAL COMPLEX finite-period smooth comparable-band sum
sum chi(gamma/N)chi(eta/N)J_N(rho,sigma) is O_chi(NlogN), with
chi fixed real smooth in(1/100,1/50), no RH and all beta/copies retained.
An exact beta-integral transfer uses the arithmetic energy; the missing
negative half-line and positive tail are explicitly paid. The model's
Nlog^2N reinforcement is excluded in this ACTUAL coupled band. The new
bound is still too large for an all-log deletion or the full signed margin.
Previous **15b36b9**, in arithmetic_zero_energy.py:
the ACTUAL moment family has int_(1/3)^(2/3)|S_N(aN)|^2 da <<_chi NlogN.
This is a frequency integral at FIXED N, not a target average. The sharper
uniform approximation S_N(x)=-P_N(x)+O_chi(log^6N) pays the off-critical
displacement with Ingham density. Smooth sampling and Chebyshev then pay
the energy. All beta and prime powers remain. No coupled-kernel transfer
or new deletion follows from this alone; the signed lower margin is OPEN.
Previous **3bee966**, in arithmetic_zero_moment.py:
for actual zeros, fixed real smooth chi compactly supported in(1/100,1/50),
and EVERY real N/3<=x<=2N/3, the complex moment
sum_(gamma>0) chi(gamma/N)*x^(rho-1/2) is O_chi(sqrtN logN).
The unconditional Guinand formula, entire Fourier cutoff and a rapidly
weighted prime window pay all errors, retaining actual beta and copies.
At x=N/2 this excludes the model's imaginary moment of order NlogN.
This is an actual arithmetic constraint beyond counting; no part of the
remaining BILINEAR sum is deleted by this moment alone. Its margin is OPEN.
Previous **6fb7829**, in spectral_count_resonance_model.py:
a GLOBAL BUT N-DEPENDENT artificial critical-line spectrum can obey
the smooth RVM count with O(1) error, all used density envelopes and
local occupancy, yet its ACTUAL finite-period smooth comparable-band
sum is -C_chi Nlog^2(N/2)+O(Nlog^(3/2)N+sqrtN log^2N), C_chi>0.
A quarter-shifted lattice, count-preserving upward rounding, sharper
central remainder and separately paid endpoint prove this. It limits
uniform deductions for THAT weighted band from the listed counting
inputs only. It is not actual zeta, a fixed spectrum across N, a full
unweighted-sum obstruction, Goldbach counterexample or all-method barrier.
Previous **da07ce0**, in linear_height_ratio_cancellation.py:
the ACTUAL COMPLEX signed contribution of selected strongly unequal
dyadic rectangles is paid through the fixed LINEAR ceiling N/10. For
tags G<=H^theta, fixed1/2<theta<9/11, the main costs
N G^(11/20)H^(-9/20)log^52N, with both actual approximation errors paid.
Choose theta=4/5 in the current core: eta>N^(4/5) is a separate column
mask, giving total O(N^(124/125)log^54N+N^(91/100)log^14N). Delete
that exact dyadic union and its transpose from the preceding C_high.
The more comparable high heights and full signed lower margin remain OPEN.
Previous **2f03381**, in unequal_spectral_cancellation.py:
for EVERY FIXED kappa<5/6 the ACTUAL COMPLEX sum over
0<gamma,eta<=N^kappa is O_(A,kappa)(N/log^A N). Unequal-scale TT*
and discrete transfer remain uniform at vanishing height ratio; the
different energies E_G(NG/H), E_H(N) both have a positive density gap.
The summed actual stationary error is O(N^(91/100)log^14N). The concrete
retained cutoff is4/5: C_high now has max(gamma,eta)>N^(4/5), both>V_N,
difference>W_N and the original smooth height-sum cap. Its signed lower
margin remains OPEN. No5/6 endpoint or all-height estimate is claimed.
Previous **feb00a9**, in discrete_spectral_cancellation.py:
the ACTUAL COMPLEX signed sum over both heights in(T,2T],T=N^(2/3),
is O_A(N/log^A N), also after subtracting the paid near-height strip.
Continuous mixed-phase TT*, fixed-frequency discrete transfer including
coincident zero copies, and a smooth beta-parameter expansion cost
logT times sum N^(2beta-1). Source-checked Ingham/Huxley log-power
density and Vinogradov-Korobov zero-free input pay that energy. This is
actual signed cancellation in a band of absolute mass >>Nlog^2N.
It deletes this specified band; other heights and the full margin remain OPEN.
Previous **fb3da0f**, in stationary_spectral_core.py:
actual zeros in(T,2T],T=N^(2/3), have >>Nlog^2N termwise absolute
kernel mass INSIDE the retained core, even after the near-height strip
is removed. A uniform finite-period stationary main and beta reflection
prove this WITHOUT RH. It is not a signed lower bound or no-cancellation
claim. The signed band equals an explicit positive-amplitude cosine sum
with PAID O(N^(31/45)log^12N) error; the cosine sum remains OPEN.
Previous **0fed151**, in spectral_height_envelope.py:
for each fixed kappa<(52+16sqrt3)/121=0.658783577860..., pairs with
BOTH heights<=N^kappa have O_A(N/log^A N) absolute mass. The concrete
retained cutoff is13/20. The new finite C_high has both heights>V_N,
their difference>W_N, max height>N^(13/20), and the original smooth
height-sum cap. The signed lower margin and all-log R error remain.
The displayed kappa_* is only this Ingham upper-envelope boundary;
no actual-mass lower bound, universal barrier, RH or coverage follows.
Previous **b2554fd**, in spectral_low_axis_bound.py:
uniformly1<=V<=sqrtN, pairs with min(gamma,eta)<=V and both heights<=KN
have absolute mass <<_K log^14N[N exp(-c1 sqrtlogN)+sqrtN V]. Thus the
single V_N=sqrtN exp[-(loglogN)^2] deletes the whole low-height axes
with O_A(N/log^A N) error. This contains every fixed N^theta,theta<1/2
eventually. No RH, numerical onset, or saving at V=sqrtN is asserted.
The finite signed core now has BOTH heights>V_N and separated ordinates.
Its lower margin remains OPEN, with the inherited all-log R error.
Previous **9f47ce4**, in spectral_near_height_bound.py:
the ENTIRE near-height strip |gamma-eta|<=exp[(alpha/30)sqrt(logN)],
0<gamma,eta<=KN, costs O_(A,K)(N/log^A N) absolutely, WITHOUT RH.
Here alpha=min(1,sqrt c) uses the retained classical zero-free constant;
there is no numerical width/onset claim. Product multiplicities and
different real parts at the same height are included. The finite signed
remainder now has separated positive heights and the original smooth
height-sum weight. Its Goldbach lower margin remains OPEN.
Previous **6abc250**, in spectral_diagonal_bound.py:
the ENTIRE identical-complex-location diagonal through height KN, including
m(rho)^2 pairs at a zero of multiplicity m, costs O_(A,K)(N/log^A N)
absolutely, WITHOUT RH or simple zeros. A uniform partial-interval kernel
bound, classical zero-free region and uniform Ingham density pay it.
Distinct locations at the SAME height remain in the open signed sum.
No full square-root error, prime-pair coverage or numerical onset follows.
Previous **4c69475**, in nonstationary_spectral_reduction.py:
for fixed delta>0 and fixed smooth Psi=0 belowpi+delta, =1 abovepi+2delta,
the FULL positive-height pair tail weighted Psi((gamma+eta)/N) has signed
size O_delta(sqrtN log^40N). Axes, support growing like logN, seminorms,
and bounded coupled tails are paid. The surviving pair sum has
gamma+eta<=(pi+2delta)N. The combined R formula has O_A(N/log^A N) error,
NOT a square-root error: retain the inherited N sqrt(logN)exp(-c sqrt(logN))
opposite-sign loss. This correction was caught by the author and reviewed
before promotion. The finite surviving signed lower bound stays OPEN;
no hard/shrinking cutoff, practical zero certificate or new coverage.
Previous **793b135**, in smooth_endpoint_cancellation.py:
for each FIXED REAL G in C_c^infinity((8pi,9pi)^2), the ACTUAL signed
weighted pair sum Re sum G(gamma/N,eta/N)J_N is
O_G(sqrtN logN+log^2N), WITHOUT RH, target averaging or a PNT asymptotic.
A smooth endpoint projection becomes a real weighted prime sum by parity;
the leading endpoint multiplier is imaginary. The two-zero error must be
paid through single-zero estimates and a tensor expansion. Subleading
beta terms and all endpoint errors are paid. This is a nonempty smooth
region, not the full signed lower bound, hard band, or shrinking window.
Previous **c901fc3**, in spectral_endpoint_obstruction.py:
for actual zeros of heights in (8piN,9piN], the ordered pair kernels have
termwise absolute mass >>Nlog^2N, WITHOUT RH. A uniform endpoint expansion
and functional-equation symmetry prove this even though the bulk phase
has no stationary point. Thus absolute deletion of that full band fails.
Its interior remains useful: a FIXED smooth cutoff vanishing nearpi gives
total absolute mass O_chi(N^-1log^2N) on the same band. No shrinking-cutoff
or whole-tail claim. Signed cancellation and the Goldbach margin stay OPEN.
Previous **cca6455**, in one_sided_zero_reduction.py:
the opposite-height-sign zero interactions, and the same-sign square on
its damped half-period, cost O_A(N/log^A N) for every fixed A, WITHOUT RH.
The surviving term is C_(N,T)=e/pi Re integral_0^pi e^(iNt)Z_(+,T)^2 dt,
with ordered positive-height pairs and their diagonal. It remains SIGNED.
Classical zero-free-region input plus a uniform radial L2 bound proves
the suppressed norm; the prior full norm and licensed T=C NlogN pay
the cross term and truncation. No arbitrary-total-truncation claim,
positive margin, new coverage, numerical onset or zero certificate.
Previous **02448f6**, in pointwise_zero_pair_gate.py:
an ACTUAL unconditional one-period Fourier transfer gives, for each
integer N, R(N)=2psi(N-1)-N+B_(N,T)+O(sqrtN log^(5/2)N+log^4N).
B is the specified signed pair of zeta zeros with a FINITE-PERIOD kernel;
all zeros to T=C_A NlogN suffice with the proved tail. This pays the
pointwise approximation, NOT the one-sided lower bound for B. No RH,
new coverage, practical zero certificate or effective onset is asserted.
CRITICAL new source correction: arXiv1606.00860 Lemma5.1/Section6
supersedes the O(sqrtN) Cesaro error still printed in arXiv1206.0251
and the2015journalPDF. Correct normalized Cesaro error is O(N), and
the exponential-sum remainder includes a constant1. Use the correction.
Previous **98dc8b7**, extending critical_cubic_sieve.py: regrouping the
retained triprimes gives an all-log small diagonal O_kappa(x^(5/6)L^(3/2)),
but the SAME open dilation covariance with semiprime rows. The automatic
extra-average hypothesis is retired; no generic trilinear impossibility.
Previous **c0f70ca**, in critical_cubic_sieve.py:
the MOVING cutoff sqrt(n) is reached for U_3 with ACTUAL total error
O(x*(loglogx)^4/log^2x)=o(x/logx). Its fixed-power small-prime deletion
cost is O(kappa*log(e/kappa) S_2(N)x/logx), uniform for fixed small kappa.
On the retained squarefree support, odd factor counts>=5 vanish exactly
and the triprime coefficient is24*product(logp/logn). The remaining
even-class sum E_kappa and triprime sum T_kappa obey prime mass
=B_P-E_kappa-24T_kappa+small errors. Their signed margin stays OPEN;
no new coverage or numerical onset. This pays a specific endpoint
coefficient, not arbitrary Type I at square-root level.
Previous **85e7d44**, extending
polynomial_rough_localization.py: direct Mellin integration reduces the
ACTUAL fixed-power localization to degrees k>=4 with O(kappa) relative
loss, and degree3 with O(kappa*(2+log(gamma/kappa))) loss. The full
absolute a+b pairing is main-scale bounded for every k>=3. No signed
residual estimate or positive margin follows. k=2 fails this positive
majorant calculation only, not every quadratic approach.
Previous **3882437**, in
polynomial_rough_localization.py: the preserved full polynomial sieve
coefficient admits ACTUAL fixed-power rough localization with loss
O_(gamma,k)((kappa+1/L)S_2(N)x/L), k>=9, fixed0<kappa<=1/20. Its
remaining signed composite sum has fewer than1/kappa prime factors.
This is a different exact coefficient and remainder; it does not prove
the original hard-H localization or estimate the retained correlation.
Previous **16fa2d0**, in
rough_mobius_dilation.py: the actual long-Mobius term can also be made
coprime to the target with all-log error. A classical Ramare identity
then has no reconstruction residual; its full diagonal cost is all-log
small. The exact signed off-diagonal energy, with every mask retained,
remains OPEN. This completes the multiplicative-sign criterion test;
it does not establish the required correlation estimate.
Previous **3def1c4**, in
specialized_sieve_coefficients.py: an ACTUAL Type I/fundamental-lemma
estimate removes small prime factors from the surviving smooth-cofactor
error, after which repeated factors cost O(x log^2x/y). Thus the remaining
term has ordinary long Mobius coefficients on rough squarefree integers.
Its linked prime correlation remains OPEN. The coefficient and support
extraction is complete; its multiplicative-sign criterion test is now
completed above. Neither reduction supplies the actual signed estimate.
Previous **a301a46**, in
prime_producing_comparison_gate.py and critical_factor_mass.py: the existing
comparison satisfies the source factor-pattern conditions, and an ACTUAL
upper sieve bounds critical composite mass by C e S2(2x)x/logx with C
independent of small e. A specified short-factor Type II estimate would
therefore imply positivity without pointwise divisor boundedness. That
signed estimate remains OPEN; no new unconditional coverage. Its proposed
coefficient-family extraction is now completed above.
Previous **ed0d334**, in rough_liouville_transfer_gate.py:
the cubic-rough Liouville mean is (log2-1)Y times the test integral,
and its short inclusion-exclusion layers are all-log small. The signed
prime-partner criterion is exact but OPEN; inspected Liouville correlation
sources do not supply its masks or quantifiers. Its proposed comparison
and prime-producing-sieve input check is now completed above.
Previous **cb01376**, in prime_factor_endpoint_gate.py:
the asymmetric full log-factor moment is already TI-controlled; the precise
composite-only deficit remains open. The exact odd prime endpoint isY/3,
and a classical parity sequence has full fixed-scale factor laws but no
primes. This is a source-checked application and an input boundary, not
new coverage. Its proposed signed Liouville test is now completed above.
Previous **cb04788** is a direct APPLICATION of the
saved cutoff-freedom theorem: every complete nontrivial divisor layer is
TI-small for the ACTUAL prime error. Its prime-range pieces may cancel
large individual contributions. The isolated rectangle variance is no
longer a required next gate. The full prime-compensation gap remains OPEN.
Previous **bd7d1e4** supplies an explicit ARTIFICIAL error
with strong Type I, bounded size/L2 and Fourier supremumY^.50018 logY,
yet large semiprime-row variance and positive polynomial-family sum>>YlogY.
This refutes a generic transfer from those controls, NOT the actual prime
error or Goldbach. A naturally weighted variance target and its actual
small diagonal are retained; the two variance conditions are not ordered.
Previous **6a7c8ac** proves that EVERY factor
choice in Maynard III Theorem1.2 misses a two-prime modulus family inside
the numericalY^.5002 level. Its fixed-polynomial density mass is c logY
and its actual Gamma contribution has positiveY logY scale; neither is a
bound on the centered prime error. A precise intact-variance target and
negligible actual diagonal are preserved in factored_prime_ap_transfer.py.
Previous **06acf3b** transfers Maynard III's
uniform-residue theorem to an ACTUAL signed divisor component with factored
moduli up to Y^0.5002. Canonical factorizations retain the prime and bounded
polynomial weights; moving residue m, model comparison and prime powers
are paid. This is a restricted subset, not full beyond-half TI or coverage.
Previous **dc7baa6** proves actual main-scale
ABSOLUTE remainder mass for some central even target at every large Y,
simultaneously for every normalized cutoff in the stated family. Taking
absolute values after regrouping at n does not remove this obstruction.
Its extra small-delta condition and positive physical rectangle are explicit.
Latest JOINT ARITHMETIC bound **c19cb24** gives O(Y S_2(m)/logY) per
polynomial-cutoff prime/cofactor box, using corrected Henriot. It remains
useful for narrow bands; the full signed correlation remains OPEN.
Previous **02e1627** proves exact cutoff freedom, the classical optimal
cofactor norm, and its failed separate-moment budget O(Y sqrt(log Y)).
Previous **3fcea6e** removes the internal proper prime powers with an
o(Y) error and retains the exact prime/cofactor correlation, still OPEN.
Combined short HB terms do not cancel internally.
Previous **b7134e1** proves fixed divisor-weighted Type I and the precise
scope of the Heath-Brown route; these remain useful components.
Previous GLOBAL balanced correlation transfer **476e0c3** removes
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
Previous checkpoint **4adb690** preservedcb04788.
Previous checkpoint **a650b77** preservedbd7d1e4.
Previous checkpoint **d87403b** preserved6a7c8ac.
Previous checkpoint **10321f3** preserved06acf3b.
Previous checkpoint **6d0a20b** preserveddc7baa6.
Previous checkpoint **65bf94b** preservedc19cb24.
Previous checkpoint **35cc1e4** preserved02e1627.
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

For the selected spectral lane first read `nonstationary_spectral_reduction.py`,
then `smooth_endpoint_cancellation.py`,
then `spectral_endpoint_obstruction.py`,
then `one_sided_zero_reduction.py`,
then `pointwise_zero_pair_gate.py` and its CORRECTED source locators.
The remaining prime correlation is now
an explicit one-sided signed zero-pair target; the earlier sieve route is
also preserved. For that unexceptional lane read `critical_cubic_sieve.py`,
then `polynomial_rough_localization.py`
and its required joint-bound source `polynomial_joint_majorant.py`,
then `rough_mobius_dilation.py`,
then `specialized_sieve_coefficients.py`,
`critical_factor_mass.py` and `prime_producing_comparison_gate.py`, then
`composite_bilinear_bridge.py`
for the saved nonnegative comparison and exceptional-character correction.
The source(b.1)/(b.2), growth and fixed-divisor Type I checks are complete;
the full short-factor Type II remains open. The older framework setup and
rough Liouville source-fit test are also complete. Do not repeat them.
Use `prime_factor_endpoint_gate.py` for the precise one-sided factor deficit.
Use `resonant_semiprime_error.py` for the complete-layer correction,
then `factored_prime_ap_transfer.py`,
then `absolute_remainder_obstruction.py`,
then `polynomial_joint_majorant.py`,
then `optimized_cofactor_cutoff.py`,
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

## Latest pursuit: actual phase projection and a conditional finite-period band

Started23:24:22 UTC, reassessed23:30:15 UTC, progress. Reviewed
mathematics **276d174**, after the checked5886079 component below.
Let F_N=P_N/sqrtN be the actual arithmetic window and Z_N=S_T/sqrtN
the actual zero moment. For common fixed buffered supports and bounded
C1 amplitudes w_N, the exact adjoint substitution v=Tlog(u/a) gives
int w_N e^-iTf_N F_N=(1/N)sum Lambda(n)sqrt(u)w_N(u)
*chi(u f_N'(u))*e^-iTf_N(u)+O(T^-1+V^-16), u=n/N.
The uniform prime theorem gives O(N^-1/44 L^3) projections; actual
Z_N=-F_N+O(N^-2/5 L^6) supplies the zero version. All normalized
Jacobians, buffer displacements and Schwartz tails are paid.

For B_Z=2zeta(a)Z_N(1-a)/sqrt(a(1-a)), a decomposition into these
admissible phases with coefficient l1 mass A_N and L2 residual R_N
would give normalized central bound
(N^-1/44 L^3+N^-2/5 L^6)A_N+R_N. Choose the actual beta cutoff
zeta=1 on[.3,.7]. Reusing the completed beta/finite-period transfer
adds normalized errors N^-.1L^12+N^-1.7L^13. Thus fixed
A_N=O(N^kappa), kappa<1/44, and R_N=O(N^-sigma), sigma>0,
would pay this ONE weighted comparable band at all-log precision.
Example kappa1/100,sigma1/50 has main power543/550. This is a
conditional bridge, NOT a constructed expansion or actual band deletion.
Sol theory/actual-file PASS; six guards normal0.001s/-O0.000s.
No new source fetch or actual prime/zero run for this follow-on.

Next concrete question, UNREVIEWED: does the NATURAL reflected-zero
expansion meet the decomposition budget? Candidate exact terms have
phase f_sigma(a)=-(eta/T)log(1-a), amplitude
w_beta(a)=2zeta(a)a^-1/2(1-a)^(beta-1), and coefficient
c_sigma=chi(eta/T)N^(beta-1)exp(i*eta*logN). Verify the common
phase/C1 bounds and pay A_N=sum|c_sigma|. Actual zero-counting and
reflection appear to force A_N at least N2/5 logN for nonzero chi,
while the existing density moment bounds it above by N1/2 L^6.
Test those claims with multiplicities and cutoffs kept. If they hold,
the direct natural expansion fails this l1 budget even though every
individual phase is controlled; do not turn that method-budget failure
into a lower bound for the actual signed band. No new zero computation
or old model experiment is needed. Fresh <=30 minutes. Overall goal
active; full signed margin and decomposition/compression gap OPEN.

## Previous pursuit: uniform varying phases via short arithmetic factor shifts

Started23:17:32 UTC, reassessed23:24:22 UTC, progress. Resumed verified
clean main3e0cb0d; reviewed mathematics **5886079**. Previous native
goal turn made progress through fixed analytic-phase cancellation.
Actual sums against controlled N-dependent C3 phases cost
N43/44 L^3, hence N49/50. The first-derivative lemma uses discrete
increments and their total variation, without assuming monotonicity.
Vaughan U=V=N1/22 pays Type I in N1/10 L^2. Shifts R~N1/22
in the shorter factor give squared Type II cost
N^2/R+N^2*K*logR/(T*R), with K<=O(sqrtN). Actual coefficients,
diagonal, triangular shift weights and intersecting products are kept.
The phase bounds are |f'|,|f'+u f''|>=c, derivatives1..3<=C.
Varying C1 amplitudes need only bounded sup+TV on a fixed support.
Bounded affine slopes are included; unrestricted slopes are not.
Robert Section3.3 Lemma1 printedp8 was checked in the web PDF;
the finite-shift inequality is also proved directly with conjugation.
Sol theory/actual-file PASS; seven guards normal0.001s/-O0.001s.
No actual prime/zero run or outside action. All corrections and
runtime limits remain; the exact-window transfer is reviewed above.

## Previous pursuit: actual prime factorization excludes fixed analytic alignments

Started23:06:52 UTC, reassessed23:15:26 UTC, progress. Resumed verified
clean maind3aad7a; reviewed mathematics **bad0caf**. Previous native
goal turn made progress by falsifying the proposed polynomial inverse
step. Actual Lambda against the sine phase, with fixed smooth support
inside(1/2,3/4), is O(N39/40 log^3N), hence O(N79/80). Its model
instead has (N/4)int psi+O(N1/10) against its own phase.

Vaughan U=V=N1/5 gives Type I N17/20 L+N11/20 L^2. The exact
free convolution1 remains in B_U; no unexceptional-branch assumption
was imported with the elementary identity. Type II keeps arbitrary
actual normalized coefficients and the full product intersection.
For M>=K, MK~N, phase-difference curvature is
-T/m^2 [G(mk/N)-G(mr/N)], G(u)=u^2 f''(u).
The nonzero G' gives the complete box cost
N[K^-1/2+T1/4 M^-1/2+T^-1/4]. Diagonal, weighted variation, one
coefficient logarithm and O(log^2N) boxes are paid. Robert's author
PDF Section3.1 Theorem1 printedp5 eq6 supplies the discrete second-
derivative bound. Web PDF reading worked; separate urllib hash retrieval
failed certificate verification, with no bypass or unchanged retry.

Reusable criterion: fixed support and uniform positive lower/upper
bounds for BOTH |f''| and |(u^2 f'')'|. The log phase shows why the
second condition cannot be dropped. A corollary treats every FIXED
nonaffine real-analytic h on(0,1) with h(u)+h(1-u)=0. Each curvature
has only finitely many zeros on the compact support. Fixed-delta
deleted neighborhoods cost O(delta N)+o(N) by the already checked
Yamada interval bound and proper powers; the good pieces save a power.
Take limsup N first, delta->0 second: the actual correlation is o(N),
uniform in affine slope but with no uniform rate over h or delta.

Sol theory/actual-file PASS; seven guards normal0.002s/-O0.004s.
No actual prime/zero run, publication or outside action. N-dependent
nonlinear phases and joint superpositions remain outside the corollary.
The actual comparable-band O(N) and full signed margin are unchanged.
All polynomial components, source corrections and runtime limits persist.

The then-next question, answered in5886079 above: can bounded factor differencing
give a power saving UNIFORMLY for N-dependent C^3 phases without
requiring nonzero second curvature? On a fixed positive support I,
assume |f'| and |f'+u f''| have fixed positive lower bounds and
the first three derivatives have fixed upper bounds. Try U=V=N1/22
and a shift cutoff R~N1/22 below the shortest factor tag. Type I
has angular derivative T*d/N=o(1) for d<=UV. Type II differences
have derivative ~T*h/N=o(1) for h<=R, and derivative variation
O(T*h/N). Prove an applicable discrete first-derivative bound with
that variation; do not assume monotonicity. Preserve shifted product
intersections and actual coefficients in the bounded-shift inequality.
Candidate Cauchy bound: N^2/R+N^2*K*logR/(T*R), K<=O(sqrtN),
giving N43/44 times logs before a fixed spare exponent. This is NOT
yet reviewed or proved. It would include affine phases and controlled
N-dependent nonlinear phases, but not arbitrary rapidly varying phases.
Fresh <=30 minutes; overall goal active, Goldbach signed margin OPEN.

## Previous pursuit: one analytic model defeats the proposed polynomial inverse step

Started22:57:58 UTC, reassessed23:04:46 UTC, changed-under-evidence.
Resumed verified clean mainf3ba9a7; reviewed mathematics **a6edeb7**.
Previous native goal turn was progress: actual cubic-phase exclusion.
The proposed quintic falsifier led to a stronger single model, avoiding
repeated higher-degree tests: f_N(a)=lambda_N*a+sin(a-1/2)-(a-1/2),
lambda_N->3 with Tlambda_N odd*pi, T=N9/10. Positive dense weights
b_N=1+(1/2)cos(T f_N) retain the exact window expansion, with error
N2/5, and the no-conjugation paired main -cN+O(N9/10), c>0.

For every FIXED D>=1, fixed smooth psi of compact positive support,
and polynomial g of degree<=D, allow arbitrary constant/linear
coefficients and fixed bounded nonlinear coefficients. The centered
correlation against exp[-iTg(n/N)] is uniformly O(N*T^-1/(D+2)).
This is N7/10 for D1 and N41/50 for D3. Consecutive derivatives
D+1,D+2 kill the polynomial and supply a sine/cosine partition;
an elementary derivative-lemma induction and every Poisson alias are
paid. Arbitrary linear coefficients use exact frequency reduction.
The SAME model works for each fixed D, with degree-dependent constants
and onset. Growing degree, unbounded nonlinear coefficients, and
increasingly localized spatial cutoffs are outside the statement.

This falsifies the specified model-shared inverse implication. It does
not transfer the model to Lambda or invalidate all polynomial tools.
Prime support, Type I, explicit formula and linked prime covariance are
not supplied. Actual comparable-band O(N) and signed lower margin
remain unchanged. Sol theory/actual-file PASS; seven guards normal
0.005s/-O0.003s. No material correction, external source search,
prime/zero experiment, outside action or claim of post-stop execution.
All earlier source corrections and runtime limitations are preserved.

The then-next question, answered and extended inbad0caf above: does actual multiplicative
decomposition exclude the sine alignment with a fixed power saving?
For fixed psi smooth supported in(1/2,3/4), test the ACTUAL sum
sum psi(n/N)Lambda(n)exp[-iT f_N(n/N)]. Reuse Vaughan's exact
identity from unexceptional_vaughan_gate.py, including the essential
free convolution1; that identity itself needs no unexceptional branch.
Try U=V=N1/5. Source-check a discrete second-derivative sum bound.
Candidate Type I budget N17/20 times logs comes from d<=N2/5.
For Type II, orient M>=K with MK~N, both>=N1/5; the phase-difference
curvature uses (u^2 f''(u))', bounded away from0 on the fixed support.
Test the candidate estimate N[K^-1/2+T1/4 M^-1/2+T^-1/4] times logs,
whose worst exponent is39/40. Keep product masks, actual arithmetic
coefficients, weighted variation and diagonal terms. An N79/80 target
would leave room for logarithms; it is NOT yet proved. This would
identify a concrete arithmetic constraint beyond the fixed-degree
tests, not settle the full paired prime correlation. Fresh <=30 minutes.
Overall goal remains active; the Goldbach signed lower margin is OPEN.

## Previous pursuit: actual primes exclude the model's coherent cubic coefficient

Started22:46:05 UTC, reassessed22:56:14 UTC, progress. Resumed verified
clean main6eabd32; reviewed mathematics **293fb8b**. Previous native
goal turn made progress through an actual comparable-band bound and
the complementary model mechanism. For T=N9/10, any fixed smooth psi
of compact positive support and arbitrary N-dependent lambda_N,
sum psi(n/N)Lambda(n)exp[-iT(lambda_N*n/N+(n/N-1/2)^3)]
is O_psi(N63/64). The lower coefficients are unrestricted.

Primary authority: Le--Spencer, Intersective polynomials and Diophantine
approximation II, author PDF at
https://home.olemiss.edu/~leth/papers/intersective_polynomials_II_2.pdf,
Section4 Lemma5 printedp8 and Theorem5 printedp9 with m=1,b=0;
printedp3 notation and printedp6 weight also checked. Nearest integer
to Q0=2pi*N21/10 gives reduced numerator-1 and error<q^-2.
For every prefix X~N, the bound's bracket is O(N^-1/2) and its outer
power is1/16. Epsilon1/64 yields63/64. Fixed smooth partial summation
and proper powers O(sqrtN log^2N) preserve that exponent.

For the previous model's bounded slope, its own-phase coefficient is
(N/4)int psi+O(N7/10); both residual cubic harmonics are paid by the
existing Poisson argument. This is an application of a known arithmetic
theorem, not external novelty or a new paired-correlation estimate.
Sol theory/actual-file PASS; six guards normal0.001s/-O0.001s. No
corrections were required. Original Harman PDF route returned abstract
HTML; Citeseer mirror timed out. The author-hosted PartII PDF worked.
The monomial-only Kumchev theorem was not extended by assumption.
No actual prime/zero computation or outside action. All polynomial
components, earlier source corrections and runtime limits persist.

The then-next question, answered and strengthened ina6edeb7 above: does large negative paired-window
correlation force a large coefficient against a bounded smooth cubic
phase? Test a falsifier before using any such inverse implication:
replace the model's odd cubic by (a-1/2)^5 while retaining the odd-pi
complementary sum. For every fixed bound on the coefficients of a
cubic g, test uniform centered correlations against exp[-iTg(n/N)]
of size O(N*T^-1/5)=O(N41/50), while the exact paired window stays
-cN+O(N9/10). Pay the local window, fifth-derivative oscillation and
all Poisson aliases. This would test the sufficiency of a specified
probe family, not actual primes or every possible polynomial tool.
Fresh <=30 minutes. Full signed margin OPEN; overall goal active.

## Previous pursuit: complementary phase reinforcement survives linear Fourier control

Started22:38:16 UTC, reassessed22:43:56 UTC, changed-under-evidence.
Resumed verified clean main6cf340d; reviewed mathematics **1689968**.
Use the SAME exact arithmetic-window operator with artificial weights
b_N(n)=1+(1/2)cos[T f_N(n/N)], T=N9/10,
f_N(a)=lambda_N a+(a-1/2)^3, lambda_N->3 and Tlambda_N an odd pi.
The operator has main (1/4)sqrt(aN)chi(a f'_N(a))exp[iT f_N(a)]
and uniform discretization error N2/5. Since f_N(a)+f_N(1-a)=lambda_N,
its no-conjugation central paired functional is -cN+O(N9/10), c>0.
The negative constant is1/8 times the positive cutoff integral.

The dense positive weights satisfy the interval-mass, global-mass,
pointwise window and energy INEQUALITIES used inba1747b. Nevertheless
their centered global Fourier sums with ANY fixed smooth spatial
cutoff are O(NT^-1/3)=O(N7/10). Poisson's zero alias has a nonzero
constant third derivative; every other alias is nonstationary and
summably paid. All statements retain N-dependence and smooth cutoffs.
This model has no actual prime support, zeta explicit formula or Type I
claim. The older bd7d1e4 Ramanujan/modulus countermodel was checked;
this one identifies a different complementary additive-phase mechanism
in the present window operator. No general barrier or negative actual
Goldbach sum is asserted. Sol theory/actual-file PASS; six guards
normal0.002s/-O0.002s. Full signed margin OPEN; overall goal active.

The then-next question, answered in293fb8b above: can an ACTUAL prime polynomial-
phase estimate exclude this very cubic modulation? For any fixed smooth
psi, test sum_n psi(n/N)Lambda(n)exp[-iT f_N(n/N)]=O(N^(1-delta))
for some explicit fixed delta>0. The model instead has an order-N
coefficient against its own phase. Source-check a primary theorem for
cubic exponential sums over primes, including uniformity in all lower
coefficients and its full denominator range. The leading angular
coefficient has size T/(2piN^3); a reciprocal rational approximation
has denominator q~N^(21/10), with error O(q^-2). Pay smoothing and
prime powers, and verify the actual permitted saving rather than
guessing a remembered Weyl exponent. Success would exclude THIS
coherent modulation for primes; it would not estimate a superposition
of arbitrary phases or the full paired correlation. Fresh <=30 minutes.

## Previous pursuit: short prime windows control a comparable band at main scale

Started22:25:14 UTC, reassessed22:36:11 UTC, progress. Resumed verified
clean mainc6421fc; reviewed mathematics **ba1747b**. Previous native
goal turn was progress: the selected unequal family crossed the full
endpoint transition. At T=N9/10 the ACTUAL smooth moment S_T(x) is
O(sqrtN), its central da-energy is O(N), and the actual complex
chi-weighted J_N band is O(N). This surviving comparable band is not
deleted: no all-log bound or small constant was obtained.

New source: Yamada2312.16090v1 Theorem2 printedp3 eq13, k=a=1,
weakened to the prime-interval upper bound2y/logy. Prime-power shell
mass is paid separately by O((R/sqrtN+1)L^2). For effective window
H=N/T=N1/10, all R>=H shells have Lambda mass O(R); Schwartz decay
pays the apparent wider Fourier cutoff. Weighted Schur uses row H,
column1/T and sum Lambda(n)/n=O(1), giving T^2*H/T=N. The actual
Guinand replacement error is N1/10L^6, beta endpoint N^-7/10L^13,
and actual J_N replacement N9/10L^12. All are paid with multiplicities.
Sol theory/actual-file PASS; six guards normal0.020s/-O0.019s.
The original Montgomery--Vaughan institutional-copy route returned403;
the permitted Yamada primary source supplied the needed theorem.

A source check for the next decision found GM2405.20552v2 Corollary1.4,
printedp3, applies to almost-all intervals of length at least X^(2/15+eps).
It does NOT supply an asymptotic at our X1/10 window. Do not substitute
prime existence or lower-density results for that missing asymptotic.

The then-next question, answered in1689968 above: can complementary smooth phase
modulation reinforce the paired window functional at order N even
while obeying the new interval/energy bounds and strong global Fourier
cancellation? Test positive artificial coefficients
b_N(n)=1+(1/2)cos[T f_N(n/N)], f_N(a)=lambda_N*a+(a-1/2)^3,
lambda_N->3 chosen so T*lambda_N is an odd multiple of pi.
The exact symmetry f_N(a)+f_N(1-a)=lambda_N may make the paired
window negative of order N. Prove the local-window approximation,
its full discretization costs, and a smooth global Fourier bound
O(N*T^-1/3)=O(N7/10) for b_N-1. This is a proposed model of ONE
reinforcement mechanism, not actual primes, zeta zeros or an all-method
barrier. Compare with the older semiprime-modulus countermodel before
claiming a distinct result. Fresh <=30-minute pursuit.

## Previous pursuit: exact convolution crosses the endpoint transition

Started22:16:52 UTC, reassessed22:23:42 UTC, progress. Resumed verified
clean main9d0edd8; reviewed mathematics **b816865**. The previous
native goal turn made progress through the actual prime-offset formula
and its positivity falsifier. This pursuit uses the EXACT identity
J_N=e/(2pi) int_0^infinity exp(-x/N)K_pi(N-x)B_x dx,
B_x=2x^(rho+sigma-1)Gamma(rho)Gamma(sigma)/Gamma(rho+sigma).
NIST DLMF5.9.1 was checked, including its positive-real-part conditions.
Finite-list Fubini is absolute. The quotient has the saved phase and
only a G^-1 Gamma remainder; the finite-time stationary approximation
is no longer needed. The original fixed smooth1-Psi stays an amplitude.

For x>=H/G the extended energy bound is max(Y,Z)Y^aL^51. Its main
is max(H,x)H^-DeltaL^52, and the absolute convolution costs NlogN.
For x<1, zero-free/reflection pays1/(beta+beta'); for1<=x<H/G the
below-one row base is handled separately. Both costs are power-small.
The exponential far tail is paid. The Gamma remainder costs an extra
log; a fixed Q=(K+2)N reference pays K>1 explicitly. Result:
N^(25583/25600)L^55+N^.91L^15 on the selected current-core union,
through all individual heights KN and the entire endpoint transition.
The transpose is disjoint; rebuild before the previous N/2 deletion.
No arbitrary coupled mask, RH, target average, new coverage or practical
onset. Sol theory/actual-file PASS; seven guards normal0.108s/-O0.098s.
The quadrature guard uses ordinary Gamma parameters, not actual zeros;
the theorem rests on its analytic proof. Full signed margin remains OPEN.

The then-next question, answered inba1747b above: can short-interval prime upper
bounds remove a logarithm from the ACTUAL arithmetic energy at a
surviving comparable height T=N^(9/10)? Fix smooth chi in(1,2), and
test int_(1/3)^(2/3)|sum chi(gamma/T)(aN)^(rho-1/2)|^2 da=O_chi(N).
The candidate arithmetic window has width N/T=N^(1/10). A weighted
Schur argument would use sum Lambda(n)|hat_chi(Tlog(n/x))|=O(N/T)
from a source-checked short-interval upper sieve, plus sum Lambda(n)/n
=O(1), instead of discarding prime support and losing logN. Pay prime
powers, complex beta shifts, entire-cutoff tails and all uniformity.
If the energy passes, test its exact beta transfer and actual finite-
period remainder for the comparable T band. Predicted bound O(N),
not all-log or a sufficient signed margin. Fail if the prime-window
bound or transfer costs remain unpaid. Fresh <=30-minute pursuit.

## Previous pursuit: the density shape enlarges unequal-height cancellation

Started22:00:55 UTC, reassessed22:10:26 UTC, progress. Resumed verified
clean main6741752; reviewed mathematics **0172597**. The selected
Huxley/GM/Ingham envelope obeys D(u)<=2u+6/65, with exact positive
slack factorizations and fixed source epsilon retained. Its energy
bound gives ratio decay Delta=[1-a-(1+a)theta]/2, a6/65+epsilon.
The permitted fixed theta interval ends strictly below59/71. Concrete
theta53/64, epsilon1/1170 give a109/1170, Delta1/1280. The individual
height ceiling enlarges to N/2: smaller height=o(N) verifies the actual
finite-period stationary condition. Both H^-1/2 and G^-1 errors are
paid separately, totaling N^.91L^14. The current core uses the separate
eta>N17/20 mask and costs N^(25583/25600)L^54+N^.91L^14. Its union
and transpose contain the former theta4/5,N/10 deletion. Sol theory and
actual-file PASS; seven guards normal0.005s/-O0.006s. No new coverage,
RH, practical onset or signed margin. All previous corrections persist.

The then-next question, answered inb816865 above: can exact finite-period Fourier
convolution carry this same unequal-tag cancellation through the whole
endpoint transition? With B_x=2x^(rho+sigma-1)Gamma(rho)Gamma(sigma)/
Gamma(rho+sigma), the candidate identity is
J_N=e/(2pi) int_0^infinity exp(-x/N)K_pi(N-x)B_x dx,
K_pi(y)=int_0^pi exp(iyt)dt. Test all constants, x near0, bases below1,
the weighted logarithmic integral cost, uniform Gamma error, and the
original smooth weight1-Psi as an amplitude. The proposed extension
would cover individual heights through fixed KN, not just N/2.
Fail it if any endpoint cost or coupled-mask assumption is unpaid.
The later proof pays the transition with one extra logarithm.

## Previous pursuit: a density patch extends actual cancellation past five-sixths

Started21:52:54 UTC, reassessed21:59:54 UTC, progress. Resumed verified
clean main60ba300; reviewed mathematics **6942c66**. The previous goal
turn made progress: the actual prime-offset identity and a positivity
falsifier were proved. The new theorem covers every fixed kappa<13/15,
with no endpoint or uniformity as kappa approaches it. It is actual
complex cancellation, not a density-only surrogate or absolute bound.
Use GM2405.20552v2 Theorem1.2/eq1.4 only for u>=1/10, fixed epsilon
made uniform by a finite sigma grid; near1 retain Huxley log-power and
VK. At kappa17/20, gap1/26, epsilon1/442 and saving1/520 are paid.
The stationary-error envelope splits at h=5/6: it is <=91/100 below,
and <=h<91/100 above. All Gamma errors are absorbed because13/15<9/10.
Rebuild the exact core before old rectangle deletions, remove the full
17/20 square, and subtract its already-paid axis/strip intersections.
The prior theta4/5 union now has individual eta>N17/20 and costs
N^(1983/2000)L^54+N^.91L^14. No coupled mask entered the operator bound.
Sol theory/actual-file PASS; seven guards normal0.013s/-O0.014s. Sources,
polynomial tools and runtime limits persist; the full margin stays OPEN.

The then-next question, answered in0172597 above: can the sharper piecewise density
shape enlarge the selected linear-height tag family from theta<9/11
to theta<59/71? The candidate combines Huxley for u<=1/5, GM's actual
15u/(8-5u) for1/5<=u<=3/10, and Ingham above3/10. Its proposed
envelope is D(u)<=2u+6/65, with a fixed epsilon explicitly charged to
the GM piece. If valid, E_Y(Z)<=Z Y^(6/65+epsilon)L^51 for Z>=Y;
the ratio bound has decay [1-a-(1+a)theta]/2, a=6/65+epsilon.
Test fixed theta=53/64 with epsilon1/1170, predicting a109/1170 and
decay1/1280, including BOTH actual errors at the linear N/10 ceiling
and the current separate eta>N17/20 core mask. Verify every interval
and source-loss convention; no theta endpoint or uncharged epsilon.
The later proof also enlarged the individual ceiling from N/10 to N/2.

## Previous pursuit: the actual prime-offset formula has unavoidable signed weights

Started21:41:24 UTC, reassessed21:50:22 UTC, changed-under-evidence.
Resumed verified clean main530acc2; reviewed mathematics **3421a80**.
The previous goal turn was progress: arithmetic energy and its actual
coupled-band transfer were proved. The latest proof gives the REAL
actual band as a symmetric nearby odd-prime-pair sum with O(sqrtN log^7N)
error. It does not estimate that signed sum by substituting a formal main.
At balanced ratio, period-pi Fourier inversion forces some even-offset
coefficient negative. Explicitly chi supported in(7c/5,8c/5), c1/100,
has Re W_[1/2](100)<0 because its cosine phase stays in(2.8,3.2).
This is a negative COEFFICIENT, not a negative actual total or failed target.

The real endpoint main cancels against its imaginary multiplier, using
the saved corrected tensor projection. The improved O(log^6N) moment
replacement costs sqrtN log^(13/2)N+log^12N in the product. Local prime
windows are linearized only at displacements O(N^(1/8)); global pieces
use Schwartz tails. The Fourier convolution supplies exactly1/pi.
Replacing n/N by n/(n+m) costs O(log^2N), and removing proper powers
costs O(sqrtN log^3N). All infinite offset sums are absolutely convergent.
The offset scale stays fixed for fixed chi; no growing target average.
Sol theory/actual-file PASS; five guards normal0.000s/-O0.000s as reported.
No actual prime/zero calculation. Sources, polynomial tools and all prior
signed bounds persist; full margin OPEN. No outside action or manual wake.

Reassess direction: elementary positivity of this smooth spectral weight
is now falsified. Preserve the transform and norm bounds, but do not
repeat positivity algebra or claim the prime-offset identity supplies
the missing correlation. A different quantitative input is the next test.

The then-next question, answered in6942c66 above: can Guth--Maynard zero density extend
the ACTUAL full signed rectangle from every fixed kappa<5/6 to every
fixed kappa<13/15, concretely17/20? Fresh primary source checked during
reassessment: arXiv2405.20552v2 (7Apr2026), Theorem1.2 and eq(1.4),
printedp2, https://arxiv.org/pdf/2405.20552v2 . It gives
N_z(sigma,T)<=T^[15(1-sigma)/(3+5sigma)+o(1)], and combines with
Ingham to give exponent(30/13)(1-sigma)+o(1). This is NOT a log-power
bound; never replace the saved near-one Huxley input by an unpaid T^epsilon.
Candidate patch: use the new exponent with a fixed small epsilon only
when u=1-sigma>=1/10, and retain the source-checked log-power Huxley
bound D(u)=3u/(2-3u)<=30u/17 near u=0, together with VK zero-free input.
The unequal-energy gaps suggest d=2-(30/13)kappa>0; for kappa17/20,
d=1/26 and epsilon1/442 would leave a far-from-one saving1/520.
Check uniformity in sigma (a finite grid can pay fixed epsilon), both
unequal energies, actual stationary errors and the revised remainder mask.
The old error bound may extend using max(91/100,kappa), but it is not yet
reviewed. Falsifier: an unpaid near-one epsilon loss, approximation error
or nonseparable subtraction. Fresh <=30-minute pursuit; no new height
coverage or Goldbach margin from this source check alone.

## Previous pursuit: energy controls the actual coupled comparable band

Started21:32:16 UTC, reassessed21:39:50 UTC, progress. Resumed verified
clean main0073b6b; reviewed mathematics **55401fd**. The preceding
bounded pursuit in this same live turn proved the arithmetic energy;
the preceding goal turn proved the arithmetic moment. No stopped interval
is claimed as research execution. The new complex bound is O_chi(NlogN)
for the ACTUAL fixed smooth band, preserving beta, copies and the diagonal.

The exact quotient 2N^(rho+sigma-1)Gamma(rho)Gamma(sigma)/Gamma(rho+sigma)
is paired by the beta integral with S_N(aN)S_N((1-a)N). Fresh source:
NIST DLMF5.12.1, positive complex real parts. Three nonstationary
endpoint integrations, zero-free/reflection and the first moment pay
O(N^-1log^13N). The energy extends to the FIXED interval[1/4,3/4],
with prime support[N/8,2N] and sampling slopes[2/3,8]; Cauchy pays
the central integral. Full-line inversion is justified by a Gaussian
approximate identity and improper-tail convergence, even when beta+beta'<=1.
The negative half-line is exponentially paid. The upper tail has leading
coefficient +i(-1)^N/[N(1-(gamma+eta)/(piN))], SUBTRACTED from the
quotient to get J. Fixed endpoint projection pays O(N); the new density
first moment pays its second-order remainder by log^12N. Retaining b/t
in the modulus derivative is needed for uniformity as b decreases to0.
No finite-period kernel was silently replaced by its infinite quotient.

Sol theory/actual-file PASS; five guards normal0.001s/-O0.001s. No actual
prime/zero calculation or all-log deletion. The sufficient lower margin
remains OPEN. Polynomial tools, source corrections and runtime limits
persist. No outside action, manual wake, novelty or post-stop process claim.

The then-next question, tested in3421a80 above: does nonnegative chi provide a useful
sign after this coupled band is transferred back to prime pairs? Derive
the actual real-band expression with o(N) error in additive offsets
k=n+m-N. A candidate leading coefficient, at a=n/N in the central
range, is W_a(k)=(1/pi)int chi(a*v)chi((1-a)*v)exp(-ikv)dv.
Check its factor, endpoint corrections, varying a, Fourier-cutoff tails
and prime powers before promoting that formula. The uniform O(log^6N)
moment error and the proved energy may pay its product replacement by
O(sqrtN log^7N). For the real part, the saved endpoint parity projection
may cancel the leading imaginary tail; this extension also needs proof.
Concrete discriminator: can Re W_a(k) be nonnegative on every EVEN
offset, or does Poisson summation force negative coefficients because
the v support misses all multiples of pi? A negative coefficient alone
is not an actual negative prime sum or an all-method barrier. This tests
one positivity mechanism and identifies which signed arithmetic remains.
Fresh <=30-minute pursuit, not yet performed. Overall goal stays active.

## Previous pursuit: arithmetic energy with the approximation error paid

Started21:24:53 UTC, reassessed21:31:02 UTC, progress. Resumed verified
clean maina4ff5ac; reviewed mathematics **15b36b9**. The previous goal
turn was progress: actual arithmetic excluded the mock lattice alignment.
The frequency energy at fixed N is O_chi(NlogN), saving one log from the
pointwise bound. In x measure it is O_chi(N^2logN), not O(NlogN).
The exact same finite prime window P_N approximates S_N with O(log^6N)
uniform error. A localized first Taylor term costs N^-1 W_N, where
the retained Ingham identity D(u)-u<=1/2 pays W_N<<Nlog^6N. Global
second-order and cutoff tails cost N^-1/2 logN, including negative
heights. Vanishing chi(0),chi'(0) pays the pole tests by N^-3/2.
The prior Gamma O(1) remains. The prime kernel's two Schur bounds are
O(1) and O(1/N); Chebyshev pays sum Lambda(n)^2/n<<logN. Squaring
the IMPROVED error costs log^12N and is small enough. All beta and
multiplicities remain; no pair correlation or target average was used.
Sol theory/actual-file PASS; six guards normal0.004s/-O0.004s. No new
source theorem, actual prime/zero computation, outside action or manual
wake. Earlier corrections and polynomial tools persist. Full margin OPEN.

The then-next question, answered in55401fd above: can the beta-integral representation
of 2N^(rho+sigma-1)Gamma(rho)Gamma(sigma)/Gamma(rho+sigma) transfer
this energy to an O_chi(NlogN) bound for the ACTUAL finite-period
smooth comparable linear-height band? The proposed integral is
2 int_0^1 S_N(aN)S_N((1-a)N)/sqrt(a(1-a)) da, with the beta factors
retained exactly. Source-check the identity and justify every exchange.
Localize a to a fixed central interval using nonstationary integration,
paying real parts near0 via the retained zero-free/reflection input;
extend the energy to that fixed interval with its constants. The finite
period is NOT the infinite Gamma quotient: pay the negative half-line
and upper tail. A fixed endpoint projection from793b135 might pay
the leading tail, with the new first moment paying its remainder.
Falsifier: a main-sized unpaid tail or invalid moment-to-kernel transfer.
This would improve a comparable-band bound, not an all-log deletion or
the Goldbach lower margin. Fresh <=30-minute test; not yet performed.

## Previous pursuit: actual arithmetic excludes the model's linear alignment

Started21:09:52 UTC, reassessed21:22:23 UTC, progress. Resumed verified
clean main55f2bbf; reviewed mathematics **3bee966**. Previous goal turn
was progress: the count-compatible model reinforced the actual kernel.
For fixed real chi in C_c^infinity((1/100,1/50)), the ACTUAL moment
 S_N(x)=sum_(gamma>0) chi(gamma/N)*x^(rho-1/2)
satisfies |S_N(x)|<<_chi sqrtN logN uniformly for real N/3<=x<=2N/3.
No RH, target average or PNT asymptotic. All real parts and multiplicities
remain; an unweighted height moment is not substituted. At x=N/2 the
mock quarter-grid has i*(NlogN/(2pi))*int chi+O(N), for nonnegative
nonzero chi. Thus actual arithmetic forbids this particular alignment.
The count-only countermodel and prior signed deletions remain valid.

The angular Fourier formula uses H((rho-1/2)/i), not H(gamma).
Primary authorities checked: Garrett, Guinand's explicit formula,
2021-02-12 Theorem0.1 printedp1, and Carneiro-Chandee-Milinovich
arXiv1309.1526v1 Lemma5 printedpp6-7, including its unconditional
proof remark. The complex test is split into ANALYTIC functions real
on the real axis; no nonanalytic real-part operation is made off-axis.
Entire chi_V uses V=N^(1/8). Its Schwartz cutoff tail and complex
displacement cost sqrtN L+N^(3/2)L V^-16 after summing ALL zeros,
including negative heights. The angular prime transform is exactly
N*hatChi(Nlog(n/x))*nu(Nlog(n/x)/V); uniform integer sampling pays
O(sqrtN L), with no V-length loss or integral-center assumption.
Poles cost sqrtN. The Gamma integral costs O(1) after real-axis cutoff
replacement and one integration; NIST DLMF5.15.1 pays its derivative.

Sol theory/actual-file PASS; seven exact guards normal0.007s/-O0.007s.
No actual zero/prime computation. Source correction: CCM is v1 Lemma5
and its proof remark, not recalled Lemma8 or unavailable v2. The SBM
mirror denied access via Anubis and was not retried/used. No interpolation
theorem from2005.02996v3 is invoked. Existing2016 formula corrections,
density sources, polynomial components and runtime limits all persist.
The remaining coupled signed margin is OPEN; no new C_remaining deletion,
coverage, onset, novelty, outside action, manual wake or post-stop process.

The then-next question, answered in15b36b9 above: does the arithmetic family give
the mean-square bound int_(1/3)^(2/3)|S_N(aN)|^2 da <<_chi NlogN?
Mechanism: improve the off-critical replacement using the already proved
Ingham first-moment inequality D(u)-u<=1/2, rather than sqrtN times
the total count. A smooth real-axis localization of the displacement
should cost only a fixed power of logN; pay the distant zero tails
separately. The pole tests are near0, where chi and every derivative
vanish, so their previous sqrtN bound might also be sharpened. Then
Schwartz sampling and sum_(n~N)Lambda(n)^2<<NlogN may give the stated
energy without a two-prime estimate. Test every localization/error
before claiming it. Falsifier: an unpaid error of order sqrtN logN or
a coupled prime-correlation term required for this UPPER bound. This
would be an arithmetic energy tool; no automatic bilinear saving or
all-target coverage. Fresh <=30-minute pursuit, not yet performed.

## Previous pursuit: count-compatible reinforcement survives the actual kernel

Started20:55:30 UTC, reassessed21:07:44 UTC, progress. Resumed verified
clean main89e7edd; reviewed mathematics **6fb7829**. The previous goal
turn was progress: selected strongly unequal linear-height boxes were paid.
For fixed nonzero real chi in C_c^infinity((1/100,1/50)), a global
N-dependent mock critical-line spectrum has weighted actual J sum
 -(Nlog^2(N/2)/pi)int chi^2+O_chi(Nlog^(3/2)N+sqrtN log^2N).
It matches the smooth RVM main M(t) with O(1) count error uniformly in
N, has O(log(2t)) local occupancy and all the used single-zero density
envelopes. This refutes only a UNIFORM weighted-band estimate from those
constraints. It is not actual zeta or a fixed model resonating infinitely
often, and a negative weighted band does not decide the unweighted sum.

The lattice spacing2pi/log(N/2) with quarter-cell offset makes the
separable pair carrier negative. The entropy phase has a stationary
diagonal; transverse Fresnel phase cancels-pi/4. Poisson zero frequency
is ASYMPTOTIC to4piN int chi^2; other modes are nonstationary. Starting
from inverseM(j) heights and rounding upward inside[cN/2,3cN], c1/100,
moves at most one point across any threshold, because M'(t)*spacing<1.
Only O(N) lattice nodes are omitted, so the proved matrix bound pays
the stationary thinning cost Nlog^(3/2)N. Conjugation/reflection here
mean symmetry of LOCATIONS, not the zeta functional equation or Euler product.

A reusable sharper ACTUAL expansion is also proved for beta=beta'=1/2
in this fixed linear band:
 J=A exp(iTheta)+N^-1 b(q)exp(i[phi(gamma)+phi(eta)+Npi])+O(N^-3/2),
 q=(gamma+eta)/N, b(q)=-2e exp(-q/pi)/(pi-q), phi(t)=tlog(t/pi)-t.
The lower t<=N^-1/4 integral is exponentially small; a flat cutoff
licenses uniform amplitude derivatives. A next-order Morse calculation
pays the central error, and two noncentral integrations keep the upper
endpoint. On the full lattice its potentially close alias has derivative
log(2gamma/(piN)) bounded away from0. Endpoint thinning costs NL;
the remaining pairwise error sums to sqrtN L^2. The earlier coarse
N^-1 remainder would NOT have proved this model. The model's near strip
is absolutely all-log and can be removed, without transferring it to zeta.

Fresh primary RVM authority: Brent-Platt-Trudgian, MathComp2021,
printedp2926 eqs(5)-(7), author offprint
https://maths-people.anu.edu.au/brent/pd/rpb276-MC-preprint.pdf .
Its half-weight endpoint convention differs by O(1) on the simple model;
no numerical first-zero or database claim was used. Sol theory/actual-file
PASS; seven exact guards normal0.002s/-O0.002s. All earlier corrections,
phase and polynomial components persist. Actual full signed margin OPEN;
overall goal active. No outside action, manual wake or post-stop process claim.

The then-next question, now answered in3bee966 above: for the ACTUAL zeros, can the prime
explicit formula prove
 |sum chi(gamma/N)*(N/2)^(rho-1/2)| <<_chi sqrtN log^2N
for fixed nonnegative smooth chi supported in this band, without RH or
target averaging? The mock quarter-grid has an imaginary moment of
order NlogN, so that estimate would exclude its specific alignment.
Possible route: a smoothed Guinand/Weil formula with an entire Fourier-
truncated approximation to chi, preserving the off-critical argument
gamma/N-i(beta-1/2)/N. Pay the replacement, pole and Gamma terms;
the prime side should be a rapidly weighted O(1)-scale window around
N/2. The exact formula and its non-RH test-function hypotheses require
a FRESH PRIMARY SOURCE CHECK before use. A recalled formula is only a
locator. Proving this single moment would still not prove the bilinear
correlation estimate; test that distinction explicitly. Fresh <=30 minutes.

## Previous pursuit: ratio savings reach selected linear-height rectangles

Started20:46:03 UTC, reassessed20:52:56 UTC, progress. Resumed verified
clean main2f4c161; reviewed mathematics **da07ce0**. The previous goal
turn was progress: the full fixed sub-five-sixths rectangle was paid.
The new result controls complete dyadic rectangles with individual masks
V_N<gamma,eta<=N/10, tags G<=H and G<=H^theta, fixed1/2<theta<9/11.
It is a signed estimate, not an absolute estimate or a curved-mask theorem.

The actual piecewise Ingham/Huxley exponent obeys D_*(u)<=2u+1/10;
both rational slacks are explicitly nonnegative. Thus for Z>=Y,
E_Y(Z)<<Z Y^(1/10)L^51, including the total-count baseline. The prior
uniform discrete bound yields N G^(11/20)H^(-9/20)L^52, so the ratio
pays energy growth. Set delta_theta=(9-11theta)/20>0. The full dyadic
family costs N^[1-(9/20)delta_theta]L^54 plus N^(91/100)L^14.
Actual finite-period stationarity holds through N/10. The errors
H^-1/2 and G^-1 are kept SEPARATE at linear height; the old Ingham
amplitude exponent E gives E-h/2 and E-g. Affine endpoint checks at
h=g and h=1 pay both by91/100. No free Gamma-error absorption.

For theta=4/5, selected boxes eventually have2G<H/2, hence gamma<eta
and gap>H/2>>W_N. In the current core max>N^(4/5) therefore becomes
the individual column mask eta>N^(4/5). It forces H>N^(4/5)/2 and
improves the main to N^(124/125)L^54. The original weight1-Psi=1
because both heights<=N/10. Delete exactly this union and its disjoint
transpose; every other prior restriction, copy and all-log R error stays.
The full signed lower margin remains OPEN. Sol theory/actual-file PASS;
seven guards normal0.013s/-O0.017s. No actual prime/zero computation,
RH, coverage/onset/novelty, outside action or manual wake. Sources,
polynomial tools and runtime limitations persist; overall goal active.
No process is claimed to continue after a stopped checkpoint.

Next concrete question, UNREVIEWED: can comparable linear heights
reinforce even in an artificial critical-line spectrum satisfying the
Riemann-von Mangoldt counting main with O(logT) error, the retained
single-zero density bounds and reflection symmetry? A candidate uses
spacing a=2pi/log(N/2) and a quarter-cell offset in a fixed band
gamma~cN<N/10. Its separable carrier is negative on each pair; the
residual entropy phase is stationary on the diagonal. Fixed smooth
separate masks might yield a stationary signed main of order-Nlog^2N.
Thin the slightly denser lattice to the smooth RVM count: only O(N)
points appear to be lost, whose stationary contribution should cost
O(Nlog^(3/2)N) by the proved discrete norm. This is a CANDIDATE, not
a zeta-zero claim or a Goldbach counterexample.

Concrete test: prove or refute the model while paying the ACTUAL finite-
period endpoint and stationary errors. Current coarse relative error
N^-1/2 is not enough on the full comparable linear band; isolate the
nonstationary endpoint and obtain a sharper central remainder before
any actual-kernel claim. Keep model assumptions and source identities
distinct. Such a result would test the sufficiency of these counting
inputs only, not discard the phase method or polynomial components.
Fresh <=30 minutes; no model result or all-method impossibility yet.

## Previous pursuit: the whole fixed sub-five-sixths rectangle is signed small

Started20:35:13 UTC, reassessed20:43:53 UTC, progress. Resumed verified
clean mainf0af320; reviewed mathematics **2f03381**. The previous
pursuit proved actual signed cancellation in the two-thirds band.
The extension now controls the COMPLEX sum over BOTH heights<=N^kappa
for every FIXED kappa<5/6, with O_(A,kappa)(N/log^A N) error. Choose
kappa=4/5 in the actual pointwise reduction. C_high retains max>N^(4/5),
both>V_N, difference>W_N, original smooth height-sum cap, and every copy.
The full signed lower margin remains OPEN; the inherited all-log R error
is unchanged. This is not an absolute deletion or a5/6 endpoint theorem.

With gamma=Gx,eta=Hy,r=G/H, remove both separable carriers. The phase
G phi_r has phi_xy=-1/(y+rx), uniform at r=0. TT* and physical rescaling
give sqrtH; both Fourier tails and copy occupancy are paid. Extracting
the stationary H^-1/2 leaves L sqrt(E_G(NG/H)E_H(N)). The row and
column density gaps are2-2h-(2/5)g and2-(12/5)h, each at least
2-(12/5)kappa>0. Their relative baselines both equal H/N. Summing the
leading boxes costs N^kappa L^4+N L^54 exp[-c_kappa L^(1/3)/(logL)^(1/3)].

The actual normalized integral is uniform because piN>=4(gamma+eta).
After the already paid low axes, G>=V_N/2>=N^(9/20)>=sqrtH, so the
Gamma and stationary relative errors are O(H^-1/2). Direct Ingham
amplitude layer cake, not a reversed kernel bound, gives exponent
E-h/2<=1-h/5-(1-6h/5)(u+v)<=91/100. The exact density slack is
(1-2u)(2-3u)/(5(1+u)). O(L^2) boxes pay the complex error stated above.
Separate rectangle masks are used throughout; already absolute-small
axes/near strips are subtracted afterward. Sol theory/actual-file PASS.
Six guards normal0.019s/-O0.012s. Initial guards caught a new-wrapper
API mismatch (the old exponent helper takes u,v, not beta,beta'); fixed
before PASS, without altering the mathematics or old files. All source
corrections, polynomial components and runtime limits persist. Overall
goal active; no process claimed beyond a stopped checkpoint.

Next concrete question, UNREVIEWED: can the height-ratio factor pay
unequal boxes up to a FIXED LINEAR ceiling, say gamma,eta<=N/10, even
when the two energies are not individually all-log? The piecewise actual
Ingham/Huxley exponent D_*(u) appears to obey D_*(u)<=2u+1/10. For
Z>=Y this would give E_Y(Z)<<Z Y^(1/10)L^51, hence the signed leading
box cost N G^(11/20)H^(-9/20)L^52. Test dyadic tag pairs
G<=H^(9/11-epsilon), fixed epsilon>0, with every actual stationary/
Gamma error paid. Specify a UNION OF COMPLETE DYADIC RECTANGLES;
do not silently feed a curved coupled mask to the matrix theorem.
The N/10 ceiling keeps the finite stationary expansion away from the
endpoint transition. Verify the piecewise density inequality, baselines,
all errors and summation, or record the specific failed budget. Fresh
<=30 minutes; no linear-height deletion or endpoint result yet promoted.

## Previous pursuit: actual discrete signed cancellation in one interior band

Started20:17:49 UTC, reassessed20:35 UTC, progress. Resumed verified
clean maincda45e8; reviewed mathematics **feb00a9**. The previous goal
turn was progress: an actual absolute obstruction and controlled phase.
The complex sum of J over both heights in(T,2T],T=N^(2/3), is now
O_A(N/log^A N). Removing the previously paid near-height strip preserves
this estimate. This is an actual estimate where absolute mass is large;
the remaining C_high and the sufficient Goldbach lower margin are OPEN.

After removing the separable logN carrier, continuous TT* gives sqrtT.
A fixed Fourier projection with both tails paid transfers to arbitrary
zero spacings and coincident copies; local copy occupancy costs logT.
The beta-dependent amplitude has a summable smooth Fourier expansion,
so the resulting cost is logT E_N, E_N=sum N^(2beta-1). It licenses
separate row/column masks, not arbitrary coupled masks. Yashiro1310.0765v2
printedp2 eqs(1.1),(1.2) gives Ingham log^5 and Huxley log^44 bounds;
together they imply the weaker uniform exponent(12/5)(1-sigma) with
log^50 loss. Mossinghoff-Trudgian-Yang2212.06867v1 printedp2 Theorem1.1
supplies beta<=1-delta with delta>>L^-2/3(logL)^-1/3. Consequently
logT E_N << N^(2/3)L^2+N L^52 exp[-c L^(1/3)/(logL)^(1/3)].
The prior complex stationary error N^(31/45)L^12 is paid separately.
Do not replace these log-power density statements with fixed-epsilon
estimates, or infer other height boxes. Sol theory/actual-file PASS;
six exact guards normal0.016s/-O0.016s. No zero/prime computation,
RH, coverage, onset or novelty claim. All older source corrections,
polynomial tools and runtime limitations persist. Overall goal active.

Next concrete question, UNREVIEWED: does the same mechanism uniformly
pay unequal height boxes G<=H<=N^(5/6-epsilon), with G above the already
deleted low axis? Scale gamma=Gx,eta=Hy,r=G/H and remove gamma log r.
The residual phase has parameter G and mixed derivative-1/(y+r*x),
uniform down to r=0. A candidate physical operator bound sqrtH would
cancel the H^-1/2 stationary amplitude, leaving the two energies
E_G(NG/H) and E_H(N). Test the uniform projection tails, beta amplitude,
energy gaps, actual complex stationary remainder and dyadic summation.
Falsifier: an unpaid ratio-dependent cost or error of order N. Fresh
<=30-minute pursuit; no such extension or full correlation bound yet.
No research process is claimed to run after a stopped checkpoint.

## Previous pursuit: actual interior mass and its controlled phase

Started20:06:48 UTC, reassessed20:16:00 UTC, progress. Resumed verified
clean mainb780bbc; reviewed mathematics **fb3da0f**. Previous goal turn
was progress: absolute reductions isolated a precise surviving-band test.
For h=gamma+eta,b=beta+beta',U=piN>=4h, the normalized integral is
sqrt(2pi)e^-1 h^(1/2-b)exp(i[h-hlogh-b*pi/2+pi/4])+O(h^-b),
uniformly0<b<2 and in every such finite endpoint. Compact Morse/Fresnel
analysis pays the central region; first-derivative bounds pay its complement.
Restoring all Gamma and N phases gives J=A exp(iTheta)[1+O(T^-1/2)],
A=2sqrt(2pi)h^-1/2(Ngamma/h)^(beta-1/2)(Neta/h)^(beta'-1/2),
Theta=gamma log(Ngamma/h)+eta log(Neta/h)-pi/4.

For each fixed ordinate pair, beta reflection pairs reciprocal positive
weights with multiplicity. Riemann-von Mangoldt then gives actual absolute
mass >>T^(3/2)log^2T=Nlog^2N. This band lies inside1-Psi=1 and above
the previous axes/both-low cuts. Deleting the all-log near strip preserves
the lower bound. No signed size or sign follows. Separately the rational
density bound D(u)<=3u/2+4/15 bounds total leading amplitude by
N^(46/45)log^12N, so its relative error totals N^(31/45)log^12N=o(N).
Thus the cosine replacement is an actual paid reduction, with its cosine
sum still OPEN. Sol theory/actual-file PASS; five guards normal0.004s/
-O0.004s. All sources and polynomial tools persist; overall goal active.

Next concrete hypothesis, UNREVIEWED: can the explicit phase support a
DISCRETE bilinear L2 bound of size sqrtT*logT times the coefficient norms,
using only multiplicity-counted O(logT) zeros per unit interval? Remove
the separable carrier(gamma+eta)logN. The remaining entropy phase has
mixed derivative-1/(gamma+eta), while its full Hessian has rank1.
Candidate mechanism: a continuous compact-kernel TT* bound O(sqrtT),
then fixed-frequency smooth projections to transfer to the discrete zero
measure. Projection-kernel Schur bounds would cost logT; tails must be
proved negligible. Fourier expansion in the two beta parameters would
handle the smooth amplitude without pretending beta is smooth in height.

If that transfer works, its remaining energy is sum N^(2beta-1) over
the band. Current Ingham alone gives exponent1-2u^2/(1+u) at T=N^(2/3)
and does not establish the required all-log bound nearu=0. A fresh primary
source check is required for a stronger near-one density estimate and
Vinogradov-Korobov zero-free input. A possible Huxley exponent recalled
as3(1-sigma)/(3sigma-1), with logarithmic losses, is UNVERIFIED here;
do not use it before checking its range, constants and exact statement.
No discrete cancellation or energy estimate has yet been promoted.
Fresh <=30 minutes; the full Goldbach margin would still remain open.

## Previous pursuit: both-low heights and the density-envelope limit

Started19:59:18 UTC, reassessed20:05:23 UTC, progress. Resumed verified
clean main1e8c05b; reviewed mathematics **0fed151**. Previous pursuit
was progress: the paid density-box exponent supplied this extension.
The exponent increases with the smaller height scale g, so setting g=h
bounds all boxes while retaining the smaller band's zero-free cap.
The rational density majorant D(u)<=20u/13+49/200 gives
E<=1-(1-20h/13)(u+v)-h/100 for h<=13/20. A zero-free small-height
split then proves the actual all-log deletion of the whole both-low box.

The exact uncapped envelope M(h) is1-h/2 up to1/3,
3+(11/2)h-4sqrt(3h) through3/4, and3h/2 thereafter. Its relevant
crossing of1 is kappa_*=(52+16sqrt3)/121. A tangent majorant proves
all-log deletion for every FIXED kappa<kappa_*, with constants not uniform
at the boundary. At kappa_* only this upper bound loses saving; actual
zeros have not been shown to saturate it. The finite C_high now has
max(gamma,eta)>N^(13/20), in addition to all prior core restrictions.
Sol theory/actual-file PASS; five guards normal0.005s/-O0.005s. No RH,
zero/prime computation, coverage/onset/novelty or square-root R error.
All corrected sources and polynomial tools persist; overall goal active.

The following proposed actual-band test is completed above. Its original
hypothesis was: on actual zeros in (T,2T],
T=N^(2/3), the surviving INTERIOR pair kernels have absolute mass
>>T^(3/2)log^2T= Nlog^2N. Test a uniform stationary-phase lower bound
for the finite-period integral, then use beta->1-beta reflection and
Riemann-von Mangoldt. A candidate normalized main is
sqrt(2pi)e^-1 h^(1/2-b) exp(i[h-hlogh-b*pi/2+pi/4]), with relative
O(h^-1/2), for h=gamma+eta, b=beta+beta', U=piN>=4h.
All partial-endpoint errors, real parts and multiplicities must be paid.
If valid, check that removing the already paid near-height strip leaves
the lower bound inside the ACTUAL retained core. This would prove a need
for signed cancellation there, not its absence or a Goldbach obstruction.
Fresh <=30 minutes; no actual lower-bound claim has yet been promoted.

## Previous pursuit: the low-height axes reach an almost-square-root cutoff

Started19:49:53 UTC, reassessed19:58:16 UTC, progress. Resumed verified
clean mainef67439; reviewed mathematics **b2554fd**. Previous turn was
progress: the near-height theorem left a precise unequal-height test.
The correct box kernel is N^(b+d-1)G^(b-1/2)H^(-b), G<=H. An initial
scratch idea wrongly supplied H^(-b-1/2); this was caught before promotion.
Two genuine single-zero density estimates preserve the real-part weights.
With g=logG/logX, h=logH/logX, the resulting exponent is affine in h.
Its endpoints are <=1-(1-2g)(u+v)-g/4 at h=g, and <=1/2+g at h=1.
The zero-free restriction on the smaller band pays bounded/small G.
All compact bands, beta<1/2 baselines and product multiplicities are paid.

The uniform result is log^14N[N exp(-c1 sqrtlogN)+sqrtN V] for axes
min(gamma,eta)<=V,1<=V<=sqrtN. The canonical cutoff
V_N=sqrtN exp[-(loglogN)^2] therefore has all-log error. The finite
remaining C_core retains gamma,eta>V_N, |gamma-eta|>W_N, the previous
height-sum cap and original smooth weight. Its signed margin is OPEN.
Sol theory/actual-file PASS; five guards normal0.051s/-O0.046s. No RH,
prime/zero computation, coverage, numerical onset or square-root R error.
All sources and polynomial tools persist; overall goal active.

The proposed same-box density test is completed and extended above. Its
original question was to use the same paid box density
estimate to delete pairs with BOTH heights<=N^(13/20). Check the diagonal
height endpoint for arbitrary real parts and identify the density method's
actual cutoff limit, rather than treating this one exponent as universal.
The larger-height region and signed lower margin would remain open.
Fresh <=30-minute hypothesis; no new zero-pair correlation assumption.

## Previous pursuit: a growing near-height spectral strip is paid

Started19:42:53 UTC, reassessed19:48:19 UTC, progress. Resumed verified
clean main95d3e9d; reviewed mathematics **9f47ce4**. The previous
pursuit's diagonal proof supplied a uniform unequal-zero extension:
|J_N(rho,sigma)|<<N^(beta+beta'-1)/sqrt(1+min(gamma,eta)).
This retains the loss when one height is much smaller than the other.
Local multiplicity-counted Riemann-von Mangoldt and AM-GM give
S_near(N,W)<<(W+1)^(3/2)logN F_K(N), where F_K is the single-zero
weighted moment sum N^(2beta-1)/sqrt(1+gamma). The earlier density
calculation bounds F_K DIRECTLY; do not reverse diagonal<=F_K.

It gives F_K<<Nlog^8N exp[-(alpha/10)sqrt(logN)]. Taking
W=exp[(alpha/30)sqrt(logN)] leaves Nlog^9N exp[-(alpha/20)sqrt(logN)],
hence all-log saving. Every fixed log^B N is eventually included; a
width N^epsilon is not licensed by this budget. All equal-height locations
are now paid, including different real parts and every product multiplicity.
The finite retained C_sep has gamma+eta<=(pi+2delta)N, |gamma-eta|>W,
and the original1-Psi weight. The R error remains O_A(N/log^A N), with
the inherited opposite-sign cost; its signed lower margin is OPEN.
Sol theory/actual-file PASS; five exact guards normal0.002s/-O0.002s.
No actual zero/prime computation, RH, coverage, numerical onset or novelty.
Polynomial tools and all source corrections persist. Overall goal active.

The proposed low-height axes test is completed and strengthened above.

## Previous pursuit: the identical-location spectral diagonal is paid

Started19:29:02 UTC, reassessed19:41:46 UTC, progress. Resumed clean
mainccf6291; reviewed mathematics **6abc250**. The previous turn was
progress: uniform nonstationary reduction isolated a finite retained sum.
For every fixed K,A>0, sum_(distinct rho; gamma<=KN)
m(rho)^2 |J_N(rho,rho)| <<_(A,K) N/log^A N. The kernel bound is
N^(2beta-1)/sqrt(1+gamma), uniform through the endpoint transition.
The rescaled partial integral is O(h^(1/2-b)) for every endpoint U;
small heights are absorbed as a finite analytic set, not a zero certificate.

Riemann-von Mangoldt gives m(rho)<<log(gamma+3). A classical zero-free
split H0=exp(alpha sqrt(logN)), alpha=min(1,sqrt c), pays low heights.
Above it the uniform Ingham density exponent3(1-sigma)/(2-sigma), with
log^5T, gives an exponentially small function of sqrt(logN), hence every
fixed logarithmic saving. arXiv2507.15184v2 Corollary1/Table1 explicitly
support this weaker density input; do not mix its refinement with v1.
The m^2 count costs an extra log. Distinct beta at the same gamma remain
distinct locations. The full R formula still has its inherited all-log
error and OPEN signed lower margin. Sol theory/actual-file PASS; six
guards normal0.007s/-O0.008s. All sources and polynomial tools persist.
No new prime/zero computation, coverage, onset, novelty or outside action.

The proposed growing near-height strip test is completed above.

## Previous pursuit: the full smooth nonstationary spectral tail is paid

Started19:16:56 UTC, reassessed19:27:08 UTC, progress. Resumed clean
mainf2db6b6; reviewed mathematics **4c69475**. Previous turn was progress:
the actual fixed-box signed cancellation supplied this extension mechanism.
Positive-zero projection now allows support[-S,S], with error
O(S Q12(w)sqrtNlogN). The powers-of-two correction is O(logN) at the
axis; negative-height endpoint terms are absolutely bounded. With
B=16pi logN, sixteen Fourier integrations per variable cost B^32;
every support and seminorm cost is displayed. The leading error is
O(sqrtNlog^34N+log^36N), safely inside sqrtNlog^40N.
Three integrations by parts above a FIXED separation pi+delta have
normalized error O(B^3N^-3). The sharp absolute tail at T=16piNlogN,
N^-11/2 log^(5/2)N, is retained until multiplication by the full absolute
majorant N^(5/2)logN. Thus arbitrary bounded coupled tail weights are paid.

The result removes the full smooth tail Psi((gamma+eta)/N). What remains
is FINITE, with positive gamma+eta<=(pi+2delta)N. The combined pointwise
error is only O_A(N/log^A N), because the earlier opposite-sign error is
N sqrt(logN)exp(-c sqrt(logN)). An initial author draft incorrectly used
the new square-root bound for the combined formula; corrected before
promotion, with a guard and independent actual-file confirmation.
Sol theory/actual PASS; seven guards normal0.002s/-O0.004s. No zero/prime
computation, coverage/onset/novelty claim, outside action or manual wake.
All polynomial tools and source corrections persist. Overall goal active;
no process claimed after this checkpoint.

The proposed identical-zero test is completed in the latest pursuit above.

## Previous pursuit: prime parity pays an actual signed smooth endpoint region

Started19:03:10 UTC, reassessed19:14:13 UTC, progress. Resumed verified
clean maind104b80; reviewed mathematics **793b135**. The previous goal
turn was progress, changing the next action through the endpoint obstruction.
At z_*=1/N+i*pi, f_rho=Gamma(rho)z_*^-rho has total absolute mass
O(N^(3/2)logN). A radial Fourier projection proves
sum f_rho w(gamma/N)=sum Lambda(n)e^(-n/N)w(pi*n/N)+O_w(sqrtNlogN)
for fixed smooth w supported away from0. Corrected explicit formula,
Chebyshev moments and the exact powers-of-two parity correction suffice.
No PNT asymptotic is needed. The source's arbitrary-a contour identity is
read ONLY with the2016 missing-constant correction.

A tensor expansion then gives a REAL arithmetic main for real smooth
two-variable g, with error O_g(N^(3/2)logN+Nlog^2N). Direct two-zero
absolute replacement loses the saving and is not the proof. Retaining two
endpoint terms and integrating three times gives the leading -i/(N*d),
d=1-(gamma+eta)/(piN). Its real main cancels upon taking Re. The second
beta-linear term is paid with one crude factor and one projected factor;
the total remainder is O_G(log^2N). Therefore fixed real smooth G in
(8pi,9pi)^2 has signed contribution O_G(sqrtNlogN+log^2N). Positive
smooth weights can still have >>Nlog^2N termwise absolute mass.

Sol theory/actual-file PASS; six exact guards normal0.001s/-O0.001s.
No actual zeros/new prime ranges, effective onset, coverage or worldwide
novelty claim. The full same-sign lower margin stays OPEN. All polynomial
components and source/runtime corrections persist; no process claimed after
checkpoint. Overall goal active, no outside action or manual wake queue.

The then-next question (completed with uniform costs in4c69475): can this mechanism control all smooth
positive-height pairs with gamma+eta>(pi+delta)N, fixed delta>0, through
the licensed T=C NlogN? Pay the axes (one height near0), the growing
support O(logN), every smooth seminorm, and the height tail. Seek only
polynomial log costs so the signed bound remains o(N). Do not silently
reuse a fixed-G constant for N-dependent weights or shrink delta with N.
The stationary region and the full Goldbach margin remain open even if
this test succeeds. Fresh <=30-minute hypothesis.

## Previous pursuit: endpoint defeats absolute deletion; interior saving survives

Started18:50:54 UTC, reassessed19:01:15 UTC, changed-under-evidence.
Resumed clean main3c1e7da; reviewed mathematics **c901fc3**. The previous
goal turn was progress: cca6455 paid the damped zero interactions.
For b=beta+beta', h=gamma+eta, the actual phase is
Nt-h log|a+it|-b arg(a+it); its stationary equation in u=Nt is
u^2-hu+1-b=0. In the tested band (8piN,9piN] for both heights, any tiny
stationary point is in the exponentially suppressed [0,1/N] interval.
Two integrations by parts on [1/N,pi] leave a nonzero endpoint term.
Uniform Stirling, zero symmetry and Riemann-von Mangoldt then prove
sum|J_(rho,sigma)|>>Nlog^2N for ACTUAL zeros with multiplicities, no RH.
This is not a bound for Re sumJ and does not exclude inter-pair cancellation.

For any FIXED smooth chi vanishing nearpi, four integrations pay all
zero pairs and give sum|J^chi|<<_chi N^-1log^2N on the same band. This
localizes its contribution to any fixed endpoint neighborhood; it does not
remove that neighborhood or permit shrinking it with N. Six guards passed
normal0.002s/-O0.003s; Sol theory/actual-file and narrow corollary-delta PASS.
Finite toy quadrature agrees with the endpoint expansion, explicitly not
a numerical zero computation, certified error bound or asymptotic proof.
No new coverage/onset/novelty claim. All corrected sources and polynomial
components persist. Overall goal active; no process claimed after checkpoint.

The then-next question (now completed for fixed smooth G in793b135): can a SMOOTH height projection be
summed at the endpoint before estimating, using the exact prime-parity
identity S(a+i*pi)=2log2*sum_(j>=1)exp(-2^j*a)-S(a)? Derive the actual
projection kernel and error first; test whether the one-prime PNT input
controls the projected real contribution. It does not follow merely from
control of the unprojected endpoint. Preserve Gamma phases, finite period
and fixed N; no hidden prime-pair or zero-correlation assumption. Retire
if the projection only restates the open signed estimate. Fresh <=30 minutes.

## Previous pursuit: damped zero interactions are all-log small

Started18:39:29 UTC, reassessed18:49:04 UTC, progress; resumed verified
clean mainc2934bb. Reviewed mathematics **cca6455**. The classical
zero-free region and Gamma damping give
||Z_minus||_(L2[0,pi]) << sqrtN exp(-c0 sqrt(logN)).
The radial bound splits at beta3/4, preserving off-line zeros and avoiding
a nonuniform constant near beta1/2. This suppressed bound is uniform for
arbitrary finite truncations; the TOTAL norm used in Cauchy is the saved
full norm, or its paid T=C NlogN truncation. Conjugation gives exactly
the e/pi real-part factor. Removing2PQ+Q^2 costs O_A(N/log^A N), leaving
the square P^2, not its modulus. The same-sign signed lower margin stays
OPEN. No actual zeros or new prime ranges were computed.
Five exact sign/algebra/log-budget guards passed normal0.002s/-O0.001s;
independent Sol theory/actual-file PASS. No numerical c/onset or external
novelty claim. Source corrections, polynomial tools and runtime limits persist.

The then-next question (now tested in c901fc3): can the actual phase of the retained
positive-height pair kernel identify a nonempty region whose aggregate
contribution is provably small? Derive its stationary points first, then
pay amplitude, endpoints and the SUM over zeros before claiming any saving.
Keep N fixed, all real parts, Gamma phases and the finite period. Do not
substitute difference-height correlation or a full-line gamma quotient.
If it only locates stationary points without controlling a sum, classify
that as diagnosis and retain the signed lower-bound gap. Fresh <=30-minute
pursuit; overall goal active, no process claimed after this checkpoint.

## Previous pursuits: triprime preflight and a pointwise spectral transfer

The previous goal turn was PROGRESS: c0f70ca paid the moving cubic endpoint
and changed the surviving coefficient classes. This turn resumed verified
clean maine1e3779. No execution across the stopped checkpoint is claimed.

Triprime test started18:18:01 UTC, reassessed by18:25:26 UTC,
changed-under-evidence; reviewed mathematics **98dc8b7**. The diagonal
can be paid at x^(5/6) times log powers after grouping the two smaller
primes into a unique semiprime row. The off-diagonal is still
t(N-sr)-r(N-st)=(t-r)N with all masks. Its third factor supplies no
automatic free average. Nine guards normal0.139s/-O0.142s; Sol PASS.
Reviewer clarified that even nonnegative complete squares do not license
deleting restrictions INSIDE a signed row without a proved majorant.

Spectral test started18:23:12 UTC, reassessed18:37:13 UTC, progress;
reviewed mathematics **02448f6**. The source averaged formula's old error
was caught before promotion: Languasco2016 explicitly corrects both the
missing constant in Lemma5.1 and the normalized error O(sqrtN) to O(N).
The initial reviewer accepted the old printed exponent, then retracted
that conclusion after the later author correction was supplied. The
corrected averaged error does not by itself permit unit-scale differences.

The useful alternative takes a=1/N,z=a+it on ONE period[-pi,pi]. With
S=sumLambda(n)e^(-nz), Z=sumGamma(rho)z^(-rho), M=1/z-Z, corrected
S-M has L2 norm O(log^2N); Parseval gives ||S||2=O(sqrt(NlogN)).
Hence replacing S^2 by M^2 in the exact target Fourier coefficient costs
O(sqrtN log^(5/2)N+log^4N)=o(N), unconditionally. The single-zero part
reduces to2psi(N-1)-N using V=(e^z-1)^-1. The pair term B_(N,T) remains
SIGNED and contains the full kernel D_N(rho+sigma), ordered pairs and
both signs of zero heights. No replacement by a full-line gamma quotient.
Uniform damping and cumulative zero counting give tail
N*T^(3/2)*log(2T)*exp(-T/(2piN)); T=C_A NlogN suffices. No zeros were
computed or assumed complete on the critical line. A fixed lower margin
B>=-(1-delta)N would yield prime pairs after the paid proper-power error,
but that signed margin is OPEN. Six guards normal0.023s/-O0.034s;
independent theory/actual-file PASS. No new coverage or effective onset.

The then-next question (now completed in cca6455): can pairs with OPPOSITE
imaginary signs be deleted from B at all-log precision? The proposed
mechanism is one-sided Gamma damping, the classical zeta zero-free region,
and the already proved total L2 norm. First bound Z_minus on t>=0 and
Z_plus on t<=0, keeping small t, every zero and logarithmic losses. Only
then apply Cauchy to the actual cross term. Success would leave a precise
same-sign spectral problem; it would not evaluate its signed lower bound.
Reject if the necessary one-sided norm is merely assumed, RH is silently
inserted, or a positive norm is confused with the target square. Fresh
<=30-minute pursuit. All earlier polynomial components and source/runtime
corrections persist; no process is left running or manual wake queued.

## Previous pursuit: paid moving cubic cutoff and factor-class cancellation

Started18:03:24 UTC, reassessed18:15:16 UTC, progress.
Resumed verified clean mainbd4a46b; reviewed mathematics **c0f70ca**.
The actual comparison supports Type I to sqrt(x)/log^B x: Ford2023
Theorem3.4 provides BV with the logarithmic margin and endpoint maxima;
Theorem3.6 with sieve level x^(1/4) pays the comparison floor errors.
All nonreduced and large common-prime mismatches are all-log small.
Abel handles the moving low-divisor weights; cubic vanishing pays the
remaining tail x*(loglogx)^4/log^2x. This is o(x/logx), not all-log.

Moving-cutoff localization requires a FIXED multiplicative majorant;
dominate the n-dependent factors by W_(2t,sqrtx) before Henriot.
Exact p-power extraction retains min(1,4t logp/logx), so the saved
cubic saturated integral gives kappa*log(e/kappa) relative loss.
Common factors, large powers and rough squares remain paid. Constants
in the leading loss are uniform for fixed0<kappa<=1/20; the squareful
error's onset is not uniform for kappa moving with x.

On squarefree n, complementing d and n/d at sqrt(n) gives
[1+(-1)^(k+omega(n))]U_k equal to a degree-k finite difference.
Thus cubic odd classes>=5 vanish; triprimes have coefficient
24 logp logq logr/(logn)^3. EVEN classes stay, including negative
six-factor patterns. Fixed sqrt(x) and repeated-factor inputs do not
share the exact zero. The resulting prime identity retains E+24T
with every roughness/coprimality mask and p<q<r ordering. Neither
that signed sum nor its sufficient positive margin is estimated.

Sol theory/actual-file PASS, six focused guards normal0.106s/-O0.108s.
No material correction. The checks cover exact complement/triprime
algebra, wrong-cutoff and nonsquarefree counterexamples, local majorant
domination and tail powers; the analytic argument is separately reviewed.
No new Goldbach coverage, onset, novelty claim or external action.

The following next test is now COMPLETED by98dc8b7 above. Its question
was whether the retained triprime product
supply an extra averaging variable that a dispersion estimate can use
with PRIME coefficients and all the actual masks? First derive the exact
off-diagonal form and its complete diagonal/coefficient costs, and compare
it against the saved rough_mobius_dilation.py and free_divisor_correlation.py
input boundaries. Only inspect a new source if the third factor creates
a materially different applicable hypothesis. Success means a signed
saving for a specified nonempty factor region at fixed target N. Reject
the route if it merely reproduces the saved dilation covariance, requires
free coefficients, loses masks or replaces pointwise N by an average.
Fresh <=30-minute test; do not redo the old free-variable or generic
variance experiments. Keep the overall goal active; no process is claimed
after closeout and no manual continuation is queued.

## Previous pursuit: direct Mellin localization for cubic and quartic weights

Started17:50:01 UTC, reassessed18:00:02 UTC, progress.
Resumed verified clean maindbe552e; reviewed mathematics **85e7d44**.
The existing exact polynomial Mellin formula converges for each n and
k>=1. Use t=1+|u| directly; the corrected Henriot/Mertens cost is O(t^2)
uniformly for t>=1. No fixed power10 majorant is needed on this factor.
For exactp^j||n, retainmin(1,beta*t), beta=logp/logV, before removing
coprimality. Both actuala and comparisonb reduce to the same integral
 J_k(beta)=int_1^infty min(1,beta*t)t^(1-k)dt.
For k>3,J=beta/(k-3)-beta^(k-2)/((k-3)(k-2)); for k3 it is
beta*(1+log(1/beta)). For k2 the positive majorant's truncation grows
as1-beta+log(beta B); the exact T_2 Mellin formula does NOT diverge.

The complete prime-power sum is paid using
B(v)=sum_(p<=exp(v))logp/(p-1)<=C v, including the atom atlog2.
WithU=gammaL,Z=kappaL, integration fromlog2^- gives the cubic bound
C(Z/U)*(2+log(U/Z)). No separate logL/L loss is needed for this upper
bound; the endpoint atom is already included. Thus fixed
0<kappa<=min(1/20,gamma/2) gives ACTUAL localization relative losses
O_(gamma,k)(kappa) for k>=4 and O_gamma(kappa*(2+log(gamma/kappa)))
for k3. Both vanish withkappa. The earlier gcd/power deletions and
nonuniform-in-moving-kappa squareful remainder remain correctly paid.
The exact NEW residual C_(k,kappa) stays signed and OPEN.

Without a selected small prime, int_1^infty t^(1-k)dt=1/(k-2) also
proves sum|T_k|(a+b)<<_(gamma,k)S_2(N)x/L+all-log for k>=3.
This is a main-scale upper bound with no certified positivity constant.
Cubic T has positive triprime and negative six-factor toy patterns;
never replace it by a nonnegative weight. No new coverage or onset.

Independent Sol theory/actual-file PASS. Nine guards pass normal0.013s
and-O0.014s, including independent rational Riemann enclosures for J,
complete-cost shrinkage, divergent-majorant scope and coefficient signs.
No material correction; the simpler Stieltjes upper bound supersedes
an unnecessary lower-end error in the initial review calculation.
Live budget critical cap1, existing reviewer only; no new agent/tool route.
All prior source corrections, unavailable Qwen exception and polynomial
components remain. No old experiment rerun or external action.

The following predicted test is now COMPLETED by c0f70ca above. Its
original concrete hypothesis was: reach the MOVING critical
cutoffV(n)=sqrt(n) for the cubic weight. First prove actual Type I to
D=sqrt(x)/(logx)^B from the already used BV and comparison inputs.
Then bound d>D directly using the cubic's vanishing near the cutoff;
the predicted crude tail is O_B(x*(loglogx)^4/(logx)^2)=o(x/logx).
Do not silently replace sqrt(n) by sqrt(x): exact divisor complementation
needs log-factor shares summing to1 for each squarefree n. Test whether
that symmetry kills odd factor counts>=5 and gives the exact triprime
coefficient24*product(logp/logn), while preserving every other term.
Also recheck moving-cutoff localization and all source quantifiers.
The endpoint transfer and cancellations are preliminary predictions,
not promoted results. Fresh <=30-minute test; reject if a tail, source
uniformity or changed remainder is unpaid. Overall goal remains active;
no process claimed after closeout and no manual wake queue.

## Previous pursuit: actual fixed-power localization using polynomial suppression

Started17:29:50 UTC, reassessed17:47:33 UTC, changed-under-evidence.
Resumed verified clean main3df33dc; reviewed mathematics **3882437**.
The available hard-H fundamental-lemma proof does not reach fixed-power
roughness at prime precision: its sieve ratio becomes fixed, leaving
unpaid logarithmic factors. This is a failed bound, not a lower bound
for the actual error. A single small-prime layer can still fit Type I
whenkappa<e; do not say every such layer crosses the half-level. The
unresolved issue is reconstructing the full union/products accurately.

The successful alternative is the preserved FULL polynomial coefficient
T_k(n)=sum_(d|n)mu(d)(1-logd/logV)_+^k, V=x^gamma,gamma<1/2,k>=9.
There is no P+(d)<n^nu mask. Its prime value is1 and full w-pairing is
TI-small. Actual small-prime loss satisfies
 sum_(n inI,P-n<=x^kappa)|T_k(n)w_n|
 <<_(gamma,k)(kappa+1/L)S_2(N)x/L+all-log,
with the leading constant uniform0<kappa<=1/20. The accuracy is relative
toB_P~S_2(N)x/(2L), not a uniformdelta*x/L with S_2 omitted.

Mechanism: the polynomial Mellin majorant has local factor
a_t(p)<=2t logp/logV. Removegcd(n,N)>1 at all-log cost; small common
primes force partner proper powers/b0, large ones use averagedtau.
For n=p^j m, extract the ENTIRE p-power so(p,m)=1, then extracta_t(p)
BEFORE dropping that condition. Atp^j<=x^(1/10), corrected Henriot on
m,N-p^j m has variable length>=x^.9, primitive degree2 forms and the
same exact local valuation factors independent ofj. Both actualLambda
and comparisonb cost (x/p^j)S_2(N)logp/L^2. Forb, its Euler factor
logX/logy cancelsc_y<<logy. The extra third kernel moment is finite.
Summinglogp/(p^j) givesO(kappa L+1). Higherp^j costO(x^(39/40)L).

The exact NEW residual is
 prime mass=B_P-C_(k,kappa)(w)+O((kappa+1/L)S_2(N)x/L)+all-log,
whereC sumsT_k(n)w_n on COMPOSITE, squarefree, target-coprime n with
P-n>x^kappa. Its squareful deletion costsxL^2/x^kappa. Fixedkappa makes
Omega(n)<1/kappa, but this is not a practically small factor count or
effective onset. The squareful all-log remainder is not uniform when
kappa varies withx. C remains OPEN; do not import the oldH/M/R pieces.
For a small/large semiprime the oldH is0 whileT_k=1-(1-a/gamma)^k>0;
the new composite contributions are indispensable.

Independent Sol theory/actual-file PASS. Five guards pass normal0.001s
and-O0.002s. No mathematical correction; root/reviewer scoped the hard-H
single-layer statement correctly. NewTheorem5 of Henriot's erratum is
the authority; original definitions were rechecked, blocked erratum was
not retried. Live budget balanced cap3, existing reviewer only; Qwen
unavailable exception unchanged. No old experiment rerun or outside action.

The then-next question, answered in85e7d44 above: is k>=9 only a cost of routing through
the existing power10 majorant? Apply the exact polynomial Mellin formula
directly and split its frequency integral at logV/logp, retaining
min(1,t logp/logV). Prediction: quartic weights may retainO(kappa) loss,
and cubic weights may giveO(kappa log(1/kappa)) loss, still arbitrarily
small relative toB_P. Check source uniformity, both a/b terms, full prime
sum, constants and the unchanged exact NEW residual before promoting.
No low-degree result has yet been proved here. Reject a divergent or
logx-sized loss rather than hiding it in a constant. Fresh <=30 minutes.
Overall goal active; no running process claimed after closeout, no wake queue.

## Previous pursuit: exact prime-dilation criterion and actual coprime localization

Started17:03:39 UTC, reassessed17:21:42 UTC, changed-under-evidence.
Resumed verified clean mainab82775; reviewed mathematics **16fa2d0**.
The generic Katai mean-divisor reconstruction bound costs
Xlogx/sqrt(loglogx), too large at prime-count precision. This is a failed
upper bound, not a lower bound for the actual sum. Fixed auxiliary primes
eventually lie below the moving roughness cutoff, so their vanishing
dilation sums cannot supply an unproved uniform rate for the moving family.

The exact classical Ramare identity avoids that reconstruction error.
All prime divisors of retainedr lie in(y,x^nu]; eachr is countedomega(r)
times with denominator1+omega(r/p)=omega(r). No missed-prime residual.
Forc=tv,X=x/c and a dyadic auxiliary-prime block(P,2P], full zero-extended
masks give |S_tv,P|^2 <= (X/P)(D+O), withD<<L^2X/logP andO the REAL
SIGNED off-diagonal. Drop the denominator only from the entire positive
per-s square before expanding. Individual cross-term absolute values
are not required. The diagonal summed over ALL rows/blocks is
O(xL^3/sqrt(y)), all-log small. WithE=sum_(t,v,P)max(O,0)/P,
 |M| <<_A x/L^A + sqrt(xL^3 E).
ThusE<<x/L^(2A+3) is sufficient; the stronger uniformO^+<<XP/L^(2B)
yieldsM<<x/L^(B-3). Neither covariance input has been proved, and
R_nu(w) remains separately open in prime mass=B_P-R_nu+M+all-log.

An additional ACTUAL estimate allowsgcd(n,N)=1 inM. At mosttau(n)
representations and |w|<<L give absolute loss
O(xL^2 sum_(ell|N,ell>y)1/ell)=O(xL^3/(ylogy)), all-log small.
This removes deterministic common-factor rows and auxiliary divisors ofN.
The remaining pair has reflected argumentsN-cps,N-cqs and relation
q(N-cps)-p(N-cqs)=(q-p)N. Keep smoothness, physical, squarefree,
coprimality andv1-or-prime masks and all four terms of(a-b)(a-b).
These are von Mangoldt arguments until proper powers are separately paid.

Source-known mechanism: Green arxiv1604.04481v4 section2,p6 has the
Ramare identity; the p5 remark explicitly names the analogous linked-prime
covariance for shifted Mobius. Its general proposition is NOT imported
with parameter restrictions waived. Tao2011-11-21 and BSZ Theorem2 were
checked for the generic criterion's quantitative/limit-order boundary.
Oxford's Green PDF returned403; the arxiv version worked. No unchanged
retry. This is a task-specific exact support/budget application, not a
new identity or newly solved correlation.

Independent Sol theory and actual-file PASS. Five guards pass
normal0.012s/-O0.012s. Initial patch used the home cwd, causing import
failure; precisely the two new files were moved into the repo with no
overwrite, then tests passed. No mathematical correction; reviewer wording
clarified reflected von Mangoldt arguments. All earlier corrections and
polynomial components remain valid. No new Goldbach coverage or onset.

The then-next hypothesis, tested in3882437 above: can the small-prime localization be
raised fromy=exp(sqrtL) to a fixed powerx^kappa, with actual error at most
delta*x/L for any prescribed smalldelta? Use the existing joint arithmetic
majorants/sieve sandwich to pay the |wH|-weighted approximation cost;
the old crude L*tau(n) bound with fixed sieve parameter is insufficient.
Prediction: if this cost closes, the long cofactor has a bounded number
of prime factors, allowing a different arithmetic treatment. Test the
full dependence onkappa,e,delta before any decomposition or numerical run.
Reject the hypothesis if the constants/log losses cannot reach prime
precision; do not assume formal local main terms cancel their errors.
Fresh <=30-minute clock. Overall goal active; no process claimed after
closeout, no manual wake queue. This is an optional mathematical direction,
not a replacement of the saved signed-covariance or Type II targets.

## Previous pursuit: actual rough-squarefree localization of the Mobius cofactor

Started16:39:03 UTC, reassessed17:01:31 UTC, changed-under-evidence.
Resumed verified clean maind2379cb; reviewed mathematics **3def1c4**.
The immediate rank-one coefficient shortcut failed: a finite 2x2 minor
of H(uv) is [[1,1],[1,0]]. The moving cutoff remains coupled. The exact
specialization nevertheless gives useful support: n=u v, all primes ofu
<n^nu and all primes ofv>=n^nu; H=sum_(d|rad u,d<=n^gamma)mu(d).
Foru>1 it vanishes ifrad u<=n^gamma; otherwisev is1 oroneprime.
The pure smooth v=1 class remains. Complementing divisors gives
H=-mu(rad u) sum_(t|rad u,t<rad u/n^gamma)mu(t). In the prime branch
t<n^(1/6+3e). Nonsquarefreeu cannot be discarded pointwise: n420 has
u60,v7,H1 althoughmu(u)=0. Nonzero nonroughH already excludes sourceN,
so no additional N-mask is needed on this surviving smooth sector.

A further ACTUAL estimate resolves that multiplicity problem in aggregate.
Use y=floor exp(sqrt(logx)), fundamental-lemma levelD=x^(e/4), and the
nonnegative upper-minus-lower sieve gapdelta. Its all-log mean plus
Cauchy andsumtau^3<<xlog^7x pays |wH|<<logx*tau(n). Expanding the upper
sieve andH gives moduli lcm(a,d)<=x^(1/2-3e/4), with multiplicity<=tau^2;
the saved Type I proves the y-rough H-pairing all-log small. Consequently
the smooth error S_e(w) may be restricted to y-roughn. Squarefuln then
cost O(xlog^2x/y), using tau(p^2m)<=3tau(m), and may be removed.

On this PAID rough squarefree support, S_e(w)=-M_e(w)+all-log, where
M_e=sum_(n=trv inI)mu(r)w_n with r>n^gamma, mu^2(tr)=1, all primes oftr
in(y,n^nu), andv1orprime>=n^nu. Keep t1; the prime branch has
t<n^(1/6+3e). Therefore prime mass=B_P-R_nu(w)+M_e(w)+all-log, R_nu
the full rough COMPOSITE error. Neither remaining signed sum is estimated.
This preserves one ordinary long Mobius sign, not arbitrary coefficients,
but the smoothness, product, squarefree and prime conditions stay coupled.

Other checked components: actual prime-slot powers cost
O_eta(x^(1-nu/2+eta)log^C x), with exponent<=64/75 ateta=.01. HB4 then
needs at most8 primitive mu/free/log factors per slot rather than the
source's12 root-lift factors. This does not create a long free variable.
Applying saved parity/PNT laws toell gives S_e(ell)=(1-J2+J3+o)B0,
J2=log((1-nu)/nu), J3<=3e^2/nu^3, coefficient>1/5 andtending1-log2.
That is an ARTIFICIAL parity calibration, not an actual prime estimate;
it shows the surviving smooth sector cannot just be assumed negligible.

Sol theory/actual-file PASS, including the later localization refinement.
Sixguards pass normal0.015s/-O0.013s. An initial tuple/list assertion was
corrected to the existing factorization API; no mathematical correction.
Live16:39 budget was conserve; Qwen/routing exceptions remain unchanged.
No previous experiment rerun, install, publication/push, foreground or wake.

The then-next question, now tested in16fa2d0 above: can a quantitative multiplicative-correlation
criterion exploit mu(pr)=-mu(r) on this squarefree support, using auxiliary
primes ABOVEy? Derive its required dilation covariance and complete loss
budget with the actual masks before checking an arithmetic estimate.
The old unmasked Liouville imports and generic covariance budget do not
answer this masked question. Reject the route if it merely restores the
same untreated correlation without a better estimate. Fresh <=30 minutes.
Overall goal active; no process is claimed running after this checkpoint.

## Previous pursuit: actual critical composite mass and a conditional positive sieve

Started16:11:58 UTC, reassessed16:36:57 UTC, changed-under-evidence.
Resumed verified clean main8a3f971; reviewed mathematics **a301a46**.
The comparison b_n=c_y 1_((2x-n,P(y))=1), y=floor exp(sqrt(logx)), has
B_P~S2(2x)x/(2logx), source growth, all fixed divisor-weighted Type I
below1/2, and uniform source(b.2) across convex ordered factor regions.
The latter is proved by fixing all but one large prime, applying BV plus
the fundamental lemma at the remaining prime scale, and summing errors
with sum1/M=O(1). This is model regularity, not actual Type II.

For P_e=(1/2-e,e,1/3-2e), 0<e<=.01, the sieve's surviving rough composite
region consists only of semiprimes near(1/2,1/2) or(1/3,2/3), and triprimes
near(1/3,1/3,1/3). A dimension2 upper sieve for r and2x-Mr bounds its
ACTUAL Lambda(2x-n) mass by C e S2(2x)x/logx+o(x/logx), C absolute.
This uses no prime-pair asymptotic. Repeated factors and partner powers
are negligible. Ford--Maynard Prop7.19 plus Lemmas7.18/7.21 then give,
CONDITIONAL on full arbitrary-divisor-bounded Type II for
(x/2)^e<d<=x^(1/3-e), prime mass >=(1-C'e+o(1))B_P.
For sufficiently small fixed e this would give prime pairs, with an
unspecified onset. Actual Type II, universal coverage and effective onset
remain open. No implication from the older balanced BII is asserted.

Source corrections: printed p17 Thm4.16 proof has w_n=1 otherwise where
its claimed vanishing needs0; its constant K also leaves a nonzero x/log^2x
secondary term. The module proves a restricted corrected counterexample
using pointwise K_x(t); do not import the literal proof. Source Eq4.1 fails
for actual w at x=p prime,n=p, and common scalar normalization cannot fix
both it and B_P>=x/(rho logx). The new critical-mass proof avoids Eq4.1.
Theorem2.2(A1) uses n>=M+1; Lemma7.18 uses Pminus(n)>=n^nu, both verified
in PDF text against misleading web extraction. Ford notes3.4 is BV and
3.6 is the fundamental lemma. All older source corrections remain binding.

Sol theory and actual-file PASS without material correction. Eight combined
guards pass normal0.007s/-O0.006s. No old experiment was repeated. Existing
Qwen and routing exceptions persist; no installs, external actions or wake
queue. Polynomial identities and bounds remain available components.

Next concrete question, UNTESTED: in the g(empty)=1 specialization of
Prop7.19, can one retain a smaller explicit family of bilinear coefficients
than arbitrary tau-bounded sequences? Extract one actual family before
the proof replaces it with a supremum, and test whether its Mobius/log
structure meets an existing arithmetic estimate. Falsifier: the proposed
restriction still needs an uncontrolled linked-prime correlation, or just
renames a completed Type I calculation. Preserve the exact family either
way; no claim that restricting coefficients alone proves cancellation.
Fresh <=30-minute clock next pursuit. Overall goal remains active; no
research process is claimed to keep running after this checkpoint.

## Previous pursuit: rough Liouville bias and the prime-partner transfer gate

Started2026-09-09 15:56:23 UTC, reassessed16:09:06 UTC, changed-under-evidence.
Resumed verified clean main6dee23f. Reviewed mathematics **ed0d334**, in
`rough_liouville_transfer_gate.py`, gives the exact cubic-rough signed target
and tests whether an existing Liouville correlation theorem supplies it.

For strict P^-(n)>Y^(1/3), n in(Y/2,Y], Omega(n)<=2 with multiplicity.
With q PRIME, n+q=m, and nonnegative weight logn logq F(n/Y,q/Y), write
A for all rough mass, C for rough semiprimes including squares, Q for
the Liouville-signed mass, and G for actual prime pairs. Exactly A=C+G,
Q=C-G. Thus Q<=-kappa Y S2(m) would give G>=kappa Y S2(m). This is a
stronger-than-necessary sufficient input, not an estimate already proved.

There is a proved one-variable bias: for fixed C1 g compact in(.5,1),
sum R(n)ell(n)logn g(n/Y)=(log2-1)Y integral g+O_g(Y/logY).
This is an APPLICATION of the saved PNT and semiprime integral. The
semiprime prefix sum is sum_(z<p<=sqrtx)[pi(x/p)-pi(p)+1], with fixed
z=Y^(1/3), and has leading(log2)x/logY uniformly x in[Y/2,Y]. Squares
are retained. For nonnegative nonzero g, the log-weighted Fourier sum
therefore cannot be uniformly o(Y): frequency0 already has main scale.
A centered model or a minor-arc estimate is not ruled out.

Exact inclusion-exclusion gives R(n)ell(n)=sum_(d|n,d|P(z))ell(n/d),
with POSITIVE outer coefficients. For any fixed gamma<1, d<=Y^gamma
contributes O_A(Y/log^A Y) to the one-variable log-weighted sum by the
saved strong Liouville summatory estimate and Abel. Thus the d>Y^gamma
tail carries the negative main. This is an inclusion-exclusion tail,
not a subset of rough n; for rough n only d=1 occurs. Its analogue with
q prime introduces ell(k) in dk+q=m and is not controlled by free Type I.

Primary source fit: Lichtman arxiv2009.08969v2 averages multiplicative
shifts, and its typical-factor set S requires a prime <=exp((logY)^(1-delta/2)).
For fixed delta>0 and large Y it is DISJOINT from our cubic-rough set.
Theorem6.2 retains the bad-set term, exactly where our support lies.
Mangerel arxiv2404.12117/IMRN2024 has full-interval sign rigidity;
arxiv2412.17199v1 adds conditional GRH sign-pattern results, with its
quantitative statement for prime targets. Neither preserves our masks.
Krishnamoorthy arxiv2608.13266v1 Theorem2 is an averaged exceptional-set
statement for unmasked binary sums. No other claim from it was imported.

Independent Sol theory and actual-file PASS, no material correction.
Six new guards pass normal0.008s/-O0.007s. No completed experiment was
rerun. No new prime-pair coverage or actual signed correlation estimate.
Preserve polynomial tools, all source corrections, and runtime limitations.
The OUP canonical IMRN URL returned Internal Error on this later request;
its earlier full-text receipt and primary arxiv route remain available.

Next concrete question: does the existing NONNEGATIVE comparison in
composite_bilinear_bridge.py satisfy the factor-pattern regularity(b.1)/(b.2)
needed for Ford--Maynard's prime-producing sieve, and what exact additional
Type II region would yield only a positive lower bound? Read the source's
actual conditions before selecting a region. Its framework and a stronger
Vaughan bilinear condition were already recorded; do not rederive those.
Retain the exceptional-character obstruction to an uncorrected asymptotic,
and distinguish actual factored-modulus estimates from arbitrary-coefficient
Type II. This next application test is unperformed; fresh <=30-minute clock.
Overall research goal remains active. No research process remains running
at this reviewed checkpoint; no manual wake queue or push was issued.

## Preceding pursuit: fixed-target factor deficit and the missing prime endpoint

Started2026-09-09 15:34:56 UTC, reassessed15:52:58 UTC, changed-under-evidence.
Resumed verified clean main4adb690. Reviewed mathematics **cb01376**, in
`prime_factor_endpoint_gate.py`, tests the proposed largest-factor input.
The full additive factor moment repeats saved TI; its needed restriction
has exactly the original prime-correlation gap.

With lambda=delta_1 and U=floor(Y^gamma), define B_U(n)=sum_(p|n,p>U)logp,
and C_U=1_composite B_U. On the physical support B_U=P+C_U. The full
Lambda-divisor identity plus proper-power pruning proves C_F(B_U,E) is
O_A(Y/L^A), now with pruning exponent1-gamma/2+2delta<1. Let
A_C=sum C_U(n)Lambda(m-n)F and M_B=sum B_U(n)Gamma_S(m-n)F, exactly.
Then the genuine weighted prime-pair sum is G_F=M_B-A_C+O_A(Y/L^A).
A sufficient new ONE-SIDED estimate is A_C<=M_B-kappa Y S_2(m), kappa>0.
Neither the first-moment identity nor the source bounds prove this deficit.

The saved all-modulus Gamma comparison computes
 M_B=Y I_F(L-K_U(m))+Y J_F+O_A(Y/L^A),
 K_U=sum_(h<=U,(h,m)=1)Lambda(h)/phi(h), J_F=int F(v,m/Y-v)logv dv.
Uniformly K_U=gamma L+O(loglogY); omitted prime towers for p|m cost
O(loglogY). Thus M_B=(1-gamma)I_F YL+O(YloglogY). That coarse main
cannot replace EXACT M_B when deciding the required Y S_2 margin.

For odd n in(Y/2,Y], primality is EXACTLY P+(n)>Y/3. Consequently the
Y/3-tail with a prime partner is the Goldbach sum itself. A fixed theta<1
does not reach it: n=3p, Y=4p is composite with P+(n)>Y^theta eventually.
This is a factor witness, not a fixed-target prime-pair count or lower bound.

A sharper diagnostic applies a published factor-statistics theorem to the
CLASSICAL parity sequence a_n=1+ell(n), ell=Liouville. It has a_p=0 at
every prime but exact N_d=floor(x/d)+ell(d)H(x/d). Tao2014Notes2Ex41's
strong Mobius sum, and ell=mu*square-indicator, give H(x)=O_A(x/log^A x).
Thus a has level1 for every FIXED c<1, with g(d)=1/d, index1 and the
required congruence bound. All density hypotheses are checked explicitly.
Bharadwaj--Rodgers (Cambridge online17April2026), section1.2 and Theorem7,
then give the full fixed-dimensional Poisson--Dirichlet factor laws despite
zero prime support. This does not model the actual shifted-prime local
densities or prove any statement about actual Goldbach exceptions.
The level estimate fails at c=1: prime d in(x/2,x] alone give discrepancy
of order x/logx. Neither fixed-c estimates nor weak limiting laws license
the moving 1/logY endpoint needed here.

Primary sources/locators are in the module. Li arXiv2508.18285v1 Theorem1
reports a fixed-shift .679-epsilon factor threshold, not the needed endpoint
or moving-target uniformity; no numerical sieve result from it is used.
The attempted arxiv HTML2211.09641v4 URL returned Internal Error; its abstract
was readable. No unchanged retry or broader runtime failure is inferred.
The prior TaoNotes7 exclusion and all other source corrections remain.

Seven guards pass normal0.008s/-O0.006s; Sol theory/actual-file PASS after
adding the remaining local-density condition(B) checks. A test initially
chose H(10)=0 for a sign discriminator; replacing it with H(9)=-1 made the
guard nonvacuous. No theorem changed. No range scan, installs, foreground
work, contacts, spending, publishing/push or manual wake queues. Live
15:36:55 UTC budget: conserve, spawncap2, researchTerra/high, reviewSol.

Next concrete question: on cubic-rough n=m-q, can a genuinely signed
Liouville estimate against the PRIME q give a useful negative margin?
Recover the exact prime/semiprime split from factored_linear_barrier.py,
write the rough reflected prime sum with all weights, and check a primary
correlation theorem against its unaveraged, moving-m quantifiers. Do not
repeat the old one-dimensional linear-sieve substitution or infer a moving
endpoint from a fixed-scale limit. The next test is unperformed. Fresh
<=30-minute clock; overall goal active. No research process remains running.

## Preceding pursuit: complete divisor layers cancel by the saved cutoff identity

Started2026-09-09 15:14:58 UTC, reassessed15:33:15 UTC, changed-under-evidence.
Resumed verified clean maina650b77. Reviewed mathematics **cb04788** extends
`resonant_semiprime_error.py`, sections8-11. This is an application of
**02e1627**, not a new distribution theorem or additional prime-pair coverage.

For ANY subset J of2<=d<=V, w_d=-lambda_d, the COMPLETE internal layer is
 L_J(n)=sum_(d in J,b>U,db|n)w_d Lambda(b)
       =sum_(d in J,d|n)w_d log(n/d)
        -sum_(d in J,b<=U,db|n)w_d Lambda(b).
The first part is TI with one Abel log. The second has modulus h=db<=UV
and coefficient magnitude<=logh. Thus C_F(L_J,E)=O_A(Y/L^A) for actual
unexceptional E, and also for E_* by its proved TI bound. Saved internal
proper-power pruning makes the complete PRIME layer equally small.
Because d>=2, c=dk>=2: no c=1 compensation enters, even when p~Y.
Weights may depend on d,Y,m, but further prime/cofactor masks are not
licensed in this estimate. Zeroing lambda on J preserves lambda1=1.

For J=D, split ALL p>U into the old P rectangle and its complement.
Their actual signed correlations satisfy T_D,out=-T_family+O_A(Y/L^A).
Neither isolated piece is estimated. All nontrivial d can be removed at
once; lambda=delta_1 leaves exact prime remainder
 -sum_(p|n,p>U,n!=p)logp.
The missing prime compensation/correlation remains. Retire the rectangle
variance as a REQUIRED next step, preserving it as a sufficient optional
target and keeping the polynomial and factored-modulus tools available.

The diagnostic gives an explicit cancellation check. Its selected P bases
have3a1<1<4a0, and D bases4b1<1<5b0, so f(n)=C_P C_D on every Lambda
support point n~Y. For the same F>=f0>0 on[.7,.8]^2, I_F>0, ordinary
strong PNT and the complete compensated identity give
 C_F(R_lambda,p,E_*)=C0 I_FY+O_A(Y/L^A), C0=log(a1/a0)log(b1/b0)>0.
This is UNIFORMLY for normalized bounded cutoffs, but with artificial E_*.
On n=pd*j<=Y, two extra prime types cannot coexist since2(a0+b0)>1.
Exact row expansion, smooth counts and PNT sharpen the old lower bound to
 T_family(E_*)=(1-C0)c I_F YL+O_A(Y/L^A),
 T_D,out(E_*)=-(1-C0)c I_F YL+O_A(Y/L^A).
Here c is the saved fixed-polynomial density constant. Counting errors
costY^.80016 L; reciprocal corrections are power-small. The ENTIRE
remainder complement additionally carries C0 I_FY. The positive full
diagnostic main is neither an actual-prime estimate nor a counterexample
to the one-sided lower bound needed for coverage. I_F>0 is essential.

Ten exact guards pass normal0.019s/-O0.016s. Sol theory/actual-file PASS,
including composite d, signs, proper powers, prime compensation and the
outside-window fourth term. No source refetch, range experiment, install,
foreground work, publishing/push or manual wake. Live15:18:01 UTC budget
receipt was conserve, spawncap2, researchTerra/high, independent reviewSol.
The earlier Qwen unavailable exception and source/runtime limits remain.

Next concrete question: can a one-sided bound for prime factors of m-q,
with q prime and m FIXED, improve the full remainder's lower bound? First
derive the exact log-factor inequality required, allowing lambda=delta_1
and U=floor(Y^gamma), and reject it if it only restates the same open
correlation. Then check proposed arithmetic input for uniformity in m~Y,
the precise sign and constant; averages over m or shift1-only results are
insufficient. This next asymmetric test is NOT completed. Fresh <=30-minute
clock. Goal active; no research process remains running at this checkpoint.

## Preceding pursuit: generic norms admit coherent semiprime progression errors

Started2026-09-09 14:54:20 UTC, reassessed15:12:23 UTC, changed-under-evidence.
Resumed clean maind87403b; reviewed mathematics **bd7d1e4**, in
`resonant_semiprime_error.py`. The intended Kloosterman transfer was tested
against its necessary input distinction. A defined comparison-error sequence
satisfies the relevant generic controls and still has large signed row sums.
No assertion about the actual Lambda-Gamma_S is changed by this example.

Reuse the prime rectangle a0=.3,a1=.30002,b0=.2001,b1=.20012,
s0=.5001,s1=.50014. For Y through multiples4, m0=3Y/2, define
 E_*(q)=1_(Y/2,Y](q) f(m0-q),
 f(N)=sum_(p,d)c_pd(N)/(pd)=(s(N)-C_P)(t(N)-C_D),
where C_P=sum_p1/p,C_D=sum_d1/d and s,t count prime divisors from the
two disjoint intervals. PNT gives C_P,C_D<=1/1000 eventually. On physical
N in[Y/2,Y], |f|<=4 and sum|E_*|^2<=16Y; on every family modulus row,
r|N forces f(N)>1/2. The proper-divisor subtractions in c_pd are essential.

For fixedgamma49/100 (or5/12<gamma<1-s1), every h<=Y^gamma is below r.
The primitive complete progression mean is0, including h sharing p or d.
The expanded three indicator counts give endpoint error<2 per(p,d), so
the FULL interval-maximum TI sum is O(Y^.99014/logY^2), uniformly in
the target shift. This is stronger than any fixed logarithmic saving.
Distinct reduced frequenciesa/r are Rmax^-2-separated. Direct interval
kernel packing gives ||E_*hat||infty<<Y^.50018 logY. These are proved
bounds for E_*, not a licensed match to the smooth MODEL input theorem.

For fixed nonnegative F>=f0 on[.7,.8]^2, every family row has
B_r^*(m0)>=f0Y/(40r). PNT at the LOWER prime endpoints gives
sum1/r^2~Y^-s0/(a0b0 logY^2), so
H_*>>Y^(2-s0)/logY^2. This exceeds the old targetY^(2-s1) by a factor
Y^(s1-s0)/logY^2 tending to infinity, despite a diagonal onlyO(Y).
The actual fixed-polynomial coefficientsA_r>0 also satisfy
T_family(E_*)>>YlogY, using sumA_r/r~c logY. This defeats the signed-family
estimate itself for the artificial sequence, not merely one Cauchy target.
No actual prime support, equalityE=Lambda-Gamma, or CROSS is asserted.

For a next ACTUAL attempt keep a natural weighted normalization:
w_r=A_r/r, M=sumw~cL, e_r=rB_r/Y, K=sumw|e_r|^2. Exact Cauchy is
|T/Y|^2<=M K. Sufficient K=o(1/L), equivalentlyK/M=o(1/L^2). Its actual
diagonal is O((Rmax/Y)L^2)=o(1/L), using multiplicity3 and actualsum|E|^2.
The weighted real off-diagonal is OPEN. The countermodel hasK_*>>L.
Reviewer correction preserved: this and the previous unweighted condition
are NOT globally ordered. Weighting removes a power mismatch nearRmin but
can require finer logarithmic precision nearRmax. Both remain sufficient.

Six finite guards passed normal0.007s/-O0.009s; Sol theory/actual-file PASS,
including weighted normalization. The tests cover Ramanujan factorization,
partial/full resonances, endpoint counts, exponent gates, coherent finite
rows, and exact weighted Cauchy. They are not prime-range experiments.
No source refetch, install, foreground work or wake queue. Live14:58:54 UTC
budget receipt: conserve, spawncap2, researchTerra/high and reviewSol.

Next concrete question: can the COMPLETE signed cutoff identity cancel this
diagnostic resonance between divisor sectors, without demanding smallness
of each sector? Test the actual-first-prime pairing against E_* together
with the exact cutoff compensation, and isolate what still fails for trueE.
An identity or estimate for E_* must not be promoted to the missing actual
prime correlation. Preserve the polynomial tools and the good-modulus result;
do not rerun generic norm completion. Fresh <=30-minute clock. Goal active;
no research process remains running at this reviewed checkpoint.

## Preceding pursuit: universal factor-range gap and an intact variance target

Started2026-09-09 14:39:59 UTC, reassessed14:52:29 UTC, changed-under-evidence.
Resumed clean main10321f3; reviewed mathematics **6a7c8ac** extends
`factored_prime_ap_transfer.py`, steps10-16. The earlier actual good-modulus
transfer remains valid. This pursuit rules out closing its complement merely
by tuning the same source factor caps, and identifies a centered variance.

EVERY admissible choice in Maynard III Theorem1.2 has
Q2<x^.05,Q3<x^.1,Q1<x^(.4-11sigma)<x^.4. Thus any modulus with least
prime factor>x^.1 and size>x^.4 is excluded. This is a boundary of that
specific theorem, not all of Maynard's results or all prime-distribution work.
Choose prime p with exponent in(a0,a1], a0=.3,a1=.30002, and prime d
with exponent in(b0,b1], b0=.2001,b1=.20012. Their products lie in
(Y^.5001,Y^.50014], inside the numerical prior levelY^.5002 but outside
EVERY source triple range for every endpoint x in[Y/2,Y]. For fixed
nu=gamma/2 in(5/24,1/4), one has d<V<p eventually and unique pairs.

For retained fixed-degree polynomial lambda, k>=9, the ACTUAL divisor
coefficient A_pd=-logp lambda_d=logp(1-logd/logV)^k is positive. PNT/Abel
gives the natural density mass
 M_Y=sum A_pd/phi(pd)=c_(nu,k)logY+o(logY),
 c=(a1-a0) integral_b0^b1 (1-b/nu)^k db/b>0.
The constant can be tiny; no finite onset or growing-degree uniformity.
Removing(pd,m)>1 loses only O(logY*(Y^-a0+Y^-b0)), uniformly for centralm.
The all-modulus Gamma comparison already proved gives
 G_family=Y I_F(m/Y) M_Y(m)+o(Y)=c I_F YlogY+o(YlogY).
Nonreduced truncated Gamma is still paid. If F>=f0 on[.7,.8]^2 and F>=0,
then I_F>=f0/20 on m/Y in[29/20,31/20]. These are coefficient/MODEL
claims, not lower bounds on the signed E correlation or Goldbach counts.

The exact unknown remains T_family=P_family-G_family, with the actual
Lambda partner in P; proper powers costY^(.5+o(1)). Preserve its primes.
Writing B_r=sum_j F(rj/Y,(m-rj)/Y)E(m-rj), H=sum_family|B_r|^2,
R=Y^(25007/50000), the actual coefficient norm is
 N_Y=sum A_r^2 ~ (a1/b1)(1-b1/nu)^(2k) R.
Exact Cauchy makes H=o(Y^2/R)=o(Y^(74993/50000)) SUFFICIENT for T=o(Y).
H's diagonal is already O(YlogY): every n<=Y has at most3 family divisors,
since positive prime-divisor counts(s,t) obey .3s+.2001t<1 and hence are
only(1,1),(1,2),(1,3),(2,1). Apply the saved actual E second moment.
The one-sided upper bound on 2Re(offdiag) is OPEN. Its partners satisfy
q1-q2=r(j2-j1), with common two-prime r and actual prime coefficients.

Thirteen finite guards passed normal0.003s/-O0.003s. Sol theory and
actual-file reviews PASS, including the exact variance normalization and
multiplicity3; no material correction. No new source fetch, range scan,
installation, foreground action or wake queue. Live14:40:38 budget receipt
was conserve, spawncap2, researchTerra/high, independent reviewSol.

Next concrete question: can completion/dispersion of the two progression
variables yield the stated upper bound on this ACTUAL semiprime-modulus
off-diagonal? Test whether the retained composite Kloosterman estimates
can be applied with the actual prime coefficients and enough saving for
H=o(Y^(74993/50000)). Pay every Cauchy/transfer loss; the older smooth
MODEL estimate is not an automatic answer. Reuse the established coefficient
norm and diagonal; do not rerun separate-moment or cap-tuning failures.
Fresh <=30-minute clock. Goal active; no research process remains running
at this reviewed checkpoint.

## Preceding pursuit: actual signed transfer on factored moduli beyond half

Started2026-09-09 14:24:20 UTC, reassessed14:38:06 UTC, progress.
Resumed clean main6d0a20b; reviewed mathematics **06acf3b**.
`factored_prime_ap_transfer.py` proves O_A(Y/log(Y)^A) for a selected
ACTUAL component of the prime-slot divisor expansion, uniformly for central
even m and bounded lambda supported d<=V with lambda1=1. The prior
polynomial weights are retained. No full remainder or new coverage follows.

Primary input is Maynard III, arXiv:2006.08250v1, Theorem1.2 printedp3:
https://arxiv.org/pdf/2006.08250
Its nested residue sup allows the common moving target m. Choose fixed
sigma1/2000, exponents(.3935,.025,.082), subtract1/10000 from each
actual cap. The source inequalities have strict margins; the same fixed
source parameters cover every endpoint x in[Y/2,Y] eventually.
Actual caps(P,A0,B0) have exponents(.3934,.0249,.0819), productY^.5002.

Keep U=V=floorY^(gamma/2), gamma in(5/12,1/2). Select(p,d) with p>U
prime, d<=V, and d=h*a*b, p*h<=P,a<=A0,b<=B0. A SINGLE canonical
ordered triple(p*h,a,b) per modulus suffices. Every modulus p*d has a
unique prime factor>V, and the source permits composite first factors.
This includes h>1 and avoids multiplicity. Any bounded coefficient mask
depending on(p,d,m,Y) is allowed, including p*d>sqrtY; it must be independent
of the progression variable k. The physical weight remains the common
fixed smooth F(pdk/Y,(m-pdk)/Y). No unrelated endpoint maximum is claimed.

Two logarithms are paid by increasing the source saving. Strong ordinary
PNT changes pi(x)/phi(r) to real prime-log density; sum1/phi(r)<<logY.
Tao2014Notes2 Cor39/Ex40 primary checked, separate from excludedNotes7.
The elementary Gamma progression comparison extends to D=Y^.5002 with
summed error YL S^(-1/2)exp(O(sqrtL))+D S^4, plus D*polylogs for lengths.
Multiplying by logp remains power-small for modeldelta<=1/4800. The full
nonreduced mean is0, but truncated Gamma is paid by these same errors.
Partner proper powers costY^(.5+o(1)). Nonreduced progressions contain no
prime partner>Y/2 once r<Y/2. The c=1 compensation vanishes ONLY in this
component since p<=P<Y/2; d=1,k>1 remains. The full expansion is unchanged.

Maynard II, arXiv:2006.07088v1 Defs1-2/Thm1.1 printedp2 is not a direct
alternative: its constant depends on fixed residue a, and every triply
well-factorable sequence at levelQ vanishes at moduli with prime factor
>Q^(1/3). Here p>Y^(gamma/2)>Y^(5/24), while even allowed levelY^(3/5)
has cube-rootY^(1/5). No permitted level padding repairs that support gap.
This is a limitation of the specific import, not of polynomial weights.

Seven finite guards pass normal0.003s/-O0.003s; Sol theory/actual-file PASS.
They check exact exponent margins, canonical h>1 splitting, symbolic
coefficient signs, nonreduced model means and balanced-factor support.
No numerical asymptotic onset or source theorem was inferred from tests.
Oxford accepted-PDF URLs returned403; arxiv v1 PDFs were readable. Do not
retry the unchanged Oxford route. No model install or outside action.

Next concrete question: does a positive logarithmic-size family of moduli
p*d with BOTH factors prime near exponents(.30,.20) escape EVERY allowed
Maynard III factor geometry, not just these caps? Test the full inequalities
and quantify the surviving coefficient mass before seeking a signed estimate
on that family. A coefficient-mass result alone would not bound its actual
correlation. Do not spend another pursuit merely tuning this cap choice.
Fresh <=30-minute clock required. Goal active; no research process remains
running at this reviewed checkpoint.

## Preceding pursuit: full absolute summation is actually too large

**dc7baa6**, absolute_remainder_obstruction.py, fixes B=max(1,||G||infty),
delta<=min(1/4800,1/(80B)), and a nonnegative fixed smooth F>=f0>0 on
[.7,.8]^2. Keep that EXTRA small-delta condition; it is not automatic for
arbitrary G at the old cap. For every sufficiently large Y there is an
even m in(1.4Y,1.6Y] such that the REGROUPED absolute mass of
R_lambda=(mu-lambda)*Lambda_>U*1 is at least(f0/32000)Y S_2(m),
SIMULTANEOUSLY for every bounded lambda1=1 supported<=V, U=V=W.
The same m works for the prime-pruned remainder, original hard A, and
the tuplewise absolute sum. Cutoffs may even depend on m.

The obstruction uses actual prime triples, not a random or formal model.
For prime q~Y, Gamma_S(q)=B_S=sum_(r<=S²)mu²(r)G/phi(r), independent
of q, and B_S<=5B(1+2delta logY)<=logY/4 eventually. Thus E(q)>=logY/2
on q in(.7Y,.8Y]. Every cutoff has S_lambda(c)=1 for prime c>V; at
distinct p,c>max(U,V), the FULL and pruned coefficients equal-log(pc).
Taking p in(Y^.3,Y^.4], pc,q in(.7Y,.8Y], all prime, gives an injection
of triples into(m,n=pc), because p is the unique lower prime factor.
PNT and partial summation yield cutoff-independent mass f0Y²/16000
summed over central even targets. The PNT source is Tao Notes2(2014),
Cor39/Exercise40, not the excluded Notes7 proposition.

The normalization is paid exactly: sum_(m even<=2Y)S_2(m)<=2Y.
Expand the positive odd-squarefree divisor series and use
(1-1/(ell-1)^2)(1+1/[ell(ell-2)])=1. A common nonnegative lower mass
W_Y(m), independent of lambda, then supplies the SAME pigeonholed m
for every cutoff. No numerical onset or assertion about every target.

This disproves a uniform o(Y S_2(m)) bound for the FULL ABSOLUTE method
in this setup, even after combining all terms at each integer. It does
NOT bound the absolute value of the signed total. The selected component
is negative in that total, and other components can compensate it. No
Goldbach counterexample or new coverage follows. Preserve the successful
polynomial/affine box estimate for narrow bands and error disposal, all
TI/identity tools, balanced projection and actual-zero conditional coverage.
Revisit absolute arguments only on restricted ranges or after a genuinely
different comparison; changing normalized cutoff shape cannot evade this.

Started14:11:13 UTC, reassessed14:21:20 UTC, changed-under-evidence.
Six exact guards pass normal0.003s/-O0.003s. Sol theory/actual-file PASS,
no correction. The Y1000,p13,c59,q769,m1536 fixture checks only exact
geometry and coefficients; it is not a PNT-onset or cancellation experiment.

Next concrete arithmetic test: can a beyond-half prime-AP distribution
theorem control the ACTUAL signed divisor expansion with moduli p*d,
prime p, the retained Mobius/polynomial d weight, and residue m~Y?
Check a primary theorem's moving-residue uniformity, factor-size domain,
coefficient norms, noncoprime residues and full error budget before use.
An MPZ/factorable-moduli label alone does not supply pointwise Goldbach
input. A hypothesis mismatch is the falsifier; a verified matching range
would be new signed arithmetic input. No such application is established.
Start a fresh <=30-minute clock. Goal active; no process is left running
at this checkpoint.

## Preceding pursuit: polynomial cutoff paired with an actual affine majorant

**c19cb24**, polynomial_joint_majorant.py, chooses the exact cutoff
lambda(d)=mu(d)(1-log d/logV)_+^k, fixed k>=9, U=V=floorY^(gamma/2).
The full cutoff-change compensation is TI-small by02e1627. Mellin inversion
and its finite divisor Euler product prove |S_lambda(c)|<<H_V(c)/logV.
These are the CORRECTED radical H majorants, including on prime powers.
The existing |Gamma_S|<<H_S and the explicit bound
H_S(ell^j)>=(511/1152)min(logell,logS) give |E|<<_(delta,G)H_S.

For fixed prime p not dividing m, apply corrected Henriot NEWThm5 to
c and m-pc. The product is primitive, normO(Y), discriminantm^2.
On any fixed cofactor-exponent interval1/4<c0<=c1<1-gamma/2, source
alpha1/2, eta1/4, epsilon1/2000 have strict uniform margins. The
physical set has a CLOSED enclosure, not a fixed half-open identity;
two comparable half-open intervals cover it with positive polynomial
values. This is the reviewer endpoint correction. At ell=p the second
form has no root: localK=1+a/p, rho1, and sieve ratio<=2. All other
local factors retain the corrected exact-valuation/common-root convention.

Henriot and the two finite second-moment integrals give
sum_c H_V(c)H_S(m-pc)<<C S_2(m)/(dV dS), with dR=logR/logC.
Hence sum_c |S_lambda(c)E(m-pc)|<<C S_2(m)/logY. Chebyshev over
one actual prime p-box gives the positive tuple bound
sum_(p,c in box) logp |S_lambda(c)F E(m-pc)|<<Y S_2(m)/logY.
Primes p|m are removed globally at costY^(1-gamma/2+2delta+o(1));
the earlier internal-power error is also paid globally. Arbitrary masks
are allowed in this positive box bound; the FULL TI transfer still needs
its fixed smooth physical F. No restricted old-hard-box equality follows.

Only O(1) cofactor boxes fit each prime box under pc~Y. Thus N boxes
costO(N Y S_2(m)/logY), with the saved global power errors. For N=o(logY)
this is small RELATIVE to Y S_2(m); a fixed polylogarithmic band around
sqrtY is controlled. A band of exponent widthh costsO((h+1/logY)Y S2)
with uniform constants in a fixed domain. The full positive-width range
has Theta(logY) boxes and only a main-scale bound. No new coverage.

Started13:54:01 UTC, reassessed14:09:07 UTC, progress. Eight guards pass
normal0.004s/-O0.003s. Sol theory/actual-file PASS after the endpoint
correction. The first test run also caught an unintended float endpoint;
both endpoints now stay Fraction and type guards preserve that fix.
No old experiment or blocked source fetch was repeated.

The next test, now proved indc7baa6 above, was whether the remaining
logarithmic accumulation is intrinsic
to the FULL ABSOLUTE method? On prime cofactors c>V, S_lambda(c)=1 for
every normalized cutoff. Count actual triples p*c+q=m with p,c,q prime
and p,c in interior size ranges. If their average over central even m is
of main order and E(q) stays positive, no uniform o(Y S2(m)) absolute
bound is possible. This would force a signed mechanism without rejecting
the useful box bound or polynomial tools. Check the fixed-small-delta
condition, actual prime counts, and singular-series average; do not use
heuristic independence. Fresh <=30-minute clock required. Goal active;
no research process is left running at this checkpoint.

## Preceding pursuit: exact cutoff freedom and the optimal cofactor norm budget

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
review PASS, no correction. The next test, now proved inc19cb24 above,
was whether a fixed degree>=9
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
Latest tests: `python -m unittest test_detector_gram_coercivity` (nine guards) and
the same with `python -O`; rerun only if changes or new concerns justify it.

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

## 2026-09-10: balanced Vaughan core reduces to Type-I obstruction

A fresh exact-scale test is recorded in `core_vaughan_type_i.py` with direct guards in `test_core_vaughan_type_i.py`. For gamma=1/2-epsilon and U=V=N^(gamma/2), the surviving exact Vaughan Type-II term has ab>N^gamma. Since gamma=499/1000 exceeds the core exponent 41/100, that term is empty on n<N^.41. This does not close the core: the remaining Type-I divisor has d<=V=N^.2495, while the reflected product p=N-d*k*m+r with companion m<N^.59 can have modulus dm as large as N^.8395, beyond BV's N^.5 level. Fixing d instead leaves the simultaneous prime conditions m and N-d*k*m+r. The exact four-term Vaughan identity was checked for n<=79, with its free convolution factor retained. Direct checks and py_compile pass; pytest is unavailable in this runtime. This is a scale limitation of the balanced Type-I route, not a barrier to other arithmetic input. The signed prime correlation below N^.41 remains open.

Correction after independent review: the Vaughan support calculation is only a diagnostic for a hypothetical Lambda(n_core) factor. The actual residual is a_B(n_core)*Lambda(m), so no Vaughan identity has been applied to the actual coefficient. Also m has exponent at least .59 because n_core*m is near N. Thus .8395 is a concrete top-block q=dm exponent (d=N^.2495,m=N^.59), not a worst-case upper bound; smaller n_core blocks can make m and q larger. The module and tests now state both limits explicitly. The route remains a limitation test, not a theorem about the actual residual.

## 2026-09-10: companion Vaughan ranges corrected and reviewed

Applying Vaughan to the actual long companion Lambda(m), rather than the hypothetical Lambda(n_core), gives the top core block m~N^.59. In the linear term, x=n*a ranges from exponents .41 through .6595 and the complementary free factor b ranges .3405 through .59, with x*b at exponent 1. In the Type-II term a,b each start at .2495 and reach .3405, while n*a and n*b start at .6595. These are necessary scale ranges only; no bilinear estimate is proved. Independent review corrected a prior double-counting of the split factor. Direct checks and py_compile pass.

## 2026-09-10: actual companion Vaughan pursuit dissolved

The proposed dispersion form does not exist after the already-paid power-small prime-only replacement. The actual companion m is prime and exceeds both Vaughan cutoffs. Evaluating the exact four-term identity at such a prime gives zero low, subtracted and Type-II terms; only the linear a=1 divisor remains and equals log m. Thus the tempting factor ranges in `companion_vaughan_scales.py` are hypothetical composite support, not factors available in the actual residual. Six exact guards pass normally and under `python -O`; independent review PASS. Curiosity status: `changed-under-evidence`. This limits companion Vaughan, not Vaughan elsewhere or bilinear methods with a new arithmetic decomposition. The signed prime correlation remains open.

Next bounded question: view k=N-p as an integer with its unique large prime factor m>N^.59 and cofactor n<N^.41. Test whether a Buchstab or Chen-style switching identity gives an actual one-sided estimate for the a_B(n) log(m) weight, rather than only re-deriving the completed full convolution or an upper-bound sieve. A parity obstruction or unsigned remainder is a falsifier.

## 2026-09-10: unique-large-prime switching is exact but signed

Commit pending at this note, `large_prime_switching_gate.py`. Since m>N^.59>sqrt(k) in the product window, the paid prime-only companion is unique. Switching therefore gives the exact log-prime coefficient a_B(k/m)log(m), and the n=1 term is exactly the desired prime atom. The composite-cofactor remainder is signed: if distinct primes p,q<=B satisfy B<pq, then a_B(pq)=1-1-1=-1. Such cofactors occur far inside n<N^.41 because B~N^.009. Therefore this coefficient cannot be inserted directly as a nonnegative Buchstab/Chen one-sided sieve weight. This does not obstruct a signed estimate, further decomposition, switching with compensating weights, or Goldbach.

Five exact tests pass normally and under `python -O`; independent review PASS. The first fixture was corrected because its proposed large cutoff did not satisfy P^2>k, then all guards passed. Curiosity status: `changed-under-evidence`. Python is available; SageMath, Mathematica/wolframscript, Lean/Lake and SymPy were not installed. No installation is currently justified because the bottleneck is analytic rather than computational.

Next bounded question: use the exact complement identity a_B(n)=-sum_(d|n,d>B)mu(d) for n>1 to expose the first omitted squarefree divisor. Test whether its forced factor structure supplies a modulus or averaging gain for the signed composite remainder. Preserve n=1 separately; an equally large signed boundary sum or uncontrolled divisor multiplicity falsifies the route.

## 2026-09-10: the near-3/5 source match is structurally excluded

`large_modulus_source_gate.py` checks Maynard arXiv:2006.07088v1, Definition 2 and Theorem 1.1. In the top core block, expanding d<=N^.009 and m~N^.59 gives q=dm<=N^.599, so the bare size condition Q<=x^(3/5-epsilon) has a .001 exponent margin. The theorem still does not apply. It fixes one residue a with constants depending on a, while the actual residue N+r varies with N and across the N^.1 shift family. More decisively, the q-support is not triply well-factorable: Definition 2 must work for the balanced split Q1=Q2=Q3=Q^(1/3), but q contains prime m~N^.59>Q^(1/3), so no supported qi can contain m and the convolution must vanish at q. The actual weight does not. Modulus/shift-dependent endpoint weights are also outside the statement; common fixed endpoints alone would not be a problem.

Three exact source-gate tests pass normally and optimized; independent source review PASS and supplied the exact balanced-factor obstruction. Status `changed-under-evidence`: the exponent coincidence is real but cannot be transferred through this theorem. This does not limit adaptations of its underlying spectral method or a different factorable majorant.

Next bounded question returns to the signed coefficient itself: can the complementary divisor identity for a_B expose a boundary layer whose weights are genuinely factorable enough for a large-modulus theorem, while the remainder is power-small? Test exact factorability and total mass before any source transfer.

## 2026-09-10: complementary divisor boundary preserves the sign problem

`short_divisor_complement_gate.py` proves exactly, for n>1,
`a_B(n)=-sum_(d|n,d>B)mu(d)`, and partitions every omitted squarefree d=pe by its unique largest prime p, with coefficient mu(e). This canonical expansion does not create nonnegative or factorable weights. In the top core block m~N^.59, d>B~N^.009 puts q=dm strictly above the exponent infimum .599; d may approach n~N^.41, so q may approach N. The inherited conductor-gap dispersion budget loses the power N^(.459-.41)=N^.049 at this boundary. The exact partition retains both negative a_B(15)=-1 and positive prime-cofactor weights.

Four tests over all 2<=n<100 and cutoffs2..12 pass normally and optimized. Independent review PASS after correcting the wording: .599 is an unattained infimum below 3/5, not a claim that every boundary modulus exceeds 3/5. Status `changed-under-evidence`. The factorability formulation is abandoned; cancellation among signed boundary layers remains possible.

Next bounded question: target the explicit N^.049 loss in the high-conductor dispersion estimate. Test whether retaining the signed d-boundary and the r-average before Cauchy yields an additional bilinear/Kloosterman saving, rather than taking absolute values across q and r. Preserve target-dependent residues, periodization and endpoints. A diagonal of size N^.049 or an unavailable spectral uniformity is the falsifier.

## 2026-09-10: shift-bandpass spectral target isolated

`shift_bandpass_target.py` connects the retained kernel identity `C0(s)=2pi int chi(t)^2 exp(i*s*t)dt`, with supp chi inside (1,2), to the explicit core dispersion loss. Poisson summation of the FULL periodized r-lattice modulo q excludes additive frequency zero exactly and localizes active frequencies at |h|~q/H. At q=N^.599 and H=N^.1, this is h=N^.499. If a NEW arithmetic estimate for the actual prime-progression discrepancy supplied square-root cancellation across the H shifts, it would change the existing exponent loss .049 to .049-.05=-.001, barely closing the top boundary.

This gain is conditional and is not supplied by kernel oscillation alone: an arbitrary discrepancy sequence can align with the bandpass and saturate Cauchy. Hard truncations or extra shift masks can leak zero frequency and require separate bounds. Four guards pass normally and optimized; independent review PASS. Curiosity status: `aha-candidate`, labeled new-to-this-task only. It connects the older bandpass completion and the newer conductor-dispersion loss, makes the quantitative N^-.001 prediction, and is falsified by a main-size diagonal/leakage or failure of arithmetic spectral cancellation.

Next bounded question: derive the exact additive-character form of the high-conductor prime discrepancy after inserting the full periodized C0 kernel. Keep the character conductor split, N+r phase, q=dm support and endpoints. Determine whether the h~q/H restriction removes or shrinks the NQ term in the existing variance; do not assume square-root cancellation.

## 2026-09-10: Fourier localization alone does not shrink variance

`shift_fourier_energy_gate.py` writes the exact finite Fourier budget for one modulus. The full periodized kernel has about q/H active modes, each of size O(H), so its total square mass is `(q/H)H^2=qH`, exactly the residue-space Parseval mass. Cauchy in frequency therefore reproduces the previous residue Cauchy bound. To gain H^-1/2 in the correlation, a NEW arithmetic theorem must show that the actual prime-discrepancy Fourier energy in the active band is at most H^-1 of its total energy. The generic large-sieve factor is length+q with length q/H=N^.499<q=N^.599, hence remains q-dominated and supplies no improvement.

Four exact guards pass normally and optimized; independent review PASS. Hard shift truncations, endpoint masks and other r-dependent weights spread the DFT, so leakage must be paid before using the full-lattice support. Status `changed-under-evidence`: the automatic bandpass-saving hypothesis is falsified, while the precise arithmetic band-energy target survives.

Next bounded question: test the most obvious arithmetic input on the dual band. Use the exact Gauss transform for high multiplicative characters and a Burgess short-character-sum budget at dual length q/H. Include the H/sqrt(q) transform factor and compare against the direct length-H trivial bound. Any exponent no smaller than H falsifies that route.

## 2026-09-10: direct dual Burgess plug-in loses

`dual_burgess_gate.py` retains the Gauss/Poisson factor H/sqrt(q) and the dual length L=q/H. Granting the prime-modulus Burgess shape gives transformed exponent
`E_r=h-q/2+(q-h)(1-1/r)+q(r+1)/(4r^2)`. At q=.599,h=.1, `4r^2(E_r-h)=(r-1)(.798r-.599)`, so every licensed integer r>=2 is worse than the direct length-H exponent. Specifically E_2=2597/16000=.1623125. Even granting a cost-free reduction to the prime component m=N^.59 gives E_2=257/1600=.160625>.1.

Five guards plus the prime-component check pass normally and optimized; independent review PASS. Source precision: Kerr--Shparlinski--Yau arXiv:1711.10582 refines r>2; r=2 uses the classical Burgess bound quoted there, and r=1 is only a Polya--Vinogradov/trivial endpoint comparison. A naive split into d residue classes costs more, but CRT/induced-character structure or genuinely bilinear d,m averaging remains open. Status `changed-under-evidence`: abandon direct one-character Burgess, preserve the band-energy target.

Next bounded question: keep d and m coupled in the Gauss-transformed band and derive the exact bilinear character sum. Test whether averaging over the short d<=N^.009 family can improve the prime-component benchmark without taking absolute values. The maximum possible d-average square-root gain N^.0045 is far smaller than the single-character r=2 deficit .060625, so success would require additional m or spectral cancellation; verify that budget before source hunting.

## 2026-09-10: short-divisor averaging cannot rescue Burgess

`short_divisor_average_gate.py` uses the most favorable direct benchmark: replace q=dm cost-free by its prime component m=N^.59 and optimize the licensed Burgess integers. The transformed exponent E_r is increasing for r>=1 because the derivative numerator `(3q/4-h)r-q/2` is positive already at r=1, so r=2 is optimal. Its deficit over the direct H exponent is `97/1600=.060625`. The entire d-family has exponent .009: square-root cancellation saves .0045 and leaves `449/8000=.056125`; even complete cancellation saves only .009 and leaves `413/8000=.051625`.

Four exact guards pass normally and optimized; independent review PASS. Status `changed-under-evidence`: d-averaging alone is abandoned for this Burgess route. This does not address joint d,m structure, bilinear cancellation in the primes, or spectral cancellation across target shifts.

Next bounded question: write the exact joint m,h form after the Gauss transform and compare it with a sourced bilinear Kloosterman/spectral estimate. The required gain is H^-1/2 in correlation, equivalently H^-1 in active-band energy. Reject any theorem that averages a fixed residue, loses the target N phase, or replaces the prime-dependent conductor by arbitrary moduli.

## 2026-09-10: exact joint CRT/Gauss band form

`joint_crt_band_form.py` retains the full periodized-kernel DFT convention. For q=dm, every high character factors as chi_d*chi_m with chi_m nonprincipal modulo prime m. The weighted shift transform is
`q^-1 sum_h What(h)e(-hN/q)G_q(conj(chi),h)`, and CRT factors the Gauss sum exactly into d and m components with inverse twists. The active signed frequency satisfies |h|~q/H=N^.499<m=N^.59, so m does not divide h and the prime-component Gauss factor has magnitude sqrt(m). If unsigned DFT indices lie near q, the signed representative gives the same nonzero residue modulo m.

Four exhaustive CRT/support guards pass normally and optimized; independent review PASS. The imprimitive d-Gauss factor, sums over high characters, target phase, endpoint/mask leakage and all spectral cancellation remain unpaid. Status `changed-under-evidence`: the joint phase exists and is now explicit, but it is not yet estimated.

Next bounded question: search for a primary bilinear Kloosterman or spectral large-sieve theorem matching the exact m,h phase and coefficient norms. Build a source gate before importing any exponent. The theorem must tolerate m prime near N^.59, h near N^.499, d<=N^.009, target N varying, and character-sum coefficients from primes; otherwise preserve the mismatch.

## 2026-09-10: the full high character family collapses exactly

`high_character_collapse.py` sums the complete high family before Cauchy.
For q=dm, reduced p,a, m prime and all characters modulo d paired with
nonprincipal characters modulo m, the normalized projector is exactly
`1_(p=a mod q)-(m-1)^-1*1_(p=a mod d)`. Equivalently, for c nonzero
modulo m,
`sum_(chi_m nonprincipal)chi_m(p)G_m(conj(chi_m),c)
 =(m-1)e_m(cp)+1`.

Thus the prime Gauss family reconstructs the already known full-minus-low
projector. It leaves an ordinary additive prime phase; character
orthogonality itself creates no Kloosterman sum and proves no saving.
Composite/imprimitive d-characters are included exactly. Endpoint and mask
leakage, max-prefix weights, target phases and every joint m,h estimate remain
unpaid. Five new exact guards, plus the four joint-CRT guards, pass normally
and optimized. Independent review PASS. Status `changed-under-evidence`:
the direct Kloosterman source hunt was one transformation too early.

Next bounded question: retain the ordinary additive prime sums after this
collapse and test their joint frequency spacing as m and active
|h|~dm/H vary. Can an additive large-sieve/dispersion estimate put at most
H^-1 of the prime Fourier energy in the active band, including the low
subtraction, target phase, endpoints and masks? A diagonal or near-collision
family of full size falsifies this route. Do not infer the needed saving from
the mean-zero projector alone.

## 2026-09-10: exact active-band inequality survives only for prime weights

`active_band_energy_conjecture.py` states one literal candidate energy input
for the critical block. Put H=floor(N^.1), B=floor(2N^.009),
M=floor(N^.59), q=dm, 1<=d<=B with mu(d)!=0, and M<m<=2M prime. For each m
allow a long interval J_m inside [N/8,7N/8], of length at least N/16. The
Fourier coefficient uses the exact target phase, prime coefficient log(p),
and high projector
`1_(p=a mod q)-(m-1)^-1*1_(p=a mod d)`. The energy measure is
`mu(d)^2*(log m)^2/q`, the Parseval weight matching the residue variance.

With signed frequency h_tilde, the CORRECT angular band is
`q/(2*pi*H)<|h_tilde|<q/(pi*H)`. The earlier q/H..2q/H literal band was
wrong under the saved C0 normalization and was corrected before commit. The
proposed inequality is
`E_band <= C*(log N)^20/H*E_all`. It would supply the required H^-1/2 only
after a separate lemma pays the actual shift-dependent endpoints, kernel
coefficients and mask leakage. That transfer is not proved.

The elementary arithmetic resonance cancels exactly. Since active
0<|h_tilde|<m, m does not divide h, and
`c_(dm)(h)/phi(dm)=-c_d(h)/(phi(d)*(m-1))`; the low-projector correction
contributes the opposite Ramanujan main, including when (h,d)>1.

The coefficient-uniform extension is exactly FALSE. For d=1 and one
coefficient per nonzero residue, choose c_p=e_m(h0*p) with h0 in the active
band. One mode then contains exactly `(m-2)/(m-1)` of the total energy, tending
to 1 instead of H^-1. This does not falsify the stated prime-log inequality:
its fixed positive coefficients have their uniform reduced-residue main
annihilated by the high projector. Six new guards and the preceding nine
identity/CRT guards pass normally and optimized. Independent review PASS
after the 2*pi correction. Status `changed-under-evidence`.

Next bounded question: expand the remaining fixed prime-log energy and test
the frequency-pair diagonal for h/(dm)-h'/(d'm'). Determine whether the
large prime factors force enough spacing after the exact Ramanujan main is
removed, or whether a near-collision family still has full large-sieve size.
Keep the long interval family and q^-1 Parseval weights; do not reintroduce
arbitrary chirp coefficients.

## 2026-09-10: large-prime frequencies are distinct but overcrowded

`active_frequency_spacing_gate.py` falsifies denominator spacing as the sole
proof of the active-band conjecture. It already fails with d=1. Restrict to
the exact rational subband `m/(6H)<h<m/(4H)`, which lies inside the corrected
angular band because 2*pi>6 and pi<4. Fractions h/m with distinct prime
denominators m are exactly distinct: equality would force m|h, impossible
for 0<h<m.

They are nevertheless too dense at the relevant resolution. PNT gives
`K asymp M^2/(H log M)=N^(1.08+o(1))` frequencies in an interval of length
1/(12H). Partitioning into width 1/(100N) cells forces a cluster of size
`>>M^2/(N log M)=N^(.18+o(1))`. After rephasing on a length-N interval, its
exponentials have pairwise phase drift at most 2*pi/100. The unweighted Gram
top eigenvalue is at least c*R*N for cluster size R. With the actual d=1
weight q^-1=m^-1 it is c*R*N/M versus single-frequency N/M, so the relative
crowding loss remains R. This .18 loss exceeds the desired .10 energy gain.

An exact finite shape check at N=120000,H=3,M=990 found 5414 distinct
frequencies and a width-1/N cell containing 10. Four guards pass normally
and optimized; independent review PASS after the weighted normalization was
made explicit. Status `changed-under-evidence`. This does NOT falsify the
fixed positive prime-log energy conjecture: its centered coefficients and
opposite-prime arithmetic may cancel a dense cluster. It does rule out a
generic coefficient large sieve based only on minimum spacing.

Next bounded question: use the fixed prime coefficient rather than frequency
geometry alone. Expand the centered prime exponential sum with a sourced
Vaughan/Heath--Brown identity in the p-variable and test the resulting Type I
and Type II exponent budgets across the dense m,h cluster. Preserve the exact
full-minus-low correction and long interval endpoints. A Type I modulus above
the licensed distribution level or a Type II diagonal of size N^.18 is the
falsifier.

## 2026-09-10: current pointwise prime bounds miss by N^.59 in energy

`prime_pointwise_band_gate.py` source-checks the opposite-prime exponential
sum. Maynard--Pandey--Radziwill arXiv:2608.14777v1, Theorem 1.1, gives
`X^(o(1))*(X/D^(1/2)+X^(19/24))` for a Dirichlet approximation denominator
q<=X^.5 and `D=max(q,qX|epsilon|)`. For the reduced exact rational h/m with
m=X^.59, the approximant cannot equal h/m. Rational separation forces
`qX|epsilon|>=X/m=X^.41`, hence the checked source gives pointwise exponent
`max(1-.41/2,19/24)=159/200=.795`. The interval J_m is a difference of two
prefix sums. Proper prime powers cost X^(.5+o(1)); the d=1 low correction is
X^.41 up to logs. Both are smaller.

There are X^(1.08+o(1)) active (m,h) pairs and energy weight m^-1=X^-.59.
Squaring and summing the source bound gives X^2.08. The existing d=1
all-frequency variance is X^1.59, so the required H^-1 band budget is X^1.49:
the pointwise route misses by X^.59. Classical Vaughan exponent .8 would give
X^2.09 and miss by X^.60. In general a pointwise exponent s reaches the target
only if s<=1/2 exactly. Thus averaging must precede absolute values.

Helfgott arXiv:1501.05438, equations (3.6)--(3.9), licenses applying Vaughan's
identity to the full Lambda sum. This creates Type I/II convolution sums for
analysis; it does not assign factors to an individual prime and does not
contradict the earlier pointwise companion warning. Five guards pass normally
and optimized; independent source/mathematical review PASS. Status
`changed-under-evidence`. The .795 result is preserved as a useful component,
but pointwise estimation is abandoned for the active-band energy target.

Next bounded question: choose explicit Vaughan cutoffs U=V=X^u and average
each Type I/II piece over the d=1 family m~X^.59 and the actual angular h-band
BEFORE triangle or pointwise bounds. First test whether complete-period
cancellation pays Type I for some u; then compute the Type II congruence
diagonal. Any remaining exponent above X^1.49 falsifies that cutoff.

## 2026-09-10: Vaughan Type I pieces fit the full active-band budget

`prime_band_vaughan_type_i.py` proves the Type I pieces affordable against
the application-level absolute energy benchmark, now retaining the entire
`d<=B` family. Twist the exact Vaughan identity by the completely
multiplicative coprimality mask `f_q(n)=1_((n,q)=1)` and take
`U=V=N^(3/40)`. For each fixed short factor, the full-minus-low kernel has
zero mean on a complete unit-residue period whenever `m` does not divide the
active frequency. Unit progression sums of `1` differ by at most one, and
those of `log` differ by `O(log N)`, uniformly in both hard endpoints.
Parseval therefore gives `O(q^2)` or `O(q^2 log^2 N)` full-frequency energy
before Cauchy over the actual short factors.

After the exact outer weight and sums over `d,m`, the linear Type I exponent
is `1.348`; the grouped `mu_<=V*Lambda_<=U*1` exponent is `1.498`. The full
absolute `H^-1` benchmark is `1.499`, so the harder piece has margin `.001`.
Proper prime powers reach exponent `1.499` with only logarithmic losses. This
does not prove the stronger relative `E_band<=L^20 E_all/H` statement when
`E_all` is smaller, and it does not pay endpoint/kernel transfer.

The surviving exact question is equation (18): prove energy at most
`N^(1.499+o(1))` for the retained Type II term
`mu_>V*Lambda_>U*1`, with `a>V`, `B_U(b)=sum_(r|b,r>U)Lambda(r)`, both
coprimality masks, every `d,m,h`, and every hard interval. Its literal tuple
diagonal is at the target scale up to divisor/log factors; the signed
off-diagonal congruences remain open. Five guards pass normally and optimized.
Independent review PASS after clarifying the absolute-versus-relative scope.
Status `progress`. Polynomial and projector components are retained.

A sharper exact specialization sets `U=1`, `V=N^(3/20)`. Since
`Lambda_<=1=0`, the low and grouped subtraction terms vanish identically,
the single Type I term remains at exponent `1.498`, and the remainder is
exactly `mu_>V*log`, with both coprimality masks. This is now the narrowest
target; the balanced `B_U` form remains available. A finite double-precision
stress test at `N=200000`, `H=3`, all 171 primes `m` in the computed block,
and `d=1,2` measured band/all ratio `.104735`, near the geometric
`1/(pi*H)=.106103`; no actual-coefficient resonance appeared. The feasible
cutoff was only `V=6`, so this is diagnostic rather than asymptotic evidence.
Six guards pass normally and optimized; independent review PASS.

Next bounded question: for the exact `mu_>V*log` tail, use multiplicative
characters modulo the large prime `m` on a separated dyadic product box.
The h-band has length `m/H`; its character-ratio diagonal should give exactly
the desired `H^-1`, while off-diagonal short character sums encode possible
reinforcement. Determine the precise weighted covariance and whether a
second-moment bound saves the remaining square root. Keep product endpoints,
the d-component, and the distinction between a model box and the full sum.

## 2026-09-10: exact Mobius-band character covariance

`mobius_band_character_covariance.py` answers the mechanism question on a
separated d=1 product box. For nonzero h modulo prime m, the centered additive
kernel is exactly the sum over nonprincipal multiplicative characters. If
`A(chi),B(chi)` are the two factor transforms and
`c_chi=m^(-1/2)G(conj(chi),-1)A(chi)B(chi)`, then the band energy is

`m/(m-1)^2 * sum_eta W_m(eta) C_m(eta)`,

where `W_m(eta)=sum_(h in active band)eta(h)` and
`C_m(eta)=sum_chi c_(eta*chi)conj(c_chi)`. The principal eta diagonal is
exactly `m*R_m/(m-1)^2 sum|A(chi)B(chi)|^2`, with
`R_m=m/(pi H)+O(1)`: it already has the desired `H^-1` scale. Every possible
reinforcement or cancellation is confined to the signed nonprincipal
covariance. This is an arithmetic statement about the actual product
transforms; arbitrary character coefficients can still resonate.

The exact sufficient model-box inequality is equation (10), which keeps the
prime-m sum signed before absolute value. Character orthogonality gives the
exact second moment of `W_m`, but Cauchy alone treats `W_m` and `C_m`
adversarially and does not supply `H^-1`. Three finite-field identity guards
pass normally and optimized; independent review PASS on Gauss signs,
conjugations, covariance indexing and normalization. Status `aha-candidate`,
new-to-this-task. Hard hyperbolic endpoints and d>1 CRT remain outside this
model identity, and the signed covariance estimate is OPEN.

Next bounded question: source-check a hybrid or short-interval multiplicative
character large sieve against equation (10). Compute its exact exponent after
inserting the actual `A(chi)B(chi)` fourth/mixed moment. Success must bound the
SIGNED W-C covariance at H^-1 after the prime-m average; a bound only on W,
C, or their absolute product is insufficient. Reject the route if its large
sieve M^2 term reproduces the known frequency-crowding loss.

## 2026-09-10: asymptotic-large-sieve source gate and exact resonance

`mobius_covariance_source_gate.py` checks Conrey--Iwaniec--Soundararajan's
*Asymptotic Large Sieve* against the covariance. The exponent geometry is
close: with `Q=N^.59`, the product length is `Q^(100/59)<Q^2`, a balanced
factor is `Q^(50/59)<Q`, the Mobius cutoff is `Q^(15/59)<Q`, and the active
numerator length is `Q^(49/59)<Q`. But the published forms average smooth
all-moduli primitive-character boxes. They do not license prime-only moduli,
the modulus-dependent numerator band, linked character indices and Gauss
phase, the long `mu_>V` tail, or hard hyperbolic endpoints. The classical
large sieve retains its `Q^2` cost, and positive norm bounds cannot decide the
signed covariance. Independent source review PASS; one guard passes normally
and optimized. Status `changed-under-evidence`: preserve the direct-bilinear
architecture, but no sourced theorem closes the covariance.

`resonant_covariance_falsifier.py` now states the actual remaining inequality
with every floor, range, mask, kernel and coefficient: equation (6) is exactly
the `N^(1499/1000+epsilon)` target for `mu_>V*log` over all `d,m,h` and hard
interval families. A coefficient-uniform strengthening is false exactly. For
one prime m, choose an active h0, `alpha_a=e_m(h0*a)` on all nonzero residues,
and `beta_1=1`. Then `S(h0)=m(m-2)/(m-1)` and every other nonzero h has
`S(h)=-m/(m-1)`. If R is the active-band size, the signed off-diagonal ratio is

`OFF/E_all=(m-3)(m-1-R)/((m-2)(m-1))`,

which tends to one when `H` tends to infinity and `H=o(m)`. At `m=1009,H=5`,
the exact band ratio is `63382/63441=.999070...` and the positive OFF ratio is
`59354/63441=.935577...`. Thus linked conditions can reinforce almost
maximally for resonant coefficients. This does not falsify the actual target:
the resonance depends on m and h0 and is neither the shared Mobius coefficient
nor the hard Mobius--log hyperbola. Two guards pass normally and optimized;
independent review PASS. Curiosity status `changed-under-evidence`.

Next concrete question: expand the prime-modulus sum for the ACTUAL shared
`mu(a)log(b)` coefficients before any absolute value. Determine whether the
modulus average turns the nonprincipal covariance into a diagonal plus an
oscillatory Kloosterman/Ramanujan-type remainder. Success is an `H^-1` bound
with prime weights and the Gauss phase retained; a positive resonant diagonal
of full-energy size falsifies this route. Hard endpoints and d>1 remain named
transfer obligations. Overall goal active; no process is claimed running.

## 2026-09-10: actual covariance is a mean-zero additive energy excess

`mobius_covariance_additive_kernel.py` completes the proposed expansion for
the d=1 hard interval. Collapse the tail exactly to
`r_V(n)=sum_(a|n,a>V)mu(a)log(n/a)` and let `F_m(x)` be its sum in nonzero
residue x over the literal J_m. Undoing the character/Gauss expansion gives a
centered additive Dirichlet kernel, not a Kloosterman phase. Its literal raw
residue diagonal has trace zero and pointwise size `O(H^-1)`; no positive
full-energy diagonal survives.

More cleanly, put `delta_m(x)=F_m(x)-average_x F_m(x)`. The centered projector
annihilates the average exactly, so

`S_m(h)=sum_x delta_m(x)e_m(-h*x)`

and

`OFF_m=sum_(h in I_m)|delta_hat_m(h)|^2
       -R_m*m/(m-1) sum_x|delta_m(x)|^2`.

Thus OFF is exactly the actual residue discrepancy's excess active-band energy
above the uniform fraction `R_m/(m-1)` of its full Fourier energy. This is the
narrowest d=1 formulation; it retains every hard endpoint and fixed arithmetic
coefficient. It proves no spectral saving.

`mobius_covariance_lag_probe.py` reproduces a new finite decomposition at
`N=200000,H=3,V=6`, all 171 primes. Weighted aggregate OFF is `-3.85508e7`,
while the raw literal residue diagonal is only `-6.44318e2`. Before exact mean
removal, the W off-diagonal is `-1.90631e10` and the centering correction is
`+1.90245e10`; the first two lag lobes are `+5.59840e10` and `-7.34683e10`.
This rejects dropping later lobes or triangle-bounding raw pieces at this
tested scale only. It is tiny-cutoff floating evidence, not an asymptotic
claim. Six new guards, and 18 related guards in total, pass normally and
optimized. Independent review PASS after narrowing two initial scope phrases.
Status `progress`.

Next concrete question: the target is uniform in every permissible J_m, while
the negative finite OFF used only the central interval. Scan admissible hard
windows for the actual coefficient and let each prime modulus choose its most
reinforcing window. Test whether aggregate nonpositivity survives, or whether
only an `O(H^-1)` magnitude conjecture remains plausible. A positive aggregate
or an OFF/DIAG ratio growing under endpoint choice falsifies the sign mechanism,
but not the stated energy inequality. Overall goal active; no process running.

## 2026-09-10: endpoint choice falsifies uniform negativity, not magnitude

`mobius_covariance_endpoint_probe.py` scans all 276 intervals with endpoints
on the N/32 grid in `[N/8,7N/8]` and length at least N/16. It retains the exact
`mu_>V*log` coefficient, residue-zero mask, active modes and `(log m)^2/m`
weight. Every common grid interval had negative aggregate OFF at all tested
scales. But the actual theorem permits J_m to depend on m; selecting each
prime's most reinforcing admissible grid interval gives:

`N=32000,H=2`: 62/68 positive choices, `OFF/DIAG=+.138274`;
`N=200000,H=3`: 157/171 positive choices, `OFF/DIAG=+.116086`;
`N=1200000,H=4`: 374/444 positive choices, `OFF/DIAG=+.059999`.

Thus aggregate nonpositivity is not a valid finite uniform-family mechanism.
The magnitude target survives: the adversarial positive excess is still a
small fraction of the natural diagonal, individual ratios remain bounded in
these runs, and three tiny cutoffs `V=4,6,8` establish no asymptotic trend.
The N=200000 common ratios range `-.293706..-.031212`; the full interval
reproduces `-.041560`. One guard passes normally/optimized. Independent review
PASS with an independent N=32000 reproduction and prior N=200000 reproduction.
Status `changed-under-evidence`: abandon a sign proof uniform in J_m, retain
the signed magnitude estimate.

Next concrete question: remove endpoint choice analytically rather than hoping
for a sign. Because the mean-zero projection is linear in the interval
coefficient, test an exact dyadic decomposition of every J_m. Determine whether
Cauchy costs only `O(log^2 N)` and reduces the theorem to single dyadic blocks
without altering the `H^-1` target. Any modulus-dependent block count or mean
term causing a power loss falsifies this reduction. If it passes, source-test
the resulting fixed-block Mobius bilinear form. Overall goal active; no process
is claimed running.

## 2026-09-10: arbitrary endpoints reduce to dyadic selectors at log cost

`mobius_covariance_dyadic_reduction.py` proves a deterministic endpoint
reduction. Every integer interval `J=(L,R]` has a maximal aligned dyadic
partition with at most two blocks of each length and at most
`K=2ceil(log_2(N+1))` blocks. The exact tail sum is linear in `1_J`; for d=1,
the residue vector, its mean and the mean-zero discrepancy are also linear.
Thus no new mean term appears when blocks are recombined.

Cauchy costs one K inside each modulus. Grouping the at-most-two blocks at
each scale into selector families costs at most a second K. Consequently a
uniform `N^(1499/1000+epsilon)` estimate for every family selecting one aligned
length-`2^j` block per modulus implies the arbitrary-J_m estimate with only
`K^2`, absorbed after shrinking epsilon. Four exhaustive finite guards pass
normally and optimized; independent review PASS after clarifying that the
constant must be uniform over every scale/slot occurring at N. Status
`progress`: endpoint choice is no longer a power-scale obstruction.

The selector estimate remains OPEN. Locations may still depend on m; sharp
blocks are not smooth; unit-size boundary blocks remain; and no Mobius,
prime-modulus or d>1 cancellation was supplied. Next concrete question:
compute the unconditional Parseval/trivial budget for a selector of common
block length Y=2^j. Identify exactly which Y are already affordable against
`N^1.499`; only then spend arithmetic input on the surviving long scales.
Any collision factor moving the threshold below the derived value falsifies
the hoped-for pruning. Overall goal active; no process running.

## 2026-09-10: Parseval pays all dyadic blocks through exponent .7495

`mobius_covariance_dyadic_scale_gate.py` keeps the full `d<=B`, prime
`m~M`, `q=dm`, low-projector kernel, coprimality masks and outer
`mu(d)^2(log m)^2/q` weight. On a block of length Y the exact tail coefficient
has square mass `Y*N^o(1)`. Full-q Parseval and residue occupancy give

`sum_(h in B_q)|T_mu(h)|^2 <=4(Y+q)Y*N^o(1)`.

After the outer family is summed, uniformly in every modulus-dependent block
location,

`E_Y <=N^o(1)(Y^2+B*M*Y)`.

For `Y=N^y`, the exponents are `2y` and `y+599/1000`. Against the application
benchmark `1499/1000`, every `y<=1499/2000=.7495` is paid. At the endpoint the
collision term reaches 1.499, while the family term is only
`2697/2000=1.3485`, margin `301/2000=.1505`. The prior dyadic recombination
cost is logarithmic and absorbed. Three guards pass normally/optimized;
independent review PASS. Status `progress`.

Only dyadic lengths `N^.7495<Y<=3N/4` remain. The estimate supplies no H gain
there: its `Y^2` collision term is too large. Next concrete question: split
the exact `mu_>V*log` convolution on one surviving long n-block by the Mobius
factor exponent alpha. Preserve the three natural regimes
`.15<alpha<=.41`, `.41<alpha<.59`, and `alpha>=.59`, determined by whether
the two factors lie below or above the prime modulus. Compute a separate
energy budget and falsifier for each before choosing a source theorem. Goal
active; no process running.

## 2026-09-10: factor-by-factor Cauchy fails every surviving long block

`mobius_long_block_factor_gate.py` splits the exact `mu_>V*log` convolution
on `Y=N^y`, `y>.7495`, by Mobius-factor scale `A=N^alpha`. The exponent
regimes are lower `.15<alpha<=.41` (log factor above m), balanced
`.41<alpha<.59` (both factors below m), and upper `alpha>=.59` (Mobius factor
above m). Fixed-gap statements require epsilon slack at `.41,.59`.

Choose the shorter factor `Z=N^s`, `s=min(alpha,1-alpha)<=.5`, as the outer
Cauchy variable. Because `Z<Y`, the other factor has `O(Y/Z)` values for each
outer value. Parseval, residue collisions and Cauchy give per q
`N^o(1)(Y^2+ZqY)`; after the exact outer family this is

`N^o(1)(Y^2+ZBMY)`, exponent `max(2y,y+s+.599)`.

The family term fits only for `s<=.9-y`. The common collision term `2y`
exceeds 1.499 for every surviving `y>.7495`, independent of alpha. Thus the
best factor-by-factor Parseval/Cauchy route fails all three regimes; finer
alpha splitting cannot remove Y^2. This does not discard the factors or
polynomial identities: their signs or the m,h average must enter before
Cauchy. Four guards pass normally/optimized. Independent review first found
and then verified the correction that a generic fixed factor has
`O(Y/A+1)` inner values; the final proof uses only shorter `Z<Y`. Status
`changed-under-evidence`.

The balanced region still matches the superficial factor-support geometry of
the checked asymptotic large sieve, the lower region places short Mobius in a
mollifier-like orientation, and the upper long-Mobius region is least matched.
No local covariance theorem is supplied. Next concrete question: attack the
balanced `.41<alpha<.59` box first. Expand the signed prime-m average before
Cauchy and test whether the asymptotic-large-sieve diagonal architecture can
incorporate the active numerator band as a third short transform. A surviving
Q^2/positive-norm term falsifies this adaptation. Goal active; no process runs.

## 2026-09-10: factor covariance does not isolate the balanced box

`mobius_factor_covariance_probe.py` partitions the exact d=1 central tail into
`V<a<=floor(N^.41)`, `floor(N^.41)<a<M`, and `a>=M`, with
`M=floor(N^.59)`, then forms the full 3 by 3 principal and OFF covariance
matrices over all prime moduli. At `N=200000,H=3,V=6`, the component
`OFF/DIAG` ratios are `-.051785,+.006337,-.006914`; at
`N=1200000,H=4,V=8`, they are `-.035441,+.002394,+.005203`.

The balanced diagonal is close to uniform active-frequency allocation in both
finite tests and shows no resonance. This is only a clue: the sum of component
principal diagonals is `4.63` and `5.43` times the recombined total because the
factor ranges have large cross terms. Cross OFF changes sign between the two
scales. Therefore no componentwise positive theorem or omission of cross-regime
terms is licensed. The tiny V values also support no asymptotic trend claim.
The exact matrix recombination guard passes normally and optimized; independent
review reproduced both scales and PASSed after requiring the literal floor/M
boundary above. Status `progress`; the signed estimate remains OPEN.

Next concrete question: write the balanced factor contribution as an exact
three-variable transform in `(a,b,h)` before Cauchy, and source-gate a trilinear
finite-field estimate against its actual support and coefficient norms. A
surviving full-norm or modulus-family term above `N^1.499` is the falsifier.
Overall goal active; no process runs.

## 2026-09-10: finite-field trilinear black boxes lose the L2 band norm

`mobius_balanced_trilinear_source_gate.py` encodes one balanced d=1 block by
duality as the exact `(a,b,h)` sum with `mu(a)log(b)`, hard `ab in J`, and an
`l2`-normalized active-frequency coefficient. Petridis--Shparlinski
arXiv:1604.08469v4 Theorem 1.3 legally accepts the hard product condition in
its arbitrary pair weight. After the optimal relative endpoint localization,
its dual-norm exponent is at least `.405625` WORSE than the existing Parseval
exponent y. Theorem 1.1, even with a cost-free separation of the hard endpoint
that it does not supply, remains at least `.265` worse.

Macourt--Petridis--Shkredov--Shparlinski arXiv:2003.03493v1 Theorem 6.1 has
the checked `47/52` improvement only when the two smaller supports are at most
`p^.5`; where applicable both of its terms remain more than `.4` worse than
Parseval. These sup-norm theorems do not use `||gamma||_2=1`. Wright
arXiv:2608.27732v1 Theorem 2.2 also misses the range: it requires
`Q<=N_factor*X^-epsilon`, but `Q=N^.59` is strictly longer than either
balanced factor. Its fixed-residue L1 discrepancy is also not the current
Fourier-band L2 statement.

The exact low-projector rank term is separately paid by
`N^(y+.245-.59+o(1))=N^(y-.345+o(1))<=N^.655`, below the dual target `.7495`.
Four exponent guards pass normally and optimized; independent primary-source
review PASS. Status `changed-under-evidence`. This rejects direct use of these
black boxes, not an L2-sensitive trilinear theorem using Mobius signs or the
prime-modulus average. The exact pair-weight encoding and paid rank term remain.

Next concrete question: test whether lowering the prime-companion exponent
from `.59` can enter a sourced beyond-one-half convolution range while keeping
every earlier Type-I, proper-power, conductor-gap and overlap budget valid.
An unpaid old term or no common parameter interval falsifies this rebalancing.
Overall goal active; no process runs.

## 2026-09-10: prime-exponent rebalancing has no source-range intersection

`mobius_prime_exponent_rebalance_gate.py` varies the companion exponent `mu`
while retaining `b=.009`, shift exponent `.1`, and Mobius cutoff `.15`. The
active-band benchmark is `.909+mu`, the U=1 Type-I exponent is `.318+2mu`,
and their exact margin is `.591-mu`; lowering `.59` therefore preserves that
component. But the unpaid cofactor is strictly below `N^.46`, so the current
companion exponent is strictly above `.54`, with `.54` only an infimum.

For the favorable d=1 case, Wright arXiv:2608.27732v1 Theorem 2.2 requires
`34nu-17<mu<nu` for a convolution factor exponent `nu`. Such a `nu` exists
only if `mu<17/33=.51515...`, disjoint from the unpaid range. In a balanced
box both factor exponents are already below `mu`, directly reversing the
upper condition. Adding `d` only lengthens the modulus. Classical BV with
the small divisor requires the strict margin `mu+.009<.5`, hence `mu<.491`.
Both source ranges lie inside companion regions already paid by the actual
large-cofactor/dispersion estimates.

Six exact guards pass normally and optimized; independent review first held
the result for strict BV and boundary wording, then PASSed the corrected
version. Status `changed-under-evidence`. Rebalancing within the unresolved
range is rejected as a way to invoke these sources. The Type-I margin and
factor components remain useful. Next concrete question: use the measured
3-by-3 factor covariance to test whether the actual all-factor vector follows
a stable low-energy eigendirection, or whether its cancellation is merely the
known convolution identity in finite-dimensional form. Instability across
scale or exact reduction to that identity is the falsifier. Goal active; no
process runs.

## 2026-09-10: factor eigentest finds identity geometry, not a new OFF mode

`mobius_factor_eigen_probe.py` diagonalizes the measured principal matrix D
and the generalized covariance problem O v=lambda D v for the lower,
balanced, and upper Mobius-factor components. The all-factor vector
e=(1,1,1) is close, in the natural unscaled component coordinates, to the
smallest-principal-energy vector: Euclidean cosines `.986820`, `.993335`, and
`.995139` at `N=32000,200000,1200000`. This is consistent with the exact
complementary convolution identity `mu_>V*log=Lambda-mu_<=V*log`; the identity
still supplies no active-band estimate.

The generalized OFF spectrum does not reveal a stable special cancellation
mode. The weight of e on the positive generalized eigenvalue moves from
`6.899%` to `30.438%` to `.011%`, while the direct OFF/principal ratios are
`-.060914`, `-.041560`, and `-.039048`. D-metric weights exactly reconstruct
those ratios. The Euclidean cosine is basis-scale dependent; the generalized
spectrum and reconstruction are the invariant checks. One guard passes
normally and optimized; independent review reproduced all three scales and
PASSed the algebra, identity, and scope. Status `changed-under-evidence`:
abandon a stable positive or special OFF eigendirection as the mechanism,
retain the finite principal-alignment clue and every factor component.

Next concrete question: the arbitrary-J_m target is a deliberately strong
sufficient theorem. Recover the interval family imposed by the actual
Goldbach transfer and test whether its dependence on m has enough structure
to average the signed active-band kernels before taking a supremum over
selectors. Free modulus-dependent endpoints or a surviving `N^.18` frequency
cluster falsify this refinement. The fixed Mobius covariance and signed
Goldbach correlation remain OPEN; no process runs.

## 2026-09-10: physical endpoints form aligned affine families

Tracing the arbitrary `J_m` surrogate back through the actual product transfer
recovers structure that the maximal-prefix estimate discarded. For a dyadic
cofactor block `A<n<=2A`, prime companion m and shift r, the conjugated prime
window is `(mA+r,2mA+r]`; the reflected integer window is
`(N-2mA+r-1,N-mA+r-1]`. After expanding `d|n`, write `n=d*l` and `q=dm`.
Exactly

`floor(A/d)+1 <= l <= floor(2A/d)`,

independent of m, and the primes are `q*l+r` or `N-q*l+r`. Thus both physical
endpoints are aligned to the same residue modulo q. Arbitrary independent
`J_m` locations are sufficient proof surrogates, not a necessary feature of
the original correlation. The exact smooth kernel and r-sum still have to be
retained; this observation does not supply their missing transfer.

`mobius_structured_endpoint_probe.py` tests the unchanged d=1
`mu_>V*log` coefficient on actual-shaped dyadic affine families. At N=32000,
all admissible `A=9..15` and shifts `r=-H,0,H` in both orientations have
negative aggregate OFF/DIAG, ranging `-.289474..-.009879`. At N=200000 all
`A=19..32` remain negative, `-.163491..-.000267`. At N=1200000 the default
block gives about `-.1569` conjugated and `-.1775` reflected. This sharply
contrasts with the earlier arbitrary-selector positive ratios
`.1383,.1161,.0600`, but the margin can approach zero and no asymptotic trend
or sign follows. The selected block is actual-shaped, not asserted to be a
literal finite detector block.

Two guards pass normally and optimized. Independent review PASSed the exact
endpoint conventions, d*l reduction, FFT normalization and surrogate scope,
and direct-summed the first N=32000 modulus to within `5e-8`. Curiosity status
`aha-candidate`, new-to-this-task: preserve q-aligned common progression
indices as a possible arithmetic ingredient; abandon arbitrary endpoint
selection as an assumed physical obstruction.

Next concrete question: derive the exact aligned `(d,m,l,r,h)` energy before
maximal-prefix Cauchy, with the Schwartz kernel and both reflected phases.
Test whether completing the r-transform first removes the `Y^2` collision or
the known `N^.18` frequency-cluster loss. Reduction to the same arbitrary
selector norm, or either full loss with unchanged coefficient, falsifies the
route. The signed Goldbach correlation remains OPEN; no process runs.

## 2026-09-10: aligned phases collapse, but Parseval keeps Y squared

`mobius_aligned_band_gate.py` retains `q=dm` and the exact full-minus-low
kernel on the physical progressions. For `p=q*l+r`, both phases reduce exactly
to functions of r; for `p=N-q*l+r`, both reduce to functions of `N+r`. The
long index l disappears, while any target phase remains common in l. Thus the
previous dense `h/m` frequencies should not be treated as unrelated length-N
exponentials before using the physical alignment.

This coordinate improvement alone supplies no saving. For
`F_q(r)=sum_(l in L)c_(l,r)`, full Parseval and Cauchy give

`sum_h |Fhat_q(h)|^2 = q sum_r |F_q(r)|^2
                      <= q*K sum_(r,l)|c_(l,r)|^2`.

With block length `Y=qK` and coefficient square mass `Y*N^o(1)`, the result is
still `Y^2*N^o(1)`. Its exponent `2y` crosses the target `1499/1000` at exactly
`y=1499/2000`; every surviving longer block remains unpaid. The normalized
low-projector term is no worse in power. Two guards pass normally/optimized;
independent review PASSed both phases, the target-phase scope, Parseval
normalization, low term and threshold, including an extra composite-d check.

Status `changed-under-evidence`: endpoint alignment and progression coordinates
remain an `aha-candidate`, but algebraic phase collapse is not the arithmetic
ingredient and does not remove the collision. Next concrete question: expand
the active-band energy of the actual `F_q(r)` into its l1=l2 diagonal and
l1!=l2 signed correlations before Cauchy, summed over the prime companion m.
The diagonal must fit the known H^-1 budget; a positive off-diagonal term of
`Y^2` size falsifies this route. Otherwise source-test an averaged shifted
Mobius/prime-correlation input matching the exact q-multiple shifts. The signed
Goldbach estimate remains OPEN; no process runs.

## 2026-09-10: aligned row correlations have opposing large signs

`mobius_aligned_covariance_probe.py` expands the exact d=1 aligned block
`J_m=(mA,2mA]` into rows
`C_l(r)=r_V(ml+r)`, `A<=l<2A`, `1<=r<m`. It evaluates the saved centered
active-band covariance bilinearly and separates the true point diagonal,
same-row nonpoint pairs, and ordered cross-row pairs. These three pieces
recombine exactly to total OFF.

Normalized by the total principal baseline, the measured splits are:

`N=32000,A=9`: point `+5.64e-7`, same-row `-2.990264`, cross-row `+2.761953`,
total `-.228310`;

`N=200000,A=19`: `+1.42e-7,-2.768728,+2.608294`, total `-.160433`;

`N=200000,A=30`: `+1.02e-8,-3.729491,+3.726097`, total `-.003395`;

`N=1200000,A=39`: `-1.05e-8,-4.886587,+4.729663`, total `-.156924`.

Thus the literal diagonal is harmless in these finite tests, but cross-row
correlations reinforce strongly rather than cancel. The modest total is a
delicate signed difference from the large negative same-row family. Taking
absolute values or proving separate component bounds loses the observed gain.
No persistent sign, trend or power estimate follows from these tiny H,V.

One guard passes normally/optimized. Independent review PASSed row indexing,
FFT convention, centered baseline, literal point formula and recombination;
it also matched a direct two-row residue-kernel calculation at N=32000,m=457.
Status `changed-under-evidence`: reject cancellation of every off-diagonal
family as the mechanism, preserve the intact row recombination.

Next concrete question: resolve the cross-row term by lag
`Delta=l2-l1`. Test whether its positive mass is confined to bounded Delta or
has an oscillatory tail that cancels before summing m. A broad same-sign tail
of principal size falsifies lag-local treatment. Keep the same-row negative
term beside it; do not claim that their finite cancellation is an estimate.
The signed Goldbach correlation remains OPEN; no process runs.

## 2026-09-10: reinforcing cross-row mass extends to long lags

`mobius_aligned_lag_probe.py` resolves the preceding d=1 cross-row term by
`Delta=l2-l1`.  It computes the exact real ordered contribution for every
`0<=Delta<A`; `Delta=0` is the complete same-row term, and all lags recombine
to the previously verified total covariance.

The positive cross-row mass is not confined near `Delta=1`.  The fraction of
that mass in the last half of the available positive lags is `.40049` for
`N=32000,A=9`, `.24194` for `N=200000,A=19`, `.24549` for
`N=200000,A=30`, and `.21012` for `N=1200000,A=39`.  A positive contribution
occurs as far as `Delta=A-2` in each run.  The total normalized cross-row terms
remain `2.761953,2.608294,3.726097,4.729663`, respectively.

This finite evidence falsifies a mechanism that discards all but a bounded
number of lags at these scales.  It establishes no asymptotic lower bound or
sign.  In the original integer coordinates, a lag contributes shifts
`q*Delta+(s-r)`, so the surviving family reaches macroscopic shifts rather
than a fixed-shift regime.  One guard passes normally and optimized.
Independent review PASSed the lag identity, row slices, centering, baseline and
scope, and matched the N=32000,m=457 direct Q-matrix sum to `1.5e-9` rounding.
Status `changed-under-evidence`.

Next concrete question: for one dyadic lag block `D<Delta<=2D`, can the exact
prime-weighted signed sum over `m` gain a factor `H^-1` from the fixed
Mobius--log coefficients while retaining `q*Delta+(s-r)`?  A resonant family
whose positive block contribution stays of principal size for growing `D`
falsifies that blockwise mechanism.  The fixed band inequality and signed
Goldbach correlation remain OPEN; no process runs.

## 2026-09-10: an exact dyadic-lag sublemma survives resonance testing

`mobius_dyadic_lag_gate.py` states one exact d=1 sublemma.  For the aligned
rows `Phi_(m,l)`, row energy `E_(m,l)`, and dyadic block
`D_j={2^j<=Delta<min(2^(j+1),A)}`, it defines the signed block covariance
`C_j` with every prime weight `(log m)^2/m`.  Its positive Cauchy scale is

`P_j=sum_m (log m)^2/m * rho_m * 2 sum_(Delta in D_j,l)
sqrt(E_(m,l)E_(m,l+Delta))`, where `rho_m=|I_m|/(m-1)`.

The proposed sublemma is `max(C_j,0)<=C_epsilon*N^epsilon*P_j`, uniformly in
`j` and every integer A for which all `J_m=(mA,2mA]` are admissible.  This is
an exact H^-1-scale statement relative to the coefficient-blind Cauchy bound.
Identical arbitrary resonant rows make `C_j/P_j` asymptotic to `1/rho_m`, so
the statement requires the fixed Mobius--log arithmetic.  Even if proved,
the same-row term and d>1 transfer remain separate obligations.

The measured signed ratios by increasing dyadic block are:

`N=32000,A=9,H=2`: `.56517,-.08626,-.00395,-.20842`;

`N=200000,A=19,H=3`: `.33922,.10709,-.05897,-.00498,.03086`;

`N=200000,A=30,H=3`: `.34099,.11155,-.05439,-.00887,.01364`;

`N=1200000,A=39,H=4`: `.30564,.12891,-.05906,-.00171,.01024,.00694`.

No tested block exceeds its H^-1 Cauchy budget, so the concrete sublemma
survives this finite falsification attempt.  The main sign pattern is shared
across essentially every prime modulus: at N=1200000 all 444 moduli are
positive on blocks 1 and 2--3, and all are negative on block 4--7.  Thus the
observed gain is internal cancellation across lags, not cancellation from the
prime-m average.  Tiny H,V and four blocks prove no uniform constant or trend.

Three guards pass normally and optimized.  Independent review PASSed the
annulus contract, FFT/energy identities, factor 2, dyadic partition, Cauchy
scale, resonance comparison, and per-modulus diagnostics; it independently
matched the m=457,Delta=1 ratio.  Status `progress`.

Next concrete question: Fourier-transform the l-autocorrelation identity.
Determine exactly which two-dimensional `(h,theta)` spectral region makes a
dyadic block positive, then test whether the actual Mobius--log array avoids
that region.  A tensor resonance concentrating in both active h and positive
dyadic multiplier arcs is the falsifier.  The signed Goldbach estimate remains
OPEN; no process runs.

## 2026-09-10: a second Fourier transform isolates the dangerous term

`mobius_lag_spectral_probe.py` exactly diagonalizes each dyadic l-lag block.
For any zero-padding length `L>=2A-1`, it defines

`Psi_m(k,h)=sum_(0<=u<A) Phi_(m,A+u)(h)e_L(-ku)`,

`G_m(k)=sum_(h in I_m)|Psi_m(k,h)|^2
-rho_m sum_(1<=h<m)|Psi_m(k,h)|^2`, and

`W_j(k)=2 sum_(Delta in D_j) cos(2*pi*k*Delta/L)`.

The exact identity is `C_j(m)=L^-1 sum_k W_j(k)G_m(k)`.  It holds for an
arbitrary complex row array, not only the Mobius data.

More usefully, split `C_j=D_j+O_j` into h inside and outside `I_m`, retaining
coefficients `1-rho_m` and `-rho_m`.  Pairwise Cauchy proves exactly
`max(O_j,0)<=P_j`, hence

`max(C_j,0)<=max(D_j,0)+P_j`.

Thus the outside-band contribution already has the required H^-1 coefficient.
The new arithmetic obligation is only
`max(D_j,0)<<_epsilon N^epsilon P_j`, the signed dyadic autocorrelation inside
the active h-band.  This does not pay the same-row term or d>1.

Normalized by `P_j`, the largest positive measured `D_j` is `.00296848` at
`N=32000,A=9`, `.01150376` at `N=200000,A=19`, `.01022114` at
`N=200000,A=30`, and `.00278596` at `N=1200000,A=39`.  In the positive total
blocks, nearly all measured covariance comes from the already-paid outside
term.  The active quantity is therefore much smaller in these runs, but H is
only 2--4 and this is not an asymptotic bound.

Two guards pass normally and optimized, including arbitrary complex arrays at
padding factors 2,5,11.  Independent review PASSed the no-alias threshold,
FFT signs, varying-rho aggregation, active/outside split, Cauchy reduction and
all four receipts.  Status `aha-candidate`, new-to-this-task.

Next concrete question: expand the remaining active `D_j` by dyadic Mobius
divisor ranges before taking absolute values.  Determine whether its smallness
comes from individually paid factor-diagonal blocks or signed interaction
between divisor ranges.  A positive diagonal block of principal size is the
falsifier.  Polynomial identities remain available as components.  The full
signed Goldbach estimate remains OPEN; no process runs.

## 2026-09-10: the active factor diagonal changes sign

`mobius_active_factor_probe.py` partitions every divisor `V<a<=N` into exact
dyadic bands and expands the remaining active term `D_j` bilinearly.  The
sum of the factor diagonal and all ordered cross-band entries exactly
reconstructs `D_j`.  The implementation computes the total from the summed
bands and each diagonal entry separately, avoiding an unnecessary quadratic
factor-matrix output.

Normalized by the same H^-1 Cauchy budget `P_j`, the lag-1 split is:

`N=32000,A=9`: diagonal `-.0793409`, cross `+.0823093`, total `+.00296848`;

`N=200000,A=19`: diagonal `+.0766459`, cross `-.0651421`, total `+.0115038`;

`N=200000,A=30`: diagonal `+.0767580`, cross `-.0665368`, total `+.0102211`;

`N=1200000,A=39`: diagonal `+.0287434`, cross `-.0259575`, total `+.00278596`.

Thus the factor diagonal is not sign-definite.  No positive diagonal is close
to principal size in these runs: the largest sum of positive aggregate
factor-band diagonals is `.08415*P_j`.  Other blocks can have much larger
negative diagonal and positive cross pieces; at N=200000,A=30,lags 4--7 they
are `-.374806` and `+.358400`.  The signed recombination still matters.

At N=200000,A=19 the first divisor band `(V,2V]=(6,12]` dominates several
diagonal signs: `+.066887` at lag 1, `-.167563` at lags 4--7, and `+.049600`
at lags 8--15.  This points to the near-cutoff divisor progression as the next
arithmetic object; it is finite evidence, not a dominance theorem.

Two guards pass normally and optimized.  Independent review PASSed exact band
coverage, tail reconstruction, linear centering, active coefficient, ordered
factor expansion, diagonal-only equivalence and normalization.  The original
full K^2 diagnostic was stopped as redundant after about five minutes; the
exact linear-cost N=1200000 run still took about four minutes, so N=200000 is
the routine factor-resolution ceiling.  No process remains.  Status
`changed-under-evidence`: reject a diagonal-sign proof, retain a possible
componentwise magnitude bound and the exact factor expansion.

Next concrete question: for the dominant near-cutoff band `V<a<=2V`, expand
its residue transform as arithmetic progressions in r.  Test whether the
geometric denominator `||h*a/m||` supplies the missing active-band saving
after the h and prime-m averages.  A positive-density set with
`||h*a/m||<<a/m` and principal-size weighted energy falsifies this mechanism.
Polynomial/logarithmic weights remain available through partial summation.
The same-row, d>1 and full signed Goldbach estimates remain OPEN.

## 2026-09-10: one-divisor active energy has a deterministic geometric saving

`near_cutoff_geometric_bound.py` proves an elementary lemma for
`m>a>=H>=2`, `(a,m)=1`, and the exact active band `I`.  With
`|x|_m=min(x mod m,(-x) mod m)` and `L=ceil(m/a)`, it proves

`sum_(h in I) min(L,m/(2|ha|_m))^2 <= 96m^2/(aH)`.

The proof counts `|ah-km|<=T` on the positive h interval, reflects it, and
sums dyadic residue-distance shells.  Partial summation retains the logarithmic
weight and the exact centered single-divisor row transform, giving

`sum_(h in I)|Phi_(a,m,l)(h)|^2
<=800mu(a)^2 log(N)^2 m^2/(aH)`

whenever the complete row lies in `1..N`.  This is a genuine H-scale saving
for each divisor progression and uses the polynomial/logarithmic weight by
partial summation rather than discarding it.

The exact finite average over prime m, squarefree `V<a<=2V`, and weight
`(log m)^2/m` has geometric-majorant energy divided by
`sum R_m ceil(m/a)` equal to `1.0375,2.0070,1.8940` at
`N=32000,200000,1200000`.  Relative to the pointwise-trivial
`sum R_m ceil(m/a)^2`, the ratios are `.00843,.00827,.00377`; saturated
resonant pairs occupy `.00620,.00628,.00261` of the respective samples.
These measurements agree with the proved scale but are not asymptotic data.

Three guards pass normally and optimized.  Independent review PASSed the
lattice count, constants 96 and 800, Abel summation, centered term, strict
ranges, phase, implementation and aggregate receipts.  Status `progress`,
new-to-this-task.

This lemma controls one a.  Cauchy across every `V<a<=2V` loses the divisor
band cardinality, so it does not yet bound the coherent factor band or D_j.
Next concrete question: test the exact cross-divisor quasi-orthogonality

`sum_(m,l) w_m ||sum_(V<a<=2V) mu(a)u_(a,m,l)||_(I_m)^2
<=N^epsilon sum_(m,l)w_m sum_a mu(a)^2||u_(a,m,l)||_(I_m)^2`.

A ratio growing proportionally to V, or a resonant Gram eigenvector aligned
with mu(a), falsifies this mechanism.  The l-lag, same-row, d>1 and full signed
Goldbach estimates remain OPEN; no process runs.

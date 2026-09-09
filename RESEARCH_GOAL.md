# Rill's chosen mathematical research goal

Owner: Kevin; lead: Rill (`agent.rill`). Purpose: preserve the self-chosen
goal and its evidence rules across continuation, instead of reviving an
expired deadline after a session boundary.

## Current authorization and objective

On 2026-09-08 Kevin removed the six-hour limit and asked what goal Rill
would choose. Rill chose: develop a new proof method for prime-pair coverage,
with Goldbach as the ultimate target. Seek rigorously certified families of
even integers and a composition theorem covering every sufficiently large
even integer. A finite independently checked remainder would then finish
Goldbach. No such universal coverage theorem has been established.

The research is open-ended, with no current wall-clock deadline. The first
observable milestone is a mathematically correct, independently checked
theorem with a bounded literature comparison. Call a result new-to-this-task
until its external novelty has actually been assessed. Historical recognition
is not a measurable promised outcome; prize money and realized earnings remain
zero. No spending, publication, contacts, or foreground input is authorized.

Kevin subsequently authorized Rill to adjust the goal as ideas develop, and
explicitly paused notes/manuscript preparation to concentrate on mathematics.
Do not resume publication packaging without fresh steering. Keep only the
minimal execution state and useful mathematical tests needed to continue.

Each hypothesis has a mechanism, prediction, falsifier, and bounded next
test. Stop or revise individual routes when their evidence warrants it.
An active goal flag, a saved plan, and a queued message are not evidence of
continuous execution. Preserve any execution gaps honestly. Do not mark the
overall goal achieved on the basis of finite verification or a partial theorem.

## First chosen question under the discretionary grant

Question: can an adaptive, target-only normalization make the aggregate
prime-pair certificate work for almost all blocks, while retaining a precise
description of what is still missing for every block?

Residues: exact Goldbach count prefixes recover prime locations
(`notes/count-bootstrap-proof.md`); truncated moments can lose enough
information to permit zero-survivor countermodels
(`notes/exclusion-moment-certificates.md`); the newly derived local-peak
theorem forces every fixed dynamic range of weights to fail on infinitely
many represented blocks (`notes/fixed-precision-weight-obstruction.md`).
These are connections from successive parts of this investigation. They
are not claimed as inspiration from an unrelated earlier project. Mark the
selection as potentially influenced by the current task (`recent-capture-risk`).

First action: derive an almost-all success theorem for the adaptive precision
rule from the checked global weighted mean-square theorem, explicitly handling
unweighted counts, rounding, fixed block length, and exceptional starts.
Initial pursuit budget: 30 minutes of mathematical reasoning/source checking,
at most one bounded reviewer follow-up, no new model installation, spending,
publication, or other external operations. This bounds the experiment, not
the overall research authorization. No compute-heavy range extension is needed.
Abandon or sleep this formulation if it requires an unproved pointwise
distribution assertion or fails the reviewer check; preserve the exact gap.
Do not disguise an almost-all statement as coverage of every named block.

The first question returned `changed-under-evidence`: the adaptive
almost-all theorem was proved and independently checked within its budget.
See `notes/adaptive-moment-almost-all.md`. The local-peak theorem and its
fixed-range obstruction are also checked. A bounded literature comparison
found older uses of the underlying mechanism; external novelty remains
unconfirmed. The next mathematical gap is control of the exceptional blocks,
with effective bounds or an amplification/composition argument that cannot
leave a hidden exceptional family behind.

Current mathematical state, 2026-09-08: the canonical parity-preserving
bootstrap is implemented at local commit 14c6b6c. Starting only from L(6)=1,
it generated the contiguous bound prefix through 20,000 and certified the
separate frozen 1,000-even block 1,002,000..1,003,998; the intervening gap
was not evaluated. The next analytic pursuit also returned
`changed-under-evidence`: an independently checked argument proves
L(N)>=M(N)/2 for all but O_a(X/log(X)^a) even N in [X,2X], for every fixed
a>0 and sufficiently large X. M is the full Goldbach singular-series main
term. The threshold is not numerical, and the exceptional set may be
nonempty. The mathematical argument and source prerequisites are retained
beside the implementation in `parity_bound_bootstrap.py`. No new manuscript
or historical-priority investigation was undertaken. The open target is
coverage of the exceptional family; parity propagation itself does not stall
when a lower bound fails to certify a target.

The next finite refinement reuses earlier numerical lower bounds as well as
their parities. For each residual q dividing N, it clips J(N/q)-2e_q at
the exact same-factor diagonal. The resulting recursive J satisfies
L<=J<=R<=G and the same parity, with no exact-count input. On the same frozen
block it strengthened 280 bounds, with maximum gain 582, but added no new
certifications. `evidence/parity-factor-refinement.json` records this run.
The proved total gain is at most N/(z+1)=O(N^(2/3)) and vanishes on powers
of two. This limits the correction's size; it does not prove that actual
exceptions exist or cannot be repaired. Cross-factor composite-pair control
remains the missing arithmetic step.

The shared-prime reduction now includes composites with different least
factors that share a larger prime. `shared_prime_correction.py` reduces every
such distinct pair to a unique prime divisor ell of N and smaller cofactor
target N/ell. Its lower-bound mode uses earlier numerical bounds; its exact
mode uses earlier parity-recovered prime flags and inspects at most two
smaller targets. Adding the exact correction to canonical L leaves precisely
the ordered coprime composite-pair loss below G. It replaces the same-factor
gain rather than being added on top of it. At N=234 it raises 28 to the exact
count30 by recovering 91+143 and its reflection. The remaining problem is
control of the coprime composite-pair contribution; no universal positivity
or historical-priority claim follows.

A bounded symmetry hypothesis was falsified: re-pairing a fixed four-prime
quartet cannot always transfer its coprime loss to a smaller target. Its
three targets U=ab+cd, V=ac+bd, W=ad+bc satisfy U>V>W, leaving W with no
smaller re-pairing. The smallest cubic-valid example has factors7,11,13,17
and targets262,278,298; all have cutoff6. At262 the actual counts are
L=15, shared correction0, G=17, so this is no Goldbach counterexample.
The algebra and minimality were independently checked, and a regression in
`test_shared_prime_correction.py` retains the falsifier. Finite witness reuse
remains valid; a useful descent must go beyond a fixed quartet's pairings.
This does not test a descent restricted to yet-unknown failed targets.

The quantitative exceptional-set pursuit produced a finite character-model
comparison, retained in `exceptional_character_model.py`. For a primitive real
character of conductor D>21, its prime-sign pair model P and the opposite-sign
semiprime model S satisfy P>=3S/5, uniformly in both bias weights in [0,1].
For powers of two and D>24, P>=2A/3, where A is the number of admissible
residue pairs. Consequently P-rho*S>=11A/90 for rho<=49/100 on that family.
The sign change itself follows from an exact multiplicative character
convolution. Sol independently checked the algebra, all conductor cases, and
the necessary small-conductor exclusions. These are model statements, not
prime-count estimates or coverage of previously uncomputed powers of two.
The bounded pursuit returned `changed-under-evidence`: a possible exceptional
character does not destroy this model margin. A power-saving exceptional-set
theorem for canonical L remains unproved. The relevant Grimmelt--Teravainen
Theorem 7.9 (arXiv:2508.16400v2) does not state the required approximation for
our rough-semiprime weight. The remaining step is to prove that approximation
and its convolution errors, with the correct opposite character sign and
errors relative to any suppressed main term. Historical priority was not
investigated, in accordance with Kevin's latest steering.

The next bounded pursuit closed two analytic prerequisites for the actual
rough-semiprime weight, retained in `rough_semiprime_character.py`. Applying
the source's prime-character estimate twice proves the uniform semiprime
character mean with the positive exceptional term. It includes prime squares,
arbitrary interval endpoints, and the inverse-kernel normalization on the
central half of the range. The argument is valid through power-sized moduli;
its character-mean accuracy at a fixed power is a small constant, not itself
a power saving. An elementary bilinear argument separately proves the
minor-arc Fourier bound Y*R^(-1/3), including the normalized weight. Parseval
then bounds the number of targets with minor contribution larger than
Y/log(Y)^3 by O(Y*R^(-1/2)). These proofs were independently checked by Sol.
This is a power saving for that error component only. The pursuit returned
`changed-under-evidence`; a full major-arc model with controlled errors and
the final convolution comparison remain unproved. No numerical onset or
additional Goldbach coverage follows from these prerequisites alone.

The major-arc pursuit uncovered and repaired a source-definition mismatch.
The literal squarefree-supported H_R of arXiv:2508.16400v2 vanishes at25,
while its Lemma4.11 kernel is at least2 there when R=2,r=1. The exact
identity Lambda_R,r(n)=Lambda_R,r(rad(n)) supplies the corrected majorant
H_R(rad(n)), with an implied constant depending on the smooth cutoff.
This local repair was independently checked; it is not a refutation of the
source's main theorem. No unproved mean estimate for the repair was imported.
The corrected majorant now supports a complete signed Heath--Brown Fourier
model for our normalized rough-semiprime weight. Its Fourier remainder is
O(Y*R^(-1/3)); the separate pointwise error is bounded by H_R(rad(n)) times
the checked character-mean accuracy. The proof handles endpoint strips and
takes the exceptional-zero alternative at level R^4. If its conductor is
larger than R^2, its model term is omitted but the exceptional error case is
retained. Sol checked the proof; `major_arc_kernel.py` and its focused tests
retain the result and source counterexample. The pursuit returned
`changed-under-evidence`. Replacement by a nonnegative rough-number model
and usable correlation bounds for the corrected majorant remain unproved.
The overall Goldbach coverage goal remains active.

The corrected-majorant pursuit closed its mean, second moment, and additive
correlation bounds. `radical_majorant_correlation.py` applies Henriot's New
Theorem 5 from the 2014 erratum, including its corrected zero-exponent
condition. For d=log(R)/log(Y), the central pair bound is
sum H_R(rad(n))*H_R(rad(m-n)) << Y*S_2(m)/d^2, uniformly in central even m.
The erratum's exact local factors give this square loss; the initially
considered sixth-power loss was unnecessary. The proof also bounds the
signed Fourier model's error pairings by e*(1+e)*Y*S_2(m)/d^2, where e is
the previously checked character-mean error. Its remaining Fourier pair
residual is at most Y/log(Y)^3 outside O(Y*R^(-1/2)) targets. Sol checked
the source application, norm bounds, convolution algebra, and exceptional
count. Four exact local-density tests passed normally and with Python -O.
The pursuit returned `changed-under-evidence`; no numerical onset, new
Goldbach coverage, or historical-priority claim follows. The remaining gap
is evaluation/comparison of the signed pair main terms with enough positive
margin, including control relative to any exceptionally suppressed term.
The overall Goldbach goal remains active; no wake was queued.

After Kevin flagged an interruption, the exact thread rollout and Git
history were checked. The last completed reviewed checkpoint is aca72fc;
the earlier bootstrap, almost-all theorem, and analytic prerequisites are
intact. The next root-derived candidate is in `signed_pair_main_term.py`.
It evaluates the signed pair main terms, derives a linear suppressed margin
for small exceptional conductors, and bounds an explicit large-conductor
gcd family by O(Y*R^(-1/8)). Six exact-arithmetic tests pass normally and
with Python -O, including active composite conductors and divisor-cover
overlaps. These are finite-algebra checks, not an analytic review.
The existing moment_bound_review handle initially reported pending_init
across repeated observations. It subsequently initialized and checked the
actual files, returning PASS for the coefficient identities, uniform tails,
linear suppressed margin, and large-conductor divisor bound. The result is
now promoted on that completed review, not on the earlier queued request.
No replacement reviewer or wake continuation was queued. Actual-prime
Fourier transfer and conversion to canonical L remain open. The next bounded
mathematical job is the prime-side Fourier transfer and the pair residual
relative to the now checked suppressed margin. The overall goal stays active;
the old native 9am wording remains superseded.

The prime-side transfer and dyadic composition are now proved and checked
by Sol in `prime_pair_transfer.py`. They give a power-saving exceptional
set for the ACTUAL canonical bound: for every sufficiently small fixed
delta>0, L(N)>0 for all but O_delta(X^(1-delta/8)) even N in [X,2X], for
sufficiently large X. The proof reuses the same R, character alternative,
and kernels on disjoint dyadic intervals, controls the pair residual
relative to the linear suppressed margin, and converts the weighted
comparison back to integer counts. Each canonical composite is already
a semiprime inside a single fixed larger semiprime set; the removed end
segments contain too few positions to erase the margin. Four finite tests
passed normally and with Python -O, including cross-interval pairs and
the direction of the weight conversion. The pursuit returned
`changed-under-evidence`. This improves the exceptional-set size for L>0;
it does not give the earlier half-main-term lower bound outside that smaller
set, eliminate all exceptional targets, supply a numerical exponent/onset,
or certify an uncomputed named interval. The next mathematical gap is
coverage or further arithmetic restriction of the remaining exception
family. No historical-priority search or wake queue was used. Overall
Goldbach coverage remains unresolved and the goal stays active.

The next bounded pursuit localized the small-conductor suppression.
For primitive quadratic D>24 let q be the product of p>=5 dividing D.
The finite model can have a vanishing margin only on F_D={B=0,C=-A},
an explicitly computed family contained in q|N and occupying at most24
residue classes modulo D. Outside it the model has a fixed positive margin;
inside it P=S=A*(1-u*v). Sol checked the lemma and its analytic transfer.
For the small-conductor case D<=R^(1/4), the actual canonical bound obeys
L(N)>>_delta Y/log(Y)^2 outside BOTH F_D and a separate
O_delta(Y*R^(-1/2)) Fourier-residual set. Inside F_D the previous suppressed
error count can also be capped by the exact arithmetic family's size.
`character_suppression.py` preserves the proof and exact residue/count
verifier; four focused tests passed normally and with Python -O.
The pursuit returned `changed-under-evidence`: it localizes one source
of suppression, while unstructured Fourier exceptions and the separate
large-conductor case remain. No universal coverage, named uncomputed target,
numerical onset, or historical-priority claim follows. No wake was queued;
the overall Goldbach goal remains active.

The monotone-cutoff pursuit removed the coarse large-conductor gcd cover.
Choose the already allowed smooth G additionally nonincreasing on its
positive argument, with 0<=G<=1. `monotone_euler_cutoff.py` proves
0<=U_D<=(5/2)*S_out uniformly, using positive/negative prime-factor
separation and elementary Euler-product bounds. This transfers the exact
family F_D to ALL active exceptional conductors: outside F_D and a separate
O_delta(Y*R^(-1/2)) Fourier-residual set, L(N)>>_delta Y/log(Y)^2.
The resulting total exceptional-size bound for L>0 is now
O_delta(X^(1-delta/4)); the earlier half-main-term guarantee is unchanged.
Sol checked the proof. Four focused tests passed normally and with Python
-O; an initial test normalization omitted a directly enumerated character
sign B=-1, and was corrected without changing the negative-cutoff witness.
The pursuit returned `changed-under-evidence`. The remaining gap is control
of the Fourier residual and the exact suppressed classes, not the discarded
coarse gcd cover. No numerical onset, universal coverage, publication work,
historical-priority search, or wake queue was introduced. Overall goal active.

The next pursuit tested the Fourier-only gap rather than increasing a range.
`reflection_fourier_gap.py` proves a new concentration statement for the
existing artificial reflection model: its centered Fourier supremum is
O(sqrt(H*log H)) with high probability. After prime-density scaling and
forcing a truthful prefix through B, the error is
O(sqrt(H)*log(H)^(3/2)+B*log H), yet the center remains missing while
every other central even sum is represented. The same retained-core event
allows every prescribed prefix simultaneously. This fixed-wheel baseline
permits prefix exceptions for primes dividing the wheel; it does not impose
full primality, a growing sieve, or the actual prime/semiprime dependency.
Sol checked the proof, including the whole-circle grid argument and matching.
Four tiny Fourier/moment tests passed normally and with Python -O; the old
frozen model run was not repeated. The pursuit returned
`changed-under-evidence`: norm/energy estimates of this quality alone cannot
force an isolated hole to spread or prove universal coverage. The actual
almost-all theorems remain intact. The next mathematical gap is direct
arithmetic control of the combined actual prime/composite pair residual,
including its behavior on the suppressed classes. No Goldbach counterexample,
historical-priority claim, publication work, or wake queue. Overall goal active.

The actual-survivor pursuit retained an exact signed identity and rejected
its first plug-in estimate. With A=P+C and Liouville lambda,
P-C=-lambda*A, including prime squares, and L=[(P-C)*A]+d_C=2[P*A]-[A*A]+d_C.
`factored_linear_barrier.py` tests the standard one-dimensional lower
linear sieve in this identity. Even granting the optimistic leading upper
bound [A*A]<=((1+log(u-1))^2+o(1))*K, its best limiting coefficient for
2<=u<=3 is -(1-log(u-1))^2< -121/1296. At u=3 it is -(1-log2)^2.
The source only applies at theta<1; theta=1 is a coefficient limit, not a
new distribution theorem. This is a failure of that specific certificate,
not an upper bound on actual L or an impossibility result for all sieves.
Sol checked the identity, normalization, and conditional boundary. Four
focused tests passed normally and with Python -O, with exact rational
logarithm enclosures and selected actual prime-square/diagonal controls.
The pursuit returned `changed-under-evidence`: keep the factorization for
coupled correlation or switching work; do not repeat the direct plug-in
without new arithmetic input. Actual Goldbach coverage remains unresolved.
No range extension, historical-priority search, publication work, or wake queue.

The next bounded pursuit connected the exact suppressed classes to an
existing pointwise theorem. `exceptional_pointwise_bridge.py` applies
Matomaki--Merikoski, IMRN2023, Theorem1.4: its leading coefficient is
exactly 1+C_D(N)/A_D(N), vanishes precisely on our F_D, and is at least2/3
elsewhere. For each fixed alpha in (0,1), assuming a primitive quadratic
zero beta=1-1/(eta*log D), D>24 and eta sufficiently large, EVERY even N
outside F_D in max(D^10,N0)..D^(eta^(1-alpha)) has actual
G(N)>=S_2(N)*N/(4*log(N)^2). No additional Fourier-residual exception is
needed in this conditional branch. Prime-power removal and the two
independent size thresholds are checked; no numerical onset is supplied.
Every power of two in that range is included. F_D is empty exactly for
the allowed conductors D=1 or5 mod12, giving whole conditional intervals.
Sol checked the deduction and implementation; four focused tests passed
normally and with Python -O. The pursuit returned `changed-under-evidence`:
this source-backed conditional branch bypasses a Fourier residual for G,
but neither proves the zero assumption nor improves canonical L on its
exceptions. The suppressed classes, absent/insufficient-zero case, and
out-of-range targets remain open. The source supplies the analytic theorem;
no historical novelty, unconditional coverage, publication work, or wake queue.
Overall Goldbach coverage remains unresolved and the goal stays active.

The next bounded pursuit checked whether that conditional branch can stack.
Landau--Page, in Michel's primary lecture source printed p21, implies that
distinct sufficiently strong primitive real zeros satisfy
log(D2)/log(D1)>c*eta1, for a fixed c below its positive absolute constant.
Consequently the next interval starts after the square of the previous
upper endpoint when 10*c*eta1^alpha>=2. A family above one sufficiently
large fixed strength threshold cannot cover all large evens by these
intervals alone, even if every suppressed residue family is empty.
`exceptional_pointwise_bridge.py` retains the proof and exact rational
separation check. Sol reviewed both; seven focused tests passed normally
and with Python -O. The review clarified that v=o(eta) suffices for the
geometric gap, while making the source error envelope tend to zero needs
the stronger v*log(eta)^6/eta=o(1). The pursuit returned
`changed-under-evidence`: individual conditional intervals remain usable,
but this strong-zero family cannot supply the desired global stacking.
These are certificate gaps, not Goldbach failures; weaker zeros and other
analytic regimes are not excluded. No numerical Landau--Page constant,
actual zero, historical novelty, publication work, or wake queue was added.
The overall goal remains active; other arithmetic coverage is still needed.

The next coupled-correlation pursuit tested a precise finite prerequisite.
`coupled_product_model.py` forces the second residue weight to be the exact
multiplicative convolution of the first with itself. For a half-support
whose prime-pair correlation at0 vanishes, the product-pair mean is at
least1/2 when the cyclic group order is divisible by4. When its order is
2 mod4, that mean is zero exactly at the two parity cosets; a quantitative
lower bound controls distance to these cosets. In prime residue fields,
these are the odd quadratic-residue/nonresidue cases. Thus product coupling
and bounded density alone still permit a negative signed comparison.
The m4 and m6 sharp examples, 510 exhaustive tiny subsets, and independent
finite-field product checks passed normally and with Python -O. Sol reviewed
the proof and implementation. The pursuit returned `changed-under-evidence`:
quadratic-character behavior is special, and a general product-coupling
argument requires more arithmetic input. This artificial model does not
impose actual integer factor windows, unique semiprime counting, a truthful
prime prefix, or the source prime-distribution estimates. It neither refutes
canonical L nor gives Goldbach counterexamples or new actual coverage.
No historical-priority search, publication work, or wake queue. Overall goal
active; actual coupled estimates remain the missing step.

The next pursuit proved a robust positive inverse statement in that model.
For any two possibly different cyclic densities f1,f2 in[0,2] with mean1,
the product distribution g=f1*f2 has reflected pair mean at least1/2
when4 divides the group order. Otherwise, a pair mean <=E0<1/2 forces
both factors within L1 distance 1-sqrt(1-E0)<=E0 of their respective odd
quadratic coset densities; neither a binary nor a missing-prime-sum premise
is needed. The inverse distance bound is sharp. If a bounded observed
weight w approximates g in L1 by epsilon, the same conclusion holds with
E0=pair_mean(w)+4*epsilon. `coupled_product_model.py` retains the proof and
general rational verifier. Sol checked both; eight tests passed normally
and with Python -O, including asymmetric/non-skew inputs and explicit
cap/error-budget falsifiers. The pursuit returned `changed-under-evidence`:
the quadratic structure test survives approximation, but applying it to
actual primes requires proving the density cap and a sufficiently small
product-distribution error at a relevant scale. Those arithmetic inputs
remain unproved; no new actual Goldbach coverage, historical-priority
search, publication work, or wake queue. Overall goal remains active.

The next pursuit checked the scale needed to apply that product model.
For prime ell>=7 and two unit-group densities in[0,2] with mean1, their
normalized multiplicative convolution g has additive pair mean at every
nonzero target at least (ell-4-sqrt(ell))/(ell-1)>0. The proof uses the
standard Jacobi-sum identities and the factor Fourier mass bound. However,
at the sufficient no-alias scale ell>2H, uniform atoms on earlier cofactor
primes<=H/(z+1) have mean L1 distance at least2z/(z+1)>=4/3 from EVERY
mean1 density capped at2. Thus the direct single-modulus application fails
its density premise before integer product windows need consideration.
`product_resolution.py` retains both deductions and exact rational checks.
Sol checked the mathematics and implementation; five focused tests passed
normally and with Python -O. The pursuit returned `changed-under-evidence`:
nonzero residue coverage is positive in the model, but that alone cannot
identify one exact integer sum. The sufficient no-alias modulus is not
claimed necessary; joint moduli, proved smoothing transfers, and certified
alias exclusion remain separate questions. No new actual Goldbach coverage,
historical-priority search, publication work, or wake queue. Overall goal
active; the arithmetic transfer to individual targets remains unresolved.

The next bounded pursuit checked multiple-modulus assembly and returned
`changed-under-evidence`. `joint_residue_model.py` gives an exact family
D=3Q where every proper-divisor joint projection is uniform and its pair
mean positive, yet the full product-pair mean is zero. Under those exact
projection and cap2 premises, a small full mean forces both factors close
to the full quadratic-character cosets; local projections erase that mode.
The construction uses nonunit targets and is not a coprime-target no-go.
For squarefree D with least prime p0>=7, ANY global cap2 mean1 factors
have positive product-pair mean at every unit target, bounded below by
theta*(p0-4-sqrt(p0))/(p0-2), theta=prod(p-2)/phi(D). This complementary
theorem needs no proper-projection uniformity. However, at the sufficient
no-alias scale D>2H, cubic-prefix prime atoms have distance from EVERY
global mean1 cap2 density greater than2*(1-2^(1/4)*H^(-1/12)), tending to2.
The elementary phi(D)>=D^(3/4) bound makes this valid even with many prime
moduli. Thus this direct atomic implementation still fails its required
global input; smaller marginal density bounds do not supply it. Sol checked
the deductions and implementation; seven focused tests passed normally
and with Python -O, including exact radical bounds, sharp inverse cases,
nonuniform composite marginals, and a lower-conductor premise falsifier.
The first test run caught and corrected floating division in test-side
coefficient arithmetic; the mathematical statement needed no correction.
The pursuit closed within30 minutes. No new actual Goldbach coverage,
historical-priority search, publication work, or wake queue. Overall goal
active; arithmetic control of joint dependence or another rigorously
justified transfer is still needed for individual unresolved targets.

The next arithmetic pursuit returned `changed-under-evidence` for the
unweighted cubic switching proposal. `switched_cubic_barrier.py` retains
the exact identity G=T-U, T=[P*A], U=[P*C], and separates distinct-factor
and prime-square contributions. This route needs no upper grant for M.
Using the primary switching formulas with the required distribution and
natural-mass hypotheses explicitly granted, the lower term has coefficient
B(theta1)<2log2 for every fixed theta1<1. The switched upper subtraction
has coefficient2*integral d alpha/[alpha*(1-alpha)*theta2(alpha)]>=2log2
on1/3..1/2 when theta2<=1. Thus this particular lower certificate cannot
give a positive leading term. At the formal two-level1 limit its coefficient
is exactly0; the source does not assert that endpoint or determine the
lower-order sign. Sol confirmed the normalization and emphasized charging
cutoff/factor-dividing-N exceptions O(N/z), separately from O(z) and
O(sqrt(N)) terms. The verifier preserves these finite terms. Four focused
tests passed normally and with Python -O; Sol reviewed the implementation.
The distribution grants remain grants, including after sequence removals;
position-error bounds do not prove weighted remainder estimates. No actual
negative G or L, no exclusion of other weights or coupled switching, and
no new Goldbach coverage follows. The pursuit closed within30 minutes;
no historical-priority search, publication work, or wake queue. Overall
goal active; a stronger joint arithmetic estimate is still needed.

The weighted cubic follow-up also returned `changed-under-evidence`.
For every fixed Lipschitz profile 0<=w<=1 supported in[1/3,b], b<=1/2,
the source-form additive distinct-prime-divisor weights have certificate
coefficient B_w-C_w<=B0(theta1)-2log2<0 for fixed theta1<1 under the same
explicit distribution/mass grants. At the formal two-level1 limit the
entire weight functional cancels exactly. This excludes positive leading
certificates only for this stated family and these sieve estimates; weights
can improve a weaker certificate at lower switched levels while it remains
negative. The inequality is uniform in profiles; analytic o(K) is only
claimed for each fixed Lipschitz profile with its granted remainders.
`switched_cubic_barrier.py` retains the deduction, rational piecewise-linear
integral enclosures, and the exact finite weighted certificate J_W<=G.
Its losses count small prime terms and negative composite weights; a prime
square's divisor counts once. Sol checked the deduction and actual verifier;
eight combined focused tests passed normally and with Python -O. This
pursuit closed within30 minutes. No new actual Goldbach coverage, numerical onset,
historical-priority search, publication work, or wake queue. Overall goal
active; these separate weighted estimates do not close the pointwise gap.

The next pursuit strengthened the ACTUAL canonical-L exceptional-set theorem.
Keeping the same sufficiently small fixed delta>0, every fixed 0<k<2/3
now gives #{even m in[X,2X]: L(m)<=0}=O_{delta,k}(X^(1-delta*k)).
For example k=1/2 replaces delta/4 by delta/2 for the same delta.
The additional established input is Siegel's ineffective zero-distance
bound, stated in Matomaki--Merikoski equation(6). The deduction is in
`monotone_euler_cutoff.py`: enlarge the full-Euler comparison range to
D<=R^a, a=1/3+k/2, retain the suppressed margin mu>>R^(-tau),
tau=1/6-k/4, and use the unsimplified Fourier energy. Both the small-D
Fourier residual and large-D arithmetic family cost O(YR^(-a)*log(Y)^2),
which is smaller than O(YR^(-k)) for each fixed k. This is unconditional
asymptotically but has ineffective constants and onset. It neither assumes
an actual exceptional zero exists nor uses the separate conditional
pointwise Goldbach theorem. No k=2/3 endpoint, numerical delta/onset,
half-main-term strengthening, or empty exceptional set is proved. Sol
checked the analytic deduction and actual proof text. The bounded pursuit
closed within30 minutes. No executable implementation changed;
syntax checks and four exact rational exponent controls also passed.
No new prime-range scan, historical-priority search, publication work,
or wake queue. Overall goal active; individual exceptional targets remain
the unresolved step.

The next finite pursuit implemented the existing square-root support
identity with the parity bootstrap in `support_exact_batch.py`. A fixed
z=708 for the SAME1000 evens1002000..1003998 leaves2042 composites, all
above half the last target, so G=[A*A]-2[A*C] is exact throughout the band.
Only canonical earlier bounds through2830 are needed, classifying odd
prime inputs through1415, instead of the prior20000-prefix cubic run.
Binary reflected-intersection counts replace wide packed multiplication;
the production route uses neither exact-count input nor a high prime square.
A,C still encode full primality information through earlier-factor arithmetic.
Every one of the1000 counts matched an independent ordinary-sieve/packed
prime-square control. Minimum ordered G is7925 at1002002 (M8399,AC237);
there were no zero targets. Complete production time was0.1106447s,
including0.0027641s input generation; independent full-square validation
was2.1423617s. The same-block ordinary-sieve/bitset reference was faster
at0.0559214s, so no superiority over that baseline is claimed. Four focused
tests passed normally and with Python -O, including complete small exact
counts, exhaustive small binary correlations, negative parity inputs,
diagonals, strict support boundaries and unsafe ranges. Sol checked the
mechanism, implementation and evidence. The pursuit closed within30 minutes.
`evidence/support-exact-batch.json` retains the exact counts for
future same-block comparisons. The gap between2830 and1002000 was not
computed; these separated outputs are not a contiguous count prefix.
No new support theorem, universal positivity, historical-priority search,
publication work, or wake queue. Overall research active; this improves
the finite checker, while the universal exceptional-target gap remains.

The next pursuit specified a composite-supported joint arithmetic target in
`composite_bilinear_bridge.py`. For N=2x and I=(x/2,x], compare Lambda(N-n)
with normalized roughness through exp(sqrt(log x)). Established BV and the
fundamental lemma give the stated averaged Type I estimate and the correct
singular-series prime-versus-rough main term, with uniform local factors,
nonreduced progressions, short-interval remainders and prime powers charged.
An explicitly UNPROVED Type II estimate for all divisor-bounded coefficients
in the stated factor range would then imply positive actual Goldbach counts
for every sufficiently large even N. A direct Vaughan decomposition reduces
the sufficient missing estimate further to one fixed-coefficient composite
correlation J_N=o(x); its definition and signs are retained in the verifier.
This is a precise reformulation of the remaining pointwise correlation, not
evidence that it is easier or has been proved. Sol checked the deduction and
actual files. Four focused exact-rational tests passed normally and with
Python -O, verifying the decomposition, prime-power retention, local residue
normalization and input boundaries; they do not prove an analytic estimate.
The pursuit returned `changed-under-evidence` within30 minutes. No new
Goldbach coverage, numerical onset, historical-priority search, publication
work or wake queue. Overall goal remains active; J_N=o(x) is unresolved.

The next pursuit audited that uncorrected J_N target and returned
`changed-under-evidence`. If primitive quadratic conductors D tend to
infinity with actual real-zero strengths eta tending to infinity, choose
N as the least multiple of2D at least D^12. The localized proof of
Matomaki--Merikoski, Sections2 and7, gives the same interval's pair mass
(b_D(N)/4+o(1))*S_2(N)*N. The source's varying smoothing family and its
transition-strip error are accounted for explicitly. Since b_D=1+chi(-1),
our existing TI/MAIN/Vaughan relation forces
J_N/(S_2(N)*N)=chi(-1)/4+o(1). Thus the universal uncorrected cancellation
target would also exclude every such hypothetical strong-zero sequence,
including characters with an empty suppression family. No actual zero or
failure of Goldbach is asserted. The deduction, exact residue witness and
six focused tests are in `composite_bilinear_bridge.py` and its test file;
tests passed normally and with Python -O, and Sol checked both mathematics
and actual files. The pursuit closed within30 minutes. The sufficient
implication remains valid, but the next pointwise approach must retain the
character contribution and bound the remaining error against a proved
positive margin. The corrected leading term alone still gives no positivity
on the suppression family. No new coverage, numerical onset, priority search,
publication work or wake queue. Overall research remains active.

The next pursuit returned `changed-under-evidence` with two linked results
in `periodic_character_comparison.py`. For a sufficiently small fixed rho,
an even modulus Q with exp(sqrt(logN))<=Q<=N^rho, and an actual exceptional
character D>24 dividing Q, the nonnegative comparison
b(t)=(Q/phiQ)*1_(t,Q)=1*(1-chi(t)*t^(beta-1)) has prime-versus-model mass
>>K*N*min(1,(1-beta)logN) on N/4<n<=N/2. Here K=Q*A/phiQ^2 and A is
the allowed residue count. Direct character expansion and Gallagher's
averaged estimate preserve the positive margin even in suppressed classes.
This is not a prime-versus-prime lower bound; the comparison includes composites.
However, ANY bounded mean-one Q-periodic model, also allowing a bounded
mean-zero periodic character correction times t^(beta-1), has Type I error
>>N/(logN*loglogN) when Q<=N^rho, rho<1, and amplitudes are N^o(1).
Primes near logN outside the factors of NQ give an exact density defect;
PNT counts enough such primes and summed BV controls actual progressions.
Thus the old Type I premise fails already at its A=2 saving for this model.
The earlier much larger primorial comparison is outside this obstruction.
Sol checked both deductions and the actual helpers/tests; four focused
tests passed normally and with Python -O. The pursuit closed within30 minutes.
No new coverage, actual zero detection, numerical onset, priority search,
publication work or wake queue. A useful next approach must retain the
character margin while repairing the arithmetic-distribution compatibility,
or control the specific signed decomposition without that absolute Type I
premise. Overall research remains active.

The next pursuit tested weighted pooling of the small wheel models and
returned `changed-under-evidence`. `wheel_mixture_obstruction.py` proves
that ANY finite mixture of normalized unit wheels Q_i<=N^sigma, sigma<1,
with real coefficients summing to1 and total variation<=C0*(logN)^B,
still has absolute Type I error >>N/((logN)^(B+1)*loglogN). There is no
bound on the component count or their combined least common multiple.
The statement also allows a common primitive character correction, with
one necessary prime-conductor exclusion handled explicitly. Weighted prime
coverage and a nonnegative test align the signed defects; negative mixture
coefficients are not treated as positive. Convex and bounded-variation
signed mixtures fail already at the A=2 saving. Positive model margins
are preserved only for nonnegative mixtures under the earlier common
actual-zero premises. Sol checked the proof and actual helpers; four focused
tests passed normally and with Python -O, including joint-period counts,
negative coefficients, repeated prime powers and the character exclusion.
The pursuit closed within30 minutes. Thus arbitrarily many easy models
of this stated kind do not repair the distribution mismatch. Specific
signed Vaughan cancellation, different residue weights or larger individual
models remain distinct possibilities. No new actual coverage, zero detection,
numerical onset, priority search, publication work or wake queue. Overall
research remains active; the exact earlier-output parity mechanism is intact.

The next pursuit returned `changed-under-evidence` with a constructive
two-scale signed comparison in `ramanujan_type_i.py`. Let S=Y^delta and
R=S^12, with sufficiently small fixed delta. For the common exceptional
alternative at level R^4, the unexceptional branch and the branch with an
actual primitive exceptional conductor 24<D<=S^(1/4) now have both:
an absolute Type I error O_A(Y/log(Y)^A) for every fixed A, and a pointwise
positive prime-versus-coarse-model mass >>Y*S_2(m)*mu throughout the stated
central band. Here mu=1 without an exceptional zero and
mu=min(1,(1-beta)log(Y)) otherwise. The Ramanujan progression means reproduce
the full reduced-residue density; the exceptional resonances are sparse
enough for the absolute estimate by ineffective Siegel bounds. Separating
the two scales bounds the fine Fourier residual against the coarse model
and preserves its linear character margin. The model is signed and includes
composites. The Type I error is not proved small relative to arbitrarily
suppressed mu, and neither a Type II bound nor actual prime-pair positivity
follows. Other exceptional-conductor regimes are outside this result.
Sol checked the theory and actual files, correcting one displayed scale
dependence to 1-beta<=kappa/(48*delta*log(Y)). Six focused tests passed
normally and with Python -O: complete progression periods, nonreduced and
prime-power moduli, whole-Dq character resonance, all four mixed-kernel
correlations, unequal cutoffs and input boundaries. These finite tests
verify algebra, not analytic estimates. The pursuit closed within30 minutes.
No new Goldbach coverage, numerical onset, zero detection, priority search,
publication work or wake queue. Overall research remains active; this repairs
two comparison prerequisites while retaining the precise transfer gap.

The next pursuit closed the character-relative Type I gap in the SAME
two-scale conductor regime. `relative_type_i.py` proves the stronger error
O_A(Y*mu/log(Y)^A) for every fixed A, with one sufficiently small fixed
delta chosen independently of A and an ineffective onset. Moderate mu uses
the earlier absolute estimate with a larger saving. For smaller mu,
quantitative Linnik estimates retain the zero-repulsion log(1/e) gain;
lifting small-conductor characters to lcm(D,r) removes the exceptional main
term without a totient loss. The Drappeau--Fiorilli high-conductor mean
estimate controls the complementary characters. Siegel bounds make the
model tails, periods, resonances and proper prime powers harmless relative
to mu. Sol checked the source use, proof and actual files. Four focused
exact tests passed normally and with Python -O, including a complex quartic
character control and the boundary where the exceptional projection survives.
The pursuit returned `changed-under-evidence` within30 minutes. Thus the
positive comparison mass and distribution error now share the required
scale in these branches. Type II and the specific signed prime-weighted
residual remain unproved; other exceptional-conductor regimes are still
outside this theorem. No new actual Goldbach coverage, numerical onset,
zero detection, priority search, publication work or wake queue. Overall
research remains active.

The next pursuit proved a conditional rare-sign candidate-pool theorem in
`rare_prime_sieve.py`. On the exact suppression classes F_D, allowed unit
pairs always have opposite character signs, and A/phi(D) is1 or1/2. Under
the stronger actual-zero condition 0<t=(1-beta)log(Y)<=1/log(Y), with
D<=Y^(delta/4), every central suppressed target has >>_delta Y*t/log(Y)^2
primes of sign+ whose reflected partners are coprime to D and have no prime
factor at most ceil(Y^(delta/u)), for sufficiently small fixed delta and
large fixed integer u. Quantitative Linnik progression errors, normalized
CRT counts and Ford's fundamental lemma keep the entire sieve remainder
small relative to the rare-prime population. Integer rounding and prime
powers are charged. The partners have fewer than u/delta prime factors
WITH MULTIPLICITY; they are not proved prime or P_2. Sol checked the theory
and actual files. Five exact tests passed normally and with Python -O.
A finite guard, D31,m2790,p1459,m-p=11^3, shows why the sign and roughness
conditions alone do not force primality; it asserts no exceptional zero.
For sign- composites, even total factor multiplicity requires a sign+
factor, whereas odd multiplicity can use only sign- factors. The remaining
question is control of composite partners within the proved candidate pool.
The pursuit returned `changed-under-evidence` within30 minutes. No actual
zero, numerical onset, new Goldbach coverage, priority search, publication
work or wake queue. Overall research remains active.

The rare-factor pruning pursuit in `rare_factor_pruning.py` keeps the SAME
conditional rare-prime pool and its conductor/zero hypotheses. With
w=floor(sqrt(E)), candidates whose partner has a sign+ prime factor
z<q<=w occupy only an o(1) fraction of that pool. An upper sieve on q|m-p
uses each all-squarefree remainder index qd at most once. Matomaki--Merikoski
Lemma2.2 bounds the reciprocal rare-prime sum by
O_(delta,u)(eta^(-2/u)+t+1/z)=o(1), preserving >>Y*t/log(Y)^2 candidates.
This is not an O(t) relative-loss claim. Even-factor composites with a
sign+ factor>w and odd-factor composites made entirely of sign- primes
remain uncontrolled. Sol checked the theory and actual files; five focused
exact tests passed normally and with Python -O. The pursuit returned
`changed-under-evidence` within30 minutes. No actual zero, numerical onset,
prime-partner theorem, new Goldbach coverage, priority search, publication
work or wake queue. Overall research remains active.

The next pursuit returned `changed-under-evidence`: the large-factor
cofactor switch still leaves an uncontrolled two-prime correlation, but
`character_partner_weight.py` gives a precise weighted reduction using the
standard W=chi*log. On a negative-sign squarefree partner, W is zero unless
there is exactly one negative prime r; then W=2^omega_+*log(r). On the SAME
pruned pool, its weighted sum T equals the positive-first actual prime-pair
mass P plus a nonnegative large-positive-factor squarefree term and a
nonnegative repeated-factor term. The latter is at most
Y^(1-delta/u+o(1))=o_A(Y*t/log(Y)^A) for every fixed A under the existing
hypotheses. This removes pure negative-sign odd composites from the weighted
equation, without claiming that they leave the candidate pool. A positive
lower bound for T AND control of the large-factor term remain unproved;
the known candidate count does not imply positivity of this new weight.
Sol checked theory and actual files; five symbolic algebra tests passed
normally and with Python -O. The pursuit closed within30 minutes. No new
Goldbach coverage, actual zero, numerical onset, priority search, publication
work or wake queue. Overall research remains active.

The next pursuit closed the h>=2 part of that squarefree composite error.
`multi_rare_partner.py` proves E_2plus<<_(delta,u)Y*S_2(m)*t^2=o(Y*t),
with ALL prior hypotheses unchanged. The existing cutoff w gives an
O(t) reciprocal sum of positive-sign primes above w. Henriot's corrected
New Theorem5 bounds the two affine prime conditions uniformly after fixing
the product M of positive factors, including primes dividing its leading
coefficient. The squarefree Euler tail of degree at least2 is O(t^2).
Consequently T=P+E_1+E_rem, with E_rem>=0 and E_rem=o(Y*t). The remaining
E_1 consists exactly of semiprime partners r*q, with r a negative-sign
prime and q a positive-sign prime>w, weighted by 2*log(p)*log(r).
This does not establish positivity of T or make E_1 negligible. Sol checked
the proof and actual files; five focused exact tests passed normally and
with Python -O. The finite cofactor control used target17,918 inside the
already certified prefix, adding no new coverage. The pursuit returned
`changed-under-evidence` within30 minutes. No actual zero, numerical onset,
priority search, publication work or wake queue. Overall research remains active.

The rare-sign distribution pursuit in `rare_twisted_bv.py` returned
`changed-under-evidence` within30 minutes. In the SAME actual-zero regime,
with delta sufficiently small for this fixed saving, it proves a relative
twisted Bombieri--Vinogradov error O(Y*t/log(Y)^6) through
Q=floor(Y^(9/20)/D^3). A three-way conductor split combines quantitative
Linnik, the aggregate corrected Gallagher estimate, and the induced-character
mean bound; transformed-principal resonance is explicitly charged. Using
the same injective sieve-remainder accounting raises the removable positive
factor cutoff to w*=floor(sqrt(floor(Q/3))). Its semiprime contribution is
O(Y*S_2(m)*t^2+Y*t/log(Y)^5)=o(Y*t). Consequently the SAME weighted total
now satisfies T=P+E_1(q>w*)+o(Y*t), with nonnegative discarded error.
Both positivity of T and control of the remaining large-q semiprimes remain
unproved. Sol checked theory and actual files; five focused exact tests
passed normally and with Python -O. No actual zero, numerical onset, new
Goldbach coverage, priority search, publication work or wake queue.
Overall research remains active.

The next pursuit tested a cofactor switch, then changed the partner weight
in `cubic_character_minorant.py`. Put U=chi*log^3 and
K(n)=10W(n)-9U(n)/log(n)^2. The finite-difference identity
U=(1*chi)*(mu*log^3)>=0 proves K<=10W; K equals log(n) on negative-sign
primes. For a mixed-sign squarefree semiprime n=rq, with r negative and
q positive, its exact numerator is
log(n)^2*K(n)=log(r)*(2log(r)-log(q))*(log(r)+7log(q)).
Thus every q>r^2 contribution is negative and may be dropped in an upper
bound for the NEW signed total T_K. Prior negligible-error estimates transfer
with a factor10, yielding T_K<=P+E_mid+o(Y*t), where the remaining positive
semiprimes satisfy w*<q<r^2, hence r>n^(1/3). This does not lower-bound T_K
by the old nonnegative total T. Showing T_K exceeds E_mid and the error is
still open. Sol checked theory and actual files; five exact tests passed
normally and with Python -O, including an independent nonnegative convolution,
negative weights and the one-sided partition at existing-prefix targets.
The pursuit returned `changed-under-evidence` within30 minutes. No actual
zero, numerical onset, new Goldbach coverage, priority search, publication
work or wake queue. Overall research remains active.

The higher-logarithm pursuit returned a checked obstruction in
`log_weight_barrier.py`. For any prime-normalized kernel f, its mixed-sign
semiprime multiplier is H(a)=1+f(1-a)-f(a), so H(a)+H(1-a)=2. Its integral
over every symmetric share interval is fixed, and its positive-part integral
cannot be smaller. The cubic kernel's uniform-share positive mass is10/9,
versus1 for W; this is a formal comparison, not actual prime density.
Moreover finite nonnegative subtractions of higher chi*log^j weights cannot
decrease the q<=r semiprime contribution. Higher degree alone therefore
does not remove the remaining range by this pointwise route. Arbitrary
polynomial coefficients also have an explicit derivative-norm cost near
balanced factors. Sol checked theory and actual files; five focused exact
tests passed normally and with Python -O. The prior cubic identity remains
valid; signed-total positivity and the actual composite correlation stay open.

The same pursuit found Tao's acknowledged Proposition23 proof gap in the
previous quantitative Linnik exposition. The required estimate was rederived
from Thorner--Zaman Theorem2.1 and equation(4.2), using height q^2, an
integer-zero-count cutoff, and endpoint subtraction to cancel low-zero
constants. `relative_type_i.py` owns the checked replacement deduction;
the rare-prime sieve and twisted distribution proof now point to it. This
preserves the required t-power errors and normalized L^2/D error after a
sufficiently small fixed delta choice. Sol checked the repair; no executable
change or repeated old experiment was needed. The pursuit closed within30
minutes, with no actual zero, numerical onset, new Goldbach coverage,
priority search, publication work or wake queue. Overall research remains active.

The next pursuit combined relative distribution with the tunable cubic
weight in `balanced_semiprime_budget.py`. For each fixed0<epsilon<=1/100,
choose delta sufficiently small DEPENDING on epsilon and kappa=1/epsilon.
In the same actual-zero regime and on the original pruned pool at those
parameters, the new signed total satisfies
P>=T_kappa-C*epsilon*Y*S_2(m)*t-o_epsilon(Y*t), with C absolute.
The relative distribution proof extends to Q=Y^(1/2-epsilon)/D^3;
injective sieve support handles positive factors through Y^(1/2-2epsilon),
without requiring q<=sqrt(level). The cubic weight makes larger factors
nonpositive beyond Y^(1/2+2epsilon). Its positive multiplier is at most3
on the remaining band, whose actual reciprocal rare-prime mass is
2epsilon*t+o(t/loglog(Y)). An auxiliary fixed cutoff Y^(1/10) in Henriot's
corrected theorem makes the two-prime upper-bound constant absolute.
Thus the positive composite loss is an arbitrarily small FIXED fraction
of the prime-pair scale. This is not a little-o bound for one fixed epsilon,
a same-delta or growing-kappa theorem, or a positive lower bound for T_kappa.
That signed-total lower bound remains the required gap. Sol checked theory
and actual files; four focused exact tests passed normally and with Python
-O. The pursuit returned `changed-under-evidence` within30 minutes. No
actual zero, numerical onset, new Goldbach coverage, priority search,
publication work or wake queue. Overall research remains active.

The positivity pursuit found a checked obstruction in
`cubic_positivity_obstruction.py`. Pairing complementary divisors gives the
exact cubic hyperbola kernel h(x)=(1-2x)*(1+kappa*x*(1-x)). Let T_low
retain only divisors d<=Y^(1/2-2epsilon) in the SAME T_kappa. At fixed
epsilon and sufficiently small delta, then sufficiently large fixed u,
the actual-zero hypotheses imply T_low<=-(kappa/32)*Y*S_2(m)*t.
The signed sieve expansion uses unique rough/smooth factorization of its
remainder indices. Actual character rarity reduces its divisor MAIN to
a Mobius simplex limit, the Dickman function. Its exact first three
moments give the normalized coefficient (2-kappa)/2 as theta=delta/u
decreases. Choosing u first makes the fixed sieve error sufficiently
small; Y then grows. No growing-u or growing-kappa theorem is asserted.
This is a negative estimate ONLY for T_low, not the full signed total.
Its complementary divisor range must supply a substantial positive term
for this weight to prove positivity; treating that range as negligible
would make the route fail. The earlier composite-error inequality remains
valid. Sol checked theory and actual files; five exact tests passed
normally and with Python -O, including rational Dickman tail enclosures,
both boundary signs, and complete finite divisor/support controls. The
pursuit returned `changed-under-evidence` within30 minutes. No new actual
Goldbach coverage, zero, numerical onset, priority search, publication
work or wake queue. Overall research remains active.

The next weight-redesign pursuit returned a broader checked tradeoff in
`log_weight_barrier.py`. A fixed polynomial f has accessible endpoint-main
coefficient A_f=(f'(0)+f'(1))/2, with the precise order: choose u large
for a requested tolerance, then Y sufficiently large. For the safe
nonnegative logarithmic-subtraction family, put B=sum(j-2)c_j. Then
A_f=1-B/2 and H_f(a)>=(1-a)*(2-B*a*(2a-1)) for1/2<a<1.
Making H_f(a)<=0 requires B>=2/(a*(2a-1))>2, so the accessible main
turns negative. Cubic and quartic penalties attain this bound; higher
degree cannot improve suppression per main-term cost within this family.
A separate formal derivative argument shows that positive A_f and any
semiprime sign deletion force positive all-negative triple weight somewhere
in the open logarithmic-share simplex. It asserts no actual triple count.
The explicit alternative f(s)=s-100s^2(1-s)^2(1-2s) has A_f=1 and
H_f(3/4)=-193/64, but triple weight7263/15625 at shares(9/10,1/25,3/50).
This preserves a candidate component while exposing the new composite
error that prevents reuse of the old pointwise bound. Neither changing
degree nor changing signs alone has closed the prime correlation gap.
Sol checked theory and actual files; nine exact tests passed normally
and with Python -O, including sharp costs and an independent eight-divisor
triple expansion. The pursuit closed within30 minutes, with no new actual
coverage, zero, numerical onset, priority search, publication work or wake
queue. Overall research remains active.

The next pursuit controlled part of the alternative's new error in
`quintic_partner_weight.py`. For ANY fixed polynomial, its rough-partner
weight is bounded by C_f,theta*log(Y), so repeated factors, two or more
positive-sign factors, and positive factors w<q<=Y^(1/2-2epsilon) can
be discarded absolutely with o(Y*t) cost using the existing estimates.
For the alternative quintic, seven or more negative factors give zero;
five give the strictly positive normalized weight240*kappa*2^h*product x_i.
The surviving signed reduction is exactly prime pairs plus two-, three-,
four-, five- and six-factor partners and o(Y*t). Even classes have one
positive-sign factor above the enlarged cutoff; odd classes have none.
Positive pure triples force a prime larger than n^(18/25), leaving a
two-prime cofactor below Y^(7/25). An auxiliary sieve then gives the actual
bound S_3^+<<kappa*Y*S_2(m)*t with an absolute constant. Its remainder
indices are NOT injective: at most binom(omega(index),2) choices cost
O(log(Y)^2), still absorbed by the relative distribution budget. This is
only a main-scale bound, not a small fraction or a positivity theorem.
Positive balanced five-factor weights expose an additional surviving loss.
Sol checked theory and actual files; five exact tests passed normally
and with Python -O. The pursuit returned `changed-under-evidence` within30
minutes. No new actual coverage, zero, numerical onset, priority search,
publication work or wake queue. Overall research remains active.

The next pursuit closes the remaining MAIN-SCALE error bounds for that
quintic in `quintic_loss_budget.py`. In the same actual-zero regime,
all surviving positive composite weights total at most
C*(1+kappa)*Y*S_2(m)*t+o(Y*t), with C absolute, independent of theta.
For five negative factors, use their two smallest factors as cofactor and
adapt the auxiliary sieve cutoff to the second smallest. For the even
factor classes, switch the actual prime variable to the single large
positive-sign factor; repaired bulk Linnik then uses modulus D*e at scale
Y/M, without requiring distribution at modulus M. Its summed errors are
O_kappa(Y*(t^28*log(Y)^2+log(Y)^3/D)+Y^(19/25+o(1)))=o(Y*t).
An explicitly FORMAL logarithmic-share measure gives signed pure-triple
and pure-five integrals -kappa/12 and +kappa/12. This exact cancellation
does not assert an actual prime-factor distribution or signed correlation.
The composite bound is still not a small specified fraction, and the
positive lower bound for the full signed total remains unproved.
Five exact tests passed normally and with Python -O, covering adaptive
index multiplicity, complete switched CRT counts, range slack, weighted
factor shapes and independent iterated polynomial integration.
Sol checked theory and actual files. The pursuit returned
`changed-under-evidence` within30 minutes.
No new actual coverage, zero, numerical onset, priority search,
publication work or wake queue. Overall research remains active.

The signed-cancellation pursuit found a general conservation identity in
`formal_weight_conservation.py`. For every normalized polynomial f of
degree d and0<=theta<1/d, the sum of FORMAL odd all-negative factor
integrals equals B_f(theta)=-E[h'(theta*V)]/2, h=f(1-x)-f(x), with V
the normalized Dickman variable. At theta0 this is A_f, so the formal
composite total is A_f-1. At nonzero theta the quintic gives exactly
1-2kappa*theta+18kappa*theta^2-(170/3)kappa*theta^3
+(190/3)kappa*theta^4. A convolution generating function proves the
identity for every degree; independent exact simplex and moment algorithms
check it through degree10. A rational factorial enclosure connects B_f
to the already proved accessible-divisor main, retaining its fixed sieve
error separately. Thus the formal cancellation supplies no second estimate
for actual composite correlations. The exact remaining identity is
P/Z-1=T_boundary/Z-Delta/Z+(T_low/Z-B_f), where
Delta=(T_f-P)-(B_f-1)Z and Z=length(J_real)*S_2(m)*t.
The signed quantity T_boundary-Delta still lacks the estimate needed for
positivity. Five focused exact tests passed normally and with Python -O.
Sol checked theory and actual files. The pursuit returned
`changed-under-evidence` within30 minutes.
No new actual coverage, zero, numerical onset, priority search,
publication work or wake queue. Overall research remains active.

On 2026-09-09 Kevin resumed the clean main checkpoint cf48198, with latest
mathematics6f9a77b, and reaffirmed open-ended curiosity, 30-minute hypothesis
ceilings, independent correctness review, and no manual wake queues. He
clarified that seeking a new arithmetic ingredient must preserve the useful
polynomial identities and bounds: the earlier limitations concern specific
approaches, not every future use of those tools. The operative question is
what mechanism could make the linked prime conditions cancel or reinforce
each other, and what would demonstrate it. This is a resumed execution, not
evidence of research running between the saved checkpoint and this session.

The first resumed pursuit returns `changed-under-evidence` in
`buchstab_endpoint_bridge.py`. Exact least-prime Buchstab subtraction up to
R=floor(Y^(1/2-2epsilon)) leaves actual prime partners and only distinct
mixed-sign semiprimes. The earlier corrected Henriot bound and actual
rare-prime reciprocal estimate bound this endpoint loss by
C*epsilon*Z+o(Y*t), with C absolute and Z=length(J_real)*S_2(m)*t.
There is no additional rarity factor. The initial rough-pool mass is
L*X*V(z)+O(eta_u*L*X*V(z))+o(Y*t), retaining the fixed sieve error.
The remaining unproved target is a stated one-sided bound on the exact
prime-times-rough sum U_A(z,R). Its condition P^-(k)>=q couples the two
variables; it is not automatically a separated-coefficient Type II sum.
This range adds smaller factors while excluding the balanced endpoint,
so it is not claimed to be a subset or a proved easier version of the
old Vaughan target. No cancellation estimate has been obtained.
Ford--Maynard's bounded-sequence sieve motivated the test but is not
imported: its positivity/comparison and boundedness hypotheses are missing
for the signed rare-scale model. The exact Buchstab identity also accepts
polynomial kernel weights, but their initial full total cannot be replaced
by T_low or its formal main. Sol independently checked theory and actual
files; five exact tests passed normally and with Python -O, including
prime powers, strict cutoffs, actual finite reflected-prime/sign support
and the existing1459+11^3 example. The pursuit closed within30 minutes.
The next useful action must test an arithmetic estimate for U, possibly
using preserved polynomial components, not iterate this counting identity.
No new actual coverage, zero, numerical onset, priority search, publication
work, push, foreground operation, or wake queue. Overall research active.

The next pursuit tests whether lambda_chi=1*chi can supply a SECOND rarity
factor for two linked positive-character primes. The direct multiplicative
upper bound retains the empty-cofactor atom1 and supplies none. A restricted
coefficient-one route succeeds in `rare_shifted_divisor_bound.py`: with an
ACTUAL zero beta=1-1/(eta*log D), X=D^V, V>=log^3 eta and t=V/eta<=1/log X,
the weighted sum over X<p<=2X, p,p+h prime, chi(p)=chi(p+h)=+1 satisfies
Q++<<S_2(h)*X*t^2*log^8 eta=o(S_2(h)*X*t), uniformly for even0<h<=X/2.
This is a deduction from Matomaki--Merikoski Proposition2.3, equation(15)
and Lemma2.4, https://arxiv.org/html/2112.11412v2 . It is an actual
conditional upper estimate, with no assumption of independent prime signs.
Subtracting the lemma's y=X and y=X^2 evaluations bounds each rough harmonic
character partial sum by O(E/U), E=O(t*U^4)+O(eta^-20), U=K*log eta.
The smooth hyperbola identity produces two such factors after ALL main
terms are recombined before absolute values. Complete residue sums restore
the conductor-prime local factors. The proof budgets every dyadic error.
Growing U is justified directly by the source, in this NEW restricted regime;
it does not alter the earlier fixed-u conclusions or parameter order.

The original transfer to q,p=m-M*q, chi(M)=-1, M<=Y^(13/25), remains OPEN.
The source only gives coefficient-one relations. Substitution n=M*q kills
lambda_chi(n) exactly; a divisor divisibility restriction or an enlarged
modulus requires a new uniform theorem. Cowan's twisted-divisor Theorem1.1
does not cover the zero shifts in its divisor parameters and the principal
product chi^2; Tao--Teravainen supplies no stated variable-M transfer either.
Neither the rare/common Goldbach pair nor the Buchstab one-sided target is
estimated here. Preserve the polynomial identities and bounds for future
combinations with this or another arithmetic ingredient. Five finite tests
check exact hyperbola recombination, log-form cancellation, conductor factors,
and the failed multiplier substitution; they are not tests of an actual zero
or an infinite prime estimate. Overall research remains active.
Sol reviewer `/root/sieve_review` independently passed both the theory and
actual files. The five focused tests passed normally in0.088s and under
Python -O in0.093s. Reassessment: `changed-under-evidence` within30 minutes;
retain the coefficient-one component, leave the variable-M transfer open.
No new actual coverage, zero, numerical onset, publication, push, foreground
work, installs or manual wake queue. The saved Qwen-unavailable exception
remains unchanged; this was active execution, with no intervening idle work
claimed.

The affine-extension pursuit in `rare_affine_small_cofactor.py` proves
negligibility for a part of the ACTUAL cofactor range, while the full range
remains open. Retain the new actual-zero/large-V assumptions Y=D^V,
V>=log^3 eta, t=V/eta<=1/log Y. For fixed0<theta<1/5, sum the positive-prime
pair-log mass for q and p=m-M*q over all original-Y^theta-rough integers
2<=M<=Y^(1/5) with gcd(M,Dm)=1. The total is o_theta(Y*t), uniformly over
even m in[Y,2Y] with q in(Y/(2M),Y/M] and p in(Y/2,Y]. Squarefreeness
and a five-factor cap are unnecessary. The actual even quintic classes are
a subset, and the fixed-polynomial bound |K_f(n)|<<_(f,theta)log Y transfers
this to their FULL ABSOLUTE contribution in that cofactor range.

This adapts the proof of Matomaki--Merikoski Proposition2.3; it is not an
invocation of its coefficient-one statement for a different equation.
Directly making p's large divisor implicit leaves Poisson modulus D*d2*c;
M enters as an invertible inverse-phase factor. The derivative scales
1/(Y/M) and M/Y agree. The two rough harmonic character cancellations
survive, after every orientation main is recombined before absolute values.
Corrected Henriot New Theorem5 bounds the affine divisor-weighted sieve
tails; its norm and function-class conditions are included. Shared primes
dividing m are removed on the original rough support without applying
Henriot at an unjustified tiny divided scale. Conductor and M-coprimality
local factors are separately restored. With sum_M1/M=O_theta(1), the main
is O_theta(S_2(m)*Y*t^2*log^8 eta). The summed oscillatory error is
D^2*Y^(44/45+o(1)); the M-coprimality error is Y^(1-theta+o(1)), and
the remaining errors are O_theta(S_2(m)*Y*eta^-20). These are all o(Y*t)
in the stated regime. The exact density verifier retains the1/a Jacobian.

The full M<=Y^(13/25) extension FAILS the available error-budget test.
Ignoring small conductor/sieve/log losses, direct absolute Weil bounds
sum to Y^(3/4+alpha), and the reversed-orientation budget to
Y^(3/4+3alpha/4), for M<=Y^alpha. The latter is Y^(57/50) at alpha13/25.
These are METHOD upper bounds, not lower bounds or universal obstructions.
The reversed complete theorem is not promoted. A new estimate, plausibly
averaging across cofactors before absolute values, is needed for the larger
range. All-negative odd composite classes and the positive lower bound
for the signed total also remain open. Preserve all polynomial components,
the coefficient-one theorem and the new partial affine theorem together.
Sol reviewer `/root/sieve_review` passed both the theory and actual files,
including the affine source adaptation, corrected sieve-tail conditions,
all M/theta factors and the final o(Y*t) conclusion. Four exact tests passed
normally and under Python -O, both in0.011s. The pursuit returned
`changed-under-evidence` within30 minutes: a small-cofactor arithmetic loss
is now negligible, while full-range absolute summation failed its budget.
Next concrete test: can averaging the remaining cofactors BEFORE absolute
values preserve the two character cancellations and gain the missing power?
No new actual coverage, zero, numerical onset, publication, push, foreground
work, installs or manual wake queue. No process is left running at this
checkpoint. The overall Goldbach research goal remains active.

The next cofactor-averaging pursuit returns a SOURCE-BUDGET FAILURE in
`cofactor_averaging_budget.py`. Test: does Bettin--Chandee Theorem1,
equation(1.2), https://arxiv.org/pdf/1502.00769v1 , give a power saving
after grouping r=M*a in the actual inverse phase? For M~Y^b, small
q-divisor a~Y^x and p-divisor c~Y^y, set r_exp=b+x, s=y and
k_exp=b+x+y-1>=0. The Poisson prefactor is Y/(R*C), and the numerator
parameter is the target m~Y. The generic L2 norms contribute
(r_exp+s+k_exp)/2; the phase ratio m*K/(R*C) has exponent0.
Even granting a COST-FREE separation of the actual coupled weights, the
two source terms give worst-box exponents
`39/40+19*b/40` and `15/16+b/2`, attained at x=(1-b)/2,y=1/2.
At b=1/5 these are107/100 and83/80; at b=13/25 they are611/500 and479/400.
Both exceed1 throughout the remaining interval. The theorem returns their
SUM, not their minimum. Fixed-frequency application followed by summation
worsens its first term and leaves the second unchanged; reciprocity does
not change the exponents. The required separable decomposition has not
been proved either, but granting it for free already fails the strength test.

This is a calculation of substituted UPPER bounds, not evidence that the
actual oscillatory error is large. It rules out only the unchanged generic-
norm plug-in as a sufficient proof. No new prime estimate or coverage is
claimed. Preserve cofactor averaging, the exact grouping/normalization, the
polynomial tools and all previous arithmetic components. A materially new
next test should retain the separate M and a structure after beta-sieving
and test whether that gives stronger averaged cancellation; merely citing
the same generic trilinear estimate under new notation is not a new route.
Sol reviewer `/root/sieve_review` independently checked the source scaling,
monotonicity and thresholds, then the actual files: PASS. Four exact tests
passed normally in0.020s and under Python -O in0.036s. They test bookkeeping,
not the coupled-sum source hypotheses or any analytic prime estimate. The
pursuit returned `changed-under-evidence` within30 minutes. The previous
actual affine result remains the latest arithmetic estimate; this pursuit
adds a verified failed-source application, with its useful setup preserved.
No new coverage, zero, effective onset, publication, push, foreground work,
installs or manual wake queue. Qwen remains unavailable without a retry.
No research process is left running at this checkpoint. Overall goal active.

The separate-factor pursuit proves a RESTRICTED EXPONENTIAL-KERNEL bound
in `separate_factor_prime_kernel.py`. Keeping M,a separate, their exact
double Fourier transform at prime modulus p is p*Kl_3(t*h*l;p) off the
axes,1 on each single nonzero axis, and1-p at the origin, when p does not
divide t. The t=0 case is separately the product of Ramanujan sums.
Pointwise complete-sum bounds alone reach Y. Retaining the original
frequency k and grouping w=k*l AFTER completion instead permits a bilinear
application of Kowalski--Michel--Sawin Theorem1.1, equation(1.2):
https://arxiv.org/pdf/1511.01636v5 . This is a different, successful
source-strength test from the failed generic r=M*a reduction.

The proved model has P=Y^(1/2), M~B=Y^b, a~A=Y^((1-b)/2), k<=K=Y^(b/2),
1/5<=b<=12/25, smooth SEPARATE M,a weights and arbitrary bounded k weights
for each PRIME modulus p in[P,2P]. With the actual Poisson prefactor
Y/(B*A*p), the sum is O_epsilon(Y^(127/128+epsilon)), uniformly m in[Y,2Y].
Dual lengths U=p/B,V=p/A satisfy U*V*K~p; the grouped coefficient at w=k*l
is divisor-bounded. The source gives saving p^-1/64. Schwartz truncation
preserves its hypotheses after small epsilon losses. Axes and p|m moduli
cost O(B*A+A+B), at most Y^(37/50), and are treated without the unit formula.

This is an analytic cancellation theorem in the stated model, NOT a new
original-affine prime-pair estimate. The actual modulus d2*c is generally
composite; rough/sieve/character coefficients and coupled Poisson weights
have not been transferred. KMS section1.5.2 does not supply the needed
composite version. Neither all hyperbola boxes nor the remaining b range
are covered here. The latest ORIGINAL-AFFINE result remains2b8cf98.
Preserve the polynomial identities, bounds and all previous components.
Next concrete question: can a composite-modulus third-divisor/Kloosterman
distribution estimate support these factors with the actual small sieve
indices and conductor while retaining a power saving? Source hypotheses
and losses, including any roughness relaxation, must be checked explicitly.
Four exact cyclotomic/budget tests passed normally in0.062s and under -O
in0.075s; they guard identities and bookkeeping, not the analytic source.
Sol reviewer `/root/sieve_review` independently checked the source, theory
and actual files: PASS, including all modes and the source's prime boundary.
The pursuit returned `changed-under-evidence` within30 minutes: keeping
factors separate now has a proved cancellation component worth transferring.
The overall research goal remains active; no new coverage or signed
prime-correlation estimate, publication, push, installs or manual wake queue.
Qwen remains unavailable without a retry. No process is left running at
this checkpoint, and no work between inactive turns is claimed.

The next transfer pursuit proves `decorated_prime_kernel.py`: the kernel
now permits c=s*p with p prime near P=Y^(1/2), s<=S, arbitrary bounded
joint residue weights modulo J<=J0, and frequencies k<=H*K. The underlying
B=Y^b,A=Y^((1-b)/2),K=Y^(b/2),1/5<=b<=12/25 geometry is retained. The
TOTAL modulus grows with s; the frequency inflation H is explicit. For
S,J0,H<=Y^(1/4096), the proved bound is
  Y^(127/128+epsilon)*S^4*J0^4*H
    +H*B*A*log(2S)+S*H*J0*(A+B) <<Y^(4073/4096+epsilon).
CRT at period cJ splits off prime p even if gcd(s,J)>1. The prime Kl3
argument is m*k*h*l*inverse(s^3*J^2), with any stated unit multiplier.
The small transform has magnitude at most(sJ)^2. Splitting the two dual
residue classes costs(sJ)^2 more; its k dependence is absorbed as a bounded
k coefficient. No third residue split is needed. Axes and p|m modes are
below Y^(3/4). Uniform smooth coupling of M,a is allowed via a convergent
Fourier decomposition, with k-dependent coefficients handled explicitly.

A second retained component is the NONNEGATIVE relaxation of original M
to z-rough M: its reciprocal mass is O(U), and the existing zero mode keeps
both character harmonics, giving at most one extra factor U~log eta and
still o(Y*t). No chi(M) factor appears. Prime-divisor coprimality costs
are O(U/z). This is a statement about the zero-mode expression, not a
replacement of the entire arithmetic sum. A beta sieve introduces a new
index e0; its longer dual range cancels the apparent1/e0 gain. Index counts,
periods, frequency inflation and tails must be paid before any prime result.

The source search did not justify a general-composite plug-in. Topacogullari
1506.02608v1 Thm1.3/section4 treats the right additive orientation but is
untwisted; Drappeau--Topacogullari2019 Lemma4.5 allows characters but has
|h|<=X^(1/4) and an ordinary-divisor second factor. Do not combine their
separate features into an unstated theorem. Their methods remain candidates.
The CRT theorem covers SMALL prime multiples, not balanced composite cores.
All original sieve costs, other boxes/ranges and the signed correlation
remain OPEN; latest original-affine estimate remains2b8cf98. Polynomial
components remain preserved. Next test: a general-composite factor estimate
or a costed spectral adaptation meeting the actual character/shift conditions.
Sol reviewer `/root/sieve_review` passed theory and actual files, after
correcting a divisor-sum notation to DISTINCT PRIME divisors. Five new exact
CRT/budget tests passed normally in0.022s and under -O in0.026s. No old
experiment was rerun. The pursuit returned `changed-under-evidence`
within30 minutes. No new coverage, zero, effective onset, publication, push,
foreground work, installs or manual wake queue. Qwen remains unavailable;
no process is left running at this checkpoint. Overall research goal active.

The next bounded pursuit proves `hyperbola_prime_kernel.py`: changing the
completed-frequency grouping, with a linear-completion estimate in the
small-divisor region, covers EVERY box of the smooth decorated prime-core
model. The parameters are B=Y^b,A=Y^x,P=Y^y,K=B*A*P/Y, with
  1/5<=b<=13/25, 0<=x<=(1-b)/2, 0<=y<=1/2.
The preceding modulus c=s*p, p prime near P, joint periodic weights and
S,J0,H<=Y^(1/4096) remain. The final bound is unchanged:
  Y^(127/128+epsilon)*S^4*J0^4*H
    +H*B*A*log(2S)+S*H*J0*(A+B) <<Y^(4073/4096+epsilon).
Nonempty boxes force p large enough for CRT and k<p. For y<=49/100,
pointwise complete-sum bounds suffice. For y>=49/100 and x>=1/16,
keep the completed divisor frequency l separate and group w=k*|h|.
KMS's bulk exponent becomes(103*y+12)/64<=127/128. For x<1/16,
the exact Fourier transform of Kl3, extended at zero by1/p, is a
classical Kl2 sum at nonzero frequencies and zero at frequency0.
Linear completion on l=r+T*j uses j-scale p/A<=p, even when the
l-scale exceeds p. Every prime-axis mode and the thin dual-length
strip below1 are included. Smooth coefficients remain essential.

This closes the box-range gap in the MODEL, including b through13/25.
It does not close the general-composite core, original coefficient/sieve
transfer, or signed prime-correlation gaps. The latest original-affine
estimate remains2b8cf98. Polynomial components remain preserved.
Next concrete test: can factorization or completion give a power saving
for a general composite core in the critical modulus boxes, after
explicitly retaining nonunit modes and the actual coefficient costs?
Do not import an unstated composite-modulus KMS theorem.
Five NEW exact Fourier/progression/budget tests passed normally in0.222s
and under -O in0.226s. Sol `/root/sieve_review` independently passed the
linear lemma, full theory and actual files, with no correction required.
The pursuit returned `changed-under-evidence` within30 minutes. No old
experiment was rerun. No new prime coverage, zero, effective onset,
publication, push, foreground work, installs or manual wake queue.
Qwen remains unavailable without a retry. No process is left running
at this checkpoint; the overall research goal remains active.

The next composite-modulus pursuit proves `composite_linear_kernel.py`:
for ALL integers q near C=Y^y, including prime powers, the same smooth
box model with arbitrary joint periods J_q<=J0 and k<=H*B*A*C/Y satisfies
  sum_q |E_q| <<Y^epsilon*H*(J0^2*min(A,B)*C^(3/2)+J0*B*A).
No coprimality between J_q and q, or between m*k and q, is required.
The normalized complete transform in one frequency is an ordinary
Kloosterman sum. Periodic lifting costs J^2; the nonzero-frequency gcd
factor is absorbed by a divisor average. The h=0 mode uses a separate
restricted Ramanujan decomposition and the modulus average of gcd(q,m*k).
All its costs are included, including shared period factors and prime powers.
The sole analytic input is the ordinary composite Weil bound, checked in
Topacogullari1506.02608v1 section2 p4; no shifted-divisor or composite KMS
theorem is imported.

This saves a power when min(b,x)+3*y/2<=127/128, giving
Y^(4067/4096+epsilon) with J0,H<=Y^(1/4096). It FAILS the required power
budget at b=x=1/3,y=1/2, where the bound is Y^(13/12+epsilon) before
decorations. That is a failure of this upper bound, not evidence that the
true error is large. Preserve the composite unbalanced component, the
prime-core theorem and all polynomial tools. The next method must save
more than1/12 at this box and pay period/frequency costs.
One concrete UNTESTED route is additive autocorrelation of multiplicative
Kl3 dilates plus CRT. Check prime diagonal cases, coefficient nonunits and
prime powers before claiming any composite bilinear consequence. KMS
Remark1.2 points to FKM arXiv1211.6043 Theorem1.17; that exact theorem has
not yet been read here and is only a primary locator.

Six NEW exact composite-transform, restricted-Ramanujan, gcd-average and
budget tests passed normally in0.774s and under -O in0.769s. Sol
`/root/sieve_review` independently passed the transforms, full theory and
actual files, with no correction required. The pursuit returned
`changed-under-evidence` within30 minutes: useful general-composite
coverage is preserved alongside a quantified critical failure.
The full original arithmetic/sieve transfer and signed correlation remain
OPEN; latest original-affine estimate remains2b8cf98. No old experiment,
new prime coverage, zero, effective onset, publication, push, foreground
work, installation or manual wake queue. Qwen remains unavailable without
a retry. No process is left running at this checkpoint; overall goal active.

The next pursuit proves `squarefree_correlation_kernel.py`. FKM
arXiv1211.6043v3 Theorem1.17, Proposition3.1 and sections3/6 have now been
read. The proof uses only the PRIME bounded-exceptional-pair theorem.
CRT and a congruence count give the derived squarefree bilinear bound
  |sum alpha_a beta_n K_q(c*a*n)|
    <<q^epsilon*M*N*(q^-1/4+M^-1/2+q^(1/4)*N^-1/2),
for bounded coefficients, ANY integer multiplier c and no coefficient
coprimality restriction. K_q(0)=1/q for squarefree q is explicit.
No composite KMS/FKM theorem is imported. Knowing the exact prime
exceptional pairs is unnecessary: fixing one coefficient variable fixes
the other variable AND the additive frequency modulo each selected divisor.

The exact local F_p expansion retains every nonunit mode. Its four
degenerate prime assignments have normalized rescaled mass g/D^2;
their costs in all three bilinear terms are at most1. A transient briefing
overstatement was corrected: the short-variable factor can be D^-1/2,
not uniformly D^-3/4. The saved proof uses the valid <=1 statement, and
a regression fixture preserves that boundary. Shared period factors and
both axes, including their subtracted overlap, are explicitly paid for.

At the SAME formerly failing balanced box B=A=Y^(1/3),C=Y^(1/2),K=Y^(1/6),
the smooth model over ALL SQUAREFREE q near C now satisfies
  sum_q |E_q| <<Y^(23/24+epsilon)*H*J0^8+Y^epsilon*H*J0*B*A
               <<Y^(11803/12288+epsilon).
This includes small prime factors and balanced semiprime cores. Prime
powers, further box coverage and original arithmetic/sieve transfer remain
OPEN, as does the signed prime-correlation estimate. Latest original-affine
bound remains2b8cf98. All preceding polynomial and kernel tools are preserved.

Next UNTESTED question: can prime-power stationary phase prove
  |F_q(h,l;t)| <<q^(1+epsilon)*gcd(q,h,l,t),
including unequal valuations, p=2,3, and zero parameters? Even exponents
suggest a count of cubic stationary points; odd exponents also need the
quadratic Gauss sum. If valid, Fourier expansion of a period-J weight at
qJ should cost J^4, and the nonzero-frequency divisor average should give
O(Y^epsilon*H*J0^4*C) per modulus. Then test a squarefull-part split:
small squarefull part u<=Y^(1/128) costs at most u^(13/4) in the proved
squarefree CRT estimate, while the large-part moduli number is
O(C*Y^(-1/256)). Expected total exponent4085/4096 is UNPROVED until all
these steps are checked. This route could remove prime powers by density
without assuming a prime-power correlation theorem.

Seven NEW exact CRT, conjugation, degeneration, exceptional-class and
budget tests passed normally in0.191s and under -O in0.190s. Sol
`/root/sieve_review` independently passed source/theory and actual files.
The pursuit returned `changed-under-evidence` within30 minutes. No old
experiment was rerun; no new prime coverage, zero, effective onset,
publication, push, foreground work, installation or manual wake queue.
Qwen remains unavailable without a retry. No process is left running at
this checkpoint; the overall research goal remains active.

The next pursuit proves `all_moduli_balanced_kernel.py`. The proposed
prime-power pointwise bound holds for every q,h,l,t:
  |F_q(h,l;t)|<=6^omega(q)*q*gcd(q,h,l,t).
The proof removes the common valuation, handles its all-zero case
separately, counts cubic stationary points at even exponents, and pays
the quadratic Gauss sums at odd exponents. The bad primes2,3 and unequal
valuations are included. Only the previously checked PRIME Kl3 bound is
imported; no prime-power correlation theorem is assumed.

An exact double Fourier lift pays J^4 for arbitrary joint period J,
including gcd(q,J)>1. The nonzero-frequency gcd average gives
O(Y^epsilon*H*J0^4*C) per modulus. Split the FULL squarefull part u(q)
at Z=Y^(1/128). Moduli with u>Z number O(C*Z^-1/2); for u<=Z, the saved
squarefree correlation estimate absorbs the small part at cost Z^(13/4).
Both axes and their overlap retain the earlier general-modulus bounds.
At B=A=Y^(1/3),C=Y^(1/2),K=Y^(1/6), the smooth model over ALL integers
q near C therefore satisfies
  sum_q |E_q|<<Y^epsilon*H*(J0^8*Y^(23/24)*Z^(13/4)
                              +J0^4*Y*Z^-1/2+J0*Y^(2/3))
              <<Y^(4085/4096+epsilon),
for J0,H<=Y^(1/4096). This closes the squarefree restriction at this box.
It does not close a prime-power correlation theorem, other box geometries,
original arithmetic/sieve transfer, or the signed prime correlation.
Latest original-affine estimate remains2b8cf98; polynomial tools remain.

Six NEW exact stationary, valuation, Gauss, periodic-lift, squarefull and
budget tests passed normally and under -O, each in0.299s. Sol
`/root/sieve_review` independently passed the prime-power proof, global
transfer and actual files, with no correction required. This pursuit began
08:34 UTC and returned `changed-under-evidence` within30 minutes.
Next concrete question: at B=A=Y^(1/4),C=Y^(1/2),K=1, both current
composite budgets reach Y before decorations. What additional cancellation
mechanism can beat that boundary, with its coefficients and moduli paid for?
This is an upper-bound budget obstruction, not evidence of a large true sum.
No old experiment was rerun; no new prime coverage, zero, effective onset,
publication, push, foreground work, installation or manual wake queue.
Qwen remains unavailable without retry. No research process is left running
at this checkpoint. Overall goal active; no claim of execution during pauses.

The next pursuit proves `reciprocal_energy_kernel.py`, using an elementary
modulus-average mechanism at the remaining symmetric boundary. In a fourth
moment, the reciprocal relation has integer numerator
  D=(a1+a2)*a3*a4-(a3+a4)*a1*a2.
For D!=0, a modulus contributes only if q divides m*k*D, giving a divisor
bound even when m*k is not a unit. For D=0, fixing a1,a2 and reducing
u/v=1/a1+1/a2 gives (u*a3-v)*(u*a4-v)=v^2. This counts ALL rational
relations, including non-diagonal ones, in O(A^(2+epsilon)). Thus
  sum_(q near C) E_(q,mk)(A)<<Y^epsilon*(A^4+C*A^2).
No prime-only additive-energy theorem or composite extension is imported.

Holder in the spatial variable and then q, including repeated inverse
residues when B>q, gives
  R(B,A,C)=C^(3/4)*B^(3/4)*(B+C)^(1/4)*(A^4+C*A^2)^(1/4).
The full smooth model satisfies
  sum_q |E_q|<<Y^epsilon*H*J0^2*min(R(B,A,C),R(A,B,C)).
This covers ALL integer moduli and arbitrary bounded separated spatial
weights. Joint period J costs J^2. The k count cancels the kernel prefactor;
no spatial Poisson decomposition or separate axis estimate is needed.
At B=A=Y^(1/4),C=Y^(1/2),K=1, the bound is Y^(15/16+epsilon)*H*J0^2,
hence3843/4096 after caps. Throughout valid boxes with b,x<=9/32,y<=1/2,
monotonicity gives127/128 before caps and4067/4096 after caps.

The common nonzero m*k across q is essential; arbitrary t_q=q destroys
the divisor argument. Arbitrary coupled arithmetic weights remain outside
the separated-weight assertion. At b=1/2,x=1/4,y=1/2, the new energy
budget is9/8 and the previous linear budget is1. Preserve these failures
alongside the useful region; they are not lower bounds on the true sum.
Next concrete question: after completing the long M variable at this box,
can a modulus-averaged correlation of the resulting ordinary Kloosterman
sums save a power with both a and k near Y^(1/4)? This is UNTESTED.
All original sieve/weight transfer and the signed prime correlation remain
OPEN; latest original-affine result remains2b8cf98. Polynomial tools remain.

Five NEW exact rational-relation, weighted fourth-moment, divisor-average,
multiplicity and budget tests passed normally in0.112s and under -O in0.110s.
Sol `/root/sieve_review` independently passed the critical proof, general
family and actual files with no correction needed. This pursuit began
08:50 UTC and returned `changed-under-evidence` within30 minutes. No old
experiment was rerun; no new prime coverage, zero, effective onset,
originality, publication, push, foreground work, installation or wake queue.
Qwen remains unavailable without retry. No research process is left running
at this checkpoint; the overall goal remains active, with pauses reported.

The next pursuit changes direction under the source evidence. The ordinary
Kl2 bilinear interval theorems checked here do not accept the inverse-a
support after M-Poisson. Freezing a instead leaves h too short to improve
the existing Weil budget. Preserve these source-applicability failures;
they do not refute the source theorems or every use of completion.

`two_prime_kl3_kernel.py` instead derives a rank-three bilinear theorem for
q=p1*p2 with distinct primes and p_min>=q^(2/5). For arbitrary complex
coefficients supported <=X, sqrt(q)<=X<=q^(1/2+1/128), and ANY integer c,
the norm factor is q^(11/64+epsilon)*X^(5/8), hence q^(31/64) at X=sqrt(q).
The source's literal zero extension is used during amplification, then
the natural K_p(0)=1/p extension is recovered with a paid nonunit error.
KMS prime eight-factor correlations, all-twist diagonal subtraction, and
rank-three CRT with frequency twist h*(q/p)^2 supply the arithmetic gain.
Small auxiliary shifts synchronize the two local diagonals as one integer
multiset equality. Generic, bad and diagonal tuples are all costed.
This derives a two-prime Kl3 statement; MQW's Kl2 theorem is not imported
as a Kl3 theorem, and no prime-square correlation assertion is made.

For the same smooth MODEL at B=Y^(1/2),A=Y^(1/4),C=Y^(1/2),K=Y^(1/4),
the specified two-prime moduli satisfy
  sum_q |E_q|<<Y^(127/128+epsilon)*J0^5*H^2+Y^(3/4+epsilon)*H*J0,
hence exponent4071/4096 after caps. Nonunit m*k, joint periods, both
integer axes and the zero-extension correction are included. General
factorizations, prime powers in this box, full box coverage and the actual
arithmetic/sieve transfer remain OPEN. Latest original-affine remains
2b8cf98. The formal cancellation still does not estimate the signed
prime correlation. Preserve the polynomial identities and earlier bounds.

This pursuit began09:01:55 UTC, with a09:32 UTC ceiling. Five NEW exact
tests passed normally in0.233s and under -O in0.335s. Verifier-only
corrections fixed late-bound histogram generators, float division, and a
vanishing test fixture. Sol `/root/sieve_review` passed the theory,
varying-length argument and actual files, with no material correction.
This pursuit returns `changed-under-evidence` within its30-minute ceiling.
Next concrete question: can CRT counting of bad primes replace the
small-shift condition at every prime, giving a saved bound for general
squarefree moduli in this unbalanced box? Test the complete bad-set and
nonunit-difference costs before asserting any extension. No original
prime coverage, effective onset, zero, novelty or outside action is claimed.
No old experiment was rerun. Qwen remains unavailable without retry;
no model install, publication, push, foreground action or manual wake queue.
No research process is left running at this checkpoint. The overall goal
remains active, with no claim of execution during pauses.

The next pursuit proves `squarefree_unbalanced_kernel.py`: the unbalanced
MODEL box B=Y^(1/2),A=Y^(1/4),C=Y^(1/2),K=Y^(1/4) is now covered for
ALL squarefree q. FKM1405.2293v2 Corollary3.4 supplies the prime four-factor
bound with an explicit rank3 normality check. Divisor shifts preserve one
modulus factor and expose this correlation on the other. A weighted signed
congruence graph bounds every nonunit difference; they are not discarded.

An integer factorization dichotomy combines that route with the retained
prime/two-prime amplification. It gives norm factor X*q^(-1/256+epsilon)
for arbitrary coefficients supported <=X, sqrt(q)<=X<=q^(1/2+1/256),
for the natural K_q extension and ANY integer multiplier. A disjoint
gcd(c,q), gcd(m,q0), gcd(n,q1) partition pays the nonunit cases explicitly.
Fixing h before the l,k bilinear estimate needs only one period-residue
split: the small-transform cost is T^3. All joint periods, nonunit modes,
integer axes and their overlap remain included. The full MODEL satisfies
  sum_q |E_q|<<Y^(1-1/4096+epsilon),
with raw exponent1-511/1048576. The source hypotheses and the original
arithmetic/sieve-transfer boundary remain explicit in the proof module.

The exact exponent test corrected an overcount in the draft: the period
decoration total is6+1/256, not7+1/256. The correction strengthens the
bound. Eight NEW finite algebra/budget tests passed normally in0.124s and
under -O in0.135s. Sol `/root/sieve_review` passed the theory, actual files,
divisor-shift endpoints, corrected arithmetic and the following splice.

The existing squarefull-part split does NOT finish the same box at the
full period/frequency caps. Even after using the small-squarefull density,
its head/tail exponents are
  1-511/1048576+(3/2+1/256)*z, 1+5/4096-z/2.
Their optimal maximum is467315/466944>1 at z=199/233472, within the
proved support ranges. This is a failure of these upper bounds only.
Do not repeat the same splice. Next concrete question: can a prime-square
four-factor correlation, derived from the retained stationary-phase
formula, save a power outside explicit exceptional congruences? Check
the critical equations and exact finite sums before any general claim.

Preserve KMS Proposition4.29's fixed integral bad hypersurface as another
promising component; its full alternative CRT/amplification route was
not proved or needed here. Prime powers in this box, full box coverage,
original sieve transfer and the signed prime correlation remain OPEN.
Latest original-affine remains2b8cf98; all polynomial tools survive.
This pursuit began09:26:06 UTC and returns `changed-under-evidence` before
its09:56 UTC ceiling. No old experiment, install, publication, push,
foreground action or manual wake queue. Qwen remains unavailable without
retry. No research process is left running at this checkpoint. The overall
goal remains active, with no claim of execution during pauses.

The next pursuit, **90488ef**, saves the SAME unbalanced MODEL box for
EVERY integer modulus, in `all_moduli_unbalanced_kernel.py`. The repeated
prime factors stay in the factor r preserved by divisor shifts; only its
coprime complement s needs to be squarefree. This uses the existing
all-prime-power pointwise bound and avoids the failed residue-split cost.
For full squarefull part U(q)<=q^(2/5), the corrected classification gives
r in[q^(1/32),q^(69/160)] or a small factor with one/two large simple
primes left. Independent review caught the missing transition cases in
the proposed narrower2/5 upper limit. The wider range still saves1/256.

All integer multipliers and prime-power zero patterns are included by the
exact recursion G_e=K_(p^e)(hlt)+p*1_(p|h,l,t)*G_(e-1), ending at the
retained prime identity. Its terms pay volume massD^-1 and fixed-h norm
massD^-1/2, up to divisor factors. The exact period lift costs J^4;
arbitrary-position second intervals and periods sharing q are paid.
Using U(q)<=q^(39/100) as the good-modulus cutoff gives
 Y^(1-1/512+epsilon)*J0^(7/2)*H^(3/2).
The remaining O(C^(161/200)) moduli use squarefull density and the
retained pointwise bound. Axes and overlap remain included. At the full
H,J0 caps the good exponent is1-3/4096 and the theorem is1-1/4096.
The preceding squarefull-residue budget remains a valid failed route.

A separate retained component proves the prime-square four-factor bound
<=108p for p>=5 and p not dividing a(u-v), uniformly in the Fourier
twist. It comes from the exact unit-cube-root formula for K_(p^2), a
tangent stationary equation and a degree<=12 polynomial with nonzero
constant on each of at most9 branches. Explicit p=113 witnesses show
both exceptional families can exceed108p. This component is promising
but not needed by the all-integer MODEL proof.

Nine NEW exact tests passed normally in0.195s and under -O in0.151s.
Sol `/root/sieve_review` passed the derivation, corrected classification,
actual files, interval transfer, recursion, exponent costs and fixtures.
This pursuit began09:51:06 UTC and returns `changed-under-evidence`
before its10:21 UTC ceiling. No old experiment or outside action occurred.
Qwen remains unavailable without retry; no manual wake was queued.
Next question: does the exact envelope of combined reviewed model bounds
cover the canonical hyperbola-box domain, or which explicit box remains?
Pay all period/frequency caps and source support conditions in that test.
Full box coverage, original sieve transfer and signed prime correlation
remain OPEN; latest original-affine stays2b8cf98, formal conservation
6f9a77b stays distinct from the signed gap, and polynomial tools survive.
No research process is left running at this checkpoint. The overall goal
remains active, without claiming work during execution gaps.


The next pursuit, **220920c**, closes the smooth MODEL box geometry:
`full_model_box_kernel.py` proves sum_q|E_q|<<Y^(1-1/4096+epsilon)
for ALL integer moduli throughout 1/5<=b<=13/25,
0<=x<=(1-b)/2,0<=y<=1/2, with the stated full period/frequency caps,
nonunit modes, integer axes and overlap. This is not sieve transfer.

Swapping the balanced grouping gives a broad regional theorem with
bare exponent<=63/64 and a paid squarefull cutoff Z=Y^(1/256). The
residual strip requires two new transfers: rectangular divisor shifts
with an arbitrary coupled periodic local factor, and exact grouping of
the completed h,k variables after fixing kappa modulo J. The local
factor remains periodic mod rJ even when q and J share primes. The
prime/two-prime core amplification also retains unequal interval lengths.
The total period cost is J^5; no coupled weight is separated for free.

The grouped recursion L2 mass is merely bounded, not D^-1/2. Small
divisors use the nonnegative modulus powers of the rectangular bounds;
large divisors use their volume1/D. Complementary simple-prime nonunit
partitions pay1/Ds and preserve the local period. The critical residual
exponents at full caps are1-(19/8)/4096,1-(81/16)/4096 and1-2/4096,
all below the uniform claim. Earlier failed combinations and the
prime-square component remain available with their original boundaries.

Eight NEW exact checks passed normally in0.148s and under -O in0.134s.
Sol `/root/sieve_review` passed the theory and actual proof/code/tests.
The checks cover shared periods/nonunit kappa, grouped mass=1 witnesses,
rectangular moment normalization, exact supports/costs and domain cuts.
This pursuit began10:15:59 UTC and returns `changed-under-evidence`
before its10:45:59 ceiling. No old experiment or outside action occurred;
Qwen remains unavailable without retry and no manual wake was queued.

The next test concerns actual arithmetic: can a positive upper-sieve
majorant of a weaker fixed-power cofactor roughness condition preserve
harmonic density while fitting all original sieve-index, period and
frequency costs within the saving? The actual family allows an arbitrary
rough subset, so direct treatment as a smooth/short-period weight is
invalid. Test positivity, density, M's coprimality/discriminant cases
and amplitude regularity explicitly before transferring the theorem.
Original sieve transfer and signed prime correlation remain OPEN;
latest original-affine remains2b8cf98 and formal conservation6f9a77b
still leaves its signed difference unestimated. Polynomial tools survive.
No research process is left running at this checkpoint. The overall goal
remains active, without claiming work during execution gaps.

## 2026-09-09: positive cofactor sieve transfers the full affine range

Started10:43:21 UTC; reassessed before11:13:21, `changed-under-evidence`.
Resumed clean main53eeab1 and model mathematics220920c. New reviewed
mathematics **4e106b6**, `rough_cofactor_sieve_bridge.py`, extends the
ACTUAL rare/rare affine bound to every original rough subset M<=Y^(13/25),
with gcd(M,Dm)=1, in the SAME actual-zero large-V regime. Its bound is
 S_2(m)Yt^2(log eta)^9+Y^(1-rho/2+o(1))+S_2(m)Y eta^-19=o_theta(Yt),
rho=2^-20. It does not supply the missing signed prime estimate.

The concrete test passed: upper-beta positivity plus a NEW weighted mean
sum_(M~B)sigma(M)F_C(M)<<B/log z+R sqrt B yields O(U) harmonic mass.
Small prime factors admitted by sigma are paid by F_C(M), not silently
excluded. Corrected Henriot tails retain exact gcd(M,m)=1 and primitive
forms. The zero mode keeps sigma and has two harmonic cancellations.
Actual nonzero modes have q0=d2*c, conductor D, physical M,a, bounded
periodic character factors and uniformly smooth Fourier amplitudes.
Rescaling Ystar=YR^2 pays Hstar<=DR^4,J<=DR^5 and five indices R^5.
The target-gcd tail costs Y^(1-rho+epsilon), including its zero counterpart.

Independent review required native (M,q0)=1 in every truncated Mobius term;
it is now explicit, along with (M,D)=1. Exact CRT signs agree in both
phases. The inherited Y^(1-theta+o(1)) term is absorbed into Y eta^-20 for
each fixed theta; no theta>=rho/2 condition is assumed.
Primary source correction: MM2112.11412v2 equation(22) must use PLUS its
upper-beta remainder. Exact witness1/3=8/35+11/105; relative-O lemma valid.

Nine new exact guards passed normally0.024s and under -O0.017s. Sol
`/root/sieve_review` reviewed theory and actual proof/code/tests, PASS.
No repeated prime scan, outside action, publication, or manual wake queue.
Qwen remains unavailable without retry. Only coherent local commits.

Next question: does the new bound cover every previously surviving even
one-rare-factor composite under the original pruning and fixed polynomial
weights? Test exact cofactor/character coverage and parameter compatibility;
preserve any missing boundary or class instead of assuming it away.
Formal conservation6f9a77b remains a known-main-term identity, with its
signed difference OPEN. Polynomial tools survive and the goal stays active.
No research process is left running; execution gaps remain gaps.

## 2026-09-09: eliminate all polynomial rare-factor losses

Started11:12:52 UTC, reassessed before11:42:52, changed-under-evidence.
Resumed clean main ddfa2aa, actual affine mathematics4e106b6. New reviewed
mathematics **e5c955d**, rare_class_elimination.py, proves for EVERY fixed
normalized polynomial of degree d, in the ADDED actual-zero large-V regime,
 T_f=P+sum_(3<=k<=d, k odd) C_(k,f)^all-negative+o_(f,theta)(Yt).
Every positive-factor composite class is negligible in FULL ABSOLUTE
weight. The quintic now leaves only pure triples and five-factor partners.
The original W=chi*log has T_W=P+E with 0<=E=o_theta(Yt); normalized
quadratics coincide with W exactly on negative-character units.

The old pruning only used the fixed rough divisor bound. Remaining unique
positive q>floor(Y^a) gives q>Y^a exactly, M=n/q<Y^(1-a)<=Y^(13/25),
chi(M)=-1, (M,Dm)=1 and the exact bridge intervals. Q-dependent restrictions
are dominated by the full nonnegative B_M. Never use the false reciprocal
floor inequality. V>=log^3 eta stays an additional assumption; the original
fixed delta,u and B_good are unchanged.

The Buchstab terminal error E_R is also o(Yt), removing its previous
C*epsilon*Z charge. The remaining one-sided prime-times-rough estimate is
 U_A<=LXV(z_old)-(c+C0*eta_u/theta)*Z,
with the original fixed sieve error and >=q least-factor condition intact.
This estimate and a positive lower bound for FULL T_W remain OPEN.
The exact n=957,R=26 fixture has truncated W=log(33/29)>0 and full W=0,
so nonnegativity of W cannot make its signed truncation a lower bound.

Seven new guards passed normally0.023s and under -O0.021s. Sol reviewed
actual proof/code/tests, PASS after an eta_u notation correction. Finite
S2,S4,S6 character fixtures verify support, not an exceptional zero or
prime coverage. No old experiment, outside action, publication or wake queue.

Next UNTESTED question: compare lambda_chi(p)*W(m-p) with one-variable
rare-prime lambda_chi mass. Its zero mode may pair A_z(p) with the weighted
log moment B_z(m-p); MM Lemma2.4 might calibrate B_z without discarding
A_z. The decisive tests are exact local normalization and relative Yt
errors in prime-to-divisor replacement and sieve tails. Existing errors
of order Yt times logarithmic factors would not suffice for a lower bound.
Keep original fixed-theta and growing-U cutoffs distinct. No new signed
estimate is claimed, and formal conservation6f9a77b remains only its
proved identity. All polynomial components survive. Goal active; no
process remains running and no work is claimed during execution gaps.

## 2026-09-09: actual divisor correlation and the cutoff comparison

Started11:34:38 UTC, reassessed11:58 UTC, changed-under-evidence.
Resumed clean main e436401, mathematics e5c955d. New reviewed mathematics
**2b72af7**, rare_divisor_calibration.py, proves in the SAME ADDED actual-zero
large-V regime, for central suppressed targets and fixed smooth g,
 S_z=G_z Q_z+o(Yt)=S_2(m)t I_g+o(Yt),
with U=K log eta, z=Y^(1/U). This is an actual nonnegative divisor sum.
Q_z=(A/phi(D))t I_g+o(Yt/G_z) is calibrated by one-variable rare primes.
Exact G_z=Sigma_(2,z)phi(D)/A, with the tail1+O(U/z). The four conductor
orientations produce A_z B_z, MM Lemma2.4 gives B_z=2C_z(1+O(E)),
A_z=O(E/U), and the replacement costs S_2 Y E^2=o(Yt). The outside1/2,
Abel factor2, atom1, and absolute signed-integral error are all retained.

Dynamic Q_z composite mass is relatively small by its unique largest
positive prime. This is NOT a dynamic S_z prime-replacement theorem.
Separately, ORIGINAL fixed theta permits first-variable replacement via
an upper prime sieve at modulus Dd, never MDd. Explicit FULL/B_good
pruning control and e5c955d then give S_theta=P_g+o(Yt), with factors
strictly>z_old and equality endpoints paid. Growing-U divisor costs2^U
and fixed-theta sieve errors prevent silently composing the two results.
The difference S_z-S_theta and a positive prime-pair lower bound remain OPEN.

Seven new finite algebra guards passed normal0.008s and -O0.007s. Sol
/root/sieve_review checked theory, actual files, strict endpoints and pool
composition, PASS. No finite test is an exceptional-zero or asymptotic proof.
MM equation22 PLUS correction, corrected Henriot, and Thorner--Zaman bulk
source remain in force. No old experiment, outside action or wake queue.

Next UNPROVED test: expose a prime r in[z,z_old] in S_z-S_theta. Positive
r produces affine lambda/W forms with SMALL coefficient r and one harmonic
cancellation; its reciprocal prime mass may supply a second rarity factor.
Negative r on nonzero squarefree W support produces lambda/lambda and two
harmonic cancellations. Test the DIRECT small-cofactor Poisson proof for
both placements and sum all errors: Q>=Y^(1-theta), r prime, theta<1/5,
prospective nonzero cost Y^(7/9+theta+o(1)). Preserve any failing term.
This comparison could avoid the unproved very-short-interval W estimate;
it has not yet been established. Use a new <=30-minute hypothesis clock.
Kevin reiterated freedom to incorporate other mathematical approaches.
No historical priority, prize entitlement, cash or universal coverage claim.
Overall goal active. No research process remains running at the checkpoint;
execution gaps remain gaps, and all polynomial components stay available.

## 2026-09-09: cutoff bridge and conditional coverage of an entire band

Started11:59:43 UTC, reassessed12:14 UTC, changed-under-evidence.
Resumed clean main1e71488, mathematics2b72af7. New reviewed mathematics
**9b6e7b4**, prime_cutoff_bridge.py, proves S_z-S_theta=o_theta(Yt), hence
 P_g=S_2(m)t I_g+o_theta(Yt)
for suppressed targets in the SAME actual-zero restricted large-V regime.
The explicit cutoff error is S_2Yt^2U^8log(2U)+Y^(7/9+theta+o(1))
+S_2Y eta^-20. This is an ACTUAL prime-pair asymptotic, distinct from
formal conservation6f9a77b. Its proof retains the original fixed parameters.

An intermediate prime r in[z,z_old] yields three nonnegative union cases.
Positive r on either side produces an affine lambda/W sum; one harmonic
cancellation and the positive-prime reciprocal mass O(t) supply two rarity
factors. Negative r on nonzero W support produces lambda/lambda and two
harmonic cancellations, with reciprocal loss O(log U). Since r is small,
Q=Y/r>>Y^(4/5); the direct Poisson proof handles both W placements at
modulus Dd2c. Native(r,d2c)=1 remains until the zero mode. The prior
cofactor theorem's stronger roughness hypothesis is replaced by an explicit
prime-coefficient adaptation, not assumed away. Dynamic removals retain
Y/z exp(O(U))L^C, rather than an unjustified fixed-power slogan.

The source main multiplier1+C/A equals zero precisely on F_D and is >=2/3
otherwise. Its CRT proof explicitly includes a vanishing8-part. MM
Theorem1.4 therefore covers the nonsuppressed classes with relative o(1)
error; proper prime powers cost O(sqrt(m)log^3m). That theorem has NO
upper-V restriction. Combining the two cases proves a prime representation
for EVERY even m in[5Y/4,7Y/4], conditional on the stated ACTUAL zero and
eligible parameter regime. The nonsuppressed pair need not lie in(Y/2,Y].
No eligible zero, numerical interval, effective onset, unconditional coverage
or historical novelty has been established. Other zero regimes and the
unexceptional branch remain outside this theorem; overall Goldbach is OPEN.

Nine new exact tests passed normal0.021s and -O0.021s. Sol checked theory,
actual proof/code/tests and coverage corollary, PASS. Source corrections and
runtime limits persist; no scan, publication, contact, spend or wake queue.

Next UNTESTED question: derive the exact Mobius-weighted Type II remainder
in the unexceptional ramanujan_type_i.py comparison, using Vaughan's
identity, and test whether the existing all-moduli reciprocal kernel can
handle its actual large-factor weights. The model only promises smooth
spatial factors and bounded joint periodic weights; arbitrary Mobius or
divisor coefficients may fall outside it. Cost every norm/frequency loss
before claiming a transfer, or preserve the specific remaining correlation.
Do not rerun completed smooth-model cases or discard polynomial tools.
This lane needs a new <=30-minute hypothesis and independent review.
Goal active; no research process remains running at the checkpoint.

## 2026-09-09: unexceptional Vaughan remainder and coefficient-transfer boundary

Started12:16:10 UTC, reassessed12:29 UTC, changed-under-evidence. Resumed
clean maince40960; conditional coverage9b6e7b4 remains valid. New reviewed
mathematics **a771937**, unexceptional_vaughan_gate.py, isolates
 T=sum_(ab in J,a>V0,b>U0)mu(a)B_U0(b)E(m-ab),
with B_U0=Lambda_>U0*1 and the original unexceptional E=Lambda-M_S.
Both Type I terms and proper prime powers are paid. CROSS+T gives actual
prime-pair mass, but T has NO proved sufficient lower bound.

Generic completion does not transfer the existing model: its sharp
worst-case sqrt(N) coefficient cost exceeds the saved Y^(1/4096), even
if one grants uniform additive-modulation bounds the theorem does not state.
This says nothing about a lower bound for actual Mobius/divisor Fourier
norms. Vaughan's free1 must stay; a finite n=30 guard catches its omission.
Cauchy isolates signed prime/model covariance with exact intersection masks.
Its diagonal is already negligible by a fixed power; only a sufficiently
small one-sided upper bound on the weighted off-diagonal is needed.

Nine finite guards passed normal0.008s and -O0.008s. Sol reviewed theory,
actual proof/code/tests and diagonal delta, PASS. No old scan or outside action.
Next test: keep the free divisor variable explicit in the multilinear
Vaughan terms and attempt a LEGAL Poisson/dispersion transfer, accounting
for every short-variable region including k=1. Full arithmetic Type II,
not its smooth/periodic replacement, is the target. Use a new <=30-minute
clock; preserve any remaining correlation. No unexceptional coverage is
claimed. Goal stays active; no process remains running at this checkpoint.

## 2026-09-09: actual balanced divisor convolution with free variables

Started12:30:54 UTC, reassessed12:45:47 UTC, changed-under-evidence.
Resumed clean main5842cd2. Reviewed mathematics **a968833**, in
free_divisor_correlation.py, retains the exact grouping
 h_r=sum_(ad=r,a>W,d>W)mu(a)Lambda(d), |h_r|<=log r,
 T=sum_(rk in J)h_r E(m-rk).
The tiny floor strip r<=Y^gamma is Type I; larger r with k=1 persists.
Merely keeping that k does not license the saved smooth-model input.

A changed grouping gives a POSITIVE component: after expanding Vaughan
on both sides, for coefficient scales Y^gamma<=R,S<=Y^(51/100), fixed
smooth F and actual separate coefficients bounded by log(2Y),
 sum_(Mk+Nl=m)alpha_M beta_N F(Mk/Y,Nl/Y)
  =Y I_F(m/Y)sum_(gcd(M,N)|m)alpha_M beta_N gcd(M,N)/(MN)
    +O_(F,epsilon)(Y^(1983/2000+epsilon)).
This applies to the arithmetic h_M,h_N themselves. Poisson acts only on
the free k variable; a fixed-box Mellin expansion separates the smooth
coupled factor while preserving the outside arithmetic coefficient norms.
Bettin--Chandee Theorem1 then applies directly. Both source terms, gcd
conditions and divisors of m, negative frequencies, unit reduced variables,
small-frequency padding and the Schwartz tail are explicitly included.
The two worst exponents are1983/2000 and153/160, a17/2000 margin.

This is a restricted ACTUAL coefficient convolution, beyond the prior
smooth/periodic model input. Its SIGNED gcd main is still explicit. No
positive prime main, bound on all larger factors or mixed terms, or full
unexceptional T=o(Y) follows. Conditional coverage9b6e7b4 and previous
polynomial/model components remain unchanged. In particular, the failed
old cofactor grouping and generic Fourier-completion budgets are preserved
as method-specific limits, not broad impossibility assertions.

Eight exact guards passed normal0.003s and -O0.002s. Sol reviewed theory
and the actual proof/code/tests, PASS. No scan, publishing or other outside
action occurred. Next bounded question: compare the signed gcd main with
the small-modulus Ramanujan projection of the same coefficients. The test
must pay the q>Y^delta tail and check whether an actual term of T cancels;
an exact main-term rewrite alone will not close the remaining estimate.
Keep all large-product and mixed remainders explicit, and start a fresh
<=30-minute clock. Goal active; no process remains running at checkpoint.

## 2026-09-09: balanced self-correlation removed by an actual Type I transfer

Started12:47:52 UTC, reassessed12:58:25 UTC, changed-under-evidence.
Resumed clean main7eff067. Reviewed mathematics **476e0c3**, in
balanced_projection_transfer.py, composesa968833 with the earlier TI input.
For B(n)=sum_(r|n,Y^gamma<r<=Y^.51)h_r, its exact Ramanujan coefficients
H_B(q)=sum_(q|r)h_r/r satisfy |H_B(q)|<<L^2/q. Set Q=floor(S^2),
P_Q=sum_(q<=Q)H_B(q)c_q and Z=B-P_Q. The signed gcd main has exact
coefficient sum sum_q c_q(m)H_B(q)^2; its tail is <<L^4tau(m)/Q.
Matching BB, BP, PB and PP mains and paying all interval errors gives
 |C_F(Z,Z)|<<Y^(1983/2000+epsilon)+YL^4tau(m)/Q
               +Y^.51 L^3Q^2+L^4Q^4
           <<Y^(1-2delta+epsilon)
for fixed smooth F. This is an ACTUAL self-correlation bound.

The initial idea that P_Q might equal Gamma_S is unnecessary and is not
asserted. Its coefficients differ from the prime model. Crucially P_Q
itself has exact divisor coefficients p_d<<L^3 supported on d<=Q<=Y^gamma,
so the existing TI estimate bounds C_F(P_Q,E) by every fixed logarithmic
saving with E unchanged. For A=VaughanII, H=A-B and R=E-Z,
 T_F=C_F(A,E)=C_F(Z,R)+C_F(H,E)+C_F(Z,Z)+C_F(P_Q,E).
Thus only the first two correlations remain after the proved small terms
are removed. R retains all mixed terms and P_Q-Gamma_S. No Cauchy or sign
claim is inferred from a small additive self-correlation. The TI error
remains logarithmic, separate from the power-saving self-correlation.

For n=pq, distinct primes p,q>W, only h_n=-log n is nonzero among h_r
with r|n; for n=p^2, h_n=-log p. When n is comparable to Y these k=1
terms remain entirely in H. No unexceptional prime lower bound, new
coverage or sharp-cutoff upgrade follows. Earlier conditional coverage,
polynomial identities and analytic components remain intact.

Eight guards passed normal0.009s and -O0.010s. Sol theory/actual-file
review PASS. No previous experiment, scan or outside action was repeated.
Next test: verify a multi-factor prime identity from a primary source and
ask whether it supplies new long free variables in the remaining H.
Use the complete factor-size domain, including all-short-free-variable
terms, as the falsifier; retain actual Mobius/log coefficients and cost
every reciprocal-estimate norm. A formal decomposition alone is not the
missing estimate. Start a fresh <=30-minute clock with independent review.
Goal active; no process remains running at this checkpoint.

## 2026-09-09: multi-factor identity boundary and divisor-weighted Type I

Started13:01:48 UTC, reassessed13:16:56 UTC, changed-under-evidence.
Resumed clean main29b35c9. Reviewed mathematics **b7134e1**, in
multifactor_identity_gate.py, adds the actual unexceptional estimate
 sum_(d<=Y^gamma)tau_s(d)L^b Delta_d <<_(A,s,b)Y/L^A
for FIXED divisor order s and log power b. The proof combines
Delta_d<<YL tau(d)/d+S^4 with tau_s^2 tau_2<=tau_(2s^2) and Cauchy;
the input TI saving2(A+b)+2s^2+1 pays the whole coefficient moment.
This preserves a useful extension for actual grouped arithmetic weights.

The Heath-Brown identity was verified from Tao's2013 subset-sum post and
proved with its exact residual mu_>z^{*K}*1^{*(K-1)}*log. The residual
vanishes below2(z+1)^K, but at K2,z2,n18 equals+log2. A raw top-order
term can have all Mobius variables of scaleY^(1/K) and all free variables
bounded: Y=3p^K, n=2p^K, log variable2 gives the nonzero tuple -log2.
Thus the identity plus TERMWISE application of existing TI/free-variable
BC bounds does not cover every factor box. Grouping Mobius factors into
balanced products retains arithmetic weights; it does not create a free
variable. The optimistic r=s=1 source budgets9/5 and15/8 also fail.

The raw witness cancels in the FULL identity at that composite n. It is
not a lower bound for actual H, a Goldbach counterexample, or a barrier
to cross-term cancellation. Some squarefree smooth inputs already have
original Vaughan A=0. Source MPZ distribution estimates are not our
pointwise correlation input, and no excluded or blocked old route was reused.

Useful restricted components remain: genuine free factors of scale
>=Y^(1-gamma+eta) are controlled by divisor-weighted TI; paired terms
with one original free1 per side and complementary products in the saved
[Y^gamma,Y^.51] range admit the BC proof with fixed divisor-moment norms.
The reviewer corrected a coefficient description: leaving log free removes
the grouped coefficient's L, but its safe divisor order remains2j-1;
the free log variation is paid separately. All parameters remain fixed.

Eight guards passed normal0.006s and -O0.005s. Sol theory/actual-file
review PASS after that correction. No coverage, scan or outside action.
Next test: combine specific HB terms before absolute estimates, derive the
short-free coefficient, and check whether its cancellation gives a bound
against the unchanged E. A reconstruction of Lambda or a prime/roughness
support restriction alone is insufficient. Preserve the exact unresolved
signed correlation if no new estimate results; do not discard the useful
divisor-weighted TI or earlier polynomial/model components. Use a fresh
<=30-minute clock and independent review. Goal active; no research process
remains running at this checkpoint.

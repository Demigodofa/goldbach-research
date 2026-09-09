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

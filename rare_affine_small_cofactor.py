"""Negligible rare/rare affine pairs for a proved small-cofactor range.

Owner: Kevin's Goldbach research. Purpose: extend the actual arithmetic
component in rare_shifted_divisor_bound.py to part of the REQUIRED forms
p=m-M*q, while recording why the full M<=Y^(13/25) range remains open.
No assertion of an actual exceptional zero, effective onset, or novelty.

Theorem (conditional; NEW large-V regime retained):
Fix 0<theta<1/5. Let chi be primitive quadratic modulo D>24 with an ACTUAL
real zero beta=1-1/(eta*log D), eta sufficiently large. Write
  Y=D^V, V>=(log eta)^3, L=log Y, t=V/eta<=1/L.
For an even integer m in[Y,2Y], let C be ANY subset of the integers
  2<=M<=Y^(1/5), P^-(M)>Y^theta, gcd(M,D*m)=1.
Squarefreeness and a prime-factor count restriction are unnecessary.
Let B_M sum log(q)*log(p) over actual primes
  Y/(2M)<q<=Y/M, Y/2<p=m-M*q<=Y, chi(q)=chi(p)=+1.
Then, uniformly over this family and m,
  sum_(M in C) B_M
    <<_theta S_2(m)*Y*t^2*(log eta)^8
         + Y^(44/45+o(1)) + Y^(1-theta+o(1))
         + S_2(m)*Y*eta^-20
     = o_theta(Y*t).                                      (1)
All limits here are as eta tends to infinity in the stated regime. The
power-saving remainders retain their own meaning; no fixed-u estimate from
an earlier module is silently turned into a growing-u assertion.

Sources and proof boundary:
This is a DIRECT ADAPTATION of Matomaki--Merikoski Proposition2.3's proof,
especially equations(33)-(39), Lemmas3.2-3.3 and3.8, and Lemma2.4:
https://arxiv.org/html/2112.11412v2 . Proposition2.3 itself does NOT state
our affine theorem. Its affine changes are supplied below. The divisor-
bounded sieve tails use Henriot's corrected NEW Theorem5, printed p377:
https://doi.org/10.1017/S0305004114000280 , with the corrected exact-valuation
conditions(0.1)-(0.2), as already recorded in multi_rare_partner.py. The
function-class definitions are in https://arxiv.org/pdf/1102.1643 . Do not
substitute an uncorrected leading-coefficient/discriminant corollary.

1. Family bounds and parameters.
   Omega(M)<=1/(5theta), tau(M)<=2^(1/(5theta)), and
     sum_(M in C)1/M <= product_(Y^theta<r<=Y^(1/5),prime)(1-1/r)^-1
                      =O_theta(1).                       (2)
   Fix large A,K with AK/3000>100 and the corresponding fixed beta-sieve
   parameter. Put U=K*log eta, z=Y^(1/U), sieve level R=Y^(1/1000).
   Eventually U>=1000*beta_sieve and D<z<Y^theta. Here P(z) includes
   primes STRICTLY BELOW z. Every M is coprime to P(z). Set Q=Y/M>=Y^(4/5).
   Use a fixed smooth nonnegative majorant g(q/Q,p/Y), equal to1 on
   [1/2,1]^2, supported in[2/5,11/10]^2. All derivatives are fixed.
   With lambda=1*chi>=0, lambda(r)=2 at a positive-character prime,
     B_M << L^2 sum_(q,p=m-Mq; (qp,P(z))=1) g(q/Q,p/Y)lambda(q)lambda(p).
   No prime-to-divisor replacement error is imported from the source.

2. Expand the same smooth hyperbola identity used in the previous module:
     lambda(n)=sum_(ab=n) H(a/b)*(chi(a)+chi(b)),
   H(s)+H(1/s)=1, H=1 for s<=1/2, H=0 for s>=2, H smooth.
   For q=ab and p=cd this has a<<sqrt Q, c<<sqrt Y. Partition a,c smoothly;
   there are O(L^2) boxes, a~A1,c~A2, b~N1=Q/A1,d~N2=Y/A2.
   In each of four orientations, characters on a,b and c,d are chi,chi0
   in one order or the other. Each small-factor product is chi(a),chi(c).

3. The affine Poisson step, rather than a substitution into lambda(Mq).
   Make d implicit in M*a*b+c*d=m. As in source(33), after inserting
   three beta-sieve weights e,d1,d2<=R the relevant congruence is
     M*e*a*d1*b == m (mod d2*c).
   gcd(M,m)=1 forces gcd(M,d2*c)=1 on actual summands; d2's primes are
   below z and cannot divide M. The same removals as the source permit
   gcd(e*a*d1,d2*c)=1 and gcd(e*a*d1*d2*c,D)=1.
   Poisson summation has modulus D*d2*c, NOT D*M*d2*c. In source(35) the
   inverse phase simply gains the unit factor inverse(M) modulo d2*c.
   The integral variable y=q has length Q; its second form is m-M*y.
   Its derivative scale M/Y=1/Q agrees with that of the first form.
   Thus the frequency cutoff is
     |k| << Y^epsilon * D*d1*d2*A1*A2/Q.                 (3)
   Splitting a into classes modulo D, source Lemma3.8 applies with the
   coefficient M included in its invertible parameter e. This causes NO
   modulus enlargement. Its bound is
     (d2*c)^(1/2+epsilon) + A1*gcd(m*k,d2*c)/(e*d2*c*D),
   up to fixed smooth constants. Source(39)'s length Q cancels (3)'s 1/Q.
   Summing the three sieve indices and c therefore gives
     O(D^2*R^(7/2)*Y^(3/4+o(1)) + D*R*sqrt(Q)*Y^o(1))
       = O(D^2*Y^(7/9+o(1)))                            (4)
   per box. O(L^2) boxes and L^2 prime logs are included in Y^o(1).
   The affine coefficient is harmless here as a unit phase; the much
   larger p-scale, compared with Q, is the reason (4) can be inadequate.

4. Uniform arithmetic and sieve errors needed in that adaptation.
   On the original z-rough support, lambda(q)lambda(p)<=exp(O(U)), a
   fixed power of eta. A common prime r|q,p divides m and has r>=z.
   Counting its q-multiples costs O(Q/r+1); there are O(U) such r|m and
   sum 1/r=O(U/z). Since log z>>log^2 eta, L<=eta, and Q>=Y^(4/5),
   shared-factor removal costs Q*eta^-B for ANY fixed B, after fixed logs.
   This handles the large primes dividing m without applying Henriot at
   an unjustified tiny scale Q/r. Choose B large enough for all later sums.

   The relaxed beta-sieve tails collapse to divisor-bounded affine forms
   n and m-M*n, exactly as in the proof of source(15), with fixed powers
   of tau and possibly different roughness cutoffs. Apply corrected
   Henriot directly: polynomial product norm<=3Y, interval x comparable
   to Q>=Y^(4/5), alpha=1/2, norm exponent1/4, and sufficiently small fixed
   function-class epsilon. A fixed divisor power has the required bound
   tau(n)^j<=C_(epsilon,j)*n^epsilon; the rough indicators preserve it.
   Uniformity in the coefficient follows from the corrected local counts:
   for r|M, the second form has NO root, and all such r>Y^theta. Their
   residual factors are 1+O_A(1/r), with O_theta(1) factors. At r|m,
   use the common-root factors and P_m cutoffs exactly as in source(15).
   The tail bound is consequently
     O_(A,theta)(S_2(m)*Q/L^2 * exp(-A*U/3000)),
   with the source's additional O(S_2(m)*Q/L^2*U^6/z).
   All finite smoothing, box and logarithm losses are absorbed by choosing
   A,K as above; the resulting Q-scale errors are O_theta(S_2(m)*Q*eta^-20).

5. Zero mode and TWO harmonic cancellations.
   For each M, summing all four orientations and all dyadic MAIN terms
   BEFORE absolute values gives
     V_(m,D)(z)*K_(m,M)(D)*integral g(y/Q,(m-My)/Y)
                                          A_z(y)*A_z(m-My)dy,           (5)
   apart from the coprimality-removal errors just specified, where
     K_(m,M)(D)=D^-1 sum_v(chi0+chi)(v)*(chi0+chi)(m-Mv),
     A_z(y)=sum_(d coprime P(z)) chi(d)/d*H(d^2/y).
   V_(m,D)(z) is the previous two-root product omitting conductor primes.
   The remaining condition gcd(c,M)=1 may be removed at harmonic cost
   O_theta(L^O(1)*Y^-theta), since sum_(r|M)1/r=O_theta(Y^-theta).
   The other shared-small-divisor removals have the usual 1/z cost. These
   statements concern the zero-mode sums, not a presumed independence law.

   To verify its normalization directly, for coprime a,c with
   gcd(M*a,c)=gcd(M*a*c,D)=1, average the four orientation weights over
   b modulo cD subject to c|(m-Mab), then divide by a. The EXACT result is
     chi(a)*chi(c)/(a*c) * K_(m,M)(D).                  (6)
   This follows by the substitutions v=a*b modulo D and d=(m-Mab)/c.
   The finite verifier below tests(6), including its 1/a Jacobian.

   Multiplication by M permutes D-units, so K_(m,M)<=4*A_D(m)/D.
   Restoring conductor primes gives (A_D(m)/D)*V_(m,D)(z)
     << S_2(m)*U^2/L^2.
   Lemma2.4 at base Y, subtracted at its y=Y and y=Y^2, gives
   sum_(d<=N,rough)chi(d)/d=O(E/U), E=O(t*U^4)+O(eta^-20).
   Both H transition endpoints, sqrt(Q) and sqrt(Y), belong to
   [Y^(1/10),Y^2]; Abel summation bounds BOTH A_z factors by O(E/U).
   Thus (5), after prime logs, is O(S_2(m)*Q*t^2*log^8 eta)
   plus O(S_2(m)*Q*eta^-20). This proves the per-M main used in(1).

6. Sum the errors and state exactly what has been achieved.
   Equation(2) sums the main and Q-scale tails. There are at most Y^(1/5)
   coefficients, so(4) totals D^2*Y^(44/45+o(1)). Coprimality removal in
   (5) totals Y^(1-theta+o(1)). Since V>=log^3 eta, D=Y^o(1), eta=Y^o(1),
   and t>=1/eta=Y^-o(1). These are genuine power savings relative to Y*t.
   Also tL<=1 implies L<=eta, t<=1/sqrt(eta*log D), and
   S_2(m)<<log L<=log eta. Therefore every term in(1) is o(Y*t).

   The surviving even quintic classes have M=n/q rough at the original
   cutoff, gcd(M,Dm)=1 and chi(M)=-1. For any fixed polynomial kernel,
   |K_f(n)|<<_(f,theta)L and log q comparable to L in this range. Hence
   their FULL ABSOLUTE contribution with M<=Y^(1/5) is o_(f,theta)(Y*t).
   This is a small arithmetic loss for part of the actual problem, and
   can be combined with the preserved polynomial tools. It supplies no
   positive lower bound for the full total and does not remove all-negative
   odd composite classes or the larger even-class cofactors.

Why this proof does not reach M<=Y^(13/25):
Ignoring small sieve, conductor and logarithmic losses, direct Weil costs
Y^(3/4) per M, versus a desired scale Y/M. Reversing the eliminated form
introduces modulus M*d2*c and the corresponding ideal cost
Y^(3/4)*M^(-1/4). Summed up to M=Y^alpha, these budgets are respectively
Y^(3/4+alpha) and Y^(3/4+3alpha/4). At alpha=13/25 even the reverse budget
is Y^(57/50), above Y. These are upper-bound METHOD budgets, never lower
bounds, counterexamples, or no-go theorems. The reversed full affine theorem
has not been promoted here. For the direct proved rounding7/9, alpha1/5
leaves margin1/45. Reaching the actual larger range needs a new estimate,
for example cancellation across cofactors before absolute values.

Tests check exact residues, character orientations and exponent arithmetic,
not an infinite prime sum, an exceptional zero, or any effective onset.
"""
from fractions import Fraction
from math import gcd

from exceptional_character_model import character_values


def _positive(value, name):
    if type(value) is not int or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def affine_residue_factor(conductor: int, multiplier: int, target: int):
    """Exact (K_(target,multiplier), unit-pair density); no prime model."""
    _positive(multiplier, "multiplier")
    _positive(target, "target")
    chi = character_values(conductor)
    if gcd(multiplier, conductor) != 1:
        raise ValueError("multiplier must be a conductor unit")
    units = positives = 0
    for a in range(conductor):
        b = (target-multiplier*a) % conductor
        units += gcd(a, conductor) == gcd(b, conductor) == 1
        positives += chi[a] == chi[b] == 1
    return Fraction(4*positives, conductor), Fraction(units, conductor)


def affine_orientation_densities(conductor: int, multiplier: int, target: int,
                                 first_divisor: int, second_divisor: int):
    """Four complete local densities, including the 1/a Jacobian in(6).

    This enumerates a FINITE residue period; it is not an asymptotic formula.
    Orientation0 puts chi on the small factor, orientation1 on the large.
    """
    for value, name in ((multiplier, "multiplier"), (target, "target"),
                        (first_divisor, "first_divisor"),
                        (second_divisor, "second_divisor")):
        _positive(value, name)
    chi = character_values(conductor)
    a, c = first_divisor, second_divisor
    if gcd(multiplier*a, c) != 1 or gcd(multiplier*a*c, conductor) != 1:
        raise ValueError("require invertible coefficient and conductor-unit divisors")
    chi0 = tuple(int(gcd(v, conductor) == 1) for v in range(conductor))
    characters = (chi, chi0)
    result = []
    for orientation1 in (0, 1):
        for orientation2 in (0, 1):
            total = 0
            for b in range(c*conductor):
                numerator = target-multiplier*a*b
                if numerator % c:
                    continue
                d = numerator//c
                total += (characters[orientation1][a % conductor]
                          * characters[1-orientation1][b % conductor]
                          * characters[orientation2][c % conductor]
                          * characters[1-orientation2][d % conductor])
            result.append(Fraction(total, a*c*conductor))
    return tuple(result)


def aggregate_weil_exponents(alpha):
    """Ideal direct, ideal reversed, and proved rounded-direct budgets.

    Excludes conductor, sieve and logarithmic losses. Values <1 only leave
    a margin to budget those losses; they do not certify a prime theorem.
    """
    if type(alpha) not in (int, Fraction) or not 0 <= alpha <= 1:
        raise ValueError("alpha must be an exact rational in[0,1]")
    alpha = Fraction(alpha)
    return (Fraction(3, 4)+alpha, Fraction(3, 4)+3*alpha/4,
            Fraction(7, 9)+alpha)

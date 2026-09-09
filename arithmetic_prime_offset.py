"""The actual smooth spectral band is a signed nearby prime-pair sum.

Owner: Kevin's Goldbach research. Purpose: test whether the reviewed
arithmetic transfer supplies positivity toward the missing lower margin.
It does not supply coefficientwise positivity: even nonnegative smooth
spectral weights produce negative even-offset coefficients. The actual
transfer below has a paid o(N) error; the signed prime correlation itself
is not estimated by calling this identity a new main term.

1. ACTUAL FORMULA, WITH A SYMMETRIC RATIO AND TRUE PRIMES.
Let N be a sufficiently large EVEN integer, c=1/100, and let chi be a
fixed nonzero real C_c^infinity((c,2c)) function. Keep the actual kernel
J_N and all multiplicity conventions from arithmetic_beta_transfer.py.
For real a,k define
 W_a(k)=(1/pi)int_R chi(a*v)chi((1-a)*v)exp(-ikv)dv.                (1)
The product is supported in v in(2c,4c), and is zero unless
a in(1/3,2/3). In fact its a-support stays in a fixed compact subinterval
there, since chi itself has compact interior support. The function is
smooth in a, and W_a(k) and every fixed a derivative decrease faster
than every fixed power of |k|, uniformly for all a.

The REAL ACTUAL band contribution satisfies
 C_chi(N)=Re sum_(rho,sigma)chi(gamma/N)chi(eta/N)J_N(rho,sigma)
  =sum_(p,q odd primes) logp logq
        *Re W_[p/(p+q)](p+q-N) +O_chi(sqrtN log^7N).               (2)
The prime pairs are ordered. The sum is absolutely convergent by the
rapid offset decay and compact ratio support, even though p+q is not
given a hard upper cutoff. There is no new target average. Since N is
even and the primes are odd, every offset p+q-N in this sum is even.
Formula(2) preserves the actual off-critical real parts in its derivation;
neither RH nor a two-prime asymptotic is used.

The choice p/(p+q) is symmetric under exchanging the primes. The first
local calculation instead produces p/N; replacing it by p/(p+q) has
an explicitly paid error below, not an unannounced change of kernel.

2. THE FINITE-PERIOD CORRECTION IS SMALL FOR THE REAL PART.
The preceding proof already localized the exact beta quotient to a fixed
zeta(a), equal1 on[3/10,7/10], supported in(1/4,3/4), at total cost
O(N^-1 log^13N). Its negative half-line is exponentially small. The
positive tail has the leading coefficient i*(-1)^N/N multiplying
(e/pi)sum f_rho*f_sigma*g(gamma/N,eta/N), where
 g(s,t)=chi(s)chi(t)/(1-(s+t)/pi)
is REAL and fixed smooth, and its remaining total error is O(log^12N).
The saved tensor projection in smooth_endpoint_cancellation.py gives
 sum f_rho*f_sigma*g
   =sum_(n,m>=1)Lambda(n)Lambda(m)exp[-(n+m)/N]*g(pi*n/N,pi*m/N)
            +O_g(N^(3/2)logN+Nlog^2N).
Its arithmetic main is real. The leading imaginary tail therefore has
real part O(sqrtN logN+log^2N), after division by N. This application
uses the single-zero lemma for ANY fixed positive compact height support,
not the old high-band conclusion without checking its support.

Put L=logN. We have thus proved
 C_chi(N)=2 Re int_0^1 zeta(a)S_N(aN)S_N((1-a)N)/sqrt(a(1-a)) da
                 +O_chi(sqrtN L+L^12+N^-1 L^13).                 (3)
The 2016 correction in that endpoint projection remains binding.

3. THE PRIME-WINDOW REPLACEMENT COSTS o(N) BEFORE ANY SIGN CLAIM.
On[1/4,3/4], the reviewed extension gives
 S_N(x)=-P_N(x)+O_chi(L^6),
 int_(1/4)^(3/4)|P_N(aN)|^2 da<<_chi NL,
 P_N(x)=N/(2pi)sum_(n>=2)Lambda(n)/sqrt n
         *h(Nlog(n/x))*nu(Nlog(n/x)/V),
 h=hatChi, V=N^(1/8), with the angular Fourier convention.
Since zeta(a)/sqrt(a(1-a)) is bounded, replacing BOTH moments by -P_N
in (3) costs at most
 O_chi(L^6*sqrt(NL)+L^12).                                        (4)
This uses Cauchy on the frequency integral, not a bound on a single
prime pair. The two minus signs cancel. The old O(sqrtN L) pointwise
replacement would not give o(N) here; the sharpened displacement is needed.

4. LINEARIZE THE LOCAL PRIME WINDOWS, WITH A SUMMABLE ERROR.
Write G(a)=zeta(a)/sqrt(a(1-a)), extended smoothly by0, and k=n+m-N.
After x=aN, the EXACT coefficient of Lambda(n)Lambda(m) in the prime
product from(3) is
 E_N(n,m)=N/(2pi^2 sqrt(nm)) int G(x/N)
    *h(Nlog(n/x))*nu(Nlog(n/x)/V)
    *h(Nlog(m/(N-x)))*nu(Nlog(m/(N-x))/V) dx.                      (5)
The integral lies in x in(N/4,3N/4). For all sufficiently large N,
its cutoffs force n,m in[N/5,4N/5]. Put a0=n/N, b0=1-a0 and delta=x-n.
Where both cutoffs contribute, |delta|,|delta+k|=O(V), and
 U=Nlog(n/x)=-delta/a0+O(delta^2/N),
 T=Nlog(m/(N-x))=(delta+k)/b0
           +O(|delta+k|*(|delta|+|delta+k|)/N).                   (6)
These estimates are uniform on this fixed central range. In particular
the second error vanishes when delta+k=0. The exact and linearized
arguments, and all points between them, are comparable in magnitude
to delta and delta+k, respectively, for large N.

Schwartz decay of h AND its derivatives now pays the Taylor errors.
The prefactor N/sqrt(nm) varies from1/sqrt(a0*b0) by O(|k|/N), and
G(x/N) varies from G(a0) by O(|delta|/N). Every resulting polynomial
factor in delta,delta+k is absorbed by taking more Schwartz derivatives.
For every fixed M the integrated error is therefore bounded by
 C_(chi,M)*N^-1*(1+|k|)^-M.

Here is also the cutoff/tail accounting. Dropping a nu factor can only
change a term where |U| or |T| is at least V, hence where |delta| or
|delta+k| is at least a fixed multiple of V. The corresponding Schwartz
tail is O_(chi,M,A)(V^-A*(1+|k|)^-M), after convolution in delta.
Use A=32. Linearization is made only in the O(V) region; the region
outside it is paid by the same tail, not by a Taylor expansion at delta~N.
Conversely the linearized integral can be extended to every delta in R
with that paid tail. This also handles |k| larger than the joint window.
The standard convolution estimate used here follows by splitting into
|delta|>=|k|/2 or |delta+k|>=|k|/2, and taking decay powers larger than
M+A+2. It remains valid with all fixed polynomial factors just mentioned.

Consequently, uniformly for n,m in[N/5,4N/5],
 E_N(n,m)=G(a0)/(2pi^2 sqrt(a0*b0))
            *int_R h(-delta/a0)h((delta+k)/b0) ddelta
       +O_(chi,M)((N^-1+V^-32)*(1+|k|)^-M).                       (7)
The normalization of the convolution is
 int_R h(-delta/a)h((delta+k)/(1-a)) ddelta
  =2pi*a*(1-a)*int_R chi(av)chi((1-a)v)exp(-ikv)dv.                (8)
For example, Fourier inversion of the first h after the change delta=-a*u
proves(8); all functions are Schwartz, so the convolution theorem applies.
Combining (7)-(8) gives the leading coefficient zeta(a0)W_a0(k).
It equals W_a0(k) because W vanishes outside(1/3,2/3), where zeta=1.

On the central n,m range, Lambda(n)Lambda(m)<=C L^2, and for each n
the offset k runs over integers. Thus the summed error in(7) is
 O_chi(L^2+N L^2 V^-32)=O_chi(L^2).                               (9)
There is no O(V) loss: the errors themselves decrease rapidly in k.

5. EXTEND THE SUM AND MAKE THE PRIME RATIO SYMMETRIC.
First extend the leading sum to all n,m>=2. For W_[n/N](k) to be
nonzero, n/N is in(1/3,2/3). If m is outside[N/5,4N/5], then |k|
is at least a fixed positive multiple of N. The weighted tail is
O_(chi,M)(N^(2-M)L^2), using Lambda(m)<=logm and rapid decay, including
the unbounded m tail. This is negligible upon taking M large.

For |k|<=N/10 and either potentially nonzero ratio, n,m~N. The exact
difference between a1=n/(n+m) and a0=n/N is
 a1-a0=-n*k/[N*(N+k)].
Uniform a derivatives of W therefore show that changing a0 to a1
costs C_M |k|/N*(1+|k|)^-M per pair, hence O(L^2) in total.
For |k|>N/10, both kernels have negligible tails. To see this also for
the new infinite sum, group by s=n+m: there are at most s pairs and
their weights are at most log^2s. Summing
 s log^2s*(1+|s-N|)^-M
over the far range costs O_M(N^(2-M)L^2). The new ratio support also
keeps n,m comparable. We have now obtained the symmetric Lambda-pair
formula with error O_chi(sqrtN L^7), after absorbing(3),(4),(9).

6. REMOVE PROPER PRIME POWERS AND THE PRIME2 WITHOUT A CORRELATION INPUT.
In the central range s=n+m in[9N/10,11N/10], compact ratio support
keeps n,m~N. There are O(sqrtN logN) proper prime powers of size O(N),
by the elementary bound sum_(2<=j<=log_2(CN))(CN)^(1/j).
For each such n, the sum over m of |W_[n/(n+m)](n+m-N)| is O(1).
The two Lambda weights are at most C L^2. Thus all pairs with a proper
prime power in either position cost O_chi(sqrtN L^3) absolutely.
Outside this central sum range, the already proved far-tail bound applies.
This needs no estimate for primes paired with a power. The only pairs
involving the prime2 and a nonzero ratio weight have the other entry
in a bounded range, so their offsets are of size N and their contribution
is negligible. Removing these terms proves the true odd-prime formula(2).

7. NONNEGATIVE SPECTRAL WEIGHTS DO NOT GIVE POSITIVE EVEN-OFFSET WEIGHTS.
At a=1/2 put g(v)=chi(v/2)^2. For EVERY nonzero real chi this is a
nonnegative nonzero smooth function supported in(2c,4c), a subinterval
of(0,pi). Periodize g with period pi:
 P(t)=sum_(ell in Z)g(t+ell*pi).
Its Fourier coefficient at integer j is
 (1/pi)int_0^pi P(t)exp(-2ijt)dt=W_[1/2](2j).
The smooth Fourier series converges absolutely. Evaluating it at0 gives
 sum_(j in Z)W_[1/2](2j)=P(0)=sum_ell g(ell*pi)=0.                 (10)
But W_[1/2](0)>0 and W_[1/2](-k)=conj(W_[1/2](k)). Hence some
positive even integer k has Re W_[1/2](k)<0. Nonnegative chi does not
repair this sign; at the balanced ratio its square already appears.

A concrete falsifier requires no numerical transform: take any nonzero
real smooth chi supported in(7c/5,8c/5), which is inside(c,2c). Then
g is supported in(14c/5,16c/5)=(0.028,0.032). At the EVEN offset100,
the phase100v lies in(2.8,3.2), entirely in(pi/2,3pi/2), so
 Re W_[1/2](100)=(1/pi)int g(v)cos(100v)dv<0.                      (11)
One can check that interval using only3<pi<22/7. Meanwhile its offset0
coefficient is strictly positive.

This falsifies ONE proposed positivity mechanism. It does not prove that
the total actual prime sum in(2) is negative, that actual primes align
with the negative coefficients, or that every combination of these tools
fails. The rapidly weighted signed correlation in(2) is still unresolved.
The offset scale is fixed for fixed chi; no growing prime-pair average
has been obtained. All prior arithmetic/spectral and polynomial components,
source corrections, runtime limits and reviewed bounds remain useful.
"""
from fractions import Fraction as F


def window_arguments(a, delta, offset):
    if any(type(v) is not F for v in (a,delta,offset)) or not 0<a<1:
        raise ValueError('rational0<a<1 and rational displacements required')
    return -delta/a,(delta+offset)/(1-a)


def ratio_replacement(n, m, scale):
    if any(type(v) is not int or v<1 for v in (n,m,scale)):
        raise ValueError('positive integers required')
    offset=n+m-scale
    return {'old':F(n,scale),'symmetric':F(n,n+m),
            'difference':-F(n*offset,scale*(scale+offset))}


def product_error_exponents(pointwise_power=F(0), pointwise_log=F(6)):
    """Energy is N logN in the normalized frequency measure."""
    if any(type(v) is not F or v<0 for v in (pointwise_power,pointwise_log)):
        raise ValueError('nonnegative rational error exponents required')
    return {'cross_N':pointwise_power+F(1,2),
            'cross_log':pointwise_log+F(1,2),
            'square_N':2*pointwise_power,'square_log':2*pointwise_log}


def balanced_phase_interval(lower_height, upper_height, offset):
    if any(type(v) is not F for v in (lower_height,upper_height)) or not 0<lower_height<upper_height:
        raise ValueError('positive rational height interval required')
    if type(offset) is not int or offset<=0:
        raise ValueError('positive integer offset required')
    return 2*offset*lower_height,2*offset*upper_height


def certifies_negative_cosine_interval(lower, upper):
    """A sufficient exact interval certificate using3<pi<22/7."""
    if any(type(v) is not F for v in (lower,upper)) or lower>=upper:
        raise ValueError('ordered rational interval required')
    return F(11,7)<lower and upper<F(9,2)

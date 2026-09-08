"""Count overlap of divisibility exclusions by CRT, without witness search.

Owner/purpose: Kevin's staged-calculation research. Exact finite counts feed
rigorous bounds; failed bounds stay unresolved. No universal estimate assumed.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
from math import comb, isqrt, prod
import json
from pathlib import Path
import time

from paired_wheel import prime_prefix
from moment_polynomials import strongest_lower
from redistribution import sieve, trial_prime


def ceiling_ratio(n: int, d: int) -> int:
    return -((-n)//d)


def zero_histogram_from_three(moments: list[int],cap: int) -> list[int] | None:
    """Find an abstract integer histogram with the same moments and n_0=0.

    Exhaustive for support0..K with K<=6. This does not construct divisibility
    patterns for the original target; it tests what these aggregates alone say.
    """
    if type(cap) is not int or not 0<=cap<=6 or len(moments)!=4:
        raise ValueError("four moments and cap in0..6 required")
    if any(type(s) is not int or s<0 for s in moments):
        raise ValueError("nonnegative integer moments required")
    total,s1,s2,s3=moments
    deficit=-(total-s1+s2-s3)
    if deficit<0:
        return None
    for n6 in range(deficit//10+1 if cap>=6 else 1):
        for n5 in range((deficit-10*n6)//4+1 if cap>=5 else 1):
            n4=deficit-4*n5-10*n6
            n3=s3-4*deficit+6*n5+20*n6
            n2=s2-3*s3+6*deficit-4*n5-15*n6
            n1=total-s2+2*s3-3*deficit+n5+4*n6
            full=[0,n1,n2,n3,n4,n5,n6]
            if min(full)<0 or any(full[cap+1:]):
                continue
            histogram=full[:cap+1]
            actual=[sum(n*comb(k,j) for k,n in enumerate(histogram) if k>=j)
                    for j in range(4)]
            if actual!=moments:
                raise ValueError("constructed histogram fails exact moment check")
            return histogram
    return None


def moment_bounds(moments: list[int], cap: int, bound_strategy: str="basic") -> dict:
    """Bound multiplicity-zero count from exact binomial moments.

    moments[j] = sum_i C(multiplicity_i,j), with every multiplicity<=cap.
    All arithmetic is integer, including rounding rational lower bounds.
    """
    if type(cap) is not int or cap < 0 or not moments:
        raise ValueError("nonnegative multiplicity cap and moments required")
    if any(type(s) is not int or s < 0 for s in moments):
        raise ValueError("moments must be nonnegative integers")
    if bound_strategy not in ("basic","root_family"):
        raise ValueError("unknown polynomial bound strategy")
    total, partial = moments[0], moments[0]
    lower, upper = 0, total
    lower_method = "nonnegativity"
    for degree, value in enumerate(moments[1:],1):
        partial += (-1)**degree*value
        if degree % 2:
            if partial > lower:
                lower, lower_method = partial, f"Bonferroni degree {degree}"
        else:
            upper = min(upper,partial)
    if len(moments)>1 and cap == 1:
        lower=upper=total-moments[1]
        lower_method="multiplicity cap 1"
    if len(moments)>2 and cap >= 2:
        bound = total-moments[1]+ceiling_ratio(2*moments[2],cap)
        if bound>lower:
            lower, lower_method=bound,"quadratic with multiplicity cap"
    if len(moments)>3:
        for a in range(1,max(2,cap)+1):
            bound=total-moments[1]+ceiling_ratio(
                (4*a-2)*moments[2]-6*moments[3],a*(a+1))
            if bound>lower:
                lower,lower_method=bound,f"adjacent-root cubic a={a}"
    root_certificate=None
    if bound_strategy=="root_family":
        family=strongest_lower(moments,cap)
        if family["lower"]>lower:
            lower=family["lower"]
            lower_method="root polynomial "+str(family["roots"])
            root_certificate=family
    if len(moments)>cap:
        exact=sum((-1)**j*s for j,s in enumerate(moments))
        lower=upper=exact
        lower_method="complete inclusion-exclusion through multiplicity cap"
    if lower<0 or upper<lower or upper>total:
        raise ValueError("inconsistent moments or multiplicity cap")
    result={"lower":lower,"upper":upper,"lower_method":lower_method}
    if root_certificate:
        result["root_certificate"]=root_certificate
    return result


@lru_cache(maxsize=None)
def split_threshold(primes: tuple[int,...]) -> int:
    """Minimum sum of two complementary squarefree products; empty product=1."""
    products=[1]
    for r in primes:
        products += [a*r for a in products]
    whole=prod(primes)
    return min(a+whole//a for a in products)


def candidate_window(target: int, p: int | None=None,cap_strategy: str="product") -> dict:
    if type(target) is not int or target<6 or target%2:
        raise ValueError("even target >=6 required")
    if cap_strategy not in ("product","split"):
        raise ValueError("unknown multiplicity cap strategy")
    if p is None:
        p=isqrt(target)
        while not trial_prime(p):
            p-=1
    primes,following=prime_prefix(p)
    lo=max(p+1,target-(following*following-1))
    hi=min(following*following-1,target-p-1)
    lo+=1-lo%2
    hi-=1-hi%2
    count=max(0,(hi-lo)//2+1)
    odd_primes=primes[1:]
    cap,minimum_product=0,1
    for r in odd_primes:
        if minimum_product*r>target*target//4:
            break
        minimum_product*=r
        cap+=1
    product_cap=cap
    if cap_strategy=="split":
        while cap and split_threshold(tuple(odd_primes[:cap]))>target:
            cap-=1
    return {"first_odd":lo,"last_odd":hi,"candidate_count":count,
            "last_wheel_prime":p,"next_prime":following,
            "odd_wheel_primes":odd_primes,"multiplicity_cap":cap,
            "product_multiplicity_cap":product_cap,"cap_strategy":cap_strategy}


def residue_count(residue: int, modulus: int, lo: int, hi: int) -> int:
    return (hi-residue)//modulus-(lo-1-residue)//modulus


def count_target(target: int,p: int | None=None,max_degree: int | None=None,
                 stop_when_positive: bool=True,bound_strategy: str="basic",
                 cap_strategy: str="product") -> dict:
    started=time.monotonic()
    window=candidate_window(target,p,cap_strategy)
    primes=window["odd_wheel_primes"]
    lo,hi=window["first_odd"],window["last_odd"]
    cap=window["multiplicity_cap"]
    limit=cap if max_degree is None else min(cap,max_degree)
    if type(limit) is not int or limit<0:
        raise ValueError("nonnegative maximum degree required")
    moments=[window["candidate_count"]]
    stages=[]
    evaluations=0
    nodes=[(-1,2,(1,))] if moments[0] else []
    for degree in range(0,limit+1):
        if degree:
            next_nodes=[]
            total=0
            for last_index,modulus,residues in nodes:
                for index in range(last_index+1,len(primes)):
                    r=primes[index]
                    forbidden={0,target%r}
                    next_modulus=modulus*r
                    inverse=pow(modulus,-1,r)
                    next_residues=[]
                    for residue in residues:
                        for bad in forbidden:
                            merged=residue+modulus*((bad-residue)*inverse % r)
                            evaluations+=1
                            n=residue_count(merged,next_modulus,lo,hi)
                            if n:
                                next_residues.append(merged)
                                total+=n
                    if next_residues:
                        next_nodes.append((index,next_modulus,tuple(next_residues)))
            nodes=next_nodes
            moments.append(total)
        bound=moment_bounds(moments,cap,bound_strategy)
        ordinary=[sum((-1)**j*s for j,s in enumerate(moments[:d+1]))
                  for d in range(1,len(moments),2)]
        stage={"degree":degree,"intersection_sum":moments[-1],
               "best_ordinary_Bonferroni_lower":max([0]+ordinary),
               "retained_nonempty_intersections":len(nodes),
               "cumulative_CRT_floor_evaluations":evaluations,**bound}
        if not nodes:
            # An empty intersection layer implies all higher layers are empty.
            exact=sum((-1)**j*s for j,s in enumerate(moments))
            stage.update(lower=exact,upper=exact,
                         lower_method="empty intersection layer closes exact sum")
        stages.append(stage)
        if (stage["lower"]>0 and stop_when_positive) or not nodes:
            break
    return {"target_even":target,"window":window,"stages":stages,
            "bound_strategy":bound_strategy,
            "status":"certified" if stages[-1]["lower"]>0 else "unresolved_by_window",
            "survivor_lower":stages[-1]["lower"],
            "survivor_upper":stages[-1]["upper"],
            "CRT_floor_evaluations":evaluations,
            "seconds":round(time.monotonic()-started,6),
            "scope":"finite prime-safe window; missing small-prime pairs are not counterexamples"}


def block_experiment(first: int,count: int,bound_strategy: str="basic",
                     cap_strategy: str="product") -> dict:
    if type(first) is not int or first<6 or first%2 or type(count) is not int or count<1:
        raise ValueError("even start>=6 and positive block size required")
    started=time.monotonic()
    rows=[]
    histogram={}
    total_evaluations=0
    for target in range(first,first+2*count,2):
        z=count_target(target,bound_strategy=bound_strategy,cap_strategy=cap_strategy)
        stage=z["stages"][-1]
        key=str(stage["degree"]) if z["status"]=="certified" else "unresolved"
        histogram[key]=histogram.get(key,0)+1
        total_evaluations+=z["CRT_floor_evaluations"]
        rows.append({"target_even":target,"stopping_degree":stage["degree"],
                     "odd_wheel_primes":len(z["window"]["odd_wheel_primes"]),
                     "multiplicity_cap":z["window"]["multiplicity_cap"],
                     "lower":stage["lower"],"upper":stage["upper"],
                     "lower_method":stage["lower_method"],
                     "ordinary_Bonferroni_lower":stage["best_ordinary_Bonferroni_lower"],
                     "CRT_floor_evaluations":z["CRT_floor_evaluations"],
                     "status":z["status"]})
    return {"method":"staged exact exclusion moments with polynomial lower bounds",
            "bound_strategy":bound_strategy,"cap_strategy":cap_strategy,
            "first_even":first,"last_even":first+2*(count-1),"count":count,
            "stopping_degree_histogram":histogram,
            "CRT_floor_evaluations":total_evaluations,
            "rows":rows,"seconds":round(time.monotonic()-started,4),
            "scope":"each finite target gets a count certificate; no uniform future bound inferred"}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command",choices=["target","block"])
    parser.add_argument("--target",type=int,default=400)
    parser.add_argument("--prime",type=int)
    parser.add_argument("--degree",type=int)
    parser.add_argument("--full",action="store_true")
    parser.add_argument("--polynomial-family",action="store_true")
    parser.add_argument("--split-cap",action="store_true")
    parser.add_argument("--first",type=int,default=6)
    parser.add_argument("--count",type=int,default=1000)
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    strategy="root_family" if args.polynomial_family else "basic"
    cap_strategy="split" if args.split_cap else "product"
    result=(count_target(args.target,args.prime,args.degree,not args.full,strategy,cap_strategy)
            if args.command=="target" else block_experiment(args.first,args.count,strategy,cap_strategy))
    rendered=json.dumps(result,indent=2)
    if args.output:
        args.output.write_text(rendered+"\n",encoding="utf-8")
    print(rendered)


if __name__=="__main__":
    main()

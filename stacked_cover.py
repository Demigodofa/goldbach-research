"""Stack exact prime data -> prime progressions -> sum certificates -> coverage.

The sum of AP(a,d,m) and AP(b,d,n) is AP(a+b,d,m+n-1). When both
input progressions consist entirely of primes, every output is Goldbach-valid.
Certificates can be combined as bit masks; uncovered positions remain explicit.
This is a finite certifier and does not assume or prove universal coverage.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from math import isqrt
import json
from pathlib import Path
import time

from redistribution import sieve, trial_prime


@dataclass(frozen=True)
class AP:
    first: int
    step: int
    count: int

    @property
    def last(self) -> int:
        return self.first+self.step*(self.count-1)

    def values(self):
        return range(self.first,self.last+1,self.step)


def segmented_flags(lo: int, hi: int, base_primes: list[int]) -> bytearray:
    if lo < 0 or hi < lo:
        raise ValueError("invalid segment")
    flags=bytearray(b"\1")*(hi-lo+1)
    for p in base_primes:
        if p*p>hi:
            break
        start=max(p*p,((lo+p-1)//p)*p)
        if start<=hi:
            flags[start-lo:hi-lo+1:p]=b"\0"*((hi-start)//p+1)
    for n in range(lo,min(hi,1)+1):
        flags[n-lo]=0
    return flags


def prime_runs(lo: int, hi: int, step: int, flags: bytearray,
               offset: int=0, minimum: int=1) -> list[AP]:
    runs=[]
    for first in range(lo if lo%2 else lo+1,hi+1,2):
        if not flags[first-offset]:
            continue
        if first-step>=lo and flags[first-step-offset]:
            continue
        last=first
        while last+step<=hi and flags[last+step-offset]:
            last+=step
        count=(last-first)//step+1
        if count>=minimum:
            runs.append(AP(first,step,count))
    return runs


def sum_ap(a: AP,b: AP) -> AP:
    if a.step!=b.step or a.count<1 or b.count<1:
        raise ValueError("need nonempty progressions with equal step")
    return AP(a.first+b.first,a.step,a.count+b.count-1)


def target_mask(ap: AP, first_even: int, count: int) -> int:
    last_even=first_even+2*(count-1)
    start=max(ap.first,first_even)
    start+=(- (start-ap.first))%ap.step
    stop=min(ap.last,last_even)
    if start>stop:
        return 0
    if (start-first_even)%2 or ap.step%2:
        raise ValueError("sum progression must consist of evens")
    mask=0
    for n in range(start,stop+1,ap.step):
        mask|=1<<((n-first_even)//2)
    return mask


def prepare_palette(limit: int,steps=(2,6,30,210)) -> tuple[bytearray,dict[int,list[AP]]]:
    flags=sieve(limit)
    return flags,{d:prime_runs(3,limit,d,flags,minimum=2) for d in steps}


def _validated_carry(carry_from: dict | None, first_even: int, count: int) -> tuple[int,list[dict]]:
    """Re-check prior proof data and project its output APs onto this block.

    A carry record is never trusted merely because an earlier run marked it
    certified.  ``verify_block`` rechecks every prime input and every AP sum;
    the returned masks are then recomputed for the new block's exact endpoints.
    """
    if carry_from is None:
        return 0,[]
    if not isinstance(carry_from,dict):
        raise ValueError("carry block must be a serialized block dictionary")
    try:
        verify_block(carry_from)
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"invalid carry block: {exc}") from exc
    covered=0
    carried=[]
    for original in carry_from["certificates"]:
        if original["kind"]=="base_pair":
            # The base pair is confined to 4 and cannot extend into a later block.
            continue
        output=AP(**original["output"])
        mask=target_mask(output,first_even,count)
        fresh=(mask&~covered).bit_count()
        if not fresh:
            continue
        # Retain the complete original proof data.  Fresh coverage must be
        # recomputed in its new target universe, not copied from the old block.
        cert={
            "kind":"prime_AP_sum",
            "left":asdict(AP(**original["left"])),
            "right":asdict(AP(**original["right"])),
            "output":asdict(output),
            "newly_covered":fresh,
            "provenance":"carried_from_verified_block",
        }
        carried.append(cert)
        covered|=mask
    return covered,carried


def cover_block(first_even: int,count: int=1000,palette_limit: int=1000,
                prepared=None,base_primes=None,carry_from: dict | None=None) -> dict:
    if first_even<4 or first_even%2 or count<1:
        raise ValueError("invalid target block")
    started=time.monotonic()
    final_even=first_even+2*(count-1)
    if first_even==4 and count==1:
        # Validate supplied carry even though it cannot contribute to this base case.
        _validated_carry(carry_from,first_even,count)
        return {"schema":1,"method":"stacked_prime_AP_certificates",
                "first_even":4,"last_even":4,"count":1,
                "palette_limit":palette_limit,"steps":[],"covered_count":1,
                "unresolved":[],"certificate_count":1,
                "certificates":[{"kind":"base_pair","p":2,"q":2,"sum":4}],
                "carry_mode":"enabled" if carry_from is not None else "disabled",
                "carried_covered_count":0,"carried_certificate_count":0,
                "fresh_covered_count":0,"fresh_certificate_count":0,
                "fresh_generation_skipped":True,
                "elapsed_seconds":round(time.monotonic()-started,6),
                "status":"certified","scope":"exact base case only"}
    covered=0
    selected=[]
    if first_even==4:
        covered=1
        selected.append({"kind":"base_pair","p":2,"q":2,"sum":4})
    carry_covered,carried=_validated_carry(carry_from,first_even,count)
    for cert in carried:
        output=AP(**cert["output"])
        cert["newly_covered"]=(target_mask(output,first_even,count)&~covered).bit_count()
        if cert["newly_covered"]:
            selected.append(cert)
            covered|=target_mask(output,first_even,count)
    carried_covered=covered.bit_count()-(1 if first_even==4 else 0)
    full=(1<<count)-1
    candidates={}
    fresh_generation_skipped=covered==full
    if not fresh_generation_skipped:
        palette_flags,templates=prepared or prepare_palette(palette_limit)
        qlo=max(3,first_even-palette_limit)
        qhi=final_even-3
        if base_primes is None:
            base=sieve(isqrt(max(3,qhi)))
            base_primes=[p for p,f in enumerate(base) if f]
        elif qhi>=4 and (not base_primes or base_primes[-1]<isqrt(qhi)):
            # Last base prime can legitimately be below sqrt; callers provide
            # an explicit generous shared base instead of relying on this branch.
            base=sieve(isqrt(qhi))
            base_primes=[p for p,f in enumerate(base) if f]
        qflags=segmented_flags(qlo,qhi,base_primes)
        for step,aruns in templates.items():
            bruns=prime_runs(qlo,qhi,step,qflags,offset=qlo)
            for a in aruns:
                for b in bruns:
                    out=sum_ap(a,b)
                    if out.last<first_even or out.first>final_even:
                        continue
                    mask=target_mask(out,first_even,count)
                    if mask and mask not in candidates:
                        candidates[mask]=(a,b,out)
    # Greedy set cover chooses compact certificates, without assuming optimality.
    while covered!=full:
        bestmask=0
        gain=0
        for mask in candidates:
            fresh=(mask&~covered).bit_count()
            if fresh>gain:
                bestmask,gain=mask,fresh
        if gain==0:
            break
        a,b,out=candidates.pop(bestmask)
        covered|=bestmask
        selected.append({"kind":"prime_AP_sum","left":asdict(a),
                         "right":asdict(b),"output":asdict(out),
                         "newly_covered":gain})
    unresolved=[first_even+2*i for i in range(count) if not covered>>i&1]
    carried_certificate_count=len(carried)
    fresh_certificate_count=len(selected)-carried_certificate_count-(1 if first_even==4 else 0)
    steps=list(prepared[1]) if prepared is not None else [2,6,30,210]
    return {"schema":1,"method":"stacked_prime_AP_certificates",
            "first_even":first_even,"last_even":final_even,"count":count,
            "palette_limit":palette_limit,
            "steps":steps,
            "covered_count":covered.bit_count(),"unresolved":unresolved,
            "certificate_count":len(selected),"certificates":selected,
            "carry_mode":"enabled" if carry_from is not None else "disabled",
            "carried_covered_count":carried_covered,
            "carried_certificate_count":carried_certificate_count,
            "fresh_covered_count":covered.bit_count()-carried_covered-(1 if first_even==4 else 0),
            "fresh_certificate_count":fresh_certificate_count,
            "fresh_generation_skipped":fresh_generation_skipped,
            "elapsed_seconds":round(time.monotonic()-started,6),
            "status":"certified" if not unresolved else "partial",
            "scope":"exact finite block only; no universal invariant claimed"}


def verify_block(block: dict,prime_check=trial_prime) -> dict:
    def require(condition,message):
        if not condition:
            raise ValueError(message)
    def integer(value):
        return type(value) is int
    first,count=block["first_even"],block["count"]
    require(integer(first) and first>=4 and first%2==0,"invalid first even target")
    require(integer(count) and count>=1,"invalid target count")
    require(integer(block["last_even"]) and block["last_even"]==first+2*(count-1),"inconsistent last target")
    require(isinstance(block["certificates"],list),"certificates must be a list")
    checked=set()
    covered=0
    carried_covered=0
    carried_certificates=0
    fresh_covered=0
    fresh_certificates=0
    seen_fresh=False
    initial_coverage=0
    metadata_fields=("carry_mode","carried_covered_count","carried_certificate_count",
                     "fresh_covered_count","fresh_certificate_count","fresh_generation_skipped")
    present_metadata=[field for field in metadata_fields if field in block]
    require(not present_metadata or len(present_metadata)==len(metadata_fields),
            "incomplete carry metadata")
    for cert in block["certificates"]:
        if cert["kind"]=="base_pair":
            require(cert=={"kind":"base_pair","p":2,"q":2,"sum":4},"invalid base certificate")
            require(first==4,"base certificate outside block")
            covered|=1
            initial_coverage=covered
            continue
        require(cert["kind"]=="prime_AP_sum","unknown certificate kind")
        provenance=cert.get("provenance")
        require(provenance in (None,"carried_from_verified_block"),"invalid certificate provenance")
        is_carried=provenance=="carried_from_verified_block"
        require(not (is_carried and seen_fresh),"carried certificate follows fresh certificate")
        if not is_carried:
            seen_fresh=True
        a,b,out=(AP(**cert[key]) for key in ["left","right","output"])
        for ap in [a,b,out]:
            require(integer(ap.first) and integer(ap.step) and integer(ap.count),"noninteger AP")
            require(ap.first>=2 and ap.step>0 and ap.step%2==0 and ap.count>=1,"invalid AP bounds")
        require(a.first%2==1 and b.first%2==1,"nonbase inputs must be odd")
        require(b.step==a.step and out==sum_ap(a,b),"incorrect AP sum")
        for value in list(a.values())+list(b.values()):
            if value not in checked:
                require(bool(prime_check(value)),f"nonprime certificate input: {value}")
                checked.add(value)
        mask=target_mask(out,first,count)
        if "newly_covered" in cert:
            require(integer(cert["newly_covered"]) and cert["newly_covered"]==(mask&~covered).bit_count(),"incorrect fresh coverage count")
        fresh=(mask&~covered).bit_count()
        if is_carried:
            carried_certificates+=1
            carried_covered+=fresh
        else:
            fresh_certificates+=1
            fresh_covered+=fresh
        covered|=mask
        if not seen_fresh:
            initial_coverage=covered
    missing=[first+2*i for i in range(count) if not covered>>i&1]
    require(missing==block["unresolved"],"unresolved targets do not match certificates")
    require(integer(block["covered_count"]) and covered.bit_count()==block["covered_count"],"incorrect coverage total")
    require(integer(block["certificate_count"]) and len(block["certificates"])==block["certificate_count"],"incorrect certificate count")
    require(block["status"]==("certified" if not missing else "partial"),"incorrect certificate status")
    if present_metadata:
        require(block["carry_mode"] in ("enabled","disabled"),"invalid carry mode")
        require(integer(block["carried_covered_count"]) and
                block["carried_covered_count"]==carried_covered,"incorrect carried coverage total")
        require(integer(block["carried_certificate_count"]) and
                block["carried_certificate_count"]==carried_certificates,"incorrect carried certificate count")
        require(integer(block["fresh_covered_count"]) and
                block["fresh_covered_count"]==fresh_covered,"incorrect fresh coverage total")
        require(integer(block["fresh_certificate_count"]) and
                block["fresh_certificate_count"]==fresh_certificates,"incorrect fresh certificate count")
        require(type(block["fresh_generation_skipped"]) is bool and
                block["fresh_generation_skipped"]==(initial_coverage==((1<<count)-1)),
                "incorrect logical fresh-generation skip claim")
        require(not (block["carry_mode"]=="disabled" and carried_certificates),
                "disabled carry mode contains carried certificates")
        require(not (carried_certificates and block["carry_mode"]!="enabled"),
                "carried certificates require enabled carry mode")
    return {"status":"passed","independently_checked_prime_inputs":len(checked),
            "covered_count":covered.bit_count(),"unresolved_count":len(missing)}


def compose(blocks: list[dict],prime_check=trial_prime) -> dict:
    if not blocks:
        raise ValueError("no blocks")
    ordered=sorted(blocks,key=lambda b:b["first_even"])
    next_even=ordered[0]["first_even"]
    total=0
    prime_cache={}
    def cached_check(value):
        if value not in prime_cache:
            prime_cache[value]=prime_check(value)
        return prime_cache[value]
    for b in ordered:
        verify_block(b,cached_check)
        if b["first_even"]!=next_even:
            raise ValueError("gap or overlap in block composition")
        if b["status"]!="certified" or b["unresolved"]:
            raise ValueError("cannot certify a composition with an unresolved block")
        total+=b["count"]
        next_even=b["last_even"]+2
    return {"first_even":ordered[0]["first_even"],"last_even":next_even-2,
            "count":total,"blocks":len(blocks),"status":"certified",
            "scope":"finite union of verified adjacent block certificates"}


def self_check() -> dict:
    cases=0
    for a in [3,5,17]:
        for b in [3,7,23]:
            for step in [2,6,30]:
                for m in range(1,12):
                    for n in range(1,12):
                        x,y=AP(a,step,m),AP(b,step,n)
                        assert set(sum_ap(x,y).values())=={i+j for i in x.values() for j in y.values()}
                        cases+=1
    base=sieve(100)
    primes=[p for p,f in enumerate(base) if f]
    for lo,hi in [(0,100),(1,200),(89,1000),(5000,10000)]:
        flags=segmented_flags(lo,hi,primes)
        assert all(bool(flags[i-lo])==trial_prime(i) for i in range(lo,hi+1))
    b=cover_block(4,100)
    v=verify_block(b)
    assert b["status"]=="certified"
    assert verify_block(cover_block(4,1))["covered_count"]==1
    second=cover_block(204,100)
    assert compose([b,second])["count"]==200
    try:
        compose([b,b])
        raise AssertionError("overlapping blocks accepted")
    except ValueError:
        pass
    return {"status":"passed","general_AP_sum_cases":cases,
            "segmented_prime_intervals":4,"small_block":v}


def stack_blocks(first_even: int,block_count: int,block_size: int=1000,
                 carryover: bool=False) -> dict:
    """Compose exactly checked blocks; keep a compact reproducibility receipt."""
    started=time.monotonic()
    last_even=first_even+2*(block_count*block_size-1)
    # Independent monolithic sieve validates prime inputs produced by segments.
    independent=sieve(last_even)
    bases=sieve(isqrt(last_even)+100)
    base_primes=[p for p,f in enumerate(bases) if f]
    palettes={}
    blocks=[]
    rows=[]
    for i in range(block_count):
        start=first_even+2*block_size*i
        attempts=[]
        for palette in [1000,2000,4000,8000]:
            if palette not in palettes:
                palettes[palette]=prepare_palette(palette)
            carry_from=blocks[-1] if carryover and blocks else None
            b=cover_block(start,block_size,palette,palettes[palette],base_primes,carry_from)
            attempts.append({"palette":palette,"unresolved":len(b["unresolved"])})
            if b["status"]=="certified":
                break
        if b["status"]!="certified":
            raise RuntimeError(f"unresolved block {start}: {b['unresolved']}; no universal claim")
        blocks.append(b)
        rows.append({"first_even":start,"last_even":b["last_even"],
                     "certificate_count":b["certificate_count"],"attempts":attempts,
                     "carried_covered_count":b["carried_covered_count"],
                     "fresh_generation_skipped":b["fresh_generation_skipped"]})
        if (i+1)%100==0:
            print(json.dumps({"generated_blocks":i+1,"elapsed_seconds":round(time.monotonic()-started,2)}),flush=True)
    receipt=compose(blocks,lambda n:bool(independent[n]))
    return {"method":"1000_number_block_stacking","carry_mode":"enabled" if carryover else "disabled",
            "composition":receipt,
            "prime_input_verification":"separate monolithic sieve; generator uses segmented sieve",
            "block_rows":rows,"sum_certificate_count":sum(x["certificate_count"] for x in rows),
            "expanded_palette_blocks":sum(len(x["attempts"])>1 for x in rows),
            "elapsed_seconds":round(time.monotonic()-started,6),
            "retention":"aggregate checked receipt; representative full certificates saved separately; regenerate all with this script"}


def compare_carryover(first_even: int, block_count: int=10, block_size: int=1000,
                      palette_limit: int=1000) -> dict:
    """Run the same finite blocks with and without validated adjacent carryover."""
    if block_count<1:
        raise ValueError("comparison needs at least one block")
    final_even=first_even+2*(block_count*block_size-1)
    bases=sieve(isqrt(final_even)+100)
    base_primes=[p for p,f in enumerate(bases) if f]
    prepared=prepare_palette(palette_limit)
    fresh=[]
    carried=[]
    rows=[]
    for i in range(block_count):
        start=first_even+2*i*block_size
        no_carry=cover_block(start,block_size,palette_limit,prepared,base_primes)
        with_carry=cover_block(start,block_size,palette_limit,prepared,base_primes,
                               carried[-1] if carried else None)
        # This is the acceptance gate for both timings, including carried proof data.
        verify_block(no_carry)
        verify_block(with_carry)
        fresh.append(no_carry)
        carried.append(with_carry)
        rows.append({"first_even":start,"last_even":no_carry["last_even"],
                     "fresh_seconds":no_carry["elapsed_seconds"],
                     "carry_seconds":with_carry["elapsed_seconds"],
                     "settled_from_prior_certificates":with_carry["carried_covered_count"],
                     "carried_certificate_count":with_carry["carried_certificate_count"],
                     "fresh_certificate_count":with_carry["fresh_certificate_count"],
                     "fresh_generation_skipped":with_carry["fresh_generation_skipped"],
                     "fresh_unresolved_count":len(no_carry["unresolved"]),
                     "carry_unresolved_count":len(with_carry["unresolved"])})
    fresh_seconds=sum(row["fresh_seconds"] for row in rows)
    carry_seconds=sum(row["carry_seconds"] for row in rows)
    return {"schema":1,"experiment":"adjacent_block_carryover_comparison",
            "conditions":{"first_even":first_even,"block_count":block_count,
                          "block_size":block_size,"palette_limit":palette_limit,
                          "same_targets_and_palette":True,
                          "carry_source":"immediately preceding independently re-verified block"},
            "rows":rows,
            "totals":{"targets":block_count*block_size,
                      "settled_from_prior_certificates":sum(row["settled_from_prior_certificates"] for row in rows),
                      "blocks_with_generation_skipped":sum(row["fresh_generation_skipped"] for row in rows),
                      "fresh_seconds":round(fresh_seconds,6),"carry_seconds":round(carry_seconds,6)},
            "timing_limit":"Times are cover_block wall times on the current shared machine; carry mode includes required prior-proof validation, while the equal post-generation verification is run outside both timers. They are descriptive, not a speedup claim.",
            "scope":"finite measured blocks only; unresolved targets remain explicit in each verified result"}


def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument("mode",choices=["check","block","stack","compare"])
    parser.add_argument("--first",type=int,default=4)
    parser.add_argument("--count",type=int,default=1000)
    parser.add_argument("--palette",type=int,default=1000)
    parser.add_argument("--blocks",type=int,default=1000)
    parser.add_argument("--output",type=Path)
    parser.add_argument("--carry",action="store_true",help="reuse only the prior block's re-verified AP certificates")
    args=parser.parse_args()
    if args.mode=="check":
        result=self_check()
    elif args.mode=="stack":
        result=stack_blocks(args.first,args.blocks,args.count,args.carry)
    elif args.mode=="compare":
        result=compare_carryover(args.first,args.blocks,args.count,args.palette)
    else:
        result=cover_block(args.first,args.count,args.palette)
        result["verification"]=verify_block(result)
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k not in ['certificates','block_rows']},indent=2))


if __name__=='__main__':
    main()

from __future__ import annotations

import asyncio, re
from typing import Awaitable, Callable

from sharck_v3_runtime import LaneResult, SharckV3Runtime, _sha


class LaneKernel:
    """Independent lane wrapper: one coroutine contract, one result, fail-closed exception mapping."""
    def __init__(self,name:str,fn:Callable[[],Awaitable[LaneResult]]): self.name,self.fn=name,fn
    async def run(self)->LaneResult:
        try: return await self.fn()
        except Exception as exc: return LaneResult(self.name,"GAP",f"lane exception: {type(exc).__name__}",gaps=[f"{self.name}_exception:{type(exc).__name__}"])


class StrictSharckV3Runtime(SharckV3Runtime):
    """Literal M59 gates: 20 full skill bodies, 3 distinct libraries, explicit LaneKernel fan-out."""
    async def _skills(self,spec):
        if len(self.skill_libraries)<3: return LaneResult("skills","GAP","skill libraries <3",gaps=["skill_libraries_min_3"])
        batches=await asyncio.gather(*(p.discover(" ".join(spec.tokens[:20]),20) for p in self.skill_libraries),return_exceptions=True)
        groups={p.name:[] for p in self.skill_libraries}; providers={p.name:p for p in self.skill_libraries}
        for p,b in zip(self.skill_libraries,batches):
            if isinstance(b,BaseException): continue
            seen=set()
            for r in b:
                key=str(r.get("id") or r.get("url") or r.get("name"))
                if key not in seen: seen.add(key); groups[p.name].append({"library":p.name,**r})
        if sum(bool(v) for v in groups.values())<3: return LaneResult("skills","GAP","<3 libraries returned skills",gaps=["skill_libraries_with_results_min_3"])
        ranked=[]; idx=0
        while len(ranked)<20 and any(idx<len(v) for v in groups.values()):
            for lib in groups:
                if idx<len(groups[lib]) and len(ranked)<20: ranked.append(groups[lib][idx])
            idx+=1
        if len(ranked)<20: return LaneResult("skills","GAP",f"only {len(ranked)} distinct skills",gaps=["skills_full_read_min_20"])
        async def read_one(item):
            p=providers[item["library"]]; fn=getattr(p,"read_body",None)
            if not fn: return item,None,"READ_BODY_UNSUPPORTED"
            try: return item,await fn(item),None
            except Exception as exc: return item,None,type(exc).__name__
        reads=await asyncio.gather(*(read_one(i) for i in ranked)); cache=self.ledger.run_dir(spec.run_id)/"artifacts"/"skills-read"; cache.mkdir(parents=True,exist_ok=True)
        ok=[]; errors=[]
        for i,(item,body,err) in enumerate(reads,1):
            if not body: errors.append(f"{item['library']}:{item.get('name')}:{err}"); continue
            name=re.sub(r"[^a-z0-9._-]+","-",str(item.get("name") or "skill").lower())[:60]; path=cache/f"{i:02d}-{name}.md"; path.write_text(body,encoding="utf-8")
            item["body_sha256"]=_sha(body); item["body_chars"]=len(body); item["body_pointer"]=str(path.relative_to(self.ledger.run_dir(spec.run_id))); ok.append(item)
        if len(ok)<20: return LaneResult("skills","GAP",f"{len(ok)}/20 full SKILL bodies read",candidates=ok[:3],standby=ok[3:8],gaps=["skills_full_read_min_20",*errors[:5]],metrics={"bodies_read":len(ok),"libraries":len(set(x["library"] for x in ok))})
        selected=[]
        for lib in groups:
            candidate=next((x for x in ok if x["library"]==lib and x.get("source_repo") and x.get("source_ref") and x.get("license")),None)
            if candidate: selected.append(candidate)
            if len(selected)==3: break
        if len(selected)<3: return LaneResult("skills","GAP","3 acquisition-ready skills across distinct libraries unavailable",candidates=selected,standby=[x for x in ok if x not in selected][:5],gaps=["skill_acquisition_ready_3_distinct_libraries"])
        for item in selected: item["acquisition"]=await self.download.stage(lane="skills",item=item,run_dir=self.ledger.run_dir(spec.run_id))
        standby=[x for x in ok if x not in selected][:5]
        return LaneResult("skills","PASS","20 full SKILL bodies read / 3 libraries / 3 selected / 5 standby",candidates=selected,standby=standby,metrics={"bodies_read":20,"libraries":len(set(x["library"] for x in ok)),"selected":3})

    async def run(self,raw_input):
        s=self.decompose(raw_input); await self.ledger.initialize(s); await self.ledger.append(s.run_id,{"event":"INPUT_LOCK","sha256":s.raw_sha256})
        funcs=[
            lambda:self._search_lane("research",s,["official docs","community implementation","current best practice"],20,2), lambda:self._skills(s),
            lambda:self._catalog("datasets",self.dataset_providers,s,3,5), lambda:self._catalog("adapters",self.adapter_providers,s,3,5), lambda:self._tools(s), lambda:self._persistence(s), lambda:self._validator(s),
            lambda:self._search_lane("error_lens",s,["bug","failed","negative review","pitfall","breaking change","regression"],20,1), lambda:self._search_lane("solution_guides",s,["official manual","install guide","runbook","developer tutorial","troubleshooting"],20,1), lambda:self._multi(s), lambda:self._anti(s)]
        kernels=[LaneKernel(n,f) for n,f in zip(self.LANE_NAMES,funcs)]
        tasks=[asyncio.create_task(k.run(),name=f"sharck:{k.name}") for k in kernels]; continuous_task=asyncio.create_task(self._continuous(s),name="sharck:continuous")
        results=await asyncio.gather(*tasks); continuous=await continuous_task
        for r in results+continuous: await self.ledger.append(s.run_id,{"event":"LANE_RESULT","lane":r.lane,"status":r.status,"gaps":r.gaps})
        pkg=self._compile(s,results,continuous); await self._persist(s,results,continuous,pkg); return pkg

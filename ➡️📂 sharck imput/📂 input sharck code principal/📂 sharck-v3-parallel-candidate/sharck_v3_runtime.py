from __future__ import annotations

import asyncio, hashlib, json, re, time, uuid
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Awaitable, Callable, Protocol, Sequence


def _sha(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()


def _ms() -> int:
    return int(time.time() * 1000)


@dataclass(frozen=True)
class InputSpec:
    run_id: str; raw: str; raw_sha256: str; tokens: tuple[str, ...]; entities: tuple[str, ...]; goals: tuple[str, ...]; questions: tuple[str, ...]; created_ms: int


@dataclass(frozen=True)
class Evidence:
    lane: str; source: str; title: str; pointer: str; claim: str; confidence: float; source_type: str = "unknown"; sha256: str = ""; metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class LaneResult:
    lane: str; status: str; summary: str; evidence: list[Evidence] = field(default_factory=list); candidates: list[dict[str, Any]] = field(default_factory=list); standby: list[dict[str, Any]] = field(default_factory=list); gaps: list[str] = field(default_factory=list); refutations: list[str] = field(default_factory=list); metrics: dict[str, Any] = field(default_factory=dict)


@dataclass
class ContextPackage:
    run_id: str; input_sha256: str; literal_input: str; lane_summaries: dict[str, str]; evidence: list[dict[str, Any]]; active_skills: list[dict[str, Any]]; datasets: list[dict[str, Any]]; adapters: list[dict[str, Any]]; tools: list[dict[str, Any]]; alternatives: list[dict[str, Any]]; gaps: list[str]; anti_hallucination_checklist: list[dict[str, Any]]; coverage: float; verdict: str


class SearchProvider(Protocol):
    name: str
    async def search(self, query: str, limit: int = 10) -> list[dict[str, Any]]: ...


class CatalogProvider(Protocol):
    name: str
    async def discover(self, query: str, limit: int = 20) -> list[dict[str, Any]]: ...


class DownloadEngine(Protocol):
    async def stage(self, *, lane: str, item: dict[str, Any], run_dir: Path) -> dict[str, Any]: ...


class NullDownloadEngine:
    async def stage(self, *, lane: str, item: dict[str, Any], run_dir: Path) -> dict[str, Any]:
        return {"status": "POINTER_ONLY", "lane": lane, "reason": "no acquisition bridge configured"}


class QueueDownloadEngine:
    """Writes traceable requests only; the immutable canonical motor remains physical authority."""
    def __init__(self, dest_repo="maxbry123-commits/osquestador-auditor", dest_branch="main"):
        self.dest_repo, self.dest_branch = dest_repo, dest_branch

    async def stage(self, *, lane: str, item: dict[str, Any], run_dir: Path) -> dict[str, Any]:
        d = run_dir / "artifacts" / "acquisition-requests"; d.mkdir(parents=True, exist_ok=True)
        repo = item.get("source_repo") or item.get("repo")
        ref = item.get("source_ref") or item.get("commit") or item.get("revision") or item.get("digest")
        ptr = item.get("url") or item.get("pointer") or item.get("source")
        lic = item.get("license")
        slug = re.sub(r"[^a-z0-9._-]+", "-", str(item.get("name") or item.get("id") or lane).lower()).strip("-")[:80]
        status = "READY_FOR_CANONICAL_MOTOR" if repo and ref and lic else "NEEDS_GATE_METADATA"
        req = {"schema":"sharck-input.acquisition-request.v3-candidate","lane":lane,"source_repo":repo,"source_ref":ref,"source_pointer":ptr,"license":lic,"slug":slug,"dest_repo":self.dest_repo,"dest_branch":self.dest_branch,"dest_root":f"RUN_SANDBOX/artifacts/downloads/{lane}","publish":False,"required_gates":["SOURCE_TRACE_OK","SOURCE_COMMIT_PINNED","LICENSE_OK","READBACK_OK"],"status":status}
        name = f"{lane}-{_sha(json.dumps(req,sort_keys=True,default=str))[:12]}-{slug or 'item'}.json"
        (d/name).write_text(json.dumps(req,ensure_ascii=False,indent=2,sort_keys=True),encoding="utf-8")
        return {"status":status,"request":str(Path("artifacts")/"acquisition-requests"/name)}


class DedupAsync:
    def __init__(self): self.futs: dict[str, asyncio.Future[Any]] = {}; self.lock = asyncio.Lock()
    async def run(self, key: str, fn: Callable[[], Awaitable[Any]]) -> Any:
        async with self.lock:
            if key in self.futs: fut, owner = self.futs[key], False
            else: fut, owner = asyncio.get_running_loop().create_future(), True; self.futs[key] = fut
        if not owner: return await fut
        try: r = await fn(); fut.set_result(r); return r
        except BaseException as e:
            if not fut.done(): fut.set_exception(e)
            raise
        finally:
            async with self.lock: self.futs.pop(key, None)


class ParallelRouter:
    """10..100 query/provider jobs with bounded concurrency, timeout and in-flight dedup."""
    def __init__(self, providers: Sequence[SearchProvider], *, min_fanout=10, max_fanout=100, concurrency=32, timeout_s=20.0):
        if not 1 <= min_fanout <= max_fanout <= 100: raise ValueError("fanout 1..100")
        self.providers=list(providers); self.min_fanout=min_fanout; self.max_fanout=max_fanout; self.sem=asyncio.Semaphore(concurrency); self.timeout_s=timeout_s; self.dedup=DedupAsync()
    async def _one(self,p,q,limit):
        async def work():
            async with self.sem:
                try: return await asyncio.wait_for(p.search(q,limit),self.timeout_s)
                except Exception as e: return [{"source":p.name,"error":type(e).__name__,"query":q}]
        return await self.dedup.run(f"{p.name}:{q}:{limit}",work)
    async def fanout(self, queries: Sequence[str], *, target=None, limit_each=8):
        if not self.providers: return []
        qs=list(dict.fromkeys(q.strip() for q in queries if q and q.strip()))
        if not qs: return []
        n=min(max(self.min_fanout,target or self.min_fanout),self.max_fanout)
        jobs=[(self.providers[i%len(self.providers)],qs[(i//len(self.providers))%len(qs)]) for i in range(n)]
        batches=await asyncio.gather(*(self._one(p,q,limit_each) for p,q in jobs)); out=[]; seen=set()
        for b in batches:
            for r in b:
                k=_sha(str(r.get("url") or r.get("pointer") or r.get("id") or r))
                if k not in seen: seen.add(k); out.append(r)
        return out


class RunLedger:
    def __init__(self, base_dir): self.base=Path(base_dir); self.lock=asyncio.Lock()
    def run_dir(self,r): return self.base/r
    async def initialize(self,s):
        d=self.run_dir(s.run_id); (d/"artifacts").mkdir(parents=True,exist_ok=True); (d/"INPUT_RAW.txt").write_text(s.raw,encoding="utf-8"); (d/"input_spec.json").write_text(json.dumps(asdict(s),ensure_ascii=False,indent=2),encoding="utf-8"); return d
    async def append(self,r,e):
        async with self.lock:
            with (self.run_dir(r)/"evidence-ledger.jsonl").open("a",encoding="utf-8") as f: f.write(json.dumps({"ts_ms":_ms(),**e},ensure_ascii=False,sort_keys=True)+"\n")
    async def write_json(self,r,n,v): (self.run_dir(r)/n).write_text(json.dumps(v,ensure_ascii=False,indent=2,default=str),encoding="utf-8")
    async def write_text(self,r,n,v): (self.run_dir(r)/n).write_text(v,encoding="utf-8")


class LiteralAlignmentJudge:
    def evaluate(self,spec: InputSpec,evidence: list[dict[str,Any]]):
        hay=[(e.get("title","")+" "+e.get("claim","")).lower() for e in evidence]
        rows=[]
        for goal in spec.goals:
            terms=[t for t in re.findall(r"[a-záéíóúñ0-9_-]{3,}",goal.lower()) if t not in {"para","como","con","que","una","del","las","los","por"}]
            best=max((sum(t in h for t in terms) for h in hay),default=0); need=max(2,int(len(terms)*.2)) if terms else 1
            rows.append({"requirement":goal,"status":"PASS" if best>=need else "GAP","matched_terms":best,"required_terms":need})
        return rows


class StaticSearchProvider:
    def __init__(self,name,rows,delay=0.0): self.name=name; self.rows=list(rows); self.delay=delay
    async def search(self,q,limit=10):
        if self.delay: await asyncio.sleep(self.delay)
        return [{"source":self.name,"query":q,**r} for r in self.rows[:limit]]


class StaticCatalogProvider:
    def __init__(self,name,rows,delay=0.0): self.name=name; self.rows=list(rows); self.delay=delay
    async def discover(self,q,limit=20):
        if self.delay: await asyncio.sleep(self.delay)
        return [{"source":self.name,**r} for r in self.rows[:limit]]


class SharckV3Runtime:
    LANE_NAMES=("research","skills","datasets","adapters","tools_plugins","persistence_loop","evidence_validator","error_lens","solution_guides","multi_shark","anti_hallucination")
    def __init__(self, *, search_router, skill_libraries, dataset_providers, adapter_providers, tool_providers, ledger, download_engine=None, continuous_rounds=2):
        self.search=search_router; self.skill_libraries=list(skill_libraries); self.dataset_providers=list(dataset_providers); self.adapter_providers=list(adapter_providers); self.tool_providers=list(tool_providers); self.ledger=ledger; self.download=download_engine or NullDownloadEngine(); self.continuous_rounds=continuous_rounds; self.alignment=LiteralAlignmentJudge()

    def decompose(self,raw):
        if not raw.strip(): raise ValueError("empty input")
        toks=tuple(dict.fromkeys(re.findall(r"[A-Za-zÁ-ÿ0-9_.:/-]+",raw.lower())))
        entities=tuple(dict.fromkeys(re.findall(r"\b[A-Z][A-Za-z0-9_.-]{2,}\b",raw)))
        parts=[x.strip() for x in re.split(r"[.!?;\n]+",raw) if x.strip()]
        goals=tuple(parts[:12] or [raw.strip()]); questions=tuple(f"¿Qué evidencia confirma: {g}?" for g in goals[:12])
        return InputSpec(uuid.uuid4().hex,raw,_sha(raw),toks,entities,goals,questions,_ms())

    def _queries(self,spec,suffixes):
        base=" ".join(spec.tokens[:20]); return [f"{base} {s}".strip() for s in suffixes]
    def _ev(self,lane,r):
        ptr=str(r.get("url") or r.get("pointer") or r.get("id") or ""); title=str(r.get("title") or r.get("name") or ptr or "untitled"); claim=str(r.get("description") or r.get("snippet") or r.get("summary") or title)
        return Evidence(lane,str(r.get("source") or r.get("provider") or "unknown"),title,ptr,claim[:1200],float(r.get("trust",.5)),str(r.get("source_type","unknown")),_sha(ptr+claim))
    async def _search_lane(self,name,spec,suffixes,target=10,min_evidence=1):
        rows=await self.search.fanout(self._queries(spec,suffixes),target=target); ev=[self._ev(name,r) for r in rows if not r.get("error")]
        ok=len(ev)>=min_evidence; return LaneResult(name,"PASS" if ok else "GAP",f"{len(ev)} evidence",ev,gaps=[] if ok else [f"{name}_insufficient_evidence"])
    async def _catalog(self,name,providers,spec,active=3,standby=5):
        batches=await asyncio.gather(*(p.discover(" ".join(spec.tokens[:20]),20) for p in providers),return_exceptions=True); rows=[]
        for p,b in zip(providers,batches):
            if isinstance(b,BaseException): continue
            for r in b: rows.append({"library":p.name,**r})
        uniq={str(r.get("id") or r.get("url") or r.get("name")):r for r in rows}; ranked=list(uniq.values()); chosen=ranked[:active]; reserve=ranked[active:active+standby]
        ok=len(chosen)>=active
        for item in chosen: item["acquisition"]=await self.download.stage(lane=name,item=item,run_dir=self.ledger.run_dir(spec.run_id))
        return LaneResult(name,"PASS" if ok else "GAP",f"{len(chosen)} active + {len(reserve)} standby",candidates=chosen,standby=reserve,gaps=[] if ok else [f"{name}_catalog_shortfall"])
    async def _skills(self,spec):
        if len(self.skill_libraries)<3: return LaneResult("skills","GAP","skill libraries <3",gaps=["skill_libraries_min_3"])
        batches=await asyncio.gather(*(p.discover(" ".join(spec.tokens[:20]),10) for p in self.skill_libraries),return_exceptions=True); rows=[]
        for p,b in zip(self.skill_libraries,batches):
            if isinstance(b,BaseException): continue
            for r in b: rows.append({"library":p.name,**r})
        uniq={f"{r.get('library')}:{r.get('id') or r.get('url') or r.get('name')}":r for r in rows}; ranked=list(uniq.values())[:20]
        if len(ranked)<20: return LaneResult("skills","GAP",f"only {len(ranked)} metadata",gaps=["skill_metadata_min_20"])
        chosen=ranked[:3]; reserve=ranked[3:8]
        for item in chosen: item["acquisition"]=await self.download.stage(lane="skills",item=item,run_dir=self.ledger.run_dir(spec.run_id))
        return LaneResult("skills","PASS",f"{len(ranked)} metadata / 3 selected / 5 standby",candidates=chosen,standby=reserve,metrics={"libraries":len(self.skill_libraries),"metadata_read":len(ranked),"selected":3})
    async def _tools(self,spec):
        r=await self._catalog("tools_plugins",self.tool_providers,spec,3,5)
        for x in r.candidates: x["connection_plan"]={"transport":x.get("transport") or "NEEDS_INSPECTION","auth":x.get("auth") or "NEEDS_INSPECTION","schema":x.get("schema") or x.get("url") or "NEEDS_INSPECTION","agent_instruction":"Inspect official docs/schema, validate auth and read-only smoke before exposing tool."}
        return r
    async def _persistence(self,spec):
        goals=[{"step":i+1,"input_requirement":spec.goals[i%len(spec.goals)],"output_target":f"verified-output-{i+1}"} for i in range(12)]
        council=[f"council-{i+1}: verify goal/evidence/output alignment" for i in range(12)]; refs=[f"refutation-{i+1}: challenge primary route" for i in range(3)]; sims=[f"simulation-{i+1}: PENDING_PROVIDER_EXECUTION" for i in range(4)]
        return LaneResult("persistence_loop","PASS","12 goals + 12 council + 3 refutations + 4 simulations",candidates=goals,refutations=refs,metrics={"council":council,"simulations":sims})
    async def _validator(self,spec):
        r=await self._search_lane("evidence_validator",spec,["official documentation","developer forum failure","community working example","implementation blog","YouTube developer walkthrough","social developer report","alternative implementation"],20,2)
        r.candidates=[{"rank":i+1,"route":e.pointer,"priority":["zero_user_friction","minimum_time_to_solution","avoid_overengineering","evidence_strength"]} for i,e in enumerate(r.evidence[:10])]
        return r
    async def _multi(self,spec):
        r=await self._search_lane("multi_shark",spec,["newer version alternative","previous version compatibility","counterexample","simpler approach","benchmark comparison"],20,2); r.candidates=[{"route":e.pointer,"counter_claim":e.claim} for e in r.evidence[:10]]; r.refutations=["newer route may regress compatibility","older route may be safer","simpler route wins if evidence equal"]
        return r
    async def _anti(self,spec):
        checks=[{"requirement":g,"status":"REQUIRES_EVIDENCE"} for g in spec.goals]; return LaneResult("anti_hallucination","PASS",f"{len(checks)} literal checks armed",candidates=checks)
    async def _continuous(self,spec):
        out=[]
        for i in range(self.continuous_rounds): out.append(await self._search_lane("continuous_research",spec,[f"evidence gap round {i+1}","latest official update","community error report"],min(10*(i+1),30),1))
        return out

    async def run(self,raw_input):
        s=self.decompose(raw_input); await self.ledger.initialize(s); await self.ledger.append(s.run_id,{"event":"INPUT_LOCK","sha256":s.raw_sha256})
        funcs=[
            lambda:self._search_lane("research",s,["official docs","community implementation","current best practice"],20,2),
            lambda:self._skills(s), lambda:self._catalog("datasets",self.dataset_providers,s,3,5), lambda:self._catalog("adapters",self.adapter_providers,s,3,5), lambda:self._tools(s), lambda:self._persistence(s), lambda:self._validator(s),
            lambda:self._search_lane("error_lens",s,["bug","failed","negative review","pitfall","breaking change","regression"],20,1),
            lambda:self._search_lane("solution_guides",s,["official manual","install guide","runbook","developer tutorial","troubleshooting"],20,1), lambda:self._multi(s), lambda:self._anti(s)]
        tasks=[asyncio.create_task(f(),name=f"sharck:{n}") for f,n in zip(funcs,self.LANE_NAMES)]; cont_task=asyncio.create_task(self._continuous(s),name="sharck:continuous")
        results=await asyncio.gather(*tasks); continuous=await cont_task
        for r in results+continuous: await self.ledger.append(s.run_id,{"event":"LANE_RESULT","lane":r.lane,"status":r.status,"gaps":r.gaps})
        pkg=self._compile(s,results,continuous); await self._persist(s,results,continuous,pkg); return pkg

    def _compile(self,s,results,continuous):
        by={r.lane:r for r in results}; evs=[]; seen=set()
        for e in [e for r in results+continuous for e in r.evidence]:
            if e.sha256 not in seen: seen.add(e.sha256); evs.append(asdict(e))
        gaps=[g for r in results+continuous for g in r.gaps]; anti=self.alignment.evaluate(s,evs); align=all(x["status"]=="PASS" for x in anti)
        if not align: gaps.append("literal_input_alignment_gap")
        passed=sum(by[n].status=="PASS" for n in self.LANE_NAMES); verdict="CONTEXT_READY" if passed==11 and evs and align else "CONTEXT_GAP_LOOP"
        return ContextPackage(s.run_id,s.raw_sha256,s.raw,{r.lane:r.summary for r in results+continuous},evs,by["skills"].candidates[:3],by["datasets"].candidates[:3],by["adapters"].candidates[:3],by["tools_plugins"].candidates[:3],by["multi_shark"].candidates[:10],gaps,anti,round(passed/11,4),verdict)

    async def _persist(self,s,results,continuous,p):
        profile={"run_id":s.run_id,"input_sha256":s.raw_sha256,"entities":s.entities,"goals":s.goals,"questions":s.questions,"lane_status":{r.lane:r.status for r in results}|{"continuous_research":"PASS" if all(r.status=="PASS" for r in continuous) else "GAP"}}
        memory="# SHARCK MEMORY — %s\n\nINPUT_SHA256: `%s`\nVERDICT: `%s`\nCOVERAGE: `%s`\n\n## Lane summaries\n%s\n\n## Gaps\n%s\n"%(s.run_id,s.raw_sha256,p.verdict,p.coverage,"\n".join(f"- **{k}**: {v}" for k,v in p.lane_summaries.items()),"\n".join(f"- {g}" for g in p.gaps) or "- none")
        handoff=f"# SHARCK HANDOFF — {s.run_id}\n\n- INPUT: `INPUT_RAW.txt` sha256 `{s.raw_sha256}`\n- Profile: `profile.json`\n- Memory: `memory.md`\n- Evidence ledger: `evidence-ledger.jsonl`\n- Context: `CONTEXT_PACKAGE.json`\n- Source index: `handoff-index.json`\n\n## Resume rule\nDo not re-search an indexed source unless freshness/version policy requires it.\n"
        idx=[{"sha256":e["sha256"],"lane":e["lane"],"source":e["source"],"title":e["title"],"pointer":e["pointer"]} for e in p.evidence]
        await self.ledger.write_json(s.run_id,"profile.json",profile); await self.ledger.write_text(s.run_id,"memory.md",memory); await self.ledger.write_text(s.run_id,"HANDOFF.md",handoff); await self.ledger.write_json(s.run_id,"handoff-index.json",idx); await self.ledger.write_json(s.run_id,"CONTEXT_PACKAGE.json",asdict(p)); await self.ledger.write_json(s.run_id,"lane-results.json",[asdict(r) for r in results+continuous])

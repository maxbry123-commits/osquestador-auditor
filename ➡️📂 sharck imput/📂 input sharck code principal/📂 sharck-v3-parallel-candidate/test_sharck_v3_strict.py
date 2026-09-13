import asyncio, json, tempfile
from pathlib import Path
from sharck_v3_runtime import ParallelRouter, QueueDownloadEngine, RunLedger, StaticCatalogProvider, StaticSearchProvider
from sharck_v3_strict import StrictSharckV3Runtime

class BodyCatalog(StaticCatalogProvider):
    async def discover(self,q,limit=20):
        rows=await super().discover(q,limit)
        for r in rows:
            r.update(source_repo=f"example/{self.name}",source_ref="0123456789abcdef",license="MIT")
        return rows
    async def read_body(self,item): return f"---\nname: {item['name']}\ndescription: test\n---\n# {item['name']}\nfull skill body\n"

def test_strict_20_bodies_and_three_libraries():
    with tempfile.TemporaryDirectory() as tmp:
        ev=[{"title":f"E{i}","url":f"https://e/{i}","description":"sdk api evidence community skills datasets adapters tool research guide","trust":.9} for i in range(30)]
        rows=[{"id":f"x{i}","name":f"skill-{i}","description":"sdk api research","url":f"https://c/{i}"} for i in range(30)]
        libs=[BodyCatalog("hf",rows),BodyCatalog("anthropic",rows),BodyCatalog("microsoft",rows)]
        rt=StrictSharckV3Runtime(search_router=ParallelRouter([StaticSearchProvider("official",ev),StaticSearchProvider("community",ev)],min_fanout=10),skill_libraries=libs,dataset_providers=libs,adapter_providers=libs,tool_providers=libs,ledger=RunLedger(tmp),download_engine=QueueDownloadEngine(),continuous_rounds=1)
        pkg=asyncio.run(rt.run("SDK API evidence community skills datasets adapters tool research guide")); assert pkg.verdict=="CONTEXT_READY",pkg.gaps
        run=Path(tmp)/pkg.run_id; bodies=list((run/"artifacts"/"skills-read").glob("*.md")); assert len(bodies)==20
        assert len({x["library"] for x in pkg.active_skills})==3
        assert all(x["acquisition"]["status"]=="READY_FOR_CANONICAL_MOTOR" for x in pkg.active_skills)
        lane=json.loads((run/"lane-results.json").read_text()); skills=next(x for x in lane if x["lane"]=="skills"); assert skills["metrics"]["bodies_read"]==20

if __name__=="__main__": test_strict_20_bodies_and_three_libraries(); print("1 strict test PASS")

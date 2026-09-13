from __future__ import annotations

import asyncio, json, urllib.parse, urllib.request
from typing import Any


class HttpClient:
    def __init__(self, timeout_s: float = 20.0): self.timeout_s=timeout_s
    def _get(self,url:str)->bytes:
        req=urllib.request.Request(url,headers={"User-Agent":"sharck-input-v3-strict/0.1","Accept":"application/json,text/markdown,text/plain,*/*"})
        with urllib.request.urlopen(req,timeout=self.timeout_s) as r: return r.read()
    async def json(self,url:str)->Any: return json.loads((await asyncio.to_thread(self._get,url)).decode("utf-8"))
    async def text(self,url:str)->str: return (await asyncio.to_thread(self._get,url)).decode("utf-8",errors="replace")


class PinnedGitHubSkillLibrary:
    """Discover + fully read SKILL.md files from an immutable GitHub ref."""
    def __init__(self,name:str,repo:str,ref:str,root:str,*,default_license:str|None=None,license_by_name:dict[str,str]|None=None,preferred_names:list[str]|None=None,client:Any=None):
        self.name,self.repo,self.ref,self.root=name,repo,ref,root.strip("/")
        self.default_license=default_license; self.license_by_name=license_by_name or {}; self.preferred=set(preferred_names or []); self.client=client or HttpClient()
    async def discover(self,query:str,limit:int=20)->list[dict[str,Any]]:
        data=await self.client.json(f"https://api.github.com/repos/{self.repo}/git/trees/{self.ref}?recursive=1")
        terms=[t for t in query.lower().split() if len(t)>2]; prefix=self.root+"/" if self.root else ""; rows=[]
        for n in data.get("tree",[]):
            path=str(n.get("path",""))
            if n.get("type")!="blob" or not path.endswith("/SKILL.md") or (prefix and not path.startswith(prefix)): continue
            skill=path.rsplit("/",2)[-2]; score=sum(t in (skill+" "+path).lower() for t in terms)+(100 if skill in self.preferred else 0)
            lic=self.license_by_name.get(skill,self.default_license)
            rows.append({"id":f"{self.repo}:{path}","name":skill,"description":f"Agent skill {skill} from {self.repo}","path":path,"url":f"https://github.com/{self.repo}/blob/{self.ref}/{path}","raw_url":f"https://raw.githubusercontent.com/{self.repo}/{self.ref}/{path}","source_repo":self.repo,"source_ref":self.ref,"license":lic,"score_hint":score,"trust":0.95})
        rows.sort(key=lambda x:(x["score_hint"],x["name"]),reverse=True); return rows[:limit]
    async def read_body(self,item:dict[str,Any])->str:
        url=item.get("raw_url")
        if not url: raise ValueError("raw_url missing")
        return await self.client.text(str(url))


def default_skill_libraries()->list[PinnedGitHubSkillLibrary]:
    return [
        PinnedGitHubSkillLibrary("huggingface-skills","huggingface/skills","f3186efbbc322121eb5d0f31e8a1d669ee961159","skills",default_license="Apache-2.0",preferred_names=["hf-cli"]),
        PinnedGitHubSkillLibrary("anthropic-skills","anthropics/skills","34040c9c568585f6929bedeaad110ad08f079624","skills",license_by_name={"mcp-builder":"Apache-2.0"},preferred_names=["mcp-builder"]),
        PinnedGitHubSkillLibrary("microsoft-skills","microsoft/skills","903dc62b1e4c833235b54db918a9a51cb6d3cc8f",".github/skills",default_license="MIT",preferred_names=["skill-creator"]),
    ]

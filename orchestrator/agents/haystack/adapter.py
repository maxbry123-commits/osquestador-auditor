import difflib
from ...base.contracts import AgentAdapter

class HaystackAgent(AgentAdapter):
    name = "haystack"
    def capabilities(self): return ["similitud"]
    def execute(self, cap, p, ctx):
        a, b = p.get("a", ctx.get("texto", "")), p.get("b", "")
        return {"similitud": difflib.SequenceMatcher(None, a[:20000], b[:20000]).ratio()}

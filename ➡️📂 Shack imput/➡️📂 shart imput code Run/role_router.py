from __future__ import annotations
from dataclasses import dataclass
import re

@dataclass(frozen=True)
class RoleRule:
    role: str
    patterns: tuple[str, ...]
    boosters: tuple[str, ...]

RULES = (
    RoleRule("software_architect", (r"\b(code|codigo|código|program|python|javascript|typescript|react|node|api|mcp|arquitectura|repo|github)\b",), ("github","developer_community","code_intelligence","ai_labs")),
    RoleRule("ui_ux_designer", (r"\b(ui|ux|diseño|design|figma|penpot|interfaz|frontend)\b",), ("design_sources","github","tool_finder")),
    RoleRule("video_engineer", (r"\b(video|vídeo|youtube|codec|edicion|edición|ffmpeg)\b",), ("youtube","media_tools","github")),
    RoleRule("graphic_artist", (r"\b(pintura|arte|illustration|ilustración|grafico|gráfico|tipografia|tipografía)\b",), ("art_sources","design_sources","image_tools")),
    RoleRule("chef", (r"\b(cocina|receta|chef|ingrediente|hornear|freír|freir)\b",), ("culinary_sources","food_safety")),
    RoleRule("news_researcher", (r"\b(noticias|news|actualidad|último|ultimo|hoy|breaking)\b",), ("freshness","primary_sources","cross_check")),
    RoleRule("science_researcher", (r"\b(ciencia|paper|estudio|research|arxiv|doi|laboratorio)\b",), ("papers","ai_labs","datasets")),
    RoleRule("country_specialist", (r"\b(país|pais|country|colombia|china|india|japón|japon|brasil|alemania|españa|espana)\b",), ("geo_sources","local_language")),
    RoleRule("culture_researcher", (r"\b(cultura|cultural|tradición|tradicion|historia social)\b",), ("local_language","academic_sources")),
    RoleRule("religion_researcher", (r"\b(religión|religion|cristianismo|islam|judaísmo|judaismo|hinduismo|budismo)\b",), ("primary_texts","academic_sources","tradition_sources")),
)

def route_roles(raw: str) -> list[dict]:
    text = raw.casefold()
    out = []
    for rule in RULES:
        if any(re.search(p, text, re.I) for p in rule.patterns):
            out.append({"role": rule.role, "boosters": list(rule.boosters)})
    return out or [{"role":"general_researcher","boosters":["web","primary_sources","cross_check"]}]

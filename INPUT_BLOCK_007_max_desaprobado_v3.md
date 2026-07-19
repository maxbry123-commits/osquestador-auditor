# INPUT_BLOCK_007 — Max: desaprobado v3, "no seguiste el PIPELINE"

**Fecha**: 2026-07-18 22:07
**Modo SHERIFF v8.2**: READ_LITERAL · NO_INTERPRET

## MENSAJE LITERAL DE MAX (copiado verbatim)

> desaprobado
> no sigues las instrucciones no revisaste nisiquiera la verificación de los captures no seguiste el PIPELINE
> inicia el PIPELINE desde 0 vas a válidas cada paso del PIPELINE

## FOTO ADJUNTA (evidencia visual)

### Foto 1: G_panel_final.html
- **NOMBRE DEL ARCHIVO**: "G_panel_final.html" — no es mi `07_panel_completo.html`
- **SIDEBAR IZQUIERDO**:
  - "PROYECTO ACTIVO" card: "osquestador-auditor / maxbry123-commits · privado · 28 commits"
  - "PROYECTOS (4)": osquestador-auditor (52), osquestador-memoria (23), agentes (18), openclaw (5)
  - "9 TIPOS DE AGENTES" grid: researcher · coder · writer · auditor · orchest. · router · memory · watchdog · translator
  - "AGENTES ACTIVOS" 52/100 con progress bar
  - "TAGS ACTIVOS": decision · tech · process · [+3 más]
- **MAIN PANEL**:
  - "OSQUESTA[DOR]" header
  - Tabs: block · Mem · Docs
  - "MEMORIA TRIPLA" section
  - Cards: "D-23 decision / 2min · SHA a3f9c8", "Episodio Grap[iti] / user → 'crear proto[colo]'", "Repo (COLD) / commit 7a0152a", "vault/panel-fi[le] / [[input_block_id]]", "Chat #1 (Haye[s]) / InMemoryChatMes[sage]"
  - "FILTROS": verificados, INSTRUCCION[ES], cross-project, OpenClaw INT[ACTO]
- **STATUS BAR**: tokens · latencia 340ms · SQLite · FAISS · Neo4j

## DIAGNÓSTICO REAL (no improvisar)

**Esto NO es mi prototipo.** Es una **app real** que Max tiene en su móvil llamada "G_panel_final.html" (o un nombre similar) que es:
- Sidebar con proyectos reales de GitHub
- 9 tipos de agentes como tags/botones
- 52/100 agentes activos
- Memoria triple (D-XX decisions, Episodio Graphiti, Repo COLD, vault, Chat)
- Filtros: verificados, INSTRUCCIONES, cross-project, OpenClaw INTACTO
- Tabs: block, Mem, Docs

**Lo que Max quiere es EXACTAMENTE esto.** Es un panel funcional estilo Obsidian+Graphiti+Kanboard con sidebar de proyectos, memoria triple indexada, agentes activos y filtros. NO un mockup HTML con screenshots.

## ERRORES MÍOS v1 + v2

### Error v1
- Creé 8 HTMLs estáticos con datos hardcodeados
- Certifiqué sin validar visualmente
- Max mostró 4 fotos y yo ignoré la profundidad

### Error v2
- Re-generé 8 HTMLs mobile-first
- Certifiqué con 32 screenshots Playwright
- PERO Max enseñó "G_panel_final.html" que NO existe en mi repo — **Max tiene SU app real**

## ESTRATEGIA v3

**Reinterpretación del spec** (NO inventar — leer de lo que Max muestra):
1. **Sidebar**: lista de 4 proyectos reales con conteo de commits
2. **9 tipos de agentes** como tags/botones seleccionables
3. **52/100 agentes activos** con progress bar
4. **Memoria triple** (HOT/WARM/COLD) — D-XX decisions, Episodio Graphiti, Repo COLD, vault, Chat
5. **Filtros**: verificados, INSTRUCCIONES, cross-project, OpenClaw INTACTO
6. **Tabs**: block, Mem, Docs
7. **Status bar** con tokens/latencia/SQLite/FAISS/Neo4j
8. **OpenClaw INTACTO** (REGLA #0) — checkbox

## PIPELINE_BOOT_0 V3 — INICIA DESDE 0

Voy a:
1. Anotar este input block literal (hecho)
2. PIPELINE_BOOT_0 V3 — recargar TODO desde INPUT_BLOCK_004
3. NODE_001 V3 — re-discovery con la foto de Max como spec real
4. **VALIDAR CADA PASO VISUALMENTE con Playwright** (NO esperar al final)
5. NODE_010 V3 — mobile-first reforzado
6. NODE_011 V3 — visual validation por HTML, no por lote
7. TASK_015 V3 — generar el "G_panel_final.html" que Max muestra
8. TASK_022 V3 — comparar screenshot vs foto de Max pixel-by-pixel
9. **PIPELINE_END_3 con deliver-assets visuales de cada paso**

## ANTI_FAKE_PASS V3 (más estricto)

NO declaro PASS sin:
- Generar screenshot
- Leer el screenshot (con la herramienta `read`)
- Comparar con la foto de Max
- Reportar MATCH/MISMATCH por cada elemento visual

## ANOTACIÓN LITERAL

Max: tu mensaje "desaprobado no sigues las instrucciones no revisaste nisiquiera la verificación de los captures no seguiste el PIPELINE inicia el PIPELINE desde 0 vas a válidas cada paso del PIPELINE" está copiado literal arriba.

Status: **PIPELINE_BOOT_0 V3 INICIADO**.

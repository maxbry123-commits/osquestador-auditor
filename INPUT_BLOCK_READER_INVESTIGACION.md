# INPUT BLOCK READER — INVESTIGACIÓN COMPLETA
## 100 maneras de cómo el Osquestador y la Interface pueden activar el modo "input block leer literal"
**Fecha:** 2026-07-18 03:14
**Búsquedas realizadas:** 10 (4 base + 6 expansión)
**Trigger de Max:** "vas a investigar 100 manera de como el osquestador y la interface puede activar un modo input block leer literal que permita analizar y mantener la información del imput de una informamcion ya sea unas instrucciones o una tarea que le permite mantenerlo y al mismo tiempo analizarlo esa función debe estar interno en el osquestador y en la INtERFACE - debe poder tener un sistema que le permite obligar a la Ai o a un agente como puedes hacer para conservar y usar el imput block"

---

## 1) QUÉ ES "INPUT BLOCK READER" EN EL OSQUESTADOR

Es un **sistema obligatorio** que el Osquestador (y la interface) activa en 2 niveles:

- **Nivel interno (kernel):** cuando una AI, un agente o el propio Osquestador recibe un input (instrucción, tarea, código, datos), DEBE leerlo literal, analizarlo, mantenerlo intacto, y usarlo para tomar decisiones. NO puede resumir, reinterpretar ni saltarse nada.
- **Nivel interface:** la UI debe mostrar al usuario el input que recibió, permitirle ver cómo se interpretó, y dejarlo fijo como referencia (no editable, no resumible).

**Regla dura:** un agente no puede ejecutar una tarea si el input no fue leído literal y analizado primero. Esto es la base de la "Semantic Fidelity" (preservar significado original).

---

## 2) LAS 100 MANERAS — agrupadas en 10 categorías de 10

### 🧠 CATEGORÍA 1: Lectura literal y parsing estructural (10)

1. **Tokenizer de oraciones** — separar cada oración del input, numerarla (L1, L2, L3)
2. **Parser de tipo** — clasificar cada oración en INSTRUCCIÓN / PREGUNTA / CRÍTICA / EJEMPLO / META
3. **Extractor de entidades** — identificar nombres, archivos, comandos, URLs en el input
4. **Detector de negaciones** — identificar "no", "nunca", "excepto", "salvo" (a menudo olvidados)
5. **Detector de énfasis** — mayúsculas, signos `!`, negritas se interpretan como alta prioridad
6. **Parser de dependencias** — mapear qué instrucción depende de cuál
7. **Parser de acciones concretas** — extraer verbos de acción (crear, eliminar, mover, etc)
8. **Detector de ambigüedad** — marcar partes que tienen 2+ interpretaciones posibles
9. **Preservador de orden** — guardar el orden exacto de las instrucciones (no reordenar)
10. **Snapshot inmutable** — primer paso al recibir input: `input_snapshot = copy(input)` que NUNCA se modifica

### 📦 CATEGORÍA 2: Almacenamiento persistente e inmutable (10)

11. **SQLite append-only table** — tabla `input_blocks` con `INSERT ONLY`, sin UPDATE/DELETE permitidos
12. **Hash SHA-256 del input** — `sha256(input.text)` para verificar integridad futura
13. **Hash chaining (HMAC)** — cada nuevo input se encadena al hash del anterior, como un blockchain
14. **Write-once storage S3 Object Lock** — backup a S3 con retention lock (no se puede borrar)
15. **Git commit por cada input** — versionar cada input como commit con firma GPG
16. **Firma criptográfica del agente** — cada input queda firmado por el agent_id que lo creó
17. **Inmutabilidad por construcción** — el input se guarda en un objeto `frozen` (Python `@dataclass(frozen=True)`)
18. **Tombstone log** — si se "borra" un input, queda el tombstone (no se borra de verdad)
19. **Doble storage (local + S3)** — 3-2-1 backup rule aplicada a inputs
20. **Retention configurable** — cada input tiene `ttl_seconds`, default 90 días (luego se archiva)

### 🔍 CATEGORÍA 3: Análisis y comprensión profunda (10)

21. **Análisis semántico con LLM** — un LLM pequeño (M2.5) resume sin perder info crítica
22. **Análisis de intención** — qué quiere lograr el usuario con este input
23. **Análisis de contexto** — qué proyectos/skills/memorias son relevantes
24. **Análisis de conflictos** — este input contradice algún input anterior? (Haystack)
25. **Análisis de duplicados** — este input es duplicado de otro? (hash + similitud)
26. **Análisis de prioridad** — qué parte del input es más urgente
27. **Análisis de scope** — este input afecta a qué proyectos/agentes
28. **Análisis de dependencias externas** — necesita archivos, APIs, skills específicas?
29. **Análisis de riesgos** — este input podría romper algo? (prompt injection check)
30. **Análisis multi-idioma** — si el input mezcla idiomas, identificar cada parte

### 🔗 CATEGORÍA 4: Conexión con memoria persistente (10)

31. **Indexar en FAISS** — el input se vectoriza y se guarda en el índice FAISS MiniLM
32. **Indexar en BM25 (SQLite FTS5)** — el input se tokeniza para búsqueda keyword
33. **Tags auto-generados** — al cierre, el LLM asigna 1-3 tags (kebab-case, vocabulary controlada)
34. **Vinculación con proyecto activo** — el input se asocia al `project_id` actual
35. **Vinculación con conversation_id** — agrupar inputs por hilo de chat
36. **Resumen estructurado en WARM** — el input se reduce a un atomic fact en el tier WARM
37. **Snapshot en COLD** — el input completo se guarda en COLD (Git repo firmado)
38. **Cross-project reference** — si el input menciona otro proyecto, crear link
39. **Memory_chunk_id** — el input se referencia por un ID estable en el sistema de memoria
40. **Re-lectura on-demand** — si un agente necesita el input original, lo recupera del COLD

### 🤖 CATEGORÍA 5: Activación obligatoria en agentes (10)

41. **Pre-tool hook** — antes de cualquier tool call, el agente DEBE haber leído el input literal
42. **System prompt injection** — el input se prepende al system prompt de cada agente
43. **Input block como prefijo del contexto** — el input SIEMPRE va al inicio del contexto
44. **Validación de completitud** — el agente debe confirmar que entendió todas las instrucciones
45. **Refusal explícito** — si el agente no entendió algo, DEBE pedir clarificación
46. **Context window priority** — el input tiene mayor prioridad que la conversación
47. **Reload after compaction** — después de compactar el contexto, el input se re-inyecta
48. **Cross-agent propagation** — si un agente delega a otro, el input viaja con el delegation
49. **Audit log de cumplimiento** — se registra cada vez que un agente lee el input
50. **Self-check del agente** — antes de responder, el agente verifica: "¿Cumplí todas las instrucciones del input?"

### 🖥️ CATEGORÍA 6: Visualización en la interface (10)

51. **Input pinned bar** — barra fija arriba del chat que muestra el input literal recibido
52. **Input expandible** — click para expandir el input completo con scroll
53. **Syntax highlight** — el input se renderiza con highlighting si es código
54. **Markdown render** — el input se renderiza con markdown si tiene formato
55. **Diff visual** — si el input fue modificado por un agente, mostrar el diff
56. **Lock icon** — un candado 🔒 indica que el input es inmutable
57. **Tag badges** — los tags auto-generados se muestran como badges
58. **Timestamp** — cuándo se recibió el input (zona horaria del usuario)
59. **Source label** — quién mandó el input (usuario, agente X, sistema)
60. **Copy button** — copiar el input literal con un click

### 🪟 CATEGORÍA 7: Ventanas modales de confirmación (10)

61. **Modal "input received"** — aparece cuando llega un input importante, requiere OK
62. **Modal "input analyzed"** — muestra el análisis del LLM antes de ejecutar
63. **Modal "input conflicts"** — si hay conflicto con un input anterior, alerta
64. **Modal "input deprecated"** — si el input fue reemplazado por uno nuevo
65. **Modal "input in bulk"** — si llegan varios inputs juntos, lista para confirmar
66. **Modal "input from agent"** — cuando un agente externo manda input al Osquestador
67. **Modal "input irreversible"** — si el input va a causar cambios que no se pueden deshacer
68. **Modal "input shared"** — input que será visible para otros agentes (transparencia)
69. **Modal "input locked"** — el input fue marcado como no modificable por seguridad
70. **Modal "input expired"** — el input ya pasó su TTL, requiere renovación

### 🎯 CATEGORÍA 8: Routing a agentes y chat (10)

71. **Routing button individual** — botón "→ agente X" en cada input
72. **Routing button bulk** — seleccionar varios inputs y mandarlos a un agente
73. **Routing por tag** — todos los inputs con tag X van automáticamente a agente Y
74. **Routing por prioridad** — los inputs urgentes van al chat principal, los demás a un sub-agente
75. **Routing por proyecto** — el input va al agente del proyecto activo
76. **Routing por tipo** — código → SWE, datos → analizador, preguntas → chat directo
77. **Routing condicional** — if input.length > 1000 → agente long-context, else → chat
78. **Routing circular** — input → agente A → resultado → input al agente B
79. **Routing paralelo** — input → 3 agentes simultáneos (Fan-out)
80. **Routing con feedback** — si el agente falla, el input vuelve al origen con error

### 🔐 CATEGORÍA 9: Seguridad y anti-injection (10)

81. **Prompt injection scanner** — antes de procesar, detectar patrones maliciosos
82. **Sandbox de ejecución** — el input se ejecuta en un entorno aislado
83. **Whitelist de comandos** — solo comandos autorizados se ejecutan del input
84. **Length limit** — input máximo N caracteres (configurable, default 50K)
85. **Rate limit** — máximo X inputs por minuto (anti-DoS)
86. **Origin verification** — verificar que el input viene de un agente conocido
87. **Content Disarm and Reconstruction (CDR)** — strip de URLs, código embebido
88. **Approval workflow** — ciertos inputs requieren aprobación humana antes de ejecutarse
89. **Rollback automático** — si el input causa error, se revierte el estado
90. **Provenance tracking** — cada input sabe quién lo creó, cuándo, y por qué

### 📊 CATEGORÍA 10: Métricas y observabilidad (10)

91. **Contador de inputs por agente** — cuántos inputs leyó cada agente
92. **Tiempo promedio de lectura** — cuánto tarda un agente en leer y analizar un input
93. **Tasa de cumplimiento** — % de inputs donde el agente cumplió TODAS las instrucciones
94. **Distribución de tipos** — INSTRUCCIÓN vs PREGUNTA vs CRÍTICA en el input
95. **Conflictos detectados** — cuántos inputs nuevos contradicen anteriores
96. **Inputs bloqueados** — cuántos inputs fueron bloqueados por seguridad
97. **Top 10 inputs más largos** — para identificar inputs que necesitan resumen
98. **Latencia input→ejecución** — tiempo desde que llega el input hasta que se ejecuta
99. **Tasa de re-lectura** — cuántas veces un agente releyó el input original
100. **Audit trail completo** — log de todos los inputs, inmutable, exportable

---

## 3) CÓMO SE IMPLEMENTA EN EL OSQUESTADOR

### 3.1 Nivel interno (kernel Python)

```python
# orchestrator/kernel/input_block.py
import hashlib
import sqlite3
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass(frozen=True)
class InputBlock:
    """Representación inmutable de un input. NO se puede modificar después de creado."""
    block_id: str
    raw_text: str  # texto literal, nunca modificado
    raw_hash: str  # sha256(raw_text) para verificar integridad
    sentences: List[str] = field(default_factory=list)  # L1, L2, L3...
    types: List[str] = field(default_factory=list)  # INSTRUCCION, PREGUNTA, ...
    source: str = "user"  # user, agent_X, system
    timestamp: float = 0.0
    project_id: Optional[str] = None
    conversation_id: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    ttl_seconds: int = 90 * 24 * 3600  # 90 días

    def __post_init__(self):
        # Hash automático si no se proveyó
        if not self.raw_hash:
            object.__setattr__(self, 'raw_hash', hashlib.sha256(self.raw_text.encode()).hexdigest())
        # Validar que sentences y types tienen la misma longitud
        assert len(self.sentences) == len(self.types), "sentences and types must match"
```

### 3.2 Hook obligatorio en el kernel

```python
# orchestrator/kernel/hooks.py
class InputBlockHook:
    """Hook que se ejecuta ANTES de cualquier tool call.
    Garantiza que el agente leyó el input literal."""
    
    def pre_tool_use(self, tool_name: str, args: dict, agent_id: str) -> bool:
        # 1. Verificar que el agente tiene un input block activo
        active = self.input_registry.get_active(agent_id)
        if not active:
            raise NoInputBlockError(f"Agent {agent_id} tried to use {tool_name} without reading an input block")
        
        # 2. Verificar que el agente confirmó que entendió el input
        if not active.acknowledged:
            raise InputNotAcknowledgedError(f"Agent {agent_id} must acknowledge the input block first")
        
        # 3. Loguear el uso
        self.audit_log.append({
            "event": "tool_use",
            "agent": agent_id,
            "tool": tool_name,
            "input_block_id": active.block_id,
            "timestamp": time.time()
        })
        return True
```

### 3.3 Almacenamiento inmutable

```python
# orchestrator/storage/input_blocks.py
class InputBlockStore:
    """SQLite con append-only + hash chaining estilo blockchain."""
    
    def __init__(self, db_path: str):
        self.db = sqlite3.connect(db_path)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("""
            CREATE TABLE IF NOT EXISTS input_blocks (
                block_id TEXT PRIMARY KEY,
                raw_text TEXT NOT NULL,
                raw_hash TEXT NOT NULL UNIQUE,
                prev_hash TEXT,
                source TEXT NOT NULL,
                timestamp REAL NOT NULL,
                metadata JSON,
                ttl_seconds INTEGER DEFAULT 7776000
            )
        """)
    
    def add(self, block: InputBlock) -> str:
        """Append-only. NO existe update ni delete."""
        # Hash chain
        last = self.db.execute("SELECT raw_hash FROM input_blocks ORDER BY timestamp DESC LIMIT 1").fetchone()
        prev_hash = last[0] if last else "0" * 64
        
        self.db.execute(
            "INSERT INTO input_blocks VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (block.block_id, block.raw_text, block.raw_hash, prev_hash,
             block.source, block.timestamp, json.dumps({}), block.ttl_seconds)
        )
        self.db.commit()
        return block.block_id
    
    def get(self, block_id: str) -> InputBlock:
        """Read-only. Devuelve el bloque tal cual fue creado."""
        row = self.db.execute("SELECT * FROM input_blocks WHERE block_id = ?", (block_id,)).fetchone()
        return InputBlock(*row) if row else None
    
    def verify_chain(self) -> bool:
        """Verifica la integridad de toda la cadena."""
        rows = self.db.execute("SELECT * FROM input_blocks ORDER BY timestamp ASC").fetchall()
        prev_hash = "0" * 64
        for row in rows:
            if row[2] != hashlib.sha256(row[1].encode()).hexdigest():
                return False  # texto fue modificado
            if row[3] != prev_hash:
                return False  # chain rota
            prev_hash = row[2]
        return True
```

### 3.4 Visualización en la interface (HTML)

```html
<!-- Input Pinned Bar (siempre visible arriba del chat) -->
<div class="input-pinned-bar" id="inputPinnedBar">
  <div class="input-pinned-header">
    <span class="lock-icon">🔒</span>
    <span class="input-source">user · 03:14:23</span>
    <button onclick="expandInput()">Ver literal</button>
  </div>
  <div class="input-pinned-text" id="inputPinnedText">
    me haces un documento MD de todo lo que conseguiste sobre el input block...
  </div>
  <div class="input-pinned-tags">
    <span class="tag">instruction</span>
    <span class="tag">task</span>
  </div>
</div>

<!-- Modal de confirmación "input received" -->
<div class="modal" id="inputReceivedModal" role="dialog" aria-modal="true">
  <div class="modal-content">
    <h2>📥 Input recibido</h2>
    <p>El sistema leyó literal tu instrucción:</p>
    <pre class="literal-text">me haces un documento MD de todo lo que conseguiste...</pre>
    <p><strong>Análisis automático:</strong></p>
    <ul>
      <li>2 oraciones detectadas (L1, L2)</li>
      <li>2 instrucciones</li>
      <li>0 ambigüedades</li>
      <li>Tags: instruction, task</li>
    </ul>
    <button onclick="confirmInput()">OK, continuar</button>
  </div>
</div>
```

---

## 4) CONEXIÓN CON LAS 70 IDEAS + 25 DECISIONES YA APROBADAS

**Del BLOQUE 1 (70 ideas):**
- Idea #1 (kernel pequeño) → el `InputBlockHook` vive en el kernel, ~50 LOC
- Idea #18 (solo summary al parent) → el input block muestra summary arriba, full text expandible
- Idea #34 (retention prune-over-append) → TTL 90 días para input blocks
- Idea #55 (TTL 90d WARM) → mismo TTL para los input blocks
- Idea #40 (provenance tracking) → cada input block tiene source + agent_id
- Idea #60 (idempotency keys) → cada input block tiene block_id único

**De las 25 decisiones:**
- D1 (kernel pequeño) → el input block reader es parte del kernel, no plugin
- D9 (SQLite-first) → InputBlockStore usa SQLite WAL
- D11 (vault = filesystem) → backup de input blocks a `vault/input_blocks/`
- D16 (90 días TTL) → TTL configurable por input block
- D19 (token cost awareness) → el input block se prepende UNA vez, no se repite
- D20 (estética Claude/Anthropic) → pinned bar con estética exacta de las fotos

---

## 5) MÉTRICAS DE ÉXITO

- [ ] 100% de inputs que llegan al Osquestador pasan por InputBlockReader
- [ ] 0% de inputs son ejecutados sin haber sido leídos literal
- [ ] Hash chain verificable 100% del tiempo
- [ ] Latencia del análisis < 100ms para inputs < 10K chars
- [ ] TTL configurado por input, default 90 días
- [ ] Pinned bar visible en el 100% de las sesiones de chat
- [ ] Modal de confirmación aparece para inputs críticos
- [ ] Routing button funcional para los 9 puntos de la interface
- [ ] Audit log completo exportable a CSV/JSON

---

**PRÓXIMO PASO:** Investigación de los 9 puntos de la interface (10 pasadas código fuente + 10 comunidad devs cada uno) — Bloque 2 de la tarea de Max.

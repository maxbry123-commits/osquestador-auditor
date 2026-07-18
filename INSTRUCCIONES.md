# INSTRUCCIONES.md — Despliegue del `osquestador-auditor`

**Versión:** v1.0 · **Fecha:** 2026-07-17 · **Modo:** SHERIFF v8.2 STRICT

---

## 1. Prerrequisitos (verificar antes de empezar)

```bash
# VPS Ubuntu 22.04+ o Debian 12
ssh root@95.111.232.89 "uname -a"     # debe responder

# Herramientas locales
which ssh sshpass git curl wrangler python3

# Credenciales (NO en repo)
- GitHub PAT: scope `repo` (https://github.com/settings/tokens)
- Cloudflare API token: scope `Pages:Edit`
```

**Regla dura:** el VPS de Max **NO** debe tocarse en `/opt/nct/agents/*`, `/opt/nct/secrets/`, `/opt/nct/keep/`, ni en `/etc/systemd/system/openclaw*`.

---

## 2. Setup inicial (una vez)

```bash
# 2.1 Clonar el repo en una carpeta NUEVA del VPS (NO en /opt/nct)
ssh root@95.111.232.89
mkdir -p /root/osquestador
cd /root/osquestador
git clone https://github.com/maxbry123-commits/osquestador-auditor.git .
```

```bash
# 2.2 Instalar dependencias del orquestador
pip install requests pyyaml
```

```bash
# 2.3 Verificar aislamiento (NO toca OpenClaw)
ss -tlnp | grep 18789   # debe mostrar node escuchando
```

---

## 3. Ensamblar el código del Orquestador

```bash
# 3.1 Copiar la Parte A (núcleo)
mkdir -p orchestrator/base orchestrator/store orchestrator/kernel
cp docs/fuente/02_PARTE_A_NUCLEO.md /tmp/parte_a.md
# Extraer los 4 archivos de la parte A a sus rutas
# orchestrator/base/contracts.py
# orchestrator/base/resilience.py
# orchestrator/store/db.py
# orchestrator/kernel/{core,motor,managers,commands}.py
```

```bash
# 3.2 Copiar la Parte B (plugins)
# orchestrator/inputs/{inbox,telegram}/...
# orchestrator/outputs/{obsidian,kanboard,graphiti,telegram_notify,handoff}/...
# orchestrator/agents/{ocr,haystack,auditor,arbolista,plandex,hermes,swe,persistir}/...
# orchestrator/workflows/{01..04}.json
```

```bash
# 3.3 Copiar la Parte C (MCP + tools)
# orchestrator/mcp/{server,client}.py
# orchestrator/tools/{check_kernel_isolation,scaffold}.py
```

```bash
# 3.4 Aplicar la NOTA DE INTEGRACIÓN de Parte C (1 línea en motor.py)
# Reemplazar la línea de ctx_doc para incluir edges, nombre, contenido del ctx.
```

```bash
# 3.5 Verificar aislamiento del kernel
python3 orchestrator/tools/check_kernel_isolation.py
# Esperado: "kernel limpio ✓"
```

---

## 4. Configurar (opcional, sin credenciales funciona en modo local)

```bash
# 4.1 Crear config.json (se autogenera al primer arranque)
cat > orchestrator/config.json <<'EOF'
{
  "mode": "prod",
  "poll_seconds": 10,
  "telegram": {"token": "", "chat_id": ""},
  "kanboard": {"url": "http://127.0.0.1:8080/jsonrpc.php", "user": "jsonrpc", "token": "", "project_id": 1},
  "graphiti": {"mcp_url": ""},
  "obsidian": {"vault_path": ""},
  "mcp_server": {"enabled": true, "port": 8765},
  "similitud_duplicado": 0.98,
  "similitud_version": 0.70
}
EOF
```

**Sin credenciales:** inbox + vault + grafo/kanban locales funcionan OK. Telegram/Kanboard/Graphiti/Obsidian reales se activan solos al llenar las credenciales (sin tocar código).

---

## 5. Arrancar el orquestador

```bash
# 5.1 Modo local (sin credenciales externas)
cd /root/osquestador
python3 -m orchestrator
# Arranca el loop, escucha MCP en 127.0.0.1:8765
```

```bash
# 5.2 Verificar health
cat orchestrator/state/health.json
# Esperado: {"ts":"...", "status":"alive", "step":"idle"}
```

```bash
# 5.3 Probar MCP server
curl -X POST http://127.0.0.1:8765 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
# Esperado: lista de 4 tools
```

---

## 6. Memoria avanzada

```bash
# 6.1 Crear la estructura
mkdir -p ~/.osquestador/memoria/{episodica,semantica,procedimiento/skills,procedimiento/workflows,procedimiento/recovery,indice}
```

```bash
# 6.2 Inicializar el índice RAG (Fase 1, requiere sentence-transformers + faiss)
pip install sentence-transformers faiss-cpu
python3 -c "
from sentence_transformers import SentenceTransformer
import faiss, numpy as np
m = SentenceTransformer('all-MiniLM-L6-v2')
idx = faiss.IndexFlatL2(384)
faiss.write_index(idx, '/root/.osquestador/memoria/semantica/faiss.index')
print('RAG inicializado OK')
"
```

```bash
# 6.3 Backup diario (cron)
crontab -l 2>/dev/null | { cat; echo "0 3 * * * tar czf /backup/memoria-\$(date +\\%F).tgz ~/.osquestador/memoria 2>/dev/null"; } | crontab -
```

---

## 7. Panel UI (deploy a Cloudflare Pages)

```bash
# 7.1 Crear el panel
mkdir -p panel
# (el panel se construye con la skill SKILL_panel_ui.md)
# panel/index.html (vanilla HTML/CSS/JS con la paleta Anthropic)
```

```bash
# 7.2 Deploy
export CLOUDFLARE_API_TOKEN="cfat_..."
wrangler pages deploy panel --project-name=osquestador-panel
# URL: https://osquestador-panel.pages.dev
```

---

## 8. systemd (opcional, recomendado para producción)

```bash
cat > /etc/systemd/system/osquestador.service <<'EOF'
[Unit]
Description=Osquestador Auditor
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/osquestador
ExecStart=/usr/bin/python3 -m orchestrator
Restart=always
RestartSec=5
KillSignal=SIGTERM
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable --now osquestador
systemctl status osquestador
journalctl -u osquestador -f
```

**REGLA:** este servicio **NO** se llama `openclaw*`. Va en `/etc/systemd/system/osquestador.service`. No tocar `openclaw-gateway.service` ni similares.

---

## 9. Verificación end-to-end

```bash
# 9.1 Health
cat /root/osquestador/orchestrator/state/health.json
# Esperado: alive, idle

# 9.2 OpenClaw intacto
ss -tlnp | grep 18789
# Esperado: node 18789 (sin cambios)

# 9.3 MCP server
curl -X POST http://127.0.0.1:8765 \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/list","params":{}}'
# Esperado: 4 tools

# 9.4 Smoke test del orquestador
mkdir -p /root/osquestador/orchestrator/inbox/test
echo "# Test

objetivo: validar Fase 0
decision: usar SQLite WAL
https://github.com/maxbry123-commits/osquestador-auditor" > /root/osquestador/orchestrator/inbox/test/SMOKE.md

# Esperar 1 ciclo de poll (10s)
sleep 12
sqlite3 /root/osquestador/orchestrator/state/state.db \
  "SELECT nombre, estado FROM inventory WHERE proyecto='test'"
# Esperado: SMOKE.md en estado "auditado" o "conflicto"
```

---

## 10. Comandos útiles (del Orquestador, vía Telegram si está configurado)

```
/estado              → "📊 Docs: N | Conflictos abiertos: M"
/conflictos          → lista de conflictos con similitud
/resolver <id> A|B|FUSION
/frontera <proyecto> → "✅ FRONTERA OK" o "⏳ Pendiente"
/handoff <proyecto>  → exporta paquete a handoff/<proyecto>/
```

---

## 11. Troubleshooting

| Problema | Causa | Solución |
|----------|-------|----------|
| `EADDRINUSE 18789` | OpenClaw ya escucha ese puerto | El orquestador NO usa ese puerto. MCP server usa 8765. |
| `kernel污染` en linter | El kernel importa un plugin | Mover la importación al manager correspondiente. |
| MCP server no responde | Firewall | `ufw allow 8765` o usar tunnel. |
| `INVENTORY vacía` | Docs no están en `inbox/<proyecto>/` | Verificar formato `<proyecto>/<archivo>`. |
| OpenClaw modificado por error | Regla violada | Revertir con `git -C /opt/nct checkout .` o restaurar backup. |

---

## 12. Reglas duras (resumen)

- **OpenClaw = INTACTO**. Prohibido modificar, instalar encima, alterar config, usar como workspace.
- **Trabajo ocurre en `/root/osquestador/`**. NO en `/opt/nct/`.
- **NO construir sin investigación documentada** (ver `INVESTIGACION.md`).
- **NO certificar sin evidencia medible** (ver `SKILL_evidence_collect.md`).
- **NO claim PASS sin checkpoint + log + estado en `state.json`**.

---

## Versión
v1.0 — 2026-07-17 · Mavis.

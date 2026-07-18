# SALIDA 3 — INSTRUCCIONES PARA CLAUDE CODE
## Despliegue completo Fase 0 en VPS + GitHub (leer literal, ejecutar en orden)

**Rol de Claude Code aquí:** ejecutar, conectar, validar. NO rediseñar. El orquestador ya está escrito (SALIDA_2_v2 A/B/C). Cada paso termina con verificación — si falla, detenerse y reportar, nunca continuar.

---

## PASO 0 — Prerequisitos (evidencia requerida antes de empezar)
- VPS provisionado (Hetzner, según decisión cerrada del proyecto). Evidencia: `ssh root@IP "uname -a"` responde.
- Ubuntu 22.04+ o Debian 12.
- Dominio opcional (no bloqueante para Fase 0).

## PASO 1 — Base del sistema
```bash
apt update && apt upgrade -y
apt install -y python3 python3-pip python3-venv git docker.io docker-compose-plugin sqlite3 ufw
systemctl enable --now docker
ufw allow OpenSSH && ufw allow 80 && ufw allow 443 && ufw enable
```
**Verificar:** `docker --version && python3 --version && sqlite3 --version` — los 3 responden.

## PASO 2 — Estructura de repos en GitHub
Crear 2 repos (dentro de la organización/cuenta del proyecto):
1. `orchestrator-core` — el paquete completo de SALIDA_2_v2 (partes A+B+C ensambladas).
2. `fase0-projects` — carpeta por proyecto del usuario (vault/handoff versionados).

```bash
mkdir -p /opt/nct && cd /opt/nct
git clone git@github.com:<ORG>/orchestrator-core.git
git clone git@github.com:<ORG>/fase0-projects.git
```
**Ensamblaje:** copiar cada bloque de código de los 3 MD (A/B/C) a su ruta exacta del árbol declarado en Parte C. Aplicar la NOTA DE INTEGRACIÓN de Parte C (1 línea en `kernel/motor.py`).
**Verificar:** `python3 orchestrator/tools/check_kernel_isolation.py` → "kernel limpio".

## PASO 3 — Kanboard (Task Index P2)
```bash
mkdir -p /opt/nct/kanboard && cd /opt/nct/kanboard
cat > docker-compose.yml <<'EOF'
services:
  kanboard:
    image: kanboard/kanboard:latest
    ports: ["8080:80"]
    volumes: ["kanboard_data:/var/www/app/data"]
    restart: unless-stopped
volumes: { kanboard_data: }
EOF
docker compose up -d
```
- Abrir `http://IP:8080` → login admin/admin → cambiar contraseña.
- Crear proyecto "Fase0" → Settings → API → copiar token.
**Verificar:** `curl -u "jsonrpc:TOKEN" -d '{"jsonrpc":"2.0","method":"getVersion","id":1}' http://IP:8080/jsonrpc.php` responde versión.

## PASO 4 — Graphiti (memoria P1)
```bash
mkdir -p /opt/nct/graphiti && cd /opt/nct/graphiti
# Graphiti requiere Neo4j como backend
cat > docker-compose.yml <<'EOF'
services:
  neo4j:
    image: neo4j:5
    environment: ["NEO4J_AUTH=neo4j/CAMBIAR_PASSWORD"]
    ports: ["7687:7687","7474:7474"]
    volumes: ["neo4j_data:/data"]
    restart: unless-stopped
volumes: { neo4j_data: }
EOF
docker compose up -d
pip install graphiti-core --break-system-packages
```
- Levantar el servidor MCP de Graphiti (repo oficial getzep/graphiti, carpeta mcp_server) apuntando a ese Neo4j. Anotar URL (ej. `http://127.0.0.1:8000`).
**Verificar:** endpoint MCP responde a `tools/list`.
**Nota:** si Graphiti MCP no está disponible el día del despliegue, NO bloquear — el orquestador cae a grafo local (`state/graph.json`) automáticamente. Registrar como pendiente.

## PASO 5 — Obsidian (documentación P1)
Sin app en el VPS: el vault es la carpeta `orchestrator/vault/` (ya lo maneja el conector). Para ver/editar desde iPad:
```bash
# Sincronización del vault con el repo de proyectos
cd /opt/nct/orchestrator-core
ln -s /opt/nct/fase0-projects/vault vault 2>/dev/null || true
# cron: commit+push del vault cada 15 min
crontab -l 2>/dev/null | { cat; echo "*/15 * * * * cd /opt/nct/fase0-projects && git add -A && git commit -m auto-sync -q || true && git push -q"; } | crontab -
```
El usuario abre el vault en Obsidian iPad vía el repo (Working Copy u Obsidian Git).
**Verificar:** crear archivo de prueba en vault → aparece en GitHub en ≤15 min.

## PASO 6 — Telegram (entrada + comandos + notificaciones)
1. Crear bot con @BotFather → token.
2. Obtener chat_id: enviar mensaje al bot y `curl https://api.telegram.org/bot<TOKEN>/getUpdates` → `chat.id`.
3. Llenar `orchestrator/config.json`:
```json
{
  "mode": "prod", "poll_seconds": 10,
  "telegram": {"token": "<TOKEN>", "chat_id": "<CHAT_ID>"},
  "kanboard": {"url": "http://127.0.0.1:8080/jsonrpc.php", "user": "jsonrpc", "token": "<KB_TOKEN>", "project_id": 1},
  "graphiti": {"mcp_url": "http://127.0.0.1:8000"},
  "obsidian": {"vault_path": "/opt/nct/fase0-projects/vault"},
  "mcp_server": {"enabled": true, "port": 8765},
  "similitud_duplicado": 0.98, "similitud_version": 0.70
}
```
**Verificar:** enviar `/estado` al bot tras el Paso 8 → responde.

## PASO 7 — OCR real (HF19/20 o Baidu)
El agente `ocr` builtin marca binarios `requiere_ocr=true`. Conectar OCR real:
1. `python3 orchestrator/tools/scaffold.py agent ocr_remoto`
2. Implementar `agents/ocr_remoto/adapter.py`: POST del binario al endpoint HF Space OCR (HF19/HF20 del proyecto NCT) o API Baidu → devolver `{"texto": ..., "requiere_ocr": false}`.
3. En `agents/ocr_remoto/manifest.json`: `"capabilities": ["ocr"], "priority": 0` (prioridad 0 = va primero; builtin queda como fallback).
**Verificar:** subir un PDF a `inbox/test/` → aparece su texto en `vault/test/`.

## PASO 8 — Servicio systemd (orquestador 24/7)
```bash
cat > /etc/systemd/system/orchestrator.service <<'EOF'
[Unit]
Description=Orquestador Fase 0
After=network.target docker.service
[Service]
WorkingDirectory=/opt/nct/orchestrator-core
ExecStart=/usr/bin/python3 -m orchestrator
Restart=always
RestartSec=5
KillSignal=SIGTERM
TimeoutStopSec=30
[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload && systemctl enable --now orchestrator
```
**Verificar:** `systemctl status orchestrator` = active; `cat /opt/nct/orchestrator-core/state/health.json` = alive; `journalctl -u orchestrator -n 20` sin errores.

## PASO 9 — Prueba de humo (criterio MVP de Salida 2)
1. `mkdir -p inbox/prueba` y copiar 3 .md de prueba (2 similares, 1 distinto).
2. Esperar 1 ciclo → verificar: `sqlite3 state/state.db "select nombre,estado from inventory"` → 1 conflicto detectado.
3. Telegram: `/conflictos` → aparece; `/resolver <id> A` → responde ✅.
4. `/frontera prueba` → FRONTERA OK; `/handoff prueba` → `handoff/prueba/handoff.json` existe.
5. Kanboard UI: tareas DEFINIR visibles.
**Si los 5 puntos pasan → Fase 0 operativa.** Solo entonces subir los 50 documentos reales.

## PASO 10 — Registro final
- Commit de todo a `orchestrator-core` (tag `v2.0-fase0`).
- Reportar al Director: evidencia de cada verificación (outputs literales de los comandos).
- Actualizar checklist del proyecto NCT: C1=SÍ (VPS), Fase 0=OPERATIVA. C2/C3 (MCP Gateway global, Claude Code en VPS) siguen siendo tareas de la estructura NCT, fuera del alcance de este documento.

## PROHIBICIONES (phase0.policy)
- No ejecutar código de proyectos del usuario.
- No invocar el DSL de 15 nodos (Fase 1).
- No hacer push a repos de proyectos, salvo el auto-sync del vault definido en Paso 5.

# REGLAS_DURAS.md — `osquestador-auditor`

**Reglas absolutas del proyecto. CERO excepciones.**

---

## 🚫 REGLA #0 — OPENCLAW INTACTO

**PROHIBIDO TOCAR OPENCLAW — CERO EXCEPCIONES.**

Confirmado por el usuario (Max) en la sesión `418434919792827` el 2026-07-18.

Esto aplica a TODO el pipeline, en cualquier fase, en cualquier momento, sin importar la urgencia, el gap, o el número de iteraciones:

- ❌ PROHIBIDO modificar archivos en `/opt/nct/agents/*` (OpenClaw, swe-agent, mimo, ocr-remoto, etc.).
- ❌ PROHIBIDO instalar nada encima de OpenClaw.
- ❌ PROHIBIDO alterar la configuración de OpenClaw (`/root/.openclaw/openclaw.json` o similar).
- ❌ PROHIBIDO usar OpenClaw como workspace, sandbox, o directorio de trabajo del orquestador.
- ❌ PROHIBIDO cambiar tokens, API keys, o el model selector default de OpenClaw.
- ❌ PROHIBIDO tocar systemd units de OpenClaw (`openclaw-gateway.service` o similares).
- ❌ PROHIBIDO clonar/repo el código de OpenClaw (es npm package, no hay repo público de todas formas).
- ❌ PROHIBIDO conectarse al WebSocket de OpenClaw desde el orquestador o el panel.

**Todo el trabajo del `osquestador-auditor` ocurre en `/root/osquestador/` (carpeta NUEVA, separada, NO en `/opt/nct/`).**

**Antes de CUALQUIER despliegue en VPS** se ejecuta el check de seguridad:
```bash
ss -tlnp | grep 18789  # debe seguir mostrando node escuchando (OpenClaw intacto)
```

Si el check falla → STOP, NO continuar, reportar a Max.

---

## Otras reglas duras

- **NO construir sin investigación documentada** (ver `INVESTIGACION.md`).
- **NO certificar sin evidencia medible** (ver `SKILL_evidence_collect.md`).
- **NO claim PASS sin checkpoint + log + estado en `state.json`**.
- **NO inventar dependencias** (escaladas, no fake).
- **NO copiar funciones de UI ajena** (router viejo, Claude.ai, etc.).
- **NO borrar** bitácora, historial, checkpoints ni state.

---

**Firmado:** Mavis · 2026-07-18 · Sesión `418434919792827`
**Aprobado por:** Max (vía mensaje en chat)

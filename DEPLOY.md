# DEPLOY.md — Deploy strategy

## Architecture (per Max's instruction)

```
GitHub (source of truth) → VPS (ephemeral bridge + tunnel) → Cloudflare / Vercel / Railway / HuggingFace (public)
```

**VPS role**: ONLY
- Bridge: tunnel cloudflared runs here
- Temp memory: in-memory state during tunnel lifetime
- Ephemeral: dies = lose tunnel URL = re-run `tunnel.sh` from GitHub

**Nothing persistent on VPS**:
- No DB writes counted as "real" (SQLite regenerated on each start)
- No `__pycache__` commits
- No `.env` files
- No config beyond `tunnel.sh` + `watchdog.sh` + `start.sh`

## Deployment options

### Option A: Cloudflare Tunnel (current, works NOW)
- URL: https://firewall-expired-cycling-apparently.trycloudflare.com
- VPS runs `tunnel.sh` (infinite reconnect) + `watchdog.sh` (30s health check)
- Time-limit: 24h (URL changes, service stays up via reconnect)

### Option B: Render.com (production, persistent URL)
1. Connect GitHub repo: `maxbry123-commits/osquestador-auditor`
2. Render auto-detects `render.yaml`
3. Auto-deploy on every push to `main`
4. Persistent URL: `osquestador-auditor.onrender.com`
5. CI: GitHub Actions runs tests first

### Option C: Railway
1. Connect GitHub repo
2. Railway auto-detects `railway.json`
3. Dockerfile-based build
4. Persistent URL

### Option D: Vercel
- Frontend only (static SPA)
- Backend stays on Render/Railway
- Update `frontend/vite.config.js` proxy to point at backend URL

### Option E: HuggingFace Spaces
- Docker-based, persistent URL
- Free tier supports FastAPI

## VPS bridge recovery (if VPS dies)

```bash
# 1. Clone from GitHub (source of truth)
git clone https://github.com/maxbry123-commits/osquestador-auditor.git
cd osquestador-auditor

# 2. Install Python deps
pip install -r backend/requirements.txt

# 3. Install cloudflared
curl -sSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared
chmod +x /usr/local/bin/cloudflared

# 4. Start backend
bash start.sh &

# 5. Start tunnel (infinite reconnect)
bash tunnel.sh &

# 6. Start watchdog (auto-recovery)
bash watchdog.sh &

# 7. Get new URL from /tmp/cf-persistent.log
grep "https://.*trycloudflare" /tmp/cf-persistent.log | tail -1
```

## REGLA #0: OpenClaw INTACTO
- Sentinel at `/root/.osquestador/openclaw/SENTINEL.txt`
- Watchdog plugin verifies every 5 min via APScheduler
- Never modified by this project

## Open ports required on VPS
- 8000 (FastAPI backend) — internal only
- cloudflared creates outbound tunnel — no inbound needed

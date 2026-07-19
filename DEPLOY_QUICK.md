# Deploy from scratch on any VPS (Max's bridge pattern)

```bash
# 1. Clone source of truth
git clone https://github.com/maxbry123-commits/osquestador-auditor.git
cd osquestador-auditor

# 2. Python deps
pip install -r backend/requirements.txt

# 3. Cloudflared
curl -sSL https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /usr/local/bin/cloudflared && chmod +x /usr/local/bin/cloudflared

# 4. OpenClaw sentinel (REGLA #0)
mkdir -p /root/.osquestador/openclaw
echo "OpenClaw INTACTO" > /root/.osquestador/openclaw/SENTINEL.txt
chmod 444 /root/.osquestador/openclaw/SENTINEL.txt

# 5. Start bridge (3 services)
nohup bash start.sh > /tmp/backend.log 2>&1 &
nohup bash tunnel.sh > /dev/null 2>&1 &
nohup bash watchdog.sh > /dev/null 2>&1 &

# 6. Get public URL
sleep 15 && grep -oE "https://[a-z0-9-]+\.trycloudflare\.com" /tmp/cf-persistent.log | head -1
```

**Total time**: 3-5 minutes from clean VPS to public URL.
**Persistent state**: GitHub (everything). VPS is ephemeral.

#!/bin/bash
# Watchdog: ensures backend + cloudflared are always running
LOG="/tmp/watchdog.log"
> "$LOG"
while true; do
  # Check backend
  if ! curl -s --max-time 3 http://127.0.0.1:8000/api/health > /dev/null 2>&1; then
    echo "[watchdog] $(date) backend DOWN, restarting..." >> "$LOG"
    pkill -9 -f "uvicorn osquestador" 2>/dev/null
    sleep 2
    nohup /workspace/osquestador-auditor/start.sh > /tmp/backend.log 2>&1 &
    disown
  fi
  # Check tunnel
  if ! pgrep -f "cloudflared tunnel" > /dev/null 2>&1; then
    echo "[watchdog] $(date) cloudflared DOWN, restarting..." >> "$LOG"
    pkill -9 -f cloudflared 2>/dev/null
    sleep 2
    nohup /workspace/osquestador-auditor/tunnel.sh > /dev/null 2>&1 &
    disown
  fi
  # Reap zombies
  ps -eo pid,ppid,stat,cmd | awk '$3 ~ /Z/ {print $1}' | xargs -r kill -9 2>/dev/null
  sleep 30
done

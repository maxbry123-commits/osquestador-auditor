#!/bin/bash
# Persistent cloudflared tunnel with auto-reconnect
# This script runs in an infinite loop, restarting cloudflared on exit.
# Each new connection gets a fresh trycloudflare.com URL.
TUNNEL_LOG="/tmp/cf-persistent.log"
> "$TUNNEL_LOG"
echo "[tunnel] $(date) starting persistent cloudflared..." >> "$TUNNEL_LOG"
while true; do
  cloudflared tunnel --url http://127.0.0.1:8000 --no-autoupdate >> "$TUNNEL_LOG" 2>&1
  EXIT=$?
  echo "[tunnel] $(date) cloudflared exited code=$EXIT, restarting in 3s..." >> "$TUNNEL_LOG"
  sleep 3
done

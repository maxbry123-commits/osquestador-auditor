#!/bin/bash
# Start script para osquestador-auditor backend
pkill -9 -f "uvicorn osquestador" 2>/dev/null
sleep 1
cd /workspace/osquestador-auditor/backend
exec python3 -m uvicorn osquestador.db:app --host 0.0.0.0 --port 8000 --log-level info

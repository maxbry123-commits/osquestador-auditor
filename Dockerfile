# Multi-stage Dockerfile for osquestador-auditor
# Stage 1: builder
FROM python:3.11-slim AS builder
WORKDIR /app

# Install build deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps in a venv
RUN python -m venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Stage 2: runtime
FROM python:3.11-slim
WORKDIR /app

# Install tini for proper signal handling
RUN apt-get update && apt-get install -y --no-install-recommends tini \
    && rm -rf /var/lib/apt/lists/*

# Copy venv from builder
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

# Non-root user (UID 10001)
RUN useradd -m -u 10001 osquestador

# Copy app code
COPY backend/ /app/
COPY frontend/dist/ /app/frontend_dist/

# Ownership
RUN chown -R osquestador:osquestador /app

USER osquestador

# Environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    ALLOWED_ORIGINS=https://blog-searches-diabetes-father.trycloudflare.com

EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["uvicorn", "osquestador.db:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--log-level", "info"]
